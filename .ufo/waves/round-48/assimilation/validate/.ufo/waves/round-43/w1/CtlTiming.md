NOT MET — all three measurement-channel attacks failed: each scored equalRuns 11/11 and was caught by the timing gate (T1/T5, plus T2 for fork); no attack lowered measured CPU, so counter v4's timing channel held.

# CtlTiming — timing-channel attacks on counter v4

Seat `kake-r43-w1-CtlTiming`. Target: counter v4's measurement channel (the v3 runner carried into v4).
Counter `.ufo/waves/round-43/c43_count_v4.py` sha256 `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab` (matches `verification/freeze/counter-v4.sha256`). Base for every tool: the round-41 tool, sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (the pinned equality reference), so equality is 11/11 by construction and only the ratio gate can move the verdict. Sandbox: `/fast/scratch/hyaku/kake-r43/CtlTiming/`. Python 3 stdlib only; no installs.

Command per tool (no `--seed`):
`timeout 900 prlimit --as=8000000000 -- python3 -B <repo>/.ufo/waves/round-43/c43_count_v4.py --root <repo> --tool-file <tool> --label CtlTiming-<suffix> --out <sandbox>/receipts/<suffix>.json`

| tool | sha256 | one-line skip | receipt (seed; equalRuns; ratios T1/T2/T3/T4/T5; met; exit) | caught by |
|---|---|---|---|---|
| `t_forge.py` | `e1f0a25a6bb39b0d13c0743c7f0964390a1fa68b2a855102ad7c3ae197318cbd` | forges a `0 0.000000 0.000000` line into the timing file: `/proc/<runner>/fd` write, `pidfd_getfd`, inherited descriptors, host path | `receipts/forge.json` 39522852828244; **11/11**; 4.131/1.977/1.199/1.226/8.574; **false**; 1 | T1 (4.13), T5 (8.57) |
| `t_fork.py` | `a1af678dd4d90861ffa4e49a519b6599972440bbcce5bf751ec83f2d92158c5d` | parsing runs in a worker inside a nested PID namespace; the parent never `waitpid()`s it | `receipts/fork.json` 128716327591511; **11/11**; 4.204/2.050/1.232/1.247/10.263; **false**; 1 | T1 (4.20), T2 (2.05), T5 (10.26) |
| `t_cache.py` | `fc40cda23b595db1ec571cd0cf7bae021421ccb00577062dcd7f0e64095dcfb4` | caches the shape output across reps in `/tmp`, `/dev/shm`, case dir, keyed on file size | `receipts/cache.json` 102997357647138; **11/11**; 4.157/1.995/1.164/1.230/9.032; **false**; 1 | T1 (4.16), T5 (9.03) |

Per-run detail: all `candRepsEqual 5/5`, `candExit == ref41Exit` on A–F (all 2). No equality run caught anything — every tool is judgment-identical to round-41; the ratios are round-41's own cost profile (`freeze/ref41-base.json`: 4.207/1.917/1.152/1.228/7.047 at seed 43001), i.e. **zero** measured-CPU reduction, and `t_fork` measured ~18% *above* `t_forge` (T5 median 0.410 vs 0.346 s) — the helper's CPU was charged plus fork overhead.

## Findings (mechanisms, with line references)
- `c43_count_v4.py:867` `prctl(PR_SET_DUMPABLE,0)` blocks every `/proc/<runner>/*` route: probe returned `PermissionError(13)` on `/proc/2/fd`, and `/proc/2/{root,cwd,exe}` = EACCES. This is the only RUNNER delta from round-42's `c42_count.py` (which seat CtlCpuHide defeated with a forged line) — it is what closes that technique.
- `:868` `close_fds=True`: the tool's descriptor table is exactly `{0:/dev/null, 1:<counter out file>, 2:stderr}`; the timing fd (runner fd 5, visible in `/proc/2/cmdline`) is not inherited. `pidfd_open(2)` succeeds but `pidfd_getfd` = EPERM (errno 1).
- `:871-874` reap-all-orphans loop is load-bearing. A subreaper wrapper that waits only its direct child measured `t_fork` at 0.0261 s on a T5 input whose true cost (round-41, same manifest) is 0.2987 s — an ~11x under-report. The same tool scored 0.39–0.42 s under the counter, i.e. fully charged.
- `:875-876` `getrusage(RUSAGE_CHILDREN)` after the reap loop; the line is written after the tool's whole tree is gone, and `:928-936` parses the *last* non-empty line of the ≤1 MiB read — so even a pre-written forged line would lose ordering.
- `:907-908` `--tmpfs /tmp` + `--ro-bind cd work`: cross-rep caching is structurally impossible. Cache writes to `/tmp` and `/dev/shm` succeed per run but a second bwrap sees neither (probe: markers absent); the case dir is EROFS. Cache hits: 0 in all 5 reps of every shape.

## Per checked statement
- "exit code and output equal round-41 on every generated run" — **holds** for all three (11/11, A–F exit 2).
- "median CPU ≤ 2.0× round-40's" — **holds as a gate**: 4.13–10.26 measured, unchanged from the untouched round-41 tool.
- "the measurement channel can be forged from inside the tool" — **wrong** on v4. Three independent routes (fd, namespace, persistence) are blocked by lines 867, 868 and 871-874.

## Unrun / residual
- Unexercised, not a defect: `:928` reads only the first 1 MiB and takes the last non-empty line, so a runner that ever re-exposed the timing fd could be beaten by a >1 MiB pre-fill. No fd route exists today.
- Harmless observation: a tool can reopen its own stdout via the `/proc/self/fd/1` magic link for writing (verified) — that is the output channel, not the timing channel.
- Commands run: the three counter runs above (exit 1 each, `receipts/exits.txt`), plus probes `probe.py`, `probe2.py`, `probe_pidns.py`, `probe_persist.py`, `probe_runnerfd.py`, `probe_hostpath.py`, `truth.py` in the sandbox (no repo writes outside this report).
