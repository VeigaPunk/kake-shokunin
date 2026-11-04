# ScoutSources — round 81, w1

**Verdict:** both RFC 9110 surfaces opened from scratch with one GET each and retained (`21c1cdce…` 502,941 B plain text, `d4317606…` 1,187,554 B HTML, both HTTP 200 at 2026-11-04T11:46:19Z, no redirect); S454 is admission-ready with one raw-substring quote and three located collapsed-only spans; S433's re-open finds the body byte-identical to the round-61 retained copy; two locator defects found and routed (never silently corrected).

Write scope: this report plus `.ufo/waves/round-81/w1/ScoutSources/` only. No production file touched, `corpus/SOURCES.md` not edited, nothing committed. Roles: leaf scout, no subagents.

## 1. Fetch receipts

Exactly one GET per URL, GET only, no credentials, no request body, no cookie jar, user agent `round81-scoutsources`; both answers carry `link: <https://www.rfc-editor.org/info/rfc9110/>; rel="canonical"` and no `last-modified`.

| surface | requested = final URL | status | fetched (UTC) | bytes | sha256 | etag | s |
|---|---|---|---|---|---|---|---|
| `rfc9110.txt` | https://www.rfc-editor.org/rfc/rfc9110.txt | HTTP/2 200, 0 redirects | 2026-11-04T11:46:19Z | 502,941 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` | `W/"7c9fc097e78bd883e559172c885e074c"` | 0.232 |
| `rfc9110.html` | https://www.rfc-editor.org/rfc/rfc9110.html | HTTP/2 200, 0 redirects | 2026-11-04T11:46:19Z | 1,187,554 | `d431760660ea44e130f6e919dab216df2d0b3a490567a98089267523368fe1e5` | `W/"0d9f5fb8eb38d3c08b055f9b0671d68b"` | 0.235 |

Command (verbatim, one invocation per URL, `curl_exit=0` both):

```
curl -sSL --max-time 45 --no-progress-meter -A round81-scoutsources \
     -D <name>.headers -o <name>.body \
     -w 'http_code=%{http_code}\nurl_effective=%{url_effective}\nsize_download=%{size_download}\ntime_total=%{time_total}\nnum_redirects=%{num_redirects}\n' <url>
```

Retained at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-81/w1/ScoutSources/`: `rfc9110.txt` (body), `rfc9110.html` (body), `rfc9110.html.text` (derived, 559,103 B, sha256 `928c4b2ed4973eacf70e52469699c9ccecdb1dc939512c447e8793054321aad5`), both `.headers` (sha256 `ce2f890f…5cc2`, `10418b5a…ca91`), `fetch-receipts.json`, `quote_proof.py`, `quote-proof.json`, `proof-transcript.txt`, `extract_text.py`, `rows-proposed.txt`.

Response notes, recorded rather than interpreted: Cloudflare set a bot-management `__cf_bm` cookie on both responses; no cookie was stored or sent back (`cookie_jar_used: false`). The RFC Editor serves no `Last-Modified`; the two ETags are the only server-side validators seen.

**Body identity against already-committed bytes (strongest receipt available):**

- `rfc9110.html` sha256 equals `.ufo/waves/round-61/sources/S433.html` (`sha256sum` → `d4317606…68fe1e5`, 1,187,554 B). A GET eight days later returns the same bytes the round-61 audit was built on.
- `rfc9110.txt` sha256 and byte count equal the receipt already in the S453 row (`.ufo/waves/round-81/../w1` fetch at 2026-11-04T10:44:53Z recorded in `corpus/SOURCES.md` S453). Two independent GETs of the same URL today agree byte-for-byte.

## 2. Locations used (line numbers in the retained text)

| what | `rfc9110.txt` | `rfc9110.html.text` |
|---|---|---|
| §15.5.5 heading (404 Not Found) | 7587 | 10774 |
| 404 means the origin server did not find a current representation | 7589–7591 | 10778–10781 |
| 404 says nothing about temporary vs permanent | 7591–7593 | 10781–10782 |
| 410 preferred over 404 | 7593–7595 | 10782–10784 |
| 404 is heuristically cacheable | 7597–7599 | 10786–10787 |
| §15.5.11 heading (410 Gone) | 7667 | 10890 |
| 410 means access is no longer available, likely permanent | 7669–7674 | 10894–10896 |
| 404 ought to be used when permanence is unknown | 7673–7674 | 10897–10899 |
| §8.3 heading (Content-Type) | 2928 | 4602 |
| §8.3 sender SHOULD rule | 2944–2946 | 4628–4630 |
| §8.3 singleton paragraph | 2964–2966 | 4649–4651 |
| §5.5 heading (Field Values) | 1579 | 2815 |
| §5.5 leading/trailing whitespace rule | 1591–1594 | 2834–2837 |
| §5.2 heading (Field Lines and Combined Field Value) | 1492 | 2705 |
| §5.3 heading / sender MUST NOT repeat a field line | 1515 / 1529–1536 | 2740 / 2756–2758 |

The stripped-text line numbers are reproducible from the retained body with `python3 -B extract_text.py rfc9110.html rfc9110.html.text`; the recipe (decode, drop `script`/`style` elements, drop remaining tags, unescape references, no whitespace normalisation, no re-wrapping) is in that file's docstring and re-derives the recorded `928c4b2e…` digest.

## 3. Defects found (routed, not silently fixed)

**F1 — the seat item's section numbers are wrong for RFC 9110.** The item (and the frozen contract's `## Sources` paragraph) says "§15.5.4 (404 Not Found) and §15.5.5 (410 Gone)". In this document §15.5.4 is **403 Forbidden** (`rfc9110.txt:7569`), §15.5.5 is **404 Not Found** (`:7587`), and **410 Gone is §15.5.11** (`:7667`). The S454 row below cites 15.5.5 and 15.5.11 and says so in its anchor cell, so a later reader cannot re-introduce the drift. Recommended: the round lesson carries a dated correction of the contract wording; the predicate and the claim text are unaffected because the row's addresses name the status codes, not the numbers.

