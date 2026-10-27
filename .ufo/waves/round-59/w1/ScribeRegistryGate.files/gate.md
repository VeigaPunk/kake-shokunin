## Gate

Fragment for `corpus/lessons/round-59.md` (Claim C3, frontier step), drafted independently of the entry scribes by seat
`ScribeRegistryGate`. Splice the three sections below under the lesson's `## Gate`, `## Registry changes (old → new)` and
`## Assimilation`.

Rows opened this round. Unit rule (the C3 counter's `units()`): one unit per CJK character, one per non-CJK whitespace token;
every quote below is 6 to 25 units and at most 160 characters, a substring of one whitespace-collapsed text node of the retained
body's article block (the container of class `devsite-article-body` .. `<devsite-content-footer`), and page-unique across the two bodies. Both
pages were opened 2026-10-27 UTC by `.ufo/waves/round-59/fetch_sources.py` (GET, HTTP 200, effective URL equal to the request
URL, userAgent `kake-shokunin-round59`) and retained under `.ufo/waves/round-59/sources/` with the sha256 receipts in
`sources/receipts.json`; the digests were re-run this wave (`sha256sum`, both equal to the receipt and to the counter's frozen
`BODY_SHA256`).

- S425 — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers — accessed 2026-10-27 — § Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC) — quote: "Google's crawlers identify themselves in three ways:" (7 units; substring of one collapsed text node of the retained body, sha256 ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa, 74477 bytes, HTTP 200), and "The source IP address of the request." (7 units; same retained body, sha256 ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa, 74477 bytes, HTTP 200)
- S426 — https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests — accessed 2026-10-27 — § Use command line tools (Last updated 2026-03-20 UTC) — quote: "Run a reverse DNS lookup on the accessing IP address from your logs, using the" (15 units; substring of one collapsed text node of the retained body, sha256 8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879, 69789 bytes, HTTP 200), and "Verify that it's the same as the original accessing IP address from your logs." (14 units; same retained body, sha256 8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879, 69789 bytes, HTTP 200)

Page-printed revision dates: S425 prints `Last updated 2026-06-12 UTC`, S426 prints `Last updated 2026-03-20 UTC`. Both anchors
name an `<h2>` of the article block (`Verify Google's crawlers and fetchers`; `Use command line tools`), not the h1, and each is
the section that holds the quote: the three self-identification signals and the S426 link for S425, the reverse-then-forward DNS
steps for S426.

