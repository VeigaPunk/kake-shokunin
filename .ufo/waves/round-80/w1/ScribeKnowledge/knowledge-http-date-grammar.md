source: S453 — RFC 9110, HTTP Semantics, §5.6.7 Date/Time Formats — https://www.rfc-editor.org/rfc/rfc9110.txt — Section 5.6.7, lines 1836-1937 of the plain-text edition (opened 2026-11-04T10:45:05Z, HTTP 200, 502,941 bytes, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, retained at .ufo/waves/round-80/w1/ScribeKnowledge/rfc9110.txt); S452 — MDN, X-Robots-Tag header — https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag — Syntax line 209, the date sentence at line 212 and the Multiple headers example at line 239 of the tag-stripped text (302 lines, 17,936 B, text sha256 8be2a4062ecee6ec671eb6cf0aab28a066a6042b8caec7feedc96d939482556e; raw 218,816 B, sha256 c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38, opened 2026-11-04T10:45:12Z, HTTP 200, retained at .ufo/waves/round-80/w1/ScribeKnowledge/mdn-x-robots-tag.raw and .txt; the round-80 scout 677-line strip numbers the same lines 211, 214, 243, text sha256 dd94203e1a38b7efb49092095364ad8298b2a0d46a80f7bc13e87e3cc554bc26, retained at .ufo/waves/round-80/w1/ScoutSources/S452-mdn-x-robots-tag.txt); grammar terms from .ufo/waves/round-80/amendments/amendment-1.md
verified-at: 2026-11-04 — every quote below was located in these retained bytes by .ufo/waves/round-80/w1/ScribeKnowledge/verify_quotes.py (receipt `quote-receipts.json`, 19/19 found); no other network read by this seat
recheck: 365d for S453; MDN is a living page, so re-open S452 and re-hash its raw body before reusing its example
ground: operability — the offline X-Robots-Tag declaration audit's date-value grammar (round-80 C2)
terms: .ufo/waves/round-80/amendments/amendment-1.md A1-A3, written before any round-80 case was scored and before scripts/x_robots_tag_audit.py was touched
scope: the HTTP-date formats and the lane's comma segmentation for `unavailable_after` values; not crawler behaviour, not robots.txt outcomes, not any live property's state

# HTTP-date — three formats, a comma in two, and the value the header carries

RFC 9110 defines one date type for HTTP fields and requires recipients to accept three shapes of
it: "A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date
formats." (`rfc9110.txt:1855-1856`, 17 words). Senders are narrower — the same paragraph continues
"MUST generate those timestamps in the IMF-fixdate format" (`rfc9110.txt:1858`, 8 words) — so the
accepted set is wider than the generated set.

## The three shapes

| Format | ABNF shape (RFC 9110 §5.6.7) | Example | Comma |
|---|---|---|---|
| IMF-fixdate | `IMF-fixdate = day-name "," SP date1 SP time-of-day SP GMT` (`rfc9110.txt:1873`) | `Sun, 06 Nov 1994 08:49:37 GMT` | one, immediately after the day name |
| obsolete RFC 850 | `rfc850-date = day-name-l "," SP date2 SP time-of-day SP GMT` (`rfc9110.txt:1902`) | `Sunday, 06-Nov-94 08:49:37 GMT` | one, immediately after the long day name |
| asctime | `asctime-date = day-name SP date3 SP time-of-day SP year` (`rfc9110.txt:1910`) | `Sun Nov  6 08:49:37 1994` | none |

`obs-date = rfc850-date / asctime-date` (`rfc9110.txt:1900`), so `HTTP-date = IMF-fixdate /
obs-date` is exactly these three alternatives. The day names are `%s"Mon"` … `%s"Sun"` for
IMF-fixdate and `%s"Monday"` … `%s"Sunday"` for the RFC 850 shape; the grammar is case sensitive —
"HTTP-date is case sensitive." (`rfc9110.txt:1914`, 4 words) — and asctime carries no zone token
because "values in the asctime format are assumed to be in UTC" (`rfc9110.txt:1863-1864`, 11
words). The RFC labels its own examples of the three shapes at lines 1848-1853.

