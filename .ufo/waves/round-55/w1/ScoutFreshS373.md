# ScoutFreshS373

Independent re-open of S373 (`https://info-search.yahoo.co.jp/archives/002850.php`), read-only. Base revision `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`; round date 2026-10-25. All quotes below were taken from **my own fetch** (2026-10-25, ~20:48Z and ~20:50Z), not from the retained file, and each was re-verified as a raw substring of the retained body as well (python `in` on the decoded body, plus `grep -c -F` spot checks).

Tooling: no install or upgrade was needed (`curl 8.23.0`, `python3`, `sha256sum`, `cmp` all present); **no pacman transaction was run**. Unit counting uses the lane's own canonical rule copied from `.ufo/waves/round-55/c55_quote_truth.py:137-139` (one unit per CJK character, one per non-CJK whitespace token). That counter's CJK class excludes CJK punctuation (`、。「」（）`), so each quote is also counted under a stricter variant charging every CJK punctuation mark one unit; **every quote below is <= 25 units under both counts** (canonical 6-23, strict 6-25). No quote contains an ASCII double quote, so the ASCII-quoted rendering is unambiguous. Only this report file was written; no git mutation was performed (`git show`, `git ls-tree`, `git ls-files` only).

## FETCH:

| field | value |
|---|---|
| method | plain GET, `curl -sSL`, read-only; no request body, no authentication, no credential material sent |
| URL | `https://info-search.yahoo.co.jp/archives/002850.php` |
| HTTP status | `200` (observed via `curl -w http_code`; `curl -sSIL` shows `HTTP/2 200`, `content-type: text/html; charset=UTF-8`) |
| effective URL after redirects | `https://info-search.yahoo.co.jp/archives/002850.php` (no redirect) |
| bytes (my fetch) | `9402` (`size_download=9402`, `wc -c` = 9402, `stat -c %s` = 9402) |
| sha256 (my fetch) | `3173d9613128e1aaa7cb55919fa52438602095bd7bc54d4437760ee8b1c03885` |
| retained body bytes | `9402` (`.ufo/waves/round-55/sources/S373.html`) |
| retained body sha256 | `3173d9613128e1aaa7cb55919fa52438602095bd7bc54d4437760ee8b1c03885` |
| receipts.json S373 | `url` = the same URL, `httpStatus: 200`, `bytes: 9402`, `sha256: 3173d961…03885`, `fetchedAt: 2026-10-25T20:40:14+00:00`, `userAgent: kake-shokunin-round55` |
| second fetch (UA `kake-shokunin-round55`) | HTTP 200, 9402 bytes, same sha256 |

**Match, no drift.** `cmp` reports byte-for-byte equality between my fetch and the retained `S373.html`; the decoded text of the two files is also identical (`ret == mine` → True). Length, sha256 and httpStatus agree with `receipts.json` on all three fields. The receipt's `fetchedAt` is ~8 minutes before my fetch and the bytes are unchanged across that window and across two different user agents, so the page is stable at the round date.

## LOCATED QUOTES:

Section keys use the page's own element names. The `<h2>` is `サイト単位、ディレクトリ単位での巡回の拒否設定 2`; the two `<h3>`s are `「*」記号` and `「$」記号`; `注意` is a `<dt>` inside `<dl class="advice">` (two such blocks, one under each `<h3>`); `記号/マッチ` is the two-column `<table>`; `例：` is inline in the `<ol>` items; `p.update` is the revision-date line; `括弧` is the parenthetical inside the `$` example's first `<ol>` item. The `<meta name="description">` is head content, not body content, and is listed separately after the table.