ADMIT theme `crawler identity verification signals` (staged package `merge/kake/`, shokuknow, read-only). Staged row **S398** is
re-grounded as **S425** — renumbered by document, not arithmetically (the registry's next unused id after S424) — and the staged
entry name is not carried. **S426** is lane-found from S425 itself.

Staged row S398, refused as staged, each point read against the retained body or the frozen census:

- `source` cell title is the page h1 `Overview of Google crawlers and fetchers (user agents)`; the page's `<title>` text before
  ` | ` is `Google Crawler (User Agent) Overview`. The row carries the `<title>` text.
- anchor clause `no revision printed on the page` is false: the page prints `Last updated 2026-06-12 UTC` (2 occurrences in the
  collapsed body); the new anchor carries it. The old anchor also lacks the `(Last updated YYYY-MM-DD UTC)` form.
- the recheck cell embeds a live command with an escaped pipe (`\|`); the row splits to 14 cells under the frozen census awk
  (11 cells means NF=13), i.e. the staged row is malformed as staged. The row carries `180d`.
- `opened` 2026-10-24 is not this round's access date; the fetch receipt is 2026-10-27T01:21:22Z.
- `used-by` names `corpus/knowledge/crawler-identity-three-signals.md`, a path that must not exist at the measured revision.

Staged entry `crawler-identity-three-signals.md`, sentences refused and why (counts are `str.count` on the whitespace-collapsed
retained S425 body):

- `the address and its reverse hostname are the two that a caller cannot forge` — `forge` 0, `cannot forge` 0: the page names
  three signals and never says which a caller can forge; a page-unsupported gloss, refused.
- `Baidu's own page checks the reverse hostname against *.baidu.com or *.baidu.jp` — `baidu` 0: cross-document attribution (that
  fact is S423's); refused, the row must not carry another page's statement.
- `Yahoo! JAPAN's crawl documentation tells the server administrator to restrict access by the address the crawler's DNS points
  at` — `Yahoo` 0: cross-document attribution; refused for the same reason.
- `All three operators the lane now holds say this in their own words` — lane meta-prose, not a page statement, and it depends on
  two documents the row does not quote; refused from the entry body.
- `A site that blocks * and believes it has excluded every crawler has not excluded that one` — the page binds the AdsBot
  exception to `with the ad publisher's permission` (1 occurrence); the unconditional sentence is refused, the bounded form kept.
- `the page's example is that AdsBot ignores the global robots.txt user agent (*) with the ad publisher's permission` — substance
  kept, but unquotable as one span: the collapsed nodes are `ignores the global robots.txt user agent (`, `*`, and `) with the ad
  publisher's permission.` An entry quoting it must split or paraphrase.
- `Special-case crawlers are similar to common crawlers, however are used by specific products where there's an agreement between
  the crawled site and the Google product about the crawl process` — present, but as one 31-unit node, above the 25-unit ceiling;
  it must be cut to a 25-unit-or-shorter subspan before it is quoted.
- the staged `verified-at:` curl (ran 2026-10-24) and the staged `ground:` line — superseded by the round-59 receipt; not carried.

Kept from the staged package: the three-signal sentence itself and the numbered list items beside it, which are separate text
nodes (`The source IP address of the request.`, `The reverse DNS hostname of the source IP.`).

S426 lane-found, provenance in the retained S425 body: `/crawling/docs/crawlers-fetchers/verify-google-requests` appears as an href 2
times (once in the page side-navigation, once in the closing sentence of the anchored h2 section); the page prints that sentence
with the link inside it, so its collapsed nodes are `Learn how to use these details to `, `verify Google's crawlers and fetchers`,
`.`. The sentence is not quotable as one span.

Reported conflict, not resolved by a row (counter version 1, for the C3 attack seats and the canonical judge): C5 requires the
row's `source`-cell title to be 6+ units and to equal the page's `<title>` text before ` | `. For S425 that text is `Google Crawler (User Agent) Overview`, 5 units. No cell can satisfy both clauses: the faithful value fails the unit floor, and the value
that passes the floor is not the page title. The row carries the page's exact title. S426's title (`Verify Requests from Google
Crawlers and Fetchers`, 7 units) meets both.

## Registry changes (old → new)

- Rows: 162 → 164. S425 and S426 are appended after S424 in that order, both `mined`, opened 2026-10-27, recheck `180d`,
  `used-by` = S425: `corpus/knowledge/crawler-identity-signals.md, corpus/knowledge/crawler-identity.md`; S426:
  `corpus/knowledge/googlebot-verification.md`. No existing row's `status`, `recheck` or `used-by` changed (a pure addition).
- Counts: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = 162 at the base revision and in the
  pre-append mirror (`assimilation/mirror-pin.json`: 162 rows, 150968 bytes, sha256 ecb5cedfcf2addc043ce6fa1b6def453088a996f95c0f60583dfdf0f30efe6ae);
  both ids are absent from the base (`grep -cE '^ *\| *S42[56] *\|'` = 0).
- Draft-row census (a scratch copy of the registry plus the two draft rows, frozen CORPUS.md awk formulas): rows 164, malformed
  (NF!=13) 0, duplicate ids none, tier/kind/status enum violations none, status histogram `mined=134 queued=8 rejected=22`, tier
  histogram `A=141 B=6 C=17`. The `used-by` existence check prints the two entry paths as missing at the base revision — expected:
  they are entry-scribe deliverables.

## Assimilation

Id lists under `.ufo/waves/round-59/assimilation/`: registry `reg-ids` 162, staged `staged-ids` 129, `collisions` 8 (S312 S329
S367 S372 S373 S374 S390 S409 — the round-57/58 set). Neither S425 nor S426 appears in either list; S398 appears in `staged-ids`
and not in `reg-ids`. Renumber map by document: staged S398 → S425; S426 has no staged id (lane-found from S425). Quarantine
slice: 12 rows (S142 S143 S148 S154 S156 S161 S178 S184 S193 S194 S195 S206), unchanged and held — the round-58 L0 question is
unanswered, so nothing from the slice is appended this round (routed around, not treated as answered).
