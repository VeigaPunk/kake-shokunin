# W2 ReviewScratchDefaultDiff — per-run default scratch in the citing-set runner (e490381)

Scope: `git diff b1752a2480aa e4903817669a -- scripts/citing_set_selftest.py` (50+/18-).
Attacked: _run/main split (lost behaviour: unknown args, cannot_evaluate sites, exit
codes), rmtree safety, SKILL.md scratch claim. Clone of lane at 0a0acfb1, sandbox
/fast/scratch/hyaku/kake-r33/w2/ReviewScratchDefaultDiff/ (TMPDIR=…/tmp). All commands
run there with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset. No tool installs. No lsp
device is exposed to this seat, so caller checks used literal grep (recorded per role).

## Verdict

No blocking defect found. The split preserves every pre-existing cannot_evaluate site,
the unknown-args note, and all three exit codes. The default scratch is a 0700 mkdtemp
dir under DEFAULT_TMPDIR, removed in a `finally`, and `args.tmpdir` is assigned exactly
once and only read afterwards — rmtree cannot target anything else. Two minor findings.

## Checks run (command → exit, observed)

All runner invocations: `python3 -B <clone>/scripts/citing_set_selftest.py --root <clone> [args]`.

1. Default-scratch lifecycle. Ran with no --tmpdir in background; listed
   /fast/scratch/hyaku/kake-r27 during and after. before=0, during=1 (exactly
   `citing-set-selftest-i939icqw`), after=0, rc=0, verdict clean, cases=45,
   failedCases=0. The pre-existing old-style shared litter
   /fast/scratch/hyaku/kake-r27/citing-set-selftest (mtime Oct 22 09:21, i.e. pre-fix
   runs) was untouched — rmtree is scoped to the private dir only. Receipts runA.json,
   runA.err.
2. Concurrency (the routed defect). Two default runs in parallel: rc=0,0; both
   top-level verdict clean, failedCases 0,0; 0 leftover `citing-set-selftest-*` dirs
   after. (runA2a/b.json. During a later step, 2 foreign prefix dirs appeared —
   live peers sharing the parent; not mine, not touched.)
3. Explicit --tmpdir stays caller-owned. `--tmpdir $D/tmp/explicit-dir` → rc=0,
   verdict clean, dir still exists after the run. runB.json.
4. scratch_error path (new). Mutant copy with DEFAULT_TMPDIR=/proc/1/kake-mutant-nope
   (sed on a sandbox copy) → rc=2, JSON failure reason "cannot create private scratch
   directory under /proc/1/kake-mutant-nope: [Errno 2] …" (runC.json). This exit-2
   path is new; at base a missing parent was silently created later by
   cases_root.mkdir(parents=True) — no behaviour lost, strictly better diagnostics.
5. Unknown args preserved. `--bogus-flag` → rc=0, note "ignored unknown arguments:
   --bogus-flag" (runD.json; _run appends it at runner_e4903817.py:719-720).
6. Exit-code table through _run. 0=clean (checks 1-3), 1=failed case
   (symlinked case dir → "symlinked case directory refused", rc=1, runSL.json),
   2=could-not-evaluate (checks 4,7-9). EXIT_OK/FAILED/CANNOT_EVALUATE constants
   unchanged (lines 147-149).
7. Stray fixture-root entries (new refusal). fixtures copy + file `stray.txt` → rc=2
   "fixture directory contains non-directory entries: stray.txt" (runE.json); broken
   symlink `broken-link` → rc=2 same shape (runS.json). Matches SKILL.md:961-962
   "reported, not raised or skipped". Committed fixtures root at e4903817 is
   45 trees, no non-dir entries (git ls-tree), so the default run is unaffected.
8. Dotted-dir exclusion preserved. fixtures copy + `.hidden-case` dir → rc=0,
   cases=45 (runH.json) — old skip behaviour kept for directories.
