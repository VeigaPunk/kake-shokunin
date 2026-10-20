# GoogleCanonical — head-only canonical link + absolute URL guidance

Read-only scout report. No registry edits. Source fetched from the official documentation and treated strictly as data; no instructions inside it were followed.

## Source identity

- **URL:** https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- **Access date:** 2026-10-20
- **Document:** "How to specify a canonical URL with rel="canonical" and other methods" (Google Search Central); page self-canonical points at this same URL; page states "Last updated 2026-07-10 UTC".
- **Relevant sections:** "The `rel="canonical"` `link` element" (anchor `#rel-canonical-link-method`); "The `rel="canonical"` HTTP header" (`#rel-canonical-header-method`); "Best practices".

## Exact located quotes (≤25 words; code-formatting backticks omitted, wording verbatim)

Section "The `rel="canonical"` `link` element" (head-only):

> The rel="canonical" link element is only accepted if it appears in the <head> section of the HTML

(17 words; sentence continues: "so make sure at least the <head> section is valid HTML.")

Same section (absolute URLs):

> Use absolute paths rather than relative paths with the rel="canonical" link element.

(12 words; next sentence: "Even though relative paths are supported by Google, they can cause problems in the long run" — 16 words.)

Section "The `rel="canonical"` HTTP header" (absolute URLs):

> As with the rel="canonical" link element, use absolute URLs in the rel="canonical" HTTP header.

(14 words.)

Supporting best-practice quotes:

> Do include a rel="canonical" link on the canonical page itself (also known as a self-referential canonical).

(16 words.)

> Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments.

(14 words.)

## Scoped teaches

1. **Head-only requirement is explicit.** A `rel="canonical"` link element is "only accepted" in the `<head>`; a link in `<body>` is not an accepted canonical declaration. This directly supports the `canonical_outside_head` finding and the contract's explicit-head bounded parse.
2. **Absolute URL is the recommendation for both delivery forms.** The page tells authors to use absolute paths with the HTML link element, and absolute URLs in the HTTP header. It does **not** say relative paths are invalid.
3. **Relative hrefs are supported but discouraged.** "Even though relative paths are supported by Google, they can cause problems in the long run." Consequence for the policy: resolving a relative href against the first `<base href>`/document URL and then comparing the normalized absolute result is faithful to the platform; using relativity alone as a failure would overstate the source. The contract's "resolve then compare absolute" choice matches this and needs no extra relativity finding id.
4. **Fragments are not canonical.** "Don't specify a URL fragment as canonical" supports rejecting `#...` in a canonical target (`canonical_fragment`).
5. **Self-referential canonical is recommended.** Relevant to the clean positive control (`absolute_match`): canonical on the canonical page itself pointing at itself is best practice, though not a hard requirement for the validator's clean verdict.
6. **Signals, not commands.** The methods "can stack"; none is required, and if no canonical is specified Google identifies a canonical itself. A validator verdict is therefore a *policy preflight*, never a prediction of Google's canonical selection — consistent with contract limit "No … Google canonical selection claim."
7. **Conflicting declarations are discouraged.** "Don't specify different URLs as canonical for the same page using different canonicalization techniques" (example given: sitemap URL differing from `rel="canonical"`). This supports treating different declared canonicals as a defect rather than a preference vote.
8. **Static HTML source is the right inspection surface.** The page says to specify the canonical in the HTML source and ensure JavaScript doesn't change the link element; HTML-source-only static inspection is aligned, with JS-injected canonicals explicitly out of scope.

## Limitations (of the source, and what it does not license)

- **No duplicate-`link` rule stated.** The page does not state what happens when one head contains two or more `rel="canonical"` links to different URLs, nor any precedence. The contract's "exactly one canonical link" (`canonical_multiple`) is our policy choice (RFC 6596 / engine behavior), not a claim sourced from this page.
- **No tokenization or case-sensitivity statement.** It gives lowercase `rel="canonical"` examples only; nothing about ASCII case-insensitive rel token lists, extra rel tokens, or attribute-name case. Those semantics come from the HTML spec / RFC 6596 (`rel_token_list`, `rel_uppercase`, `attr_uppercase`).
- **No normative URL normalization.** No algorithm for scheme/host case, default ports, dot segments, percent-encoding, or query handling. The WHATWG-like normalization in the contract is our chosen comparison method; the quote only speaks about absolute vs relative form and fragments.
- **HTTP header and non-HTML scope.** The header method is for documents including non-HTML (PDF) and "web search results only"; a static HTML-head validator cannot evaluate it, and the page advises choosing one method because using both is more error-prone.
- **Signals out of scope.** Redirects and sitemap inclusion are described as stronger/weaker canonicalization signals; redirects, HTTP headers, JS rendering, network freshness, and publishing readiness are outside the frozen capability limit.
- **Outcome guarantee absent.** The page is Google Search guidance, not a validator specification; it does not guarantee indexing or canonical selection. Quotes above are guidance, and page wording (e.g., "generally doesn't support") is deliberately non-absolute.

## Source status recommendation

- **Status: authoritative primary source (tier A) for this scoped question**, current (last updated 2026-07-10) and consistent with the page's own canonical metadata.
- Use it as the primary citation for: head-only acceptance of the `link` element, absolute-URL recommendation for element and header, relative-supported-but-discouraged nuance, fragment rejection, self-referential best practice, and the "preference/signal, not command" framing.
- **Do not** cite it for duplicate-link precedence or rel-token case-insensitivity; pair those with RFC 6596 and the WHATWG HTML `rel` token rules. Do not present the absolute-URL language as a platform validity requirement — it is a recommendation.
- No registry, lesson, or verifier edits were made; this file is the only write.

## Contract trace

Serves `C1` ("Offline static canonical publishing preflight") quality criteria: explicit-head link canonical (quotes 1, 5), absolute normalized URL comparison (quotes 2, 3, 4), fragment rejection (quote 6), and honest scope limits (teaches 6, limitations). Remaining unknown for L1: none blocking; duplicate-link and rel-token semantics require the RFC/spec pairing noted above.
