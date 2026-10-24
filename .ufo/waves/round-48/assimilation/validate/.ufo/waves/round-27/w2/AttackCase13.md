# KakeR27.AttackCase13 — consumer fixture `13-descending-range` (fresh falsification, axis: operability)

Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; HEAD == candidate; tracked tree clean before and after (`git status --porcelain -uno` empty). All source read by explicit hash: working-tree blobs equal candidate blobs (`scripts/citing_set.py` 352a471a…, `scripts/citing_set_selftest.py` c69b09b2…, fixture-13 blobs 9cc9d582…/a27e7df2…/579185d1…/6cd6a1f7…). Scratch only: `/fast/scratch/hyaku/kake-r27/AttackCase13/` (TMPDIR set there; no /tmp, no /dev/shm). No source/docs/registry edits, no repo commits, no installs, no network.

## 1. Item attacked
Fixture `scripts/fixtures/citing-set/13-descending-range` — corpus `corpus/knowledge/kimi-subpath-audit.md` header line `source: S006–S001 (corpus/SOURCES.md) …` (en-dash U+2013, bytes `342 200 223`), `population.json` = rows S001–S006, `ledger.json` = pairs (S001, corpus/knowledge/kimi-subpath-audit.md) and (S006, same file), `expected.json` = {exit 1, findings ["citation_range_invalid"]}.

## 2. Independent derivation (declared BEFORE any gate output)
Read from the gate's *source* (read-only) plus the contract, not from any run:
- `_TOKEN_RE` scans literals independently of ranges; `_RANGE_RE` matches `S<3+digits>` + one of `- – — .. through to` + `S<3+digits>` → "S006–S001" is one range, start=6, end=1.
- `evaluate()`: `end < start` → appends finding `citation_range_invalid` (reason `descending_range`) and `continue`s — the range contributes **no** citation credit.
- The same text also yields two literal tokens S001 and S006 (both in population) → `citing` = {(S001,file),(S006,file)}; ledger holds exactly those two → no `unadjudicated_citing_pair`, no `ledger_pair_not_cited`, no duplicate.
- `input_errors` empty → verdict `failed`, exit 1; findings multiset = {`citation_range_invalid`} ×1.
**Derived expectation: exit 1, findings multiset [`citation_range_invalid`] ×1, citingPairs 2, ledgerPairs 2, outsidePopulation 0.** This agrees with the fixture's `expected.json` (id tally AND multiplicity 1). No disagreement.

