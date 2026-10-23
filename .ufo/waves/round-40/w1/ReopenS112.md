# ReopenS112

Axes: freshness (live GET, hash, clock); source-fidelity (each `teaches` clause only what the pages say). No tool installed.

## Fetch

`timeout 60 curl -fsSL -D xml-names.hdr -o xml-names.html https://www.w3.org/TR/xml-names/` and the same for `https://www.sitemaps.org/protocol.html`, sandbox `/fast/scratch/hyaku/kake-r40w1/ReopenS112/`. Combined command exit 0. Both HTTP 200 at `Date: Fri, 23 Oct 2026 08:37:52 GMT`.

| file | bytes | sha256 | `ignor` raw and tag-stripped |
|---|---|---|---|
| xml-names.html | 51390 | `b4a649e5fdab9852d68eca21442481599164949bcdee5549f2ec7e38fb3cd3a8` | 0 |
| protocol.html | 45292 | `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654` | 0 |

xml-names `last-modified: Tue, 09 Oct 2018 13:27:16 GMT`. Hash equals S112's anchor, S106's anchor, `.ufo/waves/round-40/sources/xml-names.html`, and `.ufo/waves/round-39/sources/xml-names.html`. Protocol hash equals S102's retained hash and `.ufo/waves/round-40/sources/sitemaps-protocol.html`. Row clock `2026-10-23T08:29:16Z` is not on the page and was not re-observed; `corpus/lessons/round-40.md:17` records it. Bytes are unchanged, so the cited document is current.

## §2.3 and S102

Visible text, whitespace collapsed: "2.3 Comparing URI References" (TOC `xml-names.html:125-128`; heading `:283-286`). Quote verbatim at `:301`: "The comparison is case-sensitive, and no %-escaping is done or undone." Expanded name is the pair namespace name + local name (`:206-211`). Prefix: `:503-504` "the prefix functions only as a placeholder for a namespace name."

S102 extension, `protocol.html:1317-1323`: title "Extending the Sitemaps protocol"; body "You can extend the Sitemaps protocol using your own namespace. Simply specify this namespace in the root element." No ignore rule. Example through `:1349` does not add one.

## S106 and the spot-check

S106 `teaches` (`corpus/SOURCES.md:114`) still says a default namespace covers unprefixed elements "(sentences 10–11)" and that `"ignored" in sentence 14 comes from S102`. Spot-check `corpus/lessons/round-39-verifier-spotcheck.md:144` rejects that clause (agree): neither page contains `ignor`; S106's §2.3 quote is verbatim. `w2a3/ReopenS106.md:21-22` called "(sentences 10–11)" overstated and "comes from S102" wrong. Routed defect 1 (`:170-172`) asked for a superseding row. S112 is that row; S106 is left as written.

Contract (`c1-contract.md:41-48`): sentence 10 requires root `urlset` or `sitemapindex` in `http://www.sitemaps.org/schemas/sitemap/0.9`, "whatever prefix binds it", citing S102 and S103, not S106. Sentence 11 names entry children `url` or `sitemap` in the sitemap namespace. Sentence 14 says elements in any other namespace "are ignored" and cites S102's section title only.

## S112 `teaches` (`SOURCES.md:120`)

S112 states only what these sources support. The two routed defects are corrected. One inherited narrowing remains.

- "supersedes S106" — **holds**. Append-only form the spot-check required. Not a claim about the W3C page.
- "a prefix is only a placeholder" — **holds**. Paraphrase of `xml-names.html:503-504` ("functions only as a placeholder"). `:505-508` adds that applications SHOULD use the namespace name, not the prefix.
- "names compare by namespace-name string (case-sensitive, no %-unescaping) plus local name" — **holds**, narrower than the source. `:292-301`: namespace URIs are identical iff the same character sequence; the comparison is case-sensitive and no %-escaping is done or undone. The parenthetical states only the "undone" half. Local name is the other half of the expanded name (`:206-211`), not part of the %-escaping rule. Not false, not more than the source.
- "this grounds how sentences 10–11 decide namespace membership, not what they require" — **holds**. §2.3 (`:288-301`) is the membership test (string identity); §4 is why the prefix does not matter. The sentences require `urlset`/`sitemapindex`/`url`/`sitemap` and that URI; this spec does not. That splits the old overstated "(sentences 10–11)".
- "neither this source nor S102 says foreign elements are \"ignored\"" — **holds**. `ignor` is absent from both visible texts. S102 only permits another namespace (`protocol.html:1321-1323`). "Foreign" is the row's word for sentence 14's "any other namespace"; the negation still matches.
- "sentence 14's \"ignored\" is a lane reading" — **holds**. The word is in `c1-contract.md:47` and in neither source. The contract cites S102 for that sentence; S102 does not say it.

Not restated in `teaches`, still true, still in `scope`: a default namespace applies to unprefixed element names (`xml-names.html:662-663`) and not to unprefixed attributes (`:664`). Dropping it from `teaches` does not revive S106's false attribution.

No counter run (source reopen, no tool).