**F2 — a §5.2 label on a §5.3 sentence in the C2 knowledge entry.** `corpus/knowledge/response-header-expectations.md` (singleton_fields section) writes "RFC 9110 §5.2 states the sender-side rule about repeated field lines … [S433 §5.2]: 'generate multiple field lines with the same name in a message'". That sentence sits in **§5.3 Field Order** (`rfc9110.txt:1529–1536`, `rfc9110.html.text:2756–2758`); §5.2 ends at line 1514. The same entry's `[S433 §5.3]` label for the Set-Cookie clause (`:1542`) is correct. `corpus/QUALITY.md:1116` (round-53) requires a locator to point at the section containing its quote, so this is drift. I did not edit the entry (its owner is the knowledge seat this round) and I did not change the S433 `anchor` cell (SOURCES.md's round-37 note makes anchor/scope/teaches change only through superseding rows). Fix by an append-only correction note or a superseding row — L1's call.

Neither defect blocks S454's admission: the row's own anchor is self-checking.

## 4. Quotes proposed, with class, size and location

Class follows `corpus/QUALITY.md:1100–1107` (round-50): `raw-substring` when the span is in the retained bytes; `collapsed-only` when it survives only whitespace collapse, recorded with both digests and never described as raw. All spans are ≤ 25 words.

| # | span | body | lines | words | class |
|---|---|---|---|---|---|
| Q1 | "The 404 (Not Found) status code indicates that the origin server did not find a current representation for the target resource" | `rfc9110.txt` | 7589–7590 | 21 | collapsed-only |
| Q2 | "A 404 status code does not indicate whether this lack of representation is temporary or permanent" | `rfc9110.txt` | 7591–7593 | 16 | collapsed-only |
| Q3 | "the 410 (Gone) status code is preferred over 404" | `rfc9110.txt` | 7593 | 9 | **raw-substring** |
| Q4 | "The 410 (Gone) status code indicates that access to the target resource is no longer available at the origin server" | `rfc9110.txt` | 7669–7670 | 20 | collapsed-only |
| Q5 | "the status code 404 (Not Found) ought to be used instead" | `rfc9110.txt` | 7673–7674 | 11 | collapsed-only |
| Q6 | Q1's span re-checked in the other rendering | `rfc9110.html.text` | 10778–10780 | 21 | collapsed-only |
| Q7 | "generate a Content-Type header field in that message unless the intended media type of the enclosed representation is unknown to the sender" | `rfc9110.html.text` | 4629–4630 | 22 | collapsed-only |
| Q8 | "Content-Type is defined as a singleton field, it is sometimes incorrectly generated multiple times" | `rfc9110.html.text` | 4649–4650 | 14 | collapsed-only |
| Q9 | "A field value does not include leading or trailing whitespace." | `rfc9110.html.text` | 2834 | 10 | **raw-substring** |
| Q10 | "sender MUST NOT generate multiple field lines with the same name in a message" | `rfc9110.html.text` | 2756–2757 | 14 | collapsed-only |
| Q11 | Q7's span against the plain text | `rfc9110.txt` | 2944–2946 | 22 | collapsed-only |
| Q12 | Q9's span against the plain text | `rfc9110.txt` | 1591 | 10 | **raw-substring** |

Proofs, verbatim (`proof-transcript.txt`, run from the receipts directory; `set -x` captured the commands):

