#!/usr/bin/env python3
"""Google Search Console 查询工具(零依赖,纯 stdlib)。

用法见 memory/sources/gsc.md。凭证存在仓库外:~/.config/shark-agent/google.json
(与 ga4.py 共用同一次授权,见 scripts/_google.py)

  python3 scripts/gsc.py auth                     # 一次性授权(同时覆盖 GA4)
  python3 scripts/gsc.py sites                    # 列出所有 property
  python3 scripts/gsc.py queries <site>           # 关键词级 点击/曝光/CTR/排名
  python3 scripts/gsc.py pages <site>             # 页面级
  python3 scripts/gsc.py ctr-losers <site>        # 排名够好但没人点的漏损点(按损失点击排序)
  python3 scripts/gsc.py compare <site> --before YYYY-MM-DD:YYYY-MM-DD --after ...
  python3 scripts/gsc.py inspect <site> <url>     # 单页收录状态
"""

import argparse
import csv
import json
import os
import sys
import urllib.parse
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _google import (  # noqa: E402
    SCOPES, access_token, api_call as _api_call, client_credentials_from_args,
    load_config, run_oauth_flow,
)

API_BASE = "https://searchconsole.googleapis.com"

# GSC 数据回填有延迟,默认窗口结束日往前推 3 天,避免拿到不完整的尾部数据。
DATA_LAG_DAYS = 3

# 位置 -> 该位置的经验平均 CTR。用于 ctr-losers 估算"本该拿到多少点击"。
# 数据是行业粗略均值,只用来排序漏损点,不要当精确基准。
EXPECTED_CTR = {
    1: 0.270, 2: 0.150, 3: 0.110, 4: 0.080, 5: 0.060,
    6: 0.049, 7: 0.040, 8: 0.034, 9: 0.030, 10: 0.026,
}
EXPECTED_CTR_11_20 = 0.013


# --------------------------------------------------------------------------
# 凭证与 OAuth(实现在 _google.py,与 ga4.py 共用同一次授权)
# --------------------------------------------------------------------------

def cmd_auth(args):
    client_id, client_secret = client_credentials_from_args(args)
    run_oauth_flow(client_id, client_secret, SCOPES)
    print("✅ 凭证已存到 ~/.config/shark-agent/google.json(权限 600)")
    print("   scope 覆盖 Search Console + Analytics,ga4.py 无需再授权一次。")
    print("下一步:python3 scripts/gsc.py sites")


# --------------------------------------------------------------------------
# API 调用
# --------------------------------------------------------------------------

def api_call(token, path, payload=None):
    return _api_call(token, API_BASE + path, payload)


def default_window(days):
    end = date.today() - timedelta(days=DATA_LAG_DAYS)
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


def search_analytics(token, site, dimensions, start, end, limit=100, filters=None):
    payload = {
        "startDate": start,
        "endDate": end,
        "dimensions": dimensions,
        "rowLimit": min(limit, 25000),
    }
    if filters:
        payload["dimensionFilterGroups"] = [{"filters": filters}]
    site_enc = urllib.parse.quote(site, safe="")
    res = api_call(token, f"/webmasters/v3/sites/{site_enc}/searchAnalytics/query", payload)
    return res.get("rows", [])


# --------------------------------------------------------------------------
# 输出
# --------------------------------------------------------------------------

def emit(rows, headers, fmt):
    if fmt == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if fmt == "csv":
        w = csv.writer(sys.stdout)
        w.writerow(headers)
        w.writerows(rows)
        return
    if not rows:
        print("(无数据)")
        return
    widths = [len(h) for h in headers]
    text = [[str(c) for c in r] for r in rows]
    for r in text:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(c))
    line = "  ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(line)
    print("-" * len(line))
    for r in text:
        print("  ".join(c.ljust(widths[i]) for i, c in enumerate(r)))


def expected_ctr(position):
    p = int(round(position))
    if p <= 0:
        return EXPECTED_CTR[1]
    if p in EXPECTED_CTR:
        return EXPECTED_CTR[p]
    if p <= 20:
        return EXPECTED_CTR_11_20
    return 0.005


# --------------------------------------------------------------------------
# 子命令
# --------------------------------------------------------------------------

