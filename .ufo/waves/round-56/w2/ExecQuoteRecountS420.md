# ExecQuoteRecountS420

Seat: independent quote audit, W2 falsify. Entry under audit:
`corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` (95 lines, 7037 bytes) against retained body
`.ufo/waves/round-56/sources/S420.html` (sha256 `a860d4f33181302d7ab467f5a0b21f2008916bb6dc6def69e69df5b54c630209`,
7332 bytes, HTTP 200 in `receipts.json` — recomputed with `hashlib` and re-read from the receipt, both agree).
Also audited: the S420 Gate quote of `corpus/lessons/round-56.md:18`. Comparison bodies: `S367.html`, `S419.html`,
`S387.html`, `S388.html`, `S389.html` (all read raw, `newline=""`). Article block taken as
`first <h2` (offset 2456) to `個別リンクURL` (offset 2909), 453 bytes. Lane was read only; nothing was written
outside this report; no git/jj mutation; no network fetch was made.

## SCRIPT:

Own Python, run as `python3 -B /tmp/qrs420/audit.py` (script kept outside the lane, not imported from
`c56_quote_truth.py` or `span_tools.py`; the unit regex was re-derived from the stated rule, not imported):

```python
import re, json
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"; SRC=f"{LANE}/.ufo/waves/round-56/sources"
CJK=re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
units=lambda t: len(CJK.findall(t))+len([w for w in t.split() if not CJK.search(w)])
rd=lambda p: open(p,encoding="utf-8",newline="").read()
entry=rd(f"{LANE}/corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md")
lesson=rd(f"{LANE}/corpus/lessons/round-56.md")
b={s:rd(f"{SRC}/{s}.html") for s in ("S367","S419","S420","S387","S388","S389")}
rows=[]
for ln,line in enumerate(entry.split("\n"),1):
    for m in re.finditer(r'"([^"\n]+)"', line):          # ASCII double quotes only
        if units(m.group(1))>=2: rows.append(("entry",ln,m.group(1)))
for ln,line in enumerate(lesson.split("\n"),1):          # Gate quote = the S420 bullet
    if line.startswith("- S420 "): rows.append(("gate",ln,re.findall(r'"([^"\n]+)"',line)[0]))
t=b["S420"]; A=t.find("<h2"); Z=t.find("個別リンクURL")
def inart(s):
    i=t.find(s)
    while i>=0:
        if A<=i<Z: return True
        i=t.find(s,i+1)
    return False
for src,ln,s in rows:
    print(src,ln,units(s),len(s),s in t,inart(s) if s in t else False,t.count(s),
          {k:b[k].count(s) for k in ("S367","S419","S387","S388","S389")},repr(s))
# unquoted attributions: every maximal CJK/CJK-punct run in the entry, tested against the body
for ln,line in enumerate(entry.split("\n"),1):
    for m in re.finditer(r"[\u3000-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff01-\uff60\uffe0-\uffe6\u2015\u2014\u2026\u2025\u3001\u3002\u300c\u300d\u300e\u300f]+", line):
        s=m.group(0)
        if s not in t: print("MISS",ln,repr(s),t.count(s),b["S419"].count(s))
```

