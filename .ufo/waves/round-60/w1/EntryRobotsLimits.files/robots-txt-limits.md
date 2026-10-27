source: S429 — https://developers.google.com/search/docs/crawling-indexing/robots/intro — § Understand the limitations of a robots.txt file (Last updated 2025-12-10 UTC) — fetched 2026-10-27
verified-at: 2026-10-27
recheck: 180d — `curl -fsSL --compressed 'https://developers.google.com/search/docs/crawling-indexing/robots/intro' | grep -F -c 'Different crawlers interpret syntax differently.'` -> 1 (grep against the retained body 1, 2026-10-27)
ground: per-host crawl hygiene — the engine's own statement of what a robots.txt cannot do, held beside the RFC 9309 reading and the operator-specific Yahoo! JAPAN rules this lane already keeps

# A robots.txt states a preference a crawler may ignore, and a disallowed URL can still be indexed

The page's browser title is Robots.txt Introduction and Guide, its `<h1>` reads Introduction to
robots.txt (page chrome, not the title), and its revision line, Last updated 2025-12-10 UTC, sits
inside the page footer (after the article block) rather than in it [S429]. The article block carries three
`<h2>`s — What is a robots.txt file used for?, Understand the limitations of a robots.txt file,
and Create or update a robots.txt file — and the second is the section this entry is grounded on
[S429].

## What this page adds to what the lane held

The lane already held the RFC 9309 reading of the file: a crawler-access convention, not
authorization, and a disallow rule that secures nothing. That was carried with the file-location,
line/group and path-matching rules and with Google's own parser note (`corpus/knowledge/robots-txt-rules.md`,
S011 §§1, 3, S095, S096), and the identity signal lives in `corpus/knowledge/crawler-identity.md`
(both crawler types obey the same product token). None of that is repeated here.

This page adds four points, each quoted below at its source:

1. the file cannot enforce obedience — it is up to the crawler to obey;
2. crawlers interpret the syntax differently, and some do not understand every instruction;
3. a disallowed URL can still be indexed when other pages link to it;
4. the warning not to use the file to keep a page out of the index.

The page states the purpose in one sentence [S429]:

> "A robots.txt file tells search engine crawlers which URLs the crawler can access on your site."

## Limits: the file is a request, not a mechanism

Under the section heading Understand the limitations of a robots.txt file the page sets the frame
before it states any limit [S429]:

> "Before you create or edit a robots.txt file, you should know the limits of this URL blocking method"

and its first limit is cooperation between engines, not syntax [S429]:

> "robots.txt rules may not be supported by all search engines."

The enforcement limit is stated outright, and this is the sentence the entry is named for [S429]:

> "The instructions in robots.txt files cannot enforce crawler behavior to your site"

with the reason in the next clause [S429]:

> "it's up to the crawler to obey them"

The page then locates obedience in the crawler rather than in the file, and does not claim it for
crawlers in general [S429]:

> "While Googlebot and other respectable web crawlers obey the instructions in a robots.txt file, other crawlers might not"

Its remedy for content that must stay private is a different mechanism, not a stricter rule [S429]:

> "password-protecting private files on your server"

The syntax limit is a second, separate paragraph — the same file can be read two ways [S429]:

> "Although respectable web crawlers follow the rules in a robots.txt file, each crawler might interpret the rules differently"

and the page does not enumerate which instructions are the ambiguous ones [S429]:

> "some might not understand certain instructions"

## A disallowed URL can still be indexed

Here the page separates the crawl from the index [S429]:

> "A page that's disallowed in robots.txt can still be indexed if linked to from other sites."

and the page says how the URL can still surface [S429]:

> "we might still find and index a disallowed URL if it is linked from other places on the web"

so the result can print the address, and possibly anchor text from the linking pages, without a
description [S429]:

> "its URL can still appear in search results, but the search result"

The same table warns that blocking a URL does not detach its media from the rest of the web [S429]:

> "This won't prevent other pages or users from linking to your image, video, or audio file."

## The warning against using the file to hide a page

The opening section states the purpose negatively, which is the warning the staged material
dropped [S429]:

> "it is not a mechanism for keeping a web page out of Google"

and it sends a publisher who wants the page gone to another method [S429]:

> "If you want to hide the page completely from Search"

— the page points to password protection of the files, to a `noindex` meta tag or response header,
or to removing the page entirely, and links those rules out instead of restating them here [S429].

## What the page does not state

- It names one operator's crawler, Googlebot, and speaks otherwise of respectable web crawlers
  without defining the set; it says nothing about Baidu, Yahoo! JAPAN or any other operator, and it
  gives no count of operators that obey.
- It does not list the syntax differences it warns about, and it names no field, prefix or
  wildcard rule — those readings belong to the other entries the lane holds.
- It does not say how a crawler treats a robots.txt it cannot fetch, and it does not compare the
  block with an index directive beyond recommending the latter.
