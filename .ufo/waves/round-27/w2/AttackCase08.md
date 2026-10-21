# AttackCase08 — fresh falsification of consumer fixture `08-comma-list-omission`
Seat: leaf reviewer (no dispatch). Axis: **operability**. Milestone: r27-fresh-falsification.
Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (`HEAD` == candidate). Source read only at candidate: `git ls-tree ac46a74` → gate blob `352a471abec08daa56a0fb7ef23fe78f2930d773`, runner blob `c69b09b2e47f4115aa4e8ff286aa7cfe0e171a64`; working-tree sha256 gate `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`, runner `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` — byte-identical to `git cat-file -p ac46a74:scripts/citing_set.py`. Contract: `.ufo/waves/round-27/contract.json` (C2 gate/fixture interface).
**Attacked item** (read-only, live fixture): `scripts/fixtures/citing-set/08-comma-list-omission/` — `population.json` (rows S001,S002,S003); `ledger.json` (pairs (S001,corpus/knowledge/ghp-served-set.md), (S003,corpus/knowledge/ghp-served-set.md)); `corpus/knowledge/ghp-served-set.md` (single front-matter line `source: S001, S002, S003 (corpus/SOURCES.md) …`); `expected.json` (`exit 1`, `findings ["unadjudicated_citing_pair"]`). Input sha256 (all == candidate blobs): expected `49d7286dd34a00ce88a31d473272e589cb55442e76d60505cd9591437ee353e81`, ledger `3a4c858abe585fa8c3ce41ee39b97b87f3913dd2b63ca313d178e6880711eee5`, population `508e2eccc8a37939f7743ad0de9a9904b79bc5e7c5d9691da17bfe5c28c5dce6`, corpus `4b540d5e4bb55a2f561c959c8252065abc9190e076a0fa882040856d0f280f93`.

## Independent derivation (declared BEFORE any gate run)
Grounding = contract C2 semantics (token `S`+≥3 digits; range separators `-`,`–`,`—`,`..`,`to`,`through`; ascending; span ≤200; population rows only; citing pair absent from ledger ⇒ `unadjudicated_citing_pair`; ledger pair outside the citing set ⇒ `ledger_pair_not_cited`) + fixture bytes. My own sweeps, regexes written independently of the gate:
- literal-token sweep → `S001`,`S002`,`S003` (comma is NOT a declared separator ⇒ a comma list is three independent literal citations); range sweep → **zero** ranges.
- ⇒ citing set {S001,S002,S003} × `corpus/knowledge/ghp-served-set.md` ⇒ **citingPairs 3**, outsidePopulation 0, no `citation_range_invalid`, no `input_invalid`.
- ledger = 2 distinct pairs, no duplicate ⇒ **ledgerPairs 2**, no `ledger_duplicate_pair`; both ledger pairs inside the citing set ⇒ no `ledger_pair_not_cited`; citing − ledger = {S002} ⇒ exactly **one** finding: id `unadjudicated_citing_pair`, row **S002**, file `corpus/knowledge/ghp-served-set.md`.
- **Declared expected: exit 1, verdict `failed`, id multiset {`unadjudicated_citing_pair`} ×1, row/file S002 / corpus/knowledge/ghp-served-set.md, citingPairs 3, ledgerPairs 2.**
- Honest disclosure: `expected.json` was read during fixture inventory, i.e. *before* this derivation. Mitigation: the derivation is reproducible from input bytes + contract grammar alone (sweeps returned TOKENS `['S001','S002','S003']`, RANGES `[]`) and fixes row/file identity and pair counts that `expected.json` does not encode; Probe B's declared expectation differs from `expected.json`, so it cannot be produced by parroting the fixture.

## Probe A — real frozen gate CLI, scratch copy, unrelated cwd
Declared expected: exit 1, one `unadjudicated_citing_pair`, row S002, file corpus/knowledge/ghp-served-set.md.
Scratch copy `/fast/scratch/hyaku/kake-r27/attackcase08/base` (copy of live fixture; corpus bytes identical `4b540d5e…`).
```
cd /fast/scratch/hyaku/kake-r27/attackcase08        # unrelated cwd (not the repo, not the fixture parent)
TMPDIR=/fast/scratch/hyaku/kake-r27/attackcase08/tmp python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --root base --population population.json --ledger ledger.json
```
stdout (verbatim): `{"verdict": "failed", "citingPairs": 3, "ledgerPairs": 2, "findings": [{"id": "unadjudicated_citing_pair", "row": "S002", "file": "corpus/knowledge/ghp-served-set.md"}], "populationRows": 3, "corpusFiles": 1, "outsidePopulation": 0, "source": "working-tree", "revision": null}` → **EXIT=1**, stderr 0 bytes.
Every derived quantity matches: verdict, exit, id multiset (×1), row S002, file corpus/knowledge/ghp-served-set.md, citingPairs 3, ledgerPairs 2, outsidePopulation 0.

## Comparison with expected.json (id multiset AND row/file identity)
- id multiset: observed `["unadjudicated_citing_pair"]` vs expected `["unadjudicated_citing_pair"]` → equal; exit observed 1 vs expected 1 → equal.
- row/file identity: observed row `S002`, file `corpus/knowledge/ghp-served-set.md` — exactly the comma-list member absent from the ledger → agrees with the independent derivation, not merely with the id tally. **No disagreement found.**
- (`expected.json` itself carries no row/file, so the identity check is mine — see F-1.)

