# ScoutC2Sources — located quote spans (round-61 sources S430–S433)

Method: each span is a raw substring of ONE whitespace-collapsed text node of the
retained body, verified with `qc.py` (a byte-faithful reimplementation of
`.ufo/waves/round-61/c61_recheck_pins.py::body_nodes` — the `>[^<>]+<` node rule with
`script|style|noscript|svg|template|head|nav|aside|header|footer|form` and comments
blanked, entities not decoded). `units()` = one unit per CJK char, one per non-CJK
whitespace token. Every span below: 6..25 units, <=160 chars, ASCII, page-unique
(node_hits == 1). Quotes in the table use ASCII double quotes as required.

## S430 — RFC 6797 (HSTS)
Location: **§5.1 "HSTS Host Declaration"** (RFC body node 431).
The seat-requested sentence conveys that the HSTS Policy is signalled via the
Strict-Transport-Security field. Span (16 units, 119 chars):

    which is represented by and conveyed via the Strict-Transport-Security HTTP response header field over secure transport

Node context: "An HTTP host declares itself an HSTS Host by issuing to UAs an HSTS
Policy, [SPAN] (e.g., TLS)."

## S431 — W3C CSP Level 3
Location: **§3.1 "The Content-Security-Policy HTTP Response Header Field"** (node 1303).
The definition sentence "The `Content-Security-Policy` HTTP response header field is
the preferred mechanism for delivering a policy from a server to a client." is split
across nodes — the field name sits in its own `<a data-link-type="http-header">` node.
The largest compliant single-node substring carries the delivery semantics (the field
name is bound by the entry's prose). Span (18 units, 104 chars):

    HTTP response header field is the preferred mechanism for delivering a policy from a server to a client.

Node context: "The `Content-Security-Policy` [SPAN] The header's value is represented
by the following ABNF".

## S432 — WHATWG Fetch (nosniff)
Location: dfn entry for the `should response to request be blocked due to nosniff`
algorithm (§3.6 `X-Content-Type-Options` header / §3.6.1). Span (9 units, 52 chars):

    should response to request be blocked due to nosniff

LIMITATION (recorded for the scribe, not a quote): the literal value definition
`X-Content-Type-Options = "nosniff"` and the matching step `If values[0] is an ASCII
case-insensitive match for "nosniff", then return true.` are both fragmented by the
spec's inline markup (`<a>`, `<code>`, and custom `<c-*>` ABNF-highlight tags) into
sub-6-unit nodes and are NOT a substring of any single whitespace-collapsed text node.
The full sentences also fail the strict single-node rule (verified via `inline_flattened`
diagnostic). No compliant span names the `nosniff` literal value — the span above is
the strongest single-node span carrying `nosniff` on the page.

## S433 — RFC 9110 (Content-Type §8.3; field-line/singleton §5.2/§5.5)

§8.3 "Content-Type" — Content-Type field definition (12 units, 89 chars):

    The "Content-Type" header field indicates the media type of the associated representation

§5.5 "Field Values" — singleton-field definition (the semantics the `singleton_fields`
check relies on) (17 units, 100 chars):

    Fields that only anticipate a single member as the field value are referred to as "singleton fields"

§5.2 "Field Lines and Combined Field Value" — the once-vs-repeated semantics for a
field name (a field present once maps to its single field-line value) (25 units,
142 chars):

    When a field name is only present once in a section, the combined "field value" for that field consists of the corresponding field line value.
