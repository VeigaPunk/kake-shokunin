source: S001 (corpus/SOURCES.md) - https://example.test/freshness/sweep §Citation locality
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on sweep-script change - `grep -cF 'scanCitations' scripts/freshness-sweep.mjs` (expect 1)

# Freshness sweep

The freshness sweep records when each knowledge entry was last verified and
which row governs its citation locality.

## Local policy

An entry stays open until its cited rows are re-opened. No row id is named in
the body of this entry; the governing row appears in the header only.
