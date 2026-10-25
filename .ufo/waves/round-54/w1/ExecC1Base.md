# ExecC1Base — round-54 C1 do-nothing control

Seat: `L1Kake54.ExecC1Base` (leaf, read-only counter wave)
Date: 2026-10-25

## Command (verbatim, committed-byte control)

    python3 -B .ufo/waves/round-54/c54_s374_calib.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 68228b2d74e7930ae4f07e90e382a0d03ab80c7b

Executed with cwd = `/home/vgpnk/Projects/shokunin/kake-shokunin` (the relative
script path resolves to the committed counter inside that checkout). No worktree
files were read by the counter; it reads `git show <rev>:<path>` only.

## Exact output

      PASS C1.1_body: [] {'occurrences': 1}
      PASS C1.2_cells: [] {'suspect_cells': 1}
      FAIL C1.3_correction: ['no valid r54 correction block (exact quote + crawl token)'] {'block_offset': -1}
      FAIL C1.4_mismatch: ['mismatches=1'] {'mismatches': 1}
    S374 qualifier: mismatches = rendered cells missing the crawl qualifier and not superseded by an r54 correction block; met when 0
    mismatches=1 met=False
    EXIT=1

## Predicate / exit confirmation

- Frozen predicate (contract.md): "S374 qualifier: mismatches = rendered cells
  missing the crawl qualifier and not superseded by an r54 correction block;
  met when 0."
- Contract do-nothing receipt requires at base `68228b2d74e7930ae4f07e90e382a0d03ab80c7b`:
  `mismatches=1 met=False` and exit 1.
- Observed: `mismatches=1 met=False`, `EXIT=1`, shell rc = 1.
- Result: **control reproduces the committed receipt exactly.** Predicate not met
  at base, as required for a valid do-nothing control.

## Check-level detail

- C1.1_body PASS — retained round-52 body
  `.ufo/waves/round-52/sources/S374.html` at the pinned revision contains the
  exact quote 「このリンク先のウェブページの巡回を推奨していない」 once
  (occurrences=1). Claim is evaluable.
- C1.2_cells PASS — entry `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`
  contains 1 suspect rendering cell (endorsement/refusal vocabulary without
  crawl vocabulary), matching the contract's "Before: mismatch count = 1".
- C1.3_correction FAIL — no `[r54-correction 2026-10-25]` block with the exact
  quote plus an English crawl token exists at base (block_offset=-1).
- C1.4_mismatch FAIL — 1 suspect cell not superseded by a valid correction block.

## Files changed / writes

- No repository writes. Sole file written by this seat is this report:
  `.ufo/waves/round-54/w1/ExecC1Base.md` (report-path exception).
- No tool installs performed; python3 and git already present. No installs to record.

## Retained evidence

- Counter script: `.ufo/waves/round-54/c54_s374_calib.py` (committed, hashline
  snapshot at run time). Pinned base revision:
  `68228b2d74e7930ae4f07e90e382a0d03ab80c7b` (lane master tip at round open,
  per `.ufo/waves/round-54/contract.md`).

## Risks / blockers

- None. Control is deterministic committed-bytes only (`git show`); no network,
  no worktree dependence, no writes. Findings only; no admission claimed.
