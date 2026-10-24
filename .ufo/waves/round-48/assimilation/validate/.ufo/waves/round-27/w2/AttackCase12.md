# AttackCase12 — fresh falsification of consumer fixture `12-noncited-ledger-pair`

Seat: leaf reviewer (no dispatch). Axis: **operability**. Milestone: r27-fresh-falsification.
Frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (`HEAD` == candidate; `git diff ac46a74 -- scripts/` empty;
gate blob `352a471abec08daa56a0fb7ef23fe78f2930d773` == `ac46a74:scripts/citing_set.py`; runner blob
`3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c` == `ac46a74:scripts/citing_set_selftest.py`).
Contract: `.ufo/waves/round-27/contract.json` (C2 gate/fixture interface). **Attacked item** (read-only in the repo): `scripts/fixtures/citing-set/12-noncited-ledger-pair/` →
`population.json` (rows S001, S002), `ledger.json` (pairs (S001,corpus/knowledge/probe-delta-alerting.md),
(S002,corpus/knowledge/probe-delta-alerting.md)), `corpus/knowledge/probe-delta-alerting.md`, `expected.json`
(`exit 1`, `findings ["ledger_pair_not_cited"]`).

## Independent derivation (declared BEFORE any gate run)

Contract semantics: population rows define the citing scope; pair-level presence only; `ledger_pair_not_cited` =
a distinct ledger pair absent from the expanded citing set. Plus the fixture input:
- Independent S-token sweep with **my own** regex (`grep -oE '(^|[^A-Za-z0-9_])S[0-9]{3,}'`): exactly **one**
  token, `S001`; range sweep (`S###(-|–|—|..|to|through)S###`): **0** ⇒ expanded citing set =
  `{(S001, corpus/knowledge/probe-delta-alerting.md)}` ⇒ `citingPairs = 1`.
- Ledger holds **2 distinct** pairs, no repetition ⇒ `ledgerPairs = 2`, no `ledger_duplicate_pair`.
- (S001,file) is cited ⇒ **no** `unadjudicated_citing_pair`; (S002,file) is never cited (S002 is in the
  population but absent from the corpus) ⇒ **one** `ledger_pair_not_cited`; no range/malformed input ⇒ no
  `citation_range_invalid`, no `input_invalid`.
