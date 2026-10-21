# AttackCase09 — consumer fixture `09-metadata-header-reference`

Lane: r27 fresh falsification, axis **operability**. Leaf member, no dispatch.
Target: frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.

## Authority of what was read and run

- `git rev-parse HEAD` → `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (== candidate).
- Gate read read-only; sha256 == `frozen-candidate.json` `sourceFiles`: `scripts/citing_set.py`
  `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`; `scripts/citing_set_selftest.py`
  `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`.
- Fixture 09 live files == candidate hashes: `corpus/knowledge/freshness-sweep.md` `6a8e915c…`,
  `expected.json` `49d7286d…`, `ledger.json` `7c79a345…`, `population.json` `4fe30045…`.
- Live fixture and repo source unmodified (re-hashed after all runs, values above unchanged); `git status` clean under
  `scripts/`, `corpus/`. All input work in `/fast/scratch/hyaku/kake-r27/AttackCase09/` with `TMPDIR` set there
  (no `/tmp`, no `/dev/shm`).

## Independent derivation (before any gate output)

- `population.json` rows `S001`,`S002` → keys `("n",1)`,`("n",2)`; display `S001`,`S002`.
- `ledger.json` = `{"round":27,"pairs":[]}` → 0 ledger pairs ⇒ no `ledger_pair_not_cited`, no `ledger_duplicate_pair`.
- Corpus (`freshness-sweep.md`, 560 B, 13 lines): own scan `(?<!\w)S[0-9]{3,}(?!\w)` → exactly one token `S001`
  (metadata header line 1 `source: S001 (corpus/SOURCES.md) …`); range grammar → zero ranges; case-insensitive `S\d{2,}`
  → only `S001` (so `SOURCES.md`, `scanCitations`, `sweep-script` are not citations).
- ⇒ citing set = {(`S001`,`corpus/knowledge/freshness-sweep.md`)}; `S002` is an **uncited** population row ⇒ not a finding.
- Derived expectation: **exit 1** (`failed`), finding-id multiset `{unadjudicated_citing_pair × 1}`, row/file identity
  `row=S001`, `file=corpus/knowledge/freshness-sweep.md`; `citingPairs=1`, `ledgerPairs=0`, `outsidePopulation=0`.

## RUN1 — real frozen gate CLI, scratch copy, unrelated cwd

Copy `cp -a <repo>/…/09-metadata-header-reference → $S/fixture09` (hashes identical to live); cwd
`/fast/scratch/hyaku/kake-r27/AttackCase09` (not the repo); `TMPDIR=$S/tmp`.
`python3 -B <repo>/scripts/citing_set.py --root $S/fixture09 --population population.json --ledger ledger.json --json`

Observed exit **1**; stdout `verdict=failed`, `citingPairs=1`, `ledgerPairs=0`, `populationRows=2`, `corpusFiles=1`,
`outsidePopulation=0`, `source=working-tree`; one finding
`{"id":"unadjudicated_citing_pair","row":"S001","file":"corpus/knowledge/freshness-sweep.md"}`; stderr empty.
Derived expectation **= actual** (exit, id multiset, row, file). `expected.json` `{exit:1, findings:["unadjudicated_citing_pair"]}`
**agrees** with the derivation on both fields. No disagreement on exit, id tally, row, or file.

## RUN2 — consumer runner over the same scratch case

`python3 -B <repo>/scripts/citing_set_selftest.py --root <repo> --fixtures $S/fixtures-only --gate <repo>/scripts/citing_set.py --tmpdir $S/tmp --json`
→ exit **0**, `cases=1`, `failed=0`; case 09 `ok=true`, actual `{exit:1, verdict:failed, findings:["unadjudicated_citing_pair"]}`.

## RUN3 — the ONE causally meaningful input change (declared before running)

Scratch-only edit to `fixture09/corpus/knowledge/freshness-sweep.md`: appended body line
`The second governing row for this sweep is S002 and it is now named in the body.`
Pristine corpus sha256 `6a8e915c6d621cca9d4836b62da9a27f2aab73d4c018808cf7763577bf1839d9` → mutated
`d3849933b8e843a7c42f38ea8d7f2de23916f3bbf0c346a94b2a2a376052f43c`; `population/ledger/expected.json` untouched
(`expected.json` still `49d7286d…`).

**Declared before executing:** `S002` is inside the population ⇒ citing set gains a pair; ledger still empty ⇒ both pairs
unadjudicated ⇒ **exit 1**, `failed`, `citingPairs=2`, `ledgerPairs=0`, `outsidePopulation=0`, id multiset
`{unadjudicated_citing_pair × 2}`, row/file `{S001 | corpus/knowledge/freshness-sweep.md}` and
`{S002 | corpus/knowledge/freshness-sweep.md}`.

**Actual:** exit **1**, `citingPairs=2`, `ledgerPairs=0`, `outsidePopulation=0`, findings `S001` then `S002`, both
`unadjudicated_citing_pair`, both `corpus/knowledge/freshness-sweep.md`. Declared expectation **= actual** on every field.

**Discrimination (oracle not vacuous):** same consumer runner over the mutated copy now exits **1**, `failed=1`, reason
`finding-id mismatch: expected ["unadjudicated_citing_pair"], observed ["unadjudicated_citing_pair","unadjudicated_citing_pair"]`.
The green RUN2 result is earned, not structural.

## RUN4 — determinism

Fresh pristine copy `$S/fixture09-pristine`, same command: exit **1**, stdout **byte-identical** to RUN1.

## RUN5 — full live suite (context)

`python3 -B <repo>/scripts/citing_set_selftest.py --root <repo> --fixtures <repo>/scripts/fixtures/citing-set --gate <repo>/scripts/citing_set.py --tmpdir $S/tmp --min-cases 12 --json`
→ exit **0**, `cases=29`, `failed=0`, `verdict=clean`; case 09 `ok=true`, `expected == actual`.

## RUN6 — second input mode, same content

Scratch git repo `$S/fixture09-git` (pristine fixture content), commit `f3fae300a50105117f0a44504db78282f21a2edb`;
gate `--revision f3fae300…` → exit **1**, `source=git`; findings, `citingPairs`, `ledgerPairs`, `populationRows`,
`corpusFiles`, `outsidePopulation` **identical** to RUN1 (only `source`/`revision` differ). Row/file identity is
mode-independent for this case.

## Discrepancies / uncertainties

- None between derived expectation, gate output, `expected.json` and consumer runner for fixture 09.
- Fixture 09's `expected.json` is byte-identical (`49d7286d…`) to fixtures 02/04/05/06/07/08/10/22/24/25/27 — same
  expectation shape reused; my derivation rests on this case's own input (S001-only citing set), not on that shared file.
- Tooling: the `bash` tool truncated output when the last status was the gate's exit 1, so gate invocations were driven
  through a Python `subprocess` wrapper capturing exit code + stdout verbatim. No install/tool change was needed or made.

## Residual risk / verification gaps (operability)

1. **Oracle granularity (contract-level):** `expected.json` pins only exit + finding-id multiset, so fixture 09 would
   still pass if the gate mislabelled the finding's row or file. Row/file identity for this case is covered here only by
   ad-hoc probe (RUN1/RUN3); pinning `{id,row,file}` would be an oracle change, not a gate change.
2. **Mode coverage:** the fixture consumer exercises working-tree mode only; `--revision` is covered by the C2 oracle, not
   by fixtures. RUN6 shows equivalence here, but a `GitSource`-only regression would leave all 29 cases green.
3. **"Header" is prose, not structure:** the fixture's metadata header has no `---` front-matter fence, so "header-only" is
   not machine-marked. A body-only scanner is caught (0 findings ⇒ mismatch), but a scanner that *excluded* fenced front
   matter would break this fixture without the fixture making that exclusion explicit.
4. Not re-derived here (other lanes): C1 strict disposition, 16-pair oracle count, 58/55 obligations.
