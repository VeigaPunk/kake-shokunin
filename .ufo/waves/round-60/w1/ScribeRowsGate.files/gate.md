## Gate

Rows opened this round. Unit rule (the C3 counter's `units()`): one unit per CJK character, one per non-CJK whitespace token;
every quote below is 6 to 25 units and at most 160 characters, a substring of one whitespace-collapsed text node of the retained
body's article block (the container of class `devsite-article-body` .. `<devsite-content-footer`), and page-unique across the three
bodies. All three pages were fetched 2026-10-27T04:03Z by `.ufo/waves/round-60/fetch_sources.py` (GET, HTTP 200, effective URL equal
to the request URL, userAgent `kake-shokunin-round60`) and retained under `.ufo/waves/round-60/sources/` with the sha256 receipts
in `sources/receipts.json`; the digests were re-run this wave (`sha256sum` and byte counts, all three equal to the receipt). Each
page prints `Last updated <date> UTC` inside `<devsite-content-footer`, read with the R59-D3 fix's placement rule. Anchor rule
(L1 ruling, 2026-10-27): the anchor cell names the nearest article-block heading (h1/h2/h3) that precedes the row's quote, and
every quote on the row's Gate line lies in that heading's section (below the anchor heading, above the next one). S427's two
quotes sit in the page lead, so its anchor is the article h1; S428's quotes also sit in the lead, under its h1; S429's quotes
sit under the h2 named.

- S427 — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers — accessed 2026-10-27 — § Overview of Google crawlers and fetchers (user agents) (Last updated 2026-06-12 UTC) — quote: "They always respect robots.txt rules for automatic crawls." (8 units; substring of one collapsed text node of the retained body, sha256 d70ce6f5aa51ff2f7e6192191330976bd6279e3f2e91d30ef988d3d805382175, 74477 bytes, HTTP 200), and "User-triggered fetchers are part of tools and product functions where the end user triggers a fetch." (16 units; same retained body, sha256 d70ce6f5aa51ff2f7e6192191330976bd6279e3f2e91d30ef988d3d805382175, 74477 bytes, HTTP 200)
- S428 — https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers — accessed 2026-10-27 — § List of Google user-triggered fetchers (Last updated 2026-08-19 UTC) — quote: "these fetchers generally ignore robots.txt rules" (6 units; substring of one collapsed text node of the retained body, sha256 0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2, 76197 bytes, HTTP 200), and "it only covers the requestors that are more likely to show up in log files" (15 units; same retained body, sha256 0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2, 76197 bytes, HTTP 200)
- S429 — https://developers.google.com/search/docs/crawling-indexing/robots/intro — accessed 2026-10-27 — § Understand the limitations of a robots.txt file (Last updated 2025-12-10 UTC) — quote: "The instructions in robots.txt files cannot enforce crawler behavior to your site" (12 units; substring of one collapsed text node of the retained body, sha256 423d99c5bf7fec4298d00cdd46f01a495c9ad463fa704f7850a100e43e2a9edd, 178797 bytes, HTTP 200), and "A page that's disallowed in robots.txt can still be indexed if linked to from other sites." (16 units; same retained body, sha256 423d99c5bf7fec4298d00cdd46f01a495c9ad463fa704f7850a100e43e2a9edd, 178797 bytes, HTTP 200)

S425 erratum (R59-D4). The S425 `scope` cell reads `the three crawler categories and their robots.txt posture`, which reports a
robots.txt posture for all three categories. The page does not state one for all three: its `crawler-types` table gives a posture
for common crawlers ("They always respect robots.txt rules for automatic crawls.") and for special-case crawlers (the AdsBot
example, which "ignores the global robots.txt user agent (" … ") with the ad publisher's permission."), and its user-triggered
fetchers cell carries no robots.txt clause at all — it reads "User-triggered fetchers are part of tools and product functions
where the end user triggers a fetch." and closes on "acts on the request of a user." for Google Site Verifier. The cell is
superseded by S427 on the same URL (re-opened 2026-10-27, sha256 d70ce6f5…, 74477 bytes), whose `teaches` cell opens
`supersedes S425 —` and whose `scope` cell names the categories the page does state a posture for and records its silence on the
third. S425 itself is left in place: a pure addition, no existing row's status, recheck or used-by changed.

## Registry changes (old → new)

- Rows: 164 → 167. S427, S428 and S429 are appended after S426 in that order, all `mined`, opened 2026-10-27, recheck `180d`;
  `used-by` = S427: `corpus/lessons/round-60.md`; S428: `corpus/knowledge/google-user-triggered-fetchers.md,
  corpus/knowledge/googlebot-verification.md`; S429: `corpus/knowledge/robots-txt-limits.md`. S427 supersedes S425 by scope
  correction; no existing row's `status`, `recheck` or `used-by` changed (a pure addition).
- Counts: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = 164 at the base revision; all three ids
  are absent from the base (`grep -cE '^ *\| *S42[789] *\|'` = 0).
- Draft-row census (a scratch copy of the registry plus the three draft rows, frozen census awk formulas): rows 167, malformed
  (NF!=13) 0, escaped pipes 0, duplicate ids none, tier/kind/status enum violations none, status histogram `mined=137 queued=8
  rejected=22`, tier histogram `A=144 B=6 C=17`. The `used-by` existence check prints three paths as missing at the base revision —
  expected: they are this round's entry and lesson deliverables.
