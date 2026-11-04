# Round 60 — verifier spot-check (kake)

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
lane repo: `/home/vgpnk/Projects/shokunin/kake-shokunin` (branch `master`, jj-colocated)
base `97cdc122379711c2b02a8970752c8782da3ac81d` → lane tip `437f53b1f6cd22dbf307f1187f41d1c0850a1ac2`; measured T1 `9f671056c6fb5ca49bc62ed4210745f620ed4cae`
report: `.ufo/reports/round-60/kake.md` (fleet commit `caddf63b740014c804beab71331fe3468f98583e`, author+committer `kake-shokunin <kake@shokunin.local>`; author date 04:55:20 -03:00 is the jj working-copy creation stamp, committer date 05:27:10 -03:00 lands after the lane tip 05:22:09 — lands-last holds)
watchdog digest: `2026-10-27T00:56:19-03:00 launch kake round=60 pgid=1453839 driver=hyaku-inline attempt=1` · `2026-10-27T04:49:13-03:00 lane-dead-no-report kake round=60; retry same round (hyaku-inline attempt=1: operator run wrap-up mid-round; in-flight state committed to lane for next-run inheritance)` · `2026-10-27T04:55:10-03:00 launch kake round=60 pgid=3050861 driver=hyaku-inline attempt=2` · `2026-10-27T05:30:45-03:00 complete kake round=60; hyaku-inline attempt=2`

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %cn %H' -- .ufo/reports/round-60/kake.md` | `kake-shokunin caddf63b…` (author+committer `kake-shokunin`) | pass |
| SHONEN heading, one line per box | read report | `## SHONEN` with 4 lines, all `[~]` + evidence pointers | pass |
| Cited commits exist | `git cat-file -t <hash>` × 12 | all present | pass |
| Ancestry vs branch (not `@{u}`; HEAD detached) | `git merge-base --is-ancestor 437f53b1 master` and `9f671056 master` | both ancestors of `master` | pass |
| No uncommitted round work; pushed | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain` | `ahead=0 behind=0 tracked=0 untracked=0`; clean | pass |
| Prompt carries template contract | read `.ufo/prompts/kake-round-60.md` | §§1–5 (mission/axes, 1–3 claims, frontier step, L2 floor, report contract with SHONEN heading + marker rule, commit/push scope, L0) + hyaku addendum §6 incl. inline-spawn handoff, 64–128 band, WAVE-DONE rule | pass |
| Report is a report, not a marker | content read | all required sections, evidence pointers, checkable commit hashes | pass |

No conformance defects. Attempt-1 termination (`lane-dead-no-report` at 04:49) is the run-9 operator wrap-up; attempt 2 inherited and named it in the report — handled per the earlier-attempts clause.

## 2. Per-claim re-check

Re-derivation policy: the three counters are lane-owned measurement scripts; per PROTOCOL §Gate standard (Closure consequence) their committed receipts were evidence-verified and their structural predicates re-measured with plain commands; the counters themselves were **not executed** by closure. Three independent reviewer seats (non-author, dispatched by closure) re-derived C1/C2/C3 in parallel; closure re-ran the load-bearing measurements itself.

### C1 — calibration: SKILL.md gate-registry labels of the 28 round 48–59 counters match observed exits

Reported: base `members=28 mismatches=14 scores_held=3/3 met=False` → T1 `members=28 mismatches=0 scores_held=3/3 met=True`.

Closure measurements:
- Population: `git ls-tree -r --name-only 9f671056 | grep -E '^\.ufo/waves/round-(4[89]|5[0-9])/(?:[a-z0-9-]+/)?c(4[89]|5[0-9])_[a-z0-9_]+\.py$'` (same N, contract regex) → **28** at base and T1 (c48×2, c49×2, c50×2, c51×2, c52×4, c53×1, c54×2, c55×2, c56×2, c57×3, c58×3, c59×3) — matches.
- Rows: SKILL.md registry tables (header `Name | Kind | Entry command`) — base has **12 population members with no row** (c48×2, c49×2, c50×2, c51×2, c52_gate_registry, c52_mutation_ladder, c54×2); T1 has **0 unregistered**. 12 rows added ✓. (c52_mutation_ladder had a base *mention* only inside another row's pinned-values cell — its Entry-command cell carries c52_wave_ledger.py, so per the contract row rule it was unregistered; the counter's reading is correct.)
- Relabels: c53_gate_truth → `never met` (Kind cell, SKILL.md §Round 60 ledger list); crawler-identity-quote-truth-counter (c59) → `historical` with pin `b322ccabe1628fc0cfe80c2dddca03ed154d1349`; ops-debt-counter (c54) → `historical` pin `a631cc0246b97f2a949d61186c7466468faf94d6`; receipt-pin-counter pin corrected `32754df7…` → `20217f23eca15862febe14545523832e21584106`. `git merge-base --is-ancestor` confirms all three pins are ancestors of T1.
- Scores: SCORECARD axis table at T1: operability 10, freshness 10, calibration 2 ✓.
- Receipts: `controls/base-c1-gate-status.txt` ends `members=28 mismatches=14 scores_held=3/3 met=False` `EXIT=1` (12 `unregistered` + c53 `live_not_green` + receipt-pin `historical_not_green_at_pin`); `controls/after-c1-gate-status-t1.txt` ends `members=28 mismatches=0 scores_held=3/3 met=True`. Red-before: `controls/redbefore-c1-score-mutant.txt` — scratch clone at `1ea30590` + one commit moving calibration 2→10 → `scores_held=2/3 met=False` `EXIT=1`, while the round-59 counter on the same mutant exits 0 (R59-D2 fixed, shown able to fail). Selftest receipt `c1-selftest-v3.txt` 84 PASS lines / `84/84` claim consistent.
- Independent reviewer seat: AGREE on all numbers; label distribution base→T1 12 unreg/9 live/7 historical → 17 live/10 historical/1 never-met matches both receipts line-by-line.

**C1: verified (structure re-measured; exits evidence-verified from receipts). Axis: improved.**

### C2 — operability: `scripts/append_guard.py` append-only correction guard, 24 frozen cases

Reported: base `0/24` exit 1 (no tool) → T1 `24/24 met=True` exit 0; selftest 54/54; real-lane `files=53 findings=0`.

Closure measurements + reviewer seat:
- `git cat-file -t 9f671056:scripts/append_guard.py` → blob (740 lines); absent at base (`fatal: path … exists on disk, but not in '97cdc122…'` — reads the index, not the worktree).
- Receipt `controls/after-c2-guard-cases-t1.txt`: 24 PASS lines (K1–K22, R1, R2), 0 FAIL, `C2 guard-cases 24/24 met=True`, `revision: 9f671056…`, `EXIT=0`; expected-exit column matches contract table (K20→2, K21→64, K22→1, R1→0, R2→1). Base receipt `base-c2-guard-cases.txt`: all 24 FAIL `absent at 97cdc1223797`, `EXIT=1`.
- Tool selftest receipt `c2-tool-selftest-v3.txt` byte-exact `append_guard selftest: 54/54`; committed `selftest()` counted to 54 cases.
- Real-lane receipt `after-guard-real-lane-t1.txt` byte-exact `files=53 findings=0`; independent count of `corpus/knowledge/**/*.md` blobs at the run's base `fd6303ce` = 53 (T1 = 57 = 53+4, no deletions). `fd6303ce` and `8001f8d5` are ancestors of T1.
- SCORECARD capabilities row present with pin `8001f8d5` (ancestor of T1).

**C2: verified (receipts evidence-verified; existence/counts re-measured). Axis: improved. Capability admitted.**

### C3 — freshness (sourced S427/S428/S429): S425 scope overstatement superseded; user-triggered robots.txt posture re-verified

Reported: base `0/9`, registry 164 → T1 `9/9 met=True`, registry 167.

Closure measurements + reviewer seat:
- Registry rows: `git show 97cdc122:corpus/SOURCES.md | grep -cE '^\| *S[0-9]+'` → **164**; at `9f671056` → **167**; diff is exactly +3 lines, S425 byte-identical at both revisions (pure append) ✓.
- S427 row: same URL as S425; `teaches` opens `supersedes S425 —`; scope narrows to the posture the page actually states (common + special-case crawlers) and records the page's silence on user-triggered fetchers. S428: the category page `google-user-triggered-fetchers` (later revision, `Last updated 2026-08-19 UTC`). S429: robots.txt introduction. All `mined`, opened 2026-10-27, tier A.
- S425 overstatement verified by closure: S425 scope cell claims "the three crawler categories and their robots.txt posture"; the retained S427 body gives a posture only for common crawlers ("They always respect robots.txt rules for automatic crawls.") and special-case crawlers (AdsBot example); the user-triggered fetchers cell carries no robots.txt clause — re-confirmed on a fresh live fetch (HTTP 200) 2026-10-27.
- Correction entry: `corpus/knowledge/googlebot-verification.md` carries a contiguous tagged insertion `**[r60-correction 2026-10-27]**` (diff `@@ -37,6 +37,12 @@`, append-only) recording that the earlier "ignore robots.txt rules" wording overreached and the later S428 revision prints "Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules." — verified verbatim on the retained and live S428 body.
- Receipts: `base-c3-quote-truth.txt` `0/9 met=False` `EXIT=1`; `after-c3-quote-truth-t1.txt` `9/9 met=True` `EXIT=0` at `revision: 9f671056…`; selftest receipt `c3-selftest-t1.txt` `140/140`.
- Retained sources: `sha256sum` of `sources/S427.html|S428.html|S429.html` matches `sources/receipts.json` exactly (d70ce6f5…/0f296b86…/423d99c5…).

**C3: verified (rows/diff re-measured; receipts evidence-verified; sources re-hashed). Axis: improved.**

### No axis harmed

`git diff 97cdc122 437f53b1 -- SCORECARD.md` = +23/−0 only: one capabilities row + the Round 60 claims table + prose; axis scores unchanged (10/10/2). LOG.md diff appends round-60 bullets only. No owned axis (operability, freshness, calibration, coverage, depth, adjacency) harmed.

### Exploratory claims

None — all three claims are measurable. No `unprovable` ruling needed.

## 3. Discernment spot-check (LEARNING.md — checked from outside)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S427 row (admit; re-open of S425 URL) | admit (lane) | live `curl` of `overview-google-crawlers` (HTTP 200, 74,481 B) + retained body | **agree** | Both Gate quotes are exact substrings of one collapsed text node, page-unique, on the live page and the retained body (sha256-verified); the page states a robots.txt posture only for common + special-case crawlers, so a superseding row with a narrowed scope is the honest registration; S425 left in place per append-only. |
| S428 row (admit; lane-found) | admit (lane) | live `curl` of `google-user-triggered-fetchers` (HTTP 200, 76,197 B) + retained body | **agree** | "these fetchers generally ignore robots.txt rules" and "it only covers the requestors that are more likely to show up in log files" both verify verbatim live and retained; tier A (operator's own page) is right. |
| S429 row (admit; assimilated S415) | admit (lane) | live `curl` of `robots/intro` (HTTP 200, 178,797 B) + retained body | **agree** | "The instructions in robots.txt files cannot enforce crawler behavior to your site" and the disallowed-but-indexed sentence both verify verbatim; the staged entry's 15 refused/rewritten staged sentences were seat-checked against this body and the refusal reasons (wrong anchor, absent attributions, meta-prose) re-verified by closure greps (0 occurrences). |
| staged `common-crawlers-japanese.md` (reject) | reject (lane) | live `curl` of `google-common-crawlers?hl=ja` (HTTP 200, 94,035 B) + EN edition | **agree** | Exact page sentence occurs once; the staged span as written (Markdown line-break space) occurs 0 times — not a page substring. Under the counter's exact `units()` (CJK regex incl. halfwidth) the sentence is **60 units > 25 ceiling** — closure reproduced 60 exactly. The flip (re-ground on EN) is sound: closure measured the EN counterpart at **22** units by the same rule (≤25; seat prose said 19 — see routed nits). Also the round's registry delta was contract-frozen at three rows. |
| `corpus/knowledge/robots-txt-limits.md` (theme admit) | admit (lane) | retained + live S429 body | **agree** | Every quoted span verified verbatim; the six wave-2 location-description fixes kept quotes byte-identical and only corrected attribution. |

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → **exit 0**, final line `kake ok …/corpus/SOURCES.md`; W04 count 15 including the expected S427-sharing-S425-URL-by-supersession warning — matches the report's `controls/census-after-t1.txt` (exit 0).

Gate sample: ≥1 admit and ≥1 reject re-opened (3 admits + 1 reject + 1 theme admit); every Gate quote ≤ 25 units and page-unique as claimed; all six quote strings closure-verified against committed retained bodies and live fetches.

## 4. Trend verdicts

- **expansion — improved.** Two knowledge entries on ground the coverage map did not hold (`google-user-triggered-fetchers.md` → S428, `robots-txt-limits.md` → S429), one new admitted capability (`append_guard.py`), registry 164 → 167 (closure-re-measured). No admitted entry failed its bar.
- **quality — improved.** A weaker row (S425 scope overstatement) superseded by an honestly-scoped re-open; an unqualified in-entry sentence corrected append-only with a tagged correction; 12 unregistered counters registered and wrong/stale labels re-derived from runs (C1); six quote-location attribution defects fixed without altering quoted spans; counter parsing tightened across v1→v3 with the loosenings named.
- **discernment — improved.** Closure (named non-author) agrees with every sampled gate decision, admits and rejects; staged-entry refusal reasons independently reproduced (counts and substring checks); four mistakes mined with captured-by and fix; honest stated limits recorded (below). A disagreement (the 19-vs-22 unit nit) is recorded here but does not change any gate decision.

## 5. Stated limits recorded for the operator

- **C1↔C3 causal coupling** (`w2/ConnW2Cross` revert tests): the claims are independently falsifiable by their own frozen counters at one measured revision but not isolation-separable at the build — C3's appended rows turn round-59's quote-truth counter red by design and C1 then requires the honest relabel. Mechanism recorded in contract §version 3 and the lesson. Per AXES.md's causal-separability rule this is an admission note for the operator to rule on; closure finds the disclosure honest and the claims each verified.
- **C3 predicate is quote truth, not semantic support** — named in the contract; a reviewer seat checked the corrected wording's qualifications.

## 6. Routed defects and nits for the next round

1. (nit, prose) Report/SCORECARD say "three relabels"; strictly it is 2 label-word relabels (c53 → never-met, c59 → historical) + 1 pin move (receipt-pin) + the ops-debt → historical relabel named in LOG — keep the count and the named rows consistent.
2. (nit, prose) `w1/ScoutRejectCommonJa.md` and the lesson Gate line call the EN counterpart quote "19" units/tokens; closure's measurement with the lane's own `units()` is **22** (≤25 — the flip stands). Correct the number in a later erratum.
3. (nit, receipts) `controls/after-c1-gate-status-t1.txt` carries no `# receipt:` header line unlike the base receipts; keep the header convention on T1 receipts.
4. (routing, operator) C1↔C3 causal coupling (§5) — operator rules on admission semantics; the mechanism is committed.
5. (routing, operator) Open L0 questions remain open and were routed around, not answered: round-58 quarantine-hold slice (12 rows hand-checked, held), round-59 calibration-ownership rows. Quarantine slice re-verified byte-identical by a w1 reviewer seat.
6. (note for operator, promotion-owned) SHONEN boxes are all `[~]` lane-asserted with resolvable pointers; each looks mechanically checkable by a non-author (SKILL.md tables/cited sources committed; counters re-derived and logged; selftests runnable; PROVINCE spot-read accurate — new ground is publisher-side robots.txt posture, lane-owned). Promotion is operator-owned; closure writes no `[x]`.

## 7. Closure verdict

All three claims verify (structure re-measured by closure and three independent reviewer seats; exits/tallies evidence-verified from committed receipts per §Gate standard Closure consequence); no axis harmed; discernment spot-check agrees with the gate on every sampled decision. **Admitted.**
