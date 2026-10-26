# CriticC3Counter

Scope: the NEW parts of `.ufo/waves/round-57/c57_quote_truth.py` (v1, derived from `c56_quote_truth.py` v2.1 by
`derive_c57_quote_truth.py`): `content_window`/`in_content` (Baidu article block), the `发布日期：` page-identity check,
the substring-of-body title check, the staged-name refusal list, and the unchanged C1..C8 condition code as it acts on
two NEW rows. Read: `contract.md` C3, `contract.json`, the counter, the derive script, `span_tools.py`,
`sources/{S421,S422}.html`, `sources/receipts.json`, `controls/base-c3-quote-truth.txt`.

Method: every claim below marked **RUN** was executed. Fixture recipe (all writes inside a mktemp clone; lane untouched):
`D=$(mktemp -d); git clone -q --no-hardlinks <lane> $D; git -C $D checkout --detach b9a5d012`; then write
`corpus/SOURCES.md` (base + the two rows below), the two entries, `corpus/lessons/round-57.md`, and the C7 receipts under
`assimilation/validate/`; commit with `-c user.name=selftest -c user.email=selftest@local`; run
`python3 -B .ufo/waves/round-57/c57_quote_truth.py --root $D --revision HEAD`. `git -C $D rev-parse --show-toplevel` == `$D`.
The clone starts at the contract commit, so the pre-append mirror, `mirror-pin.json` and the retained bodies/receipts are
already in history and C6/C7/C8 are satisfiable without touching anything else. Base control re-run at
`28fa0b23…` in the clone: exit 1 (unchanged). No tool installed.

## ATTACKS:

**A1 — a junk tree reaches 8/8 (RUN).** Two entries that quote nothing from the article:
- S421 entry quotes three fragments of the **recommended-reading sidebar** (`<div class="list-right">`, 21138..21828):
  `"搜索内容选题技巧</a>"` 8u/12c/count 1, `"搜索流量优化指南</a>"` 8u/12c/count 1, `"权益整体介绍<"` 6u/7c/count 1.
- S422 entry quotes three fragments of the **in-window `<style>` block** (9282..9852):
  `"{ margin: 0cm 0cm 0.0001pt; text-align:"` 6u/39c, `"l { margin: 0cm 0cm 0.0001pt;"` 6u/29c,
  `"soNormal { margin: 0cm 0cm 0.0001pt;"` 6u/36c (each count 1, none in the sibling body).
- Row anchor cell: `§ 推荐阅读 (发布日期 2022-09-09)` — the anchor heading is the sidebar's own `<h2>`.
Result: `C3 quote-truth 8/8 met=True`, `EXIT=0`. C5 passed with every span outside the article prose.
Answer to the seat's question: plain sidebar link *text* is **not** available to the attack — each link text occurs twice
(`title="…"` attribute + anchor text), so `text.count(span)==1` rejects it; only markup-carrying fragments and the CSS are
page-unique. The uniqueness rule therefore blocks the readable nav text and admits the unreadable markup.

**A2 — the receipt pin is circular (RUN).** In the build commit I appended a comment to `sources/S421.html` and rewrote
`sources/receipts.json` (`sha256`, `bytes`) to match. Counter: `8/8 met=True EXIT=0`. `C6` reads `RECEIPTS` at `--revision`,
never at the contract commit, and `HELD_BODY_SHA256` is `{}` for NEW rows, so nothing in the counter ties the retained bytes
to the fetch the contract commit froze (`b9a5d012`). Any body can be swapped together with its receipt and C5's title/date/
anchor checks then certify the swapped body.

**A3 — the title and anchor rules accept any substring (RUN).** With the S421 row's title cell reduced to `死链`
(`百度搜索资源平台 — 死链 — https://…`) the counter prints `8/8 met=True EXIT=0`; the rule is only
`title in texts[sid]`, with no length, uniqueness, or `<title>`/h3 equality. A1 already shows the anchor heading accepted from
a sidebar (`推荐阅读`, 4 units, no uniqueness test).

**A4 — the predicate is set-dependent (RUN).** Adding an unrelated `.html` under `sources/` (I added `S999.html` holding the
S421 sidebar bytes) flipped the same, unedited entry from `8/8` to `7/8`:
`S421: a Gate quote occurs more than once in its own body or also in another retained body (not page-unique)` and
`S421: entry carries 0 page-unique quoted spans, expected 3+`. `others` is built from the live `ls-tree` of `sources/`, so a
committed entry's C5 verdict can change at a later revision without any edit to the entry. (For C1 the same class of defect
is the one the round exists to catch.)

