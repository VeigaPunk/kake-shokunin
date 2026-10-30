# Round 64 after-receipt reproduction

Scope: pristine detached checkout of T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`, created under `/fast/scratch/hyaku/kake-r64/ExecAfterReproduce/repo` from the lane repository. `git -C ... rev-parse --show-toplevel` was asserted equal to that path before checkout. No lane files or frozen artifacts were changed.

## Evidence

- C1: command `python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb` (from the detached checkout) returned exit 0 and exact stdout `revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`. This matches `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/after-c1.txt:1-3` in semantic result and exit status.
- C2: command `python3 -B .ufo/waves/round-64/c64_quote_tool.py --root . --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb` returned exit 0 and exact stdout `revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb present=1 tool_sha=ok selftest=4/4 frozen_cases=ok rederive=agree met=true`. Matches `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/after-c2.txt:1-3` in result and exit status.
- C3: command `node scripts/freshness-sweep.mjs --offline` returned exit 0; terminal verdict exact `VERDICT: OK (exit 0, partial: offline)`, followed by exit 0. It explicitly reports remote checks skipped offline/not counted and `complete=false`. Verdict and offline qualification match `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sweep-after.txt:1-6`; the generated timestamp/repo path and full environment-dependent diagnostics differ, so this is not byte-identical output.
- Census: command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` returned exit 0. Its 17 output lines matched `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/census-after.txt:1-17` exactly; committed receipt line 18 records `census-after-exit=0`.

The freshness sweep and census read external fleet-root state by design; these were run with the exact requested arguments. No tools were installed or updated.

## Verdict

Reproduced the three frozen after claims and the census validation on detached T0. C1, C2, sweep verdict, and census output/result match their committed after receipts; sweep output is intentionally environment-specific, while its verdict, partial/offline status, and exit match. Initial attempts against a git-archive checkout yielded `could-not-evaluate: revision ... unreadable` (exit 2), because that archive has no git revision metadata; the detached shared clone resolved this without touching the lane working tree.