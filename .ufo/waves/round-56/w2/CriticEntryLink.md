# CriticEntryLink

Entry: `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` (124 lines; blob at `a450e43e` sha256 `85f234bf…`,
byte-equal to the worktree file) vs retained body `.ufo/waves/round-56/sources/S367.html` (sha256 `0188de9dae01e90882310
98a9c6af3c8f5dc62a5982419a5f82fd98e86772a19`, 8051 bytes, HTTP 200 in `receipts.json`).

Ran, read-only: `span_tools.py check` on all 17 double-quoted spans; `grep -o -F` sweeps over S367; `sha256sum`/`wc -c` vs
`receipts.json`; one live `curl -fsSL … | grep -F -c` (-> 1) and the same grep over the retained body (-> 1); `git show`
base `e48354b7` vs tip `a450e43e` row compare; replication of `c55_readme_index.py`'s word-commonality formula (L114-166) over
`git ls-tree` at `a450e43e`. Provenance (:3, :119) verified, no fix: `sha256 0188de9d…a19` and 8051 bytes match the file and
`receipts.json` (HTTP 200, fetchedAt 2026-10-25T22:02:40+00:00), and both recheck arms re-ran today (live curl 1,
retained-body grep 1). NOT run (unrun): `c56_selftally.py`, `c56_quote_truth.py`, `c55_readme_index.py`, any `--selftest`,
`sources-census.sh`, `validate_append.sh`.

## FINDINGS:

**F1 HIGH — entry:9-10 — "This page states a third surface" is a miscount and a scope widening.**
Page (`S367.html:104`): 「リンク先ウェブページの巡回制限は、`rel=&quot;nofollow&quot;`属性を使った指定方法のほかに、HTMLの
メタタグで指定する方法と、サーバーの設定で指定する方法があります。」 The three routes are attribute + meta + server; the lane
already holds the attribute (S374), so the page adds **two** surfaces, and S372 (robots.txt at the site root) is not one of the
page's three at all — counting it into "third" is wrong in both directions. Entry:12 ("three specifying methods") and :28-29
("a sub-heading and a setting for the meta-tag and server routes only") contradict :9; `SOURCES.md:157` cell 4 says "the meta
tag and the server header, beside the per-link attribute S374 holds". Same sentence, second overread: "without refusing itself"
is a crawl claim; the page's word is インデックスへの登録 (registration), which is what the gloss permits.
Fix: "The lane holds the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`, S374) and the refusal file at the site
root (`yahoo-japan-robots-txt-refusal-rules.md`, S372). This page adds two surfaces the lane did not hold — a meta tag in the
page's own head and a directive on the server hosting it. For the meta tag it states that the crawl of the link-target pages
inside this page is refused while the page's own registration in the index is permitted [S367]; the crawl of the page itself is
not its subject. Nothing below was served to a crawler."

