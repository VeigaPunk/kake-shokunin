# Round 93 — kake: self-assessment conformance, and a conditional request evaluation instrument

Author: kake L1 (`KakeR93`). Base `10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5`; freeze
`bb8012fee38c0e497cdaf36337072737bca0b3cd`. Outside closure owns admission and the non-author
spot-check of this Gate.

## Gate

Sources opened this round (CORPUS.md rule 1), by the L1 with one public GET each and retained under
`.ufo/waves/round-93/L1/src/`:

| URL | HTTP | bytes | sha256 | opened |
|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-04T22:20Z |
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-04T22:20Z |

`rfc9111.txt` is byte-identical to the round-92 retained body, so the round-92 §4.2.2 ground is
unchanged at this fetch. Line numbers below are plain-text lines of these bodies.

Admits:

- **§13.2.2 lines 6229–6231** — "A recipient cache or origin server MUST evaluate the request
  preconditions defined by this specification in the following order" (20 words). Grounds the
  decision order of contract clauses 7–12.
- **§13.1.1 lines 5794–5795** — "An origin server MUST use the strong comparison function when
  comparing entity tags for If-Match" (15 words). Grounds If-Match using strong comparison only.
- **§13.1.2 lines 5880–5881** — "A recipient MUST use the weak comparison function when comparing
  entity tags for If-None-Match" (15 words). Grounds If-None-Match using weak comparison only.
- **§8.8.3.2 lines 3648–3653** — the two definitions, "two entity tags are equivalent if both are
  not weak and their opaque-tags match character-by-character" (15 words) and the weak counterpart
  "… if their opaque-tags match character-by-character, regardless of either or both being tagged
  as 'weak'" (19 words). Grounds both comparison functions and the Table 3 hand cases.
- **§13.1.2 lines 5930–5933** — "the origin server MUST respond with either a) the 304 (Not
  Modified) status code if the request method is GET or HEAD or b) the 412" (23 words). Grounds
  clause 10's 304-versus-412 split by method.
- **§13.1.3 lines 5956–5958** — "A recipient MUST ignore If-Modified-Since if the request contains
  an If-None-Match header field" (16 words). Grounds If-None-Match precedence over
  If-Modified-Since.
- **§13.1.3 lines 5963–5965** — ignore when "the request method is neither GET nor HEAD" (9 words).
  Grounds clause 11's method gate.
- **§13.1.4 lines 6037–6039** — "A recipient MUST ignore If-Unmodified-Since if the request contains
  an If-Match header field" (14 words). Grounds clause 9's suppression rule.
- **§13.1.4 lines 6072–6073** — "earlier than or equal to the date provided in the field value, the
  condition is true" (16 words). Grounds the `<=` boundary and the equality case.
- **RFC 9111 §4.3.2 lines 889–891** — "the If-Match and If-Unmodified-Since conditional header
  fields are not applicable to a cache" (14 words). Grounds the contract's `role: "cache"` skip.

Rejects:

- **Reject (row candidate): the RFC-Editor errata pages as a grounding row for this contract.** The
  RFC 9110 errata listing carries 14 records and none names a section in 13.x or 8.8.3.x; the RFC
  9111 listing carries two *Reported* (not Verified) records and they touch §3.5 and §4.3.4, not
  §4.3.2 or §13.2.2. So the pages ground nothing about this round's clauses. Flip: an erratum that
  touches §4.3.2, §13.1.x, §13.2.2 or §8.8.3.2.
- **Reject (row candidate): a secondary explainer for the precedence order.** The specification text
  is available and grounds the order directly; a secondary row would be tier inflation and would
  cite ground the lane already holds at tier A. Flip: a precedence point the RFC leaves unstated
  that the secondary source documents with a locator.

### Source-seat re-verification (w1/ScribeSources)

The Gate section above was written by the L1 from the L1's own retained bodies. This block is the
source seat's independent re-verification, done from bodies this seat fetched itself this round
with one public GET each and retained under `.ufo/waves/round-93/w1/ScribeSources/src/`:

| URL | HTTP | bytes | sha256 | opened (UTC) | `cmp` vs `.ufo/waves/round-93/L1/src/` |
|---|---|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9110.txt` | 200 | 502 941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | 2026-11-05T01:26:51Z | identical, exit 0 |
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84 477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` | 2026-11-05T01:26:51Z | identical, exit 0 |

