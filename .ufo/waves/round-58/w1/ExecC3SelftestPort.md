# ExecC3SelftestPort

Claim C3 counter hardening (counter before data). Ported the round-57 120-check `--selftest` suite onto the round-58 rows
S423/S424 and delivered it as a patch to the derive script plus the generated counter. No lane mutation (read-only git
`show` against the lane only), no installs, no scratch left behind.

## DIFF:

Delivered (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/w1/ExecC3SelftestPort.files/`):

| file | lines | sha256 |
| --- | --- | --- |
| `derive_c58_quote_truth.py` | 987 | `a7a819f650170713f07baf80f52ec95e2f8b1f21ff0081affa1472fa6b83c88e` |
| `c58_quote_truth.py` | 1505 | `f454d90df464bb271ed80300b3d071c4e4863d8ef3f75f375b63a8090b14b66f` |

Derive patch vs `.ufo/waves/round-58/derive_c58_quote_truth.py`, two edits:

- module docstring item (e) now reads "the previous round's suite ported to the two retained round-58 bodies (120 checks)".
- the stub region is replaced: the 12 lines (`# selftest stub until wave 1 …`, stub docstring, `def selftest()` printing
  `not ported yet`, `return 2`) become `body = body[:a] + _SELFTEST_PORT + body[b:]`, with `_SELFTEST_PORT = r'''…'''`
  defined right after `body = src[head_end:]`. Everything else in the derive (round constants, ADOPTED/ROW_URL,
  STAGED_ABSENT, BODY_SHA256, TOPIC, ARTICLE_START/END, receipt tag, `doc`, schema, description) is unchanged.

Generated counter: `diff` against the committed `.ufo/waves/round-58/c58_quote_truth.py` is exactly one hunk
(`@@ -601,13 +601,861 @@`) — the `# ---- selftest` block and nothing else. Deterministic: the delivered derive re-produced
the delivered counter byte-for-byte (measured, `cmp`). The block:

- rows: page `<title>` texts (`搜索问答剧场 【五】“百度蜘蛛”全面解析`, `开发者如何解除封禁百度蜘蛛`), anchors
  `§ 2、Q：如何才能识别当前抓取是正确的百度蜘蛛？ (发布日期 2022-08-19)` and
  `§ 如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？ (发布日期 2020-07-23)` — each heading a raw substring of one
  text node of the article block, page-unique, 4+ units; the printed dates are `发布日期：2022-08-19` / `2020-07-23` in
  those bodies; scope/teaches cells ≥20 chars; recheck 180d/90d; used-by = the derived entry paths.
- lesson Gate lines: URL, access date 2026-10-26, body sha256 + byte count, the row's anchor cell, and one page-unique
  quote carrying 百度蜘蛛 (`A：有两个方式可以判断百度蜘蛛。` 13 units; `正确识别和获取百度蜘蛛，` 11 units).
