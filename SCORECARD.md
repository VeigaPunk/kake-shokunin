# kake-shokunin — Scorecard

Axes owned by this lane: **operability + freshness** (MISSION.md fleet-2;
depth/coverage/calibration/adjacency belong to other lanes — not scored here).

The numeric ratings below are legacy round-17/18 assessments, not a fresh
proof that the current corpus is clean. Round 20 is a blocked attempt;
its local per-axis evidence and admission limits are recorded at the end.
The round-20 resume (2026-10-19) section below records this round's three
claims; ratings stay at the 10/10 ceiling.

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| operability | 10 | Every free-read verb in the domain is now **live-executed on the real repo with a byte-level write-free proof**: r11 closed probe/status/reconcile/sync-check; r12 closed the last 4 (`status --json` exit 0 with 5 violated+1 error in snapshot; `grokbots --check` exit 1 lucario; `bots list` exit 0 20 keepers; `bots report` exit 1 gaps) — 31-file state sha guard identical before/after, re-verified by 2 independent L2 re-runs. Exit-1 predicates pinned to code (gaps `cli.mjs:935`, stale-only-with-flag `:836-839`/`:932`, checked=21 `:393`); replica edge matrix (corrupt/deleted snapshot, registry faults, `--stale` variants) landed. The automation layer is now runtime-verified, not unit-file-trusted: keeper timer never fired (enable-vs-retire at L0), scribe push-gate failing (N1), lucario registry gap at L0. Corrected cmdProbe merge patch replica-verified and staged for the webzites owner (`corpus/handoffs/cmdProbe-merge-fix.md` — r11 F1 guard refuted on the `probe <id> --all` edge). Full verb free-read/writer classification (35 rows) code-verified. | round 12 |
| freshness | 10 | **r17 HOLD 10:** the standing instrument caught a real between-sweep world change before prose repair: lowercase `~/projects` was consolidated into `~/Projects` and removed, making a cited descendant miss; cite corrected to the surviving canonical report, `pathsMissSet` 9→10. Full r16 inventory re-run: 160 claims (117/117 HOLD; 15/15 r16 stale repairs still correct; 7 carried UNVERIFIABLE; 21 HISTORICAL-OK) + 16/16 new claims HOLD; 9 new deltas found and resolved/qualified (W6 path+mtime/child rename, ETag edge flip, 2 r17 self-stale counts, inode wording, dangling `corpus/claims`, ledger locus, README range gloss). Instrument integrity also improved: `projectsChildrenSet` 36 informational set; `pathsFiles` count→39-entry evaluated list; bad pins now fail closed exit 2 with a permanent case (`--selftest` **10/10**). Final §paths = 66 targets / 49 resolve / 10 declared-absent / 0 drift / 39 files; 33-file state sha guard identical. Live exit 1 remains solely expected PQ-14 `plazir-live-source-gap`. Evidence: `corpus/knowledge/freshness-sweep.md` §r17, `corpus/lessons/round-17.md`, `LOG.md` r17, `/tmp/kake-r17/{scout-claims.md,claims-delta.tsv,critic.md,reviewer-cites.md,scout-pins.md,scout-live.md}`. | 17 |

## Planned

**Round 21** (two claims on the tied-lowest owned axes; counting commands
from the round-20 resume planner seat):

1. **freshness — knowledge-entry metadata.** Before: 4/21 knowledge entries
   open with `source:`/`verified-at:`/`recheck:` (the four r20 entries).
   After: 21/21, each field filled from the entry's own evidence. Count:
   `python3 -c 'from pathlib import Path; import re; fs=sorted(Path("corpus/knowledge").glob("*.md")); [print(k, sum(bool(re.search(r"(?m)^"+k+r":\s*\S", "\n".join(p.read_text().splitlines()[:8]))) for p in fs), "/", len(fs)) for k in ("source","verified-at","recheck")]'`
2. **operability — lesson gate coverage.** Before: 1/15 lane-authored
   round lessons carry a `## Gate` heading (round-20 only). After: every lane-authored lesson
   has an appended gate (candidates, admits/rejects with reasons, spot-check
   status), never rewriting history. Count:
   `ls corpus/lessons/round-*.md | grep -v aggregator | xargs grep -l '^## Gate' | wc -l`

Named checks needing an operator-authorized free read (not claims): each
Pages repo's `build_type` and action pins; whether `/CNAME` is served under
Actions; the user-site robots.txt.

### Superseded round-20 attempt plan (2026-10-15)

- **Round 20 remains unadmitted.** Freshness is the chosen LIVE axis (10/10
  tie with operability); no numeric rating or verified-round count advances.
  The effective host aliases do not meet the dispatch contract:
  `.ufo/round-20/routing-blocker.json`.
- **Host owner / integrator unblock:** supply the already-authorized
  content/audit/connector bindings and connector fallback, then dispatch the
  saved complete 32-scope wave in a fresh session. No new overlay or route
  mutation is authorized to this lane.
- **Kake unblock:** triage each location in
  `.ufo/round-20/citation-debt.json`, marking a historical recipe locally or
  verifying a surviving source. Do not re-pin to hide the red path gate.
- **Receipt unblock:** the current interactive mission has no queue task key
  or expected receipt bag in its selected wall metadata; the integrator must
  provide a real applicable binding. Sighting stays running/incomplete.

### Historical round-18/19 plan (not current measurements)

- **round 19 (pick at round open):** the round-18 re-census left three named
  debts, each with an explicit unblock: **PQ-2** (`~/Projects/ds4cc-marketplace`
  gone — restore the repo or declare the watch dead), **PQ-14**
  (`~/Projects/plazir-15-site` gone — same), **§history** (`SUSPENDED` on
  `probeHistoryAbsent` — needs a surviving `probe-history.jsonl` via
  `KAKE_PROBE_HISTORY` or a declared end of the probe-timer era). Bare run
  stays exit 1 until they resolve; that DRIFT is correct, not a regression.
- **W7 re-census done (r18).** `~/Projects` now holds 14 children;
  `ufo-fsd-alpha` is the only origin tree (`~/Projects/ufo-fsd-alpha`,
  HEAD `964f443e`). The corpus' `origin-work/*` cites are all marked
  absent-historical — do NOT resurrect them as live claims; a restored
  tree gets a fresh cite, not a marker removal.
- Live surfaces still reachable: PQ-12 (`EDIT-LANDED` — 2026-09-30 beat,
  `7c243a1d…`, now the pin), PQ-5 `PENDING` 404/`93ddca9a…`, ds4cc
  sitemap `PRE-PUSH` 404/9 379B. `fleet.config.json` is gone with the
  webzites tree, so PQ-12's pin rests on `pins.charterGhpPin` alone.
- W6 is now sourceable cleanup, not unexplained deletion:
  `~/DIRMAP.md:1,7,27` said lowercase children were absorbed into
  `~/Projects` then `~/projects` removed — DIRMAP itself is now gone in
  W7 (marked historical). Kagi r16's shifted kake round-1 citation stands
  reported upstream.
- Operator relay (r17): effective config shows `m_swe =
  devin/swe-2:max` but `retry.fallbackChains.m_swe = null`; the requested
  final/only Daybreak fallback is **not visible as an exact chain**. Do not
  force a failure or alter the frozen mission contract; if genuine m_swe
  capacity failure occurs, record whether runtime advances to Daybreak.

