# Round 75 — Amendment 2 (terms only, before any after-state)

Recorded 2026-11-03 by the L1 (`KakeR75`) after the freeze `88f2e05f` and before any after-state
measurement, in response to the ReviewerC1 seat's two held-out findings against the frozen v0
counter. It clarifies what "the row's claim re-derives" already means in §C1; no predicate, target,
population or control changes.

## A3 — a self-test claim must be the instrument's own

Frozen §C1 E1 read "a row whose Kind family is `gate` carries a working self-test (`--selftest`
exits 0)". The v0 counter executed whatever `--selftest` command the Self-test cell named, so a row
whose cell ran a *different* file's self-test re-derived a green claim it does not own (ReviewerC1
held-out F03). The clause is made explicit:

> E1/E2 apply to the instrument's own self-test: the recorded Self-test command must name the
> effective row's instrument path. A cell whose command names another instrument, or no instrument,
> is a finding (`E1 command names <other>`), whatever its exit code.

## A4 — E4 covers every live row, and the floor covers a vanished instrument

Frozen §C1 E4 read "every `.py`/`.mjs` path token in the row's cells resolves at the measured
revision". Clarified: the check covers **every** live row's cells (not only the row effective for a
file), and an instrument whose file, or a row that named it, disappears from the derivation is
reported through the Amendment-1 `missing_frozen` term (a deleted file whose Name cell is retained
is otherwise invisible when the derivation loses it).

## A5 — the same sentence in three places

The counter code, the receipt labels and the contract must carry these three clauses as the same
sentence. Any divergence found by a later closure is a defect of this round's landing, not a
reinterpretation of the frozen claim.
