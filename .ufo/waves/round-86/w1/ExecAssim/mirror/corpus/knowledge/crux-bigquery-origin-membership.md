source: S438 — https://developer.chrome.com/docs/crux/bigquery — § CrUX on BigQuery → Materialized table schema → origin_summary (doc prints "Last updated 2026-10-13 UTC"; retained body sha256 dd17ea8cb30ec89af9eb6cbb16fcb0de3d04eb33143a3aa8ac19c9da6d5db420, 110697 bytes, fetched 2026-11-03)
verified-at: 2026-11-03
recheck: 180d
ground: field performance (Core Web Vitals, CrUX eligibility) — the documented route that answers origin membership without a CrUX API key

# Where origin membership in the CrUX dataset is published

The lane's CrUX question — whether a named origin is in the Chrome UX Report dataset — is
blocked by credentials, not by ignorance: the CrUX API needs a Google Cloud API key the lane does
not hold (S039), and the campaign session's key-free probes were its own-work observations
(staged S303/S304 rows) that this lane neither holds as registry rows nor re-ran this round. The
dataset's own documentation names a third route, and this entry records it.

The raw data behind CrUX is published on BigQuery, and the origin list is a first-class table.
The documentation's schema list describes the `origin_summary` table in one line:

> a list of all origins included in the dataset

The same schema section states the refresh cadence:

> it is updated monthly with the latest list of origins in the dataset

Each release is a new table under the `chrome-ux-report.all` dataset, alongside monthly summary
tables that carry the metrics per origin, per device and per country. The cost is the part that
matters for the lane: the documentation's access section says the CrUX dataset on BigQuery is
free to access and explore up to the limits of the free tier, which is renewed monthly and
provided by BigQuery, and that using BigQuery requires a Google Cloud account and basic
knowledge of SQL — so the prerequisite is a Google Cloud project, not a CrUX API key.

That is the concrete difference between the blocked route and the open one. The CrUX API route
needs an API key (the lane's S039 records the key requirement and the quota); the BigQuery route
needs a Google Cloud project. Neither is a credential the lane holds, and secrets are `kagi`'s
custody — but the BigQuery route is the one that can answer the question for a specific origin
without the API's per-key identity, and it names the table to query.

Scope note: this entry records where the answer lives. No BigQuery query was run, no project was
used, and no field data was read for any origin, the lane's own included.

Cross-reference: the held r28 entry `field-performance-cwv.md` carries the thresholds, the
eligibility rules and the API's key requirement; what this entry adds over it is the one place
where membership in the dataset can be read without a key — the documented `origin_summary`
table. Adoption provenance: adopted from the shokuknow staging campaign's `merge/kake` package
(staged id S352, fetched there 2026-10-24) and re-grounded in-round on 2026-11-03; the retained
body, receipt and quote classes are this lane's own (`.ufo/waves/round-70/w1/ScoutSources/`).
