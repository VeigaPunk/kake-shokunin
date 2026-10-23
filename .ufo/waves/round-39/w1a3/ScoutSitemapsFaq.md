# ScoutSitemapsFaq — sitemaps.org FAQ vs contract sentences 19–27

Opened `https://www.sitemaps.org/faq.html` (GET, no redirect). Not written into `corpus/SOURCES.md` (leaf). No installs. Affinity cookies from the response were not retained.

## Fetch

- `curl -sS -D faq.headers -o faq.html --max-time 60 -L` at 2026-10-23T06:53:06Z → **exit 0**, HTTP 200, 0 redirects, `Content-Length: 15681`, `Content-Type: text/html`, `Last-Modified: Thu, 08 Jul 2021 05:32:00 GMT`, page text "Last Updated: Monday, November 21, 2016" (`faq.html:485`).
- Bytes: UTF-8 BOM, CRLF, 15681 bytes, 508 lines. sha256 `7f5176f4c7194f4340ba86d401f93e9f4f5e7219f92360f32cd341c1a8c2d9a1`.
- Path: `/fast/scratch/hyaku/kake-r39a3w1/ScoutSitemapsFaq/faq.html`. Headers (cookies redacted): `.../faq.headers`.

## Draft SOURCES row (next id after S104; not appended)

| S105 | sitemaps.org: FAQ — https://www.sitemaps.org/faq.html | docs | A | Official FAQ restatement of Sitemap size, URL count, host and directory placement, and entity escaping; not S102's uncompressed gzip measurement | How big can my Sitemap be? faq.html:305-325; Last Updated: Monday, November 21, 2016 at faq.html:485; fetched 2026-10-23T06:53:06Z, HTTP 200, SHA256 7f5176f4c7194f4340ba86d401f93e9f4f5e7219f92360f32cd341c1a8c2d9a1 | The FAQ caps each Sitemap at 50,000 URLs and 52,428,800 bytes and keeps listed URLs on that Sitemap's host and directory | queued | 2026-10-23 | 365d | — |

Quote (17 words), grounds sentences 19–20: "Sitemaps should be no larger than 50MB (52,428,800 bytes) and can contain a maximum of 50,000 URLs." (`faq.html:309-311`).

## What the page says

- **Entity escaping** (`#faq_xml_encoding`, `faq.html:167-197`). Data values including URLs must use entity escape codes for ampersand, single quote, double quote, less than, and greater than (`faq.html:169-171`). Rendered example result (`faq.html:197`, source `&amp;amp;` / `&amp;gt;`) is `http://www.example.com/view?widget=3&amp;count&gt;2`. The `#escaped` link (`faq.html:167`) has no target in this file.
- **URL encoding of loc** (same answer, not `#faq_url_encoding`). "you can generally URL escape them as part of that script." (11 words, `faq.html:179-181`); entity escaping is still required. Also cites RFC-3986, RFC-3987, and the XML spec (`faq.html:171-177`). `#faq_url_encoding` (`faq.html:387-395`) is only "remove session IDs."
- **File location / scope** (`#faq_sitemap_location`, `faq.html:263-297`). Root placement is "strongly recommended" (`faq.html:269-271`). "you also have permission to report metadata under http://example.com/path/." (9 words, `faq.html:283-285`). "All URLs listed in the Sitemap must reside on the same host as the Sitemap." (15 words, `faq.html:289`). A sitemap at `http://www.example.com/myfolder/sitemap.xml` "can't include URLs from http://www.example.com." (13 words, `faq.html:293-295`); the subdomain example is the same paragraph.
- **gzip** (`#faq_compression`, `faq.html:427-429`, 14 words): "your Sitemap must be no larger than 50MB (52,428,800 bytes), whether compressed or not." Size answer also says you can gzip (`faq.html:323-325`). Zip is not offered; the question is "zip … or … gzipped?"
- **50,000 / 50 MB.** Sitemap: maximum 50,000 URLs and no larger than 50MB (52,428,800 bytes); bigger means multiple files plus an index (`faq.html:309-321`). Index: "up to 50,000 Sitemaps and must not exceed 50MB (52,428,800 bytes)" (17 words, `faq.html:321-323`).

## Sentences 19–27

**No contradiction of the scored predicates.**

- **19–20.** Same ceiling: ≤ 52,428,800 bytes and ≤ 50,000 entries (exactly 50,000 / exactly 52,428,800 allowed). "should" at `faq.html:309` is followed by "must create multiple" if bigger (`faq.html:313-315`). Index caps match both file kinds.
- **21, 23, 24, 26.** Silent on whitespace trimming, a 2,048-character `loc`, port defaulting, and percent-decoding or dot-segment removal. Silence is not a contradiction. URL-escaping advice matches comparing the escaped path as written (26).
- **22.** "include the protocol (for instance, http)" (`faq.html:365-371`) grounds an absolute URL; "for instance, http" does not forbid https. Trailing-slash advice is outside 19–27.
- **25.** Directory permission (`faq.html:283-285`) plus the myfolder example match the directory prefix. The example names the parent origin with no path; read with the previous sentence, it does not forbid URLs under that directory. Scheme is not in this answer (the http/https answer, `faq.html:375-383`, says list only one version, not that cross-scheme is valid).
- **27.** The FAQ never states the index exception (scheme, host, and port only). It does not apply the myfolder rule to child sitemap URLs.

**Adjacent, not a sentence-19 miss:** FAQ gzip text does not say "once uncompressed." S102 does (`sources/sitemaps-protocol.txt:178-180`: uncompressed must be ≤ 50MB). Sentence 19 counts the file's own bytes; the contract already says no gzip (`c1-contract.md:99`). A small gzip of a larger XML passes sentence 19 and fails that S102 sentence. The FAQ's "whether compressed or not" does not add the uncompressed measurement.

Confidence: high on the fetch, the quotes, and no contradiction of 19–27. The gzip note is a conflict with S102, not with sentence 19.
