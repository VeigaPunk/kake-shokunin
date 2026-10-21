# CitingSweep11 — blind citing-set data-walk: publish-channels.md, publish-queue.md

Seat: KakeR27.CitingSweep11 (scout, leaf, read-only findings). Axis: freshness.
Milestone: r27-full-citing-set. No production/source/ledger/Git edits; only this report.
No source/public-site evaluation, no network fetch, no tools installed.

Files walked (exactly these two), census snapshot 2026-10-21 ~17:03 local:

- `corpus/knowledge/publish-channels.md` — 84 lines, git blob `fc35cc9159ee6bf227f550a54efe3131105857b2`,
  sha256 `18042de41ae254a0e4138a6a1cfe6e4bdaa2bbf59b4c1de0181bca9f1bca73be`
- `corpus/knowledge/publish-queue.md` — 293 lines, git blob `2fbeab366a2c67cb10530c5abfcb95eee330208d`,
  sha256 `d6eb726ad485b7e7be533f332d1ab9dc8a437c81a5a1b78717d59e8c5bc46434`

Identity: both worktree blobs equal `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba:<path>` (rev-parse) and
both sha256 values equal the `frozen/expected.json` pins. HEAD is `be375d90afc6fc7aca369ab3cf5247bf460aeed2`;
`git status --short` is empty for both files. Census is therefore valid for the measured frozen base.
Method order: manual grep + full-line reads first; counter parser and `c1-before.json` inspected only after
the manual enumeration below.

## 1. Manual census — publish-channels.md

Every source-id-bearing line, form, ids, scope and frozen state. Quotes are <=25 words.

| line | form | ids referenced | pop? | frozen state | located support (<=25w) |
|---|---|---|---|---|---|
| 1 | grouped literal + metadata literal | S001, S002, S003, S005, S007; S019 | 5 yes; S019 no | 5 pairs r26-decided | `source: S001, S002, S003, S005 and S007 in corpus/SOURCES.md support the EOF round-20 corrections` |
| 1 | (same line, metadata) | S019 | no | out of population | `Metadata authority only: S019, not live platform verification.` |
| 2 | range `S001-S007` (ASCII hyphen) | S001,S002,S003,S004,S005,S006,S007 | 7 yes | 5 decided; S004,S006 missing | `round-20 corrections 2026-10-19 (S001-S007 opened that day)` |
| 58 | grouped literal | S001, S002 | yes | decided | `the uploaded artifact is not the full checkout; .git/.github are excluded and v4 excludes hidden paths by default (…) — S001, S002` |
| 59 | grouped literal | S005, S003, S007 | yes | decided | `a repo CNAME sets the domain only for branch publishing; under Actions it is ignored … — S005, S003, S007` |
| 60 | grouped literal | S001, S002 | yes | decided | `the uploaded artifact is not the full checkout; .git/.github are excluded and v4 excludes hidden paths by default (…) — S001, S002` |
| 61 | grouped literal | S003, S005 | yes | decided | `under Actions the repository CNAME is ignored for domain configuration; the domain is the Pages setting — S003, S005` |
| 84 (EOF) | grouped literal + 5 individual restatements | S001, S002, S003, S005, S007 | yes | decided | `The round-20 correction lines in this entry cite S001, S002, S003, S005 and S007 (lines 58-61).` |

Distinct ids: **8** = S001–S007 (S004/S006 only via the line-2 range) + S019.
Population pairs: **7** = (S001..S007, publish-channels.md). Out-of-population pair: **1** = (S019, publish-channels.md).

Scanned and excluded from the id set: `S0NN` inside the path template
`.ufo/waves/round-26/rechecks/S0NN.json` (line 84) is a placeholder, not a source id. No lowercase,
1–2-digit, >=4-digit, en/em-dash, `..`, `to` or `through`, or slash-joined source-id forms exist in this file
(explicit greps returned none). A zero-width/BOM/NBSP and `S`+non-space+digits scan also returned none, so the
census is not evaded by encoded separators.

Scope observations (facts about where ids sit, not verdicts):

- S004 and S006 are cited **only** by the line-2 parenthetical, whose stated scope is provenance
  ("opened that day", 2026-10-19). No line in this file attributes the artifact/CNAME corrections to S004 or
  S006: lines 58 and 60 cite only S001, S002; the other corrections cite S003, S005, S007. Both pairs already
  sit in the frozen 16-missing list and each has a dispatched adjudication seat (Pair05A/B = S004,
  Pair09A/B = S006 per `w1-spec.json`).
- Lines 1 and 84 are restatements, not new pairs: line 84 repeats the five ids from lines 1/58–61 after the
  r26 re-fetch and adds no new (row,file) pair.

## 2. Manual census — publish-queue.md

| line | form | ids | pop? | frozen state | located support (<=25w) |
|---|---|---|---|---|---|
| 1 | metadata literal | S019 | no | out of population | `Metadata authority only: S019 in corpus/SOURCES.md, not publishing readiness.` |

