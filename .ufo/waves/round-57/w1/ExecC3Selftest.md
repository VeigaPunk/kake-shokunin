# ExecC3Selftest

Claim C3 (freshness, sourced): the round-56 fixture suite (version 2.1, 86 checks at base `28fa0b2`) ported to the round-57
counter. Ported, not rewritten: the condition code C1..C8 and every counter constant are byte-identical to
`.ufo/waves/round-57/c57_quote_truth.py`; only the `--selftest` stub is replaced. All fixture quotes are raw substrings of the two
retained bodies (`sources/S421.html`, `sources/S422.html`, committed at `b9a5d01`), so the fixtures exercise the same substring /
article-block / page-uniqueness code the counter runs over the landed evidence.

## FILES:

- `.ufo/waves/round-57/w1/ExecC3Selftest.files/c57_quote_truth_selftest.py` — new, 1335 lines, 65756 bytes (the only file written
  besides this report; `__pycache__` from my diagnostic import removed).
  - lines 8-12: a 5-line "Selftest copy" paragraph in the docstring (the only change above the selftest banner);
  - line 592 banner … line 1294 end of `selftest()`: the ported block (fixture constants, `_fx_row()`, `_build()`, `selftest()`
    with the kill matrix inline);
  - counter path unchanged: `--revision 28fa0b23e699303725aba2727094531f5e44494d` output is identical to
    `controls/base-c3-quote-truth.txt` (empty diff against that receipt minus its wrapper-appended duplicate trailing `EXIT=1`).
- Nothing else touched: no lane Git index, no jj, no sibling lane, no fleet repo. Sandbox repos are `mktemp -d` + `git init` with
  `-c user.name=selftest -c user.email=selftest@local`, toplevel asserted equal to the temp dir, removed after each case.
- Tools: none installed, none needed.

## SELFTEST RESULT: 93/93 (exit 0)

```
KAKE_R57_SELFTEST_REV=b9a5d012f7fd python3 -B .ufo/waves/round-57/w1/ExecC3Selftest.files/c57_quote_truth_selftest.py --selftest
c57 quote-truth selftest: 93/93 (fixture revision b9a5d012f7fd, baseline conditions 8/8, 83 fixtures in the kill matrix)
```

- Composition: 87 sandbox fixtures (83 red-expected, 4 green-expected) + 5 unit-rule checks + 1 kill-matrix completeness check.
- Baseline fixture (all conditions pass) reaches **8/8** with `len(results) == 8`, asserted, not inferred from exit 0.
- Red cases: all 83 red-expected fixtures are red, and each turns red **on the condition it is ported for** — the suite asserts the
  named condition reports a note (`kills` matrix), so a fixture that went red incidentally (e.g. via C7) fails the suite. Per
  condition: C1 3, C2 7, C3 9, C4 4, C5 32, C6 10, C7 10, C8 8. The 4 green-expected fixtures (`pass`,
  `pass_census_relative_argv`, `pass_entity_span_raw`, `pass_gate_extra_short_quote`) stay green.
- Attribution was measured, not assumed: a one-off import traced each case's `run_checks` result list (name → failing checks) and
  every case matched the matrix before the assertion was switched on.
- Also run: `--selftest` without the env pin from the lane root (falls back to cwd HEAD `f7c98ff26928`) → 93/93; and in a clean
  `git clone` checked out at `b9a5d012f7fd` → 93/93. Runtime ~5 s.
