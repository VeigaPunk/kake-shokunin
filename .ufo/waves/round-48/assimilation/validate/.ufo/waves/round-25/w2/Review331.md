# Review 3.3.1 — Error Identification

**Recommendation: Disagree (one semantic overconstraint).** This is an author-side review, not an independent closure or a website conformance judgment.

## Finding — requires textual identification of the item

- **Card field / exact substring:** `publisherCheck`: “in text, both which item is in error and a description of the error”; the same added condition recurs in `limitation`: “identified and described in text”.
- **Source:** `.ufo/waves/round-25/source-wcag22.html#error-identification` (criterion paragraph; extracted `population.json` `normativeText`). It says: “the item that is in error is identified and the error is described to the user in text.” The explicit text modifier is on the error description; the criterion does not say that item identification itself must be textual. The source’s `#dfn-text` definition also describes text as programmatically determinable, with `#dfn-programmatically-determinable` explaining presentation in different modalities. A reviewer could therefore wrongly reject a case where the item is identified to the user by another means (for example, an accessible association) while a text description of the error is provided.
- **Minimal correction:** Say “confirm the item in error is identified to the user and that the error is described in text”; ask the reviewer to record how the item is identified without requiring that identification itself be textual. Make the matching change in `limitation`.

## Remaining checks

- `id` `3.3.1`, title `Error Identification`, level `A`, and the pinned source URL match the source.
- `sourceQuote` is the complete criterion body, exactly present in extracted `normativeText`, and is 25 whitespace-delimited words (within the packet’s 6–25-word rule).
- The input-error definition note at `#dfn-input-error` expressly includes required information omitted by the user and information outside required formats/values, so the check’s omitted-required-fields example is in scope. The malformed-email example describes an automatically detected error with no textual description, a valid failure example. The limitation correctly excludes a duty to detect errors or suggest corrections/prevent them; no exception in 3.3.1 is omitted.
- Evidence requests human-observed triggered error states rather than treating source-only evidence as conformance. `status` is `not-assessed`; the card does not claim a website result.