| # | Section | Quote | Units (canon / strict) | Literal English reading |
|---|---|---|---|---|
| 1 | p.update | "更新日 2010年11月24日" | 6 / 6 | Update date: 2010-11-24 |
| 2 | body intro, before 記号/マッチ | "robots.txtでは、以下のパターン記号が使用できます。" | 18 / 20 | In robots.txt, the following pattern symbols can be used. |
| 3 | 記号/マッチ table, `*` row | "ワイルドカードのパターンマッチ" | 15 / 15 | wildcard pattern match |
| 4 | 記号/マッチ table, `$` row | "URLの末尾文字のパターンマッチ" | 13 / 13 | pattern match on the URL's trailing character(s) |
| 5 | h2 title | "サイト単位、ディレクトリ単位での巡回の拒否設定 2" | 23 / 24 | Refusal settings for per-site and per-directory crawling, part 2 |
| 6 | §「*」記号, 1st clause | "「*」記号は、任意の長さの、任意のURL文字列に" | 16 / 20 | The `*` symbol is used to match, against a URL string of any length, any … |
| 7 | §「*」記号, 2nd clause | "URL文字列のいずれの部分にも使えます。" | 16 / 17 | … it can be used in any part of the URL string. |
| 8 | §「*」記号 → 例1 | "「public」で始まるすべてのディレクトリへの巡回を許可" | 21 / 23 | permit crawling of all directories that begin with `public` |
| 9 | §「*」記号 → 例1, 例 | "例：「/public_html/」や「/public_graphs/」も巡回されます。" | 9 / 15 | Example: `/public_html/` and `/public_graphs/` are also crawled. |
| 10 | §「*」記号 → 例2, 1st clause | "「_print」を含むすべてのファイルとディレクトリ" | 18 / 20 | all files and directories that contain `_print` … |
| 11 | §「*」記号 → 例2, 2nd clause | "すべてのファイルとディレクトリへの巡回を拒否" | 22 / 22 | … are refused crawling — files and directories alike |
| 12 | §「*」記号 → 例2, 例 | "例：「/card_print.html」や「/store_print/product.html」は巡回されません。" | 10 / 16 | Example: `/card_print.html` and `/store_print/product.html` are not crawled. |
| 13 | §「*」記号 → 例3 | "URL文字列に「?sessionid」を含むすべてのファイルへの巡回を拒否" | 22 / 24 | refuse crawling of all files whose URL string contains `?sessionid` |
| 14 | §「*」記号 → 例3, 例 | "例：「/cart.php?sessionid=342bca31」は巡回されません。" | 9 / 13 | Example: `/cart.php?sessionid=342bca31` is not crawled. |
| 15 | §「*」記号 → 注意, 1st clause | "以下のように書かれていた場合、" | 14 / 15 | when it is written as follows, … |
| 16 | §「*」記号 → 注意, 2nd clause | "2つの「Disallow」の指示は、同等とみなされます。" | 15 / 19 | the two `Disallow` instructions are treated as equivalent. |
| 17 | §「$」記号, 1st clause | "「$」記号は、URLの末尾にある、任意の文字列を" | 16 / 20 | The `$` symbol is used to match any string that sits at the end of the URL … |
| 18 | §「$」記号, 2nd clause | "URLの末尾にある、任意の文字列をマッチさせる" | 19 / 20 | … to match any string at the end of the URL. |
| 19 | §「$」記号 → 例1, 1st clause | "robots.txtが設置されたサイト以下で、" | 12 / 13 | at and below the site where robots.txt is installed, … |
| 20 | §「$」記号 → 例1, 2nd clause | "「.gif」で終わるすべてのファイルへの巡回を拒否" | 19 / 21 | refuse crawling of all files ending in `.gif` |
| 21 | §「$」記号 → 例1 括弧, 1st clause | "「$」を省き「/*.gif」とすると、ファイルパスに「.gif」を含む" | 17 / 24 | if you omit the `$` and write `/*.gif`, then [it matches] the file paths containing `.gif` |
| 22 | §「$」記号 → 例1 括弧, 2nd clause | "すべてのファイルの巡回が拒否されていること" | 21 / 21 | the crawling of all such files is what ends up being refused (the sentence closes になります) |
| 23 | §「$」記号 → 例2 | "「?」で終わるすべてのファイルへの巡回を許可" | 19 / 21 | permit crawling of all files ending in `?` |
| 24 | §「$」記号 → 注意 li1, 1st clause | "「$」記号がない場合、" | 7 / 10 | when there is no `$` symbol, … |
| 25 | §「$」記号 → 注意 li1, 2nd clause | "クローラーはプリフィクス（接頭辞）として扱い" | 20 / 22 | the crawler treats [it] as a prefix (head-word) and … |
| 26 | §「$」記号 → 注意 li1, 3rd clause | "記述された文字列を含むURLがすべてマッチします。" | 21 / 22 | every URL containing the written string matches. |
| 27 | §「$」記号 → 注意 li2, 1st clause | "「$」記号は、文字列の末尾でのみ意味をなします。" | 19 / 23 | The `$` symbol has meaning only at the end of the string. |
| 28 | §「$」記号 → 注意 li2, 2nd clause | "クローラーが「$」記号を見つけると、末尾であると判断" | 22 / 25 | when the crawler finds a `$` symbol, it judges [the position] to be the end … |
| 29 | §「$」記号 → 注意 li2, 3rd clause | "以降の文字列を無視します。" | 12 / 13 | and ignores the strings that follow it. |

