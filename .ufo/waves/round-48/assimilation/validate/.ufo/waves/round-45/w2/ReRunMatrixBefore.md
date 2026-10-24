# C1 before-receipt rerun

Axes: operability, freshness.

## Attack and execution

Re-ran the named before-stage matrix. To honor the lane read-only boundary, ran the unchanged command in an isolated copy at `/fast/scratch/hyaku/kake-r45/ReRunMatrixBefore`, with the original Git object store exposed read-only for the counter's revision lookups. Working directory: `/fast/scratch/hyaku/kake-r45/ReRunMatrixBefore`.

Exact command:

```sh
GIT_DIR=/home/vgpnk/Projects/shokunin/kake-shokunin/.git GIT_WORK_TREE=/fast/scratch/hyaku/kake-r45/ReRunMatrixBefore python3 -B .ufo/waves/round-45/c45_matrix.py --stage before
```

Verbatim decisive output:

```text
stage=before invalid_accepted=3 rejections_named=0 honest_witnessed=27 honest_build_met=3
MATRIX_BEFORE_PASS
```

The command returned exit status 0. Fresh receipt: `/fast/scratch/hyaku/kake-r45/ReRunMatrixBefore/.ufo/waves/round-45/verification/matrix/before.json`. It records `invalid_accepted=3`, `honest.exit=0`, `honest.valid=true`, `honest.witnessed=27`, and `honest.build_met=3`.

## Comparison with committed receipt

Committed receipt: `.ufo/waves/round-45/verification/matrix/before.json`.

- Driver path is unchanged: `.ufo/waves/round-44/c44_audit.py`.
- Driver SHA-256 matches exactly: `8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75` in both receipts.
- Result fields match: all three invalid fixtures have `exit=0`, `ok=true`, and no rejection classes; honest is valid with 27 witnessed and 3/3 builds met; totals are `invalid_accepted=3`, `rejections_named=0`, `honest_witnessed=27`, `honest_build_met=3`.
- Cohort paths are fresh-run paths with new UUID suffixes (expected path drift); the relative layout and fixture labels are unchanged:

| Cohort | Committed | Fresh |
|---|---|---|
| counter-error | `.ufo/waves/round-45/verification/matrix/runs/before/counter-error-0aad6b530615` | `.ufo/waves/round-45/verification/matrix/runs/before/counter-error-00da9caa14fd` |
| tool-absent | `.ufo/waves/round-45/verification/matrix/runs/before/tool-absent-2a0c1d171e0b` | `.ufo/waves/round-45/verification/matrix/runs/before/tool-absent-884c41f74032` |
| stale-planted | `.ufo/waves/round-45/verification/matrix/runs/before/stale-planted-681ac29dabb9` | `.ufo/waves/round-45/verification/matrix/runs/before/stale-planted-428e4536a098` |
| honest | `.ufo/waves/round-45/verification/matrix/runs/before/honest-453550700625` | `.ufo/waves/round-45/verification/matrix/runs/before/honest-ca79590228af` |

The recorded run timestamp also changed, as expected for a new execution. No unexpected result or driver drift observed.

## Verdict

**PASS — named attack confirmed.** The fresh isolated rerun reproduces the before receipt's 3/3 invalid acceptance and honest 27/27 plus 3/3 valid build result, exits 0, and matches the committed driver's SHA. Cohort UUIDs and timestamp are the only observed receipt drift.

## Files written

- Lane: `.ufo/waves/round-45/w2/ReRunMatrixBefore.md` (this report only).
- Scratch: copied inputs and run outputs are confined to `/fast/scratch/hyaku/kake-r45/ReRunMatrixBefore/`; the fresh receipt and four cohorts are under its `.ufo/waves/round-45/verification/matrix/` tree. No install performed.
