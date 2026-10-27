# MutationBaseReachability — round 62

Detector: frozen `.ufo/waves/round-62/c62_calibration.py` (SHA-256 `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`), invoked with `python3 -B <counter> --root <fixture> --revision HEAD`. Each fixture was a private detached worktree at base `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`; only the named corpus file was appended in quote-only/criterion-only, and do-nothing had an empty commit. Worktree roots were confirmed with `git rev-parse --show-toplevel` before fixture commits. No lane files or counter predicates were modified.

| Case | Isolated change | Detector output | Exit | Verdict |
|---|---|---|---:|---|
| Base | No change | `revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false` | 1 | Expected baseline failure; not a killed mutant. |
| Do-nothing | Empty commit only | `revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false` | 1 | Same baseline failure. |
| Quote-only | Appended `Round-62 correction` plus exact quote and `S432 §3.6` to knowledge file | `revision=HEAD disagreements=1 unresolved=1 quote_correction=1 criterion=0 lesson_gate=0 source_row=1 met=false` | 1 | Quote recognized; unresolved disagreement remains while criterion/gate absent. |
| Criterion-only | Appended `substantive located quote` and spotcheck filename to QUALITY | `revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=1 lesson_gate=0 source_row=1 met=false` | 1 | Criterion recognized; unresolved disagreement remains while quote/gate absent. |

Exact counter command prefix in all cases: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py --root /fast/scratch/hyaku/kake-r62/MutationBaseReachability/<case> --revision HEAD`.

The two single-axis variants are correctly insufficient for the frozen composite predicate. The `lesson_gate` remains 0 in every case; `source_row` remains 1. SHA-256 of frozen counter before probing: `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`. Scratch worktrees and directory were removed after runs. A restored-byte replay was not run: no behavior-bearing counter mutation was made, and this probe was limited to base/do-nothing/quote-only/criterion-only variants.