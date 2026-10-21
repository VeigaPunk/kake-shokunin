# Criterion 1.3.5 — Disagree

## Finding (low): the check requires markup for every implementation

- **Card field:** `publisherCheck`
- **Exact substring:** “confirm in the rendered markup that its purpose is exposed programmatically through a mechanism the implementing technology supports”
- **Why:** SC 1.3.5’s two conditions are that the input purpose is in the listed taxonomy and that the technology supports identifying the expected meaning ([`#identify-input-purpose`](../source-wcag22.html#identify-input-purpose), source lines 723–728). Its linked definition of “programmatically determined” explicitly includes non-markup technology-specific data structures exposed to assistive technology ([`#dfn-programmatically-determinable`](../source-wcag22.html#dfn-programmatically-determinable), lines 3501–3515). The linked input-purpose section likewise says other technologies may have equivalent concepts and only concepts mapped to the listed meanings are required; it says to mark up controls “where applicable” ([`#input-purposes`](../source-wcag22.html#input-purposes), lines 4098–4102). Requiring rendered *markup* without qualification can falsely reject a supported non-markup implementation that exposes the mapped purpose through its technology-specific data structure/accessibility interface. The card’s `evidenceNeeded` already accommodates “other programmatic exposure,” so the check should use the same scope.
- **Minimal correction:** replace “in the rendered markup” with “in the rendered content’s technology-specific representation (for example, HTML markup or a non-markup data structure exposed to supported assistive technology).” Keep the requirement that the implementation technology supports identifying the expected meaning.

## Otherwise correct

The card has the exact id `1.3.5`, title `Identify Input Purpose`, level `AA`, and pinned source URL. Its quote is an exact 15-word substring of the normative criterion and within the 6–25-word packet rule. Its review scope correctly limits applicability to user-related purposes in the WCAG list and supported technologies; the HTML `autocomplete` example and the no/incorrect-token failure example are criterion-specific and accurate. The limitation does not claim that source evidence alone establishes conformance, and status is `not-assessed`.

## Residual risk and verification gaps

This is a static review against the retained WCAG source, not an assessment of any website. No LSP device was available (`xd://lsp` returned “No such tool”); therefore no LSP references, definition, or diagnostics checks were possible. No tools were installed or updated.