# Round 75 — Amendment 1 (terms only, before any after-state)

Recorded 2026-11-03 by the L1 (`KakeR75`) after the freeze `88f2e05f` and before any after-state
measurement. No after-state value has been measured when this lands; it changes the wording of one
kill-rule clause and adds one counter term. The predicates, targets and controls of §C1/§C2 are
unchanged.

## A1 — the frozen population is a floor, not an equality

Contract §C1 kill rule read: "…or when the file list the counter derives differs from the 16 above."

That literal sentence forbids the round's own after-state: the appended `### Round 75 gate registry
additions` section carries live rows for `c75_row_truth.py` and `scripts/instrument_receipts.py`
(the contract's own §C1 after-state plan requires this self-application), so the derived population
grows from 16 to 18. The clause is corrected to:

> The claim is not met when any population file has an open E1–E4 finding, when `append_only` is
> false, or when the counter reports `missing_frozen > 0` — a path of the frozen 16 that the
> derivation no longer produces. Derived files beyond the frozen 16 are in-population and must
> satisfy E1–E4 like the rest.

The counter therefore prints `missing_frozen=<N>` and adds one finding per missing frozen path. Its
`--population` default is the 16 frozen paths of contract §C1. `ScribeRows`'s rows for this round's
instruments are in-population by this clause, so their claims must re-derive like any other.

## A2 — C2 population growth is the same rule

Contract §C2's population is "the same 16 files as §C1". By A1 the C2 tool's population is the same
derivation at the measured revision: the frozen 16 must be present (`missing_frozen=0`) and any
additional live-row instrument is in-population. `met = (bound == population) and (mismatches == 0)`
and `missing_frozen == 0`.

Rationale for both: growing a population with the round's own instruments is the point of a
self-verifying registry; shrinking it (a dropped row or a deleted file) stays the forbidden move,
which is why the frozen list is a floor and `append_only` is retained.
