# ScribeC2Rows — C2 registry rows S430–S433 and lesson Gate lines

Round 61, wave w1, seat ScribeC2Rows. Access date of every row and Gate line: 2026-10-27 (UTC).
Bodies: `.ufo/waves/round-61/sources/S430.html` … `S433.html`, each GET, HTTP 200, effective URL equal to
the request URL, userAgent `round61`; digests re-checked by this seat against `sources/receipts.json`
(S430 f086bfac6974e641867a427a24fb3ef564911767a244bbd7e87455765ac72c0a, 133951 bytes;
S431 be8f2468b963df915511832113794407420090f9b4d87d58b603daf01de3144e, 1011256;
S432 63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b, 1854393;
S433 d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5, 1187554).
Quote rule applied: 6..25 whitespace units, <=160 characters, ASCII only, a substring of one
whitespace-collapsed text node of the retained body, page-unique (occurrence count 1 across all text nodes).

## ROWS (append block, 11-cell registry schema, in id order)

| S430 | RFC 6797: HTTP Strict Transport Security (HSTS) — https://www.rfc-editor.org/rfc/rfc6797.html | spec | A | HSTS policy signalling (STS response header) | Section 6.1 Strict-Transport-Security HTTP Response Header Field and Section 5.1 HSTS Host Declaration; RFC 6797, November 2012 | A host declares an HSTS policy by sending the Strict-Transport-Security response header field over secure transport, so a recorded HTTPS response without that field carries no policy declaration to audit | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |
| S431 | W3C Content Security Policy Level 3 — https://www.w3.org/TR/CSP3/ | spec | A | Content-Security-Policy header as policy conveyance | Section 3.1 The Content-Security-Policy HTTP Response Header Field; W3C Working Draft WD-CSP3-20261027, 27 October 2026 | The Content-Security-Policy response header field is the document's preferred mechanism for delivering a policy from a server to a client, so the field's presence or absence in a captured response is the conveyance signal an offline audit can read | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |
| S432 | WHATWG Fetch — https://fetch.spec.whatwg.org/ | spec | A | X-Content-Type-Options nosniff value rule | Section 3.6 X-Content-Type-Options header and its value ABNF; WHATWG Living Standard accessed 2026-10-27 | The field has one defined value, nosniff, compared ASCII case-insensitively against the split field values, so a recorded value of anything else is outside the value rule | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |
| S433 | RFC 9110: HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110.html | spec | A | Content-Type field semantics and HTTP field-line rules | Section 8.3 Content-Type and Section 5.2 Field Lines and Combined Field Value; RFC 9110, June 2022 | Content-Type is defined as a singleton field, so its accidental repetition yields a combined value that only appears to be a list, while field lines of any name combine in received order by comma concatenation | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |

## GATE (lesson `## Gate` lines, CORPUS.md rule 1 format)

- S430 — https://www.rfc-editor.org/rfc/rfc6797.html — opened 2026-10-27 — "The Strict-Transport-Security HTTP response header field (STS header field) indicates to a UA that it MUST enforce the HSTS Policy" (20 units; § 6.1. Strict-Transport-Security HTTP Response Header Field)
- S431 — https://www.w3.org/TR/CSP3/ — opened 2026-10-27 — "HTTP response header field is the preferred mechanism for delivering a policy from a server to a client." (18 units; § 3.1. The Content-Security-Policy HTTP Response Header Field)
- S432 — https://fetch.spec.whatwg.org/ — opened 2026-10-27 — "Web developers and conformance checkers must use the following" (9 units; § 3.6. X-Content-Type-Options header)
- S433 — https://www.rfc-editor.org/rfc/rfc9110.html — opened 2026-10-27 — "Although Content-Type is defined as a singleton field, it is sometimes incorrectly generated multiple times" (15 units; § 8.3. Content-Type)

## Quote provenance (per Gate line)

| id | units | chars | retained body sha256 (first 16) | node | anchor section of the quote |
|---|---|---|---|---|---|
| S430 | 20 | 130 | f086bfac6974e641 | one `<pre>`/text node of §6.1 (heading "6.1. Strict-Transport-Security HTTP Response Header Field") | §6.1 |
| S431 | 18 | 104 | be8f2468b963df91 | the `<p>` text node of §3.1; the sentence's leading code element splits it, so the span starts at "HTTP response header field" | §3.1 |
| S432 | 9 | 62 | 63b0a018753c330a | the `<p>` node of §3.6 immediately before the value ABNF sentence (`X-Content-Type-Options = "nosniff" ; case-insensitive`, split across nodes 8085–8088 of the same section) | §3.6 |
| S433 | 15 | 107 | d431760660ea44e1 | the `<p>` text node of §8.3 after the ABNF block ("Although Content-Type is defined as a singleton field …") | §8.3 |

Bounds on these anchors, stated so wave 2 can attack them:

- S431's quote begins mid-sentence because §3.1's first sentence embeds the header name as a `<code>`
  element, which splits the text node; the quoted span is the remainder of that one sentence. The document
  served on 2026-10-27 is a Working Draft (`WD-CSP3-20261027`), not a W3C Recommendation — the contract's
  phrase "CSP Level 3 REC row" is not what the retained body says, and the row records Working Draft.
- S432's quote is a clause, not a full sentence: the WHATWG source wraps every header name in `<code>`, so no
  full sentence of §3.6 is a single text node. The value rule itself sits in the ABNF cell
  (`X-Content-Type-Options = "nosniff" ; case-insensitive`), which the quote does not quote verbatim.
- S433's quoted sentence is in §8.3; the §5.2 half of the anchor grounds the field-line rule quoted by the
  row's `teaches` cell but carries no Gate quote of its own.
- S430's §6.1 text is one large preformatted text node, so the quote is page-unique but the node granularity
  there is the whole section stub rather than a paragraph.
