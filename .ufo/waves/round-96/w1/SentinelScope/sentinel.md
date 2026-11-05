# SentinelScope — round-96 wave-1 confinement & sandbox report (2026-11-05T15:45:38-03:00)

Seat: SentinelScope (leaf, no subagents). Scope: confinement/sandbox attacks on the FROZEN round-96
instruments `.ufo/waves/round-96/c96_selfassess.py` (C1 counter) and `.ufo/waves/round-96/c96_reval.py`
(C2 counter + subject sandbox). The instruments were never modified; digests re-verified after all runs (r01).

## Verdict

`SENTINEL refused=28 escaped=F1,F2,F3,F4`

- refused=28: 5 C1 module-shadow/docstring probes, 14 sandbox
  open/chdir/fd/runpy/process probes (r09), 5 denied imports (r09/r10), 1
  PYTHONPATH-under--I probe (r15), 3 hostile candidates through exact counter mechanics (r10-r13).
- F1 (HIGH, instrument defect): `c96_reval.py` crashes with `NameError: name 'mutants' is not defined` on
  EVERY candidate-present scoring run — the only path C2's claim needs. Receipt r08.
- F2 (LOW, env-boundary): the C1 counter resolves `git` from PATH; a PATH-shadowed wrapper was executed (r06).
- F3 (INFO): sandbox-unaudited vectors — `os.kill(os.getppid(), 0)` succeeds (scorer-kill DoS class, no verdict
  influence), outside metadata (`os.listdir`/`os.stat`) succeeds (names/sizes only), sibling files inside the
  subject tree are readable by design. Rows in r09.
- F4 (CONFIRMATION of routed R95-7, C2 side): no effectful-shadow defense — a candidate that writes a marker
  file (inside its ephemeral tree) while answering every case correctly runs cleanly and produces correct
  decisions (r10 effect-in, r16); nothing marks or refuses it. Counter-level "admission" is formally undecidable
  this round because F1 crashes the counter before any verdict line.

## Findings detail

### F1 — c96_reval.py candidate-present path crashes (HIGH; route to round 97, never patch)
- Exploit path: land any `scripts/reval_exchange.py` at the measured revision, run the frozen counting command
  `python3 -B .ufo/waves/round-96/c96_reval.py --root . --revision <REV> --work <scratch>` -> after candidate,
  positive-control and forgery scoring (~16s), the `mutant_cases` call at frozen line 624 evaluates the name
  `mutants`, which main() never binds (it computes `n_mut` at line 561 and discards the population list; only
  `selftest()` binds it, line 511). Process dies rc=1 with an empty stdout — no `C2v96 ...` verdict line.
- Evidence: r08 (five variants incl. the frozen positive control as candidate, each rc=1 NameError); digests
  verified before and after (r01). An earlier rc=2 `population=drift` was MY fixture missing the pinned
  contract — corrected, documented in r08.
- Impact: C2's predicate (`candidate=present ... met=true`) is unreachable through the frozen bytes; the wave's
  ExecReval integration will crash the counter identically. No false-green is possible (the failure is loud),
  but the claim cannot be scored this round by the frozen instrument.
- Smallest remediation (for round 97's successor counter, not this round): bind `mutants = load_mutants(...)`
  in main() the way selftest() does. Recorded as a routed defect only.

### F2 — C1 counter executes PATH-resolved `git` (LOW; env-boundary observation)
- Exploit path: run the frozen command with PATH prefixed by an attacker directory containing a `git` wrapper ->
  the counter's evidence source (`git show`/`cat-file`/`ls-tree` results) is fully attacker-mediated (PATHMARKER
  written by the wrapper during the run; verdict line unchanged because the wrapper delegated to real git — a
  lying wrapper could fabricate any audit result).
- Evidence: r06 (rc=0 clean verdict with the shadow invoked).
- Impact bound: requires control of the counting process's environment — the same control already lets the
  attacker shadow `python3` itself, so this widens nothing at that threat level; it IS reachable, however, from
  any wrapper/CI layer that exports PATH. The instruments defend module shadows but not executable resolution.
- Smallest remediation: invoke git by absolute path or assert its origin in the successor counter.

### F3 — sandbox-unaudited vectors (INFO; no content escape, no verdict influence)
- `os.kill(os.getppid(), sig)` is unaudited: a subject can signal its parent (the counter) — denial-of-scoring
  only; it cannot fabricate met=true or read anything (r09 kill-ppid-sig0 ran).
- `os.listdir`/`os.stat` outside the tree succeed: name/size metadata disclosure only (r09).
- Under-root sibling opens are granted by the sandbox's design (the frozen hook returns early for any realpath
  under the subject's own directory — verbatim in the instrument's SANDBOX source; self-read observed allowed).
  In v3 the `read-sibling-in-root` row was REFUSED, but only because an earlier unaudited `os.chdir` (a chdir
  test whose read failed before its restore ran) left the subject's cwd outside the tree, so the relative path
  resolved to `vault/probe5.py` — realpath still refused it. Recorded consequence: `os.chdir` is unaudited and
  persists for the subject's lifetime; it enables no content escape (every subsequent open is still
  realpath-checked) but is one more subject-controlled, unhooked lever (r09).
- Smallest remediation: add os.kill/os.listdir/os.scandir/os.stat to the sandbox deny list in the successor.

### F4 — no C2 effectful-shadow defense (CONFIRMS the R95-7 item that routes forward)
- r10/r16: candidate writes `effect-marker.txt` (inside its ephemeral tree, via its own `__file__`) while
  answering construct/304/refusal cases exactly like the positive control — sandbox rc=0, correct decisions,
  marker written, nothing flagged. Outside-tree effects ARE refused (r12: PermissionError naming the outside
  path; marker absent), so the blast radius is the scoring tree alone. C1's shadow check (F1/R94-2 analog) has
  no C2 counterpart; freeze.md routes this forward and this round confirms it live.

