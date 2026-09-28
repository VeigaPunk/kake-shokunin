# kake-shokunin corpus

Memory for the web-properties & publishing domain (ds4cc.com, kimi.page/pro
mirrors, Pages deploys).

## Layout

- `knowledge/` — domain facts with citations (file path, command output, URL).
- `lessons/` — per-round lessons citing LOG.md round + evidence.

## Coverage map

| Area | Entry | Coverage |
|---|---|---|
| Fleet registry & tripwires | `knowledge/fleet-registry.md` | all 21 rows, expect semantics, pruning rules |
| Publish channels | `knowledge/publish-channels.md` | GHP push-to-main, Render apps-sdk, kimi surface verbs |
| Drift detection | `knowledge/drift-detection.md` | probe / sync-check / reconcile / kimi-map; byte-vs-marker semantics |
| Mirror pitfalls | `knowledge/mirror-pitfalls.md` | kimi byte rewriting, no dir indexes, one-chat-one-slot, dead slots |
| Fire journals & exit codes | `knowledge/fire-journal-codes.md` | state/*.json journal anatomy, exit codes 1–8/64, meter-consumption truth |
| Ops automation | `knowledge/ops-automation.md` | systemd 6h probe + daily keeper timers, probe-history semantics, full CLI verb table, bots fleet |
| Origin repos | `knowledge/origin-repos.md` | 50-clone canonical-source map, byte-verified writers, 5 sourceless artifacts |
| Speedrun pipeline | `knowledge/speedrun-pipeline.md` | record→report→prep→operator-push→X-draft; redaction + fail-closed rules |
| Round lessons | `lessons/round-1.md`, `round-3.md`, `round-4.md`, `round-5.md` | audit findings; fresh-probe corrections; journal decoder; automation+repo layer |

## Known gaps

- The five sourceless kimi artifacts (`origin-repos.md` table) still have
  no Origin repo — extraction is operator-gated, unchanged since 2026-09-21.
- GHP subpath rot beyond `index.html` is still invisible (`reconcile`
  covers index only) — no spotcheck tooling exists yet.
- kimi `apiv2` authenticated ops are capability-recorded but intentionally
  unwired; any change there is a new round's work.
- `webzites-probe.timer` provides 6h coverage; whether the operator wants
  alerting on `violated[]` deltas (vs the current silent log) is undecided.
