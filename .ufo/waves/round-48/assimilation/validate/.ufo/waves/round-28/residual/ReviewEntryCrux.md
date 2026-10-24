# ReviewEntryCrux: S038/S039 statements and SKILL.md round-28 triage rows

Reviewer: KakeR28a3.ReviewEntryCrux (leaf, read-only; findings are advisory). Lane HEAD 8ecbefe. Entry (corpus/knowledge/field-performance-cwv.md, blob 677b960) and SKILL.md (blob 7df5219) are identical at e57f601 and HEAD; the only commit after e57f601 is 8ecbefe (C1 script). Entry line numbers below refer to that file.
Method: one GET each of developer.chrome.com/docs/crux/methodology (HTTP 200, 109,246 B) and /docs/crux/api (HTTP 200, 167,991 B). Both "Last updated" dates match the retained S038 (2024-06-20) and S039 (2026-10-13). Retained S038.txt (11,819 chars) and S039.txt (23,914 chars) were split into sentences ("sN" below = sentence N of that split). "LN" = line N of the live GET text in /fast/scratch/hyaku/kake-r28a3/res/ReviewEntryCrux/ (methodology.txt, api.txt).
Every cited sentence appears in both retained and live text (link markup splits some; checked by hand). Keyword sweep for fall back, fallback, 404, not found, no data, no record and error: 0 hits in all four texts.

## S038 statements: ID | entry lines | statement | source located | verdict
A1 | 65-66 | Page must be publicly discoverable, judged by search-engine indexability | s14-15; L139-144 | OK
A2 | 66-67 | Fails if final status is not 200 after redirects | s16; L147-149 | OK
A3 | 66-68 | Fails on X-Robots-Tag noindex or meta noindex | s17-18; L150-155 | Understated: "or equivalent" dropped twice (F7)
A4 | 70-72 | Sufficiently popular; minimum undisclosed; same for pages and origins | s20-23; L158-164 | OK
A5 | 73-76 | Origin: experiences on all pages count regardless of page discoverability | s28-29; L179-182 | Quoted correctly; conflicts with s11 (L133-135), unflagged (F4)
A6 | 76 | Origins in the dataset are lowercase | s30; L183 | OK; "for querying purposes" dropped (F11)
A7 | 77-78 | Query strings and fragments stripped; URL variants aggregate | s34-35; L196 | OK; rare regrouping of distinct pages dropped (F11)
A8 | 79-80 | More than 20% of traffic in ineligible combinations: excluded entirely | s67; L219-222 | OK
A9 | 81-82 | Pages cannot be submitted manually; inclusion follows eligibility | s12-13; L136-138 | Overstated: source says "At this time" (F7)
A10 | 107-108 | Exclusion conditions are "not a complete test" | s15 ("same indexability criteria as search engines") | Inference; must be labelled [INFERENCE] (F10)
A11 | 108 | A raw 200 is not proof of a served page (cites SKILL.md) | s33; L195 | OK in substance; cite s33, not SKILL.md 65-66 (F10)
A12 | 108-110 | If no exclusion applies, low traffic is the likely cause | s48-56 user and platform rules; L199-211 | Overstated: user and platform causes omitted (F1)
A13 | 7-14 (Claim) | Only discoverable, popular pages and origins hold data, so low traffic or noindex can mean none | s8-13, s20-24, s48-56 | Incomplete: user and platform rules also gate data (F1)

## S039 statements: ID | entry lines | statement | source located | verdict
B1 | 86-88 | One POST endpoint; origin or url key; optional formFactor and metrics | s62-69; L435-460 | OK; omitted formFactor means all form factors (F9)
B2 | 88-89 | A url query returns data for that URL only | s22-23; L151 | OK
B3 | 90-91 | 28-day rolling average; updated daily around 04:00 UTC, best effort | s56, s59-60; L429-432 | OK; "approximately two days behind" omitted (F2)
B4 | 91-92 | Repeated calls on one day return the same result | s61; L433 | Overstated: holds only after the daily update (F3)
B5 | 93-95 | Google Cloud key required; 150 queries per minute per project; free; not raisable by payment | s9, s98-100; L130, L649 | OK
B6 | 96-97 | URL normalization is basic; redirects are not followed | s95-96; L636 | OK
B7 | 97-99 | No documented page-to-origin fallback; kake assumes none | keyword sweep, 0 hits | OK as absence; "Not found on the page this round" reads like a 404 (F5)
B8 | 111-112 | Name the 28-day window end date | s43-49; L363-380 | Partly: endDate (s43) vs lastDate (s44) field name; window always labelled 28 days (F8)
B9 | 115-116 | Key needed; kake holds no key and makes no call without one, cited to S039 | s9 supports the key only | Over-cited for the no-call rule (F10)

## SKILL.md triage rows (lines 682-697): ID | SKILL line | row | source located | verdict
C1 | 682-683 | Judge at p75, per form factor, over the 28-day window | S037 (75th percentile of page views); S039 s56 | OK; per-form-factor rule is policy
C2 | 685-689 | LCP <=2.5 s, >4 s; INP <=200 ms, >500 ms; CLS <=0.1, >0.25 | S037 threshold table, percentile 75 | OK (S037 is outside the named scope; checked)
C3 | 693 | Page-level record: report p75 per metric and form factor with window end date | S039 s22-23, s37, s42, s43 | OK; name metrics, set formFactor, add window caveat (F5, F8, F9)
C4 | 694 | Origin-only record: report as origin data, never as page result | S038 s11, s28; S039 s20-21 | OK as policy; "only origin-level record" is not detectable from S039 (F4, F5, F6)
C5 | 695 | No record: check final 200, no noindex, root page discoverable; then "no field data" | S038 s16-18, s26-27, s33 | Understated: no "or equivalent"; one request cannot show per-user status; user causes missing; no check method (F1, F6, F7)
C6 | 696 | Lab score gives no Core Web Vitals verdict | S036: "not a substitute for field measurement"; "cannot measure INP" | OK
C7 | 697 | API query needs an operator-provisioned Google Cloud key | S039 s9 | OK; "operator" and "kake holds none" are policy

