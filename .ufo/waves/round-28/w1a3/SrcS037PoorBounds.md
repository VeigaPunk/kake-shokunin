# SrcS037PoorBounds — S037 source opening (wave 1a3)

Seat: `KakeR28a3.SrcS037PoorBounds` (leaf scribe). Source: S037 — https://web.dev/articles/defining-core-web-vitals-thresholds

## Access record (GET, own fetch)
- Command: `curl -sS -o body.html -D headers.txt -w 'HTTP_CODE=…' https://web.dev/articles/defining-core-web-vitals-thresholds`; exit 0.
- Observed: HTTP 200; `URL_FINAL` = requested URL (no redirect); response time 0.80 s; bytes 149,322.
- UTC access time: **2026-10-22T09:29:05Z**. Response `last-modified: Wed, 07 May 2025 07:00:00 GMT`.
- Scratch: `/fast/scratch/hyaku/kake-r28a3/w1/SrcS037PoorBounds/` (`body.html` sha256 `c0ea35cff777…e6f994`, `headers.txt`, `body_norm.txt`, `body_text.txt`). A sibling fetch is recorded in `.ufo/waves/round-28/sources/receipts.json` (S037: 2026-10-22T08:30:35Z, 200, 149,322 B, sha256 `6c738f2e…`); byte hash differs because the page embeds a per-response CSP nonce — content rendered is identical for the quoted regions.

## Last-updated date (shown on page)
- Footer: "Last updated 2025-05-07 UTC." (body.html:4619). Also `dateModified: "2025-05-07"` in JSON-LD (body.html:85) and byline "Published: May 21, 2020, Last updated: May 7, 2025" (body.html:4034).

## Statements (8)
Quote check: each quote re-checked against my fetched bytes — whitespace-collapsed (`body_norm.txt`) and tag-stripped (`body_text.txt`) forms; `grep -F` matches exactly once each. HTML source encodes `"` as `&quot;`; rendered as `"` here. Word counts ≤ 25.

1. **(a)** LCP "poor" upper threshold is 4 seconds (LCP "good" is 2.5 s). **(b)** "For a 4 second threshold, roughly 26% of phone origins, and 21% of desktop origins, would be classified as poor." (20 words) **(c)** "Largest Contentful Paint" → "Achievability".
2. **(a)** The LCP good threshold was chosen for achievability: 2.5 s is consistently achievable at the 75th percentile for top-performing sites, while 1.5 s and 2 s are not. **(b)** "We find that the 1.5 and 2 second thresholds are not consistently achievable, while 2.5 seconds is consistently achievable." (19 words) **(c)** "Largest Contentful Paint" → "Achievability".
3. **(a)** INP "poor" upper threshold is 500 ms (INP "good" is 200 ms); a 300 ms poor threshold would misclassify popular sites, so 500 ms was chosen to stay inside the 10–30% achievability band. **(b)** "and greater than 500 ms is a reasonable "poor" threshold." (10 words) **(c)** "Interaction to Next Paint" → "Achievability".
4. **(a)** INP 200 ms good threshold is achievable: the majority of origins meet it at the 75th percentile. **(b)** "Using data from CrUX, we determine that the majority of origins on the web meet the 200 ms INP "good" threshold at the 75th percentile" (25 words) **(c)** "Interaction to Next Paint" → "Achievability".
5. **(a)** CLS "poor" upper threshold is 0.25 (CLS "good" is 0.1). **(b)** "For a 0.25 threshold, roughly 20% of phone origins, and 18% of desktop origins, would be classified as "poor"." (21 words) **(c)** "Cumulative Layout Shift" → "Achievability".
6. **(a)** CLS 0.1 good threshold was chosen as the balance between quality of experience and achievability (0.05 is achievable by many but too stringent for embeds). **(b)** "the slightly less stringent CLS threshold of 0.1 strikes a better balance between quality of experience and achievability." (19 words) **(c)** "Cumulative Layout Shift" → "Achievability".
7. **(a)** General criterion, good thresholds: a candidate good threshold is achievable only if at least 10% of CrUX origins meet it, and well-optimized sites consistently meet it. **(b)** "To confirm that a threshold is achievable, we require that at least 10% of origins meet the "good" threshold." (20 words) **(c)** "Criteria for the Core Web Vitals metric thresholds" → "Achievable by existing web content".
8. **(a)** General criterion, poor thresholds: unless research dictates otherwise, the default poor threshold is the level classifying the worst-performing 10–30% of origins as poor. **(b)** "Unless there is research available relevant to defining a "poor" threshold, by default the worst-performing 10-30% of origins are classified as "poor"." (22 words) **(c)** "Criteria for the Core Web Vitals metric thresholds" → "Achievable by existing web content".

## Proposed S037 registry row (contract shape)
`| S037 | web.dev: How the Core Web Vitals metrics thresholds were defined — https://web.dev/articles/defining-core-web-vitals-thresholds | docs | A | Core Web Vitals good/poor thresholds for LCP, INP and CLS, and the quality/achievability criteria used to choose them | Thresholds figure and per-metric "Quality of experience" and "Achievability" sections under "Criteria for the Core Web Vitals metric thresholds"; last updated 2025-05-07 UTC | Good/poor thresholds: LCP 2.5 s/4 s, INP 200 ms/500 ms, CLS 0.1/0.25, each at the 75th percentile; a good threshold needs ≥10% of origins meeting it and consistent achievability, and a poor threshold defaults to the worst-performing 10–30% of origins unless research says otherwise | mined | 2026-10-22 | 90d | corpus/knowledge/field-performance-cwv.md |`
- Notes: `kind`=docs (matches web.dev/Google docs rows S003/S013/S021); `tier` A; `status` mined; `opened` 2026-10-22; `used-by` exactly the C2 entry path. `recheck` 90d reflects a living web.dev doc; 365d is defensible if the L1 prefers a slower cadence for this methodology page.

## Not found (page does not say)
- No desktop-specific thresholds: the page explicitly uses the same thresholds for mobile and desktop (body.html:4172).
- No dates for future threshold revisions — only "in future years we anticipate making improvements and additions" (body.html:4113).
- No CrUX field-eligibility definition (that is S038's scope), and no API usage.
- No statement that a site is globally "poor" for any single threshold; classification is per metric at the 75th percentile.

## Tooling
No installs or upgrades performed (curl, grep, sed already present; no pacman/uv/npx usage). No lane file mutated; only this report written inside the fleet repo.
