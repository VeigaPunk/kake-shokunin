source: S463 — RFC 9111 HTTP Caching, §4.1 Calculating Cache Keys with the Vary Header Field — https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses; opened 2026-11-04; retained body `.ufo/waves/round-88/w1/ScribeVary/rfc9111.html` (178573 bytes, sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64), headers alongside it. S461 and S462 keep their own scopes; this row adds only the §4.1 match rule.
verified-at: 2026-11-04 — own GET completed 18:52:31Z; HTTP 200, 178573 bytes, sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64; byte-identical to the round-86 (`.ufo/waves/round-86/w1/ScribeKnowledge/s457-rfc9111.html`) and round-87 (`.ufo/waves/round-87/w1/ScoutAge/rfc9111.html`) retained copies of the same URL. This seat verified the source text and the decision table below; it did not run the candidate CLI, score the counter or close C2.
recheck: 180d, due 2027-05-03, or sooner after a source change. Re-fetch `https://httpwg.org/specs/rfc9111.html` into an authorized scratch directory of your own, compare the sha256 above, and re-locate §4.1 before reusing the conclusions. The scratch path is yours to choose and is not recorded here; no ephemeral path is named in this line.
ground: freshness — round-88 C2, a bounded conservative Vary-match reader over supplied request-header maps.
scope: the §4.1 match rule as read offline from two supplied header maps; not cache-key construction, storage, revalidation, freshness, serving or any browser behaviour.

# Conservative Vary matching: what §4.1 permits, and what this reader applies

RFC 9111 §4.1 decides whether a stored response may be reused for a request
that a `Vary` field would otherwise distinguish. This entry covers only the
match half of that question: given a `Vary` value and two header maps (the
request that caused the response to be stored, and the request presented now),
does the stored response match?

The reader described here is deliberately conservative. It applies the first
two of the three transformations §4.1 lists and declines the third, so every
`match` it produces is a transformation the source permits, while a
`mismatch` may be stricter than a field-specific rule would be. It never
reads a clock, a socket or a cache.

## Located quotes

Retained body: `.ufo/waves/round-88/w1/ScribeVary/rfc9111.html`
(sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64).
All §4.1 paragraphs sit on retained HTML line 269; the paragraph anchors are
`rfc.section.4.1.p.1` … `rfc.section.4.1.p.8`.