**A5 — short boilerplate is admitted (code-read + spot check).** `verify()` checks window membership but not uniqueness for
entry spans of 2..5 units, so `"百度搜索"` (4 units, count 6 in S421 / 5 in S422, in both windows) passes as an entry quote
and simply does not count toward `MIN_UNIQUE_SPANS`.

## WRONG-REJECT:

**W1 — the faithful anchor is refused (RUN).** Writing the anchor exactly as the page prints it,
`§ 推荐阅读 (发布日期：2022-09-09)` (fullwidth colon, byte-identical to S421 at 9443), gives `7/8` with
`S421: row anchor carries no 发布日期 YYYY-MM-DD printed date`. The code requires `发布日期 <date>` (ASCII space) in the row
while `contract.md` C3 and the counter's own docstring both say the anchor names the printed `发布日期：<date>`. The lane's
existing anchors use the ASCII form (S390/S409), so this is a contract-vs-code mismatch plus a trap for a drafter who copies
the page.

**W2 — the page's own title cannot be quoted (RUN).** Adding `"搜索问答剧场 【六】“死链”常见问题解析"` to the S421 entry
(raw substring at 9368, 15u/20c) gives `S421: entry line 12 uses curly double quotes; the declared form is ASCII`. The page
prints the curly quotes; the raw-substring rule forbids editing them; the curly rule forbids keeping them. The same line also
fails page-uniqueness (count 3: `<title>`, breadcrumb, h3). Any span crossing the page's own `“ ”` (title, 往期回顾 items) is
unquotable.

**W3 — the identity date is accepted outside the window, the same date quoted is refused (RUN).** S422 entry line
`"发布日期：2016-06-30"` (raw at 9222, 4u) gives `S422: entry line 12 quotes '发布日期：2016-06-30'… which sits outside the
page's content block` — while C5's own identity check accepts that string from the whole body (it is 25 bytes before the
window start, see WINDOW FINDINGS). One rule certifies the text as page identity; the other refuses the identical text as a
quote.

**W4 — entity vs rendered space (RUN, declared tradeoff).** `"为什么要及时处理死链&nbsp;？"` (10u/17c) → `8/8`.
`"为什么要及时处理死链 ？"` (the text a reader sees) → `S421: entry line 12 quotes '为什么要及时处理死链 ？'… which is not a
raw substring of the retained body`. The contract declares entities stay as written, so this is not a defect — but the note
is identical to the note for a genuinely wrong quote.

**W5 — inline `<span>` straddle (RUN, declared tradeoff).** `"包括协议死链和内容死链"` (11u) →
`not a raw substring of the retained body`. The raw is `包括<span …><span …><b>协议死链和内容死链</b></span>。`; only the
bolded run is quotable. Declared by the raw-substring rule; the cost is that the article's definition sentence cannot be
quoted as a sentence, and the counter cannot tell a straddle from a misquote.

## WINDOW FINDINGS:

Offsets are byte offsets in the retained bodies (UTF-8, as committed).

S421 (`len 30007`): window `(9346, 21828)`, 12482 B.
- 9341 `<div class="article-info">`; **9346** marker (`class="article-info"`); 9368 `<h3 class="info-title">`; 9443
  `发布日期：2022-09-09`; **9467** article prose begins (`<section powered-by="xiumi.us"`, second section 15841).
- 20418 `往期回顾` promo block; 21058 pager; 21131 article div closes; **21138** `<div class="list-right">` (sidebar);
  21164 `recommand-news`; 21251 `推荐阅读`; **21828** `class="footer"`.
- Between container start and the article text: the h3 title and the `info-item-time` date paragraph (9346..9467, 121 B) —
  identity furniture, deliberately inside. Chrome *inside* the window: sidebar 690 B + 往期回顾 713 B = 1403 B (11.2%).

S422 (`len 23676`): window `(9247, 13061)`, 3814 B.
- 9196 `<p class="info-item-time">`; **9222** `发布日期：2016-06-30` — both **outside** the window (25 B before it);
  9242 `<div class="zz_dldes_content clearfix">`; **9247** marker (window starts mid-tag); 9282 `<style>` … **9852**
  `</style>` = 570 B (14.9% of the window) of CSS *inside* it; article prose starts at 9852; 12885 empty
  `wiki-foot-right`/`wiki-download` block; **13061** `class="footer"`.
