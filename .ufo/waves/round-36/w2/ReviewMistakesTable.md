# ReviewMistakesTable — `## Mistakes` rows + routed-defect disposition (r36 w2)

Seat `KakeR36.ReviewMistakesTable`. Lane read-only; HEAD `f3a38bf`. Git ran
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE`; exits as named. No re-runs/network/installs.

## Mistakes table — per-row verdict

**Row 1 (unresolvable base hash): PASS, one nit.** `git show 3555f63f:SCORECARD.md:1564`
declares `Base b720d79976a1fb8fe6a8eb4b9f50e946b0cd5e07`; `cat-file -e` → exit 128, real
`b720d799ae99c19a…` → exit 0. Fail witness committed `verification/criterion-hash-resolve-
r36-decl-at-3555f63f.txt` (exit 1) + pass witness `-r35-decl-at-cd321279.txt` (exit 0);
QUALITY (e) `corpus/QUALITY.md:872`. Nit: captured-by "none" is true-as-no-check but
understates its evidence (the counter refusal caught it).

**Row 2 (body-blind shortcut vs key v1): evidence PASS; captured-by label WRONG.** v1
`sealed/cases-v1.json` k17–k24: body-reading checks all expect a hold; c/d checks all
`text/html; charset=utf-8` — verified. v2 `verification/v2/control-CtlShortcut.json`: 17
passed, k17–k24 all true = every (e)+(f) case. Fix receipts committed: v3
`control-CtlShortcut.json` 9; `ablation-s_ctkey.json` 13; `ablation-s_unsure.json` 24; v2
key verified rotating contentTypes + quote_missing polarity (`sealed/cases.json` k09–k24).
"34 v1 ablations, none skipped reading": `git ls-tree 9d81c75c` shows exactly 34 ablation
receipts, zero `s_*` — PASS. **Defect:** "pre-freeze control wave" mislabels chronology —
predicate declared frozen at `3555f63f` with zero receipts; controls scored under v2 from
`9d81c75c` (post-freeze, pre-build); the oracle changed after CtlShortcut scored (17→9).

**Row 3 (seats wrote deliverables into the lane): PASS; no fail-witness by disclosed
design.** `w1/ExecCriterionAblation.md`, `w1/ExecCriterionControlTree.md` self-disclose
landing `criteria/*.py` while untracked. Committed sha256s equal seat-reported ones
(8f9d87d1…, be52b331…; my sha256sum exit 0). "No check" in captured-by is honest — the
cell itself says no receipt can show this fix able to fail.

**Row 4 (selftest fixture contradicted contract): PARTIAL — pre-fix exit-1 uncommitted.**
`scripts/source_recheck_selftest.py:486-492` = `charset=shift_jis` + comment naming the old
`utf-16`/S090; `w2/ReviewSelftest.md:58-60` confirms correctness. The `utf-16` byte lives
only in the seat sandbox (landed sha 0ad5623b vs reported 9db94fec); the "landed tool exit 1"
run has no committed receipt. Omitted fix defect: f07 (`:481-485`) and f08 now share
byte-identical input and expectations.

## Routed-defect disposition — per-row verdict

1 **PASS** — no knowledge claim; QUALITY (a) carries the rule (`QUALITY.md:864`).
2 **PASS** — `criterion-version-bump-*.txt`: exit 1 on r35 cap 1500→2200, 0 on r36 v1→v2, 1
   on v2→v3 naming only the pin; "no target, cap or predicate" accurate.
3 **PASS** — `criterion-ablation-floor-r35-shape.txt` exit 1 (skip-(c) met 22/24); `-r36.txt`
   exit 0, 36 receipts all <25.
4 **PASS** — `criterion-control-tree-r35-report.txt` exit 1 (no listing); `-r36-controls.txt`
   exit 0 on all five ctl reports; the two filtered controls' absence is in Holds, so
   "listings in ctl/*.md" is honest.
5 **PASS** — corrections at `corpus/lessons/round-35.md:239` (S084 four of seven field
   lines) and `corpus/knowledge/security-txt-publishing.md:152-156` (S078-only cite).

## Mistakes the table misses (pointers)

- **`met:` label drift** (`w1/CriticPredicateIdentity.md`): all receipts name `passed >= 25
  of 28 sealed cases`; the declaration says `met: passed >= 25 …` (SCORECARD.md:1578,1718).
  A "fixable presentation defect"; absent from Mistakes and Carried-open; no append landed.
- **Post-score oracle change / freeze chronology** (same report, items 6–7): frozen declared
  before any receipt (`3555f63f`), key replaced after a control scored (17→9). Row 2's
  "pre-freeze" misstates this; nowhere in the lesson.
- **f07/f08 duplication** created by row 4's fix (selftest:481-492; w2/ReviewSelftest.md).
- **Counter-judge survivors** (`w1/MutCounterJudge.md:35-39`): M14 (non-rotated check ids
  pass via `idmap.get(check,check)`), M17, M18 — synthetic cases; Carried-open names
  ReviewCounterV2 D1–D3, not these.
- **Row-3 class recurring in wave 2, live:** `git status --porcelain` (optional locks off,
  exit 0) shows `M scripts/source_snapshot.py` (tracked, modified) plus untracked non-report
  files — `realrun/audit-run2.*`, `input-run2.json`, `snapshot-run2.txt`,
  `verification/c1-counter-v{1,2}-keyv1-at-4d5b3d55.*`,
  `criteria/r35-0b7779dc-parent-tree-report.md`. Wave-2 bounds are report-only too; the
  pattern repeated before the git-status gate ran. Sibling WIP vs L1 integration is not
  distinguishable from status alone, but the fix's prevention half did not hold.
## Checked-not-missing / not verified

Provider-filtered controls (CtlJunk, CtlCounterExploit): disclosed in Holds, not mistakes.
Carried-open correctly absorbs ReviewCounterV2 D1–D3, ReviewJailIsolation,
CriticContractAmbiguity, CriticAxisFit, ExecProbeQuoteMatch. Receipts read, not re-run
(bwrap/key bounds); v1 ablations verified via `9d81c75c` tree listing only. Lane writes:
this report only.

Report: .ufo/waves/round-36/w2/ReviewMistakesTable.md
