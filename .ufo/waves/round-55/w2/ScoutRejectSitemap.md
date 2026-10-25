# ScoutRejectSitemap

ATTACKS: the UNADOPTED staged candidate `corpus/knowledge/yahoo-japan-sitemap-constraints.md`
(staged id **S382**, staged row `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md:102`),
read from `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/yahoo-japan-sitemap-constraints.md`
(sha256 `9282674419a6185e9b9ce1553be6f497c34a68f80564a2bb84526816a73a88a3`, 1979 bytes, read-only).
Its `source:` line names **https://info-search.yahoo.co.jp/sitemaps/index.php** (the operator's *sitemap
category index*, not a rule page). Judged against `corpus/QUALITY.md` (qualifier-preserving glosses,
Platform mechanism, ≤25-unit quote ceiling) and `PROVINCE.md` §Core/§Frontier/§Adjacent.

## CANDIDATE:

- **Cited source:** `https://info-search.yahoo.co.jp/sitemaps/index.php`, anchor `§ サイトマップ →
  Sitemapsの設置場所 (the category's own summary of that page)`.
- **Three claims the entry makes** (candidate lines 12–27): (1) telling the engine where the sitemap is
  makes the crawl more efficient **"and updated or new pages are then crawled sooner"**; (2) the XML form
  has a file-size and URL-count ceiling, above which the file is split and a sitemap index is needed;
  (3) where the file is placed bounds which URLs it may list, and the location is told to the engine
  through the refusal file — closing with "the crawl decision, the sitemap's location and the sitemap's
  contents are one mechanism … it is the operator's own design rather than a practice the lane inferred".
- **Candidate's own scope note (lines 29–30):** "a claim about what the operator's category index
  states. The four sitemap pages it lists were not opened by this lane".
- **Quoted spans in the candidate:** exactly one double-quoted span (candidate line 18), the placement
  sentence; the only other quoted string is the recheck argv in backticks (line 4). No curly quotes.

**Claim-to-page test (my own fetch, below):**
- Claim (2) is on the cited page (the `複数のSitemapsを使用する場合` summary, line 149).
- Claim (3)'s placement sentence is on the cited page (line 158) and its robots.txt half too (line 158:
  `robots.txtでSitemapsの場所を検索エンジンに伝える`).
- **Claim (1)'s second half is NOT on the cited page.** My fetch of the cited page contains
  `更新` × 0, `新しく` × 0, `より早く` × 0, `早く` × 0, `更新したウェブページ` × 0. The index page's
  `サイトマップによる効率的な巡回` summary (line 131) stops at "efficiently crawls the site". The
  "updated or new pages round sooner" text lives on the sub-page `archives/002859.php`
  (`更新したウェブページや新しいウェブページなどが、より早く巡回される` × 1 there, × 0 on the cited page)
  — a page the candidate states it did not open. The staged SOURCES row S382 repeats the same overreach
  in its `teaches` cell ("brings updated and new pages round sooner").
- **The "one mechanism" closure is the lane's inference, not the operator's design.** The cited page
  lists three separate page summaries; it never states that crawl decision, sitemap location and sitemap
  contents are one mechanism. The candidate asserts this is "the operator's own design rather than a
  practice the lane inferred" — an inference marked as source text (QUALITY.md qualifier rule, r53
  §Discernment: a gloss must preserve material qualifiers; an unmarked inference must be `[INFERENCE]`).

## FETCH:

Command (plain GET, once, no retries, no credentials):
```
curl -sS -L --max-time 60 -o /tmp/yahoo_sitemaps.html \
  -w 'http=%{http_code} size=%{size_download} url=%{url_effective} ctype=%{content_type}\n' \
  'https://info-search.yahoo.co.jp/sitemaps/index.php'
```
Observed: `http=200 size=6408 url=https://info-search.yahoo.co.jp/sitemaps/index.php
ctype=text/html; charset=UTF-8`.
- **sha256 `297e619714423a02682f5ea773a60d05714cfddccc646d5e906f958c82c8917c`, 6408 bytes, HTTP 200.**
- Body readable: valid UTF-8 Japanese HTML, `<h2>サイトマップ</h2>` at line 93, four
  `entryListTitle`/`entryListBody` entries at lines 130/131, 139/140, 148/149, 157/158. **Not unreadable.**
- Stability: a second identical GET returned the same 6408 bytes and the same sha256
  (`yahoo_sitemaps_2.html`), so the body is not a transient.
