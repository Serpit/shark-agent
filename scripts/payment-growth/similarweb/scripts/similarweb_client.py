from __future__ import annotations

import argparse
import base64
import calendar
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qsl, quote, urlparse

import requests

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from shared.env_loader import (
    discover_default_env_file as shared_discover_default_env_file,
    iter_env_file_candidates as shared_iter_env_file_candidates,
    load_project_env as shared_load_project_env,
    read_env_file_values,
)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/147.0.0.0 Safari/537.36"
)
SKILL_DIR = Path(__file__).resolve().parents[1]
STATE_DIR = SKILL_DIR / "state"
TOKEN_CACHE_PATH = STATE_DIR / "token_cache.json"
LOGIN_URL = "https://dash.3ue.com/api/account/login"
SUGGEST_URL = "https://sim.3ue.com/api/KeywordGenerator/google/suggest"
SIMILARWEB_DATA_BASE_URL = "https://sim.3ue.com"
DEFAULT_SIMILARWEB_PAGE_TEMPLATE = (
    "https://pro.similarweb.com/#/digitalsuite/acquisition/keyword/organic/search/"
    "{country}/{month_path}/overview_2?keyword={keyword}&tab=0&mtd=false&webSource={web_source}"
    "&graphGranularity=Weekly&graphDuration=1m"
)
DEFAULT_WEBSITE_PAGE_TEMPLATE = (
    "https://pro.similarweb.com/#/digitalsuite/websiteanalysis/overview/website-performance/"
    "*/{country}/1m?webSource={web_source}&key={domain}"
)
DEFAULT_LANDING_PAGES_PAGE_TEMPLATE = (
    "https://pro.similarweb.com/#/digitalsuite/acquisition/search/organic/"
    "pageAnalysis/landing-pages-v2/*/{country}/{month_path}?key={domain}"
    "&pageFilter={page_filter}&webSource={web_source}&Change={change}"
)
DEFAULT_SEARCH_KEYWORDS_PAGE_TEMPLATE = (
    "https://pro.similarweb.com/#/digitalsuite/acquisition/search/organic/"
    "pageAnalysis/website-keyword-v2/*/{country}/{month_path}?key={domain}"
    "&pageFilter={page_filter}&webSource={web_source}&Change={change}"
)
REFERRAL_TABLE_PAGE_SIZE = 100

KEYWORD_DATA_PATTERNS = (
    "/api/KeywordAnalysis/Overview/Stats",
    "/api/KeywordAnalysis/Overview/VolumeClicksTrend",
    "/api/KeywordAnalysis/Overview/TopSites",
    "/api/KeywordAnalysis/Overview/TopPages",
    "/api/KeywordGenerator/google/suggest",
    "/widgetApi/KeywordAnalysisV2/KeywordAnalysisOrganic/DeviceTraffic",
    "/widgetApi/MobileTrafficV2/MobileTraffic/SingleMetric",
    "/autocomplete/keywords",
    "/autocomplete/websites",
    "/api/images/",
)

WEBSITE_DATA_PATTERNS = (
    "/api/AdIntelligence/",
    "/api/backlinks/",
    "/api/ConversionRates/",
    "/api/searchoverview/",
    "/api/websiteanalysis/",
    "/api/WebsiteOverview/",
    "/api/websiteOrganicLandingPagesV2",
    "/widgetApi/AssetsCompare/",
    "/widgetApi/MarketingMixTotal/",
    "/widgetApi/SearchKeywordsV2/",
    "/widgetApi/TrafficAndEngagement/",
    "/widgetApi/TrafficSourcesSearchV2/",
    "/widgetApi/WebNewVsReturning/",
    "/widgetApi/WebsiteAnalysisV2/",
    "/widgetApi/WebsiteGeography/",
    "/widgetApi/WebsiteOverview/",
    "/widgetApi/WebsiteOverviewDesktop/",
)

INTERNAL_PATTERNS = (
    "/api/userdata/",
    "/api/activation/",
    "/api/account/collaborationHubLink",
    "/api/api-management/user-keys",
    "/api/PerformanceAddOn/MutualAssets",
    "/api/fit-score",
    "/api/googletag",
    "/api/identities",
    "/api/startupSettings",
    "/i18n/",
    "/image",
    "/css2",
    "/telemetry",
    "/sales-api/",
    "/settings",
)

CONTROL_PLANE_PATTERNS = (
    "/api/account/",
    "/api/subscription/",
    "/api/config/",
    "/api/notice/",
    "/api/auditing/",
    "/api/balance/",
    "/mitmApi/",
)

SENSITIVE_QUERY_KEYS = ("username", "password", "token", "refreshToken", "__gmitm")
SENSITIVE_JSON_KEYS = (
    "username",
    "password",
    "token",
    "refreshToken",
    "authorization",
    "cookie",
)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def discover_default_env_file(project: str | None = None) -> Path:
    return shared_discover_default_env_file(project=project)


DEFAULT_ENV_FILE = discover_default_env_file()


def load_project_env(env_file: str | None = None, project: str | None = None) -> Path:
    return shared_load_project_env(env_file, project=project)


def redact_sensitive_text(text: str) -> str:
    redacted = text
    for key in SENSITIVE_QUERY_KEYS:
        redacted = re.sub(
            rf"([?&]{re.escape(key)}=)[^&\"'\s]+",
            rf"\1<redacted>",
            redacted,
            flags=re.IGNORECASE,
        )
    for key in SENSITIVE_JSON_KEYS:
        redacted = re.sub(
            rf'("{re.escape(key)}"\s*:\s*")[^"]+(")',
            rf'\1<redacted>\2',
            redacted,
            flags=re.IGNORECASE,
        )
    return redacted


def parse_json_text(text: str) -> Any | None:
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def sample_shape(value: Any, depth: int = 0) -> Any:
    if depth >= 2:
        return type(value).__name__
    if isinstance(value, dict):
        return {key: sample_shape(item, depth + 1) for key, item in list(value.items())[:10]}
    if isinstance(value, list):
        if not value:
            return []
        return [sample_shape(value[0], depth + 1)]
    return type(value).__name__


def classify_endpoint(host: str, path: str) -> str:
    if host == "dash.3ue.com":
        return "control_plane"
    if any(path.startswith(prefix) for prefix in KEYWORD_DATA_PATTERNS):
        return "data"
    if any(path.startswith(prefix) for prefix in WEBSITE_DATA_PATTERNS):
        return "data"
    if any(path.startswith(prefix) for prefix in INTERNAL_PATTERNS):
        return "internal"
    if any(path.startswith(prefix) for prefix in CONTROL_PLANE_PATTERNS):
        return "control_plane"
    return "other"


def summarize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    request = entry.get("request", {})
    response = entry.get("response", {})
    parsed = urlparse(request.get("url", ""))
    response_text = response.get("content", {}).get("text", "") or ""
    response_json = parse_json_text(response_text)
    post_data = request.get("postData", {})
    request_body = post_data.get("text", "") or ""
    if str(post_data.get("mimeType", "")).lower().startswith("multipart/form-data"):
        request_body = "<multipart form data omitted>"
    else:
        request_body = redact_sensitive_text(request_body)[:400]

    return {
        "host": parsed.netloc,
        "path": parsed.path,
        "method": request.get("method", "GET"),
        "status": response.get("status", 0),
        "mime_type": response.get("content", {}).get("mimeType", ""),
        "query_keys": sorted({key for key, _ in parse_qsl(parsed.query, keep_blank_values=True)}),
        "response_keys": list(response_json.keys())[:10] if isinstance(response_json, dict) else [],
        "response_shape": sample_shape(response_json) if response_json is not None else None,
        "request_body": request_body,
        "sanitized_url": redact_sensitive_text(request.get("url", "")),
        "sanitized_response_excerpt": redact_sensitive_text(response_text[:400]),
    }


