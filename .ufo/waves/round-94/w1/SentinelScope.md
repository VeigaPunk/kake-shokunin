# SentinelScope — round 94 (kake, hyaku run 15, attempt 1), wave w1

VERDICT: scope defect — a `subprocess.py` placed in the counter's own script directory runs at import time, before either counter's guard (`c94_selfassess.py:72` import, guard `shadow_check` at `:103` runs only later at `:736`; `c94_conditional.py:46` import, no guard at all). Verified: `MARKER` written and exit 7 from both counters. Credential scan: no secret-shaped string; 4 hits are the scan regex literal inside the orchestrator's own task text. Counter writes are contained under `--work` / scratch.

Scope: read-only audit of the round's counters and seat activity. Frozen files were not edited. Scratch `/fast/scratch/hyaku/kake-r94/SentinelScope/` deleted before yield; receipts copied to `.ufo/waves/round-94/w1/SentinelScope/receipts/`.
Frozen counter digests (sha256): `c94_selfassess.py` 58028584…a8306a; `c94_conditional.py` 357d8cd1…d2a750a (receipts/counter-sha256.txt).
Freeze commit `ba667b24`, 2026-11-05T11:58:20-03:00.

## Commands run, exit codes

| # | command (LANE = /home/vgpnk/Projects/shokunin/kake-shokunin) | exit | result |
|---|---|---|---|
| A | `python3 -B LANE/.ufo/waves/round-94/c94_selfassess.py --root LANE --revision 0f7d9bb… --skip-battery` (under `strace -f`) | 1 | `C1v94 … mismatches=15 E5=15 … met=false` (base control, expected) |
| B | `python3 -B LANE/.ufo/waves/round-94/c94_conditional.py --root LANE --revision 0f7d9bb… --work <scratch>/work/cond` (under `strace -f`) | 0 | `C2v93 … hand=53/53 generated=120/120 forgeries_refused=6/6 positive=admitted … met=true` |
| C | `python3 -B c94_selfassess.py --root LANE --revision 0f7d9bb… --work <scratch>/work/battery` (under `strace -f`, full battery) | 1 | `battery=8/8 predecessor_admits=7/7 … mismatches=15 … met=false` (fails only on the 15 base E5 findings) |
| D | `bwrap --ro-bind / / --dev /dev --proc /proc --unshare-user true` | 0 | usable |
| E | `bwrap … --unshare-all true` | 0 | usable |
| F | planted-module test: copy of each counter + `subprocess.py` in the same dir that writes `MARKER` then `raise SystemExit(7)` | 7 (both) | `MARKER` written, see F1 |
| G | `grep -rEn 'AKIA|ghp_|sk-[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY|op://' .ufo/waves/round-94` | 0 | 4 hits, all false positives (F5) |

Tools: none installed or upgraded. Used existing `/usr/bin/strace` and `/usr/bin/bwrap`. Pacman not used. No changes to host sysctls.

## Check 1 — lane `git status --porcelain` before/after

- Before counter runs: `?? .ufo/waves/round-94/{w1-dispatch.err, w1-dispatch.json, w1-spec.json, w1.ready, w1.ready.dispatched, w1/}` (orchestrator and seat-dispatch files; not from this seat).
- After A (selfassess): one new entry, `?? corpus/lessons/round-94.md` (created 12:01:23 -0300). Not written by the counter (strace A: 0 write-capable opens, 0 mkdir/rename/unlink). Content header is the round-94 lesson; writer not verified (item says the L1 owns it).
- After B (conditional) and after C (battery): status identical to the pre-run list above plus that one lesson entry.
- Non-status changes in the same window (from `find -newer freeze.md`): `w1/MutC1/`, `w1/ExecC2Mutants`, `w1/ScoutRFC/`, `w1/ConnectorScope.md`, `w1/SentinelScope/` (mine). Seat report directories; expected.
- Files left in LANE by this seat: `w1/SentinelScope.md` and `w1/SentinelScope/receipts/` only.
- Receipts: `receipts/status_before.txt`, `status_after_sa.txt`, `status_final.txt`.

## Check 2 — counter writes stay under `--work` / TMPDIR