## Move log
| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 18 | freshness (**HOLD 10** — the gate caught W7 before repair) | r17 close: `~/Projects` = 36 pinned children; `webzites`, `ds4cc-marketplace`, `plazir-15-site`, `origin-work/*` all live; `pathsMissSet` 10; PQ-12 PERSIST on `2026-09-26 scribe beat`/`fb365e38…` | Sweep at round open (12:40Z) exited 2 with the biggest catch to date — W7 mega-prune: 33/36 children removed, 11 added; `webzites` + both gated repos + the `origin-work` tree + the probe/keeper systemd units + `~/DIRMAP.md` gone; `ufo-fsd-alpha` re-rooted at `~/Projects/ufo-fsd-alpha` (HEAD `964f443e`, no `.ufo/charter-scribe/ledger.jsonl`). Repairs: 63 cite lines in 22 files got inline `r18 re-census` errata (absent, historical — append-only); `pathsMissSet` 10→55, `projectsChildrenSet` 36→14 re-measured; PQ-12 re-baselined `2026-09-30 scribe beat`/`7c243a1d…` (live, measured); new `probeHistoryAbsent` pin → §history `SUSPENDED` not exit-2; selftest fixture re-anchored off the dead tree → **10/10**. Carried debt: PQ-2 + PQ-14 `ANOMALY` (repos gone — exit 1 stands, correct and loud) + §history suspended. | bare run → `VERDICT: DRIFT — §armed: PQ-2 ANOMALY, plazir-gate-anomaly (exit 1)` (carried debt); `--offline` → `VERDICT: OK (exit 0, partial)`; `--selftest` → `10/10 pass`; `corpus/lessons/round-18.md`; `/tmp/kake-r18/` (before.json/before.out/after.out/after-offline.out) |
| 17 | freshness (**HOLD 10**) | R16's standing gate was live, but `pathsFiles` was a bare count (`38`) so its array-only evaluator skipped the file-set delta; malformed pins degraded silently to defaults; zero-cite `~/Projects` child churn was invisible; and the 160-claim prose inventory had not been re-run. | The 03:20:19Z sweep caught W6 before repair: lowercase `~/projects` was consolidated into existing `~/Projects` and removed, breaking one descendant cite. Canonical cite repaired; miss set 9→10; P2b child set (36) added informationally; `pathsFiles` now the evaluated 39-entry list; malformed pins fail closed exit 2 + permanent test (`10/10`). Claim sweep re-ran all 160 + 16 new claims, surfaced 9 deltas, and every actionable corpus mismatch was repaired/qualified. Final offline gate: 66 targets / 49 resolve / 10 absent / 0 drift, file +0/-0, child MATCH; live gate exits 1 only for expected PQ-14; 33-file state guard identical. | `corpus/lessons/round-17.md`; `corpus/knowledge/{freshness-sweep.md,freshness-pins.json,publish-queue.md}`; `scripts/freshness-sweep.mjs`; `LOG.md` r17; `/tmp/kake-r17/{scout-claims.md,critic.md,reviewer-cites.md,scout-pins.md}` |
| 16 | freshness | Drift detection was an ad-hoc, **path-only** sample: r10's "60/60 resolve" froze and rotted, r15's sweep covered citations but not counts / verb-outcomes / journal shape / ETag / code-line pins; SCORECARD itself carried a now-false "0 kake citations for `bounties`" and an unsided "103 locs"; re-verification had no reproducible gate | Widened to **all quantified standing claims** and instrumented: `scripts/freshness-sweep.mjs` (3 sections, pinned baselines, exit 0/1/2/64, `--selftest` 9/9, byte-identical state guard) + `corpus/knowledge/freshness-pins.json`; first complete pass 160 claims → 117 HOLD / **15 STALE** / 7 UNVERIFIABLE (10 in never-swept classes), all 15 fixed or re-pinned; **caught `plazir15-ghp` 5-commits-ahead live/source drift** (live sitemap 8 locs vs source 7, `og:url` + canonical lag; stale-not-rot) → `drift-detection.md` claim corrected, **PQ-14** ledgered, instrument now gates it (exit 1); SCORECARD self-claim corrected; rules landed: pin the *set* not the count, dated samples are not standing claims | `scripts/freshness-sweep.mjs`; `corpus/knowledge/{freshness-sweep.md,freshness-pins.json}`; corpus fixes in 8 files; `corpus/lessons/round-16.md`; `/tmp/kake-r16/` (12 L2 artifacts); LOG.md r16 |
| 15 | freshness | Path-citation base trusted on r10's un-re-measured "60/60 resolve"; PQ-2 cell's "root content-frozen" ambiguous (mirror-vs-canonical misattribution in the r15 brief); canonical side described as "working-tree-only" when files ARE tracked-but-unpushed; normalization method for the mirror freeze metric not pinned; r14 plan-note asserted r15 opens post-sweep | 58 cited paths re-swept under the 09-28T23:51:31Z `~/Projects` drift window: 49 resolve, **5 genuine danglers caught** (ufofsdbeta + .ufo + ufofsdbeta-kimi-review vanished in-window; ephemeral/wz1 emptied 21:42-03:00) — all annotated with dated flags, per-round re-sweep rule landed; PQ-12 loop read `PERSIST` with all four non-PERSIST states evidence-excluded; PQ-5 armed-watch read PENDING (P1–P3 hold, E1 never fired); PQ-2 gate confirmed closed (remote `e6bd071`, 20 unpushed); PQ-2 cell + canonical wording + normalizer-variance corrections landed; sentinel 47/47 byte-identical across the round | corpus/knowledge/publish-queue.md §r15 + PQ-2 row erratum; SKILL.md FS-traps rule + 3 absent-annotations; mirror-pitfalls.md ×2; publish-channels.md ×1; LOG.md r15; `/tmp/kake-r15/` (12 L2 artifacts + sentinel sha pair + fetch bodies) |
| 14 | freshness | Standing claims carried stale precision: r13 "byte-frozen" root claim wrong at sha level (Cloudflare cfemail re-encoding); r13 `06:00:36Z` was the journal Starting line not the history `at`; ops-automation "earlier full sweeps" wording backwards; 10+ line-number citations drifted as source/docs grew; no armed verdict path for the pending PQ-5 publish; no dated re-check loop on the operator-gated PQ-12 pin | Sweep landed mid-round and verified (row 78 `at` 00:01:09.976Z, identical 12/5/1); sentinel PASS 45/47 unchanged (timer pair only); 18-curl replication 0-diff; PQ-5 watch armed (P1–P3 verified NOW + E1–E5 + F1–F3 branches — `publish-queue.md` §r14, `SKILL.md` step 4); PQ-12 loop armed and **caught a transition in-round** — scribe `9c28d29` pushed `pushed:true` at 00:06:19Z, live literal moved to `2026-09-29` (53,386B `fb365e38…`); 12 stale citations fixed across 4 corpus files + LOG + the r13 report; 2 new facts landed (generic-sentinel non-discrimination; canonical sitemap wire-absent); charter subpath audit NULL baseline landed; r13 report-filing gap repaired; score stays 8 — armed capability ≠ caught event (critic rule) | `/tmp/kake-r14/` (12 L2 artifacts incl. sentinel-{before,after}.sha), corpus/knowledge/{publish-queue,ops-automation,keeper-timer-inert,free-read-verbs}.md, SKILL.md step-4 watch wiring, LOG.md r14 |
| 13 | freshness | corpus aging: pin-failure framed as "two consecutive probes" (r3+r7); PQ-3 "behind 2", PQ-6 wrong line cite, PQ-5 zip "1 day stale", ops-automation header "76 rows"; "churn paused" unqualified; no at-vs-mtime rule; no absent-semantics rule; r12 commits missing in BOTH repos (round-11 was kake head; main head round-6) | Standing claims re-verified against live state 22:47–22:50Z (3 timer sweeps + manual re-probe identical 12/5/1; 18-curl replication 0-diff; PQ-5 pending, PQ-2 unchanged 19/93; pin-lag persists over deploy-current a8f1e2b); 4 stale citations fixed, 2 rules landed (at-vs-mtime; absent = exact-pin miss), 1 claim rescoped (churn-paused → scribe-automation-only); r12 protocol gap repaired (round-12 commits landed + pushed in both repos); score stays 8 — plan's trigger never materialized, no falsifiable move | `/tmp/kake-r13/` (10 L2 artifacts incl. sentinel-before.sha), corpus/knowledge/{publish-queue,ops-automation,keeper-timer-inert}.md, SKILL.md r13 amendments, LOG.md r13 |
| 19 | freshness | measured at HEAD (see lesson) | verdicts recorded per gate, no scalar | `corpus/lessons/round-19-recensus.md` |
| 20 (resume) | freshness (**HOLD 10**) | `--section=paths` exit 1: drift 7 targets / 26 unannotated locations, missSet 55, newMissing 0 | exit 0: drift 0, unannotated 0, missSet 55, newMissing 0; 26/26 annotations name target + dated event + non-executable wording | `.ufo/round-20/resume/{paths-before.txt,citation-disposition.json}`; `corpus/lessons/round-20.md` §Round-20 resume |
| 20 (resume) | operability (**HOLD 10**) | isolated selftest 14/14; region marks `B19,B1095,E1166,B1346,E1348,B1366,E1368`; planted out-of-region writes survive (cb807bc killed 0/25) | selftest 15/15 (new `e2`: 26/26 in-memory sites, 31/31 API names pinned, marker-error/anchoring/boundary fixtures); marks `B1154,E1225,B1515,E1517` (regions must open inside `selftest()`); working tree killed 25/25; post-land mutation probe 9/18 → all 8 re-run survivors killed; replay-proof PASS 7/7; child-process writes named residual | `.ufo/round-20/resume/{selftest-before.txt,confinement-before.txt,confinement-after.txt,confinement-reviewer-recipe.txt,confinement-mutation-probe.txt}` |

