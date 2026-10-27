# MutC3Counter

Mutation test of `.ufo/waves/round-59/c59_quote_truth.py` — the C9 condition and the English-page
(C5/C4) changes. Counter snapshot (sha256 `52cd698c…d7966bd5`, the lane working-tree file at run
time; the file moved twice during this seat: `7430841…` → `52cd698…`, both single-commit diffs
landed by wave-1 siblings). Lane file read-only throughout; every fixture and mutant lives under
`/fast/scratch/hyaku/kake-r59/MutC3Counter/` (deleted at the end; receipts copied to
`MutC3Counter.files/`). No scratch path outside that dir was written.

Detector (bounded, deterministic — two pristine runs byte-identical): the counter's own
`run_checks(root, rev, base)` over a fixture variant set; the observed unit is
`variant → (exit, per-check state, per-check notes)`. Kill = any variant's observable result
differs from the pristine run. Baseline is green: `V0_positive` scores **9/9, exit 0** on pristine,
so no kill is attributed to a pre-existing failure. Control `M00_noop` (comment-only edit) survives,
so the matrix produces no spurious kills.

## FIXTURES:

Fixture repo `D` (scratch git; base commits hold the real `corpus/SOURCES.md` and the real
`corpus/knowledge/crawler-identity.md` bytes from `fd6303ce`, the pre-append mirror + pin, the real
retained `S425/S426.html` and `receipts.json`). 28 measured variants, each one commit.

| fixture | pins (expected pristine verdict) |
|---|---|
| V0_positive | full valid state — 9/9, exit 0 (positive control) |
| V1_stale_twice | stale sentence appears twice → C9 |
| V2_position_16 | correction 16 base lines after the bullet end → C9 |
| V3_line_deleted | one base line deleted (not append-only) → C9 |
| V4_wrong_tag | `[r59-correction 2026-10-26]` instead of the access date → C9 |
| V5_wrong_id | correction cites S426 only → C9 |
| V6_no_topic | correction quote without "IP address" → C9 |
| V7_long_quote | entry quote 170 chars / 22 units → C5 |
| V8_date_in_attribute | printed revision only inside a tag attribute (body variant) → C5 |
| V9_footer_quote | entry quote from the footer, outside the article block → C5 |
| V10_h1_anchor | row anchor names the page `<h1>` → C5 |
| V11_used_by_order | used-by cell order reversed → **passes** (sorted compare, positive) |
| V12_curly_quotes | correction carries curly double quotes → C9 |
| V13_short_quote | 4-unit quote that still carries the topic → C9 |
| V14_over_unit_ceiling | 26-unit quote (160 chars) → C9 |
| V15_one_span | entry with one page-unique topic span → C5 |
| V16_shared_span | Gate quote also present in S426 → C5 |
| V17_no_unit_count | Gate line without the "N units" annotation → C5 |
| V18_newline_span | Gate quote crossing a raw newline → **passes** (needs the collapse, positive) |
| V20_no_article_block | body without the article-body marker (body variant) → C5, C6, C9 |
| V21_code_span_quote | correction quote wrapped in backticks → C9 |
| V22_fake_heading_in_pre | row anchor heading only inside a `<pre>` sample (body variant) → C5 |
| V25_inside_bullet | correction inserted inside the stale bullet → C9 |
| V26_cross_body_span | correction quote also occurs in S426 (body augmented) → C5, C6, C9 |
| V27_chrome_quote | entry quotes page chrome inside the article window → C5 |
| V28_attr_hidden_quote | correction hides its quote in an HTML attribute → C9 |
| V23_long_bullet | 14-line stale bullet, correction at its end (synthetic base doc) → C9 |
| V24_mid_bullet | 9-line stale bullet, correction at its end (synthetic base doc) → **passes** (positive) |

Body bytes are untouched in 24 of 28 fixtures; V8/V20/V22/V26 change the retained body on purpose
(sha256 note in both runs, so their kills are notes/membership deltas), and V23/V24 use a synthetic
base document (bullet length is the only way to reach the window arithmetic).

## MUTANTS:

28 single-point textual mutants, each a copy of the snapshot in `mutants/` (sha256 recorded in
`receipts_matrix.json`); 27 killed, 1 control survivor. "delta" = the kill's observable kind:
**state** = a check verdict or the exit code flips; **notes** = the check keeps its verdict and one
diagnostic line disappears (C5 stays red only because a body variant also trips the sha256 pin).

