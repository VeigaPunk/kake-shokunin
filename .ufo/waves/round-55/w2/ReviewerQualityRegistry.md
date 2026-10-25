# ReviewerQualityRegistry

ATTACKS: `corpus/QUALITY.md` §Round-55 criteria (5) and `SKILL.md` §Round 55 gate registry additions (2 rows, L1233–1234), all read at a7a548e102b71bd16b0a6ddafa469393a2c98b69 via `git show`.

Worktree note: `git rev-parse HEAD` → 78963ae28e1c6a409a1a1322230c5671cd2efcbe; `git diff --stat a7a548e HEAD -- .ufo/waves/round-55/c55_readme_index.py .ufo/waves/round-55/c55_quote_truth.py corpus/QUALITY.md SKILL.md` → empty, exit 0, so the worktree entry-command runs executed the pinned bytes. All other reads used `git show a7a548e:<path>`. Counter sources were also extracted to a `mktemp -d` scratch and grepped there (originals read-only).

## CRITERIA

Legend per criterion: grounded (path/lesson/counter exists and says what it is cited for) / falsifier real (command exists; fails on stated base where one is named) / new vs QUALITY L1–1145 / lesson cited (LEARNING.md:35 — "a criterion is added with no lesson behind it" → discernment harmed; LEARNING.md:59 — "every criterion cites the lesson that produced it"; fleet-root `/home/vgpnk/Projects/shokunin/LEARNING.md`, unrevisioned worktree read — the lane has no LEARNING.md).

1. **Entry lands with its index row** (QUALITY §Round-55, criterion 1)
   - Grounded: YES. `corpus/lessons/round-55.md` §Mistakes has the `reference-drift` row ("21 of 46 … named by no row of the README coverage map", cites the same base control). `.ufo/waves/round-55/controls/base-c1-readme-index-v2.txt` exists; headline `C1 readme-index index_mismatches=21 knowledge_files=46 met=False`, `unindexed=21`.
   - Falsifier: REAL. Ran `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d` → `index_mismatches=21 knowledge_files=46 met=False`, `unindexed=21`, exit 1 (red on stated base, matches receipt). At `--revision a7a548e…` → `index_mismatches=0 knowledge_files=49 met=True`, exit 0; prints `index_mismatches=0` as required. Named junk cases all exist in the pinned selftest source: `fail_mega_row` (L297), `fail_constant_cell` (L292), `fail_swap_population` (L317), `fail_head_edited_to_fit` (L321).
   - New: YES — no prior QUALITY criterion (L1–1145 grep `coverage map|index row`) mentions the coverage map.
   - Lesson cited: YES (`corpus/lessons/round-55.md` exists).
   - Caveat: cites `CORPUS.md` bare; no path of that name exists in the lane at a7a548e (`git ls-tree -r a7a548e | grep -i corpus` → no CORPUS.md; worktree `ls` → absent). Resolves only out-of-tree (see DEFECTS 4).

2. **New quotes ≤ 25 units** (criterion 2)
   - Grounded: YES. `corpus/lessons/round-54-verifier-spotcheck.md` routed defect 3 = "CJK ≤25-word rule remains open. S367/S372/S373 quotes (31/27/27 units) … do not carry 'units' as de-facto compliance" — exactly the ambiguity the criterion says it stops growing. `.ufo/waves/round-55/w1/ExecStagedQuoteAudit.md` L110: "Over the 25-unit ceiling: **6 of 6**". `.ufo/waves/round-55/w1/CriticC2Contract.md` A1 family present (L28).
   - Falsifier: none named in the criterion; enforcement is C2 counter condition C5 (`C5_quote_truth`, c55_quote_truth.py L390; navigation-string junk case `fail_boilerplate_quotes` in selftest). Counter exercised red/green below. Unit rule in code matches the criterion: `units()` docstring "One unit per CJK character, one per non-CJK whitespace token" (L167–169); 3 unit-rule selftest checks passed.
   - New: YES as a hard ceiling (raw substring, content block, ≥3 page-unique spans). Derivative of the round-54 criterion "CJK quote length names its unit…" (QUALITY L1131–1142: same unit convention, same S367 31-unit overrun) — that one is a reporting rule, this is a ceiling; not a duplicate, but the tightest prior row is one round old.
   - Lesson cited: YES (`round-54-verifier-spotcheck.md` exists).

