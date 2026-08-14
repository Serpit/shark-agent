#!/usr/bin/env python3
"""外链台账归一化 —— 把散落在各项目里的提交记录汇成飞书 Base 可直接导入的载荷。

数据源(只读,不改源文件):
  - partfit3d/artifacts/seo/backlink-submissions-2026-07-31.jsonl   提交流水
  - ai-image/research/backlinks/<campaign>/results.jsonl            提交流水
  - ai-image/research/backlinks/<campaign>/candidate-pool.csv       渠道池
  - partfit3d/artifacts/seo/*-queue-*.csv                           渠道池
  - shark-agent/memory/experiments.md 里 2026-08-11 那批(本文件内 MANUAL_ROWS 硬编码)

用法:
    python3 scripts/backlink_ledger.py build            # 生成导入载荷到 artifacts/backlink-ledger/
    python3 scripts/backlink_ledger.py build --stats    # 顺带打印分布统计
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

SPACE = Path(__file__).resolve().parent.parent.parent
OUT_DIR = Path(__file__).resolve().parent.parent / "artifacts" / "backlink-ledger"

CST = timezone(timedelta(hours=8))

# 每个 jsonl 都是「单站一轮 campaign」的流水,站点归属以文件为准。
# 源文件里的 site_name / site_url / submitted_url 有大量串位(写成了目录站自己),不能当归属依据,
# 只用来交叉校验并打 Site Corrected 标。
SUBMISSION_SOURCES = [
    ("partfit3d-jsonl", "PartFit 3D", "https://partfit3d.com",
     SPACE / "partfit3d/artifacts/seo/backlink-submissions-2026-07-31.jsonl"),
    ("aidepixelate-jsonl", "AI Depixelate", "https://aidepixelate.com",
     SPACE / "ai-image/research/backlinks/aidepixelate-2026-07-28/results.jsonl"),
]

# memory/experiments.md 2026-08-11「partfit3d 免费外链首批提交」——不在任何 jsonl 里
MANUAL_ROWS = [
    {
        "site_name": "PartFit 3D",
        "site_url": "https://partfit3d.com",
        "submitted_url": "https://partfit3d.com",
        "platform": "noisework",
        "platform_url": "https://tg.noisework.cn/posts/11353",
        "classification": "B",
        "status": "published",
        "evidence_type": "public_url",
        "evidence_url": "https://tg.noisework.cn/posts/11353",
        "link_attr": "dofollow",
        "requires_reciprocal": False,
        "reciprocal_added": False,
        "recorded_at": "2026-08-11T12:00:00+08:00",
        "notes": "已有自然链,非本轮提交。页面被 Google 收录,含 2 个直达 partfit3d.com 的链接,"
                 'rel="noopener" 无 nofollow。2026-08-11 用 ego 核验。',
        "indexed": "yes",
    },
    {
        "site_name": "PartFit 3D",
        "site_url": "https://partfit3d.com",
        "submitted_url": "https://partfit3d.com",
        "platform": "Startup Collections",
        "platform_url": "",
        "classification": "A",
        "status": "pending_review",
        "evidence_type": "receipt",
        "evidence_url": "",
        "link_attr": "unknown",
        "requires_reciprocal": False,
        "reciprocal_added": False,
        "recorded_at": "2026-08-11T12:00:00+08:00",
        "notes": "进入免费审核队列,表单回执「您的回复已记录」。未付 $10 插队费,暂无公开 listing URL。",
        "review_due": "2026-08-25",
    },
    {
        "site_name": "PartFit 3D",
        "site_url": "https://partfit3d.com",
        "submitted_url": "https://partfit3d.com",
        "platform": "WebsiteHunt",
        "platform_url": "https://www.websitehunt.co/websites/partfit-3d",
        "classification": "A",
        "status": "pending_review",
        "evidence_type": "public_url",
        "evidence_url": "https://www.websitehunt.co/websites/partfit-3d",
        "link_attr": "tracking_redirect",
        "requires_reciprocal": False,
        "reciprocal_added": False,
        "recorded_at": "2026-08-11T12:00:00+08:00",
        "notes": "公开详情页已建但仍标 Pending review。免费版走站内追踪跳转 /go/23356/,不是直链,"
                 "SEO 权重低。免费队列约 12+ 月。",
        "review_due": "2026-08-25",
    },
]

CHANNEL_SOURCES = [
    ("AI Depixelate", "aidepixelate-candidate-pool",
     SPACE / "ai-image/research/backlinks/aidepixelate-2026-07-28/candidate-pool.csv"),
    ("PartFit 3D", "partfit3d-directory-queue",
     SPACE / "partfit3d/artifacts/seo/backlink-directory-queue-2026-08-04.csv"),
    ("PartFit 3D", "partfit3d-qualified-queue",
     SPACE / "partfit3d/artifacts/seo/backlink-qualified-queue-2026-08-03.csv"),
    ("PartFit 3D", "partfit3d-tool-site-dofollow-queue",
     SPACE / "partfit3d/artifacts/seo/tool-site-dofollow-queue-2026-08-07.csv"),
    ("PartFit 3D", "partfit3d-web-cafe-free-queue",
     SPACE / "partfit3d/artifacts/seo/web-cafe-free-backlink-queue-2026-08-04.csv"),
]


def to_cst(raw: str) -> str | None:
    """各源的时间戳格式不统一(Z / +00:00 / 纯日期),统一成 UTC+8 的 'YYYY-MM-DD HH:mm:ss'。"""
    if not raw:
        return None
    raw = raw.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return f"{raw} 00:00:00"
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(CST).strftime("%Y-%m-%d %H:%M:%S")


def attempt_id(row: dict) -> str:
    seed = f"{row['site_url']}|{row['platform']}|{row.get('recorded_at', '')}"
    return hashlib.sha1(seed.encode()).hexdigest()[:20]


def norm_platform(name: str) -> str:
    """渠道池与提交流水的平台名对不齐(后者常带 ' email outreach' 后缀),归一后才能交叉核对。"""
    s = name.lower().strip()
    for suffix in (" email outreach", " email submission", " submission", " directory"):
        if s.endswith(suffix):
            s = s[: -len(suffix)]
    return re.sub(r"[^a-z0-9]", "", s)


def load_submissions() -> tuple[list[dict], list[str]]:
    rows, warnings = [], []
    host_of = lambda u: re.sub(r"^https?://(www\.)?", "", u or "").split("/")[0]
    for source, site_name, site_url, path in SUBMISSION_SOURCES:
        if not path.exists():
            warnings.append(f"缺失数据源: {path}")
            continue
        canonical_host = host_of(site_url)
        for line in path.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            bad_name = r.get("site_name") != site_name
            bad_url = not host_of(r.get("submitted_url")).endswith(canonical_host)
            if bad_name or bad_url:
                broken = " + ".join(filter(None, [
                    f"site_name={r.get('site_name')!r}" if bad_name else "",
                    f"submitted_url={r.get('submitted_url')!r}" if bad_url else "",
                ]))
                warnings.append(f"[{source}] 归属串位已按源文件修正 (platform={r['platform']}): {broken}")
            rows.append({
                **r,
                "site_name": site_name,
                "site_url": site_url,
                "site_corrected": bad_name or bad_url,
                "source": source,
            })
    for r in MANUAL_ROWS:
        rows.append({**r, "site_corrected": False, "source": "shark-memory-2026-08-11"})
    for r in rows:
        r["attempt_id"] = r.get("attempt_id") or attempt_id(r)
    return rows, warnings


def load_channels(submitted_platforms: set[str]) -> tuple[list[dict], list[str]]:
    rows, warnings, seen = [], [], set()
    for site_name, source, path in CHANNEL_SOURCES:
        if not path.exists():
            warnings.append(f"缺失数据源: {path}")
            continue
        for r in csv.DictReader(path.open()):
            platform = (r.get("platform") or "").strip()
            if not platform:
                continue
            key = (site_name, norm_platform(platform))
            if key in seen:
                warnings.append(f"[{source}] 渠道重复,跳过: {platform}")
                continue
            seen.add(key)
            requirements = " / ".join(filter(None, [
                (r.get("requirements") or "").strip(),
                (r.get("login_requirements") or "").strip(),
                (r.get("asset_requirements") or "").strip(),
            ]))
            priority = (r.get("priority") or "").strip()
            rows.append({
                "site_name": site_name,
                "platform": platform,
                "opportunity_url": (r.get("opportunity_url") or "").strip(),
                "submission_url": (r.get("submission_url") or r.get("submission_route")
                                   or r.get("route") or "").strip(),
                "source_url": (r.get("source_url") or "").strip(),
                "route_type": (r.get("route_type") or "").strip(),
                "classification": (r.get("classification") or "").strip(),
                "classification_reason": (r.get("classification_reason") or r.get("qualification")
                                          or r.get("fit_reason") or "").strip(),
                "free_status": (r.get("free_status") or "").strip(),
                "link_evidence": (r.get("link_evidence") or "").strip(),
                "requirements": requirements,
                "duplicate_status": (r.get("duplicate_status") or "").strip(),
                "reciprocal_requirements": (r.get("reciprocal_requirements") or "").strip(),
                "planned_action": (r.get("planned_action") or "").strip(),
                "priority": float(priority) if priority.replace(".", "", 1).isdigit() else None,
                "contact": (r.get("contact") or "").strip(),
                "authority_metric": (r.get("authority_metric") or "").strip(),
                "authority_value": (r.get("authority_value") or "").strip(),
                "observed_at": to_cst(r.get("observed_at") or r.get("verified_at") or ""),
                "notes": (r.get("notes") or "").strip(),
                "source": source,
                "submitted": norm_platform(platform) in submitted_platforms,
            })
    return rows, warnings


SUBMISSION_FIELDS = [
    "Attempt ID", "Site", "Platform", "Status", "Link Attribute", "Classification",
    "Evidence Type", "Evidence URL", "Platform URL", "Site URL", "Submitted URL",
    "Recorded At", "Published At", "Review Due", "Indexed", "Cost USD",
    "Requires Reciprocal", "Reciprocal Added", "Site Corrected", "Source", "Notes",
]

CHANNEL_FIELDS = [
    "Platform", "Site", "Classification", "Planned Action", "Priority", "Submitted",
    "Free Status", "Link Evidence", "Route Type", "Opportunity URL", "Submission URL",
    "Source URL", "Contact", "Authority Metric", "Authority Value", "Duplicate Status",
    "Reciprocal Requirements", "Requirements", "Classification Reason", "Observed At",
    "Source", "Notes",
]


def submission_row(r: dict) -> list:
    return [
        r["attempt_id"],
        r["site_name"],
        r["platform"],
        r["status"],
        r["link_attr"],
        r["classification"],
        r["evidence_type"],
        r.get("evidence_url") or None,
        r.get("platform_url") or None,
        r["site_url"],
        r["submitted_url"],
        to_cst(r["recorded_at"]),
        to_cst(r.get("published_at", "")),
        f"{r['review_due']} 00:00:00" if r.get("review_due") else None,
        r.get("indexed", "unchecked"),
        0,  # 全部为免费渠道;付费插队一律拒绝过
        bool(r.get("requires_reciprocal")),
        bool(r.get("reciprocal_added")),
        r["site_corrected"],
        r["source"],
        r.get("notes") or None,
    ]


def channel_row(r: dict) -> list:
    return [
        r["platform"], r["site_name"], r["classification"] or None, r["planned_action"] or None,
        r["priority"], r["submitted"], r["free_status"] or None, r["link_evidence"] or None,
        r["route_type"] or None, r["opportunity_url"] or None, r["submission_url"] or None,
        r["source_url"] or None, r["contact"] or None, r["authority_metric"] or None,
        r["authority_value"] or None, r["duplicate_status"] or None,
        r["reciprocal_requirements"] or None, r["requirements"] or None,
        r["classification_reason"] or None, r["observed_at"], r["source"], r["notes"] or None,
    ]


def opts(*names, hue="Blue"):
    return [{"name": n, "hue": hue} for n in names]


def field_defs(subs: list[dict], chans: list[dict]) -> dict:
    """字段定义直接由实际数据推导选项集,避免手写枚举漏掉源里出现过的值。"""
    def seen(rows, key):
        return sorted({r[key] for r in rows if r.get(key)})

    submissions = [
        {"type": "text", "name": "Attempt ID"},
        {"type": "select", "name": "Site", "options": opts(*seen(subs, "site_name"))},
        {"type": "text", "name": "Platform"},
        {"type": "select", "name": "Status", "options": opts(*seen(subs, "status"))},
        {"type": "select", "name": "Link Attribute", "options": opts(*seen(subs, "link_attr"))},
        {"type": "select", "name": "Classification", "options": opts(*seen(subs, "classification")),
         "description": "候选池分级:A 免费直提 / B 需邮件或人工 / C 有条件 / D 受阻或不可用"},
        {"type": "select", "name": "Evidence Type", "options": opts(*seen(subs, "evidence_type"))},
        # Evidence URL / Platform URL 混有 mailto: 和空值,用 text 避免 URL 字段校验失败(1254068)
        {"type": "text", "name": "Evidence URL"},
        {"type": "text", "name": "Platform URL"},
        {"type": "text", "name": "Site URL", "style": {"type": "url"}},
        {"type": "text", "name": "Submitted URL", "style": {"type": "url"}},
        {"type": "datetime", "name": "Recorded At", "style": {"format": "yyyy-MM-dd HH:mm"}},
        {"type": "datetime", "name": "Published At", "style": {"format": "yyyy-MM-dd"},
         "description": "listing 真正公开可见的日期,与提交时间区分"},
        {"type": "datetime", "name": "Review Due", "style": {"format": "yyyy-MM-dd"},
         "description": "回核到期日:到期查 listing 是否上线、link_attr 是否 dofollow"},
        {"type": "select", "name": "Indexed", "options": opts("yes", "no", "unchecked"),
         "description": "外链页是否被 Google 收录;未收录的链不传权重"},
        {"type": "number", "name": "Cost USD", "style": {"type": "currency", "precision": 2,
                                                         "currency_code": "USD"}},
        {"type": "checkbox", "name": "Requires Reciprocal"},
        {"type": "checkbox", "name": "Reciprocal Added"},
        {"type": "checkbox", "name": "Site Corrected",
         "description": "源文件里 site_name 或 submitted_url 串位(写成了目录站),导入时按源文件所属 campaign 归位。"
                        "此类行的 Submitted URL 保留原值,可能实为目录页或 listing 页,回核时以 Platform URL 为准"},
        {"type": "select", "name": "Source", "options": opts(*seen(subs, "source"))},
        {"type": "text", "name": "Notes"},
    ]
    channels = [
        {"type": "text", "name": "Platform"},
        {"type": "select", "name": "Site", "options": opts(*seen(chans, "site_name"))},
        {"type": "select", "name": "Classification", "options": opts(*seen(chans, "classification"))},
        {"type": "text", "name": "Planned Action"},
        {"type": "number", "name": "Priority", "style": {"type": "plain", "precision": 0}},
        {"type": "checkbox", "name": "Submitted", "description": "该渠道是否已出现在「外链记录」表"},
        {"type": "text", "name": "Free Status"},
        {"type": "text", "name": "Link Evidence"},
        {"type": "text", "name": "Route Type"},
        {"type": "text", "name": "Opportunity URL", "style": {"type": "url"}},
        {"type": "text", "name": "Submission URL"},
        {"type": "text", "name": "Source URL"},
        {"type": "text", "name": "Contact"},
        {"type": "text", "name": "Authority Metric"},
        {"type": "text", "name": "Authority Value"},
        {"type": "text", "name": "Duplicate Status"},
        {"type": "text", "name": "Reciprocal Requirements"},
        {"type": "text", "name": "Requirements"},
        {"type": "text", "name": "Classification Reason"},
        {"type": "datetime", "name": "Observed At", "style": {"format": "yyyy-MM-dd"}},
        {"type": "select", "name": "Source", "options": opts(*seen(chans, "source"))},
        {"type": "text", "name": "Notes"},
    ]
    return {"外链记录": submissions, "渠道池": channels}


def chunk(rows, size=200):
    return [rows[i:i + size] for i in range(0, len(rows), size)]


def build(show_stats: bool) -> None:
    subs, warn_s = load_submissions()
    submitted_platforms = {norm_platform(r["platform"]) for r in subs}
    chans, warn_c = load_channels(submitted_platforms)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "fields.json").write_text(
        json.dumps(field_defs(subs, chans), ensure_ascii=False, indent=2) + "\n")

    manifest = {}
    for label, fields, rows, builder in [
        ("submissions", SUBMISSION_FIELDS, subs, submission_row),
        ("channels", CHANNEL_FIELDS, chans, channel_row),
    ]:
        batches = chunk([builder(r) for r in rows])
        names = []
        for i, batch in enumerate(batches, 1):
            name = f"{label}.batch{i}.json"
            (OUT_DIR / name).write_text(
                json.dumps({"fields": fields, "rows": batch}, ensure_ascii=False, indent=2) + "\n")
            names.append(name)
        manifest[label] = {"rows": len(rows), "batches": names}

    warnings = warn_s + warn_c
    manifest["warnings"] = warnings
    manifest["built_at"] = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    print(f"外链记录 {len(subs)} 行 · 渠道池 {len(chans)} 行 -> {OUT_DIR}")
    corrected = sum(1 for r in subs if r["site_corrected"])
    print(f"site 串位修正 {corrected} 行 · 其他告警 {len(warnings) - corrected} 条(见 manifest.json)")

    if show_stats:
        from collections import Counter
        for key, title in [("site_name", "站点"), ("status", "状态"), ("link_attr", "链接形态")]:
            print(f"\n{title}: {dict(Counter(r[key] for r in subs))}")
        print(f"\n渠道池已提交交叉命中: {sum(1 for r in chans if r['submitted'])}/{len(chans)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="生成飞书 Base 导入载荷")
    b.add_argument("--stats", action="store_true", help="打印分布统计")
    args = parser.parse_args()
    if args.cmd == "build":
        build(args.stats)


if __name__ == "__main__":
    main()
