# AttackCase11 — consumer fixture `11-duplicate-ledger-pair` (operability, r27-fresh-falsification)
Seat `KakeR27.AttackCase11` (leaf, read-only source). Frozen candidate
`ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. Scratch `/fast/scratch/hyaku/kake-r27/AttackCase11/` only;
`TMPDIR`/`HOME` explicit; no source edit/commit, no live-fixture write, no install.

## 1. Authority / bytes (verified before any run)
`HEAD` = `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` = frozen-candidate `candidate`; tracked files clean.
All sha256 vs `frozen-candidate.json:sourceFiles` → **MATCH**: `scripts/citing_set.py` `3a361a002f66ce16`,
`11-…/expected.json` `86c9a51aaa8ad6d7`, `ledger.json` `e706947827ca474c`,
`population.json` `4fe30045f3fa0329`, `corpus/knowledge/crawl-scope-per-host.md` `0420185517eddaa6`.
## 2. Independent expectation — declared BEFORE running the gate
Input read: population rows `["S001","S002"]`; ledger = **two identical** `(S001,
corpus/knowledge/crawl-scope-per-host.md)`; corpus file cites only `S001` (my own token scan: literals
`['001']`, ranges `[]`). Derived: citing set = 1 pair `(S001, crawl-scope-per-host.md)`; `S002` is in the
population but cited nowhere → not a citing pair, no finding; that pair IS in the ledger → no
`unadjudicated_citing_pair`; the ledger pair IS cited → no `ledger_pair_not_cited`; it is duplicated →
one `ledger_duplicate_pair` (one per distinct duplicated key, not per occurrence).
**Expected exit 1, finding-id multiset `["ledger_duplicate_pair"]` ×1.**
`expected.json` = `{exit:1, findings:["ledger_duplicate_pair"]}` → **agrees**.

## 3. Baseline — real frozen gate CLI, scratch copy, unrelated cwd
`cd …/AttackCase11/cwd`; `TMPDIR=…/tmp HOME=…/tmp python3 -B
/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py --root …/AttackCase11/base
--population population.json --ledger ledger.json --json` → `verdict failed`, `citingPairs 1`,
`ledgerPairs 2`, `findings [{id ledger_duplicate_pair, row S001, file
corpus/knowledge/crawl-scope-per-host.md, occurrences 2}]`, exit **1**. **Identity check (not just id
tally): row/file/occurrences match the duplicated ledger key exactly. ✅**
Consumer paths: real runner on scratch fixture dir → `clean, cases 1, failed 0`, exit 0; real
`citing_set.py --root <repo> --selftest` → `clean, cases 29, failed 0`, exit 0, case 11 `ok:true`; runner
`--min-cases 12` → `meetsContractMinimum true`, exit 0.

## 4. Causally meaningful input changes (expected declared per row; 9/9 matched)
|#|scratch change|declared expected|observed|
|---|---|---|---|
|A|`pairs[1].row`→S002|dup dissolves → `ledger_pair_not_cited(S002)` only; exit 1|exactly that ✅|
|B|`pairs[0].file`→other-host.md|unmatched entry → `ledger_pair_not_cited(S001,other-host.md)`; no unadjudicated; exit 1|exactly that ✅|
|C|drop duplicate (1 pair)|all checks pass → `clean`, exit 0, no findings|`clean`, exit 0 ✅|
|D|add 3rd identical entry|one distinct key → one finding, `occurrences:3`; exit 1|exactly that ✅|
|E|F|G|payload changed (`statements:99`, other `report`) / spelled `./corpus/…` / spelled `S0001`|identity is `(row,file)`; `./` and numeric-id normalisation fold to the same key → still duplicate|dup `occurrences:2`, row `S001` ✅|
|H|I|two distinct dup keys (S001×2, S002×2) / dup key not cited (S002×2)|2 `ledger_duplicate_pair` + `ledger_pair_not_cited(S002)` / + `unadjudicated_citing_pair(S001)`|exactly 3 each ✅|
Multiplicity confirmed empirically: one finding per **distinct** duplicated key, never per occurrence
(D vs H) — case 11's single-id expectation is correct, not under-specified.

## 5. Discrimination audit — case 11 is NOT vacuous
Scratch gate mutant with duplicate detection suppressed (`gate-nodup.py` sha `9c05dbb4b82f3a85…`) →
`clean`/exit 0 → runner `exit mismatch: expected 1, observed 0`, `RUNNER_EXIT=1`. Scratch `expected.json`
mutated to two `ledger_duplicate_pair` ids → runner `finding-id mismatch`, exit 1.

## 6. Findings by severity
**F1 — MEDIUM (coverage/detection gap, NOT a candidate defect): the frozen fixture format pins no
finding identity.** `expected.json` (contract `fixtureInterface`: `{exit:int, findings:[ids]}`) records
only exit + id multiset; `row`, `file`, `occurrences` are never asserted. Three scratch gate mutants
each pass **all 29 cases** with `verdict clean, failed 0`, exit 0: `gate-mutant.py` (sha
`34ee17720026f84a…`) rewrites the duplicate finding to `row S999` / `file
corpus/knowledge/WRONG-ATTRIBUTION.md`; `gate-mutant2.py` (sha `9f0d86ee618ce496…`) rewrites `row`/`file`
on all three pair-scoped findings; `gate-mutant3.py` (sha `5bf545a554287fc3…`) hard-codes `occurrences: 1`.
The real gate's attribution in case 11 is **correct** (§3) — a *detection* gap in the contract-mandated
fixture format, unfixable without changing `fixtureInterface`; expected outcomes must not be redefined.

**F2 — LOW (latent gate defect; no effect on the frozen C2 count): ledger `file` paths are normalised
differently from CLI paths → double false positive.** `normalize_relative()` (CLI args) drops empty
segments (`a//b`→`a/b`); `normalize_ledger_file()` (ledger pair `file`) only strips `./` and `\`.
Evidence: one ledger entry `file="corpus/knowledge//crawl-scope-per-host.md"` (the same real file) →
exit 1 with **two** findings for one file: `ledger_pair_not_cited(S001,
corpus/knowledge//crawl-scope-per-host.md)` **and** `unadjudicated_citing_pair(S001,
corpus/knowledge/crawl-scope-per-host.md)` — a false positive against C2's "no false positives".
Impact on the frozen measurement: **none observed** — all 41 `file` refs in
`.ufo/waves/round-27/frozen/ledger.json` are canonical (`//`, leading `/`, `..`, `./` absent; each resolves
to an existing file), so 16/16 C2 is unaffected. Latent; only a non-canonical writer reaches it.