| 12 | operability | 4 of ~20 free-read verbs replica-verified only (r11 residual); automation layer trusted from unit files (r5 docs); r11 F1 patch proposal unchallenged; charter-ghp pin framed as "queued for keeper" since r7 | All 4 live-run on the real repo, exits 0/1/0/1, 31-file sha guard byte-identical (×3 runs incl. 2 independent L2 re-runs); automation layer runtime-verified: keeper timer never fired (logs frozen 09-21, 20/21 files, turn=never 17/21), scribe is the marker writer + its push-gate failing (3 beats), no fleet.config writer exists in src/ → PQ-12 relabeled operator edit; lucario = sole registry gap (grokbots --check exit 1); 18/21/20/21 universes pinned (url filter cli.mjs:75 by design); r11 F1 guard REFUTED on `probe <id> --all` edge, corrected patch replica-verified (18 rows preserved) → handoff filed; 35-row verb classification; keeper-timer + lucario + patch filed to L0; 2 wrong citations + 2 L1 count errors caught by reviewer/critic/scribe and fixed pre-landing | `corpus/knowledge/keeper-timer-inert.md`, `corpus/handoffs/cmdProbe-merge-fix.md`, `corpus/knowledge/free-read-verbs.md` r12 append, `corpus/lessons/round-12.md`, SKILL.md r12 amendments, LOG.md r12, `/tmp/kake-r12/` (9 L2 artifacts) |
| 11 | operability | 3 of ~20 free-read verbs never live-run (r10 audit); `probe <id>` recommended in SKILL.md drift table with no side-effect warning; `status` exit-1 documented as unconditional | All 4 core free-read verbs live-run on the real repo (probe ds4cc-com exit 0 + 18→1 clobber + restore; status clobbered/restored exits 0/1; reconcile 3 runs exit 0/0/1 fleet 7-attention; sync-check 6 runs incl. bare-fleet exit 1 {ok:3,attention:6}, --dead 0, unknown-id 1, unknown-verb 64); snapshot-clobber trap + 7 CLI behaviors + merge asymmetry landed in corpus + SKILL.md; 1 citation defect fixed | `corpus/knowledge/free-read-verbs.md`, SKILL.md r11 amendments, LOG.md r11, `/tmp/kake-r11/` (13 L2 artifacts: labrat-probe/reconcile/sync, scout-verbs, revenger-merge, critic, reviewer, sentinel, executor×2, planner, connector, scribe) |
| 10 | operability | 0 scripts in repo; alerting "undecided" (README gap since r5); checklist executability unmeasured; naive history diff = 42 events / 40 phantom | detector landed+verified (6 events/0 phantom on 76 rows; exit 2/64 proven); 33/33 cmds + 60/60 paths resolve; 2 CLI traps + 3 citation defects landed/fixed; r5 record corrected (03:32:06→04:14:50) | `scripts/probe-delta.mjs`, `corpus/knowledge/probe-delta-alerting.md`, LOG.md r10, /tmp/kake-r10/* lane reports |

## Retired

- **Free-read-verb audit (operability sub-surface): saturated r12.** Every
  read-only verb in the domain (`probe`/`status`/`grokbot reconcile`/
  `sync-check`/`status --json`/`grokbots --check`/`bots list`/`bots report`
  + code-classified `lease status`/`auth`/`help`/`kimi-surface plan`/
  `browser status`) is live- or code-proven with pinned exit contracts; the
  35-row classification covers the full dispatch surface. Further rounds
  re-audit only on drift (a webzites-source change or a new verb), not on
  schedule. The parent axis stays open: writer/metered verbs remain
  operator-gated, and L0 answers may add follow-up execution support.
- The two owned axes themselves are NOT retired (freshness has standing
  re-verification work; operability owns the landed scripts' upkeep).

## Round 20 attempt — local verdicts, not round admission

Baseline program: `20d13115323fba21bb3d63204cce13425feaf399`.
Candidate program SHA-256:
`816bbe688d54761930726c7196a6bf37ff3bc4bbdfbcd896ea7e1a5f4d1a6463`.
The source commit carrying that byte-identical program is cited by the
round report after landing. The measurements below grade the saved input
surface, not an unmeasured historical corpus.

| Owned axis | Verdict | Before → after evidence |
|---|---|---|
| freshness | improved locally; blocked/unadmitted | On the same measured candidate corpus, baseline program: exit 0, drift 0, declaredAbsent 55. Candidate: exit 1, drift 7 targets / 26 unannotated locations, declaredAbsent 48; newMissing 0. `.ufo/round-20/{same-surface-baseline,acceptance,citation-debt,measured-corpus-inputs}.json` record argv, full outputs and input hashes. `node .ufo/round-20/replay-proof.mjs` also proves the isolated false-green and unchanged controls. |
| operability | unchanged | Entry/exit contracts and publishing/history logic retained; isolated selftest `14/14`, frozen CLI proof passes. Normal path/offline gates remain usefully red, not suppressed. Full evidence: `.ufo/round-20/acceptance.json`. No online armed checks ran. |

No owned axis is observed harmed in the exercised paths. This is not Rust
judgment, a compliant specialist wave, or evidence of 100 completed rounds.
No new verified-round credit is claimed. Other expertise axes are outside
the lane's scored ownership and were not re-scored.

Learning trends: **expansion unchanged** (same domain ground, no new
knowledge frontier admitted); **quality improved locally** (false-green
rule corrected and historical runbook expectations explicitly qualified);
**discernment unchanged** (no independent non-author admit/reject spot-check).
All are provisional for a blocked round.

Exact local acceptance verdicts (2026-10-15; full argv/stdout/stderr/exits in
`.ufo/round-20/acceptance.json`):

```text
CITATION_LOCALITY_PROOF: PASS (cases=7, failures=0)
exit=0
selftest: 14/14 passed
exit=0
VERDICT: DRIFT — §paths: 7 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1)
exit=1
VERDICT: DRIFT — §paths: 7 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1, partial: offline)
exit=1
```

Named debt: host role/fallback bindings; per-location corpus annotations;
operator restore-or-retire decisions for source watches and history;
the previously reported static confinement-assertion weakness; independent
spot-check; applicable receipt binding. Unblocks are in the current plan,
`corpus/lessons/round-20.md`, and `.ufo/round-20/receipt-binding.json`.

Round-20 evidence-format erratum: the initial landing serialized controlled
fixture environment values. A follow-up redacts those values to shape-only
metadata/symbolic output and preserves verdicts/exits; see the LOG and
lesson's “shape-only evidence erratum” and
`.ufo/round-20/redaction-validation.json`. The initial commit remains a
recorded conformance defect in ancestry. Program/fixtures, local axis
measurements, blocked admission and zero round credit are unchanged.

## Round 20 resume — claims and verdicts (2026-10-19)

Same round, fresh session (`LOG.md:542`); base `cb807bc`; measured on the
round-20 resume commit (hash in the fleet report and LOG). Self-verdicts
pending non-author verification. The ratings stay 10/10: the ceiling cannot
rise, so each axis row reads HOLD with its measured move.

| Claim | Axis / type | Before → after | Counting command | Self-verdict |
|---|---|---|---|---|
| C1 citation-local debt cleared | freshness | §paths exit 1 → 0; drift 7 → 0; unannotated locations 26 → 0; missSet 55 → 55; newMissing 0 → 0 | `node scripts/freshness-sweep.mjs --section=paths` | improved (HOLD 10) |
| C2 confinement proof closed | operability | selftest 14/14 → 15/15; mutants killed 0/25 → 25/25 on the same 25 function sites; residual bypasses named (aliasing, bracket access, multi-line calls, child-process and metadata writes) | `HOME=$(mktemp -d) KAKE_SELFTEST_DIR=$(mktemp -d) node scripts/freshness-sweep.mjs --selftest; node .ufo/round-20/resume/confinement-mutants.mjs` | improved (HOLD 10) |
| C3 curated source registry | capability | SOURCES rows 0 → 18 (A=16, C=2; mined 14, queued 2, rejected 2); census defects 0; knowledge entries citing a mined row 0 → 4; superseded literals left uncorrected 9 → 0; appended correction tails 0 → 27 | contract v1 census (`.ufo/round-20/resume/sources-census.txt`); `sh .ufo/round-20/resume/old-strings.sh`; `grep -rnF '**[r20-correction' SKILL.md corpus \| wc -l` | capability entered; per-axis: freshness supported (no second freshness credit), operability unchanged |

No owned axis is observed harmed: replay-proof PASS, §paths output identical
between the base and new program on the same tree, offline/armed logic
untouched. Learning trends: expansion improved (4 knowledge entries on
coverage-map ground new to the lane, each citing a mined row); quality
improved (C1, C2, 27 source-backed correction tails); discernment improved
locally (2 rejected sources with flips, 8 scout observations held back,
7 criteria from mined mistakes) — outside spot-check still owed.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Curated source registry | Keeps a contract-v1 registry of opened, scope-tiered sources (with rejections and study paths) whose mined rows back knowledge entries and appended corrections; census commands verify its shape | `corpus/SOURCES.md`; census argv/output `.ufo/round-20/resume/sources-census.txt`; mined-row citation check in `corpus/lessons/round-20.md` §Round-20 resume | 20 (resume) |
| Offline static canonical preflight | Reads a version-1 manifest of local static HTML pages and reports, read-only and network-free, whether each page's explicit-head canonical link matches the publisher's declared expectedCanonical (clean / failed-policy / could-not-evaluate, stable finding ids, exits 0/1/2/64); no search-engine selection, rendering, headers or live-delivery claim | `scripts/canonical_audit.py`; `python3 .ufo/waves/round-22/measure.py --root . --revision b539cc17c25e5f42fe8803e2aa42b4574c4b44c6` → 32/32 (`.ufo/waves/round-22/measure-after-v2.json`); selftest 62/62 and replay per-case match in `.ufo/waves/round-22/postfix/` | 22 |
| GET snapshot + canonical receipt replay | Captures 12 named public surfaces read-only and replays the offline canonical policy on committed served bytes; distinguishes receipt completeness from clean policy and 404s; no rendered-DOM or publication approval | `scripts/live_snapshot.py`; `.ufo/waves/round-23/{live/,measure-c2-after-v2.json,evaluability.json}` measured at `5bef55b1464d7ccbff802edab400d138597a621c`; receipt coverage 12/12, policy outcomes 3 clean / 5 canonical_missing / 4 not-served | 23 |
| Offline project-site base-path audit | Reads a version-1 manifest of local built HTML pages with a declared base path and reports, read-only and network-free, each same-site reference (http and https on one host count as one site) that resolves outside that base path (clean / failed-policy / could-not-evaluate, exits 0/1/2/64); no live serving, redirect, rendered-DOM or CSS/JavaScript URL claim | `scripts/base_path_audit.py`; `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision d8cd2e45a903fb05e4f34179aae8a21095a83dbb` → 30/30 with all three constant gates rejected (`.ufo/waves/round-29/verification/c2-after-d8cd2e4.json`); committed selftest 45/45 (`verification/selftest-lane-final.json`); real-input run on the round-23 snapshots of three owned project sites: 3 pages, 114 references, 4 findings, all `<a href>` to other paths on the owner host (`.ufo/waves/round-29/real-input/out/summary.json`) | 29 |

Round-24 maintenance pointer for the existing replay capability:
`scripts/receipt_replay.py` supersedes the historical round23 readers for
new receipt validation. Its recorded controls stay17/17 and12/12 at
`faace82dcf50e1c563d437f2caecb77a9a865880`; strict malformed-field results
are in `.ufo/waves/round-24/implementation-suite.json`. First-working round
remains23; no new capability or independent round24 admission is inferred.

Rows enter only through a round that demonstrates the capability running
(`AXES.md` §Capabilities); none enter through this rollout.

Round-20 resume (2026-10-19): the registry row above entered in this round,
whose report carries the census run. The 2026-10-16 placeholder row
`| — none yet — | | | |` was a current-value cell and is replaced, not kept.

## Saturation

The lane's saturation line + stagnation window N are to be declared by the
lane on its next round per `AXES.md` §The stagnation nudge; not asserted by
this conformance change.

Declared in the round-20 resume (2026-10-19): **saturation line 10/10 on
both owned axes (operability, freshness); stagnation window N = 1 completed
lane round.** Both owned axes already sit at the line (legacy ratings), so the
nudge turns on whether a capability entered: one did this round (curated
source registry), so round 21 is **not** waived by the nudge; if round 21
adds no capability, round 22 should be a frontier/capability move.


## Post-review ruling — round 20

This supersedes the earlier broad self-verdicts, without erasing them:
C1 freshness **improved-bounded (HOLD 10), annotation only** — 26 originally
unannotated locations → 4 remain (22 cleared), 7 drift targets → 3; gate
exit remains 1 after preserving historical lines. MissSet 55 → 55; no source
restored. C2 operability holds on its tested API/site population; aliases,
bracket access, split calls, metadata/fd writes and child-process writes are
not covered. C3 capability entered (18 registry rows; UTC census exit 0).
Expansion is the registry capability and crawl-scope-per-host frontier
entry only; the other three new entries supersede covered ground.
Evidence: `corpus/lessons/round-20.md` §Post-review fixes;
`.ufo/round-20/resume/post-review-restoration.txt` and anchor proof.
The 9→0 literal and 27-tail metrics above apply to `02b6dd0` only, not this
append-only corrected layout. This is the same round, no new claim.

## Round 21 — measured publishing-corpus maintenance

Measured source commit: `df6196b022a7fe9ac9a88af1293dc377a8197652`.
Baseline: `5009ecaa1cce10b895617a585ddd3f7c7c923a84`.
This section supersedes the earlier planned counting recipes (whose lesson
glob included the protected verifier file). Scores remain at the legacy
ceiling; improved means a bounded evidenced move, not a numeric increase.

| Claim | Axis / score delta | Before → after | Counting command | Verdict / evidence |
|---|---|---|---|---|
| C1 discoverable historical provenance | freshness 10→10 (HOLD) | complete exact-lowercase trios 4/21→21/21 | `node .ufo/waves/round-21/measure.mjs --revision <commit>` with the baseline and measured commits above | improved-bounded; `.ufo/waves/round-21/measure-before.json`, `measure-after.json`; dates remain historical, not current web verification |
| C2 inspectable historical decision logs | operability 10→10 (HOLD) | fixed baseline lesson population 1/15→15/15; current population 16/16 including round-21 | same revision-bound command; use its explicit baseline list in `initial.json`, and report new round-21 separately | improved-bounded; corpus-contract after exit 0, isolated selftest 7/7, frozen baseline replay PASS; `.ufo/waves/round-21/{corpus-after,corpus-selftest,replay}.json` |

The contract gate's metadata matcher is intentionally more permissive than
the exact-lowercase independent claim counter. Both find four complete
baseline trios and twenty-one complete candidate trios. Neither proves source
truth, date honesty, safe domain execution or independent admission.
The structural gate enumerates existing regular Markdown files, skips
symlinks and excludes protected-role knowledge basenames; its empty-corpus
fixture is clean. The independent measurement pins the actual population and
would flag dropped entries. Its self-source confinement assertion is bounded,
not an exhaustive write/shell proof (`w1/Confinement.md` in round-21 evidence).

No owned-axis harm observed on exercised checks: the old paths gate remains
honestly red with three drift targets/four legacy citation locations,
newMissing 0 and missSet 55. Metadata prefixes preserve all prior bytes;
fourteen lesson gates are EOF additions. The helper's broad pointer census
has zero preservation violations; seventy-eight baseline-inapplicable
diagnostics concern only author wave-report references to newly added lines
or the new round-21 lesson, not changed historical lines. Their presence is
reported, not converted to an unqualified all-reference pass.

S019 is new scoped audit evidence; registry 18→19 rows, source validation
exit 0→0. No old source status/recheck/used-by cell changes. Expansion
unchanged; quality improved (bounded to discoverability and runnable rejection
of missing metadata/gates); discernment unchanged pending an independent
round-21 admit/reject spot-check. All dispatched seats are author-side.
The round-20 non-author admission and its limits remain authoritative via
`corpus/lessons/round-20-verifier-spotcheck.md`; older blocked/owed wording is
historical. This section records no new round admission by self-attestation.

### Planned — supersedes round-21 plan

Next steered round: a source-backed frontier/capability move in crawl/canonical
signals or static publishing validation, chosen from PROVINCE's open ground.
Round 21 enters no capabilities-table row; at the declared saturation line
and one-round stagnation window the nudge permits that move. Publishing,
restoration and remote property probes remain separately operator-gated.

## Round 22 — offline static canonical preflight (recovery attempt 2)

Measured commit: `b539cc17c25e5f42fe8803e2aa42b4574c4b44c6`. Baseline:
`7c61c8cc791bde36dd5e3688bdfea2678d90146c`. Attempt-1 integration `c0fd6d5`.
Scores remain at the legacy ceiling; C1 is a capability move on operability
(tied-lowest owned axis at the saturation line; also the stagnation-nudge move
planned above). Self-verdicts are author-side; admission belongs to the
non-author closure.

| Claim | Axis / score delta | Before → after | Counting command | Verdict / evidence |
|---|---|---|---|---|
| C1 offline static canonical preflight | operability 10→10 (HOLD), capability entered | frozen 32-case matrix accepted 0/32 (validator absent, instrument validated) → 32/32, numerator derived from per-case rows against the digest-pinned oracle | `python3 .ufo/waves/round-22/measure.py --root . --revision <commit>` (baseline adds `--cases-root .`) | improved (capability), author-side; `.ufo/waves/round-22/measure-before-v2.json`, `measure-after-v2.json` (2 identical runs each, same runner sha256 `fa916ada…`) |

Falsification integrated: wave 2 (43 of 64 seats reported) found a false
clean for `///path` references, usage output/repeat-option gaps, symlink
scope gaps and a counter that repeated its instrument's numerator; 8 residual
seats found 2 more (lexical `..`, self-consistent stub). All fixed before the
measured commit; `postfix/defect-probe` 2/8 → 8/8 and `postfix/counter-probe`
0/3 → 3/3 rejected show each fix can fail on the `c0fd6d5` bytes.
No owned-axis harm on exercised checks: paths gate red unchanged (3 targets,
missSet 55, no new miss); corpus-contract exit 0 (`final-suite.txt`).
Sources 27 → 29 rows (S028, S029; census exit 0 → 0). Expansion improved
(new canonical-signal ground + capability); quality improved (bounded to the
fixed defects); discernment improved locally (two mined mistakes with
fail-capable fixes) pending the non-author spot-check.

### Planned — supersedes round-22 plan

Next steered round: freshness-axis or second publishing capability move; candidate:
run the canonical preflight over an actual built artifact of an owned
property (read-only, operator-provided build) or add redirect/header-free
sitemap-vs-canonical consistency. Restore/retire and publishing stay operator-gated.

## Round 23 — current-surface re-verification and live canonical preflight

Base: `b5d599e19bead54b96f589444e9ec64cdf67c28a` (round-22 independently admitted).
Before measurement: `6847479d404d1dd93ecb59f99ff735bd7f010a4a`, which freezes
contract/populations/counters but changes no knowledge unit or served-page input.
After: `5bef55b1464d7ccbff802edab400d138597a621c`. Both counts use the same
final runner bytes, recorded by sha256 in the measurement receipts.

| Claim | Axis / score delta | Before → after | Counting command | Verdict / evidence |
|---|---|---|---|---|
| C1 live re-verification of historical knowledge + property map | freshness 10→10 (HOLD; tied-lowest owned axis) | valid current-round claim-level receipts and appended corrections 0/17 → 17/17 units; 176 selected claims (79 HOLD, 55 STALE corrected, 42 UNVERIFIABLE with reasons) | `python3 .ufo/waves/round-23/measure_c1.py --root . --revision <commit>` | improved, author-side; `measure-c1-{before,after}-v2.json` under round-23 waves; live truth rests on observations in seat reports, not structural acceptance alone |
| C2 first live-snapshot canonical preflight | operability 10→10 (HOLD) | reproducible receipt coverage 0/12 → 12/12; separate outcomes 3 clean / 5 canonical_missing / 4 not-served (404) | `python3 .ufo/waves/round-23/measure_c2.py --root . --revision <commit>` | improved, author-side; `measure-c2-{before,after}-v2.json`; same-byte diagnostic `evaluability.py --root . --before b539cc1 --after 1b309c93…`: evaluated served pages 4/8→8/8 (not a third claim) |

Controls can fail: counter selftest 28/28; canonical selftest 82/82; snapshot
integrity probe 2/11→11/11 (5e5afb9e vs final); relaxation probe 3/13→13/13
(4d95d2e vs final). Initial counter selftest killed 13/71 mutants and left
58 survivors; expanded coverage is not an exhaustive mutation-kill claim.

No observed harm on the previous evaluated population: corpus-contract exit 0,
old frozen canonical matrix 32/32. Paths remains red with the same three old
unannotated targets. Its expanded citation universe now has missSet 69 (old55),
14 additional targets explicitly checked/annotated absent; the old pin is
unchanged, and this new set-delta warning is disclosed, not rounded up to green
(`.ufo/waves/round-23/final-suite.json`). Restore/retire remains operator-owned.

Sources 29→31 (S030/S031); no old status/recheck/used-by cell changed. Expansion
improved (GET-capture/replay capability); quality improved (base/foreign parser
defects, snapshot integrity and source wording corrected); discernment improved
locally (mistakes and rejects falsified before correction), pending non-author
admission. Dead seats remain uncredited; report records their exact errors.

### Round-23 recovery evidence and next intent

The replacement coordinator reproduced both above before/after counts on
the same named revisions (`.ufo/waves/round-23/recovery-counts.json`), and
retained the original live timestamps, policy failures, UNVERIFIABLE reasons
and red paths result. Verification is bounded by
`recovery-verification.json`; author-side review does not close independent
admission. No axis rating, claim population or expected canonical was changed
in recovery.

Planned, for the next separately steered round only: one measured freshness
claim that reconciles the live canonical findings with the named operator
repair/handoff queue, or an operability capability on the remaining
publisher-side sitemap/canonical frontier. No restoration, publication,
account operation or new round is authorized by this plan.

Recovery clarification: the report's canonical discernment verdict is
**unchanged** pending independent admit/reject spot-check. Earlier
"improved locally" describes author-side mistake learning only, not the
outside-verification trend. The contentType follow-up changes the targeted
snapshot probe from the inherited 11-case proof to 12 cases: same expanded
probe red 11/12 before → green 12/12 after (`snapshot-field-*.json`).

Committed recovery measurement: `dd58390d3a0b2942ffdd8f0330c0da3dda7b87e1`,
using the same C1/C2 commands above, again yields 17/17 (exit 0) and 12/12
(exit 0); `.ufo/waves/round-23/recovery-final-counts.json`. Baseline remains
`6847479d404d1dd93ecb59f99ff735bd7f010a4a` (0/17 and 0/12, exit 1 each).


## Round 24 — reconciliation and strict receipt replay

Claims frozen in `.ufo/waves/round-24/contract.json`; `contract-amendment.json` supersedes the rejected suffix-edit plan. Base f7de3ab4e9f030a15a857a5a08631bd8e690f436; frozen-artifact measurement ab85dbdba4499f35f7dab9c9635b9b605679dbe5. Both owned axes tie at legacy10; the lowest-axis obligation is met. Numeric ratings stay10→10 (HOLD), not a fresh assertion of corpus-wide cleanliness.

| Claim | Axis / score delta | Frozen before | Counting command | Evidence / status |
|---|---|---|---|---|
| C1 current filesystem reconciliation | freshness 10→10 | accepted0/19, sweep exit1 | `python3 -B .ufo/waves/round-24/measure_c1.py --root . --revision <commit> --json` | `measure-c1-before.json`; after is recorded only on execution |
| C2 malformed receipt replay | operability 10→10 | correct81/130; reject61/110, accept20/20; exit1 | `python3 -B .ufo/waves/round-24/measure_c2.py --root . --revision <commit> --json` | `measure-c2-before.json`; population SHA256 16da1936f30e2e7bfa405d9b51dfc18ab686edbd9f1d36f65d76626b0cab7b8f |

The 130-case selection preserves candidate observations, rejects unrepresentable companion fixtures, and keeps accepted controls. It is not an exhaustive malformed-JSON proof. Original round-23 runners are historical evidence; the maintained replay is a successor, not a byte rewrite of those receipts or runners.

### Round-24 recovery record — local measurements, admission withheld

The implementation was pushed at `faace82dcf50e1c563d437f2caecb77a9a865880`.
Its original coordinator executed the after measurements before the provider
`cyber_policy` termination; the replacement audited their JSON, Git revisions
and identical counter digests without rerunning or rerouting the interrupted
falsify assignments. Evidence: `.ufo/waves/round-24/recovery/provenance-audit.json`.

| Claim | Axis / delta | Before → after on the frozen population | Measured revisions | Local verdict |
|---|---|---|---|---|
| C1 paths reconciliation | freshness 10→10 HOLD | accepted 0/19→19/19; paths exit 1→0; 12 observed misses added and 4 recovered tokens removed from the pin (55→63) | `ab85dbdba4499f35f7dab9c9635b9b605679dbe5` → `faace82dcf50e1c563d437f2caecb77a9a865880` using the C1 command above | improved-bounded, author-side; no source restored or retired by kake |
| C2 malformed-receipt replay | operability 10→10 HOLD | correct 81/130→130/130; rejection expectations 61/110→110/110; acceptance controls 20/20→20/20; command exit 1→0 | same revisions using the C2 command above | improved-bounded on this matrix, author-side; no universal schema or originating-network-truth claim |

The C1-only revision `3d07733b482f88c42cb008397188237c80e42b67`
already measures C1 19/19 while C2 remains 81/130. Counter source digests are
identical at all three revisions. This is causal separation, not independent
non-author admission.

**Admission/progression withheld:** wave1 has 55 completed reports of 72 seats;
wave2 spawned 64 but has zero completed report files. Its durable terminal
records show 62 aborted, one connector quota error and one interruption
without a final result. No dead seat was replaced. Two new documentary-only
recovery audits are not substitutes for the unfinished falsification.
`.ufo/waves/round-24/recovery/interruption-inventory.json` preserves the
provider error and all seat outcomes. No new capability-table row is claimed.

Sources 31→34 (A29→32, C2 unchanged); all original31 rows unchanged.
Source census exit0→0, with the final W04 warning that S033 reuses RFC9110
under a distinct scope. Expansion unchanged; quality improved-bounded from
the recorded local repairs; discernment unchanged pending an outside
admit/reject spot-check. Full-round no-harm is not independently established.

Planned: retain the policy-stop and seek operator/non-author disposition
of this same round's evidence. No next round or renewed falsify dispatch
is authorized by this entry; the L0 question begins “Policy-stop disposition”.

Documentary-audit qualification: retained sweep-selftest outputs are not
shape-only conformant (concrete temporary/home-resolved paths; override
shape omitted from argv). This is disclosed, not retroactively redacted or
counted as evidence of a fully recorded isolation environment.
`recovery/docs-audit.md` and the lesson's Documentary-audit dispositions
carry this conformance debt and exact-command/timestamp clarifications.

## Round 25 — declared publisher accessibility capability

C1 targets **operability**, one of the tied-lowest owned axes (legacy10).
Before branch tip: `6883f1d580d811f7c434d1db4642596362f822b1`.
Before: no WCAG2.2 A/AA publisher-review packet or packet inventory command.
Intended after:55 exact source-bound review cards and a runnable offline
inventory, all website outcomes explicitly not-assessed. Counting command:
`python3 -B .ufo/waves/round-25/measure.py --root . --revision <commit>`.
Score stays10→10 (HOLD); execution and revision-bound outcomes are appended
only after observation. Contract: `.ufo/waves/round-25/contract.json`.

This is sourced by S035 and the new
`corpus/knowledge/accessibility-review-packet.md` entry. A capability-table
row requires an observed working run, not this declaration. Neither card
coverage nor packet structure establishes WCAG conformance.

Round24's rejected honest-stop is not reopened: C1/C2 remain candidate debt,
their refused/interrupted probes are not repeated/rephrased/rerouted/replaced,
and the policy-stop L0 disposition remains open. A different role/provider
would not grant permission. Round25's explicit steer authorizes this separate
round only, not another round or publication.

### Round-25 measured outcome — supersedes the pending declaration

Measured source: `be362b7808ea2350a4340cfa2cfde481269037f4`.
Baseline: `6883f1d580d811f7c434d1db4642596362f822b1`.

| Claim | Axis / score delta | Before → after | Counting command | Verdict / evidence |
|---|---|---|---|---|
| C1 source-bound publisher accessibility preparation | operability10→10 HOLD | absent capability0/55, exit1 → reviewed packet55/55, exit0; every website result remains not-assessed | `python3 -B .ufo/waves/round-25/measure.py --root . --revision <commit>` with the baseline and measured source above | improved, bounded to preparation; `.ufo/waves/round-25/postfix-verification/{measure-before,measure-after}.json` |

### Capabilities acquired in round25

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Publisher WCAG2.2 A/AA review preparation | Runs an offline inventory of55 source-bound criterion cards with manual evidence needs, a concrete operator handoff and explicit no-website-assessment boundary; actual browser/AT evaluation stays separately authorized | `python3 -B scripts/accessibility_packet.py --root . --json`; source S035; `corpus/handoffs/accessibility-preparation.md`; postfix-verification/packet.json under round25 | 25 |

This is local exercised capability evidence, not independent admission or
website conformance. Postfix checks: unit16/16, focused CLI39/39,
counter11/11; corrected frozen replay clean and tampered snapshot exit2;
the same quote/pin oracle exits1 on retained before code and0 on repaired
code. Three local regression changes survive the old fixtures but fail the
new fixtures (coverage-proof.json). Every packet/measurement verdict keeps
websiteConformance=not-assessed; a selftest tally is not a website result.

First coordinator failures remain visible: source6cb08's focused35/36 and
counter8/9 were corrected by an explicit64-level local JSON profile, not
relabelled as passing. Full receipts and timestamps are in verification/
and postfix-verification/ under `.ufo/waves/round-25/`.

Freshness is unchanged as a scored axis; no new property freshness or old
round24 claim is admitted. Static evidence shows prior registered scripts,
pins and knowledge bytes unchanged and six historical instruction/log
prefixes preserved; old policy-interrupted gates/probes were not run.
Source registry34→35 (A32→33, C2 unchanged; mined30→31, queued2/rejected2
unchanged), prior34 rows identical, census exit0→0 with retained W04.

Learning self-verdicts: expansion improved (new WCAG preparation frontier
entry and working capability), quality improved on this packet/proof
surface, discernment unchanged pending separate non-author admit/reject
spot-check. SHONEN/rank and verified-round credit are not self-advanced.

Planned only if separately steered: freshness recheck of S035 at release
change and its source-bound packet instructions; actual property evaluation
requires operator-named scope and authorization. Round24 policy-stop
disposition remains open; no next round or renewed old probe starts here.

## Round 26 — declared source freshness claim

C1 targets **freshness** (tied-lowest owned axis, legacy 10; not worked in
round 25). Base: `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`. Before: 0/32
prior external SOURCES rows carry a round-26 live-source receipt. Intended
after: 32 rows decided against bytes re-fetched this round with row-specific
quotes, and every adjudicated STALE knowledge statement corrected append-only.
Counting command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.
Score stays 10→10 (HOLD); measured outcomes are appended only after execution.
Contract: `.ufo/waves/round-26/contract.json` plus `contract-amendment.json`.
Round-24 C1/C2 remain unadmitted debt; no stopped work is repeated.

### Round-26 measured outcome (replacement L1, 2026-10-21)

C1 freshness **verified author-side**: baseline `97404de4ff73d6c8a4f87385cf5fdf36dca7f006` 0/32 (exit 1,
`receipts_absent`) → first candidate `e28312b14b076584fedd696fae2a684e460bd11e` 32/32 (exit 0) →
landed implementation `b44daedc9658d86374f1c3e3cdfc3a6951d0bdf6` 32/32 (exit 0, HOLD 32,
UNVERIFIABLE rows 0, findings 0). Final counter ledger: 313 row-statement
units, 7 STALE corrections, 4 earlier STALE tags reclassified as precision
notes; 6 UNVERIFIABLE statement units disclosed separately.
Counting command unchanged: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.
Exact outputs: `.ufo/waves/round-26/verification/measure-before-final-counter.json`,
`measure-final.json`; selftest 24/24 exit 0, text selftest 74/74 exit 0.
Legacy score stays freshness 10→10; operability 10→10, no new capability
claimed. Quality maintenance is measured by the receipt delta, not a scalar
increment. Expansion unchanged; quality improved; discernment unchanged
pending the independent non-author closure. Round-24 debt remains separate.


## Round27 — frozen repair-first claims

C1 freshness (tied-lowest legacy10):41/57 citing pairs adjudicated→all frozen/discovered pairs decided, with grouped S001–S006 source-grounded this round. Count: `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <commit>`. C2 operability capability:0/16→16/16 frozen-r26 omissions detected, no false positives. Count: `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision <commit>`. Base83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba; contract.json/c2-oracle.json freeze expected outcomes before implementation. Source freshness score10→10, operability10→10; no numeric ceiling inflation. r26 author-side verify claim above is superseded by non-author rejected-honest-stop, corpus/lessons/round-26-verifier-spotcheck.md;313 units are not retroactively completed.

### Round27 strict acceptance correction (before candidate measurement)

The declared41/57 is **durable pair review coverage**, not fully supported
status for every carried statement. Frozen contract.json:10/13 still requires
all pairs HOLD/supported STALE and forbids counting UNVERIFIABLE decided.
The two carried partial-UNVERIFIABLE pairs (six units) remain explicit.
Stricter code separates reviewedPairs and decided; it must not print a clean
C1 merely because the review set is complete. No original target, expected
set or baseline file is rewritten. See strict-c1-disposition.json and LOG.
C1 remains unprovable if these units remain unresolved; no credit or score
increase is taken from review coverage alone. C2 is independently measured
against the unchanged frozen16-pair omission set.

Full-barrier erratum: the final carry audit found one additional S007
UNVERIFIABLE unit absent from the old ledger fields. Known uncertainty is
**7 units /3 pairs**, not the earlier six/two description; the raw old field
sum6 stays unchanged. Original review baseline41/57 and target are preserved.
Strict expected arithmetic is38/57→55/58, not a completed C1; actual outputs
must be measured separately. Raw313 is a mixed-convention ledger-field sum,
not the semantic unit denominator (`carry-errata.json`, CarryLedger report).

## Round27 measured outcome — author honest stop

Measured candidate: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`.
The arrow at line533 is the declared target, **not** an achieved result.

| Claim | Preserved before | Observed after | Author verdict |
|---|---|---|---|
| C1 freshness | Original41/57 durable reviews; later complete strict instrument gives38/57 status-decided, exit1. Original files/counter unchanged. |58/58 reviewed;55/58 status-decided,7 known unknown units/3 pairs, exit1; original57 plus one disclosed artifact obligation. | **unprovable** — frozen after-clause not met. |
| C2 operability | New gate absent at declarations be375d9:0/16 detected, exit1 (`c2-before.json`); old r26 counter failed to detect the16 omissions. | Exact16/16 with0 false positives, real29 fixtures/Git30 checks and4 killed mutants; full-interface cold failures also observed. | **unprovable at full claimed interface** — bounded numeric component verifies, not full admission. |

Commands remain `.ufo/waves/round-27/count_c1.py --root . --revision <commit>`
and `c2_count.py --root . --revision <commit>` with `python3 -B`.
Actual commands/stdout/exits: `verification/`; all source versions and replay
links: `counter-version-chain.json`. Current interpretation:
`current-interpretation.json`; unresolved failures: `unresolved-acceptance.json`.

Legacy ratings stay10→10; no new capability/repertoire entry, promotion or
verified-round credit is self-awarded. Original57 target/before, current58
obligations and carry erratum stay separate. Raw313 is a mixed field sum.

## Round 28 — declared claims (attempt 2, before implementation lands)

Base (pushed lane tip at round start): `22c1669c1fec83d1a0769de6b9ce686c75657e66`.
Stagnation nudge applies: both owned axes sit at the 10/10 saturation line and
no capability entered in rounds 26 or 27, so the lowest-axis rule is waived
and the round makes a repair move plus a frontier move.

| Claim | Axis | Before (at base) | Declared after | Counting command |
|---|---|---|---|---|
| C1 repair-first: round-27 routed defect 1 in `scripts/citing_set.py` (unusable input documents yield the contracted JSON report and exit 2; an absent or unreachable corpus surface does not return clean) | operability | 4/15 checks pass (0/11 defect checks, 4/4 controls) | 15/15 checks pass at the landed commit | `python3 -B .ufo/waves/round-28/c1_interface_count.py --root . --revision <commit>` |
| C2 frontier: field performance (Core Web Vitals thresholds and CrUX eligibility) enters held knowledge as `corpus/knowledge/field-performance-cwv.md`, grounded in four primary sources opened this round (S036 web.dev Web Vitals, S037 web.dev threshold definitions, S038 CrUX methodology, S039 CrUX API) | freshness | 0/4 declared rows meet every check | 4/4 declared rows meet every check at the landed commit | `python3 -B .ufo/waves/round-28/c2_source_count.py --root . --revision <commit>` |

The C1 counter exports `scripts/` from the named commit and builds its own
cases; its 4 controls (valid clean working tree, valid clean Git read, a real
omission staying failed, and the commit's own 29-case fixture runner) fail a
gate that refuses every input. The 11 defect checks are the round-27
`CLI-FIFO`, `JSON-PROTOCOL` depth and `CLI-SCOPE-FALSE-GREEN` failures named in
`.ufo/waves/round-27/unresolved-acceptance.json`. Duplicate-key and nonfinite
JSON profiles, identity-path spelling and retention boundaries are outside C1
and stay open. A miss on either declared value is an honest stop.

## Round 28 — measured results (attempt 3)

Axis ratings stay 10 → 10 (saturated; stagnation nudge recorded in the
declaration). No capability, rank or promotion is self-awarded; the
non-author closure decides admission.

| Claim | Axis | Before | After | Measured commit | Counting command | Evidence |
|---|---|---|---|---|---|---|
| C1 | operability | 4/15 at `22c1669c1fec83d1a0769de6b9ce686c75657e66` | 15/15 (11/11 defect, 4/4 control) | `b5d423fc02057f67a6f3a255808313ce40d29069`; re-measured 15/15 at `8ecbefe31b81462239c572fbe23d21404442a177`, `5a83d13b28024cef461c0ef497e28681684555ac` and `e73d48bbf20759fc7758afaebf841fa02e5cfbbf` | `python3 -B .ufo/waves/round-28/c1_interface_count.py --root . --revision <commit>` | `.ufo/waves/round-28/verification/c1-before-22c1669-a3.json`, `c1-after-b5d423f-a3.json`, `c1-after-8ecbefe.json`, `c1-after-5a83d13.json`, `c1-after-e73d48b.json` |
| C2 | freshness | 0/4 at `b5d423fc02057f67a6f3a255808313ce40d29069` | 4/4 | `e57f601bd0148bb7dce9052f0cade3fd11751375`; re-measured at the final lane commit named in the round report | `python3 -B .ufo/waves/round-28/c2_source_count.py --root . --revision <commit>` | `.ufo/waves/round-28/verification/c2-before-b5d423f-a3.json`, `c2-after-e57f601.json` |

Limits: the C1 counter checks finding ids, not reason codes (reason codes at
`e73d48b` are recorded in `c1-after-e73d48b.json`); the C2 counter checks
quote shape, not quote truth (quote truth was checked separately in
`residual/ReviewGateQuotes.md`). Open findings are listed in
`corpus/lessons/round-28.md`.

## Round 29 — declared claims (before implementation lands)

Base (pushed lane tip at round start): `fe1805cf32a7aadf4574637a3a8912354cee2c7b`.
Both owned axes sit at the 10/10 saturation line and round 28 entered no
capability, so the stagnation nudge applies: the round makes a frontier move
(freshness) and a capability move (operability). The frontier area is new:
project-site base paths (PROVINCE Frontier, "Jekyll/base-path build tooling"),
not the citing-set gate that rounds 27 and 28 worked.

| Claim | Axis | Before (at base) | Declared after | Counting command |
|---|---|---|---|---|
| C1 frontier: project-site base-path knowledge enters as `corpus/knowledge/pages-base-path.md`, grounded in four primary sources opened this round (S040 GitHub Docs About GitHub Pages, S041 Jekyll Docs GitHub Pages, S042 Jekyll Docs Liquid filters, S043 Vite Docs Deploying a Static Site) | freshness | 0/4 declared ids pass | 4/4 declared ids pass at the landed commit | `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision <commit>` |
| C2 capability: offline base-path audit `scripts/base_path_audit.py` (built HTML of a project site, declared base path, same-origin references that resolve outside it) | operability | 0/30 frozen matrix cases pass (tool absent) | 30/30 cases pass at the landed commit, with all three constant gates rejected | `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision <commit>` |

C1 passes an id only when the registry row is `mined` and opened 2026-10-22,
the entry cites the id below its metadata header, the lesson `## Gate` line
carries one quote of at most 25 words, and that quote is an exact substring of
the retained visible text whose sha256 matches the round's receipt (round-28
routed defect 3: quote truth, not quote shape). C2 compares exit code, verdict
and finding reason tuples (reason codes, not ids) on 30 cases: 7 controls, 14
defects, 8 input faults, 1 usage fault; the matrix file is digest-pinned in the
counter. At base the constant gates pass 7/30, 0/30 and 7/30, so each is
rejected. Evidence: `.ufo/waves/round-29/verification/c1-before-fe1805c.json`,
`c2-before-fe1805c.json`. A miss on either declared value is an honest stop.

Declaration notes (added before any after-measurement, from wave-1 critic
`CriticClaimSizing`; targets and counters unchanged): at 30/30 with the
constant gates rejected, C2 enters a SCORECARD Capabilities row in this round.
C1's 4/4 is necessary, not sufficient: the counter proves sourcing (row,
body cite, quote found in retained bytes), not that the entry's claims follow
from the quotes, so the closure should read the entry body. Counter blobs at
`d18bbf3`: `c1_quote_truth.py` 139ede1efbbfeed612201239a4244b43aeda855d,
`c2_matrix_count.py` 58dde0628c3e40a9794c93b03c3b9f6e665173fc,
`c2-matrix.json` 0687433ecd7cd14eb90287121f82a99074503b84; host Python 3.14.8.
S040's URL redirects to `…/what-is-github-pages` (receipt `finalUrl`).

## Round 29 — measured results

Axis ratings stay 10 → 10 (saturated; stagnation nudge recorded in the
declaration). One capability row enters (above, "Offline project-site
base-path audit"), as the declaration notes said it would at 30/30. No rank,
promotion or admission is self-awarded; the non-author closure decides.

| Claim | Axis | Before | After | Measured commit | Counting command | Evidence |
|---|---|---|---|---|---|---|
| C1 | freshness | 0/4 at `fe1805cf32a7aadf4574637a3a8912354cee2c7b` | 4/4 | `f8675e5a2aac9007ade31bf98813fcb1deee8093`; re-measured 4/4 at `98dbab2`, `7697990` and `d8cd2e45a903fb05e4f34179aae8a21095a83dbb` | `python3 -B .ufo/waves/round-29/c1_quote_truth.py --root . --revision <commit>` | `.ufo/waves/round-29/verification/c1-before-fe1805c.json`, `c1-after-f8675e5.json`, `c1-after-98dbab2.json`, `c1-after-d8cd2e4.json`; wave-2 `RerunC1Counter` |
| C2 | operability (capability) | 0/30 at `fe1805cf32a7aadf4574637a3a8912354cee2c7b` (constant gates 7/30, 0/30, 7/30) | 30/30 (control 7/7, defect 14/14, input 8/8, usage 1/1), constant gates 7/30, 0/30, 7/30, all rejected | `98dbab22ae93d325c9dcd791728c38ecf79ba0b6`; re-measured 30/30 at `7697990` and `d8cd2e45a903fb05e4f34179aae8a21095a83dbb` | `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision <commit>` | `.ufo/waves/round-29/verification/c2-before-fe1805c.json`, `c2-after-98dbab2.json`, `c2-after-d8cd2e4.json`; wave-2 `RerunC2Counter` |

The counters and the matrix are byte-identical from the declaration
(`d18bbf3`) to `d8cd2e4` (blobs listed in the declaration notes). Limits,
all found by wave-2 seats and recorded in `corpus/lessons/round-29.md`: C1
proves each quote sits in the retained text and the entry cites the id below
its header, not that each entry sentence follows from its quote (the entry
was corrected by hand after wave 2); C2 compares exit, verdict and finding
tuples (reason, element, attribute, value), not `id`, `page`, `resolved` or
the counts, and passes the usage case on exit code alone. On one point the
tool is wider than the frozen matrix wording: it treats http and https on one
host as one site (S040's `http(s)` row), which no matrix case exercises; the
tool help, docstring and entry state this. The committed selftest (45
fixtures) covers the families the matrix cannot see.

## Round 30 — declared claims (before implementation lands)

Base (pushed lane tip at round start): `035668132250b75b38d399e86e540b0a0371efbc`.
Both owned axes sit at the 10/10 saturation line, so the stagnation nudge
applies as in rounds 28 and 29: the round makes a repair move (operability)
and a frontier move (freshness). The repair works the citing-set gate, which
round 29 left alone; it is the debt routed by the round-28 and round-29
spot-checks (`corpus/lessons/round-29-verifier-spotcheck.md`, "Routed
defects", item 1). The frontier move takes Render static-site deploy
semantics, which `PROVINCE.md` lists as open Frontier ground.

| Claim | Axis | Before (at base) | Declared after | Counting command |
|---|---|---|---|---|
| C1 repair-first: the citing-set gate's reason codes are asserted by committed fixtures that its runner compares, and the round-27 failure families left open by round 28 are repaired in `scripts/citing_set.py` | operability | 0/14 checks pass (R01–R08 0/8, F01–F06 0/6) | 14/14 checks pass at the landed commit, with the 3 controls holding and both constant gates below 14 | `python3 -B .ufo/waves/round-30/c1_reason_count.py --root . --revision <commit>` |
| C2 frontier: Render static-site deploy semantics enter held knowledge as `corpus/knowledge/render-static-sites.md`, grounded in four primary sources opened this round (S049 Render Docs Static Sites, S050 Render Docs Redirects and Rewrites, S051 Render Docs Static Site Headers, S052 Render Docs Custom Domains) | freshness | 0/4 declared ids pass | 4/4 declared ids pass at the landed commit | `python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision <commit>` |

C1 checks. R01–R08 are the eight round-28 reason codes
(`document_not_regular_file`, `document_not_json`, `corpus_directory_missing`,
`corpus_empty`, `not_a_directory`, `population_id_unreachable`,
`revision_not_found`, `root_not_repository_top_level`). Each passes only when
a case the counter builds returns the full tuple (exit 2, verdict
`could-not-evaluate`, finding id `input_invalid` with that reason), a
committed `scripts/fixtures/citing-set/*/expected.json` names the finding as
`{"id": "input_invalid", "reason": <code>}`, and the committed runner exits 0
on the exported tree but non-zero once the code is renamed in the gate. At
base the behaviour holds and the other two parts fail. F01–F06 are the
round-27 families: duplicate JSON member names refused with reason
`document_duplicate_key` (plus fixture and rename conditions); NaN, Infinity
and -Infinity refused with reason `document_nonfinite_number` (plus fixture and
rename conditions); population ids such as `S01` or `S1` (fewer than three
digits, so the scanner never reads them) refused with
`population_id_unreachable`; each of the four valued options given twice
refused with exit 64; a corpus 1000 directories deep measured without a
traceback (exit 1, one `unadjudicated_citing_pair`); and a terminal device
opened as an input document refused without becoming the controlling
terminal (`O_NOCTTY`). Base evidence:
`.ufo/waves/round-30/verification/c1-before-0356681.json` (0/14; controls
3/3; constant-clean stub 0/14, refuse-everything stub 0/14; counter sha256
`be2a1287…c53e`, gate sha256 `d7e79ba1…9d48`, runner sha256 `3c167895…2a1c`).

C2 is the round-29 quote-truth counter with new ids and paths, and it names its
own sha256 in its output. An id passes only when its registry row is `mined`
and opened 2026-10-22, the entry cites the id below its 8-line metadata header,
the lesson `## Gate` line carries one quote of at most 25 words, and the quote
is a substring of the retained visible text whose sha256 matches
`.ufo/waves/round-30/sources/receipts.json`. The sources were opened at
2026-10-22T11:49Z, one GET each, by `.ufo/waves/round-30/fetch_sources.py`
(each receipt names the fetcher sha256). Base evidence:
`.ufo/waves/round-30/verification/c2-before-0356681.json` (0/4). C2 proves
sourcing, not that each entry sentence follows from its quote; the closure
should read the entry body. A miss on either declared value is an honest
stop.

