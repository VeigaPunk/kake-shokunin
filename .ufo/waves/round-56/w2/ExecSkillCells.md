# ExecSkillCells

Seat ExecSkillCells, round-56 W2 falsify, lane kake-shokunin. Question attacked: the SKILL.md gate-registry self-test tallies
**beyond the ten rows C1 pins** — are they true at the tip, and how far does a C1 zero-mismatch result generalise? All runs in
my own clone `/tmp/execskillcells/D` (`git clone -q --no-checkout <lane> $D && git -C $D checkout -q
7ad7db51dfcff2eccea9f7f73726f2437b2ed8de`; `git -C $D rev-parse --show-toplevel` = `/tmp/execskillcells/D`, `rev-parse HEAD`
= `7ad7db51dfcff2eccea9f7f73726f2437b2ed8de`). `SKILL.md` at the tip is blob `0bb37a25b211075b1461dbbd4f5bca0c58d9493a`,
byte-identical to the blob at the revision under attack `a450e43e696d032e3ac308383f6b3394e0c92860`, so this inventory is the
same at both. Lane writes: this report only (no lane git/jj mutation, no pacman, no install — nothing needed; the two JS runs
used the host `node` v24.21.0).

Method: the W1 inventory was re-derived, not copied. Three passes over the tip file (1261 lines): pattern A
`[0-9]+ (sandbox-repo |generated |matrix |round-[0-9]+ regression )*(fixtures|cases|checks)` → 21 matches on 20 lines;
pattern B `[0-9]+/[0-9]+` beside `self[- ]?test` → 9 lines; plus a per-row cell scan of all 26 registry rows for tally tokens
in **any** column. The cell scan found one tally the line patterns miss: line 212, `15/15` in the Write-scope column. Both
passes were re-run independently in Python over the same file and agreed.

## INVENTORY:

Registry-row tallies (26 registry rows name a selftest; 13 carry a tally in the `Self-test` cell, 1 more carries one in another cell):

