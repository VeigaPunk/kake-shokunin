<!-- ScribeSources round-93: Gate material for corpus/lessons/round-93.md.
     The L1 appends this to the lesson's `## Gate` section, replacing or
     superseding the L1's own draft Gate paragraph (append-only; do not
     rewrite the L1's existing lines — append this block as a second
     "Admits:"/"Rejects:" group, or as its own section, keeping the
     `## Gate` heading line exactly once).

     Every quote below was checked mechanically against the bodies this seat
     fetched itself this round (retained under w1/ScribeSources/src/) by
     w1/ScribeSources/verify_quotes.py; receipt: w1/ScribeSources/quotes.json
     (all_ok=true, exit 0). Every line span is a plain-text line number of
     those bodies.

     Fetch provenance (this seat, one public GET each, 2026-11-05T01:26:51Z):

     | URL | HTTP | bytes | sha256 | cmp vs .ufo/waves/round-93/L1/src/ |
     |---|---|---|---|---|
     | https://www.rfc-editor.org/rfc/rfc9110.txt | 200 | 502941 | 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a | identical (exit 0) |
     | https://www.rfc-editor.org/rfc/rfc9111.txt | 200 | 84477 | aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e | identical (exit 0) |

     `rfc9111.txt` is also byte-identical to the round-92 retained body, so
     the round-92 §4.2.2 ground is unchanged at this fetch.

     Gate material follows. -->

### Admits (source-seat, w1/ScribeSources)

- **RFC 9110 §13.2.2 lines 6233–6234** — "A recipient cache or origin server MUST evaluate the
  request preconditions defined by this specification in the following order" (19 words). Grounds
  the decision order of contract clauses 7–12: the order is fixed by the specification, not by the
  tool.
- **RFC 9110 §13.1.1 lines 5794–5795** — "An origin server MUST use the strong comparison function
  when comparing entity tags for If-Match" (15 words). Grounds If-Match comparing strongly only.
- **RFC 9110 §13.1.2 lines 5880–5881** — "A recipient MUST use the weak comparison function when
  comparing entity tags for If-None-Match" (14 words). Grounds If-None-Match comparing weakly only.
- **RFC 9110 §8.8.3.2 lines 3648–3649** — "two entity tags are equivalent if both are not weak and
  their opaque-tags match character-by-character" (15 words). Grounds the strong comparison
  function; the worked pairs at lines 3658–3668 give its table cases.
- **RFC 9110 §13.1.2 lines 5930–5931** — "the origin server MUST respond with either a) the 304
  (Not Modified) status code if the request method is GET or HEAD" (22 words). Grounds clause 10's
  304-versus-412 split by method.
- **RFC 9110 §13.1.3 lines 5956–5957** — "A recipient MUST ignore If-Modified-Since if the request
  contains an If-None-Match header field" (13 words). Grounds If-None-Match taking precedence over
  If-Modified-Since.
- **RFC 9110 §13.1.3 lines 5963–5966** — "the request method is neither GET nor HEAD" (8 words).
  Grounds clause 11's method gate.
- **RFC 9110 §13.1.4 lines 6037–6038** — "A recipient MUST ignore If-Unmodified-Since if the request
  contains an If-Match header field" (13 words). Grounds clause 9's suppression rule.
- **RFC 9110 §13.1.4 lines 6072–6073** — "earlier than or equal to the date provided in the field
  value, the condition is true" (16 words). Grounds the `<=` boundary and the equality case.
- **RFC 9111 §4.3.2 lines 889–890** — "the If-Match and If-Unmodified-Since conditional header
  fields are not applicable to a cache" (13 words). Grounds the contract's `role: "cache"` skip.

### Rejects (source-seat, w1/ScribeSources)

- **Reject (row candidate): a row for the RFC-Editor errata pages as a grounding row for this
  contract.** The RFC 9110 errata listing (`https://www.rfc-editor.org/errata/rfc9110`, HTTP 200,
  97 750 B, sha256 `cec32fd170146656d933f627b512f2e027ae5c3592f5ec7760c3627493b30505`, fetched
  2026-11-05T01:30:04Z, byte-identical to the L1's retained `.ufo/waves/round-93/L1/src/
  errata-9110.html`) carries 14 records and none targets a section in 13.x or 8.8.3.x; the RFC 9111
  listing (`https://www.rfc-editor.org/errata/rfc9111`, HTTP 200, 40 383 B, sha256
  `1df394f9c04e33e74bf69360e3b7d3bbdeccbe80e27caaa18fdace216ccb54a4`, byte-identical to the L1's
  retained `errata-9111.html`) carries 4 records, of which the two *Reported* ones (eid 9004, 9185)
  touch §3.5 and §4.3.4, one is *Held for Document Update* (eid 9166, §5.2.3) and one is *Rejected*
  (eid 7695, §4.3.2). So the pages carry no accepted change to §13.1.x, §13.2.2, §8.8.3.2 or
  §4.3.2, and they ground nothing about this round's clauses. Flip: an erratum in *Verified* or
  *Held for Document Update* status that touches §13.1.x, §13.2.2, §8.8.3.2 or §4.3.2.
- **Reject (row candidate): a row for a secondary explainer of the precedence order.** The
  specification text is available and grounds the order directly at tier A; a secondary row would be
  tier inflation and would cite ground the lane already holds. Flip: a precedence point the RFC
  leaves unstated that the secondary source documents with a locator.
- **Reject (proposition): "the RFC fixes the 304 body content".** RFC 9110 §15.4.5 lines 7477–7478
  says a 304 response "is terminated by the end of the header section; it cannot contain content or
  trailers", and §15.4.5 lines 7456–7462 lists the header fields the sender must or should
  regenerate; the RFC fixes which *metadata* a 304 carries, not the body of the stored
  representation, whose bytes the client already holds. Flip: a section that states the 304's body
  content.
