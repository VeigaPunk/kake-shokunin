# ReopenS107

Axes: operability (one GET, hash, locate every scope/anchor/teaches claim). No tool installed.

## Fetch

`timeout 90 curl -fsSL -D headers.txt -o xmlschema11-2.html -w … --max-time 60 --proto =https https://www.w3.org/TR/xmlschema11-2/` exit 0. HTTP 200, 0 redirects, final URL unchanged, 1508774 bytes, `text/html; charset=utf-8`. Response `date: Fri, 23 Oct 2026 07:46:49 GMT`. `last-modified: Tue, 09 Oct 2018 13:22:13 GMT`. `content-location: datatypes.html`. Canonical `https://www.w3.org/TR/xmlschema11-2/`.

`sha256sum` exit 0 and `cmp -s` exit 0. Live `/fast/scratch/hyaku/kake-r39a3w2/ReopenS107/xmlschema11-2.html` and retained `.ufo/waves/round-39/sources/xmlschema11-2.html` are both `cc2ae20cdeab02600c73fd13f1cc31dbbdd61f62aa455026fa84388b540443b8` (row anchor; `sources/SHA256SUMS:9`). Byte-identical, so no visible-text diff. The row clock `2026-10-23T06:56:39Z` is not on the page; `corpus/lessons/round-39.md:35` and `:43` record the L1 re-open at 06:56:39Z. This run did not re-observe that clock.

## Cells

**scope — holds.** Lexical spaces: "The lexical space of decimal is the set of lexical representations…" `xmlschema11-2.html:2499-2503` under §3.3.3.1 (`:2473-2474`); dateTime §3.3.7.2 (`:3076`, production `:3083-3084`); date §3.3.9.2 (`:3341`, production `:3350`). Page names are unprefixed `decimal` (`:2450`), `dateTime` (`:2985`), `date` (`:3293`); the string `xsd:` occurs 0 times. Not NOTE-datetime: title `:329` is "W3C XML Schema Definition Language (XSD) 1.1 Part 2: Datatypes"; `NOTE-datetime` count 0. S104 is a different URL. Not the lane `lastmod` reading: `lastmod` count 0, and the lexical rules below differ from sentences 28–30.

**anchor — holds.** §3.3.3.1 `:2473`, §3.3.7.2 `:3076`, §3.3.9.2 `:3341`, §5.4 "Partial Implementation of Infinite Datatypes" `:8882` (a capacity floor, not a fourth grammar: decimal sixteen digits `:8918-8924`; nonnegative years less than 10000 `:8924-8928`). "W3C Recommendation 5 April 2012" verbatim `:330` (count 2). HTTP 200 and the backtick SHA256 match this GET and the retained file. Link text at `:332` is `http://www.w3.org/TR/xmlschema11-2/`; the href and this GET's canonical are `https`.

**teaches — overstated.**
- "allow no timezone" holds as "a timezone may be absent", not as "timezones are forbidden". `timezoneFrag?` at `:3084` (dateTime) and `:3350` (date). "The timezoneOffset property remains optional" `:2995-2996`; date the same `:3307-3308`. Both regexes still accept `Z` and numeric offsets (`:3152`, `:3368`).
- "offsets only to ±14:00" holds as a bound. `timezoneFrag` [63] `:10986-10987` is `Z` or ±(`00`–`13`:`minuteFrag` | `14:00`). Same class at `:3152` and `:3368`. `+14:30` is out; `Z` and `±00:00`–`±13:59` are in. Not "the only offsets are ±14:00".
- "`24:00:00`" and "require seconds" do not hold of `xsd:date`. `endOfDayFrag` [62] is `'24:00:00'` plus optional `.0` (`:10983`); the dateTime regex includes it (`:3151`). `dateLexicalRep` (`:3350`, regex `:3368`) is year-month-day plus optional timezone and has no time. dateTime's other alternative is hour, minute, and `secondFrag` (`:3083`); `secondFrag` is two digits, fraction optional (`:3109-3112`, `:10980`). date requires hour, minute, and second to be absent (`:3305-3307`).
- "sentences 28–30 are a W3C-profile lane reading that departs from the schema type S103 names" holds. Sentence 28 (`c1-contract.md:74-76`) lists complete-date W3C Datetime forms, including `YYYY-MM-DDThh:mmTZD` and TZD hours 00–23. Sentence 29 (`:76-77`) caps hh at 23, so `24:00:00` is out. Only sentence 30 (`:77-80`) is labeled "Lane reading"; it rejects a time without TZD. S103 names `tLastmod`. `sitemap.xsd:66-72` is an empty-restriction union of `xsd:date` and `xsd:dateTime` (same bases `siteindex.xsd:66` and `:69`). Those bases allow a missing timezone, `24:00:00`, and ±14:00, and dateTime requires seconds, so the block departs from that type. S103's documentation (`sitemap.xsd:59-60`) names NOTE-datetime; the row's "schema type" is the union, not that prose.
- "the decimal pattern equals sentence 32's" holds as the same language, not the same spelling. Sentence 32 (`c1-contract.md:84-85`) is `[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)`. The page (`:2503`) is `(\+|-)?([0-9]+(\.[0-9]*)?|\.[0-9]+)`. Sign class versus group; the matched strings are the same. The canonical mapping is stricter (`:2508-2512`); sentence 32 cites the lexical form.

**Quoted phrases.** No double-quoted spec sentence in the three cells. `24:00:00` is verbatim (`:10983`, `:3151`; 6 hits). `xsd:decimal`, `xsd:date`, `xsd:dateTime`, and `lastmod` are not page text. The appendix uses `xs:decimal` and `xs:dateTime` once each (`:10435`, `:10582`), never `xs:date`. The `xsd:` prefix is S103's (`sitemap.xsd:68`, `:71`). The backtick SHA256 matches the file. The lesson gate quote (`round-39.md:43`) is the words at `:3116-3117`, with a newline between "an" and "offset".

**Sentence numbers.** 28, 29, 30, and 32 say what the row says they say. The overstatement is attributing `24:00:00` and required seconds to `xsd:date` as well as `dateTime`.

Errata link at `:335` was not fetched (one GET only).
