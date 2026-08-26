# SimilarWeb API Map

This note is based on captured HAR files:

- `dash.3ue.com.har`
- `sim.3ue.com.har`
- `sim.3ue.com.har` captured on 2026-05-09 from website-analysis routes
- `着陆页新增点击-sim.3ue.com.har` captured on 2026-06-05 from the organic search page-analysis landing-pages route

- `搜索词新增点击-sim.3ue.com.har` captured on 2026-06-06 from the organic search page-analysis website-keyword route
- `外链分析-sim.3ue.com.har` captured on 2026-07-26 from the website-analysis incoming referral-traffic route

The captures show a clear split between a proxy or account control plane and the actual SimilarWeb data surface.

## 1. Surface Split

### Control plane: `dash.3ue.com`

Observed responsibilities:

- login and token refresh
- subscription and balance lookup
- notices and account-specific auditing
- proxy or node discovery via `mitmApi/nodes`

Representative paths:

- `/api/account/login`
- `/api/account/refreshToken`
- `/api/subscription/self`
- `/api/config/kv`
- `/api/balance/status`
- `/api/balance/history`
- `/api/auditing/self`
- `/api/auditing/self/sum`
- `/api/notice/all`

Interpretation:

- this host looks like a reseller or gateway control plane
- it is not the primary business data surface for SimilarWeb keyword or website analysis

### Data plane: `sim.3ue.com`

These are the endpoints worth keeping for a SimilarWeb keyword-analysis skill.

Core keyword endpoints observed in HAR:

- `GET /api/KeywordAnalysis/Overview/Stats`
- `GET /api/KeywordAnalysis/Overview/VolumeClicksTrend`
- `GET /api/KeywordAnalysis/Overview/TopSites`
- `GET /api/KeywordAnalysis/Overview/TopPages`
- `POST /api/KeywordGenerator/google/suggest`
- `GET /widgetApi/KeywordAnalysisV2/KeywordAnalysisOrganic/DeviceTraffic`
- `GET /widgetApi/MobileTrafficV2/MobileTraffic/SingleMetric`
- `GET /autocomplete/keywords`
- `GET /autocomplete/websites`
- `GET /api/images/`

These are the endpoints that directly return keyword metrics, competitor domains, page-level landing URLs, traffic composition, and related keyword suggestions.

Website-analysis endpoints observed in the 2026-05-09 HAR:

- `GET /api/WebsiteOverview/getheader`
- `GET /api/WebsiteOverview/getsimilarsites`
- `GET /widgetApi/WebsiteOverview/EngagementVisits/SingleMetric`
- `GET /widgetApi/WebsiteOverview/EngagementDesktopVsMobileVisits/PieChart`
- `GET /widgetApi/WebsiteOverview/WebRanks/SingleMetric`
- `GET /widgetApi/WebsiteOverview/EngagementOverview/Table`
- `GET /widgetApi/WebsiteOverview/EngagementVisits/Graph`
- `GET /widgetApi/WebsiteOverview/EngagementVisits/Table`
- `GET /widgetApi/WebsiteGeography/Geography/Table`
- `GET /widgetApi/MarketingMixTotal/TrafficSourcesOverview/PieChart`
- `GET /widgetApi/MarketingMixTotal/TrafficSourcesOverview/BarChart`
- `GET /widgetApi/MarketingMixTotal/TrafficSourcesOverview/BarChartPop`
- `GET /widgetApi/MarketingMixTotal/TrafficSourcesOverview/Table`
- `GET /widgetApi/SearchKeywordsV2/WebsitePerformance/Table`
- `GET /widgetApi/TrafficAndEngagement/EngagementOverview/Table`
- `GET /widgetApi/TrafficSourcesSearchV2/BrandedKeywords/WebsitePerformance/PieChart`
- `GET /widgetApi/WebNewVsReturning/NewVsReturning/Data`
- `GET /widgetApi/AssetsCompare/Visits/Graph`
- `GET /widgetApi/AssetsCompare/Duration/Graph`
- `GET /api/searchoverview/overview/traffic`
- `GET /api/searchoverview/overview/keywords`
- `GET /api/searchoverview/keywords/brand-split`
- `GET /api/searchoverview/keywords/rank-distribution`
- `GET /api/searchoverview/overview/top-keywords`
- `GET /api/searchoverview/keywords/landing-pages`
- `POST /api/websiteOrganicLandingPagesV2`
- `POST /widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/PresetsTotal`
- `POST /widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table`
- `GET /api/backlinks/summary`
- `GET /api/backlinks/timeseries`
- `GET /api/backlinks/timeseries/newlost`
- `POST /api/backlinks/refdomains`
- `POST /api/backlinks/backlinks`
- `GET /api/AdIntelligence/Advertiser/Publishers/breakdown`
- `GET /api/ConversionRates/Countries`
- `GET /api/ConversionRates/Overview` and `GET /api/ConversionRates/Overtime/Visits`, both observed as `406` in this capture
- `GET /api/websiteanalysis/GetTrafficSourcesTotalReferrals`
- `GET /api/websiteanalysis/GetTrafficSourcesTotalReferralsTable`

