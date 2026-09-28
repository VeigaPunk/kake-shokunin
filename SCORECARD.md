# kake-shokunin — Scorecard

Axes owned by this lane: **operability + freshness** (MISSION.md fleet-2;
depth/coverage/calibration/adjacency belong to other lanes — not scored here).

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| operability | 10 | Every free-read verb in the domain is now **live-executed on the real repo with a byte-level write-free proof**: r11 closed probe/status/reconcile/sync-check; r12 closed the last 4 (`status --json` exit 0 with 5 violated+1 error in snapshot; `grokbots --check` exit 1 lucario; `bots list` exit 0 20 keepers; `bots report` exit 1 gaps) — 31-file state sha guard identical before/after, re-verified by 2 independent L2 re-runs. Exit-1 predicates pinned to code (gaps `cli.mjs:935`, stale-only-with-flag `:836-839`/`:932`, checked=21 `:393`); replica edge matrix (corrupt/deleted snapshot, registry faults, `--stale` variants) landed. The automation layer is now runtime-verified, not unit-file-trusted: keeper timer never fired (enable-vs-retire at L0), scribe push-gate failing (N1), lucario registry gap at L0. Corrected cmdProbe merge patch replica-verified and staged for the webzites owner (`corpus/handoffs/cmdProbe-merge-fix.md` — r11 F1 guard refuted on the `probe <id> --all` edge). Full verb free-read/writer classification (35 rows) code-verified. | round 12 |
| freshness | 8 | No fleet re-probe needed (probe-latest 3.4h fresh at open → operability per r11 plan; next 6h sweep 00:00:59Z). r12 re-verification still landed: r5 "keeper timer runs daily" claim re-checked against live runtime — FALSE (never fired; logs frozen 09-21), corrected in corpus+SKILL; charter-ghp marker re-verified live (still `2026-09-28 scribe beat (`; pin still `2026-09-26` → config-lag + human-edit, PQ-12 relabeled); scribe push-gate status re-read (3 beats failing since 06:05Z). History row 77 = r11 sanctioned spot row, suppressed in deltas. | round 12 |

## Planned

- **round 13 (pick at round open):** freshness move — probe-latest will be
  >6h stale by then (next sweep 00:00:59Z; if the sweep lands, re-read it and
  verify the 18-row pattern + charter-ghp pin FAIL persists or flips on a
  scribe push); re-verify PQ-5 (human Publish click may have happened) and
  PQ-2 mirror delta; check whether L0 answered the keeper-timer/lucario/
  cmdProbe questions and route accordingly. If operability resurfaces
  (L0 answers arrive), the follow-up is operator-gated execution support,
  not new verb audits — the free-read surface is saturated (see Retired
  note).

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
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
