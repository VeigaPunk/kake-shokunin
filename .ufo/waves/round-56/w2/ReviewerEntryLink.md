# ReviewerEntryLink

Falsification review of `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` (line-by-line) against
`.ufo/waves/round-56/sources/S367.html` (8051 bytes, sha256 `0188de9d…`, HTTP 200 per `receipts.json`). All 17
block-quoted spans verified mechanically against the raw bytes: each is a raw substring, occurs exactly once,
sits inside the article block (`<div class="asset-body">`, HTML lines 104-115), and is within ceilings
(canonical `span_tools.py check` units: 23/8/11/15 for the four gloss pieces; max quoted piece 24 canonical
units, 34 characters). Renderings were checked qualifier-by-qualifier; the page carries no 可能性があります,
no ください-form instruction, no status code, no redirect — nothing of that class exists to be dropped.

DEFECTS:

- (minor) Line 21: "ほかに (besides) opens the sentence" — the sentence does not open with ほかに.
  Page text (line 104): `リンク先ウェブページの巡回制限は、rel="nofollow"属性を使った指定方法のほかに、HTMLのメタタグで指定する方法と、サーバーの設定で指定する方法があります。`
  The sentence opens with the topic リンク先ウェブページの巡回制限は; ほかに is a postposition on the rel=nofollow
  link phrase mid-sentence, marking that route as the "besides" alternative before the two detailed routes.
  The entry's conclusion ("a further route precedes these two") is correct. Fix: "ほかに marks the linked
  rel=nofollow method as the route given in addition to (and named before) the two that follow".
- (minor, borderline) Lines 38, 68-69, 88: the page's instructionals are declarative `〜をします`
  (`次のような記述をします`, `次のように記述します`, `次のようなディレクティブ設定をします` — "one writes / makes the
  following"), rendered as English imperatives ("write the following kind of description", "write as follows",
  "make the following kind of directive setting"). The page carries no ください-form anywhere, so no
  確認/設定してください qualifier is at stake, but the register shift should be noted. Stricter fix:
  "the following kind of description is written / directive setting is made".