```
python3 -c 'b=open("rfc9110.txt",encoding="utf-8").read(); q="the 410 (Gone) status code is preferred over 404"; i=b.find(q); print("raw_in:",q in b,"offset:",i,"line:",b[:i].count(chr(10))+1)'
raw_in: True offset: 357005 line: 7593
python3 -c 'b=open("rfc9110.html.text",encoding="utf-8").read(); q="A field value does not include leading or trailing whitespace."; i=b.find(q); print("raw_in:",q in b,"offset:",i,"line:",b[:i].count(chr(10))+1)'
raw_in: True offset: 84831 line: 2834
python3 -c 'b=open("rfc9110.txt",encoding="utf-8").read(); q="A field value does not include leading or trailing whitespace."; i=b.find(q); print("raw_in:",q in b,"offset:",i,"line:",b[:i].count(chr(10))+1)'
raw_in: True offset: 73711 line: 1591
```

The nine collapsed-only rows were each checked the same way and returned `raw_in: False collapsed_in: True`; e.g.

```
python3 -c 'import re; b=open("rfc9110.txt",encoding="utf-8").read(); q="The 404 (Not Found) status code indicates that the origin server did not find a current representation for the target resource"; print("raw_in:",q in b,"collapsed_in:"," ".join(q.split()) in re.sub(r"\s+"," ",b))'
raw_in: False collapsed_in: True
```

`quote_proof.py` is the retained, re-runnable instrument: it records for every span the body digest, char and byte span, first and last line, class and method, into `quote-proof.json` (exit 0 means every span was located and none exceeded 25 words).

**Explicit limitation, not a green:** the item asked for a raw-substring proof of every quote. Nine of twelve spans are not raw substrings of either committed body, because both the plain text and the HTML wrap prose at 72 columns and the sentence crosses a wrap. I report them as `collapsed-only` under the round-50/round-63 rule rather than rewriting the source or calling a collapsed match raw. The admission quote carried on the S454 row (Q3, 9 words) *is* raw.

## 5. Row proposals (registry shape, 11 cells, no literal pipe inside a cell)

### 5a. S454 — new

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S454 | RFC 9110: HTTP Semantics, §15.5.5 404 Not Found and §15.5.11 410 Gone — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | What the 404 and 410 status codes say about a target resource and about the permanence of its absence, and which of the two the origin server ought to use; not crawler behaviour or any search engine's treatment of an absent URL, not a sitemap or robots.txt location rule, not cache lifetime beyond each field's stated heuristic cacheability, not the lane's audit finding classes, and not what any particular surface serves | §15.5.5 lines 7587-7599 and §15.5.11 lines 7667-7688 of the retained plain text (404 meaning 7589-7591, 404 permanence 7591-7595, 410 meaning 7669-7674, 410 and 404 preference 7673-7674); §15.5.4 in this RFC is 403 Forbidden, so 410 Gone is §15.5.11; June 2022; fetched 2026-11-04T11:46:19Z, HTTP 200, 502,941 bytes, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, retained at .ufo/waves/round-81/w1/ScoutSources/rfc9110.txt | A 404 says the origin server did not find a current representation for the target resource or is not willing to disclose that one exists, and says nothing about whether that absence is temporary; a 410 says access to the target resource is no longer available at the origin server and is likely permanent, so 404 is preferred when permanence is unknown; quoted span "the 410 (Gone) status code is preferred over 404" (9 words, raw substring at line 7593) carries the preference rule; both are heuristically cacheable | mined | 2026-11-04 | 365d | corpus/knowledge/response-header-expectations.md |

Shape checked (`rows-proposed.txt`, 11 cells, no cell contains a pipe, embedded quote 9 words). `365d` follows the other RFC spec rows (S028, S029, S032, S033, S448, S453); `opened` is the fresh access date.

### 5b. S433 — change, old → new

Old (`corpus/SOURCES.md:179`, verbatim):

```
| S433 | RFC 9110: HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110.html | spec | A | Content-Type field semantics and HTTP field-line rules | Section 8.3 Content-Type and Section 5.2 Field Lines and Combined Field Value; RFC 9110, June 2022 | Content-Type is defined as a singleton field, so its accidental repetition yields a combined value that only appears to be a list, while field lines of any name combine in received order by comma concatenation | mined | 2026-10-27 | 180d | corpus/knowledge/response-header-expectations.md |
```

New:

```
| S433 | RFC 9110: HTTP Semantics — https://www.rfc-editor.org/rfc/rfc9110.html | spec | A | Content-Type field semantics and HTTP field-line rules | Section 8.3 Content-Type and Section 5.2 Field Lines and Combined Field Value; RFC 9110, June 2022 | Content-Type is defined as a singleton field, so its accidental repetition yields a combined value that only appears to be a list, while field lines of any name combine in received order by comma concatenation | mined | 2026-10-27 | 2027-05-03 | corpus/knowledge/response-header-expectations.md, corpus/lessons/round-81.md |
```

