source: S001 (corpus/SOURCES.md) - https://example.test/sitemap/orphan-audit §Audit rows
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on audit change - `grep -cF 'orphanAudit' scripts/sitemap-orphan-audit.mjs` (expect 1)

# Sitemap orphan audit

The orphan audit compares the served path set with the declared path set.

Round-26 source recheck (2026-10-21, append-only; original lines unchanged).
The cited row was re-fetched and judged HOLD at its anchor.
