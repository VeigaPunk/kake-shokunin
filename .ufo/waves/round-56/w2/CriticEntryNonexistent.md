# CriticEntryNonexistent

Attack on `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` (blob `9dc271a6…`, byte-equal to
`git show a450e43e:…`; 95 lines) against `.ufo/waves/round-56/sources/S420.html` (7332 B, sha256 `a860d4f3…`, HTTP 200
in `receipts.json`), with S419/S367 (adopted) and S387/S388/S389 (retained, not adopted) as comparison bodies. Article
block = `span_tools.py window` (offsets 2456–2909). Lane read only; no git/jj mutation. The header `recheck`'s live arm
re-ran 2026-10-25 → 1. Line numbers are the entry's (`cat -n`).

## FINDINGS:

**F1 HIGH — L74: a negative claim that is false, and false against the entry's own quote.**
Entry: "Neither body names a crawler, an interval, or what the index does with the page [S420]."
Page: S420 `クローラーはエラーページとみなさず、`; S419 `クローラーは削除されたウェブページと認識できず、`. The word クローラー
occurs once in each article block (8× in each raw body, sidebar). The entry quotes it itself at L28.
Sweep (run): `span_tools.py window S419|S420 | grep -o -F クローラー | wc -l` → 1 / 1;
`grep -o -E 'Googlebot|Slurp|Bingbot' sources/S419.html sources/S420.html | wc -l` → 0.
Fix: "Neither body names a crawler product or user agent, a crawl interval, or what the index does with the page; the
only agent word on either is クローラー (`grep -o -F 'クローラー'` on each article block prints 1, and
`grep -o -E 'Googlebot|Slurp|Bingbot'` on both bodies prints nothing, 2026-10-25) [S419][S420]." The cite must name
both ids; the sentence is about both bodies.

**F2 MEDIUM — L20 and L6: the page's conditional configuration is rendered as a flat assertion, and the return verb
is never quoted or glossed.**
Page: `サーバーが「HTTP 200 OK」のステータスを返してエラーページを表示する設定にしていると、クローラーはエラーページとみなさず、巡回を続けます。`
Entry L18 quotes `サーバーが「HTTP 200 OK」` (no verb, no conditional) and L20 renders "the server answers with the
status `HTTP 200 OK`" — "answers" comes from 返して, which is outside the span, and 設定にしていると ("is configured
to") is dropped from the rendering; L6's title then states the rule with no condition and no agent: "An error page
answered with HTTP 200 OK is not read as an error page".
Fix: quote the missing middle span `のステータスを返して` (10 units, raw substring) and render L20 as "the server
returns the status `HTTP 200 OK` — the verb 返して and the noun ステータス sit between this span and the next, both
outside the quotes; the clause closes with 設定にしていると, so the whole sentence is a conditional about a server
configuration, not a standing rule." Retitle L6 to keep the agent and the condition, e.g.
"# A nonexistent page answered 200 OK with an error page is still crawled by the crawler" (or, shorter,
"# The crawler does not treat a 200-OK error page as an error page").

**F3 MEDIUM — L12: scope narrowed past the page, unmarked.**
Entry: "The condition is a request for a page that does not exist, not a page once published and removed".
Page: `存在しないウェブページを表示しようとしたときに、` — an attempt to display; the page draws no line against a
removed page (削除 occurs 0× in the S420 article block; the single raw-body 削除 is the sidebar link to 002856). A
removed page is a page that does not exist; the operator's two pages are a taxonomy, not an exclusion in S420's words.
Also "request" is not the page's word (表示しようとした = an attempt to display, as L16 itself glosses).
Fix: "The condition is an attempt to display a web page that does not exist; the page names no cause and states no
exclusion of a page that was once published and then removed — that case has its own operator page (S419), and S420's
words do not exclude it [INFERENCE]."

**F4 MEDIUM — L54–L70: the fallback section is a second authority for a reading the lane already holds.**
Existing lane line, `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md:38`: "Three qualifiers hold the remedy's
scope: このような設定ができない場合には (where such a setting cannot be made — the fallback is conditional),
エラーページのHTMLの head (the tag belongs in the error page's own head, not in the page that used to exist at the
URL), and メタタグを使った (by means of a meta tag). The remedy text names no tag name, no content value and no
attribute [S419]". Existing line `:40`: "The same substitute appears on the operator's robots page,
`corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` (S372): a site that cannot place robots.txt is told to set
index-registration refusal with a meta tag, and that page names no value either. [S419] adds the location — the error
page's head — and still no value."
All four spans quoted at L54–L66 are the four S419-shared spans (verified `in_other_adopted_body`), and the same
reading is re-derived; L70 repeats the S372 comparison but says "the same fallback" without noting that S372 names no
location (S372 body: `ルートディレクトリに任意のファイルを設置できない場合は、「robots.txt」による巡回拒否はできません。メタタグで、インデックスへの登録拒否を設定してください。`).
Fix: replace §"Where that setting cannot be made" with one pointer plus the one differing span: "The fallback's scope
and the S372 substitute are read in `yahoo-japan-deleted-url-recrawl.md` (§The fallback where that setting cannot be
made, lines 31–40); S420 differs only in the phrase — `メタタグを使ったインデックス拒否の設定` (19 units, page-unique),
not インデックスへの登録拒否 — and names no tag name and no value (`grep -o -F -e noindex -e 'name=' -e 'content='` on
`span_tools.py window S420` prints nothing, 2026-10-25; on the raw bytes `name=` occurs 8× as the page's own HTML
attributes, so the sweep must be on the article text)."

