# ProbeBodyStability

Seat: leaf probe inside round-58 w1. Read-only against the lane; no git/jj mutation, no counter or source edit.
Only files written: this report and `.ufo/waves/round-58/w1/ProbeBodyStability.files/` (two JSON verdicts, three probe scripts, `fetch-sha256.txt`).

Hypothesis under test: the article-block text nodes of `https://ziyuan.baidu.com/college/articleinfo?id=3457` (S423) and
`https://ziyuan.baidu.com/college/articleinfo?id=3028` (S424) are byte-stable across fetches, while only script/cache-token
regions vary.

Method: three fresh fetches per page, 30 s apart (`curl -sSL --compressed -A 'Mozilla/5.0' --max-time 60`), 2026-10-26T23:53:48Z
to 23:54:52Z; extraction reuses the C3 counter's own `content_window()` / `text_segments()` from
`.ufo/waves/round-58/c58_quote_truth.py` (imported, not reimplemented), so the region measured is exactly the region the
C5 span check accepts. Article block = `class="article-info"` to `往期回顾` (S423) / `推荐阅读` (S424), text nodes only.
Scratch `/fast/scratch/hyaku/kake-r58/ProbeBodyStability/` deleted at end; receipts copied to `.files/`.

## FETCHES:

Full-body hashes (all differ; NL-normalised hash equals raw hash in every case, so line endings are not the variance):

| page | variant | bytes | chars | sha256 (full body) |
|---|---|---|---|---|
| S423 | retained | 29007 | 24294 | `8b8aef60bd7e315799e9a97dadfd02a5982f8c7e17b9d4064a6fc3913a0736ec` |
| S423 | fetch 1 | 29007 | 24294 | `85468ec4cee5c02b52b4ec4e440e95599d89e63e6ab2da63a7b23e1ff230e7d3` |
| S423 | fetch 2 | 29007 | 24294 | `a3b2c29718cc42feb3ca77a03972a8a0394e98e6b5c140c6685b9b701fda13b2` |
| S423 | fetch 3 | 29007 | 24294 | `336e01600d3d73a49b2e8e26914e5185577b0f9f315cbb20149a488f10f26966` |
| S424 | retained | 22476 | 19807 | `3ef1275b730230f2cb9c14b28b1c4bd08dc363dc7941b63d06c507fb2729cad1` |
| S424 | fetch 1 | 22336 | 19731 | `1087550ac9cbc11b5c5a7f03b9ffc90cfceadfef6f07b7abaa67203df59091e0` |
| S424 | fetch 2 | 22476 | 19807 | `998a5bb397241c8d1f484d0d4a53aefa9f732d67e1c8ca5afc16ccd566de74bb` |
| S424 | fetch 3 | 22476 | 19807 | `ebbdf1bee2efb3376c287bd0a51caa8103c7bba1141e2d3d94df2cf746b7209d` |

Article-text hashes (text nodes joined by newline; one hash per page, identical across retained + 3 fetches):

| page | article sha256 | text nodes (all / non-empty) | text chars | units | block offsets | raw block sha256 |
|---|---|---|---|---|---|---|
| S423 | `88c07fa98e07a1f0d23efac6c86854e64021179ecb6dff05b5d2f4c3be0fc326` | 159 / 155 | 3158 | 1453 | [9367, 14801) | `393400a6b882a9035e47ee1cc1f9304ff3c9b5e09b458c0490d0ebab91e04fbe` |
| S424 | `9d9d01c1eef55c7153ba826d980581d54dd31f7f64643c70e190233e420fb0f8` | 44 / 30 | 1004 | 537 | [9352, 11025) | `96e29b196811e6cc8d6cb11b6ace97306d314a88a1604883192e494d50683628` |

Per-variant article sha256 is the same value in all eight rows above (retained, f1, f2, f3 × two pages) — 8/8 match, and the
node *sequence* (not just the multiset) is identical, and the raw `text[lo:hi]` block bytes hash identically (6/6 fetch
comparisons). Block start offsets are byte-identical too (S423 9367, S424 9352), so the whole prefix is stable.

Retained receipts verified on disk: `sources/receipts.json` sha256/bytes for S423 and S424 equal `sha256sum`/`wc -c` of the
retained files; retained `fetchedAt` 2026-10-26T23:35:45Z / 23:35:46Z, UA `kake-shokunin-round58`. Fresh fetches used a
different UA (`Mozilla/5.0`) than retention and the article text still matched, so the stable region is UA-independent.

