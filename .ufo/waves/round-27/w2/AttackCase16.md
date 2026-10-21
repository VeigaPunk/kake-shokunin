# AttackCase16 — consumer fixture `16-invalid-population-shape` (r27 fresh falsification)

Lane: leaf reviewer, operability axis (secondary: oracle bindingness of `expected.json`).
Seat scratch: `/fast/scratch/hyaku/kake-r27/AttackCase16/` (TMPDIR set to `.../AttackCase16/run`; no /tmp, no /dev/shm).

## Attacked item (exact)

- Fixture: `scripts/fixtures/citing-set/16-invalid-population-shape/` (`expected.json`, `ledger.json`, `population.json`, `corpus/knowledge/static-canonical-preflight.md`).
- Consumer: `scripts/citing_set_selftest.py` (fixture runner) → gate `scripts/citing_set.py`.
- Source authority: frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. Working-tree `scripts/citing_set.py` git blob `352a471abec08daa56a0fb7ef23fe78f2930d773` == candidate blob (equal). Gate sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`; runner sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`. All four fixture files: live blob == candidate blob == scratch-copy sha256 (expected `e583ca3f…`, ledger `8d6fe5c4…`, population `fe57d814…`, corpus `91748147…`). No source read outside the candidate blob; live fixture re-verified byte-identical after all runs (`git status --porcelain --untracked-files=no` empty).

## Independent expectation (declared BEFORE any gate run)

Derived from the input documents and the contract, not from `expected.json` and not from a green run:
`population.json` = `{"round":27,"rows":{"S001":{…}}}` — `rows` is an **object**, whereas the contract fixes the population shape as `rows` = list of `{id}` (canonical `.ufo/waves/round-27/frozen/population.json` has `rows` = list of 32 objects with `id`). Therefore the population document is shape-invalid → one `input_invalid` finding → verdict `could-not-evaluate` → **exit 2**, finding-id multiset `["input_invalid"]` (×1). The corpus file cites exactly one id (`S001`), and the ledger holds exactly `(S001, corpus/knowledge/static-canonical-preflight.md)`, so the shape defect must be the *sole* cause of exit 2 (no pair-level finding may coexist).

## Probe 1 — gate CLI on a scratch copy, unrelated cwd

Command (cwd `/fast/scratch/hyaku/kake-r27/AttackCase16/run`, root = scratch copy):
`python3 -B <repo>/scripts/citing_set.py --root <scratch>/fixtures/16-invalid-population-shape --population population.json --ledger ledger.json --json`
Exit **2** (stderr empty, 0 bytes). stdout sha256 `67b5038db30aa043b3ec4126a95183ad87e358e80d7e2d4ea4214b3156edef63`:

```json
{"verdict":"could-not-evaluate","citingPairs":0,"ledgerPairs":0,
 "findings":[{"id":"input_invalid","reason":"document_shape_invalid","scope":"population","path":"population.json"}]}
```

**Disagreement check:** observed exit 2 == `expected.json.exit`; observed id multiset `["input_invalid"]` == `expected.json.findings`. **No disagreement.** The finding carries `scope=population`, `path=population.json` — the defect is attributed to the population document, not to corpus or ledger; `citingPairs`/`ledgerPairs` are 0, i.e. the evaluation aborted before any pair enumeration, confirming the population shape is the sole cause.

## Probe 2 — real consumer runner (scratch fixture dir)

`python3 -B <repo>/scripts/citing_set_selftest.py --root <repo> --fixtures <scratch>/fixtures --tmpdir <scratch>/run` → exit **0**, stdout sha256 `68bbfabe4ddcd59280200c0bf263781b94d46b06ae775a77b975ae6332ca09eb`; `verdict=clean, passed=true, cases=1, failed=0`, case 16 `ok=true`, `expected {exit 2, ["input_invalid"]}` vs `actual {exit 2, verdict could-not-evaluate, ["input_invalid"]}`. (Note only: `cases=1` < contract minimum 12 — artifact of running one case in isolation.)

## Probe 3 — ONE causally meaningful input change (declared expectation first)

Mutation (scratch copy only): `population.json` `rows` object → list `[{id:"S001",kind:"code",tier:"A"}]`; no other file touched; `expected.json` left untouched.
Pristine `population.json` sha256 `fe57d814c017b8eded06a3efbe0e82cbfad65e13ab33b9d602b0393b455541eb` → mutant `105e92aaeae611c08e91bc203364c094339ac59f9562108103abe6a478020a14`; pristine copy re-verified unchanged after mutation.

Declared expected consequence: shape error disappears; population loads 1 row (`S001`); corpus cites `S001` once, no ranges → citing set = {(S001, corpus/knowledge/static-canonical-preflight.md)} → `citingPairs=1`; ledger holds exactly that pair → `ledgerPairs=1`; no `unadjudicated_citing_pair`, no `ledger_pair_not_cited`, no `ledger_duplicate_pair`, no `citation_range_invalid` → verdict `clean`, **exit 0**, findings `[]`; and the unchanged fixture oracle must then **mismatch** (expected 2, observed 0).

