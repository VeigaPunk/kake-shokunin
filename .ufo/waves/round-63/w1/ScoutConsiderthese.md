# ScoutConsiderthese — round-63 w1

Seat: ScoutConsiderthese (scout, leaf — no subagent dispatch, no lane writes)
Item: verify the round-63 lesson Gate's stated reason for rejecting
`considerthese/2026-10-26.md` proposal 2 (receipt-rewrite watch), and judge whether
its flip condition is fair.
Method: read-only. Lane files opened; one read-only run of the frozen round-58
counter at the round-63 measured commit. No lane file, index, git/jj state, frozen
claim/counter/receipt, or scratch fixture was created or modified. No tools installed.

## Observed facts

### The proposal and the rejection

- Proposal 2 (`/home/vgpnk/Projects/shokunin/kake-shokunin/considerthese/2026-10-26.md:28`,
  under the `## Part 2` header at line 26): "Receipt-rewrite watch. Each day, list files
  under `.ufo/waves/round-*/controls/` that have more than one commit touching them
  (`git log --follow`), and flag any whose `revision:` or result line changed after the
  first commit. r56 and r57 both did this and only the verifier caught it; it's a cheap
  read I can do from GitHub."
- The round-63 lesson Gate rejects it
  (`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-63.md:43-48`):
  > Reject (c), not implemented: considerthese/2026-10-26.md:26 proposal 2 is aggregate
  > bookkeeping; the semantic class it watches (receipt rewrites) is already countered by
  > c58_receipt_rewrites.py, and a git-log watch adds a second ledger without adjudicating
  > anything. Flip: repeated verifier/gate comparisons showing the semantic counter misses
  > a receipt-rewrite class the log watch would catch.
  (Minor citation drift: the proposal text itself is at line 28, the Part 2 header at 26.)
- Same reason, earlier round: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-60.md:130-131`
  — "Proposals … 2 (receipt-rewrite watch — the round-58 `receipt-rewrite-counter` already
  runs it) … are not taken."
- Precedent: round 58 adopted proposal 2 as claim C1 in event-set form
  (`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-58.md:125-128`;
  grounding seat `.ufo/waves/round-58/w1/ScribeConsiderthese.md`).

### The counter whose predicate is the stated reason

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/c58_receipt_rewrites.py`
(committed 2026-10-26 at `1c0aa21177`; sha256 `3f52040a…26c2d`; version 2, frozen before
round-58 data; docstring lines 1-51):

- Predicate (lines 57-58, identical in `contract.json:11` and the receipt line):
  `met: undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0 AND
  unpointed == 0 AND symlinks == 0 AND new_rewritten == 0 AND new_receipts == 2`.
- Population (line 59): `POP_RE = ^\.ufo/waves/round-[0-9]+/(control|controls)/.+$` —
  every round, both spellings, any depth.
- Event (docstring lines 22-25; `events()` lines 70-101): every first-parent commit in
  the tip's ancestry that M/D/A-matches a receipt path; a path's first add is the baseline;
  a rename reads as a delete plus a possible re-add event. The walk is not pinned to
  round 58 — any receipt rewrite in rounds 59+ surfaces as an event.
- `classify()` (lines 143-174): byte-level kinds `pin-only` (every changed line carries a
  revision pin, blobs equal after masking 7-40-hex ids), `pending-fill`, `append`,
  `format`, `content`, `delete`, `readd` — i.e. the two line-kinds proposal 2 names
  (revision-line relabel; pending→result fill) are two of the counter's classes.
- Disclosure semantics (`measure()` lines 200-236): each event must match a ledger entry
  on `(path, commit, status, fromBlob, toBlob)`; `phantom`/`malformed`/`wrong_kind`/
  `unpointed` reject fabricated or misclassified disclosures; `symlinks` rejects symlinked
  receipts; `new_rewritten` forbids post-commit edits to the round's own receipts even if
  disclosed; `new_receipts` requires exactly the two after-receipts.
- Docstring "Not tested" (lines 47-49): receipts outside `control(s)/` (79 such rewrites
  exist), side branches, pre-push history rewrite.

Live state, read-only run at the round-63 measured commit:

```
$ python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
C1 receipt-rewrites events=19 undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0 symlinks=0 new_rewritten=0 new_receipts=2 met=True  (met: undisclosed == 0 AND ...)
  ledger: .ufo/waves/round-58/receipt-rewrites.json present (19 entries)
  revision: 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
EXIT=0
```

