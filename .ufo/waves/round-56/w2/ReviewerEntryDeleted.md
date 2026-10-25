# ReviewerEntryDeleted

Target: `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` vs retained `.ufo/waves/round-56/sources/S419.html` (7428 bytes, sha256 6172d5d1…, httpStatus 200 in `receipts.json`). File sha256 identical at attacked rev a450e43e and worktree HEAD 7ad7db51 — findings apply at the attacked rev. Every quoted span re-verified with `span_tools.py check S419`.

DEFECTS:

1. Line 38 `[INFERENCE]` — "`noindex` and `name="robots"` are the lane's candidate values, not the page's words." Page text (raw body, line 14): `<meta name="robots" content="index,follow,noarchive,noodp" />`. The literal string `name="robots"` occurs verbatim once in the body (`grep -F -c 'name="robots"'` → 1); `noindex` occurs 0. Half the tag's claim is false — `name="robots"` is on the page. The tag's convention (the tagged text is not on the page) fails on the raw-body standard the entry itself applies (entities kept verbatim, counts over the whole file). Fix: drop `name="robots"` from the negation — e.g. "the remedy names no tag name or value; `noindex` is the lane's candidate value, not the page's word" — or rescope the sentence to "the remedy text" (the remedy's own words name no value), because as written it asserts page-level absence that does not hold.

2. Line 53 — "No statement that the 404 is to come from the server configuration or from the application". Page text (quoted on the entry's own line 26–27): `サーバーが「HTTP 404 Not Found」のステータスを返すように設定されているかを確認してください` — the page asks to confirm whether the server is so configured, making the 404 a server setting, the same construction it uses for the 200 (`サーバーが設定されている場合`). The bullet negates what its own quote implies: the page does state the check is on the server's configuration. Fix: drop the negation or split — "the page asks only whether the server is configured to return 404; whether that configuration sits in the server itself or an application behind it is not drawn" (the server/application distinction is the lane's, not the page's).

TAG AUDIT:

- Line 38 `[INFERENCE]` (noindex / name="robots" not the page's words): DISHONEST as written — see defect 1.
- Line 44 `[INFERENCE]` "the page's silence is recorded here, not filled": honest — it marks the recorder's meta-remark, not page text. The untagged sentences before it are accurate: the article (3 sentences, verified via `span_tools.py window S419`) states no rate, trigger, frequency or duration.
- Untagged-claim spot checks, all on-page or on-lane:
  - Line 8 "failure and its two remedies in three sentences": article block is exactly 3 sentences; sentence 1 = the failure, sentence 2 = the 404 check, sentence 3 = the meta-tag fallback.
  - Line 8 grep claim (`grep -n -i -E '200|soft'` on the two sibling files prints only the status-table disclaimer): verified — only `crawl-error-status-table.md:14` matches.
  - Lines 40, 44, 46, 48, 55 sibling attributions verified: S372 entry does tell a site that cannot place robots.txt to set index-registration refusal with a meta tag and names no value (its lines 98–106); S286 "scale back … servers … trouble" (its line 10); S273 spare-fetches/capacity-limit and S274 whole-hostname backoff (its lines 11–13); S374 is the link-level rel-attribute entry; redirect-rewrite-rules.md carries S050/S135; S420 title is 存在しないウェブページが巡回される (002857).
  - Line 60 quote-class claims all verified: each of the 12 quoted spans is a raw substring, count_in_page == 1, in_content true, ≤25 units (9–23u), ≤40 chars (11–37); exactly the four named spans also occur in S420 (each once, none in S367); `&lt;head&gt;` entities stay verbatim.
- Rendering qualifier pass (each surviving Japanese qualifier against the body text): line 16 keeps 設定されている場合 (case), passive, 200 OK; line 21 keeps できず (cannot) and 可能性があります as possibility, and 巡回し続ける as "keeps crawling"; line 29 keeps 確認してください (confirm — not 設定) and 404 Not Found; line 38 keeps また (also), このような設定ができない場合には (where such a setting cannot be made), エラーページのHTMLの head (error page's own head, subject correctly the error page, not the deleted page or a link target), メタタグを使った (by means of a meta tag), and states the remedy names no tag name/value/attribute (remedy text: メタタグを使ったインデックスへの登録拒否の設定を行ってください — no value stated). No ほかに / も qualifier exists on the page; また is the only additive and is rendered. No rendering defect found.

HEADER AUDIT:

- `source:` line 1 — section label 削除したウェブページが巡回され続ける is the page's title (in the body, first line of the article window); URL https://info-search.yahoo.co.jp/archives/002856.php matches receipts.json S419.url; 更新日 2010年11月24日 is verbatim in the body; "fetched 2026-10-25" matches receipts fetchedAt 2026-10-25T22:02:41Z. Pass.
- `recheck` line 3 — live arm RUN: `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002856.php' | grep -F -c 'クローラーは削除されたウェブページと認識できず、'` printed `1` (2026-10-25); same grep on the retained body printed `1`. Count as stated. Pass.
- `ground:` line 4 — accurate: the page is a per-engine (Yahoo! JAPAN) statement about a success status on a deleted URL, the 404 check, and the head meta-tag fallback. Pass.
- Scope note line 62 — consistent with facts: a claim about one operator page; receipts show a fetch only; no delete/serve/crawl was exercised. Pass.

VERDICT: 2 defects — line 38 `[INFERENCE]` asserts `name="robots"` is not the page's word while the literal substring sits in the raw body (S419.html:14), and line 53 negates a statement its own quote implies (the 404 as the server's configuration); all renderings, the remaining tag, quote classes, header lines, scope note and the recheck count verify.