3. **Held row reuse changes `used-by` only** (criterion 3)
   - Grounding: PARTIAL. `CORPUS.md` SOURCES rule 2 verified at the canonical path `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` L116–117: "Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round lesson" — says exactly what the criterion cites. But `CORPUS.md` names no in-lane path at a7a548e (see DEFECTS 4). Counter conditions exist: `C3_row_shape` (L297) and `C4_used_by` (L309) in c55_quote_truth.py, exercised by `fail_held_row_cell_changed`, `fail_used_by_dropped_prior`, `fail_used_by_not_extended` (all in the 50/50 selftest).
   - Falsifier: REAL. Ran `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision fcaf4b85…` → `C2 quote-truth 0/8 met=False` with `C3_row_shape FAIL` and `C4_used_by FAIL` lines, exit 1.
   - New: YES — no prior `used-by` criterion in QUALITY L1–1145.
   - Lesson cited: **NO** — grounding names CORPUS.md and counter conditions only; round-55 §Mistakes has no used-by row. Per LEARNING.md:35 this criterion is `harmed` as filed.

4. **A validated append block is the appended block** (criterion 4)
   - Grounded: YES on artifacts. `w1/CriticC2Contract.md` A6 (L49 "census receipt forged, census never run") and A8 (L58 "validated document is not the appended block") exist and match; counter condition `C7_validate_before_append` (L468) exists.
   - Falsifier: REAL. All three named selftest fixtures exist — `fail_validated_doc_differs` (L777), `fail_census_forged_shape` (L768), `fail_validated_entry_differs` (L701) — and `--selftest` passed 50/50 exit 0, so each fails its mutant as expected.
   - New: YES — no prior QUALITY criterion on census-validated vs landed identity (L1–1145 grep `census|append block`).
   - Lesson cited: **NO** — though `corpus/lessons/round-55.md` §Mistakes `vacuous` row covers the same evidence ("a forged census receipt", citing CriticC2Contract A1–A8), the criterion does not cite it. A lesson exists behind it but is uncited; per LEARNING.md:59 it must be named.

5. **A counter is attacked before it scores** (criterion 5)
   - Grounded: YES. `w1/MutC1Counter.md`: "SURVIVED: M01, M05, M07, M08, M10, M11, M12, M13, M14 (9)" of 16 mutants — matches "9 of 16 mutants survived the version-1 selftest". `corpus/lessons/round-55.md` §Mistakes `vacuous` row exists and cites the same artifacts.
   - Falsifier: procedural; no command named. Supporting runs: pinned C1 `--selftest` → 35/35 exit 0 (v1 was 10/10 per MutC1Counter.md), C2 `--selftest` → 50/50 exit 0; M13's facts-assertion recommendation landed (selftest `case()` asserts fact dicts, e.g. `{"knowledge_files": N, "coverage_rows": N}`, L276).
   - New: YES as a general gate-ordering rule. Antecedents exist (QUALITY ~L311 round-28 "Show it with one recorded mutant"; ~L557–559 round-32 mutation probe) but none generalizes; not duplicates.
   - Lesson cited: YES.

## REGISTRY ROWS

Eight cells per row: Name / Kind / Entry command / Verdict map / Self-test / Pinned values / Write scope / Owner.

**Row 1 `readme-index-counter`** (SKILL L1233)
- Name, Kind, Owner: present, kind "gate (offline, committed bytes only; no network)" — source confirms: measure reads via `git show`/`git ls-tree` subprocesses only, no network code.
- Entry command: RUNS. `--revision a7a548e…` → exit 0 `index_mismatches=0 knowledge_files=49`; `--revision fcaf4b85…` → exit 1 `index_mismatches=21`.
- Verdict map: MATCHES code+runs. `0=met` predicate string byte-equal to `PREDICATE` L58 and to `contract.json` `claims.C1.predicate`; `1=not met` over the seven terms (TERMS L226; floor 46, L59); `2=could-not-evaluate` at tree/README unreadable (L133), wrong section count (L136), no table (L145); bare run (no `--revision`) → argparse usage + exit 2, observed.
- Self-test: command real, ran → `c55 readme-index selftest: 35/35`, exit 0 — matches the cell's "35 fixtures". **But the cited receipt `.ufo/waves/round-55/controls/c1-selftest-v2.txt` reads `c55 readme-index selftest: 32/32`** — see DEFECTS 2.
- Pinned values: contract predicate exact; base control exists and reproduced (21, exit 1 at fcaf4b85); "version-1 control kept as history" — `base-c1-readme-index.txt` exists in controls/.
- Write scope "none … selftest writes only `mktemp -d` sandboxes": matches source — `_fixture` uses `tempfile.mkdtemp`, `git init` inside, toplevel equality asserted (L229–236).