| id | change | killed? (delta, killing fixture) |
|---|---|---|
| M01_window_80 | `STALE_WINDOW` 8 → 80 | **killed** (state, V23: exit 1→0) |
| M02_window_4 | `STALE_WINDOW` 8 → 4 | **killed** (state, V24: exit 0→1) |
| M03_no_append_only | C9 delete/replace opcode check removed | **killed** (state, V3: 1→0) |
| M04_no_tag | `CORRECTION_TAG` requirement removed | **killed** (state, V4: 1→0; also V2/V25/V23) |
| M05_loose_s425 | `\bS425\b` → `\bS42` (no trailing boundary) | **killed** (state, V5: 1→0) |
| M06_no_topic | C9 `TOPIC["S425"] in span` removed | **killed** (state, V6: 1→0) |
| M07_char_ceiling | `CHAR_CEILING` 160 → 400 | **killed** (state, V7: 1→0) |
| M08_no_collapse | whitespace collapse of the retained body removed | **killed** (state, V0: 0→1; 32 deltas) |
| M09_article_end | `ARTICLE_END` → `</devsite-content-footer>` | **killed** (state, V9: 1→0) |
| M10_headings_h1_6 | heading regex `<h[23]>` → `<h[1-6]>` | **killed** (state, V10: 1→0) |
| M11_date_outside_nodes | printed-revision check → raw substring (outside text nodes) | **killed** (notes, V8) |
| M12_used_by_unsorted | `got = sorted(used_by(...))` → unsorted | **killed** (state, V11: 0→1) |
| M13_no_stale_once | "stale sentence preserved exactly once" removed | **killed** (state, V1: 1→0) |
| M14_no_curly | C9 curly-quote refusal removed | **killed** (state, V12: 1→0) |
| M15_loose_position | `i1 == end` → `s < i1 <= end` | **killed** (state, V25: 1→0) |
| M16_no_prose_filter | C9 code-span/comment/tag strip removed | **killed** (state, V21: 1→0; also V28) |
| M17_units_floor_2 | C9 unit floor `6 <=` → `2 <=` | **killed** (state, V13: 1→0) |
| M18_unit_ceiling | `UNIT_CEILING` 25 → 40 | **killed** (state, V14: 1→0) |
| M19_no_in_content | C9 `in_content(...)` requirement removed | **killed** (state, V20: C9 fail→pass) |
| M20_min_unique_1 | `MIN_UNIQUE_SPANS` 3 → 1 | **killed** (state, V15: 1→0) |
| M21_no_gate_unique | Gate-quote page-uniqueness check removed | **killed** (state, V16: 1→0; also V26) |
| M22_no_gate_units | Gate "N units" annotation check removed | **killed** (state, V17: 1→0) |
| M23_title_floor_6 | row-title floor `units < 3` → `units < 6` (pre-wave-1 rule) | **killed** (state, V0: 0→1; 32 deltas) |
| M24_no_cross_body | C9 cross-body uniqueness removed | **killed** (state, V26: C9 fail→pass) |
| M25_no_code_strip_headings | `article_headings` code/script strip removed | **killed** (notes, V22) |
| M26_no_chrome_strip | `text_segments` aside/nav/feedback blanking removed | **killed** (state, V27: 1→0) |
| M27_no_tag_strip_c9 | C9 tag strip removed (attributes count as prose) | **killed** (state, V28: 1→0) |
| M00_noop | comment-only edit (control) | survived, as required |

Six kills need evidence outside the frozen corpus (V23/V24 synthetic base documents; V8/V20/V22/V26
body variants). With the real bodies alone, M01, M02, M11, M19, M24 and M25 stay undetected —
their conditions are vacuous on these two pages (bullet length 4, the printed revision is always in
a `<p>`, every "IP address" span lies inside the article block, no topic span repeats across bodies).

## SURVIVORS:

None among the 27 behavioural mutants. `M00_noop` (comment-only) survives by design and proves the
detector does not manufacture kills; two pristine runs were byte-identical.

Coverage gap noted, not a mutant: C9's own-body uniqueness (`text.count(span) == 1`) is not pinned by
any fixture, because no 6..25-unit span carrying "IP address" occurs twice in the frozen S425 body
(exhaustive scan over the article block: 0 hits). A fixture would need an augmented body.

## PROPOSED FIXTURES:

1. Keep this matrix (or a port of it) as the counter's `--selftest`: V0 as the named baseline, V1–V28
   as red cases attributed by the note they add relative to V0 (not by exit code alone), plus the
   no-op control for determinism.
2. Add a long-bullet base document (14 lines) to reach `STALE_WINDOW`; the real 4-line bullet makes
   the window arithmetic unobservable, so M01/M02 are invisible on the frozen corpus.
3. Add a body-attribute fixture for the printed revision (V8) and one body with the article marker
   removed (V20): they are the only way to exercise the text-node restriction and the block
   membership rule of the English-page adaptation.
4. Add an own-body duplicate topic span fixture (same span twice inside the article block) to pin
   `text.count(span) == 1`; today that conjunct cannot fail with the frozen S425 body.
5. Add V27/V28 to the selftest's red set: page chrome inside the window and HTML attributes are the
   two newest cheat routes closed by the wave-1 revisions, and both are one-line regressions.
6. Consider a wrapper fixture that runs the counter end-to-end (`--root/--revision/--base/--json`)
   so exit codes 0/1/2 and the usage path (64) are pinned too; this seat drove `run_checks` directly.

Attribution note: M00 control survivor; all kills are reproducible from
`MutC3Counter.files/{build.py,detect.py,mutants.py,run_matrix.py,pristine.py,receipts_matrix.json}`.

VERDICT: 27/27 behavioural mutants of the C9 condition and the English-page changes killed by the fixture matrix (state-level 25, notes-level 2); control no-op survives — C9 and the C5/C4 English-page rules are behaviourally pinned, with six kills (window arithmetic, date-text-node, block membership, cross-body uniqueness, code-sample headings) reachable only through fixtures outside the frozen corpus.
