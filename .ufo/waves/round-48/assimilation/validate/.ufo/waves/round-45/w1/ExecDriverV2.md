# ExecDriverV2 — round 45 wave 1

## Changes
- Added `.ufo/waves/round-45/c45_audit.py`, retaining the v1 CLI, summary/row fields, and audit exit convention. It creates and requires an empty output cohort, writes `run-manifest.json` before counter launches, and applies the same pure receipt-validity gate to control and build receipts.
- Invalid counter exits, `tool absent`, stale/mismatched/out-of-window receipts, and receipts without a seed cannot earn witness or not-met credit; invalid rows fail the expectation. Requested build counts are pinned.
- The serialized build rows retain the v1 field set. Internal validity state is not serialized.

## Evidence
Command:
```text
python3 -B .ufo/waves/round-45/c45_audit.py --selftest
```
Decisive output, verbatim:
```text
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
```
Result: **PASS** for the named selftest attack. It retains v1 assertions and exercises timing-only `T1`, `counter_error`, `tool_absent`, stale SHA and mtime, missing seed/receipt, error-row exclusion from not-met, and one build row versus `--build-runs 3`.

## Files written
- `.ufo/waves/round-45/c45_audit.py`
- `.ufo/waves/round-45/w1/ExecDriverV2.md`

Created `/fast/scratch/hyaku/kake-r45/ExecDriverV2/`; no scratch files were needed. No tools were installed.

## Risks / blockers
- The one-second `MTIME_EPS_NS` tolerance deliberately accommodates coarse filesystem timestamps; a receipt timestamp within that tolerance just outside the nominal boundary is accepted.
- The full audit/cohort regression and matrix were not run; the task assigns full-audit ownership to `ExecRegressionHonest`. LSP was unavailable in the exposed session tools, so no LSP query was made.