# ScoutReopenS273

Axes: operability, freshness.

Result: HTTP 200, body 74323 bytes. The S273 gate quote is **not** an exact substring of the fetched body. It **is** a substring after collapsing whitespace. Article markup outside `script`/`style` matches the committed raw bytes. The fetched body was not written into the lane repo.

## Gate quote tested

From `git show 1c846ed2d67b1692ea966be064f0fc04542763c6:corpus/lessons/round-49.md`, the S273 `## Gate` span (21 whitespace tokens):

`Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit.`

Apostrophes in that span are U+0027. The same code points appear in the live body. No HTML entity and no U+2019 variant of the quote is present.

## Fetch

Command (body and headers under `/tmp`, outside the lane):

```text
mkdir -p /tmp/kake-r49-scout-s273 && curl -sS -L --max-time 90 -D /tmp/kake-r49-scout-s273/hdr -o /tmp/kake-r49-scout-s273/body -A 'kake-shokunin-r49-scout/1.0' -w 'http_code=%{http_code}\nsize_download=%{size_download}\ncontent_type=%{content_type}\nurl_effective=%{url_effective}\nnum_redirects=%{num_redirects}\nredirect_url=%{redirect_url}\n' 'https://developers.google.com/crawling/docs/crawl-budget'
```

Exit 0. Local clock at the follow-up check: `2026-10-24T21:37:31-03:00`.

```text
http_code=200
size_download=74323
content_type=text/html; charset=utf-8
url_effective=https://developers.google.com/crawling/docs/crawl-budget
num_redirects=0
redirect_url=
```

Response header fields kept:

```text
HTTP/2 200
last-modified: Wed, 22 Jul 2026 18:28:48 GMT
content-type: text/html; charset=utf-8
date: Sun, 25 Oct 2026 00:36:47 GMT
server: Google Frontend
content-length: 74323
```

Byte size, three ways, all 74323: `size_download`, `content-length`, and `wc -c /tmp/kake-r49-scout-s273/body`.

Live body sha256: `d7a6def4621020ffab7d3189f33d145b83bced19c93d3eb007e9396e105bdcdf`.

## Substring

| Check | Result |
| --- | --- |
| Exact substring of the raw fetched body | no |
| Same quote with only U+2019, `&#39;`, `&apos;`, or `&#x27;` apostrophes | no |
| `html.unescape` then exact substring | no |
| Whitespace collapsed (`\s+` → one space) then exact substring | yes |
| Quote tokens in order, only whitespace between them | yes |

The matching raw span is 154 characters, not 134. It is the quote with two line breaks and indentation, and no tags inside the span:

```text
Google\n          won't shift this newly available crawl budget to other pages unless Google is already\n          hitting your site's crawl capacity limit.
```

Collapsing that span's whitespace reproduces the gate quote exactly. An exact-substring check against the HTML body false-fails; the page prose has not dropped the sentence.

## Freshness against the committed raw

`git show 1c846ed2d67b1692ea966be064f0fc04542763c6:.ufo/waves/round-49/sources/S273.raw.html` is also 74323 bytes, sha256 `424672252aad9f2d6f59adb23186d5dad38d1011bf0074aa98ff5d1ebc5ff70e`. Live bytes are not equal to that blob.

`last-modified` is the same value already stored in `.ufo/waves/round-49/sources/S273.hdr` (`Wed, 22 Jul 2026 18:28:48 GMT`). Response `date` moved from that file's `Sun, 25 Oct 2026 00:28:54 GMT` to `Sun, 25 Oct 2026 00:36:47 GMT`.

Line diff of committed raw vs this fetch: 3 replaced lines, same lengths. Deltas are inside `script` (analytics dimension key order, a per-response `nonce`, and a feature-flag list). After removing `script` and `style` elements, both documents hash to `774ab4afbdc365bffcb38ee539d04f4d530e3163b7d5e2cc11c43c95484c752d`. Same `content-length` is not the same bytes, but the article markup did not change.

Files written: `.ufo/waves/round-49/w1/ScoutReopenS273.md`. No other lane path written. Fetched body left at `/tmp/kake-r49-scout-s273/body`.