Observed (Run C, same command as Probe 1, root = mutated scratch copy): exit **0**, stdout sha256 `fc285c047ccfc0e677dde1825b89e2bc6cec759476dbe590c99f9b91172ffdd6`:
`{"verdict":"clean","citingPairs":1,"ledgerPairs":1,"findings":[],"populationRows":1,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}` — matches the declared expectation exactly (0 disagreements).
Run D (consumer runner on the mutated dir, unchanged `expected.json`): exit **1**, stdout sha256 `c63f3a1eaf4372b4a328973dfaabd181e88a8f438c0c8ee7bae648be5d24dd3b`, `failed=1`, reason `"exit mismatch: expected 2, observed 0"`. ⇒ the oracle is binding, not vacuous: `expected.json` is satisfied only while the population shape is broken.

## Row/file identity (beyond the id tally)

- Ledger file string `corpus/knowledge/static-canonical-preflight.md` is byte-identical to the corpus-relative path the gate derives for the only corpus file under the fixture root (`root/corpus/knowledge/static-canonical-preflight.md`); identity is therefore positional, not a prefix/suffix coincidence.
- Independent cross-check on the *production* pinned inputs (read-only, not a fixture change): `python3 -B scripts/citing_set.py --root .ufo/waves/round-27/frozen --population population.json --ledger ledger.json --json` → exit **1**, stdout sha256 `5216c7d8aaa7c17995d4d2b503b892b67bb796a7ca8f096ebcba065655906643`, verdict `failed`, `citingPairs=57`, `ledgerPairs=41`, finding-id histogram exactly `{unadjudicated_citing_pair: 16}` (matches the frozen C2 oracle count 16, independent of L1's counter). Every one of the 16 findings has `row` present in `frozen/population.json` (0 violations) and `file` pointing at an existing corpus file (0 violations); 0/41 ledger entries carry a non-`corpus/knowledge/` file. The real-corpus (S001, corpus/knowledge/static-canonical-preflight.md) pair appears as an unadjudicated pair there, i.e. the same row/file identity the fixture encodes.

## Findings (author-side, this seat only)

1. **Medium — oracle precision gap (operability of the fixture family).** `expected.json` pins only `exit` + finding ids, and the runner compares only those. For case 16 that means a gate that returned exit 2 with a *different* `input_invalid` cause (e.g. `root_not_a_directory`, `document_not_json`, `corpus_file_not_utf8`) would still satisfy this fixture; the defect-attribution fields (`reason=document_shape_invalid`, `scope=population`, `path=population.json`) are observed by me but unpinned by the oracle. Evidence: Run A stdout above vs `expected.json` content `{"exit":2,"findings":["input_invalid"]}`; runner comparison code path in `scripts/citing_set_selftest.py` (`run_case`, compares `run.returncode` and `sorted(finding_ids(report))` only).
2. **Low — shape-rejection coverage gap.** Only the `rows`-is-object variant is exercised (case 15 covers malformed JSON). The other shape-invalid paths visible in the gate source (rows list containing a non-object; row without a non-empty string `id`) are not pinned by any fixture; I did not run cases 15/other cases, so this is a coverage observation from the source, not a measured defect.
3. **Informational — inert fixture field.** `ledger.json` carries `"statements":1,"stale":0,"report":"w1/PairS001Static-Canonical-Preflight.md"`; the gate ignores these fields. Harmless, but it means the fixture's ledger shape is a superset of the contract's `{row,file}` requirement and cannot detect a regression that starts consuming/validating extra ledger fields.

## Discrepancies / uncertainties

- **No disagreement** between `expected.json` and observed behaviour on either the exit code or the finding-id multiset, in the pristine case and in the mutated case (the latter diverges exactly as declared, and the consumer oracle flags it).
- Not verified here (out of this seat's scope): the other 28 fixture cases; the `--revision` git-blob source mode for this case (the consumer runner uses working-tree mode — fixture 18 covers `--revision`-less input); the `--selftest` delegation path.
- Exit 2 is a shared code across several input_invalid causes; attribution here rests on the observed `reason`/`scope`/`path` fields of the single finding plus the one-change isolation in Probe 3.

## Residual risk

- Fixture 16's `expected.json` cannot distinguish "population shape invalid" from any other exit-2 cause; a future regression that mis-classifies a *different* input defect as exit 2 would keep the consumer green (Finding 1).
- The fixture family has no case pinning the `scope`/`path`/`reason` attribution of `input_invalid`, so "which input was rejected" remains an unpinned observable.
- All measurements here are working-tree reads of candidate-identical blobs; nothing exercised the frozen Git-blob source mode for this fixture.
