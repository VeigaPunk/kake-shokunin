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
