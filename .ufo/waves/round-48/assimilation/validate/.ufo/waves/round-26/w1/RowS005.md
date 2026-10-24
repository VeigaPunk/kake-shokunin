# Row S005 — freshness recheck (round 26)

```json
{"id":"S005","verdict":"HOLD","fetchIndex":1,"quote":"If you are publishing from a custom GitHub Actions workflow, no CNAME file is created","anchorObserved":"Configuring an apex domain, ordered step 4 (\"Under \\\"Custom domain\\\", type your custom domain, then click Save.\"), and Configuring a subdomain step 4 — the Actions sentence sits inside both step-4 list items","reason":"Re-fetched 2026-10-21 (HTTP 200, sha256 dc89eecdf00c22581f1d85dd5c429d63e3d206f7d7a946c3c2f752a023e0cee9) still states that a workflow-published site creates no CNAME file and ignores any existing one, at both step-4 anchors, so the row's teaches/scope are intact; no version pin, living doc with no observed drift at the anchor","correction":null}
```

## Caveats

1. Living docs (not commit/tag-pinned): verdict rests on today's HEAD bytes, not a historical diff; response had no `Last-Modified`/`ETag`, footer says © 2026.
2. Integrity: `S005-1.raw.gz` decompresses to 240439 bytes whose sha256 equals `manifest.json`'s `dc89ee…cee9`; status 200, fetchedAt 2026-10-21T15:09:34Z.
3. Anchor confirmed structurally in preserved HTML: each section's `<ol>` has step 4 = custom-domain entry, with the Actions sentence appended in the same `<li>`; the ignored-CNAME sentence occurs exactly twice (once per section).
4. The row's "or the API" half is not stated on this page (zero `API` occurrences in the article body); it is carried by S003/S007 and the knowledge entry, not by S005 — pre-existing cell composition, not content drift, so no correction was appended.
5. Step 3's sidebar label now reads "Code, planning, and automation"; it does not move or alter the step-4 anchor.
6. Cadence 90d: prior fetch 2026-10-19, this recheck 2026-10-21, next due 2027-01-17.
7. No tools installed or upgraded.
