# SentinelScope — sandbox vector ledger (round 100, W1)

Scope: the two sandboxes added this round: `c100_fresh304.py` `SANDBOX` / `run_candidate` / `sandbox_ok`
(C2 case runner) and `c100_registry.py` `sandbox_argv` / `run_span` / `probe` (C1 tool runner).
Instruments read-only, imported with `python3 -B` (`sys.dont_write_bytecode`), never patched.
Digest check before any attack: `sha256sum -c controls/instrument-sha256.txt` → 21 of 21 `OK`.
Host: bubblewrap 0.13.1 at /usr/bin/bwrap (unchanged), Python 3.14.8, `max_user_namespaces=122865`
(read-only observation; no sysctl touched). Scratch: `/fast/scratch/hyaku/kake-r100/SentinelScope/`
(deleted before yield). Receipts here: `receipt-*.txt`, PoCs: `poc-*.py` + `poc-*.out.txt`.

`success` = the attempt achieved the stated goal. `blocked` = the sandbox held (observed rc/values given).
Commands use the counters' own argv; "probe file" = a candidate program run through `m.run_candidate`
(c100_fresh304) or a `scripts/a.py` tool in a fixture scored by `m.score()` (c100_registry).

## C2 — `c100_fresh304.py` sandbox (candidate runs with `SANDBOX`, `--tmpfs /tmp`, `--clearenv`, no tree bind)

| ID | Target / goal | Attempt (command, probe) | Observed | success |
|----|---------------|--------------------------|----------|---------|
| F1 | read /proc: other processes, counter pid | `drive.py work fr/p_probe.py` (lists `/proc`, `/proc/self/fd`, `/proc/1/cmdline`) | `pids_visible=[1,2]`; `ppid=1`; `pid1_cmdline` = bwrap argv only; `ns` differ from host (pid/net/mnt/user/ipc/uts/cgroup all new) | blocked |
| F2 | inherited fds / pipes to counter | same probe, `/proc/self/fd` | fds `0,1,2` = pipes only; fd 3 absent | blocked |
| F3 | environment secrets | same probe, `os.environ` | `{PATH:/usr/bin, LANG, HOME:/tmp, PWD:/tmp}` | blocked |
| F4 | learn counter location via mounts | same probe, `/proc/self/mountinfo` | the candidate bind shows host source path `…/c100f-*/freshen_304.py` (xfs root `/scratch/…`); discloses the counter's work-dir name, nothing readable behind it | partial (disclosure only) |
| F5 | write ro /usr, candidate file, /bin | same probe, `open(p,'w')` | `/usr/...` EROFS; `/cand/freshen_304.py` EROFS; `/bin/...` EROFS | blocked |
| F6 | write persistent host state | same probe: `/tmp/r100_w`, `/dev/r100_w` | `WROTE` — both are sandbox-private tmpfs (`/tmp`, `/dev` mounts); host path absent | blocked (ephemeral only) |
| F7 | oracle theft via parent `/proc/<ppid>/cmdline` (frozen forgery) | `python3 -B c100_fresh304.py --candidate-file frozen/neg-theft.py --work …` (control reproduced) | `hand=0/91 generated=0/300 met=false` rc=1; counter source not bound, ppid=1 in-ns | blocked |
| F8 | network: IPv4 to 1.1.1.1, host loopback listener, host abstract unix socket | same probe, `socket.connect` | `tcp 1.1.1.1:53 → OSError:101 (ENETUNREACH)`; `127.0.0.1:<host listener> → ConnectionRefused:111` (own netns lo); `\0abstract → ConnectionRefused:111` | blocked |
| F9 | outlive the case (setsid, double fork, stdio to /dev/null) | `poc-fresh304-sandbox-probe.py` `outlive`; also `drive.py … fr/p_outlive.py` | `spawned` rc=0 in 0.01 s; host `/proc` scan for the marker: `[]` at t+0 and t+3 s (scanner control: sees a host marker) | blocked |
| F10 | keep the counter blocked (pipe-holding grandchild / infinite loop) | `drive.py … p_hang.py` (`while True`) | `rc=124 elapsed=10.01s`; no survivors | blocked (bounded 10 s) |
| F11 | fork bomb / process table | `drive.py … p_fork.py`; PoC `resource` (200 forks, 1 s sleep) | `forked 200` in 2.02 s; `RLIMIT_NPROC=122865` (per real uid, shared with the operator session), no pids cgroup in the sandbox | succeeded (bounded 200; unbounded in principle — see note) |
| F12 | host RAM via `/tmp` tmpfs | `drive.py … p_tmpfs.py` (256 MiB) then `p_tmp2g.py` (2 GiB) | tmpfs total `16241557504` B (≈15.1 GiB = half of 30 GiB RAM); 2 GiB written in 0.25 s; host `free` dropped ~1.9 GB during the write | succeeded (no per-case size cap) — [INFERENCE] a 10 s run can fill the ~15 GiB tmpfs at the measured ~8 GB/s |
| F13 | syscall filtering / caps / rlimits | `drive.py … p_rlimit.py` | `CapEff=0`, `NoNewPrivs=1`, `Seccomp: 0` (no filter), `RLIMIT_AS/FSIZE/CPU = unlimited` | observation: hardening gap, not exploited |
| F14 | cross-case persistence (/tmp, /dev/shm) | `drive.py … p_cross.py` run twice | run 1 wrote `/tmp/r100_marker`; run 2 saw `tmp_before [] shm_before []` | blocked |
| F15 | detect the sandbox and change behaviour | `p_detect.py` (`os.getpid()==2`, pid1 cmdline) | detection works (`is_sandbox_pid2 True`); no oracle reachable, so detection yields no score gain | detection succeeded; no scoring gain |
| F16 | fail-open in the gate itself | `python3 -B -c` with `m.SANDBOX` bind replaced by a missing source → `m.sandbox_ok(w)` (also `PoC` last step) | `sandbox_ok: False` → counter returns 2 (`could-not-evaluate`) | blocked (fail-closed) |

