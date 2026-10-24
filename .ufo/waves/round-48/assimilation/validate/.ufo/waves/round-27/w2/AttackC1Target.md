# AttackC1Target — r27 C1 fresh falsification (freshness)

Seat `KakeR27.AttackC1Target`, critic, leaf. Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (explicit hash in every Git read).
Working-tree inputs were read only after matching frozen-candidate.json: count_c1.py `8d4c22ef…`, pairs.json `f1fa20ca…`, discovered-pairs.json `45e95683…`, carry-errata `236d9e79…` (the counter's own pin), and PairS007 report `2473852b…` (equal to the be375d9 blob). `git diff 83528f7..ac46a74 -- .ufo/waves/round-26` is empty.
Scratch is `/fast/scratch/hyaku/kake-r27/AttackC1Target/` with TMPDIR set there. No lane edits, commits or index writes. No installs.

## Verdict
The candidate's honest-stop status reproduces exactly. Strict C1 is **55/58 decided, 58/58 reviewed, exit 1**, with 7 unknown units across 3 pairs. C1 stays UNPROVABLE.
No original obligation lacks a durable record, and no known r26 or r27 STALE lacks a correction.
One fixable defect is real: the strict counter lets any pair-level HOLD override silently erase carried UNVERIFIABLE units (F1). That makes a future "58/58 green" unsafe as evidence.

## Reruns (expected = author measurements in frozen-candidate.json, declared before my runs)
| counter (blob sha256) | rev | exit | citing / reviewed / decided / unknown units | matches |
|---|---|---|---|---|
| original be375d9 `a1e46d19…` (= declaredSha256) | 83528f7 | 1 | 57 / – / 41 / – ; out `af55d0a4…` = c1-before.json sha | yes |
| original be375d9 | ac46a74 | 0 | 58 / – / 58 / – ; out `fd9d5499…` | yes (counts carried UNVERIFIABLE as decided) |
| 08014ce `26fd8bbb…` (= correctedSha256) | 83528f7 / ac46a74 | 1 / 0 | 57/–/41 ; 58/–/58 | yes (c1-guards) |
| 9ba102d `f2632131…` | 83528f7 / ac46a74 | 1 / 1 | 57/41/39 ; 58/58/56, carried 6 | yes (c1-strict-ledger) |
| candidate count_c1.py | 83528f7 | 1 | 57/41/38, 7 units/3 pairs; out `c8e7af7c…` | yes |
| candidate count_c1.py | ac46a74 | 1 | 58/58/55, 7/3; missing = S001×ghp-served-set (3), S007×ghp-custom-domain (1), S033×static-canonical-preflight (3); unreviewed=[]; out `6e053d9a…` | yes |

## Citing-set completeness (original 57 + discovered)
Independent sweep (`sweep.py`, base and candidate, all 26 knowledge files). I checked embedded ids with no word boundary (e.g. `Rejection07S013`), abbreviated ranges such as `S020-27`, lowercase or dash forms, two-digit ids and wildcards.
- The only population pair beyond the frozen 57 is S013×ghp-served-set, which is already discovered and judged.
- The only other hits are `rechecks/S0NN.json` placeholders, and their lines list rows literally.
- The 17 new pairs plus 1 override equal newDecided 18. Every r26 tag count `[r26-recheck Sx STALE]` equals stale+reclassified per (row, file). The three `[r27-recheck … STALE]` tags (S005 sitemap, S005 preflight, S004 served-set) match the three STALE records.
- The 24 r26 seat STALEs break down as 6 accepted, 4 reclassified, 1 already corrected (S021 row 6, r23) and 13 rejected. All 13 rejections have AGREE w2 reports (Rejection01, 03–09, 11, 12). No known STALE is unadjudicated.
- A/B dissent: 14 of 16 pairs agree. Pair03 (A HOLD, B STALE → HOLD) and Pair08 (A HOLD, B STALE → STALE) are both retained in the reasons.
- Not C1 debt, but disclosed broader debt:
  - 18 knowledge pairs on ids outside the population (S014 ×1, S019 ×16, S035 ×1). Recount is equal at base and candidate. Disclosed at round-27.md:43 and QUALITY:269–270.
  - 219 outside-knowledge pairs. This is a peer census that I did not re-measure.
  - SKILL-tail statements (11) and row-level `teaches` gaps (FalsifyS026, FalsifyS008). These are SOURCES/receipt scope, not knowledge pairs.

## Unit accounting (known 7/3, not the old recorded 6/2)
I re-derived this from every r26 Pair report's own count against its ledger row. All rows are equal except these four:
- S001: 28 = 21 HOLD + 3 seat STALE + 4 UNVERIFIABLE. w2 Rejection02 moves 1 of the UNVERIFIABLE to STALE. **The 3 remaining unknowns are inside the 313.**
- S033: report 9, ledger 6 (decided only), so +3 unknown outside the 313.
- S007: report 21, ledger 20, so +1 unknown outside the 313. Verified at PairS007 L8 and L40–41; the knowledge claim is at ghp-custom-domain.md:54–55. The disclosure was appended at :64–74.
- S025: report 2 HOLD (UncoveredS024S025 S-3, S-4), ledger 1, so +1 HOLD outside the 313.

So 318 = 313 + 3 + 1 + 1, and 310 decided units sit inside the 313 (313 − S001's 3). Total unknown = 3 + 3 + 1 = 7 in 3 pairs.
carry-errata.json is arithmetically correct. CarryLedger's "8" used the pre-w2 S001 count of 4 and is correctly superseded by 7.
Not independently re-derived: the 34 L1-judged units in the 14 report-less rows; there is no report to compare against.
Stale "six/two" wording survives at SCORECARD:540, SKILL:628, README:207, round-27.md:7/89–95 and ghp-served-set.md:116–120. Each is followed by an explicit 7/3 erratum (SCORECARD:547–553, SKILL:658, README:213–216, round-27.md:139–151, served-set:122–126). This is append-only and not a defect.

## F1 (defect, fixable): an override HOLD launders carried UNVERIFIABLE units
- **Attacked item:** `count_c1.py:94–125` at ac46a74. `decided.discard(key)` fires on override, then a valid HOLD/STALE runs `unknown.pop(key)`. Nothing ties a record to the specific carried units. Artifact evidence only needs a non-empty `contains` substring of any file outside `corpus/knowledge/`, the round-27 wave directory and the two r26 ledger files (`:114–116`).
- **Expected, declared before running:** a strict counter should keep the 7 units, because the probe records resolve none of them. I predicted it would instead go exit 0, 58/58.
- **Probe:**
  - Setup: a disposable clone at `…/AttackC1Target/clone` at ac46a74. Probe commit `0c2c3771ca5df13c6ac199a42a4647e218e7c458`, pairs.json `2bf6c511…`.
  - Input: append three artifact HOLD records for S001×ghp-served-set, S033×static-canonical-preflight and S007×ghp-custom-domain. Each has `evidence` = `.ufo/waves/round-26/fetched/text/<row>-1.txt` and `contains` = an arbitrary 40-character slice. These are exactly the r26 bytes that could not decide those units. The reason text says the record "resolves none of the carried units".
- **Actual:**
  - Candidate counter: **exit 0, citing 58, reviewed 58, decided 58, knownUnverifiableUnits 0, pairs 0, findings []** (out `88d02a43…`).
  - 9ba102d counter: exit 0, decided 58, while still printing `carriedUnverifiableUnits: 6`, which contradicts its own clean verdict.
  - 08014ce counter: exit 0.
- **Impacted axes:** freshness, because contract.json:10 says "UNVERIFIABLE … never counted decided" and that can now be bypassed by an unconstrained pair record. Operability, because the strict gate is not fail-closed on its own target.
- **Frozen candidate status:** unaffected today, because no such override exists. It is still 55/58.
- **Smallest safe correction:** an override of a pair with carried unknowns must not `pop` them. Clear only units the record names explicitly, for example `resolvesUnits` matching the carry identities (report row ids). Each named unit needs its own located source or quote evidence and a minimum specificity for `contains`. Anything else keeps the unknown and stays exit 1. Add this probe as a selftest red case.

## Semantic spot-checks of new pairs (not new defects)
- **S004×ghp-served-set override STALE.** S004-1.txt has 0 occurrences of "static files". The S003 general flow, in retained-text order, is trigger, checkout, build, upload, deploy, which supports items 4–5 being S003's.
  - Residual (low): r26 PairS004 row 3 had mapped "steps 4-5" to S004's own YAML example (Checkout, Setup, Build, Upload artifact, then the Deploy job) and judged it HOLD. pairs.json does not name or reject that alternative.
  - The `<ol>` numbering Pair06B cites was seen in pre-filter HTML. The retained visible text has no list numbers, so "numbered" is a non-retained observation.
  - Fix: one appended sentence naming the rejected r26 reading. The pair stays decided either way, and counts are unchanged.
- **S003 HOLD / S005 STALE on the same `S001-S006` token at sitemap:2.** This is coherent under one reading: the r20 lesson's A2 row (round-20.md:261) maps this entry to S001/S002/S003/S004/S006/S008 and excludes S005. Pair03B's dissent is preserved. I have no counterexample beyond that dissent.
- **S004 and S006 on publish-channels:2, S022 and S023 on preflight:2.** The opened-dates (2026-10-19 and 2026-10-20) match the SOURCES `opened` cells. The S008 pairs (×4) are correctly treated as retry provenance.
- **Grouped six.** Quotes and anchors were verified in the retained text; S001 lines 29–36 equal the tar block. The candidate labels the synthesis as local and marks S005 STALE.

## Uncertainties
- The 34 L1 units and the 219 outside census were not re-measured.
- Source semantics beyond the spot-checks above were not re-judged.
- HTML received digests cannot be reconstructed, by design.
- The clone and outputs remain in scratch.
- Checks for Main: rerun the F1 probe after any counter fix, and run `count_c1.py --selftest`.