**F2 HIGH — entry:77 — "No third value" is falsified by the retained body.**
Page (`S367.html:14`, the page's own head): `<meta name="robots" content="index,follow,noarchive,noodp" />` — a third content
value for `name="robots"`, outside the article block. Command: `grep -o -F 'content="index,follow,noarchive,noodp"
.ufo/waves/round-56/sources/S367.html | wc -l` -> 1. The entry already handles head content this way (:96-97 calls the head
description "outside the article block"), so the negative is false as written, not merely out of scope.
Fix: "The article gives two values and no third; the page's own head, outside the article block, carries
`index,follow,noarchive,noodp` as the page's own setting, which the article states no rule for. No example names a single
crawler in the tag's name value, and the article gives no rule for combining values."

**F3 MEDIUM — entry:21 — "ほかに (besides) opens the sentence" is false about the sentence.**
Page: the sentence opens 「リンク先ウェブページの巡回制限は、」 and the qualifier is のほかに, attached after the attribute
phrase. The conclusion ("a further route precedes these two") holds; its stated ground does not, and :121 lists the kept
qualifier as ほかに where the page writes のほかに.
Fix: "のほかに (besides) attaches to the attribute phrase the quote skips, so the attribute is the route the two named here are
added to, and 方法があります states that the methods exist without attaching an effect to either named method."

**F4 MEDIUM — entry:104 — "its only per-link route is the pointer to archives/002851.php" is an unmarked inference.**
The page states no scope for the attribute — the entry itself says so at :28 ("this page states no semantics for the
attribute"). "Per-link route" imports S374's subject into a sentence about what this page states.
Fix: "The page names one further route, as a pointer to archives/002851.php (held as S374), and states nothing about that
route's scope or its application to one link URL."

**F5 MEDIUM — entry:28-29, 38-39, 77-78, 95-96, 103-105, 106, 109, 112-115, 120-121 — negative claims and counts carry no sweep.**
Nine absences and three counts ("only", "occurs once", "at most 25 units") are unverifiable by a reader. Measured (run):
`for t in 'robots.txt' 'ワイルドカード' '優先' 'ステータス' '404' '200' 'リダイレクト' 'エラー' '失敗' 'できません'
'できない' '場合'; do printf '%s\t%s\n' "$t" "$(grep -o -F "$t" B | wc -l)"; done` -> robots.txt 0, ワイルドカード 0, 優先 0,
ステータス 0, 404 0, 200 0, リダイレクト 0, エラー 0, 失敗 0, できません 0, できない 0, 場合 1; `grep -o -F 'name="robots"' B |
wc -l` -> 3 (head + two `<pre>` examples; the six `name=` values are description, robots×3, pagetop, contents-start — no crawler
name); `grep -o -F '個別リンクURL' B | wc -l` -> 1 (`S367.html:125`, outside the article); article structure `<h3>` 2,
`<pre>` 3, `<a href>` 1 (archives/002851.php), `002851` 2 (article href + sidebar `S367.html:247`).
Fix: one paragraph after §"Quote classes" — "Sweeps for the absences above, over `S367.html` (sha256 `0188de9d…`): <command> ->
robots.txt 0, ワイルドカード 0, 優先 0, 404 0, 200 0, リダイレクト 0, エラー 0, できません 0, できない 0, 場合 1; `name="robots"`
3; 個別リンクURL 1; `<h3>` in the article 2" — and have each "no …" sentence name it.

**F6 MEDIUM — entry:106-108 — "The lane's status ground is a Google page on crawl errors (`crawl-error-status-table.md`, S286)"
attributes a role that entry does not carry.** `crawl-error-status-table.md:9-10` admits one sentence (Googlebot scaling
crawling back) and :17 says "A soft-404 remedy is not claimed from this sentence"; it states no status code, so the "no contrast
is drawn" rests on a mis-described comparator.
Fix: "The lane's nearest status ground is a Google page on crawl errors (`crawl-error-status-table.md`, S286), which admits one
scaling-back sentence and no status code; this page states none either, so no contrast is drawn."

**F7 LOW-MED — entry:56-57 — "leaves the page's own registration permitted" changes the modal.** Page: 「上記の例は、「…この
ウェブページ自身はインデックスへの登録を許可する」という意味を持ちます。」 — the example's *meaning* (permits), not an effect it
leaves behind. Fix: "So the example means the page's own registration in the index is permitted while the crawl of its link
targets is refused."

**F8 LOW — entry:69-70 — "not offered as an alternative" is ambiguous against という場合には.** Page: 「「…登録も拒否する」
という場合には、次のように記述します」 — the second tag is introduced as a separate case. Fix: "も attaches the second refusal to
the first inside that case: the tag refuses both the target crawl and the page's own registration; the page offers the two
examples as separate cases (という場合には)."

**F9 LOW — entry:22 — "without attaching an effect to any crawler" carries an unstated universal.** The page names no crawler
in the article (クローラー 6 hits, all navigation/footer), so "any crawler" is an absence claim inside a syntax note, unmarked and
unswept. Fix: drop the clause and let the F5 sweep carry it.

**F10 LOW — entry:1 — the § locator does not occur in the body.** Body (`S367.html:78`): `<h2>リンク先のウェブページの巡回制限
\u3000― ウェブページ内やサーバーでの設定</h2>` (U+3000). The entry's header uses an ASCII space: 0 hits for the ASCII form, 3
for the U+3000 form; Q1116 requires the cited heading text to occur in the body. The registry cell (`SOURCES.md:157` cell 5)
carries the same ASCII form and stays byte-equal, so the entry is the only place this can be corrected.
Fix: write the heading with U+3000, or append "（見出しの空白は全角）" to the § label.

**F11 LOW — entry:41-43 and 72-74 — the code blocks are entity-decoded renderings with no stated class.** Raw body:
`&lt;meta name="robots" content=&quot;index,nofollow&quot;&gt;`; the entry prints the decoded form as "The example printed
under it", and §"Quote classes" (:119-121) classifies only double-quoted spans. Fix: "The example printed under it (rendered;
the raw body carries `&lt;` and `&quot;`):" plus "The two example blocks are rendered forms, not quotations."

**F12 LOW — entry:12, 76, 120, 122 — counts without commands.** Measured: 17 spans, all raw, all in-content, all
`count_in_page == 1`, none in S419/S420, max 24 units (25 with 」 under a punctuation-counted reading); the first gloss as one
span is 57 units and the second 41, so "runs past the 25-unit ceiling as one span" is true; the 31-unit round-53 span is
`contract.md:80` + `corpus/lessons/round-55.md` L15, not re-measured here. Fix: name `python3 -B .ufo/waves/round-56/
span_tools.py check S367 '<span>'` and give "17 spans, max 24 units, count 1 each"; cite the 31-unit Gate line by file:line.

**F13 LOW — entry:12-29 — redundancy with the S374 entry, which states the same framing.** `yahoo-japan-rel-nofollow-
semantics.md:21`: "which is why the attribute is one of its three routes and not a separate mechanism [S374]"; `:26-27`: "the
lane's robots-refusal ground (S372, S373) and its meta/header link-target restriction (S367) are the mechanisms that speak to
crawling itself." Fix: keep the quoted opening and the attribute pointer as one sentence, and drop the re-enumeration of what
S374's entry already says.

## OMISSIONS:

**O1 MEDIUM — the operator's own 404 statements are not pointed to (entry:106-108).** `S419.html` and `S420.html` each carry
「HTTP 404 Not Found」 once (`grep -o -F '404' … | wc -l` -> 1 each). A publisher told "this page states no status code" is left
with a Google page as the lane's only status pointer, though the same operator's pages state the status this round.
Fix: "…this page states no status code; the same operator's pages on a deleted URL and on a non-existent URL do state HTTP 404
Not Found (`yahoo-japan-deleted-url-recrawl.md`, S419; `yahoo-japan-nonexistent-url-recrawl.md`, S420)."

**O2 MEDIUM — the page files `rel=nofollow` as a 巡回制限 method while S374's entry records it is not a crawl refusal; the
entry states neither side (entry:8-10, 27-29).** `yahoo-japan-rel-nofollow-semantics.md:10-13` ("A link attribute is a statement
about endorsement, not a crawl refusal"), `:24-25` ("Reading `nofollow` as 'do not fetch this URL' is the over-read this row
exists to stop"). Fix: "The page files the attribute as one of its three 巡回制限 routes [S367]; the attribute's own page, held
as S374, states endorsement and ordering and not a crawl refusal — one operator's filing and its semantics, and this entry draws
no rule from the filing."

**O3 LOW — the server example's case is unremarked (entry:92).** The page prints `X-Robots-Tag: NOFOLLOW` in upper case, both
meta values in lower case, and states no case rule. Fix: one clause naming the difference and the page's silence.

**O4 LOW — the page's age is in the header only (entry:1).** 更新日 2010年11月24日; `yahoo-japan-robots-txt-refusal-rules.md:114`
carries the corresponding body sentence. Fix: "The page prints 更新日 2010年11月24日; this entry reports the retained body fetched
2026-10-25 and makes no claim that the live documentation still reads the same."

## VERDICT PER CRITERION:

- Q1100-1108 (quote class derived from the blobs, r50): **PASS** — 17/17 raw substrings, entities as written (`&quot;`, `&lt;`).
- Q1115 (cited `S###` resolves in this lane's registry, r53): **PASS** — S286 `SOURCES.md:151`, S372 `:158`, S374 `:154`.
- Q1116 (locator points to the section holding the quote, r53): **FAIL** — F10; the three named headings otherwise occur.
- Q512-515 / Q541-545 (qualifier in the quote or marked; no over-marking, r31): **PARTIAL** — F1, F4, F9 unmarked; the two
  `[INFERENCE]` tags at :97-99 are correctly placed (the page states neither response delivery nor the token's effect).
  このウェブページ内にある, このウェブページ自身は, も, という場合には are kept in the glosses.
- Q1120-1132 (translation preserves a material qualifier, r54): **PARTIAL** — F7 (modal), F8 (case structure); nothing else
  dropped.
- Q1133-1144 (CJK length names its unit, r54): **PASS** — convention named; max 24, 25 under a punctuation count.
- Q1148-1159 (an entry lands with its index row, r55): **PASS by formula replication, counter unrun** — `corpus/README.md:70`
  names `knowledge/yahoo-japan-link-target-crawl-restriction.md`, 12-token description, shares "server" (4/52 = 8%, not
  common), one file in the row.
- Q1160-1169 (≤25 units, ≥3 page-unique spans, raw, in-content, r55): **PASS** — max 24u; 17/17 count 1, in-content, absent
  from S419/S420.
- Q1170-1173 (held row reused changes `used-by` only, r55): **PASS (row, read-only)** — 10 of 11 cells byte-equal base vs
  `a450e43e`, cell 10 (`used-by`) differs.
- Q1174-1180 (validated append), Q1181-1186 (counter attacked before it scores), Q1190-1197 and Q1199-1201 (tally, selftest
  pin): **not this seat** (wave-1/wave-2 executor and critic reports; C1).
- Q1203-1205 (held body pinned by sha256, r56): **PASS** — the pinned value equals the file and the receipt.
- Q1207-1209 (page-unique across every retained body, r56): **PASS** — every span absent from S419 and S420.
- Q1211-1213 (a staged candidate is re-derived, not renamed, r56): **PASS** — no staged name; no per-link-URL refusal claimed
  as the page's (the F4 fix keeps it out).
- Q1215-1216 (no quote from a line with a raw double quote, r56): **PASS** — the two `<meta …>` lines are code blocks, not
  quoted spans; F11 asks their class to be labelled.

VERDICT: 13 findings (2 high: "third surface" miscount/scope at :9-10, "No third value" falsified by the page's own head) and 4 omissions; quotes, receipts, row reuse, index row and unit ceilings pass — the entry needs the F1/F2 corrections plus a sweeps paragraph before admission.
