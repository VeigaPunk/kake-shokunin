# Round 75 — Amendment 3 (terms only, before any after-state)

Recorded 2026-11-03 by the L1 (`KakeR75`) after the freeze and before any after-state, in response
to the ReviewerC2 seat's provenance findings against the delivered C2 tool. The frozen §C2 claim
already says "bound to a **committed** receipt that re-derives from committed bytes"; this
amendment makes the two checks that sentence implies explicit, because the delivered tool accepted a
worktree-only receipt and never validated the receipt's declared revision.

## A6 — the receipt is read from committed bytes

`--check` reads the receipt with `git show <revision>:corpus/knowledge/instrument-receipts.json`.
A receipt that exists only in the working tree is a mismatch (`receipt=uncommitted`, `met=false`);
its worktree presence is reported as a note and is never green. A `--worktree-receipt` opt-in flag
may exist for local debugging only; the default and the evidence path are committed bytes.

## A7 — the declared revision must resolve and be an ancestor

The receipt's `revision` field must be a 40-hex token that resolves to a commit and is an ancestor
of (or equal to) the measured revision. A nonexistent token, or a revision that is not an ancestor,
is a mismatch (`receipt_revision_invalid`), never a green.

## A8 — no other term moves

The population rule, the `{path, sha256, bytes, selftest_mode}` entry shape, the Amendment-1 floor,
`met = (bound == population) and (mismatches == 0) and missing_frozen == 0`, the output line and the
exit contract are unchanged. The two new checks are implementation of "committed receipt", which the
frozen claim already required — the v0 tool under-enforced it.
