# MutationC3Noop

## Probe
- Detector: `.ufo/waves/round-61/c61_recheck_pins.py --selftest` (verbose; fixture TMPDIR under `/fast/scratch/hyaku/kake-r61/MutationC3Noop`).
- Mutant: deleted the C2 `if not pinned` failure clause, which enforces at least one dated pin. This tests whether all-carried rows plus Gate notes can pass.
- Expected: pristine selftest passes and recognizes the all-carried fixture as failing C2; mutant selftest fails because that fixture becomes 6/6 green. Restored selftest passes.

## Actual outputs
- Pristine: `c61 recheck-pins selftest: 56/56` exit 0. `CASE base-tree | C2+C5 | 1 | PASS`; `CASE all-carried-with-notes | ['C2_pinned_dates'] | 1 | PASS`; `CASE constant | C3+C4 | 1 | PASS`.
- Mutated: `c61 recheck-pins selftest: 54/56` exit 1. `CASE base-tree | C2+C5 | 1 | FAIL` (only C5 fails; C2 no longer fails); `CASE all-carried-with-notes | ['C2_pinned_dates'] | 0 | FAIL` (all checks pass unexpectedly). The selftest explicitly reports: `expected exit 1 with failures ['C2_pinned_dates'] and note '0 pins'; got exit 0 with []`.
- Restored: `c61 recheck-pins selftest: 56/56` exit 0.

## Finding
C5's carry-note rule allows every due row to be unpinned when its cadence is unchanged and each Gate line names an observed state; that is its intended carried-row path. The all-noted state does **not** pass the frozen six-condition predicate, because C2 independently requires at least one concrete pin. Thus pure do-nothing/all-noted vacuity is blocked and the frozen target is shown to fail that control (base-tree fails C2 and C5; the crafted all-noted control fails only C2). The constant control independently fails C3+C4. This test does not establish a ten-of-ten pin minimum: C2's explicit zero-pin gate proves only that zero pins are rejected.

## Hash/restoration evidence
- Pristine counter SHA-256: `f8fd06f5bf36597a44c8d9df410df5343135a1c439fe3399f04c291827e9adbd`.
- Mutant counter SHA-256: `aeb185cc35969adee60e5ba5615423c5d72f5d6f28a8e00a3ea7802eb7f73a27`.
- Restored counter SHA-256: `f8fd06f5bf36597a44c8d9df410df5343135a1c439fe3399f04c291827e9adbd` (byte-identical to pristine backup).
- Scratch clone only; no lane source, index, or git state was modified. No tools installed.

VERDICT: KILLED — C2's zero-pin gate rejects the all-noted control; removing it makes the control pass and the bounded selftest fail.