# ExecQuoteRecountS367

Independent quote audit of `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` (entry) against the retained body
`.ufo/waves/round-56/sources/S367.html`, plus the S367 Gate quote in `corpus/lessons/round-56.md:16`. Own python only (no
import of `c56_quote_truth.py`, `c56_selftally.py` or `span_tools.py`; those files were read as prose, not executed as
helpers). Scripts were written under `/tmp/s367audit/`, never in the lane; no lane file other than this report was touched.

## SCRIPT:

Two scripts, both run with `python3 -B` against the lane read-only. Unit and block definitions re-implemented from the
contract text, not imported:

```python
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
def units(t): return len(CJK.findall(t)) + len([w for w in t.split() if not CJK.search(w)])
# article block = [T.find("<h2"), T.find("個別リンクURL")) ; assert h2 >= 0 and hi > h2   (body: h2 at line 100, 個別リンクURL at 125)
# extraction: per line of the entry, re.finditer(r'"([^"]*)"', line); keep units(span) >= 2
# per span: units, len(span) (raw characters), span in T, block membership of every occurrence, T.count(span),
#           count in S419/S420/S387/S388/S389, count in the lesson line
# unquoted pass: strip '"..."' groups to '"Q"', then find runs of the CJK class; test each run in T and block membership
```

Ran outputs are reproduced verbatim in the two tables below; nothing was re-run after the first pass. Body sha256 recomputed
with `sha256sum`: `0188de9dae01e9088231098a9c6af3c8f5dc62a5982419a5f82fd98e86772a19`, 8051 bytes — equal to entry line 3,
lesson line 16 and `sources/receipts.json` (httpStatus 200, fetchedAt 2026-10-25T22:02:40+00:00).

## SPAN TABLE:

`src` = entry line, or `lesson:16` for the Gate quote. `own#` = occurrence count in S367.html; `others` = counts in
S419 / S420 / S387 / S388 / S389. Every span was also checked for occurrence outside the article block: none (own# is 1 for
all rows, and that single occurrence is inside the block).

| # | src | units | chars | raw sub | in block | own# | others | span |
|---|-----|-------|-------|---------|----------|------|--------|------|
| 1 | 16 | 16 | 17 | yes | yes | 1 | 0/0/0/0/0 | リンク先ウェブページの巡回制限は、 |
| 2 | 17 | 13 | 18 | yes | yes | 1 | 0/0/0/0/0 | HTMLのメタタグで指定する方法と、 |
| 3 | 18 | 19 | 19 | yes | yes | 1 | 0/0/0/0/0 | サーバーの設定で指定する方法があります |
| 4 | 25 | 10 | 34 | yes | yes | 1 | 0/0/0/0/0 | rel=&quot;nofollow&quot;属性を使った指定方法 |
| 5 | 35 | 11 | 11 | yes | yes | 1 | 0/0/0/0/0 | メタタグを使用する方法 |
| 6 | 36 | 14 | 30 | yes | yes | 1 | 0/0/0/0/0 | HTMLの&lt;head&gt;内に次のような記述をします |
| 7 | 48 | 23 | 23 | yes | yes | 1 | 0/0/0/0/0 | このウェブページ内にあるリンク先ウェブページの |
| 8 | 49 | 8 | 9 | yes | yes | 1 | 0/0/0/0/0 | 巡回は拒否するが、 |
| 9 | 50 | 11 | 11 | yes | yes | 1 | 0/0/0/0/0 | このウェブページ自身は |
| 10 | 51 | 15 | 15 | yes | yes | 1 | 0/0/0/0/0 | インデックスへの登録を許可する |
| 11 | 63 | 17 | 19 | yes | yes | 1 | 0/0/0/0/0 | 「リンク先ウェブページの巡回を拒否し、 |
| 12 | 64 | 24 | 25 | yes | yes | 1 | 0/0/0/0/0 | ウェブページ自身のインデックスへの登録も拒否する」 |
| 13 | 65 | 7 | 8 | yes | yes | 1 | 0/0/0/0/0 | という場合には、 |
| 14 | 66 | 10 | 10 | yes | yes | 1 | 0/0/0/0/0 | 次のように記述します |
| 15 | 84 | 11 | 11 | yes | yes | 1 | 0/0/0/0/0 | サーバーで設定する方法 |
| 16 | 85 | 22 | 23 | yes | yes | 1 | 0/0/0/0/0 | ウェブページをホスティングしているサーバーで、 |
| 17 | 86 | 18 | 18 | yes | yes | 1 | 0/0/0/0/0 | 次のようなディレクティブ設定をします |
| 18 | lesson:16 | 15 | 15 | yes | yes | 1 | 0/0/0/0/0 | インデックスへの登録を許可する |

Floor-excluded by the 2-unit rule (recorded, not tabled): entry line 42 `robots`, `index,nofollow`; line 73 `robots`,
`noindex,nofollow` — 1 unit each. Entry line 1 (source header), line 2 and line 3 contain no ASCII double quote; line 3's
recheck string is single-quoted (`'サーバーの設定で指定する方法があります'`). Quote counts per line are even (2, or 4 on lines
42 and 73), so no span was mis-parsed across a quote boundary.

Fragment contiguity (concatenation of each blockquote group against the raw body): lines 48-51 -> exact body substring
(count 1); lines 63-66 -> exact (count 1); lines 85-86 -> exact (count 1); **lines 16-18 -> not a body substring (count 0)**
— see U3.

## UNQUOTED ATTRIBUTIONS:

Every CJK run in the entry (outside the ASCII-double-quoted spans, header lines included) tested against the body. **Zero
unquoted Japanese phrases are absent from the body**; the run `個別リンク` (entry line 104, part of `個別リンクURL`) is the
only one whose single occurrence is outside the article block, which the entry itself states.

