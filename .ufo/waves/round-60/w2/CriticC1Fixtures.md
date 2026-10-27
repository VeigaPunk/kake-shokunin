# CriticC1Fixtures

ATTACKS:
- Attempted the requested wave-1 independent 54-case fixture harness against frozen C1 v1 and checked its compatibility with amendments A2–A7 and the v1 internal selftest.
- Axes: calibration correctness, fixture observability, and contract fidelity.

ADAPTATION:
- The harness is at `.ufo/waves/round-60/w1/ExecC1Fixtures.files/c60_gate_status_fixtures.py`. Its outer runner launches a fresh subprocess against each synthetic repo (`run_counter`, lines 722–738); synthetic population files contain toy Python bodies (lines 317–348).
- C1 v1 freezes actual base blob IDs in `FROZEN` (`.ufo/waves/round-60/c60_gate_status.py`, lines 104–135). Consequently the outer harness's fixtures are classified `member_changed` before its intended row/label/command checks can be exercised. The specified adaptation is not just altering the fixture member set: the counter itself has no CLI option for fixtures, and `measure(..., frozen=...)` is internal. The frozen counter selftest demonstrates the supported method: `fixture_frozen(dA, tipA)` followed by `measure(..., frozen=fzA)` (counter lines 814–816), with its own bespoke fixtures and assertions.
- Did not modify the harness or the frozen counter; did not claim the 54 cases were run. The wave-1 harness expectations predate amendments A2–A7, so even a successful adaptation must derive expected classes from the amended contract, not treat its legacy expectations as authoritative.

DIVERGENCES:
- No case-by-case divergences established: the harness was not run because its subprocess design cannot inject a fixture-specific frozen member set into the committed counter without adapting its runner to call internal `measure` and rebind the frozen set. Any assertion that a specific test fails is [INFERENCE], not an observed result.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | `.ufo/waves/round-60/w1/ExecC1Fixtures.files/c60_gate_status_fixtures.py:722-738` | This harness invokes the counter as a subprocess for toy fixture repos, whereas v1's A4 frozen blob IDs accept only actual population blobs. Its cases therefore cannot independently test amended C1 classification unless adapted to call `measure` with fixture-specific frozen IDs. | `sed -n '104,135p' .ufo/waves/round-60/c60_gate_status.py; sed -n '722,738p' .ufo/waves/round-60/w1/ExecC1Fixtures.files/c60_gate_status_fixtures.py; sed -n '814,816p' .ufo/waves/round-60/c60_gate_status.py` (reviewed source; no execution) | Adapt the harness to load the committed counter module, derive the fixture member blob IDs and invoke `measure(..., frozen=fixture_frozen(...))`; update expected classes to A2–A7. Keep all fixture commits isolated under scratch. |

VERDICT: No C1 class divergence demonstrated. The requested 54-clause run remains unexecuted; current harness is incompatible with A4 without the internal-call adaptation.