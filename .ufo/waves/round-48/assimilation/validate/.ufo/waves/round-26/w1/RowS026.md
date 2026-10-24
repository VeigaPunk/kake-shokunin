```json
{"id":"S026","verdict":"HOLD","fetchIndex":1,"quote":"This parser does not check that end tags match start tags","anchorObserved":"'html.parser — Simple HTML and XHTML parser' section > HTMLParser class-description paragraph (module overview, after the callback-overview sentence and immediately before 'Changed in version 3.4'); text view line 1","reason":"Living /3/ page still documents the same callback tokenizer: handle_starttag converts tag names to lower case, attribute names are lowercased and their character/entity references replaced, convert_charrefs defaults true, and the quoted non-validation sentence is verbatim. The page now labels itself Python 3.15.1 (last updated 2026-10-21 13:02 UTC; last-modified 13:04:30 GMT) versus Python 3.15.0 seen at 06:59 UTC in the round-23 reopen: the micro-version label moved within the 3.15 series while no taught content changed, so the anchor's 'Python 3.15' scope and its 2026-10-20 access date remain accurate as a historical record. r26 fetch: HTTP 200, 55260 bytes, sha256 d92217e08486dc9bfedf255f071fdad1ea1a506a1e8a8570c4711a47aad5faa3, matching manifest S026-1.","correction":null}
```

Caveats (freshness axis):

1. The clause “HTML5 tree construction are not validated” is not verbatim on this page (zero occurrences of “HTML5” or “tree construction”); it is an inference from the callback-only API (“serves as the basis for parsing”, “able to parse invalid markup”). Unchanged since mining; the round-23 reopen already recorded this as a P3 precision note, so no correction is proposed on a freshness axis.
2. Version drift observed: docs title moved 3.15.0 → 3.15.1 on 2026-10-21 between the round-23 reopen (06:59 UTC) and this fetch (15:10 UTC); page rebuild changed only the label/date, not the taught sentences. This satisfies the row's `on-release` cadence.
3. Digest verified locally: decompressed S026-1.raw.gz is 55260 bytes with the manifest sha256 above.
4. No tool installs or updates were needed.
