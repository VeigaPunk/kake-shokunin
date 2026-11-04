source: S367 — https://info-search.yahoo.co.jp/archives/002852.php — § リンク先のウェブページの巡回制限　― ウェブページ内やサーバーでの設定 → メタタグを使用する方法 / サーバーで設定する方法 (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002852.php' | grep -F -c 'サーバーの設定で指定する方法があります'` -> 1 (curl arm 1 and the same grep against the retained round-56 body 1, 2026-10-25)
ground: per-engine crawl hygiene — how a page refuses the crawl of the link targets it contains, from its own head or from the server that hosts it, and what that refusal leaves of the page's own indexing

# Refusing a page's link targets is a decision the page and the server can each carry

The lane holds the per-link attribute (`yahoo-japan-rel-nofollow-semantics.md`, S374) and the refusal file at the site root
(`yahoo-japan-robots-txt-refusal-rules.md`, S372). This page adds two surfaces the lane did not hold — a meta tag in the
page's own head and a directive on the server hosting it. For the meta tag it states that the crawl of the link-target pages
inside this page is refused while the page's own registration in the index is permitted [S367]; the crawl of the page itself is
not its subject. Nothing below was served to a crawler. The page prints 更新日 2010年11月24日; this entry reports the retained body
fetched 2026-10-25 and makes no claim that the live documentation still reads the same.

## The framing: three specifying methods

The opening paragraph names the subject, then the routes [S367], quoted raw:

> "リンク先ウェブページの巡回制限は、"
> "HTMLのメタタグで指定する方法と、"
> "サーバーの設定で指定する方法があります"

