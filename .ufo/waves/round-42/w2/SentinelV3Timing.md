# SentinelV3Timing — wave-2 falsify: v3 timing integrity (round 42)

Seat: `KakeR42.SentinelV3Timing`. Verdict: **no route found that still forges
CPU under counter v3**; both wave-1 forgers now score NOT MET, and three new
routes were tried and blocked. C1's v3 timing defense holds against every
attack attempted here.

Counter: `.ufo/waves/round-42/c42_count_v3.py`, sha256
`ce2d5a0ca2c3768ce2b1d7b9a57592817d7f16616ee7fb25989e580a70160acc`.
Runner guards (read from source): `PR_SET_DUMPABLE 0` before spawning the tool
(`c42_count_v3.py:566`), timing file opened for append (`:602`), runner writes
its authoritative line only after the tool exits and all orphans are reaped
(`:568-575`), counter parses the last non-empty line (`:631-637`).

## Scoring runs (real counter, fresh random seeds, no --seed)

| Tool (sha256) | Command exit | Receipt | Result |
|---|---|---|---|
| `controls/w1/CtlCpuHide/ctl_fake_timing.py` `f010a46b…` | 1 (not met) | `/fast/scratch/hyaku/kake-r42w2/SentinelV3Timing/fake_timing_v3.json` (seed 192650046095513) | equalRuns **10/10** (judgments byte-equal to tip41), ratios T1 4.09 / T2 2.744 / T3 1.396 / T4 1.232 / T5 10.783 — **real CPU measured**, no forge; e.g. T1 candCpu 1.67–1.93s vs base40 0.40–0.47s, candExit 1 = ref41Exit 1, candOutSha256 = ref41OutSha256 |
| `controls/w1/SentinelCounterSandbox/timer_probe.py` `7e8556d7…` | 1 (not met) | `…/timer_probe_v3.json` (seed 186149813385561) | equalRuns 0/10; run A candExit 1, candOutSha256 `e3b0c442…` (empty stdout — **no `TIMER_WRITE_OK`**, open failed before write); ratios reflect the probe doing no work |

Commands (both):
`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count_v3.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <tool> --label SentinelV3Timing-<suffix> --out /fast/scratch/hyaku/kake-r42w2/SentinelV3Timing/<suffix>_v3.json`
→ exit 1, `met:false` in both receipts.

## New forging routes tried (local replica of `Sandbox.run` + v3 `RUNNER`, identical bwrap argv; receipts in `/fast/scratch/hyaku/kake-r42w2/SentinelV3Timing/lab/harness.py` + probes)

1. **/proc/<runner>/fd via different paths** (`probe_fd.py`): `listdir("/proc/<ppid>/fd")` → errno 13 EACCES; same for `/proc/<ppid>/task/<tid>/fd`; `O_PATH` reopen of `/proc/<ppid>/fd/N` → EACCES; `/proc/<ppid>/{root,cwd,exe}` → EACCES. Control run with the v1-mode runner (no dumpable bit): **FD4=OK** (timing fd reopened writable), O_PATH ok, root/cwd/exe ok — so the harness reproduces the v1 exposure and v3 closes it.
2. **pidfd_open + pidfd_getfd** (`probe_pidfd.py`): cmdline readable, tfd=4 learned; `pidfd_open` succeeds, but `pidfd_getfd(4)` → EPERM in **both** v3 and v1-mode runs (no CAP_SYS_PTRACE; sandbox CapEff=0, CapBnd=0 — `probe_ns.py`). No fd stolen.
3. **Signals** (`probe_sig.py`): SIGKILL of the runner (parent) from a forked helper → runner dead, **no timing line at all** (BWRAP_EXIT=137, TIMING_LAST_LINE=None) → cpu None → shape has no median → not met. DoS only, cannot forge a lower CPU.
4. **Nested user+PID namespace** (`probe_ns.py`): `unshare(CLONE_NEWUSER|CLONE_NEWPID)` succeeds inside the sandbox (uid→65534), but ptrace attach to the runner is EPERM before and after — ancestor-namespace CAP_SYS_PTRACE is not conferred. Dead.
5. **Append-ordering defense** (`probe_append.py`): even in the v1-mode control where the fd IS stealable and the forged tail is written (`FORGED_WRITE=OK`, timing file 21→42 bytes), the last non-empty line is still the runner's real line in0 0.010061 0.020033` — the runner writes after the tool exits, so O_APPEND + last-line-wins cannot be beaten by any pre-exit write.

## Per checked statement

- "the tool cannot reopen the runner's descriptors through /proc" (`c42_count_v3.py:40`) — **holds**: every /proc alias returns EACCES; independent receipts above.
- "the timing file is opened for append" (`c42_count_v3.py:40`) — **holds and is sufficient on its own** against the v1 fake-timing write order (receipt 5).
- "a run without a runner timing line has no CPU time, and a shape without a median has no ratio (not met)" (`:58`) — **holds**: kill-route receipts show no line → no ratio.
- CPU = user+system of the tool and every descendant, read by the fixed runner — **holds for all routes attempted**; no lower-CPU forge observed in either w1 forger or any new route.
- Exit-code contract (0 met / 1 not met / 2 cannot evaluate) — **holds**: both scoring runs exited 1 with `met:false`.

## Residual risk / verification gaps

- The `PR_SET_DUMPABLE 0` guard is per-process; the runner sets it once before spawning (`:566`). No race was found (sequential in the same process). untested: an attack that pre-seeds the timing file **before** the runner's first write (the counter opens `"ab"` on a fresh random path per run — file cannot be pre-created with a known name); and exotic ptrace-via-Yama interactions (Yama not loaded/enforced in this kernel, `ptrace_scope` defaults).
- The O_APPEND defense is only as strong as the runner writing *after* every descendant; a descendant that could outlive the `os.wait()` loop would need to survive the runner's write (impossible: the loop blocks until all children are reaped).
- Not re-run: H1-H5 harm rules (out of scope for this seat); build scoring (main agent's).

Tool installs: none (no pacman/uv/cargo/npm action taken). Network: none.
