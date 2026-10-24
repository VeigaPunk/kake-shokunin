source: S001 (corpus/SOURCES.md) - https://example.test/publish/queue-contract §Accept order
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on queue-contract change - `grep -cF 'acceptOrder' scripts/publish-queue.mjs` (expect 1)

# Publish queue ordering

The queue keeps one acceptance order for a single producer and a single
consumer. Ordering is a property of the queue contract, not of the storage
layer underneath it.

- S001, §Accept order: "accepted items are dequeued in the order they were
  accepted."

Round-26 source recheck (2026-10-21, append-only; original lines unchanged).
The cited row was re-fetched by one public GET and judged HOLD at its anchor.
