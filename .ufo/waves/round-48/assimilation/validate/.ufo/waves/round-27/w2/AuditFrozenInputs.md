# AuditFrozenInputs — r27 fresh falsification (lane: frozen inputs / population / ledger / SOURCES)

Seat: `KakeR27.AuditFrozenInputs` (leaf, read-only source seat; no source edits, no subagents).
Candidate: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. Declarations: `be375d90afc6fc7aca369ab3cf5247bf460aeed2`.
Base: `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`. Scratch only: `/fast/scratch/hyaku/kake-r27/AuditFrozenInputs/` (`TMPDIR` set).
All reads used the explicit candidate hash; `HEAD == ac46a747`; `git status` shows only untracked `.ufo/` wave artifacts.

## Pre-declared expectations (declared before each probe)

- P1: all 28 `frozen/expected.json` inputs hash-match the oracle at BOTH candidate and declarations; frozen corpus copies == base/declarations corpus blobs.
- P2: `frozen/population.json` = 32 rows, byte-identical to the population sha in `r26-fail-open-before.json`.
- P3: `frozen/ledger.json` = 41 pairs / field-sum 313 / 7 stale / 4 reclassified / 6 seatUnverifiable, and byte-identical to r26's filed ledger.
- P4: independent (own) expansion of the citing set over the frozen corpus yields exactly the 16 oracle missing pairs, no extra, no ledger pair outside the citing set.
- P5: `corpus/SOURCES.md` has 35 rows; exactly 6 changed cells, all `used-by`, rows S001–S006; the applied change equals the logged old→new table.
- P6: strict C1 stays non-green (decided < reviewed).

## Results (actual command / exit / output)

P1 — `git show <rev>:<path>` + sha256 for 28 paths × {candidate, declarations, base} × {frozen copy, corpus file}:
- 28/28 frozen inputs match `expected.json` at candidate AND at declarations → **no frozen input rewritten**.
- 26/26 corpus files at declarations and at base match `expected.json` → frozen copies are the original bytes.
- 4 corpus files differ at candidate (append-only, 0 deletions): `ghp-custom-domain.md` +11, `ghp-served-set.md` +33, `sitemap-orphan-audit.md` +25, `static-canonical-preflight.md` +44 (`git diff --numstat`).
- `expected.json` 628b7a05, `contract.json` 6d2d7f51, `c2-oracle.json` 1d038205, `c1-before.json` af55d0a4: identical at declarations and candidate (unchanged targets).
- Counter chain intact: `count_c1.py` a1e46d19@declarations → 26fd8bbb@08014ce → f2632131@9ba102d → 8d4c22ef@candidate; `c2_count.py` 93f39b0f → 913a797f → 913a797f. Original counter bytes remain at declarations.

P2 — population: 32 rows/32 ids; sha `16330e1e…` == `populationSha256` in `r26-fail-open-before.json`. **Unchanged.**

P3 — ledger: 41 pairs; `sum(statements)=313`, `sum(stale)=7`, `sum(reclassified)=4`, `sum(seatUnverifiable)=6`; 6 raw UNVERIFIABLE units sit in 2 pairs (S001/`ghp-served-set` 3, S033/`static-canonical-preflight` 3); `sha256 = c2026376832ad4e41…` == `.ufo/waves/round-26/statements.json` at declarations and at candidate. **Original ledger byte-identical, not rewritten.**
- Erratum arithmetic holds: raw 6 + `carry-errata.json` S007/`ghp-custom-domain` 1 = 7 units / 3 pairs (raw 6 remains a true field sum only).

P4 — own citing-set expansion (literal `S\d{3,}` + hyphen/en-dash/em-dash/`..`/`to`/`through` ranges, intersected with population): frozen corpus → 57 pairs; missing = **exactly the 16 `c2-oracle.json` expectedPairs** (0 extra, 0 undetected); ledger pairs outside citing set = 0; duplicate ledger pairs = 0.
- `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision ac46a747…` → exit 0, `expected 16, detected 16, falsePositive 0, passed true, gateExit 1`. **Original missing-16 set unchanged.**

P5 — `corpus/SOURCES.md`: 35 rows at declarations and at candidate (S001–S035, no add/remove); cell-by-cell diff = **exactly 6 changed cells, all `used-by`, rows S001–S006**; `status/opened/recheck/tier/anchor/teaches/source/kind` byte-identical everywhere. `git diff --numstat` 10/6 = 6 rewritten rows + 4 added prose lines, nothing removed.
- Logged old→new table in `corpus/lessons/round-27.md` §"Source routing changes (only allowed used-by cells)" matches the applied cells **6/6 exactly**; `LOG.md` points to that log.
- Every newly claimed used-by path really contains that id (literal or range) in the candidate tree: claimed-not-cited = ∅ for all six rows.

