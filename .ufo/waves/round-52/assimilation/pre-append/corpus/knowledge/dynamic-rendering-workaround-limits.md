source: S249 — https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering — § "Dynamic rendering is a workaround" / "Dynamic rendering is not cloaking" (no revision printed on the page — pinned by the quoted clauses and the access date) — opened 2026-10-24
verified-at: 2026-10-24
recheck: 180d — `curl -fsSL --compressed 'https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering' | grep -F -c 'Dynamic rendering is a workaround and not a recommended solution, because it creates additional complexities and resource requirements.'` -> 1 (re-run 2026-10-24)
ground: publisher-side crawl hygiene — the vendor's own account of rendering as a technique, and the condition that separates it from cloaking (PROVINCE.md, Frontier: "canonical signals and JS rendering" open)

# Rendering is a workaround, and the line that separates it from cloaking is content, not technique

The lane holds this operator's JavaScript SEO basics
(`corpus/knowledge/js-rendering-queue.md`), which describe the crawl, render
and index phases and the queue that feeds them. This page states the other
half — when rendering is a sensible answer, and where it stops being one.

The framing is blunt (S249, § "Dynamic rendering as a workaround"):

> Dynamic rendering is a workaround and not a recommended solution, because it
> creates additional complexities and resource requirements.

The mechanism it describes is the one a publisher reaches for under pressure:
a rendering server detects the crawler and serves it a server-rendered version
without JavaScript, while users get the client-rendered version.

> A dynamic rendering server detects bots that may have problems with
> JavaScript-generated content and serves a server-rendered version without
> JavaScript to these bots while showing the client-side rendered version of
> the content to users.

And the cloaking boundary is a content condition, not a technique condition
(S249, § "Dynamic rendering is not cloaking"):

> As long as your dynamic rendering produces similar content, Googlebot won't
> view dynamic rendering as cloaking.

> Using dynamic rendering to serve completely different content to users and
> crawlers can be considered cloaking.

So the decision a publisher faces is a content-equality question — does the
version the crawler sees say the same thing as the version the user sees — and
not a question about which mechanism served it. The same section also notes
that the error pages a dynamic-rendering setup can produce are not treated as
cloaking, but are treated as any other error page: they inherit the status
code rule of `corpus/knowledge/js-rendering-queue.md`, where a non-200
response may skip the rendering pass entirely.

## Boundary

This entry holds one engine's own account of a technique; it is not a
recommendation and it is not a gate. Nothing here was observed on a live
crawl: no crawler was run, no owned property was fetched, and the page's
statements are the vendor's, not this lane's measurement. A different engine's
rule on dynamic rendering is not held by the lane and is not implied by this
entry.
