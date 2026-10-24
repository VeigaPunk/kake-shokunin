# KakeR27.AttackCase22 — fixture `22-json-knowledge-file-citation` (r27 fresh falsification)

Lane: read-only source; fixture input scratch only. Axis judged: **operability**. Milestone: r27-fresh-falsification.

## 0. Attacked item and frozen authority

- Target: `scripts/fixtures/citing-set/22-json-knowledge-file-citation/{corpus/knowledge/freshness-pins.json, population.json, ledger.json, expected.json}`.
- Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (HEAD, unmodified). All four fixture files + both scripts verified **byte-identical to the candidate blob** (git `show <full-hash>:<path> | sha256sum` vs worktree): gate `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`, runner `3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`, expected.json `49d7286d…`, ledger.json `bbca859f…`, population.json `4fe30045…`, corpus json `7b67f226…`.
- Gate and runner were extracted with `git show ac46a747…:scripts/…` into scratch; **no source was edited**. `git status --porcelain` shows no tracked-file change; `git diff <candidate> -- scripts/` is empty. All scratch under `/fast/scratch/hyaku/kake-r27/AttackCase22/` (TMPDIR set explicitly; no `/tmp`, no `/dev/shm`).

## 1. Independent derivation BEFORE reading any gate output

From the fixture bytes + contract `gateInterface` only: population rows `S001`,`S002`; one corpus file under `corpus/knowledge/`. Its text contains `S001`,`S002` as JSON string values → token rule `(?<!\w)S([0-9]{3,})(?!\w)` matches both (delimiters are `"`, non-word); no `S…sep…S` adjacency → no range. Both ids ∈ population ⇒ citing set `{(S001,corpus/knowledge/freshness-pins.json),(S002,same)}` ⇒ `citingPairs=2`. Ledger holds one pair `(S002, corpus/knowledge/freshness-pins.json)` ⇒ covers the S002 pair only. Therefore **exactly one `unadjudicated_citing_pair` (row S001)**, no `ledger_pair_not_cited` (S002 pair *is* cited), no duplicate, no input/range error ⇒ verdict `failed`, **exit 1**, findings multiset `["unadjudicated_citing_pair"]`.

`expected.json` claims `exit 1`, `["unadjudicated_citing_pair"]` → **agreement on exit, id multiset and (per §3) row/file identity. No disagreement.**

## 2. Pristine run — real frozen gate CLI, scratch copy, unrelated cwd

Declared expected: exit 1, `failed`, one `unadjudicated_citing_pair`, row `S001`, file `corpus/knowledge/freshness-pins.json`, `citingPairs=2`, `ledgerPairs=1`, `corpusFiles=1`, `outsidePopulation=0`, `source=working-tree`.

```
cd /fast/scratch/hyaku/kake-r27/AttackCase22/run
python3 -B ../gate/citing_set.py --root ../pristine --population population.json --ledger ledger.json --json
```
Actual: **exit 1**, `verdict failed`, `citingPairs 2`, `ledgerPairs 1`, `populationRows 2`, `corpusFiles 1`, `outsidePopulation 0`, `source working-tree`, findings `[{id:unadjudicated_citing_pair, row:"S001", file:"corpus/knowledge/freshness-pins.json"}]`. **Every declared field matched, including row/file identity.**

Real consumer runner (frozen runner, frozen gate, live fixture dir, read-only): `python3 -B gate/citing_set_selftest.py --root <repo> --fixtures <repo>/scripts/fixtures/citing-set --gate <scratch>/gate/citing_set.py --min-cases 12` → **exit 0**, `verdict clean`, `cases 29`, `failed 0`, `meetsContractMinimum true`; case 22 `ok: true`. `gate --selftest --root <repo>` → exit 0, 29 cases, 0 failed.

cwd-independence: identical output run from `/`, from the parent dir with a relative `--root`, and from an unrelated cwd.

## 3. ONE causally meaningful input change (declared before running)

**Mutation (scratch copy only):** `mutant/ledger.json` — the single pair's `"row": "S002"` → `"S001"` (one field). Pristine ledger sha256 `bbca859f0b35a06a1436c5999add15da6644d7338a4db39823f5ced4512f1eb6` → mutant `f0e15997de8091ece90ed15a3b4a6be5729ef3b6f568e3b91b0138110029e431`. Corpus bytes unchanged.

