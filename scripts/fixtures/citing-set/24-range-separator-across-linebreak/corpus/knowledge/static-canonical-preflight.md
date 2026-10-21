source: S001 (corpus/SOURCES.md) - https://example.test/canonical/preflight §Preflight rows
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on preflight change - `grep -cF 'canonicalAudit' scripts/canonical_audit.py` (expect 1)

# Static canonical preflight

The round-20 correction sweep spans S001
to S006 of the registry block. Every row in that span carries its own anchor
and was opened on the same day.

Round-26 source recheck (2026-10-21, append-only; original lines unchanged).
The cited span was re-fetched and judged HOLD at its anchors.
