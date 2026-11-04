source: S453 — RFC 9110 §5.6.7 Date/Time Formats — https://www.rfc-editor.org/rfc/rfc9110.txt — §5.6.7 lines 1836-1937 and §5.5 Field Values lines 1579-1633 of `.ufo/waves/round-80/sources/rfc9110.txt` (502,941 B, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, fetched 2026-11-04T10:44:53Z, HTTP 200; a second GET by the wave's scout at 10:44:33Z is byte-identical); S452 — MDN, X-Robots-Tag header (held row, re-opened this round): `.ufo/waves/round-80/w1/ScoutSources/S452-mdn-x-robots-tag.txt` (17,442 B, sha256 dd94203e1a38b7efb49092095364ad8298b2a0d46a80f7bc13e87e3cc554bc26; raw 218,816 B, sha256 c4216ffb7aa934e309329d3b5adf1e62557464eebcbaab0bb33b60a72b7aaf38). This round's stripper numbers the S452 directives block 2 lines and the comma example 4 lines above the round-79 stripper used in `corpus/knowledge/x-robots-tag-header.md`; both refer to the same bytes.
verified-at: 2026-11-04 — every quote below located by line in the retained bytes this round; two public GETs, no rendered-DOM or crawler observation
recheck: 365d for S453 (an RFC changes only by a new publication); 90d for S452, a living page
ground: operability — the `unavailable_after` date grammar of `scripts/x_robots_tag_audit.py`, widened by `.ufo/waves/round-80/amendments/amendment-1.md`
scope: the date shapes a recorded `X-Robots-Tag: unavailable_after` value may carry and the comma rule that lets such a value survive field segmentation; not crawler behaviour, not any live property's declaration, not expiry semantics

# HTTP-date shapes, and the comma that breaks naive field splitting

## What the source fixes, and what it leaves to the lane

RFC 9110 defines one date grammar, `HTTP-date`, in three formats, and makes acceptance of all three a
requirement on a recipient that parses a timestamp in an HTTP field. Two of the three formats carry a
comma inside the value itself, and the same document says a comma that is data inside a member must not
be read as a list separator — so a parser that splits a field value on commas before deciding what the
value is will destroy values its own source requires it to accept.

| Fact | Source / retained `file:line` | Exact quote | Units |
|---|---|---|---|
| All three formats are accepted by a recipient | S453 `rfc9110.txt:1855-1856` | A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats. | 19 |
| The preferred format carries a comma after the day name | S453 `rfc9110.txt:1848` | Sun, 06 Nov 1994 08:49:37 GMT    ; IMF-fixdate | 9 |
| The obsolete RFC 850 format carries one too | S453 `rfc9110.txt:1852` | Sunday, 06-Nov-94 08:49:37 GMT   ; obsolete RFC 850 format | 9 |
| The asctime format does not | S453 `rfc9110.txt:1853` | Sun Nov  6 08:49:37 1994         ; ANSI C's asctime() format | 9 |
| A comma that is data must not be read as a separator | S453 `rfc9110.txt:1625-1628` | Because commas (",") are used as the delimiter between members, they need to be treated with care if they are allowed as data within a member. | 24 |
| That rule names HTTP-date explicitly | S453 `rfc9110.txt:1629-1631` | Fields that expect to contain a comma within a member, such as within an HTTP-date or URI-reference element | 19 |
| The date grammar is case sensitive | S453 `rfc9110.txt:1914` | HTTP-date is case sensitive. | 4 |
| `X-Robots-Tag` names the accepted value shapes | S452 `S452-mdn-x-robots-tag.txt:214` | A date must be specified in a format such as RFC 822, RFC 850, or ISO 8601. | 17 |
| The same page shows a comma-bearing value | S452 `S452-mdn-x-robots-tag.txt:243` | X-Robots-Tag: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT | 10 |

## The three shapes, verbatim ABNF

    IMF-fixdate  = day-name "," SP date1 SP time-of-day SP GMT            (S453:1873)
    rfc850-date  = day-name-l "," SP date2 SP time-of-day SP GMT          (S453:1902)
    date2        = day "-" month "-" 2DIGIT
    asctime-date = day-name SP date3 SP time-of-day SP year               (S453:1910)
    date3        = month SP ( 2DIGIT / ( SP 1DIGIT ) )                    (S453:1911)

Three consequences follow from the grammar, and the lane's tool implements all three:

1. `IMF-fixdate` and `rfc850-date` each carry exactly one comma, immediately after the leading weekday
   token (`day-name` = `Mon`…`Sun`; `day-name-l` = `Monday`…`Sunday`). `asctime-date` carries none.
