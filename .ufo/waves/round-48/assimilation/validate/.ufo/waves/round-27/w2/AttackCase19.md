# AttackCase19 — consumer fixture `19-mixed-positive-negative-controls` (r27 fresh falsification)

Seat: `KakeR27.AttackCase19` (leaf, read-only source seat). Frozen candidate: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
Axis judged: **operability** (C2 gate + its fixture consumer contract). Scratch root: `/fast/scratch/hyaku/kake-r27/AttackCase19/`.
Attacked item: `scripts/fixtures/citing-set/19-mixed-positive-negative-controls/` consumed by `scripts/citing_set.py` via `scripts/citing_set_selftest.py`.

## 0. Frozen-identity check (before any execution)

`git rev-parse ac46a74^{commit}` → `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (resolves).
`git rev-parse ac46a74:scripts/citing_set.py` = `352a471abec08daa56a0fb7ef23fe78f2930d773` = `git hash-object scripts/citing_set.py` (worktree) — **equal**.
`git cat-file blob 352a471a… | sha256sum` = `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` = `sha256sum scripts/citing_set.py` — **equal** (byte-identical to candidate).
Runner: blob `c69b09b2e47f4115aa4e8ff286aa7cfe0e171a64`; sha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` = worktree — **equal**.
Fixture blobs at candidate == worktree `git hash-object` for all five files (expected `697284349fb313d945212714dbb71feb80c5e1a9`, ledger `d651cd03f7c41ff3c04c83824d8182633719d725`, population `6cd6a1f77bd98c1be9ff7f7f0e5d261328e03102`, alpha `1d5c477c0383044dbbc8dcc45c4581113028cb98`, beta `bfb41aa026be5685ba18ac1cc1fe171402ecc46c`) — fixture **not rewritten**.
Scratch copies (never the live fixture): `case19-pristine/` (sha256 ledger `5ac8127c92dae830a26afdfea8653510cdc2e6cce8555709c1f94e26f5ecd022`) and `case19-mutant/`.

## 1. Independent derivation (before reading any gate output)

Method: read the three fixture inputs + the published grammar in `contract.json`/`citing_set.py` docstring, then re-implement expansion in a throwaway scanner (`independent_scan.py`, sha256 `e5b77f4067edd8fa4849f925b2b4b626b087d91c9146d2b18b931f55215be924`) that never imports the gate.

Population = S001..S006. Cited tokens/ranges found: `alpha-entry.md` line 1 `S002–S005` (en dash, one range, start=2 end=5), literal `S001`, `S006`; `beta-entry.md` literal `S003`. Only one range in the whole corpus; no id outside the population.
Expanded citing set = 7 pairs: S001/S002/S003/S004/S005/S006 @ `corpus/knowledge/alpha-entry.md` + S003 @ `corpus/knowledge/beta-entry.md`.
Ledger = 8 entries / 7 distinct: (S001,alpha)×2, (S002,alpha), (S003,alpha), (S004,alpha), (S005,alpha), (S003,beta), (S002,beta).

**Declared expected result before running the gate (probe 1):** exit `1` (verdict `failed`), `citingPairs=7`, `ledgerPairs=8`, findings exactly 3, sorted id multiset `["ledger_duplicate_pair","ledger_pair_not_cited","unadjudicated_citing_pair"]`, with row/file identity: `ledger_duplicate_pair` = S001 / `corpus/knowledge/alpha-entry.md` / occurrences 2; `ledger_pair_not_cited` = S002 / `corpus/knowledge/beta-entry.md`; `unadjudicated_citing_pair` = S006 / `corpus/knowledge/alpha-entry.md`.
This matches `expected.json` `{exit:1, findings:[ledger_duplicate_pair, ledger_pair_not_cited, unadjudicated_citing_pair]}` — agreement on ids **and** on row/file/occurrences.

## 2. Probe 1 — real frozen gate CLI on the scratch copy, from an unrelated cwd

`cd / && TMPDIR=$S python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py --root $S/case19-pristine --population population.json --ledger ledger.json --json`
stdout (verbatim): `verdict failed`, `citingPairs 7`, `ledgerPairs 8`, `populationRows 6`, `corpusFiles 2`, `outsidePopulation 0`, `source working-tree`, findings: `ledger_duplicate_pair{S001, corpus/knowledge/alpha-entry.md, occurrences 2}`, `ledger_pair_not_cited{S002, corpus/knowledge/beta-entry.md}`, `unadjudicated_citing_pair{S006, corpus/knowledge/alpha-entry.md}`. **Exit 1.**
Disagreement with my independent derivation: **none** — ids, row, file, occurrences and both counts agree exactly. No disagreement with `expected.json`.

## 3. Probe 2 — one causally meaningful input change (declared before running)

