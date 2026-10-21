# AttackCase25 — consumer fixture `25-em-dash-range-omission` (r27 fresh falsification)

Lane: reviewer leaf (no dispatch). Axis: operability. Milestone: r27-fresh-falsification.
Candidate (explicit, never bare HEAD): `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
Writable area used: `/fast/scratch/hyaku/kake-r27/attackcase25/` only (TMPDIR exported explicitly; no `/tmp`, no `/dev/shm`).
Source, live fixture and repo files read-only, re-hashed unchanged after all runs (§7). No installs performed (none needed).

**Attacked item:** fixture `scripts/fixtures/citing-set/25-em-dash-range-omission/` consumed by the real frozen gate
`scripts/citing_set.py` (`--root <dir> --population <rel> --ledger <rel> --json`); contract
`.ufo/waves/round-27/contract.json` → `gateInterface`; oracle `.ufo/waves/round-27/oracle-implementation-corrections.json`
(expected outcome files unchanged).

**Authority before any run** — sha256 identical across worktree, `git show ac46a747:<path>` and frozen-candidate.json `sourceFiles` (all MATCH):
gate `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` · runner `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265885dd62a1c`
· fixture corpus `c9811b66b07ca30a559e228a51f8eeac5549556a68ce461df65c88e4c91cee34` · `expected.json` `49d7286dd34a00ce88a31d473272e589cb5542e76d60505cd9591437ee353e81`
· `ledger.json` `b4aaa56a604133a8db2a256f72db2e3cee3a0632d4d2c71ad23842eefc34d9d8` · `population.json` `f04a4f37f256034f70f29b7b0aade3d87a498b42a01a85bc454d51ddc3b272f6`.

## Probe A — independent expectation declared BEFORE reading any gate output

Inputs read directly from disk (not from `expected.json`): `population.json` rows = S001,S002,S003,S004,S005,S006 (6).
Corpus (only file `corpus/knowledge/free-read-verbs.md`): exactly two literal `S<digits>` tokens, `S001` and `S006`, joined by
**em dash U+2014** (bytes `e2 80 94`, hexdump-verified); the string `S004` occurs nowhere in the file.
`ledger.json` pairs = rows S001,S002,S003,S005,S006 on file `corpus/knowledge/free-read-verbs.md`; **S004 absent**; no row repeated.
Contract grammar: range = two ids joined by `-`, `–`(U+2013), `—`(U+2014), `..`, `to`, `through`, expanded inclusively; only population ids count.
Derived for the pristine fixture: expanded citing set = {S001..S006} × that file → **6 pairs**; ledger ∩ citing = 5; ledger \ citing = ∅
(no `ledger_pair_not_cited`); no duplicates; range ascending, span 5 ≤ 200 (no `citation_range_invalid`); all ids in population
(`outsidePopulation` 0); citing \ ledger = exactly `(S004, corpus/knowledge/free-read-verbs.md)` → **exactly one finding, id
`unadjudicated_citing_pair`**; verdict `failed`; **exit 1**; `citingPairs` 6, `ledgerPairs` 5. Expected id multiset = `{unadjudicated_citing_pair: 1}`.
Compared to `expected.json` (read only after the derivation): `{exit:1, findings:["unadjudicated_citing_pair"]}` → multiset matches exactly.
`expected.json` pins exit+ids only, so **row/file identity was checked independently** (below), not inferred from the expectation.

## Probe A — actual command / stdout / exit

```
cp -a <live fixture>/. /fast/scratch/hyaku/kake-r27/attackcase25/base/ ; cd /fast/scratch/hyaku/kake-r27/attackcase25/tmp   # unrelated cwd
TMPDIR=/fast/scratch/hyaku/kake-r27/attackcase25/tmp \
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --root /fast/scratch/hyaku/kake-r27/attackcase25/base --population population.json --ledger ledger.json --json
```
stdout verbatim (stderr empty), exit code **1**:
```json
{ "verdict": "failed", "citingPairs": 6, "ledgerPairs": 5,
  "findings": [ { "id": "unadjudicated_citing_pair", "row": "S004",
                  "file": "corpus/knowledge/free-read-verbs.md" } ],
  "populationRows": 6, "corpusFiles": 1, "outsidePopulation": 0,
  "source": "working-tree", "revision": null }
