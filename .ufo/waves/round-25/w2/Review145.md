# Criterion 1.4.5 — Images of Text

**Verdict: Disagree — two exception definitions need tighter operational wording.**

## Findings (Medium)

1. **Essential exception is underspecified.**
   - **Card field / substring:** `publisherCheck` — “Essential, meaning that particular presentation of text is essential to the information conveyed.” The corresponding `evidenceNeeded` asks only for “a written rationale”.
   - **Source:** [`source-wcag22.html#images-of-text`](../source-wcag22.html) lines 857–862 links “essential” to [`#dfn-essential`](../source-wcag22.html) lines 2967–2972: removal must fundamentally change the information or functionality, **and** that information and functionality cannot be achieved in another conforming way. The card repeats the criterion’s phrase but does not communicate this defined, conjunctive limit or require evidence for both parts; a reviewer could therefore accept an essential-style rationale that does not meet the exception.
   - **Minimal correction:** Define the exception as applying only when removing that presentation would fundamentally change information or functionality **and** neither can be achieved in another conforming way; require the rationale to address both conditions.

2. **Customizable exception makes the defined property set sound illustrative.**
   - **Card field / substring:** `publisherCheck` — “the user can visually customize the image of text to their requirements (for example font, size, color, background)”; `evidenceNeeded` asks for “which visual properties it changes” without requiring all four.
   - **Source:** [`source-wcag22.html#images-of-text`](../source-wcag22.html) lines 848–852 links “visually customized” to [`#dfn-visually-customized`](../source-wcag22.html) lines 4048–4052: “the font, size, color, and background can be set.” The card's “for example” can be read as making this defined set optional, broadening the exception.
   - **Minimal correction:** State that font, size, color, and background can all be set to the user's requirements, and require evidence of the user-facing means for each.

## Criterion-specific checks that agree

- `id`, `title`, `level`, and `source` correctly identify 1.4.5, “Images of Text” (AA), at `#images-of-text`.
- `sourceQuote` is a 21-word substring of the criterion body in `population.json` `normativeText` and matches the saved source at `#images-of-text` lines 843–843.
- The `publisherCheck` exclusion for text that is only part of a picture with significant other visual content matches the `image of text` definition note and its name-tag-in-a-photograph example at `#dfn-images-of-text` (lines 3120–3130); it is not an invented exception. The logotype treatment also matches the criterion note at `#images-of-text` line 868.
- The failure example is consistent with the conditional requirement and does not misstate either exception. The limitation correctly says image/source inspection cannot decide the visual-presentation or exception questions, that text alternatives do not satisfy this criterion, and that no website result is recorded. `status` is `not-assessed`.

## Residual risk and verification gaps

The omissions may lead a reviewer to apply either exception too broadly unless they consult the linked definitions. The pinned source and extracted population were checked; no runtime, website, or conformance evaluation was performed (nor is one claimed).