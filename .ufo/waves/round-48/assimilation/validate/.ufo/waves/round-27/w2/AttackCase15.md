# AttackCase15 — consumer fixture 15-invalid-json-population (r27 fresh falsification)

Seat: KakeR27.AttackCase15 · Lane: leaf (no dispatch) · Axis: operability · Milestone: r27-fresh-falsification
Attacked item: `scripts/fixtures/citing-set/15-invalid-json-population` under frozen candidate
`ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`).

## Authority / bindings actually used
- Gate bytes run = `git show ac46a747…:scripts/citing_set.py` → scratch `gate/citing_set.py`
  sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` = frozen-candidate.json entry
  (exact match). Working tree `scripts/citing_set.py` blob `352a471abec08daa56a0fb7ef23fe78f2930d773` ==
  candidate blob; fixture `population.json` blob `7a868ee71634539029d51959d89bc210d8c16c88` == candidate blob.
- Live fixture untouched after the run (re-hashed: population `c7021543…`, ledger `8d6fe5c4…`,
  expected `e583ca3f…`, corpus `91748147…` = frozen-candidate.json). `git status --porcelain scripts/` empty.
- Scratch only: `/fast/scratch/hyaku/kake-r27/AttackCase15/` (TMPDIR/TMP/TEMP set there explicitly; no /tmp, no /dev/shm).
  Unrelated cwd for every probe: `/fast/scratch/hyaku/kake-r27/AttackCase15/run`. Python 3.14.8. No installs.

## Independent expectation (declared BEFORE running P1, derived from inputs + contract only)
`population.json` = `{"round": 27, "rows": [ {"id": "S001", "kind": "code",` — truncated, malformed JSON.
Contract `gateInterface.output`: finding id `input_invalid`; exit 2 = could-not-evaluate; the gate reads the
population document before the ledger/corpus, so exactly ONE finding, `input_invalid`, and NO pair-level
findings (no `unadjudicated_citing_pair`, no `ledger_pair_not_cited`): exit **2**, finding-id multiset
**{"input_invalid":1}**, verdict `could-not-evaluate`.

## P1 — pristine scratch copy, frozen gate, unrelated cwd
Command: `python3 -B gate/citing_set.py --root …/case15-orig --population population.json --ledger ledger.json --json`
Exit **2**, stdout sha256 `e07bb575f592fe64cbb6c31552f482e4114aca8d279f6cf7891e38e749252f34`:
`{"verdict":"could-not-evaluate","citingPairs":0,"ledgerPairs":0,"findings":[{"id":"input_invalid",
"reason":"document_not_json","scope":"population","path":"population.json","detail":"Expecting property name
enclosed in double quotes: line 2 column 1 (char 55)"}]}` ; stderr empty.
Independently derived multiset == observed == `expected.json` (`exit 2`, `["input_invalid"]`). **No disagreement.**
Row/file identity: this finding class carries no row/file; observed `scope=population`, `path=population.json`
(as supplied), `reason=document_not_json` — the fault is attributed to the population document, correctly.
cwd-independence: same command with cwd=case dir → byte-identical stdout (`e07bb575…`), exit 2.

## P2 — ONE causally meaningful input change (independently declared consequence)
Change: `population.json` repaired from the truncated bytes into the valid JSON it was truncated from
(`{"round": 27, "rows": [ {"id": "S001", "kind": "code"} ]}`, sha `d0f1c5f2…`); ledger/corpus untouched.
Declared expected consequence: exit **0**, verdict `clean`, findings multiset **empty**, `citingPairs=1`,
`ledgerPairs=1`, `populationRows=1`, `corpusFiles=1`, `outsidePopulation=0` — because the only `S`-id token in
the corpus file is `S001` (metadata line `source: S001`) and `ledger.json` adjudicates exactly
`(S001, corpus/knowledge/static-canonical-preflight.md)`.
Observed: exit **0**, `{"verdict":"clean","citingPairs":1,"ledgerPairs":1,"findings":[],"populationRows":1,
"corpusFiles":1,"outsidePopulation":0,"source":"working-tree"}` — **exactly as declared**.
⇒ fixture 15's exit-2 is caused specifically by the malformed JSON, not by a vacuous/always-failing case.

## Extra boundary probes (own scratch inputs; expectations declared before each run)
- P3 (malformed **ledger**, valid population) → exit 2, findings `["input_invalid"]`, `scope=ledger`,
  `path=ledger.json`, `reason=document_not_json`. Same id as fixture 15 ⇒ the oracle cannot attribute the
  fault to the population.
- P4 (valid population, `rows: []`) → exit 1, `ledger_pair_not_cited`, `file=corpus/knowledge/static-canonical-preflight.md`,
  **`row="1"`** — I had declared `row="S001"`; the gate emits the bare numeric key (prefix lost).
- P5 (authored minimal case: population spells the id `S0001`, ledger spells it `S001`, corpus cites nothing)
  → exit 1, `ledger_pair_not_cited`, `row="S0001"`, `file=corpus/knowledge/doc.md` ⇒ the emitted `row` is the
  **population** spelling, never the ledger's own spelling.
- P6 (fixture 15 slot fed fixture 16's valid-JSON-wrong-shape population) → exit 2, findings `["input_invalid"]`,
  `reason=document_shape_invalid` ⇒ fixture 15's `expected.json` is satisfied by two distinct failure modes
  (its sha is byte-identical to fixture 16's).
- Cross-check on two live fixtures (scratch copies, read-only): 17-ledger-row-outside-population → exit 1,
  `ledger_pair_not_cited`, `row="19"` (ledger spells `S019`); 26-ledger-pair-file-absent → exit 1,
  `ledger_pair_not_cited`, `row="2"` (ledger spells `S002`).

## Findings by severity
1. **MEDIUM (operability, latent) — ledger-sourced findings lose row identity.** `ledger_pair_not_cited`
   (and `ledger_duplicate_pair`) report `row` from the population display map, falling back to the bare numeric
   key when the row is outside the population: `"19"`, `"2"`, `"1"`. No corpus/population/ledger row is spelled
   that way, so a consumer cannot join the finding back to the offending ledger row by the documented `row`
   field; in fixture 17 two ledger rows share one file, so `file` alone is ambiguous. Counting is unaffected
   (matching uses the numeric key), so no miscount — traceability only. Evidence: P4, P5, fixture 17/26 runs.
   Latent in the r27 real run: the candidate's corpus/ledger run is exit 0 (no such finding emitted today).
   Note: `scripts/citing_set_selftest.py` compares only exit + sorted finding-**id** multiset
   (exit mismatch / finding-id mismatch branches), so no fixture in the suite can observe this.
2. **LOW (oracle coverage note, not a gate defect) — fixture 15's expected.json is coarse.** Exit 2 +
   `["input_invalid"]` is satisfied by malformed JSON, wrong shape, a bad ledger, or a missing document (P3/P6).
   The gate itself discriminates correctly via `reason`/`scope`/`path`, which the oracle ignores. No rewrite of
   expected outcomes is proposed (contract forbids it); recorded as coverage granularity only.
3. **NONE for fixture 15 itself.** Independent derivation, observed run, and `expected.json` agree on exit 2 and
   the single `input_invalid` id; scope/path/reason are accurate; the fixture is not vacuous (P2).

## Residual risk / verification gaps
- Only fixture 15 (plus the two read-only cross-checks 17/26) was probed; the remaining 26 fixture cases were not
  re-run by this seat (other seats' scope; the recorded gate selftest 29/29 exit 0 was not re-verified here).
- `unadjudicated_citing_pair` row spelling under population/ledger spelling divergence (population `S0001` vs
  ledger `S001`) was not observed in a run (P5 was shaped for the ledger-not-cited direction) — [INFERENCE] from
  the shared `display.get(...)` fallback in `evaluate()`.
- The bare-numeric `row` fallback was not exercised through `--revision` (Git-source) mode; the fallback lives in
  shared code, so it is expected to be identical there — unverified.
- No install/update was performed; no pacman transaction; no source, fixture, ledger, manifest or state file was
  modified by this seat (report file only).
