# ConnectorMistakes — Round 62

## Evidence and recurrence

- Round-61 verifier spot-check, `corpus/lessons/round-61-verifier-spotcheck.md:33,36,41,46`: S432 remained admitted despite the quoted text “Web developers and conformance checkers must use the following” being only a generic lead-in; the reviewer explicitly marked quality and discernment harmed and routed a substantive located excerpt plus grounded QUALITY criterion.
- Frozen round-62 contract, `.ufo/waves/round-62/contract.md:7,9`: the claim requires a substantive S432 quote correction and a QUALITY criterion, and preserves the admitted S432 row. Its source pointers identify the relevant substantive §3.6 sentence.
- Retained source, `.ufo/waves/round-61/sources/S432.html:6151-6154`: the body says the `X-Content-Type-Options` response header “can be used to require checking of a response’s Content-Type header against the destination of a request.” This is materially informative about the field; it is not the rejected generic lead-in.
- Round-61 lesson, `corpus/lessons/round-61.md:37,43`: Gate quote requirements were explicit (6..25 units, ≤160 chars, one collapsed text node, page-unique), but S432's recorded quote was 9 units and still passed that surface-level shape bar. The miss was semantic/substantive grounding, not merely quote length or source existence.
- Earlier corroborating pattern: `corpus/lessons/round-48-verifier-spotcheck.md:91-92` describes a citation gate that catches dead token spans and confirms new quotes against retained bytes; that is useful fidelity coverage but does not establish that a real quote substantively supports its teaching. In contrast, `corpus/lessons/round-26-verifier-spotcheck.md:90` records a qualification omitted from bare “first base” wording, showing the corpus has also encountered semantic-scope defects in otherwise real quotations.

## Finding

Same broad failure class recurred: a source citation/quote can be present and structurally acceptable while failing to ground the knowledge entry's teaching. Round 61's S432 disagreement is a concrete recurrence of that semantic quote-quality gap, not evidence that the existing S432 row should be rejected. The round-62 correction should preserve the row and teach a criterion that distinguishes substantive, scope-matched support from a real but generic lead-in. Exact S432 sentence at the retained lines above gives direct support; contract §9 bounds policy to the Fetch-defined field and disclaims claims about a property's live headers.

## Axes, move, risks, verification

- **Affected axes:** quality and discernment improve if the grounded criterion is added and the knowledge citation corrected. Calibration is the frozen measured claim; this advisory finding does not alter its predicate or evidence. No axis tradeoff identified.
- **One bounded move:** append the substantive §3.6 excerpt and explanation to `corpus/knowledge/response-header-expectations.md`, then append a QUALITY criterion requiring a source quote to substantively support the exact teaching (not merely occur in the source), with a pointer to `corpus/lessons/round-61-verifier-spotcheck.md:33,36,41,46` and S432 retained source lines 6151–6154. Keep S432 admitted.
- **Risk:** overgeneralizing this one example into claims about runtime/property response headers, or treating quote presence/length/uniqueness as semantic support. Contract §9 explicitly limits scope; criterion must keep those separate.
- **Verification:** inspect the committed correction for the substantive quote and its scoped explanation; inspect QUALITY for an explicit semantic-support bar grounded in the cited lesson; retain the S432 admission. C1's frozen counter remains the sole calibration verifier and must be run only by the authorized integration/measurement process after integration.