**F5 MEDIUM — L34: "no 可能性, no interval and no frequency" carries no sweep.**
Page: no 可能性 (0×); S419 has 1× in 巡回し続ける可能性があります. Verified: `grep -o -F -e 可能性 -e 頻度 -e 間隔
.ufo/waves/round-56/sources/S420.html` → no output. Note the trap: 回 occurs 2× in the S420 article block, both
inside 巡回.
Fix: "… stated without a qualifier: `grep -o -F -e 可能性 -e 頻度 -e 間隔` on the retained body prints nothing (0),
where the deleted-URL body prints 1 可能性, 2026-10-25; the two 回 in the article block are inside 巡回."

**F6 LOW — L16: "the page names no cause such as a typo or a renamed route" carries no sweep.**
Verified: `grep -o -F -e タイプミス -e リダイレクト -e 移転` on S420.html → no output.
Fix: append "(`grep -o -F -e タイプミス -e リダイレクト -e 移転` on the retained body prints nothing, 2026-10-25)".

**F7 LOW — L44 and L50: two status-count claims, one command, one id.**
Verified (run): `grep -o -E 'HTTP [0-9]{3} [A-Za-z ]+' sources/S419.html sources/S420.html` → `S419:HTTP 200 OK`,
`S419:HTTP 404 Not Found`, `S420:HTTP 200 OK`, `S420:HTTP 404 Not Found` (4 lines, nothing else).
Fix: L44 "…the second and last status value the page names (`grep -o -E 'HTTP [0-9]{3} [A-Za-z ]+'` on both retained
bodies prints exactly those four lines, 2026-10-25)"; L50 cite both ids, [S419][S420], since the sentence covers both.

**F8 LOW — L74: "a page that should not be served" is the lane's intent characterization, untagged.**
Page: `削除したURLのウェブページ` (S419) / `存在しないウェブページ` (S420); neither says the page should not be served.
Fix: "Both bodies state a server returning 200 OK for a page that is deleted (S419) or does not exist (S420), …".

**F9 LOW — L78: a negative about crawl budget with no sweep, and a restatement of an existing line.**
Existing `yahoo-japan-deleted-url-recrawl.md:44`: "`crawl-error-status-table.md` records one admitted Googlebot
sentence: crawling is scaled back when the servers are detected to have trouble (S286)." The S420 entry restates it
and adds "S420 says nothing about crawl budget, crawl rate or a robots block" with no command.
Fix: cite the existing line instead of restating it, and give the sweep: "the S420 article block names no crawl budget,
no crawl rate and no robots.txt (`span_tools.py window S420 | grep -o -F -e クロールの予算 -e クロールレート -e
robots.txt` prints nothing, 2026-10-25)".

**F10 LOW — L82: the page-unique count names neither population nor command.**
"the other eight are page-unique" — true, but only under the round-56 definition. `span_tools.py check` compares the
three adopted bodies only; the retained set is six. I re-ran all 12 spans against S367, S387, S388, S389, S419, S420:
the eight occur only in S420 (the four shared occur once each in S419; `を行ってください` occurs 2× inside S420 itself).
Fix: add "(`span_tools.py check S420 '<span>'` for each span; page-uniqueness re-run against all six retained bodies —
S367, S387, S388, S389, S419, S420 — not only the three adopted ones, 2026-10-25; `を行ってください` closes both
sentences of the article block)".

**F11 LOW — L34: the soft-404 tag asserts an industry use the lane does not hold consistently.**
Entry: "[INFERENCE] the lane reads this shape — a success status in front of an error page — as what the industry calls
a soft 404". `corpus/knowledge/vault-properties.md:36` applies the same term to a different shape: "**302 →
`statics.kimi.ai/pages/preview-404-en.html`** (soft-404; distinct class from hard 404)". The page has no 'soft'
(`grep -ci soft` = 0), so the tag is honest about the source but the term now covers two shapes with no entry stating
the relation. Fix: "[INFERENCE] the lane reads this shape as a soft 404; the page does not use the term. The lane also
applies the term to a 302 → error page (`vault-properties.md:36`), so the reading is not narrowed to this shape."

