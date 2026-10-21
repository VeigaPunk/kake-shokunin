# PairS012CrawlScopePerHost: round-26 freshness recheck (knowledge seat)

Lane: kake-shokunin · Milestone: r26-recheck-build · Axis: freshness · Pair: S012 × `corpus/knowledge/crawl-scope-per-host.md`

## Scope and evidence

- Entry: `corpus/knowledge/crawl-scope-per-host.md`, 53 lines. It has no r20-correction tail and no later appended section. A search for `correction|[r2|r26|tail|appended` matched nothing, so every S012-dependent statement sits in the body (lines 1–51).
- Source: S012, `https://www.sitemaps.org/protocol.html` (SOURCES.md:20; population.json S012 row; fetch index 1).
- Bytes: `fetched/S012-1.raw.gz`, gz sha256 `75667be6156fee2402d735c3b45b9853ee33e830967572e759763a1f14c020cf` (8,868 B). Decompressed sha256 `5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654`, 45,292 B, equal to manifest.json:258–259. Text view `fetched/text/S012-1.txt`: 21,172 B, one line, sha256 `3dac10762e028f83b45b6c5c55c0f0db40670badc0ac33026ff595759b1dcebd`.
- Fetch: HTTP 200, finalUrl unchanged, fetchedAt 2026-10-21T15:10:39Z. Server `Last-Modified`: Thu, 15 Dec 2022 10:54:02 GMT. The page's own line reads "Last Updated: Monday, November 21, 2016" (text byte 21108). The entry cites neither date.
- Byte offsets below count after the UTF-8 BOM. Raw HTML confirms the text view is a whitespace-normalized extraction (CRLF splits inside sentences). The section anchor is `<a name="location" id="location"></a>Sitemap file location</h2>`, i.e. `#location`.

## Statements attributed to S012: verdicts

| # | Entry line | Statement (abridged) | Verdict | Verbatim quote (text byte) | Anchor observed 2026-10-21 | Reason |
|---|---|---|---|---|---|---|
| 1 | L1 | header lists S012 as a source | HOLD | This document describes the XML schema for the Sitemap protocol. (280) | Same page; SOURCES.md:20 row still names it | Name resolves. Provenance note only: the header prints the RFC 9309 URL, and S012's URL lives in SOURCES.md:20. Non-blocking. |
| 2 | L2 | `verified-at: 2026-10-19` covers S012 | HOLD + FLAG (date superseded) | The location of a Sitemap file determines the set of URLs that can be included in that Sitemap. (12127) | Same | Covered text still present. For S012 the date is superseded by the 2026-10-21 re-fetch. Content unchanged, so no correction. |
| 3 | L14–15 | sitemaps.org limits the URL set by location and requires same-host URLs | HOLD | all URLs in a Sitemap must be from a single host, such as www.example.com or store.example.com. (918) | Single-host rule in the XML section; location rule at `#location` (12105) | Both halves verbatim. |
| 4 | L17 | a site-root sitemap can cover all paths on that site (S012 share; the Google clause on L15–16 belongs to S013) | HOLD | It is strongly recommended that you place your Sitemap at the root directory of your web server. (13351) | Sitemap file location section; prefix rule at 12288 | The prefix rule ("can include any URLs starting with" its own directory) applied at the root covers all paths on the host. S013's "descendants" wording is not judged here. |
| 5 | L17–18 | a `Sitemap:` line in the host-root robots file is a supported discovery route | HOLD | You can specify the location of the Sitemap using a robots.txt file. (18914) | Heading "Specifying the Sitemap location in your robots.txt file" (18858) | Still supported. Nuance, no contradiction: for a robots.txt pointer to another host's sitemap, S012 says it "is expected that" all the URLs belong to the host pointing to it (quote: all the URLs belong to the host pointing to it., 15996). |
| 6 | L20–21 | "Makes host/path scope explicit for" sitemap-orphan-audit.md:40-47 | HOLD | The location of a Sitemap file determines the set of URLs that can be included in that Sitemap. (12127) | sitemap-orphan-audit.md:40–42 listing-coverage tail; :44 "## Procedure"; :46–47 per-host live sitemap.xml list | Anchor still resolves to host/path-scoped sitemap listing text. Adjacent, not asserted by this statement: :47 "(8 locs)" for plazir15-ghp is superseded by the same file's round-23 section (line 133, c1: 7 on 2026-10-21). That count belongs to the sitemap-orphan-audit pair. |
| 7 | L22 | same bullet: host/path scope explicit for freshness-sweep.md:58 | **STALE (anchor)** | The location of a Sitemap file determines the set of URLs that can be included in that Sitemap. (12127) | freshness-sweep.md:58 is the H4 row for `scripts/probe-delta.mjs` over the history. It has no sitemap, host, or scope text (absent from the grep matches). The sitemap host/path rows are now :62 (A4 ds4cc sitemap/robots pre-push state) and :63 (A5 PQ-14 plazir15-ghp live/source sitemap gap). | The line anchor drifted as the table grew. Correction in the block below. |
| 8 | L26 | "Source checks (quotes reopened 2026-10-19)" | HOLD + FLAG (date superseded) | The location of a Sitemap file determines the set of URLs that can be included in that Sitemap. (12127) | Heading and S012 quote both present | The quote holds. The 2026-10-19 date is an accurate record of that check and is superseded for S012 by 2026-10-21. No correction (STALE-only rule). |
| 9 | L30–31 | S012 "Sitemap file location" quote | HOLD | The location of a Sitemap file determines the set of URLs that can be included in that Sitemap. (12127) | `#location` section (12105) | Verbatim. The entry's line break is cosmetic; the whitespace-normalized text matches. |
| 10 | L31–32 | /catalog/sitemap.xml includes /catalog/ URLs, not /images/ | HOLD | can include any URLs starting with http://example.com/catalog/ but can not include URLs starting with http://example.com/images/ (12288) | Same section | Still the stated example. The entry's /images/ matches the prose sentence; the examples list uses singular /image/, which the entry does not quote. |
| 11 | L51 | Admission authority cites "the sitemap protocol" | HOLD | This document describes the XML schema for the Sitemap protocol. (280) | Page intro | Still the sitemaps.org Sitemap protocol. The RFC and Google parts of L51 are S011 and S013 claims. |

