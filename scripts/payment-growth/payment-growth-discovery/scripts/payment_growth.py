from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote, urljoin, urlparse

import requests


SKILLS_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = SKILL_DIR / "state" / "payment_growth.sqlite3"
IANA_RDAP_BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"
DEFAULT_TARGETS = (
    "checkout.stripe.com",
    "paypal.com",
    "paddle.com",
    "lemonsqueezy.com",
)
TYPICAL_PRODUCTS_PER_CATEGORY = 5
# EngagementVisits/Graph gets flaky as the key count grows; 5 is reliable here.
MAX_TRAFFIC_TREND_BATCH = 5
TRAFFIC_TREND_MAX_ATTEMPTS = 3
TRAFFIC_TREND_RETRY_BACKOFF_SECONDS = 3
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from similarweb.scripts import similarweb_client as similarweb


PLATFORM_DOMAINS = {
    "stripe.com",
    "paypal.com",
    "paddle.com",
    "paddle.net",
    "lemonsqueezy.com",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS referral_snapshots (
    id INTEGER PRIMARY KEY,
    target_domain TEXT NOT NULL,
    month TEXT NOT NULL,
    collected_at TEXT NOT NULL,
    total_count INTEGER,
    pages_fetched INTEGER NOT NULL,
    records_returned INTEGER NOT NULL,
    complete INTEGER NOT NULL,
    UNIQUE(target_domain, month)
);

CREATE TABLE IF NOT EXISTS referral_rows (
    snapshot_id INTEGER NOT NULL REFERENCES referral_snapshots(id) ON DELETE CASCADE,
    source_domain TEXT NOT NULL,
    position INTEGER NOT NULL,
    global_rank INTEGER,
    change REAL,
    new_change INTEGER NOT NULL,
    total_share REAL,
    total_visits REAL,
    month_abs_visits REAL NOT NULL,
    category TEXT,
    engagement_score REAL,
    PRIMARY KEY(snapshot_id, source_domain)
);

CREATE INDEX IF NOT EXISTS referral_rows_source_domain_idx
ON referral_rows(source_domain);

CREATE TABLE IF NOT EXISTS domain_profiles (
    source_domain TEXT PRIMARY KEY,
    registrable_domain TEXT,
    rdap_status TEXT NOT NULL,
    registered_at TEXT,
    expires_at TEXT,
    registrar TEXT,
    rdap_url TEXT,
    fetched_at TEXT NOT NULL,
    error TEXT
);

CREATE TABLE IF NOT EXISTS website_traffic_months (
    source_domain TEXT NOT NULL,
    month TEXT NOT NULL,
    visits REAL,
    available INTEGER NOT NULL,
    data_verified INTEGER,
    collected_at TEXT NOT NULL,
    country TEXT NOT NULL,
    web_source TEXT NOT NULL,
    include_subdomains INTEGER NOT NULL,
    PRIMARY KEY (
        source_domain,
        month,
        country,
        web_source,
        include_subdomains
    )
);

CREATE INDEX IF NOT EXISTS website_traffic_months_domain_month_idx
ON website_traffic_months(source_domain, month);
"""


def normalize_domain(value: Any) -> str | None:
    domain = str(value or "").strip().lower().rstrip(".")
    if "://" in domain:
        domain = urlparse(domain).hostname or ""
    domain = domain.split("/", 1)[0].split(":", 1)[0]
    if domain.startswith("www."):
        domain = domain[4:]
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z0-9-]{2,}", domain):
        return None
    return domain


def is_platform_domain(domain: str) -> bool:
    return any(
        domain == platform or domain.endswith(f".{platform}")
        for platform in PLATFORM_DOMAINS
    )


def resolve_rdap_base_url(
    bootstrap: dict[str, Any],
    domain: str,
) -> str | None:
    labels = domain.lower().rstrip(".").split(".")
    matches: list[tuple[int, str]] = []
    for service in bootstrap.get("services", []):
        if not isinstance(service, list) or len(service) != 2:
            continue
        suffixes, urls = service
        if not isinstance(suffixes, list) or not isinstance(urls, list):
            continue
        for suffix in suffixes:
            suffix_labels = str(suffix).lower().rstrip(".").split(".")
            if labels[-len(suffix_labels) :] == suffix_labels and urls:
                matches.append((len(suffix_labels), str(urls[0])))
    if not matches:
        return None
    return max(matches, key=lambda item: item[0])[1]


def _rdap_event(payload: dict[str, Any], action: str) -> str | None:
    for event in payload.get("events", []):
        if event.get("eventAction") == action:
            return event.get("eventDate")
    return None


def _rdap_registrar(payload: dict[str, Any]) -> str | None:
    for entity in payload.get("entities", []):
        if "registrar" not in entity.get("roles", []):
            continue
        vcard = entity.get("vcardArray", [])
        properties = vcard[1] if len(vcard) > 1 else []
        for property_row in properties:
            if len(property_row) >= 4 and property_row[0] == "fn":
                return str(property_row[3])
    return None


def parse_rdap_profile(
    payload: dict[str, Any],
    *,
    source_domain: str,
    rdap_url: str,
    fetched_at: str,
) -> dict[str, Any]:
    registrable_domain = normalize_domain(
        payload.get("ldhName") or payload.get("unicodeName")
    )
    return {
        "source_domain": source_domain,
        "registrable_domain": registrable_domain,
        "rdap_status": "ok",
        "registered_at": _rdap_event(payload, "registration"),
        "expires_at": _rdap_event(payload, "expiration"),
        "registrar": _rdap_registrar(payload),
        "rdap_url": rdap_url,
        "fetched_at": fetched_at,
        "error": None,
    }


def extract_snapshot_rows(
    payload: dict[str, Any],
    *,
    month: str,
    top_n: int | None = None,
) -> list[dict[str, Any]]:
    records = payload.get("referral_table", {}).get("Records", [])
    if not isinstance(records, list):
        raise ValueError("referral_table.Records must be a list")
    month_key = f"{month}-01"
    rows: list[dict[str, Any]] = []
    seen_domains: set[str] = set()
    for position, record in enumerate(records, start=1):
        if top_n is not None and position > top_n:
            break
        source_domain = normalize_domain(record.get("Domain"))
        if not source_domain:
            continue
        if source_domain in seen_domains:
            continue
        seen_domains.add(source_domain)
        monthly_values = (
            record.get("TotalVisitsAndSharePerMonth", {}).get(month_key, [])
            or []
        )
        month_abs_visits = sum(
            float(item.get("AbsValue") or 0)
            for item in monthly_values
            if isinstance(item, dict)
        )
        if not monthly_values:
            month_abs_visits = float(record.get("TotalVisits") or 0)
        rows.append(
            {
                "source_domain": source_domain,
                "position": position,
                "global_rank": record.get("Rank"),
                "change": record.get("Change"),
                "new_change": bool(record.get("NewChange")),
                "total_share": record.get("TotalShare", record.get("Share")),
                "total_visits": record.get("TotalVisits"),
                "month_abs_visits": month_abs_visits,
                "category": record.get("Category"),
                "engagement_score": record.get("EngagementScore"),
            }
        )
    return rows


def initialize_database(db_path: str | Path) -> Path:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(SCHEMA)
    return path


def save_snapshot(
    db_path: str | Path,
    *,
    target_domain: str,
    month: str,
    rows: list[dict[str, Any]],
    total_count: int | None,
    pages_fetched: int,
    complete: bool,
) -> dict[str, Any]:
    path = initialize_database(db_path)
    collected_at = datetime.now(timezone.utc).isoformat()
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(
                """
                INSERT INTO referral_snapshots (
                    target_domain, month, collected_at, total_count,
                    pages_fetched, records_returned, complete
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(target_domain, month) DO UPDATE SET
                    collected_at = excluded.collected_at,
                    total_count = excluded.total_count,
                    pages_fetched = excluded.pages_fetched,
                    records_returned = excluded.records_returned,
                    complete = excluded.complete
                """,
                (
                    target_domain,
                    month,
                    collected_at,
                    total_count,
                    pages_fetched,
                    len(rows),
                    int(complete),
                ),
            )
            snapshot_id = connection.execute(
                """
                SELECT id
                FROM referral_snapshots
                WHERE target_domain = ? AND month = ?
                """,
                (target_domain, month),
            ).fetchone()[0]
            connection.execute(
                "DELETE FROM referral_rows WHERE snapshot_id = ?",
                (snapshot_id,),
            )
            connection.executemany(
                """
                INSERT INTO referral_rows (
                    snapshot_id, source_domain, position, global_rank,
                    change, new_change, total_share, total_visits,
                    month_abs_visits, category, engagement_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        snapshot_id,
                        row["source_domain"],
                        row["position"],
                        row.get("global_rank"),
                        row.get("change"),
                        int(bool(row.get("new_change"))),
                        row.get("total_share"),
                        row.get("total_visits"),
                        float(row.get("month_abs_visits") or 0),
                        row.get("category"),
                        row.get("engagement_score"),
                    )
                    for row in rows
                ],
            )
    return {
        "target_domain": target_domain,
        "month": month,
        "total_count": total_count,
        "pages_fetched": pages_fetched,
        "records_returned": len(rows),
        "complete": complete,
    }


