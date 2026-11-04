# ScoutSources — round 77, wave w1

Scope: open, from scratch, the three sources the frozen C2 contract sentences rest on, retain the bytes, and
draft the three registry rows. Base revision `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`; lane root
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Nothing in `corpus/` was written; the L1 applies the rows.

## 1. Fetches (observed, 2026-11-03)

Command, run once per source from `.ufo/waves/round-77/w1/ScoutSources/`:

```sh
curl -sSL --max-time 30 -o <name>.raw -w '%{http_code} %{url_effective} %{size_download}\n' <url>
```

| source | HTTP | final URL | bytes (`%{size_download}` = `ls -l`) | sha256 | raw retained as |
|---|---|---|---|---|---|
| S012 candidate — sitemaps.org protocol | 200 | https://www.sitemaps.org/protocol.html | 45,292 | `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654` | `ScoutSources/protocol.raw` (`protocol.meta`) |
| S447 candidate — RFC 1952 | 200 | https://www.rfc-editor.org/rfc/rfc1952.txt | 25,037 | `164ef0897b4cbec63abf1b57f069f3599bd0fb7c72c2a4dee21bd7e03ec9af67` | `ScoutSources/rfc1952.raw` (`rfc1952.meta`) |
| S448 candidate — RFC 4287 | 200 | https://www.rfc-editor.org/rfc/rfc4287.txt | 81,922 | `3bd71d76289560c9e860151f39cebbdc402cfd8b788a62048d8dc42824f2d89c` | `ScoutSources/rfc4287.raw` (`rfc4287.meta`) |

No redirect occurred: `%{url_effective}` equals the requested URL in all three `*.meta` files.

