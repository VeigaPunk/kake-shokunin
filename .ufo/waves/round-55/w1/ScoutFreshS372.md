# ScoutFreshS372

Independent re-open of S372 (`https://info-search.yahoo.co.jp/archives/002849.php`), read-only.
Base revision `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`; round date 2026-10-25.
All quotes below were taken from **my own fetch** (2026-10-25T20:48Z), not from the retained file,
and each was then re-verified as a raw substring of the retained body as well.

Tooling: no install or upgrade was needed (`curl`, `python3`, `sha256sum`, `cmp` all present); no
pacman transaction was run. Unit counting uses the lane's own canonical rule copied from
`.ufo/waves/round-55/c55_quote_truth.py:137-139` (one unit per CJK character, one per non-CJK
whitespace token).

## FETCH:

| field | value |
|---|---|
| method | plain GET, `curl -sSL`, read-only, no POST, no cookie jar, no auth |
| URL | `https://info-search.yahoo.co.jp/archives/002849.php` |
| HTTP status | `200` (observed; `curl -w http_code=%{http_code}`) |
| bytes (my fetch) | `10168` (`size_download=10168`, and `wc -c` = 10168) |
| sha256 (my fetch) | `ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111` |
| retained body bytes | `10168` (`.ufo/waves/round-55/sources/S372.html`) |
| retained body sha256 | `ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111` |
| receipts.json S372 | `bytes: 10168`, `sha256: ee8c9def…00111`, `httpStatus: 200`, `fetchedAt: 2026-10-25T20:40:13+00:00`, `userAgent: kake-shokunin-round55` |

**Match, no drift.** `cmp` reports byte-for-byte equality between my fetch and the retained
`S372.html` (both with a custom `User-Agent: kake-shokunin-round55` and with curl's default UA —
two separate fetches, both identical). Length and sha256 agree with `receipts.json` on all three
fields (bytes / sha256 / httpStatus). The receipt's `fetchedAt` is 8 minutes before my fetch;
the page did not change in that window.

## LOCATED QUOTES:

Section keys use the page's own heading/element names: the page's `<h2>` is
`サイト単位、ディレクトリ単位での巡回の拒否設定 1`; the two `<h3>`s are `大文字と小文字の区別`
and `Allowの使い方`; `用語` is a `<dt>` inside `<dl class="advice">`; `例：` is a `<dt>` in the
example `<dl>`s; `pre` is the literal `<pre>` block; `p.update` is the revision-date line.