**Row 2 `yahoo-robots-quote-truth-counter`** (SKILL L1234)
- Name, Kind, Owner: present; source reads `git show`/`git log` only, no network.
- Entry command: RUNS. `--revision a7a548e…` → `C2 quote-truth 8/8 met=True`, exit 0; `--revision fcaf4b85…` → `C2 quote-truth 0/8 met=False`, exit 1.
- Verdict map: MATCHES. 0 = 8/8; 1 = any C1–C8 fail (conditions C1–C8 at L248–536); 2 = malformed receipt/mirror-pin JSON (L401, L482) or exception (L538–542); bare run → usage, exit 2, observed.
- Self-test: command real; ran with `KAKE_R55_SELFTEST_REV=a7a548e…` → `c55 quote-truth selftest: 50/50 (fixture revision a7a548e102b7)`, exit 0. Numbers check out exactly: 47 sandbox fixtures (`cases` dict seeded with `"pass"` L615 + 46 `@case` registrations) + 3 unit-rule checks (`unit_checks`, L797–799) = 50. **But the cited receipt `.ufo/waves/round-55/controls/c2-selftest.txt` does not exist at a7a548e** — see DEFECTS 1.
- Pinned values: `contract.json` `claims.C2` present; base control exists and reproduced (0/8, exit 1); `.ufo/waves/round-55/sources/receipts.json` and `.ufo/waves/round-55/assimilation/mirror-pin.json` both exist at a7a548e.
- Write scope "none … selftest writes only `mktemp -d` sandboxes": matches source (`_build` → `tempfile.mkdtemp(prefix="c55-qt-")`, L551).

## DEFECTS

1. **Dangling selftest receipt (row 2).** SKILL L1234 cites receipt `.ufo/waves/round-55/controls/c2-selftest.txt`; `git show a7a548e:.ufo/waves/round-55/controls/c2-selftest.txt` → `fatal: path … does not exist`; `git ls-tree --name-only a7a548e:.ufo/waves/round-55/controls/` lists 7 files, none named c2-selftest; tree-wide grep for `round-55.*c2-selftest` finds nothing. The counter itself passes 50/50; the row's frozen-proof pointer is broken.
2. **Stale selftest receipt vs row number (row 1).** SKILL L1233 claims "35 fixtures" and cites `controls/c1-selftest-v2.txt`, whose only line is `c55 readme-index selftest: 32/32`. Observed pinned-counter run: 35/35 exit 0. The frozen proof contradicts both the row and the code (receipt predates the final v2 counter). Corroboration: `corpus/lessons/round-55.md` §Mistakes fix cell also says "selftest 32 fixtures".
3. **Criteria 3 and 4 cite no lesson (LEARNING.md exposure).** LEARNING.md:35 counts "a criterion is added with no lesson behind it" as discernment `harmed`; :59 requires "every criterion cites the lesson that produced it". Criterion 3 has no behind-lesson anywhere in round-55 §Mistakes; criterion 4's evidence is in the `vacuous` row but uncited by the criterion. Criteria 1, 2, 5 cite existing lessons and are clean.
4. **Bare `CORPUS.md` citations resolve outside the lane (criteria 1, 3; minor, pre-existing convention).** No `CORPUS.md` in the lane tree at a7a548e or the worktree; content verified at the canonical `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` (SOURCES rule 2) and a vendored fleet-root copy `/home/vgpnk/Projects/shokunin/CORPUS.md`. The round-54 criterion cites "CORPUS.md SOURCES rule 1" the same way, so this is convention, not a new break; unpinpointed to a revision either way.
5. **Frozen contract kill-map mismatch (minor).** `contract.json` `claims.C2.kill` ends "64 usage" while the counter and both registry rows make usage exit 2 (`ap.error`; observed exit 2 on bare runs of both counters). The rows match the code; the contract's kill cell carries a stale 64 from the round-52-era rows.

## Residual risk and verification gaps

- I did not run the C2 selftest unpinned at worktree HEAD (unrun); the pinned run (`KAKE_R55_SELFTEST_REV=a7a548e…`) is the one that evidences this revision, and the script defaults to HEAD if the env var is unset.
- I did not run `.ufo/waves/round-55/validate_append.sh` (it regenerates receipts — a write path a leaf reviewer must not trigger).
- Exit-2 branches for unreadable tree / section-count / no-table were verified in source, not by fault injection (unrun as executed cases).
- LEARNING.md was read at the fleet-root worktree, not a pinned revision; the lane itself contains no LEARNING.md.
- Everything else above is observed output at a7a548e; no claim in this report rests on an unexecuted check except the four items marked unrun here.

VERDICT: criteria all grounded with real, base-failing falsifiers (3 minor grounding caveats: two uncited lessons per LEARNING.md, one out-of-tree CORPUS.md); registry rows' commands, maps and fixture numbers (35; 47+3; exit maps) verified against the pinned counters, but both rows' cited selftest receipts are defective — one stale (32/32 vs 35), one absent.
