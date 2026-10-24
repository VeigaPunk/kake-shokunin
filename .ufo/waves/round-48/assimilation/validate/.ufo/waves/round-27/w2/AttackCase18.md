# AttackCase18 — fresh falsification of consumer fixture `18-working-tree-input-no-revision`

Seat: leaf reviewer (no dispatch). Axis: **operability**. Milestone: r27-fresh-falsification.
Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (`git rev-parse --verify <hash>^{commit}` OK).
Gate identity: live `scripts/citing_set.py` sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` ==
`git show ac46a74:scripts/citing_set.py` sha256 == blob `352a471abec08daa56a0fb7ef23fe78f2930d773`; runner
`scripts/citing_set_selftest.py` sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` == candidate blob.
**Attacked item** (read-only in repo): `scripts/fixtures/citing-set/18-working-tree-input-no-revision/` → `population.json`
(rows S001, S002), `ledger.json` (one pair: row `S001`, file `corpus/knowledge/mirror-pitfalls.md`),
`corpus/knowledge/mirror-pitfalls.md`, `expected.json` (`exit 0`, `findings []`); all four hash-identical to the candidate
blobs (expected `a2def88b…`, ledger `c5f6d0a5…`, population `4fe30045…`, corpus `0159fbf2…`).

## Independent derivation (declared BEFORE any gate run)
Contract C2: citing pair = (population row id, corpus file) from expanding citation tokens/ranges over every regular file
under `corpus/knowledge`; `unadjudicated_citing_pair` = cited pair absent from the ledger; `ledger_pair_not_cited` = ledger
pair absent from the citing set; `ledger_duplicate_pair` = repeated ledger pair.
- Independent token sweep with **my own** regex (`grep -oE 'S[0-9]{3,}'`, contract grammar, not the gate's code): exactly
  **one** token `S001`; independent range sweep (`S###(-|–|—|..|to|through)S###`): **0** ranges ⇒ citing set =
  `{(S001, corpus/knowledge/mirror-pitfalls.md)}`, `citingPairs = 1`.
- Ledger: one pair `(S001, corpus/knowledge/mirror-pitfalls.md)`, no repetition ⇒ `ledgerPairs = 1`, no duplicate finding.
- Citing pair == ledger pair ⇒ no `unadjudicated_citing_pair`, no `ledger_pair_not_cited`.
- Population row `S002` is cited by **no** corpus file; all five finding kinds are pair-relative (none population-relative)
  ⇒ an uncited population row yields **no** finding.
- **Declared expected: exit 0, verdict `clean`, finding-id multiset ∅** (agreement with `expected.json`).

## Probe A — real frozen gate CLI, scratch copy, unrelated cwd
Declared expected: exit 0 / `clean` / findings ∅. Scratch copy `/fast/scratch/hyaku/kake-r27/AttackCase18/base/18-working-tree-input-no-revision`
(live fixture untouched); cwd `/fast/scratch/hyaku/kake-r27/AttackCase18/cwd`; `TMPDIR=/fast/scratch/hyaku/kake-r27/AttackCase18/tmp` exported.
`python3 -B /fast/scratch/hyaku/kake-r27/AttackCase18/frozen/citing_set.py --root <scratch>/base/18-working-tree-input-no-revision --population population.json --ledger ledger.json --json`
stdout `{"verdict":"clean","citingPairs":1,"ledgerPairs":1,"findings":[],"populationRows":2,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}` → **EXIT=0**.
Same command against the live repo gate (byte-identical) → identical stdout, **EXIT=0**. Declared expectation met exactly;
`expected.json` **agrees** — no disagreement.

## Probe B — consumer fixture runner on the scratch copy
Declared expected: case `18-working-tree-input-no-revision` `ok:true`, `failed 0`, runner exit 0.
`python3 -B <scratch>/frozen/citing_set_selftest.py --root <scratch> --fixtures <scratch>/fixtures-only --gate <scratch>/frozen/citing_set.py --tmpdir <scratch>/tmp --min-cases 1`
stdout `{"verdict":"clean","passed":true,"cases":1,"failed":0,"results":[{"case":"18-working-tree-input-no-revision","ok":true,"expected":{"exit":0,"findings":[]},"actual":{"exit":0,"verdict":"clean","findings":[]}}]}` → **EXIT=0**. Met.

## Probe C — ONE causally meaningful input change (expected consequence declared before running)
Mutation (scratch copy only, `mut/…/corpus/knowledge/mirror-pitfalls.md`): append one line
`Round-27 probe: source S002 (corpus/SOURCES.md) mirror follow-up row.`; sha256 pre `0159fbf2a1498107ab02efce146852e9986c496c9a9cdb11373986f81ddf0924` → post `e4ca462b0a13c19f8a9c31ae50642705ea989aeb4e6e518a7a486d9cad99f629`.
**Declared expected consequence**: the appended `S002` is a population id cited by the corpus file but absent from the
ledger ⇒ exit **1**, verdict `failed`, finding-id multiset exactly `["unadjudicated_citing_pair"]` ×1, that finding's
**row** = `S002`, **file** = `corpus/knowledge/mirror-pitfalls.md`; `citingPairs`=2, `ledgerPairs`=1, `populationRows`=2,
`corpusFiles`=1, `outsidePopulation`=0; **no** `ledger_pair_not_cited`, `ledger_duplicate_pair`, `input_invalid`,
`citation_range_invalid`; consumer runner must now mark the case **failed** (exit mismatch 1 vs 0).
Observed (frozen gate, mutated scratch copy): `{"verdict":"failed","citingPairs":2,"ledgerPairs":1,"findings":[{"id":"unadjudicated_citing_pair","row":"S002","file":"corpus/knowledge/mirror-pitfalls.md"}],"populationRows":2,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}` → **EXIT=1**.
Every declared field matched, including row/file identity; no extra ids. Consumer runner over the mutated copy:
`{"verdict":"failed","passed":false,"failed":1,"results":[{"case":"18-…","ok":false,"reason":"exit mismatch: expected 0, observed 1","actual":{"exit":1,"findings":["unadjudicated_citing_pair"]}}]}` → **EXIT=1**.
⇒ The fixture is **not vacuous**: the same gate/runner flips 0→1 on a one-line input change; the working-tree read is live
(the appended line exists in no Git blob).

## Probe D — mode discrimination (read-only, live fixture)
Declared expected: with `--revision` the fixture layout cannot be evaluated (input documents resolve repo-root-relative)
⇒ exit 2 `could-not-evaluate` + `input_invalid`; without `--revision` ⇒ exit 0 `clean`.
Observed: `--root <live fixture> --revision ac46a747…` → `{"verdict":"could-not-evaluate","findings":[{"id":"input_invalid","reason":"git_command_failed","scope":"revision","command":"show ac46a7472d945a6d7ff135e4d7f07b0b6913d835:population.json"}]}` → **EXIT=2**; same root without
`--revision` → `clean`, **EXIT=0**. As declared ⇒ fixture 18's expectation *does* discriminate "no `--revision` ⇒ working
tree" (0 vs 2); a gate silently using Git mode would fail this fixture.

## Probe E — full live fixture suite via the frozen runner (read-only context)
`python3 -B <scratch>/frozen/citing_set_selftest.py --root <repo> --fixtures <repo>/scripts/fixtures/citing-set --gate <scratch>/frozen/citing_set.py --tmpdir <scratch>/tmp --min-cases 12`
stdout `{"verdict":"clean","passed":true,"cases":29,"failed":0,"failedCases":0,"meetsContractMinimum":true}` → **EXIT=0**;
fixture-18 row `ok:true`, expected `{exit:0, findings:[]}`, actual `{exit:0, verdict:clean, findings:[]}`.

## Findings by severity
1. **[LOW — latent interface ambiguity; not a fixture-18 mismatch]** `--revision` mode resolves input documents
   **repo-root-relative**, not `--root`-relative (`GitSource.read_document` → `git show <rev>:<relative>`,
   `scripts/citing_set.py:280-286`; `normalize_relative` rejects only `..`/absolute paths). With `--root` = a repo
   sub-directory (the fixture layout) git mode returns `could-not-evaluate` / exit 2 (`input_invalid`,
   `reason=git_command_failed`) instead of evaluating (Probe D). No contract text pins this and no fixture exercises it,
   so nothing fails — but a future C2 measurement combining a sub-directory `--root` with `--revision` would silently
   yield exit 2 rather than a measurement; L1 should state the intended `--root`-vs-repo-root relation.
2. **[LOW — suite-wide verification gap]** `expected.json` and the runner (`scripts/citing_set_selftest.py:239-266`) compare only the
   **exit code** and the **sorted multiset of finding ids**; finding `row`/`file` identity is not expressible and never
   compared, so a gate mislabeling rows/files would still pass all 29 cases. Fixture 18 exposes nothing here (its
   expectation is an empty multiset; its sole pair identity I verified from the inputs and Probe C's report fields).
3. **[INFO — scope interpretation, not a defect]** Population row `S002` is cited nowhere and yields no finding: consistent with
   the contract's pair-relative finding kinds and `expected.json` exit 0, but the fixture does not test a population row
   with no citation at all. The alternative reading ("every population row must carry an adjudication") is not implemented
   and is not claimed by any finding id. Boundary flagged for L1, not a failure.
4. **[INFO — working-tree artifact]** An untracked `scripts/__pycache__/citing_set.cpython-314.pyc` appeared in the repo tree (mtime
   19:01:57). Every command I ran used `python3 -B`, which never writes bytecode, so it was not produced by my probes
   (likely a sibling seat's `import citing_set`); the same pattern already exists under `.ufo/waves/round-2{6,7}/__pycache__/`.
   Build artifact, not a source change; left untouched rather than interfere with a concurrent seat.

## Residual risk / verification gaps
- Only fixture 18 was attacked (lane scope); the other 28 cases and the 16/16 C2 oracle measurement were **not** re-verified
  by me. Probe E shows the suite currently exits 0 (29/29) — context, not my claim.
- No `--revision` C2 measurement was re-run against the real corpus (out of lane scope); the git-mode path was probed only
  on the fixture layout (Probe D).
- Live fixture + gate + runner hashes re-verified identical to the candidate blobs after all probes; `git status` shows only
  pre-existing untracked wave artifacts plus this report (and the `__pycache__` item in Finding 4).
- No corpus/knowledge file, ledger, population, expected.json, source file, registry, MANIFEST or wave state was edited
  anywhere; all writes are this report plus scratch under `/fast/scratch/hyaku/kake-r27/AttackCase18/`.
- No installs performed (no tool/channel change to record). No `/tmp` or `/dev/shm`; `TMPDIR` exported explicitly.
- **Verdict on the attacked item: fixture 18's `expected.json` is CORRECT** — independently derived (exit 0, findings ∅),
  confirmed by the real frozen gate and the real consumer runner, and a one-line input mutation produced exactly the
  declared, causally-derived red outcome (exit 1, one `unadjudicated_citing_pair`, row `S002`, file
  `corpus/knowledge/mirror-pitfalls.md`). No disagreement between my derivation, `expected.json`, and observed behavior.