Declaration notes (added before any after-measurement, from wave-1 seats
`CriticC1Counter`, `ReviewC1Before`, `CriticFamilyOutcomes`, `CriticC2Sizing`
and `CriticLearningClaim`; the declared targets and both declared counters are
unchanged):

- C1 strict supplement. Wave-1 critics built stub gates and runners that
  reach 14/14 on the declared counter without the declared property (a gate
  listing every code in one refusal; a runner comparing ids only while a
  separate source check names each code; repeats rejected only in the space
  form; F05 compared on the finding id only; F06 passed by a gate that never
  opens the device). The declared counter stays the measure. A second
  closure check, `.ufo/waves/round-30/c1_strict_checks.py`, must also pass
  at the landed commit: S1 exactly one finding per refusal; S2 the renamed
  gate emits `<code>_mutated`, the runner exits 1, and every committed
  fixture naming the code is among its failing cases; S3 repeats in every
  spelling (same usable value twice, `--name=value` twice, mixed, prefix
  abbreviation) exit 64 with the usage object; S4 the deep finding carries
  row S001 and the deep file path; S5 the terminal device is opened through
  `os.open` with `O_NOCTTY`; S6 duplicate keys and non-finite numbers
  (including `1e999`) refused in the ledger and inside row and pair objects.
  Base evidence `.ufo/waves/round-30/verification/c1-strict-before-0356681.json`:
  0/6, checker sha256 `96e7bbcd…500f`. A strict miss is reported with the
  declared result, not hidden by it.
