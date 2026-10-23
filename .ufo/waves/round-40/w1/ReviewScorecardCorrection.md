# W1 — ReviewScorecardCorrection: round-39 closure correction vs row, lesson, MANIFEST

Seat: KakeR40.ReviewScorecardCorrection (leaf, read-only review; no lane mutation, no installs, no counter runs — scoring tools is not this item).

## Sources checked
- `SCORECARD.md:2539-2546` — "## Round 39 — closure correction (appended in round 40)" + body.
- `SCORECARD.md:199` — row "Offline sitemap file audit (round 39, exploratory)", status col "39 — exploratory, pending closure"; row evidence col cites "non-author reviewer `KakeR39A3.ExploratoryVerdictC1`".
- `corpus/lessons/round-39-verifier-spotcheck.md` — :88 heading "Non-author verdict on C1 (this integrator): unprovable-but-better"; :90 "The lane's own `KakeR39A3.ExploratoryVerdictC1` … does not count … this is the verdict of record"; :121-122 harm "207 insertions, 0 deletions; no axis score line changed"; :130 per-axis verdicts (operability unprovable-but-better, rest unchanged); :175-176 routed defect 3 (append the SCORECARD correction).
- `MANIFEST.json` `rounds[523]` — round 39, type closure, admitted true; verdicts.operability "unprovable-but-better", other five "unchanged"; verification.reviewer "hyaku-closure (@m_opus session, non-author)"; verification.spotcheck `…@f171c58b918f705ca875b6cb42b9e75489cd3589`; commit f841a48d.

## Verification run (all read-only git at the lane; exit codes shown)
- `git merge-base --is-ancestor f171c58b… f043c721…` → 0 (ANCESTOR_OK); `git rev-parse HEAD` → f043c721 (tip; working copy clean for both files, porcelain empty).
- `git diff --stat f171c58b… HEAD -- corpus/lessons/round-39-verifier-spotcheck.md | wc -l` → 0 (lesson unchanged since the pinned spot-check commit; `git cat-file -t f171c58b…` → commit).
- `git show f841a48d:SCORECARD.md | grep -c 'closure correction'` → 4 (r37/r38 corrections + 2 row refs; no r39 correction); absent at r40 base f171c58b too; `git log -S'closure correction (appended in round 40' -- SCORECARD.md` → single commit f043c72 "round-40: C1 declared … round-39 closure correction".
- Lane-wide grep "pending closure": only SCORECARD 199 (the row) and 2542 (the correction's own quote), plus lesson quotes :122/:176 and w1 spec files. No other row or file carries the status.

## Per attacked statement
1. "The round-39 capability row above … still reads 'pending closure'" (2541-2542) — **holds**. SCORECARD.md:199 status col is exactly "39 — exploratory, pending closure"; it is the lane's only such row, and the row is "above" (199 < 2539).
2. "The non-author closure admitted it: C1 `unprovable-but-better`" (2542-2543) — **holds**. Lesson :88 verdict of record unprovable-but-better; MANIFEST rounds[523] admitted=true, verdicts.operability "unprovable-but-better", capabilities_added "unprovable-but-better by hyaku closure".
3. "reviewer of record the hyaku closure integrator" + "the lane's own `ExploratoryVerdictC1` is not the verdict of record" (2542-2545) — **holds**. Lesson :90 says exactly this; MANIFEST reviewer "hyaku-closure (… non-author)".
4. Pointers: lesson file, section "Non-author verdict on C1", MANIFEST `rounds[523]`, spot-check `f171c58b` (2543-2544) — **holds**. Heading exists (lesson :88); rounds[523] is the kake r39 closure; the pin resolves to a real commit, ancestor of tip f043c721, and the lesson bytes are unchanged since it (diff empty, porcelain clean).
5. "Read that row as admitted, exploratory, `unprovable-but-better`" (2544-2545) — **holds**; each adjective matches MANIFEST/row status (admitted true; "39 — exploratory" at :199; verdict as above) and satisfies routed defect 3 (lesson :175-176), which asked for exactly this marking with the lesson as reviewer pointer.
6. "Axis scores unchanged" (2545-2546) — **holds, one nuance**: the closure's per-axis VERDICT for operability is "unprovable-but-better" (lesson :130, MANIFEST verdicts), not "unchanged"; what is unchanged is the axis score line (lesson :121-122: 207 insertions, 0 deletions in SCORECARD). The same paragraph already states the verdict, so no misreading results. Not overstated.
7. Heading claim "appended in round 40" (2539) — **holds**. Absent at r39 tip f841a48d and r40 base f171c58b; present only from tip commit f043c72.

## Attack result: does the correction state the verdict exactly, with no unexplained 'pending closure' row?
**Holds.** The correction's verdict, reviewer-of-record, exploratory status, admission, and pointers match the closure lesson and MANIFEST rounds[523] exactly; the lane's ExploratoryVerdictC1 is correctly demoted; and the row at :199 is the only "pending closure" row in the lane, explicitly explained by 2541-2545.

## Findings by severity
- Material: none.
- Minor (residual, by design): SCORECARD.md:199 evidence col still cites `KakeR39A3.ExploratoryVerdictC1` as "non-author reviewer" — textually superseded (lesson :90 says that seat does not count). The correction neutralizes it (2545) and SCORECARD is append-only (0 deletions policy), but a reader of the row alone still sees the wrong reviewer citation. Consider the correction sufficient; no action required for this round.
- Minor (nuance, see statement 6): "Axis scores unchanged" is true of score lines, not of the operability verdict string; harmless in context.

## Residual risk and verification gaps
- Evidence-verified against committed bytes only (the closure itself executed no gate/selftest/counter; I re-ran none) — consistent with the closure's own stated method; no independent re-execution was in scope for this seat.
- I did not re-derive MANIFEST rounds[523] from the closure run; I read the pinned entry as-is (jq filter `.rounds[523]`).
- If a later round edits row :199 in place, this review's line anchors shift; the status string "pending closure" remains the stable search key.
