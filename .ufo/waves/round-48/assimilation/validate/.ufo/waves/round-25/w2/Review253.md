# Review 2.5.3 — Label in Name (A)

**Verdict: Disagree with the card as written on two narrowly scoped wording points; its core criterion summary is otherwise sound.** The card remains `not-assessed`; this review is not a website conformance judgment.

Review axes: criterion fidelity, publisher operability, and freshness against the pinned WCAG 2.2 Recommendation source.

## Findings

### Low — Evidence wording is broader than the defined “image of text” category

- **Card field:** `evidenceNeeded`
- **Exact substring:** `including text rendered inside images`
- **Source:** `.ufo/waves/round-25/source-wcag22.html#dfn-images-of-text` (definition at lines 3123–3130). The definition limits an image of text to text rendered in non-text form to achieve a particular visual effect; its note excludes text that is part of a picture containing significant other visual content (example: a person's name on a nametag in a photograph). Criterion `#label-in-name` applies to labels including text or *images of text*, not arbitrary text appearing in pictures.
- **Reason:** The evidence phrase can be read as requiring any text found inside an image to be transcribed as in-scope label text, omitting the definition's explicit boundary. That risks unnecessary over-inclusion for a control labeled by text that is part of a photograph.
- **Minimal correction:** Replace with `including text in images that meet WCAG's definition of images of text` (or add the definition's significant-other-visual-content exclusion).

### Low — Limitation overstates what automated checks can never establish

- **Card field:** `limitation`
- **Exact substring:** `automated tools cannot confirm which text is the visible label`
- **Source:** `.ufo/waves/round-25/source-wcag22.html#label-in-name`, line 1671, requires that for the specified components the name contain “the text that is presented visually.” The linked `#dfn-labels` and `#dfn-name` definitions (lines 3213–3219 and 3367–3374) distinguish the user-presented label from the name software exposes; the criterion does not say that automated comparison is categorically impossible.
- **Reason:** As an absolute statement, this may discourage automated checks that can compare clearly programmatically available visible text with a computed name. Ambiguous or image-based labels may still need human judgment, and an automated scan alone does not establish overall conformance; those narrower limitations do not support “cannot confirm” for every case.
- **Minimal correction:** Say that automated checks may compare straightforward cases, but cannot reliably determine every visible label or establish conformance on their own; retain the requirement for human review of ambiguous cases.

## Verified as accurate

- `id` `2.5.3`, title `Label in Name`, level `A`, and pinned source URL match the saved criterion. `status` is `not-assessed`.
- `sourceQuote` is 22 words and matches the population's `normativeText` (including the documented extraction-whitespace normalization before punctuation).
- `publisherCheck` correctly asks reviewers to compare the visible label text with the programmatically determined name and does not require the text to start the name. Its scope tracks the criterion's text/image-of-text label condition.
- The “Send” / `aria-label="Submit form"` failure example has a name that omits the visible label text. The limitation correctly identifies the note that the label text should start the name as a non-normative best practice; the source note says “A best practice”.
- The card explicitly says no website was evaluated and that no conformance claim follows. Its requested rendered-page evidence is not presented as source-only proof of conformance.

## Residual risk and verification gaps

No website or rendered control was evaluated. Review was limited to the card, packet guidance, extracted population entry, and saved pinned source with its linked definitions and notes. Image-based or otherwise ambiguous labels still require a reviewer to determine what is presented as the component's label; this report makes no claim about any actual page.
