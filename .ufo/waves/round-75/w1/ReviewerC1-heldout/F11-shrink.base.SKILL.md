# SKILL

### Round 75 gate registry additions

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| broken counter | gate (offline) | `python3 -B scripts/bad11.py --root .` | 0=met | the gate has no selftest of its own | dash | reports only | ReviewerC1 |
| ok counter | gate (offline) | `python3 -B scripts/ok11.py --selftest` | 0=met | `python3 -B scripts/ok11.py --selftest` (2/2) | dash | reports only | ReviewerC1 |
| t3 counter | gate (offline) | `python3 -B scripts/t3b.py --selftest` | 0=met | `python3 -B scripts/t3b.py --selftest` runs f1 f2 f3 (3/3) | dash | reports only | ReviewerC1 |
