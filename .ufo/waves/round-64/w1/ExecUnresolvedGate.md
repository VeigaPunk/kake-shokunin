# ExecUnresolvedGate — round 64

## Verdict

The frozen C1 counter's unresolved gate resisted both requested spot-file attacks. F1 removed the sole qualifying S432/Disagree line and returned `met=false` despite every other printed gate being green. F2 duplicated that line and returned `met=false` with `disagreements=2`, `lesson_gate=1`, and `unresolved=1`.

## Evidence

Counter implementation: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:198` counts qualifying spot lines; `:267` computes `unresolved = max(disagreements - (1 if lesson_gate else 0), 0)`; `:268-270` requires both `disagreements >= 1` and `unresolved == 0` in `met`.

Fixtures were cloned from the lane and checked out at measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`; each fixture's `git rev-parse --show-toplevel` was asserted equal to its explicit scratch directory before its fixture commit. The retained tree content, including all pinned blobs and lesson/quality/knowledge/sources, was otherwise unchanged. The only edits were in `corpus/lessons/round-61-verifier-spotcheck.md`.

F1 revision: `1d198368980a923eccfa7a2a4a1801db1c9c0d32`.
Command (run from fixture root):
`python3 -B .ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/ExecUnresolvedGate/F1 --revision 1d198368980a923eccfa7a2a4a1801db1c9c0d32`
Exit: `1`
Output:
```
revision=1d198368980a923eccfa7a2a4a1801db1c9c0d32 disagreements=0 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
```

F2 revision: `3ffbdea9413c136ae774628ec7d8dfe8be9da224`.
Command (run from fixture root):
`python3 -B .ufo/waves/round-64/c64_calibration.py --root /fast/scratch/hyaku/kake-r64/ExecUnresolvedGate/F2 --revision 3ffbdea9413c136ae774628ec7d8dfe8be9da224`
Exit: `1`
Output:
```
revision=3ffbdea9413c136ae774628ec7d8dfe8be9da224 disagreements=2 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
```

## Risks / blockers

None observed for this scoped attack. No tools installed. No lane files, frozen instruments, counters, receipts, contracts, or lessons were modified.
