# ScribeC1CellFreshness

Assignment: claim C1 (calibration counter `c59_axis_evidence.py`), freshness row of the SCORECARD axis table
(score 10, last change 17). Deliverable: a replacement **evidence cell only**, trialled in a scratch clone with the
counter's own logic. No lane mutation, no fleet mutation, no counter edit.

Base facts used: base revision `fd6303ce5c14b3f892dec586297a942ab6e4193b`, lane HEAD at read time
`cb685273cc9e331b51f45485793d5d1c91184b3a` (base is an ancestor). Axis table found at SCORECARD.md line 15 header
(`| Axis | Score | Evidence pointer | Last change |`), rows operability (score 10), freshness (score 10, last change 17),
calibration (score 2).

## CELL

Replacement text for the freshness evidence cell. No `|` character; only repo-relative committed paths in backticks;
no round-59 path (round 59 has no `## Round 59` freshness row, so citing one would score as an off-axis receipt).

```
**Legacy 10, re-anchored on receipts:** the 10 is the legacy rating from rounds 12 and 17, carried unchanged through round 58, and no round since has re-measured the whole corpus, so the number is not a fresh whole-corpus verdict. What it now rests on is the freshness instrument (`corpus/knowledge/freshness-pins.json`, `corpus/knowledge/freshness-sidecar.json`, `corpus/knowledge/freshness-sweep.md`, `scripts/source_recheck.py`) plus per-entry quote-truth receipt pairs taken on committed bytes, each pair red before the round's entries were admitted and green after, with the green receipt printing the revision it covered: round 56 went 0/8 to 8/8 for the Yahoo! JAPAN crawl-handling entries (`.ufo/waves/round-56/controls/base-c2-quote-truth.txt` red, the entries absent there, `.ufo/waves/round-56/controls/after-c2-quote-truth.txt` green); round 57 went 0/8 to 8/8 for the two Baidu dead-link entries (`.ufo/waves/round-57/controls/base-c3-quote-truth-v2.txt`, `.ufo/waves/round-57/controls/after-c3-quote-truth.txt`); round 58 went 0/8 to 8/8 for the Baidu crawler-identification and unblocking entries (`.ufo/waves/round-58/controls/base-c3-quote-truth-v2.txt`, `.ufo/waves/round-58/controls/after-c3-quote-truth.txt`). Those pairs measure the entries each round added, not the corpus. Not claimed here: semantic support of the quotes (sentence-level reviewers and the non-author closure hold that), drift-free re-fetch of every held source, or any score above the round-17 state.
```

Cell is 1490 characters, 0 `|` characters. Written to
`.ufo/waves/round-59/w1/ScribeC1CellFreshness.files/cell.txt`.

Assembly rule for the row (unchanged cells preserved verbatim): `| freshness | 10 | <cell> | 17 |` — score cell `10`
untouched, last-change cell `17` untouched (the assignment named only the third cell; if the integrator wants the
last-change cell moved to 59, that is their edit, not mine). The old cell (1218 chars) must be appended verbatim under
a `## Superseded axis-table evidence` heading for `superseded_kept` to score; I trialled exactly that.

## POINTERS

Every backticked path, checked with `git -C <lane> cat-file -e fd6303ce…:<path>` (all EXISTS, all blobs) and again at
the measured trial commit (all `resolved: true` in the counter JSON):

- `corpus/knowledge/freshness-pins.json` — EXISTS (blob)
- `corpus/knowledge/freshness-sidecar.json` — EXISTS (blob)
- `corpus/knowledge/freshness-sweep.md` — EXISTS (blob)
- `scripts/source_recheck.py` — EXISTS (blob)
- `.ufo/waves/round-56/controls/base-c2-quote-truth.txt` — EXISTS (blob)
- `.ufo/waves/round-56/controls/after-c2-quote-truth.txt` — EXISTS (blob)
- `.ufo/waves/round-57/controls/base-c3-quote-truth-v2.txt` — EXISTS (blob)
- `.ufo/waves/round-57/controls/after-c3-quote-truth.txt` — EXISTS (blob)
- `.ufo/waves/round-58/controls/base-c3-quote-truth-v2.txt` — EXISTS (blob)
- `.ufo/waves/round-58/controls/after-c3-quote-truth.txt` — EXISTS (blob)

Receipt round gate: rounds 56, 57, 58 each have a table row naming `freshness` in their `## Round N` section
(SCORECARD.md lines 4321, 4350, 4379), so the counter's `on_axis` accepts all six as on-axis receipts
(`receipts_off_axis = 0` globally).

## TALLIES

Six `A/B` occurrences in the cell (three `0/8`, three `8/8`), each an exact substring of a body cited in the same
cell. Per-file grep, `git show HEAD:<file>` line 1 in every case:

