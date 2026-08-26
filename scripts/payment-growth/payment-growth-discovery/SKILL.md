---
name: payment-growth-discovery
description: Collect complete monthly incoming referral tables for checkout.stripe.com, paypal.com, paddle.com, and lemonsqueezy.com; identify fast-growing products primarily from full-table position changes; add recent total-site traffic trends for shortlisted domains; report category-level payment-intent growth or decline with leading products; find new products; open shortlisted websites for manual validation; and estimate monthly revenue as a low/base/high USD range. Use for payment-platform opportunity discovery, category trend tracking, early product discovery, and revenue estimation. Do not use this skill to claim audited revenue or company identity.
---

# Payment Growth Discovery

Use the bundled script to collect SimilarWeb referral snapshots and compare two months or a complete rolling range. Produce two conclusions:

1. category-level payment-intent growth or decline, with typical leading products
2. newly visible or young fast-growing products

Then collect recent total-site traffic for the shortlisted domains, open the websites, validate what they sell, and estimate monthly revenue in USD. Treat payment-platform referral values as payment-intent evidence and total-site visits as product-traction evidence; neither is recharge value, transaction count, or audited revenue.

## Dependency

Read and follow [`../similarweb/SKILL.md`](../similarweb/SKILL.md) before live collection. Reuse its authentication, token cache, endpoint client, and trust boundary. Do not duplicate credentials or print raw tokens.

## Default targets

- `checkout.stripe.com`
- `paypal.com`
- `paddle.com`
- `lemonsqueezy.com`

Pass one or more `--target` arguments to override this set.

## Collect snapshots

Collect the complete source table for every target and complete month:

```powershell
python payment-growth-discovery/scripts/payment_growth.py collect `
  --month 2026-05 `
  --month 2026-06
```

The collector:

- queries each month independently
- follows every 100-row page until the upstream total is reached or a short final page is returned
- saves a snapshot only when upstream pagination explicitly reports `complete=true`
- raises an error instead of silently storing a partial table
- stores one idempotent snapshot per target and month
- replaces that snapshot on rerun instead of appending duplicates
- writes to `payment-growth-discovery/state/payment_growth.sqlite3` by default
- omits invalid pseudo-domains such as `Referral`

For rolling analysis, collect every month independently. Never construct a six-month report from a single multi-month API response.

## Build opportunity lists

```powershell
python payment-growth-discovery/scripts/payment_growth.py report `
  --previous-month 2026-05 `
  --current-month 2026-06 `
  --target lemonsqueezy.com `
  --limit 20 `
  --min-current-visits 1000 `
  --min-previous-visits 250
```

Interpret the lists as follows:

- `category_conclusions.gainers` and `.decliners`: category-level estimated payment-intent visit changes, each with representative current head products
- `new_product_growth`: product-level, cross-payment-platform candidates, deduplicated by source domain; includes every newly present product regardless of visit floor, plus enriched young domains with positive growth
- `fast_rank_growth`: the primary product-growth conclusion, covering every shared source whose full-table position improved and sorting by position gain without a visit floor
- `rank_risers`: legacy thresholded per-target rank-riser list retained for compatibility
- `traffic_gainers`: sources present in both months whose estimated absolute referral visits increased
- `newcomers`: compatibility per-target list of new sources after the configured current-visit floor
- `young_growth_candidates`: enriched sources no more than 730 days old that occur in one or more of the preceding evidence lists

Prioritize `fast_rank_growth` by `rank_gain`. Use estimated referral-visit growth, recent total-site traffic direction, repeated monthly improvement, category, domain age, and website inspection as supporting evidence. The stored `position` is the referral-table order; `global_rank` is a different SimilarWeb field and must not be used as the payment-source position.

Because both months are complete, a `new_product_growth` item with `newly_visible` means absent from the previous returned source table and present in the current one. It still does not prove that the domain is newly registered or newly launched.

Use all four targets for the main conclusion. Use one or more `--target` arguments only for a target-specific diagnostic.

## Add recent website traffic

After ranking the complete referral tables, enrich the filtered candidates with monthly total-site visits. Use a large `--limit` when the goal is to retain every positive rank mover rather than only a presentation-sized top list:

