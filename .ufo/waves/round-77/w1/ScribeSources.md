# ScribeSources — round 77, wave w1 (kake lane)

Seat: `ScribeSources` (leaf; no subagent dispatch). Base revision
`a2cc5f51002433e11cc3d2f70e650a6c60ad5e68`. Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Owned files: `corpus/knowledge/sitemap-formats.md` (the deliverable) and this report.

## 1. Deliverable

`corpus/knowledge/sitemap-formats.md` — created, 12,096 bytes, 202 lines
(`wc -lc`), sha256 `36f99b2deb0506bcddf7aad2e90e864fea11bc9c3aa36654f4d65564e092a702`
(`sha256sum corpus/knowledge/sitemap-formats.md`).

Header fields: `source:` (S012, S447, S448 with URLs, retained paths, bytes and sha256), `verified-at:`,
`recheck:`, `ground:`. Sections, in order:

| section | line | carries |
|---|---|---|
| quote convention | 8 | rendering rule, file→id map, raw-versus-stripped note |
| What a sitemap file is in this lane's reading | 16 | XML schema; three formats (XML / syndication feed / text) |
| The gzip container | 42 | gzip permission, decompressed limit, 52,428,800 bytes, `1f 8b` magic, `deflate` |
| The plain-text format | 74 | one URL per line, absolute reading, 50,000/52,428,800, UTF-8, no other content, gzip, free name |
| Syndication: RSS 2.0 and Atom 1.0 | 120 | `<link>` / `<pubDate>`; Atom `<link href>` / `<updated>` |
| The sitemap-index `<loc>` is container-agnostic | 154 | `<loc>` may name Sitemap/Atom/RSS/text; index limits; same-site bound |
| Limits | 172 | no fetch, no engine acceptance, no robots route, no ratio/server behaviour, no owned property, no error taxonomy, no BOM rule, modality, registry ids |

27 quote blocks (`grep -c '^> — '` → `27`), every one attributed to S012, S447 or S448 with retained file,
line range and section. Every body paragraph and every bullet carries an `S###`.

## 2. Own fetch of the protocol page (the one network read)

```sh
mkdir -p /fast/scratch/hyaku/kake-r77/ScribeSources/tmp
curl -sS -D /fast/scratch/hyaku/kake-r77/ScribeSources/headers.txt \
     -o /fast/scratch/hyaku/kake-r77/ScribeSources/protocol.html \
     -w 'HTTP=%{http_code} BYTES=%{size_download} URL=%{url_effective}\n' \
     --max-time 30 https://www.sitemaps.org/protocol.html
```

Observed:

```
HTTP=200 BYTES=45292 URL=https://www.sitemaps.org/protocol.html
```

Response headers retained during the seat (scratch, removed at cleanup; lines verbatim):

```
HTTP/2 200 
date: Wed, 04 Nov 2026 01:37:42 GMT
content-type: text/html
content-length: 45292
etag: "6b6deb8a7310d91:0"
last-modified: Thu, 15 Dec 2022 10:54:02 GMT
x-cache: CONFIG_NOCACHE
accept-ranges: bytes
```

```sh
sha256sum /fast/scratch/hyaku/kake-r77/ScribeSources/protocol.html
```

```
5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654  .../protocol.html
```

Byte-identical to the retained `protocol.raw` the scout fetched (same sha256, 45,292 bytes), so the entry's
line numbers are valid against either copy. First three bytes of both copies: `ef bb bf`.

## 3. RFC bytes (not re-fetched by this seat)

The item allows one public GET; that budget went to sitemaps.org. The two RFC quotes were derived from the
wave's retained raw copies, read-only:

```sh
sha256sum .ufo/waves/round-77/w1/ScoutSources/{protocol.raw,rfc1952.raw,rfc4287.raw}
```

```
5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654  protocol.raw
164ef0897b4cbec63abf1b57f069f3599bd0fb7c72c2a4dee21bd7e03ec9af67  rfc1952.raw
3bd71d76289560c9e860151f39cebbdc402cfd8b788a62048d8dc42824f2d89c  rfc4287.raw
```