Quoted spans below are blockquoted, not double-quoted, so that a
span-extraction check reads them as source text rather than as emphasis.
Each is a **raw substring** of the retained body
(`.ufo/waves/round-88/w1/ScribeVary/rfc9111.html`, sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64);
the class was derived with the lane's own tool, `python3 -B
scripts/quote_class.py classify --raw <body> --text <flat rendering>
--quote <span>`, against the flat-text rendering produced by
`.ufo/waves/round-63/quote-class/extract_text.py`. All §4.1 paragraphs sit on
retained HTML line 269; the paragraph anchors are `rfc.section.4.1.p.1` …
`rfc.section.4.1.p.8`.

**The MUST NOT sentence** — §4.1 paragraph 1 (`rfc.section.4.1.p.1`). The
sentence reads, in full: *When a cache receives a request that can be
satisfied by a stored response and that stored response contains a Vary header
field, the cache MUST NOT use that stored response without revalidation unless
all the presented request header fields nominated by that Vary field value
match those fields in the original request (i.e., the request that caused the
cached response to be stored).* The subject and the modal sit in their own
markup nodes, so the contiguous raw run that carries the rule is quoted
instead, and the modal and subject are named in prose above:

> use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match those fields

[INFERENCE] The subject (*the cache*) and the modal (*MUST NOT*) are separate
markup nodes in the retained rendering, which is why the quoted span starts
at *use*. The full sentence as printed above is **collapsed-only** against
the raw body by the lane's own classifier (the same classifier returns
`raw-substring` for the quoted span); it is reproduced here from the flat
rendering, not claimed as a raw substring.

**The three permitted transformations** — §4.1 paragraphs 2 and 3
(`rfc.section.4.1.p.2`, `rfc.section.4.1.p.3`). Paragraph 2 gives the
definition and paragraph 3 the list. The definition reads in full: *The
header fields from two requests are defined to match if and only if those in
the first request can be transformed to those in the second request by
applying any of the following:*; the quoted run below starts at *defined*
and stops before *by applying any of the following*, so that it stays inside
the 25-unit ceiling the lane sets for a new entry's quoted spans.

> defined to match if and only if those in the first request can be transformed to those in the second request

> adding or removing whitespace, where allowed in the header field's syntax

> combining multiple header field lines with the same field name

> normalizing both header field values in a way that is known to have identical semantics, according to the header field's specification

The third item continues, in the same list element, with two examples the
source gives: reordering field values when order is not significant, and
case-normalization where values are defined to be case-insensitive. [INFERENCE]
Both examples belong to the transformation this reader declines, which is why
a `mismatch` here may be stricter than the field's own specification would
be. The second item names RFC 9110 §5.2 for the combination; that pointer is
in its own markup node, so the quoted span stops before it.

**The absence sentence** — §4.1 paragraph 4 (`rfc.section.4.1.p.4`):

> a header field is absent from a request, it can only match another request if it is also absent there.

The paragraph opens with the conditional clause *If (after any normalization
that might take place)*; the quoted span starts at *a header field* because
that is the contiguous run of raw text.

**The `*` sentence** — §4.1 paragraph 5 (`rfc.section.4.1.p.5`):

> header field value containing a member "*" always fails to match.

The paragraph reads in full: *A stored response with a Vary header field value
containing a member `"*"` always fails to match.* The word *Vary* sits in its
own markup node, so the quoted span starts at *header field value*. The
member is the single asterisk character, written in the source inside ASCII
double quotes; the quoted span above is a raw substring of the retained body.

### Which quotes are page-unique

Each of the seven quoted spans above occurs exactly once in the retained body,
and each occurs in no other retained page in this lane: all seven count as
page-unique. Verified with a substring-and-count comparison against
`corpus/lessons/round-81-gate/rfc9110.html`,
`corpus/lessons/round-81-gate/rfc9110.txt`, the retained RFC 7234 body at
`.ufo/waves/round-86/w1/ScribeKnowledge/rfc7234-contrast.txt` and
`.ufo/waves/round-61/sources/S433.html`. (A shorter form of the whitespace
item — *adding or removing whitespace, where allowed in the header field*,
without the final *'s syntax* — does occur in the retained RFC 7234 body.
The longer form quoted here does not, which is why the quoted span was kept
at its full length rather than trimmed.)

## Decision table

Each rule is applied in the order listed; the first rule that fires decides
the verdict. `match` and `mismatch` are exit 0 with the verdict on stdout and
empty stderr; `invalid_input:` on stderr with empty stdout is exit 1.
*Not a token* means the string contains a character outside the HTTP token
set (`!#$%&'*+-.^_`|~` plus digits and letters).

| # | Rule | Verdict |
|---|---|---|
| R1 | The `Vary` value is not a string | `invalid_input:` (exit 1) |
| R2 | The `Vary` value has no member, or has an empty member after leading/trailing SP/HTAB is stripped | `invalid_input:` (exit 1) |
| R3 | A `Vary` member is neither `*` nor a token | `invalid_input:` (exit 1) |
| R4 | A header map is not an object, or a field name is not a token, or two field names in one map differ only in case (ambiguous duplicate) | `invalid_input:` (exit 1) |
| R5 | A field value is neither a string nor a non-empty list of strings | `invalid_input:` (exit 1) |
| R6 | The `Vary` value contains a `*` member | `mismatch` |
| R7 | A nominated field is present in both maps and the two values are byte-identical after leading/trailing SP/HTAB is stripped | `match` |
| R8 | A nominated field is present in both maps and the values differ after that trimming | `mismatch` |
| R9 | A nominated field is present in exactly one of the two maps | `mismatch` |
| R10 | A nominated field is present in neither map | contributes no difference; the field matches |
| R11 | Every nominated field is present in both maps and matches under R7 | `match` |

Field names are compared ASCII case-insensitively, so `Accept-Encoding` and
`accept-encoding` name the same field and duplicate `Vary` members that
differ only in case are redundant. A field map value given as a list is
treated as several field lines of that field and is combined in order with
`, ` (comma and SP), per RFC 9110 §5.2; the combination is ordered, so
`["gzip", "br"]` becomes `gzip, br` and not `br, gzip`.

