# ScoutReopenS274 — re-open reduce-crawl-rate

Axes: operability, freshness. Milestone: Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth.

Verdict: HTTP status **200**. The S274 gate quote **is** a substring of the fetched body (once, exact bytes).

## Gate quote

Taken from `corpus/lessons/round-49.md` `## Gate`, same span rule as `c49_quote_truth.py` (`quote:\s*"([^"]+)"` on the S274 line):

`It reduces your site's crawl rate across the whole hostname`

10 whitespace tokens. Apostrophe is U+0027. UTF-8 `4974207265647563657320796f75722073697465277320637261776c2072617465206163726f7373207468652077686f6c6520686f73746e616d65`.

## Fetch

One GET, body left in scratch, not written into the lane repo.

```
date -u → 2026-10-25T00:37:16Z
curl -sS -L --http2 --max-time 60 \
  -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' \
  -H 'Accept: text/html,application/xhtml+xml' -H 'Accept-Language: en' \
  -D /tmp/kake-r49-scout-s274/headers.txt -o /tmp/kake-r49-scout-s274/body.html \
  -w 'http_code=%{http_code} size_download=%{size_download} ...' \
  https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate
```

curl exit 0. Write-out: `http_code=200` `size_download=68787` `content_type=text/html; charset=utf-8` `num_redirects=0` `redirect_url=` `url_effective=https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate` `time_total=0.710802`.

Status line: `HTTP/2 200`. `date: Sun, 25 Oct 2026 00:37:17 GMT`. `last-modified: Tue, 06 Oct 2026 14:12:29 GMT`. `content-length: 68787`. `content-type: text/html; charset=utf-8`. `x-cloud-trace-context: 69a14f52e6a636b907ac0b11fe18054b`.

Body sha256 `13b254977638defc7fb9e8cf1f3d6092160b2ab7868f52dde3c821efb2fc1e79` (68787 bytes).

## Substring

Checked against that curl body, not the retained worktree file. `quote.encode()` is in the body bytes. Decoded UTF-8 count is 1. Surrounding markup:

`<b>It reduces your site's crawl rate across the whole hostname</b> (for example,`

Article slice from `Reduce the Google crawl rate` through the character before `Last updated 2026-10-06 UTC.` is 7983 characters and equal to the same slice of `.ufo/waves/round-49/sources/S274.raw.html`. The quote sits inside that slice. Common prefix with the retained raw file is 57873 bytes, which covers the quote. Whole-body sha256 is not the retained raw sha256 `8e279027f3af89dfff82a1483854caab55c8b3cba22f01b7748036b16fa6518f` (same length; bytes diverge after that prefix, outside the article slice). `last-modified` matches retained `.ufo/waves/round-49/sources/S274.hdr`.

Not claimed: C2 pass/fail. This seat did not run `c49_quote_truth.py`.

Report: .ufo/waves/round-49/w1/ScoutReopenS274.md
