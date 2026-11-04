VERDICT: C2 falsified at the committed carrier 7f6c68f1 — the execution-time sandbox is defeated in-process (6 of 20 candidates reach the round-89 reference and score met=true); the uncommitted working-tree sandbox under edit refuses even conforming positives, so no sandbox currently satisfies C2.

Seat: ExecSandbox (leaf). Target: `SANDBOX` string in `scripts/cache_key_conformance.py`.
Scratch (deleted before yield): /fast/scratch/hyaku/kake-r90/ExecSandbox/. Copied receipts: `w1/ExecSandbox/receipts/`.
Candidates: `w1/ExecSandbox/c01..c21` (20 files; c14 was discarded during authoring, no candidate numbered c14 exists).

## Object attacked

- Committed gate `7f6c68f1` = blob `2840f32e…` (HEAD `79e1aac2` carries the same blob). Pinned copy: `receipts/gate_committed_7f6c68f1.py`, sha256 `2840f32e53317327fbaa6df3f8e02da06363e0fcda829270651a356192517591`. Its SANDBOX is `receipts/sandbox.py` (dumped from that blob).
- Working tree at run time: `scripts/cache_key_conformance.py` is modified and uncommitted (L1 hardening: closure-bound hook, `marshal.load`/`sys._getframe`/`gc.get_*` denies, `object.__setattr__` guard). Pinned copy at run: `receipts/gate_worktree_snapshot.py`, sha256 `33650406be208b47507698884713cb093ec71fb1ff81b2de21584104ecadf08c`. The file changed again during this seat (an earlier read was `bce2291b…`), so the working tree is not a stable object; I cite only the pinned copy.

## Commands

- Sweep: `W=/fast/scratch/hyaku/kake-r90/ExecSandbox; $W/sweep.sh <gate.py> <outdir>` = for each candidate `python3 -B <gate> --candidate <abs path> --work $W/work --seed 4242 --verbose`. Seed fixed to 4242 so both gates see identical generated cases. Outputs: `receipts/committed-7f6c68f1/*.txt`, `receipts/worktree-at-run/*.txt`, summaries `receipts/summary-*.txt`, per-candidate events `receipts/events.txt`.
- Positive check: `python3 -B <gate> --candidate <abs>/.ufo/waves/round-89/w1/L1/cache_key.py --work $W/work --seed 4242` → `receipts/positive-L1-r89-{committed,worktree}.txt`.
- Pins: `receipts/pins.sha256`.
- All gate runs exit 1 on refusal, 0 on met. Gate runs are read-only with respect to LANE (work dir only under scratch).

## Results on the committed gate 7f6c68f1 (`receipts/committed-7f6c68f1/`)

