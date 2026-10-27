source: S263 — https://developers.google.com/search/docs/crawling-indexing/googlebot — § "Googlebot is the generic name for two types of web crawlers used by Google Search" (doc rev. Last updated 2026-02-03 UTC) — fetched 2026-10-24
verified-at: 2026-10-24
recheck: 180d
ground: per-host crawl hygiene — knowing which crawler is on the wire before interpreting a crawl log

# "Googlebot" is a family name, not one crawler

Google's crawler documentation states [S263], quoted raw from the page:

> "Googlebot is the generic name for two types of"

and names the two types beneath it [S263] (rendered-text quotes; the inline markup is removed
and the space before each colon is this entry's rendering, not the source's bytes — the page
closes the link element immediately before the colon; see § "Quote classes"):

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
  **[r59-correction 2026-10-27]** The claim in the bullet above is wrong as stated: a server log
  ordinarily records the requesting IP address as well as the user-agent (general access-log
  behaviour, not a statement of the overview page; the verification procedure in
  `googlebot-verification.md` starts from that logged IP), and Google's crawler overview gives
  three identification signals, not one [S425] — the HTTP user-agent request header,
  "The source IP address of the request." and "The reverse DNS hostname of the source IP." Its
  technical-properties section adds that the clients are distributed across many datacenters, so
  "your logs may show visits from several IP addresses" [S425]. What the bullet gets right
  survives: the user-agent header is what separates the Smartphone and Desktop subtypes quoted
  above, so a log line reading Googlebot still does not say which viewport the fetched HTML was
  produced for. What does not survive is the word *only* — verifying a claim to be Googlebot is a
  check on the logged IP (reverse then forward DNS, or a match against Google's published IP
  ranges), set out in `googlebot-verification.md`; the
  fuller reading of the three signals, with the datacenter spread, is
  `crawler-identity-signals.md` (S425). The sentence above stays as historical text; this
  correction supersedes it.
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

## Quote classes (round-51 correction)

Every quotation in this entry is a **rendering** of the page, not a byte slice of it: the inline
markup is removed and whitespace is collapsed. Only the first quotation, "Googlebot is the generic
name for two types of", is also an exact raw substring of the retained body (S263.html, sha256
`6afbdc82…`), and that is the string the round-51 lesson Gate pins.

Two claims this entry previously made are corrected here. (1) The parenthetical that called the
two subtype quotations "collapsed-only" and said "the source puts a space before the colon" was
false: the page closes the link element immediately before the colon (`</b></a>:`), so the space is
this entry's rendering. (2) The label "collapsed-only" was wrong for the same quotations: whitespace
collapse alone does not recover them; removing inline markup does.

Measured by the round-51 wave-1 seat `ExecQuoteRawScan` over both admitted entries: of 15 body
quotations, 3 are raw substrings, 2 survive whitespace collapse only, and 10 need markup removal;
7 of the 10 stay absent under the rendered-text reading because of the inserted space above. None is
fabricated. Evidence: `.ufo/waves/round-51/w1/ExecQuoteRawScan.md`.
