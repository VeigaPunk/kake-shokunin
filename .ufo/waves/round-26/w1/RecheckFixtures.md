# RecheckFixtures: round-26 text_of/normalize selftest

Seat: `KakeR25.RecheckFixtures-6` (executor). Milestone `r26-recheck-build`. Axes: freshness, operability.

## Deliverable

- `.ufo/waves/round-26/sandbox-tests/text_selftest.py` (9,860 bytes). Standard library only. Writes nothing (`sys.dont_write_bytecode`). Root is derived from `__file__`, so no arguments are needed. Prints one JSON line: `{schema: "kake-r26-text-selftest-v1", python, passed, total, failed[], rows[{case, passed, detail}]}`. Exit 0 if all pass, else 1.
- **Not executed**, per assignment. Every outcome below is a prediction from reading `source_text.py`, `scripts/accessibility_packet.py` and the retained manifests. L1 must run it once: `python3 .ufo/waves/round-26/sandbox-tests/text_selftest.py`.

## Test list (73 rows)

### A. Synthetic `text_of` cases (29)
- Skip tags (10): `skip_script`, `skip_style`, `skip_noscript`, `skip_template`, `skip_uppercase_tags`, `skip_nested_noscript_template`, `skip_nested_template`, `skip_style_inside_template`, `skip_stray_end_tags_do_not_underflow`, `skip_html_comment`.
- Entities (5): `entities_named_and_numeric`, `entities_nbsp_and_copy`, `entities_unknown_left_alone`, `entities_amp_lt_decoded_once`, `entities_amp_amp_decoded_once`.
- HTML block whitespace (1): `html_block_gap_collapses`.
- Passthrough, sniffing, empty (8): `plain_whitespace_and_punctuation`, `plain_entities_and_tags_untouched`, `plain_script_not_skipped`, `json_passthrough`, `empty_input`, `content_type_case_insensitive`, `sniff_doctype_without_content_type`, `sniff_html_without_content_type`.
- Invalid UTF-8 (5): `utf8_invalid_byte_plain`, `utf8_overlong_and_stray_continuation`, `utf8_truncated_sequence`, `utf8_invalid_in_html`, `utf8_invalid_run`. Each case calls `text_of` twice and requires both results to equal the expected string.

### B. `normalize` literals (6)
`normalize_whitespace_and_punctuation`, `normalize_unicode_whitespace`, `normalize_paren_spacing`, `normalize_inner_punctuation_kept`, `normalize_blank_is_empty`, `normalize_square_bracket_spacing_as_accessibility_packet`.

### C. Differential (1)
`normalize_matches_accessibility_packet`: 10 inputs compared with `scripts/accessibility_packet.py:normalized`.

### D. Corpus (37)
- `retry_supersedes_failed_attempt_only`: every `manifest-retry.json` key must replace a `manifest.json` entry whose status is not 200.
- `effective_fetches_status_200_without_error`.
- `text_views_are_exactly_the_effective_fetches`: the 34 `fetched/text/*.txt` names equal the 34 effective keys.
- `fetch_view:S0NN-N` (34 rows). For each effective fetch: sha256 and byte length of `gunzip(raw)` match the manifest, and the text view bytes equal `text_of(gunzip(raw), manifest content-type) + "\n"`.

## Predicted outcome (by reading, not run)

Predicted FAIL: 4 rows, from 2 root causes.

1. **Double HTML unescape.** `source_text.py:13` builds `HTMLParser(convert_charrefs=True)`, so character references are decoded once during parsing. `source_text.py:42-43` then runs `html.unescape` again on the joined text. Consequences: `&amp;lt;` becomes `<` (expected `&lt;`), and `&amp;amp;` becomes `&` (expected `&amp;`). Rows: `entities_amp_lt_decoded_once`, `entities_amp_amp_decoded_once`.
2. **Closing-bracket class differs.** `source_text.py:32` uses `[,.;:)\]]`. `scripts/accessibility_packet.py:25` uses `[,.;:)]`. So `x [ y ] z` becomes `x [ y] z` in `source_text`. Rows: `normalize_square_bracket_spacing_as_accessibility_packet`, and `normalize_matches_accessibility_packet`. The mismatching inputs there are `x [ y ] z`, `a ] b` and `end ]`. Controls `a [b] , c` and `p(q ) r : s ; t . u` agree.

