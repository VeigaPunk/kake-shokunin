# ExecC3SelftestPort

Leaf seat, claim C3. Wrote the ported selftest for the round-59 C3 counter and ran it. Nothing here scores the claim
(no after-state): the baseline fixture is synthetic best-evidence, not landed evidence.

**Artifact:** `.ufo/waves/round-59/w1/ExecC3SelftestPort.files/c59_quote_truth.py` (89,934 bytes) — a copy of the working-tree
counter whose `selftest()` (and the fixture helpers it needs) is ported from `.ufo/waves/round-58/c58_quote_truth.py`;
`run_checks` is byte-identical (see DIFF). Receipts: `.files/selftest-run.txt` (verbose run), `.files/v1-counter-probe.txt`.

**Counter under test:** `.ufo/waves/round-59/c59_quote_truth.py`, working tree, sha256 `7430841144fa…4df5`, 743 lines, mtime
2026-10-26 22:56. The contract-committed blob (`HEAD:…/c59_quote_truth.py`, 735 lines) is version 1; the working tree carries
version-2 amendments (diff vs HEAD: C5 title floor 6→3 units; `<style>/<script>` bodies excluded from the printed-revision
check; `article_headings` excludes `<pre|code|script|style>`; C9 "inserted where the stale bullet ends" + "rendered prose").
The selftest was run against both (v2 = the copy delivered; v1 = a probe, see COUNTER DEFECTS).

**Fixture:** 108 fixtures (103 red, 5 green) + 11 unit checks + 1 baseline = 120 checks. Every quoted span is a byte-exact
substring of one whitespace-collapsed text node of the article block of the sha256-pinned retained bodies, and each is
re-asserted at fixture-build time against the counter's own `units`/`text_segments`/`content_window` (`need()` aborts with
exit 2 rather than silently weakening a case). Fixture git repos live under `/fast/scratch/hyaku/kake-r59/ExecC3SelftestPort/`,
are toplevel-asserted, committed only with `-c user.name=selftest -c user.email=selftest@local`, and removed per case.
Run: `python3 -B .ufo/waves/round-59/w1/ExecC3SelftestPort.files/c59_quote_truth.py --selftest` (from the lane root; no env needed).

## CASES

Red fixtures are attributed by the note they *add* relative to the baseline, so a fixture that turns red on the wrong condition is caught.

