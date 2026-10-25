# ExecQuoteRecountS419

Seat: independent quote audit, W2 falsify. Entry under audit:
`corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (62 lines, 7346 bytes) against retained body
`.ufo/waves/round-56/sources/S419.html` (sha256 `6172d5d108d0c31d25244659516fc7fc81472c924ef35a51afc964cdd3a4a5c8`,
7428 bytes, HTTP 200 in `sources/receipts.json` — recomputed with `hashlib` and re-read from the receipt, both agree).
Also audited: the S419 Gate quote of `corpus/lessons/round-56.md:17`. Comparison bodies: `S367.html`, `S420.html`,
`S387.html`, `S388.html`, `S389.html` (all read raw, `newline=""`). Article block = first `<h2` (offset 2465) to
`個別リンクURL` (offset 2943), 478 bytes. Lane read only; nothing written outside this report; no git/jj mutation;
no selftest or counter was run, so no clone was needed. One network fetch was made (the entry's own recheck arm).

## SCRIPT:

Own Python, run as `python3 -B $D/qr4.py` with `D=$(mktemp -d)` (sha256 of the script
`d4d750719d4c5b692ae27ee2dab5cdd36a3ebc8a3a01895ff3189777055f6d44`; kept outside the lane; nothing imported from
`c56_quote_truth.py` or `span_tools.py`). Unit rule re-derived from the stated sentence, in two readings:
`uN` = the round tool's class (CJK `\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U0002xxxx`;
U+3000–303F punctuation costs 0), `uW` = the broad reading (U+3000–303F and U+FF00–FFEF also count). Both use
`units = len(CJK.findall(t)) + len([w for w in t.split() if not CJK.search(w)])`.

```python
NARROW=re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
WIDE  =re.compile(r"[\u3000-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\ufe30-\ufe4f\uff00-\uffef\U00020000-\U0002ffff]")
u=lambda t,rx: len(rx.findall(t))+len([w for w in t.split() if not rx.search(w)])
Q=re.compile(r'"([^"\n]+)"')            # ASCII double quotes, per line, never crossing a newline
b=read(S419); W=(b.find("<h2"), b.find("個別リンクURL"))
def blk(s):                             # True when some occurrence STARTS inside the article block
    i=b.find(s)
    while i>=0:
        if W[0]<=i<W[1]: return True
        i=b.find(s,i+1)
    return False
for ln,line in enumerate(entry.split("\n"),1):
    for m in Q.finditer(line): rows.append((ln,m.group(1)))
gate=[l for l in lesson.split("\n") if l.startswith("- S419 —")][0]   # exactly one such line
rows.append(("gate", Q.search(gate).group(1)))
# each row: uN, uW, len(span), span in b, blk(span), b.count(span), {S367,S420,S387,S388,S389 counts}
```

Cross-check, not import: `python3 -B .ufo/waves/round-56/span_tools.py check S419 <span>` (the round's documented
helper, CLI only) was run on four spans — `「HTTP 200 OK」のステータスを返すように` 14, `削除したURLのウェブページに
アクセスしたときに` 21, `サーバーが「HTTP 404 Not Found」のステータスを返すように` 19, `エラーページのHTMLの
&lt;head&gt;に、` 9 — and my `uN` agreed on all four, as did substring/block/count/uniqueness.

## SPAN TABLE:

`#` rows 1–15 are the entry's ASCII-double-quoted spans (2+ units); row 16 is the Gate quote. Counts are
`str.count` over the whole raw file (sidebar/nav included). `art` = in article block.

