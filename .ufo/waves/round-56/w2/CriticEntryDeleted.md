# CriticEntryDeleted

Attacked: `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (row S419) at `a450e43e696d`; the file's working-tree bytes are byte-equal to `HEAD` and to `a450e43` (`git diff --stat HEAD -- <path>` empty), so the line numbers below are the committed ones. Page: `.ufo/waves/round-56/sources/S419.html` (sha256 `6172d5d1…`, 7428 B, `httpStatus 200` in `sources/receipts.json`). Read-only seat: no lane file, index or jj state touched.

Measured, not a finding: C2 in my own clone (`git clone -q --no-checkout` → `checkout a450e43`) prints `C2 quote-truth 8/8 met=True`, exit 0. Every finding below is prose fidelity the counter cannot see — the contract's own limit ("quote truth is substring truth, not support").

## FINDINGS

**F1 — HIGH — entry L6: the H1 drops the page's modal.**
Attacks: `yahoo-japan-deleted-url-recrawl.md:6` — `# A deleted URL that still answers 200 OK is a page the crawler cannot drop`.
Page (S419.html:104): `クローラーは削除されたウェブページと認識できず、そのウェブページを巡回し続ける可能性があります`. "cannot drop" is an impossibility; the page states 可能性があります. The entry keeps the hedge at L21 ("a possibility; the page does not say the crawl always continues"), so L6 contradicts L21, and a reader who keeps only the heading (and the index row, `corpus/README.md:71`) leaves with the certainty the page withholds.
Fix: `# A deleted URL that still answers 200 OK may keep being crawled`

**F2 — HIGH — entry L53: a negative claim the page's own sentence contradicts, with no sweep.**
Attacks: `:53` — `- No statement that the 404 is to come from the server configuration or from the application: the page's subject is サーバー, the server, and its sentence asks whether that server is so configured.`
Page (S419.html:105): `サーバーが「HTTP 404 Not Found」のステータスを返すように設定されているかを確認してください` — the page does attribute the 404 to the server's setting, which the bullet's second clause concedes; the first clause is therefore false, and the entry's own L26–L29 quote the attribution.
Fix: `- No statement about which layer writes the 404 setting: the page's subject is サーバー, and it asks whether that server is so configured; the process behind it is not named [INFERENCE] (sweep: `python3 -B .ufo/waves/round-56/span_tools.py window S419 | grep -c -E 'アプリケーション|設定ファイル|\.htaccess'` -> 0, 2026-10-25).`

**F3 — MEDIUM — entry L44: the modal is dropped a second time.**
Attacks: `:44` — "its stated outcome is a continued crawl, and it gives no rate, no frequency and no duration".
Page: `…巡回し続ける可能性があります` (S419.html:104). "continued crawl" as *the stated outcome* is the certainty the page does not state; the same sentence handles silence carefully, so the defect is the outcome phrase alone.
Fix: "its stated outcome is a possible continued crawl, and it gives no rate, no frequency and no duration".

**F4 — MEDIUM — entry L29: unmarked inference, and the contrast belongs to the sibling page.**
Attacks: `:29` — "The verb is 確認してください, please confirm: the page asks the publisher to check the setting, not to change it".
Page (S419.html:105) says 確認してください and nothing about changing. The "not to change it" half comes from the sibling: `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md:50` — "The request is to make the setting, not to check one: the deletion page S419 asks the publisher to check whether that status is configured, S420 asks for it to be set." So the negative half is a cross-page inference stated as an [S419] fact.
Fix: `The verb is 確認してください, please confirm: [S419] asks the publisher to check whether that setting exists. The request to make the setting is the sibling page's (S420, `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md`); [INFERENCE] the two pages divide check from set, and [S419] does not say the setting must not be changed.`

