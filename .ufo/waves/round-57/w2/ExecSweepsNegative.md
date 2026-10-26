# ExecSweepsNegative

Claim C3, round-57 W2 falsify. Artifact attacked: the two entries as committed at lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` — `git diff --stat 4b8c730 -- corpus/knowledge/baidu-dead-link-types.md
corpus/knowledge/baidu-spider3-dead-link-model.md .ufo/waves/round-57/sources/` prints nothing (working tree at
`51921b97124616d8526160231aec5c5708c74f3d`, both entries and both bodies byte-identical to the attacked revision).
Bodies: `.ufo/waves/round-57/sources/S421.html` (34750 B) / `S422.html` (27327 B), sha256 as in `sources/receipts.json`.
Scopes used throughout: `RAW` whole body, `BLOCK` article block slice, `TEXT` article-block text nodes under the
counter's version-2 rule (node-by-node), `PAR`/`NODE`/`SENT` = named paragraph / one text node / one sentence.
Locators re-implemented from `c57_quote_truth.py:95-96` + its `content_window`/`text_segments`, not imported.

## SCRIPT:

`python3 -B .ufo/waves/round-57/w2/ExecSweepsNegative.files/sweeps.py` — exit 1 (one encoded claim disagrees, S422-4),
full output retained at `.ufo/waves/round-57/w2/ExecSweepsNegative.files/sweeps-run.txt`.
The script is self-contained (no network, no git write): extraction, 19 claim groups (75 term/scope checks, 66 with a stated expectation), the
stated-command audit, the five added sweeps and the quote-class sweep. Every row prints the term, the scope and the
recomputed count, so each number below is reproducible by one command. Files written by this seat: this report,
`.files/sweeps.py`, `.files/sweeps-run.txt`. No tool install was needed.

## CLAIM SWEEPS:

Every sentence of the form "the page does not say / states no / zero occurrences / not described as" found in the two
entries (`grep -nE "does not|states no|states nothing|no claim|not described|occur zero|names no|prints no|neither|nothing"`
over both files), with its sweep and count. All counts confirmed by running. Three negative sentences are about the
entry rather than the page and are excluded by scope: S421:8 ("that this entry does not copy"), S421:102 ("bind nothing
beyond what is quoted"), S422:24 tail ("claims no blocking rule from it"); each is a statement about the entry, not a
claim that the page is silent.

| # | entry:line | claim (compressed) | sweep (term@scope) | count | claimed | verdict |
|---|---|---|---|---|---|---|
| 1 | S421:66 | "not described as status-code-only" | `状态码@PAR[63-70]` | 0 | 0 | agrees |
| 1b | S421:66 | same | `页面状态@PAR[63-70]` | 1 | ctx | status word present, see risk R5 |
| 2 | S421:91 | "states nothing about removing a path from internal links" | `内链` / `内部链接` / `删除链接` / `移除链接` @TEXT | 0 / 0 / 0 / 0 | 0 | agrees |
| 2b | S421:91 | same (context) | `删除@TEXT` (nodes 24,47,87,126,130) | 5 | ctx | all five about deleted content/pages or the submission file |
| 3 | S421:95 | "does not reconcile the two 404 statements" | `矛盾@RAW`; `200@TEXT`; `404@TEXT` | 0; 1; 11 | ctx | interpretive, see R7 |
| 4 | S421:100 | "no definition of a monitor or a link checker" | `监控`/`检查`/`校验`/`巡检`/`死链检测`/`链接检查` @TEXT | 0 each | 0 | agrees |
| 4b | S421:100 | same (context) | `检测@TEXT` (node 57) | 1 | ctx | crawler checks content value; not a monitor definition |
| 5 | S421:100 | "no claim that any tool cannot see a content dead link" | `看不到`/`无法发现`/`发现不了`/`检测不到` @RAW | 0 each | 0 | agrees |
| 5b | S421:100 | same (context) | `无法@TEXT` (nodes 13,27,35) | 3 | ctx | other senses (cannot offer value / cannot be set / briefly unreachable) |
| 6 | S421:101 | "The page states the 1–2 week effect cycle" (affirmative neighbour) | `1-2@TEXT`; `生效周期@TEXT` | 1 (node 141); 2 | positive | agrees |
| 7 | S422:18 | "404 and 状态码 occur zero times in the retained body" | `404@RAW`; `状态码@RAW` | 0; 0 | 0 | agrees |
| 8 | S422:24 | "屏蔽 occurs once in the whole body, inside this label" + "the paragraph under it speaks about … only" | `屏蔽@RAW`; `@NODE:28`; `@PAR[30-34]` | 1; 1; 0 | 1; 1; 0 | agrees |
| 9 | S422:59 | "删除, 移除 and 下线 occur zero times" (+ `移出`/`清除`/`去除`/`取消收录`/`清空`) | `@RAW` | 0 each | 0 | agrees |
| 10 | S422:59 | "the article block's only 索引 occurrences are the two in the index-display sentence" | `索引@TEXT`; `@NODE:22`; `@NODE:26` | 2; 1; **1** | 2; 1; 0 | **DISAGREES** (see F1) |
| 11 | S422:18 | "the only other mention of 协议死链 is the preference" | `协议死链@RAW`; `@NODE:34` | 2; 1 | 2 | agrees |
| 12 | S422:37 | "does not restate the majority qualifier in this sentence" | `大多数@SENT[大约几天内]`; `@PAR[30-34]` | 0; 1 | 0 (sentence); 1 (paragraph) | agrees at sentence scope, see R6 |
| 13 | S422:61 | "no rate, no percentage, no measurement for dead-link handling" | `%@PAR[30-34]`; `@TEXT` | 0; 7 | 0 (paragraph); ctx | agrees (nodes 7,9,21,25,56) |
| 14 | S422:62 | "the paragraph names no report, no tool and no status" | `报告`/`工具`/`状态` @PAR[30-34] | 0/0/0 | 0/0/0 | agrees |
| 14b | S422:62 | same (context) | `平台@PAR[30-34]` | 1 (站长平台) | ctx | see R4 |
| 15 | S422:37 | "does not say the platform submission became unnecessary" | `无需`/`不需要`/`不必`/`不用` @RAW | 0 each | 0 | agrees |
| 16 | S422:18 | "names all three kinds and defines none of them here" | `定义`/`是指`/`指的是`/`即` @RAW | 0 each | 0 | agrees |
| 17 | S422:60 | "prints no status code and no HTTP term" (also covers "states neither half", S422:66) | `HTTP`/`状态`/`404`/`状态码` @RAW | 0 each | 0 | agrees |
| 18 | S422:43 | "does not say the other recognised kinds fail, are rejected, or go unhandled" | `失败`/`拒绝`/`不处理`/`无法识别`/`忽略` @RAW | 0 each | 0 | agrees |
| 19 | S422:37 | "the verb is 处理, not a removal from an index and not a deletion" | `删除索引`/`从索引`/`移出`/`取消` @RAW | 0 each | 0 | agrees |

Stated-command audit: the S422 entry prints 8 `grep -o -F '…' -> n` commands (`404`->0 twice, `屏蔽`->1 twice,
`删除`/`移除`/`下线`/`状态码`->0); all 8 recompute to the printed value — confirmed by running. The S421 entry prints
**no** page-silence command for any negative page claim (its only grep is the presence recheck `协议死链和内容死链`->1,
line 3, and one `span_tools.py check`, line 8).
Quote-class sweep (S422:74 claim "occurs once in that body and in no other retained body"): all 11 quoted spans
occur once in S422 and 0 times in S421, each inside one text node, none crosses a tag, longest = 25 units / 27 chars —
exactly the ceiling the entry states. The S421 entry states no quote class; its 22 quoted spans likewise occur once in
S421 and 0 times in S422 (swept anyway).

## ADDED SWEEPS:

Five sweeps the entries do not state; a reader checking "the page is silent" would add them. Counts confirmed by running.

| id | sweep | command / pattern | S421 | S422 |
|---|---|---|---|---|
| A1 | status codes other than 403/404/503/200 in either article | `(?<![0-9])[1-5][0-9]{2}(?![0-9])` over TEXT (ASCII-digit bounded; `\b` fails beside CJK) | TEXT codes 403,404,503,200,**500** (node 117) | **no status code**: 500 = `500亿` (node 16), 100 = `60%--100%` (node 56) |
| A2 | 删除/移除/下线/索引 in S421 | literal counts, RAW/BLOCK/TEXT | 删除 5, 移除 0, 下线 0, 索引 3/2/2 (nodes 132,135) | n/a |
| A3 | robots in either article | `(?i)robots` | RAW 3, BLOCK 0, TEXT 0 | RAW 3, BLOCK 0, TEXT 0 |
| A4 | sitemap in S421's article | `(?i)sitemap` | RAW 2, BLOCK 2, TEXT 2 (nodes 93,133) | 0 |
| A5 | English soft-404 wording | `(?i)soft[\s_-]?404\|soft\s*error\|soft\s*not[\s-]?found` | 0 | 0 |

Notes on the added counts: A1's S421 `500` is one occurrence, in the FAQ question `【死链提交】工具可以识别403、500` /
`等无效数据吗？` (node 117) whose answer is `不可以，…仅识别404` (nodes 119-120) — the page raises 500 only to reject it;
no S422 code exists at all (raw extras are markup: JS IP-range regex 127/172/192 and CSS px 267/530/476/538/123).
A2's two S421 `索引` are `索引型` (index-type sitemap) in the FAQ (nodes 132,135); the third raw `索引` is the nav link
`索引量` outside the article block. A3's three robots hits per body are a JS word list plus the `/robots/index` href and
`Robots` nav label — zero in article text, so neither page says anything about robots. A4 shows S421's article **does**
speak of sitemap: the dead-link file format `（与sitemap格式及制作方法一致）` (node 93) and the rejection of `索引型`
sitemap submissions (nodes 132-136); neither entry carries it. A5 confirms neither page uses English soft-404 wording; the
single raw `soft` is `Microsoft` in the IE-upgrade notice script.

## FALSE OR UNBACKED CLAIMS:

**F1 — FALSE (confirmed by running). `corpus/knowledge/baidu-spider3-dead-link-model.md:59`:** "the article block's only
索引 occurrences are the two in the index-display sentence above (the body's third 索引 is the navigation link 索引量,
which sits outside the article block)". The count is right (`索引@TEXT` = 2; `@RAW` = 3) and the parenthetical about
`索引量` is right, but the location is wrong: only **one** article occurrence sits in the index-display sentence
(node 22, `索引展现时效性提升，原来是`); the second is inside **`搜索引擎`** ("search engine") in the following sentence
(node 26, `我们都知道，搜索引擎从用户搜索到最终搜索结果展现的步骤是…`). Sweep: `sweeps.py` S422-4, `NODE:26 count=1
claimed=0`. The claim's conclusion (the page states no index-removal) is unaffected, but the sentence as written is false
and should read "one in the index-display sentence and one inside 搜索引擎 in the next sentence". Section location of
the two: the index-display sentence sits under the page heading `『抓取、建库更快—提交的内容更容易被抓取』` (node 12), and
the `搜索引擎` sentence is the explanatory sentence that follows it in the same section; neither is in the dead-link
section `『死链处理更及时—被黑低质页面全屏蔽』` (node 28).

**U1 — UNBACKED (no sweep command in the entry). `baidu-dead-link-types.md`:** five negative page claims (lines 66, 91,
95, 100 twice) carry no page-silence command at all; the entry has no `Page-silence sweeps` block (the S422 entry has one
at line 76). All five recompute as claimed (table rows 1-5), so this is a documentation gap, not a factual error.

**U2 — UNBACKED (no sweep command). `baidu-spider3-dead-link-model.md`:** 9 of its 13 negative-claim groups have no
printed command — 索引 accounting (59), 协议死链 uniqueness (18), 大多数 restatement (37), percentage placement (61),
no report/tool/status (62), no failure/rejection (43), define-none (18), no-removal synonyms (59), HTTP-term scope (60,
partially covered by the `状态码`/`404` commands). All recompute as claimed; only the 索引 sentence is false (F1).

**R4 — wording risk, not false. `baidu-spider3-dead-link-model.md:62`:** "the paragraph names no report, no tool and no
status" holds for those three nouns (0/0/0 in nodes 30-34) but `站长平台` is named in the same paragraph (`平台`=1); the
entry calls it "the submission channel", so the claim survives only under that reading.

**R5 — wording risk, not false. `baidu-dead-link-types.md:66`:** "the page does not describe either as status-code-only"
holds for `状态码` (0 in the discovery paragraph), but the crawler-software sentence does say the tool `分析页面状态`
("analyses page status"), node 70 — a status word is present; only the "status-code-only" reading is excluded.

**R6 — fragility, not false. `baidu-spider3-dead-link-model.md:37`:** "does not restate the majority qualifier in this
sentence" is true at sentence scope (`大多数@SENT` = 0) but the few-days sentence and the recognition sentence sit in ONE
text node (32), so a re-run with the counter's version-2 `text_segments` extractor returns 1 for the node — the sentence
slice, not the node, has to be the unit.

**R7 — interpretive, tagged [INFERENCE]. `baidu-dead-link-types.md:95`:** "The page does not reconcile the two 404
statements" cannot be settled by any sweep; supporting count `矛盾@RAW`=0, and no text node holds both `200` and
`404`; the only sentence carrying both is the impossibility sentence, split across nodes 26-27. Reported as a reading,
not a measured absence.

No credential material, session tokens, secret-manager references or private URLs were read or written. No pacman
run, no tool install, no git/jj mutation; the only writes are the three paths named in SCRIPT.

VERDICT: C3's negative claims survive except one false location in `baidu-spider3-dead-link-model.md:59` (second article 索引 sits in 搜索引擎, not the index-display sentence); S421 states no sweep command for any of its five negative page claims, and S422 leaves 9 of 13 unswept — all other 18 claim groups, all 8 printed S422 commands, the quote-uniqueness claim and the five added sweeps recompute exactly as written.
