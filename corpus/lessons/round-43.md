# Round 43 — freeze-order repair, citation annotation, registry arithmetic correction

author: kake L1, round 43 (`KakeR43`, hyaku run 5, attempt 1)

Claim and rules: `SCORECARD.md` "Round 43 — C1 and C2 declared (frozen before any seat scores)".
Base `61046fcffa23898cd93b7a5a0af4906dac9926c9` (round-42 closure spot-check commit on top of the
round-42 verdict `5949e66ffe…`). This round answers the round-42 closure's routed repairs 1, 2, 3,
4, 6 and mines the arithmetic defect as Mistake 7.

## Gate

Sources opened this round by the L1 (sibling-lane adjacency imports, orchestrator-authorized):

| Row | Source (opened 2026-10-23) | Located quote (≤25 words) | Decision |
|---|---|---|---|
| S129 | tameshi `tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md` (seat tameshi-r33-w1-CtlDoNothing; companion `ReviewFreeze.md`) | "The do-nothing shortcut never reaches predicate_pass=true" (§Verdict, paragraph 2; with "kill=0/18 accept=8/8 predicate_pass=False") | admit — pre-data control classes scored against a frozen counter before any build is judged; the method kake applies freezing counter v4 |
| S130 | kama `kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` (round 29) | "records a calibration error present when the statement was written" (§Checking self-assessment statements at writing, paragraph 2) | admit — self-assessment statements must re-derive from the committed tree at their writing revision; grounds the registry-arithmetic correction |

Row changes this round (CORPUS.md §SOURCES.md rule 2): S129, S130 added (2 admitted, 0 rejected;
registry 128 → 130 rows at this lesson's commit). No other `status`/`recheck`/`used-by` change.
No old→new cell log needed beyond this line. Both rows name sibling repo paths (kind `own-work`,
tier A scoped to the fleet-internal method each documents); rejections: none — sibling
verification-fixture and calibration method rows were the two admitted candidates this round.

## Mistakes

7. **Class: stated counts fail re-derivation from committed bytes (round 42, found by the closure).**
   Evidence: `corpus/lessons/round-42-verifier-spotcheck.md` routed defect 1 — report/SCORECARD
   "rows 128 → 131; mined +1"; committed bytes re-derive 119 → 128, mined +7, rejected +2
   (`.ufo/waves/round-43/verification/freeze/registry-count-r4{2,3}-check.txt`). Captured-by:
   none — no gate re-derived the stated counts before filing (kama's writing-revision check,
   S130, was not adopted here until this round). Fix: every registry count re-derived with the
   CORPUS.md census commands over `git show <rev>:corpus/SOURCES.md` before filing; able to
   fail — `registry_count_check.py` exits 1 on the round-42 claims and 0 on the round-43
   correction; knowledge entry `corpus/knowledge/claim-count-derivation.md` (cites S130) lands
   the discipline; the correction entry in SCORECARD names the superseded text, append-only.
8. **Class: citations of swept misroot files left unannotated across rounds 30–42 (found by the
   standing §paths gate this round).** Evidence: `node scripts/freshness-sweep.mjs --section=paths`
   exit 1 "2 unannotated miss · 2 NOT in pins.pathsMissSet"
   (`.ufo/waves/round-43/verification/freeze/sweep-before.txt`); the two tokens are the
   round-29/round-33 misroot incident paths whose fleet copies the round-29/33 sweeps deleted.
   Captured-by: the freshness sweep §paths gate caught it; QUALITY "Absence annotation content"
   defines the bar the fix must meet. Fix: one annotation row inside each Mistakes table
   (`corpus/lessons/round-29.md:104`, `corpus/lessons/round-33.md:45`), each naming the exact
   missing target, the dated removal event and the surviving lane copy, marked historical and
   non-executable; both tokens entered in `pathsMissSet`; movement census: the round-29 row
   shifts two historical wave-file pointers (`round-30/w2/CriticC1Scope.md` :118-122 →
   :119-123; `round-34/w1/CriticFrontierNovelty.md` :124-132 → :125-133), corrected by dated
   EOF notes appended to both files; sweep re-run exit 0 (`sweep-after.txt`). Able to fail —
   the sweep is red on the pre-fix tree (exit 1) and green after (exit 0); the annotation rows
   carry their own absence wording inside the ±2-line window.

## Round-42 closure routed repairs — disposition this round

1. Registry arithmetic → corrected in SCORECARD (append-only entry) + Mistake 7 + checker receipts.
2. Freeze before ANY seat scores → this round's counter v4, predicate, kill rule, control classes
   and all L1 receipts committed before the wave taskCall leaves the lane (SCORECARD "Round 43 —
   C1 and C2 declared"; the wave dispatches only after the freeze commit lands).
3. H4 qualification stays → the round-43 section carries H4 "in-class only, qualified" unchanged.
4. Wave-2 settle line → the round-43 dispatch log carries dispatch and settle lines both.
6. Report T2 range wording → the round-43 report keeps L1-receipt T2 (1.28–1.382) distinct from
   any rerun maximum, per source; the round-42 report's mixed range is corrected by this
   round's report erratum, not by editing filed bytes.
