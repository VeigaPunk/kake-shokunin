# EntryRobotsBasics

Claim C2, row S418 — `https://info-search.yahoo.co.jp/archives/002885.php`. I read the retained body
`.ufo/waves/round-55/sources/S418.html` end to end (tags stripped, every text node printed): 7559 bytes,
sha256 `2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c`, matching `sources/receipts.json`
(HTTP 200, 2026-10-25T20:40:14Z, executor's fetch — no network request by this seat). Every quote below was
located by raw substring search in that file; nothing in the lane was written except this report.

## ENTRY:

```markdown
source: S418 — https://info-search.yahoo.co.jp/archives/002885.php — § robots.txtとは？ (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — curl -fsSL 'https://info-search.yahoo.co.jp/archives/002885.php' | grep -F -c '検索エンジンに対する要求を伝えるファイルです'
ground: per-engine crawl hygiene — what the operator's refusal file is for, where the crawler looks for it on a crawl, and what an unplaced file is taken to mean

# robots.txt is a request channel the crawler looks for at the site root

The lane holds the protocol (`robots-txt-rules.md`) and the host-root scope
(`crawl-scope-per-host.md`); this page is the operator's own framing of the file [S418].

## What the file is, and what it can carry

> "検索エンジンに対する要求を伝えるファイルです"

(rendered: it is a file that conveys a request to the search engine). A definition, placed first; the
actor arrives next as サイト管理者, the site administrator [S418]. It can carry two items [S418]:

> "クローラーに巡回してほしくないウェブページ"

(rendered: the web pages the administrator does not want the crawler to crawl). The item continues
with the fragment "やディレクトリ" (or directories), so pages and directories share one item, and
the page attaches it to crawling (巡回) and to nothing else [S418].

> "サイトマップの位置"

(rendered: the location of the sitemap). Two payloads of one file — a crawl preference and a discovery
pointer — and the page gives the syntax of neither line [S418].

## When the crawler reads it

> "クローラーはrobots.txtの記述に従って"

(rendered: the crawler, in accordance with what robots.txt says)

> "サイト内のウェブページを巡回します"

(rendered: crawls the web pages inside the site). One sentence: subject the crawler, scope サイト内
(inside the site) [S418]. The lookup that precedes that crawl carries its own qualifier [S418]:

> "クローラーによる巡回の際は"

(rendered: on the occasion of a crawl by the crawler — per crawl, not once per site lifetime).

> "まずサイトのルートディレクトリ"

(rendered: first, the site's root directory — まず places the lookup ahead of the crawl)

> "（サイトの一番上の階層）にあるrobots.txtを探します"

(rendered: it looks for the robots.txt that is in the parenthetical, which glosses the root directory
as the topmost level of the site). One location, the site root; one filename [S418].

## Absence and presence

> "robots.txtが設置されていなかった場合には"

(rendered: in the case where robots.txt has not been placed)

> "そのサイトに対する巡回制限はないものとみなして"

(rendered: the crawler treats it as having no crawl restriction for that site — そのサイトに対する
scopes the conclusion to that site, and みなして marks a treatment, not a finding)

> "robots.txtが設置されていた場合には"

(rendered: in the case where robots.txt has been placed)

> "その内容に従って巡回します"

(rendered: it crawls in accordance with that content).

The condition is 設置, the file's placement — not an HTTP outcome: the page states no status code,
no redirect, no fetch failure, no cached copy [S418]. That side is the RFC's, as
`robots-txt-rules.md` states it (4xx means crawlers MAY access resources; an unreachable file
requires the complete-disallow assumption): the page says what an unplaced file means for the crawl,
the RFC says what each HTTP outcome means.

The page's unit is サイト, the site, and its ルートディレクトリ is the one place looked in; the lane's
scope is the service (protocol, authority, port) — see `robots-txt-rules.md`, `crawl-scope-per-host.md`.

## What this entry does not establish

- No directive name, wildcard, end marker or case rule: the page carries no directive token and
  points at its own refusal-settings pages サイト単位、ディレクトリ単位での巡回の拒否設定 1 and 2
  (rows S372, S373) [S418].
- No HTTP-status, redirect or caching rule; no sitemap format or sitemap-line support [S418].
- Nothing about the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`, S374): a file-level list
  and a link-level attribute are different surfaces.
- Nothing about any live property: no robots.txt was served and no crawl was observed [S418].
- [INFERENCE] Reading サイト as the RFC's service (scheme, host and port) is the lane's mapping: the
  page names no protocol, host or port.