Every quote is a raw substring of the retained body (`grep -c -F` returns >= 1 for each; the h2 title returns 3 because it also appears in `<title>` and in the category list).

Note on Q14: the value `342bca31` inside the example URL is the source page's own published illustrative placeholder, printed by Yahoo! JAPAN in the public documentation example; it is not live session material, and no credential, cookie, token or private URL is reproduced in this report.

Head-only text (not body content): the `<meta name="description">` carries "「*」や「$」の正規表現記号を使うことで" (14 / 18 units, raw substring) — "by using the `*` and `$` regular-expression symbols …" — and continues that several directives can be combined into one. The body text itself never uses 正規表現 (0 hits); it says パターン記号 (Q2) and ワイルドカードのパターンマッチ (Q3).

## RULES:

Every rule this page states that a publisher could get wrong (each anchored to a quote above):

1. **Exactly two pattern symbols exist for robots.txt** — only `*` and `$`, under a 記号 / マッチ table, introduced as "the following pattern symbols can be used" (Q2-Q4). No third symbol, no general regular-expression grammar.
2. **`*` matches a string of any length, anywhere in the URL string** — "to match, against a URL string of any length, any …", usable "in any part of the URL string" (Q6-Q7). Not a path-segment-only wildcard, not restricted to the beginning.
3. **`Allow: /public*/` permits every directory starting with `public`**, explicitly including `/public_html/` and `/public_graphs/` (Q8-Q9). Publisher trap: reading it as the `/public/` directory only.
4. **`Disallow: /*_print*.html` refuses files *and directories* that contain `_print`** — the page's wording names files and directories both — and its example includes a directory-style path, `/store_print/product.html` (Q10-Q12).
5. **`Disallow: /*?sessionid` refuses by a literal `?sessionid` inside the URL string**, example `/cart.php?sessionid=342bca31` (Q13-Q14). The `?` is part of that literal string; the page gives it no wildcard meaning.
6. **`Disallow: /private*` and `Disallow: /private` are equivalent** — "the two `Disallow` instructions are treated as equivalent" (Q15-Q16). Publisher trap: adding the shorter line as if it narrowed the rule, or assuming the two differ.
7. **`$` matches at the end of the URL** — "any string that sits at the end of the URL" (Q17-Q18); the table glosses it as a pattern match on the URL's trailing character(s) (Q4). It is not an "end-of-string anchor" in regex terminology; the page never uses that word.
8. **`Disallow: /*.gif$` refuses files ending in `.gif` at and below the site where robots.txt is installed** (Q19-Q20). The scope qualifier is part of the rule, not decoration.
9. **Omitting `$` changes the rule's reach from "ends with" to "contains"** — if you omit the `$` and write `/*.gif`, then the file paths containing `.gif` are the ones whose crawling "ends up being refused" (Q21-Q22). The single most publisher-confusable statement on the page.
10. **`Allow: /*?$` permits all files ending in `?`** (Q23).
11. **Without `$`, the crawler treats the written string as a prefix (接頭辞)**, and the page's wording for the effect is "every URL containing the written string matches" (Q24-Q26). Both halves are the page's; a gloss keeping only one is not the page's sentence.
12. **`$` is meaningful only at the end of the string**, and when the crawler finds a `$` it "judges [the position] to be the end and ignores the strings that follow it" (Q27-Q29). A `$` written mid-pattern is not an error to be reported — the crawler ignores what follows it.
13. **A `*` after a prefix broadens the rule on the `Allow` side too** — `/public*/` permits `/public_graphs/` (Q8-Q9), the mirror image of rule 9 for `Disallow`.

