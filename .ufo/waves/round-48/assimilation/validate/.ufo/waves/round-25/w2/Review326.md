# Review 326 — WCAG 2.2 SC 3.2.6 Consistent Help

**Verdict: Disagree, narrowly.** The card is otherwise source-grounded, but its failure example does not explicitly establish the page-variation condition required by the criterion’s Note 2.

## Finding

**Low — `failureExample` under-specifies the comparison condition.** Exact substring: `at the same viewport width, with no user action causing the change`.

Source: `.ufo/waves/round-25/source-wcag22.html#consistent-help`, Note 2 (line 1937): “This criterion is concerned with relative order across pages displayed in the same page variation” (15 words). The note gives same zoom level and orientation as examples; the normative body at line 1926 separately excepts changes initiated by the user. Equal viewport width alone does not explicitly establish the same page variation, so as written the example could be read as a failure even where pages are being compared across different variations.

**Minimal correction:** say the order difference occurs “in the same page variation (same zoom level, orientation, and relevant breakpoint), with no user-initiated change.” Keep the current page-order contrast.

## Checks that found no other card defect

- `id`, `title`, `level`, and `source` exactly match the extracted population entry for 3.2.6 (`population.json`, lines 421–427) and the saved criterion anchor. `sourceQuote` is the exact criterion-body phrase “they occur in the same order relative to other page content, unless a change is initiated by the user” (19 words), within the packet’s 6–25-word rule and present in `normativeText`.
- The normative condition is conditional: one of the four listed help mechanisms must be repeated on multiple pages within a set of web pages. The card does not turn this into a requirement to provide help mechanisms; its `limitation` expressly preserves that scope.
- `publisherCheck` correctly calls out the four named mechanisms and repeated occurrences, serialized order, same page variation, and the user-initiated-change exception. `evidenceNeeded` asks for an inventory and variation-specific observations rather than claiming a result.
- The criterion’s Note 1 says help may be on-page or via a direct link; the card includes both. Linked definitions at source lines 3318–3324 (`mechanism`), 3736–3740 (`set of web pages`), and 4056–4062 (`web page`) do not reveal a scope contradiction: page sets share a common purpose and author/group/organization; a mechanism is a process or technique; a web page is a non-embedded resource plus resources used with it. The broader mechanism note about platform/user-agent provision does not negate Note 1’s specific delivery forms for help mechanisms.
- `limitation` does not claim source-only or automated evidence proves conformance; it says human judgment is needed for page-set boundaries and identification of help mechanisms. `status` is exactly `not-assessed`; no website result is claimed.

## Residual risk and verification gaps

Page-set boundaries and whether a component is one of the listed help mechanisms remain reviewer judgments, as the card acknowledges. No website was evaluated. No LSP device was available in the mounted tool catalog (`read xd://lsp` returned “No such tool”); no LSP references/definition/diagnostics result is claimed. Search output was used only to locate saved-source anchors; the review is grounded in the exact card, population, criterion, notes, and definitions read from disk. No tests or runtime checks were run.

Report: .ufo/waves/round-25/w2/Review326.md