```powershell
python payment-growth-discovery/scripts/payment_growth.py traffic-enrich `
  --previous-month 2026-05 `
  --current-month 2026-06 `
  --start-month 2026-01 `
  --end-month 2026-06 `
  --limit 2000
```

Use repeated `--source-domain` arguments to analyze an already-curated shortlist directly. The collector batches domains, saves every requested month, and stores a missing month as `available=false` with `visits=null`; never convert missing SimilarWeb coverage to zero.

Each candidate in `report` receives `website_traffic` from the cached six-month window by default. Interpret it as a second evidence layer:

- `sustained_growth`: the latest three available consecutive months all increased
- `sustained_decline`: the latest three available consecutive months all decreased
- `growing` / `declining`: the full available window rose or fell without a three-month streak
- `insufficient_data` / `unavailable`: do not infer a direction
- `growth_rate`: first-to-latest total-site visit change
- `latest_month_growth_rate`: most recent available month-over-month change

A payment-referral rank rise with declining total-site traffic is a weaker or conflicting lead. A rank rise, referral-visit gain, and sustained total-site growth together are stronger evidence before opening the website and estimating revenue.

## Validate the shortlist

Do not stop at the generated rankings. Open the leading candidates in a browser and check:

- the product is live and usable rather than parked, templated, or empty
- the homepage and product explain what is sold
- public pricing, billing period, free tier, and checkout currency
- visible traction such as customer counts, reviews, changelog activity, social activity, or product usage
- whether the referral path plausibly represents merchant checkout

Inspect the top 10 new-product candidates by default, then retain 3–5 actionable leads. Manual inspection takes priority over RDAP age. Use RDAP only as supporting evidence for claims about a young domain.

For PayPal candidates, require stronger product and checkout evidence because incoming PayPal traffic includes broad wallet and consumer-payment activity.

## Estimate monthly revenue in USD

Estimate revenue only after opening and validating the website. Return a range rather than a single precise number:

- `estimated_monthly_revenue_usd_low`
- `estimated_monthly_revenue_usd_base`
- `estimated_monthly_revenue_usd_high`
- `revenue_model`: subscription, one-time purchase, marketplace take rate, advertising, or mixed
- `assumptions`: price, inferred paying users or monthly orders, conversion assumptions, and any public traction evidence
- `original_currency`, `fx_rate_to_usd`, and `fx_rate_date` when pricing is not in USD
- `confidence`: low, medium, or high

Use the model appropriate to the business:

- subscription: estimated paying users × average monthly revenue per account
- one-time purchase: estimated monthly orders × average order value
- marketplace: estimated monthly GMV × take rate
- mixed model: calculate components separately, then sum the ranges

Never equate SimilarWeb referral visits directly with successful payments. Use them only to constrain relative scale and direction. Convert every final estimate to USD using a dated, authoritative exchange rate while retaining the original currency and rate metadata.

## Build a rolling report

```powershell
python payment-growth-discovery/scripts/payment_growth.py rolling-report `
  --start-month 2026-01 `
  --end-month 2026-06 `
  --target checkout.stripe.com `
  --limit 20 `
  --min-current-visits 1000 `
  --min-months-present 3 `
  --breakout-growth-rate 1.0
```

The command requires a complete stored snapshot for every selected target and month. It fails explicitly when coverage is missing or incomplete.

- `sustained_growth`: present for at least the requested number of months and estimated visits rose in each of the latest three complete months
- `breakouts`: latest-month estimated visits grew by at least the configured rate over the preceding month
- `newly_visible`: first appeared within the final two months of the requested complete range
- `young_sustained_growth`: sustained-growth candidates whose authoritative RDAP age is within the configured threshold

Every candidate includes its complete month series, first observed month, months present, positive growth-step count, recent absolute and relative growth when calculable, and explicit risk flags.

## Enrich candidate domains

```powershell
python payment-growth-discovery/scripts/payment_growth.py enrich `
  --previous-month 2026-05 `
  --current-month 2026-06 `
  --target lemonsqueezy.com `
  --limit 20
```

The enrichment workflow:

- selects the deduplicated union of rank risers, traffic gainers, and newcomers
- discovers the authoritative RDAP service from IANA's DNS Bootstrap registry
- falls back from a source subdomain to parent labels until a registered domain is found
- records registration, expiration, registrar, authoritative query URL, status, and error
- caches each source-domain profile for 30 days; pass `--force` to retry cached failures
- isolates per-domain failures so one slow registry does not abort the batch