Not executed (analysis only, labelled): `--candidate-file` controls mode uses the public default seed 100100,
so a candidate could in principle precompute the 300 generated cases from the public source; the scored
`--revision` path seeds from the commit that contains the candidate (circular for the candidate), so that
path is not affected [INFERENCE]. A candidate that special-cases the 91 public hand inputs passes hand
but fails generated (not run; the generated population is the gate).

## C1 — `c100_registry.py` sandbox (`sandbox_argv`, tool run with `--bind work work`, tree bound read-write)

| ID | Target / goal | Attempt (fixture repo → counter command) | Observed | success |
|----|---------------|------------------------------------------|----------|---------|
| R1 | probe gaming: tool recognises the D2 argv `--zz-bogus-r100` | `poc-registry-probe-gaming.py --scratch S` → fixture `probe-aware` (`if sys.argv[1:]==['--zz-bogus-r100']: exit 0`, else 64; map `0=ok; 1=bad`) | `met=True probe_mismatch=0`; real `python3 -B scripts/a.py --zz-other` rc=64 (unmapped). Control `honest` (same map, real 64) → `met=False probe_mismatch=1 rc=64` | **succeeded** (score bypass) |
| R2 | probe gaming by sandbox detection (pid 2) | fixture `sandbox-detect` (`exit 0 if os.getpid()==2 else 64`) | `met=True`; real `--zz-other` rc=64 | **succeeded** (score bypass) |
| R3 | write into the shared scored tree: self-test rewrites its own probed file | fixture `selfrewrite` / `poc-registry-scored-tree-write.py` `self-rewrite` | self-test span `python3 -B scripts/a.py --selftest` rewrote `tree/scripts/a.py` to `exit 0`; probe ran the rewritten file → `met=True`; committed `scripts/a.py` still exits 64 (`git show HEAD:scripts/a.py` sha `5261ab80cb0f` ≠ tree `14c75fb904c5`) | **succeeded** (cross-case leak 1) |
| R4 | write into the scored tree so a later row sees it | fixture `crossrow-clean` / PoC `cross-row`: row a's self-test writes `scripts/b.py`; row b is "no self-test" | `met=True tools=2 probe_mismatch=0`; b's probe ran the rewritten b (tree sha `14c75fb904c5`), committed b (sha `7626264709c3`) exits 64 on unknown flags | **succeeded** (cross-case leak 2) |
| R5 | read instrument sources / oracle from the scored tree | fixture `oracle-visible` (`.ufo/waves/round-100/c100_registry.py`, `c100_fresh304.py` placed in the tree as the REV archive does) | `evidence.txt`: registry source readable with `has_probe_arg=True`; fresh304 source readable with `has_fresh304_reference=True`. The repair commit `e84a187` contains `.ufo/waves/round-100/{c100_registry.py,c100_fresh304.py,freeze.md}` (read-only `git ls-tree`) | **succeeded** (instrument visibility; C1 probe disclosed to tools) |
| R6 | write outside `--bind work` (absolute host path, `../`, `../../`) | fixture `evidence` (`tools` writes `/fast/…/rg/escape-abs.txt`, `../escape-up1.txt`, `../../escape-up2.txt`) | all `WROTE` inside the sandbox root tmpfs; `ls` of `..`/`../..` shows only bwrap-created mount points; host `find` for `escape*` → nothing | blocked for host (writes are sandbox-ephemeral) |
| R7 | network from a scored tool | fixture `evidence`: `connect` to host loopback listener, host abstract socket, 1.1.1.1 | `ConnectionRefusedError:111`, `ConnectionRefusedError:111`, `OSError:101` | blocked |
| R8 | outlive the tool run | fixture `outlive` (self-test starts `setsid` daemon with stdio `/dev/null`) | host `/proc` scan `[]` at t+0 and t+3 s (scanner control sees host marker); `run_registry.py outlive` → `host_survivors ''` | blocked |
| R9 | disk exhaustion | fixture `disk` (self-test writes 256 MiB into `tree/bigfile.bin`, the bind of `/fast` xfs) | `tree-file bigfile.bin size 268435456` on host disk; no quota, no RLIMIT_FSIZE (`unlimited`) | **succeeded** (no quota; bounded only by the 240 s span timeout — [INFERENCE] rate not measured beyond 256 MiB) |
| R10 | time exhaustion | fixture `hang` (probe is `while True: pass`) | `rc=124`, `elapsed=120.0s` (probe timeout 120 s; self-test span timeout 240 s); killed process gone (host scan `zz-bogus-r100` → only unrelated seat process after exit; the hang pid was absent) | blocked, but each hostile probe costs 120 s and each hostile span 240 s, with no aggregate cap |
| R11 | symlinks planted in the scored tree pointing at host paths, then counter cleanup | fixture `symlink` (self-test plants `planted-link-dir`, `planted-link-file` → host `victim-dir/…`); then counter-style `shutil.rmtree(work)` | links recorded (`tree-symlink … ->`); after rmtree the victim file and directory still exist | blocked (rmtree does not follow links) |
| R12 | fail-open when bwrap itself fails | `poc-registry-failopen-bwrap.py` (PATH shim: real bwrap with a missing bind source → exit 1) vs control with real bwrap | broken: `direct probe rc=1`, `met=True tools=1 probe_mismatch=0` (no tool ever ran; the map names 1). Control: `direct probe rc=64`, `met=False` | **succeeded** (counter integrity fail-open; no `sandbox_ok()` gate in `c100_registry.py`, unlike `c100_fresh304.py` F16) |

Totals: vectors attempted = 28 (F1–F16, R1–R12). Host escapes (out of the sandbox into the host filesystem,
network, processes or the counter's memory) = 0. Score bypasses = 3 (R1, R2, R12). Cross-case leaks
(one case's write seen by a different case) = 2 (R3, R4).

Environment notes (observations, not attempts): one background `pgrep` control in a run reported a false
negative once (`pgrep_control_sees_host_marker: False`), so survivor checks were redone with a `/proc`
scanner (`/proc/*/cmdline`) with its own positive control. During my runs another seat's live C1 probe
(`scripts/capture_delta.py --zz-bogus-r100`) also appeared in `/proc`; it is not mine and was not touched.
