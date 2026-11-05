# ExecStubs — held-out subject population for the C2 counter (round 92)

Seat: ExecStubs (leaf executor). Freeze revision measured:
`a5640ca02c20f94a0fa03af41b977b46ae99808e`. This population is **independent
evidence, not scored by the frozen predicate**: it probes what the frozen
counter `c92_heuristic.py` can and cannot distinguish, from the contract text
alone.

## Method

1. 14 candidate subjects were written from `.ufo/waves/round-92/c2-contract.md`
   alone into `subjects/` (2 conforming, 12 non-conforming; each non-conforming
   subject breaks exactly one numbered clause, named in its filename and marked
   `VIOLATION` in its source). Structures differ: `conforming-table-driven.py`
   is a validation table + first-match rule table;
   `conforming-branch-per-clause.py` is one flat function with a numbered branch
   per clause; the 12 negatives are compact standalone implementations.
2. Each subject was scored by the frozen counter, one run per subject: copied to
   `scripts/heuristic_freshness.py` in a scratch shared clone of the lane
   checked out at the freeze revision, committed there with a fixture-only
   identity (`ExecStubs fixture <execstubs@fixture.invalid>`; clone toplevel
   asserted before every commit), then
   `python3 -B .ufo/waves/round-92/c92_heuristic.py --root <clone> --revision <commit> --work <scratch>/w --candidate scripts/heuristic_freshness.py`.
3. Full stdout/stderr/exit per run: `runs/<subject>.txt`; first lines:
   `scores.txt`.

Expected: the two conforming subjects read `met=true`; every negative reads
`met=false`. Any other reading is a finding about the counter, reported, not
patched.

## Results (counter first lines verbatim in scores.txt)

| Subject | hand | gen | forgeries | met | reading |
|---|---|---|---|---|---|
| conforming-branch-per-clause | 28/28 | 120/120 | 5/5 | **true** | expected ✓ |
| conforming-table-driven | 28/28 | 120/120 | 5/5 | **true** | expected ✓ |
| neg-clause01-duplicate-case-kept | 27/28 | 120/120 | 5/5 | false | caught: `refuse/duplicate-header-name` |
| neg-clause02-cr-in-value-accepted | 28/28 | 120/120 | 5/5 | **true** | **finding F1** |
| neg-clause03-types-coerced | 28/28 | 120/120 | 5/5 | **true** | **finding F2** |
| neg-clause04-quoted-delta | 28/28 | 120/120 | 5/5 | **true** | **finding F3** |
| neg-clause05-date-parsed-as-float | 27/28 | 120/120 | 5/5 | false | caught: `refuse/date-non-integer` |
| neg-clause06-expires-parsed-as-float | 28/28 | 120/120 | 5/5 | **true** | **finding F4** |
| neg-clause08-validate-after-decision | 28/28 | 120/120 | 5/5 | **true** | **finding F5** |
| neg-clause09-nostore-ignored | 27/28 | 120/120 | 5/5 | false | caught: `store/no-store` |
| neg-clause10-smaxage-when-not-shared | 27/28 | 108/120 | 5/5 | false | caught: `explicit/s-maxage-ignored-private` + 12 gen |
| neg-clause11-public-not-honored | 27/28 | 120/120 | 5/5 | false | caught: `gate/500-public-overrides` |
| neg-clause12-cap-absent | 27/28 | 107/120 | 5/5 | false | caught: `heuristic/cap-86400` + 13 gen |
| neg-clause13-lm-after-date | 27/28 | 120/120 | 5/5 | false | caught: `gate/last-modified-after-date` |

Baseline receipt: `runs/00-baseline-candidate-absent.txt` — the same clone at
the freeze revision without a candidate reads `candidate=absent … met=false`,
exit 1, matching `controls/base-c2.txt`.

Subject sha256 digests are recorded in the seat report (`.ufo/waves/round-92/w1/ExecStubs.md`).

## Findings (defects of the frozen counter; nothing was repaired)

- **F1 — clause 2 (CR/LF/NUL in header values) is uncovered.**
  `neg-clause02-cr-in-value-accepted` skips the CR/LF/NUL refusal and reads
  `hand=28/28 generated=120/120 … met=true` (exit 0). No hand case feeds a
  control character and the seeded generator never emits one.
