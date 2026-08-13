#!/usr/bin/env python3
"""每日站点日报 —— 拉 GSC + GA4,渲染飞书卡片并投递。

手册见 memory/sources/daily-report.md。配置在 ~/.config/shark-agent/report.json(模板 scripts/report_targets.example.json)。

  python3 scripts/report_daily.py --dry-run          # 只打印,不发飞书
  python3 scripts/report_daily.py                    # 拉数 + 发飞书
  python3 scripts/report_daily.py --target partfit3d

设计原则:**永远要发出一条消息**。任何一段取数失败都降级成卡片里的一行告警,
而不是整个日报静默消失 —— 静默失败的定时任务等于没有定时任务。
"""

import argparse
import json
import os
import subprocess
import sys
import traceback
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ga4  # noqa: E402
import gsc  # noqa: E402
from _google import AuthExpired, access_token  # noqa: E402

# 配置放仓库外 —— 本仓库是 public,飞书 open_id 这类标识不能入库。
# 模板见 scripts/report_targets.example.json。
CONFIG_PATH = os.path.expanduser("~/.config/shark-agent/report.json")
EXAMPLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "report_targets.example.json")

GSC_LAG = gsc.DATA_LAG_DAYS   # 3
GA_LAG = ga4.DATA_LAG_DAYS    # 1
TOP_N = 5


# --------------------------------------------------------------------------
# 小工具
# --------------------------------------------------------------------------

def load_targets():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(
            f"没找到配置 {CONFIG_PATH}\n"
            f"照着模板建一份:cp {EXAMPLE_PATH} {CONFIG_PATH}\n"
            "然后填 lark.user_id(或 chat_id)和 ga4_property。"
        )
    with open(CONFIG_PATH) as f:
        return json.load(f)


def md(day):
    return f"{day.month}-{day.day}"


def num(v):
    v = float(v)
    return f"{v:,.0f}" if v.is_integer() else f"{v:,.1f}"


def delta(cur, prev, unit="", comparable=True):
    """把「本期 vs 上期」渲染成 `21 → 25 (▲19.0%)`。

    `comparable=False` 时**不给百分比** —— 上期窗口里有若干天根本没数据
    (站点刚上线、GA4 property 刚建),此时的变化率是纯噪音。
    2026-08-11 实测:partfit3d 的"前 7 天"只有 2 天有数据,算出来是 ▲872%,
    看着像爆发,其实只是基线缺了 5 天。
    """
    cur, prev = float(cur), float(prev)
    body = f"{num(prev)} → {num(cur)}{unit}"
    if not comparable:
        return body + " (基线不完整,变化率不可信)"
    if prev == 0:
        return body + (" (新增)" if cur > 0 else "")
    pct = (cur - prev) / prev * 100
    arrow = "▲" if pct > 0 else ("▼" if pct < 0 else "＝")
    return f"{body} ({arrow}{abs(pct):.1f}%)"


def truncate(s, n=38):
    return s if len(s) <= n else s[: n - 1] + "…"


# --------------------------------------------------------------------------
# GSC 段
# --------------------------------------------------------------------------

def _agg_gsc(rows):
    """按曝光加权聚合一组按天的 GSC 行。position 是加权均值,不能直接取算术平均。"""
    clicks = sum(r["clicks"] for r in rows)
    impr = sum(r["impressions"] for r in rows)
    pos = (sum(r["position"] * r["impressions"] for r in rows) / impr) if impr else 0.0
    return {
        "clicks": clicks,
        "impressions": impr,
        "ctr": (clicks / impr) if impr else 0.0,
        "position": pos,
    }


