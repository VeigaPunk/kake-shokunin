# Round 42 — counter sandbox/timing review

Axis: operability. Scope: `c42_count.py` `Sandbox.run` / `RUNNER`; read-only review plus temporary probes under `/fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/`.

## Finding — HIGH: candidate can forge its own CPU sample

`Sandbox.run` opens `time_path` and passes its writable FD to bwrap (`c42_count.py:451-464`). The runner receives the FD and writes the actual `getrusage` sample (`412-425`), but the tool can inspect `/proc/<runner>/cmdline` and reopen `/proc/<runner>/fd/<timerfd>` as writable. `Sandbox.run` trusts the last nonempty line of that file (`475-484`).

Exploit evidence: `timer_probe.py:4-12` (SHA-256 `7e8556d705d303ffa5ed7c63b09bb65186db46ce6edfff0047af99a5087daf4f`) wrote a 4-KiB prefix followed by `0 0.000000 0.000000` through that proc FD. Receipt `timer-receipt.json` shows candidate CPU samples `0.0` for all 25 repetitions and ratios T1–T5 all `0.0`; base40 samples remained nonzero (T1 ~0.56s; T5 ~0.06s). The runner's real line did not prevent the parser from consuming the forged trailing line. Probe deliberately had exit 97/output mismatch, so it did **not** meet: `equalRuns=0/8`, `met=false`, counter command exit 1. A matching tool could retain its real judgments/output and perform the same write ([INFERENCE]); no such matching control was scored.

Impact: the counter's CPU predicate is forgeable for candidate timings; the false value can turn a slow candidate into an apparent speed-up. No direct way to forge a base40 sample was found: candidate and base40 calls are sequential (`579-584`), each `run` opens a fresh timing file and unlinks it before return (`448-449`, `475-478`), and runner waits/reaps before recording. This is a candidate-measurement integrity defect, not evidence that base40 CPU was changed.

Smallest remediation: prevent the tool from opening the runner's descriptors (set/check `PR_SET_DUMPABLE=0` on the runner before spawning the tool); stronger option is trusted parent-side CPU accounting rather than a child-writable timing file.

## Other sandbox observations

`bwrap` is v0.13.1 (binary SHA-256 `33516b9cd1fa6432307ad71f23765fa30604b0a8d769dac0d2ba054e85aeec83`). `/usr`, tool, runner and case tree are read-only binds; `/tmp` is a writable tmpfs; the probe could also create/remove a file at `/`. `/home/vgpnk/Projects/shokunin` and `/fast/scratch` were absent in the tool's filesystem view. `--proc /proc`, `--dev /dev`, `--unshare-all`, `--clearenv`, `PATH=/usr/bin`, `LANG=C.UTF-8` are present at `453-461`. The probe could read `/proc/1/cmdline` and `/proc/1/environ`; observed `/proc/1/environ` keys were limited to PATH/LANG, with no operator variables. Parent command line/environment and its `/proc/<ppid>/fd` directory are visible. Inputs, manifest, IDs and argv are still observable; randomized names do not conceal case contents.

Same-namespace subreaper handling is present (`415-424`). Direct `CLONE_NEWPID` failed with EPERM (`ns_probe.py`, candidate exit 1), but a nested user+PID namespace was possible (`ns_user_probe.py:12-41`, candidate exit 97); its 0.10 CPU-second nested worker was included in measured candidate CPU (~0.116–0.118s), so that tested descendant path was not hidden. Timeout cleanup is not exhaustively tested.

## SCORECARD dispositions

- `SCORECARD.md:2946-2949` sandbox mechanisms: **OVERSTATED** as measurement isolation. Listed bwrap, limits, environment clearing and randomized names are present; they do not protect the timing file from `/proc` access.
- `SCORECARD.md:2944-2945` CPU-as-tool-and-descendants guarantee: **WRONG** as an integrity guarantee because the sampled value is passed through a candidate-writable FD. `/proc/1/environ` no-operator-variable clause: **HOLDS** in the probe.

## Commands and receipts

All used cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`, wrapper `timeout 900 prlimit --as=8000000000 --`; counter SHA-256 `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`.

- `probe.py` SHA `ceea154a2b4400596f30ea52b6c4f08a9b6c99f527600cde67ec9d46ffdd5f9c`; command `python3 -B .ufo/waves/round-42/c42_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/probe.py --label SentinelCounterSandbox-observe --seed 42142 --out /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/probe-receipt.json`; exit 1, `equalRuns=0/8`, ratios `.019,.019,.021,.022,.183`, `met=false`. Filesystem/proc flags used; its timer probe indexed OS argv incorrectly.
- `fd_probe.py` SHA `79e0eebe8590ba5a5d938015f630212b3b6bb2483750490dd923b0f7170461ca`; command `python3 -B .ufo/waves/round-42/c42_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/fd_probe.py --label SentinelCounterSandbox-fds --seed 42143 --out /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/fd-receipt.json`; exit 1, `equalRuns=0/8`, ratios `.021,.019,.023,.024,.185`, `met=false` (candidate exit 2; timer-FD index was wrong).
- `timer_probe.py` SHA `7e8556d705d303ffa5ed7c63b09bb65186db46ce6edfff0047af99a5087daf4f`; command `python3 -B .ufo/waves/round-42/c42_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/timer_probe.py --label SentinelCounterSandbox-timerwrite --seed 42144 --out /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/timer-receipt.json`; exit 1, `equalRuns=0/8`, ratios `0,0,0,0,0`, `met=false`.
- `ns_probe.py` SHA `efb126d8040490bde315714ada428457d3b11e2f94b2638a7424e88ba619ced4`; command `python3 -B .ufo/waves/round-42/c42_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/ns_probe.py --label SentinelCounterSandbox-nestedpid --seed 42145 --out /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/ns-receipt.json`; exit 1, `equalRuns=0/8`, ratios `.026,.027,.029,.031,.249`, `met=false`.
- `ns_user_probe.py` SHA `946c99eb7f426212beab7cc82b7a8ed120a32b90bb770fec188a007acd7f5b82`; command `python3 -B .ufo/waves/round-42/c42_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/ns_user_probe.py --label SentinelCounterSandbox-nesteduser --seed 42146 --out /fast/scratch/hyaku/kake-r42w1/SentinelCounterSandbox/ns-user-receipt.json`; exit 1, `equalRuns=0/8`, ratios `.204,.198,.220,.236,1.830`, `met=false`.
