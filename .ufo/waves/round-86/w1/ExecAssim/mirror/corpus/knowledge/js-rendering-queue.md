source: S137 — https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics — § "How Google processes JavaScript" → "Crawling" / "Rendering" (doc rev. Last updated 2026-03-04 UTC) — opened 2026-10-24; S138 — https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=zh-cn — §「Google 如何处理 JavaScript」→「渲染」(doc rev. 最后更新时间 (UTC)：2026-03-05) — opened 2026-10-24; S139 — https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=ja — §「Google が JavaScript を処理する仕組み」→「レンダリング」(doc rev. 最終更新日 2026-03-05) — opened 2026-10-24
verified-at: 2026-10-24
recheck: 180d — `curl -fsSL --compressed 'https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics' | grep -F -c 'sent to the rendering queue'` -> 1; locale editions with `grep -c '渲染队列'` -> 3 and `grep -c 'レンダリング キュー'` -> 2 (re-run 2026-10-24)
ground: publisher-side crawl hygiene — the crawl/render/index phase contract and the queue rule that feeds it (PROVINCE.md, Frontier: "canonical signals and JS rendering" open)

# The render queue is a status-code rule, not a JavaScript rule

Google processes a JavaScript web app in three phases — crawling, rendering,
indexing — and the phase boundary that binds a publisher is the queue rule,
because the rule is written in terms of the HTTP status code rather than the
presence of script (S137, § "Rendering"):

> All pages with a 200 HTTP status code are sent to the rendering queue, no
> matter whether JavaScript is present on the page.

The same section states the two consequences that follow from that sentence:

> If the HTTP status code is non- 200 (for example, on error pages with 404
> status code), rendering might be skipped.

> The page may stay on this queue for a few seconds, but it can take longer
> than that. Once Google's resources allow, a headless Chromium renders the
> page and executes the JavaScript.

So rendering is a deferred second pass over the same URL, not a second URL
space, and a non-200 response can drop a page out of the pipeline entirely.

The crawl phase fixes the other boundary, and it sits *before* the fetch
(S137, § "Crawling"):

> When Googlebot fetches a URL from the crawling queue by making an HTTP
> request, it first checks if you allow crawling. Googlebot reads the
> robots.txt file.

> If it marks the URL as disallowed, then Googlebot skips making an HTTP
> request to this URL and skips the URL. Google Search won't render JavaScript
> from blocked files or on blocked pages.

A publisher reading that order gets four rules:

1. **A `noindex` on a robots-disallowed URL is never seen.** The directive
   lives on a page the crawler never requests, so disallowing a URL does not
   de-index it — it makes it invisible, which is a different outcome.
2. **Blocking a page removes its rendered links from the discovery graph.** A
   link that exists only in the rendered DOM of a disallowed page is never
   reached, because the rendered pass never runs.
3. **An error page can be a dead end for discovery as well as for the user.**
   A 404 response may skip rendering, so a link pointing at it cannot be
   discovered through the rendered DOM.
4. **Server-side or pre-rendering stays worth doing.** The same section says
   the page may sit on the queue for a while and that not all bots run
   JavaScript, so the first fetch is what users and non-rendering agents see.

## Locale editions

The Simplified-Chinese edition states the same rule in that language, and the
Japanese edition states it in Japanese; both are separately versioned
(2026-03-05 against the English 2026-03-04).

> 所有具有 200 HTTP 状态代码的网页都会发送到渲染队列，无论网页上是否存在
> JavaScript。 (S138)

> 200 HTTP ステータス コードのすべてのページは、ページに JavaScript が存在するかどうかに
> 関係なく、レンダリング キューに送信されます。 (S139)

They are locale evidence for a publisher working in those languages; they carry
no additional rule and they are not a substitute for reading the documentation
of another engine, which states different rules.

## Boundary

This entry holds the *queueing contract* for one engine. It does not say which
canonical Google selects among duplicates — a declared canonical is a hint and
the selection is the engine's decision, which the lane's own static preflight
(`corpus/knowledge/static-canonical-preflight.md`) deliberately does not claim —
and it says nothing about any other engine. Browser execution and client-side
crawler discipline belong to `tabi` (PROVINCE.md, Adjacent); kake's side is the
publisher's placement and status codes.