- C2 closure checks. The C2 counter sha256 is `a2cd3164…5e7a`; the
  after-receipt must carry that hash and equal
  `git show <commit>:.ufo/waves/round-30/c2_quote_truth.py | sha256sum`. The
  retained sources must be unchanged since the declaration:
  `git diff --quiet 4580c78 <commit> -- .ufo/waves/round-30/sources/ .ufo/waves/round-30/fetch_sources.py`
  exits 0. Each registry row's URL must equal its receipt URL exactly.
- C2 counter limits disclosed. The citation check skips the first 8 lines of
  the entry; most lane entries carry a 3-line header, so the rule is stricter
  than "below the header", and the Render entry puts its first body citation
  of each id below line 8. Quotes are matched after whitespace collapse
  against the tag-stripped text, which keeps the site navigation, so a
  navigation string or a one-word quote would also pass; a wave-1 critic
  scored a hollow entry 4/4. The closure should read the entry body and match
  each quote to the sentence that relies on it.
- Scope. The lane's only Render property is the `app.ds4cc.com` Docker web
  service (`corpus/knowledge/publish-channels.md`); no owned property is a
  Render static site. C2 is platform knowledge for static sites; Render web
  service deploys stay open frontier.

## Round 30 — measured results

Axis ratings stay 10 → 10 (saturated; stagnation nudge recorded in the
declaration). No capability, rank or promotion is self-awarded; the non-author
closure decides admission.