`rfc9111.txt` is also byte-identical to the round-92 retained body
(`.ufo/waves/round-92/L1/src/rfc9111.txt`, `cmp` exit 0), so the round-92 §4.2.2 ground is
unchanged at this fetch. Every quote below was checked mechanically to be an exact substring of its
cited plain-text line span, and to be within the ≤25-word rule, by
`.ufo/waves/round-93/w1/ScribeSources/verify_quotes.py` (receipt
`.ufo/waves/round-93/w1/ScribeSources/quotes.json`, `all_ok=true`, exit 0).

Admits (source-seat, each re-located in the same bodies; line spans are corrected where the
Gate above cites a span that does not contain its quote):

- **§13.2.2 lines 6233–6234** — "A recipient cache or origin server MUST evaluate the request
  preconditions defined by this specification in the following order" (19 words). Grounds the
  decision order of contract clauses 7–12.
- **§13.1.1 lines 5794–5795** — "An origin server MUST use the strong comparison function when
  comparing entity tags for If-Match" (15 words). Grounds If-Match using strong comparison only.
- **§13.1.2 lines 5880–5881** — "A recipient MUST use the weak comparison function when comparing
  entity tags for If-None-Match" (14 words). Grounds If-None-Match using weak comparison only.
- **§8.8.3.2 lines 3648–3649** — "two entity tags are equivalent if both are not weak and their
  opaque-tags match character-by-character" (15 words). Grounds the strong comparison function; the
  worked pairs at lines 3658–3668 give its table cases.
- **§13.1.2 lines 5930–5931** — "the origin server MUST respond with either a) the 304 (Not
  Modified) status code if the request method is GET or HEAD" (22 words). Grounds clause 10's
  304-versus-412 split by method.
- **§13.1.3 lines 5956–5957** — "A recipient MUST ignore If-Modified-Since if the request contains
  an If-None-Match header field" (13 words). Grounds If-None-Match precedence over
  If-Modified-Since.
- **§13.1.3 lines 5963–5966** — "the request method is neither GET nor HEAD" (8 words). Grounds
  clause 11's method gate.
- **§13.1.4 lines 6037–6038** — "A recipient MUST ignore If-Unmodified-Since if the request contains
  an If-Match header field" (13 words). Grounds clause 9's suppression rule.
- **§13.1.4 lines 6072–6073** — "earlier than or equal to the date provided in the field value, the
  condition is true" (16 words). Grounds the `<=` boundary and the equality case.
- **RFC 9111 §4.3.2 lines 889–890** — "the If-Match and If-Unmodified-Since conditional header
  fields are not applicable to a cache" (13 words). Grounds the contract's `role: "cache"` skip.

Three spans in the Gate above do not contain the quote they are attached to, and one quote exceeds
the ≤25-word rule; the corrected spans and quote lengths are in the list above. The spans at issue:
the §13.2.2 evaluation-order sentence is at lines 6233–6234, not 6229–6231 (lines 6229–6231 carry
the "lost update preconditions" rationale); the §13.1.3 method gate spans lines 5963–5966, not
5963–5965 (the phrase "neither GET nor HEAD" crosses into line 5966); and the weak-comparison
definition at lines 3651–3653 is broken across lines by the hyphenation of "opaque-tags", so the
quote as printed in the Gate above is not a literal substring of its span. The §13.1.2 304-versus-412
quote at 23 words is over the ≤25-word rule at 26 words and is shortened above to 22 words. These
are recorded as findings for the round's routed list, not repaired in the Gate above.

Rejects (source-seat):