## Quote classes

Each quotation is a raw substring of `.ufo/waves/round-55/sources/S418.html` (sha256 `2b146a72…`, 7559
bytes, HTTP 200 in `receipts.json`), occurs once, and is at most 25 units (one unit per CJK character).
Renderings are unquoted and keep the source's qualifiers: まず (first), 巡回の際は (per crawl), そのサイト
に対する (for that site), みなして (treated as), 設置 (placement), サイト内 (inside the site).

Scope note: a claim about what the operator's documentation states on one page of its info centre;
no robots.txt was served to any crawler for this lane, no crawl was observed, and no directive was
tested.
```

## GATE LINE:

```text
- S418 — https://info-search.yahoo.co.jp/archives/002885.php — accessed 2026-10-25 — § robots.txtとは？ (更新日 2010年11月24日) — quote: "検索エンジンに対する要求を伝えるファイルです" (22 units; raw substring of the retained body, sha256 2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c, 7559 bytes, HTTP 200)
```

Single double-quoted span, so `c55_quote_truth.py`'s `quotes[-1]` is the located quote; URL and round date present; 22 units inside 6..25. Heading tag `<h2>robots.txtとは？</h2>`; date tag `<p class="update">更新日 2010年11月24日</p>` (page-level; no per-section date).

## ROW:

```text
| Yahoo! JAPAN robots.txt basics (r55) | `knowledge/yahoo-japan-robots-txt-basics.md` (S418) | request channel with two payloads (pages, sitemap location); root-directory lookup on each crawl, absent file = no restriction, present = follow contents |
```

Coverage cell = 22 whitespace tokens, sharing `request` and `channel` with the entry H1; the backticked path is followed by a backtick, so `c55_readme_index.py`'s `(?![A-Za-z0-9_.-])` guard matches (not dangling).

## UNIT COUNTS:

Rule (`c55_quote_truth.py:units()`): one unit per CJK character (kana/ideograph ranges), one per whitespace token holding no CJK character; CJK punctuation such as 、。（） counts 0.

- 22 検索エンジンに対する要求を伝えるファイルです · 21 クローラーに巡回してほしくないウェブページ · 7 やディレクトリ · 9 サイトマップの位置
- 13 クローラーはrobots.txtの記述に従って · 17 サイト内のウェブページを巡回します · 13 クローラーによる巡回の際は · 15 まずサイトのルートディレクトリ
- 18 （サイトの一番上の階層）にあるrobots.txtを探します · 15 robots.txtが設置されていなかった場合には · 23 そのサイトに対する巡回制限はないものとみなして · 12 robots.txtが設置されていた場合には · 13 その内容に従って巡回します

13 spans, all ≤ 25 and raw substrings of the retained body, each occurring exactly once (python `in` / `str.count` on the same bytes).

## RECHECK RUN:

- Header grep form, run against the RETAINED body: `grep -F -c '検索エンジンに対する要求を伝えるファイルです' .ufo/waves/round-55/sources/S418.html` → printed `1`, exit 0.
- Same form for クローラーに巡回してほしくないウェブページ, その内容に従って巡回します and （サイトの一番上の階層）にあるrobots.txtを探します → `1` each; the other nine via python `str.count` → `1` each.
- The network form (`curl -fsSL … | grep -F -c …`) was NOT run: this seat made no fetch.

## OMITTED:

- Breadcrumb `トップページ > 基本事項`, the 基本事項 list (8 items), the カテゴリ一覧 list (6 categories), the `個別リンクURL` widget, footer links, `© LY Corporation`, `robots-nocontent` skip markers: navigation only.
- The three cross-reference link titles are named but not quoted: link text to other pages (S372, S373, and `archives/002859.php` — no lane row, not opened), so quoting them grounds nothing on this page.
- Directive names, wildcard/end-marker syntax, case-sensitivity, `crawl-delay`, HTTP-status handling and sitemap syntax: absent from this page, recorded as absences, not imported from siblings or the RFC.
- Staged candidate `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/yahoo-japan-robots-txt-basics.md` read for shape only. Not carried: its `source: S380` id (renumbered S418 by document), its `recheck: 180d` line without a runnable command, its single quote (46 units under the counter's rule, ceiling 25 — measured, not adopted), and its index-timing sentence (a file placed today changes the next crawl, not today's index) — the page states no index timing.

VERDICT: S418 entry drafted quote-true (13 spans, all ≤25 units, all raw substrings of the retained body); Gate line and coverage row produced; nothing written outside this report.
