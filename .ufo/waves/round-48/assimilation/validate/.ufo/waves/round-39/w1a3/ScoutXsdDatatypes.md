# ScoutXsdDatatypes — XSD 1.1 decimal, date, dateTime

Axes: operability (one GET, retained bytes, line quotes) and freshness (UTC access, HTTP status, sha256). No tool installed. Row not appended to `corpus/SOURCES.md` (S104 is the last registry row read; S105 is only proposed).

## Fetch

`curl -fsSL -D headers.txt -o xmlschema11-2.html -w 'http_code=%{http_code}...' --max-time 120 https://www.w3.org/TR/xmlschema11-2/` then `sha256sum` and `wc`. Exit 0. HTTP 200, 0 redirects, `content-location: datatypes.html`, `last-modified: Tue, 09 Oct 2018 13:22:13 GMT` (server header, not an edition date). Access 2026-10-23T06:53:18Z. 15908 lines, 1508774 bytes. sha256 `cc2ae20cdeab02600c73fd13f1cc31dbbdd61f62aa455026fa84388b540443b8`. Path `/fast/scratch/hyaku/kake-r39a3w1/ScoutXsdDatatypes/xmlschema11-2.html`. Document title line 329, "W3C Recommendation 5 April 2012" line 330, this-version `http://www.w3.org/TR/2012/REC-xmlschema11-2-20120405/` line 331.

## Draft SOURCES row (contract v1; not written to the registry)

Quote grounding `teaches` (11 words), lines 3116–3117: "timezoneFrag, if present, specifies an offset between UTC and local time."

| S105 | W3C XML Schema Definition Language (XSD) 1.1 Part 2: Datatypes — https://www.w3.org/TR/xmlschema11-2/ | spec | A | Lexical space of xsd:decimal, xsd:date and xsd:dateTime (optional timezone, year numerals, 24:00:00); not NOTE-datetime and not the lane lastmod reading in sentences 28–30 | §§3.3.3.1, 3.3.7.2, 3.3.9.2 and §5.4; W3C Recommendation 5 April 2012; fetched 2026-10-23T06:53:18Z, HTTP 200, retained HTML sha256 cc2ae20cdeab02600c73fd13f1cc31dbbdd61f62aa455026fa84388b540443b8 | xsd:date and xsd:dateTime allow a missing timezone, a year outside four unsigned digits, and 24:00:00 as the next day's first moment, all rejected by sentences 28–30 | queued | 2026-10-23 | 365d | — |

## Where the spec differs from sentences 28–30

Observed in the retained HTML. Sentence numbers are `c1-contract.md`.

- Timezone optional, contradicts sentence 30. `dateTimeLexicalRep` ends `timezoneFrag?` (line 3084); `dateLexicalRep` the same (line 3350). Value space: "The timezoneOffset property remains optional" (lines 2995–2996). `dateTimeLexicalMap` sets tz absent when T is absent (lines 12867–12869). A bare date may also carry a timezone (`2005-05-10Z` matches line 3368); sentence 28's date form is only `YYYY-MM-DD`.
- Offset range is not sentence 28's hh 00–23. Line 3152: `(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?`. `+15:00` and `+14:30` match sentence 28 and fail this. `newDateTime` takes Tz from −840 to 840 minutes (line 12508).
- `24:00:00` is lexical, contradicts sentence 29's hh 00–23. Line 3151 includes `(24:00:00(\.0+)?)`. Quote (14 words), lines 3115–3116: "represent midnight of the day, which is the first moment of the next day." `dateTimeLexicalMap` calls `newDateTime(..., 24, 0, 0, tz)` (lines 12876–12877). `newDateTime` allows hour 0–24 (line 12500) and `normalizeMinute` adds `hr div 24` to the day (line 12429). Only `.0+` fractions, not `24:00:00.5` (line 10983).
- Seconds are required on `dateTime`, so sentence 28's `YYYY-MM-DDThh:mmTZD` is not an XSD `dateTime`. The non-end-of-day alternative is hour, minute, and second (line 3083); `secondFrag` is two digits or two digits, a point, and one or more digits (lines 3109–3112).
- Year range is wider than four unsigned digits. Quote (17 words), lines 3098–3099: "yearFrag is a numeral consisting of at least four decimal digits, optionally preceded by a minus sign". No leading `+` (line 10960). Quote (9 words), line 3011: "First, year is permitted to have the value zero." Year 0000 is a leap year (lines 3021–3023). §5.4 is a floor, not a cap: minimally conforming processors must support nonnegative years less than 10000 (lines 8925–8928) and must not treat a value past capacity as invalid (lines 8903–8907).

## What does not differ

- Leap seconds: "the date/time types described here do not include leap-second values" (line 14832). Agrees with sentence 29's ss 00–59. The day-of-month rule (lines 3035–3044) is the proleptic Gregorian rule sentence 29 names only as "leap years included"; year 0 is specified here and unspoken there.
- Sentence 32's decimal pattern is the same language as line 2503, `(\+|-)?([0-9]+(\.[0-9]*)?|\.[0-9]+)` (sign class versus group). "the number 2.0 is not distinct from the number 2.00" (line 2467) grounds "exact decimal". The canonical mapping is stricter (lines 2508–2525); sentence 32 cites the lexical form. `dateTimeStamp` (§3.4.28, lines 5627–5634) does require a timezone, but S103 `tLastmod` is `xsd:date` union `xsd:dateTime`, not `dateTimeStamp`.

## Unresolved

Line 335 points at `https://www.w3.org/XML/XMLSchema/v1.1/1e/errata.html` and says it may include normative corrections. That URL was not fetched. Confidence on the quotes above: high for this byte string.
