# AttackCase29 — consumer fixture `29-ledger-pair-two-numeric-spellings` (r27 fresh falsification)

Lane: leaf reviewer, operability axis. No subagent dispatch.
Seat scratch: `/fast/scratch/hyaku/kake-r27/AttackCase29/` (`tmp/` as explicit TMPDIR; no /tmp, no /dev/shm).

## Attacked item (exact)

- Fixture `scripts/fixtures/citing-set/29-ledger-pair-two-numeric-spellings/` = `expected.json`, `ledger.json`, `population.json`, `corpus/knowledge/mirror-pitfalls.md`.
- Consumer path: `scripts/citing_set_selftest.py` (fixture runner) → gate `scripts/citing_set.py`.
- Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; repo HEAD == candidate. Gate sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` (working tree == `git cat-file -p ac46a747…:scripts/citing_set.py` == frozen-candidate.json entry). Runner sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`.
- Fixture bytes: scratch copy == live file == candidate blob == frozen-candidate.json entries — corpus `0159fbf2a1498107ab02efce146852e9986c496c9a9cdb11373986f81ddf0924`, expected `86c9a51aaa8ad6d73efe145825c7afd5eff1722257a0f19de851e3ded4b2356f`, ledger `c60f42c4fab0104f1b3da8a531d9f0e20338a808fb4632559ef0a31170653178`, population `b740227da57d03a11d023fb2d57760520f79d24c31afb2357c051adf716cab30`. Re-verified byte-identical after every run.

## Independent expectation (declared BEFORE any gate run; from input + contract only)

- `population.json` rows = `S001` and `S0001` — two spellings of one registry row (identical `scope` "registry row S001 as opened on 2026-10-21").
- `corpus/knowledge/mirror-pitfalls.md` contains exactly one citation token: `S001` (line 1 `source: S001 …`); no range (`scan_text` → tokens `['S001']`, ranges `[]`).
- `ledger.json` holds two pairs, `(S001, corpus/knowledge/mirror-pitfalls.md)` and `(S0001, corpus/knowledge/mirror-pitfalls.md)` — the same file, same row under two spellings.
- Under the gate's declared id rule (numeric comparison, `S001` == `S0001`; BuildGate.md L29/L83) both ledger pairs resolve to one comparable id ⇒ the row is adjudicated **twice** for one file ⇒ exactly one `ledger_duplicate_pair`. The citing pair exists and is adjudicated ⇒ no `unadjudicated_citing_pair`; no ledger row outside the enumerated set ⇒ no `ledger_pair_not_cited`; no malformed input, no range defect.
- **Declared: exit 1; finding-id multiset `["ledger_duplicate_pair"]` ×1; row identity S001; file identity `corpus/knowledge/mirror-pitfalls.md`; citingPairs 1; ledgerPairs 2; verdict `failed`.**

## Probe 1 — real gate CLI, scratch copy, unrelated cwd

cwd `/fast/scratch/hyaku/kake-r27/AttackCase29` (unrelated to the repo); TMPDIR set explicitly; root = scratch copy:
`python3 -B <repo>/scripts/citing_set.py --root ./base --population population.json --ledger ledger.json --json`

Exit **1**; stderr 0 bytes; stdout sha256 `af6c21933491080ea1705317587a2fc89fb43da8e7e19b89eb1285c15cd1ee20` (byte-identical across 2 independent invocations — deterministic):

```json
{"verdict":"failed","citingPairs":1,"ledgerPairs":2,
 "findings":[{"id":"ledger_duplicate_pair","row":"S001","file":"corpus/knowledge/mirror-pitfalls.md","occurrences":2}],
 "populationRows":2,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}
```

**Disagreement check:** observed exit 1 == `expected.json.exit`; observed id multiset `["ledger_duplicate_pair"]` == `expected.json.findings` (multiset, repetition-preserving). Row/file identity observed = (S001, corpus/knowledge/mirror-pitfalls.md) == independently derived identity. **No disagreement.** `citingPairs=1` with `populationRows=2` is the direct measurement that the two population spellings collapsed to one comparable id.

## Probe 2 — real consumer runner (live fixture tree)

`python3 -B <repo>/scripts/citing_set_selftest.py --root <repo> --tmpdir <seat>/tmp --min-cases 12 --json` → exit **0**, stderr 0 bytes; `verdict=clean, passed=true, cases=29, failed=0, failedCases=0, meetsContractMinimum=true, notes=[]`, `gateSha256=3a361a00…`. Case row for `29-ledger-pair-two-numeric-spellings`: `ok=true`, `expected {exit 1, ["ledger_duplicate_pair"]}` vs `actual {exit 1, verdict failed, ["ledger_duplicate_pair"]}` — the fixture is discovered and enforced by the shipped consumer, not orphaned.

## Probe 3 — ONE causally meaningful input change (expectation declared first)