## Probe B — ONE causally meaningful input change (declared before running)
Mutation (scratch copy `/fast/scratch/hyaku/kake-r27/attackcase08/mut` only): in `corpus/knowledge/ghp-served-set.md` line 1 drop the middle comma-list member → `source: S001, S003 (corpus/SOURCES.md) …`; all else byte-identical.
Pristine corpus sha256 `4b540d5e4bb55a2f561c959c8252065abc9190e076a0fa882040856d0f280f93` → mutant `34530f2d87a5ff569d61eb101249ac6566050ca6d0fea5cf053c1e9ef67b25eb`.
**Declared expected consequence:** S002 no longer cited ⇒ citing set shrinks to {S001,S003} ⇒ both ledger pairs cited, nothing missing, nothing extra ⇒ verdict `clean`, `findings []`, citingPairs 2, ledgerPairs 2, **exit 0**. Had the gate still reported a finding for S002 (or any finding), the fixture's red condition would not be caused by the S002 omission — falsification.
```
cd /fast/scratch/hyaku/kake-r27/attackcase08
TMPDIR=/fast/scratch/hyaku/kake-r27/attackcase08/tmp python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --root mut --population population.json --ledger ledger.json
```
stdout: `{"verdict": "clean", "citingPairs": 2, "ledgerPairs": 2, "findings": [], "populationRows": 3, "corpusFiles": 1, "outsidePopulation": 0, "source": "working-tree", "revision": null}` → **EXIT=0**, stderr 0 bytes.
**Matches the declared expectation exactly.** The red condition of fixture 08 is therefore genuinely caused by the omitted S002 member, not by a canned or shape-driven response.

## Consumer-level evidence (real runner, real gate subprocesses)
- Runner over a scratch copy of this single case (`scripts/citing_set_selftest.py --fixtures <scratch>/fixtures --gate <repo>/scripts/citing_set.py --tmpdir <scratch>/tmp --min-cases 1`): `verdict clean, passed true, cases 1, failed 0`; case result `ok true`, expected `{exit 1, findings ["unadjudicated_citing_pair"]}` vs actual `{exit 1, verdict failed, findings ["unadjudicated_citing_pair"]}`.
- Runner over the live fixture directory (read-only): `cases 29, failed 0, failedCases 0`, `08-comma-list-omission` present and passing (gate sha256 `3a361a00…`, runner sha256 `3c167895…`).

## Findings by severity
- **F-1 (low, harness coverage gap, not a defect of this fixture):** the consumer oracle compares only exit code and sorted finding-id multiset (`scripts/citing_set_selftest.py` `run_case`: `observed != sorted(expected["findings"])`), and `expected.json` carries no row/file; 12 of 29 fixtures share one byte-identical `expected.json` (`49d7286d…`: cases 02,04,05,06,07,08,09,10,22,24,25,27). A finding attributed to the *wrong* row/file would pass the whole suite. Mitigation in this seat: Probe A inspected row/file identity and matched the independent derivation. Wave-wide observation; no fixture edit made by me.
- **F-2 (informational, no defect):** the comma is not a declared range separator, so the fixture's omitted list member is correctly reported as exactly one `unadjudicated_citing_pair` with row S002; derived expectation, observed gate output and `expected.json` agree — id tally, row and file all.
- **No blocking or high-severity finding for this fixture.** No failed finding rescoped; expected output not rewritten.

## Residual risk / verification gaps
- Exactly one input mutation performed (comma-list member removal). Not probed: ledger-side completion (adding an S002 pair ⇒ expect clean), other list spellings (`and`, `;`), an out-of-population list member (S004 ⇒ one finding + outsidePopulation 1), ledger file-path mismatch, and the `GitSource` (`--revision`) path — the fixture interface is working-tree mode, so `--revision` was not exercised for this case. Adjacent obligations, outside this seat's scope.
- Pair presence ≠ semantic support: this seat verified gate behaviour only (row/file/exit algebra); whether the S001/S003 adjudications are semantically supported is out of scope and not asserted.
- `expected.json` was read before the derivation (disclosed); Probe B's declared expectation differs from it. No HTTP/auth surface involved; no policy-stop; no r24 material read or replayed.

## Hygiene
- No live source or fixture writes. Live sha256 after all probes unchanged: expected `49d7286d…`, ledger `3a4c858a…`, population `508e2ecc…`, corpus `4b540d5e…`, gate `3a361a00…`, runner `3c167895…`; `git status --porcelain` on those paths empty.
- Scratch only under `/fast/scratch/hyaku/kake-r27/attackcase08/`; `TMPDIR` set explicitly; no `/tmp`, no `/dev/shm`, no background jobs, no dispatch, no commit/index/remote operations.
- Stray untracked `scripts/__pycache__/citing_set.cpython-314.pyc` appeared at 19:01 during this wave; every command of this seat ran `python3 -B`, so it was not produced by my runs — left untouched (not mine to delete).
- No tool/package installs needed or performed; no build, lint or formatter run.
