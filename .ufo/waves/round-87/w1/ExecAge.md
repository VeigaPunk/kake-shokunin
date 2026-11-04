# ExecAge — round 87 single v1

## Axes and scope

Calibration (2 HOLD) and freshness (10 HOLD), unchanged scores. This seat implements only the independent offline C2 candidate; no C1 artifact, production file, frozen oracle/predicate, global configuration, source repository, or external state was changed. No admission or blanket no-harm claim.

## Files delivered

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/cache_current_age.py`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/receipts.json`
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge.md`

Candidate SHA256: `d1b09ae17a54728a3b967cdc7436f19b62fc98e4304aab64324ee8969454331a`.
Frozen cases SHA256: `cea987d4ce15d53f0f80f59c28b14d2978edde1f0f768daf8aadf900defad25e`.
Candidate was not amended after scoring.

## Behavior

Stdlib-only stdin JSON reader, six exact integer output keys. Required integer-not-bool date_value/request_time/response_time/now; optional age_value defaults to zero. Negative Date is supported; other fields must be nonnegative and request_time <= response_time <= now. Unknown keys rejected. Sequential apparent_age, response_delay, corrected_age_value, conservative corrected_initial_age, resident_time and current_age arithmetic; no imported frozen cases, canned answers, saturation, or float arithmetic. Python decimal conversion limit is disabled in the CLI to preserve arbitrary-precision input/output.

Invalid input returns exit 1, empty stdout and stderr prefixed `invalid_input:`. Malformed JSON, wrong top-level shape, missing/invalid fields, ordering errors and unsupported options are covered. Valid input returns only its JSON object and newline, exit 0, empty stderr.

`--selftest` launches the real script in subprocesses in a TemporaryDirectory, uses the caller's isolated TMPDIR, asserts complete valid outputs and exact integer result types, and compares exit plus the stable `invalid_input` diagnostic identifier for every invalid fixture. It tests both max branches, Date clamping, negative Date, missing Age, equal times, 5001-digit arithmetic, every required missing field, boolean/noninteger fields, all nonnegative constraints, both ordering constraints and invalid CLI/JSON forms.

## Exact retained execution evidence

Execution used Python 3.14.8 (`/usr/bin/python`), no installations. Both authorized bounded checks ran concurrently via two stdlib ThreadPoolExecutor workers, not services or background jobs. Each child used cwd and TMPDIR `/fast/scratch/hyaku/kake-r87/ExecAge`, with PYTHONDONTWRITEBYTECODE=1.

1. Command: `/usr/bin/python -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/cache_current_age.py --selftest`
   - Exit: 0.
   - Stdout: `selftest: 61 isolated CLI fixtures passed` followed by newline.
   - Stderr: empty.
2. Command repeated for each frozen case: `/usr/bin/python -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/cache_current_age.py`
   - Input: `json.dumps(case['input'])` from unchanged `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/age-cases.json`.
   - Comparison copied the frozen count.py rule: matching exit, plus complete decoded JSON equality for exit-0 cases; diagnostic checks recorded separately.
   - Result: 17/17, all 12 complete valid outputs matched, all five invalid exits 1 and `invalid_input` prefixes matched. Driver aggregate exit field: 0 (computed result, not an additional process invocation).
   - Receipts retain every exact argv, stdin, actual exit, stdout and stderr, plus candidate/oracle digests and interpreter version.
3. Setup: `mkdir -p /fast/scratch/hyaku/kake-r87/ExecAge /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge` — exit 0.
4. After receipts persisted: `rmdir /fast/scratch/hyaku/kake-r87/ExecAge` — exit 0. Selftest TemporaryDirectory removed its contents; scratch root is removed. No clone, fixture files, /tmp tree, or bytecode was created by this seat.

## Limits, risks and handoff

- No known candidate defect observed by these bounded checks. Finite case success does not certify all inputs, universal calibration, freshness policy, RFC exclusivity or production integration.
- Scope intentionally excludes network, live clock, HTTP Date parsing, cache lifetime, storage/reuse permission and browser behavior. Actual property GET trial belongs to ExecTrial-2, source reopening to the source seat, canonical planner/integration and revision-scored counter to L1.
- No production-path revision counter, build, lint, formatter, broader test suite, provider probe, browser, service, install, commit/push or git/jj mutation was run. L1 must integrate the exact candidate bytes and own the post-integration C2 counter and wider gates.
- LSP definitions/references/refactor tools are not exposed in this seat; unavailability is tool-inventory based, not inferred from an empty symbol response. This is a new isolated candidate with no existing production callsites changed.
- Candidate path shared with ReviewAge, MutAge and ExecTrial-2 for their independent scoped work. Their results are not incorporated or claimed here; no reviewer findings constitute outside admission.
- Operator install rules read; host-wide pacman pause respected. No tool installation/update occurred.