| line | row | tally as written | command it belongs to | class |
|---|---|---|---|---|
| 212 | freshness-sweep | `selftest 15/15`; `cb807bc killed 0/25, now 25/25` | `node scripts/freshness-sweep.mjs --selftest`; `node .ufo/round-20/resume/confinement-mutants.mjs` | (c) other row — Write-scope cell, not `Self-test` |
| 726 | base-path-audit | `30 matrix fixtures plus 15 round-29 regression fixtures X01–X15` (=45) | `python3 -B scripts/base_path_selftest.py` | (a) ten |
| 1046 | link-preview-audit | `45 fixture directories at b1cbbc39`, `MIN_FIXTURES 20` | `python3 -B scripts/link_preview_selftest.py` | (c) other row — excluded by the contract |
| 1067 | source-recheck-audit | `106 fixtures` | `python3 -B scripts/source_recheck_selftest.py` | (a) ten |
| 1093 | robots-expectation-audit | `204 fixtures` | `python3 -B scripts/robots_audit_selftest.py` | (a) ten |
| 1128 | sitemap-file-audit | `235 fixtures, all 34 sentences` | `python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` | (a) ten |
| 1198 | redirect-expectation-audit | `23/23` | `python3 -B scripts/redirect_audit.py --selftest` | (a) ten |
| 1199 | commit-citation-lint | `9/9` (and `then-tally 8/8`) | `python3 -B scripts/citation_lint.py --selftest` | (a) ten |
| 1215 | wave-evidence-ledger | `19 fixtures` | `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` | (a) ten |
| 1216 | quote-truth-counter | `18 fixtures` | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee … c52_quote_truth.py --selftest` | (a) ten |
| 1233 | readme-index-counter | `44 fixtures` | `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` | (a) ten |
| 1234 | yahoo-robots-quote-truth-counter | `54 sandbox-repo fixtures … including 3 unit-rule checks` | `KAKE_R55_SELFTEST_REV=64c0ce12ffe3… … c55_quote_truth.py --selftest` | (a) ten |
| 1253 | selftest-tally-counter | `47 checks` | `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` | (b) new round-56 |
| 1254 | yahoo-crawl-handling-quote-truth-counter | `67 checks: 64 sandbox-repo fixtures … plus 3 unit-rule checks` | `KAKE_R56_SELFTEST_REV=3691e9689a03… … c56_quote_truth.py --selftest` | (b) new round-56 |

Prose tallies (12 lines, none in a `Self-test` cell; each names or implies a selftest/fixture count):

| line | tally as written | command it belongs to (as the text states it) |
|---|---|---|
| 504 | `12 cases` | `python3 .ufo/waves/round-23/snapshot_probe.py --snapshot-script scripts/live_snapshot.py --validator scripts/canonical_audit.py` |
| 593 | `Self-test: 24 cases` | `.ufo/waves/round-26/measure.py --selftest` (row 588's selftest, stated in prose) |
| 668 | `exact16/16, real29-case fixtures, Git30 checks` | round-27-era unadmitted C2 evidence (no registry row) |
| 770 | `(41 cases)` | `scripts/citing_set_selftest.py` over `scripts/fixtures/citing-set/` (row 617) |
| 1025 | `29 fixtures`; `28/28 counter score` | `scripts/link_preview_selftest.py` (round-34 wave-1 state) |
| 1029 | `35 fixtures at 76fac3b` | `scripts/link_preview_selftest.py` (revision-pinned) |
| 1110 | `194 fixtures` | `scripts/robots_audit_selftest.py` (round-38 state) |
| 1116 | `now has 204 fixtures` | `scripts/robots_audit_selftest.py` (round-39 state) |
| 1141 | `now 179 fixtures` | `scripts/sitemap_audit_selftest.py` (round-40 build state) |
| 1156 | `Selftest 183 fixtures` | `scripts/sitemap_audit_selftest.py` (round-40 revised state) |
| 1184 | `selftest 235 fixtures` | `scripts/sitemap_audit_selftest.py` (round-42 state) |
| 1203 | `11/11 and 3/3` | `python3 -B .ufo/waves/round-46/c46_matrix.py …` (fixture outcomes, read as bounded counts) |

Numbers deliberately **not** counted as selftest/fixture tallies: 321 (`12 cross-body swap mutations`, mutant survival),
1193 (`2/2 rows, 2/2 receipts`, registry completeness), 212 verdict map (`15/15; 0/25; 25/25` in the *Pinned values* sense is
covered above), 350 (exit codes `0/1/2/64`), 927 (`5/5` score), 1067/1093 (`25 of 28 sealed cases`), 1128 (`sealed 24-case
counter`), 1215 (`13 of 18 families`), 1021 (`101/102` arithmetic).

## RUNS:

All commands were run as the row documents them, from `$D`, with `KAKE_R52_/R55_/R56_/R5N_SELFTEST_REV` unset except where
the row's own cell carries the pin; every exit code was 0 and every run finished in seconds (the slowest, `freshness-sweep
--selftest`, 1.8 s; the confinement-mutants script, 33 s).

| line | claimed | printed (quoted from stdout/stderr) | agree? |
|---|---|---|---|
| 726 | 30 + 15 = 45 | `45/45 fixtures passed`; `caseNames` 45 with 15 `X*` and 30 others | yes |
| 1067 | 106 | `{"cases": 106, …, "passedOverTotal": "106/106", "verdict": "clean"}` | yes |
| 1093 | 204 | `{"cases": 204, …, "passedOverTotal": "204/204"}` | yes |
| 1128 | 235, all 34 sentences | `PASS 235/235`; `--map` → `case count: 235`, `sentence coverage: 34/34` | yes |
| 1198 | 23/23 | `selftest: 23/23 passed` | yes |
| 1199 | 9/9 | `selftest: 9/9 passed` | yes |
| 1215 | 19 | `c52 ledger selftest: 19/19` | yes |
| 1216 | 18 | `c52 quote-truth selftest: 18/18 (fixture revision 1ae8de5d4dee)` | yes |
| 1233 | 44 | `c55 readme-index selftest: 44/44` | yes |
| 1234 | 54 (+3 unit-rule checks) | `c55 quote-truth selftest: 54/54 (fixture revision 64c0ce12ffe3)` | yes |
| 1253 | 47 checks | `c56 selftally selftest: 47/47` | yes |
| 1254 | 67 checks (64+3) | `c56 quote-truth selftest: 67/67 (fixture revision 3691e9689a03)` | yes |
| 212 | `selftest 15/15` | `selftest: 36/36 passed` | **no** |
| 212 | `cb807bc killed 0/25, now 25/25` | `MUTANTS cb807bc: killed 0/25 survived 25/25` / `MUTANTS working-tree: killed 25/25 survived 0/25` | yes |
| 1046 | 45 fixture dirs at `b1cbbc39`, `MIN_FIXTURES 20` | `git ls-tree -d b1cbbc39 scripts/fixtures/link-preview/` = 45 dirs; `MIN_FIXTURES = 20`; selftest prints `{"cases": 46, …, "passedOverTotal": "46/46"}` (tip has 46 dirs) | dir count yes; not comparable to the 46-case print |
| 504 | 12 cases | `{"met": 12, "total": 12, "passed": true}` | yes |
| 593 | 24 cases | `{"passed": 24, "failed": 0}` (24 cases) | yes |
| 770 | 41 cases | `{"cases": 45, "failed": 0, "verdict": "clean"}` | **no** |

Dated-history tallies re-measured at the commit that wrote them (to separate "stale" from "superseded"): `1029` 35 fixtures at
`76fac3b` → 35 dirs; `1025` 29 fixtures → 29 dirs at `24a1647` (the commit that wrote the line); `1110` 194 → `194/194` at
`adab4c7`; `1141` 179 → `PASS 179/179` at `56d57ee`; `1156` 183 → `PASS 183/183` at `d8d5578`; `212`'s `15/15` → `selftest:
15/15 passed` at `02b6dd0` (the commit that wrote the annotation). Not run: line 668 (`16/16`, `29-case`, `30 checks`) — it
belongs to round-27 unadmitted evidence with no registry row and no named command; reported unrun.

## STALE OUTSIDE THE TEN:

Rows outside the ten: 2 carry a tally — `freshness-sweep` (212, off-column) and `link-preview-audit` (1046). **1 of those 2 is
stale**: line 212's `selftest 15/15` against `36/36` printed (accurate at `02b6dd0`, superseded since; the same cell's
`0/25 → 25/25` mutant pair still matches exactly). `link-preview-audit` is not stale — its `45` is a directory count at
`b1cbbc39` and is correct there; the tip holds 46 directories and prints a 46-case total, which is the unit mismatch the
contract uses to exclude the row.

The two new round-56 rows both agree (47/47, 67/67) but sit outside C1's frozen ten-name population, so nothing in the round
checks them.

Prose: **1 stale** — line 770's `(41 cases)` against 45 printed (41 was correct at `451e98f`, the commit that wrote the
sentence; round-30 commit `1c7773e` took the fixture set to 45 and no later text corrects the sentence). Every other prose
tally either matches the tip (504 `12/12`, 593 `24/24`, 1116 `204`, 1184 `235`) or is accurate at the revision it names
(1029, 1025, 1110, 1141, 1156 above); 668 is unrun.

Stale tally statements outside the ten, at the tip: **2** (line 212 `15` vs `36`; line 770 `41` vs `45`). Stale tally
statements inside the ten: **0** (all ten agree, per RUNS). Stale among the two new rows: **0**.

## LIMIT SENTENCE:

> C1 certifies only the ten named rows' `Self-test` cells at the measured revision; outside them SKILL.md at the tip carries
> two more row-level tallies and twelve prose fixture-counts, and two of those (line 212 `selftest 15/15` vs 36/36 printed;
> line 770 `41 cases` vs 45 printed) are stale, so a met C1 does not certify SKILL.md's tallies as a whole.

VERDICT: All ten C1-pinned tallies and both new round-56 rows agree with what their documented commands print at the tip (45/106/204/235/23/9/19/18/44/54, 47, 67), while outside C1's population two tally statements are stale — `freshness-sweep`'s off-column `selftest 15/15` (prints 36/36) and the citing-set prose `41 cases` (prints 45) — and link-preview's `45` is a directory count at `b1cbbc39`, not a case tally.
