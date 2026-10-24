# RerunC2Base — C2 before-measurement re-run (round 33, wave 1)

Scope: re-run the C2 counter `c2_pin_count.py` in an independent sandbox clone at
bc6c4a8d435473f3c30903210be30d9d6e3ef750, against revs 5777d5af79cac1ebf9144b348a9d274099e77338
(before) and bc6c4a8 itself (at), then compare with the L1 receipts.

## Sandbox

- Clone: /fast/scratch/hyaku/kake-r33/w1/RerunC2Base/clone
  (`git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone && git checkout -q bc6c4a8…`)
- TMPDIR: /fast/scratch/hyaku/kake-r33/w1/RerunC2Base/tmp (the counter only writes a
  TemporaryDirectory during c4, which is skipped at both revs since c1 fails)
- Counter script blob at bc6c4a8: 275476341e3a255cf2c4c7b3f9223561bd2e2668
  (`.ufo/waves/round-33/c2_pin_count.py`; uses only rev-parse/ls-tree/show/archive — read-only)
- Tools: python 3.14.8, git 2.56.0; no installs needed or made.

## Commands run (from /fast/scratch/hyaku/kake-r33/w1/RerunC2Base, GIT_* unset)

```
python3 -B clone/.ufo/waves/round-33/c2_pin_count.py --repo clone --rev 5777d5af79cac1ebf9144b348a9d274099e77338 > out-before-5777d5a.json   # exit 0
python3 -B clone/.ufo/waves/round-33/c2_pin_count.py --repo clone --rev bc6c4a8d435473f3c30903210be30d9d6e3ef750 > out-at-bc6c4a8.json   # exit 0
diff -u <lane>/verification/c2-before-5777d5a.json out-before-5777d5a.json    # no output — identical
diff -u <lane>/verification/c2-at-bc6c4a8.json     out-at-bc6c4a8.json        # no output — identical
```

## Observed outputs

Before (rev 5777d5af79cac1ebf9144b348a9d274099e77338), exit 0:
`met: 0` of 4; c1_retained false (all four retained entries false),
c2_row false (rowsFound 0, rowCells null), c3_section false (headingCount 0),
c4_truth false (skipped: requires c1). Same shape as L1 receipt.

At (rev bc6c4a8d435473f3c30903210be30d9d6e3ef750), exit 0:
`met: 0` of 4; identical condition and detail fields to the before run.

## Comparison with L1 receipts — byte-identical

sha256 (mine == L1 file):
- before: 55a5ab2e0be989c3806a2593f520bd10662647bf80f6cd47af12d2a6c542c3b7
- at:     e78127cca9d2ce1bcb403248ad8abdc99e44fd759585b2b9b7a782fa2de88b27

The receipts `.ufo/waves/round-33/verification/c2-*.json` are uncommitted
working-tree files (not in bc6c4a8); the counter itself (`git show rev:path`)
never reads them, so reproducibility is unaffected.

## Acceptance

- Exits: 0 and 0 — matches expectation (exit 0 = count ran; 2 reserved for unknown rev).
- met: 0 before, 0 at bc6c4a8 — agrees with receipts and with the declaration's
  "Before: met 0" (declaration commit only lands the counter; implementation is pending).
- Conditions: all four false at both revs; no condition flips spuriously.
- Differences: none — both my outputs are byte-identical to the L1 receipts.

## Notes for the L1

- At both revs the counter short-circuits c4 (requires c1), so
  `scripts/canonical_audit.py` was never executed; its in-counter correctness is
  unexercised here. When implementation lands, re-run must confirm c4 actually runs
  (manifest + subprocess path at c2_pin_count.py:157-170).
- Counter is faithful to the declared c2-row contract (S065, 11 cells, mined,
  2026-10-22, used-by) and heading contract ("## Round-33 ds4cc source pin 7fc6aa2f").

Not verified (out of scope): upstream commit anatomy, blob-id pinning vs upstream
(covered by sibling seats), c4 happy-path behavior, C1.
