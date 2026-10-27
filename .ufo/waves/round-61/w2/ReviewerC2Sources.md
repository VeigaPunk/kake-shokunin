# ReviewerC2Sources

## S430 — RFC 6797 / HSTS

- Source: `https://www.rfc-editor.org/rfc/rfc6797.html` only in the drafted registry row and Gate line; matches the retained receipt URL/effective URL. The retained HTML identifies “HTTP Strict Transport Security (HSTS)” and RFC 6797. The incorrect RFC 6790 URL does not appear in the row.
- Access: receipt is HTTP 200, `fetchedAt` 2026-10-27T09:14:55Z, `userAgent: round61`; opened/access date 2026-10-27 is consistent.
- Quote: the Gate span “The Strict-Transport-Security HTTP response header field (STS header field) indicates to a UA that it MUST enforce the HSTS Policy” occurs once in one retained text node; 20 whitespace units, 130 chars, ASCII, no pipe.
- Tier: `spec` / A is appropriate for the RFC Editor's RFC 6797 text and the stated HSTS scope.
- Verdict: verified.

## S431 — W3C CSP Level 3

- Source: `https://www.w3.org/TR/CSP3/` matches the retained receipt URL/effective URL.
- Access: receipt is HTTP 200, fetched 2026-10-27T09:14:55Z by `round61`; opened/access date 2026-10-27 is consistent.
- Status/tier: the retained page has `w3c-status=WD` and points to `/TR/2026/WD-CSP3-20261027/`; the drafted row correctly identifies a W3C Working Draft, not a Recommendation. Tier A is appropriate to the W3C primary specification, with its draft status explicitly qualified.
- Quote: “HTTP response header field is the preferred mechanism for delivering a policy from a server to a client.” occurs once in one retained text node; 18 units, 104 chars, ASCII, no pipe. Its starting point after the inline field-name markup is disclosed in the draft.
- Verdict: verified; retain the Working Draft label (do not call it a REC).

## S432 — WHATWG Fetch

- Source: `https://fetch.spec.whatwg.org/` matches the retained receipt URL/effective URL.
- Access: receipt is HTTP 200, fetched 2026-10-27T09:14:55Z by `round61`; opened/access date 2026-10-27 is consistent.
- Tier: `spec` / A is appropriate to the WHATWG Living Standard for the stated Fetch algorithm/value scope.
- Quote: “Web developers and conformance checkers must use the following” occurs once in one retained text node; 9 units, 62 chars, ASCII, no pipe.
- Evidence limitation: this quote is a generic lead-in and does not itself say `X-Content-Type-Options` or `nosniff`. The ScoutC2Sources report confirms the normative ABNF and algorithm comparison are fragmented across inline markup and cannot be quoted as one qualifying node. Thus location and body provenance are verified, but the Gate quote alone does not directly establish the row's nosniff-value teaching; the entry supplies a located paraphrase/ABNF description. Keep this bounded rather than presenting the quote as the value rule.
- Verdict: provenance/date/tier verified; quote is located but weak as direct support for the row's specific value claim.

## S433 — RFC 9110

- Source: `https://www.rfc-editor.org/rfc/rfc9110.html` matches the retained receipt URL/effective URL. Same base document as S088, but the scopes differ: S433 addresses §§8.3 and 5.2 (Content-Type and field lines); S088's registry scope is redirects/Location and 404/410 status meanings, anchored at §15.4 and related status sections. This is the expected W04 duplicate-URL-across-scopes warning, not a duplicate scope.
- Access: receipt is HTTP 200, fetched 2026-10-27T09:14:55Z by `round61`; opened/access date 2026-10-27 is consistent.
- Tier: `spec` / A is appropriate for RFC 9110 within the stated HTTP semantics scope.
- Quote: “Although Content-Type is defined as a singleton field, it is sometimes incorrectly generated multiple times” occurs once in one retained text node; 15 units, 107 chars, ASCII, no pipe. It is in §8.3, distinct from S088's scope.
- Verdict: verified; the S433 quote is distinct from S088's scope despite the shared RFC URL.

## Cross-row checks and review boundary

- SHA-256 and byte counts for all four retained HTML bodies match `sources/receipts.json`; all four receipts have the same 2026-10-27T09:14:55Z access timestamp, HTTP 200 and `round61` user agent.
- All four drafted registry rows have the expected 11 cells (12 delimiter pipes); no extra pipe occurs inside row content. Each Gate quote has zero literal pipes.
- The reviewed retained bodies `S430.html`–`S433.html` and receipt metadata support the source/date findings above. At review time, `corpus/SOURCES.md` contained no S430–S433 rows (the rows were present in the w1 `ScribeC2Rows.files/rows.md` draft); therefore this review verifies the retained row draft, not an integrated registry state. The W1 lesson draft still has placeholder Gate spans, not the final lines.
- No tools were installed; no tests/builds run.

VERDICT: S430, S431 and S433 source/date/quote/tier checks pass (S431 is a Working Draft; S433 is scope-distinct from S088); S432 provenance/date/tier pass but its located quote is only a generic lead-in and does not directly evidence the nosniff-value claim. The S430–S433 registry rows and final lesson Gate lines were not integrated at review time.