Change (single file, scratch only): in `case19-mutant/ledger.json` the **second** ledger entry (the duplicate of S001/alpha) is re-pointed to row `S002`, file `corpus/knowledge/beta-entry.md`; every other byte identical (`diff` shows 2 changed lines only). Rationale: make the duplicated pair a pair that is **not** cited, so the duplicate and the not-cited finding must be emitted for the *same* (row,file) — this exercises the two independent finding loops and per-pair duplicate scoping.
**Declared expected result before running:** exit still `1`; `citingPairs 7`, `ledgerPairs 8`; findings still exactly 3, id multiset unchanged `["ledger_duplicate_pair","ledger_pair_not_cited","unadjudicated_citing_pair"]`; but identity must move: `ledger_duplicate_pair` → S002 / `corpus/knowledge/beta-entry.md` / occurrences 2; `ledger_pair_not_cited` → S002 / `corpus/knowledge/beta-entry.md`; `unadjudicated_citing_pair` → unchanged S006 / `corpus/knowledge/alpha-entry.md`.
Actual: identical to declaration — exit 1, findings as declared above (mutant ledger sha256 `ec4f0b1d0c15f326b35d3c19faca4a56bae98843563728bc5e751ad5b22b6ac4`). No defect surfaced: both finding classes are emitted for one duplicated, uncited pair.

## 4. Probe 3 — the fixture *consumer* (runner) against the mutated case

`python3 -B scripts/citing_set_selftest.py --root <repo> --fixtures $S/mutant-fixtures --tmpdir $S/selftest-tmp-mut` → **exit 0, verdict "clean", cases 1, failed 0**, case 19 `ok: true`, expected == actual id multiset.
**Declared expected:** runner passes, because `expected.json` pins only the id multiset + exit and the mutated case keeps both. Confirmed: the row/file identity of two of the three findings moved (S001/alpha → S002/beta) and the oracle still reports clean. This is an oracle **discriminating-power limit**, not a gate defect.

## 5. Probe 4 — real full selftest (unmutated, live fixtures, read-only)

`python3 -B scripts/citing_set_selftest.py --root <repo> --tmpdir $S/selftest-tmp` → **exit 0**, `verdict clean`, `cases 29`, `failed 0`, `meetsContractMinimum true`; case 19 row: expected == actual `["ledger_duplicate_pair","ledger_pair_not_cited","unadjudicated_citing_pair"]`, exit 1.
Operability note: `citing_set.py --selftest` **cannot forward `--tmpdir`** — the gate's own argparse rejects it (`citing_set.py: unrecognized arguments: --tmpdir …`, exit **64**). The sibling must be invoked directly to redirect TMPDIR; the gate's `--selftest` path otherwise always uses the shared default `/fast/scratch/hyaku/kake-r27` (no per-seat isolation). Cosmetic/hygiene, not a gate-correctness defect.

## 6. Probe 5 — counterfactual discriminating power of case 19 (`counterfactual.py`, sha256 `a385ba7c330cc48c54af5eea36d1bc0e155b213ea3c705c7af80cf8588caac26`)

* range expansion disabled → id multiset becomes `["ledger_duplicate_pair","ledger_pair_not_cited"×3,"unadjudicated_citing_pair"]` ≠ expected ⇒ case 19 **does** catch a range-expansion regression.
* population filter disabled → id multiset unchanged ⇒ case 19 alone **cannot** catch loss of the population filter (no out-of-population id in this fixture); cases 17/27 own that boundary.

## Findings by severity

1. **MEDIUM (oracle power, not gate defect).** `expected.json` (and the runner's comparison, which is exactly exit + sorted id multiset) does **not** pin row/file identity, `occurrences`, `citingPairs` or `ledgerPairs`. Proof: §3+§4 — a ledger change that moves the duplicate and not-cited findings from S001/alpha to S002/beta leaves the oracle green. A gate that mis-attributed the row or the file inside a finding (while keeping ids and exit) would pass all 29 cases. Recommended hardening (not applied — read-only seat): let `expected.json` optionally carry `{"id","row","file"}` triples and have the runner compare them when present.
2. **LOW (operability).** `citing_set.py --selftest` rejects `--tmpdir` with exit 64, so per-seat scratch isolation is unavailable through the gate's advertised self-test entry point; the runner's own `--tmpdir` works.
3. **NO-DEFECT.** No disagreement found between the frozen gate's observable behaviour and an independent derivation of the fixture's expected exit/finding multiset and row/file identity, for the pristine case and for the mutated case.

## Residual risk / verification gaps

* Case 19 does not exercise out-of-population ids, descending/oversize ranges, invalid JSON or shape errors — those are other cases' boundaries; I did not re-derive them here.
* Row/file identity was validated against **my** independent expansion of the published grammar; the grammar itself (range separators, token boundaries) is trusted from the frozen contract/docstring and was not re-derived from the r26 population rules.
* `--revision` mode was not exercised on this fixture: the fixture's ledger paths are fixture-root-relative, so a git-revision read would resolve `population.json` against the repo root, not the case dir. Left untested, not a claim.
* No tool was installed; no source, registry, MANIFEST or fixture file was modified (all writes were to `/fast/scratch/hyaku/kake-r27/AttackCase19/` and this report).
