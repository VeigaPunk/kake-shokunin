# kake-shokunin — Scorecard

Axes owned by this lane: **operability + freshness** (MISSION.md fleet-2;
depth/coverage/calibration/adjacency belong to other lanes — not scored here).

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| operability | 10 | Every free-read verb in the domain is now **live-executed on the real repo with a byte-level write-free proof**: r11 closed probe/status/reconcile/sync-check; r12 closed the last 4 (`status --json` exit 0 with 5 violated+1 error in snapshot; `grokbots --check` exit 1 lucario; `bots list` exit 0 20 keepers; `bots report` exit 1 gaps) — 31-file state sha guard identical before/after, re-verified by 2 independent L2 re-runs. Exit-1 predicates pinned to code (gaps `cli.mjs:935`, stale-only-with-flag `:836-839`/`:932`, checked=21 `:393`); replica edge matrix (corrupt/deleted snapshot, registry faults, `--stale` variants) landed. The automation layer is now runtime-verified, not unit-file-trusted: keeper timer never fired (enable-vs-retire at L0), scribe push-gate failing (N1), lucario registry gap at L0. Corrected cmdProbe merge patch replica-verified and staged for the webzites owner (`corpus/handoffs/cmdProbe-merge-fix.md` — r11 F1 guard refuted on the `probe <id> --all` edge). Full verb free-read/writer classification (35 rows) code-verified. | round 12 |
| freshness | 8 | r13 full re-verification landed (probe-latest 3.9h fresh at open — the plan's >6h-stale trigger never materialized, so no falsifiable score move existed; 8 per critic): 3 timer sweeps + 1 manual re-probe today all identical 12-ok/5-violated/1-error + 18-curl live replication 22:50Z **0 verdict diffs**; PQ-5 re-verified pending (live stub sha `93ddca9a…` == 09-26 journals, 0 fires since 09-26T15:34Z, `kimi-map` 09-26-vintage caveat); PQ-2 unchanged (19/93 served, 74 missing, 0 transitions); charter-ghp pin-lag persists over **deploy-current** live (human pushed `b74190e…a8f1e2b` 18:32–20:43Z, Pages served each within ~30s; "churn paused" rescoped to scribe-automation-only); L0 keeper/lucario question still unanswered; 4 stale citations fixed; 2 rules landed (**at-vs-mtime** freshness read; `observed:"absent"` = exact-pin miss, never marker loss). | round 13 |

## Planned

- **round 14 (pick at round open):** freshness default — the 00:00:59Z
  sweep will have landed (re-verify the 18-row pattern held; charter-ghp
  pin FAIL persists **unless** the operator lands PQ-12's one-line
  `fleet.config.json:256` edit, in which case the row flips ok — the
  first EXIT since the 09-27T06:22Z ENTER); re-check PQ-5 (operator may
  Publish card `efc1830`) and the charter human-push series
  (`b74190e…a8f1e2b` may continue; local clone still 5 behind —
  `git pull --ff-only` is the first act of any charter work); PQ-2
  advance stays gated on the 20 unpushed ds4cc commits. If L0 answers
  arrive (keeper timer, lucario registry row), follow-up is
  operator-gated execution support, not new verb audits — the free-read
  surface is saturated (see Retired note).

## Move log
| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
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
