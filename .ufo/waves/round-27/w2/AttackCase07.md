# AttackCase07 — consumer fixture `07-through-range-omission` (axis: operability)

**Attacked item:** `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/fixtures/citing-set/07-through-range-omission`
(the fixture producer's oracle + the runner `scripts/citing_set_selftest.py` that consumes it via the frozen gate `scripts/citing_set.py`).

**Frozen authority check (before any run):** `HEAD == ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; `git status --porcelain --untracked-files=no` empty (no tracked edits).
Gate blob sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` == sha256 of `scripts/citing_set.py` in the worktree == sha256 of `git cat-file blob ac46a747…:scripts/citing_set.py`. All four fixture files byte-identical to the candidate blobs (expected `a8829336…`, ledger `8d91add0…`, population `6cd6a1f7…`, corpus `3acfb62e…`). Live fixture left unmodified (ledger still `578f8936…` at end of run).

**Axes named:** operability — (a) does the oracle match an independently derived truth, (b) is the oracle sensitive (non-vacuous), (c) is the red condition causally attributable to the fixture's own input feature.

---

## 0. Independent derivation — made BEFORE reading any gate output

Inputs read: `population.json` rows `S001,S002,S003,S004,S005,S006`; `corpus/knowledge/keeper-timer-inert.md` (the only corpus file; exactly one citation line, ASCII, `Rows S001 through S006 were re-fetched by one public GET each and judged HOLD`); `ledger.json` pairs `S001,S003,S004,S005,S006`, all `file = corpus/knowledge/keeper-timer-inert.md`.

Derivation by a **hand-rolled scanner written independently of the gate's own regexes** (own token scan + own range scan, both in `eval`/heredoc, not the gate module): tokens found `S001`,`S006`; one range `S001 through S006` → expands to `S001..S006`; all six are population ids ⇒ **citing set = 6 pairs**; ledger = 5 pairs; `citing − ledger = {(S002, corpus/knowledge/keeper-timer-inert.md)}`; `ledger − citing = ∅`; no duplicate ledger pairs.

**Declared expected (mine, pre-run):** exit **1**; finding-id multiset `["unadjudicated_citing_pair"]` ×1; **row `S002`, file `corpus/knowledge/keeper-timer-inert.md`**; no `ledger_pair_not_cited`, no `ledger_duplicate_pair`, no `citation_range_invalid`, no `input_invalid`.

`expected.json` claims `exit 1, findings ["unadjudicated_citing_pair"]` ⇒ agrees on exit and id tally. `expected.json` carries **no row/file**, so row/file identity could not be checked against the oracle and was checked against my derivation instead.

---

## Probe 1 — baseline: real frozen gate CLI, scratch copy, unrelated cwd

**Declared expected before running:** exit 1; exactly one finding `unadjudicated_citing_pair`, row `S002`, file `corpus/knowledge/keeper-timer-inert.md`; `citingPairs 6`, `ledgerPairs 5`.

Scratch copy of the fixture (byte-identical, sha256s equal to the live fixture) at `/fast/scratch/hyaku/kake-r27/AttackCase07/scratch`; cwd `/fast/scratch/hyaku/kake-r27/AttackCase07/cwd` (unrelated to the fixture); `TMPDIR=/fast/scratch/hyaku/kake-r27/AttackCase07/tmp`.

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --root /fast/scratch/hyaku/kake-r27/AttackCase07/scratch \
  --population population.json --ledger ledger.json --json
```
stdout: `verdict failed`, `citingPairs 6`, `ledgerPairs 5`, `populationRows 6`, `corpusFiles 1`, `outsidePopulation 0`, `source working-tree`,
`findings:[{"id":"unadjudicated_citing_pair","row":"S002","file":"corpus/knowledge/keeper-timer-inert.md"}]` — **EXIT=1**.

**Agreement:** exact on exit, on finding-id multiset, **and** on row/file identity. No discrepancy.

## Probe 2 — ONE causally meaningful input change: adjudicate the omitted pair

**Change (scratch only):** append `{"row":"S002","file":"corpus/knowledge/keeper-timer-inert.md","statements":1,"stale":0,"report":"w1/PairS002Keeper-Timer-Inert.md"}` to `scratch/ledger.json` (5→6 pairs). Corpus, population, expected.json untouched. Mutated ledger sha256 `11d4df0fa0eb11a54410901ac13a979950af2c3c44e08c967a670aa50fb2b557`.

**Declared expected consequence:** the one omitted pair becomes adjudicated ⇒ `findings []`, `verdict clean`, **exit 0**; `citingPairs` stays 6; `ledgerPairs` 6; **no** `ledger_pair_not_cited` (S002 is still cited by the range) and no duplicate finding.

Actual stdout: `verdict clean`, `citingPairs 6`, `ledgerPairs 6`, `findings []` — **EXIT=0**. Conforms exactly.
⇒ the fixture's red condition is real, row-specific and *clearable*: no false positive, no residual that cannot be adjudicated.

## Probe 3 (supplementary) — is the finding caused by the `through` range?

**Change (separate copy `scratch3`):** corpus line `Rows S001 through S006 …` → `Rows S001 and S006 …` (corpus sha256 `5dc48382934e3e93d8c14d906752058defcec591218d31e68b2d58408435f48b`); ledger unchanged.
**Declared expected consequence:** the range no longer expands ⇒ citing set = `{S001,S006}` (2); `S002` leaves the citing set ⇒ **no** `unadjudicated_citing_pair`; ledger still holds `S003,S004,S005`, now uncited ⇒ 3 × `ledger_pair_not_cited` (rows S003,S004,S005, same file); exit 1.
Actual stdout: `verdict failed`, `citingPairs 2`, `ledgerPairs 5`, `findings` = exactly 3 × `ledger_pair_not_cited` rows S003/S004/S005 — **EXIT=1**. Conforms exactly.
⇒ the single finding is causally produced by range expansion through the word separator `through`; conversely a *range-blind* gate would emit 3 `ledger_pair_not_cited` here, so this oracle **does** discriminate range-awareness.

## Probe 4 — consumer sensitivity (the real runner)

`scripts/citing_set_selftest.py` (runner sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`):
- Pristine copy (`pristine/`): `verdict clean`, 1 case, `ok true`, expected `{exit 1, [unadjudicated_citing_pair]}` == actual `{exit 1, failed, [unadjudicated_citing_pair]}`.
- Probe-2 mutated copy (expected.json untouched): `verdict failed`, `ok false`, `reason "exit mismatch: expected 1, observed 0"` — the oracle is **not vacuous** and not merely green-shaped.
- Live fixture tree, read-only full-suite run: 29 cases, 0 failed, `verdict clean`, `gateSha256 3a361a00…` == frozen candidate blob. Case-07 row: `ok true`, expected == actual.

