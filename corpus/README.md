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
| GHP subpath spotcheck | `knowledge/ghp-subpath-spotcheck.md` | probe/reconcile coverage math, `in-sync` masking, origin/main classification, first baseline (2 352 paths, 0 rot) |
| Sitemap/orphan audit | `knowledge/sitemap-orphan-audit.md` | URL-list→live sweep, GHP orphan impossibility proof (deploy = full-tree artifact), first baseline (103 locs, 0 orphans/dead), charter marker day-2 churn |
| kimi subpath audit | `knowledge/kimi-subpath-audit.md` | link sweep + sitemap parity; ds4cc mirror 74/93 canonical locs missing all post-vintage (0 rot); `dir/` hrefs live-dead on kimi |
| Round lessons | `lessons/round-1.md`, `round-3.md`…`round-8.md` | audit findings; fresh-probe corrections; journal decoder; automation+repo layer; subpath spotcheck; orphan audit; kimi subpath audit |

## Known gaps

- The five sourceless kimi artifacts (`origin-repos.md` table) still have
  no Origin repo — extraction is operator-gated, unchanged since 2026-09-21.
- Live-only orphan paths: **closed 2026-09-28** — GHP Pages deploys are
  full-tree artifacts, so the served set ≡ `origin/main` tree; the round-7
  sitemap sweep (103 locs) found 0 orphans/dead listings. kimi subpaths:
  **closed 2026-09-28 round 8** — link sweep + sitemap parity baseline
  (`kimi-subpath-audit.md`). Residual: JS-rendered link surfaces (vault
  PROPERTIES[]) need rendered DOM; rows with no URL list (`lucario` GHP is
  2 files — already total).
- kimi `apiv2` authenticated ops are capability-recorded but intentionally
  unwired; any change there is a new round's work.
- `webzites-probe.timer` provides 6h coverage; whether the operator wants
  alerting on `violated[]` deltas (vs the current silent log) is undecided.
