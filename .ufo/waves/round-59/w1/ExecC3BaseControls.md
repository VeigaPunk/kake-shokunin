# ExecC3BaseControls

Round-59 kake wave 1, seat ExecC3BaseControls (leaf; no subagent used). Target: claim C3 attacked against
counter version 1, `.ufo/waves/round-59/c59_quote_truth.py` as frozen at the contract commit. Nothing
outside this report and its `.files/` directory was written in the lane; no git/jj state touched.

Method. A `git clone --shared` of the lane at `45a92b64ac8a0f82dba369100e30682f14de81fb` (all work in
`/fast/scratch/hyaku/kake-r59/ExecC3BaseControls/`) built a complete after-state: rows S425/S426 appended,
the two entries, `corpus/lessons/round-59.md` with a `## Gate`, the append-only correction tail, and the
`assimilation/validate/` block produced by really running `scripts/sources-census.sh validate --file …`
(real stdout/exit, not synthesised). Mirror, retained bodies and `sources/receipts.json` are the contract
commit's own bytes. One commit per variant; each scored through the counter CLI
(`--root <clone> --revision <commit> --base fd6303ce…`). Fixtures are mine, not the wave's build; no
after-state existed at the contract commit.

Two instruments. `v1` = the contract-commit blob (`sha256 b3aef90c…`), the assignment's target. `v2` = the
counter now sitting **uncommitted** in the lane working tree (`git status` shows `M`, `sha256 74308411…`,
comments credit `w1/ScribeRegistryGate` and `w1/CriticC3Cheat`); it was scored because it changes which
holes are still live. A third column, `probe` (v1 with only the S425 title floor `units(title) < 6` → `< 3`),
was used to separate H1 from each control's own effect before v2 arrived. All scores are measured, none
inferred; receipts in `.ufo/waves/round-59/w1/ExecC3BaseControls.files/` (`matrix.json`, `matrix-v2.json`,
`score-table.txt`, `score-table-v2.txt`, per-variant `*.frozen.json` / `*.v2.json`, `probe_floor3.py`,
`v2_counter.scored.py`).

## CONTROLS:

Control holds = the fixture must NOT meet 9/9.

| fixture | what it cheats | census | v1 | v2 | v2 verdict |
|---|---|---|---|---|---|
| `good` | nothing (intended after-state) | exit 0 | 8/9 | **9/9** | baseline: v2 is reachable |
| `a1_chrome_only` | entries quote only chrome spans | exit 0 | 8/9 | 8/9 | rejected — by count/topic, not by chrome |
| `a2_chrome_mixed` | 3 content spans + 1 chrome span | exit 0 | 8/9 | **9/9** | **NOT caught (H2)** |
| `a3_chrome_substitute` | 2 content + 1 chrome span (exactly 3) | exit 0 | 8/9 | **9/9** | **NOT caught (H2)** |
| `a4_two_content_only` | 2 content spans, no chrome | exit 0 | 8/9 | 8/9 | rejected: `entry carries 2 page-unique quoted spans` |
| `b_opposite` | true spans, prose asserts the opposite | exit 0 | 8/9 | **9/9** | NOT caught — stated limit |
| `c_html_comment` | correction tail inside `<!-- … -->` | exit 0 | 8/9 | 8/9 | caught by v2 (C9, "as rendered prose") |
| `d_contradicting` | stale line kept, tail restates it | exit 0 | 8/9 | **9/9** | **NOT caught (H4)** |
| `e1_usedby_extra_exists` | used-by lists one extra existing file | exit 0 | 7/9 | 8/9 | caught: C4 exact-set note |
| `e2_usedby_extra_missing` | used-by lists one absent file | exit 1 | 6/9 | 7/9 | caught: C4 + C7 (census E11 → exit 1) |

(a) chrome-only entries — **does not meet 9/9, but not for the intended reason.** `a1` is rejected only by
`MIN_UNIQUE_SPANS` and the per-row topic rule (`S425: no page-unique span … carries IP address`;
`S425: entry carries 1 page-unique quoted spans`; `S426: entry carries 0`). The promo span was nevertheless
*accepted* as a page-unique in-content span — it is the `1` counted there. `a3` (exactly two content spans
plus the promo span) reaches **9/9 under v2**, and `a4` (the same entry minus the promo span) fails with
`entry carries 2 page-unique quoted spans`. The chrome span therefore supplies the third required span: the
block window does not exclude it (H2). Chrome measured with the counter's own
`content_window`/`text_segments`/`in_content`/`units`: S425 promo `<aside>` at window offset 858 —
`Looking for the latest updates to this page?` (8 units, 44 chars, count 1 in S425, 0 in S426), plus the
`<devsite-thumb-rating>`/`<devsite-feedback>` widget (`Send feedback`, 2 units, count 2, not unique); S426
has the feedback widget only, so no qualifying chrome span there.

