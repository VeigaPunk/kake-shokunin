# EntrySignals

Axis: freshness (sourced); claim C3; row **S425** (overview page). The lane was read-only for this
seat; no lane mutation (no git/jj write), no sibling path touched. Scratch
`/fast/scratch/hyaku/kake-r59/EntrySignals` (deleted at exit).

## What was run / not run

- `span_tools.py window S425` -> 157 text nodes; the block's last h2 is `Verify Google's crawlers
  and fetchers` (raw line 1266, `id="crawl-verify-crawler"`) and holds the three-item list.
- `span_tools.py check S425 '<span>'` per quoted span (verbatim outputs under SPAN CHECKS).
- C5 entry-loop simulation over the drafted file: 9 double-quoted spans, 0 bad, 8 page-unique spans
  of 6+ units, subject `IP address` carried.
- `grep -F -c 'The source IP address of the request.' sources/S425.html` -> `1` (single line 1276).
- Row simulator: 11 cells, no escaped pipe, `mined` / `2026-10-27` / `180d`, URL exact, anchor an h2
  of the block, revision in a text node, sha256 `ff2b9fd7…5caa` + `74477 bytes` = `receipts.json`.
- **Not run**: `c59_quote_truth.py` against a revision (no lane mutation, no after-state scoring);
  live `curl` (the recheck count is measured against the retained body, as specified); census/append.

## ENTRY

```markdown
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

> "verify Google's crawlers and fetchers"

The second span is link text pointing at the verification page
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
sentence (the `user-agent` item, the pointer's two nodes), only whole text nodes are quoted.

Scope note: this entry records what the operator's overview page states about how its crawlers
identify themselves and about the addresses a log may show; no crawl was observed and no Google
behaviour was measured.
```

## GATE LINE

- S425 — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers — accessed 2026-10-27 — § Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC) — quote: "The source IP address of the request." (7 units; substring of one collapsed text node of the retained body, sha256 ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa, 74477 bytes, HTTP 200)

## REGISTRY ROW

| S425 | Google for Developers — Google Crawler (User Agent) Overview — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers | docs | A | **Three identification signals and multi-address logs** — the operator lists a user-agent request header, the source IP address and the reverse DNS hostname of that IP, and says a crawler's logs may show several addresses | § Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC) | the page names three ways its crawlers identify themselves (the `user-agent` request header, the source IP address, the reverse DNS hostname of the source IP) and says the fleet runs on thousands of machines across datacenters, so a log may show visits from several IP addresses, with egress primarily from the United States and a possible crawl from other countries when United States requests are blocked | mined | 2026-10-27 | 180d | corpus/knowledge/crawler-identity-signals.md, corpus/knowledge/crawler-identity.md |

Cell 2 title = page `<title>` before the first ` | `; cell 6 = the block's h2; used-by =
`USED_BY["S425"]` (entry + `crawler-identity.md`).

## SPAN CHECKS

- "Google's crawlers identify themselves in three ways:" -> {'units': 7, 'chars': 52, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
- "The source IP address of the request." -> {'units': 7, 'chars': 37, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
- "The reverse DNS hostname of the source IP." -> {'units': 8, 'chars': 42, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
- "Google's crawlers and fetchers are designed to be run simultaneously by thousands of machines" -> {'units': 14, 'chars': 93, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
- "Therefore, your logs may show visits from several IP addresses." -> {'units': 10, 'chars': 63, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
- "Google egresses primarily from IP addresses in the United States." -> {'units': 10, 'chars': 65, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
- "may attempt to crawl from IP addresses located in other countries" -> {'units': 11, 'chars': 65, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
- "Learn how to use these details to" -> {'units': 7, 'chars': 33, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}
- "verify Google's crawlers and fetchers" -> {'units': 5, 'chars': 37, 'in_text_node': True, 'count_in_body': 1, 'unique': True, 'within_ceilings': True}

Not quoted: `The HTTP user-agent request header.` (`check` -> `in_text_node: False, count_in_body: 0`;
`The HTTP` and `user-agent` are separate nodes and below the 6-unit floor).

## OMITTED (page content not carried)

- Taxonomy (common / special-case / user-triggered; Google Site Verifier): classification, not identity.
- AdsBot's `*` exception: in the block, but robots.txt literature; the staged file's version is not carried.
- Protocol / encoding / size surfaces (HTTP/1.1 default, HTTP/2, the 421 opt-out, FTP/FTPS, `gzip`
  `deflate` `Brotli`, the `Accept-Encoding` example, the 15MB default and 2MB example): other subjects.
- Crawl rate / host load; HTTP caching (`ETag`, `If-None-Match`, `Last-Modified`, `If-Modified-Since`, `max-age`).
- The verification method (reverse/forward `host`, `googlebot.com` / `google.com` / `googleusercontent.com`,
  IP-range JSON, the three `host` examples): S425 only points at that page; method = S426's row.
- Staged-candidate claims without S425 support ("signal anyone can set", Baidu/Yahoo comparisons) and its file name: dropped.

## Findings

1. **Conflict, for the canonical judge (not worked around).** C5 derives
   `title = " — ".join(row[1].split(" — ")[1:-1])` and passes only if
   `if not title or units(title) < 6 or title != page_title:` is false, with `page_title` =
   `<title>` before the first ` | ` = `Google Crawler (User Agent) Overview` -> `units = 5`. The
   assignment's cell-2 shape (`Google for Developers — <title> — <url>`) forces `title == page_title`,
   so the `6+ units` floor cannot be met by any conforming row. Measured: `row title: 'Google Crawler
   (User Agent) Overview' units 5 / page title units 5 / equal True / >=6 False`. Counter message:
   `{sid}: row title {title!r} is not the page's <title> text before the site suffix {page_title!r} (6+ units)`.
2. **Observation (measured, not scored).** The revision `Last updated 2026-06-12 UTC` (raw line 1345)
   has `in_content(collapsed, …, 'S425')` = `False`: it sits outside the article window
   `content_window = (25627, 38178)`. C5's revision test uses any `>…<` text node of the body, which
   matches (`['Last updated 2026-06-12 UTC.', …]`), so the anchor is supportable; the scopes differ.
3. Quote-class boundary: the `user-agent` item and the pointer are split across text nodes by inline
   markup; only whole nodes are quoted, and the entry says so.
4. Citations: S425 only; the two lane entries by plain path; S426/S423 not named.

## Artifacts

- Entry (fenced copy above is byte-identical): `.ufo/waves/round-59/w1/EntrySignals.files/crawler-identity-signals.md`
  (4377 bytes, 82 lines). Report: `.ufo/waves/round-59/w1/EntrySignals.md`.
- Read-only inputs: `.ufo/waves/round-59/{sources/S425.html,sources/receipts.json,contract.md,c59_quote_truth.py,span_tools.py}`,
  `corpus/SOURCES.md` (S423 row shape), `corpus/knowledge/*` (house style). Scratch removed; no tool installed.

VERDICT: S425 entry drafted and quote-checked (8 page-unique spans, subject `IP address`), row well formed on every runnable check, but the frozen C5 `6+ units` title floor is unsatisfiable for the page's 5-unit printed title — escalated verbatim.