| # | Section | Quote | Units | Literal English reading |
|---|---|---|---|---|
| 1 | h2 / lead paragraph | "「robots.txt」という名前でテキストファイルを用意し" | 18 | Prepare a **text file** bearing the name "robots.txt" |
| 2 | h2 / lead paragraph | "ファイルは、サイトのルートディレクトリに設置" | 21 | [place] the file at the **site's root directory** |
| 3 | 例： (dl, 例 1) | "すべての検索エンジンのクローラーの巡回を拒否する" | 24 | to refuse the crawl of **all search engines' crawlers** |
| 4 | 例： (dl, 例 1) / pre | "User-agent: *" | 2 | User-agent: * |
| 5 | 例： (dl, 例 1) / pre | "Disallow: /" | 2 | Disallow: / |
| 6 | h2 / after 例 1 | "「User-agent: *」は、「すべてのクローラー」という意味になります。" | 21 | "User-agent: *" means "**all crawlers**" |
| 7 | h2 / after 例 1 | "「Disallow: /」に続いてそのディレクトリ名を指定します。" | 20 | follow "Disallow: /" with **that directory's name** |
| 8 | 例： (dl, 例 2) | "cgi-binというディレクトリのみを拒否対象にしたいとき" | 22 | when you want **only the cgi-bin directory** to be a refusal target |
| 9 | 例： (dl, 例 2) / pre | "Disallow: /cgi-bin/" | 2 | Disallow: /cgi-bin/ |
| 10 | h2 / after 例 2 | "巡回の拒否（Disallow:）、クローラーの受け入れ（Allow:）の記述の前には" | 22 | before the descriptions of crawl-refusal (Disallow:) and crawler-acceptance (Allow:) |
| 11 | h2 / same paragraph | "この記述がないときはすべてのクローラーに対する指示" | 25 | when that description is absent, [it is] an instruction **to all crawlers** |
| 12 | h2 / same paragraph | "「*」と同様）とみなされます。" | 10 | is treated as **the same as "*"** |
| 13 | h2 / para "また、robots.txtが…" | "robots.txtが設置されていない場合" | 11 | when robots.txt **is not installed** |
| 14 | h2 / same paragraph | "サイトに対する巡回の制限はないものとみなされます。" | 24 | it is deemed that **there is no crawl restriction on the site** |
| 15 | h2 / same paragraph | "クローラーは巡回のたびにrobots.txtの有無を確認しており" | 22 | the crawler **checks for the presence of robots.txt on every crawl** |
| 16 | h2 / same paragraph | "インデックスを更新し、検索結果に反映されるまでには" | 24 | until the index is updated and reflected in the search results, **time passes** |
| 17 | h2 / same paragraph | "すぐに設定の内容が反映されるわけではありません。" | 23 | it is **not** the case that the setting's content is reflected immediately |
| 18 | 用語 (dl.advice) | "「ルートディレクトリ」とは" | 11 | "ルートディレクトリ" (root directory) **means** … |
| 19 | 用語 (dl.advice) | "サイトの一番上の階層を指します。" | 15 | it denotes **the site's topmost hierarchy** |
| 20 | 用語 (dl.advice) | "http://example.com/robots.txtなどとなるように" | 8 | so that it becomes http://example.com/robots.txt **and the like** |
| 21 | 用語 (dl.advice) | "「robots.txt」を保存してください。" | 9 | please **save "robots.txt"** [there] |
| 22 | 用語 (dl.advice) | "ルートディレクトリに任意のファイルを設置できない" | 24 | if you **cannot place an arbitrary file at the root directory** |
| 23 | 用語 (dl.advice) | "「robots.txt」による巡回拒否はできません。" | 13 | crawl-refusal **by "robots.txt" is not possible** |
| 24 | 用語 (dl.advice) | "メタタグで、インデックスへの登録拒否を設定" | 20 | set, **with a meta tag**, refusal of registration to the index |
| 25 | h3 大文字と小文字の区別 | "Allow（許可）のあとに記述されたディレクトリ名は" | 19 | the **directory name written after Allow (permitted)** … |
| 26 | h3 大文字と小文字の区別 | "大文字と小文字の違いがあった場合" | 16 | **when there is an uppercase/lowercase difference** … |
| 27 | h3 大文字と小文字の区別 | "別のものとして扱います。" | 11 | is treated as **a different thing** |
| 28 | h3 大文字と小文字の区別 / pre | "Disallow: /private" | 2 | Disallow: /private |
| 29 | h3 大文字と小文字の区別 / pre | "Disallow: /Private" | 2 | Disallow: /Private |
| 30 | h3 大文字と小文字の区別 / pre | "Disallow: /PRIVATE" | 2 | Disallow: /PRIVATE |
| 31 | h3 Allowの使い方 | "「Allow:」は通常「Disallow:」と組み合わせて使用します。" | 15 | "Allow:" is **normally (通常)** used **in combination with** "Disallow:" |
| 32 | h3 Allowの使い方 | "あるディレクトリのなかの特定のウェブページだけを" | 24 | [for] **only a specific web page inside** a certain directory … |
| 33 | h3 Allowの使い方 / pre | "Disallow: /foo/" | 2 | Disallow: /foo/ |
| 34 | h3 Allowの使い方 / pre | "Allow: /foo/bar.html" | 2 | Allow: /foo/bar.html |
| 35 | h3 Allowの使い方 / closing sentence | "この例では、「foo」ディレクトリ以下は巡回を拒否するが" | 22 | in this example, **everything under the "foo" directory is refused**, but |
| 36 | h3 Allowの使い方 / closing sentence | "/foo/bar.htmlは巡回を許可するという意味を持ちます。" | 18 | **/foo/bar.html is permitted to be crawled** — that is what it means |
| 37 | p.update | "更新日 2010年11月24日" | 6 | Update date: 2010-11-24 |

Every row: raw substring of my fetch **and** of the retained `S372.html` (verified both by
Python `in` and by `grep -F` on the retained file), and unit count ≤ 25 under the lane's
canonical `units()`. Quotes 1, 4, 5, 9, 28-30, 33, 34 are code/example lines and therefore
count as few units; quotes 3, 8, 10, 12, 16, 18-21, 24, 25, 26, 32, 35, 37 are short fragments
chosen so that no sentence exceeds the 25-unit ceiling.

## RULES:

(a) **Printed revision date**: `更新日 2010年11月24日` — 2010-11-24. It is the only date on the
page; it sits in `<p class="update">` directly under the `<h2>`. The receipt's own `fetchedAt`
(2026-10-25) is the access date, not a revision date; the page prints no "last verified" or
"still current" marker.

(b) **Rules the page states that a publisher could get wrong** (each traceable to a quote above):

1. The refusal file is a **text file named exactly "robots.txt"**, placed at the **site's root
   directory** — not in a subdirectory, not under any other name (Q1, Q2).
2. To refuse all search-engine crawlers: `User-agent: *` plus `Disallow: /` (Q3-Q5).
3. `User-agent: *` means **all crawlers**, not merely search engines (Q6).
4. To refuse only one directory, follow `Disallow: /` with **that directory's name** — the
   example writes it with a trailing slash, `Disallow: /cgi-bin/` (Q7-Q9).
