# ReopenS105

Axes: operability (one GET, hash, locate every scope/anchor/teaches claim); freshness (status, clock, retained bytes). No tool installed.

## Fetch

`timeout 90 curl -fsSL -D headers.txt -o xml-1.0.html -w … --max-time 60 --proto =https https://www.w3.org/TR/xml/` exit 0. HTTP 200, 0 redirects, final URL unchanged, 219926 bytes, `text/html; charset=utf-8`. Response `date: Fri, 23 Oct 2026 07:41:15 GMT`. `last-modified: Tue, 09 Oct 2018 13:18:59 GMT`. Canonical `https://www.w3.org/TR/xml/`.

`sha256sum` exit 0 and `cmp -s` exit 0. Live `/fast/scratch/hyaku/kake-r39a3w2/ReopenS105/xml-1.0.html` and retained `.ufo/waves/round-39/sources/xml-1.0.html` are both `f58a4b9e1e5b8bac13fb55c4e5c7c8c5e2c176aa45ee68e2f1ab2498511927ec` (row anchor; `sources/SHA256SUMS:7`). Byte-identical, so no visible-text diff. The row clock `2026-10-23T06:56:39Z` is not on the page; `corpus/lessons/round-39.md:35` records the L1 re-open at 06:56:39–41Z. This run did not re-observe that clock.

## Cells

**scope — holds.** Production [3] S is white space: `xml-1.0.html:322-324` "S (white space) consists of one or more space (#x20) characters, carriage returns, line feeds, or tabs" and `[3] S ::= (#x20 | #x9 | #xD | #xA)+`. Optional doctypedecl: `:505-507` `[22] prolog ::= XMLDecl? Misc* (doctypedecl Misc*)?` under §2.8 (`:491`). Encoding-name matching: `:1402-1403` "XML processors SHOULD match character encoding names in a case-insensitive way". Not the sitemap UTF-8-only rule: `:1338-1339` processors MUST read UTF-8 and UTF-16; `:1352-1355` other encodings are recognized; `:1422` example `encoding='EUC-JP'`. Not Namespaces in XML: title `:39` is XML 1.0 Fifth Edition; Namespaces is a separate recommendation at `:1840-1841` (`https://www.w3.org/TR/xml-names/`). Validity (`:500-502`) requires a document type declaration; "optional" is the well-formed `[22]` `?`, which is the production the anchor cites.

**anchor — holds.** §2.3 `:321`, production [3] `:324`. §2.8 `:491`; [22] `:505`; [28] `doctypedecl` `:536`. §4.3.3 "Character Encoding in Entities" `:1337` (TOC `:130`). "W3C Recommendation 26 November 2008" verbatim `:40`. Title "Extensible Markup Language (XML) 1.0 (Fifth Edition)" verbatim `:4` and `:39`. Latest-version link text `:47` is `http://www.w3.org/TR/xml/`; the href and this GET's canonical are `https://www.w3.org/TR/xml/`. Backtick SHA256 matches the file. In-place note `:42` (7 February 2013, RFC4646/RFC4647 links only) does not change the recommendation date.

**teaches — holds.**
- "S is exactly space, tab, CR and LF": the [3] alternation is only #x20, #x9, #xD, #xA (`:324`); prose `:322-323`. Note `:324-331` keeps #xD; literal #xD is normalized (`:671-674`) and matches S only via a character reference. Sentence 21 (`c1-contract.md:60-61`) strips U+0020, U+0009, U+000D, U+000A and nothing else — the same four. "Exactly" is that closed set, not a claim that the `S` token may be empty.
- "encoding names SHOULD match case-insensitively (sentence 7)": SHOULD and "case-insensitive" are verbatim at `:1402-1403`. Sentence 7 (`c1-contract.md:35-36`) says the value must be `UTF-8`, compared case-insensitively. The row cites the compare; the scope already excludes the UTF-8-only half. SHOULD is the spec's modal, not a misquote of sentence 7's "must".
- "a doctypedecl can be well-formed, so sentence 9 is a lane safety reading, not an XML rule": `:546-547` "it is possible to construct a well-formed document containing a doctypedecl that neither points to an external subset nor contains an internal subset." The spec's subject is the document. Sentence 9 (`c1-contract.md:39-40`) labels itself "Lane reading (safety, not from a source)". A doctypedecl is inside the well-formed grammar, so `doctype_present` is not an XML rule.

**Quoted phrases.** The three cells quote no spec sentence. The only backtick span is the SHA256, which matches the file. The lesson gate quote at `round-39.md:41` ("S (white space) consists of one or more space (#x20) characters, carriage returns, line feeds, or tabs.") is verbatim at `xml-1.0.html:322-323`.

**Sentence numbers.** 7, 9, and 21 are the encoding compare, the doctype lane reading, and the whitespace strip. Each says what the row says it says.