## Findings by severity (advisory)
F1 (high; A12, A13, C5): Traffic is named as the likely cause, but S038 says Chrome on iOS, Android WebView and other Chromium browsers such as Edge provide no data (S038 s54-56; L209-211). Only desktop Chrome and Android Chrome count (s51-53), and users need usage-statistics reporting on, browser-history sync on and no sync passphrase (s48-50; L200-203). An iOS-heavy site can have no record at high traffic. Name these before traffic in entry L108-110 and SKILL row 695.
F2 (high, freshness; B3): S039 says the API is "approximately two days behind today's date" (S039 s45; api L377). The entry gives only the daily update around 04:00 UTC (L90-91). Add the lag: the newest window ends about two days before today.
F3 (medium; B4): S039 says data does not differ within a day only after the update around 04:00 UTC (s61; L433). Calls before and after that update on one UTC day can return different values. Rewrite L91-92.
F4 (medium, origin versus page; A5, C4): Unflagged source conflict. S038 s11 (L133-135): origin-level data excludes experiences that meet User and Origin criteria but not Page criteria, and Page criteria are discoverability plus popularity (s31; L185-188). S038 s28 (L179-182): origin-level data counts eligible experiences on all pages regardless of individual page discoverability. The entry quotes s28 alone. The documents cannot settle it; state it as unresolved.
F5 (medium, origin versus page; B7, C3, C4): Single-page app route changes are credited to the initial page view, and iframe views to the top-level page (S038 s38-47; L197-198). A route may have no page-level record, so entry step 1 (L103-104) and SKILL rows 693-694 need a warning. Reword "Not found on the page this round" (L97-98) to say that S039 states no page-to-origin fallback.
F6 (medium, operability; C4, C5): S039 documents no no-record response, error body or fallback (keyword sweep: 0 hits in all four texts). Entry L97-99 and SKILL rows 694-695 assume the state is detectable. Say the response is undocumented, and have kake record the literal API response for each no-record case.
F7 (low; A3, A9, C5): "or equivalent" is dropped from both noindex rules (entry L66-68; SKILL 695 "no noindex"), and "At this time" from the manual-submission rule (L81-82). S038 names a Lighthouse SEO audit for root discoverability (s26; L173-175). The entry's Limits section routes Lighthouse to tabi, but SKILL 695 gives no check method. One request cannot show per-user status (S038 s33).
F8 (low; B8, C3): S039 says collectionPeriod "will always show 28-days, even if the data is not for the full 28 days" (s48; L380). Field name conflicts: endDate in prose (s43; L363) vs lastDate in the example (s44; L370). Timezone is PST (s46). Entry L111-112 names neither the field nor the caveat.
F9 (low; B1, C3): Omitting formFactor returns an aggregate over all form factors (S039 s67; L457), but SKILL row 693 needs per-form-factor values. S039 says p75 values are "synthetically derived" and may not match interpolation over histogram bins (s37-38; L194, L202): use the reported p75 field. Name the metrics (for example interaction_to_next_paint; experimental *_with_softnavs variants exist, s42).
F10 (low; A10, A11, B9): Citation fit. Entry L115-116 cites S039 for kake's no-key and no-call rules; S039 supports only the key requirement (s9). Entry L107-108 cites SKILL.md 65-66, a webzites and kimi-pro example; cite S038 s33 (L195). Label "not a complete test" (L107) as [INFERENCE] (S038 s15).
F11 (low; A6, A7): Dropped caveats: stripping can merge distinct pages (S038 s37; L196), and "for querying purposes" applies to the lowercase rule (s30). For API lookups, S038 strips query strings in the dataset (s35), but S039 applies only basic normalization (s95-96), and the entry does not say which URL to query. Query the bare URL and read urlNormalizationDetails (S039 s73).
Verified with no finding: S037 thresholds (C2); S036 lab wording (C6); S038 popularity rule, 20% rule, discoverability conditions other than "or equivalent"; S039 endpoint, body fields, url-only scope, key, quota, URL normalization, rolling average and daily window.

## Residual risk and verification gaps
- No CrUX or PageSpeed call was made (no key; lane rule). Missing-record response, formFactor default, field name, query-string handling and metric names come from the docs and were not observed.
- F4 cannot be settled from the documents; it needs an approved observation against real data.
- S036 and S037 were checked at keyword level; entry Claim (lines 7-14) was checked only where it cites S038. lsp is not available in this seat; the files are Markdown with no code callers.

## Commands and tools
- git rev-parse HEAD; git ls-tree HEAD and e57f601 (two paths); git log --oneline e57f601..HEAD; git status --porcelain on the two paths (run without GIT_OPTIONAL_LOCKS=0; may refresh index stat data only). All exit 0; status count 0.
- curl -sS GET of the two named URLs, one each: exit 0, HTTP 200. Python 3 standard library (html.parser, re) in the sandbox for text extraction and phrase search: exit 0.
- Installs or upgrades: none (used existing curl, git, python3). No clone was needed and no git-writing code ran. The only file written in the lane is this report.
