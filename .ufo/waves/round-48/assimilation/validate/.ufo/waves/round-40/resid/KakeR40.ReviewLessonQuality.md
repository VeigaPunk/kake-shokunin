# KakeR40.ReviewLessonQuality — residual review: lesson Mistakes 1–2, QUALITY (o)/(q)/(r)

Seat: reviewer leaf (no subagents). Scope: falsify "shown able to fail" claims and captured-by
claims of lesson Mistakes 1–2; whether (r)'s 30/30 claim matches receipts. Sandbox:
`/fast/scratch/hyaku/kake-r40res/KakeR40.ReviewLessonQuality/`. No fleet mutations; no tool
installs (used existing git/python3/jq; no channel changes).

## Checks run (exact argv; each `timeout` ≤900 s, `prlimit --as=4000000000`)
1. `python3 -B criteria/preseal_order_check.py --root kake-shokunin --revision f043c721 --counter
   .ufo/waves/round-40/c1_count.py --receipts .ufo/waves/round-40/verification` → verdict fail,
   independentReceipts 0, authorReceipts 7, counterSha256 6d73b8f…, EXIT 1.
2. Same at `--revision 12211cc5` → pass, independentReceipts 76, authorReceipts 7, EXIT 0.
3. Same at `--revision ceecb1b1 --counter .ufo/waves/round-39/sealed_count.py --receipts
   .ufo/waves/round-39/verification` → fail, independentReceipts 0, authorReceipts 1,
   counterSha256 f3a0cd60…, EXIT 1.
4. `python3 -B criteria/d1_check.py --tool <git show 56d57ee4:scripts/sitemap_audit.py>` (sha256
   03a8fba4…) → green (v11 clean exit 0; v20 failed-policy/xml_malformed exit 1), EXIT 0.
5. Same `--tool <git show f171c58b:scripts/sitemap_audit.py>` (sha256 6d86c8ce…) → green, EXIT 0.
6. Same `--tool criteria/mutant_d1_fixed.py` (sha256 45f9c9e5…) → red (v11 expected clean, got
   failed-policy/xml_malformed), EXIT 1.
7. `python3 -B c1_count.py --root kake-shokunin --tool-file controls/w1/CtlKeyFinder/ctl_keyfinder.py
   --seed 183816564180758` → passed 30/30 (E 9/9 U 13/13 R 8/8), selftest PASS 150/150, met true,
   EXIT 0.
8. Same `--tool-file controls/w1/CtlLabelKeyed/ctl_label_keyed.py --seed 129625516462744` → passed
   30/30, met true, EXIT 0.
9. Same `--tool-file criteria/mutant_d1_fixed.py --seed 40001` → passed 30/30, met true, EXIT 0.
10. `jq -s 'map(select(.met))|length' verification/w1/*.json` → 27; total receipts 76.

## Findings (per attacked statement)
- **Mistake 1 fix (o amended): HOLDS.** "Shown able to fail: red at f043c721 (0 non-author receipts,
  exit 1), red at ceecb1b1 (exit 1), green at 12211cc5 (76 receipts, exit 0)" reproduces exactly
  (runs 1–3); committed `verification/criteria/preseal-*.txt` identical. 27-of-76 meeting controls
  (run 10) reproduces the evidence. Captured-by QUALITY (o): **right** — `corpus/QUALITY.md:993-1000`
  names the same revisions/check as its executable check.
- **Mistake 2 fix (q): HOLDS.** d1_check red on the mutant (exit 1) and green on base and build
  (exit 0) (runs 4–6), matching committed `w1/d1check-{base,ref,mutant}.txt`. Selftest fixture
  `r40_d1_version_1_1_clean` exists at `scripts/sitemap_audit_selftest.py:830-832` (declaration
  version="1.1", clean expectation, substantive). The mutant also scores 30/30 on the round's counter
  (run 9), so "nothing the round measured would have caught it" holds. Captured-by none → (q) added:
  **right** (`QUALITY.md:1001-1006`).
- **(r) claim: HOLDS.** Replaying the frozen counter on both standing controls with the receipts' own
  seeds gives 30/30, met true, selftest PASS 150/150 (runs 7–8), matching
  `CtlKeyFinder__ctl_keyfinder.json` and `CtlLabelKeyed__ctl_label_keyed.json` (passed 30, met true,
  counterSha256 6d73b8f…). Check is red on the round-40 counter exactly as the criterion says.
  Code corroborates the leak: `c1_count.py:259` materializes case dirs `case-<witness id>`; `:278`
  runs the regression selftest unsandboxed.

## Residual risk / verification gaps
- preseal_order_check counts any non-author-labeled receipt with matching counterSha256 regardless of
  whether it met the predicate; criterion (o) requires committed non-author control receipts, not met,
  so this is not a defect.
- Source-quote fidelity of S110/S115 and the (o) check's author-prefix coverage were not in my seat;
  left to source/review seats. No actionable finding remains in scope.