- Candidate's own recheck argv re-run by me: `curl -fsSL '<url>' | grep -F -c 'Sitemapsの設置場所によって、そのSitemaps内に記述できるURLが制限されます'` → `1` (exit 0). Note this argv proves the
  quote's presence only, not claims (1)/(2)/(3).
- Supporting fetches for the flip condition only (not quoted in QUOTES): `archives/002859.php` → HTTP 200,
  6715 bytes, sha256 `7e5def127618638346011222fc7bf24328e41d6692083c81cd843e8d1d479039`;
  `archives/002863.php` → HTTP 200, 7806 bytes, sha256 `dd03784cd85602d67e7bb6d8bf312f473f3212d40a450bf1934b1eff823e459d`.
- Units counted with the round-55 counter's own rule and regex
  (`c55_quote_truth.py:104,167-169`: one unit per CJK char, one per non-CJK whitespace token).

## VERDICT TABLE:

| # | Bar / scope check | Result | Evidence |
|---|---|---|---|
| 1 | Body readable | **PASS** | HTTP 200, 6408 bytes, UTF-8, headings at lines 93/130/139/148/157 |
| 2 | Quote ceiling ≤ 25 units | **PASS (at the limit, 25/25)** | placement quote = 25 units by the counter's `units()`; zero headroom |
| 3 | Quote page-unique vs retained bodies | **PASS** | all four candidate-side spans occur 0× in `.ufo/waves/round-55/sources/S372.html`, `S373.html`, `S418.html` |
| 4 | Quote is a raw substring of my fetch | **PASS** | placement quote ×1 in the fetched bytes (line 158) |
| 5 | Registry collision by URL | **PASS (no collision)** | `git show a7a548e:corpus/SOURCES.md \| grep -c 'https://info-search.yahoo.co.jp/sitemaps/index.php'` → **0**; host `info-search.yahoo.co.jp` → 5 rows (S374/S367/S372/S373/S418, none this URL); `grep -c 'S382'` → **0**; `git grep -l 'sitemaps/index.php' a7a548e -- corpus/` → 0 files |
| 6 | Scope (PROVINCE) | **PASS** | §Frontier "Crawl hygiene per host (robots.txt, sitemap scope, canonical signals)"; §Adjacent "kake owns publisher-side placement (robots/sitemap at the host it serves)". No browser/DOM content → not tabi's |
| 7 | **Every claim on the cited page** | **FAIL** | claim (1)'s "updated or new pages … sooner" ×0 on the cited page, ×1 on `002859.php` (not opened by the candidate) |
| 8 | **Qualifier-preserving gloss / inference marking** | **FAIL** | the "one mechanism … the operator's own design" closure is stated as source text but is the lane's inference; the index page asserts no such mechanism |
| 9 | Located-span coverage (lane bar: ≥3 distinct page-unique spans, 6–25 units) | **FAIL** | candidate carries 1 double-quoted span only |
| 10 | Non-duplicative ground | **NOTE** | `corpus/knowledge/crawl-scope-per-host.md` already holds the placement-limits-URLs rule from S012/S013 (tier A, sitemaps.org/Google); claim (3) is the Yahoo restatement of ground already held — admissible only as the operator's own wording, not as new mechanism |

## QUOTES:

Raw substrings of **my** fetch of `https://info-search.yahoo.co.jp/sitemaps/index.php`
(sha256 `297e619714423a02682f5ea773a60d05714cfddccc646d5e906f958c82c8917c`, 6408 bytes, HTTP 200);
each ≤ 25 units by the counter's unit rule; each count 1 in the fetched bytes; each count 0 in the three
retained round-55 bodies.

1. Heading `サイトマップ` → `Sitemapsの設置場所` (h3 `entryListTitle`, line 157) → body line 158 — **25 units**
   > `Sitemapsの設置場所によって、そのSitemaps内に記述できるURLが制限されます`
2. Heading `サイトマップ` → `複数のSitemapsを使用する場合` (h3, line 148) → body line 149 — **22 units**
   > `ファイルサイズや記述できるURL数に上限があります`
3. Heading `サイトマップ` → `サイトマップによる効率的な巡回` (h3, line 130) → body line 131 — **20 units**
   > `クローラーは効率的にサイトを巡回できます`

Also available on the cited page, unused above: `robots.txtでSitemapsの場所を検索エンジンに伝える` (15 units,
count 1, body line 158, same heading as quote 1).

