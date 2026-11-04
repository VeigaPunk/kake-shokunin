# Round 44 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-23 (closed_at 2026-10-24T02:49Z)
lane repo: /home/vgpnk/Projects/shokunin/kake-shokunin (jj-colocated; all git read-only checks against branch `master`)
base: 18cb2c28f47c3ec3732ffa06c456e61b3444b1a2 → tip: 942fe187034c0666b5300e134e14b76d5e92a583
report: .ufo/reports/round-44/kake.md (fleet commit 11f58229ef402428641b0d528868fbb6b79d63de, author kake-shokunin)

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity, after lane work | `git log --format='%an %cd %H' -- .ufo/reports/round-44/kake.md` | `kake-shokunin Fri Oct 23 23:43:11 2026 -0300 11f58229…`; lane tip 942fe187 committed 23:41:44 — report lands last | PASS |
| SHONEN heading, one line per box | read report | `## SHONEN` with 4 box lines (`[ ]`,`[~]`,`[ ]`,`[~]`) | PASS |
| Cited commits exist + ancestor of `master` | `git merge-base --is-ancestor <h> master` for 18cb2c28, 942fe187, 297aa62d, 5f5c9c42, 020bc457 | all 5 ancestors of master | PASS |
| Lane repo pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state …` + `git status --porcelain` | `ahead=0 behind=0`, `tracked=0 untracked=0`, HEAD=942fe187 | PASS |
| Prompt carries template contract | grep `.ufo/prompts/kake-round-44.md` | report path (line 101), L2 floor §3 (line 82), commit-then-push + push scope + L0 (§5, line 131), SHONEN (line 118), write scope (line 259), lands-last hash citation (line 325), hyaku addendum | PASS |
| Report on fleet origin | `git merge-base --is-ancestor 11f58229 origin/master` | ancestor | PASS |
| Misroot sweep | `git -C fleet status --porcelain` | only `.ufo/state/*` driver files + operator/driver scratch; zero kake-r44 files at fleet root | PASS |

Defects (status-neutral): none in step 1.

Driver digest (copied from `.ufo/watchdog.log` via the dispatched closure prompt):
launch 19:43:51 pgid=2390638 attempt=3 (invalidated: L1 dispatched under executor leaf role);
launch 19:48:02 pgid=2413377 attempt=1 (orchestrator freeze, zero progress);
launch 19:57:18 pgid=3677061 attempt=2 (second orchestrator freeze);
launch 20:17:49 pgid=1084624 attempt=3; launch 20:33:27 pgid=2228759 attempt=1;
launch 22:40:31 pgid=12119 attempt=1; complete 23:43:39 attempt=1.

## Claim re-checks

Claims were **evidence-verified** per PROTOCOL §Gate standard (closure consequence): the two
instruments (`c44_audit.py`, `scripts/ledger_latest_check.py`) are lane-owned gates; I did not
execute them. I re-measured plain counts over committed bytes and verified committed receipts,
self-test tallies, and shas. Zero exploratory claims this round.

### C1 — operability (capability acquisition): witness-class gate — MET (evidence-verified)

- Control registry: `grep -cvE '^\s*(#|$)' .ufo/waves/round-44/controls-27.tsv` → **27** (report: 27).
- Class corpus: `ls .ufo/waves/round-44/classes/g*.py` → **10 modules G1–G10** (report: ten).
- Frozen bytes: `sha256sum c44_count_v5.py c44_audit.py` → `5cedaa3b9f91…`, `8ee2c8bf9333…` (report pins `5cedaa3b…`, `8ee2c8bf…`); `classes/g6_fold_pairs.py` → `cddc5c7d862a…` (report `cddc5c7d…`). Held build `020bc457` is an ancestor of master.
- After receipt `verification/claim/after-final/after-v5.json` + `.txt`: `witnessed=27/27 notMet=27 build_met=3/3 ok=True`, counter `5cedaa3b9f91`; per-row catches present for all 27; `build#1..3 met=True equal=21/21` (report: 27/27, 3/3 — match).
- Placebo `placebo-final/`: `witnessed=0/27 ok=False` counter `9ce3acd4c4c7` (report: 0/27, exit 1 — match; mixed `caught=C` on repeat-len-band disclosed in report).
- v4 support `v4-final/`: `witnessed=0/27 (no class runs) ok=True` (match).
- Canary `canary-final/`: `notMet=5/5 ok=True` with four r42 canaries + junk (match).
- Pre-fix baseline `w2-baseline/run1|run2/`: run1 txt `witnessed=23/27 ok=False` (report: 23/27 reproduced twice — run2 present).
- Counter bytes unchanged between claim commits: `git diff 297aa62d 942fe187 --stat` touches only `ledger-after.txt` + `SCORECARD.md` (4 lines each) — match with report.
- Kill rule 4 (no circular reads): `grep -n 'controls-27\|controls-r43\|/controls/' classes/*.py` → no match; `grep -c 'open('` → 0 in all ten modules. Agree with `w2/CriticKillRules.md`.
- Self-test committed evidence (`w2/SonicPins.md:197-204`): `--selftest` exit 0; per-row receipt re-derivation at recorded seeds is `w2/ExecAfterBaseline.md` (evidence-verified, not re-executed).
- Label fix visible in the claim receipt: `buildport-m6 G2 caught=G2,G4,G9` (manifest correction 2 landed).

### C2 — freshness: r43 ledger figures re-derive — MET (re-measured)

Re-derived independently of the checker, over committed bytes at master:
- rescore-tally: `jq -r '.toolSha256' .ufo/waves/round-43/verification/l1-rescores/*.json | sort -u | wc -l` → **14** distinct shas over 14 receipts; SCORECARD.md:3581 last statement "re-scored 14 of the 27" — match.
- donothing-ratios: `ref41-base.json` → `ratios.T1=4.207, T5=7.047` → quoted "T1 4.21, T5 7.05" (LOG.md:1703) — match at quoted precision.
- build-ratio-range: build-1/2/3 → T1 1.004–1.009 → "1.00–1.01"; T5 1.105–1.215 → "1.11–1.22" (LOG.md:1705) — match.
- After receipt `verification/claim/ledger-after.txt` at tip: `3 figures, 0 mismatches`, exit 0; before `verification/ledger-before.txt`: `3 figures, 3 mismatches`, exit 1. Mismatches 3 → 0 confirmed.
- Kill rule 1 clean: r43 receipts last touched by round-43 commit b49cba9 (pre-base); `git diff base tip -- .ufo/waves/round-43/` adds only the inherited `w1/CtlPrefixCache.md` seat report (as the report states).
- Checker self-test committed evidence: `w2/SonicPins.md:241-245` — `selftest: 2/2 passed`, exit 0.

### Owned-axis harm check

`git diff base tip -- SCORECARD.md` is purely additive: one capability row in `## Capabilities`
+ the appended "Round 44" measurement section (existing axis rows untouched); LOG.md gains the
round-44 entry (line 1689); corpus/SOURCES.md `2 +0`; lesson round-44.md new. **No owned axis harmed.**

## Discernment spot-check (LEARNING.md)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S129 | Admit (locator correction) | `tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md` §Verdict first paragraph; `ReviewFreeze.md` §Verdict first paragraph | **agree** | Both quotes located verbatim: "The do-nothing shortcut never reaches `predicate_pass=true`" (CtlDoNothing.md:9-11) and "every pinned sha256 verifies over the committed blob" (ReviewFreeze.md:5). Corrected locators are accurate. |
| S130 | Admit (locator correction) | `kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` §"Checking self-assessment statements at writing" | **agree** | Quote "records a calibration error present when the statement was written" is in the first (only) paragraph under the heading. Locator correction accurate. |
| (reject sample) | — none recorded — | — | n/a | The round-44 `## Gate` contains **zero reject decisions** (two admit rows only), so no reject was sampleable this round. Recorded as a conformance observation below. |
| S131 (new row) | superseding row for S129 | byte-compare cells lesson ↔ SOURCES.md | agree | anchor + teaches cells byte-exact from the lesson table (python compare, both `True`). |
| S132 (new row) | superseding row for S130 | byte-compare cells lesson ↔ SOURCES.md | agree | anchor + teaches cells byte-exact from the lesson table (both `True`). |

Gate quotes: 6, 8, and 10 words — all ≤25 words, each with location and 2026-10-23 access date.

Census: `scripts/sources-census.sh validate --root … kake` → exit 0, `ok …/corpus/SOURCES.md`, and the
12 W04 duplicate-url warnings are byte-identical to the report's list (S033, S088, S092, S098, S099,
S102, S110, S111, S115, S116, S117, S127). Rows 130 → 132 verified by count (`grep -cE '^\| S[0-9]{3,}'` → 132).

## Per-axis verdicts

- **operability — improved** (C1): capability row earned by a passing frozen before/after demonstration; evidence-verified as above.
- **freshness — improved** (C2): three ledger figures re-derived by my own jq/wc over committed receipts; 3 → 0 mismatches.

## Trend verdicts

- **expansion: improved** — new capability row (`SCORECARD.md ## Capabilities`), SOURCES.md 130 → 132 (S131/S132 byte-exact superseding rows), lesson gained Gate + Mistakes 12/13. No axis retired.
- **quality: improved** — C2 figures now match committed receipts (verified independently); both instruments carry committed mutation-test/self-test evidence (`w2/MutClassGate.md`, `w2/MutLedgerChecker.md`, `w2/MutG6Placebo.md`, SonicPins); 6 wave-1 reports sample-reviewed per `w2/ReviewWave1Reports.md` (evidence-verified).
- **discernment: improved** — the admits' locator corrections check out on re-open; the mixed-witness caveat (`w2/CriticC1Predicate.md`) and three HIGH latent gate defects (`w2/ReviewCounterContract.md`) are disclosed and routed rather than hidden. One blemish: zero reject decisions this round (below) — not enough to flip the verdict, named for next round.

## Routed defects and observations for round 45

From the report (confirmed present at SCORECARD.md:3621-3626 and w2 reports) — lane's own queue:
audit driver HIGH latent defects (counter-error / tool-absent receipts can witness; stale planted
receipts accepted), v4-mode predicate text naming ten unexecuted class runs, frozen selftest
missing timing-only/error fixtures, SOURCES supersedes-marker enforcement gap,
`corpus/knowledge/claim-count-derivation.md` still declaring `source: S130`.

Raised by this closure (status-neutral):
1. Round-44 `## Gate` recorded no reject decisions — the admit/reject spot-check could sample
   admits only; next round's Gate must log rejects so the reject leg of the outside spot-check resumes.
2. Minor (contract rule 1 reading): the ≤25-word Gate quotes for new rows S131/S132 are recorded
   under the S129/S130 rows rather than labeled per new row; the sources are identical and were
   re-opened the same day, so the grounding holds — label them per new row next time.

Tool installs this closure: none (read-only git/jq/grep/sed over committed bytes; no installs or upgrades).