(b) true spans, prose asserting the opposite — **meets (9/9 under both v1-probe and v2).** No support test
exists; this is the limit the contract already states ("what the counter does not test: whether the English
entries are faithful … quote truth, not support"). Recorded as a stated limit, not a new hole. Note H4 sits
just past that sentence: it is the same blindness applied to the correction itself, which the sentence does
not cover.

(c) correction tail as an HTML comment — **v1: meets (C9 PASS, zero notes). v2: caught.** Rendering with
`cmark --unsafe` and stripping comment nodes, the v1-accepted document holds one comment node and its visible
text contains neither `[r59-correction` nor the quoted span, so a reader sees the stale sentence uncorrected
while v1 saw a correction. v2's rendered-prose rule rejects it with `no line inserted where the stale bullet
ends carries [r59-correction 2026-10-27] as rendered prose`. Good fix; H3 is closed in v2.

(d) stale line kept, tail contradicting S425 — **meets under v1 and v2 (9/9, C9 PASS).** Visible render:
`[r59-correction 2026-10-27] The stale bullet above stands: a server log records the user-agent string and
nothing else … [S425] — "The source IP address of the request."` C9 checks the tag, the citation and one
valid span; it never checks that the tail disagrees with the stale sentence (H4).

(e) used-by listing extra files — **control holds under both.** C4 compares the sorted set exactly, so extras
fail whether or not they exist (`e1`: only C4 turns). A missing extra is caught twice (`e2`): C4, plus census
`E11` driving the validate run to `exit=1`, which C7 rejects on both the exit string and the missing
`file<TAB>ok<TAB><path>` tail line. Order-insensitivity of the sorted compare is harmless.

## HOLES:

H1 **v1 blocker, closed in v2** — C5's row-title floor was unsatisfiable for S425, capping every evidence set
at 8/9. v1 `c59_quote_truth.py:378-380` required `title == page_title` **and** `units(title) >= 6`; S425's
page title `Google Crawler (User Agent) Overview` is 5 whitespace units, and equality pins the count to 5.
Measured: no fixture exceeds 8/9 under v1 (the strongest, `good`, sits at 8/9), and that same commit scored
9/9 under the one-constant probe with nothing else changed. Origin: floor inherited verbatim from `c58_quote_truth.py:353-355` (round-58 rows
were Chinese, ≥6 CJK units by construction); `derive_c59_quote_truth.py:165-166` changed
`.split("_")[0]` → `.split(" | ")[0]` but kept the floor. v2 lowers it to 3 units, credited to
`w1/ScribeRegistryGate`; `good` now scores 9/9. Accepted, but the weaker floor alone would still admit a
5-word English title — the H2 control does the real work of keeping quotes honest.

H2 **open in v2 — chrome counts as an article quote.** `content_window` (v1 `c59_quote_truth.py:183-190`,
unchanged in v2) spans `class="devsite-article-body` to `<devsite-content-footer`; both chrome blocks live
*inside* that range on S425 (promo `<aside>` at offset 858, feedback widget at 11812/11877), and
`text_segments` strips only `<style>`/`<script>`. The function's own docstring claims "header, navigation,
sidebar, promo and footer excluded" — not implemented. Evidence: `a3` (2 content + 1 chrome span) reaches
9/9 under v2, `a4` fails, `a1` counts the promo span. So promo/sidebar/feedback text can be quoted as located
article evidence and can satisfy the three-span minimum. Fix: in `text_segments`, blank
`<aside>`, `<devsite-feedback>`, `<devsite-thumb-rating>` and `<nav>` subtrees before extracting text nodes
(the feedback block already carries `class="nocontent" data-nosnippet`, so honouring those attributes covers
it), or start the window after the promo aside; then port the `a3`/`a4` pair into the selftest kill matrix so
the guard cannot silently regress.

H3 **v1 hole, closed in v2** — C9 v1 diffed lines and accepted an inserted `<!-- … -->` line carrying the
tag, the S425 citation and a valid span; visibility was never required. Evidence: `c_html_comment` (v1 C9
PASS, and the correction absent from rendered visible text). v2 strips HTML comments and code spans and
requires rendered prose; the fixture now fails C9 as intended.

H4 **open in v2 — a tagged restatement passes as a correction.** C9 still checks only the tag, the citation
and one valid span, so a tail that asserts the stale claim and carries a true span is accepted. Evidence:
`d_contradicting` reaches 9/9 under v2. This is a fidelity gap, not a plumbing bug: both "the stale claim is
wrong" and "the stale claim stands" can quote the same true span, so no cheap token rule separates them
(a negation-word list is brittle and would not catch a H2-style rewrite). Recommended: extend the contract's
"what the counter does not test" sentence, which today covers only the entries' faithfulness, to the
correction tail as well, and route it to the reviewer/critic seat; if a mechanical guard is wanted anyway,
require the tail to state the corrected fact in the page's own list terms (at least two of the three identity
signals) and flag the remainder for review — a raised bar, not a proof.

Minor, not holes: the topic test is a plain substring test, so `IP address` also matches `IP addresses`;
`Send feedback` is non-unique on both bodies, so a feedback-only entry can never satisfy the span count; the
`--selftest` entry point is still the version-1 stub returning 2 in the working tree (`v2_counter.py:685-687`),
so none of H2/H4 is caught by the instrument itself.

Not tested here: whether any build's English prose is faithful (reviewer/critic job), C1/C2, and any
after-state built by another seat. "A renderer does not display comment nodes" is documented HTML behaviour
[INFERENCE], evidenced here only by stripping comment nodes from `cmark` output. v2 is uncommitted and may
have moved since the copy scored (`sha256 74308411…`); re-score against the committed file before measuring.

## VERDICT:

Against v1 the claim's predicate is unreachable (ceiling 8/9 on all ten fixtures) and three false-green
routes survive the title floor: chrome spans count as article quotes, and C9 accepts both a comment-hidden
correction and a tagged restatement of the stale claim; the used-by control holds, and the opposite-prose
entry is the contract's own stated limit. The current working-tree v2 closes H1 and H3 but leaves H2 and H4
demonstrably green at 9/9.

VERDICT: BLOCK on v2 — H2 (chrome in the article block) and H4 (tagged restatement as correction) are demonstrated by fixtures scoring 9/9 met=True; H1/H3 are closed only in the uncommitted v2, which must be committed with its selftest kill matrix before any C3 measurement.
