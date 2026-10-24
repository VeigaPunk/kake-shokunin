# ReviewEntryWebDev: C2 entry, S036/S037 statements (round 28, attempt 3)

Target: `corpus/knowledge/field-performance-cwv.md` at e57f601 (blob 677b960bb4581650c9345bc300e7ee21c8db8ea2, 132 lines). Axes: fidelity to source, operability (recheck command), freshness (page dates). Verdicts are my reading; the planner (L1) owns integration.

## Bottom line
No number, date, or quote is wrong. Every threshold value, date, and exact quote matches the retained S036.txt and S037.txt or the live pages. Over 22 rows: 15 supported, 6 overstated, 1 unsupported. The recheck command reproduces (count 1). The page dates are unchanged.

## Findings by severity
Medium
- M1 (row 11, L36-37): "a target of 10-30% ... 'poor'" is stated for all three thresholds. S037 uses it for LCP and CLS only. For INP, S037 says the all-origin check suggests 300 ms, but "unlike LCP and CLS, INP has an inverse correlation with popularity"; on the top 10,000 sites 300 ms would make most mobile sites "poor", so it concludes "greater than 500 ms".
- M2 (row 10, L32-35): "only the measurement is segmented by device" drops S037's caveat: "most of the thresholds are therefore set based on mobile achievability ... more likely represent mobile thresholds".
- M3 (row 18, L57-58): "Lab tools such as Lighthouse ... cannot measure INP" generalises. S036 limits this to tools like Lighthouse, and its lab table marks Chrome DevTools as checked for INP.
- M4 (row 16, L49-50): "This bounds how often this entry needs a threshold recheck" is unsupported. S036 bounds metric changes at one per year; it does not bound kake's recheck, which L3 sets at 90 days.
- M5 (rows 3 and 22, L7-8 and L113-114): kake policy is stated as the source's. S036 says tools "should consider a page passing" at the 75th percentile; it does not say "only" field data, "must", or "only field data closes it". S036 says lab measurement is "not a substitute".
Low
- L1 (row 9, L29-31): "classified as good" drops "for that metric" (S037). SOURCES.md:45 has the same omission.
- L2 (row 11, L36-37): "chosen for achievability" omits the quality-of-experience criterion that each S037 section names.
- L3 (row 18, L58): "the lab proxy" versus S036 "is a proxy for INP".
- L4 (row 6, L22): the label "Core Web Vitals lifecycle" is not a heading; the live heading is "Lifecycle" under h2 "Core Web Vitals".
- L5 (row 14, L43): "runtime responsiveness" is the entry's wording; S036 says "runtime performance issues".
Integrity
- I1: The working tree differs from e57f601 (uncommitted, blob 95bfbea70081e40c1d77c55e478efe516ba45995; diff --stat 1 file, 42 insertions, 23 deletions; saved at scratch cwv-drift.diff). Hunks cover claim L9-15, CrUX eligibility and API bullets, and items 2 and 5. The S036/S037 statements (L7-8, L18-61, L111-114) are identical in both, so the verdicts hold for either. Working-tree-only S038/S039 wording was not audited.
- I2: HEAD moved from 8ecbefe31b81462239c572fbe23d21404442a177 to e73d48bbf20759fc7758afaebf841fa02e5cfbbf (commits 8ecbefe, 5a83d13, e73d48b, all C1). None touches the C2 file, whose last commit is e57f601.

