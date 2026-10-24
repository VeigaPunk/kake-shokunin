# HTMLBase — `<base href>` / first-base semantics (scoped source evidence)

Scope: one question only — how the first `<base href>` establishes the document base URL, for C1
"Offline static canonical publishing preflight". No registry edits, no lane edits beyond this report.

Lane base observed: `7c61c8cc791bde36dd5e3688bdfea2678d90146c` (matches contract).

## Source access

- URL: https://html.spec.whatwg.org/multipage/semantics.html#the-base-element
- Document: WHATWG HTML Living Standard, §4.2.3 "The base element" (4.2 Document metadata)
- Access date: 2026-10-20 (native fetch)
- Primary exact quote (§4.2.3, 15 words):
  > "If there are multiple base elements with href attributes, all but the first are ignored."
- Corroborating source: https://html.spec.whatwg.org/multipage/urls-and-fetching.html#document-base-url
  §2.4.3 "Document base URLs", accessed 2026-10-20. Exact quote (13 words):
  > "return the frozen base URL of the first such base element in tree order"
- Checked for bounds: https://html.spec.whatwg.org/multipage/links.html#link-type-canonical §4.6.8.4,
  accessed 2026-10-20. Canonical is only: "The canonical keyword indicates that URL given by the href
  attribute is the preferred URL for the current document", with behavior deferred to RFC 6596.
  WHATWG does not define selection rules there.

## Observed facts (normative, as written)

Section anchors are on the two URLs above.

1. Purpose: `<base>` with `href` lets authors "specify the document base URL for the purposes of parsing
   URLs"; the element represents no other content. `href` "must contain a valid URL potentially
   surrounded by spaces." (§4.2.3)
2. Cardinality: "There must be no more than one base element per document." Content model: allowed
   "In a head element containing no other base elements." Base is metadata content, no end tag. (§4.2.3)
3. Ordering (authoring conformance): a base with `href` "must come before any other elements in the tree
   that have attributes defined as taking URLs." A base with `target` must precede hyperlink elements.
   (§4.2.3)
4. Multiplicity: all but the first base with `href` are ignored; same rule for `target`. (§4.2.3)
5. Frozen base URL: only the first base (tree order) with `href` has a frozen base URL; it is set
   immediately when that element becomes first or its `href` changes. Computation parses its `href`
   against the document's *fallback base URL* plus document encoding — "Thus, the base element isn't
   affected by itself." (§4.2.3)
6. Fallback on unusable base: if parsing fails, the scheme is `data` or `javascript`, or CSP
   "Is base allowed for Document?" returns "Blocked", the frozen base URL is set to the document's
   fallback base URL — i.e. a bad base degrades to the document URL, it does not invalidate the page.
   (§4.2.3)
7. Resolution precedence (§2.4.3): document base URL = frozen base URL of the first descendant base with
   `href`; else document's base URL override; else fallback base URL (document URL, with about:blank /
   about:srcdoc special case via about base URL).
8. Relative resolution: a base like `https://www.example.com/news/index.html` makes `archives.html`
   resolve to `https://www.example.com/news/archives.html` — directory semantics come from the URL
   parser, not from a special base rule. (§4.2.3 example)
9. Late/invalid base: the conformance "must come before" rule is not restated inside the frozen-base
   algorithm; the algorithm keys only on "first ... in tree order". A validator that flags a base placed
   after URL-taking elements is enforcing authoring conformance, not re-simulating a different base
   resolution rule. [INFERENCE from absence of such a branch; the spec does not state late bases are
   ignored.]
10. The `href` IDL getter parses the attribute against the fallback base URL, explicitly "isn't affected
    by other base elements or itself", returns the URL serialization, or the raw value on parse failure.
    (§4.2.3)
11. Changing the base URL later does not retroactively change already-embedded resources; subsequent IDL
    reads can return URLs that no longer match what is displayed. (§2.4.3 note, "respond to base URL
    changes")

## Scoped teaches for C1

- A relative `canonical` link resolves (in a user agent) against the document base URL, which is the
  first `<base href>` resolved against the document URL — so the audit's canonical target may differ
  from manifest page URL when a base exists, even though base is a separate element.
- Encode "first wins": second and later `<base href>` never contribute to resolution. Presence of a
  second `<base href>` (or any second base) is itself an authoring violation to flag, distinct from its
  ignored value.
- Ordering rule: a `<base href>` must precede URL-taking elements; flagging a later base is a conformance
  finding, not evidence that browsers ignored it for that canonical.
- Invalid/`data:`/`javascript:` base href (and CSP-blocked base, if evaluable) falls back to the document
  URL. Absolute canonical targets are unaffected by any base — base only changes relative resolution.
- A page whose canonical is relative and whose base is absent resolves against the document URL, not
  against the manifest directory; the manifest/offline file path is not, by itself, the base.
- `<base target>` is orthogonal to canonical URL resolution; do not let it perturb canonical findings.
- Canonical policy authority is not in this section; WHATWG only names the keyword and defers to RFC 6596.
  C1 findings about absolute-vs-relative canonical and host equality must cite the RFC/policy scouts, not
  §4.2.3.

## Limitations (must not be overclaimed)

- §4.2.3 is conformance/runtime semantics for base; it defines no canonical selection, no ranking, no
  requirement that canonical be absolute, same-host, or equal to base.
- It does not say what a search engine does with relative canonical URLs or with ignored bases beyond
  the generic URL-parsing model; that is outside WHATWG HTML.
- CSP `base-uri` evaluation depends on the document's active policy; header-delivered CSP is invisible
  to an offline static audit, so "Blocked" cannot be fully modeled from HTML bytes.
- Frozen-base computation is dynamic (DOM insertion/mutation, ordering changes). An offline validator
  models a single parse-time snapshot and must state that assumption.
- Encoding matters: the parsing step takes the document's character encoding; an offline tool reading
  bytes must choose an encoding assumption and record it.
- The spec is a Living Standard: anchors are stable in practice but numbering/prose can change; cite the
  section anchor and access date, not a fixed edition.
- `<base>` outside `<head>` is non-conforming by content model; the spec does not prescribe that parsers
  relocate it, so offline tree-shape claims should follow parser behavior, not content model alone.

## Source status recommendation

Use as the primary normative source for base-href resolution and first-base precedence in C1 (section
anchor + access date as above). Do not use it as authority for canonical policy or search-engine
behavior; pair it with RFC 6596 and Google Search Central scouts for those claims. No registry edits
made; no tools installed; no network beyond these official documentation fetches.

Remaining unknowns (outside this ticket): how the C1 policy chooses between rejecting relative
canonical vs resolving through base; whether late-base placement is exit-2 or a finding (contract decides).
