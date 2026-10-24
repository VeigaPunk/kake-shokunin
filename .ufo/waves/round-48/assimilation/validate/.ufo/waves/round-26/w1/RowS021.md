# RowS021 — freshness recheck (round 26, C1)

```json
{"id":"S021","verdict":"HOLD","fetchIndex":1,"quote":"Even though relative paths are supported by Google, they can cause problems in the long run","anchorObserved":"Text view single flattened line 1, offset 15071, inside H3 \"The rel=\"canonical\" link element\" under H2 \"Use rel=\"canonical\" link annotations\"; footer \"Last updated 2026-07-10 UTC\"","reason":"All three teaches still hold in the re-fetched page: the link element is \"only accepted if it appears in the <head> section of the HTML\"; absolute paths are urged while relative paths are \"supported by Google\" yet discouraged; and the method is framed as a \"strong signal\" / stated preference (\"Google will decide which pages (if any) are duplicates\"), not a selection guarantee. The three anchor headings and the 2026-07-10 update date are unchanged, so scope, anchor and teaches remain correct.","correction":null}
```

## Caveats (≤10 lines)

1. Fetch #1: HTTP 200, final URL identical to recorded URL, fetchedAt 2026-10-21T15:10:43Z; decoded 194799-byte HTML sha256 `4edda778…c7e5c5` matches the manifest and Content-Length.
2. Text view is one flattened line (21019 bytes); the quote is at offset 15071, inside the "Use rel=canonical link annotations" section, not in site chrome.
3. Head-placement clause persists verbatim: "The rel=canonical link element is only accepted if it appears in the <head> section of the HTML".
4. Absolute preference persists verbatim: "Use absolute paths rather than relative paths with the rel=canonical link element" followed by the quoted relative-path caveat and "we don't recommend them".
5. Non-guarantee framing persists: "strong signal", "indicate your preference", "Google will decide which pages (if any) are duplicates"; no literal "guarantee" wording, so the row's summary remains an interpretation, not a quote.
6. Page footer "Last updated 2026-07-10 UTC" matches the row anchor and the live Last-Modified header (Fri, 10 Jul 2026 10:12:15 GMT); no drift since the 2026-10-20 opening.
7. Anchor headings all present in raw HTML: H2 "Use rel=canonical link annotations", H3 "The rel=canonical link element", H2 "Best practices".
8. Used-by quote `corpus/lessons/round-22.md:44` still matches the re-fetched bytes word-for-word; the knowledge entry's existing [r23-correction] on fragment canonicals already narrows the overstatement, so no new correction is due.
9. Living doc, not a pinned commit/tag: this HOLD certifies today's bytes only; the 90d cadence remains appropriate.
10. No tool installs or upgrades were needed for this row.