Quote extraction cross-check: the entry contains exactly 24 ASCII `"` characters = 12 spans, all captured;
the Gate line contributes the 13th span (identical to entry span #4).

## SPAN TABLE:

units = one per CJK character, one per non-CJK whitespace token (counter rule); chars = `len(span)`.
`substr` = raw substring of S420.html; `art` = some occurrence starts inside the article block.
Counts are `str.count` over the whole raw file (sidebar/nav included).

| # | src:line | span | units | chars | substr | art | S420 | S367 | S419 | S387 | S388 | S389 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | entry:14 | `存在しないウェブページを表示しようとしたときに、` | 23 | 24 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | entry:18 | `サーバーが「HTTP 200 OK」` | 7 | 18 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | entry:22 | `エラーページを表示する設定にしていると、` | 19 | 20 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 4 | entry:28 | `クローラーはエラーページとみなさず、` | 17 | 18 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 5 | entry:32 | `巡回を続けます` | 7 | 7 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 6 | entry:38 | `存在しないウェブページを表示しようとしたときには、` | 24 | 25 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 7 | entry:42 | `サーバーが「HTTP 404 Not Found」` | 8 | 25 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 8 | entry:46 | `のステータスを返すように設定を行ってください` | 22 | 22 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 9 | entry:54 | `このような設定ができない場合には、` | 16 | 17 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 10 | entry:58 | `エラーページのHTMLの&lt;head&gt;に、` | 9 | 26 | yes | yes | 1 | 0 | **1** | 0 | 0 | 0 |
| 11 | entry:62 | `メタタグを使ったインデックス拒否の設定` | 19 | 19 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |
| 12 | entry:66 | `を行ってください` | 8 | 8 | yes | yes | **2** | 0 | **1** | 0 | 0 | 0 |
| 13 | gate:18 | `クローラーはエラーページとみなさず、` (= #4) | 17 | 18 | yes | yes | 1 | 0 | 0 | 0 | 0 | 0 |

Span #12 occurs twice in its own body (offsets 2761 and 2842, both inside the article block); every other span
occurs once. All four spans the entry names in its "Quote classes" paragraph (lines 80–82) as shared with S419 —
#7, #9, #10, #12 — are confirmed at count 1 in `S419.html`, and each of those S419 occurrences is itself inside
S419's article block (offsets 2744/2810/2827/2876). The entry's claim that "the other eight are page-unique"
holds exactly: spans #1,2,3,4,5,6,8,11 have S420 count 1 and 0 in S367/S419/S387/S388/S389.
No span occurs in `S367.html`, `S387.html`, `S388.html` or `S389.html`.

## UNQUOTED ATTRIBUTIONS:

Every maximal Japanese run in the entry (95 lines, header and renderings included) was tested against the S420
body. Four runs do not occur in it; all four are accounted for by the entry itself:

- `可能性` — entry:34 (`the page has no 可能性, no interval and no frequency`). S420 count 0 (claim of absence,
  true); S419 count 1, matching the entry's S419 comparison at entry:74. Not attributed to S420.
- `インデックスへの登録拒否` — entry:74 (`S419's fallback phrase names インデックスへの登録拒否`). S420 count 0,
  S419 count 1. Explicitly attributed to S419, and true there; S420's own phrase `インデックス拒否` is present
  in the article block (count 1) as the entry says.
- `ユーザーエージェント` — entry:89 (`the only ユーザーエージェント in the retained body is a sidebar link title`).
  S420 count 1 at offset 4176, outside the article block (sidebar link `クローラー名（ユーザーエージェント名）の確認方法`).
  The entry states exactly this; true. `クローラー名` and `ユーザーエージェント名` likewise occur only outside the block.
- `—` (U+2014, entry:1,3,4,16,…) and `…` (entry:82) — punctuation, not Japanese phrases; absent from the body by
  construction, no attribution.

Other attributed phrases all occur in the body, e.g. `更新日 2010年11月24日` (1, inside the article block),
`存在しないウェブページが巡回される` (3: title, h2, sidebar `<strong>`; the h2 occurrence is the one the header names),
`個別リンクURL` (1, the widget label that closes the window), `ステータス` (2), `メタタグ` (1), `みなさず` (1),
`表示しようとした` (2). No attributed Japanese phrase fails to occur in the body.

One wording observation outside the requested span classes, reported because it is checkable against the same body:
entry:74 ends `Neither body names a crawler, an interval, or what the index does with the page` — literally false for
`クローラー`, which occurs 8 times in S420.html and 8 times in S419.html (e.g. the quoted span #4 itself). Read as
"names no crawler product/user-agent", it is true (no user-agent name inside either article block). Flagged as an
ambiguity in the sentence, not as a quote defect.

## SUMMARY:

- Spans extracted: **13 rows / 12 distinct** (12 ASCII-double-quoted spans in the entry + the Gate quote of
  `corpus/lessons/round-56.md:18`, which duplicates entry span #4).
- Over ceiling: **0** (max units 24 ≤ 25; max chars 26 ≤ 40). Under the unit rule the entity span #10 costs 9 units.
- Non-substring: **0**. In-article: **13/13**. Count-1-in-own-body: 12 rows; span #12 counts 2.
- Page-unique (S420 count 1, absent in S367/S419/S387/S388/S389) with ≥ 6 units: **9 rows / 8 distinct spans**
  (#1,2,3,4,5,6,8,11 plus the Gate duplicate of #4).
- Shared with S419: **4** (#7,#9,#10,#12), exactly the four the entry names; other eight unique. Zero hits in
  S367/S387/S388/S389 for all 13 spans.
- Ancillary claims checked: sha256/bytes/HTTP 200 agree with `receipts.json`; the documented recheck grep
  `grep -F -c 'クローラーはエラーページとみなさず、' S420.html` → 1 (retained-body arm verified; the `curl` arm was
  **not run**, no network fetch in this seat). Article block is 453 bytes, `<h2` 2456 → `個別リンクURL` 2909.
- Defects in the audited entry: **none** in the quoted spans. One ambiguity at entry:74 ("Neither body names a crawler").

VERDICT: 13/13 quotes raw substrings, in-article, ≤24 units and ≤26 chars; the four S419-shared and eight page-unique claims hold exactly; no misattributed unquoted phrase; only entry:74's "names a crawler" wording is ambiguous against a body that says クローラー 8 times.
