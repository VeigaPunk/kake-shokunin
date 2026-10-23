# resid — KakeR40.RerunKillAndBuild (kill-rule record & build score)

Axes: operability, freshness. Godspeed: cheap parallel attacks; all kept moves reproduced the record.
Tip `6d5cd54a`. No tools installed (used preinstalled bwrap 0.13.1, python 3.14.8, jaq 3.1.1).
Sandbox: /fast/scratch/hyaku/kake-r40res/RerunKillAndBuild/ (9 counter receipts + st179.out).

## Checks run (all exit 0 unless noted)
1. `jq -s 'map(select(.met))|length' .ufo/waves/round-40/verification/w1/*.json` → 27; `ls *.json|wc -l` → 76.
2. Receipt↔tool binding: for all 76 receipts, `jq -r .toolFile/.toolSha256` vs `sha256sum` of the stored
   `controls/w1/<Seat>/<tool>.py` → 76/76 OK. All 76 `.counterSha256` = frozen `6d73b8f4…8d8`.
3. `git log --format='%h %cI %s' f171c58b..6d5cd54a` → f043c72 05:31:14-03:00 → 12211cc 05:49:41 →
   56d57ee 05:51:15 → 6d5cd54 05:53:50; `merge-base --is-ancestor`: 12211cc5 ∈ 56d57ee4, f043c721 ∈ 12211cc5.
4. `git ls-tree -r 12211cc5 -- …/verification/w1` → 76 receipts + 3 d1check-*.txt (not receipts);
   names identical to worktree; `git diff --stat 12211cc5 tip` on w1 receipts and controls/w1 → empty.
5. Counter re-runs (`timeout 900 prlimit --as=4000000000 python3 -B .ufo/waves/round-40/c1_count.py`):
   `--revision 56d57ee4 --seed 40001` → passed 30/30 (E9/9 U13/13 R8/8), selftest PASS 150/150, met true;
   `--seed 987654321` → same, met true. Mirrors committed `verification/c1-at-56d57ee4{,-random}.json`
   (seeds 40001 / 2500532916261, toolSha 03a8fba4…7b22b, met true).
6. Per-class re-score with fresh random seeds, one meeting tool per class (controls/w1/):
   CtlKeyFinder/ctl_keyfinder_label_nofallback.py, CtlLabelKeyed/ctl_label_keyed.py,
   CtlPositionKeyed/ctl_v3_count.py, CtlURawBytes/ctl.py, L1CriticCounterexample/ctl_sitemapurl_no_lf.py,
   MutFamilyR/m02_file_gate.py → all 6: 30/30, PASS 150/150, met true (exit 0).
7. Hash pins: build tool blob `git show 56d57ee4:scripts/sitemap_audit.py|sha256sum` =
   `03a8fba4930a…07b22b` (= claim, = receipt toolSha); pinned selftest at f171c58b = `99ee9bbf…51db`;
   counter file sha = `6d73b8f4…` and `git diff f043c721 tip` on c1_count.py → empty (never edited).
8. Build selftest: ran 56d57ee4 selftest against 56d57ee4 tool → `PASS 179/179` (claim: 150→179).

## Per attacked statement
- **"27 of 76 control receipts meet" — HOLDS.** 76 json receipts, 27 `.met==true`; every met receipt
  shows passed=30 + selftest PASS 150/150; every receipt bound by sha256 to its stored control tool and
  to the frozen counter. 6/6 class representatives re-met on fresh seeds (no seed-dependence found).
- **"Recorded before the build lands" — HOLDS.** Receipts+controls committed at 12211cc5 (05:49:41-03:00),
  parent of build 56d57ee4 (05:51:15); blobs byte-identical to tip; kill rule (1) text (SCORECARD 2588-92)
  requires "any control receipt meets" → exploratory, and 27 met — rule fired correctly, counter never
  changed after f043c721 (verified by empty diff + file sha).
- **"Counter at the build 30/30" — HOLDS.** Independent re-run at `--revision 56d57ee4`, two seeds →
  30/30 met, byClass 9/9, 13/13, 8/8. Nuance, not a defect: the two receipt files recording this were
  committed at 6d5cd54, not inside 56d57ee4 (`git ls-tree 56d57ee4` empty for them); SCORECARD's
  "met true at the build commit" is about the counter's verdict at that revision, which reproduces.

## Findings (defects)
- None in scope. Two reviewer-side path bugs corrected mid-run (`../c1_count.py` from w1/ → wrong-dir
  COUNTER_DIFFERS false flag; `verification/…` missing the `.ufo/waves/round-40/` prefix → empty ls-tree)
  — both re-run correctly; no finding rests on the buggy outputs.

## Residual risk / verification gaps
- I re-scored 6 of 27 met receipts (one per class, as assigned); the other 21 met receipts are verified
  only structurally (hash-bound, frozen counter), not re-executed.
- The 49 non-meeting receipts were not re-run; SCORECARD's per-class non-meeting counts (skip-E 25 etc.)
  accepted from receipts' `passed` fields, not re-derived.
- d1check-*.txt and criteria receipts under w1/ were treated as non-receipts (not `.json`); consistent
  with the 76 count, content not audited (other seats' scope).
