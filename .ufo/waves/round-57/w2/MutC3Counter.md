# MutC3Counter-3

Mutation probe of the C3 counter `.ufo/waves/round-57/c57_quote_truth.py`, read at lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` (working tree verified byte-identical to that pin before the run).
Method: copy to `/tmp/mutc3/scratch/pristine.py`; baseline `KAKE_R57_SELFTEST_REV=b9a5d012f7fd python3 -B pristine.py --selftest`
from the lane root = **101/101, exit 0** (fixture revision b9a5d012f7fd, baseline conditions 8/8).
38 single-point mutants, each an exact one-occurrence string replacement; every mutant run twice
(bare, and with the 6 probe fixtures of the `m408` family inserted); plus 2 dedicated F8 validations.
All confirmed by running. Line numbers below refer to the pinned revision.

MUTANTS:

| ID | Point (line) | Single-point change | Result | Killed by |
|----|--------------|---------------------|--------|-----------|
| M01 | `text_segments` (182) | style/script regex drops `<script>` | SURVIVED | — (see SURVIVORS) |
| M02 | `text_segments` (182) | drops `<style>` | KILLED | `fail_style_css_span` |
| M03 | text-node regex (183) | `[^<>]` → `[^<]` (allows `>` in node) | SURVIVED | — |
| M04 | text-node regex (183) | drops `(?=<)` lookahead | SURVIVED | — |
| M05 | `ARTICLE_START` (95) | S421 marker made bogus | KILLED | baseline `pass` |
| M06 | `ARTICLE_END` (96) | S421 end → `class="footer"` (widens over promo block) | KILLED | `fail_anchor_sidebar_heading` |
| M07 | `content_window` (172) | end searched from 0 instead of `lo + 1` | KILLED | baseline `pass` (S422 first end hit @9102 < lo @9199) |
| M08 | `content_window` (172) | `lo + 1` → `lo` | SURVIVED | — |
| M09 | `in_content` (188) | raw substring of whole body | KILLED | `fail_nav_span_outside_content` |
| M10 | `in_content` (188) | `any` → `all` | KILLED | baseline `pass` |
| M11 | `in_content` (188) | `sid` cross-wired to `'S421'` | KILLED | baseline `pass` |
| M12 | `BODY_SHA256` check (347) | digest compared against itself | KILLED | `fail_body_swapped_with_receipt` |
| M13 | `BODY_SHA256` check (347) | `!=` → `==` | KILLED | baseline `pass` |
| M14 | title check (350) | drop `title != page_title` | KILLED | `fail_row_title_unspaced` |
| M15 | `page_title` (349) | drop `split("_")[0]` | KILLED | baseline `pass` |
| M16 | title floor (350) | `units(title) < 6` → `< 2` | SURVIVED | — |
| M17 | anchor floor (364) | `units(anchor) < 4` → `< 1` | SURVIVED bare | **F1** |
| M18 | anchor check (364) | drop `in_content` conjunct | KILLED | `fail_anchor_sidebar_heading` (`推荐阅读` is count-1 in S421) |
| M19 | date text node (356) | `in_content` → raw substring | SURVIVED | — |
| M20 | date text node (356) | check dropped (`elif False:`) | KILLED | `fail_anchor_date_mismatch` |
| M21 | anchor-cell date regex (353) | `[：: ]` → `:` (fullwidth refused) | KILLED | `fail_anchor_date_mismatch` + `pass_anchor_fullwidth_colon_date` |
| M22 | Gate `allq` filter (395) | short-quote filter dropped | KILLED | `pass_gate_extra_short_quote` (`"200"` absent from S422 body) |
| M23 | Gate spans floor (396) | `>= 6` → `>= 4` | SURVIVED bare | **F2** |
| M24 | Gate curly check (393) | dropped | KILLED | `fail_gate_curly_quote` (curly span is not ASCII-quoted, so no verify backstop) |
| M25 | Gate own-count clause (404) | `or any(text.count(q) != 1 ...)` dropped | SURVIVED bare | **F6** |
| M26 | `others` set (371) | drop `if k != sid` (self included) | KILLED | baseline `pass` |
| M27 | `others` set (371) | `others = []` | SURVIVED | — |
| M28 | entry unique floor (425) | `< MIN_UNIQUE_SPANS` → `< 1` | KILLED | `fail_entry_two_unique_spans` |
| M29 | entry unique conjunct (423) | drop `not any(span in t for t in others)` | SURVIVED | — |
| M30 | `CHAR_CEILING` (89) | 40 → 45 | SURVIVED bare | **F8** |
| M31 | character ceiling (377) | `>` → `>=` (boundary) | SURVIVED bare | **F3** |
| M32 | `UNIT_CEILING` (74) | 25 → 26 | SURVIVED bare | **F4** |
| M33 | C4 used-by (326) | comparison dropped | KILLED | `fail_used_by_*` (4 fixtures) |
| M34 | C4 want (324) | `+ [path]` dropped | KILLED | baseline `pass` |
| M35 | `used_by` split (159) | `[,;]` → `,` | SURVIVED | — |
| M36 | C8 append-only restore (550) | check dropped | KILLED | `fail_not_append_only_cell_dual` |
| M37 | C8 strict-earlier (561) | `add_commit == rev` check dropped | SURVIVED | — |
| M38 | C8 add-blob rows (570) | `sid in parse_registry(add_blob)` dropped | SURVIVED | — |

Score: 21 killed by the existing suite, 6 more killed by probe fixtures (27/38), 11 survivors.

SURVIVORS: (all confirmed by running; each is a coverage finding, not a contract change)

- **M01** — no `<script>` body lies inside either article window at b9a5d012f7fd (style-only removal yields an identical
  segment set, verified). Bodies are frozen by `BODY_SHA256`, so no fixture can synthesize one. Equivalent on frozen evidence.
- **M03 / M04** — the loose regexes produce segment sets identical to `>([^<>]+)(?=<)` on both windows (no `X>Y<` region,
  no tail text after the last `>`); verified by set difference. Frozen bodies → no fixture.
- **M08** — `find(end, lo)` vs `find(end, lo+1)`: no end marker starts exactly at `lo` (S421 end @20418 vs lo @9346;
  S422's first end hit @9102 precedes lo @9199 and is skipped either way). Identical window, byte-level argument.
- **M16** — the 6-unit title floor is unreachable: the equality conjunct pins `title` to the real `<title>` text
  (15/17 units), so lowering the floor changes nothing. Redundant conjunct given `title != page_title`.
- **M19** — `发布日期：<date>` occurs exactly once per body (S421 @9443, S422 @9222), already inside a content text node,
  so raw-substring and `in_content` agree on the frozen bodies.
- **M27** (`others = []`) — a kill needs a 6+-unit Gate span occurring once in its own body and also in the sibling.
  Exhaustive search over in-content 6–10-CJK runs: none exists; the existing sibling fixture's span `搜索资源平台`
  occurs 7× in S421 and is caught by the own-count clause regardless. Unkillable on frozen bodies.
- **M29** (entry sibling-exclusion dropped) — a kill needs ≥3 entry spans, each once-in-S421, in-content, 6–25 units,
  present in S422. SequenceMatcher over all shared ≥12-char blocks of the two bodies: 0 qualifying spans. Unkillable here.
- **M35** (`;` dropped from used_by split) — C4's `want` is always exactly one path (`PRIOR_USED_BY` empty), so `,` vs
  `,;` never separates two authorable verdicts. No fixture can distinguish them.
- **M37** — `_build` always commits `MIRROR` in the pre-append commit, so the mirror add-commit is never the tip;
  the strict-earlier condition is unreachable for any fixture in this harness.
- **M38** — the mirror is added exactly once and never modified, so the add-commit blob always equals `mirror_text`,
  which the earlier `sid in mirror_rows` loop already rejects; the branch is redundant in this harness.

Incidental finding: existing fixture `fail_char_ceiling_44_chars_25_units` quotes a **46-char / 15-unit** span — its name
is off by 2 chars and 10 units. It still kills 40→44 tightenings, but left the 41–45-char band untested (that is exactly
why M30 survived until F8). Rename suggested; no behavior change.

PROPOSED FIXTURES: (validated: added to the pristine copy the suite stays green — 107/107 exit 0 for F1–F6, 102/102 for
F8 — and added to the named mutant the suite goes red on exactly that fixture)

```python
    # --- MutC3Counter-3 probe fixtures (round-57 w2 mutation probe)

    @case("fail_m408_anchor_floor_three_units")                     # kills M17; red: C5_quote_truth
    def _(f): dual(f, REGISTRY, row(f, "S421"), row(f, "S421").replace("§ 一、了解死链", "§ 一定是"))
    # `一定是` is 3 units, page-unique and inside an article text node; only the 4-unit floor rejects it.

    @case("pass_m408_gate_span_floor_five_units", 0)                # kills M23 (no kills row: want=0)
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g + ' and "不支持目录"')
    # 5 units, in content, page-unique: legal under the suite, flagged by M23's 6..25 band check.

    @case("pass_m408_char_ceiling_boundary_40", 0)                  # kills M31 (no kills row: want=0)
    def _(f): add_entry_line(f, "S421", '\n> "面URL时，因为URL中有不规则字符，或者URL与后边的文字链接起来，导致URL"\n')
    # exactly 40 chars, 25 units, page-unique, in content: legal at 40 > ceiling, flagged at >= ceiling.

    @case("fail_m408_unit_ceiling_26_units")                        # kills M32; red: C5_quote_truth
    def _(f): add_entry_line(f, "S422", '\n> "在这我们不得不再提一下百度站长平台链接提交中的主动推"\n')
    # 26 CJK chars = 26 units, page-unique, in content: red under the 25-unit ceiling, green at 26.

    @case("fail_m408_promo_span_outside_content")                   # kills end-marker widening; red: C5_quote_truth
    def _(f): add_entry_line(f, "S421", '\n> "推荐阅读"\n')
    # promo-block heading at 21251, between the article end marker (20418) and the footer (21828);
    # independent of the anchor path that already kills M06.

    @case("fail_m408_gate_own_duplicate")                           # kills M25; red: C5_quote_truth
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g + ' and "学习如何快速处理网站死链"')
    # 12 units, in content, occurs twice in S421 and not at all in S422: only the own-count clause rejects it.

    @case("fail_m408_char_ceiling_41_chars")                        # kills M30; red: C5_quote_truth
    def _(f): add_entry_line(f, "S421", '\n> "，比如您的网站为example.com，您已制作了一个silian_ exampl"\n')
    # 41 chars / 15 units, page-unique, in content: red at ceiling 40, green at 45 (validated M30 101/102 -> killed).
```

F1–F6 + pristine: 107/107, exit 0 (every probe behaves as authored). F8 + pristine: 102/102, exit 0.
F1+M17, F2+M23, F3+M31, F4+M32, F6+M25, F8+M30: each run ends `FAIL <that fixture>` / exit 1 — mutant killed.

Restoration: the lane copy of `c57_quote_truth.py` was never written; sha256
`7aa66297b48ba259e5f7e239ccd3412b1a008141a17000e4f71ad5d39dcb2049` before, during and after all runs, identical to the
`4b8c730` blob. All mutants/variants lived in `/tmp/mutc3/scratch` (disposable); no lane path, jj state or Git index
was touched; fixture repos were created by the selftest under `tempfile.mkdtemp` with the selftest identity.

VERDICT: 38 single-point mutants of the version-2 counter — 27/38 killed (21 by the existing selftest, 6 by 7 validated
probe fixtures), 11 survivors all proven equivalent on the frozen bodies or unreachable in the selftest harness; no
counter defect, contract unchanged, suite coverage gaps named and closed by the fixtures above.
