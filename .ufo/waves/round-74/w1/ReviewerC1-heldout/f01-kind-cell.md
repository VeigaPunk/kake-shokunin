# Mini SKILL.md fixture f01 — filename in a non-first cell (Kind); kill-rule f2 shape

### Round 71 gate registry additions

Round 71 registers its calibration counter with an alias row, in the style the registry already
uses for older gates.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| calibration-counter | gate (live; calibration: the c71_calibration.py counter scores the lane's registry against the observed round-69..73 population; predicate frozen in `.ufo/waves/round-71/contract.md` section C1) | `python3 -B .ufo/waves/round-71/c71_calibration.py --root . --revision <commit>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-71/c71_calibration.py --selftest` | population frozen in the contract; base receipt is the control | read-only over committed bytes; scratch only | kake round 71 |

The counter runs offline over committed bytes only.
