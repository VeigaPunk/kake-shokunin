| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |
|---|---|---|---|---|---|---|
| broken | gate | `python3 -B scripts/broken.py` | `0=clean`; `1=failed` | `python3 -B scripts/broken.py --selftest` | none | kake |
| net | probe | `python3 -B scripts/net.py` | `0=clean`; `1=failed` | `python3 -B scripts/net.py --selftest` | none | kake |
