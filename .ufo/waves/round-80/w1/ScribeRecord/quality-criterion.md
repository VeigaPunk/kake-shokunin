# Round-80 QUALITY clause (append-only; the L1 appends this block to `corpus/QUALITY.md`)

## Round-80 criterion — a survivor mutant is killed by an isolated fixture, not by a neighbouring finding

Appended 2026-11-04 by the round-80 `ScribeRecord` seat; every criterion above stands unchanged.
Grounding: `corpus/lessons/round-80.md` §Corrections R79-4 and the round-79 mutation test
(`.ufo/waves/round-79/w1/MutC.md` §3-§4).

- **A frozen predicate conjunct that no fixture isolates is uncovered, and a fixture whose red belongs
  to a neighbouring conjunct does not cover it.** The round-79 criterion rendered the cheap-note control
  as `cheap-note (`malformed=1`)` (`corpus/QUALITY.md:1631`), while the same fixture is red through
  `undisclosed` first: the k4 mutant that zeroes `malformed` survived the whole frozen battery because
  "cheap-note stays red only via `undisclosed=1`" (`.ufo/waves/round-79/w1/MutC.md:57`; F2 at `:73` —
  an empty-note entry is counted as both `undisclosed` and `malformed`, so dropping `malformed` flips
  nothing), and the round-79 counter selftest passed all five counter mutants (`:75`). Admit: a survivor
  mutant of a frozen predicate conjunct is killed by the fixture built for that conjunct, its receipt
  shows that conjunct's own counter non-zero, and the kill is readable as that conjunct alone — for the
  cheap-note shape the mechanism is `undisclosed=1`, and it is never cited as evidence that `malformed`
  is exercised; a `malformed` survivor needs a fixture whose sole red is `malformed`. Reject: a survivor
  counted as covered because the existing battery's verdicts do not change under it; a kill claimed from
  a red that a different conjunct owns; a selftest tally substituted for the fixture run; and a criterion
  sentence that names a counter the fixture does not isolate. Able-to-fail: the round-80 isolated-fixture
  harness (`python3 -B .ufo/waves/round-80/c80_ledger_fixtures.py --root <tree> --json`) reports
  `killed == 3` with k3 `wrong_kind`, k4 cheap-note and k5 `symlinks` each killed by its own fixture and
  the cheap-note fixture red through `undisclosed == 1`; a harness that counts a mutant killed by
  another fixture's red, or that reports cheap-note's red as `malformed`, fails this clause. Receipts:
  `.ufo/waves/round-80/controls/c80-cheap-note.txt` (the cheap-note run) and the harness's `--json`
  document — `[pending receipt at draft time; the clause is the L1's to land only with those bytes
  committed]`.
