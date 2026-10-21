# ReviewSkillRegistry — r27 fresh falsification (operability)

Target: frozen candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
Attacked items: `SKILL.md` round-27 section (lines 596–661) and its 3 registry rows
(`SKILL.md:616` citing-set, `:617` knowledge-citing-count, `:618` citing-set-frozen-count).
Read-only seat: no source edit, no commit, no r24/r26 gate execution, no GET.
Scratch: `/fast/scratch/hyaku/kake-r27/ReviewSkillRegistry/{tmp,out,fx,proto}`; `TMPDIR` set explicitly; no `/tmp`, no `/dev/shm`.

Provenance: working `SKILL.md` blob `4aad7999fe72ac7bfd7edd03cb7a642eb8714617` == candidate blob;
`scripts/citing_set.py` `352a471abec08daa56a0fb7ef23fe78f2930d773`, `scripts/citing_set_selftest.py`
`c69b09b2e47f4115aa4e8ff286aa7cfe0e171a64` == candidate; `git status --porcelain` shows only pre-existing
untracked wave artifacts before and after every probe (no repo write by any gate/selftest).

## Probes (expected declared before running → actual)

| # | command (cwd) | declared expected | actual |
|---|---|---|---|
| P1 | `python3 -B <abs>/scripts/citing_set.py --selftest` (scratch, unrelated cwd) | exit 0, verdict clean, cases ≥12 | exit 0, clean, `cases=29, failed=0`, `root`/`fixtures` resolved to repo, stderr empty |
| P2 | `python3 -B scripts/citing_set.py --root . --revision ac46a74… --population .ufo/waves/round-26/population.json --ledger .ufo/waves/round-27/complete-ledger.json --json` (repo) | exit 0 clean, citingPairs=ledgerPairs=58, findings empty, corpusFiles 26, populationRows 32 | exit 0, clean, `citingPairs 58 / ledgerPairs 58 / findings [] / populationRows 32 / corpusFiles 26 / outsidePopulation 18`, `source=git` |
| P3 | `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a74…` | exit 1 (strict, UNVERIFIABLE unresolved), reviewed 58, decided <58, unknown pairs >0 | exit 1; `citingPairs 58, reviewedPairs 58, decided 55, knownUnverifiableUnits 7, knownUnverifiablePairs 3, ledgerRecordedUnverifiableUnits 6`; missing S001/ghp-served-set.md, S007/ghp-custom-domain.md, S033/static-canonical-preflight.md |
| P4 | `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision ac46a74…` | exit 0, detected 16, falsePositive 0 | exit 0; `expected 16, detected 16, falsePositive 0, passed true, gateExit 1`, `frozenRevision 83528f7…` |
| P5 | `python3 -B .ufo/waves/round-27/count_c1.py --selftest` | exit 0, all cases pass | exit 0, `failed 0` (10 cases; `inherited_ledger_tamper` → exit 2) |
| P6 | `python3 -B .ufo/waves/round-27/c2_count.py --selftest` | exit 0, all cases pass | exit 0, `failed 0` (3 cases: `frozen_missing_interior`→0, `snapshot_tampered`→2, `oracle_rewrite_not_blessed`→2) |
| P7 | `python3 -B .ufo/waves/round-27/git_name_selftest.py --gate scripts/citing_set.py --tmpdir …/tmp` | exit 0, clean, tree/Git identities equal over 5 filename shapes | exit 0, `verdict clean, cases 30, failed 0`; 5 identities (alpha, `naïve-Ω`, space, tab, newline) identical in both modes; `gateSha256 3a361a00…` |
| P8 | `python3 -B .ufo/waves/round-27/fetch_group.py --selftest` | exit 0, offline, no network | exit 0, `failed 0`; module imports no http client (fetch delegated to r26 `fetch_sources.py` helper) |
| P9 | `python3 -B scripts/citing_set.py --root . --population … --ledger … --json` (no `--revision`) | exit 0 clean 58/58 | exit 0, clean, `citingPairs 58 / ledgerPairs 58`, `source=working-tree` |
| P10a | `python3 -B scripts/citing_set.py --root .` | exit 64 usage | exit 64, `error: usage: missing required option(s): --population, --ledger` |
| P10b | `--population nope/missing.json` | exit 2 `input_invalid` | exit 2, finding `input_invalid/document_unreadable` |
| P10c | scratch corpus with `S010-S001` | exit 1 `citation_range_invalid` | exit 1, `citation_range_invalid / descending_range` |
| P11 | documented `python3 -B scripts/citing_set.py --selftest` from repo root | exit 0, 29 cases | exit 0, clean, 29 cases |
| P12 | pre-NUL prototype `.ufo/waves/round-27/before/citing_set_git_names.py` vs final gate, Git mode, newline filename | prototype loses the identity and fails; final keeps both | prototype exit 2 `input_invalid/git_command_failed`, `citingPairs 1`; final exit 1, `citingPairs 2` → `before/` is a real red input, not a claim. `beforeSha256 fffaa667…` == file on disk, `afterSha256 3a361a00…` == `scripts/citing_set.py` |

