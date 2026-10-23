# ProbeRunnerCalib — round 42, wave 1
Axes: operability (tested); freshness (unchanged). Milestone: r42-controls.
Verdict: the ≥90% CPU-accounting hypothesis **holds for all four exercised modes**, twice each; no falsification.

## Probe and detector
At the tip41 main guard, add approximately 1 second of CPU without changing its audit logic or stdout.
Modes: own main thread; two joined threads at 0.5 seconds each; one forked/waited child; one genuinely orphaned child.
The orphan waits for its parent to exit before burning; its recorded parent changes from PID 3 to runner PID 2.
Burn measured by `time.thread_time_ns()` in the actual worker(s), not wall time.
`detect.py:64-74` imports the pinned counter and calls `Sandbox(rng, td).run(...)` directly.
Only observation adjustment: redirect outer bwrap's discarded stderr to a host evidence file; RUNNER, timing fd, accounting code and all sandbox limits stay unchanged.
Expected detector: byte-equal tip41 exit/stdout, completed ≥1-second burn, and reported CPU ≥0.9 × measured burn; otherwise falsified or inconclusive.
Same detector ran on pristine, mutated and byte-restored copies. All four pristine and four restored runs passed.

## Actual outputs (seconds; paired trials)
| Mode | Measured burn | RUNNER CPU | Reported / burn | Baseline-adjusted fraction | Statement |
|---|---|---|---|---|---|
| own process | 1.000445016 / 1.000056074 | 1.041420 / 1.041832 | 104.096% / 104.177% | 99.937% / 100.017% | holds |
| threads | 1.000192162 / 1.000394859 | 1.043600 / 1.043131 | 104.340% / 104.272% | 100.131% / 100.064% | holds |
| waited child | 1.000409106 / 1.000128198 | 1.041701 / 1.042745 | 104.128% / 104.261% | 100.152% / 100.284% | holds |
| orphaned child | 1.000367645 / 1.000264045 | 1.042016 / 1.049261 | 104.163% / 104.898% | 100.033% / 100.767% | holds |
Gross fractions include normal tool CPU; adjusted fractions subtract the mean of each mode's pristine/restored CPU.
Pristine/restored CPU: own 0.042124/0.041086; threads 0.042083/0.042106; waited 0.038965/0.040578; orphaned 0.041940/0.040704.
Every one of 16 audited-tool runs exited 1 with identical stdout SHA256 `e40f2208cc2ce16424f537c28a878db7f2290823a4da14b1589677fa496cf111`.
Actual stdout: `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "bsvqwli", "status": "findings", "error": null, "findings": [{"code": "loc_not_absolute", "entry": 3}]}]}` plus newline.
Finding: `c42_count.py:415-424` accounts for the exercised joined-thread, waited-child and reparented-child work; `orphaned.burn.py:463-478` confirms the latter occurs after adoption.
These are added-work calibration probes, not judgment-skipping controls. No undercount-defect mutant was installed; no killed/survived coverage claim is made.
Full C1 scoring was not run: counter `equalRuns`, five-shape `ratios` and `met` are unscored, not passed. These samples do not establish every possible descendant pattern.

## Commands and evidence
Sandbox artifact root S = `/fast/scratch/hyaku/kake-r42w1/ProbeRunnerCalib/`.
`timeout 120 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/ProbeRunnerCalib/detect.py --phase pristine --reps 1` → 0.
`timeout 120 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/ProbeRunnerCalib/detect.py --phase mutated --reps 2` → 0.
`timeout 120 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/ProbeRunnerCalib/detect.py --phase restored --reps 1` → 0.
Raw exits, stdout, CPU, worker clocks, parent PIDs and hashes: S`pristine.json`, S`mutated.json`, S`restored.json`; stderr evidence under S`run-*/burn.stderr`.
All exact shell commands, including successful source/restoration SHA256 commands: S`commands.txt`. Python 3.14.8; no tool installs/updates.

## SHA256 and exact restoration
Counter `.ufo/waves/round-42/c42_count.py` before/after: `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`.
RUNNER string: `b3075540e3ca304bd43fab400b1c408708993995f68f79735ebe81bb8abc0705`.
S`detect.py`: `055b988b24128f0410f6e8825930573883282c40a421819945b98e536c008e47`.
All S`own.py`, S`threads.py`, S`waited.py`, S`orphaned.py` before/after equal shared tip41: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.
Mutated bytes retained only as explicit snapshots, identical to the tools at measurement:
- S`own.burn.py`: `30d7a3c453ba95cf327a8575dd8c6a93c1e2e09cfd71f435d8d6e9ca27691795`.
- S`threads.burn.py`: `b1acc5d0f8e16fc3bc1e1200bb2c47986de294b97cffd8829c23632f941cd5c0`.
- S`waited.burn.py`: `7271feaab56009ac1703409e57d38a3cda3c4bc8bd9320fe657c2c24c741110e`.
- S`orphaned.burn.py`: `88bfe1a335dcdadf34e58f763f12fb5b7684546f2a93765799b583ab6f58ce81`.
Restoration statement: holds; all four exact original byte hashes restored and the same detector passed afterward.
All started runs completed; Sandbox waited for bwrap and its runner reaped children, including each observed orphan. No service/background process was started.
