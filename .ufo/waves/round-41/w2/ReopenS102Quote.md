# ReopenS102Quote — S102 quote vs live protocol.html

Axis: freshness. No tools installed. HEAD and the named build are both `eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6`; `corpus/SOURCES.md` is clean.

## Commands (exit codes)

1. `prlimit --as=4000000000 timeout 60 curl -fsSL -D headers.txt -o protocol.html -A 'kake-r41w2-reopen/1.0' --max-time 45 https://www.sitemaps.org/protocol.html` — exit 0. HTTP 200, `Content-Length: 45292`, `Content-Type: text/html`, `Date: Fri, 23 Oct 2026 10:08:31 GMT`, `Last-Modified: Thu, 15 Dec 2022 10:54:02 GMT`. Copy: `/fast/scratch/hyaku/kake-r41w2/ReopenS102Quote/protocol.html`.
2. `sha256sum` of that file — `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654`, 45292 bytes, 1534 CRLF lines.
3. Tag-strip + entity unescape + whitespace collapse (Python `re`/`html`, same bytes) — exact sentence count 1, at collapsed offset 4796.
4. `git show eae5ae2c:corpus/SOURCES.md` — S102 is line 110; pin sha, URL, "Last Updated: Monday, November 21, 2016", and `fetched 2026-10-23T05:28:42Z` are on that line.

## Located text

Stripped (one space between tokens; anchors removed, no space invented before the period):

> Please check to make sure that your URLs follow the RFC-3986 standard for URIs, the RFC-3987 standard for IRIs, and the XML standard.

Source spans `protocol.html:569-575` (the `<a>` tags split `RFC-3986`, `RFC-3987`, and `XML standard`; the period sits immediately after `</a>`). Same bytes as `.ufo/waves/round-39/sources/sitemaps-protocol.html` and `.ufo/waves/round-40/sources/sitemaps-protocol.html` (both sha-equal, 45292 bytes). Page line 1511 still reads "Last Updated: Monday, November 21, 2016".

A second, shorter hit at `protocol.html:1021-1027` (text-file bullet) stops at "for IRIs" and has no "and the XML standard" and no period. The SCORECARD sentence is the first hit only (`SCORECARD.md:2684-2685`).

## Statements

- The round's S102 quote is on the live page's stripped text — **holds** (exact, once).
- Live page sha256 equals S102's retained HTML SHA256 (`corpus/SOURCES.md:110`) — **holds**. Unchanged since the 2026-10-23T05:28:42Z pin and since `Last-Modified` 2022-12-15.

No overstated or wrong finding on the quote or the pin. Not checked: whether that sentence licenses the RFC 3986 `URI` grammar the tool applies.
