source: S001..S006 (corpus/SOURCES.md) - https://example.test/drift/probe-set §Probe rows
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on probe-set change - `grep -cF 'probeRows' scripts/drift-detection.mjs` (expect 1)

# Drift detection

Drift detection compares the last accepted probe set with the current one and
reports the rows whose verdict moved.

Round-26 source recheck (2026-10-21, append-only; original lines unchanged).
The probe rows were re-fetched and judged HOLD at their anchors.
