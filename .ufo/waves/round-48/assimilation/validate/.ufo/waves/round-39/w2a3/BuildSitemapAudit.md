# R39 a3w2 BUILD — scripts/sitemap_audit.py (claim C1)
Seat KakeR39A3.BuildSitemapAudit (leaf). Written from `.ufo/waves/round-39/c1-contract.md` (sentences 1–34) and `.ufo/waves/round-39/sources/` (S102–S104) only; key-blind (no sealed path read, no counter run). No tools installed (none needed).

## Deliverables (L1 copies both into the lane as `scripts/`)
- `sitemap_audit.py` — `/fast/scratch/hyaku/kake-r39a3w2/BuildSitemapAudit/sitemap_audit.py` — 420 lines — sha256 `6d86c8cef78e36d372f7277096ec163cc8f1e919fa66702ad24e5e32f9a240ec`
- `sitemap_audit_selftest.py` — `/fast/scratch/hyaku/kake-r39a3w2/BuildSitemapAudit/sitemap_audit_selftest.py` — 1077 lines — sha256 `99ee9bbfc55f8e3c7a3ce073c0697d0efad573cd6028f44029eb35aac93351db`
Stdlib only; the tool reads the manifest plus the files it names, writes one JSON document to stdout, nothing to stderr, no network, no temp writes.

## Commands and exact results (cwd = the sandbox above)
- `/usr/bin/python3 -B sitemap_audit_selftest.py --tool ./sitemap_audit.py` → `PASS 150/150`, exit 0
- `… --fault-injection` → `PASS 150/150`; `FAULT silent: rejected as expected (0/150)`; `FAULT constant-clean: rejected as expected (57/150)`; exit 0
- `… --tool ./failing_silent.py` (prints nothing, exits 0) → `PASS 0/150`, exit 1
- `… --tool ./failing_clean.py` (manifest-aware, always clean) → `PASS 57/150`, exit 1
- `… --map` → `case count: 150`, `sentence coverage: 34/34`
- live: clean → verdict clean exit 0; findings → failed-policy exit 1; missing/empty/dir/invalid manifest → `{"version":1,"verdict":"could-not-evaluate","error":"input_invalid","checks":[]}` exit 2; no args / `--help` / `--manifest` alone / 4 args / `--manifest=x` → exit 64, stdout empty; stderr 0 bytes on every run
- `/usr/bin/python3 -m py_compile sitemap_audit.py sitemap_audit_selftest.py` → 0
- `failing_silent.py` / `failing_clean.py` are emitted from the selftest's own `SILENT_TOOL` (selftest:799) / `CONSTANT_CLEAN_TOOL` (selftest:804) so the fault evidence cannot drift.

