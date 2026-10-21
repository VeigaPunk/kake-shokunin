# AttackCase20 — fixture `20-range-with-population-gap` (operability, r27 fresh falsification)

Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD). Source read-only; only fixture
inputs mutated, on scratch copies under `/fast/scratch/hyaku/kake-r27/AttackCase20/`.
No production edit, no tracked-file write, no commit (tracked `git status` clean at end).

## 0. Identity of what was attacked (before any run)
`git hash-object` (live) vs `git rev-parse ac46a74:<path>` (candidate blob) — all MATCH:
`scripts/citing_set.py` `3a361a00…c228`; `scripts/citing_set_selftest.py` `3c167895…a1c`;
fixture `corpus/knowledge/ops-automation.md` `dc134c4d…c96d`; `expected.json` `a2def88b…16e9`;
`ledger.json` `0d59baab…4791`; `population.json` `8bc2eb88…c526` — same values as
`frozen-candidate.json` for this case. Scratch `case20-pristine/` byte-identical to live (sha256 both sides).

## 1. Independently derived expectation (declared BEFORE running the gate)
Basis: contract grammar (`contract.json` C1.denominator/gateInterface) — literal `S`+≥3 digits and
ranges `S…<sep>S…` with sep ∈ `-`/en-dash/em-dash/`..`/`to`/`through`, **intersected with the
population**; ledger pair = (row, file); finding ids `unadjudicated_citing_pair`,
`ledger_pair_not_cited`, `ledger_duplicate_pair`.
Input facts read first (not gate output):
- corpus = 1 file `corpus/knowledge/ops-automation.md`; its only citation is header range `S001-S007`
  (literals `S001`,`S007` subsumed by it);
- `population.json` rows = S001, S002, S005, S006, S007 → **gap** S003, S004;
- range expands to 7 rows; in-population members = those 5; S003/S004 fall outside the population ⇒ not obligations;
- `ledger.json` adjudicates exactly those 5 rows against `corpus/knowledge/ops-automation.md`.

**Derived: exit 0, finding-id multiset = `[]` (empty).** `expected.json` = `{"exit":0,"findings":[]}`
→ **agreement, no disagreement.**
Independent scanner (mine, not the gate's code — `independent_derive.py` in scratch):
`citingCount 5, outsideCount 2 [S003,S004], ledgerCount 5, missing [], ledger_not_cited [], derivedExit 0`.

## 2. Real frozen gate on the scratch copy, unrelated cwd
`cd /fast/scratch/hyaku/kake-r27/AttackCase20 && TMPDIR=$PWD python3 -B <repo>/scripts/citing_set.py
--root $PWD/case20-pristine --population population.json --ledger ledger.json --json`
stdout: `verdict clean`, `citingPairs 5`, `ledgerPairs 5`, `findings []`, `populationRows 5`,
`corpusFiles 1`, `outsidePopulation 2`, `source working-tree`; **exit 0** — matches §1.
`outsidePopulation 2` is decisive: the range *was* expanded (S003/S004 seen, then dropped by the
population gap), so the clean exit is not "range ignored".

## 3. Mutation (ONE causally meaningful input change) — declared BEFORE running
Change: scratch `case20-mutant/population.json` gains row `S003` (gap closed; no corpus/ledger byte
touched). population sha256 `8bc2eb88…c526` (pristine) → `f4b3dca8…67b5e` (mutant).
**Declared expected consequence:** range `S001-S007` now enumerates S003, in-population but
unadjudicated ⇒ exactly one finding `unadjudicated_citing_pair`, **row `S003`, file
`corpus/knowledge/ops-automation.md`**; exit **1**; no `ledger_pair_not_cited` (all 5 ledger pairs
stay cited); no duplicate; `citingPairs` 5→6, `outsidePopulation` 2→1.
Actual (same command, `--root …/case20-mutant`): `verdict failed`, `citingPairs 6`, `ledgerPairs 5`,
`populationRows 6`, `outsidePopulation 1`, `findings [{"id":"unadjudicated_citing_pair","row":"S003",
"file":"corpus/knowledge/ops-automation.md"}]`, **exit 1**. Independently re-derived expectation
matched the observed outcome exactly → row **and** file identity verified, not only the id tally.

## 4. Consumer probes (real selftest `scripts/citing_set_selftest.py`)
- Pristine fixture copy (29 cases): `verdict clean`, `passed true`, `failed 0`, exit 0; case 20 record
  expected `{exit 0, findings []}` / actual `{exit 0, verdict clean, findings []}`, `ok true`.
- Mutant fixture copy (only case 20 = §3 mutant): `verdict failed`, `failed 1`, exit 1; failure record
  `case 20-range-with-population-gap`, `reason "exit mismatch: expected 0, observed 1"`, actual
  findings `["unadjudicated_citing_pair"]` ⇒ consumer is input-sensitive and does not echo `expected.json`.

## 5. Source-mode parity probe
Fixture committed in a scratch git repo, gate run with `--revision <sha>`: `source git`,
`verdict clean`, `citingPairs 5`, `ledgerPairs 5`, `findings []`, exit 0 — identical to working-tree mode.

## 6. Findings / discrepancies
1. **Fixture-oracle coverage gap (operability, severity low-medium; not a gate defect).** The fixture
   interface compares only *exit + sorted finding-id multiset* (`citing_set_selftest.py` `finding_ids()`
   keeps `item["id"]` only; `contract.json` fixtureInterface agrees). A gate emitting the wrong
   `row`/`file` for `unadjudicated_citing_pair` would still pass every fixture, including this one.
   My §3 probe supplies the row/file evidence the suite does not assert. Recommendation (non-blocking,
   no source change in this wave): have the runner also compare row/file when `expected.json` carries them.
2. **No disagreement in this case.** Independently derived exit/finding multiset (§1) = `expected.json`
   = gate output.
3. **Residual risk.** Only S003 was probed as gap-closing row (one-change bound); S004 is symmetric in
   the code path but not independently observed. `load_population` reads `id` only, so `kind`/`tier`
   differences could not change the outcome — asserted from source reading, not run.
4. **Not assessable here (out of scope, stated not claimed):** HTTP provenance, source semantics and
   freshness of the fixture corpus doc belong to C1 seats, not to this fixture's gate operability.
5. No policy stop, no network, no install, no system change was needed or performed.

## 7. Conclusion
Fixture `20-range-with-population-gap` behaves exactly as independently derived: exit 0 with empty
finding multiset, `expected.json` correct, and one population change flips it to exit 1 with the
precisely identified row/file. Operability of this consumer fixture: **supported by run evidence**,
with 6.1 recorded as a coverage limit of the fixture oracle.
