# Round 42 — non-author verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_kfc)
Round: kake lane-round 42 (hyaku run 5, attempt 2). Lane base `1ef7a0e95f6884dd113fe583a997c633fe330ddd` → HEAD `5949e66ffe803859372adc975dd7392f0f07d626`. Report `.ufo/reports/round-42/kake.md` (fleet commit `b82c358a37361d68c356b3898dd92936d1ac9e7e`, lane-authored, pushed). This file is the only lane-repo write of the closure; nothing else in the lane was touched.

Watchdog digest (mutable log; copied verbatim at closure):
- 2026-10-23T07:48:41-03:00 launch kake round=42 pgid=1935732 driver=hyaku-inline attempt=1
- 2026-10-23T15:03:19-03:00 lane-dead-no-report kake round=42; retry same round (hyaku-inline attempt=1: superseded at T0 2026-10-23T18:00Z: stale phase-4 author (orchestrator died 2026-10-23 ~09:30 -03); fresh attempt)
- 2026-10-23T15:10:25-03:00 launch kake round=42 pgid=93876 driver=hyaku-inline attempt=2
- 2026-10-23T15:22:24-03:00 complete kake round=42; hyaku-inline attempt=2

## Step-1 conformance

| Check | Method | Result |
|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-42/kake.md` | PASS — `kake-shokunin kake@shokunin.local b82c358a…` |
| Report pushed / ancestor | `git merge-base --is-ancestor b82c358a HEAD` + `git ls-remote origin` (main=master=`cbee7b55…`) | PASS |
| SHONEN heading, one line per box | report `## SHONEN` — 4 lines, marks `[~]/[ ]/[~]/[~]`; lane SHONEN.md has exactly the 4 canonical boxes (all `[ ]`; only a non-author may write `[x]`) | PASS |
| Cited commits exist + ancestor of lane branch | `git merge-base --is-ancestor <hash> master` for `1ef7a0e9`, `5949e66ffe`, `68586658268c`, `721310b1`, `1e1da697`, `020bc457` | PASS (all ANCESTOR-OK) |
| Tool hash `914ebdee…` | `git show 5949e66ffe:scripts/sitemap_audit.py \| sha256sum` = `914ebdee7bcb…cd021`; worktree file identical | PASS |
| Lane clean + pushed | `jj-lane.sh state` → `local=5949e66ffe remote=5949e66ffe ahead=0 behind=0`; `git status --porcelain` empty; `ls-remote origin refs/heads/master` = `5949e66ffe…` | PASS |
| Prompt carries template contract | seat re-check vs `templates/round-prompt.md`: all round-level + 5 child-lane items + §6 addendum present verbatim | PASS |
| Census | `scripts/sources-census.sh validate --root … kake` → exit 0 (12 W04 duplicate-url warnings, incl. new S127; warnings not failures) | PASS |
| Report is real, not a marker | all required sections with evidence pointers; claim declared, measured, verdict filed | PASS (not `failed`) |

Conformance defects (status-neutral, routed below): D1 row-count arithmetic wrong; D2 foreign-authored commit; D3 w2 settle line missing from dispatch log; D4 report T2 range mixes sources.

## Claim re-check — C1 (operability: runnable cost of the held round-41 URL rule)

Declared measured claim, one claim per the prefer-2 sizing rule. Predicate frozen as one sentence, identical in `c42_count_v3.py:71-73` and in every receipt's `predicate` field (byte-equal, verified with Python `==` over 9 receipts). Counter sha256 `ce2d5a0ca2c37…60acc` verified against committed bytes. What I re-measured myself vs what I evidence-verified (lane-owned gate/selftest — never executed, per PROTOCOL §Gate standard):