- A (selfassess, `--skip-battery`, no `--work`): `strace -f` over all children. 0 write-capable opens (`O_WRONLY|O_RDWR|O_CREAT|O_TRUNC`), 0 mkdir/rename/unlink/link/symlink/chmod, outside `/dev/null`. 0 references to `/tmp`. Only reads: LANE `.git` objects and refs, `~/.config/git/config`, the counter file, `frozen/c1-surfaces.json`. Receipt: `receipts/selfassess.strace.gz`.
- B (conditional, `--work <scratch>/work/cond`): all writes under `<scratch>/work/cond/c93c-<pid>/` (sandbox.py, tree/, frozen population copy). The tree is removed in `finally` (`unlinkat`/`rmdir` observed). 0 `/tmp` references. Scratch work dir empty at end (0 bytes). Receipt: `receipts/conditional.strace.gz`.
- C (battery, `--work <scratch>/work/battery`): 485 write ops under `<scratch>/work/battery/`. 0 write ops with an absolute LANE path. The relative `.git/objects/..` writes come from fixture commits (`git -C <scratch fixture> add -A` / `commit -q -m fixture`, pids 2874552…2875699). 0 `/tmp` references. Receipt: `receipts/battery.strace.gz`.
- git invocations by the battery: 693 with `-C <LANE>` (cat-file 516, show 174, ls-tree 2, rev-parse 1) and 198 with `-C <scratch>`. All LANE calls are read-only subcommands.
- Default-path note: with no `--work` and no `--skip-battery`, `battery()` falls back to `$TMPDIR` or `/tmp/c94bat-<pid>` (`c94_selfassess.py:587-591`, removed in `finally`). That path was NOT exercised in this audit (I passed `--work`). Limit.
- Self-introduced writes under LANE `.git`: `git status` (my baseline calls) refreshed `.git/index` (mtime 12:00:54 -0300, my first status call). Benign index stat refresh; no tracked content changed. Noted for the record: read-only `git status` is not write-free.
- **Unattributed LANE `.git` changes in the battery window:** `.git/objects/pack/pack-4e4ed4982385a929921c1794e9db9da5b5211a24.pack` mtime 12:02:32 -0300 and `.git/` directory mtime 12:02:49 -0300. Battery trace has zero absolute-LANE write ops, so these come from a concurrent process I did not trace (another seat or host tool). Cause not identified. L1 should check whether a `gc`, `repack` or `status` ran in LANE at that time.

## Check 3 — credential, environment and home reads (both counters)

Grep over `c94_selfassess.py` and `c94_conditional.py`:
- `os.environ` / `os.getenv`: only `os.environ.get("TMPDIR", "/tmp")` (selfassess `:589`, `:616`; conditional `:490`). No other env reads.
- `expanduser`, `Path.home`, `.ssh`, `.config`, `.omp`: 0 hits.
- `token`, `key`, `secret`, `password`, `credential`: only prose, regex messages ("is not a token"), and dict keys (`for key in ...`). No credential handling.
- Network libraries (`urllib`, `http.client`, `socket`, `requests`, `urlopen`) and `jj`/`curl`/`gh`: 0 hits.
- Subprocesses: `git` only (`["git", "-C", root, ...]`), plus `sys.executable -B <sandbox|counter copy>`. The battery's sub-counter env is restricted to `PATH=/usr/bin:/bin, HOME=<work>, TMPDIR=<work>, PYTHONPATH=""` (`run_counter`, `c94_selfassess.py:~403`). The main counter and the conditional's `git` call inherit the full environment.
- Environment check: only `GIT_EDITOR, GIT_PAGER, GIT_SEQUENCE_EDITOR, GIT_TERMINAL_PROMPT` are set. No `GIT_DIR` or `GIT_INDEX_FILE` in this shell (counters would inherit them if set; that is a limit).
- Home reads: git itself reads `/home/vgpnk/.config/git/config` (2078 opens in trace A, 32 in trace B). That is inside `$HOME`, performed by git, not by counter code. No `.ssh`, `.omp`, or credential-file reads observed in any trace.
- Sandbox (conditional): the candidate runs under an audit hook (`c94_conditional.py` SANDBOX, ~`:375-398`) that refuses `os.system`, `subprocess.Popen`, `os.spawn*`, imports outside an allow-list, and file opens outside the subject tree and std prefixes. Env for the sandbox: `PATH=/usr/bin:/bin, HOME=<work>` only.