**F3 — INFO (by design): the C2 gate is presence-only; it ignores `verdict`.** A ledger entry with
`verdict:"UNVERIFIABLE", kind:"source"` still satisfies the citing pair → `clean`, exit 0. Correct for
C2's scope (missing-pair completeness); C1 is measured separately by `count_c1.py`. Flagged so C2-green
is never read as C1-supported, preserving C1's UNPROVABLE status.

## 7. Residual risk / verification gaps
- C1 (strict support) is out of this seat's scope; nothing here asserts 58/58 decided. C2-clean ≠ C1-
  supported (F3). The 29-case suite is blind to mis-attributed `row`/`file` and to a wrong `occurrences`
  count (F1); covering it belongs in `fixtureInterface`, not in a fixture rewrite.
- F2 is unexercised by any fixture; a ledger ref spelled `corpus/knowledge//x.md` would expose it.
- Not tested here: `--revision` (Git-blob) mode for this fixture (runner uses working tree);
  `git_name_selftest.py` not re-run (out of scope).
- `scripts/__pycache__/citing_set.cpython-314.pyc` appeared untracked in the live repo during the
  window (mtime 19:03:01); every invocation here used `python3 -B` and ran the gate only as a script
  (never imported), so it is not from this seat — left untouched (foreign write).

## 8. Integrity after all work
`HEAD` still `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`; `git status --porcelain scripts/` → no tracked
modification; live `citing_set.py` sha `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`;
live fixture `expected.json` sha `86c9a51aaa8ad6d73efe145825c7afd5eff1722257a0f19de851e3ded4b2356f`. Only
scratch under `/fast/scratch/hyaku/kake-r27/AttackCase11/` written.

## 9. Verdict
The committed expectation is **independently correct**; the frozen gate produces exactly it with correct
row/file attribution and correct multiplicity semantics (9/9 declared predictions matched). The fixture
**is not vacuous** — it fails a duplicate-detection-suppressed gate and a wrong-multiplicity expectation.
Two scoped weaknesses, neither a wrong answer and neither affecting the frozen C2 count: **F1**
(contract-level fixture format cannot detect mis-attributed findings) and **F2** (latent ledger path-form
false positive, unreachable with the canonical frozen ledger). No source edit proposed or made. Tools:
system `/usr/bin/python3` 3.14.8 (`-B`); **no install/upgrade/service mutation** (none needed).