9. read_expected hardening. Case with expected.json a dangling symlink → rc=1,
   reason "expected.json unreadable (symlinks are refused): [Errno 40] Too many
   levels of symbolic links …" (runEL2.json); expected.json a FIFO → rc=1,
   "expected.json must be a regular file", no hang — fstat runs before read
   (runF2.json). At base an fstat OSError would have escaped read_expected and
   crashed the whole selftest with a traceback; now it is a per-case reason.

## Findings

- MINOR (dead code): run_case's `except OSError` branch (scripts/citing_set_selftest.py:581-585,
  e4903817 blob) is unreachable. Post-change read_expected wraps every OSError
  (os.open at 439-451, fstat/fdopen/read inside the same try) into ValueError and
  raises only ValueError (434-457); the try at 581 wraps only read_expected. Runtime
  confirmation: the ELOOP case carries the "(symlinks are refused)" note that only the
  ValueError wrapper adds (583-585 would omit it). Harmless, but it suggests a path
  that cannot happen and would mask the note if ever reached.
- MINOR (asymmetry, intended-tightening consequence): the new non-directory refusal
  (739-744) does not exempt dotted files, while dotted directories are still silently
  excluded from cases (745-748; runH.json). A stray committed file such as
  `.gitignore` in scripts/fixtures/citing-set/ would flip the whole selftest to
  exit 2 where a stray dotted directory would not. None committed today; consistency
  wart only, consistent with the documented "report, not skip" contract.

## rmtree safety (acceptance item)

- `main` (812-824): mkdir/mkdtemp failure → cannot_evaluate, no finally; success →
  `args.tmpdir = tempfile.mkdtemp(prefix="citing-set-selftest-", dir=DEFAULT_TMPDIR)`
  (mode 0700), then try/finally `shutil.rmtree(args.tmpdir, ignore_errors=True)`.
- `_run` only reads args.tmpdir (752-753); grep shows no reassignment anywhere.
- shutil.rmtree refuses a symlinked top-level path (raises; swallowed by
  ignore_errors=True rather than followed), so a swapped-in symlink is not traversed.
- prepare_case's `shutil.rmtree(work_dir)` (548) targets cases_root/<case> inside the
  same private scratch and is byte-identical at base — pre-existing, not touched by
  this commit.
- Residual: between mkdtemp and finally, a same-user process could rename another
  directory onto that exact path and rmtree would delete the replacement. Parent is
  vgpnk-owned 0755 on a single-user host; modelling that adversarially is the held
  item KakeR31.CriticSandboxThreatModel, so I stop this line here per bounds.

## SKILL.md claim

SKILL.md:955-960 (0a0acfb1): "Without `--tmpdir` the runner now uses a private
directory under `/fast/scratch/hyaku/kake-r27` and removes it … The selftest scratch
still lives below that root." Verified true by observation (check 1: private dir
created under that root, removed after; check 2: concurrent runs isolated). Also
consistent with SKILL.md:616 "selftest scratch below /fast/scratch/hyaku/kake-r27".
Explicit --tmpdir remains caller-owned and unremoved (check 3), as the docstring
(90-96) and hostile selftest doc state; the hostile selftest always passes an explicit
--tmpdir (scripts/citing_set_hostile_selftest.py:242 required=True, :203-206), so it
never exercises the new default.

## Not verified / residual risk

- Did not run the frozen counter c1_code_probe.py or c1_strict_supplement.py against
  e4903817 (other seats own those); the runner variants they build inherit this
  default only when they omit --tmpdir — not checked.
- Did not verify the 3-of-4-at-base / 0-of-4-after concurrency receipt numbers
  (.ufo/waves/round-33/verification/concurrency-*.txt); I independently reproduced
  2/2 clean concurrent runs at the new rev but ran no base-rev concurrency control.
- SIGKILL during a default run would leak the private dir (no cleanup possible); the
  `finally` covers exceptions and SIGINT only. Pre-existing pattern, not worsened.

Evidence files: /fast/scratch/hyaku/kake-r33/w2/ReviewScratchDefaultDiff/
{runA,runA2a,runA2b,runB,runC,runD,runE,runH,runS,runSL,runEL2,runF2}.json,
runner_e4903817.py, runner_b1752a2.py, mutant_runner.py, tmp/ fixture variants.