- **F2 — clause 3 (scalar/value types) is uncovered.**
  `neg-clause03-types-coerced` coerces `"status": "200"` to 200, accepts bools
  as ints and pushes non-string header values through `str()`, and reads
  `hand=28/28 … met=true`. This is the exact variant round-91 routed as
  uncovered (R91-2 / K91-6: "clause 3's value-type refusal is uncovered"); the
  frozen round-92 counter still has no case for it.
- **F3 — clause 4's quoted delta-seconds refusal is uncovered AND the
  counter's own reference violates the contract (oracle/contract drift).**
  `neg-clause04-quoted-delta` accepts `max-age="600"` and reads
  `hand=28/28 … met=true`. Demonstrated separately: importing the frozen
  counter and calling its `reference()` on
  `{"stored": {"status": 200, "headers": {"Date": "1000000",
  "Cache-Control": "max-age=\"600\""}}, "now": 1000000}` returns
  `{"decision": "explicit", "lifetime": 600, "heuristic": false}` — the
  reference strips quotes in `parse_cc` *before* the bare-decimal check, so it
  accepts what clause 4 says "is a refusal". Both contract-faithful conforming
  subjects refuse that input (verified directly, exit 1,
  `invalid_input: delta-seconds argument is quoted`). The counter's
  reference-self-check runs the reference against the hand cases only, so this
  drift cannot self-report: an oracle-follower and a contract-follower are
  indistinguishable to the instrument on this clause.
- **F4 — clause 6 (Expires non-integer refusal) is uncovered.**
  `neg-clause06-expires-parsed-as-float` reads `hand=28/28 … met=true`. No
  case feeds a non-integer Expires. Same shape for clause 7 (Last-Modified)
  through the shared `delta()` helper — argued from the counter source and the
  case set, not separately counter-measured (12 negative slots).
- **F5 — clause 8 (no arithmetic before validation) is uncovered.**
  `neg-clause08-validate-after-decision` answers not-storable from a lenient
  pre-scan *before* clauses 1–7 run, so a malformed field on an unstorable
  response is never refused, and reads `hand=28/28 … met=true`. Every frozen
  refusal case rides a storable-shaped 200; no case combines a malformed field
  with `no-store` / `private`+shared / `Vary: *`.
- **F6 — the generated population can never witness a refusal-clause
  violation.** The seeded generator (counter `generate()`) emits only
  well-formed fields: integer dates, no duplicate header names, no duplicate
  Cache-Control directives, no quoted or signed delta-seconds, no control
  characters, and `Last-Modified > Date` with probability 5/2 000 005 per case
  (~0 expected in 120). All refusal coverage therefore sits in the 5 hand
  cases, which cover only Date-absent, Date-non-integer,
  duplicate-header-name, signed delta-seconds and empty-directive. Measured
  consequences: neg-clause13 (LM after Date) is caught hand-only (gen
  120/120); neg-clause11 (public) is caught hand-only (gen 120/120, the
  `public` × non-cacheable-status joint is ~0.4 %/case); the clause-4
  duplicate-directive variant (same name twice, different arguments) is
  uncovered by construction of the case set — same class as F1–F5, not
  separately counter-measured (slot budget).

What the counter does distinguish (7/12 negatives refused, each failing on
exactly the frozen case its clause predicts — see the `hand_failures` detail in
each run receipt): clauses 1, 5, 9, 10, 11, 12, 13.

## Limits

- Both conforming subjects and all 12 negatives were authored by this seat
  from the same contract reading; there is no second independent author in
  this evidence. The counter's own reference and hand cases were not used to
  write the subjects; they were consulted only for the F3 drift demonstration
  and for naming the exact caught cases after scoring.
- Clause 7 and the clause-4 duplicate-directive variant are coverage-gap
  arguments from the shared code path and the case set, not measured runs.
- The sandbox, anti-table and pins conjuncts were never in play: every subject
  reads `anti_table=ok population=ok` and none of the subjects attempts
  imports beyond `json/sys/re`, file opens or process creation.
- No tool was installed or upgraded for this seat; nothing fetched from the
  network; no pacman, no /tmp writes (scratch was
  `/fast/scratch/hyaku/kake-r92/ExecStubs`, deleted after receipts were
  copied).