## REGISTRY COLLISION CHECK:

At the build revision `a7a548e102b71bd16b0a6ddafa469393a2c98b69` (read with `git show`, worktree untouched):

```
git show a7a548e102b71bd16b0a6ddafa469393a2c98b69:corpus/SOURCES.md | grep -c 'https://info-search.yahoo.co.jp/sitemaps/index.php'   -> 0
git show a7a548e102b71bd16b0a6ddafa469393a2c98b69:corpus/SOURCES.md | grep -c 'info-search.yahoo.co.jp'                              -> 5
git show a7a548e102b71bd16b0a6ddafa469393a2c98b69:corpus/SOURCES.md | grep -c 'S382'                                                  -> 0
git grep -l 'sitemaps/index.php' a7a548e102b71bd16b0a6ddafa469393a2c98b69 -- corpus/                                                  -> (no files)
git show a7a548e102b71bd16b0a6ddafa469393a2c98b69:corpus/SOURCES.md | grep -c '^| S[0-9]'                                            -> 156 rows
```

- **The URL does not already appear in `corpus/SOURCES.md` at the build revision (0 matches): no
  duplicate-of-a-held-row-by-URL.**
- The five `info-search.yahoo.co.jp` rows are S374 (`002851.php`), S367 (`002852.php`), S372
  (`002849.php`), S373 (`002850.php`), S418 (`002885.php`) — none is the sitemap category index.
- The id **S382 is free** in the lane registry (0 matches) and is not among the round-55 collision list
  (S312 S329 S367 S372 S373 S374 S390 S409) nor in `assimilation/reg-ids`; it is in
  `assimilation/staged-ids`. So an adoption under S382 would not collide by id.
- The URL does appear as a **retained-body link** in seven already-retained files
  (`.ufo/waves/round-{52,53,55}/sources/*.html`, e.g. `round-55/sources/S418.html:343`
  `<a href="https://info-search.yahoo.co.jp/sitemaps/index.php">サイトマップ</a>`), i.e. the lane has
  *linked* this page repeatedly without ever opening it as a source.

## FLIP CONDITION (what would make this ADMIT-LATER):

The ground is in scope, the page is live and readable, the quote is page-unique and within the ceiling,
and no registry row or id collides — so nothing here is permanently inadmissible. The candidate fails
only on its citation and gloss. Two admissible flips:

- **Flip A (cheapest, keep the cited page):** keep `https://info-search.yahoo.co.jp/sitemaps/index.php`
  as the source; **delete the "updated or new pages are then crawled sooner" clause** from the entry and
  from the S382 `teaches` cell (it is not on this page); add two more located quotes from the same fetch
  — `ファイルサイズや記述できるURL数に上限があります` (22 units) and `クローラーは効率的にサイトを巡回できます`
  (20 units), or `robots.txtでSitemapsの場所を検索エンジンに伝える` (15 units) — so the entry carries ≥3
  distinct page-unique 6–25-unit spans; and re-label the "one mechanism / operator's own design"
  closure as `[INFERENCE]` (or drop it).
- **Flip B (re-anchor to the rule pages):** move the source line to the two sub-pages that actually
  state the claims — `archives/002859.php` (crawl efficiency + "sooner"; a ≤25-unit slice such as
  `より早く巡回されるようになります`, 16 units) and `archives/002863.php` (the placement rule; slices such
  as `Sitemapsは、ファイルを設置する場所によって`, 16 units, and
  `robots.txtでSitemapsのURLを記述することによって`, 13 units) — with their own retained bodies and
  sha256 receipts, and keep the category index only as the listing that links them.

Either way the entry must not restate S012/S013's placement rule as new mechanism (see VERDICT TABLE row
10); claim (3) is admissible only as the operator's own wording of ground `crawl-scope-per-host.md`
already holds.

Note on the ceiling: the placement quote is exactly **25/25** units, so any edit that appends a character
(such as a trailing `。` from the same sentence) breaks the ≤25 rule — the quote must be re-counted after
any wording change.

Tools: no tool was installed or upgraded for this seat (none needed); all commands used were `curl`,
`grep`, `git show`/`git grep`, `sha256sum`, `wc`, and a local `python3` unit counter replicating the
committed counter's regex.

VERDICT: REJECT as staged (claims (1)-second-half and the "one mechanism / operator's own design"
closure are not on the cited page and the latter is an unmarked inference; only 1 located span present) —
flip to ADMIT-LATER under Flip A or Flip B above.
