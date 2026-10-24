# ScoutXmlSpec — XML 1.0 Fifth Edition vs C1 sentences 7–9 and 21

Axes: operability (a citable row and line-located quotes, no refetch) and fidelity (set-equality and the UTF-8 compare kept as match or mismatch).

## Fetch

GET https://www.w3.org/TR/xml/ at 2026-10-23T06:53:19Z. `curl` exit 0, HTTP 200, 0 redirects, final URL unchanged. `content-type: text/html; charset=utf-8`. `last-modified: Tue, 09 Oct 2018 13:18:59 GMT`. Canonical link is the same URL. Line 39 title: Extensible Markup Language (XML) 1.0 (Fifth Edition). Line 40: W3C Recommendation 26 November 2008. Line 42: in-place edit 7 February 2013, RFC4646 and RFC4647 links only.

Bytes: `/fast/scratch/hyaku/kake-r39a3w1/ScoutXmlSpec/xml-1.0.html` (219926 bytes, 2215 lines). sha256 `f58a4b9e1e5b8bac13fb55c4e5c7c8c5e2c176aa45ee68e2f1ab2498511927ec`. No tool installed. `corpus/SOURCES.md` not modified (last registry id S104, line 112).

## Findings

Sentence 21's set **equals** the character alternatives of production [3] S, not the token. Line 322, 17 words: "S (white space) consists of one or more space (#x20) characters, carriage returns, line feeds, or tabs." Line 324: `[3] S ::= (#x20 | #x9 | #xD | #xA)+`, i.e. U+0020, U+0009, U+000D, U+000A, and nothing else. The `+` means one or more; sentence 21 also allows an empty strip. The trim is not an XML rule: lines 641–643 require the processor to pass every non-markup character to the application. Lines 328–330, first sentence, 23 words: "all #xD characters literally present in an XML document are either removed or replaced by #xA characters before any other processing is done." Lines 671–674 make that a MUST before parsing, so a parsed value holds U+000D only via a character reference (lines 330–331).

Sentence 7's case-insensitive compare **matches** the recommended name rule and **does not** match a UTF-8-only requirement. Lines 1402–1403, 11 words: "XML processors SHOULD match character encoding names in a case-insensitive way" (SHOULD, not MUST). Lines 1366–1401 name UTF-8, UTF-16, ISO-10646-UCS-2, ISO-10646-UCS-4, ISO-8859-n, ISO-2022-JP, Shift_JIS, EUC-JP and other IANA names as values that SHOULD be used. Line 1422's example is `encoding='EUC-JP'`. Production [81], line 1363, allows both cases: `[A-Za-z] ([A-Za-z0-9._] | '-')*`. Production [23], line 509, makes `EncodingDecl` optional, matching sentence 7's "if". Lines 1408–1410, 21 words: "an entity which begins with neither a Byte Order Mark nor an encoding declaration to use an encoding other than UTF-8" is fatal only in that unlabeled case, and only absent external protocol information (lines 1405–1406). Lines 1339–1342: the terms UTF-8 and UTF-16 do not apply to UTF-16BE, UTF-16LE or CESU-8.

Sentence 8 is **partly grounded**. Line 1325, 12 words: "The document entity is well-formed if it matches the production labeled document." "With namespaces" is not a well-formedness rule in this file. Lines 335–338: Namespaces in XML assigns meaning to colons; processors must accept colon as a name character. Bibliography lines 1839–1841 cite that separate 1999 Recommendation at https://www.w3.org/TR/xml-names/ (not fetched; outside the named URL).

Sentence 9 **contradicts** §2.8. The contract already marks it a lane reading, not from a source. Production [22], lines 505–508: `prolog ::= XMLDecl? Misc* (doctypedecl Misc*)?`, so the declaration is optional. Line 546, 23 words: "it is possible to construct a well-formed document containing a doctypedecl that neither points to an external subset nor contains an internal subset." Production [28], lines 536–540, is `'<!DOCTYPE' S Name … '>'`. Lines 582 and 588 are examples that contain one. Validity (lines 500–502) wants a declaration; well-formedness does not forbid it.

## Draft SOURCES row

Not appended. Draft id S105; another seat may take it. Quote grounding `teaches` is the 17-word line 322 sentence above (grounds sentence 21). Line 1402 grounds only the compare half of sentence 7. Line 546 contradicts sentence 9. Sentence 8's namespace half is not in this file.

| S105 | Extensible Markup Language (XML) 1.0 (Fifth Edition) — https://www.w3.org/TR/xml/ | spec | A | XML 1.0 white space S, optional document type declaration, and encoding-name matching; not the sitemap UTF-8-only rule and not Namespaces in XML | §2.3 production [3] lines 322-331; §2.8 productions [22] and [28] lines 505-546; §2.11 lines 671-674; §4.3.3 lines 1337-1412; Recommendation 26 November 2008; fetched 2026-10-23T06:53:19Z HTTP 200; retained HTML SHA256 f58a4b9e1e5b8bac13fb55c4e5c7c8c5e2c176aa45ee68e2f1ab2498511927ec | S is only space, tab, CR and LF; encoding names SHOULD match case-insensitively and need not be UTF-8; a doctypedecl can be well-formed | queued | 2026-10-23 | 365d | — |

## Commands

`timeout 120 curl -fsSL -D headers.txt -o xml-1.0.html -w … --max-time 90 https://www.w3.org/TR/xml/` exit 0. `sha256sum xml-1.0.html` exit 0, digest above. Headers retained beside the body; the `set-cookie` line is not evidence and is not quoted.