These endpoints return website header metadata, similar sites, visits and engagement, desktop/mobile split, ranks, geography, marketing channel mix, search overview, keyword tables, page-analysis rows, backlinks, referring domains, incoming referral traffic, and ad publisher breakdowns.

### Internal or dashboard-only endpoints

Observed examples:

- `/api/userdata/...`
- `/api/activation/...`
- `/api/api-management/user-keys`
- `/api/account/collaborationHubLink`
- `/api/fit-score`
- `/api/PerformanceAddOn/MutualAssets`
- `/api/startupSettings`
- `/settings`
- `/api/identities`
- `/sales-api/company-quota`

Interpretation:

- these mostly support the hosted UI, account state, campaign setup, recent-history, or product activation flows
- they are lower priority for a data collection skill

## 2. Request Conventions

### Date format

Observed format:

- `from=2026|03|01`
- `to=2026|03|31`

This means request builders should output `YYYY|MM|DD`, not ISO `YYYY-MM-DD`.

### Common query parameters

Frequently repeated parameters:

- `country=999`
- `isWindow=false`
- `webSource=Total`
- `device=Total` or `Device=Total`
- `sourceType=all`

Keyword parameter naming varies by endpoint:

- `key=<keyword>` for overview endpoints
- `keys=<keyword>` for widget endpoints
- `keyword=<keyword>` for suggestion endpoints

Website parameter naming also varies:

- `key=<domain>` for header, similar-sites, ad-intelligence, and landing-page endpoints
- `keys=<domain>` for most widget APIs and search overview endpoints
- `Key=<domain>` for backlinks endpoints
- `IncludeSubdomains=true` on conversion-rate endpoints, but `includeSubDomains=true` on most website-analysis endpoints
- `pageFilterJson=[{"url":"<domain>","searchType":"domain"}]` for page-analysis keyword and landing-page endpoints

Incoming referral-traffic parameter naming observed on 2026-07-26:

- `key=<domain>`
- `selectedTab=incomingTraffic`
- `orderBy=TotalShare desc`
- `asc=false`
- `page=<1-based page>`; omitting `page` behaved like page 1 in the capture
- the table returned 100 rows per full page and did not expose a page-size query parameter

### Observed request headers

Repeated across data requests:

- `accept: application/json`
- `content-type: application/json; charset=utf-8`
- `x-requested-with: XMLHttpRequest`
- `x-sw-page: <current app route>`
- `x-sw-page-view-id: <uuid-like value>`

The route header encodes the current SimilarWeb page context, for example a keyword overview page under `pro.similarweb.com`.

Website-analysis routes observed in the 2026-05-09 HAR include:

- `/digitalsuite/websiteanalysis/traffic-engagement/*/999/1m/`
- `/digitalsuite/websiteanalysis/overview/website-performance/*/999/1m`
- `/digitalsuite/websiteanalysis/traffic-overview/*/999/1m/`
- `/digitalsuite/websiteanalysis/search-overview/*/999/1m`
- `/organicsearch/pageAnalysis/landing-pages-v2/*/999/2026.04-2026.04`
- `/organicsearch/pageAnalysis/website-keyword-v2/*/999/1m`

