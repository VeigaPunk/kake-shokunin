# Review242 — Criterion card 2.4.2 Page Titled (A)

Reviewer: author-side falsify pass, KakeR25.Review242, 2026-10-21.
Target: `corpus/knowledge/accessibility-review-cards.json` card `"id": "2.4.2"` (lines 327–341).
Source: S035 pinned REC, `.ufo/waves/round-25/source-wcag22.html` section `id="page-titled"` (lines 1444–1453); population entry `.ufo/waves/round-25/population.json` lines 249–257.

## Verdict: AGREE — card is faithful; no defect found

No defect to cite: every checked card field survives a criterion-specific falsification attempt. Details, each tied to the exact evidence examined:

1. **Identity and binding are exact.** `id` `"2.4.2"`, `title` `"Page Titled"`, `level` `"A"`, and `source` `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#page-titled` match the saved source heading "Success Criterion 2.4.2 Page Titled … (Level A)" (`source-wcag22.html:1444,1448`) and the population anchor `page-titled` (`population.json:253`).

2. **Quote is grounded, not a heading.** `sourceQuote` = `"Web pages have titles that describe topic or purpose."` — 8 whitespace-delimited words, byte-identical (case-sensitive, word-bounded) to `normativeText` (`population.json:256`), and verified against the criterion body paragraph at `source-wcag22.html:1450`, not the h4 heading or the `(Level A)` label. Packet doc says the heading is excluded from normativeText; this quote never relies on it.

3. **No requirement added, no exception omitted — because none exist to handle.** The saved criterion is a single sentence with no attached note or exception and only one linked term, `web page` (`#dfn-web-page-s`). The card invents no MUST: `publisherCheck` and `evidenceNeeded` phrase everything as reviewer recording and human judgment ("records the title … then judges whether"), never as a page requirement. `limitation` even pre-empts the two most common over-additions with the criterion-specific statement "The saved normative text requires description of topic or purpose only; this card adds no uniqueness or length requirement" — verified true of the normative text. Falsification attempt: the closest candidate for an added requirement is `publisherCheck`'s "describes the topic or purpose of that particular page's content rather than only the site, a template placeholder, or a file name", which reads as stronger than the bare sentence. It survives: the sentence's "describe topic or purpose" is page-scoped (the linked definition is a single-URI resource), a site-only or placeholder title plainly does not describe a given page's topic or purpose, and the card still routes the decision through a human judgment, so it is interpretation guidance, not a new condition of conformance.

4. **No source-only evidence laundered as conformance.** `limitation` explicitly negates it: "Checking source code or running an automated tool can show that a title exists, but cannot decide whether it describes the page's topic or purpose, so neither establishes conformance", and `status` stays `"not-assessed"`. `evidenceNeeded` requires rendered-page capture plus a named human judgment, date and reviewer, which is evaluation evidence, not a conformance claim.

5. **Failure example is criterion-specific and accurate.** `failureExample` (uniform "Home - Example Recipes" title across a lentil-soup page and a contact form) is a real instance of the criterion's failure mode — a title that does not identify the page's contents — and the stated harm (tab/history switching) matches what the title is for; it is presented as an example, not as a technique or a pass/fail rule, so it cannot mislead as normative text.

## Residual risk / verification gaps

- The linked `web page` definition (`source-wcag22.html:4056–4068`) says a web page is a non-embedded resource obtained through a single URI, together with other resources used or intended to be rendered with it. Its Note 1 says those other resources need not render simultaneously; Note 2 limits a resource to non-embedded within the scope of conformance. The card does not restate these scope rules, but says "web page" and the packet's step 2 instructs reviewers to read the source definitions. Nothing in the card contradicts those notes; this is a scope reliance, not a defect.
- This review compared card text to saved source bytes and population extraction only. No live page, browser, or network target was touched, and `status` remains `not-assessed`; nothing here establishes website conformance in either direction.

No tool installs were needed or performed (tooling directive: zero installs this assignment).
