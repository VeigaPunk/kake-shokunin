# Row S030 — WHATWG HTML syntax freshness recheck (round 26, C1)

```json
{"id":"S030","verdict":"HOLD","fetchIndex":1,"quote":"On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind.","anchorObserved":"§13.1.2.1 Start tags, ordered-list step 6 of 7 (raw <h4 id=start-tags> at byte 23907, <ol> at 24124, item 6 begins 25801); §13.1.2 Elements void-element <dfn id=void-elements> at byte 12265; text view fetched/text/S030-1.txt line 1, quote at offset 9514","reason":"The re-fetched Living Standard (Last-Modified Tue, 20 Oct 2026 12:58:33 GMT; banner 'Last Updated 20 October 2026'; fetched 2026-10-21) still limits the optional single U+002F SOLIDUS to void or foreign elements in start-tag step 6, still says it 'does not mark the start tag as self-closing' and has 'no effect of any kind' on void elements, and the void-element list still names exactly 13 elements (area, base, br, col, embed, hr, img, input, link, meta, source, track, wbr), so scope, anchor and teaches all hold; response sha256 equals round-23's recorded S030 digest, so no drift at all.","correction":null}
```

## Caveats (8)

1. Fetch provenance: manifest.json row S030 index 1, status 200, 89196 bytes, sha256 `04b65bf0b4b5f3bb3815999ab499af980fa09b8832f02c1686c544ab8e79a52d`, fetchedAt `2026-10-21T15:10:50Z`, Last-Modified `2026-10-20 12:58:33 GMT`; page banner "Last Updated 20 October 2026" equals the row's stated revision.
2. Living Standard, no commit pin: this recheck tests content drift; the fetched sha256 is bit-identical to the digest corpus/lessons/round-23.md:206-207 records as S030's correct response digest (line 60's `a11dcf17…` is the cross-assigned digest the lesson corrects at lines 121-122), so the page has not changed since the row was opened.
3. Step numbering is only visible in raw HTML: the section's ordered list has 7 `<li>` items and item 6 is the solidus step; the flattened text view cannot show list numbers.
4. Void count from raw bytes: the first 13 `<code><a>` names inside the void-elements `<dd>` are exactly the 13 above; the following 5 names (template, script, style, textarea, title) belong to the separate element-kind rows.
5. Row cells are unchanged; the anchor's "opened 2026-10-21" is same-day, and with the 90d cadence the next recheck is due 2027-01-19.
6. Used-by rechecked against the same bytes: corpus/knowledge/static-canonical-preflight.md:110-111 (13 void names) and :151 (slash after an unquoted attribute value belongs to the value) hold, and corpus/lessons/round-23.md:60 quotes this same sentence verbatim.
7. Scope nuance: step 6 only grants the slash for void/foreign elements; the fetched page has no separate sentence forbidding it on normal elements, so "versus non-void HTML elements" is the complement of that grant, consistent with the six element kinds in 13.1.2.
8. No tools installed or upgraded; no host changes; only wave-retained public-GET bytes and corpus reads were used (no browser, property probe, account, or credential use).
