# ScoutC2Sources

Fetched the four C2 sources once each (GET, userAgent `round61`, <=5 redirects, no cookies/body), retained the bodies under `.ufo/waves/round-61/sources/`, and appended one receipt per source to `sources/receipts.json` (created `{"receipts":[]}`-shaped object; all four entries appended atomically). Located the per-source quote spans under the lane's own `body_nodes` rule (re-implemented in `.files/qc.py` from `.ufo/waves/round-61/c61_recheck_pins.py`). Full located spans + node context are in `.files/spans.md`.

## FETCHES:
| id  | url                                              | effectiveUrl                                     | status | bytes   | sha256 (first 16) | fetchedAt (UTC)      |
|-----|--------------------------------------------------|--------------------------------------------------|--------|---------|-------------------|----------------------|
| S430 | https://www.rfc-editor.org/rfc/rfc6797.html     | https://www.rfc-editor.org/rfc/rfc6797.html     | 200    | 133951  | f086bfac6974e641  | 2026-10-27T09:14:55Z |
| S431 | https://www.w3.org/TR/CSP3/                     | https://www.w3.org/TR/CSP3/                     | 200    | 1011256 | be8f2468b963df91  | 2026-10-27T09:14:55Z |
| S432 | https://fetch.spec.whatwg.org/                   | https://fetch.spec.whatwg.org/                   | 200    | 1854393 | 63b0a018753c330a  | 2026-10-27T09:14:55Z |
| S433 | https://www.rfc-editor.org/rfc/rfc9110.html     | https://www.rfc-editor.org/rfc/rfc9110.html     | 200    | 1187554 | d431760660ea44e1  | 2026-10-27T09:14:55Z |

- All four: single GET, no redirect (effectiveUrl == url), `content-type: text/html`. Sha256/bytes above verified against the committed files. userAgent `round61` on every request; fetchedAt recorded in UTC on the access date. S431 serves the W3C Working Draft at `/TR/CSP3/` (meta `w3c-status=WD`).

## SPANS:
Each span below is a raw substring of one whitespace-collapsed text node (`body_nodes`, entities not decoded), 6..25 units, <=160 chars, ASCII, page-unique (node_hits==1) — verified by `.files/qc.py`.

- **S430** (16 units) — §5.1 "HSTS Host Declaration": "which is represented by and conveyed via the Strict-Transport-Security HTTP response header field over secure transport" — conveys the HSTS Policy is signalled via the STS field.
- **S431** (18 units) — §3.1 "The Content-Security-Policy HTTP Response Header Field": "HTTP response header field is the preferred mechanism for delivering a policy from a server to a client." — the field name `Content-Security-Policy` sits in the adjacent `<a http-header>` node; the span is the largest compliant single-node substring of the delivery sentence, bound by the entry prose.
- **S432** (9 units) — dfn for the `… blocked due to nosniff` algorithm (§3.6/§3.6.1): "should response to request be blocked due to nosniff" — see MISSES for the value-definition limitation.
- **S433 §8.3** (12 units) — Content-Type definition: "The "Content-Type" header field indicates the media type of the associated representation".
- **S433 §5.5** (17 units) — singleton-field semantics (`singleton_fields` check): "Fields that only anticipate a single member as the field value are referred to as "singleton fields"".
- **S433 §5.2** (25 units) — field-line/once-vs-repeated semantics: "When a field name is only present once in a section, the combined "field value" for that field consists of the corresponding field line value."

## MISSES:
- **S432 `nosniff` value definition** — partial miss under the single-text-node rule. The normative `X-Content-Type-Options = "nosniff"` ABNF and the step `If values[0] is an ASCII case-insensitive match for "nosniff", then return true.` are fragmented by inline markup (`<a>`, `<code>`, custom `<c-*>` ABNF-highlight tags) into sub-6-unit nodes; neither is a substring of any single whitespace-collapsed text node (verified via the `inline_flattened` diagnostic). The strongest compliant single-node span carrying `nosniff` is the algorithm dfn "should response to request be blocked due to nosniff" (recorded above); the literal `nosniff` value cannot be quoted within the rule. Flagged so the scribe binds the `nosniff` value in prose rather than over-reaching a quote.
- No other misses; every seat-requested span was located for S430, S431, and both S433 targets.

VERDICT: 4/4 sources fetched clean (HTTP 200, single GET, receipts + sha256 pinned); 6 spans located & verified — S430 §5.1, S431 §3.1, S432 nosniff dfn, S433 §8.3 + §5.5/§5.2 — with the S432 `nosniff` value-literal flagged as unquotable under the single-text-node rule.