def summarize_har_entries(entries: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for entry in entries:
        item = summarize_entry(entry)
        key = (item["host"], item["path"], item["method"])
        grouped.setdefault(key, []).append(item)

    buckets = {
        "data_endpoints": [],
        "internal_endpoints": [],
        "control_plane_endpoints": [],
        "other_endpoints": [],
    }
    for (host, path, method), items in sorted(grouped.items(), key=lambda value: value[0]):
        category = classify_endpoint(host, path)
        statuses = Counter(item["status"] for item in items)
        query_keys = sorted({key for item in items for key in item["query_keys"]})
        response_keys = []
        for item in items:
            for key in item["response_keys"]:
                if key not in response_keys:
                    response_keys.append(key)
        record = {
            "host": host,
            "path": path,
            "method": method,
            "hits": len(items),
            "statuses": dict(statuses),
            "query_keys": query_keys,
            "response_keys": response_keys[:15],
            "response_shape": next((item["response_shape"] for item in items if item["response_shape"] is not None), None),
            "sample_url": items[0]["sanitized_url"],
            "sample_request_body": items[0]["request_body"],
            "sample_response_excerpt": items[0]["sanitized_response_excerpt"],
        }
        if category == "data":
            buckets["data_endpoints"].append(record)
        elif category == "internal":
            buckets["internal_endpoints"].append(record)
        elif category == "control_plane":
            buckets["control_plane_endpoints"].append(record)
        else:
            buckets["other_endpoints"].append(record)
    return buckets


def build_month_window(month: str) -> tuple[str, str]:
    year_str, month_str = month.split("-", 1)
    year = int(year_str)
    month_number = int(month_str)
    last_day = calendar.monthrange(year, month_number)[1]
    return f"{year:04d}|{month_number:02d}|01", f"{year:04d}|{month_number:02d}|{last_day:02d}"


def build_month_range(from_month: str, to_month: str) -> tuple[str, str]:
    start_date, _ = build_month_window(from_month)
    _, end_date = build_month_window(to_month)
    if start_date > end_date:
        raise ValueError("from_month must not be later than to_month")
    return start_date, end_date


def build_headers(
    *,
    cookie: str | None = None,
    x_sw_page: str | None = None,
    x_sw_page_view_id: str | None = None,
    user_agent: str = DEFAULT_USER_AGENT,
) -> dict[str, str]:
    headers = {
        "accept": "application/json",
        "content-type": "application/json; charset=utf-8",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": user_agent,
    }
    if cookie:
        headers["cookie"] = cookie
    if x_sw_page:
        headers["x-sw-page"] = x_sw_page
    if x_sw_page_view_id:
        headers["x-sw-page-view-id"] = x_sw_page_view_id
    return headers


def build_authenticated_headers(
    *,
    token: str,
    username: str | None = None,
    x_sw_page: str | None = None,
    x_sw_page_view_id: str | None = None,
    user_agent: str = DEFAULT_USER_AGENT,
) -> dict[str, str]:
    headers = build_headers(
        x_sw_page=x_sw_page,
        x_sw_page_view_id=x_sw_page_view_id,
        user_agent=user_agent,
    )
    headers["authorization"] = f"Bearer {token}"
    headers["cookie"] = build_token_cookie_header(token=token, username=username)
    return headers


def decode_jwt_payload(token: str) -> dict[str, Any]:
    jwt_part = token.split("|", 1)[0]
    parts = jwt_part.split(".")
    if len(parts) < 2:
        return {}
    payload = parts[1]
    padding = "=" * (-len(payload) % 4)
    try:
        decoded = base64.urlsafe_b64decode(payload + padding)
        obj = json.loads(decoded.decode("utf-8"))
        if isinstance(obj, dict):
            return obj
    except Exception:
        return {}
    return {}


def extract_token_expiry(token: str) -> datetime | None:
    payload = decode_jwt_payload(token)
    exp = payload.get("exp")
    if not isinstance(exp, int):
        return None
    return datetime.fromtimestamp(exp, tz=timezone.utc)


def is_token_usable(token: str, *, min_ttl_seconds: int = 60, current_time: datetime | None = None) -> bool:
    expires_at = extract_token_expiry(token)
    if expires_at is None:
        return False
    current = current_time or now_utc()
    return expires_at.timestamp() - current.timestamp() > min_ttl_seconds


def _append_env_candidate(paths: list[Path], seen: set[Path], path: Path) -> None:
    try:
        resolved = path.expanduser().resolve()
    except OSError:
        resolved = path.expanduser()
    if resolved in seen or not resolved.exists():
        return
    seen.add(resolved)
    paths.append(resolved)


def discover_auth_env_files(
    *,
    env_file: str | None = None,
    project: str | None = None,
    start_dir: str | Path | None = None,
    caller_dir: str | Path | None = None,
    home_dir: str | Path | None = None,
    skill_dir: str | Path | None = SKILL_DIR,
) -> list[Path]:
    paths = shared_iter_env_file_candidates(
        start_dir=start_dir,
        caller_dir=caller_dir,
        home_dir=home_dir,
        project=project,
        env_file=env_file,
    )
    if env_file:
        return paths

    seen = set(paths)
    resolved_skill_dir = Path(skill_dir).expanduser().resolve() if skill_dir else None
    for directory in ((resolved_skill_dir, *resolved_skill_dir.parents) if resolved_skill_dir else ()):
        _append_env_candidate(paths, seen, directory / ".env")
    return paths


def _stripped_value(values: dict[str, str], key: str) -> str:
    return str(values.get(key) or "").strip()


def resolve_auth_candidates(
    *,
    username: str | None,
    password: str | None,
    token: str | None = None,
    env_file: str | None = None,
    project: str | None = None,
    start_dir: str | Path | None = None,
    caller_dir: str | Path | None = None,
    home_dir: str | Path | None = None,
    skill_dir: str | Path | None = SKILL_DIR,
) -> list[dict[str, str]]:
    cli_username = (username or "").strip()
    cli_password = (password or "").strip()
    cli_token = (token or "").strip()

    files = discover_auth_env_files(
        env_file=env_file,
        project=project,
        start_dir=start_dir,
        caller_dir=caller_dir,
        home_dir=home_dir,
        skill_dir=skill_dir,
    )
    env_records: list[tuple[str, dict[str, str]]] = []
    for path in files:
        if env_file and not path.exists():
            raise FileNotFoundError(f"Env file does not exist: {path}")
        if path.exists():
            env_records.append((str(path), read_env_file_values(path)))
    env_records.append(("environment", dict(os.environ)))

    credential_candidates: list[dict[str, str]] = []
    token_candidates: list[dict[str, str]] = []
    for source, values in env_records:
        env_username = cli_username or _stripped_value(values, "SIMILARWEB_USERNAME")
        env_password = cli_password or _stripped_value(values, "SIMILARWEB_PASSWORD")
        if env_username and env_password:
            credential_candidates.append(
                {
                    "username": env_username,
                    "password": env_password,
                    "token": "",
                    "source": source,
                }
            )
        env_token = _stripped_value(values, "SIMILARWEB_TOKEN")
        if is_token_usable(env_token):
            token_candidates.append(
                {
                    "username": extract_username_from_token(env_token),
                    "password": "",
                    "token": env_token,
                    "source": source,
                }
            )

    if cli_username and cli_password:
        credential_candidates.insert(
            0,
            {
                "username": cli_username,
                "password": cli_password,
                "token": "",
                "source": "cli",
            },
        )
    if is_token_usable(cli_token):
        token_candidates.insert(
            0,
            {
                "username": extract_username_from_token(cli_token),
                "password": "",
                "token": cli_token,
                "source": "cli",
            },
        )

    deduped: list[dict[str, str]] = []
    seen_keys: set[tuple[str, str, str]] = set()
    for candidate in credential_candidates:
        key = (candidate["username"], candidate["password"], "")
        if key in seen_keys:
            continue
        seen_keys.add(key)
        deduped.append(candidate)
    for candidate in token_candidates:
        key = ("", "", candidate["token"])
        if key in seen_keys:
            continue
        seen_keys.add(key)
        deduped.append(candidate)
    return deduped


def extract_username_from_token(token: str) -> str:
    payload = decode_jwt_payload(token)
    username = payload.get("uname")
    return username.strip() if isinstance(username, str) else ""


def build_token_cookie_header(*, token: str, username: str | None = None) -> str:
    resolved_username = (username or extract_username_from_token(token)).strip()
    cookie_parts = [f"GMITM_token={token}"]
    if resolved_username:
        cookie_parts.append(f"GMITM_uname={quote(resolved_username)}")
    return "; ".join(cookie_parts)


def extract_login_token(payload: dict[str, Any]) -> str:
    if payload.get("c") != 0:
        message = payload.get("msg") or "unknown error"
        raise ValueError(f"Login failed: {message}")
    token = ((payload.get("data") or {}).get("token") or "").strip()
    if not token:
        raise ValueError("Login payload did not include a token")
    return token


def is_login_redirect_response(response: Any) -> bool:
    content_type = str(response.headers.get("content-type") or "").lower()
    if "text/html" not in content_type:
        return False
    text = str(getattr(response, "text", "") or "")
    return "location.href" in text and "dash.3ue.com" in text


def is_auth_failure(error: Exception) -> bool:
    if isinstance(error, requests.HTTPError):
        response = getattr(error, "response", None)
        status_code = getattr(response, "status_code", None)
        return status_code in (401, 403)
    message = str(error).lower()
    return (
        "similarweb session was rejected" in message
        or "login failed" in message
        or "fallback token" in message
        or "登录过期" in message
    )


def run_with_auth_candidates(
    candidates: list[dict[str, str]],
    operation,
    *,
    on_auth_failure: Callable[[dict[str, str]], bool] | None = None,
):
    if not candidates:
        raise ValueError(
            "Missing SimilarWeb credentials. Provide --username/--password, use --token as "
            "a fallback, or configure SIMILARWEB_USERNAME / SIMILARWEB_PASSWORD / "
            "SIMILARWEB_TOKEN in a project or global .env."
        )

    failures: list[str] = []
    for candidate in candidates:
        try:
            return operation(candidate)
        except Exception as error:
            if not is_auth_failure(error):
                raise
            is_explicit_login_failure = "login failed" in str(error).lower()
            if (
                not is_explicit_login_failure
                and on_auth_failure
                and on_auth_failure(candidate)
            ):
                try:
                    return operation(candidate)
                except Exception as retry_error:
                    if not is_auth_failure(retry_error):
                        raise
                    error = retry_error
            failures.append(f"{candidate.get('source', '<unknown>')}: {error}")
    raise RuntimeError(
        "All SimilarWeb auth candidates failed. "
        + "; ".join(failures)
    )


def build_keyword_page_url(*, keyword: str, month: str, country: str, web_source: str) -> str:
    month_path = month.replace("-", ".") + "-" + month.replace("-", ".")
    return DEFAULT_SIMILARWEB_PAGE_TEMPLATE.format(
        country=country,
        month_path=month_path,
        keyword=keyword.replace(" ", "%20"),
        web_source=web_source,
    )


def build_website_page_url(*, domain: str, country: str, web_source: str) -> str:
    return DEFAULT_WEBSITE_PAGE_TEMPLATE.format(
        country=country,
        domain=domain,
        web_source=web_source,
    )


def build_landing_pages_page_url(
    *,
    domain: str,
    month: str,
    country: str,
    web_source: str,
    change: str,
) -> str:
    month_path = month.replace("-", ".") + "-" + month.replace("-", ".")
    return DEFAULT_LANDING_PAGES_PAGE_TEMPLATE.format(
        country=country,
        domain=quote(domain),
        month_path=month_path,
        page_filter=quote(build_page_filter_json(domain), safe=""),
        web_source=web_source,
        change=quote(change),
    )


def build_search_keywords_page_url(
    *,
    domain: str,
    month: str,
    country: str,
    web_source: str,
    change: str,
) -> str:
    month_path = month.replace("-", ".") + "-" + month.replace("-", ".")
    return DEFAULT_SEARCH_KEYWORDS_PAGE_TEMPLATE.format(
        country=country,
        domain=quote(domain),
        month_path=month_path,
        page_filter=quote(build_page_filter_json(domain), safe=""),
        web_source=web_source,
        change=quote(change),
    )


def build_page_filter_json(domain: str) -> str:
    return json.dumps(
        [{"url": domain, "searchType": "domain"}],
        separators=(",", ":"),
    )


def build_keyword_bundle(
    *,
    keyword: str,
    month: str,
    country: str = "999",
    web_source: str = "Total",
    device: str = "Total",
    source_type: str = "all",
    duration: str = "1m",
    time_granularity: str = "Weekly",
) -> dict[str, Any]:
    start_date, end_date = build_month_window(month)
    shared_query = {
        "from": start_date,
        "to": end_date,
        "country": country,
        "isWindow": "false",
    }
    requests = [
        {
            "name": "overview_stats",
            "method": "GET",
            "path": "/api/KeywordAnalysis/Overview/Stats",
            "query": {
                **shared_query,
                "webSource": web_source,
                "key": keyword,
                "sort": "ClicksShare",
                "asc": "false",
                "includeSubDomains": "true",
                "Device": device,
            },
        },
        {
            "name": "volume_clicks_trend",
            "method": "GET",
            "path": "/api/KeywordAnalysis/Overview/VolumeClicksTrend",
            "query": {
                **shared_query,
                "device": device,
                "key": keyword,
                "timeGranularity": time_granularity,
                "duration": duration,
            },
        },
        {
            "name": "top_sites",
            "method": "GET",
            "path": "/api/KeywordAnalysis/Overview/TopSites",
            "query": {
                **shared_query,
                "device": device,
                "key": keyword,
                "sourceType": source_type,
            },
        },
        {
            "name": "top_pages",
            "method": "GET",
            "path": "/api/KeywordAnalysis/Overview/TopPages",
            "query": {
                **shared_query,
                "device": device,
                "key": keyword,
                "sourceType": source_type,
            },
        },
        {
            "name": "device_traffic",
            "method": "GET",
            "path": "/widgetApi/KeywordAnalysisV2/KeywordAnalysisOrganic/DeviceTraffic",
            "query": {
                **shared_query,
                "webSource": web_source,
                "keys": keyword,
                "sourceType": source_type,
                "includeSubDomains": "false",
                "Device": device,
            },
        },
        {
            "name": "single_metric",
            "method": "GET",
            "path": "/widgetApi/MobileTrafficV2/MobileTraffic/SingleMetric",
            "query": {
                **shared_query,
                "keys": keyword,
                "webSource": web_source,
                "sourceType": source_type,
                "GetlAllAvailableTrend": "true",
            },
        },
        {
            "name": "related_keywords",
            "method": "POST",
            "path": "/api/KeywordGenerator/google/suggest",
            "query": {
                **shared_query,
                "keyword": keyword,
                "webSource": web_source,
                "rowsPerPage": "5",
                "asc": "false",
                "sort": "score",
                "type": "Related",
            },
            "json_body": [],
        },
    ]
    return {
        "keyword": keyword,
        "month": month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "device": device,
        "requests": requests,
    }


def build_website_analysis_bundle(
    *,
    domain: str,
    month: str,
    country: str = "999",
    web_source: str = "Total",
    include_subdomains: bool = True,
    compare_domains: list[str] | None = None,
    category: str | None = None,
    page_size: int = 5,
    keyword_page_size: int = 100,
    time_granularity: str = "Monthly",
    source_type: str = "all",
) -> dict[str, Any]:
    start_date, end_date = build_month_window(month)
    include_subdomains_value = str(include_subdomains).lower()
    shared_query = {
        "country": country,
        "from": start_date,
        "to": end_date,
        "isWindow": "false",
        "webSource": web_source,
        "includeSubDomains": include_subdomains_value,
    }
    keys_for_compare = ",".join([domain, *(compare_domains or [])])
    page_filter_json = build_page_filter_json(domain)
    category_key = f"${category}" if category else None
    asset_compare_keys = ",".join(
        item for item in [domain, category_key] if item
    )
    requests = [
        {
            "name": "website_header",
            "method": "GET",
            "path": "/api/WebsiteOverview/getheader",
            "query": {
                "keys": domain,
                "mainDomainOnly": "true",
                "includeCrossData": "true",
            },
        },
        {
            "name": "similar_sites",
            "method": "GET",
            "path": "/api/WebsiteOverview/getsimilarsites",
            "query": {
                "key": domain,
                "limit": str(page_size),
                "webSource": web_source,
                "country": country,
            },
        },
        {
            "name": "engagement_visits_single_metric",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/EngagementVisits/SingleMetric",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
                "ShouldGetVerifiedData": "true",
            },
        },
        {
            "name": "engagement_desktop_mobile",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/EngagementDesktopVsMobileVisits/PieChart",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
                "ShouldGetVerifiedData": "true",
            },
        },
        {
            "name": "web_ranks",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/WebRanks/SingleMetric",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
            },
        },
        {
            "name": "engagement_overview",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/EngagementOverview/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
                "ShouldGetVerifiedData": "false",
                "ignoreFilterConsistency": "false",
                "iso": "[object Object]",
            },
        },
        {
            "name": "engagement_visits_graph",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/EngagementVisits/Graph",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": "Weekly",
                "ShouldGetVerifiedData": "false",
            },
        },
        {
            "name": "engagement_visits_table",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/EngagementVisits/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": "Weekly",
                "ShouldGetVerifiedData": "false",
            },
        },
        {
            "name": "geography",
            "method": "GET",
            "path": "/widgetApi/WebsiteGeography/Geography/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
                "orderBy": "TotalShare desc",
                "pageSize": str(page_size),
            },
        },
        {
            "name": "traffic_sources_pie",
            "method": "GET",
            "path": "/widgetApi/MarketingMixTotal/TrafficSourcesOverview/PieChart",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
            },
        },
        {
            "name": "traffic_sources_bar",
            "method": "GET",
            "path": "/widgetApi/MarketingMixTotal/TrafficSourcesOverview/BarChart",
            "query": {
                **shared_query,
                "keys": keys_for_compare,
            },
        },
        {
            "name": "traffic_sources_table",
            "method": "GET",
            "path": "/widgetApi/MarketingMixTotal/TrafficSourcesOverview/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
                "orderBy": "Share desc",
                "ignoreFilterConsistency": "false",
                "channelsOverviewViewByType": "null",
                "channelsOverviewDataFormatType": "null",
            },
        },
        {
            "name": "search_traffic",
            "method": "GET",
            "path": "/api/searchoverview/overview/traffic",
            "query": {
                **shared_query,
                "keys": domain,
            },
        },
        {
            "name": "search_keywords_overview",
            "method": "GET",
            "path": "/api/searchoverview/overview/keywords",
            "query": {
                **shared_query,
                "keys": domain,
                "SourceType": "organic",
            },
        },
        {
            "name": "search_brand_split",
            "method": "GET",
            "path": "/api/searchoverview/keywords/brand-split",
            "query": {
                **shared_query,
                "keys": domain,
            },
        },
        {
            "name": "search_rank_distribution",
            "method": "GET",
            "path": "/api/searchoverview/keywords/rank-distribution",
            "query": {
                **shared_query,
                "keys": domain,
            },
        },
        {
            "name": "search_top_keywords",
            "method": "GET",
            "path": "/api/searchoverview/overview/top-keywords",
            "query": {
                **shared_query,
                "keys": domain,
                "SourceType": "all",
                "pageSize": str(page_size),
            },
        },
        {
            "name": "search_keyword_table",
            "method": "GET",
            "path": "/widgetApi/SearchKeywordsV2/WebsitePerformance/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "SourceType": "Organic",
                "pageSize": str(page_size),
                "timeGranularity": time_granularity,
                "duration": "1m",
            },
        },
        {
            "name": "top_referrals",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/TopReferrals/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
                "orderBy": "TotalShare desc",
                "pageSize": str(page_size),
            },
        },
        {
            "name": "top_referring_categories",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/TopReferringCategories/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
                "orderBy": "TotalShare desc",
            },
        },
        {
            "name": "traffic_destination_referrals",
            "method": "GET",
            "path": "/widgetApi/WebsiteOverview/TrafficDestinationReferrals/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "timeGranularity": time_granularity,
                "orderBy": "TotalShare desc",
                "pageSize": str(page_size),
                "appMode": "single",
            },
        },
        {
            "name": "asset_compare_visits",
            "method": "GET",
            "path": "/widgetApi/AssetsCompare/Visits/Graph",
            "query": {
                **shared_query,
                "keys": asset_compare_keys,
                "timeGranularity": time_granularity,
                "ShouldGetVerifiedData": "false",
                "unBounced": "false",
            },
        },
        {
            "name": "asset_compare_duration",
            "method": "GET",
            "path": "/widgetApi/AssetsCompare/Duration/Graph",
            "query": {
                **shared_query,
                "keys": asset_compare_keys,
                "timeGranularity": time_granularity,
                "ShouldGetVerifiedData": "false",
                "unBounced": "false",
            },
        },
        {
            "name": "new_vs_returning",
            "method": "GET",
            "path": "/widgetApi/WebNewVsReturning/NewVsReturning/Data",
            "query": {
                **shared_query,
                "keys": domain,
            },
        },
        {
            "name": "advertiser_publishers",
            "method": "GET",
            "path": "/api/AdIntelligence/Advertiser/Publishers/breakdown",
            "query": {
                "country": country,
                "key": domain,
                "from": start_date,
                "to": end_date,
                "page": "1",
                "pageSize": str(page_size),
                "isWindow": "false",
                "sort": "visits",
                "asc": "false",
            },
        },
        {
            "name": "organic_landing_pages",
            "method": "POST",
            "path": "/api/websiteOrganicLandingPagesV2",
            "query": {
                **shared_query,
                "key": domain,
                "pageFilterJson": page_filter_json,
                "sort": "ClicksShare",
                "asc": "false",
                "sourceType": "paid",
            },
            "json_body": [],
        },
        {
            "name": "website_keywords_total",
            "method": "POST",
            "path": "/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/PresetsTotal",
            "query": {
                **shared_query,
                "keys": domain,
                "page": "1",
                "pageSize": str(keyword_page_size),
                "pageFilterJson": page_filter_json,
                "sourceType": source_type,
                "timeGranularity": time_granularity,
                "IncludeBranded": "false",
                "IncludeNoneBranded": "false",
                "iso": "[object Object]",
            },
            "json_body": [],
        },
        {
            "name": "website_keywords_table",
            "method": "POST",
            "path": "/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table",
            "query": {
                **shared_query,
                "keys": domain,
                "page": "1",
                "pageSize": str(keyword_page_size),
                "pageFilterJson": page_filter_json,
                "sourceType": source_type,
                "timeGranularity": time_granularity,
                "sort": "Share",
                "asc": "false",
                "IncludeBranded": "false",
                "IncludeNoneBranded": "false",
                "iso": "[object Object]",
            },
            "json_body": [],
        },
        {
            "name": "backlinks_summary",
            "method": "GET",
            "path": "/api/backlinks/summary",
            "query": {
                "Key": domain,
                "Status": "All",
            },
        },
        {
            "name": "backlinks_timeseries",
            "method": "GET",
            "path": "/api/backlinks/timeseries",
            "query": {
                "Key": domain,
                "from": start_date,
                "to": end_date,
                "isDaily": "true",
            },
        },
        {
            "name": "backlinks_new_lost",
            "method": "GET",
            "path": "/api/backlinks/timeseries/newlost",
            "query": {
                "Key": domain,
                "from": start_date,
                "to": end_date,
                "isDaily": "true",
            },
        },
        {
            "name": "backlinks_ref_domains",
            "method": "POST",
            "path": "/api/backlinks/refdomains",
            "query": {
                "Page": "1",
                "PageSize": str(keyword_page_size),
                "Status": "All",
                "Key": domain,
                "asc": "false",
                "sort": "BacklinksCount",
            },
            "json_body": [],
        },
        {
            "name": "backlinks",
            "method": "POST",
            "path": "/api/backlinks/backlinks",
            "query": {
                "Page": "1",
                "PageSize": str(keyword_page_size),
                "Status": "All",
                "FollowType": "All",
                "Key": domain,
                "asc": "false",
                "sort": "DomainScore",
            },
            "json_body": [],
        },
    ]
    return {
        "domain": domain,
        "month": month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "include_subdomains": include_subdomains,
        "compare_domains": compare_domains or [],
        "requests": requests,
    }


