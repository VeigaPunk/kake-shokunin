# ReviewRunnerCodeDiff — correctness review of the structured-code change

Scope: `git diff 5777d5af..0a0acfb -- scripts/citing_set_selftest.py` (CaseRefusal,
SetupRefusal, prepare_case, run_case, failure entries, docstring, tmpdir split).
Evidence: own clone `/fast/scratch/hyaku/kake-r33/w2/ReviewRunnerCodeDiff/clone`
at 0a0acfb1 (runner sha256 88b47f6b…, matches `git show HEAD:` byte-identical).
Axis: operability.

## Findings by severity

**No defect introduced by the diff.** Every refusal path still returns a `reason`,
every result row and per-case `failures[]` entry carries a `code` key, the coded
paths match the docstring exactly, and both new exception types are contained.

- `CaseRefusal(ValueError)` / `SetupRefusal(RuntimeError)` subclass the existing
  types, so both are caught by the pre-existing `except ValueError` /
  `except (OSError, RuntimeError)` blocks — no exception type change lets an
  error escape. Verified: `issubclass` probes printed True/True.
- P6 end-to-end: synthetic fixtures dir via `main()` produced
  `{"case":"zz-p6","reason":"case.json setup op 'git_commit' needs an earlier
  'git_init'","code":"setup_commit_before_init"}` in `failures[]`, exit 1.
- `setup_commit_without_repo`: `SetupRefusal` raised by `apply_setup` (line 529)
  propagates through `prepare_case`'s wrap (line 556, `getattr(exc,"code",
  "setup_failed")`). Unreachable via fixtures by construction (load-time check +
  fixture `.git` ban); verified only by direct call — defense in depth, matches
  docstring. `setup_failed` demonstrated with a double-`git_init` case.
- Null codes confirmed: unknown op, `.git` path refusal, FIFO expected.json,
  fixture `.git`, finding mismatch — all `code: null`, matching "Other refusals
  report `code` null".
- Docstring literal check: load-time guard is two lines (if + raise, lines
  401–402) carrying `"setup_commit_before_init"` and `"needs an earlier
  'git_init'"`; docstring names all three codes correctly (lines 124–128).
- tmpdir split: `mkdtemp` private dir removed after run (`leaked private dirs:
  []`), `scratch_error` → exit 2 with proper summary, `--tmpdir` path unchanged.

**Low — docstring/schema asymmetry (observation).** Docstring says "each … case
failure entry carries `reason` … and `code`" but run-level failure entries
(`cannot_evaluate`, `--min-cases`, lines 723, 796) have no `code` key at all:
`{"case": null, "reason": "fixture directory not found: /nonexistent-dir"}`
(observed). A consumer doing `f["code"]` over `failures[]` hits KeyError on
run-level failures. Ambiguous wording, not the C1 contract; flag for the L1.

## Residual risk (pre-existing, NOT introduced by this diff)

Reproduced identically at 5777d5af: a NUL byte in `case.json` `git_commit`
`"message"` → `subprocess.run` raises `ValueError("embedded null byte")`,
outside `prepare_case`'s `(OSError, RuntimeError)` catch → escapes `run_case`
and crashes the whole run (no JSON summary). Same for a NUL in an `argv` value
token (run_case line 629 catch covers only `TimeoutExpired`/`OSError`). Commands
above; output `ESCAPED: ValueError embedded null byte` at both revs. One
malformed fixture case still kills the runner instead of becoming a failed case.

Dead branch (harmless): `run_case` `except OSError` (line 583) is unreachable —
`read_expected` now converts every OSError to ValueError inside its outer try.

## Checks run

- `python3 -B scripts/citing_set_selftest.py --tmpdir <sandbox>` → exit 0,
  verdict clean, 45 cases, 0 failures, `code` present in all 45 rows.
- `python3 -B .ufo/waves/round-33/c1_code_probe.py --rev 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` → exit 0, met 4/4, guard_ok true, m3+recoded killed on P6.
- `--fixtures /nonexistent-dir` → exit 2, could-not-evaluate, entry lacks `code`.
- In-process probes per refusal path (all exits 0 except intentional escapes).

## Not verified / gaps

- Gate-delegated `--selftest` recursion depth; per-case timeout interplay with
  blocking FIFO `git add` (docstring acknowledges this).
- Lane HEAD moved to d2ed431a during review; its runner delta vs 0a0acfb1 is
  docstring-only (documents the stray-entry exit-2 behavior) — consistent with
  the code reviewed here.
- No tools installed; no network use; lane tree read only for the diff and this
  report write.

Report: .ufo/waves/round-33/w2/ReviewRunnerCodeDiff.md
