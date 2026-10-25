# ReviewerStaged

Fidelity review of the three round-56 staged candidates against the retained bodies
(`sources/S367.html` = staged `yahoo-japan-link-target-crawl-restriction.md`,
`S419.html` = `yahoo-japan-deleted-url-recrawl.md`,
`S420.html` = `yahoo-japan-soft-404-recrawl.md`, landing as `yahoo-japan-nonexistent-url-recrawl`).
Quotes below were machine-checked with `span_tools.py check`: all staged quotes are raw,
content-unique substrings; units are the round's CJK/token count. Staged headers still carry
pre-renumber ids (S375→S419, S376→S420) and fetched/verified dates 2026-10-24 vs receipts
2026-10-25; both are landing-edit items, not defects.

DEFECTS:

S367 — `yahoo-japan-link-target-crawl-restriction.md` (staged S367)
- staged l.24-25 "the operator also states that the same refusal can be applied to an
  individual link URL rather than to the page's whole link set" — mechanism asserted from a
  sibling page. The only `個別リンクURL` on S367 is the footer permalink widget (body l.125-126,
  the article's own URL), and the only per-link-adjacent text is the bare *link* to
  archives/002851.php (`rel="nofollow"属性を使った指定方法`, body l.104). Fix: cut the sentence,
  or re-ground on the rel-attribute method as "named here, described on its own page".
- staged l.29-31 "the choice between them changes whether the page itself stays in the index.
  A blanket `noindex` on such a page is the wrong instrument, and the operator's own page says
  so." — inference presented as the operator's words (attribution defect) + scope widened. The
  index/noindex choice exists only inside the meta-tag route (body l.110 `という意味を持ちます`
  glosses index,nofollow; l.111-113 show noindex,nofollow). The page never evaluates noindex
  and says nothing about the choice between routes affecting indexing. Fix: "Within the
  meta-tag route the operator spells the choice out: `index,nofollow` permits the page's own
  index registration while refusing link-target crawl; `noindex,nofollow` refuses both."
  Drop "the operator's own page says so" and the "stays in the index" phrasing (page: 登録を許可,
  permit registration).
- staged l.28-29 "places it cannot vouch for" — invented motive; the page states no purpose.
  Fix: drop or mark [INFERENCE].
- Minor gloss, safe to keep or tighten: l.16 "the server can carry a header" — page says
  `ディレクティブ設定` (directive configuration); the directive happens to be a header. Optionally
  render "a server directive". Quote `"X-Robots-Tag: NOFOLLOW"` (l.18) is 2 units, raw, unique —
  reuse as-is.

S419 — `yahoo-japan-deleted-url-recrawl.md` (staged S375 → row S419)
- Quote at staged l.12 (46 units, over the 25-unit ceiling). Page: body l.104
  `削除したURLのウェブページにアクセスしたときに「HTTP 200 OK」のステータスを返すようにサーバーが設定されている場合、
  クローラーは削除されたウェブページと認識できず、そのウェブページを巡回し続ける可能性があります。`
  Fix (checked, 23u, raw, unique): `"そのウェブページを巡回し続ける可能性があります"`.
  If the cause half is wanted, `「HTTP 200 OK」のステータスを返すようにサーバーが設定されている場合` also fits;
  a one-quote-per-entry landing should prefer the consequence half that carries the hedge.
- staged l.14 "the crawler has no way to tell the page is gone, so it keeps crawling it" and
  l.10 "the crawler keeps coming back to it" — dropped qualifier / modal changed. Page hedges:
  `巡回し続ける可能性があります` = "may keep crawling". Fix: "...so it *may* keep crawling it".
  Also l.14 "a success status" widens the page's specific `「HTTP 200 OK」` trigger — fix to
  "an HTTP 200 OK status".
- staged l.15-17 "the operator's remedy is to answer with a not-found status instead" — small
  shift: the page instructs to *check that* the server returns 404
  (`...設定されているかを確認してください`, body l.105). Fix: "the operator's remedy is to confirm
  the server answers HTTP 404 Not Found".
- staged l.19-21 "a deletion is only a deletion if the server stops answering with success …
  the crawl cost of a removed page is still being paid" — untagged inference; "crawl
  cost"/budget absent from the page, and "is still being crawled" states as fact what the page
  hedges. Fix: "A soft-deleted URL — one still served with HTTP 200 OK — may still be crawled
  [INFERENCE]", or cut to the page's sentence.
- Gloss, safe to keep: the `head:` "crawl budget" wording is lane-side prose, not a page claim;
  headline "cannot delete" is loose for `認識できず` (cannot recognize) — tighten to "cannot
  recognize" if touching the line anyway.

S420 — `yahoo-japan-soft-404-recrawl.md` (staged S376 → row S420)
- Quote at staged l.14 (29 units, over ceiling). Page: body l.105
  `サーバーが「HTTP 404 Not Found」のステータスを返すように設定を行ってください。`
  Fix (checked, 25u exactly, raw, unique):
  `"「HTTP 404 Not Found」のステータスを返すように設定を行ってください"`.
- staged l.9-10 "a typo in a link, a route that was renamed, a campaign page that was retired"
  — widened scope: the page names no causes (`存在しないウェブページを表示しようとしたときに`). Worse,
  a renamed route / retired page existed before — that is S419's deleted-URL case,
  contradicting "never existed". Fix: cut the list.
- staged l.20 "the crawl loop follows what the server answers, not what the site intends" —
  inflated generalization presented as the operator's statement ("the operator's statement of
  one rule", l.19). The page states only its own case: `クローラーはエラーページとみなさず、巡回を続けます`
  (body l.104). Fix: drop the aphorism or tag it: "Read together the two entries suggest
  [INFERENCE] that the status the server returns decides whether the crawl continues."
- staged l.21-23 "a styled error page … converts every mistake into a permanent crawl target"
  — "styled", "every", "permanent" absent; the page says `巡回を続けます` (continues crawling),
  not permanence. Fix: "an error page served with HTTP 200 OK is crawled as content, not read
  as an error". "one for a URL never built" (l.23) likewise narrows to invented causes.
- staged l.9 "the sibling of the deleted-URL case" — cross-page synthesis the page never makes
  (linked only via the generic category sidebar); editorial, keep only as [INFERENCE] or cut.
- Safe to keep: l.11-12 rendering of `エラーページとみなさず、巡回を続けます` (unhedged — the hedge
  asymmetry with S419 is real and must not be copied across), the 404 remedy, and the l.16-17
  fallback (`インデックス拒否` here vs S419's `インデックスへの登録拒否` — the staged rendering
  "index-refusal meta tag" covers both correctly).

SAFE-TO-REUSE LINES:
- S367: l.15-16 three-route enumeration (attribute / meta tag / server directive — page body
  l.104, "three" is implicit but enumerated); l.18 quote `X-Robots-Tag: NOFOLLOW` (2u); l.20-24
  meta-tag gloss pair (index,nofollow vs noindex,nofollow — body l.110-113); l.33-34 scope note.
- S419: l.9-10 symptom framing (title `削除したウェブページが巡回され続ける`), minus the hedge fix;
  l.16-17 fallback meta tag (`メタタグを使ったインデックスへの登録拒否`, body l.106); l.23-24 scope
  note; the `recheck` grep — the 46-unit string still matches the retained body exactly.
- S420: l.11-12 (mechanism sentence: not read as an error page, keeps crawling); l.16-17
  fallback meta tag (body l.105); l.25-26 scope note; the `recheck` grep still matches the
  retained body.
- All three: `ground:`/title headers are lane prose (acceptable), but per-round form the staged
  source ids and 2026-10-24 dates need the landing rewrite (S375→S419, S376→S420, 2026-10-25).

VERDICT PER ENTRY:
- yahoo-japan-link-target-crawl-restriction (S367): REUSE WITH EDITS — cut the per-link-URL
  sentence and the "wrong instrument / the operator says so" attribution; scope the index
  choice to the meta-tag route; quote already compliant.
- yahoo-japan-deleted-url-recrawl (S375→S419): REUSE WITH EDITS — re-cut quote to
  `"そのウェブページを巡回し続ける可能性があります"` (23u) and restore the `可能性` hedge plus the
  HTTP-200-OK-specific trigger; tag or drop the crawl-cost inference.
- yahoo-japan-soft-404-recrawl (S376→S420): REUSE WITH EDITS — re-cut quote to the 25u 404
  directive; delete the invented-causes list (internally contradicts "never existed") and the
  crawl-loop aphorism or mark it [INFERENCE]; trim "styled"/"permanent".

VERDICT: All three staged entries are salvageable with edits, not re-drafts: 3 defects each
clustered on quotes over the 25-unit ceiling (S419 46u, S420 29u), dropped `可能性` hedges
(S419), attribution/scope inflation (S367 per-link + operator-says-so; S420 causes list +
crawl-loop aphorism); checked replacement spans supplied above.
