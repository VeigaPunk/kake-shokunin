# Review244 — WCAG 2.4.4 Link Purpose (In Context)

**Verdict: Disagree.** The card is source-grounded overall, but its publisher check adds a markup-only restriction that excludes programmatically available non-markup context. One other exception phrase is stricter than the criterion if read literally.

## Findings

### Medium — `publisherCheck` excludes valid non-markup programmatic context

Exact card substring: **“Treat context as acceptable only if it is exposed in the markup, not merely placed visually nearby.”**

The criterion’s `#dfn-programmatically-determined-link-context` definition is about information determinable from relationships with a link, combined with link text, and presented in different modalities. Its linked `#dfn-programmatically-determinable` definition explicitly gives both markup and non-markup routes: Example 2 permits technology-specific data structures in a non-markup language exposed to assistive technology through a supported accessibility API (saved source lines 3505–3516). The definition’s note also says screen readers can provide context from punctuation in the current sentence (lines 3527–3534). Thus, requiring markup alone could make a reviewer reject context that is programmatically exposed through the specified non-markup route.

**Minimal correction:** “Accept context only when it is programmatically determinable and available through a supported user-agent/assistive-technology modality (including markup or an accessibility API); visual proximity alone is insufficient.”

### Low — `publisherCheck` makes the ambiguity exception sound universal

Exact card substring: **“Record a link under the exception only when its purpose would be ambiguous to every user, including users who can see the surrounding page, and write down why.”**

The criterion body at `#link-purpose-in-context` says “ambiguous to users in general.” The linked `#dfn-ambiguous-to-users-in-general` definition (saved source lines 2515–2518) tests whether the purpose can be determined from the link and all information on the webpage presented to the user simultaneously with it; it explains that readers without disabilities would not know what the link would do until activation. Read literally, “every user” imposes a more absolute threshold than “users in general,” while “surrounding page” is less precise than all simultaneously presented information.

**Minimal correction:** “Record a link under the exception only when its purpose cannot be determined from the link and all information presented simultaneously with it (that is, it is ambiguous to users in general), and write down why.”

## Confirmed accurate portions

- `id` **2.4.4**, title **Link Purpose (In Context)**, level **A**, and source URL match the saved criterion at `#link-purpose-in-context` (lines 1469–1476). `sourceQuote` is a 25-word substring of the criterion body in `normativeText`; it does not turn an informative source into a requirement.
- The `#dfn-purpose-of-each-link` definition is the nature of the result obtained by activating a hyperlink (line 3283), matching the check to determine where the link goes or what it does. Listing image, icon-only, and repeated-component links is review-plan scope, not a claim that WCAG imposes a particular inventory method.
- The check includes the same sentence as potential context, consistent with the note at `#dfn-programmatically-determined-link-context` that screen readers can provide context from punctuation in the current sentence. It also asks for programmatic associations rather than visual proximity alone.
- The failure example is consistent with the criterion as described: repeated “Read more” links have different destinations, and the product name is expressly not in a shared or programmatically associated context. The limitation accurately says source/automation cannot judge context or the exception, and that meeting this criterion alone establishes neither 2.4.9 nor overall conformance. `status` is **not-assessed**.

## Residual risk

This is a review of the card against the retained WCAG source, not an assessment of any website. The exception wording could have been intended colloquially; using the source’s “users in general” formulation removes that ambiguity.

## Verification gaps

No LSP device/server is mounted in this session (`xd://lsp` returned “No such tool” and listed the available devices). Therefore LSP status, references, definition, and diagnostics were unavailable; text search was used only to locate source excerpts, not as semantic proof. No website testing or build/test commands were run, and no tools were installed.