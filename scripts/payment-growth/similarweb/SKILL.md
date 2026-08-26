---
name: similarweb
description: Use when analyzing SimilarWeb-compatible HAR files, mapping keyword-analysis, website-analysis, monthly website-traffic, or referral-traffic endpoints, generating reusable request bundles with pagination, or separating proxy control-plane traffic from actual SimilarWeb data APIs.
---

# SimilarWeb

Use this skill when the task is to reverse engineer a SimilarWeb-compatible session from HAR, or to turn confirmed keyword-analysis / website-analysis traffic into a reusable request plan.

This skill currently focuses on the following workflows:

- summarize HAR files into `data`, `internal`, and `control-plane` endpoints
- build the core request bundle for keyword analysis around one keyword and one month
- build the observed request bundle for website analysis around one domain and one month
- build the observed request for website search keywords, including the "new clicks" UI state
- build and fetch incoming referral-traffic analysis across a month range, including single-page and automatic multi-page retrieval
- build and fetch monthly total-site visit trends for one or more shortlisted domains
- build focused search SEO requests for landing-page overview, keyword performance, and branded split
- login through `dash.3ue.com` and fetch full JSON from verified keyword-analysis endpoints

It does **not** currently provide a fully verified live client for every SimilarWeb endpoint.
The verified live path currently covers login, generated-keyword fetching, the keyword overview bundle, incoming-referral pagination, and monthly total-site visit trends.
Other website-analysis endpoints are HAR-observed and bundled, but broader live replay should be verified per endpoint before treating it as production-stable.

Further reading in this skill directory:

- [references/api-map.md](references/api-map.md) for the verified endpoint map and auth boundary
- [references/open-source-notes.md](references/open-source-notes.md) for GitHub projects worth referencing or avoiding

## When to Use

Use this skill when the user asks for things like:

- "分析 SimilarWeb 的 HAR，看看接口怎么分层"
- "把 SimilarWeb 关键词分析页面的 API 梳理出来"
- "给我一个 SimilarWeb keyword overview 的请求模板"
- "给我一个 SimilarWeb website analysis / traffic overview 的请求模板"
- "分析 checkout.stripe.com / paypal.com / paddle.com / lemonsqueezy.com 的导入流量来源，并翻页拿全量站点"
- "哪些请求是真数据，哪些只是站点自己的用户态接口"
- "从抓包里提炼一个可复用的 skill"

Do **not** use this skill when the user primarily needs:

- a guaranteed working official SimilarWeb API credential flow
- browser automation to log in and refresh a session
- full coverage of every SimilarWeb product surface

## Entry Points

Summarize one or more HAR files:

```powershell
python similarweb/scripts/similarweb_client.py summarize-har `
  C:\path\to\dash.har `
  C:\path\to\sim.har
```

Build the core keyword-analysis request bundle:

```powershell
python similarweb/scripts/similarweb_client.py build-keyword-bundle `
  --keyword "background remover" `
  --month 2026-03
```

Build the observed website-analysis request bundle:

```powershell
python similarweb/scripts/similarweb_client.py build-website-analysis-bundle `
  --domain "pollo.ai" `
  --month 2026-04 `
  --compare-domain "deevid.ai" `
  --compare-domain "hailuoai.video"
```

Build one observed incoming referral-traffic page. The upstream page size is fixed at 100 rows in the captured flow:

```powershell
python similarweb/scripts/similarweb_client.py build-referral-traffic-query `
  --domain "checkout.stripe.com" `
  --from-month 2026-01 `
  --to-month 2026-06 `
  --page 20
```

Build the landing-pages query observed on the organic search page-analysis route.
By default this targets new organic landing pages sorted by new click share, which is useful for finding newly valuable URLs on a domain:

```powershell
python similarweb/scripts/similarweb_client.py build-landing-pages-query `
  --domain "pinterest.com" `
  --month 2026-04
```

