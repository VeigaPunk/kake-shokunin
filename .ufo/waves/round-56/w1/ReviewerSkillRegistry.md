# ReviewerSkillRegistry

Scope: C1 population review — every fixture/case/check-count or N/N mention in `SKILL.md` at base
`e48354b7`, classified vs the ten pinned `POP` rows in `c56_selftally.py`. Observed tallies were
measured by running each documented selftest in a clean clone at the base revision
(`/tmp/tmp.JhdWSNRkgy/lane`, HEAD `e48354b7`), all exit 0 unless noted.

## MENTIONS:

| Line(s) | Number | Command / context | In registry row? | Class |
|---|---|---|---|---|
| 726 | 30 matrix + 15 r29 regression fixtures = 45 | `python3 -B scripts/base_path_selftest.py` | yes (pinned) | a — observed 45/45, match |
| 1067 | 101 fixtures | `python3 -B scripts/source_recheck_selftest.py` | yes (pinned) | a — observed 106/106, MISMATCH |
| 1093 | 137 fixtures | `python3 -B scripts/robots_audit_selftest.py` | yes (pinned) | a — observed 204/204, MISMATCH |
| 1128 | 150 fixtures (+34 sentences) | `python3 -B scripts/sitemap_audit_selftest.py --tool …` | yes (pinned) | a — observed 235/235, MISMATCH |
| 1198 | 23/23 | `python3 -B scripts/redirect_audit.py --selftest` | yes (pinned) | a — observed 23/23, match |
| 1199 | 8/8 | `python3 -B scripts/citation_lint.py --selftest` | yes (pinned) | a — observed 9/9, MISMATCH |
| 1215 | 19 fixtures | `c52_wave_ledger.py --selftest` | yes (pinned) | a — observed 19/19, match |
| 1216 | 18 fixtures | `c52_quote_truth.py --selftest` | yes (pinned) | a — observed 17/18 exit 1 unpinned (18-case fixture set pinned to a stale fixture rev), MISMATCH |
| 1233 | 35 fixtures | `c55_readme_index.py --selftest` | yes (pinned) | a — observed 44/44, MISMATCH |
| 1234 | 47 sandbox-repo + 3 unit-rule = 50 | `c55_quote_truth.py --selftest` | yes (pinned) | a — observed 54/54, MISMATCH |
| 1046 | 45 fixture directories at `b1cbbc39` | `python3 -B scripts/link_preview_selftest.py` | yes (excluded) | b/c — dirs at `b1cbbc39` verified 45 (accurate history); selftest prints 46/46 *cases* at base |
| 1046 | MIN_FIXTURES 20; 28/28; 35 sealed cases; ≥22/24, 24/24 | same row, pins cell | yes | b/c — script constant, historical receipts at `76fac3b`/`b1cbbc39`, sealed-case counter |
| 212 | selftest 15/15 | `node scripts/freshness-sweep.mjs --selftest` (notes cell, r20) | yes (freshness-sweep row, not pinned) | unmeasured — observed 36/36; the 15/15 claim is STALE |
| 212 | killed 0/25 → 25/25 | `confinement-mutants.mjs` mutation score | same row | c — mutant kills, not selftest tally |
| 617 | 29 consumer-input cases; pins26+28 | citing-set row, pins cell | yes (not pinned) | unmeasured — `citing_set_selftest.py` prints cases=45; the 29 is STALE |
| 618 | original57 | `round-27/count_c1.py` pins cell | yes (not pinned) | c — historical r27 population min, tied to `be375d9` |
| 619 | original16, 28-input manifest | `round-27/c2_count.py` pins cell | yes (not pinned) | c — r27 oracle/frozen input count |
| 588 | all 32 rows | `round-26/measure.py` verdict map | yes (not pinned) | c — decided-row population count (its selftest confirms 32 rows), not a selftest size |
| 593 | Self-test: 24 cases | `round-26/measure.py --selftest` (prose) | no | unmeasured — observed 24 passed, CURRENT-true |
| 770 | 41 cases | `scripts/citing_set_selftest.py` over `fixtures/citing-set/` (prose) | no | unmeasured — observed 45, STALE |
| 504 | 12 cases | `round-23/snapshot_probe.py` loopback regression (prose) | no | unmeasured — script emits exactly 12 case rows (normal, reaudit, 2 leaf, 7 tamper, blocked-redirect), CURRENT-true |
| 1025 | 29 fixtures | `link_preview_selftest.py` (prose, "round-34 additions") | no | b — round-34-era count, stale today |
| 1029 | 35 fixtures at `76fac3b` | same selftest (prose) | no | b — commit-pinned, verified 35 dirs at `76fac3b` |
| 1110 | 194 fixtures | `robots_audit_selftest.py` (prose, r38 narrative) | no | b — superseded by 204 |
| 1116 | now 204 fixtures | same (prose, r39) | no | unmeasured — observed 204/204, CURRENT-true |
| 1141 | now 179 fixtures | `sitemap_audit_selftest.py` (prose, r40) | no | b — superseded |
| 1156 | Selftest 183 fixtures | same (prose, r41) | no | b — superseded |
| 1167 | r41_* 225 fixtures | same (prose) | no | b — superseded |
| 1184 | selftest 235 fixtures | same (prose, r42) | no | unmeasured — observed 235/235, CURRENT-true |
| 998, 490 | 28 frozen cases; 32/32 | r34 `c1_matrix_count` matrix; r22 `matrix.py`/`cases.json` | no | c — matrix cells, not the tool selftest |
| 530 | 19 frozen targets | `round-24/measure_c1.py` | no | c — frozen target count |
| 1198, 1203 | 11/11, 3/3 | `c46_matrix.py` witnesses/controls | row 1198 pins cell | c — matrix cells |
| 1199 | 28 violations, 30 adjudicated | `citation_lint.py` run receipts at `7cdbaefd`/`ee43e66` | row 1199 pins cell | b — historical gate outputs |
| 1215 | 3 of 3; 13 of 18 | ledger predicate; mutation ladder | row 1215 | c — counter conditions / rejected families |
| 1216, 1234 | 8 of 8; 0/8 | counter predicate and base control | rows 1216/1234 | c — condition counts, not selftest size |
| 1233 | knowledge_files >= 46; 21 mismatches at `fcaf4b85` | readme-index predicate + historical control | row 1233 | c/b — counter predicate constant, historical receipt |
| 213 | all 7 checks (verdict map) | `c53_gate_truth.py` | yes (not pinned) | c — check count of the counter, no selftest tally claimed |
| 350 | 0/1/2/64 | exit-code list | no | n/a — not a tally |
| 146, 325 | 6/7; 4/6/7 | journal anomaly / error codes | no | n/a |
| 204, 319 | 60/60 | retired r10 claim, quoted as warning | no | b — explicitly retired history |
| 232, 263 | 3/10 | r9 link-rot baseline 2026-09-28 | row 232 / prose | c — link-rot observation |
| 252 | 2/18 vs 1/17 | hostname count correction | no | c |
| 900, 927 | 5/5 | round-30 `c1_reason_count.py` score | no | b — historical counter score |
| 960, 982 | 0/4, 3/4, 4/4 | concurrency controls r32 | no | b |
| 866 | 12 of 25 reason codes | uncovered-code count | no | c — absence count, not a selftest tally |
| 800 | (12) uncovered codes | reason-code census | no | c |
| 1021 | 101/102 | og:image floor arithmetic | no | c |
| 1005 | 0/28, 0/6, 0/13, 0/7, 0/2 | `c1_matrix_count.py` at `d08d8de` | decision table row | b — historical frozen-matrix receipt |
| 1013 | 0/5 | `c2_source_census.py` at `d08d8de` | decision table row | b |
| 1025 | 28/28 counter score | `c1_matrix_count.py` | prose | b — historical |
| 1193 | 2/2 rows | `c47_registry_count.py` | prose | b — historical counter receipt |
| 1111, 1114 | 20/20, 28/28, 20/28 | r37/r38 sealed+counter scores | prose | b |
| 1149, 1174 | 27 controls; 15 of 141 | pre-build control counts r40/r41 | prose | b/c |
| 30, 42 | 21 rows; 18 of 21 | fleet registry row count / CLI check coverage | no | c |
| 627, 659, 666-668 | 55/58, 58/58, 7 units/3 pairs, original57, 16, 29-case, Git30 | round-27 measurement numbers | no | c — pair/unit/review counts |

