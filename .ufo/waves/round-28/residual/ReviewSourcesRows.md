# Residual review — SOURCES S036–S039, Paths line, Round 28 search log
Seat KakeR28a3.ReviewSourcesRows · 2026-10-22 · advisory input for L1, not a round verdict.
Target: corpus/SOURCES.md at e57f601bd0148bb7dce9052f0cade3fd11751375 (lane HEAD 8ecbefe…;
corpus/SOURCES.md identical e57f601→HEAD — `git diff e57f601… HEAD -- corpus/SOURCES.md` empty, exit 0).
Contract: CORPUS.md §"SOURCES.md — where a shokunin learns" (v1, frozen), read read-only.

## Verdict
No contract violation found in the four rows, the Paths line, or the search-log paragraph.
One census warning (W04, S033) is pre-existing and predates the diff.

## Diff — no existing row changed (exit 0)
`git -C …/kake-shokunin diff b5d423fc02… e57f601bd01… -- corpus/SOURCES.md`
7 insertions, 0 deletions: 4 registry rows after S035, 1 Paths bullet, 1 log paragraph + blank.
Zero deletions ⇒ no existing cell touched; append-only also logged in corpus/lessons/round-28.md:54-59.
Base max id = S035 (`git show b5d423fc02…:corpus/SOURCES.md`), so S036–S039 are the next unused ids;
registry ends at S039 (no gap/reuse).

## Census (exit 0)
`TMPDIR=/fast/scratch/hyaku/kake-r28a3/res/ReviewSourcesRows/tmp /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```
W04 is a warning (never changes status) and pre-existing: the rfc9110 URL appears in 2 rows at both
b5d423f and e57f601 (git show | grep -c = 2 and 2), both untouched by the diff. E01–E12 all clean ⇒
11 cells per row (NF=13, no `|` in cells), valid id/kind/tier/status/opened/recheck, no duplicate id
or URL+scope, no community-at-A, every used-by path exists on disk, no row-shaped text outside Registry.

## Per-row checks (contract cells vs retained attempt-3 texts)
Chain per row: receipts-a3.json URL == row URL; receipts `visibleSha256` == sha256sum of the retained
text (all four match: 5ee762fc…, 2b443a0b…, 0a7047d3…, 4b2cd5ae…); anchor "last updated" == the page's
"Last updated … UTC." in the text; teaches phrases located in text or receipts lessonQuotes
(foundInVisibleText true). This verifies cell content without any fetch by this seat.
- S036 web.dev/articles/vitals · docs · A · mined · opened 2026-10-22 · recheck 90d. Receipt 09:29:23Z,
  200. "Last updated 2024-10-31 UTC." matches anchor. Sections Core Web Vitals / Core Web Vitals
  lifecycle / "Field tools to measure…" / "Lab tools to measure…" located. Teaches grounded: LCP 2.5 s,
  INP 200 ms, CLS "0.1. or less", "75th percentile … segmented across mobile and desktop"; stability and
  lab≠field backed by round-28.md:42-44 quotes.
- S037 …/defining-core-web-vitals-thresholds · docs · A · mined. Receipt 09:29:24Z, 200. "Last updated
  2025-05-07 UTC." matches. Teaches grounded: table "≤2500 ms >4000 ms 75 … ≤200 ms >500 ms 75 …
  ≤0.1 >0.25 75"; "if at least 75 percent of page views … good"; "not segregated by device".
- S038 …/docs/crux/methodology · docs · A · mined. Receipt 09:29:25Z, 200. "Last updated 2024-06-20
  UTC." matches. Sections Eligibility / Publicly discoverable / Sufficiently popular / Origin located.
  Teaches grounded: "status code other than 200 (after redirects)", X-Robots-Tag/meta noindex,
  "An exact number is not disclosed", origin aggregation, query strings and fragments stripped.
- S039 …/docs/crux/api · docs · A · mined. Receipt 09:29:26Z, 200. "Last updated 2026-10-13 UTC."
  matches. Sections CrUX API Key / The rolling average / Daily updates ("updated daily around 04:00
  UTC") / UrlNormalization / Rate limits located. Teaches grounded: origin-or-url key with formFactor,
  28-day rolling average, Google Cloud key, "150 queries per minute per Google Cloud project";
  "no API call was made" is consistent with GET-only receipts.
- opened 2026-10-22 == receipt access date (present-day ISO, E08-clean); recheck 90d is an allowed
  cadence; status mined with used-by = corpus/knowledge/field-performance-cwv.md,
  corpus/lessons/round-28.md (both exist). Tier A is scoped (scope cells name the topic) and these are
  Google's official docs for their own metric/report/API — authoritative for those scopes.

## Paths line (SOURCES.md:60)
"Field performance — S036 → S037 → S038 → S039: …" matches the contract shape
`<topic> — S003 → S010 → S014: why this order`; ids exist, all mined, ordering rationale stated.

## Round 28 search-log paragraph (SOURCES.md:90)
Question, where (four named Google pages), date 2026-10-22, counts 4/4/4/0, S018 rejection note,
stop rationale — rule 5 fields complete. Receipt cross-check: receipts.json attempt-2 accessedUtc
08:30:34Z/35Z/35Z/36Z, all httpStatus 200 → matches "08:30:34Z–08:30:36Z"; receipts-a3.json attempt-3
09:29:23Z/24Z/25Z/26Z, all "200" → matches "09:29:23Z–09:29:26Z". Gate rule 1 satisfied:
round-28.md:33-36 has per-row URL + accessed date + located quotes of 19/23/15/15 words (≤25).

## Observations (non-blocking)
- S036 anchor abbreviates section names ("Field tools and Lab tools" vs the page's "Field tools to
  measure Core Web Vitals" / "Lab tools to measure Core Web Vitals"); unambiguous, not exact strings.
- S038 "Page" and S039 "Schema"/"URLs" anchor sections confirmed by adjacent located content, not exact
  heading-string grep.
- receipts.json uses numeric httpStatus 200, receipts-a3.json string "200" — cosmetic, outside SOURCES.md.
- S036 teaches says CLS ≤0.1; saved text reads "a CLS of 0.1. or less." (visible-text extraction
  artifact); the S037 thresholds table states ≤0.1 plainly.

## Not verified / residual risk
- No URL opened by this seat (not authorized): anchors, teaches and quotes verified only against the
  lane's retained attempt-3 texts and receipts, not the live pages. Raw-HTML sha256 receipts point at
  L1 scratch copies under /fast/scratch/hyaku/kake-r28a3/sources/, which I did not re-hash.
- Census ran on the working tree; SOURCES.md proven identical to e57f601, so validated == reviewed content.
- C2 counter arithmetic (0/4 → 4/4), Gate/lesson wording, QUALITY/SKILL/README/PROVINCE text: other seats' scope.

## Tooling
No installs or upgrades (none needed). All lane work read-only; only writes were this report and an
empty scratch TMPDIR under /fast/scratch/hyaku/kake-r28a3/res/ReviewSourcesRows/tmp (census writes stdout only).
