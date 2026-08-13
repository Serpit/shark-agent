#!/usr/bin/env python3
"""Google Analytics 4 查询工具(零依赖,纯 stdlib)。

用法见 memory/sources/ga4.md。凭证与 gsc.py **共用**同一份 OAuth
(~/.config/shark-agent/google.json),不需要单独授权。

  python3 scripts/ga4.py props                    # 列出可访问的 GA4 property(拿 property ID)
  python3 scripts/ga4.py totals <prop> --days 7   # 汇总指标
  python3 scripts/ga4.py breakdown <prop> --dimension sessionDefaultChannelGroup
  python3 scripts/ga4.py pages <prop> --days 7    # 页面级(pagePath)

<prop> 传纯数字 property ID(如 123456789),也接受 `properties/123456789`。
"""

import argparse
import csv
import json
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _google import access_token, api_call  # noqa: E402

ADMIN_BASE = "https://analyticsadmin.googleapis.com/v1beta"
DATA_BASE = "https://analyticsdata.googleapis.com/v1beta"

# GA4 与 GSC 不同,**没有 3 天回填延迟** —— 昨天的数据当天就完整。
# 但「今天」仍在累积中,直接查会看起来像腰斩,所以默认窗口结束日 = 昨天。
DATA_LAG_DAYS = 1

DEFAULT_METRICS = ["activeUsers", "newUsers", "sessions", "screenPageViews"]


def normalize_property(prop):
    prop = str(prop).strip()
    return prop if prop.startswith("properties/") else f"properties/{prop}"


def default_window(days):
    end = date.today() - timedelta(days=DATA_LAG_DAYS)
    start = end - timedelta(days=days - 1)
    return start.isoformat(), end.isoformat()


# --------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------

def list_properties(token):
    """遍历 accountSummaries,返回 [(property_id, 账号名, property 名)]。"""
    out = []
    page = None
    while True:
        url = f"{ADMIN_BASE}/accountSummaries?pageSize=200"
        if page:
            url += f"&pageToken={page}"
        res = api_call(token, url)
        for acc in res.get("accountSummaries", []):
            for p in acc.get("propertySummaries", []):
                out.append((
                    p["property"].split("/")[-1],
                    acc.get("displayName", "-"),
                    p.get("displayName", "-"),
                ))
        page = res.get("nextPageToken")
        if not page:
            break
    return out


def run_report(token, prop, start, end, metrics, dimensions=None,
               limit=25, order_metric=None):
    """跑一次 runReport,返回 [(dim_values..., {metric: float})]。"""
    payload = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
        "keepEmptyRows": False,
    }
    if dimensions:
        payload["dimensions"] = [{"name": d} for d in dimensions]
    if order_metric:
        payload["orderBys"] = [
            {"metric": {"metricName": order_metric}, "desc": True}
        ]
    url = f"{DATA_BASE}/{normalize_property(prop)}:runReport"
    res = api_call(token, url, payload)

    rows = []
    for r in res.get("rows", []):
        dims = [d.get("value", "") for d in r.get("dimensionValues", [])]
        vals = {}
        for name, cell in zip(metrics, r.get("metricValues", [])):
            raw = cell.get("value", "0")
            try:
                vals[name] = float(raw)
            except ValueError:
                vals[name] = 0.0
        rows.append((dims, vals))
    return rows


def totals(token, prop, start, end, metrics=None):
    """无维度汇总。property 在窗口内没有任何数据时返回全 0,而不是报错。"""
    metrics = metrics or DEFAULT_METRICS
    rows = run_report(token, prop, start, end, metrics, limit=1)
    if not rows:
        return {m: 0.0 for m in metrics}
    return rows[0][1]


# --------------------------------------------------------------------------
# 输出(与 gsc.py 的 emit 保持同样的三种格式)
# --------------------------------------------------------------------------

def emit(rows, headers, fmt):
    if fmt == "json":
        print(json.dumps([dict(zip(headers, r)) for r in rows],
                         ensure_ascii=False, indent=2))
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


def fmt_num(v):
    return f"{v:.0f}" if float(v).is_integer() else f"{v:.2f}"


# --------------------------------------------------------------------------
# 子命令
# --------------------------------------------------------------------------

def cmd_props(args):
    token = access_token()
    rows = list_properties(token)
    if not rows:
        print("(没有可访问的 GA4 property —— 确认当前 Google 账号在 GA4 里有权限,"
              "且 GCP 项目已启用 Google Analytics Admin API)")
        return
    emit(rows, ["property_id", "account", "property"], args.format)


def cmd_totals(args):
    token = access_token()
    start, end = (args.start, args.end) if args.start and args.end else default_window(args.days)
    metrics = args.metrics.split(",") if args.metrics else DEFAULT_METRICS
    vals = totals(token, args.property, start, end, metrics)
    if args.format == "table":
        print(f"# property {args.property}  {start} ~ {end}\n")
    emit([[m, fmt_num(vals.get(m, 0))] for m in metrics], ["metric", "value"], args.format)


def _breakdown(args, dimension):
    token = access_token()
    start, end = (args.start, args.end) if args.start and args.end else default_window(args.days)
    metrics = args.metrics.split(",") if args.metrics else DEFAULT_METRICS
    rows = run_report(token, args.property, start, end, metrics,
                      dimensions=[dimension], limit=args.limit,
                      order_metric=metrics[0])
    out = [[d[0]] + [fmt_num(v.get(m, 0)) for m in metrics] for d, v in rows]
    if args.format == "table":
        print(f"# property {args.property}  {start} ~ {end}  ({dimension})\n")
    emit(out, [dimension] + metrics, args.format)


def cmd_breakdown(args):
    _breakdown(args, args.dimension)


def cmd_pages(args):
    _breakdown(args, "pagePath")


# --------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Google Analytics 4 查询工具")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_window(sp):
        sp.add_argument("--days", type=int, default=7, help="回看天数(默认 7)")
        sp.add_argument("--start", help="YYYY-MM-DD,与 --end 同时给则覆盖 --days")
        sp.add_argument("--end", help="YYYY-MM-DD")
        sp.add_argument("--metrics", help=f"逗号分隔(默认 {','.join(DEFAULT_METRICS)})")
        sp.add_argument("--limit", type=int, default=25)
        sp.add_argument("--format", choices=["table", "json", "csv"], default="table")

    sp = sub.add_parser("props", help="列出可访问的 GA4 property")
    sp.add_argument("--format", choices=["table", "json", "csv"], default="table")
    sp.set_defaults(func=cmd_props)

    sp = sub.add_parser("totals", help="窗口内汇总指标")
    sp.add_argument("property")
    add_window(sp)
    sp.set_defaults(func=cmd_totals)

    sp = sub.add_parser("breakdown", help="按任意维度拆分")
    sp.add_argument("property")
    sp.add_argument("--dimension", default="sessionDefaultChannelGroup")
    add_window(sp)
    sp.set_defaults(func=cmd_breakdown)

    sp = sub.add_parser("pages", help="页面级(pagePath)")
    sp.add_argument("property")
    add_window(sp)
    sp.set_defaults(func=cmd_pages)

    args = p.parse_args()
    try:
        args.func(args)
    except (RuntimeError, OSError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()