| Claim | Axis | Before | After | Measured commits | Counting command | Evidence |
|---|---|---|---|---|---|---|
| C1 | operability | 0/14 at `0356681` (strict 0/6) | 14/14, controls 3/3, constant gates 0/14 and 0/14 (strict 6/6) | `71c6bfabd7aa957d15732d9224888bb32849238a`; re-measured 14/14 and 6/6 at `1c7773e68a041a5c9335d7f78223ed04bdabf779` and `f80bd8fabe51eb97c0211bfdef8d108ed0793aec` (after wave-2 runner repairs) | `python3 -B .ufo/waves/round-30/c1_reason_count.py --root . --revision <commit>` | `.ufo/waves/round-30/verification/c1-after-71c6bfa.json`, `c1-after-1c7773e.json`, `c1-after-f80bd8f.json`, `c1-strict-after-*.json` |
| C2 | freshness | 0/4 at `0356681` | 4/4, control not broken | `451e98fc8415edf10f41b2aad656318e7edc84ca`; re-measured 4/4 at `1c7773e` and `f80bd8f` | `python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision <commit>` | `.ufo/waves/round-30/verification/c2-after-451e98f.json`, `c2-after-1c7773e.json`, `c2-after-f80bd8f.json` |

Every receipt names the counter sha256 (C1 `be2a1287…c53e`, strict
`96e7bbcd…500f`, C2 `a2cd3164…5e7a`) and the measured revision; C1 receipts
also name the gate (`dbfade45…7f02`) and runner sha256 (`0fc87d5b…` at
`71c6bfa`, `9f2d1ecb…14d3` at `f80bd8f`).