- `0/8` — `.ufo/waves/round-56/controls/base-c2-quote-truth.txt:1` — `C2 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)`
- `8/8` — `.ufo/waves/round-56/controls/after-c2-quote-truth.txt:1` — `C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)`
- `0/8` — `.ufo/waves/round-57/controls/base-c3-quote-truth-v2.txt:1` — `C3 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)`
- `8/8` — `.ufo/waves/round-57/controls/after-c3-quote-truth.txt:1` — `C3 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)`
- `0/8` — `.ufo/waves/round-58/controls/base-c3-quote-truth-v2.txt:1` — `C3 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)`
- `8/8` — `.ufo/waves/round-58/controls/after-c3-quote-truth.txt:1` — `C3 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)`

Pair grounding beyond the tally string (read, not inferred): each base receipt's `C1_entries_exist FAIL` block names
the round's ids as *entry absent at the measured revision* (r56: S367, S419, S420; r57: S421, S422; r58: S423, S424);
each green receipt prints `revision:` and that revision contains those entries as blobs — r56 `4cb225fb…` holds
`corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`, `-deleted-url-recrawl.md`,
`-nonexistent-url-recrawl.md`; r57 `32754df7…` holds `baidu-dead-link-types.md`, `baidu-spider3-dead-link-model.md`;
r58 `8d340c15…` holds `baidu-spider-identification.md`, `baidu-spider-unblocking.md`. All checked with
`git cat-file -e <rev>:<path>`, all present.

## COUNTER ROW DETAIL

Trial (not a lane edit): `git clone -q --shared <lane> /fast/scratch/hyaku/kake-r59/ScribeC1CellFreshness/c`,
toplevel assertion passed, freshness third cell replaced, old cell appended verbatim under
`## Superseded axis-table evidence` at EOF, committed with
`git -c user.name=selftest -c user.email=selftest@local commit` → trial commit
`c3389dd61ccca37d1cff9107e7ca469f45bc74fb`. Run:
`python3 -B <lane>/.ufo/waves/round-59/c59_axis_evidence.py --root <scratch>/c --revision HEAD --json`.

Global (exit 1, predicate not met, as expected — the other two rows are untouched):
`mismatches=8 unresolved=4 rows_no_receipt=2 receipts_off_axis=0 tallies_unfound=0 rows_no_tally=2 rows=3
scores_held=2 superseded_kept=1 met=False`.

This row (freshness), row-local using the counter's own helpers on the same revision/commit:

- pointers=10, unresolved=0
- receipts=6 (rounds 56, 57, 58 × base/after), all on-axis
- tallies=6, all `found: true`, unfound=0

Where the global 8 comes from: operability 4 unresolved (`cli.mjs:935`, then `:836-839`, `:932`, `:393` orphaned line
pointers) + rows_no_receipt + rows_no_tally = 6; calibration rows_no_receipt + rows_no_tally = 2. Freshness
contributes 0 mismatches. `scores_held=2` (operability 10, freshness 10 both unchanged from base).
`superseded_kept=1` because only the freshness old cell was appended; the operability and calibration old cells are
still inside the table, which is the other seats' work, not mine.

Receipts: `.files/counter.json`, `.files/counter.out`, `.files/rowstats.txt`, `.files/tallies.txt`,
`.files/pointer-check.txt`, `.files/scorecard-trial.diff` (the exact SCORECARD change trialled).

## HONESTY NOTES

- The cell does **not** claim the corpus is fresh. It says the 10 is legacy (rounds 12 and 17) and names the receipt
  pairs the score is now re-anchored on. It does not inflate: it explicitly disclaims "any score above the
  round-17 state".
- The cell does **not** claim semantic support of the quotes. The receipts themselves say quote-truth, not support;
  sentence-level reviewers and the non-author closure own support.
- The 0/8 → 8/8 movement is per-entry, not per-corpus: it certifies the entries a round admitted, on committed bytes,
  at the revision the green receipt prints. Earlier held entries are not re-certified by these receipts.
- Counter weakness I did not exploit and did not hide: the counter matches each `A/B` against the union of **all**
  cited blob bodies, so a tally from one cited receipt can satisfy a number attributed to another; and it cannot tell
  which receipt a number came from. My per-pair attribution was verified by hand, one grep per file, and is recorded
  in TALLIES above rather than being left to the counter's union check.
- The counter does not check that the receipt's printed `revision:` is the revision the cell means; I checked the
  three green revisions by blob existence and report that as my own check, not the counter's.
- `scores_held` is satisfied only because I kept the score cell `10`; the row's last-change cell stays `17`.
- The counter's `selftest` is a stub returning exit 2 in this version; I did not run it and did not modify it.
- No claim about rounds before 56 is made by the new cell; nothing before round 56 is cited.
- Unrun by me: the counter's wave-1 attack matrix, any after-state scoring, `span_tools.py` quote checks (C3's
  surface, not mine). No pacman transaction was run; no tool was installed for this seat.

VERDICT: freshness cell drafted and counter-trialled — that row scores 10 pointers resolved, 6 on-axis receipts, 6 tallies found, 0 unresolved; global exit 1 only from the untouched operability and calibration rows (superseded_kept 1 of 3).
