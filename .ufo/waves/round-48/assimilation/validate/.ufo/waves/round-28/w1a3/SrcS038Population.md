# SrcS038Population — CrUX methodology page: population and segmentation

Role: KakeR28a3.SrcS038Population (scribe leaf, round 28 wave 1a3). No subagents spawned; no fleet-repo, lane jj, or Git state touched. The only file written in the lane repo is this report.

## Access evidence

- URL: https://developer.chrome.com/docs/crux/methodology (named public URL assigned to this seat; GET only).
- First open via `read` (native method, Content-Type text/html) at 2026-10-22T09:29:05Z UTC.
- Raw GET stored for recheck: `curl -sS -o page.html -w 'HTTP_STATUS:%{http_code}\n' https://developer.chrome.com/docs/crux/methodology` → exit 0, `HTTP_STATUS:200`, 109246 bytes.
- Fetched bytes retained at /fast/scratch/hyaku/kake-r28a3/w1/SrcS038Population/page.html, sha256 06e52fefe81c28996a239c7d2e31d5726f0bb58d3ef75b4c1fa3289c7c95bfdb.
- Page's own last-updated line: "Last updated 2024-06-20 UTC." (present verbatim in fetched bytes).

## Statements (each quote re-checked verbatim against fetched bytes)

Recheck method: stripped tags/scripts from the saved 109246-byte HTML, decoded entities, normalized whitespace, then tested each quote as an exact substring. All 7 quotes matched (found=YES). Manual word counts all ≤ 25.

1. (a) CrUX aggregates individual user experiences into two distribution shapes: page-level and origin-level.
   (b) "individual user experiences, which are aggregated into page-level and origin-level distributions." (11 words)
   (c) Anchor: intro paragraph directly under main heading "CrUX methodology" (above ## Eligibility).
2. (a) A user's experiences enter CrUX only if all four criteria hold: usage-statistics reporting enabled, browser history synced, no Sync passphrase set, supported platform used.
   (b) "For a user to have their experiences aggregated in the CrUX dataset, they must meet the following criteria:" (18 words)
   (c) Anchor: Eligibility > User.
3. (a) Contributing clients are desktop Chrome (Windows, macOS, ChromeOS, Linux) and Android Chrome, including Custom Tabs and WebAPKs.
   (b) "Desktop versions of Chrome including Windows, macOS, ChromeOS, and Linux operating systems." (12 words)
   (c) Anchor: Eligibility > User.
4. (a) Chrome on iOS, Android apps using WebView, and other Chromium browsers (e.g. Microsoft Edge) do not provide data to CrUX.
   (b) "There are a few notable exceptions that don't provide data to the CrUX dataset:" (14 words)
   (c) Anchor: Eligibility > User.
5. (a) The page does not publish proportions of users that meet the eligibility criteria.
   (b) "Chrome does not publish data about the proportions of users that meet these criteria." (14 words)
   (c) Anchor: Eligibility > User.
6. (a) Beyond eligibility, origins/pages with more than 20% of total traffic excluded due to ineligible combinations of dimensions are dropped from the dataset entirely.
   (b) "Origins or pages having more than 20% of their total traffic excluded due to ineligible combinations of dimensions are excluded entirely from the dataset." (24 words)
   (c) Anchor: Data quality > Filtering.
7. (a) Segmentation named by the methodology: dimensions; segments; country level vs global level — dimension combinations that fail popularity at country level may still be included at global level if globally popular.
   (b) "combinations of dimensions that don't meet the popularity criteria at the country level may still be included at the global level" (21 words)
   (c) Anchor: Data quality > Filtering.

## Not found on this page (not filled from memory or other sites)

- Collection window: the page states no aggregation/collection window (no "28-day" or window text; no such section).
- Form factor: the term "form factor" does not appear; the page names client platforms only (desktop vs Android, statements 3-4).
- Exact popularity threshold: "An exact number is not disclosed" (Eligibility > Sufficiently popular).
- No PageSpeed Insights / CrUX API calls, API keys, accounts, browser profiles, live property probes, or other-site fetches were used.

## Proposed registry row (contract shape)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S038 | Chrome for Developers: CrUX methodology — https://developer.chrome.com/docs/crux/methodology | docs | A | Which users and Chrome clients contribute CrUX data and how the dataset segments experiences; not metric definitions (S036/S037) | Eligibility > User; Data quality > Filtering; intro page/origin-level paragraph; last updated 2024-06-20 UTC | Individual experiences aggregate into page-level and origin-level distributions; a user contributes only with usage-statistics reporting, history sync, no Sync passphrase, and a supported platform (desktop Chrome Windows/macOS/ChromeOS/Linux; Android Chrome incl. Custom Tabs and WebAPKs); Chrome on iOS, Android WebView, and other Chromium browsers do not contribute; no user-proportion data is published; >20% ineligible-dimension traffic exclusion drops a page/origin; country-ineligible dimension combos may still appear globally if globally popular | mined | 2026-10-22 | 90d | corpus/knowledge/field-performance-cwv.md |

## Tooling

No installs or updates performed; read /home/vgpnk/.omp/agent/RULES.md (operator tooling directive) — no tool need arose. Curl used was the system binary.

## Out of scope / not verified

Did not verify the metrics definitions, thresholds, or API behavior (other seats: S036, S037, S039). Did not assess page-live changes after the recorded GET; HTTP 200 is the response status at access time. Report is advisory input to L1 and the non-author closure; no verdict or admission is issued here.
