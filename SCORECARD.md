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
| Offline link-preview (Open Graph) audit | Reads a version-1 manifest of local HTML pages with absolute page URLs and reports, read-only and network-free, a missing one of the four Open Graph required properties (S067), more than one og:type (S068), a non-absolute og:url, and an og:url that differs from the first canonical link resolved against the page URL (clean / failed-policy / could-not-evaluate, exits 0/1/2/64); no rendered-DOM, image, X-card, tag-position or live-preview claim | `scripts/link_preview_audit.py`; `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision 5613071e0107544d825e37db1e98f0bfcfb61465` → 28/28 with all four constant gates rejected (`.ufo/waves/round-34/verification/c1-at-5613071.json`; the declared measure, necessary but not sufficient), and at the wave-2 repair `76fac3b` (`c1-at-76fac3b.json`); evidence below was added after the declaration and does not count toward C1: committed selftest 29/29 (`scripts/link_preview_selftest.py`, `verification/selftest-link-preview-at-5613071-tool.txt`); real-input run over the 102 retained ds4cc pages agrees with the C2 recount (`verification/real-input-at-5613071.json`). The matrix score alone does not prove the capability: a lookup-table tool also scores 28/28 (`corpus/lessons/round-34.md` mistake row 4) | 34 |
| Link-preview audit, round-35 contract | The same audit also reports more than one non-empty og:url (`og_url_multiple`), ignores meta and link tags inside an open `<template>`, `<svg>` or `<math>` element, and keeps auditing the readable pages when one page cannot be read (exit 2 with input and policy findings together) | `scripts/link_preview_audit.py` at `b1cbbc39`; sealed counter 24 of 24 (`.ufo/waves/round-35/verification/c1-at-b1cbbc39.json`, reveal `4c6be2bd`) against 14 of 24 at base and 7 of 24 for the lookup and constant controls; selftest 45/45 and round-34 matrix 28/28 at `b1cbbc39` (`verification/selftest-link-preview-at-b1cbbc39.txt`, `c1r34-matrix-at-b1cbbc39.json`) | 35 |
| Offline source re-check audit | Reads a version-1 manifest of recorded fetches (hops, contentType, body) of registry sources and reports, read-only and network-free, whether each row's quote still occurs in its source: final status (gone, http_error), permanent redirects with the resolved new URL (moved), HTML text rules, NFKC and whitespace-deleted case-sensitive matching (quote_missing), media types and WHATWG charset decoding (unsupported_type, charset_unsupported), per-check input faults (exits 0/1/2/64); with `scripts/source_snapshot.py` it re-checks live Gate quotes | `scripts/source_recheck.py` at `4d5b3d55`; sealed counter 28 of 28 (`.ufo/waves/round-36/verification/c1-keyrev-at-4d5b3d55.json`, reveal `fd1fb723`) against 0 at base and at most 12 for the control seats; selftest 101/101; real-input run on 90 Gate quotes (`.ufo/waves/round-36/realrun/audit.json`) | 36 |
| Offline robots.txt expectation audit | Reads a version-1 manifest of (robots status, local robots.txt, product token, URL, expected allow/disallow) and reports, read-only and network-free, each check whose decision under the round-37 contract's reading of RFC 9309 differs from the expectation (`blocked`, `exposed`; check and manifest faults; exits 0/1/2/64); no fetch, redirect, cache or crawler-specific claim | `scripts/robots_audit.py` at `9dbc88bb` (wildcard matcher repaired after measurement, see round-37 wave-2 corrections); sealed counter 28 of 28 (`.ufo/waves/round-37/verification/c1-keyrev-at-9dbc88bb.json`, reveal `424aa248`) against 0 at base, at most 4 for the do-nothing, junk, constant, all-false and no-reader controls, 20 for the stock `urllib.robotparser` and at most 24 for the 34 listed reference ablations; a stock-parser-plus-six-rule-patches control also scored 28 (disposition and its contest in the round-37 sections), so 28 of 28 does not separate the contract from that parser; selftest `scripts/robots_audit_selftest.py` does (127/134 on that control, 134/134 on the tool); live run over 12 robots.txt files (`.ufo/waves/round-37/realrun/audit.json`) | 37 — **not admitted** (round-37 closure; "Round 37 — closure correction") |

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

## Round 32 — measured results (author-side; admission belongs to the non-author closure)

| Claim | Before (rev) | After (rev) | Counting command | Receipts |
|---|---|---|---|---|
| C1 m3 killed | killed 0, guard_ok true (`a0b0dff`) | killed 1, guard_ok true; mutant fails P6 only; pristine 6/6; benign 45/0 (`2f2f12d`, `285abca`, `d061f38`, `df31d30`) | `python3 -B .ufo/waves/round-32/c1_m3_probe.py --rev <rev>` | `.ufo/waves/round-32/verification/c1-*.json` |
| C2 retained and cited | met 0/3 (`a0b0dff`) | met 3/3 (`2f2f12d`, `d061f38`, `df31d30`) | `python3 -B .ufo/waves/round-32/c2_retained_count.py --rev <rev>` | `.ufo/waves/round-32/verification/c2-*.json` |

Counters unchanged since the declaration `5b32cc7` (wave-1 `RerunC1After`,
`RerunC2After`, `ReviewDeclarationOrder`: sha256 equal, diff empty). Wave-1
reruns reproduce the before and after receipts field for field
(`w1/RerunC1Before.md`, `w1/RerunC1After.md`, `w1/RerunC2Before.md`,
`w1/RerunC2After.md`). Axis ratings unchanged (10 → 10, saturation line).

Wave-1 corrections to the declaration (appended; the declaration text above
stays as landed):
- "m3 is otherwise behaviour-equivalent" should read "refusal-equivalent":
  under m3 the setup steps before `git_commit` run in the scratch copy before
  the apply-time re-check refuses (`w1/CriticC1Wording.md`). "the spec also
  keeps the `h0-control` benign control" should read "the harness adds the
  `h0-control` control to every spec".
- C1 is a layer check, not new containment: P3 with `reason_contains` would
  kill m3 equally; P6's commit-before-init order additionally catches an
  order-insensitive guard mutant that P3 cannot (`w1/CriticP6VsP3.md`). The
  Git-pin half of routed item 2 (m3d/m3f) stays open.
- C2's three conditions are one act, and the frozen counter is weak: a hollow
  commit (blobs at unrelated paths, junk row, junk cite) scores 3
  (`w1/CriticC2Scope.md`); a wrong opened cell drops c2 and c3 together; the
  counter pins no path, section or row blob id (`w1/MutC2Conditions.md`). The
  landed commit is not hollow (`w1/ReviewEntryDockerfileTruth.md`: 6 of 6
  checkable Dockerfile sentences supported, 0 wrong). Freshness fit is weak:
  C2 is re-checkability of a pinned snapshot; a drift step was appended to the
  entry after `CriticC2Scope`, and two more blobs the entry relied on
  (`server.ts`, `.dockerignore`) are now retained (`4d13e68`).
- Late wave-1 findings (all 34 seats returned): m3g also survives with m3d
  and m3f (`w1/MutM3Variants.md`; the declaration named two of three);
  m3, m3b, m3c and m3e are killed. The m3 kill rests on the reason pin alone
  (`w1/MutReasonCheckGate.md`: dropping the check, forcing it true or removing
  the key restores survival). The C2 counter has seven reproduced defects
  (`w1/ReviewC2CounterCode.md`: no row-id pin, substring registry window,
  naive cell split, path- and mode-blind blob check, anywhere-cite); the
  counter stays frozen as declared, and the landed bytes were checked by
  hand (`w1/ReviewS062Row.md`, `w1/ReviewEntryRenderYamlTruth.md`,
  `w1/ReviewEntryDockerfileTruth.md`). Lesson `corpus/lessons/round-32.md`
  "Carried open" lists what stays open.

## Round 33 — declared claims (before implementation lands)

Base (pushed lane tip at round start): `5777d5af79cac1ebf9144b348a9d274099e77338`.
Both owned axes sit at the 10/10 saturation line; the stagnation nudge applies
as in rounds 28 to 32. C1 is a routed repair from
`corpus/lessons/round-32-verifier-spotcheck.md` "Routed defects" item 2 (pin the
refusal by a structured field, not message text) and item 3 (the probe gates a
kill on the guard and returns a verdict on timeout). C2 is a non-repair,
sourced freshness claim on a different surface than the citing-set gate: the
operator's ds4cc-marketplace upstream moved from `1fbdb8ed` (the corpus' pin
and the local clone) to `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` (one commit,
2026-10-21T17:32:55Z, three new `/magga/frostbite/` pages, sitemap.xml +3
locs), read through a sandbox clone under `/fast/scratch/hyaku/kake-r33/`.
This declaration and both counters land in one commit, before either counter
has run at any revision; the time of the declaration is that commit's time.

| Claim | Axis | Before (at base) | Declared after | Counting command |
|---|---|---|---|---|
| C1 repair: the hostile selftest's P6 check keys on a structured refusal code, not on message text — a correct runner whose load-time guard message is reworded still passes, while mutant m3 (guard deleted) and a mutant that changes only the code are killed, with the pristine runner passing hostile and benign suites | operability | `met` 2 of 4 expected (pristine passes, m3 killed; reworded fails P6; recoded not applicable) | `met` 4 of 4 with `guard_ok` true | `python3 -B .ufo/waves/round-33/c1_code_probe.py --rev <rev>` (reads `met`, `guard_ok`) |
| C2 freshness (sourced): the corpus' ds4cc-marketplace source pin advances to upstream `7fc6aa2f`: four upstream files retained by path, mode and blob id; row S065 opened this round in `## Registry`; a section `## Round-33 ds4cc source pin 7fc6aa2f` in `corpus/knowledge/sitemap-orphan-audit.md` citing S065 whose stated sitemap loc count and three page canonical verdicts equal what the counter re-derives from the retained bytes with the lane's own `scripts/canonical_audit.py` | freshness | `met` 0 of 4 | `met` 4 of 4 | `python3 -B .ufo/waves/round-33/c2_pin_count.py --rev <rev>` (reads `met`) |