Predicted PASS: the other 69 rows, including all 34 `fetch_view` rows. The peer report `w1/FetchCritic.md` states 34/34 equality. I did not rely on that claim and did not compute it myself.

## Evidence gathered (read-only)

- **Text view convention.** The last bytes of `S001-1.txt`, `S002-1.txt`, `S016-1.txt` and `S008-1.txt` are a single non-space character followed by `\n`, with no CR. The test therefore requires exactly one trailing LF after `text_of` output. This convention is not written in `source_text.py`.
- **Effective fetches.** `manifest.json` has 34 entries (S001 and S002 each have two URLs). S008-1 in the manifest has `status: null`, `error: "TimeoutError: The read operation timed out"`, `bytes: 0`. `manifest-retry.json` supersedes it with `S008-1-retry.raw.gz`, status 200, 512,359 bytes, reason "first attempt TimeoutError at 60s; single retry with 240s timeout". All other manifest entries have status 200, error null, and a content-type header.
- **Raw-byte upper bounds.** These regex counts run over gunzipped effective raw bytes, including attributes and scripts, so they are not text-node evidence.
  - `&amp;` followed by a named or numeric reference: S002-1 1, S012-1 10, S024-1 2, S026-1 12, S031-1 5. These are candidate sites for defect 1.
  - Whitespace before `]`: S007-1 3, S010-1 74, S017-1 2, S024-1 1, S025-1 1, S028-1 74, S029-1 34, S033-1 74, S034-1 8. These are candidate sites for defect 2.
- **No retained generator.** Nothing in round-26 writes `fetched/text/*.txt` or `manifest-retry.json`. `fetch_sources.py` writes only `manifest.json`, hard-codes `timeout=60`, and has no text step. `source_text.py` has no CLI. The `fetch_view` rows are therefore the only reproducible check of the committed views.

## Why the corpus rows cannot catch the two defects

The committed views were produced by the same `text_of`. Defect 1 and defect 2 are therefore frozen into the view bytes, and the equality rows still pass. Only the synthetic rows detect them. Fixing either defect changes view bytes for the candidate rows above, and requires regenerating the views and re-running the quote-binding gate. That decision belongs to L1. I changed no production file.

## Risks and caveats

- Not executed. The predictions depend on CPython `HTMLParser` behaviour under the interpreter in use, Python 3.14.8 (`python3 --version`). The cases avoid nested `<script>` and unclosed raw-text elements, which differ between `HTMLParser` releases. `skip_nested_template` assumes `<template>` is not a raw-text element. I believe this holds per the HTML spec, but I did not check it against the 3.14.8 source.
- `text_of` treats any body starting with `<html` or `<!doctype` as HTML, even under `text/plain` (`source_text.py:37`). This is untested because the intended behaviour is ambiguous.
- The expectation that `b'x\xe2\x82'` yields one U+FFFD relies on CPython's maximal-subpart replacement. It is asserted, not observed.
- `fetch_view:S008-1` reads the retry only because the test honours `manifest-retry.json`. Without that file, the empty-body first attempt would be used.
- The write tool set the executable bit on the test file because it has a shebang.

## Tooling

No tool was installed, upgraded or removed. I used the existing `python3` 3.14.8, `od` and `tail`, and one read-only Python count that wrote no files. No network access, no site probing, nothing written to `/tmp`.

## Commands for L1

- `python3 .ufo/waves/round-26/sandbox-tests/text_selftest.py`. Expect exit 1 with the 4 predicted failures. Any other failure is a real finding to investigate.
- Keep the single JSON line as the selftest artifact.