## POPULATION VERDICT:

The ten pinned rows are the right population: they are exactly the registry rows whose **self-test cell**
carries a self-assessed fixture/case tally. Every other registry row's self-test cell names the command
with no tally (freshness-sweep, c53_gate_truth, corpus-contract, canonical-audit, live-snapshot,
receipt-replay×2, accessibility-packet×2, source-recheck-counter, citing-set, knowledge-citing-count,
citing-set-frozen-count, source-snapshot) — verified by extracting column 5 of each row. Independent
re-measurement at `e48354b7` reproduces the contract's "Before" exactly: 3 rows match (base-path 45,
redirect 23, wave-ledger 19), 7 mismatch (source-recheck 101→106, robots 137→204, sitemap 150→235,
citation-lint 8→9, quote-truth 18→17/18-exit-1 unpinned, readme-index 35→44, yahoo-robots 50→54) —
i.e. `tally_mismatches=7 rows_checked=10`, the do-nothing control.

`link-preview-audit` is correctly excluded. Its self-test cell claims "45 fixture directories at
`b1cbbc39`" — a directory count pinned to a commit (verified: 45 dirs at `b1cbbc39`, so accurate
history) — while `python3 -B scripts/link_preview_selftest.py` at base prints `"cases": 46,
"passedOverTotal": "46/46"`, exit 0. Directories ≠ printed case total (and even the directory count
has since moved to 46): comparing them would be a false-positive mismatch, exactly as the contract
says.