Mutant `mutA`: scratch `ledger.json` pair[1].row `S0001` → `S002` (single numeric-spelling change; corpus/population/expected byte-identical). Mutant ledger sha256 `45209307fca581a7a982efd89db8fb443fea29154d0a046087193662da397f6a` vs pristine `c60f42c4…`. **Declared expected consequence: exit 1; finding multiset `{ledger_pair_not_cited}` ×1; `ledger_duplicate_pair` absent** (S002 is a distinct comparable id and is not cited in the corpus). Rationale: only the numeric-id collapse could have merged the two ledger rows into one duplicate; changing the second spelling to a different id must destroy that merge.

Observed: exit **1**, stderr 0 bytes, stdout sha256 `cb47f3a666998a16f41340891b887e530af33d60f627ad68119914e4ed3a5b95`:

```json
{"verdict":"failed","citingPairs":1,"ledgerPairs":2,
 "findings":[{"id":"ledger_pair_not_cited","row":"2","file":"corpus/knowledge/mirror-pitfalls.md"}],
 "populationRows":2,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}
```

Exactly the declared consequence; 0 disagreements. The `ledger_duplicate_pair` of Probe 1 was caused by the numeric-spelling identity of `S0001` with `S001` and by nothing else.

## Probe 4 — is the fixture discriminating? (declared before running)

Counterfactual recomputation over the *actual* fixture inputs using the gate's own `scan_text`, with the id key forced to **literal** (no numeric normalisation) instead of the shipped numeric key: unadjudicated 0, `ledger_pair_not_cited` 1, `ledger_duplicate_pair` 0 ⇒ literal semantics would yield exit 1 with `["ledger_pair_not_cited"]`, a **different** id multiset than `expected.json`. So fixture 29 is not vacuous: it pins the numeric-equivalence rule specifically, and a gate that compared ids as exact strings would fail this case. (Recomputation, not a repo mutation.)

## Probe 5 — oracle negative control (declared before running)

`mutC`: scratch copy of the fixture with `expected.json.exit` 1 → 0, fixtures dir containing only that case, shipped runner. **Declared expectation: the runner FAILS case 29 with "exit mismatch".** Observed: runner exit **1**, `failed=1`, `failures=[{"case":"29-ledger-pair-two-numeric-spellings","reason":"exit mismatch: expected 0, observed 1", "expected":{"exit":0,"findings":["ledger_duplicate_pair"]}, "actual":{"exit":1,"verdict":"failed","findings":["ledger_duplicate_pair"]}}]`. The oracle is load-bearing; `expected.json` is not a rubber stamp.

## Probe 6 — alias rule reaches beyond this fixture (declared before running)

`mutD` (population = single real-shaped row `S001`; corpus cites **only** the 4-digit alias `S0001`; ledger adjudicates `(S001, file)`). **Declared prediction: gate exit 0 clean** — the alias `S0001` satisfies row `S001`. Observed: exit **0**, `verdict clean`, `findings []`, `citingPairs 1`, `outsidePopulation 0`. Confirms the alias rule is a general id-normalisation, not a fixture-local coincidence. Reach on real data: the real corpus contains **no** `S`+4-or-more-digit token (grep over `corpus/knowledge` → empty) and the frozen 32-row population uses canonical 3-digit ids only, so the alias rule cannot alter the 16-pair measurement — consistent with BuildGate.md L84.

## Probe 7 — real-corpus C2 consumer (author-side cross-check)

`python3 -B .ufo/waves/round-27/c2_count.py --root . --revision ac46a7472d945a6d7ff135e4d7f07b0b6913d835` → exit **0**, `passed true`, `expected 16`, `detected 16`, `falsePositive 0`, `gateExit 1`; gate findings count 16, id histogram `{'unadjudicated_citing_pair': 16}`, rows `S001…S008, S022, S023`. The gate the fixture exercises is the same binary that carries the frozen C2 measurement.

## Findings (author-side, this seat only)

