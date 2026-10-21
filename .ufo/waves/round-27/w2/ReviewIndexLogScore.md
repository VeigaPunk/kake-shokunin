# ReviewIndexLogScore — round27 fresh falsification (readiness review)

Lane: leaf reviewer, axis **freshness**. Pinned candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`,
base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`, declarations `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
Authority read: `contract.json`, `oracle-implementation-corrections.json`, `pairs.json`, `frozen-candidate.json`,
`carry-errata.json`, `strict-c1-disposition.json`, `integration-receipt.json`, `residual-identities.json`.
No source edits; no build/lint/formatter. Scratch: `/fast/scratch/hyaku/kake-r27/reviewindexlogscore/`.
Working tree == candidate: `git rev-parse HEAD` = ac46a74; blob-equality checked for LOG/SCORECARD/SKILL/
count_c1/c2_count/pairs.json/citing_set.py/SOURCES.md/lessons-round-27 → all `SAME`.

## Findings (author-side, by severity)
### F1 — MEDIUM — SCORECARD headline claims C1 completion the candidate's own counter refutes
`SCORECARD.md:533`: "41/57 citing pairs adjudicated→**all frozen/discovered pairs decided**".
Declared expected before running: the frozen after-clause (contract.json:10/13) never counts UNVERIFIABLE
decided, so "all … decided" must mean 58/58 decided and exit 0.
Actual: `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a74…` → **exit 1**,
`citingPairs 58, reviewedPairs 58, decided 55, knownUnverifiableUnits 7, knownUnverifiablePairs 3`,
`missing 3` = S001/ghp-served-set (3u), S007/ghp-custom-domain (1u), S033/static-canonical-preflight (3u).
Discrepancy: 55/58 decided, not "all … decided". `SCORECARD.md:548` states "38/57→55/58, not a completed
C1" but only as *expected* arithmetic ("must be measured separately"); the measured 55/58 result appears
nowhere in SCORECARD — only in `.ufo/waves/round-27/frozen-candidate.json` `authorMeasurements`. An
admission reader taking the scorecard headline would credit a C1 the same commit's gate reports as
non-clean. Same file also retains the r26 record honestly (`:533` "r26 author-side verify claim above is
superseded by non-author rejected-honest-stop"), so this is one stale headline, not a rewritten record.

### F2 — LOW/MEDIUM — LOG asserts the measured C2 result in its lead paragraph, then denies claiming it
`LOG.md:1066` states "C2 operability capability: frozen-r26 missing-pair detection0/16→16/16"; the same
round-27 section states `LOG.md:1074` "Positive results remain unasserted until executed" and `LOG.md:1081`
"No claim of successful measurement or new capability credit precedes the actual consumer-visible
baseline/after runs". Declared expected: either the lead is a forecast or the after-runs are recorded in
LOG. Actual: the after-run outputs are **not** in LOG (`LOG.md:1155` "Author after-runs and the fresh85
payload will grade the fixed candidate" — still pending); only `frozen-candidate.json` holds them.
The data is true: `c2_count.py --revision ac46a74…` → exit 0, `expected 16, detected 16, falsePositive 0,
passed true, gateExit 1`. So the defect is claim-precedence/self-consistency, not fabricated data.

### F3 — LOW — receipt hash chain does not cover the shipped measurement code
`LOG.md:1071` "Exact hashes/diff and reasons: `oracle-implementation-corrections.json` and
`oracle-implementation-diff.patch`". Actual chain (sha256 of blob content):
- be375d9 count_c1.py = `a1e46d19…` (= corrections.json `declaredSha256` ✔)
- 08014ce count_c1.py = `26fd8bbb…` (= corrections.json `correctedSha256` ✔); patch `oracle-implementation-diff.patch` (151 lines) == `git diff be375d9 08014ce` (151 lines, only a/ b/ prefix form differs) ✔
- 9ba102d count_c1.py = `f2632131…`, oracle_selftest.py = `7266a97e…`
- **ac46a74 count_c1.py = `8d4c22ef…`, oracle_selftest.py = `943db49c…` — a third change made at the
  candidate commit** (carry-errata integration; selftest expectations 56→55, 39→38).
Neither corrections.json, nor `strict-c1-implementation-diff.patch` (covers 08014ce→9ba102d only), nor
`strict-c1-source-hashes.json` covers the shipped bytes; `strict-c1-source-hashes.json` lists count_c1.py
`f2632131…` under key `"priorImplementation":"08014ce…"`, but at 08014ce the file is `26fd8bbb…` (that hash
is the 9ba102d version) — a misattributed revision. Only `frozen-candidate.json` / `integration-receipt.json`
`codeSha256` pin the shipped hashes, with no diff or reason. A reader following LOG's "exact hashes" pointer
cannot reconcile the shipped counter with any receipt.

### F4 — LOW — stale strict-disposition pointer (superseded, not retracted)
`strict-c1-disposition.json` `unresolved` lists 2 pairs / 6 units (S001, S033) and
`expectedStrictArithmetic` "39/57 … 56/58". Measured: baseline `count_c1.py --revision 83528f7…` → exit 1,
`citingPairs 57, reviewedPairs 41, decided 38, knownUnverifiableUnits 7, knownUnverifiablePairs 3`;
candidate → `decided 55`. The 7th unit (S007) arrives via hash-pinned `carry-errata.json`
(`236d9e79…`, pinned inside count_c1.py). `LOG.md:1140-1147` and `SCORECARD.md:544-549` do record the
supersession ("7 units across3 pairs"), so this is a stale pointer, not a false claim — but `LOG.md:1118`
"Details: `strict-c1-disposition.json`" does not mark that file's arithmetic as superseded.

### F5 — LOW — partial reader gets the stale six-unit figure
`corpus/README.md` round-27 section: "Six inherited unknown statement units in two pairs remain explicit"
is followed (same section) by "Known unresolved units are 7 across 3 pairs… The earlier six-unit description
is the old field sum only." Corrected in place but not struck; same pattern in `LOG.md:1113-1116`
("Six inherited units remain explicit (S001… S033…)") before the erratum at `:1143`.

## Verified honest / preserved (executed, not source-text)
- r26 stays **rejected-honest-stop** in LOG, SCORECARD, corpus/README.md, lesson; `git diff base→candidate -- .ufo/waves/round-26/` = **0 files changed** (r26 ledger/receipts/reports bytes untouched); 313 units never relabelled as a semantic denominator; 7 units/3 pairs disclosed (`carry-errata.json`).
- Role floor: r26 W1 executor-2 debt disclosed (LOG r26 section; lesson "historical role floor"); r27 W1 `roleMix.executor = 3` (`w1-outcomes.json`), 67 identities / 67 nonempty reports / dead 0; the 68th identity (PrivacyBoundary) is disclosed as a residual executor, not padded into the build barrier.
- Original counter bytes preserved at declarations (`be375d9` sha256 `a1e46d19…`); original + corrected replays retained; all **28** frozen pins unchanged (`frozen/expected.json` sha256 map: 0 mismatches vs candidate blobs; 26 corpus + population + ledger, matching `SKILL.md:616`).
- All 16 `c1-before.json` missing pairs are covered by `pairs.json` (0 uncovered); extras are exactly the conservative S013 embedded reference and the S004 override. 3 STALE rows carry the contract marker in the right files: `[r27-recheck S005 STALE]` (static-canonical-preflight, sitemap-orphan-audit), `[r27-recheck S004 STALE]` (ghp-served-set).
- Historical bytes preserved: the 4 changed knowledge files are **prefix-extending** (ghp-custom-domain 4475→5101, ghp-served-set 8001→10080, sitemap-orphan-audit 13065→14606, static-canonical-preflight 19573→23662; `now.startswith(orig)` true for all).
- `corpus/SOURCES.md`: only the `used-by` cell changed, rows S001–S006; all other cells byte-identical (cell-level diff). Lesson old→new routing table matches base and candidate cells exactly (6/6).
- Retention honesty: 8 manifest records; HTML rows have `receivedSha256 ≠ sha256` (retained visible text), code rows S001 retain received bytes verbatim with the distinction stated; `rawHttpBodyRetained false` for HTML, no form/script values retained; migration receipt exit 0, 8 records, 8 own filenames removed.
- Reproduced at the pinned revision (TMPDIR set, no /tmp): C1 candidate exit 1 (55/58), C1 base exit 1 (38/57, 41 reviewed, 57 pairs), C2 exit 0 (16/16, 0 FP), gate selftest 29/29 failed 0, git-name selftest 30/30 failed 0, c1 selftest 14/14 failed 0, c2 selftest 3/3 failed 0 — every number in the frozen manifest's `authorMeasurements` reproduced exactly.

## Residual risk / verification gaps
- W2 fresh falsification had not executed at the pinned revision (`frozen-candidate.json` `actualFreshW2Spawned 0`, `plannedFreshW2 85`); admission and the fresh-85 grade remain Main's, and any post-measurement append is outside this review.
- HTTP authenticity of the 8 public fetches is asserted (status 200 + fetch dates ≥ declaration) but not re-verifiable without a re-fetch, which is out of scope; the docs correctly refuse byte-level identity.
- "L1 integrated only their assigned files" is not independently verifiable from the repo; `w1-dispatch.json` names three disjoint writer worktrees (writer-gate, writer-selftest, writer-fixtures) — consistent, not proof.
- F1–F5 are documentation/receipt defects only; none changes a measured number, and no false PASS was found in the counters, the 28 frozen inputs, or the r26 record.

Verdict: the candidate's measured behavior matches its own receipts and the frozen inputs; the defects are
a stale SCORECARD C1 headline, a LOG claim-precedence contradiction, and an uncovered third hash step in the
measurement-code receipts. Recommendation only — no admission, integration or edit performed.
