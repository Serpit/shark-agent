# SQLite schema

The default database is `payment-growth-discovery/state/payment_growth.sqlite3`.

## `referral_snapshots`

One row per target and month.

| Column | Meaning |
| --- | --- |
| `target_domain` | Payment-platform destination |
| `month` | Independent `YYYY-MM` snapshot month |
| `collected_at` | UTC collection time |
| `total_count` | Upstream source count |
| `pages_fetched` | Number of 100-row pages requested |
| `records_returned` | Valid domains retained |
| `complete` | Whether collection reached the end of the upstream table |

`(target_domain, month)` is unique. A rerun updates this row and replaces its child rows.

## `referral_rows`

One source domain within one snapshot.

| Column | Meaning |
| --- | --- |
| `source_domain` | Normalized source host with leading `www.` removed |
| `position` | One-based table position at collection time |
| `global_rank` | SimilarWeb global rank; not table position |
| `change` / `new_change` | Upstream change fields |
| `total_share` / `total_visits` | Upstream aggregate estimates |
| `month_abs_visits` | Absolute referral visits for the snapshot month |
| `category` | SimilarWeb category |
| `engagement_score` | Optional upstream score |

`(snapshot_id, source_domain)` is unique.

## `domain_profiles`

One cached RDAP lookup per normalized source host.

| Column | Meaning |
| --- | --- |
| `source_domain` | Source host used by the referral report |
| `registrable_domain` | Registered domain returned by authoritative RDAP |
| `rdap_status` | `ok`, `not_found`, `unsupported_tld`, or `error` |
| `registered_at` / `expires_at` | Registry events when disclosed |
| `registrar` | Registrar name when disclosed |
| `rdap_url` | Authoritative URL that produced the profile |
| `fetched_at` | UTC cache timestamp |
| `error` | Explicit failure detail; never interpreted as a domain-age value |

`source_domain` is unique. Enrichment updates the row on refresh and reuses profiles newer than 30 days unless `--force` is supplied.

## `website_traffic_months`

One normalized monthly total-site visit point per source-domain and request scope.

| Column | Meaning |
| --- | --- |
| `source_domain` | Shortlisted website host; subdomains are intentionally preserved |
| `month` | Requested `YYYY-MM` month |
| `visits` | SimilarWeb modeled total-site visits, or `NULL` when unavailable |
| `available` | Whether the upstream response included this month |
| `data_verified` | Upstream `KeysDataVerification` metadata; false does not mean request failure |
| `collected_at` | UTC collection time |
| `country` / `web_source` / `include_subdomains` | Request scope used for the point |

The composite request scope is unique. Reruns update the corresponding points. Missing months are persisted explicitly as unavailable and must never be interpreted as zero visits.

## Query semantics

- Compare rows by `(target_domain, source_domain)` across months.
- Collect the complete returned source table for every target and month.
- Refuse opportunity comparisons when either snapshot is missing or incomplete.
- Treat absence from a complete returned table as “not returned by SimilarWeb,” not zero traffic.
- Apply visit floors before calculating growth rates.
- Exclude known payment-platform domains from opportunity reports.
- Aggregate category conclusions from all returned sources and keep category traffic separate from revenue estimates.
- Deduplicate new-product conclusions by `source_domain` across selected payment targets while retaining the contributing target list.
- Use every positive `position` change as the primary growth signal without a visit floor; do not confuse `position` with `global_rank`.
- Include sources newly present in the complete current table in `new_product_growth` regardless of visit floor.
- Compute `domain_age_days` against the final day of the report's current month.
- Treat RDAP registration time as supporting evidence, not company or launch-date proof.
- Use payment-referral position changes as the discovery signal and recent total-site visit direction as a separate confirmation or contradiction signal.
- Calculate website trends from available points only; surface missing months and refuse to silently fill them with zero.
