source: S273 — https://developers.google.com/crawling/docs/crawl-budget
source: S274 — https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate
verified-at: 2026-10-24
recheck: 180d
ground: per-host crawl hygiene — budget consequence of robots and status codes

# Robots blocking does not free crawl budget

The lane's held robots rows stop at what a directive means. They do not say what blocking costs. Two Google documents opened this round, and only these two sentences are admitted.

Google's crawl-budget page says a block does not hand the spared fetches to other pages: Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit (S273).

Google's emergency crawl-rate page says the backoff reduces your site's crawl rate across the whole hostname (S274). The checked S274 quote does not itself name the status codes that trigger that backoff. Those words sit in the same retained paragraph and are not the admitted quote.

## What this entry does not establish

No lane property was fetched or measured. Search Console crawl stats stay operator-gated. Publishing stays operator-owned. Bing and Baidu budget models are not claimed.