def gsc_section(token, site):
    latest = date.today() - timedelta(days=GSC_LAG)
    start = latest - timedelta(days=13)  # 14 天 = 近 7 天 + 前 7 天

    by_day = gsc.search_analytics(
        token, site, ["date"], start.isoformat(), latest.isoformat(), 1000
    )
    rows = {r["keys"][0]: r for r in by_day}

    days = [(start + timedelta(days=i)) for i in range(14)]
    filled = [
        rows.get(d.isoformat(), {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0})
        for d in days
    ]
    prev7, last7 = _agg_gsc(filled[:7]), _agg_gsc(filled[7:])
    today_row = filled[-1]

    # 上期窗口有几天真有数据。缺天数 → 变化率没有意义,见 delta() 的注释。
    prev_covered = sum(1 for r in filled[:7] if r["impressions"] > 0)
    comparable = prev_covered == 7

    lines = [
        f"**{md(latest)}(GSC 回填延迟 {GSC_LAG} 天)**",
        f"点击 **{num(today_row['clicks'])}** ｜ 曝光 **{num(today_row['impressions'])}** "
        f"｜ CTR **{today_row['ctr'] * 100:.1f}%** ｜ 均位 **{today_row['position']:.1f}**",
        "",
        "近 7 天 vs 前 7 天",
        f"点击 {delta(last7['clicks'], prev7['clicks'], comparable=comparable)}",
        f"曝光 {delta(last7['impressions'], prev7['impressions'], comparable=comparable)}",
        f"CTR {prev7['ctr'] * 100:.2f}% → {last7['ctr'] * 100:.2f}% "
        f"｜ 均位 {prev7['position']:.1f} → {last7['position']:.1f}",
    ]
    if not comparable:
        lines.append(f"⚠️ 前 7 天只有 {prev_covered}/7 天有数据(站点刚起量),同比先别当真")

    queries = gsc.search_analytics(
        token, site, ["query"],
        (latest - timedelta(days=6)).isoformat(), latest.isoformat(), 25000
    )
    queries.sort(key=lambda r: (-r["clicks"], -r["impressions"]))
    if queries:
        lines += ["", f"**Top 词(近 7 天)**"]
        for r in queries[:TOP_N]:
            lines.append(
                f"· {truncate(r['keys'][0])} — {num(r['clicks'])} 点 / "
                f"{num(r['impressions'])} 曝 / 位 {r['position']:.1f}"
            )
    return "\n".join(lines)


# --------------------------------------------------------------------------
# GA4 段
# --------------------------------------------------------------------------

GA_METRICS = ["activeUsers", "newUsers", "sessions", "screenPageViews"]


# 后台/鉴权路径不是"内容表现",出现在 Top 页里只会掩盖真正有流量的页。
# 2026-08-11:/admin/depixelate 曾排到 partfit3d 浏览量第 2,实为自己点的。
DEFAULT_EXCLUDE_PATHS = ["/admin", "/auth", "/api", "/_"]


def ga_section(token, prop, exclude_paths=None):
    exclude_paths = exclude_paths or DEFAULT_EXCLUDE_PATHS
    y = date.today() - timedelta(days=GA_LAG)          # 昨天
    ybefore = y - timedelta(days=1)
    last7_start = y - timedelta(days=6)
    prev7_end = last7_start - timedelta(days=1)
    prev7_start = prev7_end - timedelta(days=6)

    # 一次按天拉 14 天,本地切窗口 —— 比分别打 4 次 runReport 省 3 次配额,
    # 也顺带拿到"上期有几天真有数据"这个判据。
    daily = ga4.run_report(
        token, prop, prev7_start.isoformat(), y.isoformat(),
        GA_METRICS, dimensions=["date"], limit=100,
    )
    by_day = {d[0]: v for d, v in daily}   # key 形如 "20260810"

    def day(d):
        return by_day.get(d.strftime("%Y%m%d"), {m: 0.0 for m in GA_METRICS})

    def span(a, b):
        out = {m: 0.0 for m in GA_METRICS}
        cur = a
        while cur <= b:
            for m in GA_METRICS:
                out[m] += day(cur)[m]
            cur += timedelta(days=1)
        return out

    t_y, t_yb = day(y), day(ybefore)
    t_l7 = span(last7_start, y)
    t_p7 = span(prev7_start, prev7_end)

    prev_covered = sum(
        1 for i in range(7)
        if day(prev7_start + timedelta(days=i))["sessions"] > 0
    )
    comparable = prev_covered == 7

    lines = [
        f"**{md(y)}(昨日)**",
        f"活跃用户 **{num(t_y['activeUsers'])}** ｜ 新用户 **{num(t_y['newUsers'])}** "
        f"｜ 会话 **{num(t_y['sessions'])}** ｜ 浏览量 **{num(t_y['screenPageViews'])}**",
        f"较前一日:活跃用户 {delta(t_y['activeUsers'], t_yb['activeUsers'])}",
        "",
        "近 7 天 vs 前 7 天",
        f"活跃用户 {delta(t_l7['activeUsers'], t_p7['activeUsers'], comparable=comparable)}",
        f"会话 {delta(t_l7['sessions'], t_p7['sessions'], comparable=comparable)}",
    ]
    if not comparable:
        lines.append(f"⚠️ 前 7 天只有 {prev_covered}/7 天有数据,同比先别当真")

    channels = ga4.run_report(
        token, prop, last7_start.isoformat(), y.isoformat(),
        ["sessions"], dimensions=["sessionDefaultChannelGroup"],
        limit=6, order_metric="sessions",
    )
    if channels:
        parts = [f"{d[0]} {num(v['sessions'])}" for d, v in channels]
        lines += ["", "**渠道(近 7 天会话)**", "｜ ".join(parts)]

    # 多取一些再本地筛,否则排除内部路径后不够 TOP_N 条。
    pages = ga4.run_report(
        token, prop, last7_start.isoformat(), y.isoformat(),
        ["screenPageViews"], dimensions=["pagePath"],
        limit=TOP_N * 4, order_metric="screenPageViews",
    )
    kept = [(d, v) for d, v in pages
            if not any(d[0].startswith(x) for x in exclude_paths)]
    hidden = len(pages) - len(kept)
    if kept:
        lines += ["", "**Top 页(近 7 天浏览量)**"]
        for d, v in kept[:TOP_N]:
            lines.append(f"· {truncate(d[0])} — {num(v['screenPageViews'])}")
        if hidden:
            lines.append(f"*(已隐藏 {hidden} 条内部路径)*")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# 卡片渲染
