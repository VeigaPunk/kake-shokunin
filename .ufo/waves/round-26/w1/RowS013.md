# S013 — FRESHNESS recheck (round 26)

Row: `corpus/SOURCES.md:21` · tier A · kind docs · scope "Google's sitemap-location and metadata handling" · anchor "Sitemap best practices; last updated 2026-07-08 UTC" · used-by `corpus/knowledge/crawl-scope-per-host.md`.

Fetched #1: `https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap` → HTTP 200, 191341 bytes, sha256 `492e22cf…78920b`, fetched 2026-10-21T15:10:40Z, `last-modified: Wed, 08 Jul 2026 15:47:49 GMT`; text view `fetched/text/S013-1.txt` (19216 chars).

```json
{"id":"S013","verdict":"HOLD","fetchIndex":1,"quote":"unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory","anchorObserved":"Build and submit a sitemap > 'Sitemap best practices' heading, paragraph 'Sitemap file encoding and location'; footer 'Last updated 2026-07-08 UTC'","reason":"The teaches sentence is reproduced verbatim in the current page's 'Sitemap file encoding and location' paragraph, so the parent-directory scope rule is unchanged. The anchor heading is still present and the displayed update pin is still 2026-07-08 UTC (echoed by HTTP Last-Modified 2026-07-08 15:47:49 GMT), so scope (sitemap location plus metadata handling, e.g. lastmod, priority/changefreq ignored) still holds.","correction":null}
```

Caveats:
- Only one fetch/index exists for this row; no multi-URL corroboration needed for a stable docs page.
- The page still adds cross-submission via robots.txt, but that route remains site/path-scoped and does not narrow the teaches.
- Scope "metadata handling" is covered on-page by lastmod use and by Google ignoring priority/changefreq; unchanged.
- Knowledge entry quote at `corpus/knowledge/crawl-scope-per-host.md:33-35` matches the re-fetched text verbatim; no knowledge correction needed from this row.
- No tool installs or upgrades were performed.