**Observed:** today's protocol.html sha256 `5e7570590fcb92d4…` is byte-identical to the SHA256 S102 recorded
on 2026-10-23 (`corpus/SOURCES.md` line 110, anchor cell: "retained HTML SHA256
`5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654`"), and the page still prints
`Last Updated: Monday, November 21, 2016` (`protocol.txt` line 891). The page has not changed in the 11 days
between those fetches, which is why every round-77 quote below re-derives from today's bytes.

## 2. Strip recipe and text hashes

Script: `ScoutSources/strip.py` (recipe documented in its module docstring). Run:

```sh
python3 -B strip.py | tee strip-output.txt
```

HTML recipe (summary): drop `<script>`/`<style>`; newline for `</p>` `</li>` `</h1-6>` `</tr>` `</pre>`
`</div>` `</dt>` `</dd>` `</table>` `</ul>` `</ol>` and `<br>`; `- ` prefix for `<li>`; remove remaining
tags; `html.unescape`; NBSP to space; collapse `[ \t]+` to one space and strip each line; collapse blank-line
runs to one.
RFC text recipe (summary): CRLF to LF; `\f` page break to newline; drop the running footer `… [Page N]` and
running header `RFC NNNN … Month YYYY`; join the two text lines across a removed page break with one space
(no de-hyphenation); same per-line whitespace tidy. Line numbers cited in this report and in the rows are
1-based lines of the `.txt` renderings.

| text | bytes | lines | sha256 |
|---|---|---|---|
| `protocol.txt` | 21,645 | 893 | `e611779a3887422f8c9968620eaec42b56f57a0ca4c2ca19836fe5dab910e80e` |
| `rfc1952.txt` | 19,375 | 572 | `175eed73d4cf835ed933c35689241063671ad3847259af0654ee46508749aeb1` |
| `rfc4287.txt` | 67,198 | 1,989 | `c325fe7899e13abc708ddd54d691cbbbdbd1e3585484e216dffcfab32c3d086c` |

Raw hashes are unchanged by stripping: `strip-output.txt` prints each raw sha256 beside its text sha256, and
they equal the fetch table above.

## 3. Quotes (all ≤25 words, all mechanically re-found)

`quotes.json` holds the machine form; `verify_quotes.py` produced these spans.

| quote id | file | lines | w | quote |
|---|---|---|---|---|
| S012-gzip-compress | protocol.txt | 353-355 | 17 | "If you would like, you may compress your Sitemap files using gzip to reduce your bandwidth requirement" |
| S012-gzip-decompressed-limit | protocol.txt | 355-357 | 12 | "however the sitemap file once uncompressed must be no larger than 50MB" |
| S012-xml-entry-and-size-limit | protocol.txt | 349-351 | 22 | "each Sitemap file that you provide must have no more than 50,000 URLs and must be no larger than 50MB (52,428,800 bytes)" |
| S012-index-limit-and-compression | protocol.txt | 363-365 | 23 | "Sitemap index files may not list more than 50,000 Sitemaps and must be no larger than 50MB (52,428,800 bytes) and can be compressed" |
| S012-index-loc-kind | protocol.txt | 457 | 16 | "This location can be a Sitemap, an Atom file, RSS file or a simple text file." |
| S012-feed-formats | protocol.txt | 493 | 15 | "You can provide an RSS (Real Simple Syndication) 2.0 or Atom 0.3 or 1.0 feed." |
| S012-feed-link-field | protocol.txt | 509 | 6 | "<link> field - indicates the URL" |
| S012-feed-modified-date | protocol.txt | 511-513 | 16 | "modified date field (the <pubDate> field for RSS feeds and the <updated> date for Atom feeds)" |
| S012-feed-modified-date-optional | protocol.txt | 513-515 | 8 | "Use of the modified date field is optional." |
| S012-text-one-url-per-line | protocol.txt | 523 | 16 | "The text file must have one URL per line. The URLs cannot contain embedded new lines." |
| S012-text-fully-specify-urls | protocol.txt | 525 | 8 | "You must fully specify URLs, including the http." |
| S012-text-count-and-size-limit | protocol.txt | 527-529 | 19 | "Each text file can contain a maximum of 50,000 URLs and must be no larger than 50MB (52,428,800 bytes)." |
| S012-text-utf8 | protocol.txt | 533 | 7 | "The text file must use UTF-8 encoding." |
| S012-text-no-other-information | protocol.txt | 539 | 13 | "The text file should contain no information other than the list of URLs." |
| S012-text-no-header-footer | protocol.txt | 541 | 10 | "The text file should contain no header or footer information." |
| S012-text-gzip | protocol.txt | 543-545 | 18 | "If you would like, you may compress your Sitemap text file using gzip to reduce your bandwidth requirement." |
| S012-text-name-anything | protocol.txt | 547 | 9 | "You can name the text file anything you wish." |
| S012-text-rfc3986 | protocol.txt | 547-551 | 23 | "You can name the text file anything you wish. Please check to make sure that your URLs follow the RFC-3986 standard for URIs" |
| S447-gzip-magic | rfc1952.txt | 240-241 | 24 | "These have the fixed values ID1 = 31 (0x1f, \037), ID2 = 139 (0x8b, \213), to identify the file as being in gzip format." |
| S447-crc32 | rfc1952.txt | 352-353 | 16 | "This contains a Cyclic Redundancy Check value of the uncompressed data computed according to CRC-32 algorithm" |
| S447-isize | rfc1952.txt | 360-361 | 12 | "This contains the size of the original (uncompressed) input data modulo 2^32." |
| S447-decompressor-header-check | rfc1952.txt | 395-397 | 21 | "A compliant decompressor must check ID1, ID2, and CM, and provide an error indication if any of these have incorrect values." |
| S448-atom-link-href | rfc4287.txt | 943-944 | 21 | "The \"href\" attribute contains the link's IRI. atom:link elements MUST have an href attribute, whose value MUST be a IRI reference" |
| S448-atom-updated-definition | rfc4287.txt | 1138-1139 | 17 | "a Date construct indicating the most recent instant in time when an entry or feed was modified" |
| S448-atom-updated-may-change | rfc4287.txt | 1145 | 10 | "Publishers MAY change the value of this element over time." |
| S448-atom-date-construct-rfc3339 | rfc4287.txt | 429-430 | 16 | "A Date construct is an element whose content MUST conform to the \"date-time\" production in [RFC3339]." |
| S448-entry-updated-exactly-one | rfc4287.txt | 612 | 8 | "atom:entry elements MUST contain exactly one atom:updated element." |

Section anchors these quotes sit in: protocol.txt `Using Sitemap index files (to group multiple sitemap files)`
lines 345-369; `<loc>` row of the sitemap-index tag table 451-457; `Other Sitemap formats` 481; `Syndication
feed` 491-515; `Text file` 517-559. rfc1952.txt `2.3. Member format` 195 and `2.3.1. Member header and
trailer` 236-400 (`2.3.1.2. Compliance` 387). rfc4287.txt `3.3. Date Constructs` 427, `4.1.2. The
"atom:entry" Element` 543 (rules 586-612), `4.2.7.` 923 / `4.2.7.1.` 941, `4.2.15.` 1136.

### 3a. Stripped-to-raw crosswalk

`python3 -B crosswalk.py > crosswalk-output.txt` (same collapsed-whitespace matcher, searching the raw fetch)
prints `quotes=27 raw_matched=24 raw_escaped=3`: 24 quotes are also contiguous in the raw bytes, 3 contain a
character the HTML escapes (`<link>`, `<pubDate>`, `<updated>`, RFC 3986 link text) and so exist only in the
stripped rendering.

| quote id | stripped lines | raw lines |
|---|---|---|
| S012-gzip-compress | 353-355 | 691-693 |
| S012-gzip-decompressed-limit | 355-357 | 693-695 |
| S012-xml-entry-and-size-limit | 349-351 | 687-689 |
| S012-index-limit-and-compression | 363-365 | 703-705 |
| S012-index-loc-kind | 457 | 885 |
| S012-feed-formats | 493 | 957 |
| S012-feed-link-field | 509 | raw:escaped |
| S012-feed-modified-date | 511-513 | raw:escaped |
| S012-feed-modified-date-optional | 513-515 | 979-981 |
| S012-text-one-url-per-line | 523 | 997 |
| S012-text-fully-specify-urls | 525 | 999 |
| S012-text-count-and-size-limit | 527-529 | 1001-1003 |
| S012-text-utf8 | 533 | 1007 |
| S012-text-no-other-information | 539 | 1013 |
| S012-text-no-header-footer | 541 | 1015 |
| S012-text-gzip | 543-545 | 1017-1019 |
| S012-text-name-anything | 547 | 1021 |
| S012-text-rfc3986 | 547-551 | raw:escaped |
| S447-gzip-magic | 240-241 | 291-292 |
| S447-crc32 | 352-353 | 420-421 |
| S447-isize | 360-361 | 428-429 |
| S447-decompressor-header-check | 395-397 | 470-472 |
| S448-atom-link-href | 943-944 | 1159-1160 |
| S448-atom-updated-definition | 1138-1139 | 1385-1386 |
| S448-atom-updated-may-change | 1145 | 1392 |
| S448-atom-date-construct-rfc3339 | 429-430 | 549-550 |
| S448-entry-updated-exactly-one | 612 | 761 |

**Convention note (cross-artefact).** `corpus/knowledge/sitemap-formats.md` (another seat's file, read-only
here) states at its lines 11-12 that its `S012`/`S447`/`S448` line numbers are *raw* offsets
(`protocol.raw`, `rfc1952.raw`, `rfc4287.raw`), while the registry rows above cite *tag-stripped* lines as
this seat's spec requires. The two are consistent — its `protocol.raw:693-695` is this row's
`protocol.txt:355-357`, and its `protocol.raw:691-692` is the same sentence as `protocol.txt:353-355` — but a
reader who moves a number from one artefact to the other must cross through this table.

## 4. Required-coverage matrix

| required fact | carried by | status |
|---|---|---|
| gzip compression is permitted | S012-gzip-compress 353-355; S012-text-gzip 543-545; S012-index-limit-and-compression 363-365 | verbatim |
| limit applies to the **decompressed** size | S012-gzip-decompressed-limit 355-357 ("once uncompressed must be no larger than 50MB") | verbatim |
| text sitemap: one URL per line, no embedded newline | S012-text-one-url-per-line 523 | verbatim |
| text sitemap: fully specified URLs | S012-text-fully-specify-urls 525 | verbatim for the scheme; **authority is inference** — see finding 2 |
| text sitemap: UTF-8 | S012-text-utf8 533 | verbatim |
| text sitemap: ≤50,000 URLs and ≤52,428,800 bytes | S012-text-count-and-size-limit 527-529 | verbatim |
| text sitemap: no other information, no header/footer | S012-text-no-other-information 539 + S012-text-no-header-footer 541 | verbatim (two separate items) |
| RSS 2.0 `<link>` and `<pubDate>` | S012-feed-link-field 509 + S012-feed-modified-date 511-513 (+ optional at 513-515) | verbatim |
| Atom 1.0 `<updated>` | S012-feed-modified-date 511-513 + S012-feed-modified-date-optional 513-515 | verbatim |
| Atom 1.0 `<link href>` | S448-atom-link-href 943-944 | **composition**: sitemaps.org names only "the `<link>` field"; `href` is RFC 4287's requirement — finding 1 |
| sitemap-index `<loc>` may name a Sitemap, Atom, RSS or text file | S012-index-loc-kind 457 | verbatim |
| RFC 1952 magic | S447-gzip-magic 240-241 | verbatim |
| RFC 1952 CRC-32 and input size | S447-crc32 352-353; S447-isize 360-361 | verbatim |
| RFC 1952 bad-header handling | S447-decompressor-header-check 395-397 | verbatim |
| RFC 4287 `atom:link` `href` | S448-atom-link-href 943-944 | verbatim |
| RFC 4287 `atom:updated` | S448-atom-updated-definition 1138-1139; S448-atom-date-construct-rfc3339 429-430; S448-entry-updated-exactly-one 612 | verbatim |

Primary `## Gate` quote per row (candidate, scribe's choice): S012 → S012-gzip-decompressed-limit (12 words);
S447 → S447-gzip-magic (24 words); S448 → S448-atom-link-href (21 words).

## 5. Drafted registry rows

Single line each, 11 columns, no literal or escaped `|` inside any cell. S012 is an in-place update: every
cell is reproduced byte-exact from `corpus/SOURCES.md` line 20 except `used-by` (anchor/scope/teaches may only
change through a superseding row — rule stated at the file's append-only correction notes).

Update line (for `corpus/lessons/round-77.md`):

> **corpus/SOURCES.md S012 used-by**: `corpus/knowledge/crawl-scope-per-host.md` → `corpus/knowledge/crawl-scope-per-host.md, corpus/knowledge/sitemap-formats.md, corpus/lessons/round-77.md`. Status `mined`, recheck `365d`, opened `2026-10-19` unchanged.

```
| S012 | sitemaps.org: Sitemaps XML format — https://www.sitemaps.org/protocol.html | spec | A | Sitemap file location and the URLs it can list | Sitemap file location section; fetched 2026-10-19 | A sitemap's location limits the set of URLs it may include | mined | 2026-10-19 | 365d | corpus/knowledge/crawl-scope-per-host.md, corpus/knowledge/sitemap-formats.md, corpus/lessons/round-77.md |
| S447 | RFC 1952 — GZIP file format specification version 4.3 — https://www.rfc-editor.org/rfc/rfc1952.txt | spec | A | The gzip member container framing — the ID1/ID2 magic, the CM byte and the CRC32/ISIZE trailer, and the header checks a decompressor must make — not the DEFLATE block encoding, not any implementation's error text, not a size limit | 2.3. Member format header diagram and 2.3.1. Member header and trailer, tag-stripped lines 195-241 (ID1/ID2 fixed values 238-241); trailer CRC32 and ISIZE 351-361; 2.3.1.2. Compliance 387-400; title page lines 1-5; RFC 1952, May 1996; fetched 2026-11-03, HTTP 200, 25,037 bytes, sha256 164ef0897b4cbec63abf1b57f069f3599bd0fb7c72c2a4dee21bd7e03ec9af67, retained at .ufo/waves/round-77/w1/ScoutSources/rfc1952.txt | A gzip member starts with the fixed bytes 0x1f 0x8b and ends with a CRC-32 of the uncompressed data plus its input size modulo 2^32, so a container is recognised and checked without trusting its name | mined | 2026-11-03 | 365d | corpus/knowledge/sitemap-formats.md, corpus/lessons/round-77.md |
| S448 | RFC 4287 — The Atom Syndication Format — https://www.rfc-editor.org/rfc/rfc4287.txt | spec | A | The atom:link href requirement and the atom:updated Date construct as Atom 1.0 defines them — not RSS, not Atom 0.3, not feed validity beyond these two elements | 4.2.7. The "atom:link" Element 923-945 (href MUST sentence 943-945); 3.3. Date Constructs 427-433; 4.2.15. The "atom:updated" Element 1136-1145; 4.1.2. entry rule 612; RFC 4287, December 2005; fetched 2026-11-03, HTTP 200, 81,922 bytes, sha256 3bd71d76289560c9e860151f39cebbdc402cfd8b788a62048d8dc42824f2d89c, retained at .ufo/waves/round-77/w1/ScoutSources/rfc4287.txt | An Atom entry's URL is the required href attribute of its atom:link element, and its modified instant is the atom:updated Date construct written as an RFC 3339 date-time | mined | 2026-11-03 | 365d | corpus/knowledge/sitemap-formats.md, corpus/lessons/round-77.md |
```

Optional second update, L1's call (not part of the frozen frontier step): S102 already carries the broad
scope these sentences use (`corpus/SOURCES.md` line 110, scope cell: "… 50,000-entry and 52,428,800-byte
limits, `loc` form and location scope …"), and its `used-by` is only `corpus/lessons/round-39.md`. If
`sitemap-formats.md` cites S102 as well, the matching line is:

> **corpus/SOURCES.md S102 used-by**: `corpus/lessons/round-39.md` → `corpus/lessons/round-39.md, corpus/knowledge/sitemap-formats.md, corpus/lessons/round-77.md`.

## 6. Mechanical checks

All commands below run from `.ufo/waves/round-77/w1/ScoutSources/` with
`TMPDIR=/fast/scratch/hyaku/kake-r77/ScoutSources/tmp`, `python3 -B`. The scripts need no scratch; the
TMPDIR directory was removed at seat close, and every receipt it produced is copied below into this
`ScoutSources/` directory.

1. Quotes — `python3 -B verify_quotes.py > verify-output.txt`, exit 0; tail of `verify-output.txt`:

   ```
   S012-text-rfc3986 file=protocol.txt lines=547-551 words=23 ok
   quotes=27 failures=0
   ```

   Every quote matched exactly once (`occurrences` check), none exceeded 25 words, none contained a pipe.
   Full per-quote lines in `verify-output.txt`.
2. Rows — `python3 -B check_rows.py > check-rows-output.txt`, exit 0; full output:

   ```
   S012 changed columns: ['used-by']
   S012 old used-by: corpus/knowledge/crawl-scope-per-host.md
   S012 new used-by: corpus/knowledge/crawl-scope-per-host.md, corpus/knowledge/sitemap-formats.md, corpus/lessons/round-77.md
   S447 anchor cell: 2.3. Member format header diagram and 2.3.1. Member header and trailer, tag-str…
   S448 anchor cell: 4.2.7. The "atom:link" Element 923-945 (href MUST sentence 943-945); 3.3. Date C…
   rows=3 cells=11 s012_changed=used-by
   ```

   Each row splits into exactly 11 non-empty cells; the drafted S012 row differs from
   `corpus/SOURCES.md` line 20 in exactly one cell (`used-by`), every other cell byte-identical; no cell
   contains an escaped pipe, and a literal pipe inside a cell would break the 11-cell count.
3. Crosswalk — `python3 -B crosswalk.py > crosswalk-output.txt`, exit 0; last line
   `quotes=27 raw_matched=24 raw_escaped=3` (table in §3a).

## 7. Findings for C2's authors (evidence-backed)

1. **sitemaps.org never says `<link href>`.** The page says "<link> field - indicates the URL"
   (`protocol.txt` 509) for feeds generally and "<updated> date for Atom feeds" (511-513). The `href`
   requirement for `atom:link` is RFC 4287 §4.2.7.1 (`rfc4287.txt` 943-944). F2 and case a02 therefore rest
   on S012 **and** S448; citing S012 alone would be an over-claim. The `atom:link` element in Atom carries no
   text content (`rfc4287.txt` 925-927), which is why a link with no `href` has no URL at all.
2. **"Fully specified (scheme + authority)" is only half verbatim.** The source says "You must fully specify
   URLs, including the http." (`protocol.txt` 525) and points at RFC 3986/3987 (547-551). The scheme is named;
   an authority requirement is an inference from "fully specify" plus the page's absolute examples. Case t03
   (`/page` relative) is defensible but its row must not quote the source as if it named the authority.
3. **The decompressed-size sentence is exact.** "however the sitemap file once uncompressed must be no larger
   than 50MB" (355-357) — G1's reading is verbatim, and the same paragraph's index sentence adds that index
   files "can be compressed" (363-365), while text files "may compress … using gzip" (543-545). The
   decompressed reading therefore applies to all three gzip-capable containers the page names.
4. **"Magic, not name" is a composition.** sitemaps.org supports name-independence only for text files ("You
   can name the text file anything you wish", 547). The `1f 8b` identification is RFC 1952's (240-241) plus
   its decompressor check (395-397). G2 and case g04 (`.gz` name with plain XML) rest on S447, not S012.
5. **`g03` truncation is the tool's classification, not the RFC's.** RFC 1952 requires "an error indication if
   any of these have incorrect values" for ID1/ID2/CM (395-397) but says nothing about a truncated member; exit
   2 for a truncated stream is compatible with the RFC and is the lane's own choice, so the row/report must
   not attribute that exit code to the RFC.
6. **Page stability.** protocol.html fetched today hashes to the same sha256 S102 recorded on 2026-10-23 and
   still prints a 2016 "Last Updated"; the round-39 quotes in `corpus/lessons/round-39.md` and the round-77
   quotes above are therefore drawn from identical bytes.
7. **Registry mechanics.** `S447`/`S448` are free ids: the registry's last row is `S446`
   (`corpus/SOURCES.md` line 192) and `grep -cE '^\| S44[0-9]'` finds only S440–S446. Row count before the
   L1's edit: 184 data rows (`grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md`). Census after is the L1's.

## 8. Remaining unknowns

- None blocking. The only judgement call left is which quote the scribe prints in `round-77.md ## Gate`
  (candidates listed in §4); every candidate is verified against retained bytes.
