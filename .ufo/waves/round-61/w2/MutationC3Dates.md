# MutationC3Dates

## Scope and detector

Probed the frozen C3 counter at the cloned lane tip (`f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`) using its bounded `--selftest` fixture detector. The tip's registry is still the base state: S001–S010 retain cadence strings and `corpus/lessons/round-61.md` is absent, so a real-lane run would be a do-nothing baseline failure and cannot count as a killed mutant. The selftest builds and removes isolated fixture repositories; no lane registry/score was changed.

## Outputs

- C3 detector: `python3 -B .ufo/waves/round-61/c61_recheck_pins.py --selftest` → `c61 recheck-pins selftest: 56/56 (green exit 0 and 6/6; base-tree and constant controls; 30 fixture cases; predicate met: conditions_passed == 6 of 6)` (exit 0).
- C2 header-counter selftest: `python3 -B .ufo/waves/round-61/c61_header_cases.py --selftest` → seven controls passed; reference implementation scored 18/18, both R3 shape controls matched expectations (12 passes, 11 rejects), final `selftest: ok (7 controls scored) exit 0`.

## Date-mutant coverage

| Mutation / boundary | Expected C3 C2_pinned_dates result | Detector evidence | Verdict |
|---|---|---|---|
| Date before opened (including equality at opened) | Reject; strict lower bound is `opened < pin` | No dedicated before/equal-opened fixture in the 30-case selftest matrix | Not probed; coverage gap |
| Date after cadence | Reject | Selftest `c2-pin-out-of-bounds` uses S003 `2027-01-18` against the 90d upper bound `2027-01-17`; expected C2 failure | Killed by selftest fixture |
| Exact upper bound for Nd cadence | Accept | Green fixture pins S003–S007 at `2027-01-17` and S008–S010 at `2027-10-19`; these equal their upper bounds | Boundary accepted in green fixture |
| Leap/day validity | Invalid calendar date rejected | Unit check `iso: 2027-02-30 is not a date` passes; no dedicated valid leap-day or leap-year arithmetic fixture | Invalid-day covered; valid leap boundary not probed |
| `on-release` +90d | Exact `opened+90d` accepted; off-by-one rejected | Green fixture sets S001/S002 to `2027-01-17`; `c2-nonnd-pin-off-by-one` sets S001 to `2027-01-18` and expects C2 failure | Exact and +1 covered; −1 not probed |
| Malformed ISO | Reject as neither a concrete date nor unchanged cadence | `c2-non-iso-cell` uses datetime text; unit checks reject datetime and `2027-02-30` | Covered for datetime and invalid day; malformed month/slash/non-padded forms not separately probed |

These are counter selftest fixture outcomes, not direct mutations against a green real after-state. No claim is made that the untested date variants were killed. The C2 header counter is a different claim and has no date-pin coverage; its selftest pass is recorded only as the requested cross-counter check.

## Restoration evidence

No source bytes were modified; the selftest's generated fixture repositories are removed by its harness. SHA-256 after the probes:

- `c61_recheck_pins.py`: `f8fd06f5bf36597a44c8d9df410df5343135a1c439fe3399f04c291827e9adbd`
- `c61_header_cases.py`: `e58d203b8bd7182cdfa6b48e1ad3771f0f26a22afb82e80d40438cba45b8327a`

No before/after mutation hash pair exists because this probe tested the existing selftest matrix without editing counter or registry bytes.

VERDICT: PARTIAL — selftest kills after-bound and +90d-positive mutants and accepts exact upper bounds; before-opened/equality, −1d on-release, and valid leap-boundary variants remain unprobed.