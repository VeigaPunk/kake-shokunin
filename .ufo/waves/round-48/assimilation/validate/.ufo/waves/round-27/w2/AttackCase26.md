# AttackCase26 — fixture `26-ledger-pair-file-absent` (r27-fresh-falsification, axis: operability)

Seat: KakeR27.AttackCase26 (leaf, no dispatch). Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD == candidate).
No installs (none needed). Source read-only, live fixture untouched; scratch only under `/fast/scratch/hyaku/kake-r27/AttackCase26/`.

## Attacked item
`scripts/fixtures/citing-set/26-ledger-pair-file-absent` consumed by `scripts/citing_set.py` (gate) through `scripts/citing_set_selftest.py` (runner).
Identity: gate blob at candidate == working tree, `sha256 3a361a002f66ce16b475e08eb2949db67f6651900d2c4b2699d5ef37ffc228` (`git cat-file -p ac46a74:scripts/citing_set.py | sha256sum` == `sha256sum scripts/citing_set.py`); runner-reported `gateSha256` identical.
Fixture blobs at candidate: `publish-channels.md 06b797b8`, `expected.json 502c20bb`, `ledger.json ed681530`, `population.json 1705091e`.

## Independently derived expectation (declared BEFORE any gate run)
From fixture inputs + `.ufo/waves/round-27/contract.json` only:
- population = {S001}; ledger = (S001, `corpus/knowledge/publish-channels.md`), (S002, `corpus/knowledge/retired-channels.md`); corpus = 1 file, `retired-channels.md` ABSENT.
- `publish-channels.md` holds exactly one token (`S001`), no range ⇒ citing set = {(S001, publish-channels.md)}; citingPairs 1, ledgerPairs 2.
- (S001, publish-channels.md) cited and ledgered ⇒ no finding. (S002, retired-channels.md) not cited ⇒ exactly one `ledger_pair_not_cited`; no `unadjudicated_citing_pair` (not cited), no duplicate.
- Expected exit **1** (verdict `failed`), findings multiset **{ledger_pair_not_cited} ×1}.
- Row/file identity: file `corpus/knowledge/retired-channels.md`; row = population id if known else numeric fallback ⇒ S002 ∉ population ⇒ row renders `"2"`.
- `expected.json` (read only after derivation) = `{"exit":1,"findings":["ledger_pair_not_cited"]}` ⇒ **agrees** with the derivation (exit + multiset exact).

## Run 1 — real frozen gate CLI, scratch copy, unrelated cwd
Scratch copy byte-identical to live fixture (publish-channels.md `b9e64c16…`, expected.json `3d2647f7…`, ledger.json `35d28a4c…`, population.json `11942908…`).
```
cd /fast/scratch/hyaku/kake-r27/AttackCase26/unrelated-cwd
TMPDIR=/fast/scratch/hyaku/kake-r27/AttackCase26/tmp python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --root /fast/scratch/hyaku/kake-r27/AttackCase26/fixture-copy \
  --population population.json --ledger ledger.json --json
```
stdout: verdict `failed`, citingPairs 1, ledgerPairs 2, populationRows 1, corpusFiles 1, outsidePopulation 0,
findings `[{id: ledger_pair_not_cited, row: "2", file: "corpus/knowledge/retired-channels.md"}]`; **exit 1**.
Matches declaration: exit ✓, id multiset ✓, file ✓, row ✓ (incl. the `"2"` fallback).

### Real consumer runner (read-only; it points the gate at the live fixture by design)
```
TMPDIR=/fast/scratch/hyaku/kake-r27/AttackCase26/tmp python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set_selftest.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --tmpdir <scratch> --json
```
exit **0**; verdict `clean`, cases 29, failed 0, meetsContractMinimum true; case `26-ledger-pair-file-absent` → `ok: true`, expected exit 1 / `["ledger_pair_not_cited"]`, actual exit 1 / `["ledger_pair_not_cited"]`. No fixture failure.

