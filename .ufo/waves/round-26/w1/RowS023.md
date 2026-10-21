# Row S023 — freshness recheck (round 26, C1)

```json
{"id":"S023","verdict":"HOLD","fetchIndex":1,"quote":"Keywords are always ASCII case-insensitive, and must be compared as such.","anchorObserved":"§4.6.8 Link types preamble (just before the link-type table), text view line 1; §4.6.8.4 \"Link type canonical\" body follows at the same heading level","reason":"The re-fetched Living Standard (Last-Modified Tue, 20 Oct 2026 12:58:32 GMT, fetched 2026-10-21) still carries both §4.6.8 and §4.6.8.4 with unchanged text: the preamble states rel keywords are ASCII case-insensitive and must be compared as such, and §4.6.8.4 states the canonical keyword's href URL is the preferred URL for the current document. Scope, teaches, and anchor all hold with no drift; the row's access date (2026-10-20) equals the page's current Last-Modified date.","correction":null}
```

## Caveats (7)

1. Fetch provenance: manifest.json entry row=S023, index=1, status 200, bytes=381019, sha256=82a81f23…f6b7, fetchedAt=2026-10-21T15:10:45Z; Last-Modified header equals the row's access date, so a living-standard drift test passes trivially this round.
2. Second clause is quoted from the §4.6.8 preamble (the general rel-keyword rule), not from §4.6.8.4 itself; §4.6.8.4 supplies the first clause in its own words.
3. Both clauses also verified separately and verbatim: `The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document.` (spec retains its own "that URL" wording; the row's paraphrase is faithful).
4. Anchor "Section 4.6.8 Link types and 4.6.8.4 canonical" matches headings in the re-fetched body; no section renumbering.
5. Text view is a single-line extraction, so anchorObserved cites heading/section rather than line numbers; body heading offsets 40385 (§4.6.8) and 52950 (§4.6.8.4).
6. No tools installed or updated; no host changes. No browsers or property probes used — only retained round-26 bytes plus the row line at corpus/SOURCES.md:31.
7. Remaining unknown: none for this row; verdict rests on retained bytes and is decidable.
