# Review 2.4.3 — Focus Order (A)

**Verdict: Agree; no criterion-specific defect found.** This is a source review of the assigned card only; it is not a review of any website or a conformance result.

## Source check

The saved Recommendation's `#focus-order` section (source-wcag22.html, lines 1456–1464) identifies Success Criterion 2.4.3 as Level A and gives the condition that a web page can be navigated sequentially and the navigation sequences affect meaning or operation, followed by the requirement that focus order preserve meaning and operability. The section has no additional criterion note or exception. The population entry for 2.4.3 (`population.json`, lines 258–265) retains the same normative text.

The linked `#dfn-navigated-sequentially` definition (lines 3378–3384) is advancing focus from element to next using a keyboard interface; linked `#dfn-keyboard-interface` (lines 3177–3190) defines the interface as obtaining keystroke input and notes that a physical keyboard is not required. `#dfn-web-page-s` (lines 4056–4077) defines the non-embedded resource and notes that its resources need not all render simultaneously, and that non-embedded status is within the conformance scope. The related `#dfn-user-interface-components` definition and notes (lines 3977–4000) define components by perceived controls, not implementation elements, and include form elements, links, and scripted components. None adds an exception or contradicts the card's stated applicability check or examples of dynamic page states.

## Card fields

- **Identity:** `id` `2.4.3`, `title` `Focus Order`, `level` `A`, and `source` URL all match the saved source's criterion, title, level, and anchor.
- **Quote:** `sourceQuote` — “focusable components receive focus in an order that preserves meaning and operability” — is an exact 12-word substring of the normative criterion and is within the 6–25 word packet rule. The card's check retains the applicability conditions omitted from this partial quote.
- **Publisher check:** It explicitly checks both conditions before proceeding. Its forward/backward sequential-navigation and in-scope-state instructions are review steps, not claims that WCAG requires one particular sequence or that an unrelated focus stop automatically fails. Requiring a judgment about preserved meaning and operability matches the criterion.
- **Evidence and failure example:** The written sequence and reasoned human judgment are appropriate evidence for a publisher review. The checkout example states a particular impact—interruption of a task whose fields must be completed together—rather than asserting that every noncontiguous form field or footer stop is automatically a failure.
- **Limitation and status:** The limitation correctly says source inspection, `tabindex`, and automated checks alone do not establish that order preserves meaning and operability, and disclaims pass/fail/conformance. `status` is `not-assessed`.

No correction is required. The card keeps the criterion's conditional scope, does not invent an exception or turn advice into a WCAG MUST, and does not present source-only evidence as conformance.