Totals: 11 statements · 10 HOLD (2 carry superseded-date flags) · 1 STALE · 0 UNVERIFIABLE.

## Considered and excluded

| Entry line | Text | Why excluded |
|---|---|---|
| L7–12 | host-root robots policy, 4xx/5xx handling, "share the one host-root robots policy" | S011 only |
| L15–16 | "For Google, unless submitted through Search Console, a sitemap affects only URLs under its parent directory" | S013; PairS013CrawlScopePerHost owns it |
| L33–35 | S013 quote and robots.txt listing note | S013 |
| L22–24 | historical ds4cc.com 404 is a different host | Hostname identity; no S012 dependence. Anchor still resolves: publish-queue.md:92–93 carries the ds4cc.com 404 sentence. |
| L37–42 | population grep and RFC recheck | Not S012 |
| L44–46 | named debt: status of veigapunk robots.txt and whether it lists project sitemaps | Open question; asserts nothing from S012; no property probed under the bounds |

## Flags (superseded dates and anchors)

- L2 and L26: the S012 check date 2026-10-19 is superseded by the 2026-10-21 re-fetch. Content unchanged.
- SOURCES.md:20 row anchor "fetched 2026-10-19" is superseded as a retrieval date. The section anchor "Sitemap file location" (`#location`) still holds. For the row seat to log in the recheck field.
- sitemap-orphan-audit.md:47 count drift (adjacent to row 6). Owned by the sitemap-orphan-audit pair.
- corpus/lessons/round-20.md:214 and SOURCES.md:49 also cite S012. Out of scope. The lesson's quote still matches (text byte 12127).

## Correction (append-only EOF block; STALE row 7 only)

```text
[r26-recheck S012 STALE] Anchor correction for the 'Refines at base cb807bc' bullet (lines 20-22), current tree as of 2026-10-21. The anchor `corpus/knowledge/freshness-sweep.md:58` no longer holds host/path-scope text: that line is now the H4 `scripts/probe-delta.mjs` history row. The sitemap host/path rows sit at `corpus/knowledge/freshness-sweep.md:62-63` (A4 ds4cc sitemap/robots pre-push state; A5 PQ-14 plazir15-ghp live/source sitemap gap). The anchor `corpus/knowledge/sitemap-orphan-audit.md:40-47` still resolves and needs no change. The scope rule the bullet relies on still holds in the sitemaps.org text re-fetched 2026-10-21 (raw sha256 5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654): 'The location of a Sitemap file determines the set of URLs that can be included in that Sitemap.' The base-commit claim is historical and was not re-derived. Original lines are unchanged.
```

## Checks performed

- sha256 of the gz and of the decompressed raw bytes; the decompressed hash and length equal manifest.json:258–259.
- Every quote used in the table occurs exactly once in the text file (BOM stripped); each is at most 25 words (maximum 18). Other checked S012 strings also occur once.
- Raw HTML contains the `#location` anchor. Multi-word sentences are split by CRLF in raw, which confirms text-view normalization and no wording change.
- freshness-sweep.md:58 read directly. A grep for `sitemap|robots|host|path scope|scope` matches :61–63 and omits :58.
- sitemap-orphan-audit.md:40–47 read. The content is still listing-coverage text, the Procedure heading, and per-host sitemap.xml observations.
- Entry grep for `correction|[r2|r26|tail|appended|verified-at|recheck`: matches only L2, L3, L37, L42. None is an appended tail.

## Tooling and bounds

- Installs or updates: none. Used read-only lane `read`/`grep`/`glob` and kernel Python stdlib (hashlib, gzip, re) on retained bytes. No network access.
- Not run: builds, tests, linters, measure.py (outside this item). No live GET or property probe. No edits to corpus, SOURCES, manifests, or sibling lanes. No round-24 material read.

## Result

```json
{"pair":"S012xcrawl-scope-per-host","statements":11,"hold":10,"stale":1,"corrections":["[r26-recheck S012 STALE] Anchor correction for the 'Refines at base cb807bc' bullet (lines 20-22), current tree as of 2026-10-21. The anchor `corpus/knowledge/freshness-sweep.md:58` no longer holds host/path-scope text: that line is now the H4 `scripts/probe-delta.mjs` history row. The sitemap host/path rows sit at `corpus/knowledge/freshness-sweep.md:62-63` (A4 ds4cc sitemap/robots pre-push state; A5 PQ-14 plazir15-ghp live/source sitemap gap). The anchor `corpus/knowledge/sitemap-orphan-audit.md:40-47` still resolves and needs no change. The scope rule the bullet relies on still holds in the sitemaps.org text re-fetched 2026-10-21 (raw sha256 5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654): 'The location of a Sitemap file determines the set of URLs that can be included in that Sitemap.' The base-commit claim is historical and was not re-derived. Original lines are unchanged."]}
```