## Probe 5 (boundary) — separator matching is case-sensitive

`scratch5`: corpus line `Rows S001 Through S006 …` (sha256 `21cd9176674ab04233402c86205e14b0169bd5ad1ffd7a07f5618453c59de4c0`).
**Declared expected:** `Through` is not in the gate's declared separator list ⇒ no range ⇒ citing = 2 ⇒ **the S002 omission becomes undetectable** ⇒ 3 × `ledger_pair_not_cited`, exit 1. Actual: identical to Probe 3 (3 × `ledger_pair_not_cited`, exit 1). Confirmed.

---

## Findings (severity order)

1. **No defect in case 07 (operability).** The oracle matches my independent derivation on exit, id multiset **and** row/file identity; Probe 2 proves the red condition is exactly the S002 row and is clearable to clean; Probe 3 proves the finding is caused by the `through` range expansion; Probe 4 proves the consumer detects a deviation in either direction. Distinctiveness against the sibling separator fixtures is real: 03 `S001–S006` (4 findings), 04 `S001-S007`, 05 `S001..S006`, 06 `S001 to S006`, 07 `S001 through S006` (the only `through` fixture), 25 `S001—S006`, 23 glued `S001toS006`, 24 across-linebreak.
2. **Residual risk R1 (consumer-oracle blindness, contract-level, not a case-07 defect).** `expected.json` pins only `exit` + sorted finding **ids**; the runner compares exactly that (contract's fixtureInterface). A gate that emitted `unadjudicated_citing_pair` with the **wrong row** (e.g. `S003`) or wrong file would still pass case 07. I verified the row/file independently for this case and they are correct, but the consumer cannot detect such a regression. Owner: fixture producer / contract (an id+row+file oracle). No change proposed by this seat; L1 decision.
3. **Residual risk R2 (coverage narrowness, low).** Case 07's oracle is a 1-element id multiset, so it exercises only the singleton-multiplicity path (multiplicity is covered by 03 with 4 and 23 with 3). It also cannot express the case-sensitivity boundary of Probe 5; no fixture contains a capitalized separator and the real corpus (64 files) uses only hyphen (13) and en dash (21) separators — no word separator at all — so that boundary carries no current operational exposure, only a fixture-suite coverage note.
4. **Verification gaps.** (i) Case 07 is only meaningful in working-tree mode; the gate's `--revision` mode scans `<root>/corpus/knowledge` of a *different* corpus (the real 64-file corpus), so fixture scope cannot be re-exercised in git mode — the git-mode path is covered by other seats, not by this fixture. (ii) I did not evaluate whether the real-corpus git-mode run agrees with `frozen/expected.json` (outside this seat's scope). (iii) No mutation of source was performed by this seat; mutation seats own that.

**Statement of scope:** source read-only; all writes confined to `/fast/scratch/hyaku/kake-r27/AttackCase07/**` and this report. Live fixture, repo, git index, state/manifest files untouched (tracked-file status empty at end of run). No tool installs (none needed). No r24 material read or re-run.
