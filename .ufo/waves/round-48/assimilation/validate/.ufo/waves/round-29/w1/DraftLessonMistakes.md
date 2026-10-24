# Round 29 wave 1 — draft Mistakes rows for `corpus/lessons/round-29.md`

Seat `KakeR29.DraftLessonMistakes` (scribe, leaf). Axes: operability, freshness.
Milestone: r29-build. Draft only; nothing landed in the lane except this report.

## What I attacked

Two round-28 mistakes were mined into two `## Mistakes` rows, each with a fix
shown able to fail by a command that exits non-zero for the named reason.

Draft (the deliverable): `/fast/scratch/hyaku/kake-r29/w1/DraftLessonMistakes/mistakes-draft.md`.
The lesson at `f8675e5` has no `## Mistakes` section yet (`git show f8675e5:corpus/lessons/round-29.md`
has only `## Claims` and `## Gate`), so the L1 adds the heading and the table, then the two rows.

## The two rows (abridged; full text in the draft file)

| Class | Evidence | Captured-by | Fix (abridged) |
|---|---|---|---|
| vacuous | Round-28 C2 counter graded quote shape, not quote truth: `.ufo/waves/round-28/c2_source_count.py:126-127` counted one curly-quoted span of 1–25 words and never opened a source. Recorded at `corpus/lessons/round-28.md:107-110` and `corpus/lessons/round-28-verifier-spotcheck.md:225-227` (routed defect 3). | none — `corpus/QUALITY.md:298-332` (round-28 section) requires a counter to reject a constant, but no criterion required a quote to be found in retained text. | Round-29 counter `.ufo/waves/round-29/c1_quote_truth.py` check `d_quote_in_retained_text`: the Gate quote must be an exact substring of `.ufo/waves/round-29/sources/S0NN.txt`, whose sha256 must equal the committed receipt. |
| vacuous | Round-28 source gate screened only what it admitted: `corpus/SOURCES.md` round-28 search log ("Identified 4, screened 4, included 4 (S036–S039, scoped tier A), excluded 0") and `corpus/lessons/round-28-verifier-spotcheck.md:228-231` (routed defect 4). | none — no criterion required a screened source step to yield a checkable rejection, and round-28's `## Gate` had no rejected line to point at. | Round-29 `## Gate` block "Screened candidates (round-28 routed defect 4)" with three rejected rows (S044–S046, `REJECTED: … ; flip: …`) and two queued (S047, S048); check `reject_path_check.py` fails on a bad quote, a missing flip clause, a wrong status, a non-tier-A cited primary, an admitted rejected URL, or zero rejections. |

## Commands and exit codes (all in my sandbox)

Sandbox: `/fast/scratch/hyaku/kake-r29/w1/DraftLessonMistakes/` (clone of the lane,
branches `state/*` and `landed/*`; the lane itself was never mutated).

Mistake (a), quote truth:

| Command | Exit | Observed |
|---|---|---|
| `clone$ python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision f8675e5` | 0 | `C1 4/4`, `controlBroken false`, all four checks true on all four ids |
| `clone$ python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision 609e6777fe3836ec813f499186248ff1992c6e99` | 1 | `C1 3/4`; S042 `d_quote_in_retained_text` false, other checks true. Commit changes exactly one letter of the S042 Gate quote ("Prepend" → "Prepond") |
| `clone$ python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision ae3e205140f1c1913531f14bff85743496166e7a` | 1 | `C1 3/4`; S040 `d_quote_in_retained_text` false. Commit swaps the S040 Gate quote for the S044 rejected candidate's quote, which is exact in `sources/screened/C1.txt` but absent from `S040.txt` |
| `clone$ python3 -B .ufo/waves/round-28/c2_source_count.py --root . --revision 1f9ffdcffcad9fa78a41aad60c00b6576d0dcfbc` | 0 | `passed 4 / 4` although one letter of the round-28 S036 Gate quote was changed. The flipped quote is not an exact substring of `.ufo/waves/round-28/sources/S036.txt` (verified: honest quote `True`, flipped quote `False`, both 18 words) |

