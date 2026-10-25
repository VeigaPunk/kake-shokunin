# Round 53 — Gate lines for the five registered rows (draft for `corpus/lessons/round-53.md` `## Gate`)

Routed defect 4 of `corpus/lessons/round-52-verifier-spotcheck.md`: the round-52 entries
`yahoo-japan-rel-nofollow-semantics.md` (lines 26–27), `baidu-friendly-crawl-guidance.md`
(lines 40, 50) and `baidu-mobile-matching-error-causes.md` (line 35) cited `S367`, `S372`,
`S373`, `S390`, `S409`, which were absent from `corpus/SOURCES.md` at `3994101`. They are this
lane's own staged rows (`~/Projects/shokuknow/merge/kake/SOURCES.append.md` lines 87, 92, 93,
110, 129, sha256 `5f0cd4c4…f0cc`; ids per `~/Projects/shokuknow/lanes/kake/ID-REMAP.md`, sha256
`f7ec0d0d…60a8`, uncommitted at read time). The same numbers in `kotodama-shokunin` name
unrelated rows; the overlap is numbering, not provenance. Each URL was opened once this round,
the body retained under `.ufo/waves/round-53/sources/`, and receipts pinned in
`.ufo/waves/round-53/sources/receipts.json`. The rows are registered under the package ids, so
all five citations resolve with no entry line changed.

- S367 — https://info-search.yahoo.co.jp/archives/002852.php — accessed 2026-10-25 — § メタタグを使用する方法 (更新日 2010年11月24日) — quote: "このウェブページ内にあるリンク先ウェブページの巡回は拒否するが" (31 units; raw substring of the retained body, sha256 0188de9dae01e9088231098a9c6af3c8f5dc62a5982419a5f82fd98e86772a19, 8051 bytes, HTTP 200)
- S372 — https://info-search.yahoo.co.jp/archives/002849.php — accessed 2026-10-25 — page body above § 大文字と小文字の区別 (更新日 2010年11月24日) — quote: "ファイルは、サイトのルートディレクトリに設置してください" (27 units; raw substring, sha256 ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111, 10168 bytes, HTTP 200)
- S373 — https://info-search.yahoo.co.jp/archives/002850.php — accessed 2026-10-25 — §「$」記号 → 注意 (更新日 2010年11月24日) — quote: "「$」記号がない場合、クローラーはプリフィクス（接頭辞）として扱い、" (27 units; raw substring, sha256 3173d9613128e1aaa7cb55919fa52438602095bd7bc54d4437760ee8b1c03885, 9402 bytes, HTTP 200)
- S390 — https://ziyuan.baidu.com/wiki/990 — accessed 2026-10-25 — announcement body above 最新UA如下 (发布日期 2017-03-24) — quote: "百度搜索需要访问网站的CSS、Javascript和图片信息" (16 units; raw substring, sha256 a8f9ae70849aa36255b80df6275722886c2bd9bc05316cb4fb7fd7d3f1ab1506, 22141 bytes, HTTP 200)
- S409 — https://ziyuan.baidu.com/wiki/1021 — accessed 2026-10-25 — article body, beta-and-rollout passage (发布日期 2017-06-07) — quote: "内测期间分析了多个抓取量异常的" (15 units; raw substring, sha256 acfb5d2589c09dce117b3cb6887535d95f2b8008ea89f494c2251e3a7c7f208a, 56621 bytes, HTTP 200)

Units per `.ufo/waves/round-52/c52_quote_truth.py` `units()` (one per CJK character, one per
non-CJK whitespace token; bound 6–40).

Staged-row defects found on re-opening and not carried into the registered rows:

- S367: the staged claim's last clause ("the same refusal can be applied to an individual link
  URL") reads the page's permalink widget `個別リンクURL` (a `<strong>` label over a read-only
  input holding the page's own URL) as a per-link refusal form. Dropped. The staged scope's "per-link
  form" is the `rel=nofollow` attribute, already held as S374.
- S390: the staged anchor says the page prints no revision stamp and names a heading
  `公告正文`; the page prints `发布日期：2017-03-24`, and `公告正文` occurs 0 times in the body
  (`grep -o -F '公告正文' S390.html | wc -l` → 0).
- S372: the staged anchor `§ 大文字と小文字の区別` covers only the case-sensitivity claim; the
  root, absence and re-read claims sit above that heading. Anchor widened.

Negative check the round-52 entries rely on (baidu-mobile lines 43–45, baidu-friendly line 49):
neither Baidu body says the agent executes script — `执行` occurs 0 times in `S390.html` and
`S409.html` (raw count).

Id collision note: after registration, `S367`, `S372`, `S373`, `S390`, `S409` appear in both
the registry and `.ufo/waves/round-52/assimilation/staged-ids`, by design (same row, same
URL). A later assimilation of the staged entries that also cite them
(`yahoo-japan-link-target-crawl-restriction.md`, `yahoo-japan-robots-txt-refusal-rules.md`,
`yahoo-japan-robots-pattern-syntax.md`, `baidu-render-crawl-ua.md`,
`baidu-render-and-crawl-agents.md`) must append to these rows' `used-by`, not add rows.
