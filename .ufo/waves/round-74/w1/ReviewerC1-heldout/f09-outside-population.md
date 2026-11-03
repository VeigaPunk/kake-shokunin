# Mini SKILL.md fixture f09 — rows only for counters outside the frozen population

### Older rounds (context)

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| selftest-tally-counter | gate (historical from round 72; green at its round-56 pin, red at later tips by design) | `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision <commit>` | `0=met`; `1=not met` | ten documented selftests | pin receipt under round-72 controls | read-only | kake round 56 |
| gate-status-counter-v2-hostportable | gate (live; host-evaluability of the 28-member gate registry) | `python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root . --revision <rev>` | `0=met`; `2=unevaluable` | env selfcheck | agreement reported, never gating | read-only | kake round 66 |
| exploratory-absent-probe | gate (proposed; the counter file was never committed) | `python3 -B .ufo/waves/round-70/c99_absent_probe.py --revision <commit>` | `0=met`; `1=not met` | none | never landed | read-only | nobody |

None of the three rows names a counter of the frozen round-69..73 population; the third path is
permanently dead.