## 3. Response Shapes

### `/api/KeywordAnalysis/Overview/Stats`

Useful fields observed:

- `Difficulty`
- `Competition`
- `CPCRangeMin`
- `CPCRangeMax`
- `TotalSpentRangeMin`
- `TotalSpentRangeMax`
- `IntentVolumeDistribution`
- `SERPCompositionBreakDown`

### `/api/KeywordAnalysis/Overview/VolumeClicksTrend`

Useful fields observed:

- `Breakdown`
- `Average`

This is the main trend endpoint for clicks and volume over time.

### `/api/KeywordAnalysis/Overview/TopSites`

Useful fields observed inside `Competitors[]`:

- `Domain`
- `Clicks`
- `OrganicShare`
- `PaidShare`
- `YearlyTrend`

### `/api/KeywordAnalysis/Overview/TopPages`

Useful fields observed inside `Pages[]`:

- `Url`
- `Domain`
- `Clicks`
- `OrganicShare`
- `PaidShare`
- `YearlyTrend`

### `/api/KeywordGenerator/google/suggest`

Useful fields observed:

- `records[]`
- `totalRecords`
- `totalClicks`
- `totalVolume`
- `maxScore`

Useful fields inside each record:

- `keyword`
- `monthlyVolume`
- `clicks`
- `cpc`
- `leadingSite`
- `difficulty`
- `primaryIntent`
- `volumeTrend`
- `score`

### `/widgetApi/MobileTrafficV2/MobileTraffic/SingleMetric`

Useful fields observed inside `Data[keyword]`:

- `VolumesMonthly`
- `Volume`
- `MobileShareMonthly`
- `MobileShare`
- `ZeroClicksMonthly`
- `ZeroClicksYearlyAverage`

### `/widgetApi/KeywordAnalysisV2/KeywordAnalysisOrganic/DeviceTraffic`

Useful fields observed inside `Data[keyword]`:

- `MonthToVisits`
- `TotalClicks`

### Website overview and engagement widgets

Useful shapes observed:

- `/api/WebsiteOverview/getheader` returns a domain-keyed object with fields such as `mainDomainName`, `icon`, `title`, `description`, `globalRanking`, and `highestTrafficCountry`
- `/api/WebsiteOverview/getsimilarsites` returns a list containing `Domain`, `DomainWithoutSub`, `Rank`, and `Favicon`
- `/widgetApi/WebsiteOverview/EngagementVisits/SingleMetric` returns `Data[domain]`
- `/widgetApi/WebsiteOverview/EngagementVisits/Graph` accepts comma-separated domains in `keys`, supports `timeGranularity=Monthly`, and returns `Data[domain].Total[]` points plus `KeysDataVerification`
- `/widgetApi/WebsiteOverview/EngagementDesktopVsMobileVisits/PieChart` returns `Data[domain]`
- `/widgetApi/WebsiteOverview/WebRanks/SingleMetric` returns `Data[domain]`
- `/widgetApi/TrafficAndEngagement/EngagementOverview/Table` returns `FromAlternativeSources`, `TotalCount`, `TotalTopLevelCount`, `KeysDataVerification`, and `Data[]`
- `/widgetApi/WebNewVsReturning/NewVsReturning/Data` returns `domain -> Graph/Total`

### Traffic sources, geography, referrals

Useful shapes observed:

