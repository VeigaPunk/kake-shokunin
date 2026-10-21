# AttackCase06 — consumer fixture `06-to-range-omission` (operability, r27-fresh-falsification)

Seat: `KakeR27.AttackCase06` (leaf reviewer, read-only source seat). Axis: **operability**. Date: 2026-10-21.
Attacked item: fixture `scripts/fixtures/citing-set/06-to-range-omission` (producer `BuildFixtures`) consumed by the frozen C2 gate `scripts/citing_set.py` (producer `BuildGate`).
Verdict: **no defect found in fixture 06**; fixture expectation, gate behaviour and frozen consumer runner agree on exit **1** and finding multiset **`{unadjudicated_citing_pair}` ×1** (row `S004`, file `corpus/knowledge/speedrun-pipeline.md`).

## 0. Authority / identity checks (all Git reads pinned to the candidate hash)

- Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; every source read used the explicit hash, never bare HEAD.
- `git show ac46a747:scripts/citing_set.py | sha256sum` = `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` = the `sourceFiles` entry in `frozen-candidate.json`; working-tree copy of the same file hashes identically → measured source is the candidate blob, not a later edit.
- Fixture digests equal the `frozen-candidate.json` entries: `expected.json 49d7286d…`, `population.json f04a4f37…`, `ledger.json 79cf6ca0…`, `corpus/knowledge/speedrun-pipeline.md 4964961c…` (re-verified after the probe: unchanged).
- Interpreter: system `python3` 3.14.8, `-B`. No tool install/upgrade performed (none needed). Scratch confined to `/fast/scratch/hyaku/kake-r27/AttackCase06/` with `TMPDIR`/`HOME` set there; no `/tmp`, `/dev/shm`.

## 1. Independent derivation (before running the gate; derived from input + `contract.json` only)

- `contract.json` C1 denominator grammar: "literal S +3-or-more digits and ranges with S at both ends separated by hyphen/en-dash/em-dash/`..`/to/through".
- Input facts: population rows = `S001..S006` (6); ledger pairs = `S001,S002,S003,S005,S006` for `corpus/knowledge/speedrun-pipeline.md` (5) → **`S004` is the only ledger gap**. Corpus text contains exactly one id-bearing phrase, `registry rows S001 to S006`; the only literal tokens are the two endpoints `S001`,`S006`.
- Derivation: the `to` range spans `S001..S006`, so the enumerated citing set is 6 pairs in that one file. Ledger covers 5 → missing pair `(S004, corpus/knowledge/speedrun-pipeline.md)`. No ledger row lies outside the enumerated set, no duplicate ledger row, no descending/oversize range, inputs well-formed.
- **Independently declared expected result: exit 1, findings multiset `{unadjudicated_citing_pair ×1}` with row `S004`, file `corpus/knowledge/speedrun-pipeline.md`; `citingPairs=6`, `ledgerPairs=5`.**
- `expected.json` (read after the derivation) = `{"exit":1,"findings":["unadjudicated_citing_pair"]}` → **agrees** on exit and on the id multiset. `expected.json` carries no row/file, so identity was cross-checked against the fixture's own input (the single ledger gap is `S004`; the single corpus file is `corpus/knowledge/speedrun-pipeline.md`): no disagreement on row/file identity.

## 2. Probe 1 — real frozen gate CLI on a scratch copy, unrelated cwd

- Copy: fixture inputs copied to `/fast/scratch/hyaku/kake-r27/AttackCase06/caseA/` (`expected.json` removed from the gate input root); gate materialised from the candidate blob to `…/AttackCase06/gate/citing_set.py`.
- Command (cwd `/fast/scratch/hyaku/kake-r27/AttackCase06/run`, unrelated to the repo): `python3 -B …/gate/citing_set.py --root …/AttackCase06/caseA --population population.json --ledger ledger.json --json`
- Actual: **exit 1**, stderr 0 bytes, stdout:
  `{"verdict":"failed","citingPairs":6,"ledgerPairs":5,"findings":[{"id":"unadjudicated_citing_pair","row":"S004","file":"corpus/knowledge/speedrun-pipeline.md"}],"populationRows":6,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}`
