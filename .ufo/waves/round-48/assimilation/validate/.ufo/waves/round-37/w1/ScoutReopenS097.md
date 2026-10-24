# ScoutReopenS097 — live re-open of the 1994 document (freshness)

Item: GET https://www.robotstxt.org/orig.html myself; compare with retained `sources/S097.txt` and its receipt; quote the passages bearing on the C1 contract; list contradictions. Axes: freshness, operability. No sealed case, key or counter touched; `/fast/scratch/hyaku/kake-r37/` never listed or read.

## Access (observed)
- Fetch 2026-10-23T03:22:58Z; response `Date: Fri, 23 Oct 2026 03:22:59 GMT`; HTTP **200**; `curl -L` `%{url_effective}` = **https://www.robotstxt.org/orig.html** — same URL requested, no redirect. **Page did not move.**
- Apache/2.4.68 (Debian); Content-Length 10782; `Last-Modified: Sun, 03 May 2020 13:24:25 GMT`; ETag `"2a1e-5a4be554a2ea6"`.
- Body sha256 `446ea1521fc0d8eb3e0106c7f20e36b368aec795f4668773b6a8641ad120c1b2` = `receipts.json` S097.`bodySha256` = `bodyBytes` 10782; `S097.html.gz` decompresses to the same 10782 bytes, same sha. **Same page**, unchanged 32 min after the 02:50:51Z receipt.
- Text: retained `S097.txt` sha `a42aee4e…` **reproduced exactly** from the live body by the receipt's textRule, plus two details the rule text omits: each removed tag becomes a space (not empty), and the file ends in `\n`. Naive tag deletion gives 1039 words and `" /robots.txt "` where the page reads `"/robots.txt"` — quoting artifact only; token sequence identical, no content drift.
- Sandbox evidence: `/fast/scratch/hyaku/kake-r37w1/ScoutReopenS097/{live.html,headers_live.txt,retained.html}`, sha256 `446ea152…`, `39c86430bf83bccc8dde4df74279c0394079e16e42c72557b14a7831670fafd1`, `446ea152…`. Line cites below are the decompressed copy (411 lines; `#method` 183, `#format` 235, `#examples` 314, `#status` 130).

## Quotes (verbatim, ≤25 words, with section) and the C1 rule each bears on
1. **The Method** (l.189): "This file must be accessible via HTTP on the local URL "/robots.txt"." — fixes name and location only; it does **not** say the path is always allowed.
2. **User-agent** (l.282): "If the value is '*', the record describes the default access policy for any robot that has not matched any of the other records." — grounds (c)'s `*` fallback when no group matches.
3. **Disallow** (l.292): "This can be a full path, or a partial path; any URL that starts with this value will not be retrieved." — grounds (d)'s prefix match; read literally, `*` and `$` are ordinary characters.
4. **Examples** (l.294): "`Disallow: /help` disallows both `/help.html` and `/help/index.html`" — the one 1994 sentence that decides a contract case shape: a prefix may end mid-segment. Agrees with (d).
5. **User-agent** (l.277): "A case insensitive substring match of the name without version information is recommended." — bears on (c); **opposes** equality matching.
6. **User-agent** (l.284): "It is not allowed to have multiple such records in the "/robots.txt" file." — bears on (c); **opposes** combining every `*` group.
7. **The Format** (l.242): "The file consists of one or more records separated by one or more blank lines (terminated by CR,CR/NL, or NL)." — bears on (b)/(c) boundaries; **opposes** "blank lines do not count".
8. **The Format** (l.258): "The record starts with one or more User-agent lines, followed by one or more Disallow lines"; (l.260) "Unrecognised headers are ignored." — bears on (b) record keys; **opposes** `allow` being a record, and requires ≥1 Disallow per record (contract allows none).
9. **Disallow** (l.303): "Any empty value, indicates that all URLs can be retrieved." — bears on (d)'s "empty value never matches": same net result only when nothing else in the group matches.
10. **The Format** (l.245): "The field name is case insensitive." — agrees with (b)'s key comparison.
11. **Disallow** (l.309): "The presence of an empty "/robots.txt" file has no explicit associated semantics, it will be treated as if it was not present" — agrees with "no rules ⇒ allowed" for a 200 empty body; says nothing about HTTP status.
12. **Status of this document** (l.141): "It is not an official standard backed by a standards body, or owned by any commercial organisation." — S097 is self-declared non-normative; S011's abstract says it "specifies and extends" Koster's 1994 method, so **S011 governs every conflict** below.

