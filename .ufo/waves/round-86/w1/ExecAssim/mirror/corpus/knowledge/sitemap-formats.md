source: S012 — https://www.sitemaps.org/protocol.html (page prints "Last Updated: Monday, November 21, 2016"; retained HTML `.ufo/waves/round-77/w1/ScoutSources/protocol.raw`, 45,292 bytes, sha256 5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654, HTTP 200); S447 — https://www.rfc-editor.org/rfc/rfc1952.txt (GZIP file format specification version 4.3, May 1996; retained `.ufo/waves/round-77/w1/ScoutSources/rfc1952.raw`, 25,037 bytes, sha256 164ef0897b4cbec63abf1b57f069f3599bd0fb7c72c2a4dee21bd7e03ec9af67, HTTP 200); S448 — https://www.rfc-editor.org/rfc/rfc4287.txt (Atom Syndication Format 1.0; retained `.ufo/waves/round-77/w1/ScoutSources/rfc4287.raw`, 81,922 bytes, sha256 3bd71d76289560c9e860151f39cebbdc402cfd8b788a62048d8dc42824f2d89c, HTTP 200)
verified-at: 2026-11-03 (own public GET of the sitemaps.org page 2026-11-04T01:37:42Z: HTTP/2 200, `content-length: 45292`, body sha256 5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654 — byte-identical to the retained `protocol.raw`; the two RFC files were read from the wave's retained raw copies, not re-fetched by this seat)
recheck: 365d, or sooner on a change to S012/S447/S448 — `curl -fsSL https://www.sitemaps.org/protocol.html | grep -c 'once uncompressed'` (retained bytes return `1`); `curl -fsSL https://www.rfc-editor.org/rfc/rfc1952.txt | grep -c 'fixed values ID1'`; `curl -fsSL https://www.rfc-editor.org/rfc/rfc4287.txt | grep -c 'MUST have an href attribute'`
ground: sitemap container and format coverage (C2) — the container and format rules an offline sitemap audit decides, attributed to the row that states each one; no fetch of any lane property, no engine acceptance

# Sitemap containers and formats

**Quote convention.** Each quote is the named line range of the named retained file with HTML markup and
entities rendered and runs of whitespace collapsed to one space; no word is added or removed, every quote
is ≤25 words, and a `code` span inside a quote sets a literal element name — read it without the
backticks. `S012` line numbers are `.ufo/waves/round-77/w1/ScoutSources/protocol.raw`, `S447`
`rfc1952.raw`, `S448` `rfc4287.raw`. The same bytes are also retained as `protocol.txt`, `rfc1952.txt` and
`rfc4287.txt` (the wave's whitespace-stripped renders, whose line numbers differ); citations here stay on
the raw files so a checker can re-read a range without the renderer.

## What a sitemap file is in this lane's reading

A sitemap file is a byte stream that lists URLs, and the protocol's own description of it is the XML
schema (S012):

> This document describes the XML schema for the Sitemap protocol.
> — S012, `protocol.raw:82`, section "Sitemaps XML format"

In the XML form the file carries one `<url>` entry per URL (S012):

> Include a `<url>` entry for each URL, as a parent XML tag.
> — S012, `protocol.raw:104-106`, section "Sitemaps XML format"

The protocol page names three formats in all — the XML schema, a syndication feed, and a text file (S012):

> in addition to the XML protocol, we support RSS feeds and text files, which provide more limited information
> — S012, `protocol.raw:943-949`, section "Other Sitemap formats"

The XML member of that set is rooted at `urlset` (S012):

> Begin with an opening `<urlset>` tag and end with a closing `</urlset>` tag.
> — S012, `protocol.raw:96-98`, section "Sitemaps XML format"

The other two members are the syndication feed (RSS 2.0 and Atom) and the plain-text list, described in the
sections below (S012).

## The gzip container

A sitemap may be gzip-compressed (S012):

> you may compress your Sitemap files using gzip
> — S012, `protocol.raw:691-692`, section "Using Sitemap index files (to group multiple sitemap files)"

The size limit is the size of the file once uncompressed (S012):

> the sitemap file once uncompressed must be no larger than 50MB
> — S012, `protocol.raw:693-695`, section "Using Sitemap index files (to group multiple sitemap files)"

The limit's byte figure is 52,428,800 (S012):

> must be no larger than 50MB (52,428,800 bytes)
> — S012, `protocol.raw:689`, section "Using Sitemap index files (to group multiple sitemap files)"

The pair that identifies the container is the gzip format's two identification bytes (S447):

> These have the fixed values ID1 = 31 (0x1f, \037), ID2 = 139 (0x8b, \213), to identify the file as being in gzip format.
> — S447, `rfc1952.raw:291-292`, §2.3.1 "Member header and trailer"

gzip's customary compression method is `deflate` (S447):

> CM = 8 denotes the "deflate" compression method, which is the one customarily used by gzip
> — S447, `rfc1952.raw:296-298`, §2.3.1 "Member header and trailer"

The audit's reading is that the container is decided by those two bytes, `1f 8b`, never by the name
(S447); the page supports name-independence only for the text file, whose name it leaves free (S012). The
protocol page states no magic bytes of its own: `grep -ci '1f 8b' protocol.raw` → `0`,
`grep -ci 'magic' protocol.raw` → `0` (S012).

## The plain-text format

The text format is a list of URLs (S012):

> You can provide a simple text file that contains one URL per line.
> — S012, `protocol.raw:991-992`, section "Other Sitemap formats → Text file"

One URL per line, with no embedded newline (S012):

> The text file must have one URL per line. The URLs cannot contain embedded new lines.
> — S012, `protocol.raw:997`, section "Other Sitemap formats → Text file"

Each URL is absolute, in this lane's reading: the page's own words are "fully specify" plus the scheme,
and it points at RFC-3986/3987 for URI syntax, but it never uses the word "absolute"
(`grep -ci 'absolute' protocol.raw` → `0`), and its one "authority" is permission language
(`protocol.raw:1183`) (S012):

> You must fully specify URLs, including the http.
> — S012, `protocol.raw:999`, section "Other Sitemap formats → Text file"

At most 50,000 URLs and at most 52,428,800 bytes (S012):

> Each text file can contain a maximum of 50,000 URLs and must be no larger than 50MB (52,428,800 bytes)
> — S012, `protocol.raw:1001-1003`, section "Other Sitemap formats → Text file"

UTF-8 (S012):

> The text file must use UTF-8 encoding.
> — S012, `protocol.raw:1007`, section "Other Sitemap formats → Text file"

No other information, no header, no footer (S012):

> The text file should contain no information other than the list of URLs.
> — S012, `protocol.raw:1013`, section "Other Sitemap formats → Text file"

> The text file should contain no header or footer information.
> — S012, `protocol.raw:1015`, section "Other Sitemap formats → Text file"

The text file may itself be gzipped, and its name is free (S012):

> you may compress your Sitemap text file using gzip
> — S012, `protocol.raw:1017-1018`, section "Other Sitemap formats → Text file"

> You can name the text file anything you wish.
> — S012, `protocol.raw:1021`, section "Other Sitemap formats → Text file"

## Syndication: RSS 2.0 and Atom 1.0

A feed may serve as a sitemap (S012):

> You can provide an RSS (Real Simple Syndication) 2.0 or Atom 0.3 or 1.0 feed.
> — S012, `protocol.raw:957`, section "Other Sitemap formats → Syndication feed"

For both families the URL is the link field (S012):

> `<link>` field - indicates the URL
> — S012, `protocol.raw:975`, section "Other Sitemap formats → Syndication feed"

and the modified date is `<pubDate>` for RSS and `<updated>` for Atom (S012):

> the `<pubDate>` field for RSS feeds and the `<updated>` date for Atom feeds
> — S012, `protocol.raw:977-979`, section "Other Sitemap formats → Syndication feed"

That date field is optional (S012):

> Use of the modified date field is optional.
> — S012, `protocol.raw:979-981`, section "Other Sitemap formats → Syndication feed"

RSS 2.0 therefore reads `<link>` text for the URL and `<pubDate>` for the date (S012). For Atom the page
names only the `<link>` field; the URL is the `href` attribute RFC 4287 requires on that element (S012,
S448):

> The "href" attribute contains the link's IRI. atom:link elements MUST have an href attribute
> — S448, `rfc4287.raw:1159-1161`, §4.2.7.1 "The "href" Attribute"

and its date is `<updated>`, the element an entry's or feed's modification time is carried by (S012, S448):

> The "atom:updated" element is a Date construct indicating the most recent instant in time when an entry or feed was modified
> — S448, `rfc4287.raw:1385-1388`, §4.2.15 "The "atom:updated" Element"

## The sitemap-index `<loc>` is container-agnostic

The index carries a sitemap's limits (S012):

> Sitemap index files may not list more than 50,000 Sitemaps and must be no larger than 50MB (52,428,800 bytes)
> — S012, `protocol.raw:703-705`, section "Using Sitemap index files (to group multiple sitemap files)"

Its `<loc>` may point at any of the protocol's containers, not only at XML (S012):

> This location can be a Sitemap, an Atom file, RSS file or a simple text file.
> — S012, `protocol.raw:885`, section "XML tag definitions → `sitemapindex` → `<loc>`"

So an index audit reads each `<loc>` as a URL, and the target's own bytes decide which container it is;
this entry draws no further distinction (S012). The page does bound the index by site (S012):

> A Sitemap index file can only specify Sitemaps that are found on the same site as the Sitemap index file.
> — S012, `protocol.raw:739-743`, section "Using Sitemap index files (to group multiple sitemap files)"

## Limits

- **No fetch.** No sitemap, feed or index was fetched or read for this entry, and no container audit was run;
  the one network read behind it is the public GET of the protocol page recorded in `verified-at`, and the
  two RFC bytes are the retained copies named in `source:` (S012, S447, S448).
- **No engine acceptance.** The page states no search engine's acceptance, parsing or rejection of these
  formats — `grep -ci 'Google' protocol.raw` → `0`, `grep -ci 'Bing' protocol.raw` → `0`,
  `grep -ci 'accept' protocol.raw` → `0` — and this entry adds none (S012).
- **No robots `Sitemap:` cross-submission.** The page does describe specifying a sitemap location in a
  robots.txt file and a sitemap on another host reached through it (`protocol.raw:1185-1209`,
  `protocol.raw:1401-1429`), but this entry claims nothing about that route: not its syntax, not its
  effect, not any interaction with the rules above (S012).
- **No compression ratio or server behaviour.** The retained gzip specification states no compression
  ratio (`grep -ci 'compression ratio' rfc1952.raw` → `0`) and no `Content-Encoding`
  (`grep -ci 'Content-Encoding' rfc1952.raw` → `0`); nothing here says how a server or CDN stores,
  re-compresses or transfers the file (S447).
- **No owned property.** No lane site, sitemap or host was fetched or measured; every sentence above is
  about the protocol page and the two RFCs, not about ds4cc.com, the kimi mirrors or the Pages hosts
  (S012).
- **No error taxonomy.** The page states no exit code or error class (`grep -ci 'exit code' protocol.raw`
  → `0`); an audit's `format_unsupported` class is a lane construct, not a protocol rule (S012).
- **No BOM rule.** The page contains no byte-order-mark sentence (`grep -ci 'BOM' protocol.raw` → `0`); a
  BOM-prefixed first URL being read clean is a lane tolerance, not a sourced rule (S012).
- **Modality is not uniform.** One-URL-per-line, full specification, the 50,000/52,428,800-byte limits
  and UTF-8 are stated with `must`; "no information other than the list" and "no header or footer" are
  stated with `should` (S012).
- **Registry ids.** `corpus/SOURCES.md` held no S447 or S448 row when this entry was written
  (`grep -c 'S447\|S448' corpus/SOURCES.md` → `0` over 300 lines), and its S012 row is scoped to sitemap
  location while line 110 records S102 as superseding S012 for the same page's broader structure and
  limits. The ids used here are the three the round's frozen contract names; the L1 assigns the final
  registry ids (S012, S447, S448).

## Feed-date grammar (lane policy, round 77)

S012 names the feed date fields but states no syntax for them (S012, "Other Sitemap formats": the
`<pubDate>`/`<updated>` sentence says only that the field is optional and indicates when the URL was last
modified). The audit therefore accepts a feed date in either form as **lane policy**, not as a sourced
rule: an ISO-8601 date-time by the sitemap `<lastmod>` rule, or an RFC 822 date read by Python's
`email.utils.parsedate_to_datetime`; a value neither form accepts is reported `lastmod_invalid`
(amendment 1, A4).

Two edges of that policy are stated here rather than left implicit. First, **RFC 822 acceptance is
unpinned by the round's matrix**: the clean cases r01/a01 carry ISO-shaped dates, so a tool that accepted
only ISO would pass them; the delivered selftest's `r77_rss_rfc822_pubdate` is the only case that
decides the RFC 822 branch. Second, S448 §4.2.6 requires `atom:updated` to be an RFC 3339 **date-time**,
while the audit reuses the sitemap rule, which accepts a date-only value; that is a recorded deviation
from S448, not an S448 reading (S448).