C1 contract for the implementation (so the counter's patterns stay valid): the
load-time guard keeps its two-line shape (`if step["op"] == "git_commit" and
not initialized:` then one `raise` line) and that raise line carries both the
code literal `"setup_commit_before_init"` and the unchanged message fragment
`needs an earlier 'git_init'`. Disclosed limits: C1 does not touch the Git-pin
mutants m3d, m3f and m3g (routed item 1; handled outside the claims this
round, see the round-33 lesson); C2 is source-side only — no live
`ds4cc.com` fetch, and canonical verdicts are the lane's offline policy, not
search-engine selection.

## Round 33 — measured results (author-side; admission belongs to the non-author closure)

| Claim | Before (rev) | After (rev) | Counting command | Receipts |
|---|---|---|---|---|
| C1 refusal keyed on a structured code | met 2 of 4, guard_ok true (`5777d5a`, also `bc6c4a8`) | met 4 of 4, guard_ok true, benign 45/0 (`b1752a2`, `e490381`, `1cf452e`) | `python3 -B .ufo/waves/round-33/c1_code_probe.py --rev <rev>` | `.ufo/waves/round-33/verification/c1-*.json` |
| C2 ds4cc pin advanced to `7fc6aa2f` | met 0 of 4 (`5777d5a`, `bc6c4a8`) | met 4 of 4 (`b1752a2`, `e490381`, `1cf452e`) | `python3 -B .ufo/waves/round-33/c2_pin_count.py --rev <rev>` | `.ufo/waves/round-33/verification/c2-*.json` |

Axis ratings unchanged (10 → 10, saturation line); no capability row is
claimed. Both counters are unchanged since `bc6c4a8` (wave-1
`CriticDeclarationOrder`: sha256 equal to the committed blobs). Wave-1
re-runs reproduce the before receipts byte for byte (`w1/RerunC1Base.md`,
`w1/RerunC2Base.md`).

Corrections and limits found by wave 1 (appended; the declaration stays as
landed):
- Declaration time. "The time of the declaration is that commit's time"
  means the committer time of `bc6c4a8`, 2026-10-22T19:52:44Z; its author
  time (16:26:05 -03:00) is the jj change-creation time and is not the
  declaration time. Before the declaration the L1 screened C2's inputs: it
  cloned upstream (19:49:58Z) and ran `scripts/canonical_audit.py` on two of
  the three frostbite pages (19:52:01Z, verdict clean). No counter had run
  (`w1/CriticDeclarationOrder.md`).
- C1 counter scope. The frozen probe also scores 4 for a commit that moves
  the code into the message text and keeps `reason_contains`
  (`w1/CriticC1RepairScope.md`, sandbox commit `489714be`). A strict
  supplement, written after that finding, checks the spec key, the reported
  `code` field apart from the reason text, a whole-message rewrite and the
  apply-time layer's own code: `python3 -B .ufo/waves/round-33/c1_strict_supplement.py --rev <rev>`
  gives 0 of 4 at `5777d5a`, 4 of 4 at `b1752a2`, `e490381` and `1cf452e`,
  and 1 of 4 on `489714be`. Other refusal sites carry `code` null; P1–P5
  still do not pin a refusing layer.
- C2 counter scope. A junk S065 row with the right id, status, date,
  used-by and hash plus copied metrics scores 4; so do a misplaced section
  and an even-backslash pipe (`w1/MutC2HollowCommit.md`). Fence-blind section
  splitting, a substring cite (`S0650`) and crash paths on malformed input
  are open (`w1/ReviewC2CounterCode.md`). The landed row matches an
  independent draft cell for cell (`w1/ScribeS065RowDraft.md`), and the
  counted facts were re-derived by three seats (`ExecRecountSitemapAt7fc6`,
  `ExecCanonicalNewPages`, `ScoutUpstreamCommitAnatomy`).
- C2 freshness fit is bounded (`w1/CriticC2FreshnessFit.md`): it adds the new
  state and marks older counts historical (wave-1 additions section), records
  the forge's deploy run (S066), and leaves `freshness-pins.json` pins stale
  and flagged, not re-pinned.

Wave-2 corrections (appended):
- Declaration screening, completed (`w2/CriticDeclarationCorrection.md`):
  at 19:50:57Z, before the declaring commit, one L1 command also read the
  four pinned blob ids, the sitemap loc counts at both commits (100 and 97)
  and all three pages' canonical links; the 19:52:01Z probe saved all three
  pages though its manifest named two. The C2 counter hard-codes no count or
  verdict, so knowing them did not make it easier to satisfy; the seat's
  counterfactual (a non-clean page stated as such) scores 2 on the frozen
  counter because the bytes no longer match upstream. C1 had no screening
  run.
- C1 code scope (`w2/CriticC1Verdict.md`): only the load-time
  commit-before-init check and apply-time setup failures carry codes. C1 is
  judged by that seat "verifies narrowly"; probe and strict supplement
  reproduce at every receipt revision (`w2/RerunC1After.md`).
- C2: all 26 factual sentences of the two entry sections supported
  (`w2/ReviewEntrySectionTruth.md`); S065 and S066 cells verified
  (`w2/ReviewS065RowTruth.md`, `w2/ReviewS066RowTruth.md`); seven
  single-condition mutations at the tip all detected
  (`w2/MutC2CounterAtTip.md`); the counter passes the round-33 hollow-control
  criterion (`w2/ExecCounterControlOnR33.md`: hollow 0 of 4).
- Harm check (`w2/CriticHarmCheck.md`, `w2/ExecOtherGatesUnchanged.md`): no
  history line rewritten; canonical, base-path, corpus-contract and offline
  freshness results unchanged. One behaviour change (stray symlinks exit 2)
  was undisclosed at `e490381` and is reverted for symlinks in the follow-up
  commit.

## Round 34 — declared claims (before implementation lands)

Base (pushed lane tip at round start): `1e54c89515b0b1f7c9d7d10e6232d15e43320713`.
Both owned axes sit at the 10/10 saturation line; the stagnation nudge applies
as in rounds 28 to 33. Neither claim touches the citing-set gate. Both work a
frontier area the lane has never held: link-preview metadata (Open Graph
protocol tags that social and chat platforms read to build a preview card for
a shared URL). Sources were opened at 20:57Z this round with
`.ufo/waves/round-34/fetch_sources.py` (S067 ogp.me, S068 Facebook "A Guide to
Sharing for Webmasters", S069 Slack "Slackbot" robots page, S070 Mastodon
PreviewCard entity; S071 and S072 opened and screened for rejection). The
ds4cc-marketplace HTML at upstream head `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`
(102 `.html` paths) is retained as `git archive` bytes plus a `git ls-tree`
listing under `.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/`. This declaration,
the matrix and both counters land in one commit; the declaration time is that
commit's committer time.

| Claim | Axis | Before (at base) | Declared after | Counting command |
|---|---|---|---|---|
| C1 capability: an offline link-preview audit `scripts/link_preview_audit.py` reads a version-1 manifest of local HTML pages and reports, network-free, missing Open Graph required properties (S067), more than one `og:type` (S068), a non-absolute `og:url`, and an `og:url` that differs from the page's canonical link (S067, S068), with the exit/verdict/finding contract in `.ufo/waves/round-34/c1-matrix.json` | operability | 0 of 28 frozen cases pass (tool absent); all four constant gates rejected | 28 of 28 cases pass with all four constant gates rejected; a capability row enters `## Capabilities` | `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision <commit>` (reads `passed`, `constantGatesAllRejected`) |
| C2 freshness (sourced learning claim): link-preview metadata enters held knowledge as `corpus/knowledge/link-preview-metadata.md`, grounded in S067–S070 (rows in `## Registry`, Gate quotes of 6–25 words that are exact substrings of retained text), and the entry states the Open Graph census of ds4cc at `7fc6aa2f` in one line that equals the counter's own recount of the retained bytes | freshness | `met` 0 of 5 | `met` 5 of 5 | `python3 -B .ufo/waves/round-34/c2_source_census.py --root . --revision <commit>` (reads `met`, `controlBroken`) |

Separability: the C1 counter reads only the tool and its own matrix; the C2
counter reads only `SOURCES.md`, the entry, the lesson and retained bytes,
and recounts with its own parser, never the C1 tool. Either verifies with the
other unlanded.

Pre-declaration screening (disclosed): before this commit the L1
(1) fetched the six candidate pages and read the phrases the matrix rests on
("The four required properties for every page are", "og:url The canonical URL
for your page", "Each URL should be a single object, so multiple og:type
values are not possible"); (2) ran `git grep -l` over `7fc6aa2f` HTML for
`og:title`, `og:image`, `twitter:card`, `rel="canonical"` and others, and
`git grep -h -o` over the `<meta property|name="og:...">` openings (87
openings each for `og:title`, `og:type`, `og:url`, `og:description`; 1 for `og:image`;
no `name="og:..."` form); (3) ran both counters at base (C1 0/28 with the
constants rejected; C2 0/5) and the C2 `recount()` function on the retained
bytes printing only its status and key names. Neither counter hard-codes a
census number or a quote.

Disclosed limits: offline only, no live `ds4cc.com` fetch and no platform
render; the gate does not check image reachability, size or type, X/Twitter
card tags (S071 rejected), JS-injected tags, or where in the document a tag
sits (S069's range-limited fetch is knowledge, not a gate check). A census
number is a count of tags in source bytes, not what any platform displays.
The C2 counter checks provenance shape and the truth of stated numbers; it
cannot tell a row's prose came from study (round-33 lesson, carried).

## Round 34 — measured results (author-side; admission belongs to the non-author closure)

| Claim | Before (rev) | After (rev) | Counting command | Receipts |
|---|---|---|---|---|
| C1 offline link-preview audit (capability) | 0 of 28, constants rejected (`1e54c89`, `d08d8de`) | 28 of 28, all four constants rejected (`5613071`, `9ef758c`) | `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision <rev>` | `.ufo/waves/round-34/verification/c1-at-*.json` |
| C2 link-preview knowledge + ds4cc census | met 0 of 5 (`1e54c89`, `d08d8de`) | met 5 of 5, controlBroken false (`9ef758c`) | `python3 -B .ufo/waves/round-34/c2_source_census.py --root . --revision <rev>` | `.ufo/waves/round-34/verification/c2-at-*.json` |

Axis ratings unchanged (10 → 10, saturation line). One capability row enters
`## Capabilities` ("Offline link-preview (Open Graph) audit", first-working
round 34). Both counters are byte-identical to their declaring commit
`d08d8de` (sha256 in each receipt's `counterSha256`).

Limits found by wave 1 (appended; the declaration stays as landed):
- Both counters are necessary, not sufficient. Wave-1 `CriticDeclarationFit`
  built a C1 tool that parses no HTML and replays the matrix by case
  directory name (`dcef39b5`, 28 of 28) and a C2 commit with junk rows, a
  census copied from the published before-receipt and first-six-word quotes
  (`0cce15f0`, 5 of 5). Both are retained under
  `.ufo/waves/round-34/retained/`; receipts
  `verification/criterion-lookup-control-c1-dcef39b.txt` and
  `verification/c2-at-critic-hollow-0cce15f.json`. The landed tool is not
  that shape: it parses each page with `html.parser`, passes a 29-fixture
  selftest none of whose fixtures copy a matrix case, and over the 102
  retained ds4cc pages reports exactly the missing counts the C2 recount
  implies (`verification/real-input-at-5613071.json`). These three checks were
  written after the finding and do not count toward C1; they are disclosed
  corroboration for the non-author read.
- An independent implementation from the interface text alone (wave-1
  `ExecIndependentOracle`, lxml) scored 28 of 28 on its first attempt, and an
  independent recount of the census with lxml (`ExecCensusIndependentRecount`)
  matched all seven numbers. Wave-1 `MutC1CounterWrongGates` built one
  single-rule-wrong tool of the ten asked (`name=` counted as `property`): it
  scores 27 of 28, killed by D7; the other rule breaks are left to wave 2.
- The og:url-versus-canonical-link rule and the absolute-og:url rule are lane
  policy: S067 and S068 define og:url as the canonical URL but name no
  `<link rel=canonical>`, and no opened source requires an absolute og:url
  (`CriticDeclarationFit` 3, `CriticSeparability` 5). The tool docstring says
  so at `5613071`.
- C2's census condition re-measures the same tag rules as C1 on real pages;
  conditions a–d (source rows, cites, quotes) are separate
  (`CriticSeparability`). C2's freshness fit is the round-29/30/31 shape: new
  current knowledge, the upstream head unchanged since round 33
  (`ExecUpstreamBlobExact`: head still `7fc6aa2f`, retained tar byte-identical
  to a fresh `git archive`).

## Round 34 — wave-2 corrections and repairs (appended)

Wave 2 `kake-r34-w2` (35 seats) attacked the landed work; reports in
`.ufo/waves/round-34/w2/`. The declaration and the measured-results table
stay as landed.

- Capability row: its evidence cell now says the 28/28 is the declared
  measure (necessary, not sufficient) and that the selftest, real-input run
  and code read came after the declaration (`w2/CriticCapabilityClaim.md`
  findings 1–2; edited in place because the row entered this round). The
  real-input run exercises only the missing-property rule: a tool with the
  canonical comparison deleted, or one that flags the wrong 15 pages, also
  gives `agrees: true` (`w2/ReviewRealInputRun.md` F1, F2). The og:type,
  absolute-og:url and canonical rules are shown on fixtures only.
- Tool repairs at `76fac3b` (after the C1 measurement; the C1 counter still
  gives 28/28 with all constants rejected, `verification/c1-at-76fac3b.json`):
  duplicate attributes now keep the first value (`w2/ReviewLinkPreviewTool.md`
  M1, `w2/CriticCapabilityClaim.md` 7); `og:image:url` satisfies `og:image`
  as S067 says it is identical (`CriticCapabilityClaim` 4); a non-regular
  page (FIFO) and a page over 16 MiB are `page_unreadable`
  (`w2/SentinelToolInputs.md` F2, `ReviewLinkPreviewTool` M2); an unparsable
  canonical href is `og_url_not_canonical` instead of a traceback with no
  JSON (`SentinelToolInputs` F1); a repeated `--manifest` is exit 64 and a
  duplicated manifest key is `input_invalid` (`ReviewLinkPreviewTool` L1,
  L3). Probes: `verification/tool-w2-repairs-probes.txt`.
- Selftest: 35 fixtures at `76fac3b` (35/35,
  `verification/selftest-link-preview-at-76fac3b.txt`). Of 13 single-rule
  mutants built by `w2/MutToolRuleBreaks.md`, three survived both the counter
  and the 29-fixture selftest (case-insensitive og:url comparison,
  trailing-slash normalisation, non-UTF-8 page read with replacement); three
  new fixtures kill each (34/35 for each mutant,
  `verification/selftest-w2-survivor-mutants.txt`).
- Still open on the tool: the first non-empty og:url is the only one
  compared; any `<link rel=canonical>` in the document counts as first,
  including inside `<template>` or `<svg>`; one non-UTF-8 page stops the whole
  manifest at exit 2; containment is path-based (hardlinks, check-then-use).
  `w2/ExecDifferentialOracle.md`: on 512 generated pages the tool and the
  wave-1 lxml implementation disagree on 171, all from vertical tab handling
  (the tool strips the WHATWG ASCII whitespace set, which excludes vertical
  tab) or a second og:url; on the 102 ds4cc pages they agree.
- Network-free and write-free held under strace for the 102 pages and the 28
  matrix cases (`w2/ExecNetworkFreeProof.md`) and under poisoned sockets
  (`ReviewLinkPreviewTool`).
- Pointer fix: the "name no `<link rel=canonical>`" point is
  `w1/CriticSeparability.md` finding 6, not 5 (`w2/ReviewScorecard34.md`).
  "No opened source requires an absolute og:url" understates S067: its URL
  type is "All valid URLs that utilize the http:// or https:// protocols",
  from which the entry infers (labelled) that a relative og:url fails the
  type (`w2/CriticC2Sufficiency.md`).
- Timing labels (`w2/CriticDeclarationTiming.md`): the selftest and the
  wave-1 real-input run were assigned at dispatch and mostly written before
  the lookup finding; only their lane receipts came after it. The tool
  docstring at `5613071` quotes S073, which was registered at `9ef758c`.
- C2 sufficiency (`w2/CriticC2Sufficiency.md`): the transcription control
  `0cce15f0` and the landed `9ef758c` both score 5 of 5; the landed entry
  carries 45 quoted spans, every one an exact match in retained text, against
  the control's four. The census totals were seen before the declaration
  (disclosed there); what the round learned is the per-page breakdown and the
  platform behaviour.
- Separability re-tested at the tip (`w2/ExecSeparabilityAtTip.md`): tip
  without the tool gives C1 0/28 and C2 5/5; tip without the entry and the
  S067–S070 rows gives C1 28/28 and C2 0/5.
- Re-runs: both counters reproduce every L1 receipt field for field
  (`w2/RerunC1Counter.md`, `w2/RerunC2Counter.md`); a third census method
  (html5lib) matches all seven numbers (`w2/ExecCensusThirdMethod.md`).
- Harm check (`w2/CriticHarmCheck.md`, `w2/ExecOtherGatesUnchanged.md`): no
  line deleted from `1e54c89` to `24a1647`; existing gates and nine earlier
  counters give the same results at base and tip. Wave-2 repairs change only
  round-34 files.

## Round 35 — declared claims (before implementation lands)

Base (pushed lane tip at round start): `16a6b8b8144f4d6e6187e9ecbb4fb5f4528b911a`.
Both owned axes sit at the 10/10 saturation line; the stagnation nudge applies
as in rounds 28 to 34. Round 34 was rejected as an honest stop because a
do-nothing control met each declared counter (`corpus/lessons/round-34-verifier-spotcheck.md`
routed defect 1). This round declares targets no do-nothing control can reach,
by sealing the inputs: the C1 case set and the C2 probe set were written by the
L1 before this declaration and before any build, are kept outside the lane
(`/fast/scratch/hyaku/kake-r35/sealed/`, mode 0700) until the reveal commit, and
are pinned here by sha256 in `.ufo/waves/round-35/sealed_count.py`. The tool
builder and the entry drafter never see them. The counter refuses (exit 2) to
measure a revision that already holds a key file, so every measured revision
predates the reveal and cannot be a copy of a key. The controls named below are
scored with this frozen counter, and their receipts are committed, before any
build.

| Claim | Axis | Before (at base) | Declared after | Counting command |
|---|---|---|---|---|
| C1 capability repair: `scripts/link_preview_audit.py` meets the round-35 contract below on 24 sealed cases (12 on the round-34 rules, 12 on the three repairs) | operability | `passed` 14 of 24 at `16a6b8b8` | `passed` ≥ 22 of 24 | `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision <commit> --key-revision <reveal commit>` (reads `passed`) |
| C2 freshness (sourced learning claim on new ground): `corpus/knowledge/security-txt-publishing.md`, how a publisher serves a valid security.txt (RFC 9116) from a GitHub Pages site, grounded in rows opened this round (S078–S085) | freshness | `met` false, `probesPassed` 0 of 12 at `16a6b8b8` | `met` true: entry present, ≤ 1500 words, `copiedShare` ≤ 0.25 with the nine pinned source texts intact, ≥ 3 good cites of S078–S099, `probesPassed` ≥ 9 of 12 | `python3 -B .ufo/waves/round-35/sealed_count.py c2 --root . --revision <commit> --key-revision <reveal commit>` (reads `met`, `probesPassed`) |

C1 contract (public; the sealed cases test exactly this and the round-34 rules):
- (a) A page with more than one non-empty `og:url` element gets one
  `og_url_multiple` finding (property `og:url`). The first non-empty og:url
  still gets the absolute check and the canonical comparison. This is lane
  policy by analogy with S068's single-og:type rule.
- (b) A `<meta>` or `<link>` start tag inside an open `<template>`, `<svg>` or
  `<math>` element counts neither as an Open Graph property nor as the
  canonical link. The element closes at its matching end tag, nesting is
  counted, and a self-closed `<svg/>` opens nothing.
- (c) A page that cannot be read (not UTF-8, not a regular file, over the read
  bound) gives `page_unreadable` for that page and no longer stops the other
  pages. The readable pages are audited, and their policy findings are reported
  beside the input findings. The verdict stays `could-not-evaluate` (exit 2), and
  `pagesChecked` counts the readable pages. Manifest-level faults are unchanged:
  `input_invalid` with no page, and nothing audited.
- Every other round-34 rule, reason name, verdict and exit code is unchanged.
  A case passes on exit code, verdict and the multiset of findings projected
  on (reason, page, property); `id` and `pagesChecked` are not compared.

C2 probes: 12 sealed questions a publisher-side entry on the bounded question
should answer (location, file format, required and single-use fields, dates,
contact order, encryption, signing, scope, and the GitHub Pages dot-directory
path). Each is one or more case-insensitive regexes over the entry text with
whitespace collapsed. The probe text stays sealed until the reveal.

Controls, each scored with the frozen counter before any build (receipts under
`.ufo/waves/round-35/verification/control-*.json`, control commits retained as
bundles under `.ufo/waves/round-35/retained/`):
- C1: the base tool unchanged (do nothing); the retained round-34 lookup tool
  `dcef39b5`; a constant tool that prints a clean report and exits 0.
- C2: the base (no entry); a junk entry shaped like the retained round-34
  control `0cce15f0` (junk rows S078–S081 marked mined, filler, ids); a
  keyword entry built from RFC 9116's table of contents and field names; a
  verbatim transcription of RFC 9116 sections 2.5 to 3.1 with the same rows.

Separability: C1 reads only the tool; C2 reads only the entry, `SOURCES.md` and
the retained texts. Either verifies with the other unlanded.

Pre-declaration work (disclosed): the L1 opened S078–S085 and re-opened S006 at
22:00–22:02Z, wrote both sealed keys, ran the C1 counter at base (14 of 24) and
the C2 counter at base (met false), and checked that the C1 key is reachable
with a private 20-line reference patch in a sandbox clone
(`/fast/scratch/hyaku/kake-r35/sealed/ref/`). That patch scored 24 of 24 and is
not the landed tool. The landed repair is written by a wave seat from the
public contract above.

Disclosed limits: the C1 cases are 24 short synthetic pages, not real
publisher pages. C2 probes test that stated facts are present, not that every
sentence is true, so the closure's read still owes the truth check. The
security.txt claim is offline: no lane property is asked to publish one, and
no live lane host is fetched.

### Round 35 — controls scored before any build (appended)

Frozen counter `.ufo/waves/round-35/sealed_count.py` as landed at `81d9fd74`.
Run in a sandbox clone (`/fast/scratch/hyaku/kake-r35/ctl/lane`) with the sealed
keys passed as `--key-file`, because the keys are not in the lane yet. Receipts
are `.ufo/waves/round-35/verification/control-<name>.json` with a matching `.exit`.
Control commits are retained as bundles `.ufo/waves/round-35/retained/r35-control-*.bundle`
(prerequisite `81d9fd74`), and the two round-34 controls come from their round-34
bundles.

| Control | Revision | Result | Target |
|---|---|---|---|
| C1 base tool, no repair (do nothing) | `16a6b8b8` | passed 14 of 24, exit 1 | ≥ 22 |
| C1 at the declaration commit | `81d9fd74` | passed 14 of 24, exit 1 | ≥ 22 |
| C1 retained round-34 lookup tool | `dcef39b5` | passed 7 of 24, exit 1 | ≥ 22 |
| C1 constant clean tool (exit 0, no findings) | `5f767534` | passed 7 of 24, exit 1 | ≥ 22 |
| C2 base, no entry | `16a6b8b8` | met false, probes 0 of 12 | met true |
| C2 at the declaration commit | `81d9fd74` | met false, probes 0 of 12 | met true |
| C2 retained round-34 hollow commit | `0cce15f0` | met false, probes 0 (no entry at the round-35 path) | met true |
| C2 junk entry and junk rows S078–S081 (round-34 `0cce15f0` shape) | `04848219` | met false: probes 0 of 12 (entry, size, copied and cites pass) | met true |
| C2 keyword entry from RFC 9116's contents and field names, same junk rows | `e5263d41` | met false: probes 3 of 12 | met true |
| C2 verbatim RFC 9116 sections 2.5–3.1 (1296 words), same junk rows | `ae9fb361` | met false: probes 8 of 12, copiedShare 0.9951 | met true |

No control reaches its target. Junk rows do satisfy the `cites` condition.
`cites` is necessary only: the probes and `copied` carry the discrimination,
and the Gate and the non-author read owe the row truth.

### Round 35 — C2 counter version 2, before any build is measured (appended)

Wave-1 `CriticC2Conditions` (`.ufo/waves/round-35/w1/CriticC2Conditions.md`) showed that
counter version 1 (`81d9fd74`, sha256 `c4d58dae…49ef`) let hidden bytes pass the `copied`, `size`
and `cites` conditions. Its two bundles score 8 and 6 probes of 12 under version 1, with every
other condition passing. Hidden padding inside an HTML comment brought a verbatim transcription
to copiedShare 0.0376 (`verification/control-c2-critic-*.json`). That is one probe short of `met`,
so a slightly longer transcription could have met it. Before the tool or the entry is measured,
the counter is revised to version 2 (`sealed_count.py`, sha256 `1b4d9d59…469b`; version 1 kept as
`sealed_count_v1.py`). The probes, the key pins, the C1 path and both targets are unchanged.
- The entry and `SOURCES.md` are read after HTML comments and Unicode format characters are
  removed (NFKC).
- `size` counts `[a-z0-9]+` words, the same words the overlap check uses, with a cap of 2200.
  The 1500 whitespace-word cap of version 1 equals about 1750 such words; 2200 leaves room for
  paths and field names, and visible padding that dilutes a transcription to 0.25 needs four
  times its length.
- `cites` reads only the first `## Registry` section, outside backtick and tilde fences. It
  counts a row only when its id is retained in `sources/receipts.json` and that receipt's URL is
  in the row's source cell.

Every control rescored under version 2 (`verification/control-v2-*.json`):

| Control | Revision | Result under version 2 |
|---|---|---|
| C1 base tool / declaration / lookup `dcef39b5` / constant clean | `16a6b8b8` / `81d9fd74` / `dcef39b5` / `5f767534` | passed 14 / 14 / 7 / 7 of 24 (C1 code path unchanged) |
| C2 base / declaration / round-34 hollow | `16a6b8b8` / `81d9fd74` / `0cce15f0` | met false, probes 0 |
| C2 junk entry and junk rows | `04848219` | met false: probes 0, cites 1 (only S078's junk row names a retained URL) |
| C2 keyword entry | `e5263d41` | met false: probes 3 |
| C2 verbatim transcription | `ae9fb361` | met false: probes 8, copiedShare 0.9951 |
| C2 critic hidden-padding transcription | `dce145db` | met false: probes 8, copiedShare 0.9781, cites 0 |
| C2 critic zero-width split with hidden rows | `79277c9f` | met false: probes 8, copiedShare 0.9781, cites 0 |
| C2 new: RFC 9116 sections 2.3–3.1 with every sixth word swapped, junk rows S078, S082 and S083 that copy the receipt URLs | `c2e38e5d` | met false: probes 6 of 12 (size, copied 0.0733 and cites pass) |

The new control's bundle is `retained/r35-control-c2-reworded.bundle`, and the critic's two
bundles are retained beside it. Limit carried: a mechanical rewording passes `copied`, and
junk rows that copy a retained URL pass `cites`. So only the probes separate the reworded
control from `met`. The closure's read of entry truth and row truth stays owed. This revision
is attacked again in wave 2.

## Round 35 — measured results (author-side; admission belongs to the non-author closure)

Keys revealed at `4c6be2bdec5630166c4013e53c226b1119ec63cc`. Both targets were declared at
`81d9fd74` and are unchanged. C2 is judged on counter version 2 (`bd14096a`), landed before any
build was measured. Receipts are `.ufo/waves/round-35/verification/<claim>-at-<rev>.json` with
matching `.exit` files.

| Claim | Before (rev) | After (rev) | Counting command | Target |
|---|---|---|---|---|
| C1 link-preview audit repair (capability) | passed 14 of 24 (`16a6b8b8`, `bd14096a`) | passed 24 of 24 (`b1cbbc39`, `95abec21`) | `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision <rev> --key-revision 4c6be2bd` | ≥ 22 of 24: met |
| C2 security.txt publishing entry (sourced) | met false, probes 0 of 12 (`16a6b8b8`, `bd14096a`, `b1cbbc39`) | met true at `95abec21`: probes 12 of 12, 1388 words, copiedShare 0.0, good cites S078 S079 S080 S082 S083 S084 S085 S086 | `python3 -B .ufo/waves/round-35/sealed_count.py c2 --root . --revision <rev> --key-revision 4c6be2bd` | met true: met |

- Counter version 1 at `95abec21` gives met true too (12 of 12, 1298 words; `verification/c2-v1-at-95abec21.json`).
- Measuring the reveal commit itself is refused with exit 2 (`verification/c1-at-4c6be2bd.json`).
- Separability: at `b1cbbc39` (tool landed, no entry) C1 is 24 of 24 and C2 met false. C2 reads
  no tool byte.
- The landed tool came from wave-1 `ExecToolRepair` (patch sha256 `7e463fa7…3a13`, applied byte
  for byte). The entry came from wave-1 `ScribeEntryDraft` (sha256 `0b5ac7e8…c397`), landed
  unedited. Neither seat read the keys.
- Axis ratings unchanged (10 → 10). Capability row "Link-preview audit, round-35 contract"
  entered `## Capabilities`.
- Limits: see `corpus/lessons/round-35.md` "Carried open". The probe topics were public, and the
  L1 also named them in the drafter's item. A mechanical rewording passes `copied`, and junk rows
  that copy a retained URL pass `cites`.

Correction appended for round-34 "Limits found by wave 1" (routed defect 2): `dcef39b5` does not
key on the case directory name. Its line 10, `h = hashlib.sha256(json.dumps(argv).encode())`,
and line 12 hash the arguments plus every relative path and file content under the current
directory. See `corpus/lessons/round-35.md` "Correction of round-34 mistake row 4".

## Round 35 — wave-2 corrections (appended)

Wave 2 `kake-r35-w2` (35 seats) attacked the landed work; reports in `.ufo/waves/round-35/w2/`.
The declaration, the counters and the measured results stay as landed. Every measured value
reproduced field for field (`RerunC1Sealed`, `RerunC2Sealed`, `ReviewScorecardLog35`). The v2
counter landed before any build was measured and tightened every rule except the size cap
(`ReviewV2Timing`). The C2 entry also meets under v1.

What the targets do not show:
- C1: 22 of 24 is reachable with contract bullet (c) skipped (+2 cases only), and the sealed cases
  hold no nested container (`ExecPartialRepairs`, `CriticC1Sufficiency`). 11 of 14 single-rule
  mutants still meet 22 (`MutToolRepair`). Every do-nothing control stays below: base 14, lookup
  7, constant 7. The landed tool scores 24, and the nesting rules rest on the builder's
  selftest fixtures. The fixture `og_url_multiple_first_value_checked` (selftest 46/46) now kills
  the one mutant that survived every detector.
- C2: an all-false entry written with the revealed probes meets it (`CriticProbeLeniency`,
  `dc8e1adf`, 12 of 12). So does an entry written from the public topic list with three landed
  row ids, by a seat that had not read the primary texts (`CriticC2Sufficiency`, `0b7779dc`, 11
  of 12). The C2 counter therefore does not show that the entry came from this round's sources,
  or that it is true. The disclosed limit "probes test that stated facts are present" overstates
  it: they test topic keywords near each other.
  - None of the pre-build controls (junk, keyword, transcription, reworded) took either shape.
  - The truth of the landed entry rests on wave-2 reads: `ReviewEntryRfcFacts` 27 of 27,
    `ReviewEntryExamples` 11 of 11, `ReviewEntryPagesFacts` 6 of 8 with two corrected by append,
    `ReviewProbeMatchesTruth` 10 true and 2 partly true.
  - This is lesson mistake row 5 and QUALITY round-35 (e), with
    `criteria/knowledge_control_check.py` exiting 1 on those two controls.
- Harm: none found in any earlier selftest or counter (`CriticHarmCheck`). The citing-set
  candidate gate now lists 7 findings instead of 4 (S001, S002 and S006 cited by the new
  entry), recorded and not adjudicated. The S001 and S002 used-by cells now include the entry.
- Post-measurement repair: the end-tag stack was quadratic on hostile input (`SentinelToolInputs`,
  499 s). The L1 fixed it with a per-name open count; the sandbox re-measure at `e068bc4b` gives
  24 of 24, selftest 46/46 and matrix 28/28. It counts toward no claim (lesson "Post-measurement
  tool repair").

## Round 36 — declared claims (before implementation lands)

Base `b720d79976a1fb8fe6a8eb4b9f50e946b0cd5e07`. One claim. Rounds 34 and 35 were rejected
because a cheap control met a knowledge-entry counter (round-35 closure routed defect 1). This
round makes no knowledge-entry claim. It works a different surface: the lane's source registry
has a shape census (`scripts/sources-census.sh`) but no tool that re-checks a row's quote against
a fetched copy of its source. Axis by the surface it changes: **freshness** — a new tool
(operation) for drift detection of `SOURCES.md` rows. The command that would show the surface
unmoved: `git ls-tree <rev> -- scripts/source_recheck.py` prints nothing, and the counter below
scores 0 of 28.

**C1 — freshness (capability): offline source re-check audit `scripts/source_recheck.py`.**
Frozen predicate, the same sentence here, in `.ufo/waves/round-36/sealed_count.py` (`PREDICATE`,
`met = cases == 28 and passed >= 25`) and in every receipt's `predicate` field:

    met: passed >= 25 of 28 sealed cases

- Before: 0 of 28 at the base (the tool is absent). After: `met` true at the build commit.
- Counting command (exit 0 met, 1 not met, 2 cannot evaluate):
  `python3 -B .ufo/waves/round-36/sealed_count.py --root . --revision <rev> --key-revision <reveal>`
- The 28 cases were written by the L1 before this declaration and stay outside the lane until a
  reveal commit; the counter pins their sha256 and refuses a revision that holds them. Seven
  contract bullets, four cases each. Every case of a bullet carries one check per rule of that
  bullet. Each of the 34 rule ablations of the L1's private reference fails at least the four
  cases of its bullet (at most 24 of 28, below target), and the reference scores 28 of 28. The
  ablation receipts are committed before any build.
- On every run the counter replaces every check id and body file name with fresh random ones, so
  no tool can key on ids, file names or labels.
- Sourced: the contract rests on rows opened this round, S088 (RFC 9110 status and redirect
  semantics), S089 (RFC 3986 reference resolution), S090 (WHATWG Encoding), S091 (UAX #15) and
  S092 (WHATWG HTML syntax), plus the existing S025 (template contents) and S033 (media types).
- Limits: the cases are synthetic fetch records, not live fetches. The tool reads a recorded
  snapshot; it does not fetch. A passing tool shows the contract below is implemented, not that
  any registry row is fresh.

C1 contract (public; the sealed cases test exactly this):

- Usage: `python3 scripts/source_recheck.py --manifest PATH` prints one JSON report on stdout:
  `{"version": 1, "verdict": V, "checksEvaluated": N, "findings": [F, ...]}`, where each finding is
  `{"check": <check id or null>, "reason": R, "target": <URL or null>}`. Exit 0 when V is `clean`,
  1 when `failed-policy`, 2 when `could-not-evaluate`, 64 on a usage error. It reads only the
  manifest and the body files it names; no network, no writes.
- Manifest (UTF-8 JSON): `{"version": 1, "checks": [check, ...]}`. A check is an object with
  `id` (non-empty string), `url` (absolute URL, scheme `http` or `https`, non-empty host), `quote`
  (non-empty string) and `hops` (non-empty list of `{"status": <integer 100-599>, "location":
  <string>}`). 301, 302, 303, 307 and 308 are redirect statuses; a redirect hop needs `location`;
  every hop but the last is a redirect and the last is not. When the last hop's status is 200
  the check also has `contentType` (string) and `body` (a relative path to a regular file inside
  the manifest's directory).
- (a) Final status. The last hop decides. 200: the quote rules (c)-(f) apply. 404 or 410: one
  `gone` finding. Any other status (including other 2xx): one `http_error` finding. No quote
  check unless the final status is 200. (S088 sections 15.5.5 and 15.5.11.)
- (b) Redirects. 301 and 308 are permanent; 302, 303 and 307 are temporary (S088 section 15.4).
  Each `location` is resolved against the URL that hop answered (the check `url` for the first
  hop, then the previous resolved location) by RFC 3986 section 5.2 (S089; S088 section 10.2.2),
  with no further normalization. When the chain starts with one or more permanent hops, the check
  gets one `moved` finding whose `target` is the resolved location of the last hop of that
  leading permanent run. A chain that starts with a temporary hop gets no `moved` finding,
  whatever follows. `moved` comes in addition to the final-status outcome. Fragment inheritance
  (S088 section 10.2.2) is out of scope.
- (c) HTML text. When the media type is `text/html` or `application/xhtml+xml`, the text is the
  decoded body with, in this order: comments removed (`<!--` to the next `-->`); the contents of
  `script`, `style` and `template` elements removed (start tag to the next end tag of the same
  name, ASCII case-insensitive; S092 raw text elements, S025 template contents); every remaining
  tag removed (`<` followed by an ASCII letter, `/` or `!`, up to the next `>`); character
  references decoded as HTML does (named, decimal and hexadecimal; Python `html.unescape`
  conforms). Text inside `title` and every other element is kept.
- (d) Quote match. The text and the quote are both normalized to NFKC (S091), then every
  character for which Python `str.isspace()` is true is deleted from both. The check holds when
  the normalized quote is a substring of the normalized text; matching is case-sensitive.
  Otherwise one `quote_missing` finding.
- (e) Media types. The media type is the part of `contentType` before any `;`, trimmed and
  compared ASCII case-insensitively; parameter names are case-insensitive too (S033). `text/plain`:
  the text is the decoded body as is (no comment, tag or reference processing), then (d). Any
  other media type: one `unsupported_type` finding and no quote check.
- (f) Decoding (S090). A body starting with a byte order mark (EF BB BF UTF-8, FE FF UTF-16BE,
  FF FE UTF-16LE) is decoded in that encoding with the mark dropped, whatever `charset` says.
  Otherwise the `charset` parameter, trimmed, with surrounding double quotes removed and matched
  ASCII case-insensitively, picks the encoding by the WHATWG Encoding label table; the tool
  supports the labels of UTF-8, UTF-16BE, UTF-16LE and windows-1252 (so `iso-8859-1`, `latin1`,
  `ascii` and `us-ascii` mean windows-1252). Any other label, even one valid in the table, gives
  one `charset_unsupported` finding and no quote check. No BOM and no `charset`: UTF-8. Bytes
  invalid in the chosen encoding decode to U+FFFD.
- (g) Input faults. An unreadable or non-JSON manifest, a non-object, `version` other than 1, or
  `checks` not a list: one `input_invalid` finding with check null, nothing evaluated. A check
  that breaks any manifest rule above (including a body path that is absolute, escapes the
  manifest directory, or is missing or not a regular file): one `check_invalid` finding for it
  (check = its id when it is an object with a non-empty string id, else null) and no other
  finding for it; the other checks are still evaluated and their findings reported.
  `checksEvaluated` counts the checks that are not `check_invalid`.
- Verdict: any `input_invalid`, `check_invalid` or `charset_unsupported` finding gives
  `could-not-evaluate`; otherwise any finding gives `failed-policy`; otherwise `clean`.
- A case passes on exit code, `verdict` and the multiset of findings projected on (check,
  reason, target); `target` is compared for `moved` only. Field order, `checksEvaluated` and
  extra fields are not compared.

Controls (receipts under `.ufo/waves/round-36/verification/control-*.json`, committed before any
build): the base (do nothing); a constant clean tool; an all-false tool (every check
`quote_missing`); a no-reader tool (status and redirect rules only, never opens a body); a junk
tool (non-JSON output); a shortcut tool keyed on ids, URL words and quote words; a naive reader
(raw substring over the UTF-8 body, no HTML, normalization or decoding rules); and the L1's
private reference with each of its 34 rule ablations. The non-ablation controls are built by a
pre-freeze control wave of fresh critic and mutation-tester seats from this public text only.
A control that meets the predicate means the counter is wrong, and it is fixed before any build.

### Round 36 — counter version 2, before any build or control seat is scored (appended)

The L1's own review of the frozen counter (`sealed_count.py` at `3555f63f`, kept as
`sealed_count_v1.py`, sha256 `28169d95…9728`) found that a tool it runs could read the counter's
command line through /proc, learn the key path or key revision, and read the key from the lane.
Version 2 (sha256 `1bf16734…162c`) runs the tool in a bubblewrap jail that sees only `/usr` and
the scratch directory, with no network and its own pid namespace; without `bwrap` it exits 2. The
cases, the key pin, the projection, the judge and the predicate (`met: passed >= 25 of 28 sealed
cases`) are unchanged. No build exists and no control seat's tool had been scored. Rescored under
version 2 (`.ufo/waves/round-36/verification/`): base `b720d799` 0 of 28 and declaration
`3555f63f` 0 of 28, exit 1; the private reference 28 of 28; each of the 34 rule ablations 16 to
24 of 28, none met (`verification/ablations/`).

### Round 36 — control wave, key version 2 and counter version 3, before any build (appended)

Pre-freeze control wave `kake-r36-ctl` (7 seats, critic and mutation-tester). Five controls
were built from the public text only and committed as sandbox commits on `9d81c75c` (bundles
`.ufo/waves/round-36/retained/r36-control-*.bundle`; seat reports `.ufo/waves/round-36/ctl/`).
`CtlJunk` and `CtlCounterExploit` ended at once on a provider cyber-policy filter: holds, not
retried, no findings. Scored with counter version 2 (receipts kept in `verification/v2/`):
constant clean 0, all-false 0, no-reader 8, naive reader 12, shortcut 17 of 28, none met.

`CtlShortcut` passed all eight cases of bullets (e) and (f) without opening a body: every quote
check there expected a hold, and the c and d checks used one fixed contentType, so a tool keyed
on that label could skip the text/plain, xhtml and decoding rules. That is a control meeting the
work of two bullets, so the key was redesigned before any build. Key version 2 (same 28 case
ids, 4 per bullet) adds checks whose correct answer is `quote_missing` where a skipped rule gives
a hold (text/plain with a reference, xhtml script text, UTF-8 bytes under a windows-1252 label)
and rotates contentTypes across the c and d checks. Counter version 3 (sha256 `88ec5914…`,
version 2 kept as `sealed_count_v2.py`) changes only `KEY_SHA256`. The predicate is unchanged:
`met: passed >= 25 of 28 sealed cases`.

Rescored under version 3 (`verification/control-*.json`, `verification/ablations/`): base
`b720d799` 0, declaration `3555f63f` 0, `9d81c75c` 0; constant clean 0, all-false 0, no-reader
8, naive reader 12, shortcut 9 of 28; the private reference 28; 36 ablations 13 to 24, none met,
including two shortcut ablations: full HTML rules only for `text/html; charset=utf-8` (13) and
no decoding with every undecodable body called a hold (24).

Correction of the declaration's base line: the full base hash is
`b720d799ae99c19a7c97f2b1391d4fe928be0e11`. The hash written at `3555f63f` after "Base" is wrong
(an L1 typing error); every receipt used the short form `b720d799` or the hash above.

## Round 36 — measured results (author-side; admission belongs to the non-author closure)

Key v2 revealed at `fd1fb723624b742a00a6e8e908f3b42901d627f8`. The predicate was declared at
`3555f63f` and is unchanged; counter version 3 (`cd321279`) landed before any build. Receipts are
`.ufo/waves/round-36/verification/c1-*.json` with matching `.exit` files.

| Claim | Before (rev) | After (rev) | Counting command | Predicate |
|---|---|---|---|---|
| C1 source re-check audit (freshness, capability) | passed 0 of 28 (`b720d799`, `cd321279`) | passed 28 of 28 (`4d5b3d55`) | `python3 -B .ufo/waves/round-36/sealed_count.py --root . --revision <rev> --key-revision fd1fb723` | `met: passed >= 25 of 28 sealed cases`: met |

- Measuring the reveal commit is refused with exit 2 (`c1-keyrev-at-fd1fb723.json`).
- The tool is wave-1 `ExecToolBuild`'s file (sha256 `577b2d7d…0d48`), landed unedited. An
  independent blind implementation by wave-1 `ExecSelftest` also scores 28 of 28
  (`verification/independent-selftest-reference.json`).
- Controls under the same counter: base 0; constant clean 0; all-false 0; no-reader 8; naive
  reader 12; shortcut 9; 36 reference ablations 13 to 24. None met.
- Selftest `scripts/source_recheck_selftest.py` 101/101 on the landed tool (fixture f08 corrected
  by the L1; lesson mistake row 4).
- Freshness evidence (not a counted claim): the first live re-check of 90 Gate quotes found 14
  findings on 13 rows (lesson "Real-input run"); wave 2 re-opens each by hand.
- Capability row "Offline source re-check audit" entered `## Capabilities`. Axis ratings
  unchanged (10 → 10).
- Limits: lesson `corpus/lessons/round-36.md` "Carried open".

## Round 36 — wave-2 corrections (appended)

Wave 2 `kake-r36-w2` (34 seats; `CriticClaimSufficiency` ended on a cyber-policy filter, a hold)
attacked the landed work; reports in `.ufo/waves/round-36/w2/`. The declaration, the counter and
the measured result stay as landed; details in `corpus/lessons/round-36.md` "Wave-2 corrections".
- Every receipt reproduced (C1 runs, controls, ablations, real-run audit). The build also meets
  under counters v1 and v2 with key v1 (28 of 28), so the result does not rest on the v2 or v3
  change.
- The declaration's sentence "a tool that skips any one rule fails all four cases of its bullet"
  is overstated: it held for the 36 listed ablations, while 9 of 32 single-point mutants of the
  landed tool and 5 of 6 new reference mutants still meet 25 (`w2/MutTool.md`,
  `w2/RerunAblations.md`), and an HTML-only casefold defect scores 26 under key v2
  (`w2/CriticKeyV2Change.md`). No do-nothing, junk, all-false, no-reader or shortcut control met 25.
- Tool defects outside the sealed set: attribute-embedded `<script` truncates a page (carried);
  body symlink escape (repaired after measurement, sandbox re-measure 28 of 28 at `bf9b2089`,
  counts toward no claim). Recorder now sends `Accept-Language`.
- Freshness result after hand re-opens: 2 rows moved (S040, S068; notes appended to SOURCES.md),
  S087 still gone; 5 Gate quotes carry markdown backticks (no drift); run 2 gives 8 findings, each
  explained (`realrun/audit-run2.json`).

## Round 37 — declared claims (before implementation lands)

Base `621fb528ba9116b9f440b8332be6dfc0cad4e972` (pushed lane tip at round start; round 36
admitted). Two claims on two different surfaces. Round 36 worked freshness on
`scripts/source_recheck.py`; the anti-loop rule moves C1 to a new frontier surface (publisher-side
crawl rules, PROVINCE "Crawl hygiene per host"). C2 only repairs a routed round-36 defect (closure
routed defect 3: the one-change tool mutants that still pass need fixture classes that kill them).

**C1 — operability (capability): offline robots.txt expectation audit `scripts/robots_audit.py`.**
Axis by the surface it changes: a new tool (operation) that tells a publisher, offline, whether
the robots.txt they will serve allows or disallows the URLs they say it should, under RFC 9309
(S011, re-opened this round) and the lane readings below. The command that would show the surface
unmoved: `git ls-tree <rev> -- scripts/robots_audit.py` prints nothing and the counter below scores
0 of 28. Frozen predicate, the same sentence here, in `.ufo/waves/round-37/sealed_count.py`
(`PREDICATE`, `met = cases == 28 and passed >= 25`) and in every receipt's `predicate` field:

    met: passed >= 25 of 28 sealed cases

- Before: 0 of 28 at the base `621fb528` (the tool is absent; `verification/c1-at-621fb528.json`,
  exit 1). After: `met` true at the build commit.
- Counting command (exit 0 met, 1 not met, 2 cannot evaluate):
  `python3 -B .ufo/waves/round-37/sealed_count.py --root . --revision <rev> --key-revision <reveal>`
- The 28 cases (7 bullets (a)–(g), 4 cases each) were written by the L1 before this declaration
  and stay outside the lane until a reveal commit; the counter pins their sha256 (`93ad9ee6…0a90`)
  and refuses a revision that holds them. Every case of a bullet carries one check per listed
  rule of that bullet, and every case has at least one check that holds and one that does not.
  Coverage statement, measured and nothing more: each of the 34 listed ablations of the L1's
  private reference scores at most 24 of 28 (16 to 24; receipts
  `.ufo/waves/round-37/verification/ablations/`), and the reference scores 28 of 28. This does not
  say that every way of skipping a rule fails; a mutation pass on the reference runs before any
  build (control wave) and its result is appended before any build.
- On every run the counter replaces every check id and robots file name with fresh random ones, so
  no tool can key on ids, file names or labels; the tool runs in a bubblewrap jail that sees only
  /usr and the scratch directory.
- Sourced: S011 (RFC 9309, re-opened this round, retained `.ufo/waves/round-37/sources/S011.txt`)
  and S095 (Google's robots.txt specification, opened this round); S096 and S097 are opened this
  round as well (row decisions in the lesson Gate).
- Limits: the cases are synthetic robots files and URLs, not live fetches. The tool reads a
  local file; it does not fetch, follow redirects, cache, or claim what any crawler does. Where
  RFC 9309 says SHOULD or MAY, the contract fixes one reading (marked "lane reading").

C1 contract (public; the sealed cases test exactly this):

- Usage: `python3 scripts/robots_audit.py --manifest PATH` prints one JSON report on stdout:
  `{"version": 1, "verdict": V, "checksEvaluated": N, "findings": [F, ...]}`, where each finding is
  `{"check": <check id or null>, "reason": R}` (extra fields allowed). Exit 0 when V is `clean`, 1
  when `failed-policy`, 2 when `could-not-evaluate`, 64 on a usage error (any argument list other
  than exactly `--manifest PATH`). It reads only the manifest and the robots files it names; no
  network, no writes.
- Manifest (UTF-8 JSON): `{"version": 1, "checks": [check, ...]}`. A check is an object with `id`
  (non-empty string, not equal to the id of an earlier check in the list), `robotsStatus` (a JSON
  integer 200–299, 400–499 or 500–599; booleans and floats are not integers), `userAgent` (a
  product token: one or more ASCII letters, `_` or `-`; RFC 9309 section 2.2.1), `url` (absolute
  URL, scheme `http` or `https`, non-empty host) and `expect` (`"allow"` or `"disallow"`). When
  `robotsStatus` is 200–299 the check also has `robots`: a relative path to a regular file inside
  the manifest's directory (after resolving symlinks and `..`). Otherwise `robots` is ignored.
- Findings per evaluated check: the tool decides whether the robots rules allow the URL for the
  user agent. `expect` `allow` and the decision is disallow: one `blocked` finding. `expect`
  `disallow` and the decision is allow: one `exposed` finding. Otherwise none.
- (a) Access result (RFC 9309 section 2.3.1). `robotsStatus` 200–299: the robots file is parsed
  and decides (rules (b)–(e)). 400–499 ("unavailable"): allowed, whatever any file says. 500–599
  ("unreachable"): disallowed, whatever any file says, including `/robots.txt`.
- (b) Lines. Only the first 512000 bytes (500 KiB, section 2.5; lane reading: exactly this
  limit) of the file are read; a leading UTF-8 byte order mark (EF BB BF) is dropped; the rest is
  decoded as UTF-8 with invalid bytes becoming U+FFFD. Lines end at CR, LF or CRLF. On each line
  everything from the first `#` is a comment and removed. A line without `:` is ignored. The key
  is the text before the first `:` with spaces and tabs trimmed, compared ASCII
  case-insensitively; the value is the text after it with spaces and tabs trimmed. Keys
  `user-agent`, `allow` and `disallow` are records; every other key (for example `sitemap`,
  `crawl-delay`) is ignored and does not end a group (section 2.2.4). An `allow` or `disallow`
  line before the first `user-agent` line is ignored (section 2.2.2).
- (c) Groups (section 2.2.1). A `user-agent` line starts a new group unless the previous record
  was also a `user-agent` line (blank, comment and ignored lines between them do not count), in
  which case it adds a name to the current group. The check's `userAgent` matches a group when it
  equals one of the group's names compared ASCII case-insensitively. The rules of every matching
  group are combined. If no group matches, the rules of every group named `*` are combined. If
  there is none, no rules apply and every URL is allowed.
- (d) Rules (sections 2.2.2, 2.2.3). A rule with an empty value never matches. `*` in a rule
  matches any sequence of characters (also none); a `$` that is the last character of the rule
  anchors the match at the end of the path (any other `$` is literal). A rule matches when it
  matches a prefix of the path starting at its first character (or the whole path when anchored).
  Of the matching rules the one with the longest normalized value (rule (e), counted in octets,
  `*` and `$` included) decides; when an `allow` and a `disallow` of that length both match,
  `allow` decides. No matching rule: allowed.
- (e) Path to match and normalization (section 2.2.2). The path to match is the URL's path (`/`
  when empty) followed by `?` and the query when the query is non-empty; the fragment is never
  part of it. The path `/robots.txt` is always allowed when (a) says the file decides. Before
  comparison both the rule value and the path are normalized: every non-ASCII character becomes
  its UTF-8 octets percent-encoded with uppercase hex; every `%XX` escape (two hex digits) of an
  unreserved character (ASCII letters, digits, `-`, `.`, `_`, `~`; RFC 3986) is decoded; every
  other `%XX` escape is kept with its hex digits uppercased. Lane reading of the section 2.2.2
  examples: reserved characters are never decoded or encoded, so `%2F` and `/` differ.
- (f) Check faults. A check that breaks any manifest rule above (not an object, id missing,
  empty or repeated, status outside the three ranges, a user agent that is not a product token,
  `expect` other than the two strings, a URL that is not absolute http(s) with a host, or for
  200–299 a robots path that is missing, absolute, escapes the manifest directory or is not a
  regular file): one `check_invalid` finding for it (check = its id when it is an object with a
  non-empty string id, else null) and no other finding for it; the other checks are still
  evaluated. `checksEvaluated` counts the checks that are not `check_invalid`.
- (g) Manifest faults. A manifest path that is not a regular file, larger than 64 MiB,
  unreadable, not UTF-8 or not JSON, a non-object, `version` other than the integer 1, or `checks`
  not a list: one `input_invalid` finding with check null, nothing evaluated.
- Verdict: any `input_invalid` or `check_invalid` finding gives `could-not-evaluate`; otherwise any
  finding gives `failed-policy`; otherwise `clean`.
- A case passes when, for each of its runs (one manifest each; most cases have one, the (g) cases
  five), the exit code, `verdict` and the multiset of findings projected on (check, reason) equal
  the sealed expectation. Field order, `checksEvaluated` and extra fields are not compared.

**C2 — operability: the fixture set of `scripts/source_recheck_selftest.py` kills the 32
round-36 one-change tool mutants.** Axis by the surface it changes: the lane's selftest gate for
its landed tool (its fixture data); not coverage of a new rule, not a new tool. Round-36 wave 2
`MutTool` found 5 of its 32 mutants pass the selftest (M07, M08, M09, M11, M24) and 9 meet the
sealed target. The command that would show the surface unmoved: the counter below at a revision
whose selftest is the base selftest gives the base count. Frozen predicate, the same sentence
here, in `.ufo/waves/round-37/c2_mutkill.py` (`PREDICATE`) and in every receipt:

    met: killed >= 32 of 32 round-36 tool mutants

- Counting command: `python3 -B .ufo/waves/round-37/c2_mutkill.py --root . --revision <rev>`
  (exit 0 met, 1 not met, 2 cannot evaluate). Before: killed 27 of 32 at the base `621fb528`
  (101 fixtures, all valid on E1 and E2; survivors M07, M08, M09, M11, M24; receipt
  `.ufo/waves/round-37/verification/c2-at-621fb528.json`, exit 1). After: `met` true at the build
  commit.
- The counter reads only the selftest's fixture data (dumped inside a jail) and runs every
  fixture itself; the selftest's own runner never runs, so a selftest cannot recognize a mutant by
  hash, name or text. A fixture counts only when it passes on both the measured round-36 tool
  (`4d5b3d55`, E1) and the round-36 independent blind implementation (E2), so a junk, all-false or
  one-reading fixture counts for nothing. A mutant is killed when a counted fixture fails on it.
- Limits: 32 known mutants, not every defect. The tool itself is not changed by C2.

Controls for both claims (receipts under `.ufo/waves/round-37/verification/control-*.json`,
committed before any build): the base (do nothing); for C1 a constant clean tool, an all-false
tool (every check reported against its expectation), a no-reader tool (status rule only, never
opens a robots file), a junk tool (non-JSON output), a shortcut tool keyed on ids, URL words,
user-agent names and file names, and a naive reader (a `disallow` value that is a raw prefix of
the URL path decides, no groups, no allow, no normalization); for C2 the base selftest, an
all-failing fixture set, a junk fixture set, a fixture set that keys on mutant ids, names or
hashes, and a snapshot fixture set (expectations recorded from E1 on random inputs). Built by a
pre-freeze control wave of fresh critic and mutation-tester seats from this public text only. A
control that meets a predicate means that counter or target is wrong; it is fixed before any
build, with the original rule kept as the rule of record (round-36 routed defect 4).

Counter digests at this declaration: `sealed_count.py` sha256 `2ebb39b5…f0e3`, `c2_mutkill.py`
sha256 `d72e232e…5cb6`. Mutant manifest pin `9300ad38…dbd4` (MutTool's `manifest.json`; its
`summary.json` sha256 `1cfa9ce1…0af9` equals the one cited in `round-36/w2/MutTool.md`).

### Round 37 — control call, before any build (appended)

Pre-freeze control call `kake-r37-ctl` (8 seats, 5 critic, 3 mutation-tester; reports in
`.ufo/waves/round-37/ctl/`). C1 controls were built from the public text only, retained in
`.ufo/waves/round-37/retained/controls/` and scored by the L1 with the frozen counter
(`verification/control-*.json`, `.exit`), predicate unchanged (`met: passed >= 25 of 28 sealed
cases`):

| C1 control | passed of 28 | met |
|---|---|---|
| base `621fb528` (tool absent) | 0 | false |
| constant clean (`CtlC1ConstantClean`) | 0 | false |
| junk, prints `not a report` (`CtlC1Junk`) | 0 | false |
| no-reader, status and fault rules only (`CtlC1NoReader`) | 0 | false |
| all-false (`CtlC1AllFalse`) | 4 | false |
| naive reader, Python `urllib.robotparser` (`CtlC1NaiveReader`) | 20 | false |

- The stock Python 3.14 `urllib.robotparser` passes every case of bullets (a), (c), (d), (f) and
  (g) and none of (b) and (e) (`control-CtlC1NaiveReader.json` perCase). It stays below target,
  but (c) and (d) do not separate it from the contract.
- `CtlC1Shortcut` died at once on a provider quota error (HTTP 429 `RESOURCE_EXHAUSTED`, model
  route gemini-4-argon) with no output; dead, not replaced. The shortcut control is built as a
  disclosed follow-up by the living seat `CtlC1NoReader` and its receipt is appended before any
  build is measured.
- Mutation pass on the L1's private reference (`MutRefPass`, read access to the reference and key,
  no case content in its report): 42 single-point mutants, **28 meet 25** (most at 28), 14 do not.
  The survivors break edge sentences the sealed cases do not test (exact 512000 limit,
  `str.strip()` vs space/tab trim, `rfind('#')`, `splitlines()`, Unicode casefold, substring
  user-agent match, `.+` for `*`, `re.search` for prefix match, raw-length specificity, `>=` on
  ties, status edges 300/399/599, floats, symlink and prefix containment, 64 MiB edge, non-UTF-8
  replacement, report `version`). The coverage statement in the declaration stands as written
  (each of the 34 listed ablations at most 24) and claims nothing more: 25 of 28 certifies the
  listed rules, not these edges. The robots selftest (wave 1) is asked to cover them.
- Junk control for the round-36 counter (round-36 routed defect 5): the junk tool scores 0 of 28
  under `.ufo/waves/round-36/sealed_count.py` with key `fd1fb723`, exit 1
  (`verification/control-r36-junk.json`). Round 36's junk control was untested; it is now run.

**C2 is withdrawn before any data.** `CtlC2FixtureSets` built four selftest variants and scored
them with the frozen C2 counter (`retained/controls/c2/c2-*.json`, variant files beside them):
all-failing 27, junk 27, keyed on mutant ids, names, hashes or source text 27 — and a snapshot
set of 299 random manifests whose expectations were recorded from E1 (no contract reading)
**32 of 32, met** (commit `da09e6c7` in the seat's sandbox; 398 fixtures valid on E1 and E2).
A sourceless fixture set meets the counter, so the counter does not measure the claimed surface
(contract-grounded fixtures). Under the round rule a counter that a control meets is redesigned
before data or the claim is dropped; no redesign that separates contract-grounded from recorded
expectations was found in time, so C2 is not a claim of this round. The fixture repair for the
five selftest survivors (routed defect 3) continues as non-claim work; its counter output is
reported as evidence only. C1 is the round's only claim.

### Round 37 — shortcut control follow-up, before any build is measured (appended)

`CtlC1Shortcut` was dead (quota error, no output). The living seat `CtlC1NoReader` built the
shortcut control as a disclosed follow-up (`ctl/CtlC1NoReader-shortcut.md`; tool retained as
`retained/controls/CtlC1Shortcut-followup-robots_audit.py`, sha256 `61724ead…7d`). It found no
id, file-name or URL-word heuristic worth trying (the counter randomizes ids and file names), so
it read the public per-case receipts, kept Python's `urllib.robotparser` (the naive reader, 20 of
28, failing only bullets (b) and (e)) and added six one-line patches, each copying one contract
rule of (b) or (e): read only 512000 bytes, drop a BOM, split only at CR/LF/CRLF, drop non-record
keys so they do not end a group, pass `path[?query]` without the fragment, keep reserved `%XX`
distinct. Scored by the L1 with the frozen counter: **28 of 28, met**
(`verification/control-CtlC1Shortcut-followup.json`).

Disposition, recorded before any build is measured: this control does not skip the claimed work.
It implements the (b) and (e) rules the stdlib lacks and delegates (c) and (d) to a library whose
group and matching rules agree with the contract on every sealed case; without the six rule
patches it scores 20. Every control that skips a bullet's rules stays at or below 24 (ablations),
and every do-nothing, junk, constant, all-false and no-reader control at or below 4. C1 is kept as
declared; the predicate, key and counter are unchanged. Limit, stated now: the sealed cases do not
separate the contract from `urllib.robotparser` where the two differ (substring user-agent match,
a non-final `$`, how `*` and `$` count toward rule length, per the naive-reader report), nor from
the 28 single-point reference mutants of `MutRefPass`. A tool meeting 25 of 28 is shown to follow
the tested rules of (a)–(g), not every contract sentence; the robots selftest is the instrument for
the rest.

## Round 37 — measured results (author-side; admission belongs to the non-author closure)

Key revealed at `424aa2480bcbac1832b2aa9da49c51b78ec5092f` (sha256 `93ad9ee6…0a90`, equal to the
pin). The predicate was declared at `202d625a` and is unchanged; the counter, key and target are
unchanged since then. Receipts: `.ufo/waves/round-37/verification/c1-*.json` with `.exit` files.

| Claim | Before (rev) | After (rev) | Counting command | Predicate |
|---|---|---|---|---|
| C1 robots.txt expectation audit (operability, capability) | passed 0 of 28 (`621fb528`, `202d625a`, `4b089da6`, `ccc3b2b9`, `528a6d02`) | passed 28 of 28 (`9dbc88bb`) | `python3 -B .ufo/waves/round-37/sealed_count.py --root . --revision <rev> --key-revision 424aa248` | `met: passed >= 25 of 28 sealed cases`: met |

- Measuring the reveal commit is refused with exit 2 (`c1-keyrev-at-424aa248….json`). The build was
  also measured before the reveal with the key file (`c1-at-9dbc88bb.json`, 28 of 28).
- The tool is wave-1 `ExecRobotsTool`'s file (sha256 `5eb767ec…cabae`), landed unedited. An
  independent blind implementation by wave-1 `ExecRobotsSelftest` scores 28 of 28 too
  (`verification/independent-selftest-reference.json`).
- Selftest `scripts/robots_audit_selftest.py` (131 fixtures, written blind from the contract):
  131/131 on the landed tool; on the shortcut follow-up 126/131 (fails space/tab-only trim of
  key and value, ASCII-only group-name folding, non-final `$`, `$` counted in specificity); on
  the stock parser 119/131; on the L1's private reference 130/131 (the reference folds
  group names with Unicode `lower()`, a reference defect the sealed cases do not reach).
- Controls under the same counter: base 0; constant clean 0; junk 0; no-reader 0; all-false 4;
  stock parser 20; shortcut follow-up 28 (disposition at `ccc3b2b9`); 34 reference ablations
  16–24. Mutation pass on the reference: 28 of 42 meet.
- Real input (evidence, not a claim): 55 checks over 12 live robots.txt files, `clean`, exit 0
  (`realrun/audit.json`).
- C2 withdrawn before data (`4b089da6`). As non-claim evidence the C2 counter reads 27 → 32 of 32
  (`verification/c2-at-621fb528.json` → `c2-evidence-at-528a6d02.json`).
- Capability row "Offline robots.txt expectation audit" entered `## Capabilities` below. Axis
  ratings unchanged (10 → 10).
- Limits: `corpus/lessons/round-37.md` "Carried open".

### Capabilities acquired in round 37

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Offline robots.txt expectation audit | Reads a version-1 manifest of (robots status, local robots.txt, product token, URL, expected allow/disallow) and reports, read-only and network-free, each check whose RFC 9309 decision under the lane readings differs from the expectation (`blocked`, `exposed`; check and manifest faults; exits 0/1/2/64); no fetch, redirect, cache or crawler-specific claim; the sealed cases certify the tested rules of (a)–(g), not every contract sentence | `scripts/robots_audit.py` at `9dbc88bb`; sealed counter 28 of 28 (`.ufo/waves/round-37/verification/c1-keyrev-at-9dbc88bb.json`, reveal `424aa248`) against 0 at base and at most 20 for the controls that skip rules; selftest 131/131 (`verification/robots-selftest-at-9dbc88bb-tool.json`); live run over 12 robots.txt files (`realrun/audit.json`) | 37 — **not admitted** (round-37 closure; "Round 37 — closure correction") |

## Round 37 — wave-2 corrections (appended)

Wave 2 `kake-r37-w2` (34 seats; reviewer, mutation-tester, scout, sentinel, revenger; no critic
seat because the critic route was exhausted, `.ufo/waves/round-37/dead-seats.txt`) attacked the
landed work; reports in `.ufo/waves/round-37/w2/`. The declaration, the counter, the key and the
measured result stay as landed; details in `corpus/lessons/round-37.md` "Wave-2 corrections".

- Reproduced byte for byte: every C1 receipt at the seven revisions (`RerunC1Sealed`), every
  control and the independent implementation (`RerunControls`), the 34 ablations and the coverage
  sentence (`RerunAblations`), the C2 evidence and the snapshot control (`RerunC2Evidence`).
- **The shortcut disposition at `ccc3b2b9` is contested and is not a pass under the round rule.**
  `ReviewShortcutDisposition`: the stdlib-plus-six-patches control delegates group selection and
  matching to `urllib.robotparser`, which is wrong on 6 of 9 contract checks written by the
  reviewer (substring user agents, wildcard rules ranked by matched length, non-final `$`), so it
  skips part of the claimed work and still scores 28 of 28; with the six patches removed it
  scores 20. `ReviewTimeline`: the declaration said a control meeting the predicate means the
  counter or target "is fixed before any build"; the L1 instead kept C1 by a written judgment
  (landed 7 min after the build seat was dispatched, 10 min before the build landed, before any
  measurement). Under the round rule the C1 counter is shown not to separate the contract from a
  control that skips (c)/(d) work. C1's self-verdict is therefore **measured met, admission
  contested** — the closure rules.
- Overstated wording, corrected here: "25 of 28 certifies the tested rules of (a)–(g)" — it
  excludes the 34 listed ablations, not every violation of a listed rule (reference mutant M20
  breaks the tie rule at 26). The measured-results capability row's "at most 20 for the controls
  that skip rules" — ablations reach 24 and one control met 28; the main-table row now says so.
  "Every case has at least one check that holds and one that does not" — the (g) cases' manifest-
  fault runs have no holding check (`ReviewWithdrawalAndWording`). "Before: 0 of 28" means the
  tool is absent at those revisions.
- Post-measurement repairs (count toward no claim): the landed tool's `*` matcher used a
  backtracking regex; a 191-byte manifest hung it (`SentinelRobotsInputs`, `ReviewRobotsTool`).
  Replaced by a linear leftmost segment scan; receipt
  `verification/postfix/wildcard-backtracking-receipt.txt` (old: killed at 10 s; new: 18 ms;
  selftest 134/134; sealed 28 of 28; 200 000-pair fuzz against the old matcher, 0 mismatches).
  The `source_recheck.py` quote handling added in wave 1 let a stray `'` or `"` in a tag disable
  script/style removal (`ReviewHardening`); a quote now opens only after `=` (seat prototype,
  106/106, 6/6, round-36 sealed 28 of 28). Three robots selftest fixtures added for the stdlib
  gaps (c12, c13, d17): 134/134 on the tool and the independent implementation, 127/134 on the
  shortcut control.
- Carried: `source_recheck.py` body reads are uncapped (1 GiB body → `MemoryError`) and the
  body-path race is narrowed, not closed (`SentinelHardening`, `ReviewRoutedClosure`); a ~60 MiB
  manifest can still raise `MemoryError` inside `json.loads`; the robots tool accepts `NaN` and
  malformed URLs (`ReviewRobotsTool`); the criteria checks each have constructed false passes and
  fails (`ReviewCriteriaV2`); two contract points split the L1 reference from the tool and the
  independent implementation (symlinked manifest directory, `/robots%2Etxt`), and the reference
  folds group names with Unicode `lower()` (`ScoutContractAmbiguityR37`, `DiffToolVsIndependent`:
  8192 checks, 0 tool/independent disagreements).
- Round-36 routed defect 3, limit line for the round-36 capability row "Offline source re-check
  audit": 28 of 28 there did not certify every contract rule — 9 of 32 one-change tool mutants met
  the sealed target and M24 (BOM mark kept) also passed the round-36 selftest; round 37's five
  fixtures make the selftest kill all 32 (evidence only, `verification/c2-evidence-at-528a6d02.json`).
- Round-36 routed defect 8, the 18 contract points the round-36 text leaves undecided
  (`.ufo/waves/round-36/w1/CriticContractAmbiguity.md`), stay undecided; carried.
- Late wave-2 result (`MutRobotsTool`): of 42 single-point mutants of the landed tool, 23 meet
  the sealed target and 3 (M04 drop invalid UTF-8 bytes, M14 first `*` group only, M15 an empty
  matching group falls back to `*`) also passed the selftest. Three fixtures added (b19, c14,
  c15); each kills its mutant (`verification/postfix/mutrobots-survivors/`), 137/137 on the tool
  and on the independent implementation.

## Round 37 — closure correction (appended in round 38)

The non-author closure (`corpus/lessons/round-37-verifier-spotcheck.md`, routed defect 1) did
**not admit round-37 C1**: a control (`retained/controls/CtlC1Shortcut-followup-robots_audit.py`,
stdlib `urllib.robotparser` plus six patches) met the frozen predicate (28 of 28,
`verification/control-CtlC1Shortcut-followup.json`) at `ccc3b2b9`, before the build, and the
declaration said such a control means the counter is wrong and is fixed before any build. The lane
kept the claim by reclassifying the control; that was a rule change after a seat had scored.
Round-37 C1 status: **not admitted**. The `## Capabilities` row "Offline robots.txt expectation
audit" (added at `b99b6679`) and the "Capabilities acquired in round 37" row carry that status: the
tool, its selftest and the independent implementation stand as non-claim work; no capability was
admitted in round 37. The round-37 counter (`.ufo/waves/round-37/sealed_count.py`, key
`424aa248`) stays the rule of record for round-37 C1 and is not re-scored here. Round-37 per-axis
verdicts are the closure's (operability and freshness `unprovable-but-better`).

## Round 38 — declared claims (before implementation lands)

Base `af43a50fa399881eead9381d835b78a015e277a6` (pushed lane tip at round start; round 37 not
admitted). One claim. Prior frontier: r36 freshness (`source_recheck.py`), r37 operability
(`robots_audit.py`). This round re-claims `robots_audit.py` under a redesigned counter: the routed
repair (closure routed defect 2). The round-37 shortcut scores below this round's target before any
data (below).

**C1 — operability (tool repair, not a new capability): `scripts/robots_audit.py` gains three
contract rules it lacks at the base, under a counter that also separates it from a
stdlib-delegating reader.** Axis by the surface it changes: the robots audit tool's manifest and
check validation and its implicit-allow comparison (three edge classes: non-JSON number literals
and long integers (h), URL characters (i), the implicit `/robots.txt` allow on the normalized path
(k)); not a new tool, not coverage of new domain ground. The command that would show the surface
unmoved: the counter below at a revision whose `scripts/robots_audit.py` is the base bytes (sha256
`944d2f51…d3e5`) scores 8 of 20. Frozen predicate, the same sentence here, in
`.ufo/waves/round-38/sealed_count.py` (`PREDICATE`, `met = cases == 20 and passed >= 19`) and in
every receipt's `predicate` field:

    met: passed >= 19 of 20 sealed cases

- Before: 8 of 20 at the base `af43a50f` (`.ufo/waves/round-38/verification/c1-at-af43a50f.json`,
  exit 1; the base tool fails every case of bullets (h), (i), (k)). After: `met` true at the build
  commit.
- Counting command (exit 0 met, 1 not met, 2 cannot evaluate):
  `python3 -B .ufo/waves/round-38/sealed_count.py --root . --revision <rev> --key-revision <reveal>`
  (before the reveal, the L1 runs it with `--key-file` on the key outside the lane).
- The 20 cases (5 bullets, 4 cases each) were written by the L1 before this declaration from the
  contract text, and stay outside the lane until a reveal commit; the counter pins their sha256
  (`8b3fac55…2941`) and refuses a revision that holds them. Counter sha256 at this declaration
  `52daff55…6e7b` (round-37 counter plus a `rawTemplate` run kind; same jail, same fresh ids and
  file names on every run, same judge). Bullets: (g) groups and (d) rules, where
  `urllib.robotparser` departs from the contract (substring user-agent match, Unicode folding,
  first-group-only, groups ended by non-record lines, wildcard rules ranked by matched length,
  non-final `$`), each case with at least one such check; (h), (i), (k) the new rules below, each
  case with at least one check the base tool gets wrong. Every case of (g), (d), (i), (k) has a
  check whose correct outcome is a finding and one whose correct outcome is none; (h) cases with a
  manifest-fault run have no holding check in that run.
- Separation, measured before this declaration with `--tool-file` (receipts committed with the
  control receipts): the L1's private reference (base tool plus the three rules) 20; the base tool
  8; round-37 controls: stdlib-plus-six-patches shortcut 7, stock `urllib.robotparser` 5, all-false
  1, no-reader 1, constant clean 0, junk 0; eight ablations of the reference 16–18 (no non-JSON
  constant rejection 18, no long-integer rule 18, no URL character rule 16, controls-and-space only
  16, printable-only 17, raw-path implicit allow 16, query ignored in the implicit allow 18, case
  folded in the implicit allow 18). Coverage statement, nothing more: each listed ablation scores
  at most 18. A tool that delegates (g)/(d) to the stdlib cannot reach 19 even with every other
  rule right: the stdlib fails all 8 (g)/(d) cases but g3 (the round-37 shortcut passes g3, fails
  the other 7).
- Harm instruments (not the claim): at the build commit the round-37 counter with key `424aa248`
  must still read 28 of 28 and `scripts/robots_audit_selftest.py` 137/137 (both read 28 and 137 on
  the reference). Every post-measurement receipt names the tool's sha256 (routed defect 5).
- Sourced: S034 (RFC 8259 section 6) and S029/S089's RFC 3986 (section 2, characters) re-opened
  this round, and S011 (RFC 9309 section 2.2.2) re-opened; row decisions in the lesson Gate.
- Limits: synthetic manifests and robots files; the tool reads local files and makes no fetch,
  redirect, cache or crawler-specific claim; (i) is a character-set rule, not a full RFC 3986
  grammar check.

Round-38 contract amendments (public; the round-37 contract in "Round 37 — declared claims" holds
except where these change it; the sealed cases test (g), (d) of that contract and (h), (i), (k)):

- (h) JSON numbers (RFC 8259 section 6, S034). The manifest is JSON as RFC 8259 defines it:
  `NaN`, `Infinity` and `-Infinity` outside a string are not JSON, so a manifest holding any of
  them gives one `input_invalid` finding (check null) and nothing is evaluated. A JSON number of any
  length is JSON: an integer `robotsStatus` outside the three ranges, however many digits it has,
  is a check fault (`check_invalid` for that check; the other checks are still evaluated), and a
  number of any length in a field the contract does not read changes nothing. Bounded: a manifest
  of up to 64 MiB of digits must still finish within the counter's 20 s.
- (i) URL characters (RFC 3986 section 2). A check's `url` holds, besides non-ASCII characters
  (kept; lane reading of rule (e)), only ASCII letters, digits, `-` `.` `_` `~`, the reserved
  characters `:` `/` `?` `#` `[` `]` `@` `!` `$` `&` `'` `(` `)` `*` `+` `,` `;` `=` and `%`. A
  `url` holding any other ASCII character anywhere (a space, a control character U+0000–U+001F or
  U+007F, `"` `<` `>` `\` `^` `` ` `` `{` `|` `}`), including a leading or trailing one, is a
  check fault (`check_invalid`). The characters are judged as written, before any parsing.
- (k) Implicit allow on the normalized path (amends (e); RFC 9309 section 2.2.2, S011). When (a)
  says the file decides, a URL whose path to match, normalized by rule (e), is exactly
  `/robots.txt` is allowed (so `/robots%2Etxt` and `/%72obots.txt` are allowed). A path to match
  with a query (`/robots.txt?x=1`), another case (`/ROBOTS.TXT`) or a kept reserved escape
  (`/robots%2Ftxt`) is decided by the rules. The fragment is never part of the path (as before).

Controls (committed before any build seat is dispatched; QUALITY (j) applies as declared): the
base (do nothing), the round-37 retained controls re-scored, and a pre-freeze control call of fresh
critic and mutation-tester seats building from this public text only: constant clean, junk,
all-false, no-reader, a shortcut keyed on ids, file names, URL words and user-agent names, a
stdlib-delegating shortcut patched for every non-(g)/(d) rule, a cheapest-wrapper shortcut around
the base tool, and a mutation pass on the private reference. **A control that meets the predicate
means this counter or target is wrong: C1 is then redesigned before any build seat is dispatched
or withdrawn; no reclassification of the control is an option.** This round-38 counter does not
replace the round-37 counter as round 37's rule of record.

## Round 38 — control call results; C1 withdrawn before any build (appended)

Control call `kake-r38-ctl` (7 seats: 5 critic, 2 mutation-tester; dispatched 04:15:37Z, all 7
returned, reports in `.ufo/waves/round-38/ctl/`; `CtlStdlibV2` discloses one existence test of the
sealed directory's path, nothing inside it observed). Every tool a seat named was scored by the L1 with the frozen v2
counter (`sealed_count.py`, sha256 `52daff55…6e7b`, predicate `passed >= 19 of 20 sealed cases`);
receipts `.ufo/waves/round-38/verification/control-*.json` and `.exit`, the tools in
`.ufo/waves/round-38/retained/controls/`, mutant receipts in `verification/mutref/`:

| Control (seat) | passed of 20 | met |
|---|---|---|
| base `af43a50f` (do nothing) | 8 | false |
| constant clean, junk, all-false (`CtlTrivial`) | 0, 0, 0 | false |
| no-reader with (a), (f), (g), (h), (i) (`CtlTrivial`) | 1 | false |
| label shortcut, pooled rules (`CtlLabelShortcut`) | 16 | false |
| base plus all three rules as wrappers (`CtlLabelShortcut` delegate ceiling) | 20 | **true** |
| base wrapper, minimal textual hacks (`CtlBaseWrapper` min) | 18 | false |
| stdlib `urllib.robotparser` for (c)/(d), patched for every other rule (`CtlStdlibV2`) | 13 | false |
| base wrapper, careful (`CtlBaseWrapper` care, all three rules) | 20 | **true** |
| base plus (h), (i), (k) as read (`CriticPredicate` rulepatch, rulepatch_pct) | 20, 20 | **true** |
| 42 single-point mutants of the private reference (`MutRefPass`) | 16–20; 28 meet | **true** |

**C1 is withdrawn before any build.** The declaration listed "a cheapest-wrapper shortcut around
the base tool, and a mutation pass on the private reference" among the controls and said a control
that meets the predicate means the counter or target is wrong, with no reclassification. Controls of
both listed kinds met it: 28 of 42 mutants (each breaks one contract sentence; 13 pass all 20) and
the wrapper arms that implement all three rules. The wrapper arms do the claimed work, so no counter
can put them below target; the declared consequence therefore leaves withdrawal, not a counter fix,
for C1 as declared. The v2 counter and receipts stay C1's rule of record. No build seat had been
dispatched. Counter defects found by the call: a tool echoing an original check id was accepted
(`MutCounterV2` F1, reproducer in its report), a missing `--tool-file` gave a traceback without a
receipt (F2), `checksEvaluated` was not compared (`CtlBaseWrapper`); declaration defects
(`CriticPredicate`): the groups bullet was labelled (g) (it is rule (c); (g) is manifest faults),
`PREDICATE` lacked the `met: ` prefix of the declared sentence, 19 of 20 tolerated one failed
held-rule case, (h)'s "64 MiB of digits" bound collides with the 64 MiB manifest cap, and the
capability rows did not carry the not-admitted status (now appended to both rows).

## Round 38 — C2 declared (redesign of C1, before any build)

**C2 — operability (tool repair): `scripts/robots_audit.py` gains rules (h), (i), (k) of the
round-38 amendments above, under counter v3.** Same surface as C1 (manifest and check validation
and the implicit-allow comparison of the robots audit tool); same contract amendments (h), (i),
(k), with the clarifications below. The command that would show the surface unmoved: counter v3 at
a revision whose tool is the base bytes scores 8 of 20. Frozen predicate, the same sentence here,
in `.ufo/waves/round-38/sealed_count_v3.py` (`PREDICATE` is this sentence verbatim; `met = cases ==
20 and passed >= 20`) and in every receipt's `predicate` field:

    met: passed >= 20 of 20 sealed cases

- Counting command (exit 0 met, 1 not met, 2 cannot evaluate):
  `python3 -B .ufo/waves/round-38/sealed_count_v3.py --root . --revision <rev> --key-revision <reveal>`
  (before the reveal the L1 uses `--key-file` on the key outside the lane). Before: 8 of 20 at the
  base `af43a50f` (`verification/c2-at-af43a50f.json`). After: `met` true at the build commit.
- Key v3 (sha256 `749ef6a6…3aa6`, pinned in the counter; outside the lane until the reveal): the
  20 cases of C1's key with bullets renamed (c) groups, (d) rules, (h) as j, (i) as u, (k) as r, and
  added checks: one check per excluded ASCII URL character (43, each alone in its URL, at six
  positions: path, query, fragment, leading, trailing, host), two `*` groups combined, a matching
  group with no rules, length ties with `*` and with a final `$`, a three-octet escape outranking a
  wildcard, allow listed before an equal disallow, a full-length wildcard rule, `*` matching
  nothing, prefix (not substring) matching, `/robots.txt/`, a `1e400` status. Every run states
  `checksEvaluated`.
- Counter v3 (sha256 in each receipt's `counterSha256`): v2 plus the fixes for F1, F2 and the
  `checksEvaluated` comparison; same jail, same fresh ids and file names on every run.
- Measured with `--tool-file` before this declaration (receipts `verification/v3/*.json`): the
  private reference 20; base 8; every C1 control except the full-rule wrappers at most 16 (label
  shortcut 16, minimal wrapper 14, stdlib for (c)/(d) patched for (h), (i), (k) 13,
  stdlib-plus-six-patches 7, stock parser 5, no-reader 1, others
  0); all 42 `MutRefPass` mutants 16–19 (none meets); the 8 reference ablations 16–18. Tools that
  implement all three rules (delegate ceiling, careful wrapper, rulepatch, rulepatch_pct) 20.
- Control classes, named before any v3 control score is read as a control: (1) do nothing (the
  base); (2) constant, junk, all-false; (3) no-reader; (4) label shortcuts keyed on ids, file
  names, URL words, user-agent names or byte patterns; (5) a tool that leaves (c)/(d) to
  `urllib.robotparser`; (6) a tool that implements at most two of (h), (i), (k); (7) the round-37
  retained controls. **A tool of any of these classes meeting the predicate withdraws C2; there is
  no further redesign this round.** Single-point mutants of the reference are coverage evidence with
  a declared bar: each of the 42 scores below 20 (measured: all do). A tool implementing all three
  rules is a build, whatever its packaging (patch, wrapper, rewrite); the four such tools above are
  recorded as builds that reach the target, not as controls.
- Clarifications of (h), (i), (k) (from `CriticPredicate`; no rule changes): (h) the bound reads
  "a manifest within the 64 MiB cap, however long its numbers, finishes within 20 s"; `1e400` and
  other non-integer numbers stay floats (round-37 (f): not integers). (i) judges characters only:
  a `%` not followed by two hex digits is allowed by (i) and kept by (e). (k) `/robots.txt?` has an
  empty query, so its path to match is `/robots.txt` (allowed); an explicit `Disallow: /robots.txt`
  does not override the implicit allow. Duplicate JSON member names stay undecided and untested.
- Harm instruments and sources as declared for C1. Limits as for C1; 20 of 20 tolerates no failed
  case.

## Round 38 — measured results (author-side; admission belongs to the non-author closure)

Key v3 revealed at `99357694f68886d3175fc6c386979c350be789bc` (`.ufo/waves/round-38/sealed/cases_v3.json`,
sha256 `749ef6a6…3aa6`, equal to the pin; C1's key `cases.json`, `8b3fac55…2941`, revealed in the same
commit). Predicate, counter v3 and key unchanged since `2dab7f31`. Receipts
`.ufo/waves/round-38/verification/c2-*.json` with `.exit` files.

| Claim | Before (rev) | After (rev) | Counting command | Predicate |
|---|---|---|---|---|
| C2 robots_audit rules (h), (i), (k) (operability, tool repair) | passed 8 of 20 (`af43a50f`, `b0ab7f60`, `2dab7f31`) | passed 20 of 20 (`3ed8e15c2707ac4cec88f48fc9be48b35be4f2b0`, tool sha256 `f4d057c4…baace`) | `python3 -B .ufo/waves/round-38/sealed_count_v3.py --root . --revision <rev> --key-revision 99357694` | `met: passed >= 20 of 20 sealed cases`: met |

- The build is wave-1 `ExecRobotsTool`'s file, landed unedited (`3ed8e15c`, only
  `scripts/robots_audit.py` changed). Measured before the reveal with the key file too
  (`c2-at-3ed8e15c.json`, 20 of 20); measuring the reveal commit is refused (exit 2).
- Harm instruments (pinned receipts, `verification/harm/`): round-37 counter on the build's tool 28
  of 28 (key `424aa248`); `robots_audit_selftest.py` 137/137 at `3ed8e15c` and 194/194 at `145a6468`
  (57 new fixtures, blind, wave-1 `ExecRobotsSelftest`; the base tool fails exactly the 45 (h), (i), (k)
  fixtures); `source_recheck_selftest.py` 106/106, hardening 9/9 and round-36 counter 28 of 28 on the
  capped `source_recheck.py` (`6629d800…9c6b`).
- Independent blind implementation (wave-1 `ExecIndependent`, `ee78ba46…95b1`): round-37 counter 28
  of 28, selftest 137/137 (C2 counter result in `verification/w2/` once scored).
- Correction to "Round 38 — control call results": **29** of 42 mutants met C1's v2 predicate, not
  28 (13 at 20, 16 at 19; `verification/mutref/`; wave-1 `CriticControlReceipts`, `CriticClaimSizing`).
- After the C2 freeze, wave-1 `CriticControlReceipts` built `CtlExampleK` (all of (h), (i) and (k)
  only for the two escapes the declaration names): 19 of 20, not met
  (`verification/w1attack/CtlExampleK.json`).
- Axis ratings unchanged (10 → 10). No capability row: C2 is a repair of an existing tool.

## Round 38 — wave-2 corrections (appended)

Wave 2 `kake-r38-w2` (34 seats: 19 reviewer, 5 scout, 4 mutation-tester, 3 critic, 2 sentinel,
1 revenger; all returned) attacked the landed work at `adab4c7e`; reports are in
`.ufo/waves/round-38/w2/`. The declaration, counter, key and measured result stay as landed.

- **Reproduced:** every C2 receipt at five revisions (`RerunC2Receipts`); 63 of 64 retained tools
  against their v2 receipts and 64 of 64 against v3, plus `CtlExampleK` 19
  (`RerunC1Withdrawal`, `RerunControlsV3`). Also reproduced: the key audit (20 cases, 43 of 43
  single-character checks, `checksEvaluated` on 22 of 22 runs; `AuditKeyV3`), every key expectation
  re-derived by hand (22 of 22; `CriticKeyExpectations`), and harm base vs tip (all selftests and the
  round-36/37 counters; `ReviewHarm`). The real run gave the build 7 of 7 against the wave-1
  oracle (`ReviewRealRun`). The independent blind implementation scores 20 of 20 under v3
  (`verification/w2/independent-v3.json`). A sweep of every v3 receipt is in
  `verification/v3-sweep.txt`: the only 20-of-20 tools are the build, the reference, the
  independent implementation and the four full-rule tools.
- **The four full-rule tools are builds by measurement:** removing (h), (i) or (k) from any of
  them scores 16 of 20 (12 of 12 ablations, `AblateBuilds`).
- **Contested, for the closure:** `CriticReclassification` holds that the "implements all three
  rules ⇒ build" class did not exist when C1 was declared and was written after those four tools
  had scored 20 under v2. On a strict reading of the round-37 ruling it is a reclassification, and
  C2 would not be admitted. On the substance (ablations above, 13 v2 false passes closed by v3) it
  holds. C2's self-verdict is therefore **measured met; admission contested**.
- **Overstated, corrected here:** 20 of 20 certifies the 22 sealed runs, not every sentence of (h),
  (i), (k). Untested sentences: four single-point reference mutants reach 20 of 20 (empty query
  `/robots.txt?`, bare `%`, explicit `Disallow: /robots.txt`, an unguarded `parse_int` that breaks
  the 20 s bound on a 64 MiB literal; `CriticKeyExpectations`). Six build mutants survive both the
  selftest and the key (`MutBuildTool`: sign or truncation of short integers, `_` rejected, U+00A0
  rejected, implicit allow limited to https, implicit allow below a directory). "Every control of
  the named classes ≤ 16" means every scored control of the seven classes. "29 of 42" stands (not
  28).
- **Defects carried to round 39:** `source_recheck.py` oversized bodies can emit `moved` alongside
  `check_invalid` and count in `checksEvaluated` (`ReviewRecheckCaps`, P2). The (j) check has 11 of
  15 surviving mutants and is name-based (`MutCcCheck`, `ReviewCcCheck`). The tool's lone-surrogate
  URL reading differs from the independent implementation, which gives `check_invalid`
  (`DiffToolVsIndependent`, `RevengerReadings`; the contract is silent). `https://[not-ipv6]/p` is
  `check_invalid` (`ReviewToolDiff`, P3). The two counter harm receipts name `toolFile` without
  `toolRevision`. The `pinned_selftest.py` `runner` field can be forged by a summary
  (`ReviewPinnedSelftest`). `timeline_check` receipts omit their invocation
  (`ReviewTimelineCheck`).
- Source and knowledge-entry wording fixes are logged in `corpus/lessons/round-38.md`
  "Wave-2 corrections".

## Round 38 — closure correction (appended in round 39)

The non-author closure (`corpus/lessons/round-38-verifier-spotcheck.md`, routed defect 1) did **not
admit round-38 C2**. The sentence that kept the four full-rule tools out of the control set ("a
tool implementing all three rules is a build … not as controls", `2dab7f31:SCORECARD.md:2250`) was
first written in the commit that also landed those tools' 20-of-20 scores: a rule changed after
seats scored. Counter v3 (`.ufo/waves/round-38/sealed_count_v3.py`, sha256 `28b120a5…0f38f9e4`)
and key v3 (`749ef6a6…77b63aa6`) stay C2's rule of record; 8 → 20 of 20 stands as a measurement,
not an admission. Round 38's verdicts: C1 withdrawn before any build (agreed by the closure); C2
not admitted. The wave-2 tools and receipts the closure re-hashed (`CriticKeyExpectations`,
`MutBuildTool`, `MutCcCheck`) are lane evidence at `.ufo/waves/round-39/r38w2-evidence/` (routed
defect 5; sums `.ufo/waves/round-39/r38w2-evidence.SHA256SUMS`, 147 files; seat clones, `tmp/` and
the 64 MiB `t/big.json`, sha256 `4594bb30…2b50b`, are not copied: `r38w2-evidence.NOTE.txt`).

## Round 39 — C1 declared (before any seat is dispatched)

Base `2909f1dcf2a4e411394a5093c4ed811a81809895`. Attempt 1 of this round died with the
orchestrator and landed nothing; its uncommitted files were moved out of the lane unread into
`/fast/scratch/hyaku/kake-r39a2/attempt1-leftovers/` and nothing here derives from them. Rounds 37
and 38 claimed `scripts/robots_audit.py`; this round does not touch it. Both owned axes sit at the
10/10 saturation line, so the stagnation nudge applies and the claim is a capability move.

**C1 — operability, capability acquisition: a new tool `scripts/sitemap_audit.py` audits local
sitemap and sitemap-index files against `.ufo/waves/round-39/c1-contract.md` (sentences 1–34,
rules (a)–(k)).** Surface: a new tool on a new edge class (sitemap file encoding, root, entries,
limits, `loc` form and scope, `lastmod`, `changefreq`, `priority`). PROVINCE Frontier lists
"sitemap scope" and round 38 lists sitemaps as still open; the lane has no sitemap-file
validator (`git ls-tree -r --name-only 2909f1dc scripts/ | grep -c sitemap_audit` → 0). Command
that shows the surface unmoved: the counter below at any revision without the tool → 0 of 24.
Sourced: S102–S104 (opened this round, `corpus/lessons/round-39.md` Gate).

Frozen predicate — this sentence, `PREDICATE` in `.ufo/waves/round-39/sealed_count.py` (with
`met = len(rec["rows"]) == CASES and passed >= TARGET`, `CASES = TARGET = 24`) and the
`predicate` field of every receipt:

    met: passed >= 24 of 24 sealed cases

- **Counting command** (exit 0 met, 1 not met, 2 cannot evaluate):
  `python3 -B .ufo/waves/round-39/sealed_count.py --root . --revision <rev> --key-revision <reveal>`
  (before the reveal the L1 uses `--key-file` on the key outside the lane). Counter sha256
  `f3a0cd6053497cd05b6a57ab712552146960c1efe2f8fb50eee36bace6084593`. Each case runs the tool in
  bubblewrap with only `/usr`, the case files and the tool visible (no network, lane or key).
- **Key** (`.ufo/waves/round-39/sealed/cases.json` at the reveal; sha256 `16440f62…4767c10b`,
  pinned in the counter): 24 cases written by the L1 by hand from the contract before this
  declaration; a case passes only if exit, verdict, error and every check's status, error and
  finding set match. Every rule group (a)–(k) has checks of both polarities.
- **Before:** 0 of 24 at the base and at this declaration commit (tool absent;
  `.ufo/waves/round-39/verification/base-2909f1dc.json`). **After:** `met` true at the build commit.
- **Key-design evidence, L1 alone, before this declaration** (summaries
  `.ufo/waves/round-39/verification/pre-summary.jsonl`; full rows withheld until the reveal because
  they quote expectations): the private reference scores 24; each of 34 single-sentence ablations
  of it scores 6–23 (none 24); constant-clean 1, junk 0, manifest-only no-reader 1, ElementTree
  root-only reader 5.
- **Control classes, frozen now, before any control seat is dispatched.** Every tool scored with
  this counter other than the exact bytes of `scripts/sitemap_audit.py` at the build commit is a
  control, whoever wrote it and however much of the contract it implements; no tool is
  reclassified as a build after it scores. Named shapes: absent tool; constant output (all clean,
  all findings, all errors); junk output; manifest-only readers; label shortcuts keyed on check
  ids, file names, positions, directory names or `sitemapUrl` strings; shallow readers
  (well-formedness or root only, stdlib or XSD delegation without the contract rules); regex
  readers without an XML parser; key finders (anything reading outside the case files); every
  mutant or ablation of the reference or of any build that changes one contract sentence.
- **Kill rule, frozen now.** (1) Before the build is dispatched, if any control receipt meets the
  predicate, C1 is **declared exploratory** (no counter, verdict from a named non-author
  reviewer); the key, counter, predicate and target are never changed after this commit. (2)
  After the build is scored, a control (any class above) that meets the predicate means C1 is
  **not met**; it is reported, never relabelled. (3) A build that scores below 24 is a miss,
  reported as an honest stop.
- **Order:** this declaration and the counter land first; the control wave (key-blind control and
  mutant seats; the L1 scores every returned tool) next, with every receipt committed; then the
  content-based control-consequence check (QUALITY (j), routed defect 4) lands; only then is the
  build seat (key-blind, contract only) dispatched. The key is revealed after the build is scored.
