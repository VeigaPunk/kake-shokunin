# ReviewerQualityCriterion — round 62

## Findings

No actionable defect in the proposed criterion’s scope or evidence grounding, provided it stays narrowly about whether a quoted excerpt substantively supports its attached teaching claim. There is no equivalent existing criterion: `corpus/QUALITY.md:375–388` (“A Gate quote is found in retained source text”) tests exact quote truth and receipt digest, not relevance/support; `corpus/QUALITY.md:1116` (locator rule, as identified by `w1/ScoutQUALITY.md:5`) tests location, not semantic support. Do not duplicate or weaken either.

The need and rejection case are directly grounded in `corpus/lessons/round-61-verifier-spotcheck.md:33–36`: non-author spot-check admitted S432 but disagreed because its quoted generic lead-in was not substantive evidence for the response-header expectation; discernment was explicitly marked harmed and the criterion gap noted. Domain scope should remain web-publishing evidence: an excerpt must express a proposition relevant to the specific publishing/header expectation it accompanies, not merely be an adjacent heading, generic lead-in, or transition. Do not turn this into a general research-method/quote-location criterion (the corpus identifies research method as chousa-owned in `corpus/SOURCES.md:3`).

## Proposed testable wording

**Substantive quote support (round 62).** Admit a web-publishing claim only when its retained, source-true quoted excerpt states evidence that substantively supports the specific teaching attached to it; an accurate but generic heading, lead-in, or transition does not suffice. Reject when the excerpt is merely introductory/adjacent or otherwise fails to support that teaching. Grounding: `corpus/lessons/round-61-verifier-spotcheck.md:33–36`; resolve by checking the named claim and quote against its retained cited source section, recording the support rationale. This criterion supplements, and does not replace, the quote-truth/digest check at `corpus/QUALITY.md:375–388`.

Testability is reviewer-judgment rather than mechanically decidable, but has concrete admit/reject conditions, a named comparison (excerpt ↔ attached claim ↔ retained cited source section), and an independently resolvable motivating record. Avoid presenting mere substring/section membership as proof of semantic support. The cited substantive §3.6 text in retained `.ufo/waves/round-61/sources/S432.html:6151–6154` says the header can require checking Content-Type against request destination; it is materially relevant to the header's function, but should not automatically be claimed to support a more specific nosniff-value rule without reading the claim and relevant normative algorithm/ABNF in context.

## Scope and evidence limits

The source row is not to be rejected or rewritten, and the historical round-61 Gate/disagreement should remain intact; the new criterion is prospective and corrective, not a retroactive change to that decision. This report reviews the criterion only; no independent post-change review or after-state is asserted. Commands: none (read-only inspection via repository file reader); no score/counter executed and no lane files other than this assigned report written.
