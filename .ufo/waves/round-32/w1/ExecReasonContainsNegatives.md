# Round 32 wave 1 — ExecReasonContainsNegatives

Seat: `KakeR32.ExecReasonContainsNegatives` (executor, operability axis).
Target: C1 input validation — malformed `reason_contains` specs are refused.
Base under test: `285abcad632e3c1c57bb402232e7d218054db383` (lane tip).

## What I built (sandbox only, no lane file written except this report)

Sandbox root: `/fast/scratch/hyaku/kake-r32/w1/ExecReasonContainsNegatives/`
- `clone/` — clone of the lane at `285abcad`, `git checkout -q 285abcad…`
- `run_variants.sh` — per-variant harness (one spec tree per variant)
- `tree-*/` — isolated trees; `out-*.json`, `err-*.txt` — captured output

Sandbox spec variants written under
`clone/scripts/fixtures/citing-set-hostile/<variant>/hostile.json`
(sha256 of each):
- `V1-reason-number` `701cecb0…382c6` — `"reason_contains": 123`
- `V2-reason-empty` `faf57155…bcbb` — `"reason_contains": ""`
- `V3-reason-null` `38413e9e…1f41c` — `"reason_contains": null`
- `V4-reason-list` `784e7307…9834` — `"reason_contains": ["needs an earlier 'git_init'"]`
- `V5-reason-never-reported` `aa681260…1ab1` — `"reason_contains": "this text is never reported by the runner"`
- `V6-reason-whitespace` `bf2233a0…8051` — `"reason_contains": "   "` (extra, not required)
- `V7-reason-bool` (built in `tree-V7/`) — `"reason_contains": true` (extra, not required)

Each variant reuses the P6 shape (setup `git_commit` then `git_init`,
`tmpdir_in_victim: true`) so the runner still reaches the load-time guard; only the
`reason_contains` value changes.

## Commands and exit codes

Command per variant (run from the sandbox root, `TMPDIR=$SB/tmp`):
`python3 -B clone/scripts/citing_set_hostile_selftest.py --root tree-<V> --tmpdir tmp/<V>`

| run | exit | observed |
|---|---|---|
| baseline (committed P1–P6 only, pristine `scripts/` from `git archive 285abcad`) | **0** | `passed: true`, all 6 cases pass, `reasonChecks {"h6": true}` |
| V1 number | **2** | `error: …/V1-reason-number/hostile.json: reason_contains must be a non-empty string`, `cases: []` |
| V2 empty string | **2** | same message, `cases: []` |
| V3 null | **2** | same message, `cases: []` |
| V4 list | **2** | same message, `cases: []` |
| V5 never-reported text | **1** | case runs; `reasonChecks {"hvn5": false}`; `passed: false` |
| V6 whitespace-only | **1** | case runs; `reasonChecks {"hvn6": false}`; `passed: false` |
| V7 boolean `true` | **2** | same message |

Raw V5 stdout (the never-reported-text case, exit 1):
```
{"schema": "kake-citing-set-hostile-v1", "passed": false, "cases": [
 {"case": "V5-reason-never-reported", "passed": false, "detail": {
   "gap": "w1-negative-never-reported", "hostile": ["hvn5"], "exit": 1, "timedOut": false,
   "reasons": {"hvn5": "case.json setup op 'git_commit' needs an earlier 'git_init'"},
   "canary": false, "victimUnchanged": true, "reasonChecks": {"hvn5": false}}}],
 "error": null}
```
Raw V1 stdout (malformed, exit 2):
```
{"schema": "kake-citing-set-hostile-v1", "passed": false, "cases": [],
 "error": "…/V1-reason-number/hostile.json: reason_contains must be a non-empty string"}
```
All runs wrote 0 bytes to stderr; no tracebacks in the unmutated tree.

Acceptance: malformed (number, empty, null, list) → exit 2 each; never-reported text →
exit 1 with the spec failing. Met.

## Evidence pointers

- Guard under test: `scripts/citing_set_hostile_selftest.py:142-144`
  (`if "reason_contains" in case and (not isinstance(case["reason_contains"], str) or not case["reason_contains"]): raise ValueError(...)`)
- Load path that turns the ValueError into exit 2: `scripts/citing_set_hostile_selftest.py:249-253`
- Reason-text check that turns a wrong claim into a failing spec:
  `scripts/citing_set_hostile_selftest.py:216` (`reasonChecks`), `:218` (`wanted`)
- Runner reason actually reported for the P6 shape: `scripts/citing_set_selftest.py:363`
  (`"case.json setup op 'git_commit' needs an earlier 'git_init'"`)
- Harness: `/fast/scratch/hyaku/kake-r32/w1/ExecReasonContainsNegatives/run_variants.sh`
- Captured outputs: `/fast/scratch/hyaku/kake-r32/w1/ExecReasonContainsNegatives/out-*.json`

## Additional checks run (beyond the assignment)

1. Benign suite still clean with the sandbox variant dirs present:
   `python3 -B clone/scripts/citing_set_selftest.py --root clone --fixtures clone/scripts/fixtures/citing-set --tmpdir tmp/benign`
   → exit **0**, `verdict clean cases 45 failed 0 failedCases 0`.
2. Mutation: deleted the two-line `reason_contains` validation in a sandbox copy
   (`tree-mut/scripts/citing_set_hostile_selftest.py`) and ran the V4 list spec.
   Result: **exit 1 with an uncaught `TypeError: 'in <string>' requires string as left operand, not list`**
   at `citing_set_hostile_selftest.py:216`. So the validation is load-bearing: without it the
   run does not exit 2 but crashes into the same exit code as a genuine spec failure.
   The mutant was not committed anywhere; it lives only in `tree-mut/`.
3. Suite-level blast radius of one malformed spec (tree = committed P1–P6 + V1):
   **exit 2, `cases: []`** — the malformed spec aborts the whole load, so no committed spec
   is evaluated and no per-spec result is emitted. Committed P1–P6 + V5 instead gives
   **exit 1** with P1–P6 all `passed: true` and only V5 false.

## Advisory findings (no code changed)

- **F1 (operability, minor):** spec loading is all-or-nothing. One malformed spec makes the
  hostile selftest exit 2 with an empty `cases` array, so a contributor who typos one new
  spec loses all six committed specs' results in that run and must bisect by hand. Acceptable
  today (fail loudly, never silently pass) and the exit-2 contract is what C1 claims, but a
  per-spec error list would make triage cheaper. Not fixed by me: the lane owns the file.
- **F2 (operability, minor):** whitespace-only `reason_contains` (`"   "`) passes the
  load-time validation (it is a non-empty string) and then fails as a *spec* failure
  (exit 1) rather than as bad input (exit 2). Behaviour is fail-loud, not unsafe; the
  validator only rejects empty strings, not blank ones.
- **F3 (operability, informational):** without the validation the malformed list crashes the
  process with a traceback instead of exiting 2, so exit code 1 alone does not distinguish
  "spec failed" from "selftest crashed". Any counter that keys on exit 1 for
  `citing_set_hostile_selftest.py` should also assert stderr is empty.

## What I did not verify

- The lane's own counters `python3 -B .ufo/waves/round-32/c1_m3_probe.py --rev <rev>` were
  not run; my scope was the spec-level input validation, not the m3 mutant kill claim.
- No build, lint or test command of the lane was run (parent owns the post-integration gate).
- I did not exercise the `reason_contains` path against a runner other than
  `scripts/citing_set_selftest.py` at `285abcad`.
- No network access was made; no operator-owned host was contacted.

Tooling: no packages installed, no versions changed (Python 3.14.8 and the system `git`
were already present and were the only tools used).