Quotes 2 and 11 are in browser-rendered form; the retained `.txt` inserts spaces inside inline code (`' * '`, `" /robots.txt "`). All twelve strings were asserted as substrings of the live body's extracted text.

## Contradictions with C1 contract sentences (concrete divergence, all S011-governed)
- **(c) equality.** Group `googlebot`, check userAgent `Googlebot-News`: S097 substring-matches (Q5); contract matches only `*`. Differs whenever a version suffix exists.
- **(c) multiple `*`.** Contract combines every `*` group; Q6 forbids more than one. A file with two `*` groups has a contract result and no 1994 result.
- **(b) `allow` is a record / (d) allow wins ties.** Q8 makes `Allow:` an unrecognised header. On `Allow: /help.html` + `Disallow: /help`, S097 blocks /help.html (Q4); contract allows it.
- **(c) blank lines.** `User-agent: a`, blank, `User-agent: b`, `Disallow: /x`: S097 = two records, the first invalid (no Disallow), so `a` gets nothing; contract = one group {a,b} and blocks `/x` for `a`.
- **(d) wildcards/anchors.** `Disallow: /*.pdf$` blocks nothing under Q3's literal prefix; the contract blocks `*.pdf`. Every rule using `*` or `$` divides the readings.
- **(d) empty value.** With `Disallow:` and `Disallow: /` in one group, contract blocks all (empty never matches); Q9 reads as allow-all. Diverges only under the allow-all reading.
- **(f) validity.** Q8's "at least one Disallow field needs to be present in a record" is a validity rule the contract drops (a user-agent-only group is accepted, not `check_invalid`).
- **Silences (no 1994 basis, so no support claimed):** (c) "the rules of every matching group are combined" — 1994 gives each name one policy and never says what happens when two named records both match (only the `*` fallback half is grounded, Q2); (a) the 4xx/5xx split — status codes are never mentioned, and Q11 is about an *empty 200 body*, not absence; (e) query/fragment/percent-encoding and `/robots.txt`-always-allowed — silent, only "partial URL" plus bare-path examples; (b) the 500 KiB cap, BOM, U+FFFD — silent; (f)/(g) — no fault model at all.

## Bearing on the round (advisory)
S097 bears on two contract rules: (c)'s `*` fallback (not the combining) and (d)'s plain prefix matching (not wildcards or the allow tiebreak); it fixes the file's location but never connects it to (e)'s `/robots.txt`-always-allowed sentence. It contradicts seven listed sentences and is silent on status codes, limits, normalization and faults. The SCORECARD sentence "Sourced: S011 … S095 … S096 and S097 are opened this round as well" must not be read as S097 supporting (a), (d) wildcards, `Allow`, or equality matching.
Row recommendation for the Gate: S097 | robotstxt.org orig 1994 | historical | non-normative, superseded by S011 | supports location, `*` fallback, literal prefix; contradicts Allow, `*`/`$`, equality match, single-`*`, blank-line boundary; silent on status, limits, normalization, faults | HTTP 200, same URL, unchanged since 2020-05-03.

## Not verified / notes
- Did not fetch the plain-`http://` variant or archive snapshots; did not follow the page's dead link ("This code is no longer available", l.366). Footer still © 2007 — stale chrome, intact normative text.
- `corpus/SOURCES.md` at 4b089da ends at S094; no S095–S097 rows exist yet (Gate's call, not mine).
- No robots parsing run (source freshness item only); no sealed tree or C1 counter access; no tool installs.
