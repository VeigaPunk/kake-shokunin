# Gate quotes — kake round 80 (`## Gate` source evidence)

Access date for every entry: **2026-11-04** (UTC fetch timestamps recorded below). One public GET per
source by this seat: the round's `ScoutSources` seat had not published when this seat started (its
directory was empty and `ScoutSources.md` absent at 10:44Z; both landed at 10:46-10:47Z, mid-run —
`scout-status.txt`). The two fetches below are byte-identical to the scout's retained pair, which is
recorded as a cross-check, not as a substitute opening. Each quote was re-located in the retained
bytes this round; the locator script and its receipt are named under each row.

## S453 — RFC 9110, HTTP Semantics, §5.6.7 Date/Time Formats

- URL: `https://www.rfc-editor.org/rfc/rfc9110.txt` (final URL identical), HTTP 200
- Retrieved: 2026-11-04T10:45:05Z; 502,941 bytes; sha256
  `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`
- Retained: `.ufo/waves/round-80/w1/ScribeKnowledge/rfc9110.txt`
- Gate quote, `rfc9110.txt:1855-1856` (17 words):

  > A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats.

## S452 — MDN, X-Robots-Tag header (re-open; no new row)

- URL: `https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag` (final URL
  identical), HTTP 200
- Retrieved: 2026-11-04T10:45:12Z; raw 218,816 bytes, sha256
  `c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38`
- Retained: `.ufo/waves/round-80/w1/ScribeKnowledge/mdn-x-robots-tag.raw`; tag-stripped text
  `mdn-x-robots-tag.txt` (302 lines, 17,936 B, sha256
  `8be2a4062ecee6ec671eb6cf0aab28a066a6042b8caec7feedc96d939482556e`)
- Numbering: this seat's 302-line strip reproduces the round-79 text byte for byte, so line numbers
  match `corpus/knowledge/x-robots-tag-header.md` (`S452:209`, `:212`, `:239`). The scout's
  677-line strip numbers the same sentences `:211`, `:214`, `:243` (raw bytes identical; only the
  stripping pipeline differs) — `.ufo/waves/round-80/w1/ScoutSources/S452-mdn-x-robots-tag.txt`.
- Gate quote for the comma-bearing example, `mdn-x-robots-tag.txt:239` (8 tokens; scout numbering
  `:243`):

  > X-Robots-Tag: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT

  The raw body and the tag-stripped text are byte-identical to the round-79 retained pair
  (`S452-mdn-x-robots-tag.raw` sha256 `c4216ffb…7aaf38`, `.txt` sha256 `8be2a406…82556e`), so the
  page did not change between the two rounds.

## Supporting lines opened this round (not Gate quotes)

- `rfc9110.txt:1841-1842` — RFC 9110 calls its preferred format "a fixed-length and single-zone
  subset of the date and time specification used by the Internet Message Format [RFC5322]".
- `rfc9110.txt:1848` — `Sun, 06 Nov 1994 08:49:37 GMT    ; IMF-fixdate`
- `rfc9110.txt:1852` — `Sunday, 06-Nov-94 08:49:37 GMT   ; obsolete RFC 850 format`
- `rfc9110.txt:1853` — `Sun Nov  6 08:49:37 1994         ; ANSI C's asctime() format`
- `rfc9110.txt:1873` — `IMF-fixdate  = day-name "," SP date1 SP time-of-day SP GMT`
- `rfc9110.txt:1900` — `obs-date     = rfc850-date / asctime-date`
- `rfc9110.txt:1902` — `rfc850-date  = day-name-l "," SP date2 SP time-of-day SP GMT`
- `rfc9110.txt:1910` — `asctime-date = day-name SP date3 SP time-of-day SP year`
- `rfc9110.txt:1914` — "HTTP-date is case sensitive."
- `rfc9110.txt:1629-1631` — the list-member comma sentence (quoted in two fragments in the entry).
- `mdn-x-robots-tag.txt:209` — `unavailable_after: <date/time>`
- `mdn-x-robots-tag.txt:212` — "A date must be specified in a format such as RFC 822 , RFC 850 , or
  ISO 8601." (the spaces before the commas are the tag-stripped text's link boundaries; the same
  sentence renders clean at `ScoutSources/S452-mdn-x-robots-tag.txt:214`, quoted in the entry)
- `mdn-x-robots-tag.txt:258` — "Not part of any current specification."
- `rfc9110.txt:1911` — `date3        = month SP ( 2DIGIT / ( SP 1DIGIT ))` (the A2 widening limit)

## Quotes not located

None. All 19 quoted spans checked by `verify_quotes.py` (whitespace-collapsed substring match against
the retained bytes) are present: 15 in `rfc9110.txt`, 3 in `mdn-x-robots-tag.txt`, 1 in the scout's
`S452-mdn-x-robots-tag.txt`; receipt `quote-receipts.json`, summary `quotes=19 found=19 missing=0`.