def build_referral_traffic_query(
    *,
    domain: str,
    from_month: str,
    to_month: str,
    country: str = "999",
    web_source: str = "Total",
    page: int = 1,
    sort: str = "TotalShare",
    asc: bool = False,
) -> dict[str, Any]:
    if page < 1:
        raise ValueError("page must be at least 1")
    start_date, end_date = build_month_range(from_month, to_month)
    asc_value = str(asc).lower()
    shared_query = {
        "key": domain,
        "isWWW": "false",
        "country": country,
        "iso": "[object Object]",
        "to": end_date,
        "from": start_date,
        "isWindow": "false",
        "webSource": web_source,
        "selectedTab": "incomingTraffic",
        "ignoreFilterConsistency": "false",
    }
    requests = [
        {
            "name": "referral_totals",
            "method": "GET",
            "path": "/api/websiteanalysis/GetTrafficSourcesTotalReferrals",
            "query": dict(shared_query),
        },
        {
            "name": "referral_table",
            "method": "GET",
            "path": "/api/websiteanalysis/GetTrafficSourcesTotalReferralsTable",
            "query": {
                **shared_query,
                "orderBy": f"{sort} {'asc' if asc else 'desc'}",
                "asc": asc_value,
                "page": str(page),
            },
        },
    ]
    return {
        "domain": domain,
        "from_month": from_month,
        "to_month": to_month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "page": page,
        "page_size": REFERRAL_TABLE_PAGE_SIZE,
        "sort": sort,
        "asc": asc,
        "requests": requests,
    }