## OVERREADS:

Statements a plausible but careless gloss would add that **this page does not make** (absence counts are over my own 9402-byte fetch; body-only counts are over the `<div class="asset-body">` region):

- **No Allow-vs-Disallow precedence rule.** 優先 / 優先順位 occur 0 times. The page shows one `Allow:` and one `Disallow:` line inside the same `User-agent: *` block but states no algorithm (not "Allow wins", not "longest match wins"). "Allow overrides Disallow" is an addition.
- **No enforcement, penalty, ranking or duty language.** 強制 / 必須 / 遵守 / ペナルティ occur 0 times. The page describes matching behaviour, never a duty to obey or a consequence of violating.
- **No crawler-identity statement.** The page names no crawler and no user agent, and never says which crawlers the rules bind; every example uses the generic `User-agent: *`. "This binds Yahoo! JAPAN's own crawler" is not on this page.
- **No case-sensitivity rule.** 大文字 / 小文字 occur 0 times; case is page 1's subject (002849.php = S372), not this page's.
- **No directive other than the pattern symbols.** `Crawl-delay`, `Request-rate`, `Sitemap:`, `Host`, `Clean-param` all occur 0 times; the single `sitemap` hit is the site's own navigation link to its サイトマップ category page.
- **No placement, absence, encoding, size, or status rules.** No root-directory placement rule (page 1's subject), no 404 / 403 / 5xx behaviour, no エラー, no IP or host rules, no line-count or file-size limit, no encoding requirement.
- **No regular-expression grammar.** 正規表現 appears only in the head `<meta name="description">` (where `*` and `$` are called 正規表現記号); inside the body it occurs 0 times, and the page describes no character classes, alternatives, quantifiers or escapes (文字クラス / 選択肢 / エスケープ / 数量詞 = 0 hits; no `[]` or `|` tokens in the body text). "robots.txt supports full regular expressions" overreads a meta tag.
- **No statement that `?` is a wildcard.** The page only gives `?sessionid` as a literal string to be contained in the URL (Q13-Q14); "the `?` matches any single character" is unstated and would contradict the example.
- **No statement about how `*` interacts with `/` as a path separator, nor about URL encoding, query-string boundaries, redirects, or case.** The page's own guarantee is only "any part of the URL string" (Q7).
- **No statement that `$` anchors the *path* specifically.** The page says the end of the URL / the end of the string (Q4, Q17-Q18, Q27); "the end of the path" is a narrowing gloss. Likewise no statement that a mid-pattern `$` makes the rule invalid — the page says the crawler judges it to be the end and ignores what follows (Q28-Q29).
- **No update-lag, re-crawl, or index-refresh figure, and no claim of currency.** The page carries only the printed date line (Q1): 更新日 2010-11-24, roughly fifteen and a half years before the round date 2026-10-25, with no "as of" or "still valid" assertion. Presenting these as Yahoo! JAPAN's current rules overreads.
- **Not the whole ruleset.** The title ends in 2, and the page's own category list points to the companion page サイト単位、ディレクトリ単位での巡回の拒否設定 1 (002849.php = S372) plus the rel-attribute (002851.php) and in-page/server-side (002852.php) pages. Treating this page as the complete Yahoo! JAPAN crawl-refusal ruleset is an overread.
- **The `$`-less matching rule is printed in two clauses that do not perfectly agree** (prefix per Q25, "every URL containing the written string" per Q26). Asserting either one *as the page's single rule*, or asserting a reconciliation the page does not make, is an overread of the text.

VERDICT: Independent re-fetch of S373 (HTTP 200, 9402 bytes, sha256 3173d961…03885) is byte-identical to the retained body and to receipts.json — no drift; 29 operative quotes located from my own fetch, each a raw substring of the retained body and <= 25 units under both the lane's canonical counter and a stricter punctuation-charging count, with the printed revision date 2010年11月24日.