[INFERENCE] IMF-fixdate is the shape MDN's own example uses, but MDN does not name IMF-fixdate:
its `unavailable_after` entry says "A date must be specified in a format such as RFC 822, RFC 850, or
ISO 8601." (`ScoutSources/S452-mdn-x-robots-tag.txt:214`, 17 words). The round-79-numbered tag-strip
carries the same sentence at `S452:212`, where link boundaries leave spaces before the commas; the raw
body is byte-identical in both rounds (`sha256 c4216ffb…7aaf38`). RFC 9110 describes its preferred
format as "a fixed-length and single-zone subset of the date and time specification used by the
Internet Message Format" (`rfc9110.txt:1841-1842`, 17 words), so reading MDN's "RFC 822" as the
family that IMF-fixdate fixes is this entry's reading, not either page's sentence.

## Where the comma sits, and why it matters to a list parser

Only the two non-asctime shapes carry a comma, and in both it follows the weekday token: `day-name
","` for IMF-fixdate, `day-name-l ","` for RFC 850. asctime has no comma at all. RFC 9110 says such
a value can be a member of a list-based field and needs delimiting: "Fields that expect to contain a
comma within a member, such as within an HTTP-date or URI-reference element" (`rfc9110.txt:1629-1630`,
18 words), which "ought to be defined with delimiters around that element" (`rfc9110.txt:1631`, 9
words). The RFC does not define `X-Robots-Tag`: the retained text has 0 occurrences of
`x-robots-tag` (`grep -ci x-robots-tag rfc9110.txt` -> 0, exit 1; control `grep -ci robots` -> 2,
exit 0), and MDN states "Not part of any current specification." (`S452:258`, 6 words).

## What the lane's tool accepts (amendment terms, not a run)

`.ufo/waves/round-80/amendments/amendment-1.md` amends the round-79 grammar in three terms:

- **A1 — comma ownership.** A comma that immediately follows the leading weekday token of an
  `unavailable_after` value belongs to that value and does not end the directive segment. Scope is
  values whose first token is a weekday name: `Mon`…`Sun` for IMF-fixdate, `Monday`…`Sunday` for the
  RFC 850 shape. Every other comma keeps the round-79 rule (it terminates the segment).
- **A2 — asctime added.** The asctime shape joins IMF-fixdate, the RFC 850 shape, ISO 8601 date and
  ISO 8601 date-time in the accepted set, with the day-of-month field space-padded to width two (a
  single space is also accepted).
- **A3 — same vocabulary.** No new finding id and no new exit code; a comma-bearing value that
  fails its shape is `xrt_invalid_value` and is dropped, never `xrt_unknown_directive`.

[INFERENCE] Because both comma-bearing shapes in the table above begin with a weekday token, A1's
scope covers exactly those two; an asctime value needs no comma rule. [INFERENCE] The effect on
S452's own example, `X-Robots-Tag: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT` (`S452:239`, 8
tokens), is that the value stays one segment; this entry did not run the tool, so that is the
amendment's declared consequence, not an observed result.

[INFERENCE] The comma rule is a lane segmentation decision, not an HTTP rule. RFC 9110 says only
that a field expecting a comma inside a member ought to define delimiters; it neither defines this
header nor blesses a bare comma inside an unquoted member.

## Limits

- **No tool run, no live property.** Everything above is read from the two retained files and the
  amendment; no URL beyond those two was requested, and no serving host is described.
- **Source vocabularies differ.** MDN names RFC 822, RFC 850 and ISO 8601; RFC 9110 names
  IMF-fixdate, the obsolete RFC 850 shape and asctime. The accepted set is the union, not either
  list alone.
- **Case and zone.** HTTP-date is case sensitive and asctime is assumed UTC. What the tool does with
  a lowercase weekday or a named zone is not stated by the amendment.
- **A2 is wider than the RFC by one branch.** RFC 9110's `date3 = month SP ( 2DIGIT / ( SP 1DIGIT ))`
  (`rfc9110.txt:1911`) admits exactly two renderings of the day (`Nov 16`, `Nov  6`); A2's prose also
  accepts a single-space single digit (`Nov 6`) [INFERENCE]. No frozen round-80 case exercises that
  widened branch (c34 uses `Nov  6`, c43 uses `Nov 16`), so it changes no oracle byte.
- **One document, two rows.** S453 cites the same plain-text edition as S028
  (`sha256 21c1cdce…7232a`), whose scope is URI schemes; the rows differ by section and scope, not
  by bytes.
- **Price of the source.** RFC 9110 is a published RFC (recheck 365d); MDN is a living page, so its
  raw and text hashes are recorded and must be re-taken before the example is reused.