## Per-statement table (line numbers are e57f601)
| # | Line | Statement (abridged) | Verdict | Located source text |
|---|---|---|---|---|
| 1 | 1-3 | Pages last updated S036 2024-10-31, S037 2025-05-07; opened HTTP 200, 2026-10-22T09:29Z | supported | Live "Last updated 2024-10-31" and "2025-05-07"; receipts-a3.json accessedUtc 09:29:23Z and 09:29:24Z, httpStatus "200" |
| 2 | 3 | Recheck `grep -c '>INP</a>: Stable'` = 1 | supported | Reproduced today: 1 |
| 3 | 7-8 | Pass = p75 of page loads for LCP, INP, CLS; "only on field data"; "must" | overstated (M5) | S036: "Tools that assess Core Web Vitals compliance should consider a page passing if it meets the recommended targets at the 75th percentile for all three" |
| 4 | 9-10 | LCP <=2.5 s (poor >4 s); INP <=200 ms (poor >500 ms); CLS <=0.1 (poor >0.25) | supported | S037 table: "<=2500 ms >4000 ms 75", "<=200 ms >500 ms 75", "<=0.1 >0.25 75"; S036 "within 2.5 seconds", "200 milliseconds or less", "0.1. or less" |
| 5 | 13-14 | No field data is "never a pass"; lab numbers do not replace it | supported (policy clause) | S036: lab "is not a substitute for field measurement" |
| 6 | 20-23 | LCP, INP, CLS current; all stable; quote "LCP : Stable CLS : Stable INP : Stable" | supported (L4 label) | S036: "The Core Web Vitals are at the following lifecycle stages: LCP : Stable CLS : Stable INP : Stable" (exact) |
| 7 | 24-27 | Good bounds 2.5 s, 200 ms, 0.1; poor bounds 4000 ms, 500 ms, 0.25; each at p75 | supported | S037 table (row 4); S036 "pages should have a INP of 200 milliseconds or less" |
| 8 | 27-28 | Between good and poor bounds = "needs improvement" | supported (implied) | S037 names "good", "needs improvement", "poor"; the band itself is not defined |
| 9 | 29-31 | p75 of all page views; at least 75% good makes the site "classified as good" | overstated (L1) | S037 opening section: "the site is classified as having 'good' performance for that metric" |
| 10 | 32-35 | Same thresholds on mobile and desktop; "only the measurement is segmented by device" | overstated (M2) | Quotes exact; "the same threshold is used for both" supports clause 1. S037 device section: "most of the thresholds are therefore set based on mobile achievability" |
| 11 | 36-37 | Set for achievability with CrUX; "target of 10-30% ... 'poor'" for all thresholds | overstated (M1, L2) | S037 LCP and CLS: "This falls in our target range of 10-30%"; default rule: "by default the worst-performing 10-30% of origins are classified as 'poor'"; INP: "greater than 500 ms is a reasonable 'poor' threshold" |
| 12 | 37-38 | Data as of April 2020 (LCP, CLS) and May 2022 (INP) | supported | S037 captions: "as of April 2020" (LCP, CLS); "as of May 2022" (INP) |
| 13 | 38-39 | "policy choices that can change, not physical limits" | supported (paraphrase) | S037: "we conclude ... reasonable"; CLS: "in a future iteration of Core Web Vitals"; LCP: zero ms "is not practically achievable" |
| 14 | 43-46 | INP experimental, meant to cover runtime responsiveness beyond FID; promoted 2023; quote "with the intent to eventually retire FID"; kake does not report FID | supported (L5) | S036: "to address the runtime performance issues present on the web more comprehensively than First Input Delay (FID)"; "INP was promoted in 2023 from experimental to pending status with the intent to eventually retire FID" (exact). "kake does not report FID" is kake's choice |
| 15 | 47-48 | Stable metrics change at most once per year; changes in docs and changelog; can be retired and replaced | supported | S036: "Stable Core Web Vitals metrics won't change more than once per year. Any change ... documentation, as well as in the metric's changelog"; "A stable metric can be retired and replaced" |
| 16 | 49-50 | "This bounds how often this entry needs a threshold recheck" | unsupported (M4) | Not in S036; L3 sets the recheck at 90d |
| 17 | 54-56 | CrUX collects anonymized real-user data per CWV; feeds PageSpeed Insights and Search Console report | supported | S036: "collects anonymized, real user measurement data for each Core Web Vital"; "powers tools like Chrome DevTools, PageSpeed Insights, and Search Console's Core Web Vitals report" |
| 18 | 57-58 | "Lab tools such as Lighthouse ... cannot measure INP"; "TBT is the lab proxy" | overstated (M3, L3) | S036: "Tools like Lighthouse that load pages in a simulated environment without a user cannot measure INP"; "is a proxy for INP". Live lab table: Chrome DevTools INP "check"; Lighthouse INP "block (use TBT instead)" |
| 19 | 59-60 | Lab "is not a substitute for field measurement" | supported | S036 exact: "While lab measurement is an essential part of delivering great experiences, it is not a substitute for field measurement." |
| 20 | 60-61 | Lighthouse score = "development evidence", not a CWV pass | supported (inference) | S036 "essential part of delivering great experiences" plus the p75 field pass rule; "development evidence" is kake's wording |
| 21 | 111-112 | Item 3: judge each metric at p75 against the S037 table, per form factor | supported | S037 table (p75); S036 "segmented across mobile and desktop devices". The 28-day window is S039, not audited |
| 22 | 113-114 | Item 4: "Lab results may guide a fix; only field data closes it" | overstated (M5) | S036: "Performance optimizations that improve TBT in the lab may improve INP in the field" supports "may guide"; "only field data closes it" is not in S036 |

