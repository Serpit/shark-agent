import importlib.util
import base64
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
from urllib.parse import urlparse


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "similarweb_client.py"
)


def load_module():
    if not MODULE_PATH.exists():
        raise AssertionError(f"Expected module to exist: {MODULE_PATH}")
    spec = importlib.util.spec_from_file_location("similarweb_client", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["similarweb_client"] = module
    spec.loader.exec_module(module)
    return module


def build_fake_token(expires_at: datetime) -> str:
    header = {"alg": "none", "typ": "JWT"}
    payload = {"exp": int(expires_at.timestamp())}

    def encode_part(value):
        raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")

    return f"{encode_part(header)}.{encode_part(payload)}.signature|opaque"


def build_fake_token_with_username(expires_at: datetime, username: str) -> str:
    header = {"alg": "none", "typ": "JWT"}
    payload = {"exp": int(expires_at.timestamp()), "uname": username}

    def encode_part(value):
        raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")

    return f"{encode_part(header)}.{encode_part(payload)}.signature|opaque"


class SimilarWebHarAnalysisTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_redact_sensitive_text_hides_login_credentials_and_tokens(self):
        text = json.dumps(
            {
                "url": "https://dash.3ue.com/api/account/login?username=user@example.com&password=super-secret&ts=1776324270626&__gmitm=proxy-token",
                "data": {
                    "token": "header.payload.signature|opaque",
                    "refreshToken": "refresh-me",
                },
            }
        )

        redacted = self.module.redact_sensitive_text(text)

        self.assertNotIn("super-secret", redacted)
        self.assertNotIn("user@example.com", redacted)
        self.assertNotIn("header.payload.signature|opaque", redacted)
        self.assertNotIn("refresh-me", redacted)
        self.assertNotIn("proxy-token", redacted)
        self.assertIn("<redacted>", redacted)

    def test_summarize_entry_omits_multipart_request_body(self):
        entry = {
            "request": {
                "method": "POST",
                "url": "https://sim.3ue.com/challenge/mp_verify",
                "postData": {
                    "mimeType": "multipart/form-data; boundary=secret-boundary",
                    "text": (
                        'Content-Disposition: form-data; name="existing_token"\r\n\r\n'
                        "sensitive-session-material"
                    ),
                },
            },
            "response": {
                "status": 200,
                "content": {"mimeType": "application/json", "text": '{"ok":true}'},
            },
        }

        summary = self.module.summarize_entry(entry)

        self.assertEqual("<multipart form data omitted>", summary["request_body"])
        self.assertNotIn("sensitive-session-material", json.dumps(summary))

    def test_summarize_har_entries_separates_data_and_internal_endpoints(self):
        entries = [
            {
                "request": {
                    "method": "GET",
                    "url": "https://sim.3ue.com/api/KeywordAnalysis/Overview/Stats?key=background+remover&country=999",
                },
                "response": {
                    "status": 200,
                    "content": {
                        "mimeType": "application/json",
                        "text": '{"Difficulty":93.0}',
                    },
                },
            },
            {
                "request": {
                    "method": "POST",
                    "url": "https://sim.3ue.com/api/KeywordGenerator/google/suggest?keyword=background+remover&type=Related",
                    "postData": {"mimeType": "application/json; charset=utf-8", "text": "[]"},
                },
                "response": {
                    "status": 200,
                    "content": {
                        "mimeType": "application/json",
                        "text": '{"records":[{"keyword":"background remover"}]}',
                    },
                },
            },
            {
                "request": {
                    "method": "GET",
                    "url": "https://sim.3ue.com/api/userdata/activation/list",
                },
                "response": {
                    "status": 200,
                    "content": {"mimeType": "application/json", "text": '{"ok":true}'},
                },
            },
            {
                "request": {
                    "method": "GET",
                    "url": "https://dash.3ue.com/api/account/login?username=user@example.com&password=secret",
                },
                "response": {
                    "status": 200,
                    "content": {
                        "mimeType": "application/json",
                        "text": '{"c":0,"data":{"token":"sensitive-token"}}',
                    },
                },
            },
        ]

        summary = self.module.summarize_har_entries(entries)

        self.assertEqual(2, len(summary["data_endpoints"]))
        self.assertEqual(1, len(summary["internal_endpoints"]))
        self.assertEqual(1, len(summary["control_plane_endpoints"]))
        self.assertEqual(
            "/api/KeywordAnalysis/Overview/Stats",
            summary["data_endpoints"][0]["path"],
        )
        self.assertEqual(
            "/api/userdata/activation/list",
            summary["internal_endpoints"][0]["path"],
        )
        self.assertEqual(
            "/api/account/login",
            summary["control_plane_endpoints"][0]["path"],
        )

    def test_summarize_har_entries_separates_website_analysis_data_endpoints(self):
        entries = [
            {
                "request": {
                    "method": "GET",
                    "url": "https://sim.3ue.com/api/WebsiteOverview/getheader?keys=pollo.ai&mainDomainOnly=true",
                },
                "response": {
                    "status": 200,
                    "content": {
                        "mimeType": "application/json",
                        "text": '{"pollo.ai":{"title":"Pollo AI"}}',
                    },
                },
            },
            {
                "request": {
                    "method": "GET",
                    "url": "https://sim.3ue.com/widgetApi/MarketingMixTotal/TrafficSourcesOverview/Table?keys=pollo.ai&country=999",
                },
                "response": {
                    "status": 200,
                    "content": {
                        "mimeType": "application/json",
                        "text": '{"Data":[{"Source":"Search","Share":0.5}]}',
                    },
                },
            },
            {
                "request": {
                    "method": "POST",
                    "url": "https://sim.3ue.com/api/backlinks/refdomains?Key=pollo.ai&Page=1&PageSize=100",
                    "postData": {"mimeType": "application/json; charset=utf-8", "text": "[]"},
                },
                "response": {
                    "status": 200,
                    "content": {
                        "mimeType": "application/json",
                        "text": '{"TotalRecords":1,"Records":[]}',
                    },
                },
            },
            {
                "request": {
                    "method": "POST",
                    "url": "https://sim.3ue.com/api/startupSettings?force=false",
                    "postData": {"mimeType": "application/json; charset=utf-8", "text": '["WebAnalysis"]'},
                },
                "response": {
                    "status": 200,
                    "content": {
                        "mimeType": "application/json",
                        "text": '{"settings":{"version":"1"}}',
                    },
                },
            },
            {
                "request": {
                    "method": "GET",
                    "url": "https://sim.3ue.com/api/account/collaborationHubLink",
                },
                "response": {
                    "status": 200,
                    "content": {
                        "mimeType": "application/json",
                        "text": '{"Succeeded":true}',
                    },
                },
            },
        ]

        summary = self.module.summarize_har_entries(entries)

        data_paths = {item["path"] for item in summary["data_endpoints"]}
        internal_paths = {item["path"] for item in summary["internal_endpoints"]}

        self.assertIn("/api/WebsiteOverview/getheader", data_paths)
        self.assertIn("/widgetApi/MarketingMixTotal/TrafficSourcesOverview/Table", data_paths)
        self.assertIn("/api/backlinks/refdomains", data_paths)
        self.assertIn("/api/startupSettings", internal_paths)
        self.assertIn("/api/account/collaborationHubLink", internal_paths)

    def test_build_keyword_bundle_contains_expected_endpoints(self):
        bundle = self.module.build_keyword_bundle(
            keyword="background remover",
            month="2026-03",
            country="999",
            web_source="Total",
            device="Total",
        )

        self.assertEqual("background remover", bundle["keyword"])
        self.assertEqual("2026|03|01", bundle["from"])
        self.assertEqual("2026|03|31", bundle["to"])
        requests = bundle["requests"]
        self.assertEqual(7, len(requests))
        self.assertEqual("/api/KeywordAnalysis/Overview/Stats", requests[0]["path"])
        self.assertEqual("GET", requests[0]["method"])
        self.assertEqual(
            "/api/KeywordGenerator/google/suggest",
            requests[-1]["path"],
        )
        self.assertEqual("POST", requests[-1]["method"])
        self.assertEqual("Related", requests[-1]["query"]["type"])

    def test_build_website_analysis_bundle_contains_expected_endpoints(self):
        bundle = self.module.build_website_analysis_bundle(
            domain="pollo.ai",
            month="2026-04",
            country="999",
            web_source="Total",
            compare_domains=["deevid.ai", "hailuoai.video"],
        )

        self.assertEqual("pollo.ai", bundle["domain"])
        self.assertEqual("2026|04|01", bundle["from"])
        self.assertEqual("2026|04|30", bundle["to"])

        requests = {request["name"]: request for request in bundle["requests"]}
        self.assertEqual(
            "/api/WebsiteOverview/getheader",
            requests["website_header"]["path"],
        )
        self.assertEqual("pollo.ai", requests["website_header"]["query"]["keys"])
        self.assertEqual(
            "pollo.ai,deevid.ai,hailuoai.video",
            requests["traffic_sources_bar"]["query"]["keys"],
        )
        self.assertEqual(
            "/api/searchoverview/overview/top-keywords",
            requests["search_top_keywords"]["path"],
        )
        self.assertEqual(
            "/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table",
            requests["website_keywords_table"]["path"],
        )
        self.assertEqual("POST", requests["website_keywords_table"]["method"])
        self.assertEqual([], requests["website_keywords_table"]["json_body"])
        self.assertIn(
            '{"url":"pollo.ai","searchType":"domain"}',
            requests["website_keywords_table"]["query"]["pageFilterJson"],
        )

    def test_build_website_traffic_trend_query_uses_month_range_and_monthly_graph(self):
        bundle = self.module.build_website_traffic_trend_query(
            domains=["app.topkey.io", "climatenest.org"],
            from_month="2026-01",
            to_month="2026-06",
        )

        self.assertEqual(["app.topkey.io", "climatenest.org"], bundle["domains"])
        self.assertEqual("2026|01|01", bundle["from"])
        self.assertEqual("2026|06|30", bundle["to"])
        request = bundle["requests"][0]
        self.assertEqual(
            "/widgetApi/WebsiteOverview/EngagementVisits/Graph",
            request["path"],
        )
        self.assertEqual(
            "app.topkey.io,climatenest.org",
            request["query"]["keys"],
        )
        self.assertEqual("Monthly", request["query"]["timeGranularity"])
        self.assertEqual("true", request["query"]["includeSubDomains"])

    def test_extract_monthly_website_visits_sums_graph_points_by_month(self):
        payload = {
            "Data": {
                "app.topkey.io": {
                    "Total": [
                        [
                            {"Key": "2026-05-04", "Value": 100.25},
                            {"Key": "2026-05-11", "Value": 49.75},
                            {"Key": "2026-06-01", "Value": 225.0},
                        ]
                    ]
                },
                "climatenest.org": {
                    "Total": [
                        [
                            {"Key": "2026-06-01", "Value": 80.0},
                        ]
                    ]
                },
            },
            "KeysDataVerification": {
                "app.topkey.io": False,
                "climatenest.org": True,
            },
        }

        result = self.module.extract_monthly_website_visits(payload)

        self.assertEqual(
            {
                "app.topkey.io": {
                    "data_verified": False,
                    "months": [
                        {"month": "2026-05", "visits": 150.0},
                        {"month": "2026-06", "visits": 225.0},
                    ],
                },
                "climatenest.org": {
                    "data_verified": True,
                    "months": [
                        {"month": "2026-06", "visits": 80.0},
                    ],
                },
            },
            result,
        )

    def test_build_referral_traffic_query_uses_observed_range_and_page(self):
        bundle = self.module.build_referral_traffic_query(
            domain="checkout.stripe.com",
            from_month="2026-01",
            to_month="2026-06",
            page=22,
        )

        self.assertEqual("checkout.stripe.com", bundle["domain"])
        self.assertEqual("2026|01|01", bundle["from"])
        self.assertEqual("2026|06|30", bundle["to"])
        self.assertEqual(22, bundle["page"])

        requests = {request["name"]: request for request in bundle["requests"]}
        totals = requests["referral_totals"]
        table = requests["referral_table"]
        self.assertEqual(
            "/api/websiteanalysis/GetTrafficSourcesTotalReferrals",
            totals["path"],
        )
        self.assertEqual(
            "/api/websiteanalysis/GetTrafficSourcesTotalReferralsTable",
            table["path"],
        )
        self.assertEqual("incomingTraffic", table["query"]["selectedTab"])
        self.assertEqual("TotalShare desc", table["query"]["orderBy"])
        self.assertEqual("false", table["query"]["asc"])
        self.assertEqual("22", table["query"]["page"])

    def test_build_referral_traffic_query_rejects_reversed_range(self):
        with self.assertRaisesRegex(ValueError, "from_month"):
            self.module.build_referral_traffic_query(
                domain="paypal.com",
                from_month="2026-06",
                to_month="2026-01",
            )

    def test_build_landing_pages_query_defaults_to_new_organic_click_share(self):
        bundle = self.module.build_landing_pages_query(
            domain="pinterest.com",
            month="2026-04",
            country="999",
            web_source="Total",
        )

        self.assertEqual("pinterest.com", bundle["domain"])
        self.assertEqual("2026|04|01", bundle["from"])
        self.assertEqual("2026|04|30", bundle["to"])
        self.assertEqual("organic", bundle["source_type"])
        self.assertEqual("New", bundle["change"])
        self.assertEqual("ClicksShare", bundle["sort"])
        self.assertFalse(bundle["asc"])

        request = bundle["requests"][0]
        self.assertEqual("landing_pages", request["name"])
        self.assertEqual("POST", request["method"])
        self.assertEqual("/api/websiteOrganicLandingPagesV2", request["path"])
        self.assertEqual([], request["json_body"])
        self.assertEqual("pinterest.com", request["query"]["key"])
        self.assertEqual("New", request["query"]["Change"])
        self.assertEqual("organic", request["query"]["sourceType"])
        self.assertEqual("ClicksShare", request["query"]["sort"])
        self.assertEqual("false", request["query"]["asc"])
        self.assertEqual("true", request["query"]["includeSubDomains"])
        self.assertIn(
            '{"url":"pinterest.com","searchType":"domain"}',
            request["query"]["pageFilterJson"],
        )

    def test_build_search_keywords_query_defaults_to_new_click_share(self):
        bundle = self.module.build_search_keywords_query(
            domain="pinterest.com",
            month="2026-04",
            country="999",
            web_source="Total",
        )

        self.assertEqual("pinterest.com", bundle["domain"])
        self.assertEqual("2026|04|01", bundle["from"])
        self.assertEqual("2026|04|30", bundle["to"])
        self.assertEqual("all", bundle["source_type"])
        self.assertEqual("New", bundle["change"])
        self.assertEqual("Share", bundle["sort"])
        self.assertFalse(bundle["asc"])

        requests = {request["name"]: request for request in bundle["requests"]}
        total = requests["search_keywords_total"]
        table = requests["search_keywords_table"]
        self.assertEqual(
            "/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/PresetsTotal",
            total["path"],
        )
        self.assertEqual(
            "/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table",
            table["path"],
        )
        self.assertEqual("POST", total["method"])
        self.assertEqual("POST", table["method"])
        self.assertEqual([], total["json_body"])
        self.assertEqual([], table["json_body"])
        self.assertEqual("pinterest.com", table["query"]["keys"])
        self.assertEqual("New", table["query"]["Change"])
        self.assertEqual("all", table["query"]["sourceType"])
        self.assertEqual("Share", table["query"]["sort"])
        self.assertEqual("false", table["query"]["asc"])
        self.assertEqual("true", table["query"]["includeSubDomains"])
        self.assertEqual("false", table["query"]["IncludeBranded"])
        self.assertEqual("false", table["query"]["IncludeNoneBranded"])
        self.assertIn(
            '{"url":"pinterest.com","searchType":"domain"}',
            table["query"]["pageFilterJson"],
        )

    def test_build_search_landing_pages_overview_query_uses_lightweight_endpoint(self):
        bundle = self.module.build_search_landing_pages_overview_query(
            domain="pinterest.com",
            month="2026-04",
            country="999",
            web_source="Total",
        )

        self.assertEqual("pinterest.com", bundle["domain"])
        self.assertEqual("2026|04|01", bundle["from"])
        self.assertEqual("2026|04|30", bundle["to"])
        self.assertEqual("all", bundle["source_type"])

        request = bundle["requests"][0]
        self.assertEqual("search_landing_pages_overview", request["name"])
        self.assertEqual("GET", request["method"])
        self.assertEqual("/api/searchoverview/keywords/landing-pages", request["path"])
        self.assertEqual("pinterest.com", request["query"]["keys"])
        self.assertEqual("all", request["query"]["SourceType"])
        self.assertEqual("5", request["query"]["pageSize"])

    def test_build_search_keyword_performance_query_uses_widget_endpoint(self):
        bundle = self.module.build_search_keyword_performance_query(
            domain="pinterest.com",
            month="2026-04",
            country="999",
            web_source="Total",
        )

        request = bundle["requests"][0]
        self.assertEqual("search_keyword_performance", request["name"])
        self.assertEqual("GET", request["method"])
        self.assertEqual(
            "/widgetApi/SearchKeywordsV2/WebsitePerformance/Table",
            request["path"],
        )
        self.assertEqual("pinterest.com", request["query"]["keys"])
        self.assertEqual("Organic", request["query"]["SourceType"])
        self.assertEqual("Monthly", request["query"]["timeGranularity"])
        self.assertEqual("1m", request["query"]["duration"])
        self.assertEqual("100", request["query"]["pageSize"])

    def test_build_branded_keywords_query_uses_pie_chart_endpoint(self):
        bundle = self.module.build_branded_keywords_query(
            domain="pinterest.com",
            month="2026-04",
            country="999",
            web_source="Total",
        )

        request = bundle["requests"][0]
        self.assertEqual("branded_keywords", request["name"])
        self.assertEqual("GET", request["method"])
        self.assertEqual(
            "/widgetApi/TrafficSourcesSearchV2/BrandedKeywords/WebsitePerformance/PieChart",
            request["path"],
        )
        self.assertEqual("pinterest.com", request["query"]["keys"])
        self.assertEqual("true", request["query"]["includeSubDomains"])
        self.assertEqual("Monthly", request["query"]["timeGranularity"])

    def test_build_headers_sets_xhr_defaults_and_optional_cookie(self):
        headers = self.module.build_headers(
            cookie="session=abc123",
            x_sw_page="https://pro.similarweb.com/#/digitalsuite/acquisition/keyword/organic/search/999/2026.03-2026.03/overview_2?keyword=background%20remover",
            x_sw_page_view_id="view-id-1",
        )

        self.assertEqual("XMLHttpRequest", headers["x-requested-with"])
        self.assertEqual("application/json", headers["accept"])
        self.assertEqual("session=abc123", headers["cookie"])
        self.assertEqual("view-id-1", headers["x-sw-page-view-id"])

    def test_extract_login_token_returns_bearer_token(self):
        payload = {
            "c": 0,
            "data": {
                "token": "jwt-token|opaque",
                "username": "demo",
            },
        }

        token = self.module.extract_login_token(payload)

        self.assertEqual("jwt-token|opaque", token)

    def test_extract_login_token_rejects_unsuccessful_payload(self):
        with self.assertRaises(ValueError):
            self.module.extract_login_token({"c": 401, "msg": "expired"})

    def test_is_login_redirect_response_detects_html_redirect(self):
        response = SimpleNamespace(
            headers={"content-type": "text/html; charset=utf-8"},
            text="<script> location.href = 'https://dash.3ue.com?msg=登录过期';</script>",
        )

        self.assertTrue(self.module.is_login_redirect_response(response))

    def test_build_authenticated_headers_adds_bearer_token(self):
        token = build_fake_token_with_username(
            datetime.now(timezone.utc) + timedelta(hours=1),
            "demo user",
        )
        headers = self.module.build_authenticated_headers(
            token=token,
            x_sw_page="https://pro.similarweb.com/#/digitalsuite/acquisition/keyword/organic/search/999/2026.03-2026.03/overview_2?keyword=background%20remover",
            x_sw_page_view_id="view-id-1",
        )

        self.assertEqual(f"Bearer {token}", headers["authorization"])
        self.assertEqual("XMLHttpRequest", headers["x-requested-with"])
        self.assertIn("GMITM_token=", headers["cookie"])
        self.assertIn("GMITM_uname=demo%20user", headers["cookie"])

    def test_fetch_generated_keywords_returns_full_json_payload(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {"c": 0, "data": {"token": "jwt-token|opaque"}}
            login_response.raise_for_status.return_value = None

            suggest_response = mock.Mock()
            suggest_response.headers = {"content-type": "application/json; charset=utf-8"}
            suggest_response.text = '{"records":[{"keyword":"background remover"}],"totalRecords":1}'
            suggest_response.json.return_value = {
                "records": [{"keyword": "background remover"}],
                "totalRecords": 1,
                "totalClicks": 10.0,
                "totalVolume": 20.0,
                "maxScore": 5.0,
            }
            suggest_response.raise_for_status.return_value = None

            session.get.return_value = login_response
            session.post.return_value = suggest_response

            client = self.module.SimilarWebClient(session=session)
            payload = client.fetch_generated_keywords(
                username="demo",
                password="secret",
                keyword="background remover",
                month="2026-03",
            )

        self.assertEqual(1, payload["totalRecords"])
        self.assertEqual("background remover", payload["records"][0]["keyword"])
        login_call = session.get.call_args
        self.assertEqual("https://dash.3ue.com/api/account/login", login_call.args[0])
        post_call = session.post.call_args
        self.assertEqual(
            "Bearer jwt-token|opaque",
            post_call.kwargs["headers"]["authorization"],
        )
        self.assertEqual([], post_call.kwargs["json"])

    def test_fetch_generated_keywords_rejects_login_redirect_html(self):
        session = mock.Mock()
        login_response = mock.Mock()
        login_response.json.return_value = {"c": 0, "data": {"token": "jwt-token|opaque"}}
        login_response.raise_for_status.return_value = None

        suggest_response = mock.Mock()
        suggest_response.headers = {"content-type": "text/html; charset=utf-8"}
        suggest_response.text = "<script> location.href = 'https://dash.3ue.com?msg=登录过期';</script>"
        suggest_response.raise_for_status.return_value = None

        session.get.return_value = login_response
        session.post.return_value = suggest_response

        client = self.module.SimilarWebClient(session=session)

        with self.assertRaises(RuntimeError):
            client.fetch_generated_keywords(
                username="demo",
                password="secret",
                keyword="background remover",
                month="2026-03",
            )

    def test_fetch_keyword_overview_bundle_returns_payloads_for_all_overview_endpoints(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {
                    "token": "jwt-token|opaque",
                    "username": "demo",
                },
            }
            login_response.raise_for_status.return_value = None

            def build_json_response(payload):
                response = mock.Mock()
                response.headers = {"content-type": "application/json; charset=utf-8"}
                response.text = json.dumps(payload)
                response.json.return_value = payload
                response.raise_for_status.return_value = None
                return response

            session.get.side_effect = [
                login_response,
                build_json_response({"Difficulty": 93.0}),
                build_json_response({"Average": {"Volume": 1200}}),
                build_json_response({"Competitors": [{"Domain": "example.com"}]}),
                build_json_response({"Pages": [{"Url": "https://example.com/page"}]}),
                build_json_response({"Data": {"background remover": {"MonthToVisits": []}}}),
                build_json_response({"Data": {"background remover": {"Volume": 1200}}}),
            ]

            client = self.module.SimilarWebClient(session=session)
            payload = client.fetch_keyword_overview_bundle(
                username="demo",
                password="secret",
                keyword="background remover",
                month="2026-03",
            )

        self.assertEqual("background remover", payload["keyword"])
        self.assertEqual("2026-03", payload["month"])
        self.assertEqual({"Difficulty": 93.0}, payload["overview_stats"])
        self.assertEqual({"Average": {"Volume": 1200}}, payload["volume_clicks_trend"])
        self.assertEqual(
            {"Competitors": [{"Domain": "example.com"}]},
            payload["top_sites"],
        )
        self.assertEqual(
            {"Pages": [{"Url": "https://example.com/page"}]},
            payload["top_pages"],
        )
        self.assertEqual(
            {"Data": {"background remover": {"MonthToVisits": []}}},
            payload["device_traffic"],
        )
        self.assertEqual(
            {"Data": {"background remover": {"Volume": 1200}}},
            payload["single_metric"],
        )

        self.assertEqual(7, session.get.call_count)
        stats_call = session.get.call_args_list[1]
        self.assertIn(
            "/api/KeywordAnalysis/Overview/Stats",
            stats_call.args[0],
        )
        self.assertEqual(
            "Bearer jwt-token|opaque",
            stats_call.kwargs["headers"]["authorization"],
        )
        self.assertIn("GMITM_token=", stats_call.kwargs["headers"]["cookie"])

    def test_fetch_keyword_overview_bundle_rejects_login_redirect_html(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {
                    "token": "jwt-token|opaque",
                    "username": "demo",
                },
            }
            login_response.raise_for_status.return_value = None

            redirect_response = mock.Mock()
            redirect_response.headers = {"content-type": "text/html; charset=utf-8"}
            redirect_response.text = "<script> location.href = 'https://dash.3ue.com?msg=登录过期';</script>"
            redirect_response.raise_for_status.return_value = None

            session.get.side_effect = [login_response, redirect_response]

            client = self.module.SimilarWebClient(session=session)

            with self.assertRaises(RuntimeError):
                client.fetch_keyword_overview_bundle(
                    username="demo",
                    password="secret",
                    keyword="background remover",
                    month="2026-03",
                )

    def test_fetch_website_analysis_bundle_executes_get_and_post_requests(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {
                    "token": "jwt-token|opaque",
                    "username": "demo",
                },
            }
            login_response.raise_for_status.return_value = None

            def build_json_response(payload):
                response = mock.Mock()
                response.headers = {"content-type": "application/json; charset=utf-8"}
                response.text = json.dumps(payload)
                response.json.return_value = payload
                response.raise_for_status.return_value = None
                return response

            session.get.side_effect = [
                login_response,
                build_json_response({"pollo.ai": {"title": "Pollo AI"}}),
                build_json_response([{"Domain": "example.com"}]),
            ]
            session.post.side_effect = [
                build_json_response(
                    {
                        "SearchEngines": ["Google"],
                        "TotalCount": 1,
                        "Data": {"Records": []},
                    }
                )
            ]

            client = self.module.SimilarWebClient(session=session)
            bundle = {
                "domain": "pollo.ai",
                "month": "2026-04",
                "from": "2026|04|01",
                "to": "2026|04|30",
                "country": "999",
                "web_source": "Total",
                "requests": [
                    {
                        "name": "website_header",
                        "method": "GET",
                        "path": "/api/WebsiteOverview/getheader",
                        "query": {"keys": "pollo.ai"},
                    },
                    {
                        "name": "similar_sites",
                        "method": "GET",
                        "path": "/api/WebsiteOverview/getsimilarsites",
                        "query": {"key": "pollo.ai", "limit": "5"},
                    },
                    {
                        "name": "website_keywords_table",
                        "method": "POST",
                        "path": "/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table",
                        "query": {"keys": "pollo.ai"},
                        "json_body": [],
                    },
                ],
            }

            with mock.patch.object(
                self.module,
                "build_website_analysis_bundle",
                return_value=bundle,
            ):
                payload = client.fetch_website_analysis_bundle(
                    username="demo",
                    password="secret",
                    domain="pollo.ai",
                    month="2026-04",
                )

        self.assertEqual("pollo.ai", payload["domain"])
        self.assertEqual({"pollo.ai": {"title": "Pollo AI"}}, payload["website_header"])
        self.assertEqual([{"Domain": "example.com"}], payload["similar_sites"])
        self.assertEqual(
            {"SearchEngines": ["Google"], "TotalCount": 1, "Data": {"Records": []}},
            payload["website_keywords_table"],
        )
        self.assertEqual(3, session.get.call_count)
        self.assertEqual(1, session.post.call_count)
        post_call = session.post.call_args
        self.assertEqual(
            "https://sim.3ue.com/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table",
            post_call.args[0],
        )
        self.assertEqual([], post_call.kwargs["json"])
        self.assertEqual(
            "Bearer jwt-token|opaque",
            post_call.kwargs["headers"]["authorization"],
        )

    def test_fetch_website_traffic_trend_query_returns_normalized_months(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {
                    "token": "jwt-token|opaque",
                    "username": "demo",
                },
            }
            login_response.raise_for_status.return_value = None

            trend_payload = {
                "Data": {
                    "app.topkey.io": {
                        "Total": [
                            [
                                {"Key": "2026-05-01", "Value": 42000.0},
                                {"Key": "2026-06-01", "Value": 62853.0},
                            ]
                        ]
                    }
                },
                "KeysDataVerification": {"app.topkey.io": False},
            }
            trend_response = mock.Mock()
            trend_response.headers = {
                "content-type": "application/json; charset=utf-8"
            }
            trend_response.text = json.dumps(trend_payload)
            trend_response.json.return_value = trend_payload
            trend_response.raise_for_status.return_value = None
            session.get.side_effect = [login_response, trend_response]

            client = self.module.SimilarWebClient(session=session)
            payload = client.fetch_website_traffic_trend_query(
                username="demo",
                password="secret",
                domains=["app.topkey.io"],
                from_month="2026-05",
                to_month="2026-06",
            )

        self.assertEqual(
            [
                {"month": "2026-05", "visits": 42000.0},
                {"month": "2026-06", "visits": 62853.0},
            ],
            payload["monthly_visits"]["app.topkey.io"]["months"],
        )
        trend_call = session.get.call_args_list[1]
        self.assertIn(
            "/widgetApi/WebsiteOverview/EngagementVisits/Graph",
            trend_call.args[0],
        )
        self.assertEqual("2026|05|01", trend_call.kwargs["params"]["from"])
        self.assertEqual("2026|06|30", trend_call.kwargs["params"]["to"])

    def test_fetch_referral_traffic_query_aggregates_all_pages(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {"token": "jwt-token|opaque", "username": "demo"},
            }
            login_response.raise_for_status.return_value = None

            def json_response(payload):
                response = mock.Mock()
                response.headers = {
                    "content-type": "application/json; charset=utf-8"
                }
                response.text = json.dumps(payload)
                response.json.return_value = payload
                response.raise_for_status.return_value = None
                return response

            totals_payload = {
                "dictionary": {"checkout.stripe.com": {"TotalVisits": 1000}},
                "Categories": [],
            }
            page_one_records = [
                {
                    "Domain": f"source-{index}.example",
                    "Rank": index,
                    "Change": 0.1,
                    "TotalShare": 0.01,
                    "TotalSharePerMonth": [],
                    "TotalVisitsAndSharePerMonth": {},
                }
                for index in range(1, 101)
            ]
            page_two_records = [
                {
                    "Domain": f"source-{index}.example",
                    "Rank": index,
                    "Change": 0.2,
                    "TotalShare": 0.001,
                    "TotalSharePerMonth": [],
                    "TotalVisitsAndSharePerMonth": {},
                }
                for index in range(101, 172)
            ]
            page_one = {
                "TotalShare": 1.0,
                "TotalVisits": 1000.0,
                "TotalVisitsGlobalList": {"checkout.stripe.com": 1000.0},
                "TopCategories": [],
                "Categories": {},
                "AllCategories": [],
                "Topics": [],
                "TotalCount": 171,
                "TotalUnGroupedCount": 171,
                "Records": page_one_records,
            }
            page_two = {**page_one, "Records": page_two_records}
            session.get.side_effect = [
                login_response,
                json_response(totals_payload),
                json_response(page_one),
                json_response(page_two),
            ]

            client = self.module.SimilarWebClient(session=session)
            result = client.fetch_referral_traffic_query(
                username="demo",
                password="secret",
                domain="checkout.stripe.com",
                from_month="2026-01",
                to_month="2026-06",
                all_pages=True,
            )

        self.assertEqual(totals_payload, result["referral_totals"])
        self.assertEqual(171, len(result["referral_table"]["Records"]))
        self.assertEqual("source-1.example", result["referral_table"]["Records"][0]["Domain"])
        self.assertEqual("source-171.example", result["referral_table"]["Records"][-1]["Domain"])
        self.assertEqual(
            {
                "all_pages": True,
                "start_page": 1,
                "end_page": 2,
                "pages_fetched": 2,
                "page_size": 100,
                "total_count": 171,
                "records_returned": 171,
                "complete": True,
            },
            result["pagination"],
        )
        data_calls = session.get.call_args_list[1:]
        self.assertEqual(
            [
                "/api/websiteanalysis/GetTrafficSourcesTotalReferrals",
                "/api/websiteanalysis/GetTrafficSourcesTotalReferralsTable",
                "/api/websiteanalysis/GetTrafficSourcesTotalReferralsTable",
            ],
            [urlparse(call.args[0]).path for call in data_calls],
        )
        self.assertEqual("1", data_calls[1].kwargs["params"]["page"])
        self.assertEqual("2", data_calls[2].kwargs["params"]["page"])

    def test_fetch_landing_pages_query_posts_observed_new_clicks_request(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {
                    "token": "jwt-token|opaque",
                    "username": "demo",
                },
            }
            login_response.raise_for_status.return_value = None

            landing_response = mock.Mock()
            landing_payload = {
                "FromAlternativeSources": False,
                "TotalCount": 1722121,
                "Data": [
                    {
                        "Url": "es.pinterest.com/ideas/lector-manga/908210122266",
                        "Clicks": 315800.0,
                        "ClicksShare": 0.0048231869750125925,
                        "ChangeState": "New",
                        "TopKeyword": "lector manga",
                    }
                ],
            }
            landing_response.headers = {"content-type": "application/json; charset=utf-8"}
            landing_response.text = json.dumps(landing_payload)
            landing_response.json.return_value = landing_payload
            landing_response.raise_for_status.return_value = None

            session.get.return_value = login_response
            session.post.return_value = landing_response

            client = self.module.SimilarWebClient(session=session)
            payload = client.fetch_landing_pages_query(
                username="demo",
                password="secret",
                domain="pinterest.com",
                month="2026-04",
            )

        self.assertEqual("pinterest.com", payload["domain"])
        self.assertEqual("New", payload["change"])
        self.assertEqual("ClicksShare", payload["sort"])
        self.assertEqual(landing_payload, payload["landing_pages"])
        self.assertEqual(1, session.post.call_count)
        post_call = session.post.call_args
        self.assertEqual(
            "https://sim.3ue.com/api/websiteOrganicLandingPagesV2",
            post_call.args[0],
        )
        self.assertEqual([], post_call.kwargs["json"])
        self.assertEqual("New", post_call.kwargs["params"]["Change"])
        self.assertEqual("organic", post_call.kwargs["params"]["sourceType"])
        self.assertEqual("ClicksShare", post_call.kwargs["params"]["sort"])
        self.assertEqual("false", post_call.kwargs["params"]["asc"])
        self.assertEqual(
            "Bearer jwt-token|opaque",
            post_call.kwargs["headers"]["authorization"],
        )

    def test_fetch_search_keywords_query_posts_total_and_table_requests(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {
                    "token": "jwt-token|opaque",
                    "username": "demo",
                },
            }
            login_response.raise_for_status.return_value = None

            total_response = mock.Mock()
            total_payload = {
                "TotalCompetitive": {},
                "TotalPresets": {"LongTail": 906302},
                "Total": 2011526,
            }
            total_response.headers = {"content-type": "application/json; charset=utf-8"}
            total_response.text = json.dumps(total_payload)
            total_response.json.return_value = total_payload
            total_response.raise_for_status.return_value = None

            table_response = mock.Mock()
            table_payload = {
                "SearchEngines": ["Google"],
                "TotalCount": 2011526,
                "Data": {
                    "KeywordsCount": 2011526,
                    "OverallClicks": 85463790.0,
                    "Records": [
                        {
                            "Keyword": "boldog húsvéti ünnepeket",
                            "Clicks": 21480,
                            "OrganicClicks": 21480.0,
                        }
                    ],
                },
            }
            table_response.headers = {"content-type": "application/json; charset=utf-8"}
            table_response.text = json.dumps(table_payload)
            table_response.json.return_value = table_payload
            table_response.raise_for_status.return_value = None

            session.get.return_value = login_response
            session.post.side_effect = [total_response, table_response]

            client = self.module.SimilarWebClient(session=session)
            payload = client.fetch_search_keywords_query(
                username="demo",
                password="secret",
                domain="pinterest.com",
                month="2026-04",
            )

        self.assertEqual("pinterest.com", payload["domain"])
        self.assertEqual("New", payload["change"])
        self.assertEqual("Share", payload["sort"])
        self.assertEqual(total_payload, payload["search_keywords_total"])
        self.assertEqual(table_payload, payload["search_keywords_table"])
        self.assertEqual(2, session.post.call_count)
        total_call = session.post.call_args_list[0]
        table_call = session.post.call_args_list[1]
        self.assertEqual(
            "https://sim.3ue.com/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/PresetsTotal",
            total_call.args[0],
        )
        self.assertEqual(
            "https://sim.3ue.com/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table",
            table_call.args[0],
        )
        self.assertEqual([], total_call.kwargs["json"])
        self.assertEqual([], table_call.kwargs["json"])
        self.assertEqual("New", table_call.kwargs["params"]["Change"])
        self.assertEqual("all", table_call.kwargs["params"]["sourceType"])
        self.assertEqual("Share", table_call.kwargs["params"]["sort"])
        self.assertEqual("false", table_call.kwargs["params"]["asc"])
        self.assertEqual(
            "Bearer jwt-token|opaque",
            table_call.kwargs["headers"]["authorization"],
        )

    def test_fetch_search_landing_pages_overview_query_gets_payload(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {"token": "jwt-token|opaque", "username": "demo"},
            }
            login_response.raise_for_status.return_value = None

            response = mock.Mock()
            payload = {
                "Data": [
                    {
                        "Url": "www.pinterest.com/ideas/example",
                        "Clicks": 1000,
                        "ClicksShare": 0.01,
                        "TopKeyword": "example",
                    }
                ]
            }
            response.headers = {"content-type": "application/json; charset=utf-8"}
            response.text = json.dumps(payload)
            response.json.return_value = payload
            response.raise_for_status.return_value = None

            session.get.side_effect = [login_response, response]

            client = self.module.SimilarWebClient(session=session)
            result = client.fetch_search_landing_pages_overview_query(
                username="demo",
                password="secret",
                domain="pinterest.com",
                month="2026-04",
            )

        self.assertEqual(payload, result["search_landing_pages_overview"])
        data_call = session.get.call_args_list[1]
        self.assertEqual(
            "https://sim.3ue.com/api/searchoverview/keywords/landing-pages",
            data_call.args[0],
        )
        self.assertEqual("all", data_call.kwargs["params"]["SourceType"])
        self.assertEqual(
            "Bearer jwt-token|opaque",
            data_call.kwargs["headers"]["authorization"],
        )

    def test_fetch_search_keyword_performance_query_gets_payload(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {"token": "jwt-token|opaque", "username": "demo"},
            }
            login_response.raise_for_status.return_value = None

            response = mock.Mock()
            payload = {"TotalCount": 1, "Data": [{"Keyword": "example", "Clicks": 10}]}
            response.headers = {"content-type": "application/json; charset=utf-8"}
            response.text = json.dumps(payload)
            response.json.return_value = payload
            response.raise_for_status.return_value = None

            session.get.side_effect = [login_response, response]

            client = self.module.SimilarWebClient(session=session)
            result = client.fetch_search_keyword_performance_query(
                username="demo",
                password="secret",
                domain="pinterest.com",
                month="2026-04",
            )

        self.assertEqual(payload, result["search_keyword_performance"])
        data_call = session.get.call_args_list[1]
        self.assertEqual(
            "https://sim.3ue.com/widgetApi/SearchKeywordsV2/WebsitePerformance/Table",
            data_call.args[0],
        )
        self.assertEqual("Organic", data_call.kwargs["params"]["SourceType"])

    def test_fetch_branded_keywords_query_gets_payload(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            session = mock.Mock()
            login_response = mock.Mock()
            login_response.json.return_value = {
                "c": 0,
                "data": {"token": "jwt-token|opaque", "username": "demo"},
            }
            login_response.raise_for_status.return_value = None

            response = mock.Mock()
            payload = {"Data": {"Branded": 0.2, "NonBranded": 0.8}}
            response.headers = {"content-type": "application/json; charset=utf-8"}
            response.text = json.dumps(payload)
            response.json.return_value = payload
            response.raise_for_status.return_value = None

            session.get.side_effect = [login_response, response]

            client = self.module.SimilarWebClient(session=session)
            result = client.fetch_branded_keywords_query(
                username="demo",
                password="secret",
                domain="pinterest.com",
                month="2026-04",
            )

        self.assertEqual(payload, result["branded_keywords"])
        data_call = session.get.call_args_list[1]
        self.assertEqual(
            "https://sim.3ue.com/widgetApi/TrafficSourcesSearchV2/BrandedKeywords/WebsitePerformance/PieChart",
            data_call.args[0],
        )
        self.assertEqual("true", data_call.kwargs["params"]["includeSubDomains"])

    def test_save_token_cache_and_load_cached_token_roundtrip(self):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        token = build_fake_token(future)

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "token_cache.json"
            client = self.module.SimilarWebClient(cache_path=cache_path)

            client.save_token_cache(
                username="demo",
                token=token,
                roles=["similarweb.pro"],
            )

            cached = client.load_cached_token("demo")

        self.assertEqual(token, cached["token"])
        self.assertEqual(["similarweb.pro"], cached["roles"])
        self.assertTrue(cached["expires_at"])

    def test_get_access_token_uses_valid_cached_token_without_login(self):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        token = build_fake_token(future)

        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "token_cache.json"
            session = mock.Mock()
            client = self.module.SimilarWebClient(session=session, cache_path=cache_path)
            client.save_token_cache(username="demo", token=token, roles=["similarweb.pro"])

            result = client.get_access_token(username="demo", password="secret")

        self.assertEqual(token, result["token"])
        session.get.assert_not_called()

    def test_get_access_token_relogs_when_cached_token_is_expired(self):
        expired = datetime.now(timezone.utc) - timedelta(minutes=1)
        cached_token = build_fake_token(expired)
        fresh_token = build_fake_token(datetime.now(timezone.utc) + timedelta(hours=1))

        login_response = mock.Mock()
        login_response.json.return_value = {
            "c": 0,
            "data": {
                "token": fresh_token,
                "username": "demo",
                "roles": ["similarweb.pro"],
            },
        }
        login_response.raise_for_status.return_value = None

        with mock.patch.dict(os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "token_cache.json"
            session = mock.Mock()
            session.get.return_value = login_response
            client = self.module.SimilarWebClient(session=session, cache_path=cache_path)
            client.save_token_cache(username="demo", token=cached_token, roles=["stale"])

            result = client.get_access_token(username="demo", password="secret")
            cached = client.load_cached_token("demo")

        self.assertEqual(fresh_token, result["token"])
        self.assertEqual(fresh_token, cached["token"])
        session.get.assert_called_once()

    def test_get_access_token_uses_fallback_token_without_login(self):
        token = build_fake_token_with_username(
            datetime.now(timezone.utc) + timedelta(hours=1),
            "token-user",
        )
        session = mock.Mock()
        client = self.module.SimilarWebClient(session=session)

        try:
            result = client.get_access_token(
                username="token-user",
                password="",
                token=token,
            )
        except Exception as error:
            result = error

        self.assertIsInstance(result, dict)
        self.assertEqual(token, result["token"])
        self.assertEqual("fallback_token", result["source"])
        session.get.assert_not_called()

    def test_invalidate_cached_token_removes_matching_record(self):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        token = build_fake_token(future)

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = Path(tmpdir) / "token_cache.json"
            client = self.module.SimilarWebClient(cache_path=cache_path)
            client.save_token_cache(username="demo", token=token)

            invalidator = getattr(client, "invalidate_cached_token", None)
            self.assertIsNotNone(invalidator)
            removed = invalidator("demo")

            self.assertTrue(removed)
            self.assertIsNone(client.load_cached_token("demo"))

    def test_resolve_auth_candidates_puts_tokens_after_credentials(self):
        token = build_fake_token_with_username(
            datetime.now(timezone.utc) + timedelta(hours=1),
            "token-user",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            project = root / "project"
            home = root / "home"
            project.mkdir()
            home.mkdir()
            project_env = project / ".env"
            project_env.write_text(
                f"SIMILARWEB_TOKEN={token}\n",
                encoding="utf-8",
            )
            global_env = home / ".config" / "agent-skills" / ".env"
            global_env.parent.mkdir(parents=True)
            global_env.write_text(
                "SIMILARWEB_USERNAME=global-user\n"
                "SIMILARWEB_PASSWORD=global-pass\n",
                encoding="utf-8",
            )

            with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(
                self.module,
                "discover_auth_env_files",
                return_value=[project_env, global_env],
            ):
                candidates = self.module.resolve_auth_candidates(
                    username=None,
                    password=None,
                    env_file=None,
                    project=None,
                    start_dir=project,
                    caller_dir=project,
                    home_dir=home,
                    skill_dir=None,
                )

        self.assertEqual(
            [
                {
                    "token": "",
                    "username": "global-user",
                    "password": "global-pass",
                    "source": str(global_env),
                },
                {
                    "token": token,
                    "username": "token-user",
                    "password": "",
                    "source": str(project_env),
                }
            ],
            candidates,
        )

    def test_run_with_auth_candidates_retries_after_cached_token_is_invalidated(self):
        rejected = self.module.requests.HTTPError("401 Client Error")
        rejected.response = SimpleNamespace(status_code=401)
        calls = []
        invalidations = []

        def operation(auth):
            calls.append(auth["source"])
            if len(calls) == 1:
                raise rejected
            return "ok"

        try:
            result = self.module.run_with_auth_candidates(
                [
                    {
                        "username": "user",
                        "password": "pass",
                        "source": "credentials",
                    }
                ],
                operation,
                on_auth_failure=lambda auth: invalidations.append(auth["username"]) or True,
            )
        except Exception as error:
            result = error

        self.assertEqual("ok", result)
        self.assertEqual(["credentials", "credentials"], calls)
        self.assertEqual(["user"], invalidations)

    def test_run_with_auth_candidates_does_not_retry_without_cached_token(self):
        rejected = self.module.requests.HTTPError("401 Client Error")
        rejected.response = SimpleNamespace(status_code=401)
        calls = []

        def operation(auth):
            calls.append(auth["source"])
            raise rejected

        with self.assertRaises(RuntimeError):
            self.module.run_with_auth_candidates(
                [
                    {
                        "username": "user",
                        "password": "wrong",
                        "source": "credentials",
                    }
                ],
                operation,
                on_auth_failure=lambda auth: False,
            )

        self.assertEqual(["credentials"], calls)

    def test_run_with_auth_candidates_tries_next_credentials_after_login_failure(self):
        calls = []

        def operation(auth):
            calls.append(auth["source"])
            if auth["source"] == "project":
                self.module.extract_login_token(
                    {"c": 401, "msg": "invalid username or password"}
                )
            return "ok"

        try:
            result = self.module.run_with_auth_candidates(
                [
                    {
                        "username": "project-user",
                        "password": "wrong",
                        "source": "project",
                    },
                    {
                        "username": "global-user",
                        "password": "valid",
                        "source": "global",
                    },
                ],
                operation,
            )
        except Exception as error:
            result = error

        self.assertEqual("ok", result)
        self.assertEqual(["project", "global"], calls)

    def test_login_command_falls_back_to_manual_token_after_login_failure(self):
        future = datetime.now(timezone.utc) + timedelta(hours=1)
        token = build_fake_token_with_username(future, "token-user")
        fake_client = mock.Mock()
        fake_client.invalidate_cached_token.return_value = True

        def get_access_token(*, username, password, token=None):
            if token is None:
                raise ValueError("Login failed: login count limit")
            return {
                "username": username,
                "roles": [],
                "token": token,
                "source": "fallback_token",
            }

        fake_client.get_access_token.side_effect = get_access_token

        with mock.patch.dict(os.environ, {}, clear=True), \
             mock.patch.object(
                 sys,
                 "argv",
                 [
                     "similarweb_client.py",
                     "login",
                     "--username",
                     "account-user",
                     "--password",
                     "account-pass",
                     "--token",
                     token,
                 ],
             ), \
             mock.patch.object(self.module, "SimilarWebClient", return_value=fake_client), \
             mock.patch("sys.stdout", new_callable=io.StringIO) as stdout, \
             mock.patch("sys.stderr", new_callable=io.StringIO):
            try:
                self.module.main()
                error = None
            except BaseException as caught:
                error = caught

        self.assertIsNone(error)
        self.assertEqual("fallback_token", json.loads(stdout.getvalue())["source"])
        self.assertEqual(2, fake_client.get_access_token.call_count)
        fake_client.invalidate_cached_token.assert_not_called()

    def test_login_command_loads_credentials_from_env_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            env_file.write_text(
                "SIMILARWEB_TOKEN=ignored-token\n"
                "SIMILARWEB_USERNAME=env-user\n"
                "SIMILARWEB_PASSWORD=env-pass\n",
                encoding="utf-8",
            )
            fake_client = mock.Mock()
            fake_client.min_token_ttl_seconds = 60
            fake_client.get_access_token.return_value = {
                "username": "env-user",
                "roles": ["similarweb.pro"],
                "token": "internal-token",
                "source": "login",
            }

            with mock.patch.dict(os.environ, {}, clear=True), \
                 mock.patch.object(
                     sys,
                     "argv",
                     ["similarweb_client.py", "login", "--env-file", str(env_file)],
                 ), \
                 mock.patch.object(self.module, "SimilarWebClient", return_value=fake_client), \
                 mock.patch("sys.stdout", new_callable=io.StringIO):
                self.module.main()

            fake_client.get_access_token.assert_called_once_with(
                username="env-user",
                password="env-pass",
                token=None,
            )

    def test_build_website_traffic_trend_command_outputs_monthly_request(self):
        with mock.patch.object(
            sys,
            "argv",
            [
                "similarweb_client.py",
                "build-website-traffic-trend-query",
                "--domain",
                "app.topkey.io",
                "--domain",
                "climatenest.org",
                "--from-month",
                "2026-01",
                "--to-month",
                "2026-06",
            ],
        ), mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
            self.module.main()

        output = json.loads(stdout.getvalue())
        self.assertEqual(
            ["app.topkey.io", "climatenest.org"],
            output["domains"],
        )
        self.assertEqual(
            "Monthly",
            output["requests"][0]["query"]["timeGranularity"],
        )

    def test_fetch_website_traffic_trend_command_passes_range_and_domains(self):
        fake_client = mock.Mock()
        fake_client.fetch_website_traffic_trend_query.return_value = {
            "domains": ["app.topkey.io"],
            "monthly_visits": {},
        }

        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(
            sys,
            "argv",
            [
                "similarweb_client.py",
                "fetch-website-traffic-trend-query",
                "--username",
                "demo",
                "--password",
                "secret",
                "--domain",
                "app.topkey.io",
                "--from-month",
                "2026-01",
                "--to-month",
                "2026-06",
            ],
        ), mock.patch.object(
            self.module,
            "SimilarWebClient",
            return_value=fake_client,
        ), mock.patch(
            "sys.stdout",
            new_callable=io.StringIO,
        ):
            self.module.main()

        fake_client.fetch_website_traffic_trend_query.assert_called_once_with(
            username="demo",
            password="secret",
            token=None,
            domains=["app.topkey.io"],
            from_month="2026-01",
            to_month="2026-06",
            country="999",
            web_source="Total",
            include_subdomains=True,
            time_granularity="Monthly",
        )

    def test_build_referral_traffic_command_outputs_requested_page(self):
        with mock.patch.object(
            sys,
            "argv",
            [
                "similarweb_client.py",
                "build-referral-traffic-query",
                "--domain",
                "checkout.stripe.com",
                "--from-month",
                "2026-01",
                "--to-month",
                "2026-06",
                "--page",
                "20",
            ],
        ), mock.patch("sys.stdout", new_callable=io.StringIO) as stdout:
            self.module.main()

        output = json.loads(stdout.getvalue())
        self.assertEqual(20, output["page"])
        self.assertEqual(
            "20",
            output["requests"][1]["query"]["page"],
        )

    def test_fetch_referral_traffic_command_passes_auto_pagination_options(self):
        fake_client = mock.Mock()
        fake_client.fetch_referral_traffic_query.return_value = {
            "domain": "checkout.stripe.com",
            "referral_table": {"Records": []},
            "pagination": {"pages_fetched": 0},
        }

        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(
            sys,
            "argv",
            [
                "similarweb_client.py",
                "fetch-referral-traffic-query",
                "--username",
                "demo",
                "--password",
                "secret",
                "--domain",
                "checkout.stripe.com",
                "--from-month",
                "2026-01",
                "--to-month",
                "2026-06",
                "--all-pages",
                "--max-pages",
                "20",
            ],
        ), mock.patch.object(
            self.module,
            "SimilarWebClient",
            return_value=fake_client,
        ), mock.patch(
            "sys.stdout",
            new_callable=io.StringIO,
        ):
            self.module.main()

        fake_client.fetch_referral_traffic_query.assert_called_once_with(
            username="demo",
            password="secret",
            token=None,
            domain="checkout.stripe.com",
            from_month="2026-01",
            to_month="2026-06",
            country="999",
            web_source="Total",
            page=1,
            sort="TotalShare",
            asc=False,
            all_pages=True,
            max_pages=20,
        )

    def test_fetch_command_retries_after_invalidating_cached_token(self):
        rejected = self.module.requests.HTTPError("401 Client Error")
        rejected.response = SimpleNamespace(status_code=401)
        fake_client = mock.Mock()
        fake_client.min_token_ttl_seconds = 60
        fake_client.fetch_generated_keywords.side_effect = [
            rejected,
            {"records": [], "totalRecords": 0},
        ]
        fake_client.invalidate_cached_token.return_value = True

        with mock.patch.dict(os.environ, {}, clear=True), \
             mock.patch.object(
                 sys,
                 "argv",
                [
                    "similarweb_client.py",
                    "fetch-generated-keywords",
                    "--username",
                    "user",
                    "--password",
                    "pass",
                    "--keyword",
                    "background remover",
                    "--month",
                    "2026-03",
                ],
             ), \
             mock.patch.object(self.module, "SimilarWebClient", return_value=fake_client), \
             mock.patch("sys.stdout", new_callable=io.StringIO):
            self.module.main()

        self.assertEqual(2, fake_client.fetch_generated_keywords.call_count)
        fake_client.invalidate_cached_token.assert_called_once_with("user")


if __name__ == "__main__":
    unittest.main()
