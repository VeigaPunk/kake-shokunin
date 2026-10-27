# ScoutQUALITY — round 62

## Finding

**No equivalent substantive-support criterion exists in `corpus/QUALITY.md`.** The nearest precedent is the round-29 “A Gate quote is found in retained source text” criterion (`corpus/QUALITY.md:375–388`), which tests quote truth: exact substring in retained visible source text, digest verified against receipt. It expressly distinguishes shape from truth, but does not require that a true quote substantively support the teaching claim attached to it. Round 53's locator criterion (`QUALITY.md:1116`) requires the locator to identify the section containing the quote; it likewise does not test semantic support. The round-29 rule is therefore complementary, not equivalent.

## Grounded evidence

- Non-author verifier spot-check, `corpus/lessons/round-61-verifier-spotcheck.md:32–36`: S432 was admitted, but the quoted §3.6 text, “Web developers and conformance checkers must use the following,” is a generic lead-in, not substantive evidence for the response-header expectation. The verifier explicitly says discernment was harmed and that the finding had not yet been learned into QUALITY.
- Original S432 Gate record remains at `corpus/lessons/round-61.md:43`: this is historical evidence and should remain unchanged.
- The existing S432 row was also independently quote-checked in `.ufo/waves/round-61/w1/ReviewerC2EntryQuotes.md:13–14,27–29`; it describes the quoted material as introductory/partial, not a quote carrying the normative value grammar. This does not overturn the round-61 admission and is secondary evidence to the non-author finding.
- Retained S432 body, `.ufo/waves/round-61/sources/S432.html:6151–6154` (WHATWG Fetch §3.6): body says the `X-Content-Type-Options` response header “can be used to require checking of a response’s Content-Type header against the destination of a request.” This describes what the header does; the following section contains the nosniff algorithm. It is materially more relevant to the row's response-header subject than the generic ABNF introduction.

## How to add without rewriting history

Append a new dated/round-labelled criterion to the end of the relevant QUALITY section (or a new round-62 section), grounded in `corpus/lessons/round-61-verifier-spotcheck.md:32–36`, and state the substantive-support test separately from round-29's exact-text/digest test: a retained, quote-true excerpt must express evidence relevant to the attached teaching claim, not merely be an adjacent heading/lead-in/transition; an admission whose excerpt does not ground that teaching is not supported by quote truth alone. Keep the verifier's S432 disagreement in the lesson as the motivating record. Do **not** edit the round-61 S432 Gate line, mark its source row rejected, or rewrite prior QUALITY criteria; use a separately appended correction/qualification only if the lane's normal lesson process records the new source quote. Preserve the old row as the historical admitted record and make the new criterion prospective/superseding guidance.

## Confidence and limits

High confidence on the gap: inspected the existing quote-truth and locator rules plus the cited non-author verdict. This is a scoped corpus reading, not an LSP semantic trace (the task concerns documents, not exported code contracts). No files outside this assigned report were written; no scoring/counter action was taken.