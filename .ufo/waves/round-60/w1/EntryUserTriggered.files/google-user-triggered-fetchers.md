source: S428 — Google Crawling Infrastructure — Google User-Triggered Fetchers — https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers — § List of Google user-triggered fetchers (Last updated 2026-08-19 UTC) — article `<h1>`; no `<h2>` precedes the robots sentence
verified-at: 2026-10-27 (retained body sha256 0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2, 76197 bytes)
recheck: 180d — `curl -fsSL --compressed 'https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers' | grep -F -c 'these fetchers generally ignore robots.txt rules'` -> 1 (grep against the retained body 1, 2026-10-27)
ground: per-engine crawl hygiene — whether a fetch a person asked for is governed by robots.txt, and which signals remain for the publisher

# User-triggered fetchers generally ignore robots.txt, and the page identifies them by IP range and reverse DNS

The page's `<title>` begins Google User-Triggered Fetchers (the element continues with ` | `-separated site
suffixes), the on-page heading prints the same words in sentence case, and the printed revision reads
`Last updated 2026-08-19 UTC` inside `<devsite-content-footer` [S428]. Nine `<h2>` sections follow — Chrome
Web Store, Feedfetcher, Gemini Notebook, Google-Agent, Google Messages, Google Pinpoint, Google Publisher
Center, Google Read Aloud, Google Site Verifier — one per fetcher. The robots sentence is in the intro,
directly under the `<h1>` and above the first `<h2>`: no `<h2>` holds it [S428].

## What the page calls a user-triggered fetcher

> "User-triggered fetchers are initiated by users to perform a fetching function within a Google product."

and the example it gives is a product that [S428]:

> "acts on a user's request, or a site hosted on Google Cloud (GCP)"

— the sentence continues with a site on Google Cloud whose users retrieve an external RSS feed. The page
then says the fetchers' general technical properties are the ones it documents for Google's crawlers, and
points to its published range objects for the addresses [S428] (that sentence is split across link elements,
so it is carried here as the lane's reading rather than quoted).

## The robots.txt posture, in the page's words

> "Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules."

The word is `generally`. The page does not name a fetcher that does respect robots.txt, and it does not say
what the exception covers [S428]. This intro sentence is the page's whole robots.txt statement: none of the
nine per-fetcher `<h2>` sections repeats or qualifies it [S428].

## How a publisher can still identify these fetchers

Addresses first — the page names three range objects [S428]:

> "The IP ranges the user-triggered fetchers use are published in the"

`user-triggered-fetchers.json`, `user-triggered-fetchers-google.json`, and `user-triggered-agents.json`
(each token is one unit, below this entry's six-unit quotation floor, so they are named in backticks).

Then reverse DNS, split by who owns the fetcher [S428]:

> "The user-triggered fetchers' reverse DNS mask, depending on whether the fetcher is Google or user owned, matches"

`***-***-***-***.gae.googleusercontent.com` on the user-owned side and
`google-proxy-***-***-***-***.google.com` on the Google side, in that order [S428]. For Google-Agent the
page says, and names its own range object [S428]:

> "Google-Agent is used by agents hosted on Google infrastructure to navigate the web and perform actions upon user request. It uses IP ranges from"

`user-triggered-agents.json`. So both identifiers the page supplies are address-based — published range
objects and a reverse DNS mask — and it does not make the user-agent string an identifier. Its caution box
states that the user-agent string can be spoofed; that box sits in an `<aside>`, which the article-text-node
rule behind this entry's quotations excludes, so the statement is carried here unquoted as the lane's
reading [S428].

## The wording divergence against S426, dated

`corpus/knowledge/googlebot-verification.md` line 38 quotes the verification page (row S426, page revision
`Last updated 2026-03-20 UTC`) as printing, in its user-triggered cell, `these fetchers ignore robots.txt
rules.` This page, at revision `Last updated 2026-08-19 UTC`, prints:

> "these fetchers generally ignore robots.txt rules"

Same subject, same verb, with `generally` inserted, on two documents of the same documentation set five
months apart [S426][S428]. The framing clause before it moves too: the S426 cell reads
`acts on the request of a user`, the S428 intro `acts on a user's request`. The lane records both
differences with both revision dates and does not decide which wording governs a given request. (The S426
words are carried in backticks because each double-quoted span in this entry is checked against this entry's
own row body, S428, and the S426 words are not in it.)

## What this entry does not establish

- **No exception set.** Nothing on the page names a user-triggered fetcher that respects robots.txt, or the
  case in which the `generally` fails [S428].
- **No per-fetcher posture.** The nine sections print a user-agent string and an associated product each;
  not one of them carries a robots.txt clause [S428].
- **No verification procedure.** The page links to its verification page and to Web Bot Auth; it does not
  spell out the reverse-DNS-then-forward-DNS test in its own text [S428].
- **No claim that S426 is wrong or retracted.** The divergence is dated; the lane holds both quotes and
  attributes each to its page and revision.
- **No completeness claim about the list.** The page says so itself [S428]:

  > "The list is not exhaustive, it only covers the requestors"

  and this entry does not add one.
- **Nothing about other vendors.** No statement here bounds fetchers that are not Google's.

[S428] .ufo/waves/round-60/sources/S428.html (HTTP 200, 2026-10-27T04:03:37+00:00, user agent tagged
`round60`; receipt .ufo/waves/round-60/sources/receipts.json). [S426] row S426, retained body
.ufo/waves/round-59/sources/S426.html.