These match the scout's `*.meta` fetch records (`200 <url> <bytes>`), so the bytes quoted are the fetched
bytes, not a rendering. The entry's `verified-at` line states this split explicitly.

## 4. Quote integrity (construction check, not a project gate)

Each quote was extracted from its named line range before drafting, and re-checked after drafting with the
file's blockquotes parsed back out, backticks stripped, HTML tags/entities rendered and whitespace collapsed:

```python
# run in-session against the written file and the retained raw files
# pairs = (quote, "— S###, `file:a-b`, …") blocks; for each: strip backticks, flatten lines a..b,
# drop HTML tags, unescape &lt; &gt; &amp; &quot; &apos; &#39;, collapse whitespace, test substring
```

Observed:

```
quotes=27 max_words=24 problems=0
```

and the paragraph check (`S\d{3}` required per paragraph/bullet, excluding the convention note and header):

```
paragraphs: 64 gaps: 0
```

No quote exceeds 25 words (max 24, the RFC 1952 ID1/ID2 sentence); every quote is a contiguous substring of
its named range with no words added or removed.

## 5. Late-arriving scout artifacts and reconciliation

At write time `w1/ScoutSources.md` and `w1/ScoutSources/verify-output.txt` did not exist:
`test -f … && echo YES || echo NO` → `SCOUT_MD_NO`, `VERIFY_NO` (checked at 22:38 and again immediately
before the write). Only the scout's raw fetch directory existed. Per the item, the entry says in its
provenance line that quotes are derived from this seat's own fetch plus the retained RFC copies.

Both files landed after the write (checked again: `SCOUT_MD_YES`, `VERIFY_YES`). I read them and reconciled:

| scout finding | effect on the entry |
|---|---|
| F1 sitemaps.org never says `<link href>` | already split: `<link>` field from S012, `href` from S448; sentence tightened to say the page names only the `<link>` field |
| F2 "fully specified (scheme + authority)" is half verbatim; authority is inference | the text section now marks "absolute" as this lane's reading and records `grep -ci 'absolute' protocol.raw` → `0`, with the single "authority" hit identified as permission language (`protocol.raw:1183`) |
| F3 decompressed-size sentence is exact | no change; entry quotes it and adds the 52,428,800-byte figure from `protocol.raw:689` |
| F4 "magic, not name" is a composition; name-independence is stated only for text files | sentence rewritten: the two-byte decision is S447's, name-independence is S012's text-file sentence only |
| F5 `g03` truncation is a tool choice, not the RFC's | not asserted in the entry; the Limits "No error taxonomy" bullet keeps error classes out of the sourced rules |
| F6 page stability | consistent with my own GET (same sha256); no change |
| F7 S447/S448 are free ids; corpus has 184 data rows, last S446 | consistent with my own count; entry's registry bullet already says no S447/S448 row existed |

No quote, hash or claim in the entry conflicts with the scout's verified spans (all 27 scout quotes are on the
same bytes; line numbers differ only because the scout cites the stripped `.txt` renders, which the entry's
convention note explains).

## 6. Absence checks behind the Limits section

Run from `.ufo/waves/round-77/w1/ScoutSources/`; each count is `grep -ci`:

```
'1f 8b'              protocol.raw 0
'magic'              protocol.raw 0
'BOM'                protocol.raw 0
'byte order mark'    protocol.raw 0
'exit code'          protocol.raw 0
'format_unsupported' protocol.raw 0
'absolute'           protocol.raw 0
'Google'             protocol.raw 0
'Bing'               protocol.raw 0
'accept'             protocol.raw 0
'compression ratio'  protocol.raw 0   rfc1952.raw 0
'ratio of'           protocol.raw 0   rfc1952.raw 0
'Content-Encoding'   protocol.raw 0   rfc1952.raw 0
'once uncompressed'  protocol.raw 1
'authority'          protocol.raw 1   (line 1183, permission language)
'robots'             protocol.raw 13  (includes the sitemap-location-in-robots.txt section)
```

Substring traps avoided: `grep -i ratio` matches `incorporation` / `Considerations` / `reduction` in
`rfc1952.raw`, so the entry states the exact phrase's absence, not the substring's.