So at the measured revision the counter is green, still walks all rounds' receipts, and
zero receipt rewrites occurred in rounds 59-63 (events stayed at the 19 base events;
ledger has 19 entries). It is a standing gate in `SKILL.md`'s registry (receipt-rewrite-counter
row, "first-parent history walk over every file at any depth under every round's
control(s)/, against the round-58 ledger").

Coverage comparison vs the proposal's method (from the round-58 grounding seat
`.ufo/waves/round-58/w1/ScribeConsiderthese.md`, which I re-read in full):
the proposal lists `controls/` only and misses round 52's `control/` (6 of 19 base
events); a ">1 commit" file flag collapses 19 events on 16 paths into 16 and carries no
status/blob ids/kind; its revision/result line test keeps 15 of 19 base events and loses
the four detail-line-only reruns; it has no disclosure concept, so it cannot fail a
predicate — it flags for a human. The counter's event set is a strict superset on every
axis the proposal names.

## Verdict on the stated reason: TRUE

The Gate's reason has two clauses, both verified:

1. "the semantic class it watches (receipt rewrites) is already countered by
   c58_receipt_rewrites.py" — confirmed against the predicate and the code: population
   any-depth `control(s)/` across all rounds, whole first-parent ancestry, M/D/re-add
   events keyed on git blobs, byte-level classification that includes exactly the
   relabel and pending-fill line-kinds proposal 2 names, and a disclosure ledger with
   fabrication/misclassification guards. Live-verified green at measured commit
   `05b0d7f4` (output above).
2. "a git-log watch adds a second ledger without adjudicating anything" — accurate:
   proposal 2's own text is a flag-for-human-attention watch ("flag any whose
   revision: or result line changed"); it defines no disclosure state and no pass/fail.
   The counter subsumes its detection surface and adds adjudication (the ledger
   vocabulary and the frozen predicate).

## Is the flip condition fair?

Flip as recorded: "repeated verifier/gate comparisons showing the semantic counter
misses a receipt-rewrite class the log watch would catch."

Fair in kind, overweighted in quantity, and practically near-unsatisfiable as written:

- Fair in kind. It names concrete evidence content (a demonstrated coverage miss), a
  producer (verifier/gate comparisons — non-author closure), and it is consistent with
  the lane's own epistemic rule recorded two paragraphs below it in the same lesson
  (`round-63.md` "Outside verdict": this round's gate decisions are lane self-assessment,
  author-side; the non-author closure decides agreement). A flip that commits the lane
  to reopen on outside evidence is the correct shape.
- Overweighted in quantity. The rejection rests on a static code read; the flip demands
  *repeated* dynamic demonstrations. One clearly demonstrated miss should reopen
  consideration; "repeated" entrenches the status quo and is a heavier burden than the
  evidence that supports the rejection.
- Near-vacuous as written. The counter's coverage is a strict superset of the watch's on
  every axis proposal 2 names (population, event granularity, line kinds, disclosure),
  so "a receipt-rewrite class the log watch would catch" that the counter misses is
  close to empty by construction. The one documented residual is rename-with-edit: the
  counter folds a rename into a `delete` event plus a `readd` event and never byte-compares
  the new path's content against the old path's (ScribeConsiderthese.md GROUNDING and
  DIFFERENCES; the counter's own `--no-renames` design note in its docstring). The lane's
  history has zero receipt renames (`git log --diff-filter=R -M -- .ufo` printed nothing
  at the round-58 base), so even that residual has never been exercisable. The flip never
  names this scenario, nor the counter's own stated "not tested" list (receipts outside
  `control(s)/`, side branches, pre-push history rewrite) — the only places a future
  watch could genuinely add coverage, and all outside proposal 2's stated scope.
- Producer asymmetry. The flip is not actionable by the proposal's own mechanism: the
  reflector's daily read can never satisfy it; only verifier spot-checks can. That is
  consistent with the author-side/outsider split, but the lane should note the flip is
  outsourced by design.

Recommendation (for the record, not a lane edit): keep the rejection; soften the flip
from "repeated … comparisons" to "a demonstrated miss", and name the concrete reopen
scenarios — the counter's population or ancestry walk narrowed in a future round, receipt
migration out of `control(s)/`, or a rename-with-edit whose byte linkage the event set
does not compare.

## Confidence and unknowns

- Confidence high on the reason verification (code + live run at the measured commit).
- Confidence high on the superset-coverage claim for the proposal's stated scope; the
  rename-content linkage is the single documented exception and is quoted from the
  round-58 grounding seat rather than re-derived with a fixture (no fixture built — leaf
  seat, read-only; and the lane base shows no rename history to exercise it against).
- Unknown not resolvable from here: whether the non-author verifier's round-63 closure
  will agree with this self-assessed rejection; the flip's producer clause defers to it.