Scope and limits (wave 2):
- C1 repairs the round-27 families round 28 routed (duplicate keys,
  non-finite numbers, short ids, repeated options) and two round-28 residual
  findings (deep corpus, `O_NOCTTY`). Still open: the round-27
  IDENTITY-PATHS, RETENTION-FRAGMENT, RETENTION-TRUST-BOUNDARY and
  C1-UNIT-OVERRIDE families, the socket `document_unreadable` label, and 12
  of 25 reason codes without a fixture (`CriticC1Scope`).
- The deep-corpus and `O_NOCTTY` repairs are guarded by the round counters
  only, not by committed fixtures; repeated options gained fixtures 42–45 in
  wave 2. The declared counter does not test abbreviations; the strict
  supplement does (`MutGateRepeatsWalkTty`).
- The strict supplement loads the declared counter from its own directory;
  the closure should check `declaredCounterSha256` equals `be2a1287…c53e`.
  Wave-2 `CriticStrictChecker` built stubs passing 6/6 through four holes
  (unchecked counter hash, S2 not requiring the other cases to pass, S3 no
  once-only control for `=value` and abbreviated spellings, S6 overflow at
  one depth only); the landed gate and runner are not such stubs, but the
  checker's verdict alone does not prove the property.
- Runner survivors (`MutRunnerCompare`): a runner that treats a missing
  reason as a wildcard, ignores the exit for object cases, or accepts mixed
  oracles still passes every instrument.
- The declared C2 closure command `git diff --quiet 4580c78 <commit> --
  .ufo/waves/round-30/sources/ …` exits 1 because `sources/screened/` was
  added; limited to the S049–S052 files, `receipts.json` and the fetcher it
  exits 0 (`RerunC2Counter`).
- Harms found by wave 2 and repaired before this record: the runner crashed
  on mixed-reason expectations and on an unwritable case copy
  (`ScoutNoHarmDiff`, fixed at `1c7773e`), and `case.json` setup could write
  outside `--tmpdir`, run fixture Git hooks, read outside the case and accept
  unbounded setups (`SentinelRunnerSetup`, fixed at `f80bd8f`; the sentinel's
  probes now each fail with a refusal reason).

## Round 31 — declared claims (before implementation lands)

Base (pushed lane tip at round start): `f1ffb81738c92c0537b99b30970143ab9419f990`.
Both owned axes sit at the 10/10 saturation line, so the stagnation nudge
applies as in rounds 28 to 30: one repair move (operability) and one frontier
move (freshness). The repair is the citing-set runner containment debt that
the round-30 closure routed (`corpus/lessons/round-30-verifier-spotcheck.md`,
"Routed defects", item 1); it is the only citing-set work this round. The
frontier move takes Render web services and the Blueprint file
(`render.yaml`), which `PROVINCE.md` (round-30 section) lists as open
Frontier ground, and checks the lane's own Render property file against it.

| Claim | Axis | Before (at base) | Declared after | Counting command |
|---|---|---|---|---|
| C1 repair: the citing-set fixture runner `scripts/citing_set_selftest.py` refuses the five hostile fixture shapes N1, N2, N3, N5 and N6 named in the round-30 routed defect 1, and each refusal has a committed hostile fixture checked by a committed hostile selftest | operability | 0/5 probes pass, control K1 holds | 5/5 probes pass at the landed commit, with control K1 holding | `python3 -B .ufo/waves/round-31/c1_sandbox_probes.py --root . --revision <commit>` |
| C2 frontier (learning claim): Render web-service and Blueprint semantics enter held knowledge as `corpus/knowledge/render-web-services.md`, grounded in four primary sources opened this round (S057 Render Docs Blueprint YAML Reference, S058 Render Docs Web Services, S059 Render Docs Docker on Render, S060 Render Docs Health Checks) | freshness | 0/4 declared ids pass | 4/4 declared ids pass at the landed commit | `python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision <commit>` |

C1 probes (read the counter docstring for the exact build of each). The
counter exports `scripts/` at the commit and runs the exported runner once
per probe over a scratch fixture directory holding a benign copy of fixture
`01-single-literal-clean` and the hostile case or cases. A probe passes only
when the runner exits 1 within 90 s, the benign case passes, every hostile
case is a failure, no harm is observed, and the commit carries a
`scripts/fixtures/citing-set-hostile/P<n>-*/` directory that the exported
`scripts/citing_set_hostile_selftest.py` reports as passed.

- P1 (N1): case `argv` `["--selftest"]`, `["--self"]` and `["--revision",
  "HEAD", "--selftest"]`; harm = a canary written by scripts planted in the
  case (`scripts/citing_set.py`, `scripts/citing_set_selftest.py`).
- P2 (N2): a case carrying a `.git` file that points at a victim repository,
  with setup `[git_commit]` and with setup `[mkdir]`; harm = the victim's
  HEAD, ref list or commit count changes.
- P3 (N3): setup `[git_commit]` with no `git_init`, the runner's `--tmpdir`
  inside a victim repository; harm as P2.
- P4 (N5): `expected.json` as a symlink to a matching expectation outside the
  case, padded past 1 MiB, and as a FIFO.
- P5 (N6): a symlinked case directory.
- Control K1: the exported runner over the committed fixture tree with
  `--min-cases 45` exits 0 with at least 45 cases.

Base evidence: `.ufo/waves/round-31/verification/c1-before-f1ffb81.json`
(0/5, K1 holds with 45 cases; counter sha256 `4707cebf…6d1a`, runner sha256
`9f2d1ecb…14d3`). At base each gap shows its harm: P1 writes the canary, P2
and P3 change the victim, P4 hangs on the FIFO until the 90 s limit, P5
exits 0.

C2 is the round-30 quote-truth counter with new ids and paths, and a quote
must now have 6 to 25 words (round-30 wave 1 showed a one-word quote could
pass). An id passes only when its registry row is `mined` and opened
2026-10-22, the entry cites the id below its first 8 lines, the lesson
`## Gate` line carries one quote of 6 to 25 words, and the quote is a
substring of the retained visible text whose sha256 matches
`.ufo/waves/round-31/sources/receipts.json`. The L1 opened the sources at
2026-10-22T15:41:23Z–15:41:29Z, one GET each, with
`.ufo/waves/round-31/fetch_sources.py` (sha256 `bc66ceb0…42c9`, named in each
receipt). The same fetch opened S061 (Render Docs, Configure Other DNS
Providers) for the round-30 routed defect 4; S061 is not a C2 id. Base
evidence: `.ufo/waves/round-31/verification/c2-before-f1ffb81.json` (0/4,
counter sha256 `de48d460…31b8`). C2 proves sourcing, not that each entry
sentence follows from its quote; the closure should read the entry body.

Closure checks, written so they can pass as written (round-30 routed defect 6):

- Counter identity: `git show <commit>:.ufo/waves/round-31/c1_sandbox_probes.py | sha256sum`
  and the same for `c2_quote_truth.py` equal `4707cebf…6d1a` and
  `de48d460…31b8`, and each after-receipt names that hash.
- Retained sources unchanged since this declaration:
  `git diff --quiet <declaration commit> <commit> -- .ufo/waves/round-31/sources/receipts.json .ufo/waves/round-31/sources/S057.txt .ufo/waves/round-31/sources/S058.txt .ufo/waves/round-31/sources/S059.txt .ufo/waves/round-31/sources/S060.txt .ufo/waves/round-31/sources/S061.txt .ufo/waves/round-31/fetch_sources.py`
  exits 0. Screened candidates are kept in `.ufo/waves/round-31/screened/`,
  outside that list.

A miss on either declared value is an honest stop.

Declaration notes (added before any C2 after-measurement, from wave-1 seats
`CriticC2Sizing`, `CriticRoutedDispositions` and `CriticLearningClaim`; the
declared targets and both declared counters are unchanged):

