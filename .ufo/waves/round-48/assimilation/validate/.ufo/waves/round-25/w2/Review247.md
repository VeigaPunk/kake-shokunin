# Review247 — 2.4.7 Focus Visible

**Verdict: Disagree (two focused wording corrections in `limitation`; otherwise agree).**

**Axes:** operability, freshness. Reviewed only the assigned 2.4.7 card against the pinned WCAG 2.2 source.

## Findings

1. **`limitation` — “This criterion only requires that some mode with a visible focus indicator exists.”** This drops the criterion's universal subject: “Any keyboard operable user interface has a mode of operation” (`source-wcag22.html#focus-visible`, §2.4.7, lines 1510–1515). The linked definition says a focus indicator is the pixels changed to signal that a user interface component is in a focused state (`#dfn-focus-indicator`, lines 3005–3013); the linked `user interface component` definition and notes clarify that components are perceived controls, not merely programmatic elements (`#dfn-user-interface-components`, lines 3977–3991). As written, the limitation can be read as requiring only one mode/indicator somewhere, rather than a qualifying mode for every keyboard-operable interface. **Minimal correction:** “Every keyboard-operable user interface must have at least one mode of operation in which its keyboard focus indicator is visible.”

2. **`limitation` — “It does not set minimum size, contrast, or freedom from being hidden behind other content; those belong to other criteria (2.4.11 Focus Not Obscured (Minimum), 2.4.13 Focus Appearance) and are not evaluated here.”** The blanket wording can wrongly suggest that an indicator obscured by other content is outside 2.4.7. The criterion itself requires the focus indicator to be visible (§2.4.7, lines 1512–1515). The related criteria address distinct matters: 2.4.11 says the *focused component* is not entirely hidden due to author-created content (lines 1569–1573), while 2.4.13 sets focus-indicator area and contrast requirements (lines 1591–1606). **Minimal correction:** distinguish the focused component from its indicator: “This criterion does not set minimum indicator size or contrast (2.4.13); 2.4.11 separately addresses whether the focused component is entirely hidden by author-created content. The focus indicator itself must still be visible under 2.4.7.”

## Agreement / source checks

- `id` `2.4.7`, `title` `Focus Visible`, `level` `AA`, and the pinned `source` URL are correct. `sourceQuote` exactly matches the complete normative criterion in `population.json` `normativeText` and the saved source section.
- `publisherCheck` correctly tests a mode in which keyboard focus remains indicated across keyboard-operable components; the named keyboard navigation, widgets, and reachable author setting are reasonable review steps, not asserted extra WCAG tests. `evidenceNeeded` is appropriately evidentiary, and the stylesheet-removes-outline example is a valid failure when nothing replaces the indicator.
- `status` is correctly `not-assessed`; the source/automation limitation and no-conformance-claim boundary are appropriate. The §2.4.7 source section has no exception or note to omit. Its linked focus-indicator definition is present; linked component-definition notes explain perceived controls and script-generated components.

## Verification limits

The `lsp` device is unavailable (`read xd://lsp` returned “No such tool”), so no LSP status, references, definition, or diagnostics were available. This is a prose/JSON card review; literal searches were used only to locate source anchors, not as semantic proof. No website, browser, or runtime was tested.