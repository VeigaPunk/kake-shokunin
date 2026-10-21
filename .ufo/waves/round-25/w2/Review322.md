# Review 322 — 3.2.2 On Input

**Verdict: Disagree — revise the card before treating it as packet-ready.** The criterion identity and the core exception are represented correctly, but the quote exceeds the packet's limit and two instructions can lead reviewers to count events that are not necessarily a change of context or a change of setting.

## Findings

### Medium — `sourceQuote` exceeds the 25-word limit

- **Field / exact value:** `sourceQuote`: `Changing the setting of any user interface component does not automatically cause a change of context unless the user has been advised of the behavior before using the component`
- **Evidence:** This is an exact quotation from the normative body at `source-wcag22.html#on-input` (criterion paragraph, source line 1877), and the same wording is in the population's `normativeText` (`population.json`, lines 394–400). It is 29 whitespace-delimited words, exceeding the packet's documented 6–25-word quote rule and the requested maximum.
- **Minimal correction:** Shorten it to the exact 16-word prefix `Changing the setting of any user interface component does not automatically cause a change of context`.

### Medium — `publisherCheck` over-includes possible context changes

- **Field / exact substring:** `publisherCheck`: `new page or window, viewport or focus moved, content changing the meaning of the page, form submitted`
- **Evidence:** The criterion at `source-wcag22.html#on-input` applies to a *change of context*. The linked definition at `source-wcag22.html#dfn-change-of-context` (lines 2719–2747) defines that as a **major** change that can disorient users unaware of it; viewport and focus are categories, not an assertion that every movement qualifies. The definition's example names *moving focus to a different component* and *significantly* rearranging content. A form submission by itself is not listed as a change of context; it may qualify when it causes a defined context change, such as navigation. As written, the checklist can treat any viewport/focus movement or submission as a context change and produce false failures. The linked definition's note (lines 2740–2743) also cautions that content changes do not always change context; the card's limitation correctly recognizes that point.
- **Minimal correction:** Ask reviewers to decide whether the effect is a major change capable of disorienting an unaware user; retain only examples qualified accordingly (e.g. a new page/window, a significant viewport/focus change, or content changing page meaning). Count a form submission only when its result is a change of context.

### Low — `failureExample` does not establish a setting change

- **Field / exact substring:** `failureExample`: `as soon as a new option is highlighted with the arrow keys`
- **Evidence:** The normative trigger at `source-wcag22.html#on-input` is **changing the setting** of the component. “Highlighted” can describe focus or a preview without establishing that the select list's setting has changed. The example therefore does not unambiguously establish the criterion's triggering condition, even though arrowing can change a particular control's selected value.
- **Minimal correction:** Say the user selects/commits a new option as the control's setting and the page navigates immediately, with no prior advice.

## Checks that agree

- `id` `3.2.2`, title `On Input`, level `A`, and source URL `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#on-input` match the pinned source and population.
- The quote is otherwise from the normative criterion body; the exception for advice **before using the component** is retained in the publisher check and evidence request.
- The user-interface-component definition is linked from the criterion; its notes say components are user-perceived controls, may be implemented by one programmatic element, and include form elements, links, and script-generated components (`#dfn-user-interface-components`, lines 3980–3991). No card instruction conflicts with those notes.
- The card's limitation explicitly says no website was evaluated and makes no pass, fail, inapplicability, or conformance claim; it does not present source-only evidence as conformance. `status` is `not-assessed`.

## Residual risk and verification gaps

This is a source-grounded review of the card only; no website or runtime behavior was evaluated. The pinned criterion has no note in its section; the linked definition notes were reviewed. No builds, tests, or packet checks were run.