**F5 — MEDIUM — entry L38/L48: three widenings inside the fallback paragraph.**
(a) `:38` — "エラーページのHTMLの head (the tag belongs in the error page's own head, not in the page that used to exist at the URL)". S419 never says the deleted URL serves an error page and never excludes it: `表示` has 0 hits in the body and `エラーページ` occurs once, only as the remedy's location (S419.html:106).
Fix: `エラーページのHTMLの head (the tag belongs in the head of the HTML of an error page — the page's object is エラーページ, and it does not say which URL serves it) [INFERENCE]`.
(b) `:38` — "[INFERENCE] `noindex` and `name="robots"` are the lane's candidate values, not the page's words." `noindex` is absent (0 hits), but `name="robots"` is on the page: `<meta name="robots" content="index,follow,noarchive,noodp" />` (S419.html:14).
Fix: `… are the lane's candidate values: the remedy sentence carries neither a tag name nor a value. The page's own head prints name="robots" with the value index,follow,noarchive,noodp (S419.html:14 — described in prose, not quoted: the line holds a raw double quote), which is the operator's directive for this page, not the remedy's value.`
(c) `:48` — "The meta tag is a page-level head setting". Page-level versus site-level is the lane's classification, not the page's.
Fix: prefix `[INFERENCE]`.

**F6 — MEDIUM — entries L44/L46/L48/L52/L54/L55: page-silence negatives carry no sweep.**
Attacks: `:44` "states no rate effect and no trigger", `:46` "names no block and no budget", `:48` "names no link attribute", `:52` "No tag name, content value, attribute or syntax", `:54` "Nothing about how long … or when it stops", `:55` "Nothing about a URL that never existed".
Fix — one sentence at the end of §Quote classes: `Page-silence sweeps (2026-10-25): `python3 -B .ufo/waves/round-56/span_tools.py window S419 | grep -c -E 'noindex|robots|リダイレクト|canonical|レート|頻度|期間|削除ツール|ブロック|予算'` -> 0; the same window against `アプリケーション|設定ファイル|\.htaccess` -> 0; `grep -o -F '表示' .ufo/waves/round-56/sources/S419.html | wc -l` -> 0.`

**F7 — LOW — entries L8 and L60: counts without their commands.**
Attacks: `:8` "in three sentences"; `:60` "Four spans also occur on the sibling S420 body", "occurs once in that body", "at most 25 units".
Fix: name the instruments — `python3 -B .ufo/waves/round-56/span_tools.py window S419 | grep -o '。' | wc -l` -> 3; `python3 -B .ufo/waves/round-56/span_tools.py check S419 '<span>'` prints `count_in_page=1, in_content=True` for all twelve spans and `in_other_adopted_body=True` for exactly the four named (run 2026-10-25).

**F8 — LOW — entry L60: the stated unit convention is not the counter's, and the 40-character ceiling is unnamed (r54: "report the exact counting convention and the gate's accepted range").**
Attacks: `:60` — "(one unit per CJK character, one per non-CJK whitespace token)".
Evidence: `c56_quote_truth.py:97,160-162` counts CJK punctuation as 0 units (`CJK_RE` covers kana/kanji ranges only, not 、。「」); span `また、このような設定ができない場合には、` is 18 units by `units()` and 20 by the entry's wording. No ceiling is breached — the twelve spans are 9–23 units and at most 37 characters — the wording is what is inexact.
Fix: `and is at most 25 units under the counter's units() (`c56_quote_truth.py:160-162`: one unit per CJK character in the counter's ranges — CJK punctuation such as 、。「」 costs 0 — and one per non-CJK whitespace token), and at most 37 characters against the counter's 40-character ceiling.`

**F9 — LOW — entry L40 restates an existing lane entry.**
Attacks: `:40` — "a site that cannot place robots.txt is told to set index-registration refusal with a meta tag, and that page names no value either".
Existing line: `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md:106` — "(rendered: with a meta tag, set refusal of registration in the index.) The page names no tag value and no scope for that substitute [S372]." Only the delta is new.
Fix: `S372's page names the same substitute for a site that cannot place robots.txt and names no value (`corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` §What a site without root write access is told). [S419] adds only the location — the error page's head — and still no value.`

**F10 — LOW — entry L46: a check is called a remedy.**
Attacks: `:46` — "its two remedies are a response status and a head meta tag". The page's first instruction is 確認してください (a check, S419.html:105), the same defect as F4.
Fix: "its two instructions are a check of the 404 setting and a head meta tag".

## OMISSIONS

