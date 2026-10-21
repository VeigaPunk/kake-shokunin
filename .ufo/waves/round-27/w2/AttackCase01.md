# KakeR27.AttackCase01 — consumer fixture `01-single-literal-clean` (fresh falsification, operability)

Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. HEAD verified `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` before and after. Source read-only; every source read was checked to equal the candidate blob first (`git rev-parse <candidate>:scripts/citing_set.py` = `352a471abec08daa56a0fb7ef23fe78f2930d773` = `git hash-object scripts/citing_set.py`; sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228` = frozen-candidate.json). All 5 fixture-01 files byte-identical candidate vs worktree (PROBE U). Scratch only: `/fast/scratch/hyaku/kake-r27/AttackCase01/` (TMPDIR set there). No installs. No network. No source/docs/registry edits; live fixture untouched.

## 0. Independent derivation of fixture-01 expected outcome (from input + contract, BEFORE reading gate output)

Derived from `contract.json` `gateInterface` + `citation grammar` (the gate's own docstring is source text, not evidence; the derivation below is from the input bytes and the contract's stated finding-id vocabulary `unadjudicated_citing_pair | ledger_pair_not_cited | ledger_duplicate_pair | input_invalid | citation_range_invalid`).

Inputs: `population.json` rows = {S001, S002}; `ledger.json` pairs = {(S001, corpus/knowledge/publish-queue.md)}; corpus = 1 file `corpus/knowledge/publish-queue.md`.

Token scan of the corpus file (`grep -oE '(^|[^A-Za-z0-9_])S[0-9]{3,}([^A-Za-z0-9_]|$)'`): exactly two hits, both `S001` — one in the `source:` metadata header, one in the `- S001, …` body bullet. No `S002` anywhere. Range scan (`S[0-9]{3,}\s*(-|–|—|\.\.|through|to)\s*S[0-9]{3,}`): **no match** — the `—` in the metadata line is followed by `'Accept order`, not `S###`.

Therefore expanded citing set = {S001 × publish-queue.md} = **1 citing pair**; ledger covers it exactly, so:
- `unadjudicated_citing_pair`: 0 (S001 is adjudicated)
- `ledger_pair_not_cited`: 0 (S002 is in the population but cited nowhere ⇒ no citing pair, so it is not a ledger pair; S002 contributes nothing)
- `ledger_duplicate_pair`: 0, `citation_range_invalid`: 0, `input_invalid`: 0

**Derived expectation: exit 0, finding-id multiset = ∅.** Fixture `expected.json` = `{"exit":0,"findings":[]}` — **AGREES**. `expected.json` was read only after this derivation was fixed; the gate output had not yet been run.

## 1. Baseline: real frozen gate CLI, scratch copy, unrelated cwd

Command (cwd `/fast/scratch/hyaku/kake-r27/AttackCase01`; gate = candidate blob exported to `gate/citing_set.py`, sha256 `3a361a00…`):
`python3 -B gate/citing_set.py --root runA/fx --population population.json --ledger ledger.json`

Input hashes (scratch copy == live fixture): corpus `65ec79a3f211…`, population `4fe30045f3fa…`, ledger `d34c78c0df04…` — identical to live and to candidate blobs.

Actual: **EXIT 0**, stdout `{"verdict":"clean","citingPairs":1,"ledgerPairs":1,"findings":[],"populationRows":2,"corpusFiles":1,"outsidePopulation":0,"source":"working-tree","revision":null}`, stderr empty. **Matches the derivation exactly**: citingPairs 1, ledgerPairs 1, zero findings, S002 correctly outside the citing set. PROBE AN: exported frozen copy and repo gate produce byte-identical JSON.

## 2. The ONE causally meaningful input change (declared before running)

Change: append one line to the scratch corpus file only — `- S002, 'Second queue claim'` (population/ledger untouched). New corpus sha256 `0850c9816478…` (pristine `65ec79a3f211…`); population `4fe30045…`, ledger `d34c78c0…` unchanged.

**Declared expectation:** S002 is a population row and is now cited in the same file ⇒ a second citing pair (S002 × publish-queue.md) exists and is absent from the ledger ⇒ **exit 1, finding multiset = {`unadjudicated_citing_pair`}**, and the finding's identity must be **row=S002, file=corpus/knowledge/publish-queue.md** (not S001).

Actual: **EXIT 1**, `{"verdict":"failed","citingPairs":2,"ledgerPairs":1,"findings":[{"id":"unadjudicated_citing_pair","row":"S002","file":"corpus/knowledge/publish-queue.md"}]}`. **Matches**, including row/file identity — the row is the newly cited S002, not the pre-existing S001.

**Identity cross-check (PROBE C, separate scratch):** ledger `file` changed to `corpus/knowledge/absent.md`. Declared: exit 1, multiset {`unadjudicated_citing_pair`, `ledger_pair_not_cited`}, unadjudicated identity (S001, publish-queue.md), not-cited identity (S001, absent.md). Actual: exactly that, two findings, distinct file identities. Row/file identity is preserved per finding, not conflated.

## 3. Real consumer commands re-run (not mocks, not intent)

| command | result |
|---|---|
| `python3 -B scripts/citing_set.py --selftest` (unrelated cwd) | EXIT 0, `cases 29, failed 0, passed true`, gateSha256 `3a361a00…`, runnerSha256 `3c167895…` |
| `python3 -B scripts/citing_set.py --root . --revision ac46a74… --population .ufo/waves/round-26/population.json --ledger .ufo/waves/round-27/complete-ledger.json --json` (SKILL.md-documented operator command) | EXIT 0, clean, citingPairs 58, ledgerPairs 58, corpusFiles 26, outsidePopulation 18 — reproduces `verification/consumer-current.json` exactly |
| `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision ac46a74…` | EXIT 0, `expected 16, detected 16, falsePositive 0, passed true, gateExit 1` |
| gate on the frozen snapshot (working-tree copy) | EXIT 1, 16 findings, all `unadjudicated_citing_pair`; **(row,file) set identical to `c2-oracle.json` expectedPairs** — 16/16, gate-only ∅, oracle-only ∅ (PROBE Z) |

## 4. Findings

**F1 — MEDIUM. `expected.json` cannot express row/file identity, so the 29-case fixture suite has ZERO row/file discriminating power.**
`expected.json` carries only `exit` + finding **ids**; the runner compares exit + sorted ids (`scripts/citing_set_selftest.py:274-282`), and `finding_ids()` (`scripts/citing_set_selftest.py:144-165`) discards `row`/`file`. Probe: a scratch gate wrapper that preserves exit and the id multiset but rewrites every finding's `row`/`file` to constants → **the real runner over all 29 live fixture copies reports `verdict clean, passed true, cases 29, failed 0`**. A gate that names the wrong row/file pair for all 16 omissions is invisible to the fixture layer.
*Severity is bounded, and I verified the compensating control:* the C2 oracle compares `(row,file)` **sets** (`.ufo/waves/round-27/c2_count.py:27-28`), and the same identity-mutating wrapper fails it (`detected 0, falsePositive 1, passed False`, PROBE X). So the C2 claim is sound; the **fixture suite alone** is not an identity oracle, and the round's evidence must not cite the 29-case green as identity proof. **Not a source defect** — `expected.json` shape is contract-frozen. Recommend (L1, not done here): the report cite `c2_count` for identity and the fixture suite only for exit+id coverage.

**F2 — MEDIUM. The fixture suite is blind to the `verdict` field and to the `citingPairs`/`ledgerPairs` counters.**
Probe: a scratch wrapper forcing `verdict:"clean"` on every run (exit and findings untouched) → **runner reports `clean, passed true, 29/29`**. Probe: a wrapper forcing `citingPairs=0, ledgerPairs=0` → **runner reports `clean, passed true, 29/29`**. Both are contract-consistent with `expected.json` (which has no such fields), so this is a **scope limit of the fixture oracle, not a bug**. Consequence: the fixtures cannot falsify a gate that reports a wrong verdict string or wrong counts. Same remedy as F1 — pair the fixture green with `c2_count` (which does read `verdict` via `out['verdict']` and `gateExit`).

**F3 — LOW (latent, contract-interface defect). `--revision` mode with a non-toplevel `--root` enumerates one file set and reads another.**
`GitSource.corpus_files()` runs `git -C <root> ls-tree <rev> -- corpus/knowledge` — the pathspec is **cwd-relative** to `<root>`; `read_document()` runs `git -C <root> show <rev>:<relative>` — the path is **git-toplevel-relative**. When `<root>` is a strict subdirectory of the repo, the two disagree (PROBE P: enumerated `corpus/knowledge/publish-queue.md`, but the bytes read are the **toplevel** blob sha256 `d6eb726a…`, 28410 B, citing S019 — not the fixture blob `65ec79a3…`, 698 B, citing S001). PROBE AE: for the *same* relative path, working-tree mode returns 698 B / `65ec79a3…` while git mode returns 28410 B / `d6eb726a…` — **the two modes disagree on which file a relative path denotes.** Reachability in this repo is limited but real: `--root` = any `scripts/fixtures/citing-set/<case>` (each has its own `corpus/knowledge`) → PROBE J exit 1 `ledger_pair_not_cited`; in a scratch repo I reproduced a **false clean** (PROBE AJ: exit 0 while the file actually under `--root` cites S001 and was never evaluated). The gate's own docstring says "read blobs when `--revision` set" (contract `gateInterface.inputs`), so the modes are contracted to be equivalent.
*Reachability caveat, stated honestly:* every **shipped** invocation uses `--root` = repo toplevel (`SKILL.md` operator command, `c2_count.py` snapshot, `git_name_selftest.py` builds `--root` = its own repo root) — PROBE S confirms toplevel mode is self-consistent (26 files, 0 read/enumerate mismatches). So this does **not** currently corrupt any round measurement. It is a latent trap for any operator who points `--root` at a subdirectory, and for `--revision` + fixture root combinations. Smallest safe correction (L1, not done here): make `GitSource` resolve paths against the repo toplevel consistently (e.g. prefix pathspecs with the toplevel-relative prefix of `<root>`, or refuse `--root` ≠ toplevel in `--revision` mode with `input_invalid`).

**F4 — LOW. Fixture 01 alone has near-zero discriminating power; it is a positive control, not a defect-detector.**
Probe with a fail-open gate (always `clean`, exit 0, no findings): fixture 01 **PASSES** (as do 18, 20, 21, 28 — 5/29 pass, 24 fail). Fixture 01 detects only false-positive gates (a wrapper emitting one spurious `unadjudicated_citing_pair` ⇒ fixture 01 fails, exit mismatch) and literal-scanner removal (literal-blind wrapper ⇒ fixture 01 fails with `ledger_pair_not_cited`). It is blind to range scanning (no ranges in its corpus) and to population-filter removal (S001 is the only cited id). Expected of a clean-positive control; recorded so the round does not over-claim fixture 01 as C2 evidence.

**F5 — INFORMATIONAL, resolved. My own first recompute said 34 missing pairs vs the gate's 16.**
Cause was **my** crude recompute omitting the population filter (34 − 18 outside-population = 16). With the contract's population filter applied, my independent recount is **57 citing pairs / 18 outside-population / 16 missing — identical to the gate**, and the 16 (row,file) identities equal `c2-oracle.json` exactly. **No gate defect; no disagreement.** Recorded because the discrepancy was real for one step of the trace.

## 5. Residual risk / verification gaps
- F1/F2 mean the 29-case green proves exit+id coverage only. Identity, verdict and counters are proven solely by `c2_count` (F1 verified) — a green citing only the fixture suite would be a false identity provenance.
- F3 is latent: not exercised by any shipped command; no current round number depends on it, but the contract asserts mode equivalence, and a false clean is reachable.
- Fixture 01 exercised in working-tree mode only; `--revision` mode for this fixture is unusable today (F3), and the C2 identity control is what substitutes.
- Probed branch set for fixture 01: literal token, metadata header, EOF prose, duplicate citation of S001, plus S002 addition, ledger file rename, and 5 wrapper mutants (identity / fail-open / false-positive / counters / verdict). Range and list branches, numeric-spelling branches, and input-failure branches for fixture 01 are other cases' scope.
- One mutation on fixture-01 input as assigned; the extra probes mutate the **gate wrapper** or the **scratch copy only**, never live source.
- Live tree untouched: fixture-01 sha256s unchanged (PROBE U), `git status --porcelain scripts/ corpus/` shows only a stray `scripts/__pycache__/` created by a probe importing the gate as a module (removed; re-verified absent) and no tracked modification; HEAD still `ac46a747…`. All scratch under `/fast/scratch/hyaku/kake-r27/AttackCase01/`.
- No tool installs required or performed.
- This report is falsification evidence for the operability axis only. It does not bear on C1 strict status (C1 remains UNPROVABLE: 55 strictly decided of 58 reviewed, 7 known unknown units). Pair presence ≠ semantic support.

Report: .ufo/waves/round-27/w2/AttackCase01.md