**F12 LOW — L30: an interpretive verb gloss sits inside a rendering note, untagged.**
Entry: "(rendered: the crawler does not regard it as an error page — みなさず is a treatment, not a finding about the
body.)" That is the lane's reading of the verb. Fix: "(rendered: the crawler does not regard it as an error page.)
[INFERENCE] みなさず is a treatment verb, not a statement about the response body; S419 uses 認識できず."

Confirmed, not re-counted: the sibling reviewer's single defect (L56, the dropped additive `また、`) is real — the raw
body reads `設定を行ってください。<br / >また、このような設定ができない場合には、`. Its L14 pass on L74 is the
counterexample F1 attacks: the sidebar link it cites is a link title, not the article's use of クローラー.

## OMISSIONS:

- **O1 MEDIUM — the page's trigger is a pair, and the entry never states it.** The configuration is one clause:
  `…のステータスを返してエラーページを表示する設定にしていると、` — a success status returned *and* an error page
  displayed. The entry splits it into L18/L22 and quotes neither 返して nor the pairing, so a publisher cannot tell
  whether the trigger is the status alone or the status plus an error-page body. Fix: quote `のステータスを返して`
  (10 units) and render the clause once as a single configuration (see F2).
- **O2 LOW — the page's own headline is a claim, and it is never reported.** Title/heading
  `存在しないウェブページが巡回される` ("a nonexistent web page is crawled") occurs 3× in the body and is the operator's
  statement of the outcome; the entry cites it only as a locator (L1) and its own title states a weaker, agentless
  fact. Fix: report the heading as the page's summary, e.g. "the page's own heading states the outcome: the
  non-existent page is crawled."
- **O3 LOW — the L74 difference list is presented as exhaustive but omits the recognition clause.** S419:
  `削除されたウェブページと認識できず` (cannot recognize it as a *deleted page*); S420: `エラーページとみなさず` (does not
  regard it as an *error page*). Different verb, different object. Fix: add "S419's recognition clause names the
  deleted page, S420's names the error page."

## VERDICT PER CRITERION:

| Criterion (QUALITY, round-52..56) | Result |
|---|---|
| r50 "A quote's match class is derived from its own two blobs, never asserted" | PASS — 12/12 spans are raw substrings of the retained body, inside the content block, none a collapsed-only span labelled raw |
| r53 "A source id cited as held ground resolves in the lane's registry" | PASS — `corpus/SOURCES.md:166` row S420, URL 002857.php; S419 at `:165` |
| r53 "A source locator points to the section containing its quote" | PASS — the cited heading occurs 3× in the body; the article window contains all 12 spans |
| r54 "A translation preserves a material source qualifier" | FAIL — F2: the conditional 設定にしていると and the return verb 返して are dropped at L20 and in the L6 title |
| r54 "CJK quote length names its unit" | PASS — L82 names the unit and the 25-unit ceiling; measured 7–24 units, ≤24 characters |
| r55 "≤25 units, raw substring, content block, ≥3 page-unique spans" | PASS — 8 page-unique spans across all six retained bodies |
| r55 "An entry lands with its index row" | PASS — `corpus/README.md:72` names `knowledge/yahoo-japan-nonexistent-url-recrawl.md` |
| r55 "A held row reused changes `used-by` only" | not this seat — S420 is a new row; registry cells are the L1's surface |
| r56 "Sibling pages share phrases; page-unique across every retained body; a Gate quote once in its own page" | PASS on the facts (verified over six bodies); the claim carries no population or command — F10 |
| r56 "A staged candidate is re-derived, not renamed" | PASS — 'soft' absent from the body, the term is tagged [INFERENCE], no `yahoo-japan-soft-404-recrawl` file exists (prose mentions only); F11 disputes the term's scope, not the rename |
| r56 "A quote is not taken from a line with a raw double quote" | PASS — S420's article block holds no ASCII double quote; the spans use 「」 |
| Negative claim carries its sweep / population unit named (assignment rule; r50/r54 house rule) | FAIL — F1 (and false as written), F4, F5, F6, F7, F9, F10 carry negatives or counts with no command; F7's both-bodies claim cites one id |

VERDICT: quote-true but not claim-true — L74's "neither body names a crawler" is false in both article blocks (the entry quotes クローラー itself at L28), L6/L20 flatten the page's conditional configuration and never quote 返して, L12 narrows the condition past the page's words, and nine negatives/counts carry no sweep command; fix F1–F4 before admission.
