# Round 77 — Amendment 2 (terms-only; recorded before any after-state)

Written after the attack seat `ReviewC1` scored a **reference** counter (not the delivered one) and before the
delivered `c77_shonen_ledger.py` exists and before any after-state. It corrects one arithmetic error in the
frozen contract and closes four ways a letter-compliant counter could be greened. No claim sentence, axis,
target predicate or kill rule changes: `met <=> boxes == 4 and unexamined == 0 and mismatches == 0` stands.

## A1. Base target arithmetic

The contract's C1 target line said the base prints `mismatches=4`. Under the frozen mismatch definition that
is wrong: at `a2cc5f51` there is no ledger, so no row and no marker assertion exists and the mismatch count is
**0**. The base red is carried by `unexamined=4`. The frozen base line is therefore:

```
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false
```

exit 1. The report quotes this line, not the earlier one.

## A2. Checks are declarations, never executable

A ledger row's `checks[]` entries carry **no shell command**. Each check is
`{"id": <str>, "kind": <fixed keyword>, "path": <repo-relative path>, "params": {...}, "observed": <value>}`
where `kind` is one of a counter-implemented vocabulary — `exists`, `count_at_least`, `regex_count`,
`all_ids_resolve`, `no_match` — and the counter ignores any check whose `kind` is outside it (a mismatch, not a
silent pass). This closes the "counter executes ledger-supplied shell commands" hole: the ledger can describe
a measurement, never cause one.

## A3. `observed` comparison is exact, on one normalised form

For every check the counter computes its own observation from committed bytes at `--revision` and compares it
with the row's `observed` **after a single normalisation**: integers compare as integers, strings compare as
exact strings. A row whose recorded `observed` disagrees is a mismatch even when `holds` is true; `holds` is
advisory only and never read by `met`. (This keeps honest rows admissible and makes a fabricated `holds` flag
inert.)

## A4. Box range and revision argument

- A ledger row whose `box` is not one of 1, 2, 3, 4 is a mismatch (never ignored).
- `--revision` is **required**; omitting it is a usage error (exit 64), never a default to `HEAD` or the
  worktree.
- One row per box; a second row for the same box is a mismatch.
- `[x]` requires a `verifier` string naming a non-author; a `[~]` or `[x]` with no row is a mismatch; a
  `" "` marker with an `evidenced` row is a mismatch.

## A5. What the delivered counter must survive (the attack fixtures)

Fixtures 02 (four `evidenced` rows with `holds=true` and no measurements), 03 (`[x]` over `gap` rows with a
fabricated verifier), 04 (a `command` check), 05 (a row for box 7), 06 (`observed` contradicting the
derivation) and 07 (untracked worktree ledger at a base revision) must each stay **red** — `met=true` on any
of them voids the claim. The delivered counter's `--selftest` must include at least these six shapes plus a
clean 4-box fixture.
