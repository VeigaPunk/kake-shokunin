# SrcS039Request — S039 CrUX API source opening (round 28, wave 1a3)

Seat: KakeR28a3.SrcS039Request (leaf scribe). Axis: freshness (field performance, C2). No subagents, no installs, no repo mutations. Only this report written inside the lane.

## Fetch evidence

- GET `https://developer.chrome.com/docs/crux/api` via `curl -sS -D <scratch>/s039.headers -o <scratch>/s039.html -w '%{http_code}'` → **status 200**, exit 0. UTC access time **2026-10-22T09:29:09Z**; server `Date: Thu, 22 Oct 2026 09:29:09 GMT`. Content-Type text/html.
- Saved bytes: `~fast/scratch/hyaku/kake-r28a3/w1/SrcS039Request/s039.html` (167,991 bytes, 4338 lines), sha256 `f992ba82e5da4e8fe8dc5c435f139fe3eba4583469b64bd4f00c660fb932abbb`.
- Page's own last-updated line: `Last updated 2026-10-13 UTC.` (raw line 3885).
- Quote verification method: each quote re-checked by exact-substring grep against the saved raw bytes; line numbers below are from that file. Quotes S1 and S6 are contiguous in the rendered text but wrap a code token in the raw HTML (noted per row).

## Statements (plain-English / verbatim quote / anchor)

| # | (a) knowledge statement | (b) quote (words) | (c) anchor | raw line |
|---|---|---|---|---|
| S1 | The CrUX API has one endpoint, and records are fetched with an HTTP POST (JSON body, key query param). | "There is a single endpoint for the CrUX API which accepts POST HTTP requests." (14) | Schema | 3479 (raw wraps `POST` in `<code>`) |
| S2 | Querying by `origin` aggregates the data of every page under that origin into one record. | "When the identifier is an origin all data present for all pages in that origin are aggregated together." (18) | Data model → Origin | 3037 |
| S3 | Querying by `url` returns data for that specific page only. | "When the identifier is a URL, only data for that specific URL will be returned." (14) | Data model → URLs | 3046 |
| S4 | A record lookup is keyed by exactly one URL pattern — either origin or url (union field `url_pattern`). | "The URL pattern is the URL that the record applies to." (12) | Schema → Key | 3653 |
| S5 | `formFactor` is the device class of the end-user's navigation. | "The device class that the end-user used to navigate to the page." (13) | Data model → Form Factor | 3059 |
| S6 | `formFactor` takes one of `DESKTOP`, `PHONE`, `TABLET`; omitting it returns a record aggregated across all form factors. | "This field uses the values DESKTOP, PHONE, or TABLET." (11) | Schema → Request body | 3517–3518 (raw wraps values in `<code>`) |
| S7 | If `metrics` is omitted, every available metric found is returned (page lists the allowed metric names). | "If none are specified then any metrics found will be returned." (12) | Schema → Request body | 3526 |
| S8 | The page documents **no** error response for keys with no data: grep `(?i)404|NOT_FOUND|\berror\b` over the saved bytes → no matches. The only failure-adjacent mechanism documented is URL normalization, which is applied to raise lookup success, not as a no-data error. | "Object representing the normalization actions taken to normalize a URL to achieve a higher chance of successful lookup." (19) | Schema → UrlNormalization | 3825 |

## Proposed S039 registry row (contract shape)

`| S039 | Chrome for Developers: CrUX API — https://developer.chrome.com/docs/crux/api | docs | A | CrUX API request shape and response fields: origin vs url key, formFactor values, metrics selection; no no-data error documented on this page | Data model (Origin, URLs, Form Factor), Schema (Request body, Key, UrlNormalization), Example queries; last updated 2026-10-13 UTC | The API accepts one POST JSON body keyed by origin or url (union url_pattern), optionally filtered by formFactor (DESKTOP/PHONE/TABLET) and metrics; omitting metrics returns all available metrics; the page documents no 404/NOT_FOUND no-data error | mined | 2026-10-22 | 90d | corpus/knowledge/field-performance-cwv.md |`

Matches c2_source_count.py expectations: source cell contains the declared URL, tier A, status mined, opened 2026-10-22, used-by includes `corpus/knowledge/field-performance-cwv.md`; no `|` inside cells.

## Not found / limits

- HTTP 404 / `NOT_FOUND` / any error response for a key with no data: **not found on this page** (grep above). The no-data error contract must come from another source or be stated as open.
- No API-key acquisition details beyond "requires a Google Cloud API key provisioned for Chrome UX Report API usage" (CrUX API Key section).
- **Not verified by me:** the counter run, the L1-drafted knowledge entry, and the round-28 lesson Gate line (entry and Gate are L1's pieces; my quotes above are 1–25 words and fit the Gate's curly-quote requirement).

## Tooling record

No installs or updates made (per operator rule, none expected; all tools pre-existing: curl, grep/read, python3 unused). Scratch confined to `/fast/scratch/hyaku/kake-r28a3/w1/SrcS039Request/`.