def build_website_traffic_trend_query(
    *,
    domains: list[str],
    from_month: str,
    to_month: str,
    country: str = "999",
    web_source: str = "Total",
    include_subdomains: bool = True,
    time_granularity: str = "Monthly",
) -> dict[str, Any]:
    normalized_domains = list(
        dict.fromkeys(
            str(domain).strip().lower()
            for domain in domains
            if str(domain).strip()
        )
    )
    if not normalized_domains:
        raise ValueError("at least one domain is required")
    start_date, end_date = build_month_range(from_month, to_month)
    request = {
        "name": "website_traffic_trend",
        "method": "GET",
        "path": "/widgetApi/WebsiteOverview/EngagementVisits/Graph",
        "query": {
            "country": country,
            "from": start_date,
            "to": end_date,
            "isWindow": "false",
            "webSource": web_source,
            "includeSubDomains": str(include_subdomains).lower(),
            "keys": ",".join(normalized_domains),
            "timeGranularity": time_granularity,
            "ShouldGetVerifiedData": "false",
        },
    }
    return {
        "domains": normalized_domains,
        "from_month": from_month,
        "to_month": to_month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "include_subdomains": include_subdomains,
        "time_granularity": time_granularity,
        "requests": [request],
    }


def extract_monthly_website_visits(
    payload: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    data = payload.get("Data") or {}
    if not isinstance(data, dict):
        raise ValueError("website traffic trend Data must be an object")
    verification = payload.get("KeysDataVerification") or {}
    result: dict[str, dict[str, Any]] = {}
    for domain, domain_payload in data.items():
        totals = (
            domain_payload.get("Total", [])
            if isinstance(domain_payload, dict)
            else []
        )
        if totals and isinstance(totals[0], list):
            points = totals[0]
        elif isinstance(totals, list):
            points = totals
        else:
            points = []
        monthly: dict[str, float] = {}
        for point in points:
            if not isinstance(point, dict):
                continue
            month = str(point.get("Key") or "")[:7]
            value = point.get("Value")
            if not re.fullmatch(r"\d{4}-(?:0[1-9]|1[0-2])", month):
                continue
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                continue
            monthly[month] = monthly.get(month, 0.0) + float(value)
        result[str(domain)] = {
            "data_verified": (
                bool(verification.get(domain))
                if domain in verification
                else None
            ),
            "months": [
                {"month": month, "visits": monthly[month]}
                for month in sorted(monthly)
            ],
        }
    return result


def build_landing_pages_query(
    *,
    domain: str,
    month: str,
    country: str = "999",
    web_source: str = "Total",
    include_subdomains: bool = True,
    source_type: str = "organic",
    change: str = "New",
    sort: str = "ClicksShare",
    asc: bool = False,
) -> dict[str, Any]:
    start_date, end_date = build_month_window(month)
    include_subdomains_value = str(include_subdomains).lower()
    asc_value = str(asc).lower()
    page_filter_json = build_page_filter_json(domain)
    request = {
        "name": "landing_pages",
        "method": "POST",
        "path": "/api/websiteOrganicLandingPagesV2",
        "query": {
            "country": country,
            "to": end_date,
            "from": start_date,
            "isWindow": "false",
            "webSource": web_source,
            "key": domain,
            "pageFilterJson": page_filter_json,
            "sort": sort,
            "asc": asc_value,
            "Change": change,
            "sourceType": source_type,
            "includeSubDomains": include_subdomains_value,
        },
        "json_body": [],
    }
    return {
        "domain": domain,
        "month": month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "include_subdomains": include_subdomains,
        "source_type": source_type,
        "change": change,
        "sort": sort,
        "asc": asc,
        "requests": [request],
    }


def build_search_keywords_query(
    *,
    domain: str,
    month: str,
    country: str = "999",
    web_source: str = "Total",
    include_subdomains: bool = True,
    source_type: str = "all",
    change: str = "New",
    sort: str = "Share",
    asc: bool = False,
    page: int = 1,
    page_size: int = 100,
    time_granularity: str = "Monthly",
    include_branded: bool = False,
    include_non_branded: bool = False,
) -> dict[str, Any]:
    start_date, end_date = build_month_window(month)
    include_subdomains_value = str(include_subdomains).lower()
    asc_value = str(asc).lower()
    page_filter_json = build_page_filter_json(domain)
    shared_query = {
        "country": country,
        "to": end_date,
        "from": start_date,
        "isWindow": "false",
        "webSource": web_source,
        "keys": domain,
        "pageFilterJson": page_filter_json,
        "Change": change,
        "sourceType": source_type,
        "includeSubDomains": include_subdomains_value,
        "IncludeNoneBranded": str(include_non_branded).lower(),
        "IncludeBranded": str(include_branded).lower(),
        "page": str(page),
        "pageSize": str(page_size),
        "timeGranularity": time_granularity,
        "iso": "[object Object]",
    }
    requests = [
        {
            "name": "search_keywords_total",
            "method": "POST",
            "path": "/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/PresetsTotal",
            "query": shared_query,
            "json_body": [],
        },
        {
            "name": "search_keywords_table",
            "method": "POST",
            "path": "/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table",
            "query": {
                **shared_query,
                "sort": sort,
                "asc": asc_value,
            },
            "json_body": [],
        },
    ]
    return {
        "domain": domain,
        "month": month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "include_subdomains": include_subdomains,
        "source_type": source_type,
        "change": change,
        "sort": sort,
        "asc": asc,
        "page": page,
        "page_size": page_size,
        "time_granularity": time_granularity,
        "include_branded": include_branded,
        "include_non_branded": include_non_branded,
        "requests": requests,
    }


def build_search_landing_pages_overview_query(
    *,
    domain: str,
    month: str,
    country: str = "999",
    web_source: str = "Total",
    include_subdomains: bool = True,
    source_type: str = "all",
    page_size: int = 5,
) -> dict[str, Any]:
    start_date, end_date = build_month_window(month)
    request = {
        "name": "search_landing_pages_overview",
        "method": "GET",
        "path": "/api/searchoverview/keywords/landing-pages",
        "query": {
            "country": country,
            "from": start_date,
            "to": end_date,
            "isWindow": "false",
            "webSource": web_source,
            "includeSubDomains": str(include_subdomains).lower(),
            "keys": domain,
            "SourceType": source_type,
            "pageSize": str(page_size),
        },
    }
    return {
        "domain": domain,
        "month": month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "include_subdomains": include_subdomains,
        "source_type": source_type,
        "page_size": page_size,
        "requests": [request],
    }


def build_search_keyword_performance_query(
    *,
    domain: str,
    month: str,
    country: str = "999",
    web_source: str = "Total",
    include_subdomains: bool = True,
    source_type: str = "Organic",
    page_size: int = 100,
    time_granularity: str = "Monthly",
    duration: str = "1m",
) -> dict[str, Any]:
    start_date, end_date = build_month_window(month)
    request = {
        "name": "search_keyword_performance",
        "method": "GET",
        "path": "/widgetApi/SearchKeywordsV2/WebsitePerformance/Table",
        "query": {
            "country": country,
            "from": start_date,
            "to": end_date,
            "isWindow": "false",
            "webSource": web_source,
            "includeSubDomains": str(include_subdomains).lower(),
            "keys": domain,
            "SourceType": source_type,
            "pageSize": str(page_size),
            "timeGranularity": time_granularity,
            "duration": duration,
        },
    }
    return {
        "domain": domain,
        "month": month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "include_subdomains": include_subdomains,
        "source_type": source_type,
        "page_size": page_size,
        "time_granularity": time_granularity,
        "duration": duration,
        "requests": [request],
    }


def build_branded_keywords_query(
    *,
    domain: str,
    month: str,
    country: str = "999",
    web_source: str = "Total",
    include_subdomains: bool = True,
    time_granularity: str = "Monthly",
) -> dict[str, Any]:
    start_date, end_date = build_month_window(month)
    request = {
        "name": "branded_keywords",
        "method": "GET",
        "path": "/widgetApi/TrafficSourcesSearchV2/BrandedKeywords/WebsitePerformance/PieChart",
        "query": {
            "country": country,
            "from": start_date,
            "to": end_date,
            "isWindow": "false",
            "webSource": web_source,
            "includeSubDomains": str(include_subdomains).lower(),
            "keys": domain,
            "timeGranularity": time_granularity,
        },
    }
    return {
        "domain": domain,
        "month": month,
        "from": start_date,
        "to": end_date,
        "country": country,
        "web_source": web_source,
        "include_subdomains": include_subdomains,
        "time_granularity": time_granularity,
        "requests": [request],
    }


class SimilarWebClient:
    def __init__(
        self,
        *,
        session: requests.Session | None = None,
        user_agent: str = DEFAULT_USER_AGENT,
        cache_path: Path | None = None,
        min_token_ttl_seconds: int = 60,
    ):
        self.session = session or requests.Session()
        self.session.trust_env = False
        self.user_agent = user_agent
        self.cache_path = Path(cache_path) if cache_path else TOKEN_CACHE_PATH
        self.min_token_ttl_seconds = min_token_ttl_seconds

    def _load_cache_file(self) -> dict[str, Any]:
        if not self.cache_path.exists():
            return {}
        try:
            payload = json.loads(self.cache_path.read_text(encoding="utf-8"))
        except Exception:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _save_cache_file(self, payload: dict[str, Any]) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load_cached_token(self, username: str) -> dict[str, Any] | None:
        cache = self._load_cache_file()
        record = cache.get(username)
        return record if isinstance(record, dict) else None

    def invalidate_cached_token(self, username: str) -> bool:
        cache = self._load_cache_file()
        if username not in cache:
            return False
        del cache[username]
        self._save_cache_file(cache)
        return True

    def save_token_cache(self, *, username: str, token: str, roles: list[str] | None = None) -> dict[str, Any]:
        cache = self._load_cache_file()
        expires_at = extract_token_expiry(token)
        record = {
            "username": username,
            "token": token,
            "roles": roles or [],
            "expires_at": expires_at.isoformat() if expires_at else None,
            "updated_at": now_utc().isoformat(),
        }
        cache[username] = record
        self._save_cache_file(cache)
        return record

    def login(self, *, username: str, password: str) -> dict[str, Any]:
        response = self.session.get(
            LOGIN_URL,
            params={
                "username": username,
                "password": password,
                "ts": str(int(time.time() * 1000)),
            },
            headers={
                "accept": "application/json, text/plain, */*",
                "user-agent": self.user_agent,
                "referer": "https://dash.3ue.com/zh-Hans/",
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        token = extract_login_token(payload)
        return {
            "token": token,
            "username": ((payload.get("data") or {}).get("username") or username),
            "roles": (payload.get("data") or {}).get("roles") or [],
            "raw": payload,
        }

    def get_access_token(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
    ) -> dict[str, Any]:
        fallback_token = (token or "").strip()
        if fallback_token:
            if not is_token_usable(
                fallback_token,
                min_ttl_seconds=self.min_token_ttl_seconds,
            ):
                raise ValueError("SimilarWeb fallback token is invalid or expired")
            return {
                "token": fallback_token,
                "username": username or extract_username_from_token(fallback_token),
                "roles": [],
                "raw": None,
                "source": "fallback_token",
            }

        cached = self.load_cached_token(username)
        if cached and is_token_usable(
            cached.get("token", ""),
            min_ttl_seconds=self.min_token_ttl_seconds,
        ):
            return {
                "token": cached["token"],
                "username": cached.get("username") or username,
                "roles": cached.get("roles") or [],
                "raw": None,
                "source": "cache",
            }

        login_result = self.login(username=username, password=password)
        self.save_token_cache(
            username=login_result["username"],
            token=login_result["token"],
            roles=login_result["roles"],
        )
        return {
            **login_result,
            "source": "login",
        }

    def fetch_generated_keywords(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        keyword: str,
        month: str,
        country: str = "999",
        web_source: str = "Total",
        rows_per_page: int = 20,
        sort: str = "score",
        suggestion_type: str = "Related",
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        login_result = self.get_access_token(
            username=username,
            password=password,
            token=token,
        )
        start_date, end_date = build_month_window(month)
        response = self.session.post(
            SUGGEST_URL,
            params={
                "keyword": keyword,
                "country": country,
                "from": start_date,
                "to": end_date,
                "isWindow": "false",
                "webSource": web_source,
                "rowsPerPage": str(rows_per_page),
                "asc": "false",
                "sort": sort,
                "type": suggestion_type,
            },
            headers=build_authenticated_headers(
                token=login_result["token"],
                username=login_result["username"],
                x_sw_page=build_keyword_page_url(
                    keyword=keyword,
                    month=month,
                    country=country,
                    web_source=web_source,
                ),
                x_sw_page_view_id=x_sw_page_view_id or f"manual-{int(time.time() * 1000)}",
                user_agent=self.user_agent,
            ),
            json=[],
            timeout=20,
        )
        response.raise_for_status()
        if is_login_redirect_response(response):
            raise RuntimeError("SimilarWeb session was rejected and redirected to dash login")
        payload = response.json()
        if not isinstance(payload, dict):
            raise RuntimeError("SimilarWeb suggest endpoint did not return a JSON object")
        return payload

    def fetch_keyword_overview_bundle(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        keyword: str,
        month: str,
        country: str = "999",
        web_source: str = "Total",
        device: str = "Total",
        source_type: str = "all",
        duration: str = "1m",
        time_granularity: str = "Weekly",
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        login_result = self.get_access_token(
            username=username,
            password=password,
            token=token,
        )
        bundle = build_keyword_bundle(
            keyword=keyword,
            month=month,
            country=country,
            web_source=web_source,
            device=device,
            source_type=source_type,
            duration=duration,
            time_granularity=time_granularity,
        )
        page_view_id = x_sw_page_view_id or f"manual-{int(time.time() * 1000)}"
        x_sw_page = build_keyword_page_url(
            keyword=keyword,
            month=month,
            country=country,
            web_source=web_source,
        )
        payload: dict[str, Any] = {
            "keyword": keyword,
            "month": month,
            "from": bundle["from"],
            "to": bundle["to"],
            "country": country,
            "web_source": web_source,
            "device": device,
        }
        for request_plan in bundle["requests"]:
            if request_plan["method"] != "GET":
                continue
            response = self.session.get(
                f"{SIMILARWEB_DATA_BASE_URL}{request_plan['path']}",
                params=request_plan["query"],
                headers=build_authenticated_headers(
                    token=login_result["token"],
                    username=login_result["username"],
                    x_sw_page=x_sw_page,
                    x_sw_page_view_id=page_view_id,
                    user_agent=self.user_agent,
                ),
                timeout=20,
            )
            response.raise_for_status()
            if is_login_redirect_response(response):
                raise RuntimeError(
                    f"SimilarWeb session was rejected while requesting {request_plan['name']}"
                )
            endpoint_payload = response.json()
            if not isinstance(endpoint_payload, dict):
                raise RuntimeError(
                    f"SimilarWeb endpoint {request_plan['name']} did not return a JSON object"
                )
            payload[request_plan["name"]] = endpoint_payload
        return payload

    def fetch_website_analysis_bundle(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        domain: str,
        month: str,
        country: str = "999",
        web_source: str = "Total",
        include_subdomains: bool = True,
        compare_domains: list[str] | None = None,
        category: str | None = None,
        page_size: int = 5,
        keyword_page_size: int = 100,
        time_granularity: str = "Monthly",
        source_type: str = "all",
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        login_result = self.get_access_token(
            username=username,
            password=password,
            token=token,
        )
        bundle = build_website_analysis_bundle(
            domain=domain,
            month=month,
            country=country,
            web_source=web_source,
            include_subdomains=include_subdomains,
            compare_domains=compare_domains,
            category=category,
            page_size=page_size,
            keyword_page_size=keyword_page_size,
            time_granularity=time_granularity,
            source_type=source_type,
        )
        page_view_id = x_sw_page_view_id or f"manual-{int(time.time() * 1000)}"
        x_sw_page = build_website_page_url(
            domain=domain,
            country=country,
            web_source=web_source,
        )
        headers = build_authenticated_headers(
            token=login_result["token"],
            username=login_result["username"],
            x_sw_page=x_sw_page,
            x_sw_page_view_id=page_view_id,
            user_agent=self.user_agent,
        )
        payload: dict[str, Any] = {
            "domain": domain,
            "month": month,
            "from": bundle["from"],
            "to": bundle["to"],
            "country": country,
            "web_source": web_source,
            "include_subdomains": include_subdomains,
            "compare_domains": compare_domains or [],
        }
        for request_plan in bundle["requests"]:
            method = request_plan["method"]
            url = f"{SIMILARWEB_DATA_BASE_URL}{request_plan['path']}"
            if method == "POST":
                response = self.session.post(
                    url,
                    params=request_plan["query"],
                    headers=headers,
                    json=request_plan.get("json_body", []),
                    timeout=20,
                )
            else:
                response = self.session.get(
                    url,
                    params=request_plan["query"],
                    headers=headers,
                    timeout=20,
                )
            response.raise_for_status()
            if is_login_redirect_response(response):
                raise RuntimeError(
                    f"SimilarWeb session was rejected while requesting {request_plan['name']}"
                )
            payload[request_plan["name"]] = response.json()
        return payload

    def fetch_website_traffic_trend_query(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        domains: list[str],
        from_month: str,
        to_month: str,
        country: str = "999",
        web_source: str = "Total",
        include_subdomains: bool = True,
        time_granularity: str = "Monthly",
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        login_result = self.get_access_token(
            username=username,
            password=password,
            token=token,
        )
        bundle = build_website_traffic_trend_query(
            domains=domains,
            from_month=from_month,
            to_month=to_month,
            country=country,
            web_source=web_source,
            include_subdomains=include_subdomains,
            time_granularity=time_granularity,
        )
        request_plan = bundle["requests"][0]
        response = self.session.get(
            f"{SIMILARWEB_DATA_BASE_URL}{request_plan['path']}",
            params=request_plan["query"],
            headers=build_authenticated_headers(
                token=login_result["token"],
                username=login_result["username"],
                x_sw_page=build_website_page_url(
                    domain=bundle["domains"][0],
                    country=country,
                    web_source=web_source,
                ),
                x_sw_page_view_id=(
                    x_sw_page_view_id or f"manual-{int(time.time() * 1000)}"
                ),
                user_agent=self.user_agent,
            ),
            timeout=20,
        )
        response.raise_for_status()
        if is_login_redirect_response(response):
            raise RuntimeError(
                "SimilarWeb session was rejected while requesting website traffic trend"
            )
        traffic_trend = response.json()
        if not isinstance(traffic_trend, dict):
            raise RuntimeError(
                "SimilarWeb website traffic trend endpoint did not return a JSON object"
            )
        monthly_visits = extract_monthly_website_visits(traffic_trend)
        verification = traffic_trend.get("KeysDataVerification") or {}
        for domain in bundle["domains"]:
            monthly_visits.setdefault(
                domain,
                {
                    "data_verified": (
                        bool(verification.get(domain))
                        if domain in verification
                        else None
                    ),
                    "months": [],
                },
            )
        return {
            **{key: value for key, value in bundle.items() if key != "requests"},
            "traffic_trend": traffic_trend,
            "monthly_visits": monthly_visits,
        }

    def fetch_referral_traffic_query(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        domain: str,
        from_month: str,
        to_month: str,
        country: str = "999",
        web_source: str = "Total",
        page: int = 1,
        sort: str = "TotalShare",
        asc: bool = False,
        all_pages: bool = False,
        max_pages: int | None = None,
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        if max_pages is not None and max_pages < 1:
            raise ValueError("max_pages must be at least 1")
        login_result = self.get_access_token(
            username=username,
            password=password,
            token=token,
        )
        bundle = build_referral_traffic_query(
            domain=domain,
            from_month=from_month,
            to_month=to_month,
            country=country,
            web_source=web_source,
            page=page,
            sort=sort,
            asc=asc,
        )
        page_view_id = x_sw_page_view_id or f"manual-{int(time.time() * 1000)}"
        headers = build_authenticated_headers(
            token=login_result["token"],
            username=login_result["username"],
            x_sw_page=build_website_page_url(
                domain=domain,
                country=country,
                web_source=web_source,
            ),
            x_sw_page_view_id=page_view_id,
            user_agent=self.user_agent,
        )

        def fetch_plan(request_plan: dict[str, Any]) -> dict[str, Any]:
            response = self.session.get(
                f"{SIMILARWEB_DATA_BASE_URL}{request_plan['path']}",
                params=request_plan["query"],
                headers=headers,
                timeout=20,
            )
            response.raise_for_status()
            if is_login_redirect_response(response):
                raise RuntimeError(
                    f"SimilarWeb session was rejected while requesting {request_plan['name']}"
                )
            endpoint_payload = response.json()
            if not isinstance(endpoint_payload, dict):
                raise RuntimeError(
                    f"SimilarWeb endpoint {request_plan['name']} did not return a JSON object"
                )
            return endpoint_payload

        referral_totals = fetch_plan(bundle["requests"][0])
        current_page = page
        pages_fetched = 0
        aggregated_records: list[Any] = []
        referral_table: dict[str, Any] | None = None
        total_count: int | None = None
        complete = False

        while True:
            page_bundle = build_referral_traffic_query(
                domain=domain,
                from_month=from_month,
                to_month=to_month,
                country=country,
                web_source=web_source,
                page=current_page,
                sort=sort,
                asc=asc,
            )
            page_payload = fetch_plan(page_bundle["requests"][1])
            records = page_payload.get("Records", [])
            if not isinstance(records, list):
                raise RuntimeError(
                    "SimilarWeb endpoint referral_table returned a non-list Records field"
                )
            if referral_table is None:
                referral_table = dict(page_payload)
                raw_total_count = page_payload.get("TotalCount")
                total_count = raw_total_count if isinstance(raw_total_count, int) else None
            aggregated_records.extend(records)
            pages_fetched += 1

            reached_total = (
                total_count is not None
                and current_page * REFERRAL_TABLE_PAGE_SIZE >= total_count
            )
            reached_last_page = len(records) < REFERRAL_TABLE_PAGE_SIZE
            complete = reached_total or reached_last_page
            reached_limit = max_pages is not None and pages_fetched >= max_pages
            if not all_pages or complete or reached_limit:
                break
            current_page += 1

        assert referral_table is not None
        referral_table["Records"] = aggregated_records
        return {
            "domain": domain,
            "from_month": from_month,
            "to_month": to_month,
            "from": bundle["from"],
            "to": bundle["to"],
            "country": country,
            "web_source": web_source,
            "sort": sort,
            "asc": asc,
            "referral_totals": referral_totals,
            "referral_table": referral_table,
            "pagination": {
                "all_pages": all_pages,
                "start_page": page,
                "end_page": current_page,
                "pages_fetched": pages_fetched,
                "page_size": REFERRAL_TABLE_PAGE_SIZE,
                "total_count": total_count,
                "records_returned": len(aggregated_records),
                "complete": complete,
            },
        }

    def fetch_landing_pages_query(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        domain: str,
        month: str,
        country: str = "999",
        web_source: str = "Total",
        include_subdomains: bool = True,
        source_type: str = "organic",
        change: str = "New",
        sort: str = "ClicksShare",
        asc: bool = False,
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        login_result = self.get_access_token(
            username=username,
            password=password,
            token=token,
        )
        bundle = build_landing_pages_query(
            domain=domain,
            month=month,
            country=country,
            web_source=web_source,
            include_subdomains=include_subdomains,
            source_type=source_type,
            change=change,
            sort=sort,
            asc=asc,
        )
        page_view_id = x_sw_page_view_id or f"manual-{int(time.time() * 1000)}"
        x_sw_page = build_landing_pages_page_url(
            domain=domain,
            month=month,
            country=country,
            web_source=web_source,
            change=change,
        )
        headers = build_authenticated_headers(
            token=login_result["token"],
            username=login_result["username"],
            x_sw_page=x_sw_page,
            x_sw_page_view_id=page_view_id,
            user_agent=self.user_agent,
        )
        request_plan = bundle["requests"][0]
        response = self.session.post(
            f"{SIMILARWEB_DATA_BASE_URL}{request_plan['path']}",
            params=request_plan["query"],
            headers=headers,
            json=request_plan.get("json_body", []),
            timeout=20,
        )
        response.raise_for_status()
        if is_login_redirect_response(response):
            raise RuntimeError("SimilarWeb session was rejected while requesting landing_pages")
        return {
            "domain": domain,
            "month": month,
            "from": bundle["from"],
            "to": bundle["to"],
            "country": country,
            "web_source": web_source,
            "include_subdomains": include_subdomains,
            "source_type": source_type,
            "change": change,
            "sort": sort,
            "asc": asc,
            "landing_pages": response.json(),
        }

    def fetch_search_keywords_query(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        domain: str,
        month: str,
        country: str = "999",
        web_source: str = "Total",
        include_subdomains: bool = True,
        source_type: str = "all",
        change: str = "New",
        sort: str = "Share",
        asc: bool = False,
        page: int = 1,
        page_size: int = 100,
        time_granularity: str = "Monthly",
        include_branded: bool = False,
        include_non_branded: bool = False,
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        login_result = self.get_access_token(
            username=username,
            password=password,
            token=token,
        )
        bundle = build_search_keywords_query(
            domain=domain,
            month=month,
            country=country,
            web_source=web_source,
            include_subdomains=include_subdomains,
            source_type=source_type,
            change=change,
            sort=sort,
            asc=asc,
            page=page,
            page_size=page_size,
            time_granularity=time_granularity,
            include_branded=include_branded,
            include_non_branded=include_non_branded,
        )
        page_view_id = x_sw_page_view_id or f"manual-{int(time.time() * 1000)}"
        x_sw_page = build_search_keywords_page_url(
            domain=domain,
            month=month,
            country=country,
            web_source=web_source,
            change=change,
        )
        headers = build_authenticated_headers(
            token=login_result["token"],
            username=login_result["username"],
            x_sw_page=x_sw_page,
            x_sw_page_view_id=page_view_id,
            user_agent=self.user_agent,
        )
        payload: dict[str, Any] = {
            "domain": domain,
            "month": month,
            "from": bundle["from"],
            "to": bundle["to"],
            "country": country,
            "web_source": web_source,
            "include_subdomains": include_subdomains,
            "source_type": source_type,
            "change": change,
            "sort": sort,
            "asc": asc,
            "page": page,
            "page_size": page_size,
            "time_granularity": time_granularity,
            "include_branded": include_branded,
            "include_non_branded": include_non_branded,
        }
        for request_plan in bundle["requests"]:
            response = self.session.post(
                f"{SIMILARWEB_DATA_BASE_URL}{request_plan['path']}",
                params=request_plan["query"],
                headers=headers,
                json=request_plan.get("json_body", []),
                timeout=20,
            )
            response.raise_for_status()
            if is_login_redirect_response(response):
                raise RuntimeError(
                    f"SimilarWeb session was rejected while requesting {request_plan['name']}"
                )
            payload[request_plan["name"]] = response.json()
        return payload

    def _fetch_single_get_query(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        bundle: dict[str, Any],
        result_key: str,
        x_sw_page: str | None = None,
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        login_result = self.get_access_token(
            username=username,
            password=password,
            token=token,
        )
        page_view_id = x_sw_page_view_id or f"manual-{int(time.time() * 1000)}"
        request_plan = bundle["requests"][0]
        response = self.session.get(
            f"{SIMILARWEB_DATA_BASE_URL}{request_plan['path']}",
            params=request_plan["query"],
            headers=build_authenticated_headers(
                token=login_result["token"],
                username=login_result["username"],
                x_sw_page=x_sw_page,
                x_sw_page_view_id=page_view_id,
                user_agent=self.user_agent,
            ),
            timeout=20,
        )
        response.raise_for_status()
        if is_login_redirect_response(response):
            raise RuntimeError(f"SimilarWeb session was rejected while requesting {result_key}")
        return {
            key: value
            for key, value in bundle.items()
            if key != "requests"
        } | {
            result_key: response.json(),
        }

    def fetch_search_landing_pages_overview_query(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        domain: str,
        month: str,
        country: str = "999",
        web_source: str = "Total",
        include_subdomains: bool = True,
        source_type: str = "all",
        page_size: int = 5,
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        bundle = build_search_landing_pages_overview_query(
            domain=domain,
            month=month,
            country=country,
            web_source=web_source,
            include_subdomains=include_subdomains,
            source_type=source_type,
            page_size=page_size,
        )
        return self._fetch_single_get_query(
            username=username,
            password=password,
            token=token,
            bundle=bundle,
            result_key="search_landing_pages_overview",
            x_sw_page=build_website_page_url(
                domain=domain,
                country=country,
                web_source=web_source,
            ),
            x_sw_page_view_id=x_sw_page_view_id,
        )

    def fetch_search_keyword_performance_query(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        domain: str,
        month: str,
        country: str = "999",
        web_source: str = "Total",
        include_subdomains: bool = True,
        source_type: str = "Organic",
        page_size: int = 100,
        time_granularity: str = "Monthly",
        duration: str = "1m",
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        bundle = build_search_keyword_performance_query(
            domain=domain,
            month=month,
            country=country,
            web_source=web_source,
            include_subdomains=include_subdomains,
            source_type=source_type,
            page_size=page_size,
            time_granularity=time_granularity,
            duration=duration,
        )
        return self._fetch_single_get_query(
            username=username,
            password=password,
            token=token,
            bundle=bundle,
            result_key="search_keyword_performance",
            x_sw_page=build_website_page_url(
                domain=domain,
                country=country,
                web_source=web_source,
            ),
            x_sw_page_view_id=x_sw_page_view_id,
        )

    def fetch_branded_keywords_query(
        self,
        *,
        username: str,
        password: str,
        token: str | None = None,
        domain: str,
        month: str,
        country: str = "999",
        web_source: str = "Total",
        include_subdomains: bool = True,
        time_granularity: str = "Monthly",
        x_sw_page_view_id: str | None = None,
    ) -> dict[str, Any]:
        bundle = build_branded_keywords_query(
            domain=domain,
            month=month,
            country=country,
            web_source=web_source,
            include_subdomains=include_subdomains,
            time_granularity=time_granularity,
        )
        return self._fetch_single_get_query(
            username=username,
            password=password,
            token=token,
            bundle=bundle,
            result_key="branded_keywords",
            x_sw_page=build_website_page_url(
                domain=domain,
                country=country,
                web_source=web_source,
            ),
            x_sw_page_view_id=x_sw_page_view_id,
        )


def load_har_entries(paths: list[str]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for raw_path in paths:
        path = Path(raw_path).expanduser().resolve()
        payload = json.loads(path.read_text(encoding="utf-8"))
        entries.extend(payload.get("log", {}).get("entries", []))
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize SimilarWeb-compatible HAR files and build request bundles.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary_parser = subparsers.add_parser("summarize-har", help="Summarize HAR entries into data/internal/control buckets.")
    summary_parser.add_argument("paths", nargs="+", help="HAR file paths")

    bundle_parser = subparsers.add_parser("build-keyword-bundle", help="Build the core keyword-analysis request plan.")
    bundle_parser.add_argument("--keyword", required=True, help="Target keyword")
    bundle_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    bundle_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    bundle_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    bundle_parser.add_argument("--device", default="Total", help="SimilarWeb device value")

    website_bundle_parser = subparsers.add_parser(
        "build-website-analysis-bundle",
        help="Build the observed website-analysis request plan.",
    )
    website_bundle_parser.add_argument("--domain", required=True, help="Target domain")
    website_bundle_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    website_bundle_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    website_bundle_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    website_bundle_parser.add_argument(
        "--compare-domain",
        action="append",
        default=[],
        help="Optional comparison domain. Repeat for multiple domains.",
    )
    website_bundle_parser.add_argument("--category", help="Optional SimilarWeb category key for asset comparison")
    website_bundle_parser.add_argument("--page-size", type=int, default=5, help="Small table page size")
    website_bundle_parser.add_argument("--keyword-page-size", type=int, default=100, help="Keyword/backlink table page size")

    traffic_bundle_parser = subparsers.add_parser(
        "build-website-traffic-trend-query",
        help="Build a monthly website total-visits trend request.",
    )
    traffic_bundle_parser.add_argument(
        "--domain",
        action="append",
        required=True,
        help="Website domain. Repeat for multiple domains.",
    )
    traffic_bundle_parser.add_argument("--from-month", required=True)
    traffic_bundle_parser.add_argument("--to-month", required=True)
    traffic_bundle_parser.add_argument("--country", default="999")
    traffic_bundle_parser.add_argument("--web-source", default="Total")
    traffic_bundle_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
    )
    traffic_bundle_parser.add_argument(
        "--time-granularity",
        default="Monthly",
    )

    referral_bundle_parser = subparsers.add_parser(
        "build-referral-traffic-query",
        help="Build the observed incoming referral-traffic totals and paginated table requests.",
    )
    referral_bundle_parser.add_argument("--domain", required=True, help="Target domain")
    referral_bundle_parser.add_argument("--from-month", required=True, help="First month in YYYY-MM format")
    referral_bundle_parser.add_argument("--to-month", required=True, help="Last month in YYYY-MM format")
    referral_bundle_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    referral_bundle_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    referral_bundle_parser.add_argument("--page", type=int, default=1, help="Result page; observed page size is 100")
    referral_bundle_parser.add_argument("--sort", default="TotalShare", help="Sort field")
    referral_bundle_parser.add_argument("--asc", action="store_true", help="Sort ascending instead of descending")

    landing_bundle_parser = subparsers.add_parser(
        "build-landing-pages-query",
        help="Build the observed organic landing-pages request, defaulting to new pages sorted by click share.",
    )
    landing_bundle_parser.add_argument("--domain", required=True, help="Target domain")
    landing_bundle_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    landing_bundle_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    landing_bundle_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    landing_bundle_parser.add_argument("--source-type", default="organic", help="SimilarWeb sourceType value")
    landing_bundle_parser.add_argument("--change", default="New", help="Change filter, such as New")
    landing_bundle_parser.add_argument("--sort", default="ClicksShare", help="Sort field")
    landing_bundle_parser.add_argument("--asc", action="store_true", help="Sort ascending instead of descending")
    landing_bundle_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    search_keywords_bundle_parser = subparsers.add_parser(
        "build-search-keywords-query",
        help="Build the observed website keyword-analysis request for new search keyword clicks.",
    )
    search_keywords_bundle_parser.add_argument("--domain", required=True, help="Target domain")
    search_keywords_bundle_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    search_keywords_bundle_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    search_keywords_bundle_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    search_keywords_bundle_parser.add_argument("--source-type", default="all", help="SimilarWeb sourceType value")
    search_keywords_bundle_parser.add_argument("--change", default="New", help="Change filter, such as New")
    search_keywords_bundle_parser.add_argument("--sort", default="Share", help="Sort field")
    search_keywords_bundle_parser.add_argument("--asc", action="store_true", help="Sort ascending instead of descending")
    search_keywords_bundle_parser.add_argument("--page", type=int, default=1, help="Result page")
    search_keywords_bundle_parser.add_argument("--page-size", type=int, default=100, help="Result page size")
    search_keywords_bundle_parser.add_argument("--time-granularity", default="Monthly", help="SimilarWeb timeGranularity value")
    search_keywords_bundle_parser.add_argument("--include-branded", action="store_true", help="Include branded keywords")
    search_keywords_bundle_parser.add_argument("--include-non-branded", action="store_true", help="Include non-branded keywords")
    search_keywords_bundle_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    search_landing_pages_bundle_parser = subparsers.add_parser(
        "build-search-landing-pages-overview-query",
        help="Build the lightweight search overview landing-pages request.",
    )
    search_landing_pages_bundle_parser.add_argument("--domain", required=True, help="Target domain")
    search_landing_pages_bundle_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    search_landing_pages_bundle_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    search_landing_pages_bundle_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    search_landing_pages_bundle_parser.add_argument("--source-type", default="all", help="SimilarWeb SourceType value")
    search_landing_pages_bundle_parser.add_argument("--page-size", type=int, default=5, help="Result page size")
    search_landing_pages_bundle_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    keyword_performance_bundle_parser = subparsers.add_parser(
        "build-search-keyword-performance-query",
        help="Build the SearchKeywordsV2 website performance table request.",
    )
    keyword_performance_bundle_parser.add_argument("--domain", required=True, help="Target domain")
    keyword_performance_bundle_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    keyword_performance_bundle_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    keyword_performance_bundle_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    keyword_performance_bundle_parser.add_argument("--source-type", default="Organic", help="SimilarWeb SourceType value")
    keyword_performance_bundle_parser.add_argument("--page-size", type=int, default=100, help="Result page size")
    keyword_performance_bundle_parser.add_argument("--time-granularity", default="Monthly", help="SimilarWeb timeGranularity value")
    keyword_performance_bundle_parser.add_argument("--duration", default="1m", help="SimilarWeb duration value")
    keyword_performance_bundle_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    branded_keywords_bundle_parser = subparsers.add_parser(
        "build-branded-keywords-query",
        help="Build the branded versus non-branded keyword pie chart request.",
    )
    branded_keywords_bundle_parser.add_argument("--domain", required=True, help="Target domain")
    branded_keywords_bundle_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    branded_keywords_bundle_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    branded_keywords_bundle_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    branded_keywords_bundle_parser.add_argument("--time-granularity", default="Monthly", help="SimilarWeb timeGranularity value")
    branded_keywords_bundle_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    login_parser = subparsers.add_parser("login", help="Login through dash.3ue.com and return account metadata.")
    login_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    login_parser.add_argument(
        "--project",
        help="Project env profile to use when --env-file is not provided.",
    )
    login_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    login_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    login_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")

    generated_parser = subparsers.add_parser(
        "fetch-generated-keywords",
        help="Login and fetch full JSON from SimilarWeb keyword suggestion endpoint.",
    )
    generated_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    generated_parser.add_argument(
        "--project",
        help="Project env profile to use when --env-file is not provided.",
    )
    generated_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    generated_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    generated_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    generated_parser.add_argument("--keyword", required=True, help="Target keyword")
    generated_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    generated_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    generated_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    generated_parser.add_argument("--rows-per-page", type=int, default=20, help="Number of suggestions to request")
    generated_parser.add_argument("--sort", default="score", help="Sort field")
    generated_parser.add_argument("--type", default="Related", help="Suggestion type, such as Related")

    overview_parser = subparsers.add_parser(
        "fetch-keyword-overview-bundle",
        help="Login and fetch the verified SimilarWeb keyword overview bundle as one JSON object.",
    )
    overview_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    overview_parser.add_argument(
        "--project",
        help="Project env profile to use when --env-file is not provided.",
    )
    overview_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    overview_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    overview_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    overview_parser.add_argument("--keyword", required=True, help="Target keyword")
    overview_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    overview_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    overview_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    overview_parser.add_argument("--device", default="Total", help="SimilarWeb device value")
    overview_parser.add_argument("--source-type", default="all", help="SimilarWeb sourceType value")
    overview_parser.add_argument("--duration", default="1m", help="Trend duration value")
    overview_parser.add_argument("--time-granularity", default="Weekly", help="Trend timeGranularity value")

    website_parser = subparsers.add_parser(
        "fetch-website-analysis-bundle",
        help="Login and fetch the observed SimilarWeb website-analysis bundle as one JSON object.",
    )
    website_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    website_parser.add_argument(
        "--project",
        help="Project env profile to use when --env-file is not provided.",
    )
    website_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    website_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    website_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    website_parser.add_argument("--domain", required=True, help="Target domain")
    website_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    website_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    website_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    website_parser.add_argument(
        "--compare-domain",
        action="append",
        default=[],
        help="Optional comparison domain. Repeat for multiple domains.",
    )
    website_parser.add_argument("--category", help="Optional SimilarWeb category key for asset comparison")
    website_parser.add_argument("--page-size", type=int, default=5, help="Small table page size")
    website_parser.add_argument("--keyword-page-size", type=int, default=100, help="Keyword/backlink table page size")
    website_parser.add_argument("--time-granularity", default="Monthly", help="SimilarWeb timeGranularity value")
    website_parser.add_argument("--source-type", default="all", help="SimilarWeb website keyword sourceType value")

    traffic_parser = subparsers.add_parser(
        "fetch-website-traffic-trend-query",
        help="Login and fetch normalized monthly website total-visits trends.",
    )
    traffic_parser.add_argument("--env-file")
    traffic_parser.add_argument("--project")
    traffic_parser.add_argument("--username")
    traffic_parser.add_argument("--password")
    traffic_parser.add_argument("--token")
    traffic_parser.add_argument(
        "--domain",
        action="append",
        required=True,
        help="Website domain. Repeat for multiple domains.",
    )
    traffic_parser.add_argument("--from-month", required=True)
    traffic_parser.add_argument("--to-month", required=True)
    traffic_parser.add_argument("--country", default="999")
    traffic_parser.add_argument("--web-source", default="Total")
    traffic_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
    )
    traffic_parser.add_argument(
        "--time-granularity",
        default="Monthly",
    )

    referral_parser = subparsers.add_parser(
        "fetch-referral-traffic-query",
        help="Login and fetch incoming referral traffic, optionally aggregating multiple 100-row pages.",
    )
    referral_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    referral_parser.add_argument("--project", help="Project env profile to use when --env-file is not provided.")
    referral_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    referral_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    referral_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    referral_parser.add_argument("--domain", required=True, help="Target domain")
    referral_parser.add_argument("--from-month", required=True, help="First month in YYYY-MM format")
    referral_parser.add_argument("--to-month", required=True, help="Last month in YYYY-MM format")
    referral_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    referral_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    referral_parser.add_argument("--page", type=int, default=1, help="Starting result page")
    referral_parser.add_argument("--sort", default="TotalShare", help="Sort field")
    referral_parser.add_argument("--asc", action="store_true", help="Sort ascending instead of descending")
    referral_parser.add_argument("--all-pages", action="store_true", help="Continue until the last observed 100-row page")
    referral_parser.add_argument("--max-pages", type=int, help="Optional cap when --all-pages is enabled")

    landing_parser = subparsers.add_parser(
        "fetch-landing-pages-query",
        help="Login and fetch the observed SimilarWeb landing-pages JSON payload.",
    )
    landing_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    landing_parser.add_argument(
        "--project",
        help="Project env profile to use when --env-file is not provided.",
    )
    landing_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    landing_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    landing_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    landing_parser.add_argument("--domain", required=True, help="Target domain")
    landing_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    landing_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    landing_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    landing_parser.add_argument("--source-type", default="organic", help="SimilarWeb sourceType value")
    landing_parser.add_argument("--change", default="New", help="Change filter, such as New")
    landing_parser.add_argument("--sort", default="ClicksShare", help="Sort field")
    landing_parser.add_argument("--asc", action="store_true", help="Sort ascending instead of descending")
    landing_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    search_keywords_parser = subparsers.add_parser(
        "fetch-search-keywords-query",
        help="Login and fetch observed SimilarWeb new search keyword clicks payloads.",
    )
    search_keywords_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    search_keywords_parser.add_argument(
        "--project",
        help="Project env profile to use when --env-file is not provided.",
    )
    search_keywords_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    search_keywords_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    search_keywords_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    search_keywords_parser.add_argument("--domain", required=True, help="Target domain")
    search_keywords_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    search_keywords_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    search_keywords_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    search_keywords_parser.add_argument("--source-type", default="all", help="SimilarWeb sourceType value")
    search_keywords_parser.add_argument("--change", default="New", help="Change filter, such as New")
    search_keywords_parser.add_argument("--sort", default="Share", help="Sort field")
    search_keywords_parser.add_argument("--asc", action="store_true", help="Sort ascending instead of descending")
    search_keywords_parser.add_argument("--page", type=int, default=1, help="Result page")
    search_keywords_parser.add_argument("--page-size", type=int, default=100, help="Result page size")
    search_keywords_parser.add_argument("--time-granularity", default="Monthly", help="SimilarWeb timeGranularity value")
    search_keywords_parser.add_argument("--include-branded", action="store_true", help="Include branded keywords")
    search_keywords_parser.add_argument("--include-non-branded", action="store_true", help="Include non-branded keywords")
    search_keywords_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    search_landing_pages_parser = subparsers.add_parser(
        "fetch-search-landing-pages-overview-query",
        help="Login and fetch the lightweight search overview landing-pages payload.",
    )
    search_landing_pages_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    search_landing_pages_parser.add_argument("--project", help="Project env profile to use when --env-file is not provided.")
    search_landing_pages_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    search_landing_pages_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    search_landing_pages_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    search_landing_pages_parser.add_argument("--domain", required=True, help="Target domain")
    search_landing_pages_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    search_landing_pages_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    search_landing_pages_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    search_landing_pages_parser.add_argument("--source-type", default="all", help="SimilarWeb SourceType value")
    search_landing_pages_parser.add_argument("--page-size", type=int, default=5, help="Result page size")
    search_landing_pages_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    keyword_performance_parser = subparsers.add_parser(
        "fetch-search-keyword-performance-query",
        help="Login and fetch the SearchKeywordsV2 website performance table payload.",
    )
    keyword_performance_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    keyword_performance_parser.add_argument("--project", help="Project env profile to use when --env-file is not provided.")
    keyword_performance_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    keyword_performance_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    keyword_performance_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    keyword_performance_parser.add_argument("--domain", required=True, help="Target domain")
    keyword_performance_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    keyword_performance_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    keyword_performance_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    keyword_performance_parser.add_argument("--source-type", default="Organic", help="SimilarWeb SourceType value")
    keyword_performance_parser.add_argument("--page-size", type=int, default=100, help="Result page size")
    keyword_performance_parser.add_argument("--time-granularity", default="Monthly", help="SimilarWeb timeGranularity value")
    keyword_performance_parser.add_argument("--duration", default="1m", help="SimilarWeb duration value")
    keyword_performance_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    branded_keywords_parser = subparsers.add_parser(
        "fetch-branded-keywords-query",
        help="Login and fetch the branded versus non-branded keyword pie chart payload.",
    )
    branded_keywords_parser.add_argument("--env-file", help="Path to the env file. Defaults to caller project .env discovery.")
    branded_keywords_parser.add_argument("--project", help="Project env profile to use when --env-file is not provided.")
    branded_keywords_parser.add_argument("--username", help="dash username; falls back to SIMILARWEB_USERNAME")
    branded_keywords_parser.add_argument("--password", help="dash password; falls back to SIMILARWEB_PASSWORD")
    branded_keywords_parser.add_argument("--token", help="Fallback token; falls back to SIMILARWEB_TOKEN")
    branded_keywords_parser.add_argument("--domain", required=True, help="Target domain")
    branded_keywords_parser.add_argument("--month", required=True, help="Month in YYYY-MM format")
    branded_keywords_parser.add_argument("--country", default="999", help="SimilarWeb country code")
    branded_keywords_parser.add_argument("--web-source", default="Total", help="SimilarWeb webSource value")
    branded_keywords_parser.add_argument("--time-granularity", default="Monthly", help="SimilarWeb timeGranularity value")
    branded_keywords_parser.add_argument(
        "--no-include-subdomains",
        action="store_true",
        help="Set includeSubDomains=false",
    )

    args = parser.parse_args()
    if args.command == "summarize-har":
        summary = summarize_har_entries(load_har_entries(args.paths))
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return
    if args.command == "build-keyword-bundle":
        bundle = build_keyword_bundle(
            keyword=args.keyword,
            month=args.month,
            country=args.country,
            web_source=args.web_source,
            device=args.device,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return
    if args.command == "build-website-analysis-bundle":
        bundle = build_website_analysis_bundle(
            domain=args.domain,
            month=args.month,
            country=args.country,
            web_source=args.web_source,
            compare_domains=args.compare_domain,
            category=args.category,
            page_size=args.page_size,
            keyword_page_size=args.keyword_page_size,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return
    if args.command == "build-website-traffic-trend-query":
        bundle = build_website_traffic_trend_query(
            domains=args.domain,
            from_month=args.from_month,
            to_month=args.to_month,
            country=args.country,
            web_source=args.web_source,
            include_subdomains=not args.no_include_subdomains,
            time_granularity=args.time_granularity,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return

    if args.command == "build-referral-traffic-query":
        bundle = build_referral_traffic_query(
            domain=args.domain,
            from_month=args.from_month,
            to_month=args.to_month,
            country=args.country,
            web_source=args.web_source,
            page=args.page,
            sort=args.sort,
            asc=args.asc,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return
    if args.command == "build-landing-pages-query":
        bundle = build_landing_pages_query(
            domain=args.domain,
            month=args.month,
            country=args.country,
            web_source=args.web_source,
            include_subdomains=not args.no_include_subdomains,
            source_type=args.source_type,
            change=args.change,
            sort=args.sort,
            asc=args.asc,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return
    if args.command == "build-search-keywords-query":
        bundle = build_search_keywords_query(
            domain=args.domain,
            month=args.month,
            country=args.country,
            web_source=args.web_source,
            include_subdomains=not args.no_include_subdomains,
            source_type=args.source_type,
            change=args.change,
            sort=args.sort,
            asc=args.asc,
            page=args.page,
            page_size=args.page_size,
            time_granularity=args.time_granularity,
            include_branded=args.include_branded,
            include_non_branded=args.include_non_branded,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return
    if args.command == "build-search-landing-pages-overview-query":
        bundle = build_search_landing_pages_overview_query(
            domain=args.domain,
            month=args.month,
            country=args.country,
            web_source=args.web_source,
            include_subdomains=not args.no_include_subdomains,
            source_type=args.source_type,
            page_size=args.page_size,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return
    if args.command == "build-search-keyword-performance-query":
        bundle = build_search_keyword_performance_query(
            domain=args.domain,
            month=args.month,
            country=args.country,
            web_source=args.web_source,
            include_subdomains=not args.no_include_subdomains,
            source_type=args.source_type,
            page_size=args.page_size,
            time_granularity=args.time_granularity,
            duration=args.duration,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return
    if args.command == "build-branded-keywords-query":
        bundle = build_branded_keywords_query(
            domain=args.domain,
            month=args.month,
            country=args.country,
            web_source=args.web_source,
            include_subdomains=not args.no_include_subdomains,
            time_granularity=args.time_granularity,
        )
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return

    client = SimilarWebClient()
    auth_candidates = resolve_auth_candidates(
        username=getattr(args, "username", None),
        password=getattr(args, "password", None),
        token=getattr(args, "token", None),
        env_file=getattr(args, "env_file", None),
        project=getattr(args, "project", None),
    )

    def run_auth(operation):
        return run_with_auth_candidates(
            auth_candidates,
            operation,
            on_auth_failure=lambda auth: (
                not auth.get("token")
                and client.invalidate_cached_token(auth["username"])
            ),
        )

    if args.command == "login":
        login_result = run_auth(
            lambda auth: client.get_access_token(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
            ),
        )
        output = {
            "username": login_result["username"],
            "roles": login_result["roles"],
            "ok": True,
            "source": login_result.get("source", "login"),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if args.command == "fetch-keyword-overview-bundle":
        payload = run_auth(
            lambda auth: client.fetch_keyword_overview_bundle(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                keyword=args.keyword,
                month=args.month,
                country=args.country,
                web_source=args.web_source,
                device=args.device,
                source_type=args.source_type,
                duration=args.duration,
                time_granularity=args.time_granularity,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.command == "fetch-website-analysis-bundle":
        payload = run_auth(
            lambda auth: client.fetch_website_analysis_bundle(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domain=args.domain,
                month=args.month,
                country=args.country,
                web_source=args.web_source,
                compare_domains=args.compare_domain,
                category=args.category,
                page_size=args.page_size,
                keyword_page_size=args.keyword_page_size,
                time_granularity=args.time_granularity,
                source_type=args.source_type,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.command == "fetch-website-traffic-trend-query":
        payload = run_auth(
            lambda auth: client.fetch_website_traffic_trend_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domains=args.domain,
                from_month=args.from_month,
                to_month=args.to_month,
                country=args.country,
                web_source=args.web_source,
                include_subdomains=not args.no_include_subdomains,
                time_granularity=args.time_granularity,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.command == "fetch-referral-traffic-query":
        payload = run_auth(
            lambda auth: client.fetch_referral_traffic_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domain=args.domain,
                from_month=args.from_month,
                to_month=args.to_month,
                country=args.country,
                web_source=args.web_source,
                page=args.page,
                sort=args.sort,
                asc=args.asc,
                all_pages=args.all_pages,
                max_pages=args.max_pages,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.command == "fetch-landing-pages-query":
        payload = run_auth(
            lambda auth: client.fetch_landing_pages_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domain=args.domain,
                month=args.month,
                country=args.country,
                web_source=args.web_source,
                include_subdomains=not args.no_include_subdomains,
                source_type=args.source_type,
                change=args.change,
                sort=args.sort,
                asc=args.asc,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.command == "fetch-search-keywords-query":
        payload = run_auth(
            lambda auth: client.fetch_search_keywords_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domain=args.domain,
                month=args.month,
                country=args.country,
                web_source=args.web_source,
                include_subdomains=not args.no_include_subdomains,
                source_type=args.source_type,
                change=args.change,
                sort=args.sort,
                asc=args.asc,
                page=args.page,
                page_size=args.page_size,
                time_granularity=args.time_granularity,
                include_branded=args.include_branded,
                include_non_branded=args.include_non_branded,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.command == "fetch-search-landing-pages-overview-query":
        payload = run_auth(
            lambda auth: client.fetch_search_landing_pages_overview_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domain=args.domain,
                month=args.month,
                country=args.country,
                web_source=args.web_source,
                include_subdomains=not args.no_include_subdomains,
                source_type=args.source_type,
                page_size=args.page_size,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.command == "fetch-search-keyword-performance-query":
        payload = run_auth(
            lambda auth: client.fetch_search_keyword_performance_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domain=args.domain,
                month=args.month,
                country=args.country,
                web_source=args.web_source,
                include_subdomains=not args.no_include_subdomains,
                source_type=args.source_type,
                page_size=args.page_size,
                time_granularity=args.time_granularity,
                duration=args.duration,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if args.command == "fetch-branded-keywords-query":
        payload = run_auth(
            lambda auth: client.fetch_branded_keywords_query(
                username=auth["username"],
                password=auth["password"],
                token=auth["token"] or None,
                domain=args.domain,
                month=args.month,
                country=args.country,
                web_source=args.web_source,
                include_subdomains=not args.no_include_subdomains,
                time_granularity=args.time_granularity,
            ),
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    payload = run_auth(
        lambda auth: client.fetch_generated_keywords(
            username=auth["username"],
            password=auth["password"],
            token=auth["token"] or None,
            keyword=args.keyword,
            month=args.month,
            country=args.country,
            web_source=args.web_source,
            rows_per_page=args.rows_per_page,
            sort=args.sort,
            suggestion_type=args.type,
        ),
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