Cell-level diff — only two cells move; `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `status`, `opened` stay byte-identical:

| cell | old | new | why |
|---|---|---|---|
| recheck | `180d` | `2027-05-03` | the same 180-day cadence, re-anchored to the fresh access 2026-11-04T11:46:19Z (2026-11-04 + 180 d), in the registry's absolute-date style (`S003`–`S007`); the interval does not change, the due date now cites this round |
| used-by | `corpus/knowledge/response-header-expectations.md` | `corpus/knowledge/response-header-expectations.md, corpus/lessons/round-81.md` | the old→new of this re-open is logged in the round lesson, which therefore cites the row |

Deliberately unchanged: `opened` (2026-10-27) stays the first-open date per the registry's round-27 note, and `anchor` stays untouched because SOURCES.md's round-37 note allows anchor/scope/teaches changes only through a superseding row; the fresh access receipt therefore lives in this report, in `.ufo/waves/round-81/w1/ScoutSources/fetch-receipts.json`, and in the lesson row. If the L1 wants the interval form instead, the fallback is `recheck` unchanged and `used-by` alone moving — but then the contract's "recheck change" is unmet, so the absolute date is the primary proposal.

What the re-open actually confirms (the substantive part of a recheck): §8.3's sender rule, §8.3's singleton paragraph and §5.5's whitespace rule all still sit at the anchor's sections in a body **byte-identical** to the round-61 copy, so no knowledge-statement correction is owed for S433's own two claims. The one locator drift is in the citing entry, not the row (F2).

## 6. Tier decision

Both rows are **tier A, kind `spec`**. RFC 9110 is an IETF Standards Track document, not secondary material: the retained plain text says `STD: 97` (line 7), `Category: Standards Track` and `June 2022` (line 11), and `This is an Internet Standards Track document.` (line 32). It defines the status codes and the field rules the audit reads; nothing stands between the lane and the normative text. Tier B is for material restating a primary (S452's MDN page, S056's sibling-lane report) and would misstate what this row is. Tier C would be wrong for the same reason.

**What S454 cannot support.** (i) That any surface answers 404 or 410 now, or that a path is absent — that is a capture receipt's job, and C2's own surfaces are ds4cc.com, not rfc-editor.org. (ii) Crawler or search-engine treatment of an absent URL — no search engine's handling is in §15.5.5/§15.5.11 (S011 and S449 govern crawling directives). (iii) Sitemap or robots.txt location rules (S012, S011). (iv) Cache lifetime — only the "heuristically cacheable" property is stated, and the section defers to RFC 9111. (v) That a 404 means "deleted" or "never existed"; the section says only that no current representation was found or that the server will not disclose one. (vi) The audit's finding classes and exit codes, which are lane policy, not RFC text.

**What S433 cannot support.** (i) What any server actually emits, or that a repeated `Content-Type` occurs on a live surface. (ii) Crawler behaviour or MIME-sniffing outcomes. (iii) Media-type parameter semantics beyond §8.3.1, which the anchor does not cover. (iv) That a repeated field is invalid on the wire — it is a sender MUST NOT with a list-syntax exception, and recipients still receive such lines. (v) A §5.2 citation for the repeated-field-line sentence: per F2 that sentence is §5.3, so the row's anchor supports the combination rule (§5.2) and the Content-Type singleton rule (§8.3), not a §5.2 label on the sender rule.

## 7. Method, limits, cleanup

- Search before reading: the registry's last id is S453 and S454 is free (`rows` census over `corpus/SOURCES.md`, 191 S-rows). S433's row has never changed since its creation at `d2da25de` (round 61) — `git log -L179,179` — so this round's re-open is the first.
- Read-only git only (`git log -L`, `git show`), no mutating git or jj command anywhere; no fixture repo was needed.
- No tool installed or upgraded; no pacman transaction was attempted (host-wide pause respected).
- Unrun: nothing in this seat's item. I did not run the C1/C2 counters, the audit, or any lane gate — that is not this seat's assignment.
- Scratch tree `/fast/scratch/hyaku/kake-r81/ScoutSources` deleted before yield (`rm -rf`), after copying every receipt into the lane tree; no fixture or clone was created.

## 8. Pointers

- Receipts: `.ufo/waves/round-81/w1/ScoutSources/` — `fetch-receipts.json`, `rfc9110.txt`, `rfc9110.html`, `rfc9110.html.text`, `rfc9110.txt.headers`, `rfc9110.html.headers`, `quote_proof.py`, `quote-proof.json`, `proof-transcript.txt`, `extract_text.py`, `rows-proposed.txt`.
- Row insert: after `corpus/SOURCES.md:200` (S453) if S454 keeps this id; `corpus/SOURCES.md:179` is the S433 row.
- Knowledge entry for the C2 grounding: `corpus/knowledge/response-header-expectations.md` (its `source:` header line needs S454 added by its owner; I did not edit it).
