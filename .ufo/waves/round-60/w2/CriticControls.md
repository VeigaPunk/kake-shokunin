# CriticControls

ATTACKS: Cheap, deliberately weak controls against frozen C1/C2/C3 version-1 judges at B1 scale. Axes: calibration (C1), operability (C2), sourced freshness (C3). The assignment specified how to judge each control; I inspected the frozen source and committed base-control receipts, but did not run new controls in scratch. No result below is represented as a fresh execution.

CONTROLS:

| Claim | Control | Result |
|---|---|---|
| C1 | 12 unregistered rows / junk cells / label every member live | Counter selftest exposes fixtures for unregistered members and junk rows, but not a unified 12-member “junk rows / everything live” adversarial control. Existing observed base receipt reports 14 mismatches, 12 unregistered, plus live c53 failure and historical c57 receipt-pin failure: `controls/base-c1-gate-status.txt` lines 3–54. Thus the actual base population fails; exact requested combined control was not run. |
| C2 | Clean-case-only tool; byte-prefix port; ignore tags | Existing version-1 selftest receipt scores the clean-only `always_clean_summary` 7/24 (lines 3–5), byte-prefix port 8/24 (line 7), and reference 24/24 (line 8): `controls/c2-selftest.txt`. The requested ignore-tags-only tool was not run / not present as a named control. |
| C3 | Rows only, no entries | Not run. The supplied `controls/base-c3-quote-truth.txt` measures the base state, not a rows-only mutation. |

FINDINGS:

| Severity | Target file:line | Issue | Evidence command | Fix |
|---|---|---|---|---|
| low | `.ufo/waves/round-60/controls/c1-selftest.txt:3-80` | C1 selftest covers many structural and score mutants, but does not evidence the specifically assigned batch control with 12 junk/incomplete registrations and all members labelled live; base receipt does show expected failing population. | `cat .../controls/c1-selftest.txt; cat .../controls/base-c1-gate-status.txt` (outputs referenced above) | Add one explicit combined negative fixture and assert its mismatch classes/count. |
| low | `.ufo/waves/round-60/controls/c2-selftest.txt:3-9` | C2 has strong observed clean-only and byte-prefix negative controls; no explicit ignore-tags-only mutant is evidenced. This is a control-coverage gap, not evidence the counter accepts it. | `cat .../controls/c2-selftest.txt` | Add a tool that otherwise implements the rule but treats hidden/comment/code-span tags as visible; assert K9/K10 reject it. |
| low | `.ufo/waves/round-60/controls/base-c3-quote-truth.txt` | No rows-only/no-entries C3 control evidence was located; do not infer it passes or fails. | `read` of the named base receipt; no modified fixture execution | Add a rows-only fixture and require C1/C2/C4–C9 to fail as applicable. |

VERDICT: The available C1/C2 receipts falsify do-nothing and simple clean-only/byte-prefix cheats; C1 combined junk batch and C2 ignore-tags and C3 rows-only controls remain unrun, so no further counter-acceptance claim is established.
