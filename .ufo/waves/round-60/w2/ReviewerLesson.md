# ReviewerLesson

ATTACKS: Reviewed `corpus/lessons/round-60.md` at B1 (`8b33fd248d126b48d838af5c38bc175850f41a09`) against the round contract and `CORPUS.md`; checked the referenced wave-1 search-log commands and frozen controls at B1.

GATE:
- S427–S429 each include a canonical URL, accessed date `2026-10-27`, page digest/byte count and quoted source text. The quotes shown are within the stated 6–25-unit and 160-character limits; their named anchors align with the lesson's declared A1 heading rule. This review did not independently re-parse retained HTML or re-run the quote-truth counter.
- The reported access date matches the contract's UTC date for the retained fetches. No gate-specific actionable defect found.

MISTAKES:
- Four mistake rows use classes present in `CORPUS.md`'s vocabulary: `stale-premise`, `scope`, `reference-drift`, `survivor`. Their evidence pointers name round-55/59 files, B1 controls and corpus paths; the round-60 red-before claims are supported by committed controls (`base-c1-gate-status.txt`, `base-c2-guard-cases.txt`, `base-c3-quote-truth.txt`, `redbefore-c1-score-mutant.txt`, and the three selftest receipts). The C1 score-mutant receipt explicitly shows `scores_held=2/3 met=False`, exit 1, versus round-59 counter exit 0. No broken pointer or unsupported red-before claim identified in this check.

COUNTS:
- Search-log counts cite `w1/ScribeSearchLog.md`, whose `COMMANDS` table pairs the reported staged/lane counts with commands and observed outputs; it also describes the arithmetic behind the 4/4/3/1 candidate counts. Thus the lesson's pointer resolves to reproducibility detail rather than leaving its counts ungrounded. No contradictory count identified.
- Assimilation's `reg-ids`, `staged-ids`, collision IDs and S415→S429 mapping are internally consistent with the lesson's stated census and mirror details; the assimilation files themselves were not independently regenerated in this review.

FINDINGS:
| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| none | — | No actionable finding in the scoped sections. | `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 8b33fd248d126b48d838af5c38bc175850f41a09:corpus/lessons/round-60.md`; `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 8b33fd248d126b48d838af5c38bc175850f41a09:.ufo/waves/round-60/w1/ScribeSearchLog.md`; `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 8b33fd248d126b48d838af5c38bc175850f41a09:.ufo/waves/round-60/controls/redbefore-c1-score-mutant.txt` | — |

Residual risk / verification gaps: Did not rerun counters, independently rederive assimilation ID lists, or re-parse retained source HTML. These are not presented as verified by this seat.

VERDICT: No actionable defect found in Gate, Mistakes, Search-log counts, or assimilation ID claims within the assigned review scope.