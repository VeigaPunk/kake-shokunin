source: S374 — https://info-search.yahoo.co.jp/archives/002851.php — § rel属性の利用 (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d
ground: per-engine crawl hygiene — what a link attribute says, and what it does not say, about crawling a link target

# A link attribute is a statement about endorsement, not a crawl refusal

Yahoo! JAPAN's info centre states what its engine reads into `rel=nofollow` on an `<a>` element
[S374], quoted raw from the retained body:

> "このリンク先のウェブページの巡回を推奨していない"

(rendered: the site owner is taken to consider the link target's page one it does not recommend,
or a link it cannot vouch for). The same page then states what still happens to that URL [S374],
quoted raw:

> "検索結果の表示順序を決める要素としては考慮されません"

(rendered: the attribute is not weighed when the result order is decided). The page's own subject
is リンク先のウェブページの巡回制限 — restricting the crawl of a page's *link targets* — which is
why the attribute is one of its three routes and not a separate mechanism [S374].

## Why the lane needs this as a rule rather than trivia

- **The attribute is not a refusal.** A publisher who writes `rel=nofollow` on a link has said
  the target is not endorsed; the lane's robots-refusal ground (S372, S373) and its
  meta/header link-target restriction (S367) are the mechanisms that speak to crawling itself.
  Reading `nofollow` as "do not fetch this URL" is the over-read this row exists to stop.
- **The URL is still used to find new pages.** The page says the tagged URL is used to discover
  new pages; it does not say the target is never fetched. A crawl-log question about a
  `nofollow`-linked URL is therefore not answered by the attribute alone.
- **Ordering and crawling are separate decisions.** The lane's spam-signal and ranking rows say
  nothing about this attribute on any engine other than the one that documents it, and the
  engine that documents it keeps the two decisions apart.

## What this entry does not establish

- It says nothing about Google, Bing or Baidu: it is one operator's page, and the lane has no
  row from another operator stating the same semantics.
- It does not establish how other link-attribute values (`sponsored`, `ugc`) are read by this
  operator; the page's subject is `nofollow`.
- It does not establish any effect on the *source* page's own indexing.
- It does not establish crawl behaviour on any live property; no operator-owned surface was
  fetched this round.

## Quote classes

Both quotations above are exact raw substrings of the retained body
`(S374.html, sha256 3ad358bd…)`: the source text is Japanese, the UTF-8 bytes carry no inline
markup inside either sentence, and the only rendering this entry applies is the English gloss in
parentheses, which is unquoted. The lesson Gate pins the first of the two.