Escapes (sandbox=ok, clauses 6/6, hand 70/70, generated 120/120, met=true; keys match the gate's own reference on every case):

| cand | route | why the hook does not fire |
|---|---|---|
| c05_frame_globals_roots | `sys._getframe(0)` walk to the sandbox frame; `f_globals["_roots"] = ("/",)`; `open(REF)` | `_hook` reads `_roots` from module globals at call time; `sys._getframe` is not in `_DENY`; the widened prefix passes `rp.startswith(_roots)` |
| c13_hook_die_noop | same frame walk; `f_globals["_die"] = lambda why: None`; `open(REF)` | `_die` is a module global called by `_hook`; when it returns the hook falls through and the `open` proceeds |
| c18_no_hook_reimport | `gc.get_objects()` finds the function named `_hook`; rebind `__globals__["_die"]` and `["_roots"]`; `open(REF)` | `gc.get_objects` is not in `_DENY`; the hook's globals are reachable and mutable |
| c20_realpath_spoof_posixpath | `posixpath.realpath = lambda *a,**k: "/usr/lib/python3.14/x"`; `open(REF)`; restore | `_hook` calls `os.path.realpath` (same object as `posixpath.realpath`) at event time; the missed event is `open <REF>` because the spoofed resolution is a stdlib path |
| c21_realpath_spoof_os_path | same with `os.path.realpath` | same |
| c11_posixsubprocess_cat | `_posixsubprocess.fork_exec((b"/usr/bin/cat", REF), …)`; pipe output into the candidate | `_posixsubprocess` is stdlib, so the import passes; `fork_exec` raises no event in `_DENY` (`subprocess.Popen` is denied but not raised); the child is `/usr/bin/cat`, outside Python and outside the hook; the open of REF happens in the child, never audited |

Caught on the committed gate (sandbox=violation, exit 97; event as printed by the hook):

- `open <REF>` on the reference path itself: c01 (SourceFileLoader.get_data), c02 (io.open_code), c04 (`/proc/self/root` + REF), c06 (pathlib.read_bytes), c07 (zipimporter + open), c08 (posix.open), c10 (linecache), c12 (`_io.FileIO`), c15 (`importlib.util.spec_from_file_location().loader.get_data`), c17 (`pathlib.open`).
- `open /home/…/round-89/__pycache__/c89_key.cpython-314.pyc`: c19 (`spec.loader.exec_module`), the `.pyc` path is the first unapproved open.
- `open /usr/lib/python3.14`: c03 (`os.open` of the stdlib root itself, then `dir_fd` relative read). The root check requires a trailing separator, so the stdlib directory is refused. This is a false refusal, not a catch of an escape; the relative `dir_fd` read did not reach REF in any case (see analysis below).
- `ctypes.dlopen`: c09 (`ctypes.CDLL(None).fopen`), c16 (`ctypes.pythonapi` + os.open).

Positive control on the committed gate: `positive-L1-r89-committed.txt`: `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok met=true` (conforming, not an escape).

## Results on the working-tree snapshot 33650406 (`receipts/worktree-at-run/`)

All 20 candidates, including the escapes, are refused with `SANDBOX_VIOLATION marshal.loads` (hand=0/85). The conforming L1 positive (`positive-L1-r89-worktree.txt`) is also refused: `clauses=0/6 hand=0/85 generated=0/120 sandbox=violation met=false`; so is the base `scripts/cache_key.py` positive (`receipts/pos_base_cache_key.py`, run under the same snapshot, output not receipted separately). I checked 2 of the 4 positives; the other two were not run. Cause: the hardened `_DENY` includes `"marshal.load"`, and the deny test is `event.startswith(deny_events)`, so it matches `marshal.loads`, which every stdlib import of cached bytecode raises (json, re, …). So the working tree over-refuses every conforming candidate I tried, and its 20/20 refusals are not evidence that escapes are caught. Blocking event for L1: `marshal.loads`, not any escape route.

## Analysis (routes I expected to work but that were caught or are structurally blocked)

- `dir_fd`: `os.open(rel, dir_fd=D)` where D is a stdlib directory. The hook resolves `rel` against the process cwd (`work/cwd`), not against D, so the two resolutions differ only through a base mismatch; I found no relative path whose cwd-resolution lands in roots while its D-resolution lands on REF without a symlink into the stdlib root. Not exercised beyond c03.
- `zipimport`, `marshal`, `mmap`, `codecs`: all require a file open that is audited.
- `ctypes`: `ctypes.dlopen` / `ctypes.dlsym` are audited and in `_DENY`.
- `sys.modules` injection: needs source bytes from somewhere; no escape without another route. Not tested as a standalone candidate (the seat says at least 10 candidates; 20 were written).
- Preloaded modules (`posix`, `_io`, `codecs`, `linecache`, `marshal`, `zipimport`, `_frozen_importlib_external`) skip the `import` event. I checked the list with `python3 -I -S`; none of them gives an unaudited open or spawn on the committed gate.

## Defects in the committed gate (for L1)

1. The hook's state lives in module globals (`_roots`, `_die`, `_hook`, `_DENY`, `_cand`) and is reachable through `sys._getframe` and `gc.get_objects`; both are unlisted. Any in-process rewrite of those globals removes the sandbox (c05, c13, c18).
2. `os.path.realpath` is looked up at event time, so a candidate that replaces it switches the sandbox's open-decision (c20, c21).
3. `_posixsubprocess.fork_exec` is not denied and does not raise a denied event; `subprocess.Popen` is denied but the lower layer is not (c11). Denying `_posixsubprocess` by import would be the minimal fix; the working tree attempts that but the marshal regression above blocks any evaluation.
4. Hook `open` event only; the spawned child reads the file outside the audit (c11) — any spawn denial must be at spawn, not at open.
5. The roots test omits the stdlib directory itself (no trailing separator), so `open /usr/lib/python3.14` is refused (c03). Cosmetic, but it is a false refusal in the sandbox's own contract.

## Limits

- Scope is the sandbox; I did not re-score the gate's hand/generated populations, the advisory cases, or the RFC gap rows.
- The working tree was edited by L1 during this seat; I pinned a copy at one instant (sha `33650406…`). The committed-gate result is stable across both sweeps I ran.
- Escape keys were judged by the gate's own reference, not by an independent reference; the reference itself is the round-89 file and the gate's reference is the same contract.
- Candidates c01–c21 excluding c14 were run with seed 4242 only. Other seeds not tried.
- Did not test `subprocess.Popen` directly (it is denied by name) nor `os.posix_spawn` (denied by name).
- No install, no package change, no pacman, no network, no git mutation (read-only `git show`/`git status` only), no fixture clone was created.

## Tooling

None installed or upgraded. Python 3.14.8 (`/usr/bin/python3`) and `/usr/bin/cat` were the only binaries used.
