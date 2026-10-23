# RerunBuildB — w2 (falsify): T5/T2 margin re-measurement

Verdict: **margins hold** — no finding. Both fresh unseeded counter runs at lane tip
`721310b19af88d3c43c01647d3ce29d51e6e3b96` met the predicate; every ratio is below 2.0.
Largest ratio seen across all five scored runs (L1's three + these two) is T2 = **1.720**
(r1), distance from 2.0 = **0.280**; the build's closest-to-limit margin is T2, not T5.

## Commands (exact)

```
timeout 900 prlimit --as=8000000000 -- python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-42/c42_count_v3.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 721310b19af88d3c43c01647d3ce29d51e6e3b96 \
  --label RerunBuildB-r1 --out /fast/scratch/hyaku/kake-r42w2/RerunBuildB/r1.json   # exit 0
timeout 900 prlimit --as=8000000000 -- python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-42/c42_count_v3.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 721310b19af88d3c43c01647d3ce29d51e6e3b96 \
  --label RerunBuildB-r2 --out /fast/scratch/hyaku/kake-r42w2/RerunBuildB/r2.json   # exit 0
```

No `--seed` either run (random seeds recorded: r1 245640470013593, r2 106089532423973).
`--revision` and `--tool-file` are mutually exclusive in v3 (first attempt passed both →
argparse exit 2; corrected).

## Artifacts

- Counter: `…/.ufo/waves/round-42/c42_count_v3.py` sha256 `ce2d5a0c…` (matches L1).
- Build at revision (tool blob): sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` — identical to the frozen build's tool.
- Receipts: `/fast/scratch/hyaku/kake-r42w2/RerunBuildB/r{1,2}.json`.

## Ratios (median cand CPU / median base40 CPU; exact)

| run | T1 | T2 | T3 | T4 | T5 |
|-----|-----|-----|-----|-----|-----|
| r1 | 1.027 | **1.720** | 1.386 | 1.268 | 1.121 |
| r2 | 1.045 | 1.260 | 1.281 | 1.241 | 1.160 |
| L1-1 | 1.058 | 1.280 | 1.396 | 1.264 | 1.168 |
| L1-2 | 1.006 | 1.319 | 1.390 | 1.235 | 1.093 |
| L1-3 | 0.976 | 1.382 | 1.427 | 1.276 | 1.096 |

Largest ratio seen: **T2 = 1.7197495453572955** (r1) → 0.28025 below 2.0.
Equality: 10/10 runs equal (10,229 generated values + five timing files) each; `met: true` both.
r1 T2 is the highest T2 observed across all runs (L1 max 1.382); T2 is the noisiest shape
(1.26–1.72), T5 stable (1.09–1.17).

## Checks

- Predicate "≤ 2.0 on each of five shapes": holds (max 1.720). Held, not overstated.
- Equality with round-41 tool on every generated run: holds (10/10 both, exit 0).
- T5/T2 margins: verdict above.
- No control produced; no tool mutation (reads only); no installs needed.

## Gaps

- `--revision` path validated against the tip only; earlier revisions not re-run (out of scope).
- 5 reps/shape per counter; T2 spread (1.26–1.72) suggests the margin is ~0.28–0.74 → no
  credible approach to 2.0 without the work being skipped (kill rule covers that).