## Probe 1 — ONE causally meaningful input change (scratch only)
Declaration written first: `/fast/scratch/hyaku/kake-r27/AttackCase26/probe1-declaration.txt`.
Change (one file): scratch `population.json` rows += `{"id":"S002","kind":"code","tier":"A","scope":"registry row S002 as opened on 2026-10-21"}`
(pristine `11942908…` → mutated `4fe30045f3fa03294a9ffb79bf09dd9bd573df167a228e5ac76233888d5b13c8`).
Declared expected: exit 1; findings still exactly `{ledger_pair_not_cited ×1}`; **row flips `"2"` → `"S002"`**; file unchanged; citingPairs 1; ledgerPairs 2; populationRows 2; corpusFiles 1; outsidePopulation 0; verdict `failed`.
Observed: exit **1**; findings `[{id: ledger_pair_not_cited, row: "S002", file: "corpus/knowledge/retired-channels.md"}]`; citingPairs 1; ledgerPairs 2; populationRows 2; corpusFiles 1; outsidePopulation 0; verdict `failed` — **all declared fields matched**.

## Findings (author-side, severity ordered)
### F1 — MEDIUM: the fixture does not exercise the boundary its name claims
Pristine ledger row `S002` is **not in the population**, and the gate builds the citing set only from population ids
(`scripts/citing_set.py`: `if key in population: citing.add((key, relative)) else: outside.add(...)`), so (S002, retired-channels.md)
can never be cited **whether or not the file exists** (with the file present the token lands in `outside`, not `citing`).
Case 26's observable outcome (exit 1, `ledger_pair_not_cited`) is identical to `12-noncited-ledger-pair` (file present, row uncited)
and `17-ledger-row-outside-population` (file present, row outside population); only `corpusFiles`/`outsidePopulation` differ.
Probe 1 confirms the causal structure: with S002 in the population the finding survives *because the file is absent* (row now `S002`),
so absence becomes the operative cause only after the population change. `expected.json` is still correct w.r.t. actual gate behaviour —
a coverage-strength gap, not a wrong oracle. [INFERENCE] for "creating the file alone would not change the finding" (no second mutation, by one-change rule);
it follows from the cited source branch plus Probe 1's result. Recommendation to L1 (no edit by this seat): put `S002` in case 26's population
so the absent file is the sole cause, or rename the case to say it duplicates the outside-population path.

### F2 — MEDIUM (operability): finding `row` identity degrades to a bare number
Pristine run emits `row: "2"` for ledger row `S002`; the ledger spelling is discarded because the display map is built only from the
population and the fallback is `str(key[1])`. A consumer reading the gate JSON (not the ledger) cannot map the finding back to the ledger
row id (`S002` vs `S0002` equally ambiguous). Probe 1 proves the rendering is population-dependent, not ledger-dependent (`"2"` → `"S002"`).
No oracle can catch it: the runner compares only exit + sorted finding ids (`citing_set_selftest.py: run_case`), and no fixture
`expected.json` carries a `row` or `file` key (grep over `*/expected.json` → no match). Row/file identity is outside the whole C2 oracle surface.

### F3 — LOW / no-discrepancy: an absent ledger-referenced file is not `input_invalid`
The gate never reads ledger-referenced files, so absent `corpus/knowledge/retired-channels.md` yields `ledger_pair_not_cited` (exit 1),
not `input_invalid` (exit 2) — consistent with the contract (`ledger_pair_not_cited` = ledger pair outside the enumerated set;
`input_invalid` covers documents/corpus entries actually read). Recorded because the case name invites the opposite expectation.

### No false PASS / no scope defect observed
expected.json ≡ independent derivation ≡ gate output (exit, id multiset, file, row) ≡ runner observation for case 26; runner 29/29 clean;
candidate blob identity verified; no source/live-fixture write (`git status --porcelain scripts/` empty; live fixture hashes unchanged);
no r24 material executed; no network/credential/property operations.

## Residual risk / verification gaps
- F1/F2 are candidate-accurate but oracle-blind; fixture/expected edits belong to L1 (this seat edited no source).
- Only working-tree source mode exercised here (`--revision` Git-blob path untouched by this fixture).
- The `"2"` row rendering and the population-gated citing set are the two behaviours a future gate change could alter silently without breaking any expectation.
