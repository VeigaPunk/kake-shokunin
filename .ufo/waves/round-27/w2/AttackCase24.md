# AttackCase24 — consumer fixture `24-range-separator-across-linebreak` (r27 fresh falsification)

Lane: leaf reviewer, operability axis. No subagent dispatch.
Seat scratch: `/fast/scratch/hyaku/kake-r27/AttackCase24/` (`tmp/`, `unrelated-cwd/`; TMPDIR set explicitly; no /tmp, no /dev/shm).

## Attacked item (exact)

- Fixture `scripts/fixtures/citing-set/24-range-separator-across-linebreak/` = `expected.json`, `ledger.json`, `population.json`, `corpus/knowledge/static-canonical-preflight.md`.
- Consumer path: `scripts/citing_set_selftest.py` (fixture runner) → gate `scripts/citing_set.py`.
- Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; repo HEAD == candidate. Gate working-tree blob `352a471abec08daa56a0fb7ef23fe78f2930d773` == candidate blob; runner blob `c69b09b2e47f4115aa4e8ff286aa7cfe0e171a64` == candidate blob. Gate sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`, runner sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` (both match `.ufo/waves/round-27/frozen-candidate.json`).
- Fixture bytes (scratch copy == `git show candidate:<path>` == live file == frozen-candidate entries): corpus `efa1adaba88322a3c9d4db077e5a2cbb6e236fc56fcfbb5b2f38887fbac391d4`, expected `49d7286dd34a00ce88a31d473272e589cb5542e76d60505cd9591437ee353e81`, ledger `0c120d08d11bda61b0c812e1ca5bfbdd88d87ee748ff74c39237446a7d957045`, population `f04a4f37f256034f70f29b7b0aade3d87a498b42a01a85bc454d51ddc3b272f6`.

## Independent expectation (declared BEFORE any gate run; derivation from input + contract only)

- `population.json` rows = S001…S006 (6 rows). `corpus/knowledge/static-canonical-preflight.md` names only S001 and S006 as literals, but contains `spans S001` + newline + `to S006` — a range whose separator sits across a linebreak; the contract's range grammar admits `to` as a separator, so the span S001…S006 enumerates all 6 population rows as citing pairs in that one file ⇒ citing set = {(S001…S006, corpus/knowledge/static-canonical-preflight.md)}.
- `ledger.json` holds 5 pairs (S001, S002, S003, S004, S006), all with file `corpus/knowledge/static-canonical-preflight.md`. **S005 is cited but unadjudicated** ⇒ exactly one `unadjudicated_citing_pair`.
- No ledger row lies outside the enumerated set (no `ledger_pair_not_cited`), no duplicates, no range defect (`1 ≤ 6`, span 5 ≤ 200), inputs well-formed.
- **Declared: exit 1; finding-id multiset `["unadjudicated_citing_pair"]` ×1; row identity S005; file identity `corpus/knowledge/static-canonical-preflight.md`; citingPairs 6; ledgerPairs 5; verdict `failed`.**

## Probe 1 — real gate CLI, scratch copy, unrelated cwd

cwd `/fast/scratch/hyaku/kake-r27/AttackCase24/unrelated-cwd`; TMPDIR=`.../AttackCase24/tmp`; root = scratch copy:
`python3 -B <repo>/scripts/citing_set.py --root <scratch>/fixture24 --population population.json --ledger ledger.json --json`

Exit **1**; stderr 0 bytes; stdout sha256 `dcbff2302f37023b8c20a5a692aa08f72195622dd9cb795a3b5e74a8c7b442c8` (byte-identical across 2 independent invocations):

```json
{"verdict":"failed","citingPairs":6,"ledgerPairs":5,
 "findings":[{"id":"unadjudicated_citing_pair","row":"S005","file":"corpus/knowledge/static-canonical-preflight.md"}],
 "populationRows":6,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}
```

**Disagreement check:** observed exit 1 == `expected.json.exit`; observed id multiset `["unadjudicated_citing_pair"]` == `expected.json.findings` (multiset, repetition-preserving). Row/file identity observed = (S005, corpus/knowledge/static-canonical-preflight.md) == independently derived identity. **No disagreement.**
Measurement that the across-linebreak range was really enumerated (not inferred from source text): `citingPairs=6` while only S001 and S006 appear as literals ⇒ the S001→S006 range contributed S002…S005. `outsidePopulation=0`, `corpusFiles=1`, `populationRows=6`.

## Probe 2 — real consumer runner (live fixture tree)

`python3 -B <repo>/scripts/citing_set_selftest.py --root <repo> --tmpdir <seat>/tmp --min-cases 12 --json` → exit **0**, stderr 0 bytes; `verdict=clean, passed=true, cases=29, failed=0, failedCases=0, meetsContractMinimum=true`, `notes=[]`. Case row for `24-range-separator-across-linebreak`: `ok=true`, `expected {exit 1, ["unadjudicated_citing_pair"]}` vs `actual {exit 1, verdict failed, ["unadjudicated_citing_pair"]}` — i.e. the fixture is not orphaned: it is discovered and enforced by the shipped consumer.

## Probe 3 — ONE causally meaningful input change (expectation declared first)

