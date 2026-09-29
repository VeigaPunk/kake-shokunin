# kake-shokunin — Scorecard

Axes owned by this lane: **operability + freshness** (MISSION.md fleet-2;
depth/coverage/calibration/adjacency belong to other lanes — not scored here).

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| operability | 10 | Every free-read verb in the domain is now **live-executed on the real repo with a byte-level write-free proof**: r11 closed probe/status/reconcile/sync-check; r12 closed the last 4 (`status --json` exit 0 with 5 violated+1 error in snapshot; `grokbots --check` exit 1 lucario; `bots list` exit 0 20 keepers; `bots report` exit 1 gaps) — 31-file state sha guard identical before/after, re-verified by 2 independent L2 re-runs. Exit-1 predicates pinned to code (gaps `cli.mjs:935`, stale-only-with-flag `:836-839`/`:932`, checked=21 `:393`); replica edge matrix (corrupt/deleted snapshot, registry faults, `--stale` variants) landed. The automation layer is now runtime-verified, not unit-file-trusted: keeper timer never fired (enable-vs-retire at L0), scribe push-gate failing (N1), lucario registry gap at L0. Corrected cmdProbe merge patch replica-verified and staged for the webzites owner (`corpus/handoffs/cmdProbe-merge-fix.md` — r11 F1 guard refuted on the `probe <id> --all` edge). Full verb free-read/writer classification (35 rows) code-verified. | round 12 |
| freshness | 9 | r15: the armed-watches read was pure re-verification (PQ-12 `PERSIST` — pin `2026-09-26` vs live `2026-09-29 scribe beat (` / `fb365e38…` == remote+clone `9c28d29`; PQ-5 still pending 404/13,409B/`93ddca9a…`; PQ-2 gate closed, remote `e6bd071` unchanged, still 20 unpushed) — but the **path-citation re-sweep caught the drift event**: 58 unique cited paths re-tested under the kasegi-reported `~/Projects` mtime window (2026-09-28T23:51:31Z) → 49 resolve, 5 genuine danglers incl. `ufofsdbeta` + `ufofsdbeta-kimi-review` (present at r1, gone now) + `ephemeral/wz1`; dated annotations landed in SKILL.md/mirror-pitfalls/publish-channels + a per-round re-sweep rule; critic re-ruling (complete sweep > sample) made it move-eligible. publish-queue.md §r15; LOG r15. | round 15 |

## Planned