- **Reject (row candidate): a row for the RFC-Editor errata pages as a grounding row for this
  contract.** The RFC 9110 errata listing (`https://www.rfc-editor.org/errata/rfc9110`, HTTP 200,
  97 750 B, sha256 `cec32fd170146656d933f627b512f2e027ae5c3592f5ec7760c3627493b30505`, fetched
  2026-11-05T01:30:04Z, byte-identical to the L1's retained
  `.ufo/waves/round-93/L1/src/errata-9110.html`) carries 14 records and none targets a section in
  13.x or 8.8.3.x; the RFC 9111 listing (`https://www.rfc-editor.org/errata/rfc9111`, HTTP 200,
  40 383 B, sha256 `1df394f9c04e33e74bf69360e3b7d3bbdeccbe80e27caaa18fdace216ccb54a4`, byte-identical
  to the L1's retained `errata-9111.html`) carries 4 records, of which the two *Reported* ones
  (eid 9004, 9185) touch §3.5 and §4.3.4, one is *Held for Document Update* (eid 9166, §5.2.3) and
  one is *Rejected* (eid 7695, §4.3.2). So the pages carry no accepted change to §13.1.x, §13.2.2,
  §8.8.3.2 or §4.3.2, and they ground nothing about this round's clauses. Flip: an erratum in
  *Verified* or *Held for Document Update* status that touches §13.1.x, §13.2.2, §8.8.3.2 or §4.3.2.
- **Reject (row candidate): a row for a secondary explainer of the precedence order.** The
  specification text is available and grounds the order directly at tier A; a secondary row would
  be tier inflation and would cite ground the lane already holds. Flip: a precedence point the RFC
  leaves unstated that the secondary source documents with a locator.
- **Reject (proposition): "the RFC fixes the 304 body content".** RFC 9110 §15.4.5 lines 7477–7478
  says a 304 response "is terminated by the end of the header section; it cannot contain content or
  trailers", and §15.4.5 lines 7456–7462 lists the header fields the sender must or should
  regenerate; the RFC fixes which *metadata* a 304 carries, not the body of the stored
  representation, whose bytes the client already holds. Flip: a section that states the 304's body
  content.

## Registry

- Rows added: S471–S476 (six rows; see the report's Sources & frontier section for the id list).
- Rows touched: none.
- Census `validate --root … kake`: exit 0 before (`.ufo/waves/round-93/assimilation/census-before.txt`)
  and exit 0 after; W04 advisories 31 → 37 (the new rows re-scope `rfc9110.txt`, already held at
  S033/S453/S454/S455/S465/S466).

## Mistakes

| # | Class | Evidence | Captured-by | Fix (shown able to fail) |
|---|---|---|---|---|
| 1 | A frozen contract and its own reference disagreed on a field's type | the reference refused `if_unmodified_since: 600` as "date field must be a raw field value string" while the contract's input block declares `if_modified_since`/`if_unmodified_since` as ints; the first `--selftest` run read `reference drift on ius/older-modification-passes` | the counter's pre-freeze reference self-check (`controls/ctl-c2-fixtures.txt` was produced only after the fix) | clause 1 of the contract and the reference both now read the two date fields as `null` or a non-negative int; the refusal cases were re-keyed to a string date and a bool date, and the generator emits ints |
| 2 | A sandbox denied a module the runner itself needs | the positive control failed with `ModuleNotFoundError: No module named 'pkgutil'` inside `runpy.run_path` because `sys.path[:] = [root]` ran without preloading the stdlib modules the sandbox itself uses | the pre-freeze fixture battery (`selftest FAIL: … pos-good.py admitted=False hand=14/44`) | the sandbox now preloads `importlib.machinery, importlib.util, json, os, pkgutil, runpy, sys` before the path reset, exactly as the round-92 sandbox does; the same control then reads `7/7 fixtures scored as declared` |
| 3 | A self-test asserted through the production entry point, so its own fixture could never pass | `report()` applies the real `BASE_PINS`, so the synthetic lane read `pins=short` even with zero mismatches and the "repaired" revision could not exit 0 | the C1 selftest's own exit-code assertion | the selftest now asserts on `audit(..., base_pins=synth)` and checks `mismatches`/`short` directly; `controls/ctl-c1-selftest.txt` prints `5/5 planted findings, exit 1 on planted, exit 0 on repaired` |
| 4 | A control never wrote its own fixture | the "planted" commit was empty (`git commit` exit 1, "nothing to commit") and the battery reported `planted findings []` — the planted defect set was built but `write_all(planted)` was never called | the selftest's expected-findings assertion (an empty finding list where five were declared) | the write call was added; the same battery then reports exactly the five planted `(class, path)` pairs |

Disclosure: mistakes 1–4 were found and fixed before the freeze commit; no counter, case, predicate,
label or target was changed after it. Every instrument defect the wave found is routed in the
round's report, not patched.

## Wave review and Routed

Appended after the wave settles; see the round report for the seat-by-seat record.
