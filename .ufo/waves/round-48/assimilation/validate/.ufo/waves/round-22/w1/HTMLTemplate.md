# HTMLTemplate — template inertness and document-tree bounds

Seat `KakeR22.HTMLTemplate` (scout). Round 22, W1, axis operability,
milestone offline-canonical-capability. Report only: no registry edits, no
lane edits beyond this file, no verifier/lesson bytes touched, no installs.

## Source identity

- URL: https://html.spec.whatwg.org/multipage/scripting.html#the-template-element
- Access date: 2026-10-20
- Section: **§4.12.3 "The template element"** (multipage `scripting.html`,
  fragment `#the-template-element`; anchor id confirmed present in the fetch)
- Document: WHATWG HTML Standard, multipage living standard; page header
  reads "Last Updated 20 October 2026"
- Fetch provenance: 276,128 bytes, sha256
  `5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43`,
  scratch copy `/tmp/r22-scripting.html` (outside the lane). Quote matches
  verified against whitespace-normalized rendered text; each quote occurs
  exactly once.

## Located quotes

Primary — document-tree bounds (14 words):

> "The template contents of a template element are not children of the element itself."

Location: §4.12.3, standalone paragraph after the
`shadowrootcustomelementregistry` boolean-attribute paragraph and before
"It is also possible, as a result of DOM manipulation…". The linked phrase
"are not children of the element itself" targets `syntax.html#template-syntax`.

Corroborating — inertness (17 words, mid-sentence clause; in the source it
follows a comma and ends the note):

> "so that they aren't in a browsing context and thus remain inert (e.g. scripts do not run)"

Location: §4.12.3, closing note of the "appropriate template contents owner
document" algorithm (step 1, substep 2: a single proxy `Document` with null
browsing context owns the template contents of all template elements).

Context sentence (21 words, same section): "The template element is used to
declare fragments of HTML that can be cloned and inserted in the document by
script." Rendering sentence (8 words): "In a rendering, the template element
represents nothing."

## Scoped teaches (what this source establishes)

1. **Template contents are outside the document tree.** Each `template`
   element has an associated `DocumentFragment` — its "template contents" —
   whose host is the template element; the contents are expressly *not*
   children of the element. The element's content model is `Nothing`. A
   `<link rel="canonical" href="…">` placed inside `<template>…</template>`
   therefore lands in that fragment, not in `<head>` and not anywhere in the
   document tree.
2. **The contents are inert.** They are owned by an inert template document
   with a null browsing context, so they "remain inert (e.g. scripts do not
   run)"; the template represents nothing in rendering; contents enter the
   document only when script clones and inserts them. Inertness is a property
   of the subtree, not merely of `<script>`.
3. **Consequence for the frozen matrix case `template_decoy`.** A
   canonical-looking link inside `<template>` is not a canonical link for
   head discovery: it must not satisfy "exactly one canonical link in explicit
   head", must not count toward duplicate detection, and its `href` must not
   be resolved/compared (so it must not manufacture wrong-host, wrong-path,
   wrong-query, or invalid-URL findings). With no other link present, the page
   is an absent-canonical policy failure — exit `1` under the frozen exitMap,
   not a could-not-evaluate exit `2`. If a real head canonical also exists,
   the result must be clean (or the real link's own finding), with the decoy
   fully ignored.
4. **The guarantee is about the parse/DOM tree, not about raw bytes.** The
   markup still contains the decoy link, so any scanner that does not model
   template contents will see it. Correct offline behavior requires the
   validator to exclude links with a `<template>` ancestor (e.g. template-depth
   tracking in a token walk); regex or flat-token scanning of the serialized
   HTML will misclassify `template_decoy`. This implementation step is
   **[INFERENCE]** from the tree-bound fact, not spec text.

## Limitations

- This page defines HTML template semantics only. The token "canonical" does
  not occur in the fetched page (0 matches): it says nothing about the
  `canonical` link type, its allowed or required position, duplicate policy,
  or URL comparison. Those belong to the links section (`links.html#link-type-
  canonical`), sourced by a separate seat, not to this report.
- Living standard, not a frozen edition: section numbering, anchor target, and
  prose can change. Only the access date, page pubdate (20 October 2026), and
  fetched-bytes sha256 pin this read; re-fetch and re-check the quote digest at
  integration.
- The claim governs conforming DOM construction. It does not describe how a
  particular validator parses bytes, and a non-conforming scanner can still
  miscount. It also says nothing about JavaScript-inserted links, HTTP
  headers, rendering-time discovery, or search-engine selection.
- The parser insertion rules for the "in template" insertion mode live in
  `parsing.html` and were not opened. That the parser appends such a link to
  the template-contents fragment follows from the template-contents model, but
  the insertion-mode text is uncorroborated here — treat as **[INFERENCE]**.
- `shadowrootmode`/declarative-shadow-root templates are only visible here in
  the attribute table; their conversion path was not read, so no claim is made
  about them beyond the general template-contents statement.
- No browser execution, no tests, no search-engine documentation. Nothing here
  establishes how any crawler treats a template-wrapped canonical.

## Source status recommendation

- Official WHATWG HTML Standard, §4.12.3, normative for HTML semantics.
  Suitable as **tier A** authority for exactly one claim: template contents are
  not children of the element/document tree and are inert. Cite with the URL
  anchor, access date 2026-10-20, page pubdate, and fetched sha256; record it
  as a living source, revalidated on release.
- Do **not** cite it for canonical policy, duplicate/conflict handling, URL
  resolution, or search-engine behavior. In any source row, pair the scope
  sentence with that exclusion.
- Quote hygiene: the inertness sentence is a mid-sentence clause and must be
  presented as such (not capitalized into a standalone sentence); do not
  truncate across the sentence boundary. Both recorded quotes are exact and
  ≤25 words.

## Hygiene / boundaries

- Only file written: this report. No registry, corpus, ledger, verifier, or
  lesson edits; no git/jj writes in the lane; no source changes.
- No credentials, accounts, host services, or package transactions. No tool
  installs or updates were needed or made.
- Network: two GETs of the single cited URL (reader fetch plus curl for
  byte-exact verification); no other hosts.