Re-measured (plain reads of committed receipts, `python3` JSON extraction):
- **Before** — `verification/v3probe/donothing-{1,2}.json` (round-41 tool at base): `met=false`, `equalRuns 10/10`, ratios T1 4.172/4.275, T2 2.732/2.831, T3 1.339/1.360, T4 1.239/1.190, T5 7.805/7.807. Matches report ("T1 4.17–4.28, T2 2.73–2.83, T5 7.81"). **Before = not met — confirmed.**
- **After (counter's own receipts)** — `verification/build/c1-v3-020bc457-{1,2,3}.json`: `met=true`, `equalRuns 10/10`, T1 1.058/1.006/0.976, T2 1.280/1.319/1.382, T3 1.396/1.390/1.427, T4 1.264/1.235/1.276, T5 1.168/1.093/1.096. Matches report. **After = met on the counter's own receipts — confirmed.**
- **Kill rule (2) firing** — `verification/w2v3/L1-*.json`: all four re-scored `met=true`, `equalRuns 10/10`, fresh seeds, max ratios 1.475 / 1.796 / 1.602 / 1.664 — the four witnessed live-seat controls (`MutBuildAuthority/M8-port-five-digits`, `CtlFreshCache/v1_casefold`, `v2_prefix32`, `v4_hosttable`). **Round verdict NOT MET — confirmed by my own measurement.**
- Control wave: `verification/w1v3/` holds exactly 86 receipts, exactly 3 met (`MutRegexPct__portpct`, `MutRegexStructure__mutant_empty_host`, `MutRegexStructure__mutant_port_letters`) — matches report.

Evidence-verified (committed evidence of lane-owned instruments, not executed):
- Counter lineage hashes v1 `7bfc32c5…`, v2 `01d3fb8d…`, v3 `ce2d5a0c…` match committed bytes; do-nothing control met draft 1 (`draft1/` receipt) before freeze, as §9 requires.
- H1 selftest tally `PASS 235/235` on build (py314 + py310 receipts) and round-41 tool; H2 real-run receipt committed (`verification/harm/realrun-020bc457.json`); H4 receipts at two seeds; kill-rule text frozen at `d1c3f372` (`git log -S` — unchanged through HEAD).
- Wave shape: w1 dispatch log 33 seats spawned/settled 0 dead 0 refused; w2 spec + 32 attack files; totals match the report's 67-seat two-v1-wave shape within the policy bands.

### Freeze-provenance weight (per claim-sizing rules — the closure's ruling)

Routed defect 1 / Mistake 6 is **substantive, not a recording lag**: wave-1 seats scored under v1 while v2 (`c23c145c`, 11:21Z) and v3 (`3490614`, 11:44Z) were committed mid-wave (wave 1 live 11:14Z→12:03Z); the instrument's evaluated population grew 8→9→10 runs and timing populations changed after scored evidence (e.g. `MutRegexPct__unicodedigit` met v1, fails v3's added run E). §6.9/claim-sizing freezes counter + kill rule + predicate **before any seat scores**; "before the build is scored" is a substitution, as the lane's own critic ruled (ATTACK SUPPORTED).

Weight: **fatal to any measured admission of C1.** The build's met ×3 cannot be admitted as a verified improvement; no post-hoc exploratory relabel is available (AXES.md requires the exploratory claim declared up front with a named non-author reviewer; the lane itself reported "not relabelled"). **The defect does not reverse the round's verdict**: the NOT MET result rests on four witnessed controls meeting the unchanged frozen v3 under the kill rule frozen at `d1c3f372`, with the predicate sentence identical in plan, counter and receipts; a provenance-tainted bar, if anything, makes the miss easier to believe, not harder. The negative verdict and all receipts stand.

### Per-axis verdicts

- **operability: unchanged** — the claimed improvement does not verify (C1 NOT MET); the round-41 tool stays unadmitted and round 41 stays rejected-harmed; no new harm introduced (H1–H5 hold with the scope qualifications the lane itself routed: H4 in-class only, H5 post-observation, CPU-only pricing).
- **freshness: unchanged** — S123/S124 re-opened by wave-2 seats, bytes equal to retentions (verified below); no drift found, no freshness claim made.

## Discernment spot-check (LEARNING.md — outside check)

Sampled 2 admits + 1 reject from `corpus/lessons/round-42.md ## Gate`; re-opened every source myself (live fetch + retained bytes under `.ufo/waves/round-42/sources/`, `SHA256SUMS`).