def cmd_sites(args):
    token = access_token(load_config())
    res = api_call(token, "/webmasters/v3/sites")
    rows = [
        [s["siteUrl"], s.get("permissionLevel", "")]
        for s in res.get("siteEntry", [])
    ]
    emit(rows, ["siteUrl", "permission"], args.format)


def _dimension_report(args, dimension):
    token = access_token(load_config())
    start, end = (args.start, args.end) if args.start and args.end else default_window(args.days)
    rows = search_analytics(token, args.site, [dimension], start, end, args.limit)
    rows.sort(key=lambda r: -r["clicks"])
    out = [
        [
            r["keys"][0],
            r["clicks"],
            r["impressions"],
            f"{r['ctr'] * 100:.1f}%",
            f"{r['position']:.1f}",
        ]
        for r in rows
    ]
    if args.format == "table":
        print(f"# {args.site}  {start} ~ {end}  ({dimension})\n")
    emit(out, [dimension, "clicks", "impr", "ctr", "pos"], args.format)


def cmd_queries(args):
    _dimension_report(args, "query")


def cmd_pages(args):
    _dimension_report(args, "page")


def cmd_ctr_losers(args):
    """排名进了前 20、曝光够多、但 CTR 明显低于该位置经验值的词。

    输出按「预估损失点击」降序 —— 这就是改 title/meta 的优先级队列。
    """
    token = access_token(load_config())
    start, end = (args.start, args.end) if args.start and args.end else default_window(args.days)
    rows = search_analytics(token, args.site, ["query"], start, end, 25000)

    losers = []
    for r in rows:
        if r["impressions"] < args.min_impressions:
            continue
        if r["position"] > args.max_position:
            continue
        exp = expected_ctr(r["position"])
        if r["ctr"] >= exp * args.threshold:
            continue
        lost = r["impressions"] * (exp - r["ctr"])
        losers.append([
            r["keys"][0],
            r["impressions"],
            r["clicks"],
            f"{r['ctr'] * 100:.1f}%",
            f"{exp * 100:.1f}%",
            f"{r['position']:.1f}",
            f"{lost:.0f}",
        ])
    losers.sort(key=lambda x: -float(x[-1]))
    losers = losers[: args.limit]

    if args.format == "table":
        print(f"# {args.site}  {start} ~ {end}")
        print(f"# 筛选:曝光 ≥{args.min_impressions}、排名 ≤{args.max_position}、"
              f"CTR < 该位置经验值的 {args.threshold:.0%}")
        print("# lost = 预估损失点击(曝光 × CTR 差),按它排序就是改 title/meta 的优先级\n")
    emit(losers, ["query", "impr", "clicks", "ctr", "exp_ctr", "pos", "lost"], args.format)


def _parse_range(s, label):
    try:
        a, b = s.split(":")
        return a, b
    except ValueError:
        sys.exit(f"--{label} 格式应为 YYYY-MM-DD:YYYY-MM-DD,收到 {s!r}")


def cmd_compare(args):
    """改动前后对比。把同一个维度在两个时间窗的表现放一起看。"""
    token = access_token(load_config())
    b_start, b_end = _parse_range(args.before, "before")
    a_start, a_end = _parse_range(args.after, "after")

    before = {r["keys"][0]: r for r in
              search_analytics(token, args.site, [args.dimension], b_start, b_end, 25000)}
    after = {r["keys"][0]: r for r in
             search_analytics(token, args.site, [args.dimension], a_start, a_end, 25000)}

    out = []
    for key in set(before) | set(after):
        b = before.get(key)
        a = after.get(key)
        bc, ac = (b["clicks"] if b else 0), (a["clicks"] if a else 0)
        bi, ai = (b["impressions"] if b else 0), (a["impressions"] if a else 0)
        if max(bi, ai) < args.min_impressions:
            continue
        bp = f"{b['position']:.1f}" if b else "-"
        ap = f"{a['position']:.1f}" if a else "-"
        bctr = f"{b['ctr'] * 100:.1f}%" if b else "-"
        actr = f"{a['ctr'] * 100:.1f}%" if a else "-"
        out.append([key, bc, ac, ac - bc, bi, ai, bctr, actr, bp, ap])
    out.sort(key=lambda x: -abs(x[3]))
    out = out[: args.limit]

    if args.format == "table":
        print(f"# {args.site}  before {b_start}~{b_end}  →  after {a_start}~{a_end}\n")
    emit(out, [args.dimension, "clk_b", "clk_a", "Δclk",
               "impr_b", "impr_a", "ctr_b", "ctr_a", "pos_b", "pos_a"], args.format)


