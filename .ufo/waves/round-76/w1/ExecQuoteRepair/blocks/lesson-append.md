
## Corrections

- **The deletion-control quote skipped an observed field (the contract's R6; corrected by round 76).** The
  `## Gate` bullet "Reject — deleting the failing row as a repair" quotes the deletion control as
  `files=15 append_only=false met=false`; no committed receipt line contains that fragment. The whole line
  in `.ufo/waves/round-75/controls/ctl-deletion.txt:1` is `C1v1 revision=afc73a87759b4218d54369b583e021b6e800de73 rows=27 live=15 files=15 mismatches=2 classes=E3 append_only=false met=false`.
  The landed deletion control at `.ufo/waves/round-75/controls/ctl-deletion-landed.txt:3` is `C1v1 revision=153fa2a9eda8d95618697186feb18574cc7daae1 rows=27 live=15 files=15 mismatches=3 classes=E3 append_only=false met=false missing_frozen=1`.
  The observed mismatches=2 classes=E3 sits between files=15 and append_only=false; the verdict the round
  drew (append_only=false, so deletion is not a repair) is unaffected. Appended 2026-11-03 by the round-76
  C1 repair; the historical bullet is not rewritten. `[r76-correction 2026-11-03]`
