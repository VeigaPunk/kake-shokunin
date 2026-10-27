# ReviewerContractTimeline

ATTACKS: Contract amendment chronology, amendment labels/effect, and predicate sentence consistency between contract.md and contract.json.

TIMELINE:

- Base: `97cdc122379711c2b02a8970752c8782da3ac81d`.
- Contract v1 commit `b3b9e29ceb388ab1795c0c399703df5172b298ce` at 01:12:42 -0300; it declares C1–C3, shape and pre-data process, and the base setup.
- Amendment/counter freeze commit `1ea305904933ac0f57e84ac1e7a8207e486f577d` at 02:25:50 -0300 includes A1–A9, A3a, version-1 counters, base receipts and selftests, and w1 reports/results. The final B1 build is `8b33fd248d126b48d838af5c38bc175850f41a09` at 02:37:02 -0300.
- Evidence timestamps are consistent with the freeze ordering: e.g. A1 origin report `w1/EntryUserTriggered.md` records the L1 ruling and is present before freeze; A2 report `w1/ExecC1Registered.md` is timestamped 01:22:27 -0300; A3a origin `w1/ExecC1Data52.md` is timestamped 01:22:15 -0300. The earliest listed after-state counter receipt (`controls/base-c2-guard-cases.txt`) is timestamped 02:17:43 -0300, before the 02:25:50 freeze commit; however it is a base-state control, not an after-state score. The freeze commit records the controls as frozen before any after-state score, and the subsequent B1 commit is later.
- Conclusion: no evidence found that an amendment was introduced after an after-state score. Available history supports amendments and v1 freeze preceding the B1 after-state. Reports' filesystem timestamps are corroborative only; git commit chronology is the primary evidence.

AMENDMENTS:

| ID | Claimed label | Actual effect / assessment |
|---|---|---|
| A1 | Mixed rationale; loosening plus tightening | Adds `<h1>` to allowed anchors (loosens); requires nearest preceding heading and the row anchor to name it (tightens). Honest. |
| A2 | Disambiguation | Drops ambiguous optional argument segments, including `[--base <rev>]` and no-placeholder options; narrows command interpretation. Tightening/clarification, accurately described. |
| A3 | Tightening | Restricts executable command/environment/args, forbids selftest, constrains root and shell metacharacters. Accurate. |
| A4 | Tightening | Freezes member paths/blob ids and rejects missing, changed, or extra population files. Accurate. |
| A5 | Tightening | Adds exact exit requirements for historical/never-met labels and validates label/pin structure. Accurate. |
| A6 | Tightening | Detects duplicates across rendered tables and enforces cell structure. Accurate. |
| A7 | Tightening | Restricts source of scorecard data and requires unique tables/rows and exact scores. Accurate. |
| A8 | Tightening | Requires exact finding/summary output, reducing permissive case acceptance. Accurate. |
| A9 | Tightening | Adds scope, correction-run, parsing, date, receipt, ancestry and footer constraints. Accurate. |
| A3a | C1 exception before freeze; not explicitly labelled tightening/loosening | Carves out one SELF_CHECKOUT member with an exact no-argument command because it cannot accept the general `--revision` contract. This loosens A3's general command constraint for one identified member, but is a disclosed compatibility exception, not hidden scope relaxation. |

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| none | — | No actionable timeline, amendment-label, or predicate drift defect found. | `git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --format='%H %ci %s' 97cdc122379711c2b02a8970752c8782da3ac81d..8b33fd248d126b48d838af5c38bc175850f41a09`; `stat -c '%y %n' .../w1/*.md .../controls/*`; contract text/JSON predicate comparison | — |

Predicate check: contract.md and contract.json carry identical frozen sentences for C1 (`met: members == 28 AND mismatches == 0 AND scores_held == 3`), C2 (`met: cases_passed == 24 of 24`), and C3 (`met: conditions_passed == 9 of 9`). Command read the frozen JSON and markdown from commit `1ea305904933ac0f57e84ac1e7a8207e486f577d`; all three matched exactly.

VERDICT: Timeline and amendment disclosures are consistent with the available commit/report evidence; no actionable defect found in this scope.