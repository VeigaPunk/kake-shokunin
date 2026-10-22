# MistakesRowsCheck — round 29 wave 2 (falsify)

Target: the two `## Mistakes` rows in `corpus/lessons/round-29.md` (lines 72-86) at lane commit
`7697990cbca20291f3b0367b8ff4220e93b38b03`. Sandbox: `/fast/scratch/hyaku/kake-r29/w2/MistakesRowsCheck/`
(clone checked out at 7697990, TMPDIR inside the sandbox). No installs. No network. Lane untouched except this file.

## Row 1 — round-28 C2 counter graded quote shape, not truth (class vacuous)

Evidence pointers, all checked at 7697990, all say what the row says:
- `.ufo/waves/round-28/c2_source_count.py:126-127` is `QUOTE_RE.findall(line)` plus `len(quotes) == 1 and 1 <= words <= 25`; `QUOTE_RE` (line 41) is the curly-quote span. The counter only `show()`s registry, entry and lesson (lines 89-91); it never reads a source text.
- `corpus/lessons/round-28.md:107-110` and `corpus/lessons/round-28-verifier-spotcheck.md:225-227` record the defect; `residual/ReviewGateQuotes.md` exists at `.ufo/waves/round-28/residual/` (the bare path is relative, as in round 28).
- `corpus/QUALITY.md:298-332` is exactly the section "Counters and field evidence — round 28".

