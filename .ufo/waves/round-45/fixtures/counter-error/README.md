# counter-error fixture

A fake counter that writes a receipt copied from a REAL committed receipt
(`verification/claim/after-final/tools/repeat-len-band.json`, byte-exact except the
runs map is truncated to the A-G runs) and then exits 2 — simulating the frozen
counter's `CannotEvaluate` path (`c44_count_v5.py:1097-1098`, reachable after the
class-run entries are recorded at `:1108`). The receipt keeps its real
`counterSha256` (the frozen v5 sha), real seed and a real G-class divergence.

Under the frozen v1 driver this receipt is credited as a witness (round-44 defect 1a).
Under driver v2 it is refused with class `counter_error` (the exit gate fires first).

Shape fidelity: the receipt was rewritten to the partial shape a real
`CannotEvaluate` produces (A-G runs only, no T runs, `equalRuns` null, an
error note); `w2/AttackFixtureShapes.md` documented the original full-receipt
shape as an unreachable combination and this correction lands it.
