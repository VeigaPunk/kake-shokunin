source: S453 — RFC 9110 §5.6.7 Date/Time Formats — https://www.rfc-editor.org/rfc/rfc9110.txt — §5.6.7 lines 1837-1925 and §5.2 lines 1626-1633 of the retained plain text `.ufo/waves/round-80/sources/rfc9110.txt` (502,941 B, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, fetched 2026-11-04T10:44:53Z, HTTP 200); S433 — RFC 9110 §5.2 Field Lines and Combined Field Value, held row for the comma-concatenation rule; S452 — MDN, X-Robots-Tag header, held row for the `unavailable_after` value syntax (`.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.txt:209-212`, `:239`)
verified-at: 2026-11-04 — every quote below located by line in the retained bytes this round; one public GET, no rendered-DOM or crawler observation
recheck: 365d for S453 (an RFC changes only by a new publication); 90d for S452, a living page
ground: operability — the `unavailable_after` date grammar of `scripts/x_robots_tag_audit.py`, widened by `.ufo/waves/round-80/amendments/amendment-1.md`
scope: the date shapes a recorded `X-Robots-Tag: unavailable_after` value may carry and the comma rule that lets such a value survive field segmentation; not crawler behaviour, not any live property's declaration, not expiry semantics

# HTTP-date shapes, and the comma that breaks naive field splitting

## What the source fixes and what it leaves to the lane

RFC 9110 defines one date grammar, `HTTP-date`, in three formats and makes acceptance of all three a
requirement on a recipient that parses a timestamp in an HTTP field. Two of the three formats contain
a comma inside the value itself, and the same document says a comma that is data inside a member must
not be read as a list separator — so a parser that splits a field value on commas before deciding
what the value is will reject the values its own source shows.

| Fact | Source / retained `file:line` | Exact quote | Units |
|---|---|---|---|
| All three formats are accepted by a recipient | S453 `rfc9110.txt:1855-1856` | A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats. | 19 |
| The preferred format carries a comma after the day name | S453 `rfc9110.txt:1848` | Sun, 06 Nov 1994 08:49:37 GMT    ; IMF-fixdate | 9 |
| The obsolete RFC 850 format carries one too | S453 `rfc9110.txt:1852` | Sunday, 06-Nov-94 08:49:37 GMT   ; obsolete RFC 850 format | 9 |
| The asctime format does not | S453 `rfc9110.txt:1853` | Sun Nov  6 08:49:37 1994         ; ANSI C's asctime() format | 9 |
| A comma that is data must not be read as a separator | S453 `rfc9110.txt:1626-1630` | need to be treated with care if they are allowed as data within a member … such as within an HTTP-date | 21 |
| The date grammar is case sensitive | S453 `rfc9110.txt:1914` | HTTP-date is case sensitive. | 4 |
| `X-Robots-Tag` names the accepted value shapes | S452 `S452-mdn-x-robots-tag.txt:211-212` | A date must be specified in a format such as RFC 822, RFC 850, or ISO 8601. | 17 |
| The same page shows a comma-bearing value | S452 `S452-mdn-x-robots-tag.txt:239` | X-Robots-Tag: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT | 10 |

## The three shapes, verbatim ABNF

    IMF-fixdate  = day-name "," SP date1 SP time-of-day SP GMT            (S453:1873)
    rfc850-date  = day-name-l "," SP date2 SP time-of-day SP GMT          (S453:1902)
    date2        = day "-" month "-" 2DIGIT
    asctime-date = day-name SP date3 SP time-of-day SP year               (S453:1910)
    date3        = month SP ( 2DIGIT / ( SP 1DIGIT ) )                    (S453:1911)

Read structurally, three consequences follow and the lane's tool implements all three:

1. `IMF-fixdate` and `rfc850-date` each carry exactly one comma, immediately after the leading
   weekday token (`day-name` = `Mon`…`Sun`, `day-name-l` = `Monday`…`Sunday`). `asctime-date` carries
   none.
2. `date3` pads a single-digit day with a space inside the two-digit field (`Nov  6`), so an
   asctime value may contain two consecutive spaces — whitespace normalization that collapses runs
   would corrupt it.
3. A recipient that requires all three will accept a value that a comma-first splitter destroys.
   That is the defect the round-79 tool carried and this round's amendment removes.

## What the lane's tool accepts after amendment 1

`scripts/x_robots_tag_audit.py` now accepts, for `unavailable_after`, the four families in
`.ufo/waves/round-80/amendments/amendment-1.md` A1-A3:

| Family | Shape accepted | Ground |
|---|---|---|
| ISO 8601 | `YYYY-MM-DD` or `YYYY-MM-DD[ T]hh:mm[:ss][Z or ±hh:mm]` | S452:211-212 names ISO 8601 |
| IMF-fixdate | `Day, DD Mon YYYY hh:mm:ss GMT` | S453:1873; S452 names RFC 822, whose fixdate this is |
| RFC 850 | `Weekday, DD-Mon-YY hh:mm:ss GMT` | S453:1902; S452:211-212 |
| asctime | `Day Mon  D hh:mm:ss YYYY` | S453:1910-1911 |

The comma rule is the amendment's A1: a comma that immediately follows the leading weekday token of
an `unavailable_after` value belongs to the value; every other comma terminates the segment, as in
round 79. A value that matches no family stays `xrt_invalid_value` and is dropped, so a comma-bearing
value with a wrong zone yields `xrt_invalid_value` only, never `xrt_unknown_directive` (A3).

## Lane readings — marked, not sourced

- **asctime is accepted although S452 does not name it.** S452:211-212 names RFC 822, RFC 850 and
  ISO 8601; RFC 9110:1855-1856 requires a recipient of an HTTP-date to accept all three HTTP-date
  formats, asctime included. The lane follows the stricter recipient requirement and records the
  disagreement rather than hiding it. `[INFERENCE]`
- **A single space before a one-digit day is also accepted** (`Nov 6`), although `date3` requires
  `SP 1DIGIT` after the month's `SP`. This is a lenient reading, chosen so a space-collapsed
  transcript does not flip a value to invalid. `[INFERENCE]`
- **RFC 822 is read as its IMF-fixdate subset.** RFC 822 permits far more shapes (comments,
  folding, two-digit years in some forms); the lane accepts only the fixed-length subset RFC 9110
  calls `IMF-fixdate`, because that is the shape both sources exhibit. `[INFERENCE]`
- **ISO 8601 is not an HTTP-date.** S452 names it for this header; RFC 9110's `HTTP-date` production
  does not include it. The tool therefore accepts a union of two vocabularies, and the union is a
  lane policy, not a standard. `[INFERENCE]`

## Limits

- No crawler is observed and no live property is measured here; the entry is about what a recorded
  declaration may carry and what the offline audit decides.
- The two-digit RFC 850 year is accepted by shape only; RFC 9110:1924-1926's 50-year window rule is
  not implemented, so a `94` value is not resolved to a century.
- `date2`'s `2DIGIT` year and `date1`'s `4DIGIT` year are matched by count, not by calendar
  validity: `31 Feb 2025` matches the shape. The tool decides grammar, never whether a calendar date
  exists.
- Case sensitivity (S453:1914) is enforced for the fixed tokens the regexes spell; bot names keep the
  round-79 lower-casing rule, which is the lane's own reading.
