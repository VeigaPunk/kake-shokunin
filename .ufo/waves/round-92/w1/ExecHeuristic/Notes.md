# ExecHeuristic — C2 subject notes (round 92, wave 1)

Deliverable: `scripts/heuristic_freshness.py` (500 lines, stdlib only: `json`,
`re`, `sys`). Implements `.ufo/waves/round-92/c2-contract.md` v1 clauses 1–13.

## Measurement

- Development clone: `/fast/scratch/hyaku/kake-r92/ExecHeuristic/clone`,
  `git clone -q --shared` of the lane, detached at freeze
  `a5640ca02c20f94a0fa03af41b977b46ae99808e`; `rev-parse --show-toplevel`
  asserted equal to the clone before the first commit; `refs/heads/master`
  re-pointed at the lane tip per the fixture rules. Three fixture-identity
  commits (`ExecHeuristic fixture <execheuristic@fixture.invalid>`), HEAD
  `846d7642dc1748e66c9e0ae2a1464bd970bb17d0`.
- Frozen counter run:
  `python3 -B .ufo/waves/round-92/c92_heuristic.py --root $S/clone
  --revision 846d7642dc1748e66c9e0ae2a1464bd970bb17d0 --work $S/work`
  → exit 0,
  `hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok
  population=ok seed=92 met=true`.
  Receipt: `counter.txt` (both output lines; `candidate_sha256`
  `7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c`).
- Selftest: `python3 -B scripts/heuristic_freshness.py --selftest` →
  `selftest 54/54`, exit 0. Receipt: `selftest.txt` (run on the landed LANE
  copy; byte-identical to the measured clone blob, sha256 above).
- The landed file `scripts/heuristic_freshness.py` is uncommitted in the lane
  worktree (this seat never commits in the lane); the L1 lands it. The
  counter receipt names the clone revision that carries the identical bytes.

## Iteration history (what the counter caught)

1. First counter run: `hand=5/28 generated=0/120`, every decision case a
   `PermissionError: sandbox: import denied: __future__` — the frozen
   sandbox's import allowlist has no `__future__`, so
   `from __future__ import annotations` is refused at run_path time. Fix:
   dropped the import (the module carries no annotations that need it).
2. Second run: `met=true` (28/28, 120/120, 5/5, anti_table=ok,
   population=ok). A dead-weight cleanup (unused selftest helper parameter)
   followed; counter re-run at the final HEAD, same reading.

## Composition question (routed defect R91-4 / K91-9 asks for it)

`scripts/cache_control_effective.py` (r86) exposes `split_directives`,
`argument` and `http_date`, but composition was **not possible** for this
subject, on two independent grounds:

1. The frozen counter extracts only the candidate blob into the subject tree
   and runs it with `sys.path = [<subject dir>]` under an audit hook that
   denies `open` outside that tree and every import outside a frozen
   allowlist. A sibling import (`import cache_control_effective`) has no
   module to find; even a vendored copy would fail because the r86 reader
   imports `email.utils`/`datetime` handling whose `email` package is not in
   the allowlist. This is the same reachability wall that refuses
   `neg-oracle-import.py`.
2. The r86 reader's contract is a different wire shape
   (`{"cache_control": [strings], "shared": bool, "expires"/"date":
   HTTP-date strings}`) with a quoted-comma-aware splitter and real HTTP-date
   parsing; contract v1 here declares a naive `split(",")`, SP/HTAB trimming,
   ASCII-lowercased names, quoted-string arguments, and integer epoch-second
   `Date`/`Expires`/`Last-Modified` (the lane adapter convention shared with
   `cache_current_age.py`/`stored_reuse.py`). Composing it would change
   decisions on inputs the v1 grammar defines differently.

Clause 4 was therefore implemented directly, mirroring the contract text.

## Findings for the routed list (frozen instruments untouched)

- **Contract/reference drift, unexercised.** `c2-contract.md` clause 4 says a
  delta-seconds argument "must be a bare non-negative decimal integer: a
  quoted or signed form is a refusal". The counter's `reference.parse_cc`
  strips a surrounding quoted-string *before* the `[0-9]+` check, so
  `{"Cache-Control": "max-age=\"5\""}` is accepted by the reference
  (`explicit`, lifetime 5) while a contract-faithful reader refuses it. The
  landed tool follows the contract (refusal; pinned by selftest fixture
  `refuse/delta-seconds-quoted`). Neither the 28 hand cases nor the seed-92
  generated population can produce a quoted delta argument (the generator
  emits only bare `max-age=%d`/`s-maxage=%d` forms), so `met=true` is
  unaffected — verified. Routed as a contract-vs-reference wording defect for
  the round's list; no frozen byte was edited.
- **Sandbox allowlist note.** `__future__` is not in the counter's import
  allowlist; any future subject using `from __future__ import annotations`
  (or any PEP 563/604-style annotation syntax needing it) is refused before
  its first line runs. Informational for sibling seats.
