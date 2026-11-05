VERDICT: C2 instrument landed and measured — `scripts/heuristic_freshness.py` reads `hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true` (exit 0) on the frozen counter at clone revision `846d7642dc1748e66c9e0ae2a1464bd970bb17d0`.

Seat: ExecHeuristic (leaf). Scope executed: implement the C2 subject per
`.ufo/waves/round-92/c2-contract.md` (clauses 1–13), stdlib only, develop in a
scratch clone, land `LANE/scripts/heuristic_freshness.py`, copy receipts.

## Files changed

- `scripts/heuristic_freshness.py` — new, 500 lines, sha256
  `7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c`.
  Uncommitted in the lane worktree (this seat never commits in the lane); the
  L1 lands it. Byte-identical to the measured clone blob (verified:
  worktree == `git show HEAD:` == lane copy, same sha256).
- `.ufo/waves/round-92/w1/ExecHeuristic/{counter.txt,selftest.txt,Notes.md}`
  — receipts and method notes.

## Behavior

One JSON object on stdin → one JSON object on stdout with exactly
`decision`/`lifetime`/`heuristic`; refusal is `invalid_input: <reason>` on
stderr, exit 1, empty stdout. `--selftest` runs 54 in-memory fixtures (the
contract's 28 worked cases plus refusal/boundary shapes the frozen hand set
does not carry: clause-2 CR/LF/NUL, clause-3 bool/float/out-of-range types,
clause-4 quoted/conflicting/empty directives, clause-8 validation-before-
decision) and prints `selftest 54/54`, exit 0. The module docstring names the
two lane conventions (10 % fraction, 86400 s cap) as lane conventions, not RFC
requirements, and states the integer-epoch-seconds adapter convention shared
with `cache_current_age.py`/`stored_reuse.py`.

## Evidence (exact commands, exit codes, receipt paths)

All paths below are relative to the lane root
(`/home/vgpnk/Projects/shokunin/kake-shokunin`).

1. Clone setup (fixture discipline):
   `git clone -q --shared <lane> $S/clone`;
   `git -C $S/clone checkout -q --detach a5640ca02c20f94a0fa03af41b977b46ae99808e`;
   `git -C $S/clone rev-parse --show-toplevel` → `$S/clone` (asserted before the
   first commit); `update-ref refs/heads/master` to the lane tip. Three
   fixture-identity commits; HEAD `846d7642dc1748e66c9e0ae2a1464bd970bb17d0`.
2. Frozen counter:
   `python3 -B .ufo/waves/round-92/c92_heuristic.py --root $S/clone
   --revision 846d7642dc1748e66c9e0ae2a1464bd970bb17d0 --work $S/work`
   → **exit 0**; line 1:
   `C2v92 revision=846d7642… candidate=present hand=28/28 generated=120/120
   forgeries_refused=5/5 anti_table=ok population=ok seed=92 met=true`.
   Receipt: `.ufo/waves/round-92/w1/ExecHeuristic/counter.txt` (full two-line
   output; `candidate_sha256 7bfe82da…`, `hand_failures []`,
   `population_drift []`, all five forgeries `admitted: false`).
3. Selftest on the landed lane copy:
   `python3 -B scripts/heuristic_freshness.py --selftest` → **exit 0**,
   `selftest 54/54`. Receipt:
   `.ufo/waves/round-92/w1/ExecHeuristic/selftest.txt`.
4. Iteration evidence (scratch, not cited as receipts): the first counter run
   read `hand=5/28 generated=0/120 met=false` because
   `from __future__ import annotations` trips the frozen sandbox's import
   allowlist (`PermissionError: sandbox: import denied: __future__`); dropping
   the import (no annotation syntax needs it) and one dead-weight cleanup
   produced the final `met=true` run above. Four refusal paths were
   smoke-tested during iteration (missing Date, extra top-level key, invalid
   JSON, quoted `max-age`) — all `invalid_input:` on stderr, exit 1, empty
   stdout.

## Composition answer (routed defect R91-4 / K91-9)

Composition with `scripts/cache_control_effective.py` was **not possible**,
verified two ways: (a) the frozen counter extracts only the candidate blob
into the subject tree and runs it with `sys.path=[<subject dir>]` under an
audit hook denying `open` outside that tree and every import outside a frozen
allowlist — a sibling import has no module to find, and even a vendored copy
fails because the r86 reader's `email.utils` dependency is not allowlisted
(the same wall that refuses `neg-oracle-import.py`); (b) the r86 reader's wire
shape (`cache_control` string array, HTTP-date strings, quoted-comma-aware
splitting) is a different contract from v1's naive `split(",")` + integer
epoch seconds, so composing it would change decisions on contract-defined
inputs. Clause 4 was implemented directly; no reader was duplicated silently —
the reason is recorded in `Notes.md` and here.

## Findings / defects (frozen instruments untouched, routed for the round's list)

- **F1 — contract/reference drift, unexercised.** `c2-contract.md` clause 4
  declares a quoted delta-seconds form a refusal; the counter's
  `reference.parse_cc` strips the quoted-string before the `[0-9]+` check, so
  `max-age="5"` is *accepted* by the reference (`explicit`, lifetime 5) and
  *refused* by the landed contract-faithful tool (selftest fixture
  `refuse/delta-seconds-quoted` pins the refusal). The 28 hand cases contain
  no quoted delta argument and the seed-92 generator emits only bare
  `max-age=%d`/`s-maxage=%d` forms, so `met=true` is unaffected — verified by
  the run above. Routed as a wording defect in the frozen pair; no frozen byte
  edited.
- **F2 — sandbox allowlist note (informational).** `__future__` is absent from
  the counter's import allowlist; any future subject using
  `from __future__ import annotations` is refused before its first statement.
  Sibling seats writing scored subjects should avoid it.
- **F3 — no defect found in the counter's predicates themselves.** The
  anti-table, population pins, forgery sandbox and generated-population
  reference all behaved as declared on this subject; five forgeries refused,
  zero anti-table hits, pins digest `b780fa24…` matched.

## Honest limits

- The tool decides over supplied integers only, per contract scope: no clock,
  no HTTP-date parsing, no network, no store, no reuse/revalidation/serving
  decision (that stays with `stored_reuse.py`), and no claim about any live
  property.
- `--selftest` is in-memory fixtures, not a substitute for the frozen counter;
  the counter receipt is the measurement.
- The lane worktree file is uncommitted; if the L1 lands different bytes the
  counter must be re-run at the carrier revision.
- No tools were installed or upgraded this seat (stdlib only); nothing to
  record under the tooling directive.

## Blockers

None.