5. The **target crawler's user-agent name must be written before** the Disallow:/Allow:
   description; when that description is absent the instruction is treated as one to **all
   crawlers**, i.e. **the same as "*"** (Q10-Q12).
6. If **no robots.txt is installed**, the site is deemed to carry **no crawl restriction** —
   absence is permission, not a default-deny (Q13-Q14).
7. The crawler **checks for the file's presence on every crawl**, so a file installed later is
   followed from the next crawl onward (Q15).
8. Placement is **not immediate**: updating the index and reflecting it in the search results
   **takes time**, so the setting's content is **not reflected immediately** (Q16-Q17).
9. "ルートディレクトリ" means **the site's topmost hierarchy**; the file must land there, e.g.
   `http://example.com/robots.txt` — "and the like" for other layouts (Q18-Q21).
10. If you **cannot place an arbitrary file at the root directory**, crawl-refusal by robots.txt
    **is not possible**; the substitute instruction is to set, **with a meta tag**, a refusal of
    registration to the index (Q22-Q24).
11. The **directory name written after Disallow/Allow is case-sensitive** — `private`, `Private`,
    `PRIVATE` are three distinct directories (Q25-Q30).
12. `Allow:` is **normally** (通常) used **together with** `Disallow:`; the worked example pairs
    `Disallow: /foo/` with `Allow: /foo/bar.html`, meaning everything **under** the foo
    directory is refused while `/foo/bar.html` is permitted (Q31-Q36).

## OVERREADS:

Statements a plausible but careless gloss would add that **this page does not make** (checked
against my own fetch; the term counts are over the whole 10168-byte body):

- **No crawl-delay / directive set.** No `Crawl-delay`, `Sitemap:`, `Request-rate` or any other
  robots directive appears (0 hits). The single サイトマップ hit is a nav link to the site's own
  sitemap category, not a robots.txt directive.
- **No wildcard or pattern syntax.** No ワイルドカード and no `*`/`$` pattern rules appear here;
  the only `*` on the page is the literal `User-agent: *` token. Pattern syntax is the subject of
  the *next* page (002850.php = S373). "This page defines `*` and `$` matching" is an overread.
- **No enforcement or penalty claim.** 強制 / 必須 / 遵守 / 強制力 / ペナルティ / 順位 all occur
  **0 times**. The page describes the crawler's *check*, never a duty to obey and never a ranking
  consequence. "Yahoo! JAPAN enforces robots.txt / penalises violators" is not on this page.
- **No precedence rule for Allow vs Disallow.** The page shows one paired example and says
  Allow is "通常" used with Disallow; it never states a general precedence algorithm (e.g. "the
  longest matching path wins"). The example's outcome is stated, the rule behind it is not.
- **No prefix-match / path-matching rule.** The page says only to follow `Disallow: /` with a
  directory name, and that the name is case-sensitive. It never says a rule is a string prefix,
  nor how a partial path is matched — that is page 2's subject.
- **No filename-case or User-agent-case rule.** Case-sensitivity is scoped, in the page's own
  words, to "the directory name written after Allow (permitted)" only. "The filename robots.txt
  must be lowercase" and "the User-agent name is case-sensitive" are both unstated.
- **No file-size, encoding, or fetch-status rules.** No size / line-count limit, no encoding
  requirement (the two UTF-8 hits are the page's own XHTML charset declarations), and no
  404 / 403 / 5xx behaviour for an unreachable or erroring robots.txt (0 hits each).
- **No security framing.** The file is framed as a crawl-refusal setting for crawlers, never as
  an access-control or security mechanism, and never as able to keep a page unreachable to readers.
- **No update-lag figure.** The page says index/serp reflection "takes time" but gives **no**
  duration or SLA. "Changes take 24-48 hours to take effect" is an addition.
- **No subdomain or protocol rule.** The root-directory rule is stated for "the site"; the page
  says nothing about per-subdomain robots.txt files or about which scheme the crawl uses.
- **No claim of currency.** The printed 更新日 is 2010-11-24, fifteen years before the round date.
  Presenting these as "the current, updated rules" overreads; the page carries no "as of" or
  "still valid" assertion beyond that date line.
- **Not the whole ruleset.** The title ends in "1", and the category list points to a sibling
  "サイト単位、ディレクトリ単位での巡回の拒否設定 2" (002850.php = S373) plus rel-attribute
  (002851.php) and server-side (002852.php) pages. Treating this page as the complete Yahoo!
  JAPAN crawl-refusal ruleset is an overread.

VERDICT: Independent re-fetch of S372 is byte-identical to the retained body and to receipts.json (HTTP 200, 10168 bytes, sha256 ee8c9def…00111 — no drift); 37 operative quotes located from my own fetch, each a raw substring and ≤25 units under the lane's canonical counter, with the printed revision date 2010年11月24日.