- The window's first 605 B are a style sheet, and the page's printed date is not in the window at all.

Q3 (`in_content` and the recommended-reading list): **yes** — A1's S421 gate span and all three entry spans are sidebar
markup and `in_content` returns True for them; the docstring's "navigation … excluded" is false for both pages (S421 sidebar
inside; S422 style block inside).

Q4 (`发布日期：` met by a date printed elsewhere): not on these bodies — each prints the string exactly once (S421 at 9443,
S422 at 9222) and neither page carries `datePublished`/`pubdate`/`publish_time`. But the check is whole-body and
element-agnostic: it does not require `info-item-time`, and for S422 it is satisfied by text outside the content block the
counter defines. A page that printed a second `发布日期：` line (comment, related article) would satisfy whichever date the
anchor named.

Q5 (other-body uniqueness with two bodies): **inert here**. `sources/` holds exactly S421 and S422 (two different Baidu
templates); a search of every S422 in-window span of 6..25 units and <=40 chars found **0** that also occur in S421 (the
only cross-body strings are short: `百度搜索` 4u, `搜索资源平台` 6u but only in S422's `<title>`, outside its window). So
"page-unique" reduces to `count == 1` in the page's own body — and it is not stable: A4 shows a third body flips it.

## RECOMMENDED COUNTER CHANGES:

Ordered by risk; all are counter-side and can land before the entries exist (no data is scored yet).

1. **Pin provenance to the contract commit** (fixes A2): read `receipts.json` at `b9a5d012f7fd` and require the measured
   revision's copy to be byte-equal; add `HELD_BODY_SHA256 = {"S421": "32eaf8b7…", "S422": "7cf2e27d…"}` (values from
   `sources/receipts.json`) and check it for NEW rows too. Optionally add the two body hashes to `contract.json`.
2. **Narrow the window to the article prose** (fixes A1/A5): strip `<style>…</style>` and `<script>…</script>` before
   locating; end the window at `往期回顾` for S421 and at `wiki-foot-right` for S422; start it at the article `<h3>`/first
   `<p>` (S421: 9368/9467) and at the first text after `</style>` (S422: 9852). Sizes then become ~10.9 KB and ~3.0 KB, and
   the sidebar/pager/CSS are excluded as the docstring already claims.
3. **Refuse markup spans** (cheap, kills the remaining junk class): reject any span containing `<`, `>`, `{`, `}`, or `;`
   and require the span to occur in the tag-stripped window text (entities kept). This rejects `搜索内容选题技巧</a>` and all
   CSS spans while keeping `&nbsp;` spans valid.
4. **Strengthen the identity checks** (fixes A3): require the row's title cell to equal the page's `<title>` with the
   `_…_百度搜索资源平台` suffix removed (or the h3 text), >= 6 units; require the anchor heading to be >= 6 units and
   page-unique. As written, `死链` and `推荐阅读` both pass.
5. **Accept the page's own date form** (fixes W1): `re.search(r"发布日期[：: ]\s*(\d{4}-\d{2}-\d{2})", anchor_cell)` and
   require the matched date to sit inside the content window — which forces S422's window to include the byline or the row to
   state the date is printed outside the article block.
6. **Freeze the uniqueness sibling set** (fixes A4): compute `others` from the sources present at the contract commit
   (`git ls-tree b9a5d012 sources/`), not from the live `sources/` directory, so a later body cannot flip a committed entry.
7. **Distinguish the refusal notes** (fixes W3/W4/W5 diagnosability): separate notes for "not a raw substring" vs "raw only
   after tag stripping (inline markup straddle)" vs "outside the window"; and scope the entry-quote window check to the same
   region as the identity check so the printed date is either inside both or refused by both.
8. **Two labeling fixes**: the `--json` payload says `"schema": "kake-r57-c2-quote-truth-v1"` (names C2, not C3); and
   `--selftest` still exits 2 — port A1, A2, A4, W1, W2, W3 as fixtures (they are cheap: each is one row/entry line change
   on the recipe above).

Unrun: nothing above is unrun except A5's generalisation (code-read plus one span spot-check). No pacman, no network, no
writes outside `$D` and this file.

VERDICT: C5 passes 8/8 on a tree that quotes only sidebar markup and style-block CSS, and C6's receipt pin is circular (body + receipt rewritten together still pass 8/8) — both fixable counter-side before the entries are written; also confirmed two wrong-rejects (faithful `发布日期：` anchor, page's own curly-quoted title) and a set-dependent uniqueness rule.