P6 — `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a747…` → exit 1, population 32, citingPairs 58, reviewedPairs 58, **decided 55**, knownUnverifiable 7 units/3 pairs, unreviewed 0; findings = S001/`ghp-served-set` 3, S007/`ghp-custom-domain` 1, S033/`static-canonical-preflight` 3. At declarations → citingPairs 57, reviewed 41, decided 38, exit 1. **C1 is not green; 58 reviewed ≠ 58 decided.**
- 3 STALE pairs each carry exactly one `[r27-recheck S0NN STALE]` marker in the citing file (S005/sitemap, S005/preflight, S004/served-set).
- Denominator delta: candidate corpus expands to 58 pairs; declarations to 57; **only added pair** = (S013, `corpus/knowledge/ghp-served-set.md`), **no removals** → monotone.

## Findings (author-side, severity order)

**F1 — Medium — registry record contradicts itself.** `corpus/SOURCES.md` (round27 "anchor clarification for S001" paragraph, same commit as the edit) ends "original row cells are not rewritten", yet that commit rewrote six row cells (the `used-by` column, S001–S006). A reader consulting SOURCES.md alone would conclude the registry was untouched this round. The lessons log (`corpus/lessons/round-27.md`) correctly states the mutable/immutable cell split. Suggested wording: scope the sentence to `status/recheck/opened/tier/anchor/teaches/source/kind` and name the six `used-by` cells as the only rewritten cells. No frozen/C1/C2 effect.

**F2 — Low — the six rewritten `used-by` cells are still not exhaustive, and the scope is now inconsistent.** At the candidate tree S001/S002/S004 are also cited by `corpus/lessons/round-20.md`, `round-21.md`, `round-26.md`, `round-26-verifier-spotcheck.md`, `round-7.md` (S003/S005/S006 omit `round-7.md`); none of those files is listed, while `corpus/lessons/round-27.md` now is. The lesson discloses this as debt ("Other registry rows' pre-existing routing exhaustiveness is not claimed repaired") and `w1/CitingSweep04.md` already flagged the same asymmetry for S019, so this is disclosed, not hidden — but the six "allowed" cells remain under-inclusive after the allowed change, and the lesson's claim "route every enumerated knowledge citer" is true only for knowledge files + this lesson.

**F3 — Low — the 57→58 growth is self-authored text, and no artifact says so.** The inherited `ghp-served-set.md` contains S013 only filename-embedded (`…Rejection07S013.md`, preceded by a digit → not a token). The 58th pair exists only because the candidate's own appended line 111 writes a standalone "S013". `discovered-pairs.json` attributes the pair to the *inherited* embedded pointer; the lesson says "conservatively included embedded artifact-reference pair grows the denominator 57→58". The obligation is real, counted, and judged as `artifact` (HOLD = the report contains the quoted string, explicitly not platform support) — direction is conservative (no obligation removed) — but the honest provenance is "made explicit by this round's own adjudication text", which no filed artifact states.

**F4 — Informational (not a defect) — the base "before" state is not re-executable with this oracle.** `c2_count.py --revision 83528f7c…` exits 2 `git_input_unavailable` because `frozen/` postdates the base. The base fail-open therefore rests on `r26-fail-open-before.json` (r26 `measure.py` exit 0, 32/32). My independent expansion corroborates it structurally: the inherited 41-pair ledger covers only 41 of the 57 base citing pairs, so the 16 omitted pairs could not have been inside r26's counted set.

## Uncertainties / limits

- Every probe above is byte- or shape-level. **No source truth, HTTP authenticity, quote fidelity or support relationship was inferred from structural integrity, and none was verified here** — that axis belongs to the W1 source/artifact adjudication seats; pair presence and hash equality prove nothing about what a source teaches.
- "313" was verified only as the ledger's mixed field sum (per `carry-errata.json`), not as a semantic unit denominator; the 7-unit/3-pair known-unknown set is the erratum's reconciliation over a 6-unit raw field sum, not a recomputed semantic count.
- The 57/58 pair counts depend on my re-implementation of the citation/range rules (literal `S\d{3,}` with word boundaries; six range separators). It agrees with the committed gate and `count_c1.py` on this input, but a rule divergence outside this corpus would change the denominator.
- r26 ledger identity was established against `.ufo/waves/round-26/statements.json` at the declarations commit; no r24 material was read, retried or rephrased.
- No tool was installed; no pacman transaction was made.

Report: `.ufo/waves/round-27/w2/AuditFrozenInputs.md` (relative to `/home/vgpnk/Projects/shokunin/kake-shokunin`).
