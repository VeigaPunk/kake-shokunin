REPRODUCED — all four r42-control red receipts reproduce under counter v4 (8/8 unseeded runs not met; seeded replays byte-identical to the freeze receipts).

Item: score the four r42 controls in `.ufo/waves/round-43/controls-r42/` (v1_casefold, v2_prefix32, v4_hosttable, M8-port-five-digits; junk_constant skipped) with `c43_count_v4.py` twice each, no `--seed`, and compare equalRuns / unequal-run lists to the L1 freeze receipts.

## Verdict
REPRODUCED. 8/8 unseeded receipts: `met: false`, exit 1. No live-seat control meets v4, so the C1 kill rule ("any live-seat control meeting v4 -> C1 NOT MET") is not tripped. Seeded replays reproduce the freeze receipts run-for-run and sha-for-sha: the freeze is trustworthy and the counter is seed-stable.

## Commands (exit codes)
```
timeout 900 prlimit --as=8000000000 -- python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/c43_count_v4.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --tool-file .../controls-r42/<name>.py --label ExecRerunControls-<name>-<r1|r2> \
  --out /fast/scratch/hyaku/kake-r43/kake-r43-w1-ExecRerunControls/<name>-<r1|r2>.json
```
Unseeded exits: v1 r1=1 r2=1, v2 r1=1 r2=1, v4 r1=1 r2=1, M8 r1=1 r2=1 (`exits.txt`); seeded replays all exit 1. <=3 concurrent processes, all under `timeout 900` + `prlimit --as=8000000000`; no process tree of this seat left running.
sha256 (unchanged from freeze): counter `c43_count_v4.py` = `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab`; `v1_casefold.py` = `9993b842427d1592713309420626e46e42f1e56defab28b2f5349e6391cf4bc4`; `v2_prefix32.py` = `eadf5df4b5c26059429a5dbffd2d87bcdbca6f460ba982c81360736e6856aa0f`; `v4_hosttable.py` = `dc8b6ecdcc638d20d34f66aaeadd8aa8ba798f5307c2fa8d80a876d2ae16ece7`; `M8-port-five-digits.py` = `391608309640431acfc873d48e33189cf71a399faaa410ce6d65b910282bbb1f`.

## Eight unseeded receipts (met / equalRuns / unequal runs)
| receipt | seed | met | equalRuns | unequal runs | max ratio | vs freeze unequal list |
|---|---|---|---|---|---|---|
| v1_casefold-r1 | 141456777419246 | false | 9/11 | F, T2 | 1.448 | identical |
| v1_casefold-r2 | 143511601705506 | false | 9/11 | F, T2 | 1.416 | identical |
| v2_prefix32-r1 | 183352669453755 | false | 9/11 | F, T3 | 1.315 | E missing |
| v2_prefix32-r2 | 202661366917226 | false | 8/11 | F, T2, T3 | 1.412 | E missing |
| v4_hosttable-r1 | 46372103033198 | false | 9/11 | F, T3 | 1.421 | identical |
| v4_hosttable-r2 | 40452572176799 | false | 9/11 | F, T3 | 1.574 | identical |
| M8-port-five-digits-r1 | 38787505527747 | false | 9/11 | F, T3 | 1.416 | identical |
| M8-port-five-digits-r2 | 191541386827480 | false | 9/11 | F, T3 | 1.313 | identical |
Freeze unequal lists: v1 [F,T2], v2 [E,F,T2,T3], v4 [F,T3], M8 [F,T3]. All 8 seeds differ from the freeze seeds (independent os.urandom draws). `note: null` in all 8; no "tool absent", no cannot-evaluate.

## Seeded replays (freeze seeds) — byte-identical to freeze
| tool | seed | met | equalRuns | unequal runs | freeze unequal | per-run flags + out sha256 |
|---|---|---|---|---|---|---|
| v1_casefold | 75489578906268 | false | 9/11 | F, T2 | F, T2 | all 11 shapes match |
| v2_prefix32 | 202843337434829 | false | 7/11 | E, F, T2, T3 | E, F, T2, T3 | all 11 shapes match |
| v4_hosttable | 224536126245930 | false | 9/11 | F, T3 | F, T3 | all 11 shapes match |
| M8 | 277967031012645 | false | 9/11 | F, T3 | F, T3 | all 11 shapes match |
Every run's `ref41OutSha256` and `candOutSha256` equals the freeze receipt's value (44/44 sha comparisons identical); `ref41`/`base40`/`counter`/`tool` shas identical in all four.

## The one divergence: v2's run E is seed-dependent, not a counter defect
v2's freeze receipt has E unequal; neither unseeded rerun does (E equal in both). Cause is the control's own defect: `controls-r42/v2_prefix32.py:293-303` caches `_parse_url` by `value[:32]` in a module-global `_PREFIX_CACHE`, so the defect fires only when two values in one corpus collide on their first 32 code points. Reproduced deliberately: seed 202843337434829 gives E unequal (7/11) again, seed 22222 gives E unequal (7/11), seed 11111 gives E equal (8/11); two runs at seed 11111 gave identical output sha256 on all 11 shapes -> the counter is deterministic given a seed. Run F is unequal in all 15 receipts of this seat (8 unseeded + 4 seeded + 3 probes) and is the only shape carrying the r42 defect classes under v4's `cases_f` (`c43_count_v4.py:458-490`), so F-unequal is the stable witness.

## Per checked statement
- "all eight receipts must be not met" — holds: 8/8 `met: false`, exit 1.
- "record equalRuns and the unequal runs per receipt" — done above, read from the receipt JSON.
- "compare to the freeze receipts' unequal-run lists" — done; 7/8 identical, v2's E explained and reproduced under the freeze seed.
- Counter v4 unchanged since freeze — holds: on-disk sha256 equals `verification/freeze/counter-v4.sha256` and the `counterSha256` in every freeze receipt.
- Tool shas unchanged since freeze — holds: on-disk sha256 of all four controls equals the `toolSha256` in each freeze receipt.
- No pre-freeze seat score in `.ufo/waves/round-43/w1/` (only sibling wave reports, none a C1 control score).

## Artifacts / scope
Receipts + logs + `exits.txt`, `exits-seeded.txt`, `run_batch.sh`, `run_seeded.sh` in `/fast/scratch/hyaku/kake-r43/kake-r43-w1-ExecRerunControls/` (36 files, ~90 KB). Only file written in the lane repo: this report. No git/jj mutation, no network access, no tooling installs (python3, sha256sum, coreutils only).

## Risks / blockers
None blocking. v2's unequal-run list is seed-sensitive, so a seat reporting only the unequal list without the seed cannot compare v2 lists directly; the `met: false` verdict and the F-unequal witness are seed-stable. Absolute CPU medians carry mild contention noise from concurrent siblings, but each ratio compares the candidate against the base40 tool measured in the same process and stayed far under the 2.0 limit.
