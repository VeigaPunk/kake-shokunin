# ReopenS113

Axes: freshness (one GET versus the row hash), clause accuracy of `teaches`. No tool installed. No counter (scout, not a control).

## Fetch

`timeout 90 curl -fsSL -D headers.txt -o /fast/scratch/hyaku/kake-r40w1/ReopenS113/xmlschema11-2.html -w … --max-time 60 --proto =https https://www.w3.org/TR/xmlschema11-2/` exit 0. HTTP 200, 0 redirects, final URL unchanged, 1,508,774 bytes, `text/html; charset=utf-8`. `date: Fri, 23 Oct 2026 08:37:51 GMT`. `last-modified: Tue, 09 Oct 2018 13:22:13 GMT`. `content-location: datatypes.html`. Canonical `https://www.w3.org/TR/xmlschema11-2/`. `sha256sum` exit 0: `cc2ae20cdeab02600c73fd13f1cc31dbbdd61f62aa455026fa84388b540443b8`. `cmp -s` against `.ufo/waves/round-39/sources/xmlschema11-2.html` and `.ufo/waves/round-40/sources/xmlschema11-2.html` both exit 0. The anchor hash holds. The re-fetch clock `2026-10-23T08:29:16Z` is not on this response; this GET is later and byte-identical.

## Productions

[16] `dateTimeLexicalRep` (`xmlschema11-2.html:3081-3084`, §3.3.7.2 `:3076`): `yearFrag '-' monthFrag '-' dayFrag 'T' ((hourFrag ':' minuteFrag ':' secondFrag) | endOfDayFrag) timezoneFrag?`. Regex `:3148-3152`: `-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]+)?|(24:00:00(\.0+)?))(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?`.

[18] `dateLexicalRep` (`:3348-3350`, §3.3.9.2 `:3341`): `yearFrag '-' monthFrag '-' dayFrag timezoneFrag?`. Regex `:3368`: `-?([1-9][0-9]{3,}|0[0-9]{3})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?`.

Timezone [63] `:10984-10987`: `'Z' | ('+' | '-') (('0' digit | '1' [0-3]) ':' minuteFrag | '14:00')`. `minuteFrag` [60] `:10977` is `[0-5] digit`. `endOfDayFrag` [62] `:10983` is `'24:00:00' ('.' '0'+)?`. `secondFrag` [61] `:10980` is two digits, fraction optional.

## teaches (`SOURCES.md:121`)

1. **supersedes S107 — holds.** S107 (`SOURCES.md:115`) attributes `24:00:00` and required seconds to both types. [18] has no time part; [16] does.

2. **both allow an absent timezone — holds.** `timezoneFrag?` on [16] (`:3084`) and [18] (`:3350`). dateTime: "no properties except timezoneOffset permitted to be absent. The timezoneOffset property remains optional." (`:2992-2996`). date: "hour, minute, and second required to be absent. timezoneOffset remains optional." (`:3305-3308`).

3. **offsets only to ±14:00 — holds** as a bound, not "the only offsets are ±14:00". Shared tail is `Z` or ±(`00`–`13`:`00`–`59` | `14:00`) at `:3152`, `:3368`, and [63]. `+14:30` is out. `Z` is in as `'00:00'` (`:3121-3122`). The canonical-fragment argument is an integer between −840 and 840 inclusive (`:13295`).

4. **`24:00:00` belongs to dateTime, not date — holds.** [62] and the dateTime regex (`:3151`); absent from [18] and `:3368`. [62] also allows a `.0+` fraction.

5. **required seconds belong to dateTime, not date — holds.** [16]'s first alternative includes `secondFrag` (not optional); the other is `endOfDayFrag`, which contains `:00`. date requires second absent (`:3305-3307`). The fraction is optional (`:10980`), so "seconds" is the two-digit field.

6. **sentences 28–30 are a W3C-profile lane reading that departs from the schema type S103 names — holds.** Sentence 28 (`c1-contract.md:74-76`) lists complete-date W3C forms, including `YYYY-MM-DDThh:mmTZD` and TZD hours 00–23. Sentence 29 (`:76-77`) caps hh at 23, so `24:00:00` is out. Only sentence 30 (`:77-80`) is labeled "Lane reading" (a time without TZD is invalid). S103's type is `tLastmod`, an empty-restriction union of `xsd:date` and `xsd:dateTime` (`sitemap.xsd:66-72`; same bases `siteindex.xsd:66` and `:69`). That union allows a missing timezone, a timezone on a date, `24:00:00`, and ±14:00, and dateTime requires seconds. The block rejects the first three and allows `hh:mm` without seconds and TZD hours through 23. `sitemap.xsd:59-60` names NOTE-datetime; the schema type is the union.

7. **the decimal pattern equals sentence 32's — holds** as the same language, not the same spelling. Page `:2503` is `(\+|-)?([0-9]+(\.[0-9]*)?|\.[0-9]+)`. Sentence 32 (`c1-contract.md:84-85`) is `[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)`. Sign group versus class; the matched strings are the same. The canonical mapping is stricter (`:2508-2512`); sentence 32 cites the lexical form.

No clause wrong. The page string `xsd:` occurs 0 times; the prefix is S103's (`sitemap.xsd:68`, `:71`).