def save_domain_profile(
    db_path: str | Path,
    profile: dict[str, Any],
) -> dict[str, Any]:
    path = initialize_database(db_path)
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            connection.execute(
                """
                INSERT INTO domain_profiles (
                    source_domain, registrable_domain, rdap_status,
                    registered_at, expires_at, registrar, rdap_url,
                    fetched_at, error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(source_domain) DO UPDATE SET
                    registrable_domain = excluded.registrable_domain,
                    rdap_status = excluded.rdap_status,
                    registered_at = excluded.registered_at,
                    expires_at = excluded.expires_at,
                    registrar = excluded.registrar,
                    rdap_url = excluded.rdap_url,
                    fetched_at = excluded.fetched_at,
                    error = excluded.error
                """,
                (
                    profile["source_domain"],
                    profile.get("registrable_domain"),
                    profile["rdap_status"],
                    profile.get("registered_at"),
                    profile.get("expires_at"),
                    profile.get("registrar"),
                    profile.get("rdap_url"),
                    profile["fetched_at"],
                    profile.get("error"),
                ),
            )
    return profile


def _normalize_fractional_seconds(value: str) -> str:
    # Python < 3.11 only accepts 3 or 6 fractional digits; RDAP returns 1-9.
    return re.sub(
        r"\.(\d+)",
        lambda match: "." + match.group(1)[:6].ljust(6, "0"),
        value,
        count=1,
    )


def _parse_timestamp(value: str) -> datetime:
    text = _normalize_fractional_seconds(value.replace("Z", "+00:00"))
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def enrich_domains(
    db_path: str | Path,
    domains: list[str],
    *,
    fetcher: Callable[[str], dict[str, Any]],
    force: bool = False,
    cache_days: int = 30,
    now: str | None = None,
) -> dict[str, Any]:
    path = initialize_database(db_path)
    now_value = _parse_timestamp(now) if now else datetime.now(timezone.utc)
    cutoff = now_value - timedelta(days=cache_days)
    fetched = 0
    cached = 0
    failed = 0
    normalized_domains = list(
        dict.fromkeys(
            domain
            for value in domains
            if (domain := normalize_domain(value))
        )
    )
    with closing(sqlite3.connect(path)) as connection:
        known = {
            row[0]: row[1]
            for row in connection.execute(
                """
                SELECT source_domain, fetched_at
                FROM domain_profiles
                WHERE source_domain IN ({})
                """.format(",".join("?" for _ in normalized_domains) or "NULL"),
                normalized_domains,
            )
        }
    for domain in normalized_domains:
        if (
            not force
            and domain in known
            and _parse_timestamp(known[domain]) >= cutoff
        ):
            cached += 1
            continue
        try:
            profile = fetcher(domain)
        except Exception as error:
            profile = {
                "source_domain": domain,
                "registrable_domain": None,
                "rdap_status": "error",
                "registered_at": None,
                "expires_at": None,
                "registrar": None,
                "rdap_url": None,
                "fetched_at": now_value.isoformat(),
                "error": str(error),
            }
            failed += 1
        save_domain_profile(path, profile)
        fetched += 1
    return {
        "database": str(path.resolve()),
        "domains": normalized_domains,
        "profiles_fetched": fetched,
        "profiles_cached": cached,
        "profiles_failed": failed,
    }


def collect_snapshots(
    db_path: str | Path,
    *,
    targets: list[str],
    months: list[str],
    fetcher: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    saved = []
    for target_domain in targets:
        normalized_target = normalize_domain(target_domain)
        if not normalized_target:
            raise ValueError(f"Invalid target domain: {target_domain}")
        for month in months:
            if not re.fullmatch(r"\d{4}-(?:0[1-9]|1[0-2])", month):
                raise ValueError(f"Invalid month: {month}")
            payload = fetcher(
                target_domain=normalized_target,
                month=month,
                max_pages=None,
            )
            pagination = payload.get("pagination", {})
            if pagination.get("complete") is not True:
                raise RuntimeError(
                    f"{normalized_target}:{month} did not return a "
                    "complete referral table"
                )
            rows = extract_snapshot_rows(payload, month=month)
            table = payload.get("referral_table", {})
            saved.append(
                save_snapshot(
                    db_path,
                    target_domain=normalized_target,
                    month=month,
                    rows=rows,
                    total_count=pagination.get(
                        "total_count",
                        table.get("TotalCount"),
                    ),
                    pages_fetched=int(pagination.get("pages_fetched") or 1),
                    complete=bool(pagination.get("complete")),
                )
            )
    return {
        "database": str(Path(db_path).resolve()),
        "targets": targets,
        "months": months,
        "collection_scope": "full",
        "snapshots_saved": len(saved),
        "records_saved": sum(item["records_returned"] for item in saved),
        "snapshots": saved,
    }


def create_live_fetcher() -> Callable[..., dict[str, Any]]:
    client = similarweb.SimilarWebClient()
    auth_candidates = similarweb.resolve_auth_candidates(
        username=None,
        password=None,
    )

    def fetcher(
        *,
        target_domain: str,
        month: str,
        max_pages: int | None,
    ) -> dict[str, Any]:
        return similarweb.run_with_auth_candidates(
            auth_candidates,
            lambda auth: client.fetch_referral_traffic_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domain=target_domain,
                from_month=month,
                to_month=month,
                all_pages=True,
                max_pages=max_pages,
            ),
            on_auth_failure=lambda auth: (
                not auth.get("token")
                and client.invalidate_cached_token(auth["username"])
            ),
        )

    return fetcher


