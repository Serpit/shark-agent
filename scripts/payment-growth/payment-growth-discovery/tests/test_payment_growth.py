import importlib.util
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "payment_growth.py"
)


def load_module():
    if not MODULE_PATH.exists():
        raise AssertionError(f"Expected module to exist: {MODULE_PATH}")
    spec = importlib.util.spec_from_file_location("payment_growth", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["payment_growth"] = module
    spec.loader.exec_module(module)
    return module


def row(
    domain,
    position,
    visits,
    *,
    global_rank=1000,
    total_share=0.01,
    category="Computers_Electronics_and_Technology",
):
    return {
        "source_domain": domain,
        "position": position,
        "global_rank": global_rank,
        "change": 0.0,
        "new_change": False,
        "total_share": total_share,
        "total_visits": visits,
        "month_abs_visits": visits,
        "category": category,
        "engagement_score": 1.0,
    }


class PaymentGrowthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_extract_snapshot_rows_preserves_positions_and_month_visits(self):
        payload = {
            "referral_table": {
                "TotalCount": 3,
                "Records": [
                    {
                        "Domain": "www.alpha.example",
                        "Rank": 1200,
                        "Change": 0.5,
                        "NewChange": False,
                        "TotalShare": 0.2,
                        "TotalVisits": 1500.0,
                        "TotalVisitsAndSharePerMonth": {
                            "2026-06-01": [
                                {
                                    "Site": "checkout.stripe.com",
                                    "Value": 1.0,
                                    "AbsValue": 1234.5,
                                }
                            ]
                        },
                        "Category": "Business_and_Consumer_Services",
                        "EngagementScore": 3.0,
                    },
                    {
                        "Domain": "Referral",
                        "Rank": -1,
                        "TotalVisits": 900.0,
                    },
                    {
                        "Domain": "beta.example",
                        "Rank": 2200,
                        "Change": 1.0,
                        "NewChange": True,
                        "TotalShare": 0.1,
                        "TotalVisits": 800.0,
                        "TotalVisitsAndSharePerMonth": {},
                    },
                ],
            }
        }

        rows = self.module.extract_snapshot_rows(payload, month="2026-06")

        self.assertEqual(2, len(rows))
        self.assertEqual("alpha.example", rows[0]["source_domain"])
        self.assertEqual(1, rows[0]["position"])
        self.assertEqual(1234.5, rows[0]["month_abs_visits"])
        self.assertEqual("beta.example", rows[1]["source_domain"])
        self.assertEqual(3, rows[1]["position"])
        self.assertEqual(800.0, rows[1]["month_abs_visits"])

    def test_extract_snapshot_rows_deduplicates_normalized_domains(self):
        payload = {
            "referral_table": {
                "Records": [
                    {"Domain": "www.alpha.example", "TotalVisits": 1000},
                    {"Domain": "alpha.example", "TotalVisits": 900},
                ]
            }
        }

        rows = self.module.extract_snapshot_rows(payload, month="2026-06")

        self.assertEqual(1, len(rows))
        self.assertEqual("alpha.example", rows[0]["source_domain"])
        self.assertEqual(1, rows[0]["position"])

    def test_save_snapshot_replaces_same_target_month_without_duplicates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-06",
                rows=[
                    row("alpha.example", 1, 1000),
                    row("beta.example", 2, 900),
                ],
                total_count=200,
                pages_fetched=2,
                complete=False,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-06",
                rows=[row("alpha.example", 4, 1200)],
                total_count=150,
                pages_fetched=1,
                complete=False,
            )

            with closing(sqlite3.connect(db_path)) as connection:
                snapshot_count = connection.execute(
                    "SELECT COUNT(*) FROM referral_snapshots"
                ).fetchone()[0]
                stored_rows = connection.execute(
                    """
                    SELECT source_domain, position, month_abs_visits
                    FROM referral_rows
                    """
                ).fetchall()

        self.assertEqual(1, snapshot_count)
        self.assertEqual([("alpha.example", 4, 1200.0)], stored_rows)

    def test_collect_website_traffic_saves_available_and_missing_months(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"

            def fetcher(*, domains, from_month, to_month, **options):
                self.assertEqual(["app.topkey.io"], domains)
                self.assertEqual("2026-01", from_month)
                self.assertEqual("2026-03", to_month)
                self.assertEqual("999", options["country"])
                self.assertEqual("Total", options["web_source"])
                self.assertTrue(options["include_subdomains"])
                return {
                    "monthly_visits": {
                        "app.topkey.io": {
                            "data_verified": False,
                            "months": [
                                {"month": "2026-01", "visits": 100.0},
                                {"month": "2026-03", "visits": 300.0},
                            ],
                        }
                    }
                }

            summary = self.module.collect_website_traffic(
                db_path,
                domains=["app.topkey.io"],
                start_month="2026-01",
                end_month="2026-03",
                fetcher=fetcher,
                collected_at="2026-07-27T00:00:00+00:00",
            )

            with closing(sqlite3.connect(db_path)) as connection:
                stored_rows = connection.execute(
                    """
                    SELECT month, visits, available, data_verified
                    FROM website_traffic_months
                    ORDER BY month
                    """
                ).fetchall()

        self.assertEqual(
            [
                ("2026-01", 100.0, 1, 0),
                ("2026-02", None, 0, 0),
                ("2026-03", 300.0, 1, 0),
            ],
            stored_rows,
        )
        self.assertEqual(2, summary["points_available"])
        self.assertEqual(1, summary["points_missing"])

    def test_analyze_website_traffic_classifies_sustained_directions(self):
        growing = self.module.analyze_website_traffic(
            [
                {"month": "2026-04", "visits": 100.0, "available": True},
                {"month": "2026-05", "visits": 150.0, "available": True},
                {"month": "2026-06", "visits": 225.0, "available": True},
            ]
        )
        declining = self.module.analyze_website_traffic(
            [
                {"month": "2026-04", "visits": 300.0, "available": True},
                {"month": "2026-05", "visits": 200.0, "available": True},
                {"month": "2026-06", "visits": 100.0, "available": True},
            ]
        )

        self.assertEqual("sustained_growth", growing["trend"])
        self.assertEqual(1.25, growing["growth_rate"])
        self.assertEqual(0.5, growing["latest_month_growth_rate"])
        self.assertEqual(2, growing["positive_growth_steps"])
        self.assertEqual("sustained_decline", declining["trend"])
        self.assertAlmostEqual(-2 / 3, declining["growth_rate"])
        self.assertEqual(2, declining["negative_growth_steps"])

    def test_opportunity_report_attaches_cached_website_traffic(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-05",
                rows=[row("candidate.example", 100, 1000)],
                total_count=1,
                pages_fetched=1,
                complete=True,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-06",
                rows=[row("candidate.example", 10, 3000)],
                total_count=1,
                pages_fetched=1,
                complete=True,
            )
            values = [100, 120, 150, 180, 240, 360]
            self.module.collect_website_traffic(
                db_path,
                domains=["candidate.example"],
                start_month="2026-01",
                end_month="2026-06",
                fetcher=lambda **_: {
                    "monthly_visits": {
                        "candidate.example": {
                            "data_verified": False,
                            "months": [
                                {"month": f"2026-{index:02d}", "visits": value}
                                for index, value in enumerate(values, start=1)
                            ],
                        }
                    }
                },
                collected_at="2026-07-27T00:00:00+00:00",
            )

            report = self.module.build_opportunity_report(
                db_path,
                current_month="2026-06",
                previous_month="2026-05",
                limit=10,
                site_traffic_months=6,
            )

        traffic = report["fast_rank_growth"][0]["website_traffic"]
        self.assertEqual("sustained_growth", traffic["trend"])
        self.assertEqual(6, traffic["months_available"])
        self.assertEqual(360.0, traffic["latest_visits"])
        self.assertEqual(2.6, traffic["growth_rate"])

    def test_live_website_traffic_fetcher_reuses_auth_candidate_chain(self):
        client = mock.Mock()
        client.fetch_website_traffic_trend_query.return_value = {
            "monthly_visits": {}
        }
        candidates = [
            {
                "username": "user@example.com",
                "password": "secret",
                "token": "",
                "source": "test",
            }
        ]
        with mock.patch.object(
            self.module.similarweb,
            "SimilarWebClient",
            return_value=client,
        ), mock.patch.object(
            self.module.similarweb,
            "resolve_auth_candidates",
            return_value=candidates,
        ):
            fetcher = self.module.create_live_website_traffic_fetcher()
            output = fetcher(
                domains=["candidate.example"],
                from_month="2026-01",
                to_month="2026-06",
                country="999",
                web_source="Total",
                include_subdomains=True,
            )

        self.assertEqual({"monthly_visits": {}}, output)
        client.fetch_website_traffic_trend_query.assert_called_once_with(
            username="user@example.com",
            password="secret",
            token=None,
            domains=["candidate.example"],
            from_month="2026-01",
            to_month="2026-06",
            country="999",
            web_source="Total",
            include_subdomains=True,
        )

    def test_build_opportunity_report_returns_three_evidence_backed_lists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-05",
                rows=[
                    row("alpha.example", 20, 1000),
                    row("steady.example", 3, 2000),
                    row("low-base.example", 30, 10),
                    row("early-riser.example", 1000, 10),
                    row("paypal.com", 8, 5000),
                ],
                total_count=5,
                pages_fetched=1,
                complete=True,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-06",
                rows=[
                    row("alpha.example", 5, 3000),
                    row("steady.example", 4, 2100),
                    row("newcomer.example", 10, 2000),
                    row("low-base.example", 6, 900),
                    row("early-riser.example", 100, 20),
                    row("paypal.com", 2, 9000),
                ],
                total_count=6,
                pages_fetched=1,
                complete=True,
            )

            report = self.module.build_opportunity_report(
                db_path,
                current_month="2026-06",
                previous_month="2026-05",
                min_current_visits=1000,
                min_previous_visits=250,
                limit=10,
            )

        self.assertEqual(
            ["alpha.example"],
            [item["source_domain"] for item in report["rank_risers"]],
        )
        self.assertEqual(
            [
                "early-riser.example",
                "low-base.example",
                "alpha.example",
            ],
            [
                item["source_domain"]
                for item in report["fast_rank_growth"]
            ],
        )
        self.assertEqual(15, report["rank_risers"][0]["rank_gain"])
        self.assertEqual(
            ["alpha.example", "steady.example"],
            [item["source_domain"] for item in report["traffic_gainers"]],
        )
        self.assertEqual(2000.0, report["traffic_gainers"][0]["absolute_growth"])
        self.assertEqual(2.0, report["traffic_gainers"][0]["growth_rate"])
        self.assertEqual(
            ["newcomer.example"],
            [item["source_domain"] for item in report["newcomers"]],
        )
        evidence_lists = {
            key: report[key]
            for key in (
                "rank_risers",
                "traffic_gainers",
                "newcomers",
                "young_growth_candidates",
                "new_product_growth",
            )
        }
        self.assertNotIn("low-base.example", str(evidence_lists))
        self.assertNotIn("paypal.com", str(report))

    def test_resolve_rdap_base_url_uses_longest_label_match(self):
        bootstrap = {
            "services": [
                [["uk"], ["https://rdap.example/uk/"]],
                [["co.uk"], ["https://rdap.example/co-uk/"]],
                [["com"], ["https://rdap.example/com/"]],
            ]
        }

        base_url = self.module.resolve_rdap_base_url(
            bootstrap,
            "shop.alpha.co.uk",
        )

        self.assertEqual("https://rdap.example/co-uk/", base_url)

    def test_parse_rdap_profile_extracts_registration_expiration_and_registrar(self):
        payload = {
            "objectClassName": "domain",
            "ldhName": "ALPHA.COM",
            "events": [
                {
                    "eventAction": "registration",
                    "eventDate": "2025-02-03T04:05:06Z",
                },
                {
                    "eventAction": "expiration",
                    "eventDate": "2027-02-03T04:05:06Z",
                },
            ],
            "entities": [
                {
                    "roles": ["registrar"],
                    "vcardArray": [
                        "vcard",
                        [["fn", {}, "text", "Example Registrar, Inc."]],
                    ],
                }
            ],
        }

        profile = self.module.parse_rdap_profile(
            payload,
            source_domain="app.alpha.com",
            rdap_url="https://rdap.example/domain/alpha.com",
            fetched_at="2026-07-27T00:00:00+00:00",
        )

        self.assertEqual("app.alpha.com", profile["source_domain"])
        self.assertEqual("alpha.com", profile["registrable_domain"])
        self.assertEqual("2025-02-03T04:05:06Z", profile["registered_at"])
        self.assertEqual("2027-02-03T04:05:06Z", profile["expires_at"])
        self.assertEqual("Example Registrar, Inc.", profile["registrar"])
        self.assertEqual("ok", profile["rdap_status"])

    def test_enrich_domains_reuses_fresh_cached_profiles(self):
        calls = []

        def fetcher(domain):
            calls.append(domain)
            return {
                "source_domain": domain,
                "registrable_domain": "alpha.com",
                "rdap_status": "ok",
                "registered_at": "2025-02-03T04:05:06Z",
                "expires_at": None,
                "registrar": None,
                "rdap_url": "https://rdap.example/domain/alpha.com",
                "fetched_at": "2026-07-27T00:00:00+00:00",
                "error": None,
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            first = self.module.enrich_domains(
                db_path,
                ["app.alpha.com"],
                fetcher=fetcher,
                now="2026-07-27T12:00:00+00:00",
            )
            second = self.module.enrich_domains(
                db_path,
                ["app.alpha.com"],
                fetcher=fetcher,
                now="2026-07-28T12:00:00+00:00",
            )

        self.assertEqual(["app.alpha.com"], calls)
        self.assertEqual(1, first["profiles_fetched"])
        self.assertEqual(0, first["profiles_cached"])
        self.assertEqual(0, second["profiles_fetched"])
        self.assertEqual(1, second["profiles_cached"])

    def test_enrich_domains_records_one_failure_and_continues(self):
        def fetcher(domain):
            if domain == "broken.example":
                raise RuntimeError("temporary RDAP failure")
            return {
                "source_domain": domain,
                "registrable_domain": domain,
                "rdap_status": "ok",
                "registered_at": None,
                "expires_at": None,
                "registrar": None,
                "rdap_url": f"https://rdap.example/domain/{domain}",
                "fetched_at": "2026-07-27T00:00:00+00:00",
                "error": None,
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            summary = self.module.enrich_domains(
                db_path,
                ["broken.example", "healthy.example"],
                fetcher=fetcher,
                now="2026-07-27T12:00:00+00:00",
            )
            with closing(sqlite3.connect(db_path)) as connection:
                statuses = connection.execute(
                    """
                    SELECT source_domain, rdap_status, error
                    FROM domain_profiles
                    ORDER BY source_domain
                    """
                ).fetchall()

        self.assertEqual(2, summary["profiles_fetched"])
        self.assertEqual(1, summary["profiles_failed"])
        self.assertEqual(
            [
                ("broken.example", "error", "temporary RDAP failure"),
                ("healthy.example", "ok", None),
            ],
            statuses,
        )

    def test_report_identifies_young_domains_with_growth_evidence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-05",
                rows=[
                    row("young.example", 40, 1000),
                    row("old.example", 30, 1000),
                ],
                total_count=2,
                pages_fetched=1,
                complete=True,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-06",
                rows=[
                    row("young.example", 5, 5000),
                    row("old.example", 4, 6000),
                    row("new.example", 8, 3000),
                ],
                total_count=3,
                pages_fetched=1,
                complete=True,
            )
            for domain, registered_at in [
                ("young.example", "2025-12-01T00:00:00Z"),
                ("old.example", "2015-01-01T00:00:00Z"),
                ("new.example", "2026-05-01T00:00:00Z"),
            ]:
                self.module.save_domain_profile(
                    db_path,
                    {
                        "source_domain": domain,
                        "registrable_domain": domain,
                        "rdap_status": "ok",
                        "registered_at": registered_at,
                        "expires_at": None,
                        "registrar": None,
                        "rdap_url": f"https://rdap.example/domain/{domain}",
                        "fetched_at": "2026-07-27T00:00:00+00:00",
                        "error": None,
                    },
                )

            report = self.module.build_opportunity_report(
                db_path,
                current_month="2026-06",
                previous_month="2026-05",
                min_current_visits=1000,
                min_previous_visits=250,
                limit=10,
                max_domain_age_days=730,
            )

        self.assertEqual(
            ["young.example", "new.example"],
            [
                item["source_domain"]
                for item in report["young_growth_candidates"]
            ],
        )
        self.assertEqual(211, report["young_growth_candidates"][0]["domain_age_days"])
        self.assertEqual("rank_riser", report["young_growth_candidates"][0]["signals"][0])
        self.assertEqual("newcomer", report["young_growth_candidates"][1]["signals"][0])
        self.assertNotIn("old.example", str(report["young_growth_candidates"]))

    def test_report_can_filter_to_one_payment_target(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            for target in ("checkout.stripe.com", "lemonsqueezy.com"):
                self.module.save_snapshot(
                    db_path,
                    target_domain=target,
                    month="2026-05",
                    rows=[row(f"{target}.source.example", 20, 1000)],
                    total_count=1,
                    pages_fetched=1,
                    complete=True,
                )
                self.module.save_snapshot(
                    db_path,
                    target_domain=target,
                    month="2026-06",
                    rows=[row(f"{target}.source.example", 2, 5000)],
                    total_count=1,
                    pages_fetched=1,
                    complete=True,
                )

            report = self.module.build_opportunity_report(
                db_path,
                current_month="2026-06",
                previous_month="2026-05",
                targets=["lemonsqueezy.com"],
            )

        self.assertEqual(["lemonsqueezy.com"], report["targets"])
        flattened = str(report)
        self.assertIn("lemonsqueezy.com.source.example", flattened)
        self.assertNotIn("checkout.stripe.com.source.example", flattened)

    def test_report_outputs_category_changes_and_typical_head_products(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-05",
                rows=[
                    row("ai-a.example", 1, 100, category="AI"),
                    row("ai-b.example", 2, 200, category="AI"),
                    row("design.example", 3, 500, category="Design"),
                ],
                total_count=3,
                pages_fetched=1,
                complete=True,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-06",
                rows=[
                    row("ai-new.example", 1, 400, category="AI"),
                    row("ai-a.example", 2, 300, category="AI"),
                    row("ai-b.example", 3, 100, category="AI"),
                    row("design.example", 4, 200, category="Design"),
                ],
                total_count=4,
                pages_fetched=1,
                complete=True,
            )

            report = self.module.build_opportunity_report(
                db_path,
                current_month="2026-06",
                previous_month="2026-05",
                min_current_visits=0,
                min_previous_visits=0,
                limit=10,
            )

        gain = report["category_conclusions"]["gainers"][0]
        decline = report["category_conclusions"]["decliners"][0]
        self.assertEqual("AI", gain["category"])
        self.assertEqual(300.0, gain["previous_payment_intent_visits"])
        self.assertEqual(800.0, gain["current_payment_intent_visits"])
        self.assertEqual(500.0, gain["absolute_change"])
        self.assertAlmostEqual(5 / 3, gain["growth_rate"])
        self.assertEqual(
            ["ai-new.example", "ai-a.example", "ai-b.example"],
            [item["source_domain"] for item in gain["top_products"]],
        )
        self.assertEqual("Design", decline["category"])
        self.assertEqual(-300.0, decline["absolute_change"])

    def test_report_outputs_cross_platform_new_product_growth(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            for target in ("checkout.stripe.com", "lemonsqueezy.com"):
                self.module.save_snapshot(
                    db_path,
                    target_domain=target,
                    month="2026-05",
                    rows=[],
                    total_count=0,
                    pages_fetched=1,
                    complete=True,
                )
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-06",
                rows=[row("new.example", 50, 1500, category="AI")],
                total_count=1,
                pages_fetched=1,
                complete=True,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="lemonsqueezy.com",
                month="2026-06",
                rows=[
                    row("new.example", 20, 500, category="AI"),
                    row("tiny-new.example", 2000, 50, category="AI"),
                ],
                total_count=2,
                pages_fetched=1,
                complete=True,
            )

            report = self.module.build_opportunity_report(
                db_path,
                current_month="2026-06",
                previous_month="2026-05",
                min_current_visits=1000,
                min_previous_visits=250,
                limit=10,
            )

        self.assertEqual(2, len(report["new_product_growth"]))
        product = report["new_product_growth"][0]
        self.assertEqual("new.example", product["source_domain"])
        self.assertEqual(2000.0, product["current_payment_intent_visits"])
        self.assertEqual(
            ["checkout.stripe.com", "lemonsqueezy.com"],
            product["payment_targets"],
        )
        self.assertEqual(["newly_visible"], product["signals"])
        self.assertEqual(
            "tiny-new.example",
            report["new_product_growth"][1]["source_domain"],
        )

    def test_report_rejects_incomplete_snapshots(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-05",
                rows=[row("alpha.example", 10, 1000)],
                total_count=3000,
                pages_fetched=20,
                complete=False,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="checkout.stripe.com",
                month="2026-06",
                rows=[row("alpha.example", 5, 2000)],
                total_count=3000,
                pages_fetched=30,
                complete=True,
            )

            with self.assertRaisesRegex(
                ValueError,
                "checkout.stripe.com:2026-05=incomplete",
            ):
                self.module.build_opportunity_report(
                    db_path,
                    current_month="2026-06",
                    previous_month="2026-05",
                )

    def test_rolling_report_separates_sustained_breakout_and_newly_visible(self):
        months = [
            "2026-01",
            "2026-02",
            "2026-03",
            "2026-04",
            "2026-05",
            "2026-06",
        ]
        sustained_visits = [100, 200, 300, 400, 500, 700]
        sustained_positions = [50, 40, 30, 20, 10, 5]
        spike_visits = [100, 100, 100, 100, 100, 1000]

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            for index, month in enumerate(months):
                rows = [
                    row(
                        "sustained.example",
                        sustained_positions[index],
                        sustained_visits[index],
                    ),
                    row("spike.example", 30, spike_visits[index]),
                    row("falling.example", index + 1, 1000 - index * 100),
                ]
                if month == "2026-06":
                    rows.append(row("new.example", 8, 800))
                self.module.save_snapshot(
                    db_path,
                    target_domain="checkout.stripe.com",
                    month=month,
                    rows=rows,
                    total_count=len(rows),
                    pages_fetched=1,
                    complete=True,
                )
            self.module.save_domain_profile(
                db_path,
                {
                    "source_domain": "sustained.example",
                    "registrable_domain": "sustained.example",
                    "rdap_status": "ok",
                    "registered_at": "2025-12-01T00:00:00Z",
                    "expires_at": None,
                    "registrar": None,
                    "rdap_url": "https://rdap.example/domain/sustained.example",
                    "fetched_at": "2026-07-27T00:00:00+00:00",
                    "error": None,
                },
            )

            report = self.module.build_rolling_report(
                db_path,
                start_month="2026-01",
                end_month="2026-06",
                targets=["checkout.stripe.com"],
                min_current_visits=500,
                min_months_present=3,
                breakout_growth_rate=1.0,
                limit=10,
            )

        self.assertEqual(
            ["sustained.example"],
            [item["source_domain"] for item in report["sustained_growth"]],
        )
        sustained = report["sustained_growth"][0]
        self.assertEqual(6, sustained["months_present"])
        self.assertEqual(5, sustained["positive_growth_steps"])
        self.assertEqual(300.0, sustained["recent_absolute_growth"])
        self.assertEqual(0.75, sustained["recent_growth_rate"])
        self.assertEqual(15, sustained["recent_position_gain"])
        self.assertEqual(211, sustained["domain_age_days"])
        self.assertEqual(6, len(sustained["series"]))
        self.assertEqual(
            ["spike.example"],
            [item["source_domain"] for item in report["breakouts"]],
        )
        self.assertEqual(
            ["new.example"],
            [item["source_domain"] for item in report["newly_visible"]],
        )
        self.assertEqual(
            ["sustained.example"],
            [
                item["source_domain"]
                for item in report["young_sustained_growth"]
            ],
        )
        self.assertNotIn("falling.example", str(report))

    def test_rolling_report_rejects_missing_or_incomplete_snapshots(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="paddle.com",
                month="2026-01",
                rows=[row("alpha.example", 1, 1000)],
                total_count=1,
                pages_fetched=1,
                complete=False,
            )

            with self.assertRaisesRegex(
                ValueError,
                "paddle.com:2026-01=incomplete.*paddle.com:2026-02=missing",
            ):
                self.module.build_rolling_report(
                    db_path,
                    start_month="2026-01",
                    end_month="2026-02",
                    targets=["paddle.com"],
                )

    def test_collect_snapshots_fetches_complete_table_for_every_target_month(self):
        calls = []

        def fetcher(*, target_domain, month, max_pages):
            calls.append((target_domain, month, max_pages))
            return {
                "referral_table": {
                    "TotalCount": 300,
                    "Records": [
                        {
                            "Domain": "alpha.example",
                            "Rank": 100,
                            "TotalVisits": 3000,
                            "TotalVisitsAndSharePerMonth": {
                                f"{month}-01": [{"AbsValue": 3000}]
                            },
                        },
                        {
                            "Domain": "beta.example",
                            "Rank": 200,
                            "TotalVisits": 2000,
                            "TotalVisitsAndSharePerMonth": {
                                f"{month}-01": [{"AbsValue": 2000}]
                            },
                        },
                        {
                            "Domain": "gamma.example",
                            "Rank": 300,
                            "TotalVisits": 1000,
                            "TotalVisitsAndSharePerMonth": {
                                f"{month}-01": [{"AbsValue": 1000}]
                            },
                        },
                    ],
                },
                "pagination": {
                    "pages_fetched": 3,
                    "total_count": 300,
                    "complete": True,
                },
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            summary = self.module.collect_snapshots(
                db_path,
                targets=["checkout.stripe.com", "lemonsqueezy.com"],
                months=["2026-05", "2026-06"],
                fetcher=fetcher,
            )
            with closing(sqlite3.connect(db_path)) as connection:
                stored_count = connection.execute(
                    "SELECT COUNT(*) FROM referral_rows"
                ).fetchone()[0]

        self.assertEqual(
            [
                ("checkout.stripe.com", "2026-05", None),
                ("checkout.stripe.com", "2026-06", None),
                ("lemonsqueezy.com", "2026-05", None),
                ("lemonsqueezy.com", "2026-06", None),
            ],
            calls,
        )
        self.assertEqual("full", summary["collection_scope"])
        self.assertEqual(4, summary["snapshots_saved"])
        self.assertEqual(12, summary["records_saved"])
        self.assertEqual(12, stored_count)

    def test_collect_snapshots_rejects_incomplete_upstream_table(self):
        def fetcher(*, target_domain, month, max_pages):
            return {
                "referral_table": {
                    "TotalCount": 3000,
                    "Records": [],
                },
                "pagination": {
                    "pages_fetched": 20,
                    "total_count": 3000,
                    "complete": False,
                },
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaisesRegex(
                RuntimeError,
                "did not return a complete referral table",
            ):
                self.module.collect_snapshots(
                    Path(tmpdir) / "growth.sqlite3",
                    targets=["checkout.stripe.com"],
                    months=["2026-06"],
                    fetcher=fetcher,
                )

    def test_create_live_fetcher_requests_unbounded_single_month_pages(self):
        fake_client = mock.Mock()
        expected = {
            "referral_table": {"TotalCount": 250, "Records": []},
            "pagination": {"pages_fetched": 2, "complete": False},
        }
        fake_client.fetch_referral_traffic_query.return_value = expected
        auth = {
            "username": "demo",
            "password": "secret",
            "token": "",
            "source": "test",
        }

        def run_candidates(candidates, operation, on_auth_failure=None):
            return operation(candidates[0])

        with mock.patch.object(
            self.module.similarweb,
            "SimilarWebClient",
            return_value=fake_client,
        ), mock.patch.object(
            self.module.similarweb,
            "resolve_auth_candidates",
            return_value=[auth],
        ), mock.patch.object(
            self.module.similarweb,
            "run_with_auth_candidates",
            side_effect=run_candidates,
        ):
            fetcher = self.module.create_live_fetcher()
            result = fetcher(
                target_domain="lemonsqueezy.com",
                month="2026-06",
                max_pages=None,
            )

        self.assertEqual(expected, result)
        fake_client.fetch_referral_traffic_query.assert_called_once_with(
            username="demo",
            password="secret",
            token=None,
            domain="lemonsqueezy.com",
            from_month="2026-06",
            to_month="2026-06",
            all_pages=True,
            max_pages=None,
        )

    def test_create_live_rdap_fetcher_falls_back_from_subdomain(self):
        class FakeResponse:
            def __init__(self, status_code, payload):
                self.status_code = status_code
                self._payload = payload

            def json(self):
                return self._payload

            def raise_for_status(self):
                if self.status_code >= 400:
                    raise AssertionError(f"unexpected HTTP {self.status_code}")

        class FakeSession:
            def __init__(self):
                self.headers = {}
                self.trust_env = True
                self.urls = []

            def get(self, url, timeout):
                self.urls.append((url, timeout))
                if url == self.module.IANA_RDAP_BOOTSTRAP_URL:
                    return FakeResponse(
                        200,
                        {
                            "services": [
                                [["com"], ["https://rdap.example/"]]
                            ]
                        },
                    )
                if url.endswith("/domain/app.alpha.com"):
                    return FakeResponse(404, {})
                if url.endswith("/domain/alpha.com"):
                    return FakeResponse(
                        200,
                        {
                            "objectClassName": "domain",
                            "ldhName": "ALPHA.COM",
                            "events": [
                                {
                                    "eventAction": "registration",
                                    "eventDate": "2025-02-03T04:05:06Z",
                                }
                            ],
                        },
                    )
                raise AssertionError(f"unexpected URL {url}")

        session = FakeSession()
        session.module = self.module
        fetcher = self.module.create_live_rdap_fetcher(
            session=session,
            now=lambda: "2026-07-27T00:00:00+00:00",
        )

        profile = fetcher("app.alpha.com")

        self.assertFalse(session.trust_env)
        self.assertEqual("alpha.com", profile["registrable_domain"])
        self.assertEqual("ok", profile["rdap_status"])
        self.assertEqual(
            [
                self.module.IANA_RDAP_BOOTSTRAP_URL,
                "https://rdap.example/domain/app.alpha.com",
                "https://rdap.example/domain/alpha.com",
            ],
            [url for url, _ in session.urls],
        )

    def test_enrich_command_selects_report_candidates_and_caches_profiles(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="lemonsqueezy.com",
                month="2026-05",
                rows=[row("candidate.example", 50, 1000)],
                total_count=1,
                pages_fetched=1,
                complete=True,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="lemonsqueezy.com",
                month="2026-06",
                rows=[row("candidate.example", 5, 5000)],
                total_count=1,
                pages_fetched=1,
                complete=True,
            )

            def fetcher(domain):
                return {
                    "source_domain": domain,
                    "registrable_domain": domain,
                    "rdap_status": "ok",
                    "registered_at": "2026-01-01T00:00:00Z",
                    "expires_at": None,
                    "registrar": None,
                    "rdap_url": f"https://rdap.example/domain/{domain}",
                    "fetched_at": "2026-07-27T00:00:00+00:00",
                    "error": None,
                }

            stdout = io.StringIO()
            with mock.patch.object(
                self.module,
                "create_live_rdap_fetcher",
                return_value=fetcher,
            ), redirect_stdout(stdout):
                self.module.main(
                    [
                        "enrich",
                        "--db",
                        str(db_path),
                        "--current-month",
                        "2026-06",
                        "--previous-month",
                        "2026-05",
                        "--limit",
                        "10",
                    ]
                )
            output = json.loads(stdout.getvalue())

        self.assertEqual(["candidate.example"], output["domains"])
        self.assertEqual(1, output["profiles_fetched"])

    def test_rolling_report_command_outputs_complete_range(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            for month, position, visits in [
                ("2026-04", 30, 1000),
                ("2026-05", 20, 2000),
                ("2026-06", 10, 4000),
            ]:
                self.module.save_snapshot(
                    db_path,
                    target_domain="paddle.com",
                    month=month,
                    rows=[row("candidate.example", position, visits)],
                    total_count=1,
                    pages_fetched=1,
                    complete=True,
                )

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                self.module.main(
                    [
                        "rolling-report",
                        "--db",
                        str(db_path),
                        "--target",
                        "paddle.com",
                        "--start-month",
                        "2026-04",
                        "--end-month",
                        "2026-06",
                        "--limit",
                        "5",
                    ]
                )
            output = json.loads(stdout.getvalue())

        self.assertEqual(3, output["coverage"]["complete_snapshots"])
        self.assertEqual(
            ["candidate.example"],
            [
                item["source_domain"]
                for item in output["sustained_growth"]
            ],
        )

    def test_rolling_enrich_command_enriches_rolling_candidates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            for month, position, visits in [
                ("2026-04", 30, 1000),
                ("2026-05", 20, 2000),
                ("2026-06", 10, 4000),
            ]:
                self.module.save_snapshot(
                    db_path,
                    target_domain="paddle.com",
                    month=month,
                    rows=[row("candidate.example", position, visits)],
                    total_count=1,
                    pages_fetched=1,
                    complete=True,
                )

            def fetcher(domain):
                return {
                    "source_domain": domain,
                    "registrable_domain": domain,
                    "rdap_status": "ok",
                    "registered_at": "2026-01-01T00:00:00Z",
                    "expires_at": None,
                    "registrar": None,
                    "rdap_url": f"https://rdap.example/domain/{domain}",
                    "fetched_at": "2026-07-27T00:00:00+00:00",
                    "error": None,
                }

            stdout = io.StringIO()
            with mock.patch.object(
                self.module,
                "create_live_rdap_fetcher",
                return_value=fetcher,
            ), redirect_stdout(stdout):
                self.module.main(
                    [
                        "rolling-enrich",
                        "--db",
                        str(db_path),
                        "--target",
                        "paddle.com",
                        "--start-month",
                        "2026-04",
                        "--end-month",
                        "2026-06",
                        "--limit",
                        "5",
                    ]
                )
            output = json.loads(stdout.getvalue())

        self.assertEqual(["candidate.example"], output["domains"])
        self.assertEqual(1, output["profiles_fetched"])

    def test_collect_command_writes_database_and_prints_summary(self):
        calls = []

        def fetcher(*, target_domain, month, max_pages):
            calls.append((target_domain, month, max_pages))
            return {
                "referral_table": {
                    "TotalCount": 1,
                    "Records": [
                        {
                            "Domain": "candidate.example",
                            "Rank": 100,
                            "TotalVisits": 2500,
                            "TotalVisitsAndSharePerMonth": {
                                f"{month}-01": [{"AbsValue": 2500}]
                            },
                        }
                    ],
                },
                "pagination": {
                    "pages_fetched": max_pages,
                    "total_count": 1,
                    "complete": True,
                },
            }

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            stdout = io.StringIO()
            with mock.patch.object(
                self.module,
                "create_live_fetcher",
                return_value=fetcher,
            ), redirect_stdout(stdout):
                self.module.main(
                    [
                        "collect",
                        "--db",
                        str(db_path),
                        "--target",
                        "lemonsqueezy.com",
                        "--month",
                        "2026-06",
                    ]
                )
            output = json.loads(stdout.getvalue())
            with closing(sqlite3.connect(db_path)) as connection:
                stored_count = connection.execute(
                    "SELECT COUNT(*) FROM referral_rows"
                ).fetchone()[0]

        self.assertEqual(1, output["snapshots_saved"])
        self.assertEqual(1, output["records_saved"])
        self.assertEqual("full", output["collection_scope"])
        self.assertEqual([("lemonsqueezy.com", "2026-06", None)], calls)
        self.assertEqual(1, stored_count)

    def test_traffic_enrich_command_collects_selected_candidate_series(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "growth.sqlite3"
            self.module.save_snapshot(
                db_path,
                target_domain="paddle.com",
                month="2026-05",
                rows=[row("candidate.example", 20, 1000)],
                total_count=1,
                pages_fetched=1,
                complete=True,
            )
            self.module.save_snapshot(
                db_path,
                target_domain="paddle.com",
                month="2026-06",
                rows=[row("candidate.example", 10, 2000)],
                total_count=1,
                pages_fetched=1,
                complete=True,
            )

            def fetcher(**kwargs):
                self.assertEqual(["candidate.example"], kwargs["domains"])
                self.assertEqual("2026-01", kwargs["from_month"])
                self.assertEqual("2026-06", kwargs["to_month"])
                return {
                    "monthly_visits": {
                        "candidate.example": {
                            "data_verified": True,
                            "months": [
                                {"month": month, "visits": visits}
                                for month, visits in [
                                    ("2026-01", 100),
                                    ("2026-02", 120),
                                    ("2026-03", 140),
                                    ("2026-04", 180),
                                    ("2026-05", 240),
                                    ("2026-06", 360),
                                ]
                            ],
                        }
                    }
                }

            stdout = io.StringIO()
            with mock.patch.object(
                self.module,
                "create_live_website_traffic_fetcher",
                return_value=fetcher,
            ), redirect_stdout(stdout):
                self.module.main(
                    [
                        "traffic-enrich",
                        "--db",
                        str(db_path),
                        "--target",
                        "paddle.com",
                        "--current-month",
                        "2026-06",
                        "--previous-month",
                        "2026-05",
                        "--start-month",
                        "2026-01",
                        "--end-month",
                        "2026-06",
                    ]
                )
            output = json.loads(stdout.getvalue())

        self.assertEqual(["candidate.example"], output["domains"])
        self.assertEqual(6, output["points_available"])
        self.assertEqual(0, output["points_missing"])



if __name__ == "__main__":
    unittest.main()
