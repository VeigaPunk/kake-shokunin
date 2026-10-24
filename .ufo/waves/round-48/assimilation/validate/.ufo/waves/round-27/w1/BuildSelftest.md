# BuildSelftest — r27 citing-set selftest runner (operability)

Seat: `KakeR27.BuildSelftest` (executor, axis operability, milestone r27-full-citing-set).
Scope: exactly one file, `scripts/citing_set_selftest.py`. No fixtures, no gate, no commits.

## 1. File delivered

| Item | Value |
|---|---|
| Path | `/fast/scratch/hyaku/kake-r27/writer-selftest/scripts/citing_set_selftest.py` (new) |
| Worktree / branch | `/fast/scratch/hyaku/kake-r27/writer-selftest` · `kake-r27-selftest` |
| Base | `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (`git rev-parse HEAD`, worktree clean before this file) |
| Size | 384 lines · 13 623 bytes |
| SHA-256 | `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` |
| Git state | `?? scripts/citing_set_selftest.py` — uncommitted, per "L1 integrates; do NOT commit" |

No other path in the repo or in a sibling worktree was written. No git mutation, no fixture, no gate.

## 2. Contract rows implemented

Contract source: `.ufo/waves/round-27/contract.json`, key `gateInterface`.

- `cli` — "python3 -B scripts/citing_set.py --root <dir> [--revision <commit>] --population <relative-json> --ledger <relative-json> [--json]".
  The runner issues exactly `python3 -B <gate> --root <case-dir> --population population.json --ledger ledger.json --json`, one subprocess per case, `cwd=<case-dir>`, `TMPDIR`/`HOME` isolated under `/fast/scratch/hyaku/kake-r27`.
- `fixtureInterface` — "scripts/fixtures/citing-set/<case>/{corpus/knowledge/*,population.json,ledger.json,expected.json}".
  The runner discovers every immediate subdirectory of the fixture directory and never reads outside a case dir.
- "expected.json {exit:int,findings:[finding-id,...]} with repeated ids retained" — the runner compares the **exact subprocess exit code** and the **exact sorted multiset** of finding ids (repetitions kept; `Counter`-equivalent via sorted-list equality).
- "Runner invokes gate subprocess per fixture and compares exit+sorted finding ids, nonzero on any mismatch." — exit 0 only when every case matches; exit 1 on any mismatch; exit 2 when the run cannot be evaluated.
- "Code0 clean,1 failed findings,2 could-not-evaluate,64 usage." — the runner reuses the same code space for its own verdicts: 0 clean, 1 failed, 2 could-not-evaluate.
- "Use TMPDIR=/fast/scratch/hyaku/kake-r27" — honoured for every child process.

## 3. Runner contract (as implemented)

CLI: `python3 -B scripts/citing_set_selftest.py [--root <repo>] [--fixtures <dir>] [--gate <path>] [--tmpdir <dir>] [--timeout <s>] [--min-cases <n>] [--json] [--selftest]`.

- Defaults are location-derived: `root` = parent of `scripts/`, `gate` = `<root>/scripts/citing_set.py`, `fixtures` = `<root>/scripts/fixtures/citing-set`.
- Unknown flags are recorded in `notes` and ignored (never fatal), so the gate's `--selftest` delegation `python3 -B scripts/citing_set_selftest.py --root <repo-root>` is accepted verbatim. `--selftest` is accepted as a no-op alias.
- One JSON object on stdout; stderr stays empty, so verbatim forwarding by the gate is safe.

Summary object (stdout), keys:

| Key | Meaning |
|---|---|
| `schema` | `kake-citing-set-selftest-v1` |
| `verdict` | `clean` \| `failed` \| `could-not-evaluate` |
| `passed` | boolean; true only for `verdict == clean` |
| `cases` | integer count of discovered fixture cases |
| `failed` | integer count of unsatisfied obligations (one per failing case, or one when the run could not be evaluated) — **`failed == 0` only ever for a passing run** |
| `failedCases` | failing fixture cases only |
| `caseNames`, `results`, `failures` | per-case evidence: expected vs observed exit and sorted ids, exact argv, reason |
| `contractMinimumCases`, `meetsContractMinimum` | contract asks ">=12 meaningful cases"; reported, enforced only with `--min-cases 12` (default 0, so a fixture shortfall cannot silently pass as clean) |
| `runner`, `runnerSha256`, `gate`, `gateSha256`, `fixtures`, `root`, `notes` | provenance |

Non-pass guards (all verified, see §5): missing gate → exit 2; absent/empty fixture directory → exit 2; missing/unparsable/malformed `expected.json` → that case fails (never skipped); exit mismatch → case fails; id-multiset mismatch → case fails; gate stdout that is not a JSON report → case fails; gate report without a `findings` array or with a non-array `findings` → case fails; gate timeout or start failure → case fails.

## 4. Interface agreement (peers, frozen, not silently changed)

- BuildGate (confirmed, no differences): gate is `scripts/citing_set.py`; stdout is always the JSON report `{"verdict":...,"citingPairs":int,"ledgerPairs":int,"findings":[{"id":...,"row":...,"file":...}]}`; exit 0/1/2/64; ids exactly `unadjudicated_citing_pair`, `ledger_pair_not_cited`, `ledger_duplicate_pair`, `citation_range_invalid`, `input_invalid`; `input_invalid` → exit 2 `could-not-evaluate`; `citation_range_invalid` → exit 1 `failed`, range not expanded, endpoints remain literal citations; one `ledger_duplicate_pair` per distinct pair (`occurrences`:N), a duplicated pair still counts as adjudicated; `row` = population id, `file` = corpus-relative path.
- BuildFixtures (confirmed, no differences): every case dir self-contained; `expected.json` = `{"exit":int,"findings":[<finding-id>,...]}`, ids only, duplicates retained, no extra keys, no extra files.
- BuildGate explicitly declined a per-case `(row,file)` extension to `expected.json`: the `(row,file)` pinning is carried by `.ufo/waves/round-27/c2_count.py` against `c2-oracle.json`. The runner therefore keeps the frozen fixture interface and does not fork it.

## 5. Evidence — synthetic smoke run (NOT repo evidence)

Fixtures and gate do not exist in any lane at the time of writing, and the parent seat forbids mid-flight checks, so the runner was exercised against a **synthetic stub gate and synthetic fixtures** under `/fast/scratch/hyaku/kake-r27/BuildSelftest/smoke/` (stub gate sha256 `2c5949d4ebf774e5cf6680e2a637ce75823c589d9660b68d91922fa78ede79fb`). No repo file, no sibling worktree and no live lane path was touched.

| Run | Invocation | Observed |
|---|---|---|
| `out2.json` sha256 `08c0d93ea405c1ad9bd13afe8f288eabb581eed746b8143f1127f40ca5cc67ec` | 8 synthetic cases | `verdict=failed cases=8 failed=5`, exit 1 |
| `out-nf.json` sha256 `e217cefad7e69629b14850897013a952cf8e7027556736d03e98d54fdfbb0913` | stub gate emitting no `findings` array | case `a-match` failed: "gate report carries no 'findings' array", exit 1 |
| `out-default.json` sha256 `7a7f6be7048d1ff705a80dd235a15e10eb00260780e3a725766720e6bc31cc42` | `--root fakerepo` only (defaults) | `clean cases=1 failed=0`, exit 0; gate and fixtures resolved under `--root` |

Per-case outcomes in `out2.json`: passing — `a-match` (exit 0, no ids), `b-missing-pair` (exit 1, one `unadjudicated_citing_pair`), `f-dup-ids` (exit 1, **two** identical ids, repeated ids retained). Failing — `c-exit-mismatch` "exit mismatch: expected 0, observed 1"; `d-ids-mismatch` "finding-id mismatch: expected [\"ledger_pair_not_cited\"], observed [\"unadjudicated_citing_pair\"]"; `e-bad-expected` "expected.json must carry an integer \"exit\""; `g-dup-ids-lost` "finding-id mismatch: expected [\"unadjudicated_citing_pair\"], observed [\"unadjudicated_citing_pair\",\"unadjudicated_citing_pair\"]"; `h-no-expected` "expected.json unreadable: [Errno 2] No such file or directory". Additional boundary runs: empty fixture directory → exit 2, `could-not-evaluate`, `failed=1`; missing gate → exit 2, `could-not-evaluate`, `failed=1`; `--selftest --bogus-flag` → tolerated, `verdict=clean`, `notes=["ignored unknown arguments: --bogus-flag", ...]`.

**Not verified:** no run against the real `scripts/citing_set.py` and the real fixture set has occurred. Both are absent at write time (L1 must run the integration check after landing all three writers' files). The stub gate exercises the runner's control flow, not the real gate's behaviour.

## 6. Uncertainties

1. Real-gate stdout shape is asserted against BuildGate's message, not observed. The runner tolerates a banner before the JSON object (raw-decode scan) and fails loudly on a non-JSON stdout; if the real gate prints a non-JSON trailing line after the report, the raw-decode path still returns the first complete object — an unverified assumption.
2. `--min-cases` defaults to 0, so a fixture set below the contract's ">=12 meaningful cases" is reported (`meetsContractMinimum:false`) but not fatal. If the L1 wants the contract minimum enforced, run with `--min-cases 12`; the trade-off is that a late fixture shortfall would then fail the whole selftest rather than warn.
3. `failed` counts obligations, not cases (`failedCases` holds the case count). A checker that reads only `failed` still cannot mistake a could-not-evaluate run for a pass.
4. `AGENTS.md` requires "Every change appends a LOG.md entry". That entry is deliberately **not** written by this seat: the assignment restricts me to the single source file, and `LOG.md` is an integration-owned path. L1 must append the round-27 entry for `scripts/citing_set_selftest.py`.

## 7. Suggested missing behavioural boundaries (for L1 / gate / fixtures owners)

1. **`expected.json` cannot express `(row,file)`.** The frozen schema carries ids only, so a gate that reports the right id for the *wrong* pair passes the fixture oracle. Covered today only by `c2_count.py` against the frozen 16-pair oracle — the fixture set has no equivalent. Suggestion: keep the frozen schema, but let one fixture case assert a *wrong-pair* detection through a corpus that cannot produce the claimed pair (i.e. the id must be absent), rather than by extending the schema.
2. **No case pins the `verdict` string.** The runner compares exit + ids only. A gate that emits `verdict:"clean"` with exit 1 (or vice versa) passes. Suggestion: one fixture case whose expected exit is 2 (`input_invalid`) plus a documented verdict expectation, or an optional runner flag that also compares `verdict` when `expected.json` carries it.
3. **No case pins the `citingPairs` / `ledgerPairs` counters.** The contract's report shape has them; nothing in the fixture oracle observes them. Suggestion: a positive fixture case where the expected counts are derivable by hand from `population.json`/`ledger.json`.
4. **No case covers the `--revision <commit>` read path.** The contract lists it on the gate CLI; the runner never passes `--revision` (fixtures are working-tree cases). Suggestion: one fixture case that runs the gate twice — once on the working tree, once with `--revision` against a fixture-local git repository — so the two read paths are proven equivalent.
5. **No negative case for a gate that writes outside its root.** The runner isolates `TMPDIR`/`HOME` but does not assert write confinement. Suggestion: a case that records the fixture directory's digest before and after the gate run, so a gate that mutates its own inputs fails.
6. **`ledger_pair_not_cited` multiplicity is unproven.** BuildGate froze "one per distinct ledger pair absent from the citing set"; no fixture case asserts two such pairs at once. Suggestion: one case with two ledger pairs outside the citing set, expecting the id twice.
7. **Symlinked-input rejection** (`input_invalid` for a symlinked `corpus/knowledge` dir or a symlinked knowledge file) is a declared gate behaviour with no fixture case. Suggestion: one case per symlink shape.

## 8. Tooling

No tool install, upgrade or service mutation was needed or performed. No `pacman`, no `uv tool install`, no `cargo`/`npm`. Interpreter used: `/usr/bin/python3` (system), invoked with `-B`. All scratch confined to `/fast/scratch/hyaku/kake-r27/BuildSelftest/` (smoke assets) and `/fast/scratch/hyaku/kake-r27/citing-set-selftest/home` (isolated HOME created by the runner's child environment).
