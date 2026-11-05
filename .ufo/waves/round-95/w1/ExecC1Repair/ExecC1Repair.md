# ExecC1Repair — round 95 (R94-5 row files, R94-9 registry rows)

Seat: ExecC1Repair. Base: fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3 (SKILL.md bytes via git show). Read-only on the lane tree; nothing mutated, no git writes.

VERDICT: REPAIR-DIFF 15 predicted-E5=0   (15 edited rows + 5 inserted registry rows; prediction, frozen counter NOT run)

## Artifacts (this directory)
- repair.diff — unified diff against git show fdd5fdbe:SKILL.md
- repairs.md — per edited row: base line, row first cell, old token, new file, cat-file kind/size
- registry-rows.md — the five R94-9 rows and provenance notes
- predict.txt — prediction receipt lines

## Checks run (command -> rc)
- sha256 c95_selfassess.py = 8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193 (match); c95_conditional.py = f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312 (match). Files live at `.ufo/waves/round-95/` (not `controls/`); the digests list is `controls/instrument-sha256.txt`, present at 8f638b59.
- `git apply --check repair.diff` in a scratch copy of base bytes -> rc 0; `git apply` -> rc 0; result equals the intended patched bytes (sha prefix 2349de2beb12).
- Ancestry: fdd5fdbe -> 43cdd9fc -> 8f638b59 (all `merge-base --is-ancestor` rc 0).
- E5 replication (c95_selfassess rule: backticked `scripts|corpus|.ufo` tokens in SKILL rows, brace-expanded, must be non-empty regular blobs):
  - base at fdd5fdbe: 15 row occurrences, 13 distinct tokens (matches the counter's base E5=15).
  - patched at fdd5fdbe: 6 findings, all round-95 paths absent before the instruments commit (expected).
  - patched at 8f638b59 (tip proxy, contains 43cdd9fc): 0 findings. Predicted E5=0.
- Identity replication: 255 base rows -> 260 patched rows; every base first cell present; no row's path-token count shrank (edits are one-for-one).

## Findings and deviations (reported, not silently resolved)
1. Count: 15 directory rows, not 13. `.ufo/waves/round-85/w1/ExecRegistry/` occurs in three rows (1535/1536/1537). The 13 in the seat list are distinct tokens; the base E5=15 is per row occurrence.
2. `.ufo/waves/round-85/w1/ExecRegistry/registry-rows.mjson` (named in the seat spec) does not exist at fdd5fdbe. Used `c1-base.json` (728 B blob) from the same directory.
3. Row 1588 has a brace group `{expected-ledger.json,age-cases.json,snapshots/}` (one token). The directory moved to prose; the single backticked blob `expected-ledger.json` keeps the count at 1.
4. R94-5 review: the freeze requires a non-author seat to review the 13 rows. This seat authored the choices; the L1 must route the row review to a non-author seat.
5. c94_selfassess.py (fdd5fdbe, line 598): `met` is true when `skip_battery` is set, so `--skip-battery` can print `met=true`. This is the round-94 closure defect c95 removes; recorded in the c94 registry row, not repaired (instrument frozen).
6. c94_conditional.py docstring still says "Round-93 C2 counter" (copy-paste). Recorded, not repaired.
7. c93/c94 commands and all `--selftest` commands are derived from each script's argparse at fdd5fdbe; the freeze names only the c95 commands.
8. The five round-95 registry rows cite round-95 files, which exist only from the instruments commit 43cdd9fc onward. The L1 must apply the diff on a tip at or after 8f638b59; on fdd5fdbe alone the prediction is E5=6.

## Tooling
No tools installed or updated. No subagent dispatched (no dispatch tool available to this seat; leaf). No sysctl touched.

## Hand-off to L1
- Apply repair.diff to the integration tip (after 8f638b59 or later) and run the frozen counter once: `python3 -B .ufo/waves/round-95/c95_selfassess.py --root . --revision <REV>`. Predicted: E5=0; the other classes are outside this seat's scope.
- Route the row-by-row review of the 15 edited rows to a non-author seat (R94-5).
