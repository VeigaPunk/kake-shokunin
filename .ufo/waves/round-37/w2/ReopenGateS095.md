# ReopenGateS095 — S095 Gate line and SOURCES row, live re-open (wave 2)

Seat: KakeR37.ReopenGateS095 (leaf). Sandbox `/fast/scratch/hyaku/kake-r37w2/ReopenGateS095/`,
clone at lane tip `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c` (`rev-parse` exit 0). Live re-open
2026-10-23T03:45:05Z–03:45:35Z. No installs, no lane writes; network was one public doc URL.

## Commands (all in the sandbox)

- `git clone -q …/kake-shokunin clone && git checkout -q 79d3c780…` → exit 0; HEAD `79d3c780…`.
- `curl -sS -o /dev/null -D - '<requested URL>'` → exit 0; `HTTP/2 301`,
  `location: /crawling/docs/robots-txt/robots-txt-spec` (relative), `date: Fri, 23 Oct 2026 03:45:05 GMT`.
- `curl -sS -o /dev/null -D - '<final URL>'` → exit 0; `HTTP/2 200`,
  `last-modified: Mon, 31 Aug 2026 14:57:06 GMT`, `content-length: 99414`.
- `curl -sS -L -w 'num_redirects=%{num_redirects} final=%{url_effective} code=%{http_code}'` →
  exit 0; `num_redirects=1 final=https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec code=200`.
- `python3 -B refetch.py` (lane rule: `fetch_sources.py::visible_text`, same UA; fetched
  2026-10-23T03:45:35Z) → exit 0; `status=200`, `bodyBytes=99414`, `textWords=3030`,
  `textSha256=a90948534ca17e54196115163fb9a5f6afbb0b347f97a44b01a3a1d636ddbbc6`.
- `sha256sum .ufo/waves/round-37/sources/S095.txt` → same `a9094853…bbc6`; `receipts.json` S095
  `textSha256` is the same string, `accessedUtc` `2026-10-23T02:50:49Z`, `status` 200,
  `finalUrl` the crawling URL.
- Heading extraction from the live HTML → h1 `How Google interprets the robots.txt specification`;
  the row's five named h2s each present (`grep -cF` = 1 each).
- `grep -cF 'Last updated 2026-08-31 UTC.'` → 1; `grep -cF 'How Google interprets…'` → 1.
- `grep -cF '<Gate quote>' S095.txt` → 1. Quote offset 13205 in live text, after h2
  `Order of precedence for user agents` (12809) and before the next h2 (17788): located in the
  section the Gate names; 11 words (≤25).
- Quote in retained S011.txt/S096.txt/S097.txt → 0, 0, 0 (not page chrome of another source).
- `grep -cF 'most specific matching group'` in S095 retained → 0, live text → 0,
  S011.txt → 0, `corpus/knowledge/robots-txt-rules.md` → 0 (final grep exit 1 because the last
  count was zero).
- Row parsed by header → 11 cells for 11 columns; no stray `|`.

## Verdicts

| Attacked statement | Verdict |
|---|---|
| Requested URL `…/search/docs/crawling-indexing/robots/robots_txt` redirects to the recorded final URL | **holds**: one-hop `HTTP/2 301` with relative Location; target 200 |
| Final URL is canonical | **holds**: live `<link rel="canonical" href="https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec">`; 200 served directly |
| Anchor sections exist verbatim | **holds**: all five h2s, once each, exact strings |
| “last updated 2026-08-31 UTC” | **holds**: page text “Last updated 2026-08-31 UTC.” and `Last-Modified: Mon, 31 Aug 2026 14:57:06 GMT` |
| Retained text sha256 `a9094853…bbc6` | **holds**: reproduced byte-identically by an independent fetch 55 min after the recorded one |
| fetched 2026-10-23T02:50:49Z, HTTP 200 | **partly unverifiable**: receipt and wave-1 scout agree, but the timestamp itself cannot be independently replayed; 200 at the recorded/next fetch holds |
| kind `docs`, tier `A` | **holds**: Google's own documentation for its own crawler policy; CORPUS tier A covers “official docs” scoped to this claim |
| `teaches`: group selection, merging, path-rule precedence | **holds**: live text “Only one group is valid for a particular crawler … most specific user agent”; “all the rules … combined internally into a single group”; “User agent specific groups and global groups (`*`) are not combined”; “most specific rule based on the length of the rule path … Google uses the least restrictive rule” |
| `scope` not protocol-wide | **holds**: “This page describes Google's interpretation of the REP. For the original standard, check RFC 9309 .” |
| status `mined`, opened `2026-10-23`, recheck `90d`, used-by entry | **holds**: entry cites S095 in `source:` and at lines 15/17/25/37/45/81; `90d` is a permitted cadence |
| Gate quote verbatim, section, ≤25 words | **holds**: exact substring, 1 occurrence, correct section, 11 words |
| Gate quote grounds `teaches` | **overstated (partial)**: the quote grounds the group-selection half; it says nothing about path-rule precedence, which the row’s own “Order of precedence for rules” section grounds instead. Contract CORPUS.md rule 1 asks for a quote grounding `teaches`; a strict reading makes this a partial ground, not a wrong one |
| `corpus/lessons/round-37.md:88-90`: draft phrase “the most specific matching group”, “which is S095's wording” | **wrong (adjacent)**: 0 occurrences in S095 retained text and live text. S095 says “the most specific group” / “the group with the most specific user agent”. The lesson’s substantive point (RFC 9309 does not use it) stands; the S095 attribution is false verbatim |

## Notes / remaining unknowns

- **Body hash is volatile, text hash is not.** Retained body `c8c1f204…` (99414 B), wave-1 scout
  live `55efdb56…` (99418 B), my fetch `314bcafc…` (99414 B): same visible text each time,
  differing HTML inside the GA/GTM `<script type="application/json">` block. The row cites the
  text hash, which is the reproducible key; a future freshness gate keyed on body sha256 would
  falsely fail this row.
- `used-by` lists only the knowledge entry although the round-37 lesson’s Gate also cites S095;
  CORPUS.md rule for `used-by` reads “knowledge entries or lessons citing the row”. Same shape as
  S096/S097 in this round, so a consistency question, not an S095-specific defect.
- Not tested: whether the 301 is stable over time (single observation, plus the wave-1 scout’s);
  the page’s own “Last updated” date is 2026-08-31, predating the round.
