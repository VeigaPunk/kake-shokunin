# kake round 78 — contract amendment 4 (terms only, before any after-state)

Recorded 2026-11-03 after ExecC3Matrix flagged that amendment 3 §C4's exit column contradicts
the frozen exit alphabet. No C3 after-state exists (the tool is still being written; no case has
been scored). This amendment corrects the **exit column only**; nothing else in §C4 changes.

## D1 — exit code per case follows the alphabet

The frozen alphabet is `0 = all checks match`, `1 = any finding`, `2 = input or check fault`,
`64 = usage`. Amendment 3 §C4 printed `0` for the finding cases, which is inconsistent with it.
Corrected rows (exit `1`, effective/findings unchanged from §C4):

| id | exit | findings |
|---|---|---|
| g11_max_snippet_invalid | 1 | invalid_value |
| g13_unavailable_invalid | 1 | invalid_value |
| g15_empty_content | 1 | empty_content |
| g16_unknown_directive | 1 | unknown_directive |
| g19_body_tag_respected | 1 | tag_outside_head |
| g23_noarchive_ignored | 1 | ignored_rule |
| g31_missing_content | 1 | empty_content |
| g32_nocache_ignored | 1 | ignored_rule |

Every remaining exit-0 row of §C4 stays `0`; g34 stays `2` with `error=missing_file` and g35 stays
`2` with `error=duplicate_check_id`. A finding and a matching effective set coexist (g19 is the
clear case): `correct` compares all three fields, so a finding never suppresses the effective list.

`[r78-correction 2026-11-03]`

## D2 — a case whose findings are non-empty expects exit 1

This is a restatement, not a new rule: `expect.json` for a finding case carries
`{"exit":1,"effective":[…],"findings":[…]}`. The matrix counts a case wrong when the tool's exit,
effective list or finding list differ; a tool that prints the right findings but exits 0 fails.
