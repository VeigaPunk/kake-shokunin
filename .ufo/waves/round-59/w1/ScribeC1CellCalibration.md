# ScribeC1CellCalibration

Claim C1, calibration row (score 2, last change 58). Drafted a replacement for the third
(evidence) cell only; the score cell (2) and last-change cell (58) are unchanged. The cell was
tested in a throwaway shared clone of the lane at base `fd6303ce5c14b3f892dec586297a942ab6e4193b`
(HEAD when cloned: `cb685273cc9e331b51f45485793d5d1c91184b3a`), never in the lane itself.

## CELL:

```
Score 2 rests on the round-58 receipt-ledger move only: the counter `.ufo/waves/round-58/c58_receipt_rewrites.py` re-derives every post-commit measurement-receipt event and checks each note pointer, blob and kind. Its after receipt `.ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt` records events=19, undisclosed=0 and new_receipts=2 at revision de7d96e720522ea15fba3fd9ee3ce58c42596031, while its base receipt `.ufo/waves/round-58/controls/base-c1-receipt-rewrites-v2.txt` records undisclosed=19 with new_receipts=0. That counter's selftest receipt `.ufo/waves/round-58/controls/c1-selftest-v2.txt` prints 45/45. The move extends the round-57 receipt-pin gate, whose final selftest `.ufo/waves/round-57/controls/c1-selftest-final.txt` prints 71/71, and the round-56 selftest-tally gate, whose selftest `.ufo/waves/round-56/controls/c1-selftest.txt` prints 59/59. Legacy: the 10 score cells of the other rows are a legacy round-17 and round-18 assessment, not a fresh calibration proof, and this cell does not re-prove them. The claim is only machine-checked disclosure completeness for the measured event population; it does not claim that every past run occurred, does not claim quote or prose truth, and does not raise the score.
```

- No `|` character (asserted in the replacement script); ASCII only; one line, 1243 characters.
- Also written verbatim to `.ufo/waves/round-59/w1/ScribeC1CellCalibration.files/cell.txt`.

## POINTERS:

All six backticked paths are repo-relative committed blobs. Existence checked with
`git -C <lane> cat-file -e fd6303ce5c14b3f892dec586297a942ab6e4193b:<path>` (all OK), and each
resolved at the measured scratch revision by the C1 counter (`"resolved": true, "why": "ok"`).

| Path | base `cat-file -e` | round section names calibration |
|---|---|---|
| `.ufo/waves/round-58/c58_receipt_rewrites.py` | exists | yes (Round 58 row: calibration) |
| `.ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt` | exists | yes |
| `.ufo/waves/round-58/controls/base-c1-receipt-rewrites-v2.txt` | exists | yes |
| `.ufo/waves/round-58/controls/c1-selftest-v2.txt` | exists | yes |
| `.ufo/waves/round-57/controls/c1-selftest-final.txt` | exists | yes (Round 57 row: `calibration (declared; operability argued)`) |
| `.ufo/waves/round-56/controls/c1-selftest.txt` | exists | yes (Round 56 row: `calibration (declared; operability argued)`) |

No absolute, `~`, `/tmp` or bare /home token appears in the cell. Five cited blobs are receipts
under `.ufo/waves/round-58|57|56/`; those three `## Round N` sections each carry a table row naming
calibration (SCORECARD.md table rows at lines 4394, 4361, 4334). The counter agrees: `receipts_off_axis` 0
and its calibration row is not counted in `rows_no_receipt`.

## TALLIES:

Each `A/B` in the cell, and the exact grep hit in a cited committed blob (base revision):

| Tally | File | grep line |
|---|---|---|
| `45/45` | `.ufo/waves/round-58/controls/c1-selftest-v2.txt` | 47: `c58 receipt-rewrites selftest: 45/45` |
| `71/71` | `.ufo/waves/round-57/controls/c1-selftest-final.txt` | 1: `c57 receipt-pins selftest: 71/71` |
| `59/59` | `.ufo/waves/round-56/controls/c1-selftest.txt` | 1: `c56 selftally selftest: 59/59` |

