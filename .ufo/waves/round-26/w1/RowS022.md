# RowS022 — freshness recheck (round 26, C1)

```json
{"id":"S022","verdict":"HOLD","fetchIndex":1,"quote":"Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons","anchorObserved":"Main-content opening paragraph under H1 \"Fix canonicalization issues\" (id=fix-canonicalization-issues); footer \"Last updated 2026-08-21 UTC\"","reason":"Opening paragraph still states Google may choose a different canonical despite an explicit designation; page footer date 2026-08-21 matches the row anchor and the live Last-Modified header (Fri, 21 Aug 2026 11:28:27 GMT), so scope and teaches are unchanged.","correction":null}
```

## Caveats (≤10 lines)

1. Fetch #1: HTTP 200, final URL identical to recorded URL, fetched 2026-10-21T15:10:44Z; decoded 178056-byte HTML sha256 `4d42dd82…b173e47` matches the manifest exactly (manifest digest covers decoded bytes, not the .raw.gz container).
2. Anchor did not move: the H1 and opening paragraph sit in main content immediately after "Send feedback"; only site chrome text precedes them.
3. Scope language persists verbatim: the steps reference the "Google-selected canonical" versus "your preferred canonical URL".
4. The row's usedBy lesson quote, `corpus/lessons/round-22.md:45`, still matches the re-fetched bytes word-for-word; no lesson correction needed.
5. Living doc, not a pinned commit/tag: content drift is possible, hence the 90d cadence remains appropriate; this recheck only establishes today's HOLD.
6. No tool installs or upgrades were needed for this row.