| # | src:line | span | uN | uW | chars | substr | art | S419 | S367 | S420 | S387 | S388 | S389 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | entry:12 | `削除したURLのウェブページにアクセスしたときに` | 21 | 21 | 24 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | entry:13 | `「HTTP 200 OK」のステータスを返すように` | 14 | 15 | 25 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | entry:14 | `サーバーが設定されている場合、` | 14 | 15 | 15 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 4 | entry:16 | `HTTP 200 OK` (rendering) | 3 | 3 | 11 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 5 | entry:18 | `クローラーは削除されたウェブページと認識できず、` | 23 | 24 | 24 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 6 | entry:19 | `そのウェブページを巡回し続ける可能性があります` | 23 | 23 | 23 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 7 | entry:25 | `削除されたウェブページが巡回され続けるときには、` | 23 | 24 | 24 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 8 | entry:26 | `サーバーが「HTTP 404 Not Found」のステータスを返すように` | 19 | 21 | 37 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 9 | entry:27 | `設定されているかを確認してください` | 17 | 17 | 17 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 10 | entry:29 | `HTTP 404 Not Found` (rendering) | 4 | 4 | 18 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 11 | entry:33 | `また、このような設定ができない場合には、` | 18 | 20 | 20 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 12 | entry:34 | `エラーページのHTMLの&lt;head&gt;に、` | 9 | 10 | 26 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 13 | entry:35 | `メタタグを使ったインデックスへの登録拒否` | 20 | 20 | 20 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 14 | entry:36 | `の設定を行ってください` | 11 | 11 | 11 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 15 | entry:38 | `robots` (from `name="robots"`) | 1 | 1 | 6 | yes | no | 5 | 7 | 5 | 5 | 5 | 5 |
| 16 | gate:17 | `クローラーは削除されたウェブページと認識できず、` (= #5) | 23 | 24 | 24 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |

Row 15 is below the assignment's 2+ unit rule and below the counter's skip (`units < 2 and len < 12`,
`c56_quote_truth.py:414`); all five of its S419 occurrences sit outside the article block (head `meta`, `rel`
tokens), and the entry tags the string `[INFERENCE]` as a lane candidate value, not the page's word.

Findings on this table (each names what it attacks):

- **F1 — no defect in the quoted spans.** Against `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md:12-36,60`
  and `corpus/lessons/round-56.md:17`: all 14 entry spans of 2+ units and the Gate quote are raw substrings of
  `S419.html`, every occurrence starts inside the article block, each occurs exactly once in its own body, and none
  exceeds 25 units or 40 characters under either unit reading (max uN 23, uW 24, chars 37). The Gate quote is
  page-unique across all five comparison bodies, as the counter's C5 requires.
- **F2 — undercount in the entry's self-description** (attacks `yahoo-japan-deleted-url-recrawl.md:60`). The line
  says "Four spans also occur on the sibling S420 body" and names #8, #11, #12, #14. Under the counter's own span
  rule (any ASCII-double-quoted span of 2+ units anywhere in the entry, `c56_quote_truth.py:412-421`), **six** spans
  occur in `S420.html`: the four named plus #4 `HTTP 200 OK` and #10 `HTTP 404 Not Found` (count 1 each). Under the
  entry's own narrower reading (a "quotation" = a `> "…"` block line), the four named are exactly right. No
  predicate impact: C5 requires ≥3 page-unique spans of ≥6 units and 8 exist; the shared spans need only be raw,
  in-block and ≤25 units. Suggested wording: "four of the Japanese spans, and the two status strings".
- **F3 — unit-rule reading, not a defect** (attacks the Gate row's "(23 units)" and the entry's "at most 25
  units"). 23 is the round tool's count, where U+3001 `、` costs 0; the broad CJK-character reading gives 24 for the
  same span. The ceiling holds under both, but the contract's "punctuation and markup entities cost 0 or 1 unit"
  admits both numbers, so the round record should name which reading a stated tally uses.
- **F4 — `robots` is not a page quote.** #15 occurs 5× in `S419.html` and 7× in `S367.html`; the entry's
  `[INFERENCE]` tag and the words "not the page's words" (entry:38) keep it out of the quotation class, so nothing
  false is claimed — recorded because a reader scanning ASCII quotes will hit it.

## UNQUOTED ATTRIBUTIONS:

Every maximal Japanese run in the entry (62 lines, header, prose and renderings included; the ASCII-quoted spans
removed first) was tested against the raw body: 15 distinct phrases, and **none is missing from the body**. List of
phrases the entry attributes to the page that do NOT occur in the body: **empty**.

Inventory (line: phrase — body count, in-block):
`1: 削除したウェブページが巡回され続ける` 3 yes (title, h2, sidebar `<strong>`) · `1: 更新日` 1 yes ·
`3: クローラーは削除されたウェブページと認識できず` 1 yes (the `recheck:` grep string) ·
`21,60: 可能性があります` 1 yes · `29,60: 確認してください` 1 yes · `38,60: このような設定ができない場合には` 1 yes ·
`38,60: エラーページの` 1 yes · `38: メタタグを使った` 1 yes · `53: サーバー` 3 yes ·
`55: 存在しないウェブページが巡回される` 1 **no** (sidebar category link only) ·
`60: 」のステータスを返すように` 2 yes · `60: の設定を行ってください` 1 yes · `60: エラーページ` 1 yes ·
`60: サーバーが「` 1 yes · `60: 設定されている場合` 1 yes.

- **F5 — the one out-of-block phrase is attributed elsewhere.** `存在しないウェブページが巡回される` (entry:55) is
  named as the sibling page (002857, row S420), not as this page's text; its single S419 occurrence is the sidebar
  link to that page. Not a misattribution.
- **F6 — one qualifier is an entity rendering, not a raw substring** (attacks `yahoo-japan-deleted-url-recrawl.md:38`).
  The line presents `エラーページのHTMLの head` as the middle of "Three qualifiers"; as written that string has
  S419 count 0 (the body writes `エラーページのHTMLの&lt;head&gt;に、`, count 1). It is unquoted prose, so C5 does not
  test it, and entry:60 declares that quotations keep entities as written — but the three qualifiers are presented
  as page wording, and one of them silently drops `に、` and renders the entity. Recommend either
  `エラーページのHTMLの&lt;head&gt;に` or an explicit "(rendering)" marker.

## SUMMARY:

- Spans checked: **16 rows / 15 distinct** — 14 entry spans of 2+ units (plus the 1-unit `robots` recorded and
  excluded) and the Gate quote `corpus/lessons/round-56.md:17`, which duplicates entry #5.
- Over ceiling: **0** (max uN 23 ≤ 25, max uW 24 ≤ 25, max chars 37 ≤ 40).
- Non-substring: **0**. In article block: 15/15 of the 2+ unit spans. Occurrences ≠ 1 in own body: **0**.
- Page-unique with ≥6 units (count 1 in S419, absent from S367/S420/S387/S388/S389): **8 distinct** — #1, #2, #3,
  #5, #6, #7, #9, #13 (the counter needs 3).
- Shared with `S420.html`: **6** (#4, #8, #10, #11, #12, #14); the entry names 4 (F2). Hits in `S367`, `S387`,
  `S388`, `S389`: **0** for every span.
- Ancillary claims re-checked: sha256/bytes/HTTP 200 agree with `receipts.json`; the `recheck:` **curl arm was run**
  (2026-10-25): HTTP 200, 7428 bytes, sha256 `6172d5d1…` — byte-identical to the retained body — and
  `grep -F -c 'クローラーは削除されたウェブページと認識できず、'` → 1 on both the live and the retained copy, exactly
  as entry:3 states. The entry's grep claim (entry:9) reproduces: `grep -n -i -E '200|soft'` over
  `crawl-error-status-table.md` and `crawl-budget-consequences.md` prints one line, `crawl-error-status-table.md:14`,
  the soft-404 disclaimer. "The remedy text names no tag name, no content value and no attribute" (entry:38) holds:
  the 478-byte block contains no `<meta`, `noindex`, `content=` or `name=`, and `メタタグ` once. The S372
  cross-reference (entry:40) is consistent with `yahoo-japan-robots-txt-refusal-rules.md:99-106`, which quotes
  `メタタグで、` / `インデックスへの登録拒否を設定してください` and states "names no tag value". No curly double
  quote (U+201C/U+201D) occurs anywhere in the entry or in the S419 Gate line: the only non-ASCII, non-Japanese
  characters in the entry are `§`, U+2014 and U+2026.
- Defects in the audited entry: **1 wording** (F2, four-vs-six shared spans) and **1 rendering** (F6, the entity
  qualifier). No quote is fabricated, misattributed, over-ceiling or out of block.

VERDICT: 15/15 spans of 2+ units are raw in-block substrings occurring once in S419, ≤23/24 units and ≤37 chars; the only entry defects are the "four spans shared with S420" undercount (six share) and one entity-rendered qualifier at entry:38.