Non-tally numbers are also verified in the cited receipts, not just asserted: after receipt line 1
`events=19 undisclosed=0 ... new_receipts=2`, line 3 `revision: de7d96e7...`, line 4 `EXIT=0`; base
receipt line 1 `events=19 undisclosed=19 ... new_receipts=0 met=False`, line 22
`revision: 044048597d62f3199494b63b36e90dd57825e350`. No other `A/B` appears in the cell, so the
counter's `tallies_unfound` is 0 and the calibration row is not in `rows_no_tally`.

## COUNTER ROW DETAIL:

Command (scratch clone `<scratch>/c`, replacement cell committed as `af6fc1898b05c19473d5c2e4ac9fe6da395f7cdc`,
old cell appended verbatim under `## Superseded axis-table evidence` at EOF, selftest identity
`user.name=selftest user.email=selftest@local`):

`python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root <scratch>/c --revision HEAD --json`

Calibration row at HEAD: 6 pointers, 6 resolved, 0 unresolved; receipts 5, all on-axis;
tallies `45/45` found, `71/71` found, `59/59` found; contributes no `rows_no_receipt`,
no `rows_no_tally`, no `receipts_off_axis`, no `tallies_unfound`.

Whole-table totals at HEAD: `unresolved=11`, `rows_no_receipt=2`, `receipts_off_axis=0`,
`tallies_unfound=0`, `rows_no_tally=1`, `mismatches=14`, `scores_held=2`, `superseded_kept=1`,
`rows=3`, `names_ok=true`, `met=false`, exit 1. The 11+2+1 residual mismatches are the
operability and freshness rows (unchanged by this seat): operability 4 unresolved + no receipt +
no tally; freshness 7 unresolved (`/tmp/kake-r17/...` and `corpus/claims`) + no receipt.

At base `fd6303ce...` the same counter reports `mismatches=16` (`unresolved=11`,
`rows_no_receipt=3`, `rows_no_tally=2`, `superseded_kept=0`), and the calibration row there is
`{"pointers": [], "tallies": []}` — 2 mismatches (no receipt, no tally). This cell removes those
2. `superseded_kept` is 1, not 3, because only this row's old cell was appended; the frozen
predicate's `superseded_kept == 3` needs the other two rows' cells preserved too, which is outside
this seat's scope. Calibration row alone is clean; the table predicate is not met.

## HONESTY NOTES:

- The cell claims machine-checked disclosure completeness for the measured event population only.
  The round-58 verdict itself records the residual limit: pointer-only prose notes and semantically
  fabricated values can pass; human review remains required. This cell does not upgrade that.
- The cited `45/45`, `71/71`, `59/59` are printed by committed receipt blobs; I did not re-run those
  selftests or `c58_receipt_rewrites.py`. Their truth is as recorded at base, and the counter's own
  "Not tested" clause applies: it checks that the cell's tallies occur in cited blobs, not that the
  receipt's run happened or that the tally is the receipt's own result.
- The cell does not claim every past run occurred, does not claim quote/prose truth, and does not
  claim the other rows' 10 ratings are verified; those are legacy round-17/18 assessments and are
  explicitly left un-re-proved.
- No score change is proposed: calibration stays 2. No claim is made about whether "receipt-ledger
  disclosure" is calibration rather than operability as AXES.md defines it; that ownership ruling
  remains open as recorded in rounds 54-58.
- Only the C1 counter was executed (read-only, on a scratch clone). `--selftest` was not run; the
  frozen version 1 stub prints "wave 1 writes the fixture kill matrix" and exits 2.
- No lane writes except this report and `cell.txt`; no git/jj mutation in the lane; scratch removed.

VERDICT: calibration evidence cell redrafted and counter-tested clean (0 mismatches for this row, 2 removed from base 16, table still red at 14), score 2 held and not inflated.
