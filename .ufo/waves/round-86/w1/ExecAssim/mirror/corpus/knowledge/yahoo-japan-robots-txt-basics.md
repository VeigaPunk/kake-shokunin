source: S418 — https://info-search.yahoo.co.jp/archives/002885.php — § robots.txtとは？ (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — curl -fsSL 'https://info-search.yahoo.co.jp/archives/002885.php' | grep -F -c '検索エンジンに対する要求を伝えるファイルです' -> 1 (curl form and the same grep against the retained body, both 1, 2026-10-25)
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

(rendered: on the occasion of a crawl by the crawler — the page binds the lookup to the crawl; it states no lookup frequency).

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
  (rows S372, S373) and at a third page on the sitemap, quoted raw [S418]:

> "サイトマップによる効率的な巡回"

  (rendered: the page's third link — efficient crawling by means of a sitemap; its content is not read
  here and no row is held for it).
- No HTTP-status, redirect or caching rule; no sitemap format or sitemap-line support [S418].
- Nothing about the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`, S374): a file-level list
  and a link-level attribute are different surfaces.
- Nothing about any live property: no robots.txt was served and no crawl was observed [S418].
- [INFERENCE] Reading サイト as the RFC's service (scheme, host and port) is the lane's mapping: the
  page names no protocol, host or port.

## Quote classes

Each quotation is a raw substring of `.ufo/waves/round-55/sources/S418.html` (sha256 `2b146a72…`, 7559
bytes, HTTP 200 in `receipts.json`), occurs once, and is at most 25 units (one unit per CJK character).
Renderings are unquoted and keep the source's qualifiers: まず (first), 巡回の際は (on the occasion of a crawl), そのサイト
に対する (for that site), みなして (treated as), 設置 (placement), サイト内 (inside the site).

Scope note: a claim about what the operator's documentation states on one page of its info centre;
no robots.txt was served to any crawler for this lane, no crawl was observed, and no directive was
tested.
