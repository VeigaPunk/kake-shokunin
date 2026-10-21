source: S001 (corpus/SOURCES.md) - https://example.test/probe/delta §Delta window
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on delta change - `grep -cF 'deltaWindow' scripts/probe-delta.mjs` (expect 1)

# Probe delta alerting

The probe delta entry alerts when a probe result moves outside the recorded
window.

Round-26 source recheck (2026-10-21, append-only; original lines unchanged).
The cited row was re-fetched and judged HOLD at its anchor.
