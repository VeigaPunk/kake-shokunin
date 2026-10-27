# SentinelC1Exec

Seat scope: execution safety of the frozen C1 counter
`.ufo/waves/round-60/c60_gate_status.py` (blob at B1 `8b33fd24`, read from a `--shared` clone of the lane).
I did not run the 28-member measurement and make no claim about C1's met/unmet verdict; everything below is
about the executor: process construction, argv/env rendering, scratch and clone lifecycle.

ATTACKS: shell and argv construction · env scrubbing (`PYTHONPATH`, `PYTHONSTARTUP`, `PYTHONHOME`,
`sitecustomize.py`/`usercustomize.py`/`.pth` inside the clone) · a member writing outside its clone and to the
lane `.git` · a member that never exits · a member that double-forks a daemon · grandchildren after timeout ·
SIGINT/SIGTERM mid-run · foreign dirs under `--work` · `/tmp` fallback · git option injection via `--root`/`--revision`
· unexpected exceptions vs the kill rule · the frozen 28-member map.

ATTACKS RUN:
1. Env/import hijack — hostile parent env + `sitecustomize.py`, `usercustomize.py`, `leak.pth` in the clone and on
   `PYTHONPATH`. HELD: child env is exactly `{PATH=/usr/bin:/bin, HOME=<scratch>, TMPDIR=<scratch>, LANG=C.UTF-8}`,
   no leak (`sitecustomize leak=False .pth leak=False`), `-B`, `stdin=/dev/null`, member stdout/stderr discarded.
2. No shell — `grep -nE "shell=True|os\.system|os\.popen"` finds nothing; all three call sites use list argv
   (`:152`, `:382`, `:404`). Metachar/pure-placeholder words are refused (`metachar -> 'meta'`,
   `--work=<scratch> -> 'meta'`).
3. Git option injection — `--root=--upload-pack=/bin/true` and `--revision=--all` / `=--verify` all end in exit 2
   (toplevel/revision check), and `^{commit}` is appended before verify, so no option is ever formed.
4. Escape — a member run wrote `…/probe/ESCAPED_WRITE` outside its clone; `os.access(lane/.git, W_OK) is True`;
   a member bound and connected a loopback socket (no network/fs isolation of any kind).
5. Processes — a double-forked daemon is alive after `run_member` returned, cwd = the **deleted** clone; on timeout
   (`TIMEOUT=5` monkeypatch) the counter returns 124 while a forked grandchild survives reparented.
6. Signals — SIGINT: exit `-2` (128+2, i.e. not a verdict), leftovers `[]`; SIGTERM: exit `-15`, leftover
   `c60-run-*`; SIGTERM without `--work`: leftover `c60-work-*` in `TMPDIR`.
7. Cleanup — a member that leaves a `0500` dir makes `shutil.rmtree(..., ignore_errors=True)` fail silently and the
   run dir stays (normal exit, no signal). `--work` cleanup deletes any foreign `c60-run-*`/`c60-self-*` dir.
8. Fallback — with `TMPDIR` unset the work dir is created under `/tmp` (`/tmp/c60-work-…`).
9. Kill rule — an unexpected exception (`ValueError`) exits **1**, the code that means "not met", with no verdict line.
10. Population (C1 term `members == 28`): re-derived with the counter's own `POP_RX` at base `97cdc122` and at B1 —
    28 and 28, no extras, all 28 `FROZEN` blob ids match at both revisions.

FINDINGS:

