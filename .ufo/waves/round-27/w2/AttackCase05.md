# AttackCase05 — fresh falsification of consumer fixture `05-ascii-dotdot-range-omission`

Seat: leaf reviewer (no dispatch). Axis: **operability**. Milestone: r27-fresh-falsification.
Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (`HEAD` == candidate; `git status --porcelain scripts/` empty;
gate blob `352a471abec08daa56a0fb7ef23fe78f2930d773` == `ac46a74:scripts/citing_set.py`; runner blob
`c69b09b2e47f4115aa4e8ff286aa7cfe0e171a64` == `ac46a74:scripts/citing_set_selftest.py`; gate file sha256
`3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`, runner sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`).
Contract: `.ufo/waves/round-27/contract.json` (C2 gate/fixture interface).
**Attacked item** (read-only in repo): `scripts/fixtures/citing-set/05-ascii-dotdot-range-omission/` →
`population.json` (rows S001–S006), `ledger.json` (pairs S001,S002,S004,S005,S006, all on
`corpus/knowledge/drift-detection.md`), `corpus/knowledge/drift-detection.md` (single citation construct
`source: S001..S006 …`), `expected.json` (`exit 1`, `findings ["unadjudicated_citing_pair"]`).
Input sha256 (all == candidate blobs; live fixture untouched): corpus `570b9c54662cd115bcab7f538e6d0a8d3158f4fc504365114d043a4524ab1574`, population `f04a4f37f256034f70f29b7b0aade3d87a498b42a01a85bc454d51ddc3b272f6`,
ledger `1dfc93cc24952d4f40c91e256d7a618d707780c0235b173b8104dbbb2dc6b172`, expected `49d7286dd34a00ce88a31d473272e589cb5542e76d60505cd9591437ee353e81`.

## Independent derivation (declared BEFORE any gate run)

Grounding = contract C2 semantics (separators `-`,`–`,`—`,`..`,`to`,`through`; ascending; span ≤ 200; population
rows only; missing citing pair ⇒ `unadjudicated_citing_pair`; ledger pair outside the citing set ⇒
`ledger_pair_not_cited`) + the fixture bytes. My own sweeps (regexes written independently of the gate source):
- literal tokens → `S001`, `S006` (both population rows); range sweep → exactly one range `S001..S006` (ASCII
  double-dot) ⇒ expanded citing set S001–S006 ⇒ **citingPairs 6**, `outsidePopulation 0`, no `citation_range_invalid`
  (ascending, span 5), no `input_invalid`;
- ledger = 5 distinct pairs, no duplicate ⇒ `ledgerPairs 5`, no `ledger_duplicate_pair`;
- citing minus ledger = {S003} ⇒ exactly one finding, row **S003**, file `corpus/knowledge/drift-detection.md`;
  every ledger pair is inside the citing set ⇒ no `ledger_pair_not_cited`.
- **Declared expected: exit 1, verdict `failed`, id multiset `{unadjudicated_citing_pair}` ×1**, row/file
  `S003` / `corpus/knowledge/drift-detection.md`.
- Honest disclosure: the fixture's `expected.json` was read during input inspection; the derivation is driven by input
  bytes + contract grammar and additionally fixes row/file identity and the `citingPairs` counts, which
  `expected.json` lacks; Probe C declares an expectation *different* from `expected.json`, so it cannot be parroting.

## Probe A — real frozen gate CLI, scratch copy, unrelated cwd

Declared expected: as derived (exit 1, one `unadjudicated_citing_pair`, row S003, file corpus/knowledge/drift-detection.md).
Scratch copy `/fast/scratch/hyaku/kake-r27/AttackCase05/base` (copy of live fixture; corpus bytes identical `570b9c54…`).
```
cd /fast/scratch/hyaku/kake-r27/AttackCase05/run   # unrelated cwd
TMPDIR=/fast/scratch/hyaku/kake-r27/AttackCase05/tmp python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --root /fast/scratch/hyaku/kake-r27/AttackCase05/base --population population.json --ledger ledger.json --json
```
stdout `{"verdict":"failed","citingPairs":6,"ledgerPairs":5,"findings":[{"id":"unadjudicated_citing_pair","row":"S003",
"file":"corpus/knowledge/drift-detection.md"}],"populationRows":6,"corpusFiles":1,"outsidePopulation":0,
"source":"working-tree","revision":null}` → **EXIT=1**, stderr 0 bytes.
Id tally, exit **and row/file identity** equal my declared expectation and `expected.json`. A separate
mini-implementation of the contract semantics (not the gate) independently reproduced `citingPairs=6,
ledgerPairs=5, ids=[unadjudicated_citing_pair/S003/corpus/knowledge/drift-detection.md], exit=1`.

## Probe B — real consumer runner (fixture suite) over the live fixture set

Declared expected: case `05-ascii-dotdot-range-omission` ok; suite green; ≥12 cases.
`TMPDIR=… python3 -B scripts/citing_set_selftest.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tmpdir /fast/scratch/hyaku/kake-r27/AttackCase05/tmp --min-cases 12 --json`
→ `{"schema":"kake-citing-set-selftest-v1","verdict":"clean","passed":true,"cases":29,"failed":0,"failedCases":0,
"contractMinimumCases":12,"meetsContractMinimum":true}` **EXIT=0**; case 05 `ok:true`, expected
`exit 1 / ["unadjudicated_citing_pair"]` == actual `exit 1 / ["unadjudicated_citing_pair"]`.

## Probe C — ONE causally meaningful input change (scratch copy only)

Change (one file, one construct): in `/fast/scratch/hyaku/kake-r27/AttackCase05/mut/corpus/knowledge/drift-detection.md`
replace the ASCII double-dot range `S001..S006` with the non-range list `S001, S006`. Mutant corpus sha256
`6e9bd5252066317cc5f0b9eb62143e99ec9471e0e07debcb3e2706fed37150a7`; pristine `570b9c54…`; population/ledger bytes unchanged.
**Declared expected (before running): exit 1, verdict `failed`, id multiset `{ledger_pair_not_cited} ×3`
(rows S002, S004, S005; file corpus/knowledge/drift-detection.md), `citingPairs 2`, `ledgerPairs 5`, and NO
`unadjudicated_citing_pair`** — `,` is not a declared separator, so the range stops expanding: only the literals
S001/S006 remain citing pairs, the three ledger-only rows become uncited, and S003 stops being an obligation.
Actual: `{"verdict":"failed","citingPairs":2,"ledgerPairs":5,"findings":[{"id":"ledger_pair_not_cited","row":"S002",…},
{"id":"ledger_pair_not_cited","row":"S004",…},{"id":"ledger_pair_not_cited","row":"S005",…}],"populationRows":6,
"corpusFiles":1,"outsidePopulation":0}` **EXIT=1** — exactly as declared; my mini-implementation predicted the
identical multiset and row/file detail.
⇒ the fixture's red state is caused solely by the ASCII `..` range expansion, and the oracle discriminates: a
gate without `..` support would emit 3×`ledger_pair_not_cited` and fail this fixture.

## Discrepancies vs `expected.json`
None. Exit code, finding-id multiset (multiplicity 1) and row/file identity agree with the independently derived
expectation and with the frozen `expected.json`.

## Author-side findings (this seat)
- **F1 (low, oracle-strength gap — contract-compliant, not a breach):** `expected.json` stores finding **ids only**
  and the runner compares exit + sorted id multiset only (`scripts/citing_set_selftest.py` `finding_ids()`/`run_case()`);
  `row`, `file`, `citingPairs`, `ledgerPairs` are never asserted. A regression mis-attributing the finding's row or
  file (e.g. S002 instead of S003), or reporting right ids with wrong counts, passes all 29 cases. The current
  candidate is correct on fixture 05 (Probe A: row `S003`, file `corpus/knowledge/drift-detection.md`), so this is a
  latent suite weakness, not a live defect. Fixture 05's expected multiset is byte-identical to 04/06/07/25, so
  id-tally alone cannot name the separator — only Probe C shows `..` is load-bearing.
- **F2 (info, coverage):** the ASCII `..` grammar is covered by one fixture/omission position (middle row of
  `S001..S006`); no second `..` fixture varies the omitted position — coverage observation, not a defect.

## Residual risk / verification gaps
- Fixture 05 exercised in **working-tree mode only**; the `--revision` Git-blob path was not run for it (the runner
  never passes `--revision`), so Git-mode enumeration of `..` ranges is unexercised here.
- The 29-case green is the runner's own verdict and does not by itself evidence row/file correctness (F1) — my
  row/file check is seat-local evidence only; no mutant gate was built (this seat attacks the consumer fixture, not
  source) — the input mutation stands in for it; no r24/r26 replay; no HTTP/authenticity check (URLs are placeholders).

## Hygiene
No source/fixture/ledger/manifest/registry writes in the repo — `git status --porcelain scripts/` empty before and
after; live fixture sha256s unchanged. Writes: this report and scratch under `/fast/scratch/hyaku/kake-r27/AttackCase05/`
(`base/`, `mut/`, `run/`, `tmp/`, captured stdout/exit files); `TMPDIR` exported explicitly; no `/tmp`, no `/dev/shm`.
No tool/package installs needed or performed; no build, lint or formatter run.
