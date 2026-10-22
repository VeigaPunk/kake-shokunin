# RunC1Counter — C1 independent re-run of the counting command

Seat: KakeR28a3.RunC1Counter (leaf). Weather: godspeed. No installs were
needed; no tool was installed or updated this wave.

## What I ran

Two independent runs of the C1 counter at the two declared revisions, each
with its own scratch dir, stdout redirected to a result file, exit code
captured:

1. Base (round-27 defect state), scratch `a`:
   ```
   cd /home/vgpnk/Projects/shokunin/kake-shokunin \
   && TMPDIR=/fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter \
      python3 -B .ufo/waves/round-28/c1_interface_count.py \
        --root . --revision 22c1669c1fec83d1a0769de6b9ce686c75657e66 \
        --scratch /fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter/a \
        > /fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter/before.json
   echo "EXIT=$?"   ->   EXIT=1
   ```
2. Repair commit, scratch `b`:
   ```
   cd /home/vgpnk/Projects/shokunin/kake-shokunin \
   && TMPDIR=/fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter \
      python3 -B .ufo/waves/round-28/c1_interface_count.py \
        --root . --revision b5d423fc02057f67a6f3a255808313ce40d29069 \
        --scratch /fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter/b \
        > /fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter/after.json
   echo "EXIT=$?"   ->   EXIT=0
   ```

Wall times: before run 41.28 s, after run 1.30 s (counter exits 1 when
passed < total, so exit 1 at base is the expected failure signal, not a
harness error).

## Results

| Metric | Base (22c1669) | Repair (b5d423f) |
|---|---|---|
| passed/total | 4/15 | 15/15 |
| defect passed/total | 0/11 | 11/11 |
| control passed/total | 4/4 | 4/4 |
| counter exit | 1 | 0 |

Per-case (ids in output order): U1-population-fifo, U2-ledger-fifo,
U3-population-deep-json, U4-ledger-deep-json, A1-corpus-absent-working-tree,
A2-corpus-absent-git, A3-corpus-empty-working-tree, A4-corpus-blob-git,
A5-population-unreachable-id, A6-blank-revision, A7-nested-git-root,
K1-valid-clean-working-tree, K2-valid-clean-git,
K3-valid-failed-missing-pair, K4-fixture-selftest.

- Base: all 11 defect cases FAIL, all 4 controls PASS.
- Repair: all 15 cases PASS.

## Comparison vs verification JSONs

Structurally compared (Python) the new outputs against
`.ufo/waves/round-28/verification/c1-before.json` and
`c1-after-b5d423f.json`: top-level summary keys, case id sets, per-case
`kind`/`attacks`/`passed`, `reasons`, and `observed` exit/verdict/finding.

- Base: 0 per-case differences vs `c1-before.json`.
- Repair: 0 per-case differences vs `c1-after-b5d423f.json`.

## Evidence pointers

- New before run: `/fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter/before.json`
  (passed 4, defect 0/11, control 4/4; case U1 fails at before.json:15).
- New after run: `/fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter/after.json`
  (passed 15, defect 11/11, control 4/4; case U1 passes at after.json:15).
- Verification originals: lane
  `.ufo/waves/round-28/verification/c1-before.json` and
  `c1-after-b5d423f.json`.
- Counter source: lane `.ufo/waves/round-28/c1_interface_count.py`
  (main returns 1 when passed != len(cases), line 331).

## Caveats / not verified

- I did not re-audit the counter script's own logic or the round-27 defect
  records; this is a re-run of the counting command as specified.
- Network sources (S036-S039) are out of scope for this seat; C2 is a
  different wave.
- No file in the lane repo was mutated; I only wrote this report plus the
  scratch outputs under `/fast/scratch/hyaku/kake-r28a3/w1/RunC1Counter/`.

## Risks / blockers

- None for C1 counting. The counter's `--scratch` paths are per-revision
  (`a`/`b`), so the two runs cannot collide.