- `/widgetApi/MarketingMixTotal/TrafficSourcesOverview/PieChart` returns `Data.Total`
- `/widgetApi/MarketingMixTotal/TrafficSourcesOverview/BarChart` returns `Data`, `DailyData`, `WeeklyData`, and `MonthlyData`
- `/widgetApi/MarketingMixTotal/TrafficSourcesOverview/Table` returns `Filters` and `Data[]`
- `/widgetApi/WebsiteGeography/Geography/Table` returns country filters plus `Data[]`
- `/widgetApi/WebsiteOverview/TopReferrals/Table`, `/TopReferringCategories/Table`, and `/TrafficDestinationReferrals/Table` return `TotalCount`, `TotalTopLevelCount`, and `Data[]`
- `/api/websiteanalysis/GetTrafficSourcesTotalReferrals` returns a domain-keyed `dictionary` plus `Categories`
- `/api/websiteanalysis/GetTrafficSourcesTotalReferralsTable` returns `TotalShare`, `TotalVisits`, `TotalVisitsGlobalList`, `TopCategories`, `Categories`, `AllCategories`, `Topics`, `TotalCount`, `TotalUnGroupedCount`, and `Records[]`
- useful referral row fields include `Domain`, `Rank`, `Change`, `NewChange`, `Share`, `FilteredShare`, `TotalVisits`, `TotalShare`, `TotalSharePerMonth`, `TotalVisitsAndSharePerMonth`, `SiteOrigins`, `Category`, and optional `EngagementScore`
- the capture proves 1-based pagination with 100 rows per full page: `TotalCount=2171` produced 100 rows on pages 1 and 2 and 71 rows on page 22
- these rows describe estimated incoming referral visits into the target domain; they are not the same as the SEO link graph returned by `/api/backlinks/*`

### Search overview and page analysis

Useful shapes observed:

- `/api/searchoverview/overview/traffic` returns `TrafficSourcesVisits` and `AdSpend`
- `/api/searchoverview/overview/keywords` returns domain-keyed interval metrics
- `/api/searchoverview/keywords/brand-split` returns branded/non-branded shares
- `/api/searchoverview/keywords/rank-distribution` returns `Country` and `RankSplit`
- `/api/searchoverview/overview/top-keywords` returns keyword-keyed objects containing `Clicks`, `ClicksShare`, `OrganicClicks`, and `PaidClicks`
- `/api/searchoverview/keywords/landing-pages` returns `Url`, `Clicks`, `ClicksShare`, `Spend`, `TopKeyword`, and `TotalKeywords`
- `/widgetApi/SearchKeywordsV2/WebsitePerformance/Table` returns `FromAlternativeSources`, `TotalCount`, `TotalTopLevelCount`, and `Data[]`
- `/widgetApi/TrafficSourcesSearchV2/BrandedKeywords/WebsitePerformance/PieChart` returns branded versus non-branded search keyword split data.
- `/api/websiteOrganicLandingPagesV2` returns `FromAlternativeSources`, `TotalCount`, `TotalTopLevelCount`, and `Data[]`
- `/api/websiteOrganicLandingPagesV2` with `Change=New`, `sourceType=organic`, `sort=ClicksShare`, and `asc=false` represents the observed "new clicks" landing-pages view. Useful row fields include `Url`, `Trend`, `Clicks`, `DesktopClicks`, `PrevClicks`, `ClicksShare`, `KeywordsCount`, `TopKeyword`, `ChangeState`, `SerpFeatures`, and `LatestKeywordSerpDate`.
- `/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/PresetsTotal` returns `TotalCompetitive`, `TotalPresets`, and `Total`
- `/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table` returns `SearchEngines`, `TotalCount`, `Data`, and `Header`
- `/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/PresetsTotal` plus `/widgetApi/WebsiteAnalysisV2/WebsiteAnalysis/Table` with `Change=New`, `sourceType=all`, `sort=Share`, and `asc=false` represents the observed "搜索词新增点击" website-keyword view. Useful table fields include `SearchEngines`, `TotalCount`, `Data.KeywordsCount`, `Data.OverallClicks`, `Data.Records[]`, and `Header`.

### Backlinks and ad intelligence

Useful shapes observed:

- `/api/backlinks/summary` returns `Target`, `TopTlds`, and `TopCountries`
- `/api/backlinks/timeseries` returns daily rows with `Date`, `Backlinks`, `ReferringDomains`, and `Rank`
- `/api/backlinks/timeseries/newlost` returns daily rows with new/lost backlinks and referring domains
- `/api/backlinks/refdomains` and `/api/backlinks/backlinks` return `TotalRecords`, `Records`, `Page`, and `PageSize`
- `/api/AdIntelligence/Advertiser/Publishers/breakdown` returns `records`, `totalCount`, and `hasAdIntelMetrics`

