# MutHeuristic — round-92 mutation test (C2 instrument and C2 counter)

VERDICT: C2's frozen counter scores the shipped tool `met=true` and kills 11 of 24
single-clause tool mutants, but its `met` does not establish conformance to contract v1 —
13 tool mutants survive it, 9 hand-built subjects that violate named contract clauses read
`met=true`, and 12 of 16 counter mutants survive, three of them at the `met`-conjunct level.
C2 as an *instrument-conformance* claim is therefore narrower than its wording; C2 as a
*capability* claim (the tool decides the 28 worked cases and 120 generated cases as the
reference does) holds on the bytes I measured.

## What I ran

| Step | Command | Exit | Receipt |
|---|---|---|---|
| baseline (shipped tool as a scratch commit) | `python3 -B .ufo/waves/round-92/c92_heuristic.py --root <clone> --revision ee82c5bb --work <scratch>` | 0, `hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true` | `w1/MutHeuristic/pristine-shipped.txt` |
| 24 tool mutants | same counter, one commit per mutant in a scratch clone | 11× exit 1 `met=false`; 13× exit 0 `met=true` | `w1/MutHeuristic/tool-mutants.txt`, `tool-matrix.json`, `tool-detail.json` |
| 16 counter mutants | `python3 -B <mutant> --root <clone> --revision <rev> --work <dir>` | 2× exit 2 (reference drift), 2× exit 1, 12× exit 0 `met=true` | `w1/MutHeuristic/counter-mutants.txt`, `counter-matrix.json`, `cm16-no-sandbox.txt` |
| 13 witness subjects | pristine counter over each subject revision | 4× exit 1 `met=false`, 9× exit 0 `met=true` | `w1/MutHeuristic/subjects.txt`, `pristine-subjects.json` |

Setup: `S=/fast/scratch/hyaku/kake-r92/MutHeuristic`; one clone
(`git clone -q --shared LANE $S/clone`, `checkout -q --detach a5640ca0…`,
`update-ref refs/heads/master $(git -C LANE rev-parse refs/heads/master)`); toplevel
asserted equal to `$S/clone` before every commit; every commit carried
`-c user.name=mut-fixture -c user.email=mut@fixture.invalid`. LANE was never staged,
committed, checked out or edited. Shipped tool sha256
`7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c` (re-checked at report
time, unchanged); frozen counter sha256
`8f356c8d4a8dea5de80f97f61ba6e8147b0e60b9e356cf651df28b0db1405f3f`.

## Findings

**F1 — 13 of 24 single-clause tool mutants survive the frozen counter.** Each changes one
contract clause; the counter reads `hand=28/28 generated=120/120 met=true` for every one.
Survivors: clause 9 (Vary member equality→substring), clause 4 (quoted delta-seconds
accepted), clause 2 (NUL accepted), clause 3 (non-bool `shared`), clause 3 (negative
`now`), clause 3 (status 0..999), clause 3 (`true` accepted as int), Input (extra
top-level key), Input (extra `stored` key), clause 2 (no value trim), clause 2 (trim set
widened), clause 5 (signed `Date`), clause 8 (`not-storable` decided before validation).
Each is a missing case class; the full per-mutant table, sha256, commit and detector is
`w1/MutHeuristic/tool-mutants.txt`. The 11 killed mutants are killed by named hand cases
(10) and the generated population (1 — T01, status 204).

**F2 — nine contract-violating subjects read `met=true` under the pristine counter.**
These are not mutants of the tool but independent subjects built from the contract text
(`subjects.txt` carries each one-clause diff and its reading): N6 non-bool `shared`, N7
negative `now`, N8 status 99/600-class bounds, N9 trim-everything, N10 `Vary: Accept-*`
treated as `*`, N11 NUL accepted, N12 quoted delta accepted, N13 clause-8 ordering
violated, N14 extra top-level key accepted — all `met=true`, exit 0. `met=true` therefore
means "agrees with 28 hand cases + 120 generated cases + 5 forgeries", not "implements
contract v1".

**F3 — the counter's reference drifts from the contract on quoted delta-seconds, and the
drift is unobservable.** Contract clause 4: "A delta-seconds argument (`max-age`,
`s-maxage`) must be a bare non-negative decimal integer: a quoted or signed form is a
refusal." The reference strips the quotes before the digit check:

```
$ python3 - <<'PY'   # reference() imported from the frozen counter
inp = {"stored": {"status": 200, "headers": {"Date": "1000000", "Cache-Control": 'max-age="600"'}}, "now": 1000000}
print(reference(inp))
PY
{'decision': 'explicit', 'lifetime': 600, 'heuristic': False}

$ echo '{"stored": {"status": 200, "headers": {"Date": "1000000", "Cache-Control": "max-age=\"600\""}}, "now": 1000000}' \
  | python3 scripts/heuristic_freshness.py ; echo exit=$?
invalid_input: max-age argument is not a bare non-negative decimal integer
exit=1
```

No hand case and no generated case carries a quoted argument, so the counter's exit-2
"reference drift" self-check never fires. The counter docstring's claim that "an
oracle/contract drift exits 2 rather than passing silently" is false for this class. The
tool is right and the oracle is wrong here.