| case | condition targeted | result |
|---|---|---|
| `baseline (all-correct evidence)` | 9/9 + exit 0 | PASS |
| `fail_missing_entry_signals` | C1_entries_exist | PASS (exit 1) |
| `fail_staged_candidate_name_survives` | C1_entries_exist | PASS (exit 1) |
| `fail_no_source_header` | C2_entry_provenance | PASS (exit 1) |
| `fail_source_line_drops_url` | C2_entry_provenance | PASS (exit 1) |
| `fail_no_cite_below_header` | C2_entry_provenance | PASS (exit 1) |
| `fail_verified_at_wrong_date` | C2_entry_provenance | PASS (exit 1) |
| `fail_recheck_junk_cadence` | C2_entry_provenance | PASS (exit 1) |
| `fail_row_short` | C3_row_shape | PASS (exit 1) |
| `fail_row_status_not_mined` | C3_row_shape | PASS (exit 1) |
| `fail_new_row_already_in_base` | C3_row_shape | PASS (exit 1) |
| `fail_used_by_missing_stale_doc` | C4_used_by | PASS (exit 1) |
| `fail_gate_quote_fabricated` | C5_quote_truth | PASS (exit 1) |
| `fail_gate_quote_outside_content` | C5_quote_truth | PASS (exit 1) |
| `fail_gate_quote_char_ceiling_161` (English) | C5_quote_truth | PASS (exit 1) |
| `fail_gate_quote_unit_ceiling_26` | C5_quote_truth | PASS (exit 1) |
| `fail_gate_quote_twice_in_body` | C5_quote_truth | PASS (exit 1) |
| `fail_gate_quote_shared_with_sibling` | C5_quote_truth | PASS (exit 1) |
| `fail_gate_missing_sha` | C5_quote_truth | PASS (exit 1) |
| `fail_gate_quote_off_topic` | C5_quote_truth | PASS (exit 1) |
| `fail_gate_curly_quote` | C5_quote_truth | PASS (exit 1) |
| `fail_span_crosses_text_node_boundary` (English) | C5_quote_truth | PASS (exit 1) |
| `fail_nav_span_outside_article_block` (English) | C5_quote_truth | PASS (exit 1) |
| `fail_footer_only_span` (English) | C5_quote_truth | PASS (exit 1) |
| `fail_entry_quote_char_ceiling_161` (English) | C5_quote_truth | PASS (exit 1) |
| `fail_entry_quote_unit_ceiling_26` | C5_quote_truth | PASS (exit 1) |
| `fail_entry_without_topic_span` | C5_quote_truth | PASS (exit 1) |
| `fail_entry_curly_quote` | C5_quote_truth | PASS (exit 1) |
| `fail_row_title_substring_only` | C5_quote_truth | PASS (exit 1) |
| `fail_anchor_not_h2_or_h3` (English) | C5_quote_truth | PASS (exit 1) |
| `fail_anchor_date_mismatch` | C5_quote_truth | PASS (exit 1) |
| `fail_anchor_heading_inside_code_sample` (v2) | C5_quote_truth | PASS (exit 1) |
| `fail_printed_revision_only_in_script` (v2) | C5_quote_truth | PASS (exit 1) |
| `fail_body_edited` | C5_quote_truth | PASS (exit 1) |
| `fail_receipt_sha` | C6_receipt_pins | PASS (exit 1) |
| `fail_receipts_not_json` | C6_receipt_pins | PASS (exit 2) |
| `fail_validate_exit` | C7_validate_before_append | PASS (exit 1) |
| `fail_validate_e04_finding` | C7_validate_before_append | PASS (exit 1) |
| `fail_validate_root_argv` | C7_validate_before_append | PASS (exit 1) |
| `fail_validated_entry_differs` | C7_validate_before_append | PASS (exit 1) |
| `fail_mirror_not_base` | C8_mirror_bytes | PASS (exit 1) |
| `fail_pin_null` | C8_mirror_bytes | PASS (exit 1) |
| `fail_mirror_added_in_measured_commit` | C8_mirror_bytes | PASS (exit 1) |
| `fail_c9_stale_line_rewritten` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_stale_line_deleted` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tail_twenty_lines_away` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tail_appended_at_eof` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tail_without_tag` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tag_inside_html_comment` (v2) | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tail_without_s425` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_citation_inside_code_span` (v2) | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tail_span_not_in_page` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tail_span_without_ip_address` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_quote_inside_html_comment` (v2) | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tail_curly_quotes` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tag_wrapped_with_indent` (v2, false red) | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_tag_hidden_in_html_attribute` (v2) | C9_stale_claim_corrected | **FAIL (exit 0)** |
| `fail_c9_quote_hidden_in_html_attribute` (v2) | C9_stale_claim_corrected | **FAIL (exit 0)** |
| `fail_c9_stale_line_duplicated` | C9_stale_claim_corrected | PASS (exit 1) |
| `fail_c9_bullet_ends_beyond_window` | C9_stale_claim_corrected | PASS (exit 1) |
| `pass_census_relative_argv`, `pass_unrelated_source_body_present`, `pass_span_160_chars`, `pass_span_25_units`, `pass_c9_bullet_ends_immediately` | green (no new failure) | PASS (exit 0) |

Unit rules (11, all PASS): Latin per word, halfwidth kana per char, non-BMP CJK per char; S425 title = 5 units and clears the v2
3-unit floor, a two-word title is below it; 26 units > 25, 161 chars > 160, 160 chars and 25 units sit on the ceilings; unreadable `--base` is unevaluable (exit 2); argparse error exits 64.

## TALLY

`118/120` (baseline 1, fixtures 108, unit 11), exit 1. Baseline: exit 0, **9/9 conditions pass** on the best-evidence
fixture against the v2 counter. The 2 failures are the two false-green routes below, not fixture errors: every one of the
other 103 red fixtures turned red on its own condition and added no other check.

## COUNTER DEFECTS FOUND

1. **D1 (v2, false green, open).** C9's "rendered prose" rule strips only `<!--…-->` and backtick code spans, not other
   markup, so a correction whose required token sits *inside an HTML tag attribute* passes C9. Case
   `fail_c9_tag_hidden_in_html_attribute` puts `<span data-note="[r59-correction 2026-10-27]"></span>` in the inserted block
   (tag not rendered at all) → counter exit **0**, C9 green. Case `fail_c9_quote_hidden_in_html_attribute` does the same with
   the required quoted span (`<span title='"The source IP address of the request."'>`) → exit **0**, C9 green. The same hole
   admits a hidden `S425` citation. Fix direction: strip all tags/attributes before testing, or test only text nodes of the
   rendered block.
2. **D2 (v2, false red, minor, open).** The block maps `\n`→`" "` but not the continuation indent, so a tag or span wrapped
   onto an *indented* continuation line is rejected although its rendered prose carries it: `fail_c9_tag_wrapped_with_indent`
   reds with "no line inserted where the stale bullet ends carries [r59-correction 2026-10-27] as rendered prose". Fails safe
   (over-strict), but it forbids a faithful wrapped correction.
3. **D3 (v1, fixed in v2).** v1's C5 demanded a 6-unit row title; S425's `<title>` ("Google Crawler (User Agent) Overview")
   is 5 units, so C5 was unsatisfiable and 9/9 unreachable. Probe against the contract-committed v1 blob scores this same
   fixture **8/9, exit 1**, with exactly `S425: row title 'Google Crawler (User Agent) Overview' is not the page's <title>
   text … (6+ units)` (`.files/v1-counter-probe.txt`). v2 (3 units) scores it 9/9; the selftest pins both sides (5-unit title
   passes, 2-word title fails).
4. **D4 (v1, fixed in v2).** v1's printed-revision check counted `<script>` bodies as text, so a page printing `Last updated
   <date> UTC` only inside a script passed; v2 reds it (`fail_printed_revision_only_in_script`), and v1 does not.

Contract note (not a defect; counter and `contract.md` C9 agree with each other): the claim prose says "append-only tail"
while C9 requires the insertion **exactly where the stale bullet ends**, so a literal end-of-file append fails
(`fail_c9_tail_appended_at_eof`, `fail_c9_tail_twenty_lines_away`). The C3 builder must insert mid-document.

## DIFF

Only `selftest()` and its helpers changed; `run_checks` byte-identical.

- `run_checks` slice (from `def run_checks(` to the selftest banner): identical, 25,069 bytes, sha256
  `39e5e1a273e1310cef68696b6e6c43dbc9dd1d32968706cadbd9496148450b16`.
- Everything before that banner (docstring, PREDICATE, all constants, all shared helpers) and everything from
  `def main() -> int:` onward: identical.
- Unified diff is confined to `@@ -679,12 +679,1016 @@`: +1008 / −4 lines; the 4 removed lines are v1's stub comment and
  its `print(...)/return 2` body. Counter 743 → copy 1747 lines.
- Added: `selftest()` + fixture helpers (`_selftest_lane_root`, `_selftest_retained`, `_selftest_base_doc`, `_selftest_tmp`,
  `_fx_row`, `_fx_entry`, `_fx_lesson`, `_build`, `_bullet_end`, `_stale_measured`, `_long_bullet_base`, `_short_bullet_base`)
  and the byte-exact fixture spans asserted against the retained bodies.

## Notes / risks

- The counter changed under this seat mid-wave: v1 (contract-committed) → v2 (working tree, 22:56). D1/D2 are against v2; if
  the counter moves again, re-run the artifact (fixture spans are asserted, so drift fails loudly rather than silently).
- `_bullet_end` replicates C9's bullet-end rule on the fixture side; the green baseline plus
  `pass_c9_bullet_ends_immediately`/`fail_c9_bullet_ends_beyond_window` pin that replica.
- Scratch `/fast/scratch/hyaku/kake-r59/ExecC3SelftestPort/` was removed after copying receipts. No tool installs (none
  needed). No lane git/jj mutation, no file written outside the report and `.files/`.
- Unrun here (parent owns post-integration gates): the counter against the landed round-59 evidence, and every scoring run.

VERDICT: Ported selftest delivered and run — 118/120, baseline 9/9 on v2; two real v2 C9 false-green routes (tokens hidden in HTML attributes) and two already-fixed v1 defects (title floor, script-body revision).
