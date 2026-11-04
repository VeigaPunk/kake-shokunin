# Round-80 amendment 3 — R79-2 evaluability at a measured revision (before the carrier measurement)

Found by the wave's `ExecGuard` seat while validating its own design, before any carrier measurement:
in `c80_defect_queue.py`'s `--revision` mode the counter exports a scratch tree that has no `.git` and
did not carry the governed ledger, so `scripts/ledger_append_guard.py --root <tree> --json` could only
report `files=0` there — R79-2 would read `open` at the carrier no matter what the lane held. The item's
condition and the claim's predicate are unchanged; only the plumbing that makes the condition
decidable at a revision changes.

- `scripts/ledger_append_guard.py` gains `--base-file <path>`: compare against an exported base
  snapshot instead of `git show`. `--selftest` still prints `fixture append: passed`,
  `fixture non-prefix: failed`, `selftest: 2/2 passed`.
- `c80_defect_queue.py` exports `.ufo/waves/round-58/receipt-rewrites.json` from the measured revision
  and writes the base revision's copy (`--base`, default `9998dc7a`) to a snapshot, passing
  `--base-file` in revision mode. Worktree mode is unchanged.

`--revision` remains the honest measurement mode: every item is still decided from the measured
revision's bytes, and the guard still verifies that the base ledger's bytes survive as a prefix.
