source: S367 — https://info-search.yahoo.co.jp/archives/002852.php — § リンク先のウェブページの巡回制限 ― ウェブページ内やサーバーでの設定 → メタタグを使用する方法 / サーバーで設定する方法 (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002852.php' | grep -F -c 'サーバーの設定で指定する方法があります'` -> 1 (curl arm 1 and the same grep against the retained round-56 body 1, 2026-10-25)
ground: per-engine crawl hygiene — how a page refuses the crawl of the link targets it contains, from its own head or from the server that hosts it, and what that refusal leaves of the page's own indexing

# Refusing a page's link targets is a decision the page and the server can each carry

The lane holds the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`, S374) and the refusal file at the site root
(`yahoo-japan-robots-txt-refusal-rules.md`, S372). This page states a third surface: a page can refuse the crawl of the link
targets it contains without refusing itself [S367]. Nothing below was served to a crawler.

## The framing: three specifying methods

The opening paragraph names the subject, then the routes [S367], quoted raw:

> "リンク先ウェブページの巡回制限は、"
> "HTMLのメタタグで指定する方法と、"
> "サーバーの設定で指定する方法があります"

(rendered: as for the crawl restriction of link-target web pages, there is a method specified with an HTML meta tag and a
method specified in the server's settings). ほかに (besides) opens the sentence, so a further route precedes these two, and
方法があります states that the methods exist without attaching an effect to any crawler. That route is named in the same sentence
and links to another page of this operator [S367], quoted raw:

> "rel=&quot;nofollow&quot;属性を使った指定方法"

(rendered: the specifying method that uses the `rel=nofollow` attribute). The link goes to archives/002851.php, held here as
S374; this page states no semantics for the attribute. The page gives a sub-heading and a setting for the meta-tag and
server routes only: the attribute route is a pointer, with no sub-heading and no example of its own.

## The meta tag: the page's head, two values

The sub-heading and its instruction [S367], quoted raw:

> "メタタグを使用する方法"
> "HTMLの&lt;head&gt;内に次のような記述をします"

(rendered: the method that uses a meta tag; write the following kind of description inside the HTML `<head>` — the placement
is the page's own head, and no other placement is named). The example printed under it:

```html
<meta name="robots" content="index,nofollow">
```

The page then glosses that example, quoted raw in pieces because the sentence runs past the 25-unit ceiling as one span
[S367]:

> "このウェブページ内にあるリンク先ウェブページの"
> "巡回は拒否するが、"
> "このウェブページ自身は"
> "インデックスへの登録を許可する"

(rendered: the crawl of the link-target web pages that are inside this web page is refused, but this web page itself is
permitted registration in the index). このウェブページ内にある scopes the refusal to the page's own link set, and the subject of the
first half is the crawl of the targets, not of the page. 上記の例は in front of the gloss and という意味を持ちます after it mark it as the
example's meaning [S367]. So `index,nofollow` leaves the page's own registration permitted while refusing the crawl of its
link targets.

## The second value: refusing the page with its targets

The case the page states next, quoted raw [S367]:

> "「リンク先ウェブページの巡回を拒否し、"
> "ウェブページ自身のインデックスへの登録も拒否する」"
> "という場合には、"
> "次のように記述します"

(rendered: where the meaning is that it refuses the crawl of the link-target web pages and also refuses the registration of
the web page itself in the index, write as follows). も carries the addition, so the second refusal is added to the first,
not offered as an alternative. The example printed under it:

```html
<meta name="robots" content="noindex,nofollow">
```

The two values differ in one position, and the page's two glosses separate them: the first permits the page's own
registration, the second refuses it together with the targets [S367]. No third value, no example naming a single crawler in
the tag's name value, and no rule for combining values.

## The server route: one token, one value, no gloss

The sub-heading, its instruction and its example [S367], quoted raw:

> "サーバーで設定する方法"
> "ウェブページをホスティングしているサーバーで、"
> "次のようなディレクティブ設定をします"

(rendered: the method of setting it on the server; on the server that is hosting the web page, make the following kind of
directive setting).

```
X-Robots-Tag: NOFOLLOW
```

The body gives the token and that one value and stops: no gloss sentence, no second value, no statement of which request the
setting belongs to [S367]. The document's own description in its head, outside the article block and so not quoted here,
calls the route the setting of the server's HTTP header [S367]; [INFERENCE] the token is delivered in the HTTP response, and
[INFERENCE] the value is read as refusing the crawl of the page's link targets because the sub-heading sits under a page
titled for that restriction — the body spells out neither, unlike the two meta-tag glosses.

## What this entry does not establish

- The page does not state that the same refusal can be applied to an individual link URL: its only per-link route is the
  pointer to archives/002851.php [S367]. 個別リンクURL occurs once, in the site boilerplate outside the article block, as the
  label of the page's own URL field.
- It states no status code: no 200 and no 404, no fetch failure, no redirect [S367]. The lane's status ground is a Google
  page on crawl errors (`crawl-error-status-table.md`, S286); this page states none, so the two do not meet and no contrast
  is drawn.
- It states no possibility hedge, no conditional for a server that cannot be configured, and no fallback. The refusal-file
  entry (`yahoo-japan-robots-txt-refusal-rules.md`, S372) records this operator telling a site without root write access to
  use a meta tag for index registration refusal; this page states no such fallback of its own [S367].
- It states nothing about a robots.txt file, a crawler name in the tag, wildcards, or precedence when a page carries more
  than one route, and nothing about the attribute's own meaning: `yahoo-japan-rel-nofollow-semantics.md` (S374) records that
  the tagged URL is still used to find new pages and that the attribute is not weighed when the result order is decided
  [S374, S367].

## Quote classes

Each quotation is a raw substring of `.ufo/waves/round-56/sources/S367.html` (sha256 `0188de9d…`, 8051 bytes, HTTP 200 in
`receipts.json`), occurs once, sits inside the article block, and is at most 25 units (one per CJK character, one per
non-CJK whitespace token). Renderings are unquoted and keep the qualifiers ほかに, 方法があります, このウェブページ内にある, このウェブページ自身は, も,
という場合には. The sentence a round-53 gate quote carried as one 31-unit span is quoted here in pieces.

Scope note: a claim about what the operator's documentation states on one page of its info centre; no setting was served to any crawler for this lane, no crawl was observed, and no directive was tested.
