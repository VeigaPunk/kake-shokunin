# Wave-2 report: ReopenSourcesRejected

Item: re-open the rejected (S071, S072, S074, S075) and queued (S076, S077) sources and test each rejection/queue reason against a fresh ordinary GET on 2026-10-22.

Method: one `curl -sS -L --compressed` GET per receipts.json `url`, browser-like UA/Accept headers, no cookies, no JS, in /fast/scratch/hyaku/kake-r34/w2/ReopenSourcesRejected (fetch.sh + got/ artifacts retained there). Extracted text per the declared rule (script/style/comments/tags removed, entities decoded, whitespace collapsed) — my Python extractor is not byte-identical to the retained fetcher's (sha differs), but it is applied identically to fresh and retained bodies, and it produced equal text and equal word counts for every source.

| Src | URL requested | Status / final URL | Fresh vs retained body | Fresh vs retained visible text | Reason holds? |
|-----|---------------|--------------------|------------------------|--------------------------------|---------------|
| S071 | developer.x.com/en/docs/x-for-websites/cards/overview/markup | 200, 2 redirects → https://docs.x.com/overview | identical (622,081 B, sha aa5753ce…) | identical, 394 words | YES |
| S072 | docs.github.com …/customizing-your-repositorys-social-media-preview | 200, same URL | differs (sha c990fcbe → e69427ea), same 197,853 B | identical, 741 words | YES |
| S074 | core.telegram.org/bots/api | 200, same URL | differs (099bc4f9 → da9dd940), same 860,230 B | identical, 73,876 words | YES |
| S075 | linkedin.com/post-inspector/ | 200, same URL | identical (3,577 B, sha 2426c99b…) | identical, 2 words: "Post Inspector" | YES |
| S076 | oembed.com/ | 200, same URL | identical (24,634 B, sha fb181e66…) | identical, 2,030 words | YES (queued) |
| S077 | github.com/jekyll/jekyll-seo-tag | 200, same URL | differs (bfb28de0 → b7d92e90), same 279,797 B | identical, 750 words | YES (queued) |

Details per reason, from fresh bytes:

- S071 rejection: the markup path still 301→302-redirects to docs.x.com/overview (generic docs index). Fresh text has zero `og:` and zero `meta` mentions; the single `card` occurrence is the payment sentence "saving a first payment card". The page's own head does carry generic docs.x.com og: tags (og:title/og:description/og:url/og:image/og:type) — these document the docs site itself, unchanged from retained, and ground no cards-markup rule. Reason holds.
- S072 rejection: fresh visible text still documents only Settings > Social preview image upload ("Social preview" ×1, "Settings" ×3); zero `og:`, `meta`, "open graph" in text. The five `og:` hits in raw HTML are GitHub Docs' own head meta (og:site_name/title/type/url/image). Reason holds.
- S074 rejection: fresh text = the 73,876-word Bot API reference; zero `og:`/`meta`/`property` in text. Raw HTML `og:` ×3 are the page's own head meta (og:title "Telegram Bot API", og:image, og:description — present identically in retained bytes), and `property=` ×4 includes a stray `<meta property="description">`. None documents which page tags Telegram's preview reads. Reason holds.
- S075 rejection: byte-identical 3,577-B JS shell; whole visible text is still exactly "Post Inspector" (2 words). Head carries `<meta name="og:title" content="Post Inspector">` (name=, not property=) — same as retained, no preview rule obtainable by plain GET. Reason holds.
- S076 queue note: fresh text still gives the oEmbed provider-endpoint/discovery/response format (oEmbed ×25, provider ×38, endpoint ×12, discover ×2); still a mechanism separate from page meta tags. Nothing changed to make it mined on its own; queued status stands.
- S077 queue note: README still lists "Open Graph title, description, site title, and URL (for Facebook, LinkedIn, etc.)" and "Twitter Summary Card metadata" under "What it does". Text identical to retained; queued status stands.

Net: all four rejections and both queue rulings still hold on 2026-10-22 bytes; no flip condition met (S071 did not serve markup docs; no Telegram primary tag page surfaced — out of scope; S075 still a 2-word shell). Byte diffs on S072/S074/S077 are confined to script/style/attribute noise — tag-stripped visible text is character-identical.

Not verified: I did not probe alternate UA/no-UA GETs (item allowed one GET each), did not fetch LinkedIn help alternates, and my extractor is not the pinned fetcher (sha eaf370…/a36758b…) — word-count parity is on my own pipeline, consistent across fresh and retained.

Tools installed/updated: none; used preinstalled curl 8.23.0 and Python 3 (stdlib only).

Artifacts: /fast/scratch/hyaku/kake-r34/w2/ReopenSourcesRejected/{fetch.sh,got/*.{body,headers,meta,err,txt}}

Evidence pointers: got/*.meta (status, final URL, redirect count); got/*.body sha256 vs .ufo/waves/round-34/sources/receipts.json; corpus/SOURCES.md:79-85 (reasons tested).
