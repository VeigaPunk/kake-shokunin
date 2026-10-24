# AttackCase02 — consumer fixture `02-single-literal-missing`

Seat KakeR27.AttackCase02 (leaf, fresh falsification, axis operability). Target: live fixture
`scripts/fixtures/citing-set/02-single-literal-missing` (read-only).
Gate `scripts/citing_set.py` sha256 `3a361a00…ffc228`; runner `scripts/citing_set_selftest.py` sha256 `3c167895…d62a1c`.

## 0. Frozen-source check (before reading behaviour)
`git rev-parse HEAD` → `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` = frozen candidate.
`git hash-object` of gate + all 5 fixture files == candidate tree blobs (gate 352a471a…, population
a716bd2a…, ledger b9c88538…, expected a8829336…, cadence-log 927b6136…, publish-queue 883a0bd1…).
Source read == candidate source; no live edit made.

## 1. Independent derivation (from fixture input + contract, before running any gate)
Hand-read inputs: `population.json` rows {S001,S002}; `ledger.json` pairs
{(S002, corpus/knowledge/cadence-log.md)}; corpus/knowledge holds exactly `cadence-log.md` (cites
S002 only) and `publish-queue.md` (cites S001 only); no other S-token and no range form in either.

Declared before running: exit **1**, verdict `failed`, id multiset **{unadjudicated_citing_pair ×1}**
for row **S001** / file **corpus/knowledge/publish-queue.md**; citingPairs 2, ledgerPairs 1,
corpusFiles 2, populationRows 2, outsidePopulation 0. Reason: cited pairs =
{(S001,publish-queue.md),(S002,cadence-log.md)}; ledger covers only (S002,cadence-log.md) →
(S001,publish-queue.md) unadjudicated; ledger pair is itself cited → no `ledger_pair_not_cited`; no duplicate.

`expected.json` (read after the derivation): exit 1, findings ["unadjudicated_citing_pair"] —
**agrees** on exit and id multiset. It carries no row/file fields, so it cannot witness identity (§4.2).

## 2. Base run — real frozen gate CLI, scratch copy, unrelated cwd
Scratch copy `/fast/scratch/hyaku/kake-r27/AttackCase02/fx/02-single-literal-missing`; TMPDIR/TMP/TEMP
= `/fast/scratch/hyaku/kake-r27/AttackCase02/tmp` (no /tmp, no /dev/shm); gate cwd = the AttackCase02
scratch dir (unrelated to the fixture).

```
python3 -B <repo>/scripts/citing_set.py --root <scratch>/fx/02-single-literal-missing \
  --population population.json --ledger ledger.json --json
```
Exit **1**; stdout: `verdict failed`, `citingPairs 2`, `ledgerPairs 1`, `populationRows 2`,
`corpusFiles 2`, `outsidePopulation 0`, `source working-tree`, one finding
`{id: unadjudicated_citing_pair, row: S001, file: corpus/knowledge/publish-queue.md}`.
Observed == derived expectation, including **row/file identity** (S001 ↔ the file that cites it; the
ledger-covered pair S002/cadence-log.md is not reported). No disagreement.
Consumer runner on the same copy: `python3 -B <repo>/scripts/citing_set_selftest.py --root <repo>
--fixtures <scratch>/fx --gate <repo>/scripts/citing_set.py --tmpdir <scratch>/tmp --min-cases 1`
→ exit **0**, `verdict clean`, `cases 1, failed 0`, actual == expected. Runner note "fixture count 1
< contract minimum 12" is expected for a single-case probe.

## 3. Mutation — ONE causally meaningful input change
Scratch `ledger.json`: the single pair's `file` `corpus/knowledge/cadence-log.md` →
`corpus/knowledge/publish-queue.md` (right row, wrong file). Ledger hash pristine
`b5049c2f80b0941160116859ba2e5221033d67f6b0036a60cac1211e7f0d9193` → mutant
`a7a30a2c51cd428db185959cfa14c23ead8acc8b101aab3d7918c49be7896553`. No other file touched.

Declared before running: the ledger entry now names a file that does not cite S002, so it adjudicates
nothing; (S002,cadence-log.md) becomes unadjudicated while (S001,publish-queue.md) stays
unadjudicated, and the ledger pair is not in the cited set → exit **1**, verdict `failed`, ids
**[ledger_pair_not_cited, unadjudicated_citing_pair, unadjudicated_citing_pair]** with
ledger_pair_not_cited=(S002, corpus/knowledge/publish-queue.md), unadjudicated=(S001,
corpus/knowledge/publish-queue.md) and (S002, corpus/knowledge/cadence-log.md); citingPairs 2,
ledgerPairs 1, outsidePopulation 0.

Actual: exit **1**, findings exactly those three with those rows/files and those counters —
**identical to the declared expectation**. The gate keys on the (row, file) **pair**, not the row:
a ledger entry with the correct row but a non-citing file adjudicates nothing. Runner on the mutated
copy: exit **1**, `verdict failed`, reason `finding-id mismatch: expected
["unadjudicated_citing_pair"], observed ["ledger_pair_not_cited","unadjudicated_citing_pair",
"unadjudicated_citing_pair"]` — the oracle is live and does not echo the declaration.

## 4. Findings
4.1 **No behavioural defect** in fixture 02 or the gate path it exercises: derived exit/id multiset
== `expected.json` == observed base run; row/file identity correct; mutation moved the outcome
exactly as predicted, including multiset growth to three findings.
4.2 **Low severity, oracle coverage gap (fixture design, not gate defect).** `expected.json` holds
only `{exit, findings:[ids]}` and the runner compares only exit + sorted finding **ids**
(`citing_set_selftest.py:144-161`, `run_case` 210-290). Row/file are never compared, so a gate
reporting the wrong row/file under the same id would still pass this and every fixture; no
fixture-level identity oracle exists. §2/§3 supply that witness for this case only.
4.3 **Hash note.** This `expected.json` blob (`a8829336…`) is byte-identical to fixtures 04–10
(one unadjudicated pair each) and differs from 03/13/14 (`a27e7df2…`) and 01/12
(`34c54d14…`/`502c20bb…`). Consistent with the contract shape, but the expectation file carries no
per-case discrimination; discrimination lives in the input, and identity is unasserted (4.2).

## 5. Residual risk / verification gaps
- Only the single literal-pair branch probed; range/list/metadata/EOF/duplicate/outside-population
  and input-failure branches are other seats' scope.
- One mutation only (as assigned). Not probed here: population edits (dropping S001 would hide the
  omission as outsidePopulation), ledger row-spelling variants (S0001 vs S001), `--revision` blob
  mode for these inputs.
- Mutation ran in working-tree source mode only; GitSource equivalence not exercised here.
- Live fixture/source untouched: post-run sha256 of all 5 live fixture files identical to pre-run;
  HEAD still `ac46a747…`; `git status --porcelain` shows no tracked modification (only pre-existing
  untracked wave artifacts). All scratch material under `/fast/scratch/hyaku/kake-r27/AttackCase02/`.
- No tool installs required or performed in this seat.
