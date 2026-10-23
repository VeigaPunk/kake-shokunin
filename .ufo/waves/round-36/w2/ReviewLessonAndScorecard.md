# ReviewLessonAndScorecard — round-36 lesson / SCORECARD / LOG number re-derivation

Attacked: every count and hash in `corpus/lessons/round-36.md`, SCORECARD "Round 36"
sections (lines 1563–1732) + capability row (line 197), LOG round-36 entry (lines
1488–1506). Method: sandbox clone at `f3a38bf`
(`/fast/scratch/hyaku/kake-r36w2/ReviewLessonAndScorecard/clone`), receipts parsed
directly, sha256 recomputed, counter re-run live (bwrap present), selftest re-run.

## Reproduced exactly

| Claim (source) | Receipt / re-derivation | Result |
|---|---|---|
| C1 28/28 at `4d5b3d55`, met (lesson; SCORECARD:1718; LOG:1500; cap row) | `verification/c1-at-4d5b3d55.json`, `c1-keyrev-at-4d5b3d55.json` (exit files 0); live re-run: `python3 -B sealed_count.py --revision 4d5b3d55… --key-revision fd1fb723…` → passed 28, met true, exit 0 | match |
| Before 0/28 at `b720d799`, `3555f63f`, `9d81c75c`, `cd321279` (lesson; SCORECARD:1701) | `control-base.json`, `control-declaration.json`, `control-counter-v2-commit.json`, `c1-keyrev-at-cd321279.json`; live re-runs all: passed 0, met false, exit 1 | match |
| Reveal commit refused exit 2 (lesson; SCORECARD:1720) | `c1-keyrev-at-fd1fb723.json` `error:"key visible at the measured revision"`, `.exit`=2; live re-run exit 2, identical stdout | match |
| Tool sha256 `577b2d7d…0d48`, unedited (lesson; SCORECARD:1721) | `sha256sum` at `f3a38bf` and at `4d5b3d55` blob = `577b2d7d028964e0…5510d48`, = receipt `toolSha256` | match |
| Counter sha256 `88ec5914…` (SCORECARD:1696) | `sha256sum sealed_count.py` = `88ec59140258…42ff8e`, = every v3 receipt `counterSha256`; v1 `28169d95…9728`, v2 `1bf16734…162c` match SCORECARD text | match |
| Key pin = key v2 (SCORECARD:1696–1698) | `KEY_SHA256` v3 = `44c94838…ef1d` = `sha256(sealed/cases.json)`; v2 pin `a690d39e…` = `sha256(cases-v1.json)`; v2→v3 file diff = docstring + `KEY_SHA256` line only | match |
| 28 cases, 7 bullets × 4 (lesson; SCORECARD:1584) | `sealed/cases.json`: 28 cases, bullets a–g each exactly 4; case ids identical to `cases-v1.json` | match |
| Controls v3: 0,0,8,12,9; none met (lesson; SCORECARD:1701,1724; LOG:1499; cap row "at most 12") | `control-{CtlConstantClean,CtlAllFalse,CtlNoReader,CtlNaiveReader,CtlShortcut}.json` = 0,0,8,12,9, all met=false, .exit 1 | match |
| CtlShortcut v2 17/28 passing all (e),(f) cases (lesson; SCORECARD:1688,1690; QUALITY (f)) | `v2/control-CtlShortcut.json` passed=17, perCase pass-set = all of a,b, all 4 e cases (k17–k20), all 4 f cases (k21–k24), plus k12 | match |
| 36 ablations 13–24, none met; s_ctkey 13, s_unsure 24 (lesson; SCORECARD:1702,1725; LOG:1499) | `ablations/`: 36 `ablation-*.json`, min 13 (`s_ctkey`), max 24, all met=false | match |
| Each rule ablation fails ≥4 cases of its own bullet (SCORECARD:1586) | perCase of all 34 rule ablations: every own-bullet case id in fail set | match |
| Private reference 28/28 (SCORECARD:1678,1702) | `ablations/reference-private.json` passed 28 met true | match |
| Independent blind impl 28/28 (lesson; SCORECARD:1721; LOG:1501) | `independent-selftest-reference.json` passed 28; `toolSha256 a5176fee…221f` = `retained/independent/selftest-seat-reference.py` sha256 | match |
| Selftest 101/101 (lesson; SCORECARD:1726; LOG:1501; cap row; SKILL:1066) | `python3 -B scripts/source_recheck_selftest.py` → `{"passed":101,"failed":0}`, exit 0 | match |
| Real-input run: 90 evaluated, exit 1 failed-policy; findings quote_missing 9 (S004–S008,S017,S025,S065,S068), moved 2 (S040→what-is-github-pages, S068→…), gone 1 (S087), unsupported_type 2 (S016,S066); 14 findings/13 rows (lesson; SCORECARD:1728; LOG:1502) | `realrun/audit.json`: checksEvaluated 90, verdict failed-policy, `.exit` 1; 14 findings, 13 distinct check ids; reason counts 9/2/1/2 exactly; manifest 90 checks; input.json 90 entries, distinct ids, no operator-owned host | match |
| Gate access times 01:08:56–01:09:01Z, HTTP 200 ×7 (lesson; LOG:1494–1495) | `sources/receipts.json`: exact per-row times/status; `bodySha256`/`bodyBytes` match gunzipped `S0*.html.gz` for all 7; all 7 lesson quotes are substrings of retained `S0*.txt`; word counts 10/19/9/10/4/8/7 match | match |
| Row cells S088–S094 (lesson row-change list) | `corpus/SOURCES.md:96-102`: mined×5/rejected×2, opened 2026-10-23, recheck 90d, used-by `scripts/source_recheck.py` (mined) / `—` (rejects); retained-text sha cells = `sha256(S0*.txt)` | match |
| Wrong declared base hash + correction (lesson mistake 1; SCORECARD:1565,1706; QUALITY (e)) | `git cat-file -t b720d79976a1fb8f…5e07` → "could not get object info"; line 1565 retains it, :1706 corrects; `criterion-hash-resolve-r36-decl-at-3555f63f.txt` exit 1, r35 file exit 0 | match |
| Criterion receipts (b)(c)(d) (lesson mistakes bullets) | version-bump: r35 v1→v2 exit 1 (cap 1500→2200), r36 v1→v2 exit 0, v2→v3 exit 1 naming KEY_SHA256; ablation-floor r35 exit 1 / r36 exit 0 "36 ablation receipts scored"; control-tree r35 exit 1 / r36 five controls exit 0 | match |
| w1 wave = 36 seats (LOG:1500) | `w1/swarm-registry.json` members = 36 | match |
| SCORECARD diff additions-only + one capability row | `git diff --numstat b720d799 f3a38bf -- SCORECARD.md` = `172 0`; hunks `@@ -196,0 +197 @@` (cap row) and `@@ -1560,0 +1562,171 @@` | match |
| Whole-diff additions only; SOURCES/SKILL/LOG/lessons append-only | `git diff --numstat` full range: 0 deleted lines in every file (23866 ins / 0 del) | match |
| SKILL rows + QUALITY (a)–(f) (LOG:1504–1506) | SKILL:1066–1067 rows exist; QUALITY:860–887 (a)–(f); security-txt:152 and round-35.md:239 appended corrections present | match |

