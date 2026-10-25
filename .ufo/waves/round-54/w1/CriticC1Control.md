# CriticC1Control — cheapest do-nothing control vs frozen C1 counter

**Verdict: the do-nothing control does NOT reach target. Design not invalidated by this attack.**

## Instrument used

The frozen counter is the committed blob `HEAD:.ufo/waves/round-54/c54_s374_calib.py`
(landed in `acae1dc` "round-54: freeze claims and calibration controls"; the script does
not exist at base `68228b2d` itself — base is the measurement target, HEAD carries the
instrument). Run verbatim from the committed blob:

```
git show HEAD:.ufo/waves/round-54/c54_s374_calib.py \
  | python3 -B - --root . --revision 68228b2d74e7930ae4f07e90e382a0d03ab80c7b
```

## Cheapest do-nothing variants attempted (all read-only)

| # | Variant | Result |
|---|---------|--------|
| 1 | Counter at full base hash, untouched worktree | `mismatches=1 met=False`, **EXIT=1** |
| 2 | Counter at abbreviated base `68228b2d` | identical output, **EXIT=1** |
| 3 | Worktree already carries the repair (uncommitted `M corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`, contains `[r54-correction 2026-10-25]` at line 54) | still `met=False` — counter reads `git show <rev>:<path>` committed bytes only, so an uncommitted repair cannot suppress the control |
| 4 | Pre-entry revision `73c22a36` (parent of `5422ff3`, which added the Yahoo entry — a state where the repair is literally impossible) | `FAIL C1.2_entry … missing`, `met=False`, **EXIT=2** |
| 5 | Empty tree `4b825dc…` | `FAIL C1.1_body … missing`, `met=False`, **EXIT=2** |

Run 1 output verbatim:

```
  PASS C1.1_body: [] {'occurrences': 1}
  PASS C1.2_cells: [] {'suspect_cells': 1}
  FAIL C1.3_correction: ['no valid r54 correction block (exact quote + crawl token)'] {'block_offset': -1}
  FAIL C1.4_mismatch: ['mismatches=1'] {'mismatches': 1}
S374 qualifier: mismatches = rendered cells missing the crawl qualifier and not superseded by an r54 correction block; met when 0
mismatches=1 met=False
EXIT=1
```

Matches the committed receipt `controls/base-c1-s374.txt` byte-for-byte
(md5 `48833c0…` equal worktree vs HEAD). No `[r54-correction` marker exists anywhere
at base (grep of `git show 68228b2d:corpus/knowledge/…` — 0 hits), so no pre-existing
marker can satisfy C1.3 for free.

## Design notes favorable to the counter

- Committed-bytes-only reads make the worktree-repair spoof (variant 3) futile; the
  repair must land in a commit to count, which is exactly the claim's "After" state.
- Genuinely discriminating: exit 1 (not met) vs exit 2 (unevaluable) both observed
  live — not a constant `met=True` stub (the contract's junk-control clause).

## Defect found (collateral, not a design invalidation)

The **worktree copy** of `c54_s374_calib.py` is a mutated, broken variant (uncommitted
`git diff` vs HEAD): it replaces `CRAWL_RE`/`EN_CRAWL_RE` with `NEGATIVE_CRAWL_RE` but
still references `CRAWL_RE` (line 89) and `EN_CRAWL_RE` (line 183) and drops the
`corr_at` assignment. Executing it crashes:

```
NameError: name 'CRAWL_RE' is not defined   (line 89, run_checks)
EXIT=1
```

Exit code coincidentally stays 1, but it is a crash, not a verdict — `mismatches=` is
never printed, and a repaired tree would crash identically (no discrimination).
**Smallest safe correction:** any seat needing the counter must run the committed
blob (`git show HEAD:…`) or commit the diff before use; the lane should either drop
or complete this worktree mutation before the executor wave, since the contract's
`argv=` line names the worktree path.

## Impacted axes

- Correctness of control: holds at frozen blob.
- Operability hazard: worktree mutant breaks verbatim `argv=` from the receipt.

No installs performed. Read-only throughout.
