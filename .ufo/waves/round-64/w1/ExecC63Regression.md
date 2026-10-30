# ExecC63Regression — T0 regression sweep

Target revision: `4c8295fa5e3b628f1fdf3840299ae415c01849fb`.

## Commands and observed results

Run from `/home/vgpnk/Projects/shokunin/kake-shokunin`:

1. `python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 4c8295fa`

   Output: `revision=4c8295fa disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true` (exit 0).

2. `python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 4c8295fa`

   Output: `revision=4c8295fa present=1 selftest=4/4 frozen_cases=ok met=true` (exit 0).

3. `python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root . --revision 4c8295fa --fleet /home/vgpnk/Projects/shokunin`

   Output: `C2 id-resolver 5/5 met=True (met: gate_conditions_passed == 5 of 5)` (exit 0). G1–G5 all PASS; G2 selftest 72/72; G5 green exit 0 summary `(116, 116, 0, 0, 0)`, reference ids cited=116.

4. `TMPDIR=/fast/scratch/hyaku/kake-r64/ExecC63Regression python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision 4c8295fa --work /fast/scratch/hyaku/kake-r64/ExecC63Regression/c60 --jobs 4`

   Output ended: `C1 gate-status members=28 mismatches=1 scores_held=3/3 met=False` (exit 1; 112.10 seconds). The output identifies `.ufo/waves/round-56/c56_selftally.py` as `label=live e_T=1 MISMATCH live_not_green`; all other listed entries were marked `ok`.

## Verdict

The C63 calibration and quote regressions and the C57 resolver regression met their expected results. C60 did not: members=28 but mismatches=1 and met=False. The named red is the live C56 selftally gate (`live_not_green`). No timeout. No tool installation. Scratch directory removed after the run.