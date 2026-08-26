# SimilarWeb Open-Source Notes

This note tracks GitHub projects that are adjacent to the SimilarWeb skill, with an emphasis on whether they help the current "logged-in web flow" approach.

## Recommended References

### `DaWe35/Similarweb-free-API`

Repository:

- <https://github.com/DaWe35/Similarweb-free-API>

What it does:

- calls `https://data.similarweb.com/api/v1/data?domain=<domain>`
- uses a hidden endpoint exposed by the SimilarWeb browser extension
- returns free domain-level overview data without an API key

Why it matters:

- useful as a secondary public-data path for domain traffic snapshots
- does not depend on the reseller control plane

Why it is not enough for this skill:

- it is domain-centric, not keyword-centric
- it does not cover `sim.3ue.com` keyword-analysis endpoints
- it does not help with logged-in keyword overview pages or generated keywords

### `chat-data-llc/shopify_store_traffic_api`

Repository:

- <https://github.com/chat-data-llc/shopify_store_traffic_api>

What it does:

- calls `https://pro.similarweb.com/widgetApi/WebsiteOverview/EngagementVisits/SingleMetric`
- authenticates with `.DEVICETOKEN.SIMILARWEB.COM` and `.SGTOKEN.SIMILARWEB.COM` cookies
- batches domain traffic checks for Shopify stores

Why it matters:

- confirms that private `pro.similarweb.com` widget APIs can be replayed from browser cookies
- reinforces the broader conclusion that SimilarWeb web traffic often hinges on cookie-backed browser state rather than official API keys

Why it is only a reference:

- focuses on website overview, not keyword analysis
- uses a different cookie set from the `dash.3ue.com` plus `sim.3ue.com` flow verified in this project
- should not be mixed blindly with the current token plus `GMITM_*` auth strategy

## Low-Confidence References

### `wchan757/similarweb_scraper`

- <https://github.com/wchan757/similarweb_scraper>
- downloads HTML through desktop-browser automation and parses `Sw.preloadedData`
- fragile and operationally heavy
- not a good base for a stable skill

### `miguelmota/similarweb-scrape`

- <https://github.com/miguelmota/similarweb-scrape>
- archived DOM scraper against public SimilarWeb pages
- README explicitly warns about bot detection and breakage risk
- useful only as historical context

## Practical Takeaway

The most reusable open-source ideas are:

1. the free extension endpoint for public domain snapshots
2. cookie-backed replay of private widget endpoints

For this skill's current purpose, the most reliable path remains local expiration-aware cache reuse followed by account login through `dash.3ue.com` and replay against `sim.3ue.com` keyword-analysis endpoints. A separately configured valid token is reserved for the final fallback when account login fails or reaches its login-count limit.