**Declared expected:** exit 1; findings multiset `["ledger_pair_not_cited","unadjudicated_citing_pair"]` — `ledger_pair_not_cited` for row S001 and `unadjudicated_citing_pair` for row **S002** (the ledger now adjudicates the wrong row of the pair it shares a file with).

**Actual:** **exit 1**, `verdict failed`, `citingPairs 2`, `ledgerPairs 1`, findings `[{id:unadjudicated_citing_pair, row:"S002", file:"corpus/knowledge/freshness-pins.json"}]` — **one** finding, not two.

**Discrepancy, resolved against my own declaration:** my expectation was arithmetically wrong. Ledger after mutation = `{(S001,file)}`; that pair *is itself cited* by the corpus file, so it is not "not cited"; and S002 is now the only citing pair absent from the ledger ⇒ exactly one `unadjudicated_citing_pair`. The **gate is correct**; the declaration was not. The mutation is nonetheless causally load-bearing: the reported row **flipped S001 → S002**, so the gate demonstrably matches ledger pairs by **(row, file) identity**, not by row or by count.

Supplementary identity probes (same scratch, declared per probe): adding the missing S001 pair → exit 0 `clean`, findings `[]`; corrupting the ledger *file* path → exit 1 with `ledger_pair_not_cited`(S002, `freshness-pin.json`) + `unadjudicated_citing_pair`×2 (S001,S002 @ `freshness-pins.json`); removing the corpus file → exit 1, `ledger_pair_not_cited`×1, `citingPairs 0`; population row spelled `S0001` → row reported as `S0001` (numeric identity); ledger file prefixed `./` → identical to pristine; identical content moved to a `.md` path with the ledger updated → identical finding shape, file renamed. Cwd/extension/root-relative resolution all behave as documented.

## 4. Findings

