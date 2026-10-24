# Review1410 — Card 1.4.10 Reflow (AA), r25 w2 author-side falsification

Verdict: **AGREE — no actionable card defect found.** This is a source-grounded review of the publisher aid, not an assessment of any website.

Axes assessed: **operability** (the card gives an implementable human review procedure) and **freshness** (the criterion is bound to the pinned 2024-12-12 WCAG 2.2 REC source).

## Structural grounding

- In `corpus/knowledge/accessibility-review-cards.json`, the card fields are `id: "1.4.10"`, `title: "Reflow"`, `level: "AA"`, and `source: "https://www.w3.org/TR/2024/REC-WCAG22-20241212/#reflow`; these match the saved source heading/section `id="reflow"` and `(Level AA)` (`.ufo/waves/round-25/source-wcag22.html`, lines 1002–1008).
- `sourceQuote`: “Content can be presented without loss of information or functionality, and without requiring scrolling in two dimensions” is a 17-word exact substring of the criterion's `normativeText` in `population.json` for 1.4.10, and is taken from the criterion body (source lines 1008–1013), not an informative note.
- `status` is `not-assessed`. The card's `limitation` explicitly says it does not assess a website and that completing the card does not establish conformance; it does not offer source-only evidence as a pass.

## Criterion-specific prose review

- **Both reflow cases and their thresholds are distinguished correctly.** `publisherCheck` asks for vertically scrolling content at width equivalent to 320 CSS pixels, and content designed to scroll horizontally at height equivalent to 256 CSS pixels. Those are the two separate cases in the normative criterion (source lines 1008–1011). Its 1280px-wide/400% and 1024px-tall/400% examples accurately track informative Note 1 (line 1015), not new thresholds. The linked definitions support this usage: `CSS pixel` is the CSS unit (lines 2925–2933), and `viewport` is the object in which the user agent presents content (lines 4031–4039).
- **The exception is neither omitted nor broadened into a blanket exemption.** The criterion excepts only parts requiring two-dimensional layout for usage or meaning (line 1013). The card asks reviewers to record such parts and their reason, using Note 2's illustrative examples (line 1017); “such as” keeps the list illustrative. Its limitation correctly says an excepted part does not excuse the rest of the page. It does not convert Note 2's examples into exhaustive requirements.
- **“Without scrolling in both directions” is consistent in context with the criterion's two-dimensional-scrolling rule.** The check separately names the width and height cases, and the sourceQuote states the criterion's exact two-dimension limit; the card does not require eliminating the single scrolling direction appropriate to each content type.
- **Evidence and failure example are appropriately criterion-specific.** The evidence requests the tested size/zoom and observations of a second scroll direction or lost/clipped/unreachable content. The fixed 960-CSS-pixel article text column at a 320-CSS-pixel equivalent viewport is a concrete non-exempt vertical-reading example that forces horizontal scrolling; it illustrates the width case without claiming a real site failed.
- **No advice is misrepresented as a universal WCAG MUST.** The viewport examples are framed as examples, and the exception examples as “such as”; the required criterion remains tied to the normative text. The human judgment caveat on whether two-dimensional layout is genuinely required is apt.

**Minimal correction:** none needed; no defect substring to correct.

## Residual risk / verification gaps

- No website was opened or evaluated; status correctly remains `not-assessed`. No packet selftest or other check command was run because this assignment is a read-only semantic review.
- No tool was installed or updated (none was needed).