| entry line | phrase | body location |
|---|---|---|
| 1 | リンク先のウェブページの巡回制限 | 100 (h2), also title and category `<li>` (4 occurrences) |
| 1 | ウェブページ内やサーバーでの設定 | 100, title, `<li>` (3 occurrences) |
| 1 | メタタグを使用する方法 / サーバーで設定する方法 | 105 / 114 (the only two article `<h3>`) |
| 1 | 更新日 + 2010年11月24日 | 101 (`<p class="update">更新日 2010年11月24日</p>`, count 1) |
| 3 (recheck) | サーバーの設定で指定する方法があります | 104 |
| 21 | ほかに | 104 — **as `のほかに`**, see U1 |
| 22, 121 | 方法があります | 104 |
| 54, 121 | このウェブページ内にある | 110 |
| 55 | 上記の例は / という意味を持ちます | 110 |
| 69, 121 | も | 110 (`…登録も拒否する`) |
| 104 | 個別リンクURL | 125 — outside the article block, URL-field label, count 1 |
| 121 | このウェブページ自身は | 110 |
| 122 | という場合には | 110 |

- **U1 (entry:21 vs body:104) — position claim false.** Entry line 21: "ほかに (besides) opens the sentence". Body line 104
  reads `リンク先ウェブページの巡回制限は、<a …>rel=&quot;nofollow&quot;属性を使った指定方法</a>のほかに、HTMLのメタタグで…`;
  `ほかに` is preceded by `の` and follows the link text mid-sentence (`のほかに` count 1, `ほかに、` count 1). The entry's
  conclusion — a further route precedes the two named methods — is still supported by that link, but the stated word
  position is contradicted by the body. The word itself is present, so no unquoted phrase is unattested.
- **U2 (entry:1 vs body:100) — locator normalization, not a quote.** The `§` locator writes
  `リンク先のウェブページの巡回制限 ― ウェブページ内やサーバーでの設定` with an ASCII space before U+2015; the h2 has U+3000
  there (`…巡回制限　― ウェブページ内や…`), so the locator string is not a raw substring. It is an unquoted header locator, so
  no quote rule is broken; flagged because round-56's C2 v1 rejected a truthful build on exactly this fullwidth/ASCII
  distinction (contract, "Counter versions", C2 v2 bullet).
- **U3 (entry:16-18 vs body:104) — fragment group is not one sentence.** The three raw spans are each true, but their
  concatenation is not a body substring: between fragment 1 and fragment 2 the body carries the nofollow link text and
  `のほかに、`. The entry quotes that link span separately (line 25) and discusses `ほかに` immediately after, so the omission
  is disclosed in prose, but the three blockquote lines read as a consecutive sentence.
- **U4 (entry:42,73) — ASCII renderings, entity-encoded in the body.** `<meta name="robots" content="index,nofollow">` and
  `<meta name="robots" content="noindex,nofollow">` are not raw substrings (body 111/112 print
  `&lt;meta name="robots" content=&quot;…&quot;&gt;`). The entry presents them as printed examples, not as quotes, and the
  tokens `index,nofollow` (2 occurrences — it is also a substring of `noindex,nofollow`), `noindex,nofollow` (1),
  `X-Robots-Tag: NOFOLLOW` (1) and `rel=&quot;nofollow&quot;` (1) all occur literally. Consistent with the contract's note
  that the meta-tag example lines are not quoted as spans.
- **U5 — entry claims about the page's shape, spot-checked against the body.** Two article `<h3>` only (105, 114), so "no
  sub-heading … of its own" for the attribute route holds; `&lt;meta` appears exactly twice, so "no third value" holds;
  `個別リンクURL` once outside the block, matching the entry's own bullet; the head `meta name="description"` (body:13) does
  contain `サーバーのHTTPヘッダーの設定`, matching entry's "the setting of the server's HTTP header".

## SUMMARY:

- Spans extracted and tabled: **18** (17 from the entry, header lines included; 1 Gate quote, `round-56.md:16`). Four
  further ASCII-double-quoted spans were floor-excluded at 1 unit.
- Over ceiling (25 units, or 40 raw characters): **0**. Max units 24 (`#12`), max characters 34 (`#4`).
- Non-substring of the retained body: **0**.
- Not inside the article block (first `<h2` .. `個別リンクURL`): **0**.
- Occurring more than once in S367.html: **0**; occurring in S419, S420, S387, S388 or S389: **0** (all 18 spans).
- Unique page-wide and >= 6 units: **18 of 18** (smallest is #13 at 7 units; the 8-unit #8 and 7-unit #13 are still
  page-unique).
- Gate-quote claim re-verified: `インデックスへの登録を許可する` = 15 units / 15 characters / substring / count 1, matching
  `round-56.md:16`; body sha256 and byte count match the entry, the lesson and `receipts.json`.
- Defects returned, none of them a quote-truth failure: U1 (position claim about `ほかに`, entry:21 vs body:104), U3
  (fragment group read as one sentence, entry:16-18 vs body:104), U2 (locator spacing normalization, entry:1 vs body:100),
  U4 (entity-encoded example renderings, informational).
- Unrun: no fetch of `archives/002852.php` was attempted (retained body used as ground, per lane rule); the round-53 31-unit
  original quote cited in the entry's "Quote classes" was not compared against a round-53 record — unrun, not asserted.

VERDICT: 18/18 spans quote-true, page-unique, in-block, under both ceilings; 0 non-substring and 0 unquoted Japanese phrases absent from the body, with one prose position claim (ほかに "opens the sentence") contradicted by body:104.