## 3. Real frozen gate on a scratch copy, unrelated cwd
Scratch copies extracted with `git show ac46a747:…`; fixture dir = `…/AttackCase13/caseA/fixture`; gate = `…/gate/citing_set.py` (sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`).
`cd /fast/scratch/hyaku/kake-r27/AttackCase13 && TMPDIR=…/tmp python3 -B …/gate/citing_set.py --root …/caseA/fixture --population population.json --ledger ledger.json --json` → **exit 1**; stdout sha256 `7d8b2bf706ae8c0b5be0b4ca18821be6e6e02554d240abdb0b33b4c62150630e` (412 B), stderr empty:
`{"verdict":"failed","citingPairs":2,"ledgerPairs":2,"findings":[{"id":"citation_range_invalid","file":"corpus/knowledge/kimi-subpath-audit.md","range":"S006–S001","start":6,"end":1,"reason":"descending_range"}],"populationRows":6,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}`
**Identity check (not only the id tally):** the finding's `file` is the corpus file that actually contains the offending range (`corpus/knowledge/kimi-subpath-audit.md`, root-relative, matching the ledger's `file` spelling exactly → both ledger pairs resolved, hence zero `ledger_pair_not_cited`); `range`/`start`/`end` identify the exact offending token pair; the fixture's two ledger rows (S001, S006) each resolve to that one real document — no phantom row, no phantom file, no duplicate row spelling.

## 4. Shipped consumer (fixture runner) on the same scratch copy
`python3 -B …/gate/citing_set_selftest.py --root …/AttackCase13 --gate …/gate/citing_set.py --fixtures …/caseA --tmpdir …/tmp` → **exit 0**, verdict `clean`, 1 case, 0 failed; runnerSha256 `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`; case actual == expected (exit 1, ["citation_range_invalid"]). Note the runner invokes the gate with `cwd=case_dir` and `--root=case_dir`, while §3 ran from an unrelated cwd — resolution is root-relative, cwd-independent (operability positive).
**Negative control (proves the green is not vacuous / not a mock echo):** scratch copy with `expected.json` rewritten to `{"exit":0,"findings":[]}` → runner verdict `failed`, failedCases 1, reason `exit mismatch: expected 0, observed 1`, runner exit 1. The fixture's pass depends on the real exit+id comparison.

## 5. Second execution mode (git blobs) — read-only cross-check
Scratch git repo `caseC` containing the same fixture bytes (commit `982a7f25c8b9c68a6908362c3f6ec56013f7b78d`, disposable, outside the project repo): `python3 -B …/gate/citing_set.py --root …/caseC --revision 982a7f25… --population population.json --ledger ledger.json --json` → **exit 1**, verdict failed, `source":"git"`, same single finding `citation_range_invalid` / file `corpus/knowledge/kimi-subpath-audit.md` / range `S006–S001` / start 6 / end 1, citingPairs 2, ledgerPairs 2. Working-tree and git-blob modes agree.

## 6. ONE causal input change (independently declared consequence)
Change (scratch copy `caseB` only): corpus header `source: S006–S001` → `source: S001–S006` (en-dash preserved; endpoints swapped only). Pristine corpus sha256 `73866065f86365f5e90a6bd3d59dd52d91776e905cc3f7867c8190e39dfc49a8` → mutant sha256 `c61d618248fbeb1c9f5d0f4a5741c9ade88baebb2e371bd212324119dc5bd92f`; `diff` = that single line only; population/ledger/expected bytes untouched.
**Declared expected before running:** range now ascending (span 5 ≤ 200) → NO `citation_range_invalid`; range expansion enumerates S001..S006 → citingPairs 6; ledger still only S001+S006 → **exactly 4 × `unadjudicated_citing_pair` for rows S002, S003, S004, S005, file `corpus/knowledge/kimi-subpath-audit.md`**; no `ledger_pair_not_cited`, no duplicate; exit 1 (failed), outsidePopulation 0.
**Actual:** exit 1; stdout sha256 `6de9e9f5a6eca96d90d7400aeb31ae86a8850778802f252b48470e477ebb853d` (723 B), stderr empty → findings = 4 × `unadjudicated_citing_pair`, rows S002/S003/S004/S005, all file `corpus/knowledge/kimi-subpath-audit.md`; citingPairs 6, ledgerPairs 2, populationRows 6, corpusFiles 1, outsidePopulation 0. **Exact match with the declared expectation**, including row identity and multiplicity.
Causal meaning: the descending-range finding in §3 is produced by the range-validity branch, not by a fixed print; and a valid ascending range really does expand interior rows into citing obligations (the fixture's own corpus has no interior ledger rows, so §3 alone could not have distinguished "descending range skipped" from "ranges ignored"). Interior rows S002–S005 receive **no** credit from the descending range (§3 citingPairs 2 ⇒ only the two literal endpoints), which is the intended non-silent-expansion behaviour.

## 7. Discrepancies / uncertainties
- No disagreement between independent derivation, fixture `expected.json`, gate stdout, and runner verdict for fixture 13.
- Semantic-coherence note (not a gate defect, not a fixture failure): the ledger credits S001 and S006 from a file whose only citation form is a *descending group range* the gate itself declares invalid; credit survives only because literals are scanned independently of ranges (contract-consistent, `expected.json` still demands exit 1, so no false green is possible).
- Fixture 13's `expected.json` is byte-identical to fixture 14's (`a27e7df2…`); the two cases are behaviourally distinct (13 = descending, 14 = span 900 via `S001..S900`), only the finding id coincides. Not a defect.
- `citation_range_invalid` carries no `row` field (contract marks `row` optional; the finding spans two rows). Row-level attribution for range findings is not available — a reporting-granularity limit, not an incorrectness.

## 8. Residual risk / verification gaps
- The descending/oversize branch is **not exercised by the real corpus**: 8 ranges found across the 26 files of `corpus/knowledge`, 0 descending, 0 oversize. The branch is fixture-only, so it is proven by fixtures, not by production data; a real-corpus descending range would flip the C2 gate verdict to exit 1 without any of the 16 oracle omissions being implicated.
- Only one input mutation was performed (as scoped). Not probed for this fixture: a descending range whose endpoints lie outside the population; a ledger row spelled numerically differently for this file; `unadjudicated_citing_pair` vs `ledger_pair_not_cited` interplay here. Those belong to the other fixture seats.
- Fixture-13 cannot be exercised in `--revision` mode against the project repo (git mode resolves `rev:<path>` from the repo root, and `--root` must be the repo root, where `corpus/knowledge` is the real corpus) — hence the disposable scratch git repo in §5.
- No source mutation was performed (not one of the four mutation seats); the gate's descending branch was not independently mutated, so "the gate flags descending ranges because of that branch" rests on the source read + the §5/§6 behaviour pair rather than on a mutant-kill.

## 9. Verdict (recommendation only)
Fixture `13-descending-range` is **operable and honest** for this candidate: independent derivation == fixture expectation == real gate stdout == shipped runner verdict, with row/file identity correct in every finding; the shipped consumer rejects a deliberately wrong expectation; the fixture's single mutation produces exactly the declared causal consequence. No blocking defect found for fixture 13. Status of the fixture is "gate detects the descending range and exits 1", not "the citing set is clean" — the ledger of this fixture is not thereby proven complete.