- **round 16 (pick at round open):** freshness default — continue the armed
  **PQ-12 dated re-check loop** (five states `PERSIST | EDIT-LANDED |
  CHURN-AGAIN | SILENT | ANOMALY`: `PERSIST` if pin still `2026-09-26` vs
  live `2026-09-29 scribe beat (`; `EDIT-LANDED` if the operator re-pins —
  row flips ok on the NEXT full sweep after the edit, the first EXIT since
  09-27T06:22Z; `CHURN-AGAIN` if a 09-30 beat lands first — next scribe
  fire ~06:06Z, push leg working but telemetry degraded: grok-web 300s
  timeout + kimi route failure → local-fallback beats) + **PQ-5 watch
  read** (P1 sentinel check → still pending = one curl; if E1 fires the
  E-chain is move-eligible) + **PQ-2 re-verify** (19/93, gated on the 20
  unpushed ds4cc commits — remote `e6bd071` at r15 close) + **path-sweep
  cadence** (re-run the `test -e` sweep over the cited base every round
  while FS drift is live — r15 caught 5 danglers; r10's "60/60" is retired
  as a standing claim). Note: r15 opened 00:44:25Z, BEFORE the 06:00:59Z
  sweep (r14's plan premise was wrong) — the first post-06:00:59Z round
  carries new row 79 (row 80 once the 12:00:59Z sweep lands): check for a
  `charter-ghp` EXIT or any `violations→ok` flip, run probe-delta rows
  78→79/80. L0 keeper/lucario answers: still unanswered at r15 close —
  same operator-gated support applies; the kasegi `~/Projects/bounties`
  vanish is a sibling item with 0 kake citations — monitor only. PQ-3's
  `git pull --ff-only` precondition stays cleared (`9c28d29`); pull/fetch
  in `origin-work/*` still needs explicit sanction under the read-only
  contract.

## Move log
| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 15 | freshness | Path-citation base trusted on r10's un-re-measured "60/60 resolve"; PQ-2 cell's "root content-frozen" ambiguous (mirror-vs-canonical misattribution in the r15 brief); canonical side described as "working-tree-only" when files ARE tracked-but-unpushed; normalization method for the mirror freeze metric not pinned; r14 plan-note asserted r15 opens post-sweep | 58 cited paths re-swept under the 09-28T23:51:31Z `~/Projects` drift window: 49 resolve, **5 genuine danglers caught** (ufofsdbeta + .ufo + ufofsdbeta-kimi-review vanished in-window; ephemeral/wz1 emptied 21:42-03:00) — all annotated with dated flags, per-round re-sweep rule landed; PQ-12 loop read `PERSIST` with all four non-PERSIST states evidence-excluded; PQ-5 armed-watch read PENDING (P1–P3 hold, E1 never fired); PQ-2 gate confirmed closed (remote `e6bd071`, 20 unpushed); PQ-2 cell + canonical wording + normalizer-variance corrections landed; sentinel 47/47 byte-identical across the round | corpus/knowledge/publish-queue.md §r15 + PQ-2 row erratum; SKILL.md FS-traps rule + 3 absent-annotations; mirror-pitfalls.md ×2; publish-channels.md ×1; LOG.md r15; `/tmp/kake-r15/` (12 L2 artifacts + sentinel sha pair + fetch bodies) |
| 14 | freshness | Standing claims carried stale precision: r13 "byte-frozen" root claim wrong at sha level (Cloudflare cfemail re-encoding); r13 `06:00:36Z` was the journal Starting line not the history `at`; ops-automation "earlier full sweeps" wording backwards; 10+ line-number citations drifted as source/docs grew; no armed verdict path for the pending PQ-5 publish; no dated re-check loop on the operator-gated PQ-12 pin | Sweep landed mid-round and verified (row 78 `at` 00:01:09.976Z, identical 12/5/1); sentinel PASS 45/47 unchanged (timer pair only); 18-curl replication 0-diff; PQ-5 watch armed (P1–P3 verified NOW + E1–E5 + F1–F3 branches — `publish-queue.md` §r14, `SKILL.md` step 4); PQ-12 loop armed and **caught a transition in-round** — scribe `9c28d29` pushed `pushed:true` at 00:06:19Z, live literal moved to `2026-09-29` (53,386B `fb365e38…`); 12 stale citations fixed across 4 corpus files + LOG + the r13 report; 2 new facts landed (generic-sentinel non-discrimination; canonical sitemap wire-absent); charter subpath audit NULL baseline landed; r13 report-filing gap repaired; score stays 8 — armed capability ≠ caught event (critic rule) | `/tmp/kake-r14/` (12 L2 artifacts incl. sentinel-{before,after}.sha), corpus/knowledge/{publish-queue,ops-automation,keeper-timer-inert,free-read-verbs}.md, SKILL.md step-4 watch wiring, LOG.md r14 |
| 13 | freshness | corpus aging: pin-failure framed as "two consecutive probes" (r3+r7); PQ-3 "behind 2", PQ-6 wrong line cite, PQ-5 zip "1 day stale", ops-automation header "76 rows"; "churn paused" unqualified; no at-vs-mtime rule; no absent-semantics rule; r12 commits missing in BOTH repos (round-11 was kake head; main head round-6) | Standing claims re-verified against live state 22:47–22:50Z (3 timer sweeps + manual re-probe identical 12/5/1; 18-curl replication 0-diff; PQ-5 pending, PQ-2 unchanged 19/93; pin-lag persists over deploy-current a8f1e2b); 4 stale citations fixed, 2 rules landed (at-vs-mtime; absent = exact-pin miss), 1 claim rescoped (churn-paused → scribe-automation-only); r12 protocol gap repaired (round-12 commits landed + pushed in both repos); score stays 8 — plan's trigger never materialized, no falsifiable move | `/tmp/kake-r13/` (10 L2 artifacts incl. sentinel-before.sha), corpus/knowledge/{publish-queue,ops-automation,keeper-timer-inert}.md, SKILL.md r13 amendments, LOG.md r13 |

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
