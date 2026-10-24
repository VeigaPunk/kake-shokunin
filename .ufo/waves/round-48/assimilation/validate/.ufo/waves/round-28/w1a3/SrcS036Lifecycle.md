# SrcS036Lifecycle — C2 source opening, S036 https://web.dev/articles/vitals

Seat: KakeR28a3.SrcS036Lifecycle (scribe, leaf). Report written per w1a3 spec.

## Fetch record
- Command: `TMPDIR=/fast/scratch/hyaku/kake-r28a3/w1/SrcS036Lifecycle date -u +%Y-%m-%dT%H:%M:%SZ && curl -sS -o vitals.html -D vitals.headers -w 'HTTP %{http_code} total %{time_total}s' https://web.dev/articles/vitals; echo " curl_exit=$?"`
- UTC access time: 2026-10-22T09:29:06Z (date before curl). HTTP status: 200. Total: 1.526755s. Exit: 0.
- Headers: HTTP/2 200; last-modified: Thu, 31 Oct 2024 07:00:00 GMT; content-type text/html; charset=utf-8; content-length 143746; server Google Frontend.
- Bytes fetched: 143746 (`wc -c`), identical size to the shared S036 receipt (.ufo/waves/round-28/sources/receipts.json, accessed 2026-10-22T08:30:34Z, sha256 cbbfb174bfc220ab3c0fa2a2ebb611d594bb5d95950c6cc57e342d32c5d8b838). This seat re-opened the URL itself as assigned.
- Scratch: /fast/scratch/hyaku/kake-r28a3/w1/SrcS036Lifecycle/{vitals.html, vitals.headers}. No tools installed (none needed; tooling directive complied, no chain used).

## Page metadata
- Page title: "Web Vitals | Articles | web.dev"; description "Essential metrics for a healthy site".
- Page's own last-updated: "Published: May 4, 2020, Last updated: October 31, 2024" (vitals.html:4006); footer "Last updated 2024-10-31 UTC." (vitals.html:4297). HTTP Last-Modified header agrees (2024-10-31 07:00:00 GMT).

## Statements (8). Quote check: each quote reappears verbatim in the fetched bytes' visible text — HTML minus tags/script/style, standard entities unescaped, whitespace preserved (same method receipts.json documents). Verified by script on vitals.html: every quote `in text` = True; word counts ≤ 25. Q3/Q7/Q8/Q9 additionally matched raw byte substrings with no tag breaks; Q1/Q2/Q4/Q5/Q6 contain inline tags (<em>/<strong>/<a>) so raw bytes break the phrase and the visible-text check is the applicable one.

1. (a) The current stable Core Web Vitals set is LCP (loading), INP (interactivity), CLS (visual stability); the lifecycle bullet list marks each "Stable" (vitals.html:4078-4080). (b) "The current set focuses on three aspects of the user experience—loading, interactivity, and visual stability—and includes the following metrics (and their respective thresholds):" (23w) (c) Anchor: Core Web Vitals (h2 #core-web-vitals), vitals.html:4026.
2. (a) "Stable" is the lifecycle phase holding the current set Chrome considers essential. (b) "Stable metrics are the current set of Core Web Vitals that Chrome considers essential for great user experiences." (18w) (c) Anchor: Lifecycle (h3 #lifecycle), vitals.html:4072.
3. (a) INP was promoted from experimental to pending in 2023, with the stated intent to eventually retire FID. (b) "INP was promoted in 2023 from experimental to pending status with the intent to eventually retire FID." (17w) (c) Anchor: Lifecycle > Pending (h4 #pending), vitals.html:4093.
4. (a) FID was retired and replaced when INP became a stable Core Web Vital metric in 2024 (page names no narrower date). (b) "This is exactly what happened to FID as INP became a stable Core Web Vital metric in 2024." (18w) (c) Anchor: Lifecycle, Key point aside, vitals.html:4104.
5. (a) Field tools named: Chrome User Experience Report collects anonymized real-user data for each Core Web Vital and powers Chrome DevTools, PageSpeed Insights, and Search Console's Core Web Vitals report; the field table shows all four cover LCP/INP/CLS (vitals.html:4124-4150). (b) "The Chrome User Experience Report collects anonymized, real user measurement data for each Core Web Vital." (16w) (c) Anchor: Field tools to measure Core Web Vitals (h4 #field_tools_to_measure_core_web_vitals), vitals.html:4113. Secondary quote: "and powers tools like Chrome DevTools, PageSpeed Insights, and Search Console's Core Web Vitals report." (15w), same paragraph.
6. (a) All Core Web Vitals are first and foremost field metrics; many are also measurable in the lab. (b) "While all of the Core Web Vitals are, first and foremost, field metrics, many of them are also measurable in the lab." (22w) (c) Anchor: Lab tools to measure Core Web Vitals (h4 #lab_tools_to_measure_core_web_vitals), vitals.html:4200.
7. (a) Lab tools named: Chrome DevTools (LCP/INP/CLS), Lighthouse (LCP/CLS; cannot measure INP because there is no user input in a simulated environment; use TBT as a lab proxy for INP) (table vitals.html:4218-4230). (b) "Tools like Lighthouse that load pages in a simulated environment without a user cannot measure INP, as there is no user input." (22w) (c) Anchor: Lab tools to measure Core Web Vitals, Note aside, vitals.html:4236.
8. (a) Lab measurement is not a substitute for field measurement; only field measurement captures the complete picture. (b) "While lab measurement is an essential part of delivering great experiences, it is not a substitute for field measurement." (19w) (c) Anchor: Lab tools to measure Core Web Vitals, vitals.html:4239. Corroborating: "Only field measurement can accurately capture the complete picture." (9w), vitals.html:4241.

## Not found on this page (do not fill from memory/other sites)
- No narrower date than "2024" for INP becoming stable / FID retirement; no exact FID retirement date.
- No CrUX API or PageSpeed API details, no CrUX eligibility criteria, no API keys/accounts (links to developer.chrome.com/docs/crux and PageSpeed Insights exist; those are S038/S039 territory).
- No definition of the "experimental"/"pending" durations except pending ≥ six months (vitals.html:4095).

## Proposed registry row (contract shape; kind/tier conventions from sibling rows S038 "docs"/"A" and S039 "source-doc"/"primary" — L1 can normalize)
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S036 | https://web.dev/articles/vitals | docs | primary | Metric lifecycle and tooling: which metrics are stable Core Web Vitals, how INP replaced FID, and which tools measure field vs lab; thresholds are S037's scope | Core Web Vitals (h2) > Lifecycle (h3, incl. Pending h4 and Key point aside); Field tools / Lab tools h4 sections; page last updated 2024-10-31 UTC | Stable Core Web Vitals are LCP, INP, CLS; lifecycle phases experimental/pending/stable; INP promoted in 2023 with intent to retire FID, and FID was retired when INP became a stable Core Web Vital metric in 2024; field tools: CrUX, Chrome DevTools, PageSpeed Insights, Search Console CWV report; lab tools: Chrome DevTools, Lighthouse (cannot measure INP; TBT proxy) | mined | 2026-10-22 |  | corpus/knowledge/field-performance-cwv.md |

## Limits
- Not verified: nothing on this page was cross-checked against any other page; statements are solely from the fetched bytes of S036.
- The L1's drafted entry (corpus/knowledge/field-performance-cwv.md) is theirs to write; this report is advisory input only.