1. **Low — oracle precision gap: `expected.json` pins no row/file identity.** All 29 expected.json files carry exactly the keys `{exit, findings}` (verified across the whole family), and the runner compares exactly `run.returncode` and `sorted(finding_ids(report))` (`scripts/citing_set_selftest.py`, `run_case`, L263–L276). For this case the *whole* discriminating content is "one row adjudicated twice under two spellings"; a gate that attributed the same finding to the wrong row (say `S002`) or the wrong file would keep the runner green, because the id multiset is identical. My Probes 3/4 measured the true attribution (S001 / corpus/knowledge/mirror-pitfalls.md, occurrences 2) and it is correct, but that observable is unpinned by the fixture. Contract-conformant (`contract.json` fixtureInterface fixes `expected.json` as `{exit, findings:[id,…]}`), so this is a coverage limit, not a contract breach.
2. **Low — the fixture pins the numeric-id rule but not its *boundary* against the corpus token grammar.** The token rule requires `S` + ≥3 ASCII digits, so `S01` (Probe B, ledger pair[1].row `S0001`→`S01`) is *not* a corpus-citable literal, yet as a ledger row it still collapses onto `S001` (`id_key` accepts any digit count). Probe B observed exactly the base result (`ledger_duplicate_pair`, row S001, occurrences 2), i.e. a 2-digit ledger spelling merges with a 3-digit row. Both `S01` and `S0001` collapse because `_NUMERIC_ID_RE` is `^S([0-9]+)$`. Benign on the real corpus (no alias spellings exist there), but the boundary is unpinned by any fixture.
3. **Informational — `row` in a finding is a *display* label, not the ledger's declared spelling.** For a ledger row outside the population the gate renders the bare number: Probe E (ledger rows `S001` and `S019`, population `S001`) reported `{"id":"ledger_pair_not_cited","row":"19",…}` and the shipped fixture `17-ledger-row-outside-population` likewise reports `"row":"19"` for a declared `S019` — the `S` prefix and zero-padding are lost (`display.get(row, …)` falls back to `str(key[1])`). Consumers matching on the row string would not find `S019` in the output. Also note `display` keeps only the *first* id per comparable key (`load_population`), so `S001` wins over `S0001` for display; the finding therefore cannot show that two spellings were involved — the fixture's whole subject — except via `occurrences: 2`.
4. **Informational — inert ledger fields.** The ledger rows carry `statements`, `stale`, `report`; the gate's `load_ledger` reads only `row`/`file`. This fixture therefore carries no evidence about statement-unit counting, and its `statements: 1` values say nothing about the strict-C1 "six UNVERIFIABLE statement units" fact.
5. **Informational — obligation existence is citation-driven.** The gate emits no finding for a population row that is never cited (fixture 21 pins that: 2 population rows, empty citing set, empty ledger ⇒ exit 0). Consequence here: the corpus cites one spelling only, yet both population rows are satisfied by it via the numeric collapse — the `S0001` population row is never independently cited. That is the intended alias semantics (BuildGate.md L83), but it means the fixture cannot detect a regression where a *second* real row sharing a numeric value would be silently absorbed.
6. **Informational — no operability defect found in this consumer path.** The gate is deterministic (two byte-identical stdout runs), emits one JSON object on stdout with empty stderr, uses only relative `--population`/`--ledger` paths, runs correctly from an unrelated cwd, writes nothing, and the shipped runner discovers and enforces the case (29/29 clean, `meetsContractMinimum=true`).

## Discrepancies / uncertainties

- **No disagreement** on the exit code, the finding-id multiset, or the row/file identity, in the pristine case, in the mutated case, or in the runner's own comparison.
- `expected.json` cannot distinguish finding *cause* or *attribution* (Finding 1); my attribution evidence is the observed stdout plus Probe 3's clearing/replacement behaviour, not the fixture oracle.
- Probe 4 is a recomputation over the fixture inputs using the shipped scanner with a literal id key; it is not an executed run of a literal-identity gate (the assignment allowed one input change; the mutation seats hold the gate-source mutations).
- Not verified here (other seats' scope): the other 28 fixture cases' internals, the `--revision` Git-blob source mode for this fixture (Probes 1/3/4/5/6/7 are working-tree reads; Probe 7 is a Git-blob run of the frozen corpus but not of this fixture), and the `--selftest` delegation path (the runner was invoked directly).
- Source was read only from candidate-identical blobs; the live fixture was re-verified byte-identical after every run; `git status --porcelain --untracked-files=no` is empty (no production edit, no commit, no index/jj/remote change); no `__pycache__` was produced under `scripts/`. Scratch writes confined to `/fast/scratch/hyaku/kake-r27/AttackCase29/`.

## Residual risk

- A regression that keeps the count of `ledger_duplicate_pair` findings at one for this input but attributes it to the wrong row/file, or that swaps the numeric-id rule for exact-string ids *in a way that still yields one duplicate id*, stays green for the whole fixture family (Finding 1). Probe 4 shows a full switch to literal ids would be caught; partial or boundary regressions (Finding 2) would not.
- The numeric-id rule's reach is asserted by this fixture but not bounded by it: no fixture pins where the token grammar (`S`+≥3 digits) and the id-comparison grammar (`S`+any digits) must diverge (Finding 2).
- `row` labels in findings are lossy for out-of-population rows (Finding 3); a consumer keying on the ledger's declared spelling would mis-resolve such findings, and the shipped fixture 17 already exhibits it.
- All measurements are working-tree reads of candidate-identical blobs; the Git-blob (`--revision`) mode was exercised only through the frozen-corpus C2 consumer (Probe 7), not through this fixture.

Tool installs: none (Python 3.14.8, git 2.56.0 already present; no pacman/uv/cargo/npm action taken).
