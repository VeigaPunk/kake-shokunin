# CriticQuoteDefect — S432 quote and correction

## Counterexample / finding

The proposed replacement is substantively relevant to the existing xcto_nosniff_value teaching, but it is not by itself evidence for the whole rule. S432 §3.6 states that the `X-Content-Type-Options` response header can require checking a response’s `Content-Type` against request destination. The existing entry additionally asserts the literal `nosniff` value grammar and algorithmic comparison; those are separate claims supported by the §3.6 material described at entry lines 81–87, not by the replacement sentence alone. A correction that presents the sentence as proving the literal value rule would overclaim.

The exact disagreement is quote adequacy, not S432 admission: the round-61 spot-check keeps `S432 / Fetch | Admit | Disagree`, saying the “Web developers…” text is a generic lead-in rather than substantive evidence for the expectation (spot-check lines 32–36). Retain that row and its reason unchanged. An appended correction using the coherent §3.6 sentence at retained source lines 6151–6154 directly addresses the stated defect by replacing generic lead-in evidence with a proposition naming the response header and checking relationship. It supports the entry’s header-purpose framing, while the existing ABNF/algorithm citations must remain separately scoped to value semantics.

## Evidence and commands

- `read /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html:6151-6154` — source sentence spans lines 6152–6154: “response header can be used to require checking of a response’s Content-Type header against the destination of a request.” Line 6151 supplies the `X-Content-Type-Options` heading/subject markup.
- `read /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61-verifier-spotcheck.md` — lines 32–36 show Admit/Disagree and identify the generic lead-in as the defect; lines 41–47 record quality/discernment harm and route a substantive located excerpt while preserving the row.
- `read /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/response-header-expectations.md` — lines 71–94 show the xcto class; lines 81–87 separately describe the ABNF and algorithm, highlighting why the replacement sentence must not be conflated with value-rule support.
- `read /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md:1-38` — existing rows distinguish admit/reject behaviors and cite motivating evidence; lines 28–29 say changes append a superseding row and motivating lesson.

## Smallest safe correction

Append a clearly labeled correction to the knowledge entry quoting the complete substantive proposition (with the markup-supplied `X-Content-Type-Options` subject made explicit), cite S432 §3.6 and retained lines 6151–6154, and explain narrowly that it supports the header’s Content-Type/destination-checking purpose. State that the separate ABNF/algorithm passage supports the `nosniff` value comparison; do not imply the quoted sentence establishes that grammar. Append a QUALITY criterion grounded in the round-61 disagreement that rejects generic lead-ins as evidence for a teaching claim, independently of source admission, and requires preserving the original finding while recording the correction. Do not rewrite the historical S432 row or change its admission/status.

## Impacted axes

Calibration/discernment is addressed only if the correction and criterion are actually appended and the historical disagreement remains visible; quote relevance alone is a knowledge-quality correction, not proof that the non-author agreed. Quality is directly implicated by the recorded failed evidence bar. No conclusion about post-change state or independent closure is made here.