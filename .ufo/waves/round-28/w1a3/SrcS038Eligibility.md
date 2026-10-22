# SrcS038Eligibility — CrUX methodology: origin/page eligibility

Round 28 (attempt 3), wave 1a3. Seat: KakeR28a3.SrcS038Eligibility (leaf, freshness axis).
Target: open S038 https://developer.chrome.com/docs/crux/methodology and extract eligibility facts only.

## Fetch record
- Command: `curl -sS -o crux-methodology.html -w "HTTP_STATUS=%{http_code} TIME=%{time_total} SIZE=%{size_download}\n" -L https://developer.chrome.com/docs/crux/methodology`
- Exit code: 0. Response: `HTTP_STATUS=200 TIME=1.024785 SIZE=109250`
- Access time (UTC): 2026-10-22T09:29:04Z
- Fetched bytes kept at `/fast/scratch/hyaku/kake-r28a3/w1/SrcS038Eligibility/crux-methodology.html`, SHA-256 `40319e543a04c7b69ff5c52e36910a15f5d58aa6a44d6764f53c72eb118f14ac`
- No installs performed (curl already present; operator directive N/A).
- Page's own last-updated date: **Last updated 2024-06-20 UTC** (shown in the License footer section; bytes `2024-06-20` present in raw HTML).

## Verification method (all quotes)
Each quote below was re-checked against the fetched bytes: the HTML was entity-decoded, tags removed, whitespace collapsed, and each quote was required to occur as an exact substring. All 8 pass (`in_stripped=True`). Quotes are ≤25 words.

## Knowledge statements (page-said only)
| # | Plain-English (kake knowledge) | Verbatim quote | Anchor (section heading) |
|---|---|---|---|
| 1 | A page must be publicly discoverable even to be considered for the CrUX dataset. | "A page must be publicly discoverable to be considered for inclusion in the CrUX dataset." (15) | Publicly discoverable |
| 2 | Discoverability reuses the same indexability criteria search engines use. | "A page is determined to be publicly discoverable using the same indexability criteria as search engines." (16) | Publicly discoverable |
| 3 | A page served with an HTTP status other than 200 after redirects fails discoverability. | "The page is served with an HTTP status code other than 200 (after redirects)." (14) | Publicly discoverable |
| 4 | A page served with an X-Robots-Tag: noindex header (or equivalent) fails discoverability. | "The page is served with an HTTP X-Robots-Tag: noindex header or equivalent." (12) | Publicly discoverable |
| 5 | A page is "sufficiently popular" only if it reaches a minimum number of visitors (threshold same for pages and origins; exact number never disclosed). | "A page is determined to be sufficiently popular if it has a minimum number of visitors." (16) | Sufficiently popular |
| 6 | Pages/origins below the popularity threshold are excluded entirely from the dataset. | "Pages and origins that don't meet the popularity threshold are not included in the CrUX dataset." (16) | Sufficiently popular |
| 7 | Experiences meeting the User and Origin criteria but not the Page criteria are excluded even from origin-level data in every CrUX data source. | "Experiences which meet the User and Origin criteria but not Page aren't included in the origin-level data available in all CrUX data sources." (23) | Eligibility |
| 8 | If a page is discoverable for some users but returns a non-success HTTP status in some circumstances, those experiences are excluded. | "If page is publicly discoverable for some users, but returns a non-success HTTP status in some circumstances, then those experiences won't be included in CrUX." (25) | Page |

## Proposed registry row (contract shape)
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S038 | Chrome for Developers: CrUX methodology — https://developer.chrome.com/docs/crux/methodology | docs | A | Conditions for an origin and a page (URL) to appear in CrUX and what happens when a page does not qualify; not user-segment details (see S038 population seat) | Eligibility (h2); Publicly discoverable; Sufficiently popular; Page | A page must be publicly discoverable (same indexability criteria as search engines); disqualified by non-200 status after redirects or X-Robots-Tag: noindex; popularity = minimum visitor threshold, exact number not disclosed, same for pages and origins; below-threshold pages/origins excluded; experiences meeting User+Origin but not Page are excluded even from origin-level data; experiences with non-success HTTP status on some loads are excluded | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |

## Related facts the page also states (context, not numbered statements)
- Pages/origins are included/removed automatically as eligibility changes; manual submission is not possible ("Pages and origins are automatically included or removed from the dataset if their eligibility changes over time. At this time, you cannot manually submit pages or origins for inclusion." — Eligibility).
- If an origin is publicly discoverable, eligible experiences across all its pages aggregate at origin level regardless of individual page discoverability, and all count toward the origin's popularity (Origin).
- URL query parameters and fragments are stripped before aggregation, so URL variations share one page's popularity pool (Page).
- Experiences are attributed to the top-level page only; iframes are not reported separately (Page).
- AMP pages are included like any other page; AMP Cache/Viewer-served pages counted since June 2020 CrUX release (AMP).
- Ad metrics require ≥1 authorized seller in ads.txt (Ad metrics).

## Not found (page does not say; not filled from memory/other sites)
- The exact minimum visitor number for the popularity threshold (page explicitly says it is not disclosed).
- Any specific numeric popularity threshold, country/global threshold values, or the proportion of users meeting the user criteria.
- Details of what makes an origin "publicly discoverable" beyond the listed 200/noindex conditions (Lighthouse check pointer is given, not a definition).
- Any CrUX API/PageSpeed access specifics — network bound forbids fetch of other pages (S039 seat covers API).

## Out-of-scope per bounds
- No pages other than S038 fetched; no API calls; no key/account/browser. No lane-repo mutation; only this report written in repo. No subagents spawned.
