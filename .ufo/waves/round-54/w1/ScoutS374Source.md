# ScoutS374Source — S374 retained-body re-open

Scope: re-open `.ufo/waves/round-52/sources/S374.html` locally; verify exact
quote/title and whether the quoted clause retains a crawl qualifier.
Evidence is the round-52 retained body on disk — **no network request was
issued this round** (consistent with `.ufo/waves/round-54/source-reopen.txt`,
which declares "local retained-body re-open; no network request").

## Retained-body identity (verified against receipts/baselines)

- Path: `.ufo/waves/round-52/sources/S374.html` — 8153 bytes, mtime
  2026-10-25 07:19 local.
- sha256 = `3ad358bdbe7a74798df151c282e4b57af7475686dc405b3f8bad08f68881aecb`
  — matches `.ufo/waves/round-52/sources/receipts.json` (S374: url
  `https://info-search.yahoo.co.jp/archives/002851.php`, httpStatus 200,
  bytes 8153, fetchedAt 2026-10-25T10:19:41+00:00) and
  `.ufo/waves/round-52/baselines.json`. The fetched bytes are intact and
  byte-identical to the round-52 capture; my reads did not alter the file.

## Exact quote — retained-body verdict

Gate quote `このリンク先のウェブページの巡回を推奨していない`:

- Occurs **exactly once** in the retained body, at byte offset 3157 (line
  104), inside the article's first content paragraph
  (`<div class="asset-body"><p>…`), i.e. it is body text of the source, not
  a navigation chrome artifact.
- The quote is a **clause** of a longer sentence. The full source sentence
  reads (entities decoded):
  「`<a>`タグに属性rel="nofollow"が指定された場合、このリンク先のウェブページの
  巡回を推奨していない、あるいは信頼できるリンクではないとサイト管理者
  （ウェブマスターやブログのオーナー）が考えているとみなします。」

## Crawl qualifier — retained

The quoted clause **does retain the crawl qualifier**, verbatim. The literal
Japanese is 「このリンク先のウェブページの**巡回**を推奨していない」 — "does not
recommend the **crawling (巡回)** of this link-target web page." The object of
「推奨していない」 ("does not recommend") is specifically the *crawl* of the
linked page, not the page/link itself in the abstract. 「巡回」 is the
site's crawl vocabulary (the whole page category is 「クローラー」).

Corroborating source-level signals, all in retained bytes:

- `<title>` (line 33): `リンク先のウェブページの巡回制限　― rel属性の利用 -
  インフォセンター - Yahoo!検索` — "Restricting the crawl of linked web
  pages — using the rel attribute."
- `<h2>` (line 100) repeats `リンク先のウェブページの巡回制限　― rel属性の利用`;
  the phrase occurs 4× total in the body (title, h2, two sidebar entries).
- `<p class="update">` (line 101): 更新日 2010年11月24日 — matches the
  registry anchor cell `§ rel属性の利用 (更新日 2010年11月24日)`.
- `<meta name="description">` (line 13) frames the page as being about
  「特定のリンク先ウェブページの巡回を制限する方法」 — methods to restrict
  crawling of specific link targets.

## Companion sentence (same paragraph)

The next sentence, also retained verbatim: rel="nofollow" URLs 「新しい
ウェブページを見つけるために利用されますが、検索結果の表示順序を決める要素として
は考慮されません」 — used to discover new pages, not weighed in ranking.
This is what the registry row's "still used to find new pages and is not
weighed when the results are ordered" cell rests on.

## Bearing on the round-53 quality ruling

The round-53 closure ruled quality harmed because the entry's gloss
(`corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` lines 13–14:
"rendered: the site owner is taken to consider the link target's page one it
does not recommend, or a link it cannot vouch for") dropped the crawl
qualifier. Retained-body evidence **confirms the ruling**: 「巡回を」 sits
inside the quoted clause itself, so the dropped qualifier is a source-fidelity
defect, not an interpretive choice. Note the registry row cell for S374 does
hedge elsewhere ("the attribute speaks to endorsement and ordering, not to
whether the target is fetched"), so the harm is confined to the endorsement
gloss losing 「巡回」.

The entry's round-54 correction block (lines 52–60) renders the phrase as
"not recommend the **crawling** of the link target's web page" and cites the
source title リンク先のウェブページの巡回制限 — this reading is supported by
the retained bytes above.

## Retained-body vs fresh-request boundary

- All findings derive from the 8153-byte retained file whose sha256 pins it
  to the round-52 fetch; nothing here reflects the source's live state on
  2026-10-25.
- The page's own canonical field (line 121 input) is
  `https://info-search.yahoo.co.jp/archives/002851.php`; whether the live URL
  still serves these bytes is **unevaluated** by this scout (no fetch
  performed or permitted under the read-only wave).

## Install/tooling log

No tools installed or updated; pacman untouched per wave rules.

Report: .ufo/waves/round-54/w1/ScoutS374Source.md
