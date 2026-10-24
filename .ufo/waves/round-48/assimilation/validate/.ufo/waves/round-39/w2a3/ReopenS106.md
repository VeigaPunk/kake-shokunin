# ReopenS106

Axes: operability (one GET, hash, locate every scope/anchor/teaches claim); freshness (status, clock, retained bytes). No tool installed.

## Fetch

`timeout 60 curl -fsSL -A 'kake-r39a3-reopen/1.0' -D headers.txt -o xml-names.html https://www.w3.org/TR/xml-names/` exit 0. HTTP/2 200, `date: Fri, 23 Oct 2026 07:46:38 GMT`, `last-modified: Tue, 09 Oct 2018 13:27:16 GMT`, `content-location: Overview.html`, canonical `https://www.w3.org/TR/xml-names/`, 51390 bytes, `text/html; charset=utf-8`.

`sha256sum` printed `b4a649e5fdab9852d68eca21442481599164949bcdee5549f2ec7e38fb3cd3a8` for both live `/fast/scratch/hyaku/kake-r39a3w2/ReopenS106/xml-names.html` and retained `.ufo/waves/round-39/sources/xml-names.html` (row anchor; `sources/SHA256SUMS:8`). Python `a==b` True, 51390 bytes. Byte-identical, so no visible-text diff. Page has no `sitemap` and no `ignor`. The row clock `2026-10-23T06:56:39Z` is not on the page; `corpus/lessons/round-39.md:35,42` records the L1 re-open. Retained mtime is `2026-10-23 03:57:43 -0300` (06:57:43Z). This run did not re-observe 06:56:39Z.

## Cells

**scope — holds.** Expanded name is the pair namespace-name + local name: `xml-names.html:206-211`. Namespace URIs are identical iff the strings are the same character sequence: `:292-300`, and that comparison decides whether two names belong to the same namespace: `:288-291`. Default-namespace scope: `:655-660` (start-tag through matching end-tag, excluding inner defaults). Case-sensitive namespace-name comparison: `:301`. Not a sitemap rule to ignore foreign elements: the file never says sitemap or ignore.

**anchor — holds.** §2.3 heading and TOC are "Comparing URI References": `:125-128`, `:283-286`. §4 is "Qualified Names" (`:130`, `:475`); the placeholder sentence is inside it at `:503-504` ("the prefix functions only as a placeholder for a namespace name"). §§6.1–6.2 are "Namespace Scoping" and "Namespace Defaulting": `:133-134`, `:614`, `:654` (parent id `scoping-defaulting` at `:613`). "W3C Recommendation 8 December 2009" verbatim `:35`. Title "Namespaces in XML 1.0 (Third Edition)" verbatim `:34`. Backtick SHA256 matches the file. HTTP 200 observed on this GET. The fetch clock was not re-observed.

**teaches — wrong.**
- "A prefix is only a placeholder" **holds** as a paraphrase of `:503-504` (not a quotation). `:505-508` adds that applications SHOULD use the namespace name, not the prefix.
- "names compare by namespace-name string (case-sensitive, no %-unescaping) plus local name" **holds** as a paraphrase, not a quote. `:296-301`: identical iff the same sequence; "The comparison is case-sensitive, and no %-escaping is done or undone." The row's "no %-unescaping" is the "undone" half only; the spec also forbids doing the escaping. Local name is the other half of the expanded name (`:206-211`, `:625-637`).
- "a default namespace covers unprefixed elements" **holds**: `:662-663` "A default namespace declaration applies to all unprefixed element names within its scope." `:254-255` says the same in §2.1. It does not apply to unprefixed attributes (`:664`).
- "(sentences 10–11)" **overstated.** Sentence 10 (`c1-contract.md:41-43`) requires root local name `urlset` or `sitemapindex` in the literal namespace `http://www.sitemaps.org/schemas/sitemap/0.9`, "whatever prefix binds it", and cites S102 and S103, not S106. Sentence 11 (`:44-45`) names entry children `url` or `sitemap` in the sitemap namespace. Neither sentence states case-sensitive comparison, %-escaping, or that a default namespace covers unprefixed names. "Whatever prefix" matches the placeholder reading for sentence 10 only.
- `"ignored" in sentence 14 comes from S102, not here` **wrong** on "comes from S102"; "not here" **holds**. Sentence 14 (`c1-contract.md:47-48`) does say "are ignored" and cites S102 "Extending the Sitemaps protocol". That section title is verbatim at `sitemaps-protocol.html:1317`. Its body (`:1321-1323`) is only "You can extend the Sitemaps protocol using your own namespace. Simply specify this namespace in the root element." Neither `sitemaps-protocol.html` nor `sitemaps-protocol.txt` contains `ignor`. `xml-names.html` does not either.

**Quoted phrases.** The only quoted word in the three cells is "ignored". It is verbatim in sentence 14 and absent from this page and from S102. The backtick SHA256 matches the file. The lesson gate quote at `round-39.md:42` ("The comparison is case-sensitive, and no %-escaping is done or undone.") is verbatim at `xml-names.html:301`.

**Sentence numbers.** 10 and 11 are the root namespace-plus-local-name rule and the entry namespace-plus-local-name rule; they do not say the comparison or default-namespace clauses the parenthetical attaches. 14 does say "ignored", but that word is the contract's, not S102's and not S106's.