- entries: every quoted span is a raw substring of a single article-block text node (verified with `span_tools.py` and by
  the counter's own `text_segments`/`in_content`), ≥3 page-unique 6+ unit spans each, one carrying the subject, ceilings
  respected; receipts tagged `kake-shokunin-round58`; sandbox repos under `TMPDIR` with the `rev-parse --show-toplevel`
  assertion and `-c user.name=selftest -c user.email=selftest@local`.
- composition = 120 checks: 112 cases (`pass` baseline + 111 fixtures, 105 in the kill matrix), 5 unit-rule checks,
  2 exit-code checks (unreadable base rev → 2, argparse error → 64), 1 kill-matrix coverage check.

Deviations from a literal port (each measured, not stylistic):

- `fail_staged_name_survives_taxonomy` → `fail_staged_name_survives_identification` (one STAGED_ABSENT path this
  round, not two).
- `fail_staged_name_survives_recognition` → `fail_entry_span_from_sibling_body` (see UNPORTED).
- `fail_style_css_span` → `fail_row_title_other_page` (see UNPORTED).
- `fail_entry_nonunique_verbatim_spans` → `fail_entry_two_unique_spans_one_shared` (two page-unique spans + the shared
  6-unit span `封禁百度蜘蛛`): the literal port carried zero unique spans, and a mutant with entry page-uniqueness
  disabled still scored 120/120, so the fixture did not bind that clause.
- `fail_anchor_heading_not_in_body_dual` → `fail_anchor_heading_not_page_unique` (in-content heading `封禁百度蜘蛛`,
  5 occurrences in that body): same reason — the anchor page-uniqueness mutant survived the literal port.
- `fail_char_ceiling_44_chars_25_units` → `fail_char_ceiling_44_chars_under_unit_ceiling` (the round-58 44-character
  span carries 5 units; the assertion `units(span) <= UNIT_CEILING < len(span)` is kept).

## SELFTEST RUN:

Shared clone of the lane at contract commit `fff3eea6aa349c8635fd84a791cc32de350ee1c2`
(`/fast/scratch/hyaku/kake-r58/ExecC3SelftestPort/lane`, HEAD = that commit, `git rev-parse --show-toplevel` = the clone,
working tree otherwise clean):

```
cd /fast/scratch/hyaku/kake-r58/ExecC3SelftestPort/lane && \
TMPDIR=/fast/scratch/hyaku/kake-r58/ExecC3SelftestPort \
KAKE_R58_SELFTEST_REV=fff3eea6aa349c8635fd84a791cc32de350ee1c2 \
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/w1/ExecC3SelftestPort.files/c58_quote_truth.py --selftest
```

Output: `c58 quote-truth selftest: 120/120 (fixture revision fff3eea6aa34, baseline conditions 8/8, 105 fixtures in the
kill matrix)` — RC=0, no `FAIL` lines. The baseline sandbox passes 8/8 conditions; every red fixture exits 1 (2 for
`fail_bad_receipts`) and each turns its tabled condition red.

Clause-mutation probes, each applied to the delivered counter and run through the same selftest (all killed — the suite
goes red, and the named fixture is the one that reports it):

| mutant | score | fixture that fires |
| --- | --- | --- |
| anchor page-uniqueness removed | 119/120 | `fail_anchor_heading_not_page_unique` (note absent) |
| entry page-uniqueness removed | 119/120 | `fail_entry_two_unique_spans_one_shared` (exit 0) |
| Gate page-uniqueness removed | 118/120 | `fail_gate_quote_shared_with_sibling`, `fail_m408_gate_own_duplicate` |
| body digest freeze removed | 119/120 | `fail_body_swapped_with_receipt` (note absent) |
| 25-unit ceiling removed | 119/120 | `fail_m408_unit_ceiling_26_units` (exit 0) |
| article-block containment removed | 115/120 | nav/footer/promo/sidebar span fixtures (exit 0) |
| 40-character ceiling removed | 116/120 | character-ceiling fixtures (exit 0) |
| TOPIC changed to a non-subject | 113/120 | baseline fails (0/8), Gate/entry subject notes |
| staged-name check removed | 119/120 | `fail_staged_name_survives_identification` (exit 0) |

Note measured, not assumed: the round-57 suite also scores 120/120 under the anchor page-uniqueness mutant, i.e. that
clause was already unbound there; the port now binds it. `fail_bad_receipts` is the only exit-2 fixture; all other red
fixtures are exit 1.

## UNPORTED:

- `fail_style_css_span` (r57) — the two round-58 article blocks carry no `<style>`/`<script>` body to quote from
  (measured: 0 `<style>` elements in both pages, and no script block between `class="article-info"` and the end marker
  `往期回顾`/`推荐阅读`), so the "CSS body excluded even inside the window" case has no real-body sample. Replaced by
  `fail_row_title_other_page` (S423 row carrying the S424 page title), which keeps the fixture count at 111.
- `fail_staged_name_survives_recognition` (r57's second staged-name fixture) — round 58 freezes a single
  `STAGED_ABSENT` path (`corpus/knowledge/baidu-crawler-identification.md`), so its only literal port is the duplicate
  `fail_staged_name_survives_identification`. Replaced by `fail_entry_span_from_sibling_body` (an S423-only span quoted
  inside the S424 entry must be refused as not a raw substring of that body).
- Nothing else was unported and no check was reported unrun: 109 of the 111 round-57 fixtures ported with their
  semantics (spans, locators and titles swapped to S423/S424); the remaining 6 case names are the two replacements and
  the four renames listed under DIFF.
- Out of scope for this seat and therefore not run: the lane's build/lint/test gate (parent owns post-integration),
  any `git`/`jj` mutation in the lane, and any install (none was needed).

Scratch `/fast/scratch/hyaku/kake-r58/ExecC3SelftestPort` deleted after copying the two receipts into `.files/`; the
delivered derive reproduces the delivered counter byte-for-byte (verified before deletion).

VERDICT: 120/120 green — ported suite delivered as derive patch + generated counter (single selftest-block hunk, deterministic), 109/111 r57 fixtures ported, 2 replacements + 4 renames documented, 9/9 clause mutants killed.