## DIFFS:

Every differing line region, classified against the retained body (base `<script>…</script>` spans, article window,
article end marker). "in article" = region intersects the article block.

- S423, fetch 1/2/3: 3 changed lines each, forming 2 contiguous script regions; 2/2 regions lie wholly inside `<script>`
  blocks; both start after the article end; 0 regions inside the article block. Same three lines every time:
  - `<script … src="…/uni_login_wrapper.js?cdnversion=202610270735">` → `…753` (f1), `…754` (f2, f3)
  - `<script src="…/passApi/js/wrapper.js?cdnversion=1793057745">` → `1793058828` / `1793058860` / `1793058892`
  - inline `url_sets` JS: `passreg : "https://passport.baidu.com/v2/?reg&u=…ziyuan.baidu.com%3A8021%2F&…"` →
    port `8010` (f1), `8087` (f2), `8032` (f3)
- S424, fetch 2/3: 3 changed lines each, 2 script regions, 0 inside the article block — the same two `cdnversion` lines
  plus the same `passreg` port churn (`8054` retained → `8087` / `8109`).
- S424, fetch 1: 3 regions — the two script regions above, plus one deletion in the trailing recommendation list *after* the
  article end marker (base lines 306–307: one `<li><a href="?id=3039" …>智能小程序命中搜索算法的常见问题</a></li>` entry absent),
  which is why the body is 140 bytes / 76 chars shorter and the variant span grows to 2640 chars.
- No diff region on either page touches the article block, in any of the 6 comparisons: `inside_article_block` = 0 everywhere.

Churn magnitude: S423 varies over 568 of 24294 chars (2.3%); S424 over 568 of 19807 chars (2.9%) in f2/f3, 2640 chars
(13.3%) in f1. Varying content is version/CDN query strings, one inline JS port, and one trailing list item.

## HYPOTHESIS:

**Holds for the load-bearing clause, falsified for the parenthetical clause.**

- Article-block text nodes are byte-stable: 8/8 variant hashes equal, node sequence equal, raw block bytes equal, block
  offsets equal. The 25-unit/40-char quote surface of both pages is reproducible from a fresh fetch — a quote that passes
  `span_tools.py check` on the retained body passes on all three fresh bodies.
- Full bodies are *not* byte-stable: 6/6 fresh fetches differ from the retention, and differ from each other (S423 equal
  length but three distinct digests; S424 two distinct lengths). Explained by `cdnversion` query strings, an inline JS
  port and (once) a trailing recommendation entry.
- So "only script/cache-token regions vary" is too narrow: the trailing recommendation list after the end marker
  (`往期回顾` / `推荐阅读` content) is also volatile. That region is outside the article block, so quote validity is
  unaffected, but a claim phrased as "only script regions vary" would be wrong.

Consequence for the C-claims (measured, not inferred from intent): `c58_quote_truth.py` C6 compares `receipts.json`
sha256/bytes against the *retained file* (lines 465–468), never against a live refetch, and C5 pins `BODY_SHA256` frozen at
the contract commit (line 91, checked at 349). Body-level volatility therefore does not break C5/C6 — the pin is
self-consistent by construction. What it does mean: body sha256/byte count are a retention fingerprint, not a
reproducibility guarantee; any future gate that re-fetches and compares the body digest will fail 6/6 on this pair, while
an article-text digest or a quote-substring re-check will pass. Reproducible field to cite: the article-text sha256 above,
or the existing span checks re-run against a fresh body.

Untested / limits: one 30 s cadence, one UA, one host, one ~70 s window, 6 samples total; server-side A/B or
cache-hit/miss variation over longer horizons is not excluded [INFERENCE]. Only the two adopted rows were probed, not
staged S395. No check of the S423 `往期回顾` list beyond its first differing occurrence; S424 f1 is the only observed
list fluctuation. `span_tools.py check`/`spans` were not run against the fresh bodies (the equals-node-set result makes it
redundant) — reported as unrun rather than passed.

VERDICT: Article text byte-stable 8/8 (and block bytes 6/6); full bodies unstable 6/6 — hypothesis holds for the quote surface, its "only script regions vary" parenthetical is falsified by one trailing recommendation-list shift, and the C5/C6 pins remain self-consistent because they compare against the retained file, not a refetch.
