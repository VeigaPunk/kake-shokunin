# SrcS039Limits — CrUX API (S039) source opening report

Round 28 w1a3, leaf seat KakeR28a3.SrcS039Limits. Freshness axis.

## Fetch
- Command: `mkdir -p /fast/scratch/hyaku/kake-r28a3/w1/SrcS039Limits && cd ... && TZ=UTC date -u '+%Y-%m-%d %H:%M:%S UTC' > access_time.txt && curl -sS -L -D headers.txt -o crux-api.html -w 'http_code=%{http_code}\nurl=%{url_effective}\n' https://developer.chrome.com/docs/crux/api > curl_status.txt` — exit 0.
- Output: `http_code=200`, effective URL `https://developer.chrome.com/docs/crux/api`, 167,991 bytes.
- Access time (recorded): 2026-10-22 09:29:05 UTC.
- HTTP headers: `last-modified: Tue, 13 Oct 2026 07:00:00 GMT`; `date: Thu, 22 Oct 2026 09:29:06 GMT`.
- Fetched bytes: `/fast/scratch/hyaku/kake-r28a3/w1/SrcS039Limits/crux-api.html`, SHA-256 `e2462517c6dd179ba36ae9872667fc1510e72f644217fe1ecd93e130b73f8b42`. All quotes below were re-checked by exact substring match against the normalized text of these bytes (Python check: all 10 candidates `OK`, none MISS).
- Page's own last-updated date: footer "Last updated 2026-10-13 UTC" and JSON-LD `dateModified: "2026-10-13"` (matches HTTP last-modified).

## Statements (plain-English knowledge, verbatim quote ≤25 words, anchor)
1. The CrUX API requires a Google Cloud API key provisioned for "Chrome UX Report API" usage.
   Quote: "Using the CrUX API requires a Google Cloud API key provisioned for Chrome UX Report API usage."
   Anchor: CrUX API Key (crux-api.html:2938,2940).
2. The API is limited to 150 queries per minute per Google Cloud project, offered without charge; the quota cannot be increased by paying (quote covers the limit; the "not possible to pay" clause is in the same paragraph).
   Quote: "The CrUX API is limited to 150 queries per minute per Google Cloud project, which is offered without charge."
   Anchor: Rate limits (crux-api.html:3859,3861).
3. The data is a 28-day rolling average: at any time the report shows the past 28 days aggregated together.
   Quote: "The data in the Chrome UX Report is a 28-day rolling average of aggregated metrics."
   Anchor: The rolling average (crux-api.html:3467).
4. Data is updated daily around 04:00 UTC, and results do not change within the same day after that update (repeated calls yield the same results — caution aside, crux-api.html:3475).
   Quote: "Data is updated daily around 04:00 UTC."
   Anchor: Daily updates (crux-api.html:3473).
5. There is no service level agreement for update times; updates run on a best-effort basis every day.
   Quote: "There is no service level agreement for update times; it is run on a best-effort basis every day."
   Anchor: Daily updates (crux-api.html:3473).
6. Querying with an origin identifier aggregates data for all pages under that origin into origin-level data.
   Quote: "When the identifier is an origin all data present for all pages in that origin are aggregated together."
   Anchor: Origin (crux-api.html:3035,3037).
7. Querying with a URL identifier returns data for that specific URL only — no automatic fallback to the origin is described.
   Quote: "When the identifier is a URL, only data for that specific URL will be returned."
   Anchor: URLs (crux-api.html:3044,3046).
8. URL normalization applies only basic automated changes to improve lookup success; complex actions such as following redirects are not handled (and the page never mentions a fallback to origin — 0 occurrences of "fallback" in the bytes).
   Quote: "Object representing the normalization actions taken to normalize a URL to achieve a higher chance of successful lookup."
   Anchor: UrlNormalization (crux-api.html:3823,3825).

## Not found (page does not say)
- No fallback-to-origin behavior for failed URL lookups (term "fallback" absent from fetched bytes).
- No per-day quota, no other rate limits beyond the 150/min per-project limit; no cost tier other than "without charge".
- No caching/TTL semantics beyond the same-day stability caution (statement 4).

## Proposed registry rows (contract shape)
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S039.1 | https://developer.chrome.com/docs/crux/api | source-doc | primary | web properties | CrUX API Key | CrUX API requires a Google Cloud API key provisioned for Chrome UX Report API | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |
| S039.2 | https://developer.chrome.com/docs/crux/api | source-doc | primary | web properties | Rate limits | 150 queries/min per Google Cloud project, free, cannot pay to increase | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |
| S039.3 | https://developer.chrome.com/docs/crux/api | source-doc | primary | web properties | The rolling average | CrUX data is a 28-day rolling average of aggregated metrics | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |
| S039.4 | https://developer.chrome.com/docs/crux/api | source-doc | primary | web properties | Daily updates | Data updated daily around 04:00 UTC; stable within the same day | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |
| S039.5 | https://developer.chrome.com/docs/crux/api | source-doc | primary | web properties | Daily updates | No SLA for update times; best-effort daily | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |
| S039.6 | https://developer.chrome.com/docs/crux/api | source-doc | primary | web properties | Origin | Origin query aggregates all pages under that origin | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |
| S039.7 | https://developer.chrome.com/docs/crux/api | source-doc | primary | web properties | URLs | URL query returns only that URL's data; no fallback described | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |
| S039.8 | https://developer.chrome.com/docs/crux/api | source-doc | primary | web properties | UrlNormalization | Normalization is basic automated changes only; redirects not handled | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |

## Notes
- Tooling: no installs or upgrades performed; used existing `curl`, `grep`, `python3` (Channel: n/a per operator directive — nothing needed).
- Access log and raw bytes retained at /fast/scratch/hyaku/kake-r28a3/w1/SrcS039Limits/ (headers.txt, crux-api.html, curl_status.txt, access_time.txt).
- Not verified: behavior of the live API (no API calls permitted); anything beyond what this single page states.