### The twenty frozen cases

The table above reproduces all twenty frozen verdicts exactly. The mapping
is by the rule that fires first.

| Case | Input in one line | Rule | Verdict |
|---|---|---|---|
| 1 | `accept-encoding`; gzip / gzip | R7, R11 | match |
| 2 | `Accept-Encoding`; gzip / gzip (name case differs) | R7, R11 | match |
| 3 | `accept-encoding`; gzip / GZip | R8 | mismatch |
| 4 | `accept-encoding`; absent / absent | R10, R11 | match |
| 5 | `accept-encoding`; absent / gzip | R9 | mismatch |
| 6 | `accept-encoding`; gzip / absent | R9 | mismatch |
| 7 | `*`; gzip / gzip | R6 | mismatch |
| 8 | `accept-encoding, *`; gzip / gzip | R6 | mismatch |
| 9 | `accept-encoding`; `" gzip "` / gzip | R7, R11 | match |
| 10 | `accept-encoding`; `gzip, br` / `br, gzip` | R8 | mismatch |
| 11 | `accept-encoding, accept-language`; gzip+en / gzip+en | R7, R11 | match |
| 12 | `accept-encoding, accept-language`; gzip+en / gzip+fr | R8 | mismatch |
| 13 | `Accept-Encoding, accept-encoding`; gzip / gzip | R7, R11 | match |
| 14 | empty `Vary` value | R2 | `invalid_input:` (exit 1) |
| 15 | `accept encoding` (SP inside a member) | R3 | `invalid_input:` (exit 1) |
| 16 | `accept-encoding`; `gzip, br` / `["gzip", "br"]` | R7, R11 | match |
| 17 | `accept-encoding`; `br, gzip` / `["gzip", "br"]` | R8 | mismatch |
| 18 | `accept-encoding`; `gzip;q=1` / `gzip; q=1` | R8 | mismatch |
| 19 | `accept-encoding`; integer field value | R5 | `invalid_input:` (exit 1) |
| 20 | integer `Vary` value | R1 | `invalid_input:` (exit 1) |

Case 2 is decided by ASCII case-insensitive name comparison. That rule is
not in §4.1: it is RFC 9110 §5.1, whose sentence *Field names are
case-insensitive* is held under S433 with its own retained body at
`.ufo/waves/round-61/sources/S433.html`. That sentence is quoted here from
S433's body, not from this entry's row body, and it is not one of the seven
spans counted above. Cases 16 and 17 turn on the ordered `, ` combination,
which §4.1's second permitted transformation names by pointing at RFC 9110
§5.2.

### Precedence: validation before the wildcard rule

R4 and R5 are checked before R6. A request whose `Vary` value contains `*`
*and* whose header map is malformed is refused with `invalid_input:`, not
answered with `mismatch`. The frozen case set does not contain such a case
(frozen cases 7 and 8 carry a `*` member, and both have well-formed header
maps; frozen case 19 has a malformed map and no `*`), so the 20 frozen
verdicts alone cannot tell this ordering from the opposite one. The
200-case seeded population does contain such cases — **r53, r150 and
r193** — and the counter's own reference implementation answers all three
with `invalid`. This precedence is declared, not incidental: it is the
behaviour frozen in `.ufo/waves/round-88/c88_vary.py` (`reference()`, the
`if star:` branch after the `normalise()` call).

## Error patterns

- Treating a `*` member as an ordinary field name. `*` is not a token and
  not a field; it always fails.
- Answering `mismatch` because a value differs only in case, in element
  order, or in internal whitespace. Those are the field-specific
  normalizations §4.1's third transformation permits and this reader
  declines; the difference is a deliberate conservatism, not a bug.
- Folding values case-insensitively "because field names are
  case-insensitively". The name rule (RFC 9110 §5.1) does not extend to
  values; a `GZip` value differs from `gzip`.
- Reordering a combined field value to make two requests match. The
  combination is ordered, so `gzip, br` and `br, gzip` differ.
- Trimming whitespace inside a value rather than only leading and trailing
  it. `gzip;q=1` and `gzip; q=1` differ; ` gzip ` and `gzip` do not.
- Reading a `match` as permission to reuse. §4.1 paragraph 1 governs reuse
  *without revalidation*; a `match` verdict is a statement about the
  nominated fields only.