## UNMEASURED SELF-ASSESSMENTS:

8 mentions outside the ten pinned rows state a selftest/probe case tally that C1's counter does not
measure (none are in any row's self-test cell, so all are out of scope by the contract's own rule):
- L212 `selftest 15/15` — freshness-sweep selftest now prints 36/36 (STALE unmeasured claim).
- L617 `29 independent consumer-input cases` — citing-set selftest now 45 (STALE).
- L770 `(41 cases)` — same selftest, also stale vs 45 (STALE).
- L593 `Self-test: 24 cases` — round-26 measure selftest, still 24 (true, unmeasured).
- L504 `12 cases` — snapshot_probe, still 12 (true, unmeasured).
- L1116 `now 204 fixtures` — robots selftest, still 204 (true, unmeasured; the ROW claim 137 is
  the stale one).
- L1184 `selftest 235 fixtures` — sitemap selftest, still 235 (true, unmeasured).
- L1184 chain note: the same selftest's row claims 150 — measured via the pinned row, so the
  sitemap *row* is covered; only the prose echoes above are unmeasured.
Three of the eight are themselves stale (15/15, 29, 41) — additional calibration debt the claim
leaves unmeasured, consistent with the contract's disclosed "~20 fixture-count mentions in SKILL.md
prose outside the ten rows".

## LIMIT SENTENCE:

C1 measures only the ten registry rows whose self-test cell states a tally; it knowingly leaves
eight further selftest-tally mentions outside those rows unmeasured — three of them (freshness-sweep
15/15, citing-set 29 and 41) already stale at the base revision — a disclosed limitation of scope,
not a defect in the predicate.

VERDICT: Population sound — ten pinned rows = all registry rows claiming a selftest tally; 8 unmeasured tally mentions outside them (3 stale) are a disclosed limit; link-preview-audit exclusion verified (45 dirs @b1cbbc39 vs 46/46 cases @base).