- Two independent runs produced byte-identical stdout (deterministic). Observed == derived == `expected.json`.

## 3. Probe 2 — ONE causally meaningful input change (declared before running)

- Change (scratch corpus copy only): `registry rows S001 to S006` → `registry rows S002 to S005` (mutated file sha256 `e042df3c…`; live fixture untouched). Ledger, population and the separator word `to` are unchanged, so the only causal variable is the range endpoints.
- **Independently declared expected consequence:** range `S002..S005` expands to 4 population rows → `citingPairs=4`, `ledgerPairs=5`; `S004` remains a range-interior row absent from the ledger → `unadjudicated_citing_pair` (row `S004`); ledger rows `S001` and `S006` are now outside the enumerated citing set → `ledger_pair_not_cited` ×2 (rows `S001`, `S006`); exit **1**, verdict `failed`; `outsidePopulation=0` (both are population rows).
- Actual: **exit 1**, stderr 0 bytes, stdout exactly `findings = [{ledger_pair_not_cited,S001},{ledger_pair_not_cited,S006},{unadjudicated_citing_pair,S004}]`, `citingPairs=4`, `ledgerPairs=5`, `outsidePopulation=0`, `corpusFiles=1`.
- **Match, with no slack.** Falsification value: a gate that ignored the `to` separator would have produced 3×`ledger_pair_not_cited` and **no** `unadjudicated_citing_pair` — the observed run rules that out. A gate with an off-by-one on either endpoint would have produced 5 or 3 citing pairs, or flagged `S002`/`S005`; the observed 4/row-set rules that out. The `unadjudicated` finding tracks the ledger gap, not the endpoint text (row stayed `S004` across both runs).

## 4. Supplementary probes (same input, different execution mode / consumer runner)

- Git-revision mode: same fixture content committed in a scratch repo (`git init` + commit `f8e05131…`), `python3 -B …/gate/citing_set.py --root …/gitcase --revision HEAD --population population.json --ledger ledger.json --json` → **exit 1**, `source:"git"`, `citingPairs=6`, `ledgerPairs=5`, identical single finding (`unadjudicated_citing_pair`, row `S004`, same file). Working-tree and Git modes agree on identity — no mode-dependent rerouting.
- Frozen consumer runner (real selftest, candidate tree exported read-only to `…/AttackCase06/selftest-root`): `python3 -B scripts/citing_set_selftest.py --root …/selftest-root` → **exit 0**, stdout `{"schema":"kake-citing-set-selftest-v1","verdict":"clean","passed":true,"cases":29,"failed":0,"failedCases":0}` with `06-to-range-omission` among `caseNames`. So the fixture passes through the real runner, not only through a hand-typed command.
- Measurement hygiene note: an earlier combined shell chain printed `SELFTEST_EXIT=1`; that number was an artefact of my own `$?` capture inside a busy temporary shell, not a gate/selftest failure. Re-measured in an isolated invocation the same command returns **exit 0** with the clean summary above; the earlier value is retracted, not counted as evidence.

## 5. Discrepancies, residual risk, verification gaps

- No disagreement found between: independent derivation, `expected.json`, real gate CLI (working-tree mode), real gate CLI (git mode), and the frozen selftest runner — for exit code, id multiset, and row/file identity.
- Residual risks (not fixture-06 defects, stated for the L1): (a) fixture 06 exercises only a **single** finding, so finding *multiplicity* is untested by this case (fixtures 03/19/23/24 carry multiplicity); (b) `expected.json` schema carries ids only, so row/file identity is not machine-checked by the runner — it was checked here by hand against the fixture input; (c) the gate's own `--revision` path was exercised on a fresh scratch repo, not on the kake repo's real corpus tree, so corpus-wide behaviour of fixture 06 remains unobserved (out of this case's scope).
- Verification gaps: no build/lint/formatter run (forbidden in this wave); no production edit, no commit, no fixture or source mutation — the only mutation was on the scratch copy under `/fast/scratch/hyaku/kake-r27/AttackCase06/`.
- Installs: none. No `pacman`, `uv tool install`, `cargo`, `npm`.