## Sentence → fixture (verbatim from `--map`)
sentence  1: cli_clean_roundtrip, cli_single_document_findings
sentence  2: cli_equals_form, cli_extra_argument, cli_help, cli_manifest_without_value, cli_no_args, cli_repeated_option
sentence  3: man_checks_empty, man_checks_missing, man_checks_not_array, man_invalid_json, man_invalid_utf8, man_not_object, man_unreadable_file, man_version_bool, man_version_float, man_version_string, man_version_two
sentence  4: chk_absolute_file, chk_dotdot_file, chk_duplicate_id, chk_id_null, chk_missing_member, chk_nonstring_file, chk_nonstring_id, chk_not_object, chk_url_ftp, chk_url_no_host, chk_url_relative, chk_url_scheme_case
sentence  5: file_is_directory, file_relative_to_manifest_dir, file_unreadable
sentence  6: enc_invalid_bytes, enc_utf8_bom_allowed, enc_utf8_bytes
sentence  7: enc_decl_latin1, enc_decl_lowercase_utf8, enc_decl_mixed_case_utf8, enc_decl_utf16, enc_invalid_suppresses_findings
sentence  8: wf_cdata_loc, wf_malformed, wf_malformed_suppresses_findings, wf_valid_minimal
sentence  9: wf_doctype, wf_doctype_internal_subset, wf_doctype_suppresses_root
sentence 10: root_default_namespace, root_invalid_suppresses_entries, root_no_namespace, root_prefixed, root_sitemapindex, root_wrong_local, root_wrong_namespace
sentence 11: ent_numbering_counts_entries_only, ent_prefixed_entries, ent_sitemap_in_urlset, ent_url_in_sitemapindex, root_prefixed
sentence 12: ent_unexpected_root_child_only, ent_zero_entries
sentence 13: ec_element_unexpected_both_levels, ent_numbering_counts_entries_only, ent_sitemap_in_urlset, ent_unexpected_root_child, ent_unexpected_root_child_only, ent_url_in_sitemapindex
sentence 14: ent_other_namespace_entry_child, ent_other_namespace_root_child
sentence 15: ec_dup_loc_and_field, ec_each_field_once, ec_loc_missing, ec_loc_missing_still_checks_lastmod, ec_loc_repeated
sentence 16: ec_dup_loc_and_field, ec_each_field_once, ec_field_repeated_changefreq, ec_field_repeated_lastmod_index, ec_field_repeated_lastmod_urlset
sentence 17: ec_changefreq_in_sitemapindex, ec_element_unexpected_both_levels, ec_priority_in_sitemapindex, ec_unknown_entry_child
sentence 18: ec_order_not_checked
sentence 19: lim_normal_size, lim_too_large
sentence 20: lim_exactly_50000_entries, lim_too_many_entries, lim_too_many_with_entry_findings
sentence 21: cf_whitespace_stripped, lm_whitespace_stripped, loc_nbsp_not_stripped, loc_xml_whitespace_stripped, pr_whitespace_stripped
sentence 22: loc_empty_host, loc_ftp_scheme, loc_host_without_scheme, loc_relative_and_too_long, loc_relative_path
sentence 23: loc_2047_accepted, loc_2048_too_long, loc_counts_codepoints_not_bytes, loc_relative_and_too_long, loc_too_long_and_out_of_scope
sentence 24: chk_url_scheme_case, scope_explicit_default_port, scope_host_case_insensitive, scope_scheme_case_insensitive
sentence 25: loc_too_long_and_out_of_scope, scope_empty_loc_path_is_root, scope_host_mismatch, scope_path_prefix_ok, scope_path_prefix_rejected, scope_port_mismatch, scope_scheme_mismatch
sentence 26: scope_dot_segments_not_removed, scope_path_case_sensitive, scope_percent_not_decoded
sentence 27: root_sitemapindex, scope_index_host_mismatch, scope_index_path_ignored, scope_index_port_mismatch
sentence 28: lm_complete_date, lm_day_32, lm_fraction, lm_fraction_empty, lm_hour_24, lm_index_date, lm_index_invalid, lm_leap_day, lm_lowercase_z, lm_minute_60, lm_minutes_utc, lm_month_13, lm_nonleap_day, lm_second_60, lm_seconds_offset, lm_time_without_tzd, lm_tzd_hour_24, lm_whitespace_stripped, lm_year_month, lm_year_only
sentence 29: lm_complete_date, lm_day_32, lm_fraction, lm_fraction_empty, lm_hour_24, lm_index_date, lm_leap_day, lm_lowercase_z, lm_minute_60, lm_minutes_utc, lm_month_13, lm_nonleap_day, lm_second_60, lm_seconds_offset, lm_tzd_hour_24
sentence 30: lm_index_date, lm_index_invalid, lm_time_without_tzd, lm_year_month, lm_year_only
sentence 31: cf_all_valid, cf_case_sensitive, cf_unknown_value, cf_whitespace_stripped
sentence 32: pr_bare_dot, pr_comma, pr_empty, pr_exponent, pr_negative, pr_out_of_range, pr_valid_forms, pr_whitespace_stripped
sentence 33: cli_clean_roundtrip, cli_single_document_findings, out_all_statuses, out_clean_item_shape, out_error_item_shape, out_findings_deduplicated, out_findings_item_shape, out_manifest_order_preserved
sentence 34: cli_clean_roundtrip, cli_single_document_findings, out_all_clean_exit_zero, out_all_statuses, out_error_item_shape, out_mixed_error_wins, out_multiple_findings_exit_one

Rules (a)–(k), pos/neg fixture counts, both polarities present: (a) 4/4 (b) 2/5 (c) 3/4 (d) 4/6 (e) 3/11 (f) 3/2 (g) 3/8 (h) 9/9 (i) 7/13 (j) 2/2 (k) 2/6; `--map` prints every name.

Lane readings pinned by fixtures: doctype pre-scan before parsing (DOCTYPE + malformed → `doctype_present` only; sitemap_audit.py:155,172); `too_large`/`encoding_invalid` gate before any XML work and suppress everything (:172); `--manifest=<path>` is a usage error (:378); `loc_too_long` and `loc_out_of_scope` are independent (:267); `too_many_entries` coexists with entry findings (:219); findings deduped as a set, sorted with file-level first (:351); other- and no-namespace children ignored at root (:214) and entry (:233) level; malformed port → `loc_not_absolute` / `check_invalid` (:67 — outside the contract, noted).

Risks: XML 1.1 declarations pass (Expat 3.14 accepts them; no version gate — the contract names the dialect, not a gate); DOCTYPE-vs-malformed precedence is a lane reading (both sentences say “no other finding”); strict `--manifest <path>` spelling. No lane file touched, no counter run, no attacked statements to hold/overstate (BUILD seat).