**O1 — the page's own summary drops the modal; the entry does not note it.** `<meta name="description" content="このページでは、クローラーが削除したウェブページへの巡回を続けてしまう原因と対応方法について説明しています。" />` (S419.html:13) states the continuation with no 可能性 and frames the page as 原因 and 対応方法. That is the likely source of the flat reading in F1/F3 and in the registry row, and a publisher who compares entry with page otherwise meets an unexplained contradiction. Add after L21: `The page's own description (S419.html:13 — page chrome, not article text) states the continuation without the 可能性 the body carries, and frames the page as 原因 and 対応方法; the hedge in this entry is the body's, not the page's summary. [S419]`

**O2 — the page never says what the deleted URL answers with.** `表示` has 0 hits; `エラーページ` appears once, only as the meta tag's location (S419.html:106). S420 is the page that names `エラーページを表示する設定` (S420.html:104). A publisher following the fallback needs that gap, because it is why "the error page's head" has no stated home here. Add to §What this entry does not establish: `- Nothing about what the deleted URL answers with: [S419] names エラーページ only as the meta tag's location and states no response body; the display setting is the sibling page's (S420).`

## VERDICT PER CRITERION

- **r53 source id resolves in this lane's registry — PASS.** S419 row `corpus/SOURCES.md:165`; S286/S273/S274/S372/S374/S050/S135 registered at `:151/:149/:150/:158/:154/:58/:143`.
- **r53 locator points to the section containing its quote — PASS.** Heading `削除したウェブページが巡回され続ける` at S419.html:100; all twelve spans report `in_content=True`.
- **r54 a translation preserves a material source qualifier — FAIL.** F1 and F3 drop 可能性; F4/F10 turn a check into a remedy.
- **r54 CJK quote length names its unit and the accepted range — PARTIAL.** F8: convention stated but not the counter's; 40-character ceiling unnamed (max span 37 chars).
- **r55 quotes ≤25 units, raw substring, inside the content block, ≥3 page-unique — PASS.** Twelve spans, 9–23 units by `units()`, ≤37 chars, all raw substrings, `count_in_page=1`, eight page-unique.
- **r55 an entry lands with its index row — PASS.** `corpus/README.md:71`; the row itself names the qualifier the H1 drops ("possibility and cannot-be-configured qualifiers").
- **r56 page-unique means unique across every retained body — PASS.** Exactly the four named spans are shared with S420 and no others (`check` `in_other_adopted_body`).
- **r56 a staged candidate is re-derived, not renamed — PASS.** No soft-404 term; the file is `yahoo-japan-deleted-url-recrawl`.
- **r56 a quote is not taken from a raw-double-quote line — PASS.** No entry span comes from S419.html:14; F5(b) keeps that line in prose.
- **Negative claim carries its sweep — FAIL.** F2, F6. No QUALITY.md line owns this rule (nearest is Q14, absence-annotation content, a different subject); `.ufo/waves/round-56/w1/ScoutQuality.md:63` records the gap.
- **Count carries its command — FAIL.** F7. Same gap (ScoutQuality GAPS 1).
- **C2 mechanical — PASS but blind.** `8/8 met=True` at `a450e43` in my clone; the counter sees none of F1–F9.

Impacted axes: C2 (freshness) — this entry is one of the three C2 rows and the published artifact; every fix above is prose, so no counter tally changes. C1 unaffected. Smallest safe correction: F1 (one heading line), F2 (one bullet), F6 (one sweep sentence); F3/F4/F5/F8/F9/F10 are single-sentence edits. L1-owned duplicate authority: `corpus/SOURCES.md:165` states "**A deleted URL answered with 200 OK stays in the crawl**" and "a 200 OK on a removed page leaves it crawled" — the same flat modal as F1; correcting that cell means re-running C7's validated append.

Divergence with the sibling seat (`.ufo/waves/round-56/w2/ReviewerEntryDeleted.md`, verdict line 29): it independently found F2 and F5(b) — same two defects — and reads L38's "not in the page that used to exist at the URL" as a correct subject statement (F5(a) here). Its qualifier pass starts at line 16, so the heading (F1) and L44 (F3) were not tested against 可能性; those two are the findings it does not share.

VERDICT: mechanically quote-true (C2 8/8) but the entry drops the page's 可能性 in its heading (L6) and at L44, and its L53 negative claim contradicts the page's own sentence — fix F1, F2, F3, F6 before publication; F4/F5/F7/F8/F9/F10 are precision and hygiene edits.
