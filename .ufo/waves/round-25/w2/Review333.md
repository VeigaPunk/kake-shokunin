# Review333 — Card 3.3.3 Error Suggestion (AA), author-side falsify review

Scope: card `3.3.3` in `corpus/knowledge/accessibility-review-cards.json` (lines 591–608) against the pinned source `S035` (.ufo/waves/round-25/source-wcag22.html, section `#error-suggestion`, lines 1973–1984) and extracted `.ufo/waves/round-25/population.json` entry (lines 448–455). Read-only review; no website, browser, or network target; card status stays `not-assessed`. No tools installed for this review (none needed).

## Grounding verification (what the card gets right)

- **Identity exact.** Card `id` "3.3.3", `title` "Error Suggestion", `level` "AA", `source` "https://www.w3.org/TR/2024/REC-WCAG22-20241212/#error-suggestion" match population.json (id/title/level/anchor/source) and the saved source heading `<bdi class="secno">Success Criterion 3.3.3 </bdi>Error Suggestion` with `<p class="conformance-level">(Level AA)</p>` (source line 1973, 1977). No duplicate or missing ID.
- **Quote is legitimate.** `sourceQuote` "If an input error is automatically detected and suggestions for correction are known, then the suggestions are provided to the user" — 21 whitespace-delimited words (within 6–25), case-sensitive, starts/ends at word boundaries, and is an exact substring of population `normativeText`, taken from the criterion body paragraph (source lines 1979–1981), not a heading, doclink, or conformance label. It truncates before "unless it would jeopardize…" but that is the documented short-quote rule, and the exception is carried in the card's `publisherCheck` and `limitation`, so no exception is lost to the reader.
- **Omission/format errors grounded.** `publisherCheck`'s "including omitted required fields and values outside an accepted format or range" is grounded in the linked definition `#dfn-input-error` (source lines 3145–3161): "information provided by the user that is not accepted", Note list items 1 (required information omitted by the user) and 2 (falls outside the required data format or values). Not an added requirement.
- **Failure example is criterion-accurate.** `failureExample` (delivery date "31/12/2026" rejected with only "Invalid date", expected format known to the validator) instantiates exactly the violated normative conditional: auto-detected input error + known suggestion + not provided. No misstatement.
- **No conformance leakage.** `evidenceNeeded` requires rendered-interface capture and human-reviewed rationales; `limitation` states "this card records review readiness only and makes no conformance claim for any website"; `status` is `not-assessed`. No source-only evidence is offered as a WCAG result, and no informative advice is escalated into a MUST about websites.

## Findings

### F1 — Medium: unconditional exception rationale required even when no correction is known

- **Field/substring:** `publisherCheck`, "Where no suggestion is shown, record the publisher's stated reason and check it is that a suggestion would jeopardize the security or purpose of the content".
- **Reason:** The normative criterion is doubly conditional — source lines 1979–1981: "If an input error is automatically detected **and suggestions for correction are known**, then the suggestions are provided to the user, unless…". When the system does not know a correction, the criterion is silent: no suggestion is owed and no exception rationale is owed. The same `publisherCheck` paragraph explicitly walks rules where the system does not know a correction ("record whether the system knows a correction"), and the subsequent "Where no suggestion is shown…" sentence, read over the whole walkthrough, demands a security-or-purpose justification for those too. That converts the criterion's applicability gate into an extra documentation obligation — an added requirement not in the standard. The card's own `evidenceNeeded` scopes it correctly ("for each rule where a known correction is withheld"), so this is a wording defect in `publisherCheck`, not intent.
- **Source anchor:** `source-wcag22.html` `#error-suggestion` (line 1979) — "suggestions for correction are known"; exception clause line 1980 "unless it would jeopardize the security or purpose of the content".
- **Minimal correction:** `publisherCheck`: replace "Where no suggestion is shown, record the publisher's stated reason and check it is that a suggestion would jeopardize the security or purpose of the content" with "Where a correction is known but is not provided to the user, record the publisher's stated reason and check it is that providing the suggestion would jeopardize the security or purpose of the content; where no correction is known, record that the criterion is not triggered."

### F2 — Low: suggestion required "in text" though the criterion does not fix the medium

- **Field/substring:** `publisherCheck`, "confirm the message presented to the user states that correction in text, not only that the input is wrong".
- **Reason:** Normative text (source line 1980) says "the suggestions are provided to the user" with no medium requirement; the saved criterion contains no "in text" wording. Text is the normal means on the web, and the error itself must be identified in text by 3.3.1 (Level A, part of any AA claim), but making a textual statement of the correction a hard check item is stricter than this criterion's own words. Flagged as a minor over-requirement so the card does not present a convention as the criterion's requirement; practical impact small.
- **Source anchor:** `source-wcag22.html` `#error-suggestion` (lines 1979–1981) — "then the suggestions are provided to the user".
- **Minimal correction:** `publisherCheck`: replace "states that correction in text, not only that the input is wrong" with "provides that correction to the user (normally as text alongside the identified error, which 3.3.1 requires in text)".

### F3 — Low: check scope keyed to publisher-authored validation may miss automatically detected errors from platform defaults

- **Field/substring:** `publisherCheck`, "List every input the publisher validates automatically (client or server)".
- **Reason:** "Automatically detected" (source line 1979) is a property of the content's behavior, not of deliberate author-written validation. Input errors are also automatically detected through markup-enabled native constraint validation (e.g., `type="email"`, `required` browser messages) or framework rejections the publisher did not hand-write; keying the inventory to what "the publisher validates" can silently exclude exactly those errors from the walkthrough, under-scoping the review relative to the criterion.
- **Source anchor:** `source-wcag22.html` `#error-suggestion` (line 1979) — "If an input error is automatically detected"; definition `#dfn-input-error` (lines 3145–3161).
- **Minimal correction:** `publisherCheck`: replace "List every input the publisher validates automatically (client or server)" with "List every input whose value the content automatically rejects as not accepted, including native constraint validation and framework defaults, whether client or server".

## Verdict

Disagree (fixable, none fatal): the card is source-faithful in identity, quote, exception handling, and non-conformance framing, but F1 adds an exception-rationale obligation where the criterion does not even apply, and F2/F3 harden a medium and narrow the detection scope beyond/short of the normative wording. Apply the three minimal corrections; card remains `status: not-assessed` and no website conformance is implied by this review.

Residual risk / verification gaps: the Understanding/How-to-Meet documents are not in the pinned source, so F2 was judged on the REC text alone; a reviewer could legitimately keep "in text" as packet-internal advice if labeled as such rather than as the criterion's requirement. No build, selftest, or measurement commands were run per lane bounds.