## What the frozen instruments refuse (command + observed rc in the named receipt)

| Probe | Result |
|---|---|
| a1 PYTHONPATH `subprocess.py` shadow, counter run from a non-script cwd | REFUSED — marker absent, rc=0 verdict=clean (r03) |
| a2 cwd `subprocess.py` shadow | REFUSED — marker absent, rc=0 verdict=clean (r04) |
| a3 effectful `subprocess.py` beside a counter COPY in scratch | REFUSED — marker absent, rc=0 verdict=clean, self-reported digest identical (r05) |
| a4 startup `os.py` PYTHONPATH shadow (interpreter-level control) | REFUSED — stdlib os loads; the scrub's own `_os` is not attacker-reachable (r06 control B) |
| a5 docstring-vs-command | CLEAN — frozen command `python3 -B` (no -I/-E in executable code); docstring claims no isolation flag (r18) |
| sandbox: symlink inside tree -> outside file | REFUSED — PermissionError realpath message (r09, r13) |
| sandbox: absolute open outside tree | REFUSED (r09) |
| sandbox: chdir outside then relative open | REFUSED (r09) |
| sandbox: chdir out and back, then open | containment holds (r09) |
| sandbox: os.open fd on outside path | REFUSED (r09) |
| sandbox: io.open_code outside | REFUSED (r09) |
| sandbox: runpy.run_path outside file | REFUSED (r09) |
| sandbox: import subprocess/ctypes/socket/tempfile/multiprocessing | REFUSED — import allowlist (r09 + v2 receipt rows inside r10-r14 runs) |
| sandbox: os.execv / os.fork / os.posix_spawn / os.system / os.spawnv | REFUSED — process-creation denials (r09; spawnv denied via the os.fork audit event) |
| sandbox: PYTHONPATH shadow of an allowed module under -I | REFUSED — stdlib loads, marker absent; WITHOUT -I the same shadow executes rc=7, so -I is load-bearing (r15) |
| sandbox: open of `../sandbox.py` (counter's work dir, outside tree) | REFUSED (r09) |
| sandbox: sibling read after a subject-controlled chdir left cwd outside | REFUSED — relative path resolved against the outside cwd and was denied (r09; also evidence `os.chdir` is unaudited and persists) |
| candidate: writes marker OUTSIDE the tree, then answers | REFUSED — subject dies rc=1 on every case, marker absent (r12) |
| candidate: symlink-then-open outside | REFUSED — rc=1, PermissionError (r13) |
| candidate: os.execv | REFUSED — rc=1, "process creation denied: os.exec" (r14) |

## Base-control reproduction (read-only; committed receipts never re-stamped)

- c96_selfassess full frozen-form run on the lane at base `bde98691…`: line1 byte-identical to
  `controls/c1-successor-at-base.txt` (counter=a282da65…, battery=23/23, admit=5/5, shadow=absent,
  predecessor_admits=6/22, ng_pred_admits=3/3, met=true), rc=0 (r02; diff check in r18).
- c96_reval frozen-form run on the lane at base: line1 byte-identical to `controls/base-c2.txt`
  (candidate=absent … met=false), rc=1 (r07). This run also demonstrates the crash-free absent-candidate path.

## Zero-mutation / resume_continuity_v1

`resume_continuity_v1` has no surface in this round's instruments, contract or freeze (zero occurrences — r18);
per the round-61 sentinel precedent the duty substitutes to: every scoring run leaves the lane tree untouched.
Verified: `git status --porcelain` byte-identical before/after the bracketed run set (C1 full battery, C2 base,
4 attack runs); HEAD constant `049e8eca…` (r17). No sysctls touched; no tools installed; no mutating git/jj
anywhere — the only mutated repo is this seat's scratch fixture (toplevel asserted before first commit).

## Honesty ledger

- Invalid intermediate probes superseded by final receipts (documented so nothing silent is relied on): a first
  sandbox matrix opened "outside" files that were actually inside the subject root (my layout error — the
  sandbox root is the subject's own directory); a rerun hit a stale in-tree symlink and a NameError'd probe
  body; the first C2 fixture lacked the pinned contract file. Final receipts (r09, r13, r08) come from fresh,
  verified layouts.
- All five C2 counter runs crashed (F1) before emitting a verdict; no C2 candidate verdict is claimed anywhere.
  The "refused" rows for hostile candidates are scored at the sandbox layer (exact counter mechanics replicated:
  same extracted sandbox bytes sha256 f4374ac4…, same -I -B spawn, same env/cwd shape), not at the
  counter-verdict layer.
- Unrun checks: none owed by this seat's spec. Not attempted (out of scope): predecessor differential runs,
  timing/TOCTOU races on the audit hook, kernel-level escapes.

## Receipts (this directory, flat)

r01 digests+provenance; r02 C1 full lane base; r03 a1; r04 a2; r05 a3; r06 a5+interpreter controls; r07 C2 lane
base; r08 F1 crash; r09 sandbox matrix v3; r10-r14 hostile-candidate mechanics (pos / effect-in / effect-out /
execv / symlink); r15 PYTHONPATH-under--I; r16 effectful standalone; r17 lane zero-mutation; r18 static citations.

Report copy filed at `.ufo/waves/round-96/w1/SentinelScope.md` (the Report path named by the seat spec).
Scratch tree /fast/scratch/hyaku/kake-r96/SentinelScope/ deleted before yield (receipts copied out first).
