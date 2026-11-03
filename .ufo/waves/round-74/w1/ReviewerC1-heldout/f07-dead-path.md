# Mini SKILL.md fixture f07 — single row whose entry-command path is dead; kill-rule f4 shape

### Round 73 gate registry additions

Round 73 registers its wave-pointer counter below.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| c73_wave_pointers.py | gate (live; calibration: round-72 receipt pointers resolve at the measured revision or carry a dated correction; predicate frozen in `.ufo/waves/round-73/contract.md` section C1) | `python3 -B .ufo/waves/round-73/c73_wave_pointers_missing.py --root . --revision <commit>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | `--selftest` | pointer table frozen in the contract | read-only over committed bytes; scratch only | kake round 73 |

The row names the counter correctly; the entry command's path does not exist in the tree.