def create_live_rdap_fetcher(
    *,
    session: requests.Session | None = None,
    now: Callable[[], str] | None = None,
) -> Callable[[str], dict[str, Any]]:
    http = session or requests.Session()
    http.trust_env = False
    http.headers.update(
        {
            "Accept": "application/rdap+json, application/json",
            "User-Agent": "payment-growth-discovery/1.0",
        }
    )
    bootstrap: dict[str, Any] | None = None

    def fetcher(source_domain: str) -> dict[str, Any]:
        nonlocal bootstrap
        domain = normalize_domain(source_domain)
        if not domain:
            raise ValueError(f"Invalid domain: {source_domain}")
        if bootstrap is None:
            response = http.get(IANA_RDAP_BOOTSTRAP_URL, timeout=15)
            response.raise_for_status()
            bootstrap = response.json()
        base_url = resolve_rdap_base_url(bootstrap, domain)
        fetched_at = (
            now() if now else datetime.now(timezone.utc).isoformat()
        )
        if not base_url:
            return {
                "source_domain": domain,
                "registrable_domain": None,
                "rdap_status": "unsupported_tld",
                "registered_at": None,
                "expires_at": None,
                "registrar": None,
                "rdap_url": None,
                "fetched_at": fetched_at,
                "error": "No authoritative RDAP service in IANA bootstrap",
            }
        labels = domain.split(".")
        for start in range(len(labels) - 1):
            candidate = ".".join(labels[start:])
            rdap_url = urljoin(
                base_url.rstrip("/") + "/",
                f"domain/{quote(candidate, safe='')}",
            )
            response = http.get(rdap_url, timeout=15)
            if response.status_code == 404:
                continue
            response.raise_for_status()
            return parse_rdap_profile(
                response.json(),
                source_domain=domain,
                rdap_url=rdap_url,
                fetched_at=fetched_at,
            )
        return {
            "source_domain": domain,
            "registrable_domain": None,
            "rdap_status": "not_found",
            "registered_at": None,
            "expires_at": None,
            "registrar": None,
            "rdap_url": None,
            "fetched_at": fetched_at,
            "error": "Domain not found in authoritative RDAP service",
        }

    return fetcher


def _load_month_rows(
    connection: sqlite3.Connection,
    month: str,
) -> dict[tuple[str, str], dict[str, Any]]:
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        """
        SELECT
            snapshots.target_domain,
            rows.source_domain,
            rows.position,
            rows.global_rank,
            rows.month_abs_visits,
            rows.total_share,
            rows.category
        FROM referral_rows AS rows
        JOIN referral_snapshots AS snapshots ON snapshots.id = rows.snapshot_id
        WHERE snapshots.month = ?
        """,
        (month,),
    ).fetchall()
    return {
        (row["target_domain"], row["source_domain"]): dict(row)
        for row in rows
    }


def _load_domain_profiles(
    connection: sqlite3.Connection,
) -> dict[str, dict[str, Any]]:
    connection.row_factory = sqlite3.Row
    return {
        row["source_domain"]: dict(row)
        for row in connection.execute(
            "SELECT * FROM domain_profiles"
        ).fetchall()
    }


def _load_snapshot_status(
    connection: sqlite3.Connection,
    months: list[str],
) -> dict[tuple[str, str], bool]:
    placeholders = ", ".join("?" for _ in months)
    rows = connection.execute(
        f"""
        SELECT target_domain, month, complete
        FROM referral_snapshots
        WHERE month IN ({placeholders})
        """,
        months,
    ).fetchall()
    return {
        (row["target_domain"], row["month"]): bool(row["complete"])
        for row in rows
    }


def _month_end(month: str) -> datetime:
    start = datetime.strptime(month, "%Y-%m").replace(tzinfo=timezone.utc)
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1)
    else:
        next_month = start.replace(month=start.month + 1)
    return next_month - timedelta(days=1)


def _month_sequence(start_month: str, end_month: str) -> list[str]:
    try:
        current = datetime.strptime(start_month, "%Y-%m")
        end = datetime.strptime(end_month, "%Y-%m")
    except ValueError as error:
        raise ValueError("Months must use YYYY-MM format") from error
    if current > end:
        raise ValueError("start_month must not be after end_month")
    months = []
    while current <= end:
        months.append(current.strftime("%Y-%m"))
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    return months


def _shift_month(month: str, offset: int) -> str:
    try:
        value = datetime.strptime(month, "%Y-%m")
    except ValueError as error:
        raise ValueError("Months must use YYYY-MM format") from error
    absolute_month = value.year * 12 + value.month - 1 + offset
    year, month_index = divmod(absolute_month, 12)
    return f"{year:04d}-{month_index + 1:02d}"


def collect_website_traffic(
    db_path: str | Path,
    *,
    domains: list[str],
    start_month: str,
    end_month: str,
    fetcher: Callable[..., dict[str, Any]],
    collected_at: str | None = None,
    country: str = "999",
    web_source: str = "Total",
    include_subdomains: bool = True,
    batch_size: int = MAX_TRAFFIC_TREND_BATCH,
) -> dict[str, Any]:
    if batch_size < 1:
        raise ValueError("batch_size must be at least 1")
    months = _month_sequence(start_month, end_month)
    normalized_domains = []
    seen = set()
    for value in domains:
        domain = normalize_domain(value)
        if domain and domain not in seen and not is_platform_domain(domain):
            normalized_domains.append(domain)
            seen.add(domain)
    timestamp = collected_at or datetime.now(timezone.utc).isoformat()
    records = []
    for index in range(0, len(normalized_domains), batch_size):
        batch = normalized_domains[index : index + batch_size]
        payload = fetcher(
            domains=batch,
            from_month=start_month,
            to_month=end_month,
            country=country,
            web_source=web_source,
            include_subdomains=include_subdomains,
        )
        series_by_domain = payload.get("monthly_visits", {})
        for domain in batch:
            domain_payload = series_by_domain.get(domain, {})
            points = {
                point.get("month"): point.get("visits")
                for point in domain_payload.get("months", [])
                if point.get("month") in months
            }
            data_verified = domain_payload.get("data_verified")
            for month in months:
                visits = points.get(month)
                records.append(
                    (
                        domain,
                        month,
                        float(visits) if visits is not None else None,
                        int(visits is not None),
                        None if data_verified is None else int(bool(data_verified)),
                        timestamp,
                        country,
                        web_source,
                        int(include_subdomains),
                    )
                )
    path = initialize_database(db_path)
    with closing(sqlite3.connect(path)) as connection:
        connection.executemany(
            """
            INSERT INTO website_traffic_months (
                source_domain, month, visits, available, data_verified,
                collected_at, country, web_source, include_subdomains
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(
                source_domain, month, country, web_source, include_subdomains
            ) DO UPDATE SET
                visits = excluded.visits,
                available = excluded.available,
                data_verified = excluded.data_verified,
                collected_at = excluded.collected_at
            """,
            records,
        )
        connection.commit()
    available = sum(record[3] for record in records)
    return {
        "database": str(path),
        "domains": normalized_domains,
        "start_month": start_month,
        "end_month": end_month,
        "months": months,
        "series_saved": len(normalized_domains),
        "points_available": available,
        "points_missing": len(records) - available,
    }