| Item | Lane decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S126 admit (supersedes S123) — Python `re` docs, possessive quantifiers | admit | https://docs.python.org/3/library/re.html — retained bytes sha256 `1559698e…8f17e2`; quote verified in retained text (HTML wraps the sentence across lines, hence single-line grep misses) and present in the live page (live sha `c1cece90…` — living-doc churn only) | **agree** | Quote "do not allow back-tracking when the expression following it fails to match" + "Added in version 3.11." verified; the correction (technique documented, build rejected — `8a30432d…` fails H5) is accurate and honestly scoped |
| S127 admit (supersedes S124) — RFC 9844 | admit | https://www.rfc-editor.org/rfc/rfc9844.txt — live sha256 `7585b9a9…4b135` **byte-equal to retention**; line 192 "This document completely obsoletes [RFC6874],"; lines 195–197 "reverts the change that it made to the URI syntax" | **agree** | Obsolescence and syntax-revert verified at the cited lines; the teaches cell's scope discipline ("does not itself single out non-ASCII/\|") is exactly right |
| S125/S128 reject — RFC 6874 | reject | https://www.rfc-editor.org/rfc/rfc6874.txt — live sha256 `5f54b04f…80d5` **byte-equal to retention**; lines 198–202 `ZoneID = 1*( unreserved / pct-encoded )` verified | **agree** | The grammar is real but the document is obsoleted by RFC 9844 (confirmed inside RFC 9844 itself); S128 adds the contract-required `flip:` clause; rejection with standing reason is correct taste |

All located quotes ≤ 25 words. Rule-2 hygiene: S123/S124 `used-by` old→new logged in the lesson; S117–S119 restored to `9e3c31d2` cells with superseding rows S120–S122. Census `validate` exit 0 at closure. **Outside spot-check agrees with the gate on all sampled admits and rejects → discernment trend supported.**

## Trend verdicts (integrator's)

- **expansion: unchanged** — no capability enters the SCORECARD table (C1 not met); registry growth is curation inside the existing SOURCES capability.
- **quality: improved** — weaker registry rows superseded by stronger ones this round (S126/S127/S128 correcting S123/S124/S125), round-41 rule-2 breaches restored with superseding rows, counter coverage gaps named with able-to-fail receipts (Mistake 5's fix criteria frozen for next round); no admitted entry was found false or stale and left unmarked. The failed C1 bounds the round's *axis* work, not the corpus-quality observables — that bound is carried by the verdict (rejected-honest-stop), not double-counted into a quality-harm. (The lane's "harmed-bound" is not a protocol verdict; this ruling and its evidence are the closure's.)
- **discernment: improved** — honest negative reported against the lane's own interest; four meeting controls self-reported with witnesses instead of relabelled; freeze-provenance defect disclosed, not repaired post hoc; and the outside spot-check above agrees with every sampled gate decision.

## Routed defects for the lane (next round) and notes for the operator

1. **Row arithmetic in report + SCORECARD is wrong (must fix).** Report/SCORECARD say "rows 128 → 131; mined +1 net of supersessions". Measured over committed bytes: base `1ef7a0e9` = **119** rows (mined 92 / queued 8 / rejected 19); tip `5949e66ffe` = **128** rows (mined 99 / queued 8 / rejected 21) → +9 rows (S120–S128), mined +7, rejected +2, queued unchanged. The census exit codes (before/after, both 0) are correct and committed; only the stated counts fail re-derivation. Next round: append a correction entry (never rewrite) and re-derive every registry count with the CORPUS.md census commands over committed bytes before filing.
2. **Freeze discipline**: freeze the counter before ANY seat scores (not before the build is scored). The Mistake-5 criteria (6+-digit ports, repetition classes) are the right next instrument — freeze them pre-dispatch.
3. **H4** stays qualified (in-class only) until measured out-of-class; either broaden the measurement or keep the clause qualified in SCORECARD.
4. **Recording gap**: `w2-dispatch-log.txt` carries the dispatch line but no settle line (w1's log has both); the 0-dead/0-refused claim for wave 2 is corroborated by 32 attack files + receipts but the log should carry its own settle record.
5. **Foreign-authored commit `5076e26`** (João Pedro Veiga `jpveigao10@gmail.com`, "considerthese: 2026-10-23 daily reflection", +38 lines at `considerthese/2026-10-23.md`) sits mid-range in lane history. Not round work, never cited. Operator: confirm it was your own push; if any seat wrote it, that is a lane-identity defect.
6. **Minor**: report's after-range "T2 1.28–1.72" mixes the L1 receipts (1.28–1.382) with wave-2 rerun maxima (1.720); keep per-source numbers distinct.
7. SHONEN: all four boxes remain `[ ]` in `SHONEN.md` (report lines are `[~]` author assertions; box 2 is honestly `[ ]` this round). If the operator wants promotion review, boxes 1–4 each need a named non-author verifier — promotion is operator-owned, not closure-owned.

Capabilities added: none. Promotions/mints: none.
