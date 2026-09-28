# kake-shokunin corpus

Memory for the web-properties & publishing domain (ds4cc.com, kimi.page/pro
mirrors, Pages deploys).

## Layout

- `knowledge/` — domain facts with citations (file path, command output, URL).
- `lessons/` — per-round lessons citing LOG.md round + evidence.

## Coverage map

| Area | Entry | Coverage |
|---|---|---|
| Fleet registry & tripwires | `knowledge/fleet-registry.md` | all 20 rows, expect semantics, pruning rules |
| Publish channels | `knowledge/publish-channels.md` | GHP push-to-main, Render apps-sdk, kimi surface verbs |
| Drift detection | `knowledge/drift-detection.md` | probe / sync-check / reconcile / kimi-map; byte-vs-marker semantics |
| Mirror pitfalls | `knowledge/mirror-pitfalls.md` | kimi byte rewriting, no dir indexes, one-chat-one-slot, dead slots |
| Round lessons | `lessons/round-1.md` | what the audit found, what stays manual |

## Known gaps

- No live probe run inside this repo this round — all classifications cite the
  2026-09-26 webzites evidence, not a fresh sweep.
- `~/Projects/webzites/repos/` holds ~40 cloned site repos; only the
  `sourceDir`-bound ones are documented here.
- kimi `apiv2` authenticated ops are capability-recorded but intentionally
  unwired; any change there is a new round's work.