```
Observed vs declared: exit ✔1, verdict ✔failed, `citingPairs` ✔6, `ledgerPairs` ✔5, id multiset ✔`{unadjudicated_citing_pair:1}`.
**Row/file identity ✔**: row `S004` = exactly the ledger-omitted id and the range-interior id that appears nowhere literally in
the file; file = the only corpus file, equal to the ledger's file field after normalisation. No disagreement.
Consumer rerun (real fixture runner over live fixtures, read-only): `python3 -B scripts/citing_set_selftest.py --tmpdir <seat>/tmp`
→ exit 0, `{"verdict":"clean","passed":true,"cases":29,"failed":0,"failedCases":0,"contractMinimumCases":12,"meetsContractMinimum":true}`;
case `25-em-dash-range-omission` → `ok:true`, expected = actual = `{exit:1, findings:["unadjudicated_citing_pair"]}`; runner-reported
gate digest `3a361a00…`, runner digest `3c167895…` (= candidate blobs).

## Probe B — ONE causally meaningful input change, expectation declared first

Mutation (scratch input only): range separator **em dash U+2014 → U+2015 HORIZONTAL BAR**, one byte at offset 14 (`0x94`→`0x95`),
length unchanged (490). Pristine sha256 `c9811b66b07ca30a559e228a51f8eeac5549556a68ce461df65c88e4c91cee34` → mutant sha256
`091e99b06852613c62b46b8bce17afdd1d27f8e830109c58d15599c27987a6f3`; ledger/population/expected untouched.
Declared expected consequence: U+2015 is not a declared separator, so the range is NOT expanded; but U+2015 is not a word character,
so `S001`/`S006` still match the literal-token rule → citing set {S001,S006}, `citingPairs` **2**; citing \ ledger = ∅ → **zero**
`unadjudicated_citing_pair` (the S004 obligation must vanish); ledger \ citing = {S002,S003,S005} → **3** `ledger_pair_not_cited`
(same file); no range finding; `ledgerPairs` 5; `outsidePopulation` 0; verdict `failed`; **exit 1**.
```
cd /fast/scratch/hyaku/kake-r27/attackcase25/tmp ; TMPDIR=… python3 -B <repo>/scripts/citing_set.py \
  --root …/attackcase25/mutant --population population.json --ledger ledger.json --json
```
stdout verbatim (stderr empty), exit code **1**:
```json
{ "verdict": "failed", "citingPairs": 2, "ledgerPairs": 5,
  "findings": [ { "id": "ledger_pair_not_cited", "row": "S002", "file": "corpus/knowledge/free-read-verbs.md" },
                { "id": "ledger_pair_not_cited", "row": "S003", "file": "corpus/knowledge/free-read-verbs.md" },
                { "id": "ledger_pair_not_cited", "row": "S005", "file": "corpus/knowledge/free-read-verbs.md" } ],
  "populationRows": 6, "corpusFiles": 1, "outsidePopulation": 0,
  "source": "working-tree", "revision": null }
```
Observed vs declared: exit ✔1, verdict ✔failed, `citingPairs` ✔2, `ledgerPairs` ✔5, `unadjudicated_citing_pair` count ✔0,
`ledger_pair_not_cited` count ✔3 with rows S002/S003/S005 and the expected file ✔, `outsidePopulation` ✔0. No discrepancy.

## What the observed runs establish (observed, not source-text asserted)

1. The fixture's red finding arises **solely** from em-dash range expansion: dropping the declared separator makes the S004
   obligation disappear, and `S004` occurs nowhere literally in the file — case 25 genuinely exercises the range-aware path.
2. The separator class is exactly as declared: an undeclared dash (U+2015) is **not** silently treated as a range (had it been,
   probe B would have reproduced probe A's single `unadjudicated_citing_pair`; it did not). Both comparison directions are
   exercised and correctly signed: missing → `unadjudicated_citing_pair` (A), surplus → `ledger_pair_not_cited` (B).
## Discrepancies / uncertainties
* **No discrepancy** between independent derivation, `expected.json` and real gate output — exit, finding-id multiset and
  row/file identity all agree (probes A and B).
* Recorded uncertainty, not asserted: `expected.json` encodes only exit + id multiset, so *which* row is missing is not pinned
  by the oracle; a variant fixture omitting a different row would still satisfy it — a property of the oracle format, not a
  defect of case 25. `expected.json` for case 25 is byte-identical to the hyphen/en-dash/`..`/`to`/`through` siblings
  (`49d7286d…`); the runner reports 29/29 clean, and the em-dash case stays independently discriminating per above.
* Residual risk / gaps: GitSource mode (`--revision <commit>`) not exercised for this fixture (contract fixture interface and
  runner use working-tree mode; other seats' cases); the single permitted mutation was spent on the separator-grammar boundary
  (higher value) so the "S004 appears literally" omission shape was not probed; C1 (`count_c1.py`) and the 16-pair oracle were
  not re-derived (out of scope: C2/operability).
* Integrity: post-run sha256 of gate, runner and all three live fixture files = identical to the authority list above;
  `git status --porcelain -- scripts/` empty. Scratch copies only; no source, fixture, ledger, registry, MANIFEST or sibling file written.