## Check 4 — the battery's shadow-subprocess route (code read + run C)

- F1 (`c94_selfassess.py:~502-540`): (a) the copied counter in a shadow dir with a fake `subprocess.py` must refuse. Run C: `self_rc=2`, `selfcheck=shadowed`. Good. (b) the predecessor runs with `subprocess.run` replaced in-process by `injected_git(CLEAN, rev)` (`:531-532`), restored in `finally` (`:537`). The stub answers only `rev-parse`, `show`, `ls-tree`; any other subcommand returns `128`. So F1 cannot spawn real git.
- **Limit (not contained):** the stub covers `subprocess.run` only, and only for the duration of `pmod.audit(...)`. Predecessor code is loaded in-process by `load_module` (`:384-387`) from frozen predecessor bytes (`:440-443`). It runs with the counter's full authority: it can `open()` any path, call `os.system`, or `os.popen`. The containment rests on the predecessor being a frozen, committed file. The conditional's SANDBOX (check 3) is the stronger model; the self-assess battery has no equivalent.
- The battery's fixtures are all under `<work>/battery/` (`make_repo` with `shutil.rmtree` + `makedirs` on the work path). Verified by trace C.

## Check 5 — credential-shaped strings in round-94

`grep -rEn 'AKIA|ghp_|sk-[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY|op://'` over `.ufo/waves/round-94`, exit 0, 4 hits, all false positives (the scan regex literal inside the orchestrator's task text, not a secret):
- `.ufo/waves/round-94/w1-dispatch.json:84` (`AKIA`, `ghp_`, `op://` literal)
- `.ufo/waves/round-94/w1-dispatch.json:153` (same)
- `.ufo/waves/round-94/w1-spec.json:55` (same)
- `.ufo/waves/round-94/w1/swarm-registry.json:66` (same)
- `sk-…` and `BEGIN … PRIVATE KEY`: 0 hits. Broad grep (`password|secret|token=|api[_-]?key`) names only the same 3 JSON files, all of which are the task text. No secret found.

## Check 6 — sysctl and bwrap

- `/proc/sys/user/max_user_namespaces` = `122865` (read only; not written).
- `/usr/bin/bwrap` usable: `--unshare-user` exit 0; `--unshare-all` exit 0. No host sysctl change needed.

## Check 7 — writes outside LANE by this wave's seats

- `/home/vgpnk/Projects/shokunin/.ufo/waves/round-94` does not exist (fleet root). Nothing to list under that path.
- Fleet-root files newer than the freeze (`-maxdepth 2`, excluding LANE): `.ufo/watchdog.log`, `kasegi-shokunin/LOG.md`, `kasegi-shokunin/SCORECARD.md`, `kotoba-shokunin/plans`, `.scratch/run15-state.json`, `.jj/repo`, `.jj/working_copy`. These are other lanes and host tooling, not round-94 seats (round-94 seats write under LANE only). Owner not verified; not in my scope to fix.

## Findings

**F1 (scope defect, verdict) — planted module runs before the guard.** Python with `-B` puts the script's directory first on `sys.path`. Any file `subprocess.py` in `LANE/.ufo/waves/round-94/` is imported by the counter before any check.
- Evidence: receipt `receipts/planted-MARKER.txt` ("planted subprocess.py imported"), `receipts/planted-subprocess.py.txt` (the planted file), exit 7 from both `c94_selfassess.py` and `c94_conditional.py` copies.
- `c94_selfassess.py:72` imports `subprocess`. The shadow check at `:103` (`shadow_check`) and its call at `:736` run after the import. A module-level planted file therefore runs first. The guard refuses only after code has already executed. Only the copy in a scratch dir was tested, not the frozen file itself in LANE.
- `c94_conditional.py:46` imports `subprocess`. There is no shadow check in this counter (grep for `shadow`: none).
- Impact: a seat or process with write access to `round-94/` can run code inside the counter process and print a forged `C1v94 … met=true` line. The forgery needs the counter's sha256, which is public (F2 check in `c94_selfassess` only verifies the digest string). Smallest remediation (not applied, frozen): invoke with `python3 -I` or `python3 -P` (Python 3.11+ — this host runs 3.14), or move the import of anything the counter needs to run from a directory without writes.

**F2 (label defect in frozen v2 counter).** `c94_conditional.py` prints `C2v93 …` and `seed=93` and names its scratch `c93c-<pid>` / `c93sel-<pid>`. It is the v2 counter but reports itself as v93. Receipt line: `receipts/conditional.stdout` line 1. The L1 should not cite it as a v94 receipt without noting the label.

**F3 (PATH-resolved git).** Both counters call `git` through the inherited PATH with no absolute path. Strace shows lookups across `~/.local/bin`, `~/.opencode/bin`, mise shims, and fnm multishells before `/usr/bin/git`. A `git` earlier on PATH would run against the lane with the counter's authority. Not exploited; limit. The battery's sub-counters get `PATH=/usr/bin:/bin`, the main path does not.

**F4 (battery not contained).** See check 4: predecessor code runs in-process with full authority. Frozen input; limit, not a fix request.

**F5 (scan false positives).** Four regex-literal hits in task text, check 5. No secret.

**F6 (`git status` writes index).** My own `git status` calls refreshed `.git/index` (12:00:54 -0300). Benign; disclosed so the "read-only git" claim is qualified.

**F7 (unattributed LANE `.git` writes).** pack mtime 12:02:32 -0300 and `.git/` dir mtime 12:02:49 -0300, during the battery window. Not from the battery (0 LANE write ops in trace C). Cause unidentified. Owner needed.

**F8 (/tmp writes outside scratch, other actors).** `/tmp/x.tar` (141,731,840 bytes, 12:01, over the 50 MB scratch rule), `/tmp/r40tree`, `/tmp/freeze-gate-0je56adx` (replaced `freeze-gate-bhoziiya`), `/tmp/kasegi_r78_S112.txt`. Zero `/tmp` references in any counter trace, so not from the counters. Owners not verified.

**F9 (lane `.jj` write).** `LANE/.jj/repo/store/extra` mtime newer than the freeze. This seat ran no jj command. Origin not identified.

**F10 (lesson file).** `LANE/corpus/lessons/round-94.md` appeared during this audit (12:01:23 -0300). Owner (L1) per the item; not verified.

## Honest limits

- strace filters: `open/openat/creat/mkdir*/unlink*/rename*/rmdir/symlink*/link*/chmod/truncate/execve`. Not traced: `io_uring`, `mmap` writes, network sockets, and any process outside this seat's own process tree. Concurrent writers (F7, F8, F9, F10) were not traced.
- Ran the battery only with `--work`. The default `/tmp` path (no `--work`) was read, not executed.
- Did not verify F1 against the frozen LANE file itself (copy in scratch only). The import order is fixed by Python, so the conclusion holds for the frozen file in the same directory, but I did not run that exact file.
- Did not test whether `c94_conditional.py` run from a planted dir would also refuse the planted module at its sandbox level (the sandbox is a separate process; the planted module ran in the parent).
- `git` `GIT_*` override variables were not set in this shell, so the GIT_DIR/GIT_INDEX_FILE exposure was not exercised.
- Did not inspect LANE `.git/hooks`, `config`, or any `core.fsmonitor` setting; git would run them only on write commands, which the counters do not issue.

## Receipts (under `.ufo/waves/round-94/w1/SentinelScope/receipts/`)

- `selfassess.strace.gz`, `selfassess.stdout`, `selfassess.stderr` (run A)
- `conditional.strace.gz`, `conditional.stdout`, `conditional.stderr` (run B)
- `battery.strace.gz`, `battery.stdout`, `battery.stderr` (run C)
- `planted-subprocess.py.txt`, `planted-MARKER.txt`, `out.txt`, `out_s.txt` (run F)
- `status_before.txt`, `status_after_sa.txt`, `status_final.txt` (check 1)
- `counter-sha256.txt` (frozen digests)

Scratch `/fast/scratch/hyaku/kake-r94/SentinelScope/` deleted after the receipts were copied.
