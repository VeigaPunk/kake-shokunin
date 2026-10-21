# AttackCase28 — fixture `28-ledger-row-numeric-spelling` (operability)

Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD == candidate). Seat scratch
`/fast/scratch/hyaku/kake-r27/AttackCase28` (TMPDIR/HOME set there; no /tmp, no /dev/shm).
Source read-only; only scratch fixture copies mutated. No tool installs. No production edits.

## Attacked item (exact)

- Gate `scripts/citing_set.py` sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`
- Runner `scripts/citing_set_selftest.py` sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`
- Fixture `scripts/fixtures/citing-set/28-ledger-row-numeric-spelling/`: `ledger.json` `ebf83cb3…`,
  `population.json` `b740227d…`, `expected.json` `a2def88b…`, `corpus/knowledge/mirror-pitfalls.md` `0159fbf2…`
- All five worktree files are byte-identical to `git show ac46a747…:<path>` (sha256 of candidate blob vs
  worktree file). `git status --porcelain -- scripts/` = empty after all runs.

## Independent derivation (declared BEFORE reading any gate output)

Population rows `S001`, `S0001`; ledger pairs `{row:"S0001", file:"corpus/knowledge/mirror-pitfalls.md"}`;
one corpus file. Independent scan of the corpus text (own regex, not gate code): literal tokens `["S001"]`,
ranges `[]`, no other `S<digits>` substring. Gate semantics from source: `S<digits>` ids compare numerically
(`id_key` → `("n",1)` for both `S001` and `S0001`); population collapses to one key, display `S001`.
⇒ citing set `{("n",1) × corpus/knowledge/mirror-pitfalls.md}` (1 pair); ledger key identical; one occurrence
⇒ no duplicate; no range/input error.
**Declared expectation: exit 0, finding-id multiset `[]`** (agrees with `expected.json`: exit 0, `[]`).

## Run A — real frozen gate CLI, scratch copy, unrelated cwd

`cd /fast/scratch && TMPDIR=$SEAT/tmp HOME=$SEAT/home python3 -B <repo>/scripts/citing_set.py --root
$SEAT/case28-pristine --population population.json --ledger ledger.json --json`
stdout `{"verdict":"clean","citingPairs":1,"ledgerPairs":1,"findings":[],"populationRows":2,"corpusFiles":1,
"outsidePopulation":0,"source":"working-tree","revision":null}` — exit **0**. Derived = observed;
`expected.json` agrees. **No disagreement.** Identity (not just tally): citingPairs=1 / ledgerPairs=1 /
outsidePopulation=0 ⇒ the single citation `S001` was enumerated and matched to the ledger pair
`S0001`/`corpus/knowledge/mirror-pitfalls.md` (path string identical, no `./` prefix).

## Run B — consumer runner, scratch copy

`python3 -B scripts/citing_set_selftest.py --root $SEAT --fixtures $SEAT/fixtures --gate <frozen gate>
--tmpdir $SEAT/tmp` → exit 0, `verdict clean`, `cases 1`, `failed 0`, case `ok:true`
(`expected {exit 0, findings []}` = `actual {exit 0, findings []}`).

## Run C — consumer runner, live repo fixture suite (read-only)

Same frozen gate/runner sha256 → exit 0, `verdict clean`, `cases 29`, `failed 0`, `passed true`; case row
`{"case":"28-ledger-row-numeric-spelling","ok":true,"expected":{"exit":0,"findings":[]},
"actual":{"exit":0,"verdict":"clean","findings":[]}}`.

## Mutation (ONE change, declared before running)

`case28-pristine` → `case28-mutant`; `ledger.json` pair `row`: `"S0001"` → `"S002"` (pristine `ebf83cb3…`
→ mutant `5128938c…`; corpus/population/expected untouched).
**Declared expected consequence:** citing set unchanged; ledger becomes `{("n",2) × mirror-pitfalls.md}` ⇒ one
`unadjudicated_citing_pair` (row `S001`) **and** one `ledger_pair_not_cited` (row `2`; key `("n",2)` is not in
the population), both file `corpus/knowledge/mirror-pitfalls.md` ⇒ verdict `failed`, **exit 1**, sorted ids
`["ledger_pair_not_cited","unadjudicated_citing_pair"]`.

Run D (same CLI/cwd, `--root $SEAT/case28-mutant`): stdout `{"verdict":"failed","citingPairs":1,
"ledgerPairs":1,"findings":[{"id":"ledger_pair_not_cited","row":"2","file":"corpus/knowledge/mirror-pitfalls.md"},
{"id":"unadjudicated_citing_pair","row":"S001","file":"corpus/knowledge/mirror-pitfalls.md"}],
"populationRows":2,"corpusFiles":1,"outsidePopulation":0}` — exit **1**. Observed == declared.
Run E (consumer runner over the mutant) → exit 1, `failed 1`, reason `exit mismatch: expected 0, observed 1`.
⇒ the clean result of Run A is **not vacuous**: row identity genuinely participates in the pair key (a
file-only matcher would still report clean), and the numeric-spelling match is not over-broad.

## Findings (severity ordered)

1. **Low — finding-level row identity is lossy; ledger spelling never reported.** Run D: ledger row literally
   `S002` is reported `row:"2"` (bare number, no `S`, no padding); `unadjudicated_citing_pair` is reported
   `row:"S001"` — the population's first spelling, not the ledger's `S0001`. Cause: findings render
   `display.get(key)` with fallback `str(key[1])`, discarding the ledger's literal row id. Verdict/exit are
   correct, but a consumer cannot round-trip a finding to the ledger row it names. Oracle blindness: the
   runner compares **only exit + sorted finding ids**, and this case's `expected.json` is `{"exit":0,
   "findings":[]}` ⇒ no row/file identity is asserted anywhere for case 28; a row-rendering regression would
   still pass 29/29.
2. **Informational — population row count is pre-collapse.** Run A/D report `populationRows:2` although the
   two rows are one numeric row under the gate's own equivalence rule. No finding flags the collapse, so a
   reader of `populationRows` would believe two distinct rows exist.
3. **Informational — fixture 28 does discriminate exact-string vs numeric comparison.** Under exact-string
   comparison the ledger key `S0001` ≠ citing key `S001`, which yields `ledger_pair_not_cited` and exit 1 ≠
   the frozen expectation; the case is a real oracle for the numeric-spelling rule, not a shape-only green.

## Discrepancies

None between independent derivation, `expected.json`, Run A/B/C outputs, and Run D/E declared-vs-observed.
Row/file identity on the pristine path agrees (paths identical as written).

## Residual risk / verification gaps

- Only **working-tree** source mode exercised here; `--revision` is not applicable to this fixture layout
  (its `corpus/knowledge` is not at the repo-relative path the `git ls-tree` source enumerates), so the
  gate's `--revision` path stays untested by this case.
- Padding equivalence rests on one observed direction (cited `S001` matched ledger `S0001`); further
  spellings (e.g. `S0000001`) were not executed — only ONE input change was in scope.
- Row-rendering defects (finding 1) lie outside the fixture oracle's comparison surface; the 29-case suite
  is blind to them.
- Out of this seat's scope: `count_c1.py`, `c2_count.py`, C1/C2 tallies, W1 source adjudications, r26 material.
