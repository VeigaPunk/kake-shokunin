source: S002 (corpus/SOURCES.md) - https://example.test/publish/cadence §Retry window
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on cadence change - `grep -cF 'retryWindow' scripts/publish-queue.mjs` (expect 1)

# Publish cadence log

The cadence log records one line per accepted publish attempt.

- S002, §Retry window: "a rejected attempt is retried once inside the window."
