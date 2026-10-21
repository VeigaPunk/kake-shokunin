# Review 1.3.1 — Disagree

## Finding: publisher check narrows the criterion to visual presentation

- **Card field / exact substring:** `corpus/knowledge/accessibility-review-cards.json` — `publisherCheck`: “every piece of information, structure, and relationship that the visual presentation conveys”.
- **Source:** The pinned normative criterion at `source-wcag22.html#info-and-relationships` (line 670) says: “Information, structure, and relationships conveyed through presentation can be programmatically determined or are available in text.” Its linked `presentation` definition at `source-wcag22.html#dfn-presentation` (line 3464) is “rendering of the content in a form to be perceived by users”; it is not limited to visual rendering. **[INFERENCE]** The card’s operative check could omit relationships conveyed through auditory presentation. The criterion section contains no additional note (it closes at line 673). The `programmatically determined` definition (lines 3505–3515) also gives both markup and non-markup/API examples; these do not establish a visual-only scope.
- **Minimal correction:** Replace “that the visual presentation conveys” with “conveyed through presentation (including visual or auditory formatting where used)”. The existing visual examples may remain examples, not the limit of the review.

## Other requested checks

- `id`, `title`, `level`, and `source` match the extracted population record (population lines 61–67): `1.3.1`, `Info and Relationships`, `A`, and the pinned `#info-and-relationships` URL.
- `sourceQuote` is a 16-word quote from `normativeText`; it is within the 6–25-word packet rule. Its extraction whitespace before the comma is the documented normalization, not a wording change.
- `status` is `not-assessed`. The failure example describes a plausible missing programmatic label/required-state relationship; it does not itself claim that the example or a page was evaluated. The evidence requirement is not presented as conformance evidence, and `limitation` explicitly says source inspection or automated checks do not demonstrate the criterion is met. No defect found in these fields.

## Residual risk and verification gaps

This is a bounded semantic review of the card against the saved source and population only; no website was tested. The `lsp` device is unavailable (`read xd://lsp` returned “No such tool”), so LSP status, references, definition, and diagnostics were unavailable; literal searches were used only to locate source anchors, not as semantic proof. No tests, builds, or installs were run.