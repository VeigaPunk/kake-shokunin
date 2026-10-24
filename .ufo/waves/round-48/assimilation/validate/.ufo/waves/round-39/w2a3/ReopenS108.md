# ReopenS108

Axes: operability (one GET, hash, locate every scope/anchor/teaches claim); freshness (status, clock, retained bytes). No tool installed.

## Fetch

`timeout 90 curl -fsSL -D headers.txt -o faq.html -w … --max-time 60 --proto =https https://www.sitemaps.org/faq.html` exit 0. HTTP 200, 0 redirects, final URL unchanged, 15681 bytes, `text/html`. Response `date: Fri, 23 Oct 2026 07:46:42 GMT`. `last-modified: Thu, 08 Jul 2021 05:32:00 GMT`.

`sha256sum` and `cmp -s` exit 0. Live `/fast/scratch/hyaku/kake-r39a3w2/ReopenS108/faq.html` and retained `.ufo/waves/round-39/sources/faq.html` are both `7f5176f4c7194f4340ba86d401f93e9f4f5e7219f92360f32cd341c1a8c2d9a1` (row anchor; `sources/SHA256SUMS:10`). Byte-identical, so no visible-text diff. The row clock `2026-10-23T06:56:39Z` is not on the page; `corpus/lessons/round-39.md:35` and `:44` record the L1 re-open at 06:56:39Z, HTTP 200. This run did not re-observe that clock.

## Cells

**scope — holds.** Size and count: `faq.html:305` "How big can my Sitemap be?" and `:309-311` "Sitemaps should be no larger than 50MB (52,428,800 bytes) and can contain a maximum of 50,000 URLs." Host and directory: `:263-265` "Where do I place my Sitemap?"; `:289` "All URLs listed in the Sitemap must reside on the same host as the Sitemap."; `:283-285` permission to "report metadata under http://example.com/path/"; `:293-295` a sitemap in `myfolder` "can't include URLs from http://www.example.com." Entity and URL escaping: `:161-163` "How do I represent URLs in the Sitemap?"; `:167-169` "entity escape codes"; `:179-181` "you can generally URL escape them" and "You will still need to entity escape them." Not S102's "uncompressed": that word is absent here; FAQ says "whether compressed or not" (`:427-429`). S102 has it verbatim at `sources/sitemaps-protocol.txt:179` ("once uncompressed must be no larger than 50MB") and `sitemaps-protocol.html:693`.

**anchor — holds.** Size section `:305` (`#faq_sitemap_size`). Location section `:263` (`#faq_sitemap_location`). Escaping is the represent-URLs answer `:161` (`#faq_xml_encoding`), not a heading titled "escaping"; `#faq_url_encoding` (`:387`) is session IDs only. "Last Updated" is verbatim at `:485`: "Last Updated: Monday, November 21, 2016". The cell's "21 November 2016" is that calendar day, not those characters in that order. Backtick SHA256 matches the file. HTTP 200 matches this GET; the 06:56:39Z instant is the lesson record above.

**teaches — holds.**
- "50,000 URLs and 52,428,800 bytes (sentences 19–20)": both numbers are at `:309-311`. "more than 50,000" / "bigger than 50MB" (`:313-315`) is the same boundary as sentence 19 "larger than 52,428,800" and sentence 20 "More than 50,000 entries" (`c1-contract.md:57-59`). The index cap is the same pair (`:321-323`).
- "same-host, same-directory placement (sentence 25)": same host is verbatim at `:289`. Directory scope is the path prefix at `:283-285` plus the myfolder counterexample `:293-295`, which is sentence 25's directory clause (`c1-contract.md:67-70`: path must start with the sitemap URL's directory). "same-directory" is the row's gloss, not a page phrase. This answer does not mention scheme or port; sentence 25 also checks those, and the cell does not say the FAQ states them.
- "never states the index's host-only rule (sentence 27)": sentence 27 (`c1-contract.md:72-73`) is scheme, host and port only, from S102 "same site" (`sitemaps-protocol.txt:196-197`). FAQ index text is count and size (`:317-323`), lastmod (`:335-339`), and the schema link (`:461`). No "same site" exception and no host-only rule for an index.

**Quoted phrases.** "Last Updated" is verbatim (`:485`). "uncompressed" is S102's word (`sitemaps-protocol.txt:179`), not a FAQ quote. The SHA256 matches. The lesson quote at `round-39.md:44` ("Sitemaps should be no larger than 50MB (52,428,800 bytes) and can contain a maximum of 50,000 URLs.") is verbatim at `faq.html:309-311`.

**Sentence numbers.** 19–20 are the byte and entry ceilings, 25 is urlset host plus directory prefix, 27 is the index host-only rule. Each says what the row says it says.
