# Curated sources to consider — kake — 2026-11-03

**Status: unassimilated future reading after hyaku.** This is a separate source-candidate note, not a training round, source admission, readiness claim or instruction to change the current plan. Existing dated reflections remain unchanged.

Public primary sources were read on **2026-11-03 (UTC)**. No candidate code was installed or executed, no live target was tested, and no analyzed artifact was uploaded. All commentary below is original; source material is linked rather than copied.

## 1. W3C WCAG Evaluation Methodology 2.0
- **Type and source:** Methodology / W3C Group Note — [primary source](https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/)
- **Version / maintenance:** Dated Group Note, 2026-07-23. Dated Note and official overview opened 2026-11-03; overview identifies the July 2026 publication. [Evidence](https://www.w3.org/TR/wcag-em-2/)
- **Why it fits:** Provides a structured route from evaluation scope and product exploration to representative sampling and reporting. This is well matched to the lane’s accessibility review preparation, especially separating an inventory or sampled result from a whole-site conformance assertion.
- **Reading and proposed later use:** Read the conformance-claims discussion and steps 1, 3 and 5. After hyaku, consider a review-packet outline recording scope, sample rationale, complete processes and unevaluated states, without assessing a live property.
- **Limits:** Informative methodology, not additional WCAG requirements. Sample evaluation alone cannot establish whole-site conformance. Browser and assistive-technology execution remain adjacent, separately authorized work; publication remains operator-owned.
- **License:** W3C Document License (2023); preserve status and attribution for any later reproduction. [License evidence](https://www.w3.org/copyright/document-license-2023/)
- **Duplicate check:** Same W3C accessibility family as existing WCAG 2.2 and criterion sources, but neither WCAG-EM URL nor source name occurs in the supplied inventory/context. The distinct gap is evaluation design and reporting limits.

## 2. Nu Html Checker (vnu)
- **Type and source:** Maintained repository — [primary source](https://github.com/validator/validator)
- **Version / maintenance:** Rolling latest release; GitHub metadata records publication at 2026-11-03 11:01 UTC. The annotated latest tag resolves to release commit 93ef02990d37eb26c0d4a4af7c7882d7cbe37ade (tag object 2453dcd70c6f4166b3a7a14977e6821d364bc21b), independently checked 2026-11-03. The project uses rolling latest rather than major-number releases. No binary downloaded or run. [Release](https://github.com/validator/validator/releases/tag/latest) · [Pinned commit](https://github.com/validator/validator/commit/93ef02990d37eb26c0d4a4af7c7882d7cbe37ade)
- **Why it fits:** A standards-oriented markup checker offers a separate perspective on generated HTML before publishing. It complements host-scope, canonical-link and header audits rather than replacing them.
- **Reading and proposed later use:** Read its usage and checker-output documentation. After hyaku, consider an offline comparison on owned saved HTML: identify which structural problems existing publisher checks miss and which findings need human judgment.
- **Limits:** Markup checks cannot establish accessibility, browser behavior, indexing or deployment correctness. Do not send private HTML to a hosted checker. A moving latest tag needs a full revision and artifact digest before any approved future execution.
- **License:** MIT for repository; review bundled dependency notices before redistribution. [License evidence](https://raw.githubusercontent.com/validator/validator/main/LICENSE)
- **Duplicate check:** No validator/validator repository or Nu checker source family found in the supplied lane inventory. Related HTML/WHATWG standards already exist, but this is an additional implementation reference.

## Admission boundary

Re-check the exact version, relevant sections and licensing before later use. Any adoption needs the lane’s normal independent review and evidence gates after hyaku. This file changes no corpus registry, skill, scorecard, training input, authorization or deployment state.