# --------------------------------------------------------------------------

def build_card(label, blocks, footer):
    elements = []
    for i, (title, body) in enumerate(blocks):
        if i:
            elements.append({"tag": "hr"})
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": f"**{title}**"}})
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": body}})
    elements.append({"tag": "hr"})
    elements.append({"tag": "note", "elements": [{"tag": "plain_text", "content": footer}]})
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📊 {label} 日报 · {date.today().isoformat()}"},
            "template": "blue",
        },
        "elements": elements,
    }


def card_to_text(card):
    """--dry-run 时的可读预览。"""
    out = [card["header"]["title"]["content"], ""]
    for el in card["elements"]:
        if el["tag"] == "hr":
            out.append("-" * 48)
        elif el["tag"] == "div":
            out.append(el["text"]["content"].replace("**", ""))
        elif el["tag"] == "note":
            out.append(el["elements"][0]["content"])
    return "\n".join(out)


# --------------------------------------------------------------------------
# 飞书投递
# --------------------------------------------------------------------------

def send_lark(card, lark_cfg):
    chat_id, user_id = lark_cfg.get("chat_id"), lark_cfg.get("user_id")
    if not (chat_id or user_id):
        sys.exit(f"{CONFIG_PATH} 里 lark.user_id 和 lark.chat_id 都是空的,没地方发。")
    dest = ["--chat-id", chat_id] if chat_id else ["--user-id", user_id]
    cmd = [
        "lark-cli", "im", "+messages-send", *dest,
        "--as", "bot",
        "--msg-type", "interactive",
        "--content", json.dumps(card, ensure_ascii=False),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"飞书投递失败(exit {res.returncode}):\n{res.stdout}\n{res.stderr}")
    return res.stdout.strip()


# --------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="每日 GSC + GA4 飞书日报")
    p.add_argument("--target", default="partfit3d", help="report.json 里 targets 的 key")
    p.add_argument("--dry-run", action="store_true", help="只打印,不发飞书")
    args = p.parse_args()

    cfg = load_targets()
    target = cfg["targets"].get(args.target)
    if not target:
        sys.exit(f"{CONFIG_PATH} 里没有 target {args.target!r};"
                 f"已有:{', '.join(cfg['targets'])}")

    blocks = []
    footer_bits = []

    try:
        token = access_token()
    except AuthExpired as e:
        # 凭证挂了也要发消息 —— 否则日报只是"没来",没人知道是坏了还是没数据。
        card = build_card(target["label"], [
            ("⚠️ Google 凭证失效", f"日报取不到数。\n```\n{e}\n```"),
        ], "shark-agent · report_daily.py")
        if args.dry_run:
            print(card_to_text(card))
        else:
            send_lark(card, cfg["lark"])
        sys.exit(1)

    try:
        blocks.append(("🔍 Google Search Console", gsc_section(token, target["gsc_site"])))
        footer_bits.append("GSC=自有真值")
    except Exception:
        blocks.append(("🔍 Google Search Console",
                       f"⚠️ 取数失败\n```\n{traceback.format_exc(limit=2).strip()}\n```"))

    prop = (target.get("ga4_property") or "").strip()
    if prop:
        try:
            blocks.append(("📈 Google Analytics 4",
                           ga_section(token, prop,
                                      target.get("ga4_exclude_paths"))))
            footer_bits.append(f"GA4 property {prop}")
        except Exception:
            blocks.append(("📈 Google Analytics 4",
                           f"⚠️ 取数失败\n```\n{traceback.format_exc(limit=2).strip()}\n```"))
    else:
        blocks.append(("📈 Google Analytics 4",
                       "未配置 property ID。跑 `python3 scripts/ga4.py props` 查到后"
                       "填进 `~/.config/shark-agent/report.json`。"))

    footer = " · ".join(["shark-agent report_daily.py"] + footer_bits)
    card = build_card(target["label"], blocks, footer)

    if args.dry_run:
        print(card_to_text(card))
        print("\n--- card json ---")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        return
    print(send_lark(card, cfg["lark"]))


if __name__ == "__main__":
    main()
