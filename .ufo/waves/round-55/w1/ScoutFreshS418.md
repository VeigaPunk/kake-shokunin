# ScoutFreshS418

Seat: ScoutFreshS418 (leaf, round-55 W1, lane `kake-shokunin`).
Assignment: independent re-open of S418 — fetch `https://info-search.yahoo.co.jp/archives/002885.php`
myself, compare with the retained body, and locate the page's operative rules from my OWN fetch.

## FETCH:

- Command: `curl -sSL` (plain GET, read-only, no auth headers, no cookies replayed), 2026-10-25.
- Status: HTTP 200; `content-type: text/html; charset=UTF-8`; final URL `https://info-search.yahoo.co.jp/archives/002885.php` (no redirect).
- Bytes: 7559 (curl-reported `size_download` = 7559; `wc -c` on the saved body = 7559).
- sha256 (my fetch): `2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c`
- Retained body `.ufo/waves/round-55/sources/S418.html`: bytes 7559, sha256 `2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c` → **byte-identical** (`cmp` exit 0; also UTF-8-normalized diff empty).
- `receipts.json` entry `S418`: url matches, `httpStatus` 200, `bytes` 7559, `sha256` `2b146a72…9312c` → **all three fields match my live fetch**.
- Robustness: a second fetch with `curl -sSL -A "kake-shokunin-round55"` (the receipt's recorded UA) returned the same 7559 bytes and the same sha256 → the retained body is UA-stable, not UA-frozen.
- Drift: **none** (status, byte length, and sha256 all equal). Freshness of the retained body is confirmed against the live origin.
- All quotes below were located in MY OWN fetched copy (temp dir `/tmp/tmp.RX9c8ELzCu/S418.html`), not read out of the retained file; each was then re-confirmed as a raw substring of the retained body (identical bytes ⇒ same result) via Python `in` and `grep -cF` (all ≥ 1, `grep -F` literal, no regex).
- Unit counting: rule = one unit per CJK character + one unit per non-CJK whitespace-delimited token. I also report a `worst` count (every ASCII char counted separately) as a safety margin; every quote is ≤ 25 units under the rule count, and every one except the two "worst" ones is also ≤ 25 under the worst count. No quote exceeds 25 under either reading.
- Tooling: no new tool installed (curl + python3 already present). No pacman run.

## LOCATED QUOTES:

Section key: the only `h2` in the body is "robots.txtとは？"; the body has one `p.update` line (更新日) and three body paragraphs; there is no `h3` inside the main content (the `h3` elements in the file are sidebar "「基本事項」カテゴリ" / "カテゴリ一覧" navigation modules, not operative rules). All quotes below sit in the main article body under the `h2` "robots.txtとは？" unless noted.

| # | Heading / section | Quote (raw substring) | Units (rule / worst) | Literal English reading |
|---|---|---|---|---|
| H | h2 page title | "robots.txtとは？" | 4 / 12 | "What is robots.txt?" — the article title question. |
| D | body, revision line `p.update` | "更新日 2010年11月24日" | 9 / 14 | "Updated date 24 November 2010" — the page's printed last-update date. |
| 1 | body ¶1, first sentence | "robots.txtは、検索エンジンに対する要求を伝えるファイルです" | 22 / 22 | "robots.txt is a file that conveys requests to search engines." (Sentence continues in the body with the site's description clause; quote stops at the full stop.) |
| 2 | body ¶1, second clause | "サイト管理者はrobots.txtをとおして" | 13 / 22 | "Site administrators, through robots.txt, …" — the subject of the following list; the page says site administrators CAN ("できます") convey the listed information through robots.txt. |
| 3 | body ¶1, list item 1 | "巡回してほしくないウェブページやディレクトリ" | 22 / 22 | "web pages and directories that [you] do not want crawlers to crawl" — i.e. pages/directories to keep out of crawling. (The list item begins "クローラーに巡回してほしくない…"; the full item is 28 CJK units and would breach the 25-unit ceiling, so the quote is trimmed at the start.) |
| 4 | body ¶1, list item 2 | "サイトマップの位置" | 9 / 9 | "the location of the sitemap" — the second thing robots.txt can convey. |
| 5 | body ¶2, sentence 1 | "クローラーはrobots.txtの記述に従って" | 14 / 23 | "Crawlers, in accordance with the description in robots.txt, …" — the crawl behaviour is governed by the file's content. |
| 6 | body ¶2, sentence 1, tail | "サイト内のウェブページを巡回します。" | 18 / 18 | "… crawl the web pages within the site." — scope of the crawl, and the verb is "crawl" (巡回), not "index". |
| 7 | body ¶2, sentence 2 | "まずサイトのルートディレクトリ" | 15 / 15 | "first … the root directory of the site" — where the crawler looks first. |
| 8 | body ¶2, sentence 2, parenthetical | "サイトの一番上の階層" | 10 / 10 | "the topmost hierarchy of the site" — the page's own definition of the root directory. |
| 9 | body ¶2, sentence 2, tail | "サイトの一番上の階層）にあるrobots.txtを探します。" | 21 / 21 | "looks for the robots.txt that is in (the topmost hierarchy of the site)." — the file is looked up at the site root. |
| 10 | body ¶2, sentence 3, first clause | "robots.txtが設置されていなかった場合には" | 16 / 25 | "if robots.txt has not been installed (placed), …" — conditional on absence of the file. |
| 11 | body ¶2, sentence 3, first clause, tail | "そのサイトに対する巡回制限はないものとみなして" | 23 / 23 | "… it is regarded as there being no crawl restriction for that site" — the absence default. |
| 12 | body ¶2, sentence 3, second clause | "robots.txtが設置されていた場合には" | 13 / 22 | "if robots.txt has been installed, …" — conditional on presence of the file. |
| 13 | body ¶2, sentence 3, second clause, tail | "その内容に従って巡回します。" | 14 / 14 | "… it crawls according to its contents." — the presence behaviour. |

Quotes 1–13 are all raw substrings of the fetched body (Python `in` = True; `grep -cF` count ≥ 1). Quotes 3 and 8 are deliberate partial spans of a longer sentence/list item, chosen only to stay under the 25-unit ceiling; the trimmed-out surrounding text is reported above in the reading column and is present verbatim in the body.

## RULES:

(a) Printed revision date: **"更新日 2010年11月24日"** (24 November 2010) — the page's `p.update` line. The page also carries `<meta name="robots" content="index,follow,noarchive,noodp" />` and the meta description "robots.txtは、検索エンジン（クローラー）に対してサイト内の巡回時の要求を伝えるファイルです。" (the latter restates rule 1 with the parenthetical "（クローラー）" that the visible body sentence omits). The visible body text is the operative text; the meta description is boilerplate head metadata.

(b) Rules the page states that a publisher could get wrong:

1. **What robots.txt is for.** It is the file through which a site tells search engines what to do; specifically it can carry two things (site administrators "can" convey them, i.e. permission not obligation): (i) web pages/directories that crawlers should not crawl, and (ii) the location of the sitemap. (Quotes 1–4.)
2. **Crawlers crawl the site's web pages in accordance with robots.txt's description.** The page's verb for what robots.txt governs is crawling (巡回), not indexing — the page never says robots.txt controls indexing or removal from the index. (Quotes 5–6.)
3. **Placement: the file is looked for first at the site root.** "First" the crawler looks in the site's root directory, which the page defines as "the topmost hierarchy of the site" — the root is the top level, not a per-directory or per-path location. (Quotes 7–9.)
4. **Absence default.** If robots.txt has not been installed, the crawler is deemed to have no crawl restriction for that site and crawls the site's web pages. So *not* having robots.txt is not a block, and having one is not a block by itself. (Quotes 10–11.)
5. **Presence behaviour.** If robots.txt has been installed, the crawler crawls according to that file's contents. (Quotes 12–13.)
6. **The page defers the actual syntax.** The body says only that the description of robots.txt and the method of placing it are covered on other pages, and links to three: "サイト単位、ディレクトリ単位での巡回の拒否設定 1" (`/archives/002849.php`, = S372), "サイト単位、ディレクトリ単位での巡回の拒否設定 2" (`/archives/002850.php`, = S373), and "サイトマップによる効率的な巡回" (`/archives/002859.php`). So this page states the *rules of the mechanism* but no directive syntax, no file-name casing rule, no size limit, no syntax examples.

## OVERREADS:

Statements a plausible but careless gloss would add that this page does **not** make (each verified absent from the fetched body):

1. That robots.txt controls **indexing / de-indexing** ("blocked pages won't appear in results"). The page only ever says crawling (巡回) and the crawl restriction for the site; it never mentions インデックス in the operative body. (The word appears only in the unrelated sidebar link "インデックス", a category name.)
2. That robots.txt is **mandatory**, or that its absence blocks or de-indexes the site. The page states the opposite default: absence is treated as no crawl restriction.
3. That robots.txt **must** contain a sitemap directive. The page says the file *can* convey the sitemap location ("伝えることができます"), not that it must.
4. That a robots.txt **applies only to Yahoo! JAPAN**, or conversely that it is a cross-engine standard enforced by all crawlers. The page speaks generically of "search engines" and "crawlers" and never says which engines honour it; the site's own category list shows sibling pages on ディレクティブ設定 etc., but no enforcement scope is stated here.
5. Any **directive syntax** (User-agent, Disallow, Allow, Sitemap: line format, wildcards, path matching), **file encoding**, **maximum size**, **crawl-delay**, **HTTP status of a missing robots.txt**, or **per-host/per-protocol scoping**. None appear; the page explicitly points elsewhere for description and placement method.
6. That robots.txt is a **security or access-control** mechanism (it is a request channel to search engines; the page calls it "要求を伝える", not protection) — the page states nothing about privacy, credentials, or blocking non-search-engine scrapers.
7. That the page states a **current** policy or validity date. The only date on the page is the printed 更新日 of 2010-11-24; the page asserts nothing about the file's ongoing validity, and it says nothing about how the content was updated or reviewed.
8. That **no robots.txt in a subdirectory** is used, or that the root file can be overridden per-subdirectory. The page mentions the root directory only; the "サイト単位、ディレクトリ単位での巡回の拒否設定" pages (S372/S373) are linked but their content is not reproduced here, so any per-directory rule would have to be sourced there, not here.
9. That the crawler **respects** robots.txt in the sense of a guarantee, or that violating it has consequences (penalties, de-indexing). The page only describes crawl behaviour ("従う"), with no enforcement or penalty statement.
10. That the page **recommends** or **requires** listing sitemap locations in robots.txt. The list under "次の情報を伝えることができます" is an enumeration of what can be conveyed, with no modal force.

Confidence: high for all findings above (byte-identical live fetch, every quote re-verified as a raw substring by two independent methods, headings parsed from the DOM). Unresolved/unverified: the *content* of the three linked pages (S372, S373, `/archives/002859.php`) was not re-fetched here — S372/S373 are other seats' scope; `/archives/002859.php` was not fetched and is not covered by this report.

VERDICT: Live re-fetch of S418 is byte-identical to the retained body (7559 bytes, sha256 2b146a72…9312c, matching receipts.json on status/bytes/hash — no drift); 13 operative passages located from my own fetch, all ≤25 units and raw substrings, with the printed revision date 2010年11月24日, 6 publisher-facing rules, and 10 overread traps the page does not support.
