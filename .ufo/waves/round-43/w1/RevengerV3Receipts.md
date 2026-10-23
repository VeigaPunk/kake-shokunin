DEFECT: v2_prefix32's v3 "met" is seed-dependent — 3 of 4 controls reproduce met; v2 failed 8/10 on one fresh seed.

# Scope
Re-ran committed round-42 counter v3 (`c42_count_v3.py`, sha256 `ce2d5a0ca2c3768ce2b1d7b9a57592817d7f16616ee7fb25989e580a70160acc`, verified)
against each control in `.ufo/waves/round-43/controls-r42/`, no `--seed`, vs r42 w2 L1 receipts (`.ufo/waves/round-42/verification/w2v3/L1-*.json`).

# Command (per tool, cwd lane root; exit 0 met / 1 not met)
`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count_v3.py --root . --tool-file .ufo/waves/round-43/controls-r42/<tool> --label RevengerV3-<sfx> --out /fast/scratch/hyaku/kake-r43/RevengerV3Receipts/<sfx>.json`

# Per tool: sha256 | my v3 receipt | r42 L1 receipt
- `M8-port-five-digits.py` `391608309640431acfc873d48e33189cf71a399faaa410ce6d65b910282bbb1f`
  - mine: met true, 10/10, ratios 0.986/1.441/1.366/1.203/1.168, exit 0, seed (receipt) — `v3-M8.json`
  - L1 : met true, 10/10, ratios 1.023/1.372/1.475/1.25/1.169, seed 215890093716836 → HOLDS
- `v1_casefold.py` `9993b842427d1592713309420626e46e42f1e56defab28b2f5349e6391cf4bc4`
  - mine: met true, 10/10, ratios 1.1/1.478/1.591/1.441/1.33, exit 0 — `v3-v1.json`
  - L1 : met true, 10/10, ratios 1.252/1.682/1.796/1.353/1.338, seed 204644689653110 → HOLDS
- `v2_prefix32.py` `eadf5df4b5c26059429a5dbffd2d87bcdbca6f460ba982c81360736e6856aa0f`
  - mine #1: met FALSE, 8/10, ratios 1.088/1.451/1.535/0.735/1.035, exit 1, seed 49580540867739, caught by A and E — `v3-v2.json`
  - mine #2: met true, 10/10, ratios 1.054/1.464/1.519/0.665/1.175, exit 0 — `v3-v2-re2.json`
  - L1 : met true, 10/10, ratios 1.038/1.471/1.602/0.699/1.127, seed 234865355777660 → OVERSTATED: reproducible but not robust; some seeds catch it
- `v4_hosttable.py` `dc8b6ecdcc638d20d34f66aaeadd8aa8ba798f5307c2fa8d80a876d2ae16ece7`
  - mine: met true, 10/10, ratios 1.018/1.379/1.559/1.365/1.126, exit 0 — `v3-v4.json`
  - L1 : met true, 10/10, ratios 1.066/1.443/1.664/1.392/1.161, seed 129858960042458 → HOLDS

# sha256 cross-check vs w2 reports — all four EQUAL
- M8 = MutBuildAuthority.md:22 `391608309640431a…` (same file renamed).
- v1/v2/v4 = CtlFreshCache.md:12-15 rows `9993b842…`/`eadf5df4…`/`dc8b6ec…` (committed names v1_casefold/v2_prefix32/v4_hosttable
  vs report names v1_commonprefix/v2_userinfocache/v4_uriokmemo — same bytes, renamed on commit).
- controls-r42/SHA256SUMS matches all four files.

# Finding
v3 catches v2_prefix32 in the equality runs on some seeds (mine: A+E unequal, 8/10). The v4 freeze receipt caught v2
at 7/11 (E,F,T2,T3). So "all four r42 controls must be met under v3" is wrong as a universal: v3's blindness to v2 is
stochastic (prefix-32-keyed table collides only when a run draws a shared-prefix pair with divergent parses). The L1
receipt's 10/10 is genuine but lucky; a rescore can land not-met. The kill-rule direction still holds — v2 met on the
recorded seed and meets on most seeds — but "counter v3 could not catch v2" is overstated: it catches it sometimes.

# r43 freeze receipts (v4 counter, for reference; `.ufo/waves/round-43/verification/freeze/r42ctl-*.json`)
M8 9/11 (F,T3); v1 9/11 (F,T2); v2 7/11 (E,F,T2,T3); v4 9/11 (F,T3); junk 0/11 — all not met under v4, consistent with freeze claims.

# Notes
No installs. Receipts + seeds: /fast/scratch/hyaku/kake-r43/RevengerV3Receipts/{v3-M8,v3-v1,v3-v2,v3-v2-re2,v3-v4}.json
