# ReopenS110 — S110 quote, anchor, teaches

Axes: freshness of https://www.w3.org/TR/xml/ against the retained row; then quote, anchor, and each `teaches` clause. No tool installed. No counter run (this seat did not build a tool).

## Freshness — holds

`curl -fsSL -D headers.txt -o xml-live.html --max-time 60 https://www.w3.org/TR/xml/` (sandbox `/fast/scratch/hyaku/kake-r40w1/ReopenS110/`). HTTP/2 200 at `Fri, 23 Oct 2026 08:38:15 GMT`; `content-location: Overview.html`; `last-modified: Tue, 09 Oct 2018 13:18:59 GMT`; canonical `https://www.w3.org/TR/xml/`. Live sha256 `f58a4b9e1e5b8bac13fb55c4e5c7c8c5e2c176aa45ee68e2f1ab2498511927ec`, 219926 bytes, byte-identical to `.ufo/waves/round-40/sources/xml-1.0.html` and to `SHA256SUMS` line 3 and the S110 anchor cell. Row fetch `2026-10-23T08:28:47Z` is ~10 min earlier; the page has not moved. Edition: `xml-1.0.html:40` “W3C Recommendation 26 November 2008”; this version `xml-1.0.html:45` `http://www.w3.org/TR/2008/REC-xml-20081126/`.

## Gate quote — holds

`corpus/lessons/round-40.md:15`. After whitespace collapse the 25-word sentence is an exact substring of the §2.8 Note (`xml-1.0.html:517-519`), straight apostrophes in `'1.0'`. It is the Note after productions [22]–[27], immediately after the VersionNum sentence (`:516-517`). “Note after [26]” holds. Decision-cell abbreviation `[2] Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | …` matches `xml-1.0.html:306` through `[#x20-#xD7FF]`; the ellipsis drops `[#xE000-#xFFFD] | [#x10000-#x10FFFF]`. “(no #x0)” holds: `#x0` is not in [2].

## Anchor — holds

`corpus/SOURCES.md:118`. §2.2 production [2] at `xml-1.0.html:292` / `:306` (`#charsets`, `#NT-Char`). §2.8 [24] VersionInfo and [26] `VersionNum ::= '1.' [0-9]+` at `:508-513`, Note at `:517-520`. §4.3.3 at `:1337` (`#charencoding`).

## teaches — per clause

1. **U+0000 is not an XML Char — holds.** [2] is `#x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]` (`:306`). `#x0` is outside it. Same fact in prose: control characters `#x0` to `#x1F` “most of which cannot appear in XML” (`:1283`). The only explicit well-formedness constraint named Legal Character (`:1141-1142`) covers character references, not literal bytes; a literal U+0000 still fails because text is a sequence of Char (`:293-303`) and `[^<&]` in the notation matches Char only.
2. **Rider “so UTF-16 bytes without a BOM read as UTF-8 are not well-formed (contract sentence 8)” — holds as inference, not a quoted sentence.** Normative: no BOM and no encoding declaration, using an encoding other than UTF-8 is a fatal error (`:1405-1410`), so those bytes are read as UTF-8; ASCII-range UTF-16 is legal UTF-8 (byte `00` is U+0000) and then fails Char. Contract sentence 8 (`.ufo/waves/round-39/c1-contract.md:38-39`) is the right label for that failure. Boundary, not a miss: a UTF-16 payload that is illegal UTF-8 fails earlier as an encoding fatal error (`:1412-1416`). Non-normative Appendix F (`:2053`, table near `:2099`) guesses UTF-16 from `3C 00 3F 00` / `00 3C 00 3F` without a BOM; it does not override §4.3.3. The spec’s name “UTF-16” does not include UTF-16BE/LE (`:1340-1342`).
3. **A UTF-16 entity MUST begin with the BOM — holds.** `xml-1.0.html:1342-1346`: “Entities encoded in UTF-16 MUST and entities encoded in UTF-8 MAY begin with the Byte Order Mark … (#xFEFF).”
4. **An XML 1.0 processor processes a 1.x declaration as 1.0, so `version="1.1"` alone is not malformed — holds.** Note (`:517-520`): it “will process it as a 1.0 document” and “will accept 1.x documents provided they do not use any non-1.0 features.” `1.1` matches [26]. “Alone” is that proviso. Normative companion, not a contradiction: documents SHOULD NOT specify a version other than `1.0` (`:516-517`); SHOULD NOT is not a well-formedness failure. The “will process” sentence is a Note, which the anchor already says.

## Attacked statements

| Statement | Verdict |
|---|---|
| Row hash, date, URL, HTTP 200 | holds |
| Gate quote and “§2.8, Note after [26]” | holds |
| Anchor §2.2 [2], §2.8 [24]/[26]/Note, §4.3.3, 26 Nov 2008 | holds |
| U+0000 not a Char | holds |
| UTF-16 MUST begin with the BOM | holds |
| 1.x processed as 1.0; `version="1.1"` alone not malformed | holds |
| “read as UTF-8 ⇒ not well-formed” | holds as inference; not overstated for the ASCII-range case the row describes |

Confidence: high. Unresolved: none on the source text. No `c1_count.py` receipt (no tool built).