**F4 — the anti-table conjunct has no frozen subject.** The anti-table scans only
`a.candidate`; the five frozen forgeries are never scanned, and none embeds a hand-case
digest or a forgery stem. A subject that behaves correctly but carries `# neg-status-table`
(N2) or a 16-hex hand-case digest (N3) is refused by the pristine counter
(`anti_table=hit`, `met=false`, exit 1) and admitted by counter mutant CM11 (same subject,
`anti_table=hit`, `met=true`, exit 0). The counter docstring's claim that "the anti-table
conjunct is exercised by a frozen subject rather than being an unfalsified assertion" is
falsified — the only witnesses are mine. Receipt: `counter-mutants.txt`, `counter-matrix.json`.

**F5 — the `PINS_SHA` blob check is load-bearing and unwitnessed.** A revision whose
`frozen/c2-population.sha256` gains one trailing comment line reads `population=drift`,
`met=false`, exit 1 under the pristine counter; under CM12 (`pins_ok = not drift`) the same
revision reads `population=ok`, `met=true`, exit 0. No frozen control exercises this path.

**F6 — the C2 counter does not pin its own blob.** C1's counter carries a `self` conjunct
against `frozen/c1-self.sha256`; C2's has none. CM13 (`met = True or (…)`) reads `met=true`
on the shipped tool *and* on N4-cap43200 where the real counts are `hand=25/28
generated=102/120` (pristine: `met=false`, exit 1). Nothing downstream can distinguish a
mutated C2 counter from the frozen one.

**F7 — the three sandbox guards are mutually redundant for the frozen population.**
Removing the `open` denial alone (CM09) and removing the import allowlist denial alone
(CM10) each still refuse all five forgeries (`forgeries_refused=5/5`, `met=true`): the
import allowlist blocks the counter module's own `argparse`/`shutil`/`subprocess` imports,
and the `open` denial blocks the counter-blob and pins reads. The process guard (CM15) is
exercised by no forgery. Only bypassing the sandbox wholesale (CM16) admits
`neg-oracle-import.py` and `neg-pin-reader.py` (`forgeries_refused=3/5`, `met=false`,
exit 1). The population cannot attribute a refusal to a guard, so the "refused by
execution" evidence is weaker than it reads.

**F8 — `KEYS_OUT` is dead code in the frozen counter.** Defined at
`.ufo/waves/round-92/c92_heuristic.py:47`, never read; output-key exactness comes from
`got == expected`. CM14 (emptied constant) is indistinguishable.

**F9 — hand-case coverage of the heuristically-cacheable set is 2 of 12.** Only 404 and 500
are hand cases; a wrong set entry for 204 is caught only because the generated population
draws status 204 (T01, CM07: `generated=115/120`, exit 1). 206/300/301/308/405/410/414/501
are covered only by the generator's fixed status list.

**C1 counter probe.** `sha256 .ufo/waves/round-92/c92_defects.py` =
`9ba796212cf8b0cca9251e0208962609fc2b9a224b0f25610aa2c7f346f13195` =
`frozen/c1-self.sha256`; at the freeze revision it reads `open=3 closed=0 battery=hit
differential=fail self=ok met=false`, exit 1, and at `e143faff` (pin file absent) `self=hit`
— the pin is live. Limits: the pin is an internal consistency check (a mutant that also
rewrites the pin file reads `self=ok`), and item A's execution binding could not be
mutation-tested because `integration/mutation-tip.*` did not exist during this seat's run,
so every item-A predicate path returns "mutation receipt absent" at the freeze revision.

## Surviving-mutant clause list (tool)

clause 9 Vary-member equality · clause 4 delta-seconds bareness · clause 2 CR/LF/NUL ·
clause 3 `shared` type · clause 3 `now` bound · clause 3 status bounds · clause 3
bool-is-not-int · Input extra top-level key · Input extra `stored` key · clause 2 value
trimming · clause 5 decimal-integer form · clause 8 validate-before-decide.

## Honest limits

- Every verdict is the frozen counter's own output on committed scratch bytes; nothing here
  is an admission and nothing changes the round's claim predicate or the frozen files.
- The witness subjects (N2–N14) are mine, derived from the contract text; they are not the
  lane's deliverables and were never written into LANE outside this directory.
- Scratch was deleted after the receipts were copied; the scratch revisions in `revs.json`
  are therefore historical identifiers, and the reproducible form is the diff text in
  `tool-mutants.txt` / `counter-mutants.txt` / `subjects.txt`.
- No network GET, no tool install, no writes outside
  `.ufo/waves/round-92/w1/MutHeuristic/`.

## Deliverables

`.ufo/waves/round-92/w1/MutHeuristic/`: `Mutations.md`, `tool-mutants.txt`,
`counter-mutants.txt`, `subjects.txt`, `tool-matrix.json`, `tool-detail.json`,
`counter-matrix.json`, `pristine-subjects.json`, `pristine-shipped.txt`,
`cm16-no-sandbox.txt`, `tool-mutant-revs.json`, `revs.json`.
