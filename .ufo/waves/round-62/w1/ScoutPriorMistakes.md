# ScoutPriorMistakes — round 62

## Finding: `source/lead-in-misquote` (S432)

**Observed.** Round-61's own lesson records the Gate quote as “Web developers and conformance checkers must use the following” (9 units), tagged §3.6 (`corpus/lessons/round-61.md:43`). The non-author spot-check reopened WHATWG Fetch §3.6 and disagreed: it is a generic lead-in, not substantive evidence for the row's response-header expectation (`corpus/lessons/round-61-verifier-spotcheck.md:30-36`). The verifier explicitly says the quote fails to ground the teaching, while the S432 row remains admitted; routed defect asks for a substantive excerpt and append-only correction/new row plus a grounded criterion (`round-61-verifier-spotcheck.md:41-46`).

The retained source provides a direct replacement in the same section: “response header can be used to require checking of a response’s Content-Type header against the destination of a request” (`.ufo/waves/round-61/sources/S432.html:6151-6154`, source section heading at 6149). This makes the header's function and relation to Content-Type/request destination explicit. It is substantively relevant to the existing S432 scope, unlike the generic lead-in. Preserve the existing S432 row as instructed; correction should be append-only, retaining the historical quote and adding a dated correction/replacement quote rather than rejecting the row.

**Inference / proposed classification.** Classify as `source/lead-in-misquote`: a source span may be authentic and correctly located yet still fail to evidence the registry/knowledge row's stated teaching because it is only a generic transition. This is distinct from a fabricated quote or an incorrect section locator: the dispute is evidentiary relevance. Confidence high: the report's explicit disagreement and the adjacent direct source language establish the contrast.

## Testable QUALITY criterion proposal

A source quote used to support a row's teaching **MUST itself state the subject-matter proposition the row teaches; generic lead-ins, headings, or transition text do not qualify even when verbatim, page-unique, and correctly located.** When a non-author spot-check finds an admitted quote fails this bar, preserve the original record and append a dated correction with a substantive located replacement; do not silently relabel/reject the row.

Grounding: `corpus/lessons/round-61-verifier-spotcheck.md:33,36,41-46` (specific S432 failure, quality/discernment harm, routed fix), and retained authoritative body `.ufo/waves/round-61/sources/S432.html:6151-6154` (the replacement's claim-bearing text). This adds semantic relevance to existing mechanical quote checks; it does not claim those checks are defective.

**Falsifier / acceptance test:** against the retained S432 body, adjudicate the round-61 Gate span and proposed replacement by asking whether the quoted span itself names the relevant response-header behavior. The old “Web developers and conformance checkers must use the following” must fail as a generic lead-in; the §3.6 response-header/Content-Type/destination span must pass. The lesson/entry must retain the old quote as history and visibly append the correction. A generic phrase that happens to satisfy length, uniqueness, and section-location checks must still fail this criterion.

## Boundaries and unresolved

This is advice only. No lane files, frozen claim, counter, criterion, or score were changed or evaluated. The source body lines and lesson/verifier evidence were read directly; no semantic LSP server was available/queried, and no exported code contract is implicated.