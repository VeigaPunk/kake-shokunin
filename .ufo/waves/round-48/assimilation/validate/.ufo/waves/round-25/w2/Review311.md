# Review311 — criterion card 3.1.1 Language of Page (A)

Reviewer: KakeR25.Review311 (author-side falsify wave, r25 C1). Scope: card `3.1.1`
in `corpus/knowledge/accessibility-review-cards.json` against the pinned REC
`.ufo/waves/round-25/source-wcag22.html` and `.ufo/waves/round-25/population.json`.
Read-only semantic review; no code, website, browser, network, or r24 work.

Axes: (1) identity binding (id/title/level/source/population uniqueness),
(2) quote grounding (6–25-word word-boundary substring of normativeText),
(3) normative fidelity (added requirements, omitted exceptions, informative→MUST,
misstated failure example, source-only-as-conformance), (4) operability
(a publisher reviewer could actually execute the check and evidence asks).

## Verdict: AGREE — no defect found in card 3.1.1

Every check below is grounded in the saved source; none is a generic restatement.

1. **Identity binding exact.** Card `id` `3.1.1`, `title` `Language of Page`,
   `level` `A`, `source`
   `https://www.w3.org/TR/2024/REC-WCAG22-20241212/#language-of-page` match the
   population entry (`population.json:367-373`, `anchor: "language-of-page"`)
   and the saved source section `id="language-of-page"` with heading
   `Success Criterion 3.1.1 Language of Page` and `(Level A)` label
   (`source-wcag22.html:1777,1781`). Exactly one card carries `"id": "3.1.1"`
   (cards.json:483) — no duplicate or missing-ID population drift.

2. **Quote is a true normative-body substring.** `sourceQuote` =
   `The default human language of each web page can be programmatically determined`
   — 12 words (6–25 rule), case-sensitive, starts/ends at word boundaries, and is
   a substring of `normativeText` `"The default human language of each web page
   can be programmatically determined ."` (`population.json:373`). The trailing
   ` .` is the documented extractor spacing artifact (packet: normalization
   "removes extractor-added whitespace before punctuation"), not a word change.
   The criterion body is a single sentence (`source-wcag22.html:1783`); there are
   no notes, exceptions, or "except" clauses in the normative text, so nothing
   normative could be omitted.

3. **No added requirement / no informative→MUST conversion.** The card's
   satisfying mechanism is hedged — `publisherCheck`: "(for HTML, typically a
   valid lang value on the html element)" — so the card never turns a sufficient
   technique into a MUST; the normative test it operationalizes stays
   `programmatically determined` as defined at `source-wcag22.html:3501-3505`
   ("extract and present this information to users in different modalities"),
   which the card's "exposed in a form user agents and assistive technologies
   can read" mirrors without strengthening. "Document metadata" in
   `evidenceNeeded` is correctly retained generality for non-HTML documents, not
   an opening for HTTP-header-only declarations, because the HTML path is
   separately stated and the check tests the *declared value against the
   identified language*.

4. **"Predominant language" is operationalization, not new scope.** `default
   human language` is not a separately defined glossary entry in the pinned
   source (grep over `source-wcag22.html`: zero matches for the compound term;
   only `human language` is defined, `source-wcag22.html:3081-3085`, including
   signed languages). The card's "language that predominates in its
   human-readable content" is the standard review operationalization, flagged as
   a reviewer step rather than a standard requirement, and the `limitation`
   keeps the card a work aid "never a replacement for the standard".

5. **Per-page scope carried correctly.** `publisherCheck`: "Repeat for every
   page template, locale variant, and dynamically or separately served page,
   since the criterion applies to each web page" honors the normative "each web
   page" (web page defined at `#dfn-web-page-s`, `source-wcag22.html:1783` link
   title: single URI plus resources rendered together). It makes no process- or
   site-level conformance claim, so §5.2 conformance boundaries are not misused.

6. **Failure example is criterion-specific and canonical.** `failureExample`
   describes a shared template hard-coding `lang="en"` on German product pages so
   screen readers apply English pronunciation — the classic wrong-default-
   declaration failure for 3.1.1 (page-level wrong declaration), correctly not a
   passage-level example that would belong to 3.1.2, and not a generic
   restatement of the criterion.

7. **Boundary to 3.1.2 drawn in the right field.** `limitation`: "Language
   changes of individual passages are 3.1.2, not this criterion" prevents the
   most likely scope bleed for this criterion pair.

8. **No source-only evidence as conformance.** `limitation` explicitly blocks
   the shortcut: "Finding a lang attribute in source or via an automated checker
   does not show the declared value matches the page's actual default language,
   nor cover every page and locale variant", and `evidenceNeeded` demands
   capture "from the rendered page, not only from source templates". Status is
   `not-assessed` and the limitation keeps it there.

## Residual risk / verification gaps

- Card-vs-Understanding: the pinned source is the TR normative text only;
  Understanding/technique content was not in scope of this review, and the card
  makes no technique-level MUSTs, so no gap bites.
- "Valid lang value" inherits whatever validity policy the packet's reviewer
  applies (e.g., BCP 47 well-formedness); the hedge "typically" keeps this
  advisory, but a stricter reviewer could over-apply it — acceptable as written.
- This is author-side review, not independent closure; the packet's status
  remains `not-assessed` and no website conformance is implied.

No tool installs or updates were needed for this review (no channel/version
entries to record).