## Commands and exit codes
- `curl -sSL --max-time 60 -w 'HTTP %{http_code}'` on https://web.dev/articles/vitals: HTTP 200, 143742 bytes, exit 0. Same for defining-core-web-vitals-thresholds: HTTP 200, 149322 bytes, exit 0. One GET each.
- `sha256sum` of retained S036.txt: 5ee762fc1bce131604beebc2892b307f5ca51f04169608a8d94e3a08d8d4b445 (16,766 chars); S037.txt: 2b443a0b8c5847db718cd58a1adcdf0d336e47166f9486084408593f438ebc49 (25,029 chars). Both equal the receipts visibleSha256 values. Exit 0.
- Python, receipts method (strip script, style and tags; unescape; collapse whitespace) on the live GETs: visible-text sha256 identical to the two retained files. Raw HTML differs from the receipts (live 1cb8a481a1bb4465f2dc61ebab82fd92ed0a0d9870c8f689b8f68971e87a588a and 1a6d1d13840a68199bb010cd57f077c152fb678db94b59d79a2ba782e30eda48; receipts 44aee957681d2174476f41e9b5e831ff2f43e4d13a908287e006fd400964e4c2 and f660898060476f851b90f8cc4ffd526c75f28e8ba6a6f1f28152e3a50f2c0b93) at the same byte sizes; the receipts note page tokens.
- `grep -c '>INP</a>: Stable'` on live vitals HTML: 1, exit 0. All 10 quoted phrases in the entry: exact substrings of the retained text (True). Live lab table (second table on the vitals page) parsed, exit 0.
- Read-only git in kake-shokunin: `rev-parse HEAD`; `merge-base --is-ancestor 8ecbefe...` (yes); `log -- <file>` (only e57f601); `hash-object` without -w (working tree 95bfbea7); `show e57f601:<file>` (blob 677b960b); `diff --stat e57f601 --`. All exit 0. No mutating command.
- Scratch only: /fast/scratch/hyaku/kake-r28a3/res/ReviewEntryWebDev/ (vitals.html, thresholds.html, cwv-e57f601.md, cwv-drift.diff). Created the residual directory for this report.
- Evidence: corpus/SOURCES.md:44-45 (S036, S037 rows); .ufo/waves/round-28/sources/receipts-a3.json (accessedUtc 2026-10-22T09:29:23Z and 09:29:24Z).

## Not verified and residual risk
- S038 and S039 claims (claim L10-15 popularity clause, CrUX eligibility, CrUX API bullets, items 1, 2 and 5, Limits) are outside this target. The working tree adds unaudited wording ("about two days behind", "Pacific Standard Time without daylight saving", "Chrome on iOS ... send no data").
- Only the visible text of S036 and S037 was compared against raw markup, plus the checks above. No CrUX or PageSpeed API call and no property probe.
- Residual risk: read as a verdict rule, M1 to M3 would misstate INP's basis, the device neutrality of the thresholds, and lab-tool INP capability. Recommend the planner resolve M1 to M5 before the entry is relied on.
- Tooling: no installs or updates. Used host curl, sha256sum, python3 and read-only git. No pacman.
