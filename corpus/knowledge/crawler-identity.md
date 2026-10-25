source: S263 — https://developers.google.com/search/docs/crawling-indexing/googlebot — § "Googlebot is the generic name for two types of web crawlers used by Google Search" (doc rev. Last updated 2026-02-03 UTC) — fetched 2026-10-24
verified-at: 2026-10-24
recheck: 180d
ground: per-host crawl hygiene — knowing which crawler is on the wire before interpreting a crawl log

# "Googlebot" is a family name, not one crawler

Google's crawler documentation states [S263], quoted raw from the page:

> "Googlebot is the generic name for two types of"

and names the two types beneath it [S263] (collapsed-only quotes; the source puts a space
before the colon and breaks the lines):

> "Googlebot Smartphone : a mobile crawler that simulates a user on a mobile device"

> "Googlebot Desktop : a desktop crawler that simulates a user on desktop"

The page says how the two are told apart [S263] (collapsed-only quote):

> "You can identify the subtype of Googlebot by looking at the HTTP user-agent request
> header in the request"

and states the consequence for robots.txt [S263] (collapsed-only quote):

> "both crawler types obey the same product token (user agent token) in robots.txt"

## Why the lane needs this as a rule rather than trivia

- **A user-agent string is the only thing a server log records about the crawler.** Two
  crawlers share the name "Googlebot", so a log line saying "Googlebot" does not say whether
  the fetch was the mobile or the desktop variant, and therefore does not say which viewport
  the fetched HTML was produced for.
- **The same page can be crawled twice by the same engine under two names.** For a publisher
  running per-device checks, a "crawled" conclusion drawn from a bare "Googlebot" is
  ambiguous in the same way a canonical conclusion drawn from a declared element is
  ambiguous.
- **The robots product token does not separate them.** The page says both types obey the same
  product token, so a robots.txt rule cannot target one subtype — a fact the lane's own
  robots reading (S011) and Google's robots interpretation (S095) do not answer.
- **The registry's Googlebot-adjacent row is about the parser, not the crawler.** S096 holds
  Google's released `robotstxt` matcher library, which answers "how is the rule evaluated",
  not "who is the agent". This row answers the second question.

## What this entry does not establish

- It does not establish Google's crawl rate, its scheduling, or its treatment of any
  particular URL.
- It does not enumerate the non-Google bots Google operates; the page lists them, and the
  lane has no use for that list beyond identity.
- It does not establish anything about how a specific crawler identifies itself on a specific
  lane property: no operator-owned property was fetched this round.
- The page's own revision line ("Last updated 2026-02-03 UTC") was read from the retained
  body this round; the entry is a documentation reading, not a live observation.
