# AttackCase14 — consumer fixture `14-oversize-range` (r27 fresh falsification)

Axis: **operability**. Seat read-only (scratch only under `/fast/scratch/hyaku/kake-r27/AttackCase14/`).
Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.

## 0. Authority
- HEAD = `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; `git status --porcelain -- scripts/` empty.
- Gate blob == candidate blob: worktree `git hash-object scripts/citing_set.py` = `352a471abec08daa56a0fb7ef23fe78f2930d773` = `git rev-parse ac46a747…:scripts/citing_set.py`; file sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` (runner reports same `gateSha256`).
- Live fixture bytes identical before/after all runs: `corpus/knowledge/origin-repos.md` `d261d1b4…244c9f`, `expected.json` `5c64d42c…e77fb3`, `ledger.json` `5087ae2f…14f62b`, `population.json` `97a86edf…7c2d0`. No production edit, no install.

## 1. Attacked item (input read before any gate output)
`scripts/fixtures/citing-set/14-oversize-range/`
- `population.json` rows: `S001`, `S900`.
- `ledger.json` pairs: `(S001, corpus/knowledge/origin-repos.md)`, `(S900, corpus/knowledge/origin-repos.md)`.
- `corpus/knowledge/origin-repos.md` L1: `source: S001..S900 (corpus/SOURCES.md) - https://example.test/repos/origin §Row span` — no other `S<digits>` token in the file.

## 2. Independently declared expectation (derived before running the gate; no gate output, no `expected.json` seen)
From input + `contract.json` gateInterface + the gate's declared grammar (`scripts/citing_set.py` docstring L21-56):
- Literal-token rule also matches `S001`/`S900` inside `S001..S900` (tokens and ranges scanned independently) → citing set = 2 pairs, both ledger-adjudicated → no `unadjudicated_citing_pair` / `ledger_pair_not_cited` / duplicate.
- Range `S001..S900` spans 900 ids (>200) → exactly **one** `citation_range_invalid` (span_too_large); declared semantics: "an invalid range is not expanded; its endpoints remain literal citations".
- `input_invalid` impossible (both JSON docs well-formed; corpus dir/file regular).
- **Declared: exit 1, verdict `failed`, finding-id multiset `["citation_range_invalid"]` (count 1)**; `citingPairs` 2, `ledgerPairs` 2, `outsidePopulation` 0.

## 3. Run 1 — real frozen gate, scratch copy, unrelated cwd
Copy → `/fast/scratch/hyaku/kake-r27/AttackCase14/pristine` (byte-identical). cwd `/`, `TMPDIR=/fast/scratch/hyaku/kake-r27/AttackCase14`:
`python3 -B …/scripts/citing_set.py --root …/AttackCase14/pristine --population population.json --ledger ledger.json --json`
Actual, exit **1**: `{"verdict":"failed","citingPairs":2,"ledgerPairs":2,"findings":[{"id":"citation_range_invalid","file":"corpus/knowledge/origin-repos.md","range":"S001..S900","start":1,"end":900,"reason":"span_too_large"}],"populationRows":2,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}`
**Comparison:** observed exit 1 == declared 1; observed sorted ids `["citation_range_invalid"]` == declared == `expected.json` `{"exit":1,"findings":["citation_range_invalid"]}` (sha `5c64d42c…`). No exit/tally disagreement.
**Identity (manual):** finding `file` = `corpus/knowledge/origin-repos.md` = the single corpus file (exact relative path); `range` `S001..S900`; start 1 / end 900; reason `span_too_large`; row mapping 1:1 on S001/S900; no row-level findings.

Consumer commands re-run (real selftests):
- `python3 -B scripts/citing_set.py --selftest` (repo root) → exit **0**; `verdict clean, passed true, cases 29, failed 0, failedCases 0, meetsContractMinimum true`; case `14-oversize-range` `ok:true`, expected == actual `exit 1, ["citation_range_invalid"]`.
- `python3 -B scripts/citing_set_selftest.py --root . --tmpdir …/AttackCase14/selftest` → exit **0**, same 29/29 clean summary.
- Wart only: `scripts/citing_set.py --selftest --tmpdir …` → exit **64** (gate parser has no `--tmpdir`; usage JSON on stdout + stderr); the sibling runner does accept `--tmpdir`.

