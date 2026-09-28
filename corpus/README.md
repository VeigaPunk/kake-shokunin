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
| Fire journals & exit codes | `knowledge/fire-journal-codes.md` | state/*.json journal anatomy, exit codes 1–8/64, meter-consumption truth |
| Round lessons | `lessons/round-1.md`, `round-3.md`, `round-4.md` | audit findings; fresh-probe corrections; journal decoder |

## Known gaps

- 50 cloned site repos under `~/Projects/webzites/repos/` (verified
  2026-09-28, `ls | wc -l`; round-1 said ~40); only the `sourceDir`-bound
  ones are documented here.
- Round-3 ran live probes (09-28); next gap: a recorded re-probe cadence or
  reconcile-diff spotcheck for GHP subpaths (`reconcile` covers index only).
- kimi `apiv2` authenticated ops are capability-recorded but intentionally
  unwired; any change there is a new round's work.
