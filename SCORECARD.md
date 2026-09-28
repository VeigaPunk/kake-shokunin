# kake-shokunin — Scorecard

Axes owned by this lane: **operability + freshness** (MISSION.md fleet-2;
depth/coverage/calibration/adjacency belong to other lanes — not scored here).

| Axis | Score | Evidence pointer | Last change |
|---|---|---|---|
| operability | 8 | `scripts/probe-delta.mjs` landed + verified (real history: 6 events / 0 phantom; exit 0/2/64 proven; input validation per critic falsifiers); checklist audit measured: 33/33 commands + 60/60 cited paths resolve (Scout r10), 5 verbs executed live with 2 undocumented CLI behaviors landed (`status` exit-1 `src/cli.mjs:99`; kimi-surface no `--help` `:1197-1198`); 3 citation defects found+fixed (ExecutorB/Scout r10). Before r10: 6 (checklists partially executable, no runnable alert artifact, suite executability unmeasured — LOG r3/r7/r9) | round 10 |
| freshness | 8 | No live-surface re-probe this round (probe-latest 2.07h fresh at audit, 12 ok/5 violated/1 error, 0 new); corpus record drift caught+corrected instead (r5 veigapunk window 09-21T03:32:06→04:14:50, not 04:14→09-22T22:58) — freshness benefit counted under operability, no double-count | round 9 |

## Planned

- **round 11 (both owned axes at 8 — pick at round open):** operability
  residual = only 3 of ~20 free-read verbs executed live (r10 audit; the rest
  cite LOG rounds) — execute the live subset (`probe <id>`, `sync-check`,
  `reconcile`) if probe-latest is fresh; **or** freshness move — fresh
  `probe --all` + PQ-ledger/marker re-verification if probe-latest is >6h
  stale at round open.

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 10 | operability | 0 scripts in repo; alerting "undecided" (README gap since r5); checklist executability unmeasured; naive history diff = 42 events / 40 phantom | detector landed+verified (6 events/0 phantom on 76 rows; exit 2/64 proven); 33/33 cmds + 60/60 paths resolve; 2 CLI traps + 3 citation defects landed/fixed; r5 record corrected (03:32:06→04:14:50) | `scripts/probe-delta.mjs`, `corpus/knowledge/probe-delta-alerting.md`, LOG.md r10, /tmp/kake-r10/* lane reports |

## Retired

- none. No saturation or wrong-fit evidence for either owned axis.
