# HTMLLink — canonical rel keyword and HTML context

**Source**
- URL: https://html.spec.whatwg.org/multipage/links.html#link-type-canonical
- Accessed: 2026-10-20T21:33Z (UTC)
- Section: 4.6.8.4 Link type "canonical" (HTML Standard, multipage)
- Retrieval: direct HTTPS GET of the live page; no account, no tool install, no network writes. Scratch copies at `/tmp/links.html`, `/tmp/semantics.html`.

**Exact located quote (19 words)**
> The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document.

Verbatim bytes confirmed in source HTML; the missing article before "URL" is in the spec, not a transcription artifact.

**Supporting exact fragment (15 words, same section)**
> The canonical keyword may be used with link element. This keyword creates a hyperlink.

## Scoped teaches (observed)

- The `canonical` keyword is defined only for the `link` element and creates a hyperlink (§4.6.8.4). The non-normative summary table adds: effect on `link` = Hyperlink; *not allowed* on `a`/`area`; *not allowed* on `form`; not marked body-ok.
- The referenced URL is the "preferred URL for the current document", aimed at helping search engines reduce duplicate content; the section defers detail to *The Canonical Link Relation* [[RFC6596]].
- `rel` is an "unordered set of unique space-separated tokens"; keywords are "always ASCII case-insensitive, and must be compared as such" (`rel="next"` equals `rel="NEXT"`). A keyword "must not be specified more than once per rel attribute." The canonical section itself adds no extra token rule.
- `link` element context: metadata content; usable "Where metadata content is expected", in a `noscript` child of `head`, and in the body only when the element is "allowed in the body". That status holds only if `rel` contains *only* body-ok keywords; the body-ok list is `dns-prefetch`, `modulepreload`, `pingback`, `preconnect`, `prefetch`, `preload`, `stylesheet` — `canonical` is absent.
- `link` `href`, when present, "must be a valid non-empty URL potentially surrounded by spaces"; if `href`/`imagesrcset` are absent, "the element does not define a link." So a canonical `link` without `href` creates no canonical signal.
- The spec explicitly notes browsers normally do not process `canonical`: "canonical ought not be included in rel's supported tokens"; a search-engine-like consumer could, in theory. It is not a browser behavior in the processing model.

## Limitations / where the frozen policy exceeds the source

- **Uniqueness is not normative here.** §4.6.8.4 and the table do not say "exactly one canonical link per page", nor address duplicate/conflicting canonicals. The contract's "exactly one canonical link in explicit head" is a local policy ([INFERENCE], reasonable from singular "the preferred URL", but not a spec conformance requirement).
- **Head-only is derived, not stated for canonical.** The canonical section never says `head`. Head placement follows from `link` being metadata content and `canonical` not being body-ok ([INFERENCE], high confidence). A `link rel=canonical` in body is non-conforming; what a search engine does with it is outside this spec.
- **No canonical-specific URL resolution text.** Resolution of relative `href` and `base` precedence is generic HTML/URL behavior, not defined in §4.6.8.4. The contract's first-head-`base` rule is consistent with HTML's single-`base` model but is not spelled out in this section.
- **No acceptance semantics.** The spec does not define validation verdicts, conflict detection, cross-host/query/fragment policy, credentials rejection, or publishing readiness. Those are policy choices; RFC 6596 is cited for relation detail but was not fetched in this scoped task.
- `href=""` is invalid against "valid non-empty URL", yet URL parsing yields the document URL; §4.6.8.4 gives no special canonical handling for that shape ([INFERENCE] on parse result).
- The effect table is explicitly non-normative; use the prose sections for normative claims.
- Scope exclusion: no HTTP `Link` header, redirects, JavaScript rendering, or search-engine selection claims are supported by this section.

## Source status recommendation

Use as a **primary, citable normative source for the `rel=canonical` keyword and `link`-element HTML context**, with the living-standard caveat: WHATWG HTML is continuously updated, not a fixed W3C Recommendation. Cite the section permalink plus access date, quote the exact bytes above, and keep uniqueness/head-only/conflict/credential rules labeled as local policy rather than spec requirements. Pair with RFC 6596 if canonical relation semantics beyond "preferred URL" are asserted. Do not present the non-normative table as normative proof.

**Confidence:** high for the quoted text, token case-insensitivity, element applicability, and `link` context rules; medium-high for head-only as a derivation; explicitly not sourced for "exactly one", conflict handling, or URL normalization policy.

**Remaining unknowns:** whether every frozen matrix case's expected finding aligns with these derived-vs-normative distinctions (e.g. `body_link`, `duplicate_same`, `duplicate_different`, `href_empty`); RFC 6596 detail; search-engine behavior (deliberately out of scope).

**No registry edits.** Read-only seat; only this report was written.
