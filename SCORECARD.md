# kake-shokunin — Scorecard

Axes owned by this lane: **operability + freshness** (MISSION.md fleet-2;
depth/coverage/calibration/adjacency belong to other lanes — not scored here).

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| operability | 9 | Free-read verb suite **fully live-executed** (r11 closed the r10 residual: `probe <id>`, `sync-check`, `grokbot reconcile` + `status` variants, all on the real repo, backup-guarded where writing). Central finding: `probe <id>` **clobbers the 18-row fleet snapshot to 1 row** (18→1 live; status exit 1→0 while clobbered, masking 5 violated + 1 error) — unintended defect, not spot-probe semantics (webzites-side archaeology: merge intent comment `fleet.mjs:27-29`, fix applied to `tick`/`bots task` in the r2 era but `cmdProbe:78` left raw; 11 `total:1` rows in history). 7 undocumented CLI behaviors landed: probe unknown-id exit 2 + HELP no-write (`cli.mjs:1097-1101`); `status --json` always exits 0 (`:94-97`); plain status exit 1 is **snapshot-relative** (`:99`); reconcile `NOSRC`/`no-source-file` silently exit 0 (`:269-272`); reconcile unknown-id = crash exit 1 + stack (un-awaited `:1086`); sync-check `--all`/`--dead` real but undocumented (`kimi-surface.mjs:184-190`); sync-check bad-set stricter than reconcile's (`:206`). Landed: `corpus/knowledge/free-read-verbs.md` (4 verb cards, 3-universe model, state-persistence model, live-run provenance); SKILL.md step-1 spot-probe trap + backup/restore recipe, status-exit sharpening, write-path cite fix (`cli.mjs:998-1002`→`:78` — was the install template), 3 drift-table rows, cited-paths entry. Sentinel: exactly 2 sanctioned state writes (history +1 `total:1` line, clobber→restore byte-identical), zero unsanctioned. | round 11 |
| freshness | 8 | No fleet re-probe needed (probe-latest 2.6h fresh at round open → operability move per plan); the one `total:1` history append is the sanctioned spot row, spot-rule-suppressed in deltas; r11 live verbs re-read every live URL surface (reconcile 21 rows, sync-check 9 rows) with zero verdict drift vs the 18:51Z snapshot. | round 11 |

## Planned

- **round 12 (pick at round open):** freshness move — if `probe-latest.json` is
  >6h stale at open, run `probe --all` + PQ-ledger/marker re-verification
  (charter-ghp beat-pin was 2×FAIL at r7; check whether the keeper re-pinned
  it); else operability residual — live-run the remaining replica-verified
  free-reads on the real repo (`status --json`, `grokbots --check`, `bots
  list`/`report` — all read-only per `cli.mjs`) and file the `cmdProbe` merge
  fix as a webzites-owner handoff (one-line patch proposal exists in
  `/tmp/kake-r11/scout-verbs.md` F1 — kake never edits webzites source).

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 11 | operability | 3 of ~20 free-read verbs never live-run (r10 audit); `probe <id>` recommended in SKILL.md drift table with no side-effect warning; `status` exit-1 documented as unconditional | All 4 core free-read verbs live-run on the real repo (probe ds4cc-com exit 0 + 18→1 clobber + restore; status clobbered/restored exits 0/1; reconcile 3 runs exit 0/0/1 fleet 7-attention; sync-check 6 runs incl. bare-fleet exit 1 {ok:3,attention:6}, --dead 0, unknown-id 1, unknown-verb 64); snapshot-clobber trap + 7 CLI behaviors + merge asymmetry landed in corpus + SKILL.md; 1 citation defect fixed | `corpus/knowledge/free-read-verbs.md`, SKILL.md r11 amendments, LOG.md r11, `/tmp/kake-r11/` (13 L2 artifacts: labrat-probe/reconcile/sync, scout-verbs, revenger-merge, critic, reviewer, sentinel, executor×2, planner, connector, scribe) |
| 10 | operability | 0 scripts in repo; alerting "undecided" (README gap since r5); checklist executability unmeasured; naive history diff = 42 events / 40 phantom | detector landed+verified (6 events/0 phantom on 76 rows; exit 2/64 proven); 33/33 cmds + 60/60 paths resolve; 2 CLI traps + 3 citation defects landed/fixed; r5 record corrected (03:32:06→04:14:50) | `scripts/probe-delta.mjs`, `corpus/knowledge/probe-delta-alerting.md`, LOG.md r10, /tmp/kake-r10/* lane reports |

## Retired

- none. No saturation or wrong-fit evidence for either owned axis.
