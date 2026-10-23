# CriticDeclaration — read-only adversarial review

Axes: **operability** (judged); **freshness** (owned, not claimed). Frozen assignment revision: `f043c72146ddb7e3bb1c64d26fd5ae2b01b508f8`.
No code run, tool built/scored, runtime invoked, or production file edited. Commands/exit codes: none; tool calls were file reads/searches only. No installs. Stored results below are evidence read, not reproduced verification.
Paths below are lane-relative unless absolute. `C` = `.ufo/waves/round-40/c1_count.py`; `Q` = `corpus/QUALITY.md`; `P` = fleet `.ufo/prompts/kake-round-40.md`.

## Per-rule findings
| Attacked statement / rule | Finding | Evidence and smallest safe correction |
|---|---|---|
| One concrete after-value, one command (P:343–345) | holds | SCORECARD:2578–2599 names one Boolean predicate and revision-scoped command; the 30-witness numerator plus 150-fixture regression is concrete, not a score increase. |
| Same predicate in declaration, code, receipts (P:357–360) | holds | SCORECARD:2578–2582 = C:31; C:286–287 implements the conjunction, including 30 rows, exit 0 and exact summary. Every inspected pre-receipt and `/fast/scratch/hyaku/kake-r40/l1/ref.json:2` carries that sentence. Current file digests were not recomputed. |
| Do-nothing target exclusion (P:352–356) | holds for recorded controls | SCORECARD:2597–2603; base 10/30 and constants/no-reader below target. This does not establish exclusion of the partial-repair counterexample below. |
| Shortcut cannot meet / repair of three classes | overstated | SCORECARD:2553–2557,2611–2614 exceeds the exercised sub-shapes: C:102–105 has no LF-bearing `sitemapUrl`. Preserve the frozen target; score the proposed partial repair separately and apply SCORECARD:2619–2623 if it actually meets. |
| Axis named by changed surface (P:361) | holds | SCORECARD:2551,2553–2558 changes a runnable held sitemap auditor: operability, not freshness merely because sources were reopened. |
| No universal repair inference (P:346–347) | overstated | SCORECARD:2553–2567 names broad E/U/R classes, while C:81–139 enumerates 30 templates, not every character/location/interaction. Append an explicit finite-witness limitation without changing the predicate or erasing the original claim. |
| QUALITY (n): controls only skip declared work | overstated | SCORECARD:2611–2616 includes single-sub-shape partial repairs, overlapping Q:960–963's near-complete/single-point-mutant warning; its pre-decode NUL example can also describe a behavior-equivalent implementation (below). Require a demonstrated skipped behavior, not mechanism alone; do not retroactively exempt a scored control. |
| QUALITY (o): pre-declaration tool hash/class inventory | holds for inspected inventory | SCORECARD:2600–2607 names base, four present L1 controls, absence, and the reference/build class. Present tools have full hashes in pre-receipts:21; reference hash matches the external receipt:21. Absence correctly has null hash. No undisclosed scored tool was found in the inspected evidence. |
| QUALITY (o): independent attacks before freezing | wrong against inherited requirement | SCORECARD:2548,2600–2607,2624–2626 places only L1 controls/reference before declaration and independent mutation after it. `corpus/lessons/round-39-verifier-spotcheck.md:177–178` expressly requires non-author mutant families and a tweaked shortcut before a later countable sitemap claim freezes. Public witnesses remove sealing, not that routed duty. Later attacks cannot supply earlier evidence; record the unmet prerequisite for the canonical judge. |
| Coverage versus quality (P:362–365) | holds | SCORECARD:2557–2558 explicitly claims repair/quality of a held capability, not a new capability, coverage, or depth. One claim is permitted; two is only preferred. No calibration claim is made. |
| Isolation / no-network description | overstated | SCORECARD:2594–2596 describes bubblewrap, but C:278–279 launches the regression runner outside it; `scripts/sitemap_audit_selftest.py:873–876` directly launches the tool. Scope isolation wording to the 30 witnesses; regression isolation is not established. |
| Frozen target / consequence | holds as declaration, not yet exercised here | SCORECARD:2619–2623 explicitly distinguishes before-build exploratory conversion, after-score failure, and a build miss. No result from this read-only seat fires that rule. Do not change it after scores. |