The last row is the blindness itself: the round-28 counter scores the same on a
quote that is absent from the source as on the honest one.

Mistake (b), reject path (`reject_path_check.py`, my sandbox witness):

| Command | Exit | Observed |
|---|---|---|
| `python3 -B reject_path_check.py --registry reg.md --lesson lesson.md --entry entry.md --screened-dir cand --primary-dir screened` | 0 | 5 screened candidates, 5 passed; S044–S046 rejected rows all clean, S047–S048 queued rows consistent |
| same with `--lesson mut/M1-quote-one-letter.md` | 1 | S044 "quote not an exact substring of the candidate text" |
| same with `--registry mut/M2-no-flip.md` | 1 | S044 "teaches names no flip condition" |
| same with `--registry mut/M3-registry-mutated.md` | 1 | S044 "registry status is 'mined', not 'rejected'" |
| same with `--lesson mut/M4-zero-rejected.md` | 1 | S044, S045, S046 "registry rejects a candidate the lesson does not mark rejected" |
| same with `--entry mut/M5-entry-admits.md` | 1 | S044 "rejected candidate URL appears in the entry or an admitting Gate line" |

Supporting reads: `grep -n "" corpus/lessons/round-28-verifier-spotcheck.md` at `fe1805c`
gives line 225 ("The C2 counter checks quote shape, not quote truth") and line 228
("The frontier step screened only the four sources it then admitted"). `grep -n "" corpus/SOURCES.md`
gives line 100 for the round-28 search log entry. `git show 36b6b21:.ufo/waves/round-28/c2_source_count.py`
gives the quote check at lines 126-127.

The four Gate quotes I used in the sandbox honest state were each verified as
exact substrings of the collapsed retained text with a separate script
(`check_quotes.py`: S040 10 words, S041 22, S042 16, S043 19, all `exact True`).

## Evidence pointers

- Draft rows: `/fast/scratch/hyaku/kake-r29/w1/DraftLessonMistakes/mistakes-draft.md`
- Harness: `build_state.py`, `build_landed_states.py`, `build_r28_state.py`,
  `reject_path_check.py`, `check_quotes.py` in the same directory
- Sandbox commits: honest `6aa709872d7b6272154aa3a4cf31b6fedca4bebd`, flip `3504fd6c689285a735ca72d70219058bf912da07`,
  leak `f33eae60cd267139f9bd20d9da9489816e6745da`, landed flip `609e6777fe3836ec813f499186248ff1992c6e99`,
  landed leak `ae3e205140f1c1913531f14bff85743496166e7a`, r28 flip `1f9ffdcffcad9fa78a41aad60c00b6576d0dcfbc`
- Check outputs: `out-landed.json`, `out-honest.json` in the sandbox directory

## Limits and open findings

- `reject_path_check.py` is a sandbox witness, not a committed lane counter. It
  makes the mistake row point at a command that fails for the named reason; it
  is not proposed as a new claim.
- The C1 counter proves a quote is present in retained text. It does not prove
  the quote supports the claim it is attached to; `.ufo/waves/round-29/w1/CriticC1CounterGameable.md`
  shows eleven fake states scoring 4/4 on that counter. My rows do not claim more.
- My sandbox states are synthetic. The landed bytes at `f8675e5` were read but
  not modified; the lane working tree and Git index were never touched, and no
  `git add`, `commit`, `stash`, `checkout`, `reset`, `pull` or `push` ran in the lane.
- The round-29 lesson's `## Mistakes` section does not exist yet; if the L1 has
  added one by integration time, the two rows should be appended to that table
  rather than a second table.
- No tool was installed or updated. No pacman transaction ran.

## Out of scope

The C2 base-path audit, the citing-set surface, the C1 counter's provenance
pinning (a sibling critic's proposal), and the QUALITY.md criteria draft.