## 4. Auth Boundary

This is the most important constraint.

Observed facts from HAR:

- `dash.3ue.com` login returns a token through the control plane
- `sim.3ue.com` business requests do not show `Authorization` or `Cookie` headers in the captured HAR
- `sim.3ue.com` requests still succeed with `200`

Initial interpretation from HAR alone:

- the real auth is being handled by a hidden session layer, reverse proxy, browser plugin, or MITM bridge
- the HAR is enough to recover request shapes
- the HAR is not enough, by itself, to prove a clean-room replay strategy
- the website-analysis HAR proves request and response shapes, but not live replay reliability for every endpoint

Additional live verification:

- `GET https://dash.3ue.com/api/account/login?...` returns a token in JSON
- replaying that token as `Authorization: Bearer <token>` against `POST /api/KeywordGenerator/google/suggest` succeeds
- replaying the same token together with `GMITM_token` and `GMITM_uname` cookies also succeeds against:
  - `GET /api/KeywordAnalysis/Overview/Stats`
  - `GET /api/KeywordAnalysis/Overview/VolumeClicksTrend`
  - `GET /api/KeywordAnalysis/Overview/TopSites`
  - `GET /api/KeywordAnalysis/Overview/TopPages`
  - `GET /widgetApi/KeywordAnalysisV2/KeywordAnalysisOrganic/DeviceTraffic`
  - `GET /widgetApi/MobileTrafficV2/MobileTraffic/SingleMetric`
- unauthenticated calls return HTML redirect content that points back to `dash.3ue.com`
- the bearer token contains a JWT `exp`, so local cache reuse can be gated by expiration time
- a 2026-07-26 live check verified account login followed by bearer-token replay against the generated-keywords endpoint
- a 2026-07-27 live check verified a single multi-domain `EngagementVisits/Graph` request for `app.topkey.io` and `climatenest.org`, normalized across 2026-01 through 2026-06

Practical consequence:

- a safe first version of the skill can support login plus generated-keyword fetching
- the same auth strategy is now verified for the keyword overview bundle
- the same auth strategy is implemented for the website-analysis bundle, but those endpoints still need endpoint-by-endpoint live verification
- the monthly `EngagementVisits/Graph` subset is endpoint-verified and can be used to confirm or contradict shortlisted payment-growth leads
- a 2026-07-27 live check verified bearer-token replay and two-page collection against the incoming referral totals/table endpoints for `checkout.stripe.com`, `paypal.com`, `paddle.com`, and `lemonsqueezy.com` across 2026-05 and 2026-06
- token cache can be local and expiration-aware while passwords remain in the configured credential source
- cache reuse avoids unnecessary fresh logins when the upstream limits concurrent devices
- a server-rejected cached token should be removed before one fresh-login retry
- because the control plane can reject additional logins after its login-count limit is reached, a separately configured valid token can be tried after all account candidates fail
- broader live replay should still be treated cautiously until each endpoint is verified

## 5. Minimal Skill Scope

The smallest useful SimilarWeb skill from these HARs should do these things well:

1. separate control-plane traffic from data traffic
2. generate reusable request bundles for keyword analysis
3. generate reusable request bundles for website analysis
4. sanitize sensitive strings before showing or storing any HAR-derived output
5. support the verified live flow: login plus generated-keyword fetching
6. support the verified live flow: keyword overview bundle fetching
7. support HAR-observed website-analysis bundle replay with explicit trust-boundary notes
8. support focused HAR-observed SEO requests for landing-page overview, keyword performance, and branded keyword split
9. support HAR-observed incoming referral totals, deterministic page requests, and bounded automatic pagination
10. support live-verified multi-domain monthly total-site visit trends
11. cache bearer tokens locally until they approach JWT expiry
12. resolve account credentials, refresh a rejected cached token through login, retry once, and then use a valid configured token only as fallback


That is exactly the scope implemented by `similarweb/scripts/similarweb_client.py`.