## Mismatches / gaps

1. **Minor — S068 moved target text.** Lesson: `moved` 2 (S068 → `…/docs/sharing/webmasters/`).
   `audit.json` target is `https://developers.facebook.com/documentation/sharing/webmasters`;
   `…/docs/sharing/webmasters/` is the *origin* URL (manifest S068 hop). S040's arrow shows the
   resolved new path; S068's shows the old one. Either wrong target or inconsistent notation.
2. **Minor — cross-reference off by one.** Lesson: "routed defects 2–5; their fixes are QUALITY
   round-36 (a)–(d)". QUALITY:862 grounds (a)–(d) in routed defects **1–4**; defect 5's fix is
   the appended corrections (disposition table row 5), not QUALITY (a)–(d).
3. **Verification gap — v2-era ablation floor.** SCORECARD:1678 "each of the 34 rule ablations
   16 to 24 of 28" was scored under key v1/counter v2; those receipts were replaced by the v3
   rescore, whose committed minimum is 14 (`f_labelcase`). No committed receipt re-derives the
   16 floor; consistent (key v2 changed expectations) but not reproducible.
4. **Nit — LOG "opened at 01:08Z".** Receipts span 01:08:56–01:09:01Z; rounds into 01:09.
5. **Nit — predicate field.** SCORECARD:1575 claims "the same sentence … in every receipt's
   `predicate` field"; receipts carry `passed >= 25 of 28 sealed cases` (no `met:` prefix);
   counter `PREDICATE` constant matches receipts, not the declared sentence verbatim.

## Not verified
- Scout "byte-identical" live re-fetches (their w1 reports only; bodies verified vs receipts).
- w1 report count 35 vs 36 members (seat count claim verified; report-per-seat not claimed).
- v2-era receipts other than controls are gone; key-v1 shortcut/ablation internals not replayed.
- No installs made (bwrap/python3/git already present).

## Verdict
Every headline number reproduces from committed receipts and live counter/selftest re-runs;
SCORECARD diff is additions-only plus the one inserted capability row. Two minor text defects
(S068 arrow target; QUALITY letter mapping), one unverifiable v2-era floor, two nits.
