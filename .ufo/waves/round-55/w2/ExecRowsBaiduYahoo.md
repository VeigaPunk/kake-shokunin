# ExecRowsBaiduYahoo

ATTACKS: the three coverage-map rows added at revision `a7a548e102b71bd16b0a6ddafa469393a2c98b69` in
`corpus/README.md` §Coverage map — line 48 (`knowledge/baidu-friendly-crawl-guidance.md`, S329), line 49
(`knowledge/baidu-mobile-matching-error-causes.md`, S312), line 66
(`knowledge/yahoo-japan-rel-nofollow-semantics.md`, S374) — claim C1.

All lane bytes were read with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show a7a548e…:<path>`;
no index/jj operation, no scratch repo, nothing written inside the lane except this report. No tool was
installed or upgraded, so there is no tool/version/channel record to make. No labrat probe was needed.

## Method (commands run)

- Row extraction: `git show a7a548e…:corpus/README.md | sed -n '48p;49p;66p'`; a `python3` pass over the
  same bytes restricted to lines 15–70 (`## Coverage map` starts at 15, `### Frontier ground map` at 71)
  confirmed one 3-cell coverage row per file and that each Entry cell is exactly `` `knowledge/<file>` (S###) ``.
  The same three files also appear once each in the *Frontier ground map* sub-table (5-cell rows 91/92/93,
  `Entries`+`Rows` columns, no coverage cell) — different section, not a duplicate coverage row.
- Genuinely added: `git diff fcaf4b85… a7a548e… -- corpus/README.md` → `84 insertions(+), 0 deletions`;
  the three rows appear as `+` lines (diff offsets 8, 9, 26).
- No STALE window in-lane: `git diff --quiet fcaf4b85… a7a548e… -- <the three knowledge files>` → exit 0,
  printed `UNCHANGED base..rev`.
- Statement support read from each file at the revision (`git show …:corpus/knowledge/<file>`), with
  retained bodies re-opened read-only at `.ufo/waves/round-52/sources/{S329,S312,S374}.html`.
- C1 counter, run read-only: `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision a7a548e…`
  → `index_mismatches=0 knowledge_files=49 met=True`, `unindexed=0 multi=0 thin=0 duplicate=0
  head_changed=0 deleted=0 dangling=0 coverage_rows=51`, `EXIT=0`.

## PER-ROW:

| file | statement (atomic) | class | evidence line (quoted ≤25 words) | command output |
|---|---|---|---|---|
| baidu-friendly-crawl-guidance.md | "a block on that agent binds the desktop and mobile crawlers" | SUPPORTED | :11 "如果封禁的agent是Baiduspider，会对PC和移动同时生效"; :14-15 "neither the PC nor the mobile Baiduspider will fetch the blocked object" | file :6 H1 "A Baiduspider robots block binds the desktop and mobile crawlers at once"; body grep -c of the :11 quote = 1 |
| baidu-friendly-crawl-guidance.md | "wildcard symbols `*` and `$`" | SUPPORTED | :15 "the crawler honours the two wildcard symbols"; :19-20 "names them as `*`, matching 0 or more arbitrary characters, and `$`" | body lines 344-356: `Baiduspider 支持使用通配符 "*" 和 "$" 来模糊匹配 url`; `"*" 匹配 0 或多个任意字符`, `"$" 匹配行结束符` |
| baidu-friendly-crawl-guidance.md | "the spider trap as a parameter-generated URL space with a robots remedy" | SUPPORTED | :22-23 "defines it as a URL space a site generates from parameters"; :29 "The page's remedy is a `robots.txt` rule over the generated space" | body :397-403 "蜘蛛黑洞特指网站通过极低的成本制造出大量参数过多、内容类同但 url 不同的动态 URL"; body :417-422 "通过 robots 规则拒绝提供给搜索引擎 … Disallow: /*?*" |
| baidu-mobile-matching-error-causes.md | "Baidu's mobile-matching correspondence-error list" | SUPPORTED | :8 "lists the causes of a failed PC↔mobile correspondence"; :61 correction "This list describes common correspondence errors" | file :1 header `source: S312 — …/courseinfo?id=267&page=15`; body :170 "以下是常见的对应不准确错误" |
| baidu-mobile-matching-error-causes.md | "an ajax-loaded mobile body and a Baiduspider robots block, both quoted raw" | SUPPORTED | :11 "手机页使用了ajax等异步加载的方法加载内容主体"; :16 "放开对Baiduspider的robots封禁，以便Baiduspider获取您PC站与手机站之间的对应关系。" | `grep -c -F` each quote in S312.html → 1 and 1 (2 blockquote lines in the file) |
| baidu-mobile-matching-error-causes.md | "the five-item list also names an unusable mobile page, a rule-pattern format error and a wrong PC-mobile mapping" | SUPPORTED | :19-22 "The list names five causes in all: the mobile page is unusable … a format error in the submitted rule pattern, and a wrong correspondence" | scoped re-derivation: items after body :170 = 5 (`手机页不可用，比如死链` / `robots封禁` / `ajax` / `格式错误。正则格式错误，文件格式错误等` / `对应关系错误`); row names 3 of 5, a subset — no overreach |
| baidu-mobile-matching-error-causes.md | "no matching algorithm or threshold stated" | SUPPORTED | :46-47 "It does not state the matching algorithm, a pass threshold, or how long a resubmission takes to be reflected" | body keyword scan `阈值|算法|通过率|匹配度` → 0 hits each |
| yahoo-japan-rel-nofollow-semantics.md | "One operator's rel=nofollow reading" | SUPPORTED | :8 "Yahoo! JAPAN's info centre states what its engine reads into `rel=nofollow`"; :38 "it is one operator's page" | header :1 host `info-search.yahoo.co.jp`; file :38 names Google/Bing/Baidu only inside "It says nothing about" |
| yahoo-japan-rel-nofollow-semantics.md | "the phrase is a crawl qualifier on the link target's page" | SUPPORTED | :54-57 "The phrase includes a crawl qualifier: the site owner is taken to **not recommend the crawling of the link target's web page**" | correction block :52-62 printed; source title :20 `リンク先のウェブページの巡回制限` |
| yahoo-japan-rel-nofollow-semantics.md | "the URL may still be used to discover new pages" | SUPPORTED | :29 "The page says the tagged URL is used to discover new pages"; :60-61 "the source continues that the URL may be used to discover new pages" | body S374 :7 "…のURLは、新しいウェブページを見つけるために利用されますが…" |
| yahoo-japan-rel-nofollow-semantics.md | "the attribute is not weighed in result ordering" | SUPPORTED | :19 "(rendered: the attribute is not weighed when the result order is decided)" | body S374 :7 "検索結果の表示順序を決める要素としては考慮されません"; grep -c of the quoted span = 1. Residual: the Japanese sentence's grammatical subject is the nofollow'd link's URL, not the attribute token — the file's gloss (and so the row) shifts the subject; row is faithful to the file, so not OVERREACH |
| yahoo-japan-rel-nofollow-semantics.md | "other operators and attribute values out of scope" | SUPPORTED | :38 "It says nothing about Google, Bing or Baidu"; :40-41 "does not establish how other link-attribute values (`sponsored`, `ugc`) are read" | file lines 36-44 printed |

Totals: 12 atomic statements (plus the id-equality check below), 12 SUPPORTED, 0 OVERREACH, 0 UNSUPPORTED,
0 STALE.

Id equality (row `(S###)` = file `source:` header = SOURCES.md row): SUPPORTED for all three.
`python3` header-id vs Entry-cell-id comparison → `S329 == ['S329']`, `S312 == ['S312']`, `S374 == ['S374']`,
`equal: True` each. Registry: `git show a7a548e…:corpus/SOURCES.md | grep -cE '^\|\s*S(329|312|374)\s*\|'`
→ 1 each (rows 155 S329, 156 S312, 154 S374).

## COUNTS RE-DERIVED:

| number in row | where | re-derivation command | observed |
|---|---|---|---|
| wildcard symbols = 2 (`*`, `$`) | row 48 | `python3` over S329.html body: lines `"*"` / `"$"` in the wildcard block | 2 distinct symbols (body 345, 347); quote "支持使用通配符" ×1 |
| five-item list | row 49 | `python3` scoped count of `^[1-9]、` after the body line containing `以下是常见的对应不准确错误` (body :170) | 5 items (body :171-175) — note the page has other numbered lists (18 `^[1-9]、` lines page-wide), so the scope was pinned to the intro sentence |
| "both quoted raw" = 2 | row 49 | `grep -c -F` each file quote in S312.html | 1 + 1 → both spans present exactly once |
| one operator | row 66 | `grep -nE 'Google|Bing|Baidu|Yahoo'` on the file + header host | Yahoo! JAPAN only affirmatively (:8, :38); header host `info-search.yahoo.co.jp` |
| coverage-cell tokens (>=5 rule, no `\|`) | rows 48/49/66 | `python3` `len(cell.split())`, 3-cell split | 31 / 40 / 42 tokens; exactly 3 cells each |
| ids in rows 48/49/66 | all three | `grep -cE '^\|\s*S(329|312|374)\s*\|'` on `corpus/SOURCES.md` | 1 / 1 / 1 (lines 155 / 156 / 154) |
| C1 index terms | whole map | `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision a7a548e…` | `index_mismatches=0 knowledge_files=49 met=True coverage_rows=51`, all sub-terms 0, exit 0 |

## PROPOSED REPLACEMENTS:

none needed — every statement in all three Coverage cells is supported by the named file at the measured
revision, every count re-derives to the observed value, and every `(S###)` id matches the file's own
`source:` header and exists as exactly one registry row.

## UNRUN:

- Live re-fetch of `ziyuan.baidu.com` / `info-search.yahoo.co.jp` — `unrun`; this attack is row-vs-file,
  not file-vs-vendor. The three entries are byte-identical base..rev, so no in-lane drift window exists.
- `c55_readme_index.py` selftest/junk-fixture suite — `unrun` (parent gate); only the counter run itself
  was executed.
- Frontier ground map rows 91-93 for the same files — not adjudicated (different table, outside the
  assigned §Coverage map rows).
- No labrat probe dispatched: not needed for a row-vs-file diff.

VERDICT: all three C1 coverage rows (README 48, 49, 66) are fully SUPPORTED at a7a548e — 12/12 atomic statements plus all id and count checks re-derived and matching; no replacement coverage cell required.