## 7. Findings for the L1 (not claim changes)

1. **S012's registry scope is narrower than the page this entry reads.** `corpus/SOURCES.md:20` scopes S012
   to "Sitemap file location and the URLs it can list", while line 110 records S102 (same URL) as superseding
   S012 with the broader structure/limits scope. The entry cites S012/S447/S448 as the frozen contract names
   them and records the tension in its Limits bullet; the L1 may prefer to re-cite S102 on landing.
2. **No S447/S448 rows exist yet.** `grep -c 'S447\|S448' corpus/SOURCES.md` → `0`; data rows `184`
   (`grep -cE '^\| S[0-9]+ \|'`), last row `S446`, file 300 lines. The scout has drafted the rows; adoption
   is the L1's.
3. **The protocol page does document robots.txt sitemap submission, including a sitemap on another host**
   (`protocol.raw:1185-1209`, `1401-1429`). The Limits bullet therefore says *this entry* claims nothing
   about that route, rather than claiming the page is silent — the latter would be false.
4. **No BOM rule exists on the page** (`grep -ci 'BOM'` → `0`), while the page file itself begins `ef bb bf`.
   A BOM-prefixed first URL read clean (matrix `t07`) is a lane tolerance, and the entry says so.
5. **The page states no error taxonomy** (`exit code` → `0`, `format_unsupported` → `0`), so exit 2 for an
   unsupported root is a lane construct, not a sourced rule — relevant to X1's citation.

## 8. Gates

None run. This seat's item names no gate, and no build, lint, test, matrix or tool execution was performed;
in particular `scripts/sitemap_audit.py` and the C2 matrix were not run by this seat. The only checks here
are the quote/paragraph integrity checks in §4 and the `grep` counts in §6, both read-only.

## 9. Touched surfaces

- `corpus/knowledge/sitemap-formats.md` — created (the one owned product file).
- `.ufo/waves/round-77/w1/ScribeSources.md` — this report (created).
- Nothing else written. Read-only git status after the write:
  `git status --porcelain -- corpus/knowledge/sitemap-formats.md .ufo/waves/round-77/w1/ScribeSources.md`
  → `?? corpus/knowledge/sitemap-formats.md` (the report was not yet written at that call).
- No `git`/`jj` mutation, no commit, no add, no stash, no checkout; no writes to `MANIFEST.json`,
  `.ufo/state/`, `.ufo/watchdog.log`, `corpus/SOURCES.md`, `corpus/lessons/`, `SHONEN.md`, `scripts/`, any
  wave dir other than this report, or any sibling lane.

## 10. Out of scope (stated in the entry, restated here)

No sitemap/feed/index fetch; no engine acceptance or rejection; no robots `Sitemap:` cross-submission; no
compression ratio, `Content-Encoding`, server or CDN behaviour; no claim about any owned property
(ds4cc.com, kimi mirrors, Pages hosts); no error taxonomy; no BOM rule.

## 11. Scratch and cleanup

Scratch: `/fast/scratch/hyaku/kake-r77/ScribeSources/` (fetch body, headers, `tmp/`). Receipts that matter
(HTTP status, headers, byte count, sha256) are copied into §2 above. Cleanup:

```sh
rm -rf -- /fast/scratch/hyaku/kake-r77/ScribeSources
```

Confirmed gone: `test -e /fast/scratch/hyaku/kake-r77/ScribeSources` → non-zero. No file under `/tmp` was
used as evidence.

## 12. Tooling

No install or upgrade. `curl` (host package) was used for the single public GET; `python3` (3.13, host) for
the quote extraction/integrity checks; `grep`, `awk`, `sha256sum`, `od`, `wc` for receipts.

## 13. Known limits

- The entry cites the raw retained files, not the scout's stripped `.txt` renders; the convention note maps
  the two so a checker can use either, but line numbers are not interchangeable.
- Quotes are whitespace-collapsed and entity-rendered; a byte-exact matcher must apply that rendering first
  (the convention note says so).
- The entry records the format rules only; whether the round-77 audit meets the frozen C2 predicate is
  C2's business, not this report's.