For candidates produced by `rolling-report`, use the corresponding command:

```powershell
python payment-growth-discovery/scripts/payment_growth.py rolling-enrich `
  --start-month 2026-01 `
  --end-month 2026-06 `
  --target checkout.stripe.com `
  --limit 20
```

## Filtering rules

- Filter invalid non-domain labels during ingestion.
- Exclude payment-platform domains from opportunity reports, including Stripe, PayPal, Paddle, and Lemon Squeezy domains.
- Require complete source tables for both comparison months.
- Use full-table position gain as the primary product-growth signal.
- Include all returned sources in category totals; apply visit floors only to product-growth candidate lists.
- Do not apply visit floors to `fast_rank_growth` or newly present `new_product_growth` items.
- Apply current and previous visit floors only to traffic-growth rates and existing young-product growth to reduce low-base spikes.
- Preserve source subdomains because checkout or application subdomains may carry distinct commercial meaning.
- Use RDAP's returned `ldhName` as the registrable domain; do not infer legal company ownership from it.

## Output contract

`collect` prints only collection metadata:

- targets and months
- `collection_scope=full`
- saved snapshots and rows
- upstream total count, pages fetched, and confirmation that the full upstream table was exhausted

`report` returns evidence with:

- `category_conclusions.gainers` and `.decliners`, including previous/current estimated payment-intent visits, absolute and relative change, and up to five typical current head products per category
- `new_product_growth`, deduplicated across selected payment targets with combined previous/current estimated payment-intent visits, target positions, signals, and risk flags
- `fast_rank_growth`, covering all positive full-table position changes and ordered by position improvement, with previous/current position and estimated visits
- target and source domain
- current and previous table positions
- current and previous estimated visits
- rank gain, absolute growth, or growth rate as applicable
- SimilarWeb global rank and category when available
- cached RDAP registration fields and domain age at the end of the current report month
- a cross-filtered young-domain list when registration data is available
- `website_traffic_window`, describing the cached recent month range
- `website_traffic` on every shortlisted product item, including explicit monthly availability, first/latest visits, total-window growth, latest month-over-month growth, positive/negative steps, and trend classification

The final human-facing report adds manual validation and the USD revenue fields defined above. Keep the two conclusion sections separate:

1. category growth/decline with representative head products
2. new-product growth with website findings and estimated monthly revenue in USD

`traffic-enrich` prints collection metadata for shortlisted total-site traffic:

- normalized domains and requested months
- saved series count
- `points_available` and `points_missing`

`rolling-report` additionally returns:

- required and complete snapshot coverage
- the ordered month range and per-domain series
- months present and positive month-to-month growth steps
- sustained-growth, breakout, newly-visible, and young-sustained lists
- `paypal_broad_intent`, `unknown_category`, and `rdap_unavailable` risk flags

See [`references/schema.md`](references/schema.md) when changing persistence or writing direct SQL.

## Trust boundary

- SimilarWeb values are modeled estimates.
- Incoming referral traffic is only a proxy for commercial or payment activity.
- Total-site traffic is a separate modeled estimate of product traction; it can confirm or contradict the payment-referral signal but does not prove revenue.
- Missing total-site months remain unavailable, never zero, and trend labels use only available points.
- PayPal traffic is broader than merchant checkout traffic and needs stricter interpretation.
- Rank in the source payload is SimilarWeb global rank. The skill records table order separately as `position`.
- Monthly opportunity reports refuse missing or incomplete snapshots.
- Absence from a complete returned table is stronger than absence from a bounded top-N sample, but SimilarWeb coverage can still omit unmeasured sources.
- Category values are estimated payment-intent visits, not recharge amounts or revenue.
- One source appearing across multiple payment targets can contribute traffic to each target; product conclusions deduplicate the domain while retaining its target list.
- Rolling “sustained” means three consecutive increases at the end of the selected range; inspect the full series for earlier volatility.
- RDAP registration time describes the current registry object. It is not proof of launch date, first-ever registration, operator identity, or business legitimacy.
- Missing or failed RDAP data remains unknown; never substitute a guessed domain age.
- Keep the SQLite state, credentials, tokens, and raw responses out of version control.
