source: S001toS006 (corpus/SOURCES.md) - https://example.test/publish/queue-rows §Queue rows
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on queue-row change - `grep -cF 'queueRows' scripts/publish-queue.mjs` (expect 1)

# Publish queue rows

The queue entry names the registry span it covers without a separator space.
The span is written as one glued token, so the row ids inside it are only
reachable through the range reading.

Round-26 source recheck (2026-10-21, append-only; original lines unchanged).
The cited span was re-fetched and judged HOLD at its anchors.
