# Mini SKILL.md fixture f10 — filename appears only in the Entry-command cell (real alias-row shape)

### Round 70 gate registry additions

Round 70 registers its pointer-audit counter under an alias, mirroring the registry's existing
alias rows.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| pointer-audit-counter | gate (live; calibration: SCORECARD evidence pointers resolve at the measured revision or carry a dated calibration annotation; predicate frozen in `.ufo/waves/round-70/contract.md` section C1) | `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root . --revision <commit>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --selftest` | pointer table frozen in the contract | read-only over committed bytes; scratch only | kake round 70 |

The counter's filename appears nowhere except inside the entry command.