## Strongest counterexample: missing declared U sub-shape
[INFERENCE; unbuilt/unrun] Keep the reference's E/R and all `loc` handling; reject TAB, CR and leading C0/space in `sitemapUrl`, but omit LF rejection there. C:102–105 exercises only TAB, CR, leading space and U+0001 in that field. Other witness manifests use the clean `su`; random seeds never change this omission. The inspected regression fixture table (`scripts/sitemap_audit_selftest.py:114–792`) likewise has no LF-bearing `sitemapUrl`.
Concrete omitted input: a clean in-scope file, `sitemapUrl = "http://w123.example/d/site\nmap.xml"`, and `loc = "http://w123.example/d/p"`. SCORECARD:2564–2568 requires `check_invalid`; the proposed partial repair would let `urlsplit` erase LF and return clean. It is explicitly a skipped sub-shape under SCORECARD:2611–2614. Thus 30/30 plus 150/150 is structurally compatible with this omission, but **no met result is claimed without scoring**.
Smallest safe correction: retain the original apparatus/result; give this exact omission to an authorized control executor, then honor the frozen consequence if measured met. An added LF witness would be supplemental, not a replacement rule after data.

## False-control counterexample: equivalent NUL implementation
[INFERENCE; unbuilt/unrun] Reference `/fast/scratch/hyaku/kake-r40/shared/ref_fix.py:183–193` strictly decodes UTF-8, then tests decoded U+0000. Computing a raw-byte NUL flag before decoding, retaining decode-error precedence, and using the flag only after successful decoding is behavior-equivalent: valid UTF-8 contains U+0000 iff its bytes contain 0x00; stripping a UTF-8 BOM changes neither. It fits the literal pre-decode-sniff example at SCORECARD:2615 yet omits no E work. This is a classification defect, not evidence that a genuine skipped-work control scored met.
Smallest safe correction: distinguish an incorrect pre-decode verdict from an equivalent precomputed flag; acknowledge the frozen class ambiguity rather than reclassifying a survivor after seeing its score.

## Stored receipts inspected (not runs by this seat)
`pre/` below is `.ufo/waves/round-40/verification/pre/`; counts are passed/30, E/U/R, selftest summary (runner exit), met.
| Receipt | Recorded result |
|---|---|
| `pre/base-f171c58b.json`, `pre/base-f171c58b-seed2.json` | 10; 4/9,3/13,3/8; 150/150 (0); false |
| `pre/l1-const_clean.json` | 5; 2/9,3/13,0/8; 42/150 (1); false |
| `pre/l1-junk.json` | 0; 0/9,0/13,0/8; 0/150 (1); false |
| `pre/l1-all_false.json` | 8; 0/9,4/13,4/8; 10/150 (1); false |
| `pre/l1-no_reader.json` | 8; 2/9,3/13,3/8; 47/150 (1); false |
| `pre/l1-absent.json` | 0; byClass empty; selftest null; false |
| `/fast/scratch/hyaku/kake-r40/l1/ref.json` | 30; 9/9,13/13,8/8; 150/150 (0); true; build candidate, not a control |
Recorded counter SHA256: `6d73b8f498a29a5a86c9a7f1ce5d87cd135c40f1b634d869d14659cc10bee8d8`.
Recorded tool SHA256s: base `6d86c8cef78e36d372f7277096ec163cc8f1e919fa66702ad24e5e32f9a240ec`; const_clean `700ef41f68b50d3ea2168b56107fea2d2093556a7427b9bef9fbfd85006f75e2`; junk `71a2d79cb80f223013a4da0fc2b35463b430aff62c6ac783f79a5f45b4f068a4`; all_false `165028d968d008d931fc797f80a9e7dce10893f51186dcd23bc42cb799c824a8`; no_reader `a8beaab16c012224c4b8469f91f867165a7e9e1f7aa10a227e917fb0b0db1b73`; reference `03a8fba4930ad7628a569e7aa30b3ece728fbb6eb3fa4ac7c9a78dfbeb07b22b` (paths in SCORECARD:2601–2605 and receipt `toolFile`; not recomputed).
The external reference receipt is not present in the lane's inspected `verification/pre/` listing: preserve it with the other receipts for committed provenance. This evidence-placement repair does not repair the pre-freeze timing requirement. Operability is impacted; no freshness change/harm or round-admission verdict is asserted.