Fix shown able to fail — reproduced. I fetched the two cited sandbox commits from the wave-1 seat clone into my clone (they are not in the lane repo, so a reader can't reach them from the lane alone):
- `c1_quote_truth.py --root . --revision X`: f8675e5 exit 0, 4/4; 98dbab2 exit 0, 4/4; 7697990 exit 0, 4/4; fe1805c exit 1, 0/4; `609e6777` (parent f8675e5, one letter in S042: Prepend→Prepond) exit 1, 3/4, with only S042 failing and only on `d_quote_in_retained_text`.
- An independent mutation of my own (S043 quote "base"→"bese", committed on 7697990 in my sandbox as 3783d25): exit 1, 3/4.
- `.ufo/waves/round-28/c2_source_count.py --root . --revision X`: fe1805c exit 0, 4/4; `1f9ffdc` (parent 36b6b21) exit 0, 4/4. That commit deletes the final "s" of "devices", so the quote is no longer in the retained S036.txt: the original is a substring of the collapsed text and the mutated quote is not. Strictly, this deletes one letter rather than changing one.

Captured-by "none": the claim is overstated. The row says "no criterion required a quote to be found in retained text". But the pre-round QUALITY.md at fe1805c already has two such criteria, each scoped to another surface:
- Round 25 (line 172): "A card quote must be in normativeText".
- Round 26 (line 212): "A recheck HOLD needs a row-specific located quote".

What was missing was a rule for Gate-quote counters. The row's own evidence also shows the defect was caught after the fact, by `residual/CriticC2Counter.md` and the verifier spot-check (routed defect 3).

Verdict row 1: **holds** on class, evidence and fix-can-fail. One limit to state: the captured-by sentence should read roughly "none for Gate counters; the round-25 and round-26 quote-location criteria covered cards and recheck rows only; caught after the fact by residual/CriticC2Counter.md and spot-check defect 3". A second, smaller limit: cite the sandbox commits as wave-1 sandbox objects (path given above), not as lane commits.

## Row 2 — round-28 source gate screened only what it admitted (class vacuous)

Evidence pointers: `corpus/SOURCES.md:100` has the quoted "Identified 4, screened 4, included 4 (S036–S039, scoped tier A), excluded 0". `round-28-verifier-spotcheck.md:228-231` is routed defect 4. Both hold. Captured-by "none" also holds: the pre-round QUALITY.md has no criterion about screening or producing a rejection.

Witness inputs: `reg.md` is byte-identical to `corpus/SOURCES.md` at both f8675e5 and 7697990. `lesson.md` and `entry.md` are the f8675e5 versions. `cand/C1-6.txt` and `screened/S040-S043.txt` are byte-identical to `.ufo/waves/round-29/sources/screened/` and `.ufo/waves/round-29/sources/`. Note that the directory names are swapped: `cand/` holds the candidates and `screened/` holds the primaries.

Base command, run from `.ufo/waves/round-29/verification/reject-path`:
`python3 -B reject_path_check.py --registry reg.md --lesson lesson.md --entry entry.md --screened-dir cand --primary-dir screened`

| Input | Exit | Observed |
|---|---|---|
| honest witness inputs | 0 | 5/5 passed |
| honest committed corpus at 7697990 (SOURCES.md, lesson, entry, sources dirs) | 0 | 5/5 passed |
| `--lesson mut/M1-quote-one-letter.md` | 1 | S044 quote not an exact substring |
| `--registry mut/M2-no-flip.md` | 1 | S044 teaches names no flip condition |
| `--registry mut/M3-registry-mutated.md` | 1 | S044 status 'mined', not 'rejected' |
| `--lesson mut/M4-zero-rejected.md` | 1 | S044-S046 "registry rejects a candidate the lesson does not mark rejected" |
| `--entry mut/M5-entry-admits.md` | 1 | S044 URL appears in the entry |
| my X1: lesson and registry both relabel S044-S046 as queued (drop `REJECTED:`, status `queued`) | **0** | 5/5 passed, rejectedRowsInRegistry 2 |
| my X2: S044 bullet deleted from lesson, registry row still rejected | **0** | 4/4 passed; S044 is never checked |
| my X3: S042 tier set to B | 1 | cited primary S042 is tier B |
| my X4: S044 `flip:` clause emptied (`flip: |`) | **0** | 5/5 passed |
| my X5: S044 URL put into the S041 admitting Gate line | 1 | URL in an admitting Gate line |
| my X6: `--primary-dir` points to a missing directory | 1 | cited primaries have no retained text |

Counterexample (X1). The Fix cell says the witness fails "when no candidate is rejected at all". It does not:
- The script computes `rejected_rows` (`reject_path_check.py:120`) but never gates on it.
- The return condition (line 127) is only `results and passed == len(results)`.
- So a round that screens five candidates and rejects none, recorded consistently, exits 0. That repeats the very "excluded 0" defect this row repairs.
- Named mutation M4 fails only because the lesson and the registry disagree, not because there are zero rejections.

X2 shows that a registry rejection with no lesson bullet escapes every check. X4 shows the flip check is a substring test. Neither the witness nor a criterion is wired into a standing gate: `reject_path` appears only in this lesson and in `w1/DraftLessonMistakes.md`, and the round-29 `QUALITY.md` section adds a quote-truth criterion (its line 42 in that section) but no screened-rejection criterion. That leaves row 2 with no recurrence guard.

Smaller operability notes:
- `mut/` keeps four stale `.json` mutations that the script can't take as input.
- `w1/DraftLessonMistakes.md:64` names a `check_quotes.py` that exists only in the wave-1 sandbox, not in the lane.

Verdict row 2: **broken in part.** The class, evidence and captured-by hold. The five named mutations fail as stated. The "fails when no candidate is rejected at all" clause is false (X1).

Smallest safe correction, either of:
- In the script, return 1 when no result has `rejected` true. A tighter version also cross-checks that every registry row with status `rejected` opened this round has a lesson bullet (this closes X2).
- In the lesson, strike the "no candidate is rejected" clause and describe M4 as a lesson-registry mismatch.

Impacted axes: operability (the witness's claimed reject power) and freshness (no standing guard against a repeat of excluded 0).

## Not verified
- I did not re-open any URL or check the S044-S046 rejection reasons against the live pages.
- I did not check row text against wave-1 reports beyond `DraftLessonMistakes.md`.
- I did not run C2 or the selftest; they are outside these rows.
