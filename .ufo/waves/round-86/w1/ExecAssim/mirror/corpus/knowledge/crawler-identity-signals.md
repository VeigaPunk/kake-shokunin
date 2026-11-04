source: S425 — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers — § Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC) — fetched 2026-10-27
verified-at: 2026-10-27
recheck: 180d — `curl -fsSL --compressed 'https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers' | grep -F -c 'The source IP address of the request.'` -> 1 (grep against the retained body 1, 2026-10-27)
ground: per-host crawl hygiene — what Google's own crawler overview says a server log can show about a crawler's identity, and why one crawler may appear under several IP addresses

# Google's crawlers name three identity signals, and the page says logs may show several source IPs

The operator's crawler overview (printed `Last updated 2026-06-12 UTC`, the date carried in the row
anchor) closes its body with a section headed `Verify Google's crawlers and fetchers`, which opens
with a count and a three-item list [S425]:

> "Google's crawlers identify themselves in three ways:"

## The three signals

The first item is written with a code-labelled token inside the sentence
`The HTTP user-agent request header.`; inline markup splits its text nodes, so the signal is named
here rather than quoted. The other two items are single text nodes [S425]:

> "The source IP address of the request."

> "The reverse DNS hostname of the source IP."

The inventory is therefore the `user-agent` request header, the source IP address, and the reverse
DNS hostname of that address [S425]. The page lists the three; it does not rank them, give a
decision rule when they disagree, or say that any one alone proves the requester is Google. It also
gives no count of addresses per crawler and no per-country share — omissions, not claims [S425].

## Why one crawler can appear under several addresses

The log consequence sits in the page's `Technical properties` section [S425]:

> "Google's crawlers and fetchers are designed to be run simultaneously by thousands of machines"

Those clients sit in datacenters around the world to save bandwidth, and the page draws the
consequence for a log reader [S425]:

> "Therefore, your logs may show visits from several IP addresses."

So an address-count argument — one host visited from two addresses, so one of the two must be an
impostor — is not supported by this page [S425].

## Egress location and the stated fallback

> "Google egresses primarily from IP addresses in the United States."

> "may attempt to crawl from IP addresses located in other countries"

The second is a mid-sentence fragment of one text node (the full sentence exceeds the quotation
ceiling). Read together, the page says primary United States egress plus a possible crawl from
elsewhere when it detects that a site is blocking United States requests [S425]. It names no other
country and promises no fallback.

## Where the page sends the reader for the test

> "Learn how to use these details to"

The sentence continues with the link text `verify Google's crawlers and fetchers` (a 5-unit text node, named here rather than quoted), which points at the verification page
(`…/crawling/docs/crawlers-fetchers/verify-google-requests`) [S425]. This page states that the
details are usable for verification, not the method; reverse DNS, forward DNS and published
IP-range matching belong to the verification page's own row this round.

## Related lane entries, by path

- `corpus/knowledge/crawler-identity.md` — the entry corrected append-only this round; this page's
  three-item list is the row its correction cites.
- `corpus/knowledge/baidu-spider-identification.md` — another operator's identification methods, kept
  as its own row; nothing from it is quoted or restated here.

## Quote classes

Every quotation above is an exact raw substring of one text node of the article block in the
retained body `S425.html` (74477 bytes, HTTP 200, sha256
`ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa`), each within 25 units and 160
characters and page-unique across both bodies retained this round. Where inline markup splits a
sentence (the `user-agent` item, the pointer sentence and its link), only whole text nodes of 6 or more units are quoted; shorter nodes are named in backticks.

Scope note: this entry records what the operator's overview page states about how its crawlers
identify themselves and about the addresses a log may show; no crawl was observed and no Google
behaviour was measured.