Build the website search-keywords query observed on the organic search page-analysis route.
By default this targets new search keywords sorted by click share, matching the "搜索词新增点击" UI state:

```powershell
python similarweb/scripts/similarweb_client.py build-search-keywords-query `
  --domain "pinterest.com" `
  --month 2026-04
```

Build focused search SEO request plans:

```powershell
python similarweb/scripts/similarweb_client.py build-search-landing-pages-overview-query `
  --domain "pinterest.com" `
  --month 2026-04

python similarweb/scripts/similarweb_client.py build-search-keyword-performance-query `
  --domain "pinterest.com" `
  --month 2026-04

python similarweb/scripts/similarweb_client.py build-branded-keywords-query `
  --domain "pinterest.com" `
  --month 2026-04
```

Login through `dash.3ue.com`:

```powershell
python similarweb/scripts/similarweb_client.py login
```

Set project-specific values in the caller project's `.env`, and prefer shared SimilarWeb credentials in a user-level global `.env` or the skills root `.env`:

```env
SIMILARWEB_USERNAME=your-user
SIMILARWEB_PASSWORD=your-password
# Optional fallback when dash login is unavailable or reaches its login limit
SIMILARWEB_TOKEN=your-existing-token
```

Recommended global locations are `~/.config/agent-skills/.env`, `~/.codex/skills/.env`, `~/.env`, or a shared file such as `<skills-root>/.env`. For multi-project local use, keep only project-scoped credentials in each project root `.env`; keep shared SimilarWeb credentials in a user-level file or the skills-root `.env`. Follow the credential-management policy of the repository where the skills are installed.

Default live commands should usually omit `--env-file`: the client builds a candidate chain instead of stopping at the caller project's `.env`. This lets it continue from a project `.env` without SimilarWeb credentials to user-level env files and then to the skill install directory and its parents, including `<skills-root>/.env` when the skill lives under `<skills-root>/similarweb`.

Use `--env-file` only when you intentionally want to pin one exact env file for a one-off run. Passing `--env-file .env` disables fallback to global or skills-root env files.

You can still pass `--project <project-name>` or set `SKILL_PROJECT` for the agent turn.

The client first reuses an unexpired account token from `similarweb/state/token_cache.json`, then logs in with the configured account when necessary. Because `dash.3ue.com` can impose login-count limits, a valid `SIMILARWEB_TOKEN` or `--token` is accepted only as the final fallback after account candidates fail. The client never prints the token.

Login and fetch the full generated-keywords JSON payload:

```powershell
python similarweb/scripts/similarweb_client.py fetch-generated-keywords `
  --keyword "background remover" `
  --month 2026-03 `
  --rows-per-page 20
```

Login and fetch the verified keyword overview bundle:

```powershell
python similarweb/scripts/similarweb_client.py fetch-keyword-overview-bundle `
  --keyword "background remover" `
  --month 2026-03
```

Login and fetch the HAR-observed website analysis bundle:

```powershell
python similarweb/scripts/similarweb_client.py fetch-website-analysis-bundle `
  --domain "pollo.ai" `
  --month 2026-04
```

Build or fetch normalized monthly total-site visits for multiple domains in one request:

```powershell
python similarweb/scripts/similarweb_client.py build-website-traffic-trend-query `
  --domain app.topkey.io `
  --domain climatenest.org `
  --from-month 2026-01 `
  --to-month 2026-06

python similarweb/scripts/similarweb_client.py fetch-website-traffic-trend-query `
  --domain app.topkey.io `
  --domain climatenest.org `
  --from-month 2026-01 `
  --to-month 2026-06
```

Login and fetch the complete incoming referral table. Use `--all-pages` without `--max-pages` to continue until `TotalCount` is reached or a short final page is returned:

```powershell
python similarweb/scripts/similarweb_client.py fetch-referral-traffic-query `
  --domain "checkout.stripe.com" `
  --from-month 2026-01 `
  --to-month 2026-06 `
  --all-pages