- Treating a missing field as a mismatch by default. A field absent from
  both requests matches.
- Letting an unvalidated input fall through to a verdict. A non-string
  `Vary` value, a non-token member, a non-object header map and a
  non-string field value are all refused, not guessed.
- Reading a `mismatch` as *the field is different* in general. It is *this
  reader cannot show a permitted transformation makes these equal*.

## Runnable checklist

Run from the lane root. Each command reads one JSON object on stdin with
the `Vary` value as `vary` and the two header maps as `stored` (the request
that caused the response to be stored) and `presented` (the request presented
now). Exit 0 prints the verdict on stdout; exit 1 prints `invalid_input:` on
stderr and nothing on stdout.

1. One match:

   ```sh
   printf '%s' '{"vary":"accept-encoding","stored":{"accept-encoding":"gzip"},"presented":{"accept-encoding":"gzip"}}' | python3 -B scripts/vary_match.py
   ```

   Expected: `match` on stdout, exit 0, empty stderr.

2. One mismatch:

   ```sh
   printf '%s' '{"vary":"accept-encoding","stored":{"accept-encoding":"gzip"},"presented":{"accept-encoding":"br"}}' | python3 -B scripts/vary_match.py
   ```

   Expected: `mismatch` on stdout, exit 0, empty stderr.

3. One refused input:

   ```sh
   printf '%s' '{"vary":"","stored":{},"presented":{}}' | python3 -B scripts/vary_match.py
   ```

   Expected: exit 1, empty stdout, stderr beginning `invalid_input:`.

   The `scripts/vary_match.py` path is the production path the round
   contract names; the file is integrated by L1. At the base commit
   `f4479c14813037ad993a49a3dee4028763470f7a` no such script exists, so
   these three commands are expected to fail until the script lands. The
   verdict expectations above are the counter's reference verdicts for the
   same three inputs, computed from the frozen reference implementation.

## What this entry does not establish

- **No cache-key claim.** Nothing here constructs, derives or compares a
  cache key. §4.1 paragraph 1 governs which stored response may be
  considered; the key itself is a separate construction.
- **No storage claim.** Whether a response may be stored at all is
  §3's question, not §4.1's.
- **No revalidation claim.** A `match` verdict says the nominated fields
  are not shown to differ under this profile. It does not say revalidation
  is unnecessary: paragraph 1 permits reuse *without revalidation* only
  when the fields match, and other conditions can still require it.
- **No freshness claim.** Age, lifetime and current age are separate
  questions; S462 holds the age-arithmetic slice.
- **No browser claim.** No user agent, cache implementation or HTTP client
  behaviour was observed or asserted. Nothing here says any real cache
  makes these decisions this way.
- **No live surface is asserted clean.** The only network access was one
  GET of the specification. No site, header set or response was probed.
- **The conservative asymmetry.** `match` is always a permitted
  transformation: the reader only reports `match` when the two values are
  equal after transformations §4.1 permits (whitespace trimming, ordered
  field-line combination). `mismatch` may be stricter than a field-specific
  rule: a `mismatch` on `GZip` against `gzip`, on `br, gzip` against
  `gzip, br`, or on `gzip; q=1` against `gzip;q=1` would be permitted by
  the third transformation for some fields, and this reader declines that
  transformation. The asymmetry is one-directional and never in the unsafe
  direction.
- **Ordered line combination and OWS trimming are local adapter
  conventions.** The RFC 9110 §5.2 pointer for combining field lines and
  the choice of SP/HTAB as the trimmed whitespace are this reader's
  conventions for rendering an input, not quotations from §4.1. §4.1 itself
  says "adding or removing whitespace, where allowed in the header field's
  syntax" without naming a whitespace set, and points at RFC 9110 §5.2 for
  the combination without fixing a joiner here. A reader that combined
  field lines differently, or trimmed a different whitespace set, would
  produce different verdicts on some inputs while still satisfying §4.1.
- **The decision table is a reader specification, not a conformance
  suite.** The twenty frozen cases are hand-labelled expectations; the
  200-case seeded population is scored against the counter's own reference
  implementation of the profile. Passing either is not proof of RFC
  conformance, and this entry records no score of its own.