Distinct ids: **1** = S019. Population pairs: **0**. Out-of-population pair: **1** = (S019, publish-queue.md).
No other `S###` token exists anywhere in the 293 lines, including the provenance header, the r23 live
re-verification section and the EOF (lines 280–293); no ranges and no `SOURCES.md` row references. This file
cites no source by id other than the metadata-authority pointer.

## 3. Comparison with count_c1.py and c1-before.json (after manual census)

Independent replay of the counter's own regexes on the base bytes:

- `RANGE` found exactly one range: `(1, 7)` in publish-channels.md, none in publish-queue.md; span 6 is within
  the <=200 guard and the pair is ascending, so no `citation_range_invalid`.
- `LITERAL` ids: publish-channels {S001,S002,S003,S005,S007,S019}; publish-queue {S019}. Population
  intersection (32 rows, S014/S019/S035 excluded): publish-channels **7** pairs, publish-queue **0**.
- Result is identical to the manual table: the counter's range expansion is the *sole* generator of the
  (S004, publish-channels.md) and (S006, publish-channels.md) pairs, and it matches the frozen denominator rule
  (range with S at both ends separated by hyphen; historical metadata included; `S0NN` not an id; S019 filtered
  by population membership).

`c1-before.json` at revision `83528f7`: population 32, citingPairs 57, decided 41, missing 16. Its slice for
these two files contains **exactly two** entries — S004/publish-channels.md and S006/publish-channels.md
(2/16 = 12.5%); publish-queue contributes zero missing and zero decided pairs. This composes with the r26
ledger (5 decided publish-channels pairs: S001, S002, S003, S005, S007) to 5 + 2 = 7 population pairs, matching
the manual census. `discovered-pairs.json` and `pairs.json` were absent at census time (ENOENT), so the counter
had no monotone additions to apply for these files.

## 4. Additional obligations / out-of-population references

- Inherited32-row pairs present in these files but **not** in frozen57: **none**. All 7 publish-channels pairs
  are in the frozen set (5 decided, 2 missing); publish-queue has none. No denominator growth is claimed by
  this seat.
- Named separately (outside the 32-row population, therefore not in 57 and not C1-adjudicable):
  **(S019, corpus/knowledge/publish-channels.md)** line 1 and **(S019, corpus/knowledge/publish-queue.md)**
  line 1. S019's SOURCES row is own-work "publishing corpus contract audit", scope "Local provenance-field and
  lesson-heading census only; no verification of historical platform claims". If the population were ever
  widened to include S019 these would add 2 pairs and grow the denominator monotonically; under the frozen
  population they must be reported, not silently dropped and not counted as covered.
- S014 and S035: **zero occurrences** in both files (checked); they are not referenced here.
- Conditional naming for any later discovery: the only possible additional pairs this seat can see are the two
  S019 pairs above; no literal/grouped/range/alternate form was missed.

## 5. Freshness/operability caveats for L1

- `corpus/SOURCES.md` `usedBy` omits publish-channels.md for **all seven** S001–S007 rows (S001/S002 →
  ghp-served-set.md; S003 → ghp-custom-domain.md + ghp-served-set.md; S005/S007 → ghp-custom-domain.md;
  S004/S006 → ghp-served-set.md). `usedBy` is therefore not a safe bound for the citing set; the counter's
  enumeration plus the r26 ledger are.
- The r26 `statements.json` pair records carry only `statements` counts (2,2,2,2,1 for publish-channels) and no
  anchor/quote fields; carried decided pairs are accepted by count_c1 on pair membership alone. This is a
  structural observation, not a re-adjudication.
- publish-queue has zero population pairs: its only source pointer is S019, whose own scope disclaims
  verification of historical platform claims. C1 therefore cannot measure any publish-queue claim by
  construction; that is a coverage boundary of the frozen population, not a missing pair.
- Line pins in this report are base-revision pins (`publish-channels.md` 1,2,58–61,84; `publish-queue.md` 1).
  Append-only r27 edits at EOF do not shift them, but L1 must re-measure at the candidate revision.

## 6. Uncertainties

- Census reflects files at 2026-10-21 ~17:03 local; later concurrent appends to these files were not observed
  and would need a re-walk. No live-source or public-site verification was performed (out of scope).
- The 2 undecided publish-channels pairs are obligations already frozen; this seat supplies the citing-site
  evidence only (single line-2 provenance occurrence), not their HOLD/STALE judgment.

## 7. Verdict (author-side, for L1)

- publish-channels.md: 8 distinct source ids, 7 population pairs, 2 undecided (S004, S006) — both already in the
  frozen 16-missing set; 1 out-of-population reference (S019).
- publish-queue.md: 1 distinct source id (S019), 0 population pairs, 0 missing pairs; 1 out-of-population
  reference.
- Additional obligations found by this walk: **0**. Counter/c1-before agreement: exact for both files.
- Evidence class: manual line census + independent regex replay + frozen JSON slice; no edits, no installs.