Declaration written to `/fast/scratch/hyaku/kake-r27/AttackCase24/mutation-declaration.txt` **before** the mutant gate run: append exactly one ledger pair `{"row":"S005","file":"corpus/knowledge/static-canonical-preflight.md","statements":2,"stale":0,"report":"w1/PairS005Static-Canonical-Preflight.md"}` to the scratch `ledger.json` (5→6 pairs); corpus/population/expected left byte-identical. Declared expected consequence: **exit 0, verdict `clean`, findings `[]`, citingPairs 6, ledgerPairs 6, populationRows 6, corpusFiles 1, outsidePopulation 0, source `working-tree`**; falsification criterion = any nonzero exit, any residual finding, or citingPairs/ledgerPairs ≠ 6/6. Rationale: only the exact (row, file) pair attributed by Probe 1 can clear that finding — so the mutation is a causal test of row/file identity, not a cosmetic edit.

Observed: mutant ledger sha256 `bb57f695745338ce366ef742b309e8c2fdd2139c89944e7f4dc7bcb63886e2b6` (pristine `0c120d08…`); corpus and expected re-verified byte-identical to the candidate after the edit. Same command/cwd as Probe 1 → exit **0**, stderr 0 bytes, stdout sha256 `c64dd6e1b75a05464cf2efbd349c5f9cb2e5ed8939903acb30adf5be8421b976`:

```json
{"verdict":"clean","citingPairs":6,"ledgerPairs":6,"findings":[],"populationRows":6,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}
```

Exactly the declared consequence; 0 disagreements. The single finding of Probe 1 was caused by the genuine (S005, corpus/knowledge/static-canonical-preflight.md) obligation and nothing else.

## Findings (author-side, this seat only)

1. **Low — oracle precision gap: `expected.json` pins no row/file identity.** The fixture's oracle is `{exit, findings:[ids]}` and the runner compares exactly `run.returncode` and `sorted(finding_ids(report))` (`scripts/citing_set_selftest.py`, `run_case`). For this case the *whole* discriminating content is "one pair is missing"; a gate that attributed the same finding to the wrong row (say S002) or the wrong file (say a different corpus file) would keep the runner green, because the id multiset is identical. My Probe 3 measured the true attribution (S005 / corpus/knowledge/static-canonical-preflight.md) and it is correct, but that observable is unpinned by the fixture. Contract-conformant (`contract.json` fixtureInterface fixes `expected.json` as `{exit, findings:[ids]}`), so this is a coverage gap of the fixture family, not a contract breach.
2. **Informational — inert ledger fields.** The ledger rows carry `statements`, `stale`, `report`, which the gate's loader ignores (only `row`/`file` are read). Therefore this fixture cannot detect a regression in statement-unit counting, and the `statements: 2` values here are not evidence about the strict-C1 "six UNVERIFIABLE statement units" fact.
3. **Informational — obligation existence is citation-driven.** The gate emits no finding for a population row that is never cited (fixture 21 pins that as intended: 2 population rows, empty citing set, empty ledger ⇒ exit 0, findings `[]`). Consequence for this fixture: had the across-linebreak range *not* been recognized, the S005 obligation would vanish silently and the ledger rows S002–S004 would be reported as `ledger_pair_not_cited` — the runner would still fail loudly (different id multiset), so the fixture is discriminating in both directions. The counterfactual is an inference from the executed `citingPairs=6` and the fixture-21 oracle, not an executed run (the assignment allowed exactly one input change).
4. **Informational — no operability defect found in this consumer path.** Gate is deterministic (two byte-identical stdout runs), emits a single JSON object on stdout with empty stderr, uses only relative `--population`/`--ledger` paths, works from an unrelated cwd, writes nothing, and refuses nothing here; the runner discovers the case and enforces it (29/29 clean).

## Discrepancies / uncertainties

- **No disagreement** on the exit code, the finding-id multiset, or the row/file identity, in the pristine case and in the mutated case.
- `expected.json` cannot distinguish finding *cause* or *attribution* (Finding 1); my attribution evidence is the observed stdout plus the mutation's clearing behaviour, not the fixture oracle.
- Not verified here (other seats' scope): the other 28 fixture cases' internals, the `--revision` Git-blob source mode for this fixture, and the `--selftest` delegation path (the runner above was invoked directly; the gate's `--selftest` delegation was not exercised for this case).
- Source was read only from candidate-identical blobs; the live fixture was re-verified byte-identical after every run and `git status --porcelain --untracked-files=no` is empty (no production edit, no commit, no index/jj/remote change). Scratch writes confined to `/fast/scratch/hyaku/kake-r27/AttackCase24/`.

## Residual risk

- A regression that keeps the count of `unadjudicated_citing_pair` findings at one for this input but attributes it to the wrong row/file stays green for the whole fixture family (Finding 1); the same blind spot applies to every case whose expected multiset contains one repeated id.
- The across-linebreak separator is exercised only via the word separator `to` on its own line; other separator tokens with a linebreak (`-`, `–`, `—`, `..`, `through`) are covered by other cases with same-line separators, so a separator-token-specific linebreak regression inside the `to` branch only would not be caught by case 24 alone.
- All measurements here are working-tree reads of candidate-identical blobs; no Git-blob (`--revision`) mode was exercised for this fixture.

Tool installs: none (Python 3.14.8 and git already present; no pacman/uv/cargo/npm action taken).