- **Declared expected: exit 1, verdict `failed`, finding-id multiset `{ledger_pair_not_cited}` ×1**, row/file
  identity `S002` / `corpus/knowledge/probe-delta-alerting.md` (the fixture's ledger pair #2).

## Probe A — real frozen gate CLI, scratch copy, unrelated cwd

Declared expected: as derived above (exit 1, one `ledger_pair_not_cited`).
Scratch copy `/fast/scratch/hyaku/kake-r27/AttackCase12/pristine` (live fixture untouched); corpus sha256
`e1eacd981b00d0ea61b228a9777cc460764f07d4b12c1fda8ed3677c1db95ccc`, population
`4fe30045f3fa03294a9ffb79bf09dd9bd573df167a228e5ac76233888d5b13c8`, ledger
`2001e8490c5450b66973fd2275ff9de745d7cc5dc993a76e54b66ebcbafaf2d5`.
```
cd /home/vgpnk   # unrelated cwd
TMPDIR=/fast/scratch/hyaku/kake-r27/AttackCase12 python3 -B \
  /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py \
  --root /fast/scratch/hyaku/kake-r27/AttackCase12/pristine \
  --population population.json --ledger ledger.json --json
```
stdout `{"verdict":"failed","citingPairs":1,"ledgerPairs":2,"findings":[{"id":"ledger_pair_not_cited","row":"S002",
"file":"corpus/knowledge/probe-delta-alerting.md"}],"populationRows":2,"corpusFiles":1,"outsidePopulation":0,
"source":"working-tree","revision":null}` → **EXIT=1**.
Id tally, exit **and row/file identity** equal my independently declared expectation and `expected.json`. No disagreement.

## Probe B — real consumer selftest (fixture runner) over the live fixture set

Declared expected: case `12-noncited-ledger-pair` ok; suite green.
`TMPDIR=… python3 -B scripts/citing_set_selftest.py --root . --tmpdir /fast/scratch/hyaku/kake-r27/AttackCase12/selftest --min-cases 12 --json`
→ `{"verdict":"clean","passed":true,"cases":29,"failed":0,"meetsContractMinimum":true}` **EXIT=0**; case 12
`ok:true`, expected `exit 1 / ["ledger_pair_not_cited"]` == actual `exit 1 / ["ledger_pair_not_cited"]`.

## Probe C — ONE causally meaningful input change (scratch copy only)

Change: appended one line to `/fast/scratch/hyaku/kake-r27/AttackCase12/mutant/corpus/knowledge/probe-delta-alerting.md`
— `The delta window is also attested by S002 in the same source list.` (adds exactly one literal `S002`, no
range, no other S-token). Mutant corpus sha256 `8e605de0cfd1582866064c30a258e963fde70f6208af733ead58c7f9efd4cf90`;
population/ledger bytes unchanged.
**Declared expected (before running): exit 0, verdict `clean`, findings `[]`, `citingPairs 2`, `ledgerPairs 2`** —
the added (S002,file) pair is in the ledger, so adjudicated; the `ledger_pair_not_cited` pair disappears and no
new unadjudicated pair arises.
Actual: `{"verdict":"clean","citingPairs":2,"ledgerPairs":2,"findings":[],"outsidePopulation":0,…}` **EXIT=0** — exactly as declared.
⇒ the fixture's red state is caused solely by the uncited `S002` row (no hardcoding, no stale constant).

## Probe D — git-revision mode boundary on this fixture

Declared expected: `--root` = fixture subdirectory + `--revision` cannot resolve `population.json` at the repo root
⇒ honest refusal `exit 2`, `could-not-evaluate`, one `input_invalid` (reason `git_command_failed`).
Actual: `{"verdict":"could-not-evaluate",…,"findings":[{"id":"input_invalid","reason":"git_command_failed","scope":"revision",
"command":"show ac46a747…:population.json"}]}` **EXIT=2** — as declared; never a false clean.

## Discrepancies vs `expected.json`
None. Exit code, finding-id multiset (multiplicity 1) and row/file identity all agree with the independently
derived expectation and with the frozen `expected.json`.
## Author-side findings (this seat)
- **F1 (low, coverage gap — not a contract breach):** the frozen runner compares only exit + sorted finding **ids**
  (`scripts/citing_set_selftest.py`, `finding_ids()`/`run_case()`), and `expected.json` stores ids only.
  Fixtures **12**, **17**, **26** all declare the identical expectation (`exit 1`, `["ledger_pair_not_cited"]`)
  over causally different inputs (population row never cited / ledger row outside population / ledger pair file
  absent). A regression mis-attributing the finding's **row or file** would pass all 29 cases. The current
  candidate is correct on fixture 12 (Probe A: row `S002`, file `corpus/knowledge/probe-delta-alerting.md`), so this
  is a latent suite weakness, not a live defect.
- **F2 (low, operability/UX):** in `--revision` mode the document paths resolve against the **repository root**,
  not against `--root`; with a subdirectory `--root` the gate exits 2 `input_invalid/git_command_failed` and the
  message names only `show <rev>:population.json`, never stating that `--root` must be the repo root. The contract
  CLI line (`--root <dir> [--revision <commit>]`) does not state this. Failure is honest (never a false clean) and
  does not affect C2's own measurement, whose oracle uses the repo root.
- **F3 (info, consequence of F1):** `expected.json` cannot express row/file attribution, so the frozen oracle
  cannot assert it; my row/file check above is seat-local evidence only.

## Residual risk / verification gaps
- Git-mode corpus-path semantics with a subdirectory `--root` were **not** exercised (the population read
  short-circuits first, Probe D) — untested, not a claim.
- Fixture 12 was evaluated in working-tree mode only; the runner never passes `--revision`, so no fixture
  exercises the Git-blob path for a subdirectory root.
- The 29-case green is the runner's own verdict; it does not by itself evidence row/file correctness (F1).

## Hygiene
No source/fixture/ledger/manifest/registry writes in the repo (`git status --porcelain` shows only pre-existing
untracked round-27 evidence). Only writes: this report and scratch under `/fast/scratch/hyaku/kake-r27/AttackCase12/`
(`pristine/`, `mutant/`, `selftest/`); `TMPDIR` exported explicitly; no `/tmp`, no `/dev/shm`. No installs needed.