def create_live_website_traffic_fetcher() -> Callable[..., dict[str, Any]]:
    client = similarweb.SimilarWebClient()
    auth_candidates = similarweb.resolve_auth_candidates(
        username=None,
        password=None,
    )

    def fetch_once(**kwargs: Any) -> dict[str, Any]:
        return similarweb.run_with_auth_candidates(
            auth_candidates,
            lambda auth: client.fetch_website_traffic_trend_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                **kwargs,
            ),
            on_auth_failure=lambda auth: (
                not auth.get("token")
                and client.invalidate_cached_token(auth["username"])
            ),
        )

    def fetch(**kwargs: Any) -> dict[str, Any]:
        # EngagementVisits/Graph intermittently answers a valid request with 400
        # or a login-redirect page. Retry with backoff before giving up.
        last_error: Exception | None = None
        for attempt in range(TRAFFIC_TREND_MAX_ATTEMPTS):
            try:
                return fetch_once(**kwargs)
            except Exception as error:  # noqa: BLE001 - upstream failure is opaque
                last_error = error
                if attempt < TRAFFIC_TREND_MAX_ATTEMPTS - 1:
                    time.sleep(TRAFFIC_TREND_RETRY_BACKOFF_SECONDS * (attempt + 1))
        raise last_error  # type: ignore[misc]

    return fetch


def analyze_website_traffic(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: row["month"])
    series = []
    for row in ordered:
        available = bool(row.get("available", row.get("visits") is not None))
        series.append(
            {
                "month": row["month"],
                "visits": (
                    float(row["visits"])
                    if available and row.get("visits") is not None
                    else None
                ),
                "available": available,
                "data_verified": row.get("data_verified"),
            }
        )
    available_points = [point for point in series if point["available"]]
    result = {
        "trend": "insufficient_data",
        "series": series,
        "months_requested": len(series),
        "months_available": len(available_points),
        "first_month": None,
        "first_visits": None,
        "latest_month": None,
        "latest_visits": None,
        "absolute_change": None,
        "growth_rate": None,
        "latest_month_growth_rate": None,
        "positive_growth_steps": 0,
        "negative_growth_steps": 0,
        "all_data_verified": None,
    }
    verification = [
        point["data_verified"]
        for point in available_points
        if point["data_verified"] is not None
    ]
    if verification:
        result["all_data_verified"] = all(bool(value) for value in verification)
    if not available_points:
        return result
    first = available_points[0]
    latest = available_points[-1]
    result.update(
        {
            "first_month": first["month"],
            "first_visits": first["visits"],
            "latest_month": latest["month"],
            "latest_visits": latest["visits"],
        }
    )
    if len(available_points) < 2:
        return result
    changes = [
        current["visits"] - previous["visits"]
        for previous, current in zip(available_points, available_points[1:])
    ]
    absolute_change = latest["visits"] - first["visits"]
    result.update(
        {
            "absolute_change": absolute_change,
            "growth_rate": (
                absolute_change / first["visits"]
                if first["visits"]
                else None
            ),
            "latest_month_growth_rate": (
                changes[-1] / available_points[-2]["visits"]
                if available_points[-2]["visits"]
                else None
            ),
            "positive_growth_steps": sum(change > 0 for change in changes),
            "negative_growth_steps": sum(change < 0 for change in changes),
        }
    )
    recent = available_points[-3:]
    consecutive_recent = (
        len(recent) == 3
        and _month_sequence(recent[0]["month"], recent[-1]["month"])
        == [point["month"] for point in recent]
    )
    if consecutive_recent and all(change > 0 for change in changes[-2:]):
        result["trend"] = "sustained_growth"
    elif consecutive_recent and all(change < 0 for change in changes[-2:]):
        result["trend"] = "sustained_decline"
    elif absolute_change > 0:
        result["trend"] = "growing"
    elif absolute_change < 0:
        result["trend"] = "declining"
    else:
        result["trend"] = "flat"
    return result


def _load_website_traffic(
    connection: sqlite3.Connection,
    start_month: str,
    end_month: str,
) -> dict[str, list[dict[str, Any]]]:
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        """
        SELECT source_domain, month, visits, available, data_verified
        FROM website_traffic_months
        WHERE month >= ? AND month <= ?
          AND country = '999'
          AND web_source = 'Total'
          AND include_subdomains = 1
        ORDER BY source_domain, month
        """,
        (start_month, end_month),
    ).fetchall()
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(row["source_domain"], []).append(dict(row))
    return grouped