def cmd_inspect(args):
    """单页收录状态 —— 用来查「已发现-尚未编入索引」到底卡在哪。

    配额:每 property 每天 2000 次、每分钟 600 次。
    """
    token = access_token(load_config())
    res = api_call(token, "/v1/urlInspection/index:inspect", {
        "inspectionUrl": args.url,
        "siteUrl": args.site,
        "languageCode": "zh-CN",
    })
    idx = res.get("inspectionResult", {}).get("indexStatusResult", {})
    if args.format == "json":
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return
    rows = [
        ["verdict", idx.get("verdict", "-")],
        ["coverageState", idx.get("coverageState", "-")],
        ["robotsTxtState", idx.get("robotsTxtState", "-")],
        ["indexingState", idx.get("indexingState", "-")],
        ["lastCrawlTime", idx.get("lastCrawlTime", "-")],
        ["pageFetchState", idx.get("pageFetchState", "-")],
        ["googleCanonical", idx.get("googleCanonical", "-")],
        ["userCanonical", idx.get("userCanonical", "-")],
    ]
    emit(rows, ["field", "value"], args.format)


# --------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Google Search Console 查询工具")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp, with_window=True):
        sp.add_argument("--format", choices=["table", "json", "csv"], default="table")
        if with_window:
            sp.add_argument("--days", type=int, default=28, help="回看天数(默认 28)")
            sp.add_argument("--start", help="YYYY-MM-DD,与 --end 同时给则覆盖 --days")
            sp.add_argument("--end", help="YYYY-MM-DD")
            sp.add_argument("--limit", type=int, default=100)

    sp = sub.add_parser("auth", help="一次性 OAuth 授权")
    sp.add_argument("--client-secret-file", help="从 Google Cloud 下载的 client_secret json")
    sp.add_argument("--client-id")
    sp.add_argument("--client-secret")
    sp.set_defaults(func=cmd_auth)

    sp = sub.add_parser("sites", help="列出有权限的 property")
    add_common(sp, with_window=False)
    sp.set_defaults(func=cmd_sites)

    sp = sub.add_parser("queries", help="关键词级报表")
    sp.add_argument("site")
    add_common(sp)
    sp.set_defaults(func=cmd_queries)

    sp = sub.add_parser("pages", help="页面级报表")
    sp.add_argument("site")
    add_common(sp)
    sp.set_defaults(func=cmd_pages)

    sp = sub.add_parser("ctr-losers", help="排名够好但没人点的漏损点")
    sp.add_argument("site")
    sp.add_argument("--min-impressions", type=int, default=30)
    sp.add_argument("--max-position", type=float, default=20.0)
    sp.add_argument("--threshold", type=float, default=0.5,
                    help="低于该位置经验 CTR 的多少倍才算漏损(默认 0.5)")
    add_common(sp)
    sp.set_defaults(func=cmd_ctr_losers)

    sp = sub.add_parser("compare", help="改动前后两个时间窗对比")
    sp.add_argument("site")
    sp.add_argument("--before", required=True, help="YYYY-MM-DD:YYYY-MM-DD")
    sp.add_argument("--after", required=True, help="YYYY-MM-DD:YYYY-MM-DD")
    sp.add_argument("--dimension", choices=["query", "page"], default="query")
    sp.add_argument("--min-impressions", type=int, default=10)
    sp.add_argument("--limit", type=int, default=50)
    sp.add_argument("--format", choices=["table", "json", "csv"], default="table")
    sp.set_defaults(func=cmd_compare)

    sp = sub.add_parser("inspect", help="单页收录状态")
    sp.add_argument("site")
    sp.add_argument("url")
    sp.add_argument("--format", choices=["table", "json", "csv"], default="table")
    sp.set_defaults(func=cmd_inspect)

    args = p.parse_args()
    try:
        args.func(args)
    except (RuntimeError, OSError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