Pin/code-map checks (read-only): `frozen/expected.json` = 28 sha256 entries = 26 corpus + `population.json` + `ledger.json`
(matches the row's "26 corpus inputs + population/ledger,28 total"); `git diff be375d9…ac46a74` over
`c1-before.json`, `c2-oracle.json`, `frozen/expected.json`, `contract.json`, r26 `statements.json`, `population.json`, `measure.py` = empty;
`c1-before.json` cites 57 pairs/16 missing; `c2-oracle.json` `expectedPairs 16`, `expectedExit 1`, `frozenRevision 83528f7…`;
`complete-ledger.json` 58 pairs, `derivedFrom [r26 statements.json, r27 pairs.json]`; `pairs.json` = 17 new + 1 carried override;
manifest 8 entries — code rows `receivedSha256==sha256`, `rawHttpBodyRetained true`; HTML rows differ, `public_visible_text`, `rawHttpBodyRetained false`;
registry table: header 8 cells, exactly 3 rows of 8 cells, no 4th row; `before/` referenced by no script (no production alias); no `jj` in r27 scripts.

## Findings (author-side)

**F1 — MEDIUM. The artifact SKILL.md designates as the exact stricter interpretation contradicts the delivered CLI.**
`SKILL.md:630` points to `strict-c1-disposition.json` as "Exact original baseline and stricter interpretation". That file lists
`unresolved` = S001(3 units) + S033(3 units) only, states "Six inherited unknown units in two pairs remain explicit", and predicts
"candidate56/58 strictly decided". The delivered CLI (P3) reports **7 unknown units in 3 pairs** (S001 3, S007 1, S033 3) and **55/58 decided**.
The section's final carry-correction paragraph carries the 7/3 figure, so SKILL.md itself is not wrong — but the pointer artifact is stale,
and `carry-errata.json` (S007 unit) is not reflected in the disposition's `unresolved` list. Fix scope: add S007/ghp-custom-domain.md(1)
to `strict-c1-disposition.json.unresolved` and restate the arithmetic line (7 units / 3 pairs; 55/58 decided); then the SKILL.md pointer is exact.

**F2 — LOW. Stale numeral inside the strict round27 measurement note.** `SKILL.md:620-622` states "review-complete inputs with six inherited
unknown units remain exit1"; the CLI reports `ledgerRecordedUnverifiableUnits 6` but `knownUnverifiableUnits 7`. Self-corrected later in the
same section ("The earlier six description is not the total"), yet the earlier sentence reads standalone. Suggest "six ledger-recorded plus one
report-disclosed (7 total, 3 pairs)".

**F3 — LOW. Dead path in the round-27 code map.** `SKILL.md:602` cites `pairs.json` unqualified; the only such file is
`.ufo/waves/round-27/pairs.json` (no repo-root `pairs.json`). Every other reference in the section is path-qualified. Suggest
`.ufo/waves/round-27/pairs.json`.

**F4 — INFO. Two runnable round-27 tools have prose only, no registry row.** `git_name_selftest.py` (P7) and `fetch_group.py` (P8) are
documented in prose with invocation but have no row, so their verdict map/write scope sit outside the table; the r26 precedent
(`source-recheck-counter` row) suggests rows for both. Both run clean as delivered.

## Residual risk / verification gaps

- Not run: `fetch_group.py` default GET mode (no live GETs) and `--sanitize-existing --root .` against the live repo (it writes the repo's
  `fetched/` dir — a source write, forbidden for this seat). Idempotence of the offline migration is covered only by fixture cases, not on the
  live manifest.
- Not verifiable from artifacts: fixture producer/runner author separation (process fact); C1 semantic truth of each HOLD/STALE (out of this lane).
- The `used-by` exclusion is regex-level and the gate scans `corpus/knowledge` only — lesson/SKILL citations are out of its scope by design.
- `git_name_selftest.py` defaults to a shared scratch root (`/fast/scratch/hyaku/kake-r27`) unless `--tmpdir` is passed; SKILL.md documents
  the explicit `--tmpdir`, so the delivered path is safe.
- No tools installed; no pacman transaction; no system change.

Verdict: the round-27 section and its 3 registry rows are operable as delivered — every documented entry command runs clean from an
unrelated cwd with the exact verdict maps claimed (0/1/2/64), all three selftests pass, the pinned counts (29 cases, 28 frozen inputs,
16-pair oracle, 57 baseline, 58 obligations) reproduce, and no capability is pre-claimed from an unrun check. Three documentation defects
(F1 medium, F2/F3 low) and one registry-completeness gap (F4) remain; F1/F2 are the same stale six-unit figure and should be repaired
together in the disposition file and the note.