def _attach_website_traffic(
    item: dict[str, Any],
    traffic_by_domain: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    output = dict(item)
    output["website_traffic"] = analyze_website_traffic(
        traffic_by_domain.get(item["source_domain"], [])
    )
    if not traffic_by_domain.get(item["source_domain"]):
        output["website_traffic"]["trend"] = "unavailable"
    return output


def _attach_profile(
    item: dict[str, Any],
    profiles: dict[str, dict[str, Any]],
    *,
    as_of: datetime,
) -> dict[str, Any]:
    output = dict(item)
    profile = profiles.get(item["source_domain"])
    if not profile:
        return output
    output.update(
        {
            "registrable_domain": profile["registrable_domain"],
            "rdap_status": profile["rdap_status"],
            "registered_at": profile["registered_at"],
            "expires_at": profile["expires_at"],
            "registrar": profile["registrar"],
        }
    )
    if profile["registered_at"]:
        registered_at = _parse_timestamp(profile["registered_at"])
        output["domain_age_days"] = max(0, (as_of - registered_at).days)
    return output


def report_candidate_domains(report: dict[str, Any]) -> list[str]:
    candidates = []
    seen = set()
    for key in (
        "rank_risers",
        "fast_rank_growth",
        "traffic_gainers",
        "newcomers",
        "sustained_growth",
        "breakouts",
        "newly_visible",
        "new_product_growth",
    ):
        for item in report.get(key, []):
            domain = item["source_domain"]
            if domain not in seen:
                seen.add(domain)
                candidates.append(domain)
    return candidates


def _category_conclusions(
    current: dict[tuple[str, str], dict[str, Any]],
    previous: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    category_totals: dict[str, dict[str, float]] = {}
    current_products: dict[str, dict[str, dict[str, Any]]] = {}
    all_keys = set(current) | set(previous)
    for key in all_keys:
        _, source_domain = key
        if is_platform_domain(source_domain):
            continue
        current_row = current.get(key)
        previous_row = previous.get(key)
        category = str(
            (current_row or previous_row or {}).get("category")
            or "Unknown"
        )
        totals = category_totals.setdefault(
            category,
            {"previous": 0.0, "current": 0.0},
        )
        previous_visits = float(
            (previous_row or {}).get("month_abs_visits") or 0
        )
        current_visits = float(
            (current_row or {}).get("month_abs_visits") or 0
        )
        totals["previous"] += previous_visits
        totals["current"] += current_visits
        if not current_row:
            continue
        target_domain, source_domain = key
        products = current_products.setdefault(category, {})
        product = products.setdefault(
            source_domain,
            {
                "source_domain": source_domain,
                "previous_payment_intent_visits": 0.0,
                "current_payment_intent_visits": 0.0,
                "payment_targets": [],
            },
        )
        product["previous_payment_intent_visits"] += previous_visits
        product["current_payment_intent_visits"] += current_visits
        product["payment_targets"].append(target_domain)

    categories = []
    for category, totals in category_totals.items():
        previous_visits = totals["previous"]
        current_visits = totals["current"]
        absolute_change = current_visits - previous_visits
        products = []
        for product in current_products.get(category, {}).values():
            product["payment_targets"] = sorted(
                set(product["payment_targets"])
            )
            product["absolute_change"] = (
                product["current_payment_intent_visits"]
                - product["previous_payment_intent_visits"]
            )
            products.append(product)
        products.sort(
            key=lambda item: item["current_payment_intent_visits"],
            reverse=True,
        )
        categories.append(
            {
                "category": category,
                "previous_payment_intent_visits": previous_visits,
                "current_payment_intent_visits": current_visits,
                "absolute_change": absolute_change,
                "growth_rate": (
                    absolute_change / previous_visits
                    if previous_visits > 0
                    else None
                ),
                "top_products": products[
                    :TYPICAL_PRODUCTS_PER_CATEGORY
                ],
            }
        )
    gainers = sorted(
        (
            item
            for item in categories
            if item["absolute_change"] > 0
        ),
        key=lambda item: item["absolute_change"],
        reverse=True,
    )
    decliners = sorted(
        (
            item
            for item in categories
            if item["absolute_change"] < 0
        ),
        key=lambda item: item["absolute_change"],
    )
    return {"gainers": gainers, "decliners": decliners}


def _new_product_growth(
    current: dict[tuple[str, str], dict[str, Any]],
    previous: dict[tuple[str, str], dict[str, Any]],
    profiles: dict[str, dict[str, Any]],
    *,
    min_current_visits: float,
    min_previous_visits: float,
    max_domain_age_days: int,
    as_of: datetime,
    limit: int,
) -> list[dict[str, Any]]:
    current_by_domain: dict[str, dict[str, Any]] = {}
    previous_by_domain: dict[str, float] = {}
    for (_, source_domain), row in previous.items():
        previous_by_domain[source_domain] = (
            previous_by_domain.get(source_domain, 0.0)
            + float(row["month_abs_visits"] or 0)
        )
    for (target_domain, source_domain), row in current.items():
        if is_platform_domain(source_domain):
            continue
        visits = float(row["month_abs_visits"] or 0)
        item = current_by_domain.setdefault(
            source_domain,
            {
                "source_domain": source_domain,
                "current_payment_intent_visits": 0.0,
                "payment_targets": [],
                "target_positions": {},
                "category": row["category"] or "Unknown",
                "_category_visits": -1.0,
            },
        )
        item["current_payment_intent_visits"] += visits
        item["payment_targets"].append(target_domain)
        item["target_positions"][target_domain] = row["position"]
        if visits > item["_category_visits"]:
            item["category"] = row["category"] or "Unknown"
            item["_category_visits"] = visits

    candidates = []
    for source_domain, item in current_by_domain.items():
        current_visits = item["current_payment_intent_visits"]
        newly_visible = source_domain not in previous_by_domain
        if not newly_visible and current_visits < min_current_visits:
            continue
        previous_visits = previous_by_domain.get(source_domain, 0.0)
        output = {
            key: value
            for key, value in item.items()
            if not key.startswith("_")
        }
        output["payment_targets"] = sorted(
            set(output["payment_targets"])
        )
        output["previous_payment_intent_visits"] = previous_visits
        output["absolute_change"] = current_visits - previous_visits
        output["growth_rate"] = (
            output["absolute_change"] / previous_visits
            if previous_visits > 0
            else None
        )
        output = _attach_profile(output, profiles, as_of=as_of)
        signals = []
        if newly_visible:
            signals.append("newly_visible")
        elif (
            previous_visits >= min_previous_visits
            and output["absolute_change"] > 0
            and output.get("domain_age_days") is not None
            and output["domain_age_days"] <= max_domain_age_days
        ):
            signals.append("young_growth")
        if not signals:
            continue
        output["signals"] = signals
        risk_flags = []
        if "paypal.com" in output["payment_targets"]:
            risk_flags.append("paypal_broad_intent")
        if output["category"] == "Unknown":
            risk_flags.append("unknown_category")
        output["risk_flags"] = risk_flags
        candidates.append(output)
    candidates.sort(
        key=lambda item: (
            item["current_payment_intent_visits"],
            item["absolute_change"],
        ),
        reverse=True,
    )
    return candidates[:limit]


def build_rolling_report(
    db_path: str | Path,
    *,
    start_month: str,
    end_month: str,
    targets: list[str] | None = None,
    min_current_visits: float = 1000,
    min_months_present: int = 3,
    breakout_growth_rate: float = 1.0,
    max_domain_age_days: int = 730,
    limit: int = 20,
) -> dict[str, Any]:
    if min_months_present < 1:
        raise ValueError("min_months_present must be at least 1")
    if limit < 1:
        raise ValueError("limit must be at least 1")
    months = _month_sequence(start_month, end_month)
    path = initialize_database(db_path)
    with closing(sqlite3.connect(path)) as connection:
        connection.row_factory = sqlite3.Row
        snapshot_rows = connection.execute(
            """
            SELECT target_domain, month, complete
            FROM referral_snapshots
            WHERE month BETWEEN ? AND ?
            """,
            (start_month, end_month),
        ).fetchall()
        selected_targets = (
            [
                domain
                for value in targets
                if (domain := normalize_domain(value))
            ]
            if targets
            else sorted({row["target_domain"] for row in snapshot_rows})
        )
        snapshot_status = {
            (row["target_domain"], row["month"]): bool(row["complete"])
            for row in snapshot_rows
        }
        coverage_errors = []
        for target in selected_targets:
            for month in months:
                status = snapshot_status.get((target, month))
                if status is None:
                    coverage_errors.append(f"{target}:{month}=missing")
                elif not status:
                    coverage_errors.append(f"{target}:{month}=incomplete")
        if coverage_errors:
            raise ValueError(
                "Rolling report requires complete snapshots: "
                + ", ".join(coverage_errors)
            )
        data_rows = connection.execute(
            """
            SELECT
                snapshots.target_domain,
                snapshots.month,
                rows.source_domain,
                rows.position,
                rows.global_rank,
                rows.month_abs_visits,
                rows.category
            FROM referral_rows AS rows
            JOIN referral_snapshots AS snapshots
                ON snapshots.id = rows.snapshot_id
            WHERE snapshots.month BETWEEN ? AND ?
            """,
            (start_month, end_month),
        ).fetchall()
        profiles = _load_domain_profiles(connection)

    selected_target_set = set(selected_targets)
    grouped: dict[
        tuple[str, str],
        dict[str, dict[str, Any]],
    ] = {}
    for row in data_rows:
        if row["target_domain"] not in selected_target_set:
            continue
        key = (row["target_domain"], row["source_domain"])
        grouped.setdefault(key, {})[row["month"]] = dict(row)

    sustained_growth = []
    breakouts = []
    newly_visible = []
    as_of = _month_end(end_month)
    recent_months = months[-3:]
    recent_visibility_months = set(months[-2:])
    for (target_domain, source_domain), by_month in grouped.items():
        if is_platform_domain(source_domain):
            continue
        current = by_month.get(end_month)
        if not current:
            continue
        current_visits = float(current["month_abs_visits"] or 0)
        if current_visits < min_current_visits:
            continue
        present_months = [month for month in months if month in by_month]
        series = [
            {
                "month": month,
                "present": month in by_month,
                "position": (
                    by_month[month]["position"]
                    if month in by_month
                    else None
                ),
                "visits": (
                    float(by_month[month]["month_abs_visits"] or 0)
                    if month in by_month
                    else None
                ),
            }
            for month in months
        ]
        positive_growth_steps = 0
        for previous_month, current_step_month in zip(months, months[1:]):
            previous_row = by_month.get(previous_month)
            current_step_row = by_month.get(current_step_month)
            if (
                previous_row
                and current_step_row
                and float(current_step_row["month_abs_visits"] or 0)
                > float(previous_row["month_abs_visits"] or 0)
            ):
                positive_growth_steps += 1
        item = {
            "target_domain": target_domain,
            "source_domain": source_domain,
            "current_position": current["position"],
            "current_visits": current_visits,
            "global_rank": current["global_rank"],
            "category": current["category"],
            "first_seen_month": present_months[0],
            "months_present": len(present_months),
            "positive_growth_steps": positive_growth_steps,
            "series": series,
        }
        item = _attach_profile(item, profiles, as_of=as_of)
        risk_flags = []
        if target_domain == "paypal.com":
            risk_flags.append("paypal_broad_intent")
        if not current["category"] or current["category"] == "Unknown":
            risk_flags.append("unknown_category")
        if item.get("rdap_status") != "ok":
            risk_flags.append("rdap_unavailable")
        item["risk_flags"] = risk_flags

        recent_rows = [by_month.get(month) for month in recent_months]
        if len(recent_rows) == 3 and all(recent_rows):
            recent_visits = [
                float(row["month_abs_visits"] or 0)
                for row in recent_rows
            ]
            recent_absolute_growth = recent_visits[-1] - recent_visits[0]
            recent_growth_rate = (
                recent_absolute_growth / recent_visits[0]
                if recent_visits[0] > 0
                else None
            )
            recent_position_gain = (
                recent_rows[0]["position"] - recent_rows[-1]["position"]
            )
            item.update(
                {
                    "recent_absolute_growth": recent_absolute_growth,
                    "recent_growth_rate": recent_growth_rate,
                    "recent_position_gain": recent_position_gain,
                }
            )
            if (
                len(present_months) >= min_months_present
                and recent_visits[0] < recent_visits[1] < recent_visits[2]
            ):
                sustained_growth.append(dict(item))

        previous = (
            by_month.get(months[-2])
            if len(months) >= 2
            else None
        )
        if previous:
            previous_visits = float(previous["month_abs_visits"] or 0)
            absolute_growth = current_visits - previous_visits
            growth_rate = (
                absolute_growth / previous_visits
                if previous_visits > 0
                else None
            )
            if (
                growth_rate is not None
                and growth_rate >= breakout_growth_rate
            ):
                breakouts.append(
                    {
                        **item,
                        "previous_visits": previous_visits,
                        "absolute_growth": absolute_growth,
                        "growth_rate": growth_rate,
                    }
                )
        if present_months[0] in recent_visibility_months:
            newly_visible.append(dict(item))

    sustained_growth.sort(
        key=lambda item: (
            item.get("recent_absolute_growth", 0),
            item["current_visits"],
        ),
        reverse=True,
    )
    breakouts.sort(
        key=lambda item: (
            item["absolute_growth"],
            item["growth_rate"],
        ),
        reverse=True,
    )
    newly_visible.sort(
        key=lambda item: (
            item["current_visits"],
            -item["current_position"],
        ),
        reverse=True,
    )
    young_sustained_growth = [
        item
        for item in sustained_growth
        if item.get("domain_age_days") is not None
        and item["domain_age_days"] <= max_domain_age_days
    ]
    return {
        "start_month": start_month,
        "end_month": end_month,
        "months": months,
        "targets": selected_targets,
        "coverage": {
            "required_snapshots": len(months) * len(selected_targets),
            "complete_snapshots": len(months) * len(selected_targets),
        },
        "thresholds": {
            "min_current_visits": min_current_visits,
            "min_months_present": min_months_present,
            "breakout_growth_rate": breakout_growth_rate,
            "max_domain_age_days": max_domain_age_days,
        },
        "sustained_growth": sustained_growth[:limit],
        "breakouts": breakouts[:limit],
        "newly_visible": newly_visible[:limit],
        "young_sustained_growth": young_sustained_growth[:limit],
    }


def build_opportunity_report(
    db_path: str | Path,
    *,
    current_month: str,
    previous_month: str,
    targets: list[str] | None = None,
    min_current_visits: float = 1000,
    min_previous_visits: float = 250,
    limit: int = 20,
    max_domain_age_days: int = 730,
    site_traffic_months: int = 6,
) -> dict[str, Any]:
    if limit < 1:
        raise ValueError("limit must be at least 1")
    if site_traffic_months < 1:
        raise ValueError("site_traffic_months must be at least 1")
    traffic_start_month = _shift_month(current_month, -(site_traffic_months - 1))
    path = initialize_database(db_path)
    with closing(sqlite3.connect(path)) as connection:
        current = _load_month_rows(connection, current_month)
        previous = _load_month_rows(connection, previous_month)
        profiles = _load_domain_profiles(connection)
        snapshot_status = _load_snapshot_status(
            connection,
            [previous_month, current_month],
        )
        website_traffic_by_domain = _load_website_traffic(
            connection,
            traffic_start_month,
            current_month,
        )
    selected_targets = (
        [domain for value in targets if (domain := normalize_domain(value))]
        if targets
        else sorted(
            target
            for target, month in snapshot_status
            if month == current_month
        )
    )
    coverage_errors = []
    for target in selected_targets:
        for month in (previous_month, current_month):
            status = snapshot_status.get((target, month))
            if status is None:
                coverage_errors.append(f"{target}:{month}=missing")
            elif not status:
                coverage_errors.append(f"{target}:{month}=incomplete")
    if coverage_errors:
        raise ValueError(
            "Opportunity report requires complete snapshots: "
            + ", ".join(coverage_errors)
        )
    target_set = set(selected_targets)
    current = {
        key: value
        for key, value in current.items()
        if key[0] in target_set
    }
    previous = {
        key: value
        for key, value in previous.items()
        if key[0] in target_set
    }

    fast_rank_growth = []
    rank_risers = []
    traffic_gainers = []
    newcomers = []
    for key, current_row in current.items():
        target_domain, source_domain = key
        if is_platform_domain(source_domain):
            continue
        current_visits = float(current_row["month_abs_visits"] or 0)
        previous_row = previous.get(key)
        shared = {
            "target_domain": target_domain,
            "source_domain": source_domain,
            "current_position": current_row["position"],
            "current_visits": current_visits,
            "global_rank": current_row["global_rank"],
            "category": current_row["category"],
        }
        if previous_row is not None:
            previous_visits = float(
                previous_row["month_abs_visits"] or 0
            )
            rank_gain = (
                previous_row["position"] - current_row["position"]
            )
            if rank_gain > 0:
                fast_rank_growth.append(
                    {
                        **shared,
                        "previous_position": previous_row["position"],
                        "previous_visits": previous_visits,
                        "rank_gain": rank_gain,
                    }
                )
        if current_visits < min_current_visits:
            continue
        if previous_row is None:
            newcomers.append(shared)
            continue
        previous_visits = float(previous_row["month_abs_visits"] or 0)
        if previous_visits < min_previous_visits:
            continue
        rank_gain = previous_row["position"] - current_row["position"]
        absolute_growth = current_visits - previous_visits
        evidence = {
            **shared,
            "previous_position": previous_row["position"],
            "previous_visits": previous_visits,
        }
        if rank_gain > 0:
            rank_risers.append({**evidence, "rank_gain": rank_gain})
        if absolute_growth > 0:
            traffic_gainers.append(
                {
                    **evidence,
                    "absolute_growth": absolute_growth,
                    "growth_rate": absolute_growth / previous_visits,
                }
            )

    fast_rank_growth.sort(
        key=lambda item: (item["rank_gain"], item["current_visits"]),
        reverse=True,
    )
    rank_risers.sort(
        key=lambda item: (item["rank_gain"], item["current_visits"]),
        reverse=True,
    )
    traffic_gainers.sort(
        key=lambda item: (item["absolute_growth"], item["growth_rate"]),
        reverse=True,
    )
    newcomers.sort(
        key=lambda item: (item["current_visits"], -item["current_position"]),
        reverse=True,
    )
    as_of = _month_end(current_month)
    fast_rank_growth = [
        _attach_profile(item, profiles, as_of=as_of)
        for item in fast_rank_growth[:limit]
    ]
    rank_risers = [
        _attach_profile(item, profiles, as_of=as_of)
        for item in rank_risers[:limit]
    ]
    traffic_gainers = [
        _attach_profile(item, profiles, as_of=as_of)
        for item in traffic_gainers[:limit]
    ]
    newcomers = [
        _attach_profile(item, profiles, as_of=as_of)
        for item in newcomers[:limit]
    ]
    combined: dict[tuple[str, str], dict[str, Any]] = {}
    for signal, items in (
        ("rank_riser", rank_risers),
        ("traffic_gainer", traffic_gainers),
        ("newcomer", newcomers),
    ):
        for item in items:
            age = item.get("domain_age_days")
            if age is None or age > max_domain_age_days:
                continue
            key = (item["target_domain"], item["source_domain"])
            candidate = combined.setdefault(key, {**item, "signals": []})
            candidate["signals"].append(signal)
    young_growth_candidates = sorted(
        combined.values(),
        key=lambda item: (item["current_visits"], -item["domain_age_days"]),
        reverse=True,
    )[:limit]
    category_conclusions = _category_conclusions(current, previous)
    new_product_growth = _new_product_growth(
        current,
        previous,
        profiles,
        min_current_visits=min_current_visits,
        min_previous_visits=min_previous_visits,
        max_domain_age_days=max_domain_age_days,
        as_of=as_of,
        limit=limit,
    )
    fast_rank_growth = [
        _attach_website_traffic(item, website_traffic_by_domain)
        for item in fast_rank_growth
    ]
    rank_risers = [
        _attach_website_traffic(item, website_traffic_by_domain)
        for item in rank_risers
    ]
    traffic_gainers = [
        _attach_website_traffic(item, website_traffic_by_domain)
        for item in traffic_gainers
    ]
    newcomers = [
        _attach_website_traffic(item, website_traffic_by_domain)
        for item in newcomers
    ]
    young_growth_candidates = [
        _attach_website_traffic(item, website_traffic_by_domain)
        for item in young_growth_candidates
    ]
    new_product_growth = [
        _attach_website_traffic(item, website_traffic_by_domain)
        for item in new_product_growth
    ]
    return {
        "current_month": current_month,
        "previous_month": previous_month,
        "targets": selected_targets,
        "website_traffic_window": {
            "start_month": traffic_start_month,
            "end_month": current_month,
            "months": site_traffic_months,
        },
        "thresholds": {
            "min_current_visits": min_current_visits,
            "min_previous_visits": min_previous_visits,
            "max_domain_age_days": max_domain_age_days,
            "site_traffic_months": site_traffic_months,
        },
        "rank_risers": rank_risers,
        "fast_rank_growth": fast_rank_growth,
        "traffic_gainers": traffic_gainers,
        "newcomers": newcomers,
        "young_growth_candidates": young_growth_candidates,
        "category_conclusions": category_conclusions,
        "new_product_growth": new_product_growth,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Collect payment-platform referral snapshots and compare monthly "
            "growth opportunities."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect_parser = subparsers.add_parser(
        "collect",
        help="Collect complete SimilarWeb referral snapshots into SQLite.",
    )
    collect_parser.add_argument(
        "--db",
        default=str(DEFAULT_DATABASE),
        help="SQLite database path",
    )
    collect_parser.add_argument(
        "--target",
        action="append",
        help="Target payment domain. Repeat for multiple targets.",
    )
    collect_parser.add_argument(
        "--month",
        action="append",
        required=True,
        help="Snapshot month in YYYY-MM format. Repeat for multiple months.",
    )
    report_parser = subparsers.add_parser(
        "report",
        help="Compare two stored months and output opportunity rankings.",
    )
    report_parser.add_argument(
        "--db",
        default=str(DEFAULT_DATABASE),
        help="SQLite database path",
    )
    report_parser.add_argument("--current-month", required=True)
    report_parser.add_argument("--previous-month", required=True)
    report_parser.add_argument(
        "--target",
        action="append",
        help="Only report one payment target. Repeat for multiple targets.",
    )
    report_parser.add_argument("--limit", type=int, default=20)
    report_parser.add_argument(
        "--min-current-visits",
        type=float,
        default=1000,
    )
    report_parser.add_argument(
        "--min-previous-visits",
        type=float,
        default=250,
    )

    traffic_enrich_parser = subparsers.add_parser(
        "traffic-enrich",
        help="Collect monthly total-site traffic for selected opportunity candidates.",
    )
    traffic_enrich_parser.add_argument(
        "--db",
        default=str(DEFAULT_DATABASE),
        help="SQLite database path",
    )
    traffic_enrich_parser.add_argument("--current-month", required=True)
    traffic_enrich_parser.add_argument("--previous-month", required=True)
    traffic_enrich_parser.add_argument("--start-month", required=True)
    traffic_enrich_parser.add_argument("--end-month", required=True)
    traffic_enrich_parser.add_argument(
        "--target",
        action="append",
        help="Only select candidates from one payment target. Repeatable.",
    )
    traffic_enrich_parser.add_argument(
        "--source-domain",
        action="append",
        help="Override candidate selection with an explicit website. Repeatable.",
    )
    traffic_enrich_parser.add_argument("--limit", type=int, default=20)
    traffic_enrich_parser.add_argument(
        "--min-current-visits",
        type=float,
        default=1000,
    )
    traffic_enrich_parser.add_argument(
        "--min-previous-visits",
        type=float,
        default=250,
    )
    traffic_enrich_parser.add_argument(
        "--batch-size", type=int, default=MAX_TRAFFIC_TREND_BATCH
    )

    rolling_parser = subparsers.add_parser(
        "rolling-report",
        help="Analyze sustained growth across a complete month range.",
    )
    rolling_parser.add_argument(
        "--db",
        default=str(DEFAULT_DATABASE),
        help="SQLite database path",
    )
    rolling_parser.add_argument("--start-month", required=True)
    rolling_parser.add_argument("--end-month", required=True)
    rolling_parser.add_argument(
        "--target",
        action="append",
        help="Only report one payment target. Repeat for multiple targets.",
    )
    rolling_parser.add_argument("--limit", type=int, default=20)
    rolling_parser.add_argument(
        "--min-current-visits",
        type=float,
        default=1000,
    )
    rolling_parser.add_argument(
        "--min-months-present",
        type=int,
        default=3,
    )
    rolling_parser.add_argument(
        "--breakout-growth-rate",
        type=float,
        default=1.0,
        help="Minimum latest-month growth rate for breakouts.",
    )
    rolling_parser.add_argument(
        "--max-domain-age-days",
        type=int,
        default=730,
    )

    rolling_enrich_parser = subparsers.add_parser(
        "rolling-enrich",
        help="Enrich candidates from a complete rolling month range.",
    )
    rolling_enrich_parser.add_argument(
        "--db",
        default=str(DEFAULT_DATABASE),
        help="SQLite database path",
    )
    rolling_enrich_parser.add_argument("--start-month", required=True)
    rolling_enrich_parser.add_argument("--end-month", required=True)
    rolling_enrich_parser.add_argument(
        "--target",
        action="append",
        help="Only enrich one payment target. Repeat for multiple targets.",
    )
    rolling_enrich_parser.add_argument("--limit", type=int, default=20)
    rolling_enrich_parser.add_argument(
        "--min-current-visits",
        type=float,
        default=1000,
    )
    rolling_enrich_parser.add_argument(
        "--min-months-present",
        type=int,
        default=3,
    )
    rolling_enrich_parser.add_argument(
        "--breakout-growth-rate",
        type=float,
        default=1.0,
    )
    rolling_enrich_parser.add_argument(
        "--max-domain-age-days",
        type=int,
        default=730,
    )
    rolling_enrich_parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore fresh cached profiles.",
    )

    enrich_parser = subparsers.add_parser(
        "enrich",
        help="Enrich opportunity candidates with authoritative RDAP data.",
    )
    enrich_parser.add_argument(
        "--db",
        default=str(DEFAULT_DATABASE),
        help="SQLite database path",
    )
    enrich_parser.add_argument("--current-month", required=True)
    enrich_parser.add_argument("--previous-month", required=True)
    enrich_parser.add_argument(
        "--target",
        action="append",
        help="Only enrich one payment target. Repeat for multiple targets.",
    )
    enrich_parser.add_argument("--limit", type=int, default=20)
    enrich_parser.add_argument(
        "--min-current-visits",
        type=float,
        default=1000,
    )
    enrich_parser.add_argument(
        "--min-previous-visits",
        type=float,
        default=250,
    )
    enrich_parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore fresh cached profiles.",
    )

    args = parser.parse_args(argv)
    if args.command == "collect":
        output = collect_snapshots(
            args.db,
            targets=args.target or list(DEFAULT_TARGETS),
            months=args.month,
            fetcher=create_live_fetcher(),
        )
    elif args.command == "traffic-enrich":
        report = build_opportunity_report(
            args.db,
            current_month=args.current_month,
            previous_month=args.previous_month,
            targets=args.target,
            min_current_visits=args.min_current_visits,
            min_previous_visits=args.min_previous_visits,
            limit=args.limit,
        )
        output = collect_website_traffic(
            args.db,
            domains=args.source_domain or report_candidate_domains(report),
            start_month=args.start_month,
            end_month=args.end_month,
            fetcher=create_live_website_traffic_fetcher(),
            batch_size=args.batch_size,
        )

    elif args.command == "report":
        output = build_opportunity_report(
            args.db,
            current_month=args.current_month,
            previous_month=args.previous_month,
            targets=args.target,
            min_current_visits=args.min_current_visits,
            min_previous_visits=args.min_previous_visits,
            limit=args.limit,
        )
    elif args.command == "rolling-report":
        output = build_rolling_report(
            args.db,
            start_month=args.start_month,
            end_month=args.end_month,
            targets=args.target,
            min_current_visits=args.min_current_visits,
            min_months_present=args.min_months_present,
            breakout_growth_rate=args.breakout_growth_rate,
            max_domain_age_days=args.max_domain_age_days,
            limit=args.limit,
        )
    elif args.command == "rolling-enrich":
        report = build_rolling_report(
            args.db,
            start_month=args.start_month,
            end_month=args.end_month,
            targets=args.target,
            min_current_visits=args.min_current_visits,
            min_months_present=args.min_months_present,
            breakout_growth_rate=args.breakout_growth_rate,
            max_domain_age_days=args.max_domain_age_days,
            limit=args.limit,
        )
        output = enrich_domains(
            args.db,
            report_candidate_domains(report),
            fetcher=create_live_rdap_fetcher(),
            force=args.force,
        )
    else:
        report = build_opportunity_report(
            args.db,
            current_month=args.current_month,
            previous_month=args.previous_month,
            targets=args.target,
            min_current_visits=args.min_current_visits,
            min_previous_visits=args.min_previous_visits,
            limit=args.limit,
        )
        output = enrich_domains(
            args.db,
            report_candidate_domains(report),
            fetcher=create_live_rdap_fetcher(),
            force=args.force,
        )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