- Not run: the counter against a landed round-57 build (no entries/rows/lesson/receipts exist yet — the fixture set is synthetic for
  exactly this reason); mutation testing of the counter itself (not this seat's assignment).

## NEW FIXTURES:

Round-57 risks (the c56 Yahoo! fixtures were re-pointed at S421/S422; the held-row S367 cases become "a NEW row that already exists
in the base registry fails", since `HELD_BODY_SHA256 = {}` at round 57 makes the held-body pin vacuous):

| fixture | mutation (real evidence) | kills |
| --- | --- | --- |
| `fail_nav_span_outside_content` | entry quotes `我的溯源提交` — S421 nav item before `class="article-info"` (raw, 6 units, count 1) | C5 (`outside the page's content block`) |
| `fail_footer_span_outside_content` | entry quotes `百度开发者中心` — S421 footer link after `class="footer"` | C5 (same note) |
| `fail_gate_quote_outside_content` | S421 Gate quote replaced by the nav string `我的溯源提交` | C5 |
| `fail_anchor_date_mismatch` | row anchor `(发布日期 2022-09-08)` while the page prints `发布日期：2022-09-09` | C5 |
| `fail_anchor_missing_pub_date` | anchor loses `(发布日期 2022-09-09)` entirely | C5 |
| `pass_entity_span_raw` | entry gains `为什么要及时处理死链&nbsp;？` (entity kept as written) | green |
| `fail_entity_span_decoded` | same span with `&nbsp;` decoded to a space | C5 (`not a raw substring`) |
| `fail_span_crosses_inline_span_tag` | entry quotes `包括协议死链和内容死链`; the raw body carries `<span …><span …><b>` between the halves | C5 (`not a raw substring`) |
| `fail_gate_quote_shared_with_sibling` | S421 Gate quote → `搜索资源平台` (6 units, 7× in S421, 4× in S422) | C5 (`not page-unique`) |
| `fail_entry_nonunique_verbatim_spans` | entry keeps only `搜索资源平台` / `百度搜索资源平台` / `【死链提交】工具` (all repeated) | C5 (<3 page-unique spans) |
| `fail_row_title_unspaced` | S421 row title → staged unspaced `搜索问答剧场【六】死链常见问题解析` (page prints the spaced form) | C5 (title not in body) |
| `fail_staged_name_survives_taxonomy` | `corpus/knowledge/baidu-dead-link-taxonomy.md` created | C1 |
| `fail_staged_name_survives_recognition` | `corpus/knowledge/baidu-spider3-dead-link-recognition.md` created | C1 |
| `fail_new_row_already_in_base` | S421 row appended to the base-revision registry (replaces the S367 held-row cases) | C3 (+C8 mirror carries the row) |
| `fail_used_by_wrong_entry` | S421 `used-by` = the S422 entry (the "entry 1 only" rule) | C4 |
| `fail_anchor_heading_not_in_body` / `_dual` | anchor heading → `存在しない見出し` (S421 names `一、了解死链`, S422 names `死链处理更及时—被黑低质页面全屏蔽` — S422 has no `h` element) | C5 |
| `fail_char_ceiling_44_chars_25_units` / `_dual` | 46-character 15-unit span and a 51-character 1-unit URL beside the 25-unit rule | C5 (character ceiling) |

Dropped from the c56 set, with reasons: `fail_held_body_edited` (no held body is pinned at round 57) and
`fail_entry_only_spans_shared_with_unadopted_body` (round 57 retains exactly two bodies; cross-body uniqueness is exercised by the
two sibling-shared fixtures above). Note for reviewers: S421 and S422 share no plain-text run of 6+ units that occurs exactly once
in S421 (the longest shared run is `百度搜索资源平台`, 8 units, twice in S421), so the sibling-shared fixture uses `搜索资源平台`
(6 units, 7× in S421, 4× in S422), which trips the own-body-count and sibling clauses in a single note.

## INTEGRATION NOTE:

1. In `.ufo/waves/round-57/c57_quote_truth.py`, replace the span from the line
   `# --------------------------------------------------------------------------- selftest` (line 586 in the frozen file, up to but
   not including `def main() -> int:` at line 594) with the identical span from `c57_quote_truth_selftest.py` (line 592 up to but
   not including `def main() -> int:` at line 1297). That span is: `_FX_TITLE`, `_FX_ANCHOR`, `_FX_SCOPE`, `_FX_TEACHES`,
   `_FX_RECHECK`, `_FX_GATE_QUOTE`, `_FX_BASE_REGISTRY`, `_fx_row()`, `_FX_LESSON`, `_FX_ENTRY`, `_build()`, `selftest()` (kill
   matrix inline). Do not copy the docstring paragraph; it is a note for this seat, not a condition.
2. Constants it needs — all already module-level in `c57_quote_truth.py`, none to add: `REGISTRY`, `LESSON`, `RECEIPTS`, `MIRROR`,
   `MIRROR_PIN`, `VALIDATE`, `VALIDATE_REG`, `SOURCES_DIR`, `ADOPTED`, `NEW_ROWS`, `ROW_URL`, `STAGED_ABSENT`, `UNIT_CEILING`,
   `ROUND_DATE`, `BASE_REV`, `ROW_RE`; helpers `git()`, `show()`, `parse_registry()`, `units()`, `set_used_by()`, `run_checks()`;
   imports `hashlib`, `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `tempfile` (all present). The block reads no new lane file.
3. The only lane read is `git show <rev>:.ufo/waves/round-57/sources/S{421,422}.html` (working-tree fallback if absent at `rev`), so
   it scores at any commit carrying the retained bodies: `KAKE_R57_SELFTEST_REV=b9a5d012f7fd python3 -B
   .ufo/waves/round-57/c57_quote_truth.py --selftest` must print `93/93 … baseline conditions 8/8` and exit 0. Without the env var
   it uses the cwd HEAD. `main()` needs no change; the `--revision` path is untouched.
4. Rows and entry paths are generated from `ADOPTED`/`ROW_URL`, so a rename of either carries into the fixtures; only the two
   fixture Gate quotes and the two anchor strings are literal (`协议死链和内容死链`, `启用了全新的死链识别模型`, `一、了解死链`,
   `死链处理更及时—被黑低质页面全屏蔽`) and all four are raw substrings of the retained bodies as committed at `b9a5d01`.
5. Keep the two `assert units(span) <= UNIT_CEILING < len(span)` lines: they are what makes the character-ceiling fixtures fail if
   the ceiling constants ever move.

VERDICT: ported selftest in place and green — 93/93 (87 fixtures: 83 red-expected, each asserted red on its named condition; 4 green; baseline 8/8), identical in a clean clone at `b9a5d012f7fd`; drop-in block is line 592 to just before `def main()` (line 1297) of `w1/ExecC3Selftest.files/c57_quote_truth_selftest.py` with no new constants.
