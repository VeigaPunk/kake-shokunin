# Round 55 — seat settlement (L1, from `w1-results.json`, `w2-results.json` and committed reports)

Wave 1 (build, v1 policy): 40 seats dispatched, 40 settled in `w1-results.json`; 39 committed reports in `w1/`
(`ls .ufo/waves/round-55/w1/*.md | wc -l`). Roles: scribe 27, scout 4, executor 3, connector 2, critic 2,
mutation-tester 1, reviewer 1. Dead/lost: `ScribeQuality` settled but wrote no report in this lane — its
output names `.ufo/waves/round-45/w2/ScribeQuality.md` and describes another lane's round-45 criteria (no such file
exists in the lane; a same-named file elsewhere in the fleet belongs to kumitate); its draft was discarded.

Wave 2 (falsify, v1 policy): 36 seats dispatched; reports committed under `w2/` as they landed. Roles: executor 14,
reviewer 5, scout 4, mutation-tester 3, critic 3, scribe 3, sentinel 1, connector 1, simplifier 1, revenger 1.
W2 was written to the orchestrator while `ScribeQuality` (W1) was the only unsettled W1 seat.
Per-seat status of W2 is recorded in the report (§Work performed) from `w2-results.json`.

Round total: 76 seats (40 + 36), no residual call. Never replaced a dead seat. Seat reports in `w1/` and `w2/`
were committed at settlement, before later work cited them.

## Wave 2 settlement (from `w2-results.json`, 36 settled)

34 committed seat reports in `w2/` (`ls .ufo/waves/round-55/w2/*.md | wc -l`). `ScribeScorecard` and `ScribeLog` settled
with outputs about other lanes/rounds (mori round 47; a round-49 LOG entry) and no report file in the lane — misdirected seats, like W1 `ScribeQuality` (their drafts were not used; the SCORECARD and LOG entries were written by the L1 from
the receipts). No seat was replaced. `MutC2Counter` reported 52 mutants, 44 killed, 8 redundant survivors; its 29 proposed
kill fixtures were not ported into the selftest (disclosed in the report).