```

Use `--max-pages` only for diagnostics or explicitly bounded exploration, never for a full monthly tracking snapshot.

Login and fetch the landing-pages payload:

```powershell
python similarweb/scripts/similarweb_client.py fetch-landing-pages-query `
  --domain "pinterest.com" `
  --month 2026-04
```

Login and fetch the website search-keywords payloads:

```powershell
python similarweb/scripts/similarweb_client.py fetch-search-keywords-query `
  --domain "pinterest.com" `
  --month 2026-04
```

Login and fetch focused search SEO payloads:

```powershell
python similarweb/scripts/similarweb_client.py fetch-search-landing-pages-overview-query `
  --domain "pinterest.com" `
  --month 2026-04

python similarweb/scripts/similarweb_client.py fetch-search-keyword-performance-query `
  --domain "pinterest.com" `
  --month 2026-04

python similarweb/scripts/similarweb_client.py fetch-branded-keywords-query `
  --domain "pinterest.com" `
  --month 2026-04
```

## Workflow

1. Run `summarize-har` first and confirm the request set really contains keyword-analysis or website-analysis traffic rather than only dashboard bootstrap traffic.
2. Keep only the endpoints in the `data_endpoints` bucket when the goal is data collection.
3. Treat `dash.3ue.com` and similar control-plane requests as account or proxy infrastructure, not as the SimilarWeb data surface itself.
4. Use `build-keyword-bundle` to generate the smallest useful request plan for one keyword.
5. Use `build-website-analysis-bundle` when the HAR route is under website analysis, traffic overview, search overview, backlinks, referrals, geography, or SimilarWeb widget APIs.
6. Use `build-referral-traffic-query` for a deterministic incoming-referral request page. Use `fetch-referral-traffic-query --all-pages` to continue through the observed 100-row pages until `TotalCount` is reached or a short page is returned; use `--max-pages` to cap request volume.
   For payment-growth opportunity discovery, the current target set is `checkout.stripe.com`, `paypal.com`, `paddle.com`, and `lemonsqueezy.com`.
7. Treat referral traffic and SEO backlinks as different datasets. Referral rows estimate visits flowing from a source domain into the target; `/api/backlinks/*` describes discovered links and referring domains.
8. Use `build-landing-pages-query` or `fetch-landing-pages-query` for the high-value organic landing-pages view. The default parameters match the observed "new clicks" UI state: `Change=New`, `sourceType=organic`, `sort=ClicksShare`, `asc=false`.
9. Use `build-search-keywords-query` or `fetch-search-keywords-query` for the website search-keywords "new clicks" view. The default parameters match the observed "搜索词新增点击" UI state: `Change=New`, `sourceType=all`, `sort=Share`, `asc=false`.
10. Use `build-search-landing-pages-overview-query`, `build-search-keyword-performance-query`, or `build-branded-keywords-query` for focused SEO views when the full website-analysis bundle is too broad.
11. For the currently verified live keyword workflow, use `login`, `fetch-generated-keywords`, or `fetch-keyword-overview-bundle`.
12. Referral-traffic live replay is verified for the current payment-growth target set. Monthly total-site visits are also live-verified through `EngagementVisits/Graph`; use them after referral ranking has produced a shortlist. For other website-analysis endpoints, still check endpoint status and payload shape because broader website analysis remains HAR-observed rather than fully verified.
13. Env discovery builds a candidate chain instead of stopping at the first `.env`: explicit `--env-file`, caller/project directory chain, selected project root, workspace chain, user-level global env files, and the skill install directory chain.
14. Auth resolution puts every complete username/password pair first and appends valid `SIMILARWEB_TOKEN` / `--token` candidates afterward, so tokens remain fallback-only.
15. The client caches the login response token by username in `similarweb/state/token_cache.json` and reuses it while the JWT `exp` remains safely in the future.
16. If a live request rejects a cached token with `401`, `403`, or a login redirect, the client removes that account's cache entry, logs in again, and retries the operation once. If account login fails or reaches its login limit, the client continues to the configured fallback token.
17. Never commit cookies, tokens, usernames, passwords, raw sensitive HAR excerpts, or multipart challenge bodies.

## Output Contract

`summarize-har` returns grouped endpoints with:

- `host`, `path`, `method`, `hits`, and `statuses`
- normalized `query_keys`
- sampled `response_keys` and `response_shape`
- sanitized sample URL, request body, and response excerpt

`build-keyword-bundle` returns:

- normalized month window in SimilarWeb date format `YYYY|MM|DD`
- the core request list for overview stats, trend, top sites, top pages, device traffic, single metric, and related keywords

`build-website-analysis-bundle` returns:

- normalized month window in SimilarWeb date format `YYYY|MM|DD`
- top-level request context such as `domain`, `month`, `country`, `web_source`, `include_subdomains`, and `compare_domains`
- the observed request list for website header, similar sites, engagement, ranks, geography, traffic sources, search overview, keyword tables, landing pages, assets compare, backlinks, and ad publisher breakdown

`login` returns:

- `ok`
- `username`
- `roles`
- `source`, which may be `cache` or `login`

`fetch-generated-keywords` returns:

- the full JSON object from `POST /api/KeywordGenerator/google/suggest`
- fields such as `records`, `totalRecords`, `totalClicks`, `totalVolume`, and `maxScore`

`fetch-keyword-overview-bundle` returns one JSON object that includes:

- top-level request context such as `keyword`, `month`, `from`, `to`, `country`, `web_source`, and `device`
- `overview_stats`
- `volume_clicks_trend`
- `top_sites`
- `top_pages`
- `device_traffic`
- `single_metric`

`fetch-website-analysis-bundle` returns one JSON object that includes:

- top-level request context such as `domain`, `month`, `from`, `to`, `country`, `web_source`, `include_subdomains`, and `compare_domains`
- one property per request name from `build-website-analysis-bundle`
- both JSON objects and JSON arrays are preserved as returned by SimilarWeb

`build-website-traffic-trend-query` returns:

- normalized `from` / `to` month boundaries and the requested domain list
- one multi-domain monthly request to `GET /widgetApi/WebsiteOverview/EngagementVisits/Graph`
- the defaults `country=999`, `webSource=Total`, `includeSubDomains=true`, and `timeGranularity=Monthly`

`fetch-website-traffic-trend-query` returns:

- `monthly_visits`, keyed by requested domain
- explicit month/value points normalized to `{month, visits}`
- `data_verified` copied from `KeysDataVerification`; `false` is an upstream metadata value, not a failed request

`build-referral-traffic-query` returns:

- the requested `domain`, `from_month`, `to_month`, normalized `from` / `to`, and `page`
- a totals request to `GET /api/websiteanalysis/GetTrafficSourcesTotalReferrals`
- a page request to `GET /api/websiteanalysis/GetTrafficSourcesTotalReferralsTable`
- the observed incoming-traffic defaults `selectedTab=incomingTraffic`, `orderBy=TotalShare desc`, `asc=false`, and a fixed observed page size of 100

`fetch-referral-traffic-query` returns:

- `referral_totals`, preserving the summary dictionary and categories
- `referral_table`, preserving table metadata and `Records[]`; with `--all-pages`, `Records[]` is the ordered merge of fetched pages
- `pagination`, including `start_page`, `end_page`, `pages_fetched`, `page_size`, `total_count`, `records_returned`, and `complete`
- row fields useful for opportunity discovery, including `Domain`, `Rank`, `Change`, `NewChange`, `TotalShare`, `TotalVisits`, `TotalSharePerMonth`, `TotalVisitsAndSharePerMonth`, `Category`, and `EngagementScore` when present

`build-landing-pages-query` returns:

- top-level request context such as `domain`, `month`, `from`, `to`, `country`, `web_source`, `source_type`, `change`, `sort`, and `asc`
- one `POST /api/websiteOrganicLandingPagesV2` request with body `[]`
- default observed query values for new organic landing pages: `Change=New`, `sourceType=organic`, `sort=ClicksShare`, and `asc=false`

`fetch-landing-pages-query` returns one JSON object that includes:

- the same top-level request context
- `landing_pages`, preserving the endpoint JSON payload with fields such as `FromAlternativeSources`, `TotalCount`, `TotalTopLevelCount`, and `Data[]`

`build-search-keywords-query` returns:

- top-level request context such as `domain`, `month`, `from`, `to`, `country`, `web_source`, `source_type`, `change`, `sort`, and `asc`
- one `POST /widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/PresetsTotal` request with body `[]`
- one `POST /widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table` request with body `[]`
- default observed query values for new search-keyword clicks: `Change=New`, `sourceType=all`, `sort=Share`, and `asc=false`

`fetch-search-keywords-query` returns one JSON object that includes:

- the same top-level request context
- `search_keywords_total`, preserving the presets total payload with fields such as `TotalCompetitive`, `TotalPresets`, and `Total`
- `search_keywords_table`, preserving the table payload with fields such as `SearchEngines`, `TotalCount`, `Data`, and `Header`

Focused search SEO builders return one-request plans:

- `build-search-landing-pages-overview-query`: `GET /api/searchoverview/keywords/landing-pages`
- `build-search-keyword-performance-query`: `GET /widgetApi/SearchKeywordsV2/WebsitePerformance/Table`
- `build-branded-keywords-query`: `GET /widgetApi/TrafficSourcesSearchV2/BrandedKeywords/WebsitePerformance/PieChart`

Focused search SEO fetchers return the same top-level request context plus:

- `search_landing_pages_overview`
- `search_keyword_performance`
- `branded_keywords`

## Trust Boundary

Current verified state:

- the HAR proves the keyword-analysis request shapes
- the 2026-05-09 HAR proves website-analysis request shapes for traffic engagement, website performance, traffic overview, search overview, page analysis, backlinks, and ad publisher breakdown
- the 2026-06-05 landing-pages HAR proves the organic page-analysis landing-pages request shape for the "new clicks" UI state
- the 2026-06-06 search-keywords HAR proves the organic page-analysis website-keyword request shape for the "搜索词新增点击" UI state
- the 2026-07-26 external-link-analysis HAR proves the incoming referral totals/table request shapes, the implicit 100-row page size, explicit `page=1/2/22` pagination, and a 71-row final page for `TotalCount=2171`
- the HAR proves `dash.3ue.com` is a separate control plane
- login plus bearer-token replay against `KeywordGenerator/google/suggest` has been verified
- login plus bearer-token replay against the keyword overview bundle endpoints has also been verified
- manual token input is supported only as a final fallback for account-login failure or login-count limits; token values are never included in command output
- website-analysis bundle construction is implemented from HAR evidence, but full live replay has not been verified endpoint-by-endpoint
- a 2026-07-27 live check verified bearer-token replay and two-page collection for `GetTrafficSourcesTotalReferrals` and `GetTrafficSourcesTotalReferralsTable` across `checkout.stripe.com`, `paypal.com`, `paddle.com`, and `lemonsqueezy.com` for 2026-05 and 2026-06
- a 2026-07-27 live check verified multi-domain monthly replay of `EngagementVisits/Graph` for `app.topkey.io` and `climatenest.org` across 2026-01 through 2026-06
- broader endpoint coverage beyond these verified flows is still not fully verified

Do not:

- present this skill as a fully verified official SimilarWeb API client across every endpoint
- commit tokens, cookies, or raw sensitive HAR excerpts
- assume every `sim.3ue.com` endpoint belongs in a data-collection workflow