- C2 strict supplement. `CriticC2Sizing` built a hollow commit (sandbox
  `b6580c79`) that the declared C2 counter scores 4/4: quotes taken from page
  navigation or a code example, rows after the Registry table, an entry whose
  only body line is a comment. The declared counter stays the measure. A
  second closure check, `.ufo/waves/round-31/c2_strict_checks.py` (sha256
  `5111264f…46ad`), must also pass at the landed commit: S1 each Gate quote
  lies in the page body and in no other retained page, with at least 4
  lettered words; S2 each row lies inside `## Registry` with the receipt URL;
  S3 the entry, comments removed, has at least 2 lines per id that carry a
  verified 6-word or longer quote of that id; S4 the entry's render.yaml
  section names blob `d17ab7e5` and gives each key (type, runtime,
  dockerfilePath, dockerContext, healthCheckPath, envVars, sync) a line with
  a verified quote; S5 the retained `.html.gz` bodies and `.txt` files match
  the receipts and the text re-derives from the body. Before: 0/5 at
  `f1ffb81` and 1/5 (S5 only) at `c88b97e`
  (`.ufo/waves/round-31/verification/c2-strict-before-*.json`). The two
  sandbox commits of `CriticC2Sizing` score 1/5 and 2/5. A strict miss is
  reported with the declared result, not hidden by it.
- The `.html.gz` bodies are outside the declared no-change list
  (`CriticRoutedDispositions`); S5 covers them.
- C1 wave-1 attack seat `CriticC1Counter` ended on a provider cyber-policy
  refusal (its full text is in the round report); it produced no finding, and
  that item is not re-run under another route.

## Round 31 — measured results

Axis ratings stay 10 → 10 (saturated; stagnation nudge recorded in the
declaration). No capability, rank or promotion is self-awarded; the non-author
closure decides admission.

| Claim | Axis | Before | After | Measured commits | Counting command | Evidence |
|---|---|---|---|---|---|---|
| C1 | operability | 0/5 at `f1ffb81`, K1 holds | 5/5, K1 holds (45 cases) | `c88b97e6b02d85357b4b1e12d4bc09669ef82035`; re-measured 5/5 at `fde133ab48086bb9a06911b4ab045e2ad9086347` (no `scripts/` change between them) | `python3 -B .ufo/waves/round-31/c1_sandbox_probes.py --root . --revision <commit>` | `.ufo/waves/round-31/verification/c1-after-c88b97e.json`, `c1-after-fde133a.json`; hostile selftest `hostile-selftest-c88b97e.json` (exit 0) and `hostile-selftest-base-runner.json` (exit 1, 0/5) |
| C2 | freshness | 0/4 at `f1ffb81` | 4/4, control not broken | `fde133ab48086bb9a06911b4ab045e2ad9086347` | `python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision <commit>` | `.ufo/waves/round-31/verification/c2-after-fde133a.json` |
| C2 strict (closure supplement) | freshness | 0/5 at `f1ffb81`; 1/5 at `c88b97e` | 5/5 | `fde133ab48086bb9a06911b4ab045e2ad9086347` | `python3 -B .ufo/waves/round-31/c2_strict_checks.py --root . --revision <commit>` | `.ufo/waves/round-31/verification/c2-strict-after-fde133a.json` |

Every receipt names its counter sha256 (C1 `4707cebf…6d1a`, C2
`de48d460…31b8`, strict `5111264f…46ad`) and the measured revision; C1
receipts also name the runner sha256 (`5371530d…ce6c` after, `9f2d1ecb…14d3`
before). The declared C2 closure command passes as written
(`.ufo/waves/round-31/verification/closure-command-check.txt`).

Scope and limits:
- C1 covers the five routed shapes N1, N2, N3, N5 and N6, nothing more. Not
  repaired and named in `SKILL.md` "Citing-set runner containment — round
  31": option values in `argv` are not restricted; a setup `fifo` on
  `.gitattributes` can block `git add` until the case timeout; the gate's own
  Git calls have no timeout; dot-named entries in the fixture directory are
  still skipped; the round-27 families, the socket label, 12 unfixtured
  reason codes, the round-30 strict-checker holes and runner mutants m2, m4,
  m5 stay open.
- A wave-1 critic whose run ended after a provider safety filter switched its
  model (`w1/seat-status.json`) reported one more route (a fixture laid out
  as a bare Git repository read through `--revision`). It is recorded as
  advisory and unverified; the L1 did not reproduce or repair it.
- C2 proves sourcing and, through the strict supplement, quote location,
  per-id use in the entry and a render.yaml key section. It does not prove
  each sentence follows from its quote; the closure should read the entry
  body. Nothing about the live `app.ds4cc.com` service was observed.
- Wave 1 lost 18 of 33 seats at spawn (all executor, scribe and
  mutation-tester seats); the L1 authored every build artifact, so no
  non-author seat wrote any of them.

## Round 31 — attempt 2 re-measure and wave-2 repairs

Attempt 1 (L1 `KakeR31`) died in an omp process restart at 17:26Z after
pushing `92235a0`; attempt 2 (L1 `KakeR31a2`) inherited that tip and two
untracked paths (`.ufo/waves/round-31/census-after.txt`, byte-identical to a
fresh validate run, and `w2/swarm-registry.json`, an attempt-1 wave-2 registry
with no seat spawned). Both were committed at `9a7f5be`. Axis ratings stay
10 → 10; no capability, rank or promotion is self-awarded.

| Claim | Counting command | At `92235a0` (attempt-1 tip) | At `9a7f5be2b2091fc9b76adc803b8b442d5c292d08` (after wave-2 repairs) | Receipts |
|---|---|---|---|---|
| C1 | `python3 -B .ufo/waves/round-31/c1_sandbox_probes.py --root . --revision <commit>` | 5/5, K1 holds (runner `5371530d…`) | 5/5, K1 holds (runner `7c95a18e…8969`) | `verification/c1-a2-at-92235a0.json`, `c1-a2-at-9a7f5be.json` |
| C1 hostile selftest | `python3 -B scripts/citing_set_hostile_selftest.py --root <export> --tmpdir <dir> [--runner <base runner>]` | — | exit 0, 5/5; base runner exit 1, 0/5 | `verification/hostile-selftest-a2-at-9a7f5be.json`, `hostile-selftest-a2-base-runner.json` |
| C2 | `python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision <commit>` | 4/4 | 4/4, control not broken | `verification/c2-a2-at-92235a0.json`, `c2-a2-at-9a7f5be.json` |
| C2 strict | `python3 -B .ufo/waves/round-31/c2_strict_checks.py --root . --revision <commit>` | 5/5 | 5/5 | `verification/c2-strict-a2-at-92235a0.json`, `c2-strict-a2-at-9a7f5be.json` |

The 45 committed fixtures stay clean at `9a7f5be` (`verification/benign-a2-at-9a7f5be.json`).
Census mode before → after: rows 56 → 61, tier A 47 → 52, mined 43 → 48
(`census-mode-before-f1ffb81.txt`, `census-mode-after-a2.txt`).

Wave 2 (`kake-r31-a2-w2`, 36 seats) findings that changed committed bytes at
`9a7f5be` (each repair checked in `verification/a2-fixes/README.txt`):
dot-named symlinked cases now fail (spec P5 gained `.h5b`, which the `fde133a`
runner fails); the ambiguous `--r` is refused; a scratch path holding ":" is
refused; the hostile selftest holds a benign `h0-control` copy so a runner
that refuses cases by name fails it (the `c88b97e` selftest passed such a
sham); entry, SKILL, QUALITY, PROVINCE, README and SOURCES corrections are
appended, not rewritten.

Limits found by wave 2 and not repaired:
- The frozen C1 counter trusts the runner's reported failure names: a sham
  runner committed in place of the real one scores 5/5
  (`a2-w2/ReviewHostileSelftestCode.md` F1). The Git pins and several
  defence-in-depth checks are not probed by any spec
  (`a2-w2/CriticC1Wording.md`, `a2-w2/CriticHostileSpecsFit.md`).
- The C2 strict supplement certifies quote provenance, not truth: three
  constructed hollow or false commits score 5/5
  (`a2-w2/ReviewC2StrictChecker.md`). Wave-2 readers found the entry's
  claims supported except two inferences contradicted by the retained text
  (PORT at line 22, secret files at line 61) and two overbroad lines (23,
  67); all are corrected in the entry's appended section.
- Wave-1 record notes (`a2-w2/CriticSeatAccounting.md`): four wave-1 scouts
  finished after provider fallbacks (429, then 402) on the same model, and
  the wave-1 dispatch time was 15:54:35Z, not 15:54:40Z.
- Guard mutation (`a2-w2/MutRunnerGuards.md`): single-guard mutants m1, m2,
  m4, m5 are killed by the hostile selftest and the C1 counter; m3 (drop the
  "git_init before git_commit" check) survives, because the setup re-check
  and the `--git-dir`/`--work-tree` pin still refuse the shape. Only removing
  all three layers shows harm. No fixture pins that guard alone.

## Round 32 — declared claims (before implementation lands)

Base (pushed lane tip at round start): `a0b0dffcd95b2215f638a5ff7591dd4fde325d27`.
Both owned axes sit at the 10/10 saturation line, so the stagnation nudge
applies as in rounds 28 to 31. Both claims are routed repairs from the
round-31 closure (`corpus/lessons/round-31-verifier-spotcheck.md`, "Routed
defects"): C1 is item 2 (mutant m3), C2 is item 5 (the unretained external
`render.yaml`, blob `d17ab7e5`). Declared at 18:58Z, before either counting
command was run at any revision.

| Claim | Axis | Before (at base) | Declared after | Counting command |
|---|---|---|---|---|
| C1 repair: the round-31 surviving mutant m3 (delete the load-time `git_commit`-needs-earlier-`git_init` guard in `scripts/citing_set_selftest.py`) is killed by the committed hostile selftest, while the unmutated runner still passes it and the benign fixtures stay clean | operability | `killed` 0 (expected; round-31 MutRunnerGuards saw exit 0) | `killed` 1 with `guard_ok` true | `python3 -B .ufo/waves/round-32/c1_m3_probe.py --rev <rev>` (reads `killed`, `guard_ok`) |
| C2 repair (sourced): the two external ds4cc-marketplace blobs that `corpus/knowledge/render-web-services.md` reads offline at commit `1fbdb8ed` (`render.yaml` blob `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`, `apps-sdk/Dockerfile` blob `ee0b63819a9ce71e51469796541b9075e9676ae9`) are retained byte-identical in the lane, registered as a `SOURCES.md` row opened this round, and cited by that row id in the entry | freshness | 0/3 conditions | 3/3 conditions | `python3 -B .ufo/waves/round-32/c2_retained_count.py --rev <rev>` (reads `met`) |

C2 conditions, each counted over `git ls-tree`/`git show` bytes at the
revision only: (1) both blob ids appear in `git ls-tree -r <rev>` (byte
identity with the external blobs, so the retained copy is the read source, not
a paraphrase); (2) `corpus/SOURCES.md` `## Registry` holds a row whose source
cell names `ds4cc-marketplace` and `1fbdb8ed` and whose `opened` cell is
`2026-10-22`; (3) `corpus/knowledge/render-web-services.md` cites that row's
id at least once. Truth step (routed item 4): byte identity is checked by
blob id, not by quote matching.

Disclosed limits: C1 kills m3 by the refusal *reason* (the load-time message)
because m3 is otherwise behaviour-equivalent (the apply-time re-check and the
Git pins still refuse the shape); this trusts the runner's reported reason
text for that one case, the same shape as routed item 1, so the spec also
keeps the `h0-control` benign control. The Git-pin mutants m3d/m3f stay
unprobed alone; they are not claimed.

Correction (appended, round 32): the declaration above says "Declared at
18:58Z". That time was estimated, not read; the declaring commit `5b32cc7`
was made at 2026-10-22T18:54:19Z, before which the declaration was written
and no counting command had run. Lesson `corpus/lessons/round-32.md`
`## Mistakes`.