| severity | target file:line | issue | evidence | fix |
|---|---|---|---|---|
| medium | `.ufo/waves/round-60/c60_gate_status.py:404-409,411` | No process containment. Members run in the caller's session with no `start_new_session`, no process-group kill, no rlimits. A double-forking member outlives the counter; on timeout only the direct child is killed, so grandchildren persist and the run is still reported. | probe_all.py §4: `fork_m rc=0 daemon alive after run_member returned: True cwd=…/clone (deleted)`; `loopfork_m.py rc=124 … grandchild alive=True ppid=1494` | `subprocess.run(..., start_new_session=True)` and on `TimeoutExpired` `os.killpg(proc.pid, SIGKILL)`; wrap in `bwrap --unshare-all --die-with-parent` (or at least `resource.setrlimit(RLIMIT_NPROC/RLIMIT_CPU)`) in `preexec_fn`. |
| medium | `:484-497` + `:408-409` | A hung observation (exit 124, i.e. "we never finished") is scored as a **label** mismatch — `historical_bad_exit`, `never_met_bad_exit`, `live_not_green` — and the process exits 1 = "not met" per the contract's kill rule, so a blocked/slow member is recorded as proof that a registry row lies. Exit 124 also collides with a member that legitimately exits 124. | probe_all.py §5: `kind=historical e_T=124 e_P=124 classes=['historical_bad_exit','historical_not_green_at_pin']`; `kind=live … ['live_not_green']` | Give timeout its own class (`timed_out`) and make `measure` return 2 (unevaluable, no verdict) when any `e_T`/`e_P` is 124 or negative; only tighten, so it cannot be used to dodge a red. |
| medium | `:410-411`, `:1160-1166` | The docstring's "they are removed on exit" is false for any signal and for any cleanup error: `rmtree(..., ignore_errors=True)` swallows failures, and `main`'s `finally` only runs for handled exceptions/SIGINT. | probe_all.py §2b `locked_m rc=0 leftovers=['c60-run-…']`; §9 `SIGTERM exit=-15 leftovers=['c60-run-…']`, `SIGTERM without --work … TMPDIR residue=['c60-work-…']` | `rmtree(..., onerror=chmod-and-retry)` and print a warning on residue; install `SIGTERM`/`SIGHUP` handlers that run the same cleanup as `finally`. |
| medium | `:1160-1166` | `--work` cleanup deletes **every** entry named `c60-run-*`/`c60-self-*` in the work dir, not just its own. Two counters sharing one `--work` (or any unrelated dir with that prefix) delete each other's in-flight run dirs → spurious `OSError`/clone failures → false reds, and a destructive surprise. | probe_all.py §7: `counter exit=2 \| KEEPME still there: False \| shared now: []` | Track created dirs in a set and delete only those; never prefix-scan a caller-supplied `--work`. |
| medium | `:349-355`, `:401-405` | No isolation, and `validate_command` bounds only the *shape* of argv, not its values: any flag and any path are accepted (`--work /home/vgpnk/Projects/shokunin/kake-shokunin`, `--out ../../`, `--fleet <fleet root>`). A4 freezes the 28 member blobs, so the *code* is pinned to base bytes, but the *arguments* come from `SKILL.md` at the measured revision, which is exactly the tree under test. Anything a member does with that path lands in the lane. | probe_all.py §2 (`writable lane .git=True`, `ESCAPED_WRITE: True`) and §6 (`lane path as flag value -> None`, `relative escape -> None`) | Reject any argument token that is an absolute path, contains `..`, or is `<fleet root>`; allow-list the flags each frozen member may receive (the round-59 per-member documented flags are already in the registry). |
| low | `:1143-1144` | With `TMPDIR` unset the work dir is created under `/tmp` (the documented 'else the system temp' fallback), so a caller who forgets `TMPDIR` writes clone trees and fixture repos to `/tmp`, and (with the cleanup finding) leaves them there after SIGTERM. | probe_all.py §8: `work dir=/tmp/c60-work-… existed=True` | Require `--work` or `TMPDIR` (exit 64 otherwise), as the contract's observation stanza already assumes. |
| low | `:1156` | Only `RuntimeError`/`OSError` map to exit 2. Any other exception exits **1** — indistinguishable from "not met" — and prints a traceback with no `C1 gate-status …` verdict line, so a receipt that records only the exit code records a false verdict. | probe_all.py §11: `exit=1 stderr_last='ValueError: logic error' stdout=''` | Catch `Exception` and return 2, keeping the traceback on stderr; reserve 1 strictly for `met=False`. |
| low | `:67-68` | Docstring overclaims what it enforces: "No network" is true of the counter, not of the 28 members it runs — a member bound and connected a socket; "Read-only" likewise describes the counter, while members run with the caller's uid and the lane's `.git` writable. | probe_all.py §3 (`socket bind+connect=True`), §2 | Reword to "the counter makes no network calls; members are not sandboxed", and state the trust boundary (frozen blobs, unfrozen argv) explicitly. |

Held (no finding): env is exactly the four documented variables and no import hook from the clone, `PYTHONPATH`,
`PYTHONSTARTUP` or `.pth` reaches a member; there is no shell anywhere; member output never feeds a verdict; git args
are fixed, NUL-safe and hex-validated; a failed clone raises `RuntimeError` and still removes its run dir
(`leftovers after clone failure: []`); the run dir is removed on normal exit and on SIGINT.

Untested / deferred: the full 28-member measurement (L1's job); whether a member's own subprocesses ever write outside
scratch in the current population (`[INFERENCE]`: none observed — only my probe members were hostile); object-store
safety of `git clone --shared` — I tested the `git gc --prune=now`-in-the-clone path and the source objects survived,
so no finding is raised for it.

VERDICT: The counter's own process is read-only and its env/shell/argv construction holds, but it provides no
containment (orphaned daemons, silent scratch residue, foreign-dir deletion under `--work`, `/tmp` fallback) and it
converts a hung observation or an internal crash into "not met" — the L1 must read `e_T/e_P == 124` (and any
non-0/1/2 exit) as unevaluable, not as a label mismatch.