- (minor, borderline) Line 103-104: "The page does not state that the same refusal can be applied to an
  individual link URL". The page's own head meta description — which the entry itself invokes at line 96-97 —
  reads `特定のリンク先ウェブページの巡回を制限する方法` ("methods that restrict the crawl of *specific*
  link-target web pages"), which arguably states the restriction targets specific link targets. The claim
  survives narrowly (both body routes are page-scoped examples; no per-URL syntax is given), but as written it
  is in tension with the description text the entry relies on elsewhere. Fix: scope the claim to the article
  body ("the body gives no per-URL route; its only per-link route is the pointer to archives/002851.php") or
  reconcile with the 特定の phrasing.
- (minor, borderline) Line 68 rendering: `という場合には` is rendered "where the meaning is that it refuses…";
  the Japanese is a bare conditional clause ("in the case that it refuses… also refuses…") — the "meaning"
  scaffolding and the subject "it" are renderings' additions. Qualifiers survive (も → "also", 場合 → "where").
  Fix if strict literalism is required: "in the case of refusing the crawl of the link-target web pages and
  also refusing the registration of the web page itself in the index, write as follows".
- (note) Lines 41-43, 72-74, 91-93: the ```html code blocks (`<meta name="robots" content="index,nofollow">`,
  `noindex,nofollow`, `X-Robots-Tag: NOFOLLOW`) are entity-decoded renderings, not raw substrings of the body
  (page stores `&lt;meta name="robots" content=&quot;index,nofollow&quot;&gt;`). The "Quote classes" claim
  "Each quotation is a raw substring" is true of the `>` quotes but could be read to cover the code blocks.
  Content is faithful; class-boundary wording only.

No defect on qualifier survival in the renderings themselves: ほかに → "besides" (line 21), 方法があります →
"there is a method…" without any crawler effect attached (line 20-22, correct), このウェブページ内にある →
"inside this web page" (line 53-54, scoping claim correct), このウェブページ自身は → "this web page itself"
(line 53), も → "also… added to the first, not… an alternative" (line 68-70, correct), という場合には →
conditional "where" (line 68), サーバーで → "on the server that is hosting the web page" (line 88). Subject
checks pass: gloss 1 keeps crawl-of-targets as the refused thing and the page itself as the permitting
subject; gloss 2 adds the second refusal via も.

TAG AUDIT:

- Line 97 `[INFERENCE]` "the token is delivered in the HTTP response": honest. The body states only
  `ウェブページをホスティングしているサーバーで、次のようなディレクティブ設定をします` + `X-Robots-Tag: NOFOLLOW`;
  delivery in a response is nowhere on the page.
- Lines 97-99 `[INFERENCE]` "the value is read as refusing the crawl of the page's link targets": honest.
  The body gives no gloss for NOFOLLOW; only the page title/section supplies the restriction framing.
- Untagged claims all verified on-page: `rel=&quot;nofollow&quot;属性を使った指定方法` link →
  `archives/002851.php` (line 27, href verified); attribute route has no sub-heading and no example
  (lines 28-29, verified: link text only); head meta description at HTML line 13
  (`サーバーのHTTPヘッダーの設定`) correctly characterized as outside the article block (line 96-97);
  `個別リンクURL` occurs exactly once at HTML line 125 inside `tag-area`, outside the article block
  (line 104-105, verified); zero occurrences of 200/404/可能性/確認してください/設定してください/robots.txt/
  user-agent names/wildcards (grep counts all 0) supporting lines 106-113 absence claims.
- Sibling-content claims verified: S372 sibling (`yahoo-japan-robots-txt-refusal-rules.md` lines 95-106)
  does record the meta-tag fallback for a site without root write access (line 109-111 claim accurate);
  S374 sibling (`yahoo-japan-rel-nofollow-semantics.md` lines 19, 29-30) records URL-still-used-for-discovery
  and attribute-not-weighed (line 112-115 claim accurate). Source IDs S374→002851, S372→002849, S286→Google
  crawl-error page confirmed from sibling `source:` lines.
- Provenance claim (line 122) verified: round-53 gate anchor on S367 was 31 units (w1 ScoutQuality L15 /
  EntryLinkTarget L165); the same sentence is re-cut here into 23/8/11/15-unit pieces, all ≤25.
- Scope note (line 124): honest — documentation-claim only; nothing served, crawled, or tested for the lane.

HEADER AUDIT:

- `source:` line 1: URL `https://info-search.yahoo.co.jp/archives/002852.php` matches receipts.json S367;
  section label corresponds to the page's `<h2>` and `<title>`; sub-heading names `メタタグを使用する方法` and
  `サーバーで設定する方法` match the two `<h3>`s; 更新日 2010年11月24日 matches `<p class="update">`.
  One byte-level note: the page h2 separates 制限 and ― with U+3000 ideographic space (`制限　―`), while the
  `source:` label uses ASCII space — the label occurs in the page only modulo whitespace normalization.
- `recheck:` line 3: stated count verified on both arms. Retained body:
  `grep -F -c 'サーバーの設定で指定する方法があります' S367.html` → 1. Live arm run this session:
  `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002852.php' | grep -F -c …` → 1 (curl exit 0).
- `verified-at: 2026-10-25` consistent with receipts `fetchedAt: 2026-10-25T22:02:40+00:00`.
- `ground:` line 4 consistent with page content (page-scope link-target crawl refusal via head or server).
- Quote-classes block (lines 119-122): sha256 prefix `0188de9d…`, 8051 bytes, HTTP 200 all match
  receipts.json; once-only / in-article / ≤25-unit claims mechanically verified for all 17 `>` spans.

VERDICT: Fidelity holds — every quoted span is a unique in-article raw substring under the 25-unit ceiling, both [INFERENCE] tags are honest, both recheck arms print 1; five minor wording defects (ほかに "opens the sentence", declarative→imperative rendering, individual-URL claim vs 特定の description, という場合には scaffolding, code-block "raw substring" boundary) and one header whitespace-normalization note, none fatal.