(rendered: as for the crawl restriction of link-target web pages, there is a method specified with an HTML meta tag and a
method specified in the server's settings). のほかに (besides) attaches to the attribute phrase the quote skips, so the attribute is
the route to which the two named here are added, and 方法があります states that the methods exist without attaching an effect to
either named method. That attribute route is named in the same sentence and links to another page of this operator [S367], quoted raw:

> "rel=&quot;nofollow&quot;属性を使った指定方法"

(rendered: the specifying method that uses the `rel=nofollow` attribute). The link goes to archives/002851.php, held here as
S374; this page states no semantics for the attribute. The page gives a sub-heading and a setting for the meta-tag and
server routes only: the attribute route is a pointer, with no sub-heading and no example of its own. The page files the attribute
as one of its three 巡回制限 routes [S367]; the attribute's own entry (`yahoo-japan-rel-nofollow-semantics.md`, S374) records an
endorsement reading and not a crawl refusal, so this entry draws no rule from the filing.

## The meta tag: the page's head, two values

The sub-heading and its instruction [S367], quoted raw:

> "メタタグを使用する方法"
> "HTMLの&lt;head&gt;内に次のような記述をします"

(rendered: the method that uses a meta tag; the following kind of description is written inside the HTML `<head>` — the placement
is the page's own head, and no other placement is named). The example printed under it (rendered; the raw body carries `&lt;` and `&quot;`):

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
example's meaning [S367]. So the example means that the page's own registration in the index is permitted while the crawl of its
link targets is refused.

## The second value: refusing the page with its targets

The case the page states next, quoted raw [S367]:

> "「リンク先ウェブページの巡回を拒否し、"
> "ウェブページ自身のインデックスへの登録も拒否する」"
> "という場合には、"
> "次のように記述します"

(rendered: in the case of refusing the crawl of the link-target web pages and also refusing the registration of the web page
itself in the index, write as follows). も attaches the second refusal to the first inside that case: the tag refuses both; the
page offers the two examples as separate cases (という場合には). The example printed under it (rendered, as above):

```html
<meta name="robots" content="noindex,nofollow">
```

The two values differ in one position, and the page's two glosses separate them: the first permits the page's own
registration, the second refuses it together with the targets [S367]. The article gives two values and no third; the page's own
head, outside the article block, carries a robots meta tag with the value `index,follow,noarchive,noodp` as that page's own setting,
for which the article states no rule (`grep -o -F 'noarchive,noodp' .ufo/waves/round-56/sources/S367.html | wc -l`
-> 1). No example names a single crawler in the tag's name value, and the article gives no rule for combining values.

## The server route: one token, one value, no gloss

The sub-heading, its instruction and its example [S367], quoted raw:

> "サーバーで設定する方法"
> "ウェブページをホスティングしているサーバーで、"
> "次のようなディレクティブ設定をします"

(rendered: the method of setting it on the server; on the server that is hosting the web page, make the following kind of
directive setting). The example printed under it (the page prints the token in upper case, the two meta values in lower case, and states no case rule):

```
X-Robots-Tag: NOFOLLOW
```

The body gives the token and that one value and stops: no gloss sentence, no second value, no statement of which request the
setting belongs to [S367]. The document's own description in its head, outside the article block and so not quoted here,
calls the route the setting of the server's HTTP header [S367]; [INFERENCE] the token is delivered in the HTTP response, and
[INFERENCE] the value is read as refusing the crawl of the page's link targets because the sub-heading sits under a page
titled for that restriction — the body spells out neither, unlike the two meta-tag glosses.

## What this entry does not establish

- The page names one further route, as a pointer to archives/002851.php (held as S374), and states nothing about that route's
  scope or its application to one link URL; the article body gives no per-URL route for the meta tag or the server directive.
  個別リンクURL occurs once, in the site boilerplate outside the article block, as the label of the page's own URL field. The page's
  head description, outside the article block, speaks of methods that restrict the crawl of 特定の (specific) link-target pages;
  this entry does not read that as a per-URL syntax [INFERENCE].
- It states no status code: no 200 and no 404, no fetch failure, no redirect [S367]. The lane's nearest status ground is a Google
  page on crawl errors (`crawl-error-status-table.md`, S286), which admits one scaling-back sentence and no status code; this page
  states none either, so no contrast is drawn. The same operator's pages on a deleted URL and on a non-existent URL do state
  `HTTP 404 Not Found` (`yahoo-japan-deleted-url-recrawl.md`, S419; `yahoo-japan-nonexistent-url-recrawl.md`, S420).
- It states no possibility hedge, no conditional for a server that cannot be configured, and no fallback. The refusal-file
  entry (`yahoo-japan-robots-txt-refusal-rules.md`, S372) records this operator telling a site without root write access to
  use a meta tag for index registration refusal; this page states no such fallback of its own [S367].
- It states nothing about a robots.txt file, a crawler name in the tag, wildcards, or precedence when a page carries more
  than one route, and nothing about the attribute's own meaning: `yahoo-japan-rel-nofollow-semantics.md` (S374) records that
  the tagged URL is still used to find new pages and that the attribute is not weighed when the result order is decided
  [S374].

## Quote classes

Each block-quoted span is a raw substring of `.ufo/waves/round-56/sources/S367.html` (sha256 `0188de9d…`, 8051 bytes, HTTP 200 in
`.ufo/waves/round-56/sources/receipts.json`), occurs once, sits inside the article block, and is at most 25 units under the counter's
`units()` (`.ufo/waves/round-56/c56_quote_truth.py`: one unit per CJK character in the kana/kanji ranges, so CJK punctuation costs 0,
plus one per non-CJK whitespace token) and at most 40 characters (`python3 -B .ufo/waves/round-56/span_tools.py check S367 '<span>'`
prints `count_in_page=1`, `in_content=True`, `in_other_adopted_body=False` for each of the 17 spans; the longest is 24 units,
2026-10-25). The code blocks are renderings with the entities decoded, not quotations. Renderings are unquoted and keep the
qualifiers のほかに, 方法があります, このウェブページ内にある, このウェブページ自身は, も, という場合には. The sentence a round-53 gate quote
carried as one 31-unit span (`corpus/lessons/round-55.md` line 15) is quoted here in pieces. The heading in the `source:` line is
the page's own `<h2>` text, whose space before ― is U+3000 (the registry cell for S367 keeps an ASCII space and stays byte-equal to its
base row).

Sweeps over the article text (`python3 -B .ufo/waves/round-56/span_tools.py window S367 | grep -o -F <term> | wc -l`, 2026-10-25):
robots.txt 0, ワイルドカード 0, 優先 0, ステータス 0, 404 0, 200 0, リダイレクト 0, エラー 0, できません 0, できない 0, 場合 1; on the raw body
`grep -o -F 'name="robots"' .ufo/waves/round-56/sources/S367.html | wc -l` -> 3 (the page's head and the two meta examples; no crawler name
appears as a name value) and `個別リンクURL` -> 1.

Scope note: a claim about what the operator's documentation states on one page of its info centre; no setting was served to any crawler for this lane, no crawl was observed, and no directive was tested.