## 4. Run 2 — ONE causally meaningful input change (expectation declared before running)
Change (scratch copy only): add population row `S500`, an id **interior** to the rejected range, absent from the ledger. `population.json` `97a86edf…7c2d0` → `359aa982eb8bba2c20eea981fec297aded8266ef55d7b8826487851b27ff270b`; corpus/ledger/expected untouched.
**Declared consequence:** rejected range contributes no rows → S500 is never a citing pair → **no** `unadjudicated_citing_pair` for S500; `citingPairs` stays 2; id multiset stays exactly `["citation_range_invalid"]`; exit stays 1; `populationRows` becomes 3. (Falsifier: a flag-but-still-enumerate implementation → `citingPairs` 3 + extra `unadjudicated_citing_pair` S500.)
Actual: exit **1**, findings only `citation_range_invalid` (same file/range/start/end/reason), `citingPairs` 2, `ledgerPairs` 2, `populationRows` 3, `outsidePopulation` 0 → **matches declared expectation exactly**; rejected range confirmed not expanded.

## 5. Supplementary input-boundary probes (same scratch seat; expectations declared first)
Declared: rule is "citation_range_invalid for descending/>200 span" / "spans more than 200 ids".
Probe A `…/AttackCase14/boundary` (corpus sha `2ff0397a9011ce867d9bbfcf4df5ac88dbfb3435e02f2730f1df077d43b133df`), range `S001..S201` (201 ids) → per the declared rule it must be invalid. Actual exit 1, findings **only** `ledger_pair_not_cited` (S900) — **no** `citation_range_invalid`; `citingPairs` 1, `outsidePopulation` 200 → the 201-id range was accepted and expanded.
Probe B `…/AttackCase14/boundary2`, range `S001..S202` (202 ids) → exit 1, findings `citation_range_invalid` (range `S001..S202`, start 1, end 202, reason `span_too_large`) + `ledger_pair_not_cited` (S900); `outsidePopulation` 1 → invalid range not expanded, consistent with the declared rule.

## 6. Findings by severity
**F1 — MEDIUM — off-by-one between declared span rule and implemented guard.** The code rejects only ranges covering ≥202 ids (`end - start > 200`, `MAX_RANGE_SPAN = 200`), while the gate docstring L53-54 ("spans more than 200 ids") and `contract.json` (">200 span") require rejection of >200 ids, i.e. ≥201. Evidence: probe A (201 ids → not flagged, expanded, 200 ids into `outsidePopulation`) vs probe B (202 ids → flagged). Bounded impact (one id) but the declared contract is violated exactly at the guard boundary, and **no fixture among the 29 pins that boundary** (fixture 14 uses span 899).

**F2 — MEDIUM — fixture 14's oracle cannot discriminate its named semantics, nor file/row identity.** `expected.json` of `14-oversize-range` is **byte-identical** to `13-descending-range` (both sha256 `5c64d42ca67b00c347ea9889f5309b2010e10f29b97e3f6410844d3bf8e77fb3`, `{"exit":1,"findings":["citation_range_invalid"]}`). The runner compares only exit + sorted id multiset (`scripts/citing_set_selftest.py` `run_case`: `observed != sorted(expected["findings"])`), so (a) an implementation reporting `reason:"descending_range"` for this oversize input, or attributing the finding to the wrong file, still passes fixture 14; (b) `expected.json` has no channel for row/file identity, so the verified `file`/`range`/`start`/`end` (§3) are unpinned by any oracle.

**F3 — LOW — committed fixture cannot distinguish "flag but still enumerate" from correct "reject without expansion".** The ledger is satisfied by the *literal* tokens `S001`/`S900` embedded in `S001..S900`, and the population holds only those two endpoints, so the citing set is identical whether or not the rejected range is enumerated. §4 shows the discriminating input exists (population row `S500` → correct: `citingPairs` 2, no extra finding; flag-but-enumerate: `citingPairs` 3 + `unadjudicated_citing_pair`) — it is absent from the committed fixture set.

**No defect in the fixture's expected value:** the independently derived exit + id multiset (§2) equals the committed `expected.json` and the observed output (§3).

## 7. Residual risk / verification gaps
- Fixture 14 is exercised only in working-tree mode (its directory is not a Git repo); the `--revision` Git-blob path never applies to it. Git-mode range behaviour is exercised only indirectly by `c2_count.py` (not re-run here).
- Row/file identity of range findings is unverifiable by the oracle for **all** fixtures (F2); my identity check was manual and limited to fixture 14.
- The >200 boundary (F1) is unpinned by every fixture; a fix needs a case at exactly 201/202 ids, or restatement of the rule (">200 gaps" / "≥202 ids"). No expectation was changed.
- `input_invalid`/exit-2 paths are not applicable to this fixture's inputs and were not exercised.
- All mutant/boundary runs used scratch copies; live fixture byte-identical before/after (§0); no tracked file changed; no tools installed this seat.
