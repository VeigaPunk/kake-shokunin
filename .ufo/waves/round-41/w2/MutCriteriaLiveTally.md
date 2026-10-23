# MutCriteriaLiveTally — operability mutation probe
Axes: operability (judged); freshness (context only, not checked). Scope: QUALITY (s) draft checker, not a round verdict.
Scratch: `/fast/scratch/hyaku/kake-r41w2/MutCriteriaLiveTally/` (S below).

## Real-round commands and observed outputs
- `timeout 30s prlimit --as=4000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/criteria/live_tally_check.py --dispatch-log /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/w1-dispatch-log.txt /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/resid-dispatch-log.txt --receipts /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-40/verification/w1` → exit **1**.
- stdout: `dead seats: ['CtlUTabOnly']; receipts: 76; dead-seat receipts in tally: 4`; listed `CtlUTabOnly-dead__tool_cr_lf.json`, `CtlUTabOnly-dead__tool_tab_lf.json`, `CtlUTabOnly-dead__tool_tab_only.json`, `CtlUTabOnly-dead__tool_tab_only_query.json`.
- `timeout 30s prlimit --as=4000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/criteria/live_tally_check.py --dispatch-log /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/w1-dispatch-log.txt --receipts /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/verification/w1` → exit **0**.
- stdout: `dead seats: none; receipts: 141; dead-seat receipts in tally: 0`. Both runs had empty stderr; full transcripts: `S/round-runs.json`.

## Mutants and independent fixtures
Command: `timeout --signal=TERM --kill-after=2s 240s prlimit --as=4000000000 --fsize=200000000 -- python3 -B /fast/scratch/hyaku/kake-r41w2/MutCriteriaLiveTally/probe.py` → exit **0** (5.35 seconds).
Same bounded detector exercised each isolated checker on pristine, mutated and restored bytes: 14 fixtures × 3 stages × 7 mutants = 294 checker runs; every pristine/restored stage passed 14/14. Seven mutants killed, zero survived, zero inconclusive.
Each child command, exit, stdout and stderr is retained verbatim in `S/results.json` and `S/work/<mutant>/result.json`; child runs use `timeout --signal=TERM --kill-after=2s 10s prlimit --as=4000000000 --fsize=200000000 -- python3 -B ...`.
Fixtures explicitly cover `DeadSeat-dead__tool.json` (F01), `DeadSeat__tool.json` (F02), `DeadSeat-tool.json` (F03), live prefix collisions, dead seats in either dispatch log, underscore/digit seat names, HOLD vs DEAD, non-JSON/empty tallies, bare names, and missing inputs.
Below, exits are pristine/mutated/restored; expected detector means that fixture's fixed expected exit AND stdout. Every mutation changes exactly one source line in its own scratch copy.
| Mutant / original line | Defect | Catching fixture / expected exit | Actual exits | Actual mutated stdout | Verdict |
|---|---|---|---|---|---|
| M01_first_log_only.py:17 | Only first dispatch log read | F05 / 1 | 1/0/1 | A | killed |
| M02_no_hyphen.py:26 | Drop hyphen separator | F01 / 1 | 1/0/1 | B | killed |
| M03_no_double_underscore.py:26 | Drop `__` separator | F02 / 1 | 1/0/1 | B | killed |
| M04_loose_prefix.py:26 | Match any seat-name prefix | F04 / 0 | 0/1/0 | C | killed |
| M05_no_seat_underscore.py:19 | Omit underscore from seat capture | F07 / 1 | 1/0/1 | A | killed |
| M06_always_green.py:30 | Always exit zero | F01 / 1 | 1/0/1 | D | killed |
| M07_hold_as_dead.py:19 | Read HOLD instead of DEAD | F01 / 1 | 1/0/1 | A | killed |
Actual stdout A: `dead seats: none; receipts: 1; dead-seat receipts in tally: 0\n`.
Actual stdout B: `dead seats: ['DeadSeat']; receipts: 1; dead-seat receipts in tally: 0\n`.
Actual stdout C: `dead seats: ['DeadSeat']; receipts: 1; dead-seat receipts in tally: 1\n  DeadSeatSibling__tool.json\n`.
Actual stdout D: `dead seats: ['DeadSeat']; receipts: 1; dead-seat receipts in tally: 1\n  DeadSeat-dead__tool.json\n`.

## Findings and statement status
- **holds** — red on round 40, green on round 41, with the exact requested inputs.
- **holds on checked fixtures** — dead-seat receipts are detected both with and without the extra `-dead` suffix; seven plausible one-line regressions are caught by these fixtures.
- **LOW / scope; overstated if read without its filename precondition** — “a control tally counts live seats only” is not an arbitrary-filename guarantee: `.ufo/waves/round-41/criteria/live_tally_check.py:5,26` excludes bare `DeadSeat.json`. F12, with `DEAD Parent.DeadSeat`, exits 0 and prints `dead seats: ['DeadSeat']; receipts: 1; dead-seat receipts in tally: 0`. This follows line 5's explicit contract; it is not a demonstrated violation within the documented `-`/`__` layout. It would be inconclusive, not a killed mutant, against an unconditional expectation of exit 1. No naming contract was changed.
- No claim that the real-round pair alone kills these mutants; mutant executions used the independent fixtures above.

## Hashes and restoration
Lane source SHA-256 before = after = all seven working copies before/restored: `ef48ca2bb14648bb6a9d35a6ec04c53fd648575b90874efef0c1679674eb767d`. All seven `restored_exact` fields are true; lane source was never written.
Mutated SHA-256 values (mutant artifacts intentionally retained in `S/mutants/`):
- M01 `ec48e1c6213450d2ae15cc7265747a6c499040b3c0cdc44e798f0773ce3a93af`
- M02 `db2d7ea7991221ddb9234a7b3d2497ba6034adba979ad3ba2d9ef84cd0b3f3a1`
- M03 `081c4de098bf3e65802923f9cf5cf4f7d1e2d3720f5f2d999eadcd9254f6391d`
- M04 `296ce6e55f18cd82e1e6f4cb7092b2d2db1689881280f7979766859ab03cd3f2`
- M05 `4dda97a0468d36cab0eb8baf63e484bc2b86162244702dd08da5b958d8e4b2fa`
- M06 `b186b3d9d5bc5ca5d4a1bf48b06e1f01f3e1104bf7551e193225f21220eb17ba`
- M07 `e5ca62d71536d6d03926581d8f30453a856515a11cc4cf5ff649d8998b4071d3`
Detector SHA-256: `01f5101930446eb5ee2975b3ee4dea286ed8f7ae0df3780f4bc8d0db0963fca0`. No installs, network requests, background services, or unfinished child processes. Scratch files plus aggregate are under 1 MB; all execution was synchronous, with at most two checker subprocess groups at once.