**F1 — MEDIUM (observability of the fixture oracle; cross-cutting, already reported by AttackCase01/03/04/05 — independently re-confirmed here, with a fixture-22-specific proof).** The fixture oracle pins only exit + the finding-id multiset; `expected.json` carries no row/file, and `finding_ids()` (`scripts/citing_set_selftest.py:144-165`) + `run_case()` (`:274-282`) discard `row`/`file`. Fixture-22-specific decisive form: the **mutant** of §3 — whose ledger adjudicates S001 instead of S002, so the semantic subject of the case changed — was run through the **real** frozen runner carrying the **pristine** `expected.json`: `verdict clean, failed 0, case ok=true, expected {exit:1, findings:["unadjudicated_citing_pair"]} == actual {exit:1, findings:["unadjudicated_citing_pair"]}`. The fixture cannot distinguish "S001 is the missing pair" from "S002 is the missing pair". Independently, a scratch **oracle-blindness probe** (a stub that emits each case's expected id multiset with `row:"WRONG-ROW"`, `file:"wrong/nonexistent-file.md"` — a probe of the harness, not a gate, and not passing credit) run over all 29 live fixture copies reports `verdict clean, cases 29, failed 0`: a gate naming the wrong row/file for every omission is invisible to the whole fixture layer. **Mitigation (measured, not asserted):** the wave-level C2 measurement *does* pin identity — `c2_count.py:26-27` compares exact `(row,file)` sets against the frozen 16-pair oracle; my run `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision ac46a747…` → exit 0, `expected 16, detected 16, falsePositive 0, passed true`. So the real detection is identity-pinned one layer up; the gap is confined to the 29-case fixture suite.

**F2 — LOW (fixture provenance, inert in the gate).** `22-json-knowledge-file-citation/ledger.json` carries `"report": "w1/PairS002Freshness-Pins.md"`, and **that path does not exist anywhere in the repo** (the actual W1 pair reports are `w1/Pair02A.md`/`w1/Pair02B.md`, matching `pairs.json`'s `reviewA`/`reviewB` fields). This contradicts `w1/BuildFixtures.md:14`'s own declaration "nothing referenced outside the case dir". The field is **inert**: `load_ledger()` reads only `row` and `file`; no shipped consumer reads `report`/`statements`/`stale`. All 29 fixtures carry such dangling pointers (66 refs), so this is a suite-wide fixture-producer defect, not fixture-22-specific. Effect: a human auditing this case's adjudication follows a dead pointer.

**F3 — LOW/INFO (fixture is a synthetic miniature; no wave-level counterpart).** The fixture's `corpus/knowledge/freshness-pins.json` is *not* the real corpus file (sha `7b67f226…` vs real `2db3d777…`), and the real `corpus/knowledge/freshness-pins.json` cites **no** registry row at all (grep for `S[0-9]{3,}` → empty); the wave ledger adjudicates S002 at `corpus/knowledge/static-canonical-preflight.md`, not at `freshness-pins.json` (`pairs.json`). The miniature is internally consistent and legitimate as a fixture, but fixture 22 does not mirror any real (row,file) pair, so it exercises no real adjudication.

**F4 — INFO (coverage; already reported by CliJson F12 / AttackCase12 / AttackCase18 — re-confirmed).** The 29 fixtures give `GitSource` **zero** coverage: `run_case()` never passes `--revision`, and `c2_count.py` also runs the gate working-tree-only. Independently measured: in `--revision` mode `GitSource.read_document` issues `git show <rev>:<relative>`, which resolves **repo-root-relative, not `--root`-relative**; `--root <fixture dir> --revision <sha> --population population.json` → exit 2 `input_invalid`/`git_command_failed`, and `--root <fixture dir> --revision <sha>` from a non-repo dir → exit 2 `revision_not_found`. Fixture 22 is therefore unexercisable in blob mode against the project repo (a disposable scratch git repo is required). Also confirmed: `--root` = repo root with the fixture's docs repo-relative scans the **real** 26-file corpus (12 findings), i.e. git mode and working-tree mode are not interchangeable for a fixture directory.

## 5. Operability positives (measured)

- Fixture 22 is **uniquely load-bearing and non-redundant**: it is the only case in the suite whose corpus file is `.json` (suite census: 1 `.json` vs 30 `.md`). Deleting the one `.json` corpus file across all 29 copies (simulating a `.md`-only corpus reader) → runner exit 1, `failed 1`, and the **only** failing case is `22-json-knowledge-file-citation` (`expected ["unadjudicated_citing_pair"], observed ["ledger_pair_not_cited"]`). No other fixture can catch a gate that skips non-markdown knowledge files; fixture 22 is the sole discriminator for the property its name claims.
- The fixture is a genuine negative control, not a constant-output stamp: 7 distinct input perturbations produced 4 distinct outcomes (exit 0 clean; exit 1 with 1 finding; exit 1 with 1 `ledger_pair_not_cited`; exit 1 with 3 findings), and the runner rejects each mutant on exit or id-multiset mismatch (runner exit 1, `failed 2` on the add-pair and bad-file variants).
- Deterministic and cwd-independent; gate/runner sha256 pinned to the candidate blob.

## 6. Verdict, residual risk, verification gaps

**Verdict: no behavioural defect in the gate or in fixture 22's expectations.** `expected.json` agrees with the independent derivation on exit, id multiset **and** row/file identity; the real frozen gate reproduces it exactly on a scratch copy from an unrelated cwd; the real consumer runner is green (29/29, ≥12 required) and rejects every mutant I fed it. My §3 declared expectation was wrong and the gate was right — recorded as such.

**Residual risk:** (a) F1 — the 29-case fixture layer cannot see row/file misattribution; a gate that reported the wrong row for all 16 omissions would still pass every fixture (only `c2_count.py` pins identity, and it is a different corpus). (b) F2 — every fixture's `report` pointer is dead, so fixture ledger provenance is unverifiable by following it. (c) F3 — the fixture asserts no real adjudication, so its green proves grammar handling, not real-world adjudication.

**Verification gaps / not established here:** (i) the `--revision`/blob path of the gate on fixture-shaped inputs is unexercised by any shipped consumer (F4) — I characterised it but did not measure a *correct* blob-mode fixture run, because the project repo's blob layout makes it impossible without a disposable repo; (ii) I did not mutate the gate source (read-only lane), so "would a wrong-identity gate pass the wave-level C2 oracle?" is answered only for the fixture layer, not for `c2_count.py`; (iii) `statements`/`stale`/`report` inertness was established by grep of the shipped consumers, not by a runtime probe; (iv) fixture 22's `.json` corpus file is a synthetic miniature, so no real-world JSON knowledge file was exercised.

No installs, upgrades, or tool changes were required; none were performed. Python 3.14.4, git, coreutils only.