2. `date3` pads a single-digit day inside the two-digit field (`Nov  6`), so an asctime value contains
   two consecutive spaces; whitespace normalization that collapses runs would corrupt it (S453:1917-1918
   forbids a sender adding whitespace, and this entry's reading keeps internal runs intact).
3. A parser that requires all three formats will accept a value that a comma-first splitter destroys.
   That is the round-79 defect and this round's amendment removes it.

## What the lane's tool accepts after amendment 1

| Family | Shape accepted | Ground |
|---|---|---|
| ISO 8601 | `YYYY-MM-DD` or `YYYY-MM-DD[ T]hh:mm[:ss][Z or ±hh:mm]` | S452:214 names ISO 8601 |
| IMF-fixdate | `Day, DD Mon YYYY hh:mm:ss GMT` | S453:1873; S452:214 names RFC 822, whose fixdate subset this is |
| RFC 850 | `Weekday, DD-Mon-YY hh:mm:ss GMT` | S453:1902; S452:214 |
| asctime | `Day Mon  D hh:mm:ss YYYY` | S453:1910-1911 |

The comma rule is amendment A1: a comma that immediately follows the leading weekday token of an
`unavailable_after` value belongs to the value; every other comma terminates the segment, as in round
79. A value matching no family stays `xrt_invalid_value` and is dropped, so a comma-bearing value with
a wrong zone yields `xrt_invalid_value` only, never `xrt_unknown_directive` (A3).

## Lane readings — marked, not sourced

- **asctime is accepted although S452 does not name it.** S452:214 names RFC 822, RFC 850 and ISO 8601
  and never asctime; RFC 9110:1855-1856 requires a recipient of an HTTP-date to accept all three
  HTTP-date formats, asctime included. The lane follows the recipient requirement and records the
  disagreement instead of hiding it. `[INFERENCE]`
- **A single space before a one-digit day is also accepted** (`Nov 6`), although `date3` requires `SP
  1DIGIT` after the month's `SP`. A lenient reading, chosen so a space-collapsed transcript does not
  flip a value to invalid; amendment A2 states it as a widening. `[INFERENCE]`
- **RFC 822 is read as its IMF-fixdate subset.** RFC 822 permits far more shapes; the lane accepts only
  the fixed-length subset RFC 9110 names `IMF-fixdate`, because that is the shape both sources
  exhibit. `[INFERENCE]`
- **ISO 8601 is not an HTTP-date.** S452 names it for this header; RFC 9110's `HTTP-date` production
  does not include it. The tool therefore accepts a union of two vocabularies, and the union is a lane
  policy, not a standard. `[INFERENCE]`
- **The §5.5 sentence is an `ought` on field definers, not a rule for parsers.** `X-Robots-Tag` is
  defined by no specification (S452:137, :265), so §5.5 explains why the round-79 splitter failed; it
  does not by itself bind a parser. The comma rule is the lane's amendment, grounded in that sentence
  plus S452's own example. `[INFERENCE]`

## Per-carrier scope: the header and the meta carrier now disagree

The lane holds two instruments that read an `unavailable_after` value from different carriers, and after
this round they do not agree on the same literal. Observed, not inferred
(`.ufo/waves/round-80/w1/ConnectorC/meta-date-probe.out`; the meta tool's own `--selftest` prints
`selftest: 94/94 passed`, exit 0):

| literal | header carrier (`x_robots_tag_audit.py`, this round) | meta carrier (`meta_robots_audit.py`, round 78) |
|---|---|---|
| `Wed, 03 Dec 2025 13:09:53 GMT` | accepted, exit 0 | accepted, exit 0 |
| `Sunday, 06-Nov-94 08:49:37 GMT` | accepted, exit 0 (c33) | `invalid_value` + `unknown_directive`, exit 1 |
| `Sun Nov  6 08:49:37 1994` | accepted, exit 0 (c34) | `invalid_value`, exit 1 |
| `Sun Nov 16 08:49:37 1994, noindex` | accepted, `noindex` kept, exit 0 (c43) | date rejected, `noindex` kept, exit 1 |

The divergence is a frozen-scope difference, not a bug in either instrument: the header tool follows
RFC 9110 §5.6.7's three formats (this round's amendment A1-A2), while the meta tool's grammar is S449's
Google-accepted set as frozen by round-78 contract C3 and pinned by case `m25_rfc850_unimplemented_invalid`
— it declares RFC 850 unimplemented (`scripts/meta_robots_audit.py:74-78`, `:389`). Harmonizing them is
routed, not done: round-78's grammar, matrix and receipts are frozen. Any statement about
`unavailable_after` must therefore name its carrier.

## Limits

- No crawler is observed and no live property is measured; the entry is about what a recorded
  declaration may carry and what the offline audit decides.
- The two-digit RFC 850 year is accepted by shape only; RFC 9110:1924-1926's 50-year window rule is not
  implemented, so a `94` value is not resolved to a century.
- `date2`'s `2DIGIT` year and `date1`'s `4DIGIT` year are matched by count, not by calendar validity:
  `31 Feb 2025` matches the shape. The tool decides grammar, never whether a calendar date exists.
- Case sensitivity (S453:1914) is enforced for the fixed tokens the regexes spell; bot names keep the
  round-79 lower-casing rule, which is the lane's own reading.
