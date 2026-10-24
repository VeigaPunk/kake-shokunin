# ReviewR41FixtureClasses — H1 classification of the 42 `r41_*` fixtures (Kake r42 w1)

Axis: operability (fixture-class truth). No tools installed.

Identity: clone at tip `d1c3f372b59f…`; selftest `scripts/sitemap_audit_selftest.py` from that clone. base40 = `/fast/scratch/hyaku/kake-r42/shared/base40.py` sha256 `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` — byte-identical to `git show 8eb121c8:scripts/sitemap_audit.py` (same sha256), so "red on base40" ≡ "red on `8eb121c8`". tip41 = `/fast/scratch/hyaku/kake-r42/shared/tip41.py` sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.
Commands (cwd = clone, each `timeout 900 prlimit --as=8000000000 -- python3 -B scripts/sitemap_audit_selftest.py --tool <tool>`): tip41 → exit 0 `PASS 225/225`; base40 → exit 1 `PASS 196/225`; `--map` → exit 0. Logs: `/fast/scratch/hyaku/kake-r42w1/ReviewR41FixtureClasses/{tip40→tip41,base40,map}.txt` (tip41.log, base40.log, map.txt).

Counts: red on `8eb121c8` = **29** (all `r41_*`; the 196 passes include all 183 non-r41 fixtures). Green on both tools = **13**. tip41: green on all 42.

H1 sentence ("42 `r41_*` = 29 change fixtures red on `8eb121c8` + 13 guards green on both: 4 valid-value controls, 2 `/?` positives, the port-letter parity guard, 6 IP-literal TAB/LF/CR guards") — **holds**, verified by set difference: the 13 green are exactly `r41_loc_path_sub_delims`, `r41_loc_path_pct_7e`, `r41_loc_ipv6_literal_host`, `r41_loc_userinfo_with_colon`, `r41_loc_query_slash_question_clean`, `r41_loc_fragment_slash_question_clean`, `r41_loc_port_letter`, `r41_{loc,manifest_url}_ipv6_literal_{tab,lf,cr}` — no extras, none missing.
Detail: among the 29 red, `r41_loc_host_{space,pipe,caret,backtick}` differ only in finding id (base40 `loc_out_of_scope` vs expected `loc_not_absolute`, same exit/verdict) — still red; the other 25 differ in exit and verdict too (`r41_manifest_url_c0_interior`: exit 1 vs 2, `failed-policy` vs `could-not-evaluate`).

| fixture | base40 (8eb121c8) | tip41 (50287ac6) |
|---|---|---|
| `r41_loc_bad_percent_triplet` | RED | green |
| `r41_loc_fragment_backtick` | RED | green |
| `r41_loc_fragment_caret` | RED | green |
| `r41_loc_fragment_pipe` | RED | green |
| `r41_loc_fragment_second_hash` | RED | green |
| `r41_loc_fragment_slash_question_clean` | green | green |
| `r41_loc_fragment_space` | RED | green |
| `r41_loc_host_backtick` | RED | green |
| `r41_loc_host_caret` | RED | green |
| `r41_loc_host_pipe` | RED | green |
| `r41_loc_host_space` | RED | green |
| `r41_loc_ipv6_literal_cr` | green | green |
| `r41_loc_ipv6_literal_host` | green | green |
| `r41_loc_ipv6_literal_lf` | green | green |
| `r41_loc_ipv6_literal_tab` | green | green |
| `r41_loc_one_hex_percent` | RED | green |
| `r41_loc_path_brace` | RED | green |
| `r41_loc_path_bracket` | RED | green |
| `r41_loc_path_caret` | RED | green |
| `r41_loc_path_del` | RED | green |
| `r41_loc_path_pct_7e` | green | green |
| `r41_loc_path_pipe` | RED | green |
| `r41_loc_path_space` | RED | green |
| `r41_loc_path_sub_delims` | green | green |
| `r41_loc_port_letter` | green | green |
| `r41_loc_query_backtick` | RED | green |
| `r41_loc_query_caret` | RED | green |
| `r41_loc_query_pipe` | RED | green |
| `r41_loc_query_slash_question_clean` | green | green |
| `r41_loc_query_space` | RED | green |
| `r41_loc_query_then_second_hash` | RED | green |
| `r41_loc_terminal_one_hex_percent` | RED | green |
| `r41_loc_userinfo_backtick` | RED | green |
| `r41_loc_userinfo_caret` | RED | green |
| `r41_loc_userinfo_pipe` | RED | green |
| `r41_loc_userinfo_second_at` | RED | green |
| `r41_loc_userinfo_space` | RED | green |
| `r41_loc_userinfo_with_colon` | green | green |
| `r41_manifest_url_c0_interior` | RED | green |
| `r41_manifest_url_ipv6_literal_cr` | green | green |
| `r41_manifest_url_ipv6_literal_lf` | green | green |
| `r41_manifest_url_ipv6_literal_tab` | green | green |

Residual risk: one deterministic run per tool (fixture dirs materialized in temp dirs each run); no counter receipts needed for this item. Per round-41 records the 6 IP-literal whitespace guards were red only on the r41 first build `0b485431…`, not on base — consistent with this run (green on base40).
