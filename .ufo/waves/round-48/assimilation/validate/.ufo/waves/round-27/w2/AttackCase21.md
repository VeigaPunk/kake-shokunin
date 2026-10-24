# AttackCase21 — consumer fixture 21-no-citations-empty-citing-set (r27 fresh falsification)

Lane: leaf reviewer, read-only source seat, no source edit, no dispatch. Judged axis: operability.
Candidate under attack: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD == candidate; `git rev-parse HEAD` = ac46a74…, worktree shows only untracked `.ufo/waves/**`).
Gate source blob == working bytes: `git rev-parse ac46a74:scripts/citing_set.py` = `352a471abec08daa56a0fb7ef23fe78f2930d773` == `git hash-object scripts/citing_set.py`; sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`.
Fixture live bytes == candidate blobs (`git diff ac46a74 -- scripts/fixtures/citing-set/21-…` empty): expected.json `a2def88b…`, ledger.json `7c79a345…`, population.json `4fe30045…`, corpus `16d794be0d8bde8734cec3584086a61a2418f6508cf8d62587c41d63c2c22941` (543 B).

## Attacked item
Fixture `scripts/fixtures/citing-set/21-no-citations-empty-citing-set`: population rows S001,S002 (kind code/tier A); ledger `{"round":27,"pairs":[]}`; one corpus file `corpus/knowledge/free-read-verbs.md` (543 B) whose front matter/body/EOF prose name **no** registry row.

## Independently derived expectation (declared before running the gate)
Read from the contract gate interface + the gate grammar in `scripts/citing_set.py` (`_TOKEN_RE = (?<!\w)S([0-9]{3,})(?!\w)`, `_RANGE_RE` needing S+3digits on both sides, findings = cited-but-not-ledger pairs only; a population row that is never cited is **not** an obligation).
Own scan of the corpus bytes (own regex, not the gate): tokens `[]`, ranges `[]` → citing set empty.
→ expected **exit 0**, finding-id multiset **`[]`**, verdict `clean`, citingPairs 0, ledgerPairs 0, corpusFiles 1, outsidePopulation 0, populationRows 2.
Frozen `expected.json` (`{"exit":0,"findings":[]}`) was read only *after* this derivation; it agrees.

## Actual run 1 — real frozen gate CLI, scratch copy, unrelated cwd
```
cd /fast/scratch/hyaku/kake-r27/AttackCase21   # unrelated cwd; TMPDIR=/fast/scratch/hyaku/kake-r27/AttackCase21/tmp
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --root …/AttackCase21/case21 --population population.json --ledger ledger.json --json
```
stdout: `{"verdict":"clean","citingPairs":0,"ledgerPairs":0,"findings":[],"populationRows":2,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}` — **exit 0**.
Matches the independently derived expectation exactly (exit, id multiset, and every reported counter). Two consecutive runs byte-identical (`base1.json` vs `base2.json`). Live fixture untouched afterwards (hashes above re-read; `git status --porcelain` unchanged, no tracked-path diff).
Consumer runner (real, whole suite, `--tmpdir` inside my seat): `scripts/citing_set_selftest.py` → `verdict clean, cases 29, failed 0`, case `21-no-citations-empty-citing-set ok=true, expected {exit 0, findings []} == actual {exit 0, findings []}`.
**No disagreement found for fixture 21.**

## Mutation probe (one causally meaningful input change, scratch only)
Declared expectation before running: appending one literal token `S001` (a population row, absent from the empty ledger) to the corpus file must yield **exit 1**, verdict `failed`, finding-id multiset `["unadjudicated_citing_pair"]` (exactly one), `row="S001"`, `file="corpus/knowledge/free-read-verbs.md"`, citingPairs 1, ledgerPairs 0.
Actual: `{"verdict":"failed","citingPairs":1,"ledgerPairs":0,"findings":[{"id":"unadjudicated_citing_pair","row":"S001","file":"corpus/knowledge/free-read-verbs.md"}],"populationRows":2,"corpusFiles":1,"outsidePopulation":0}` — **exit 1**. Matches the declaration on every field including row/file identity.
Interpretation: the base clean result comes from *scanning* the corpus file and finding zero citations, not from the gate failing to read the corpus; the empty ledger does not suppress the red condition.

## Boundary probes (scratch only)
Declared expectation: with `corpus/knowledge` empty → exit 0, findings `[]`, corpusFiles 0; with the corpus directory absent → identical. Actual: both `{"verdict":"clean",…,"corpusFiles":0}` exit 0.

## Findings
1. **F1 (no defect, fixture 21).** Independent derivation = `expected.json` = real gate output (exit, id multiset, counters). Fixture 21's expectation is correct, not a rubber stamp.
2. **F2 (LOW, fixture discriminating power).** Fixture 21 alone cannot distinguish "corpus scanned and citation-free" from "corpus not scanned": empty/absent corpus yields the identical clean/exit-0/0-findings outcome. Only the suite or the mutation above proves corpus reading. Acceptable for a clean-control case, but it is a vacuous-by-construction case: it pins the *absence* of obligations, never the enumeration machinery.
3. **F3 (LOW–MED, oracle identity gap, whole fixture layer).** All 29 fixture `expected.json` files carry exactly the keys `("exit","findings")`; none pins `row`/`file` (verified by scanning every `*/expected.json`). The runner compares only exit + sorted finding ids (`citing_set_selftest.py:238-266`, `finding_ids()`), so row/file identity is never asserted at the fixture layer. Demonstrated empirically with two scratch cases: corpus citing `S001` → finding `row S001`, corpus citing `S002` → finding `row S002`; both produce the identical id multiset `["unadjudicated_citing_pair"]` and both cases pass the real runner (`verdict clean, cases 2, failed 0`) with the *same* expected.json. A gate that mislabels the row of every finding would pass all 29 fixtures. The corpus-level oracle `c2-oracle.json` *does* pin row+file (16 pairs, `corpus/knowledge/…` convention — same convention the gate emits), so identity is asserted there, not in the fixture layer. For fixture 21 specifically the gap is vacuous (expected findings are empty), which is why my identity check had to be made against the mutant.
4. **F4 (LOW, provenance of fixture expectations).** The gate and all 29 fixtures landed in the **same** commit `ac46a74`, so "declared before implementation" is not demonstrable from git for the fixture layer. Weak corroboration only: filesystem mtime of `21-…/expected.json` = 17:10:58 precedes `scripts/citing_set.py` = 18:43:30; the contract's declared-before corpus oracle `c2-oracle.json` has mtime 16:58:44 and covers the 16 corpus pairs, not fixture expectations. `oracle-implementation-corrections.json` lists `expectedOutcomeFilesUnchanged` = {contract.json, c2-oracle.json, c1-before.json, frozen/expected.json} — the 29 fixture `expected.json` files are **not** in that pinned set.

## Residual risk / verification gaps
- Fixture 21 proves only the "no citation" control; the enumeration/range/omission semantics for fixture 21 are absent by construction (F2).
- Row/file identity at the fixture layer is unverified by any oracle (F3); the whole-suite green result is therefore an exit+id-tally green, not an identity green. Identity holds only where c2-oracle.json pins it.
- Fixture-level expectation provenance is same-commit (F4); my independent derivation is the only independence evidence I produced for this fixture.
- I did not exercise the gate's `--revision` (GitSource) path for fixture 21, nor the git-blob corpus path; fixture 21 is a working-tree case (case 18 covers the no-revision mode separately, not mine).
- Suite green (29/29) is one runner execution; I did not re-run it under a second TMPDIR/HOME isolation to check environmental determinism.

## Hygiene
Source read-only: no repo file created or edited except this report; the single input change lives in `/fast/scratch/hyaku/kake-r27/AttackCase21/case21-mut/`. `TMPDIR` set explicitly to the seat scratch; no `/tmp` or `/dev/shm` use; no network; no installs (none needed); no commits/index/jj/remote changes; no subagent dispatch; no fleet/state/MANIFEST/sibling/domain-source writes.
