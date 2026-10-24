# GoogleTroubleshoot — canonical declaration vs Google-selected canonical

Seat: scout (leaf, read-only). Scope: one official-source question; no registry/lane edits, no tools installed, no target instructions followed (source page contained none). Needed for sourced C1 and its quality criteria.

## Source

- URL: https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting
- Access date: 2026-10-20
- Page title: "Fix canonicalization issues" (Google Search Central). Page footer: `Last updated 2026-08-21 UTC`.
- Section holding the quote: **Fix canonicalization issues** — opening paragraph, immediately before numbered step 1 ("Check which page Google considers to be the canonical page").
- Companion checked in the same session (different URL, corroboration only): https://developers.google.com/search/docs/crawling-indexing/canonicalization — section "How Google indexes and chooses the canonical URL".

## Exact located quote (17 words)

> Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons

Verbatim contiguous substring; line wrap only. Second exact quote, same page, section **Common canonicalization issues**, intro (20 words):

> There are various reasons why the selected canonical URL differs from the canonical URL you'd prefer to see in Search.

Terminology observed on the page: step 1 names the two sides as "the Google-selected canonical" versus "your preferred canonical URL"; the URL Inspection link targets `#google-selected-canonical`.

## Scoped teaches (declaration vs selection)

- **Two different objects.** The canonical *declaration* is what the page asserts (`rel="canonical"`, redirects, sitemaps, hreflang — "technical signals" the site controls). The *selected* canonical is Google's deduplication outcome for a cluster, observable only through URL Inspection's "Google-selected canonical". The page's premise is that they can diverge even when the declaration is explicit.
- **Declaration is an input, not a verdict.** Divergence causes the page lists are content-quality/signals plus technical misconfiguration: incorrect canonical elements (CMS-injected `rel="canonical"`/3xx), missing localization annotations, misconfigured servers returning cross-domain content, hacked cross-domain canonical injection, syndication, copycat hosts.
- **Remedy is differential.** Compare selected vs preferred, audit the declared signals, then make clustered pages genuinely different; re-evaluation can take **up to two weeks**, and Search Console "Request Indexing" is quota-limited.
- **C1 boundary, sourced.** This page independently supports the frozen contract's limits wording: policy comparison, not search-engine selection. An offline validator can only judge declaration consistency/conflicts; a clean verdict must never be phrased as "Google will select this URL".
- Companion page states the same boundary in one line: "indicating a canonical preference is a hint, not a rule".

## Limitations of this source for the task

- Troubleshooting guidance, not a normative algorithm: no factor weights, no precedence order, no deterministic selection function. It cannot ground any selection prediction.
- Its primary diagnostic (URL Inspection / Search Console) is a **live verified-property tool**, unavailable offline and out of lane; an offline preflight cannot reproduce step 1.
- Selection inputs include content quality and other index-time signals that are not statically observable from HTML; two-week re-evaluation and quotas are operational, not testable.
- This page does **not** define the mechanics C1 enforces — exact-head placement, one-link policy, `rel` token casing, absolute vs relative resolution, duplicate-link precedence, `base` handling. Those belong to `consolidate-duplicate-urls` (sibling scout) and are not derivable here; do not cite this page for them.
- Snapshot is point-in-time (page dated 2026-08-21 UTC, accessed 2026-10-20); wording may change.

## Source status recommendation

**Current and authoritative for the distinction only** — primary vendor documentation, stable canonical URL, explicit last-updated stamp. Use it to source the declaration-vs-selected split and to justify C1's "not search-engine selection" limit; quote the 17-word sentence verbatim when the distinction is asserted. Do **not** promote it to authority for canonical-link parsing rules, duplicate-link resolution, or any claim about which URL Google would pick. For those, defer to the mechanics source; for the distinction itself no secondary source is needed.

## Touched surfaces

- `.ufo/waves/round-22/w1/GoogleTroubleshoot.md` — this report (only file written).
- No registry, corpus, verifier, script, or lane-state edits; no installs (none needed); no live-property calls.

## Checks for main agent

- Re-open the URL and confirm the 17-word quote still appears verbatim in the opening paragraph of "Fix canonicalization issues".
- If C1 findings are worded as selection guarantees anywhere, reject against this boundary.
