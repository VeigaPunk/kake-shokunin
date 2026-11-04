# Frozen C3 derivations

Authority: contract.md plus contract-amendment-{1,2,3,4}.md. Amendment 3 C4 fixes page payloads/effective/findings; amendment 4 D1–D2 overrides the eight finding-case exits. Amendment 3 C1/C6 fixes the exact population at 36. No manifest carries an expectation.

| Case | Contract sentence/rule | Expected value |
|---|---|---|
| g01_absent_tag | C4 row g01; C2.6 default: no matching element. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 0, "findings": []}` |
| g02_noindex | C4 row g02; C2.2 collapse over declared values only. Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 0, "findings": []}` |
| g03_none_expansion | C4 row g03; C2.2 'none expands to noindex + nofollow'. Amendment 4: any finding means exit 1. | `{"effective": ["nofollow", "noindex"], "exit": 0, "findings": []}` |
| g04_all_default | C4 row g04; C2.2 'all expands to index + follow'. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 0, "findings": []}` |
| g05_index_follow_one | C4 row g05; comma split + whitespace trim. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 0, "findings": []}` |
| g06_conflicting_noindex | C4 row g06; C2.2 noindex beats index. Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 0, "findings": []}` |
| g07_conflicting_nofollow | C4 row g07; C2.2 nofollow beats follow. Amendment 4: any finding means exit 1. | `{"effective": ["nofollow"], "exit": 0, "findings": []}` |
| g08_max_snippet_two | C4 row g08; C2.4 smallest non-negative integer. Amendment 4: any finding means exit 1. | `{"effective": ["max-snippet:20"], "exit": 0, "findings": []}` |
| g09_max_image_preview_two | C4 row g09; C2.4 order none < standard < large. Amendment 4: any finding means exit 1. | `{"effective": ["max-image-preview:standard"], "exit": 0, "findings": []}` |
| g10_max_video_no_limit | C4 row g10; C2.4 -1 loses to a non-negative value. Amendment 4: any finding means exit 1. | `{"effective": ["max-video-preview:30"], "exit": 0, "findings": []}` |
| g11_max_snippet_invalid | C4 row g11; C2.6 default when only invalid tokens; A4 invalid value is ignored for effect. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 1, "findings": ["meta_robots_invalid_value"]}` |
| g12a_unavailable_datetime | C4 row g12a; C2.7 input trimmed as written, RFC 3339 date-time (A2 form i). Amendment 4: any finding means exit 1. | `{"effective": ["unavailable_after:2020-09-21T15:00:00Z"], "exit": 0, "findings": []}` |
| g12b_unavailable_date | C4 row g12b; C2.7; A2 form i full-date, the source's own example. Amendment 4: any finding means exit 1. | `{"effective": ["unavailable_after:2020-09-21"], "exit": 0, "findings": []}` |
| g12c_unavailable_rfc822 | C4 row g12c; C2.7; A2 form ii RFC 822-style, B6 zone list. Amendment 4: any finding means exit 1. | `{"effective": ["unavailable_after:25 Jun 2010 15:00:00 PST"], "exit": 0, "findings": []}` |
| g13_unavailable_invalid | C4 row g13; A2 invalid date ignored for effect; C2.6 default. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 1, "findings": ["meta_robots_invalid_value"]}` |
| g14_uppercase | C4 row g14; name and tokens are ASCII-case-insensitive; effective vocabulary is lower case. Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 0, "findings": []}` |
| g15_empty_content | C4 row g15; C2.6/I empty content, default effective. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 1, "findings": ["meta_robots_empty_content"]}` |
| g16_unknown_directive | C4 row g16; C2.6/A4 unknown token ignored, default. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 1, "findings": ["meta_robots_unknown_directive"]}` |
| g17_googlebot_ignored | C4 row g17; name googlebot is not in agents, so no matching element and no finding. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 0, "findings": []}` |
| g18_googlebot_with_agents | C4 row g18; googlebot is a configured agent, so the element matches. Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 0, "findings": []}` |
| g19_body_tag_respected | C4 row g19; A1 body tags join the effective set and are reported as lane hygiene. Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 1, "findings": ["meta_robots_tag_outside_head"]}` |
| g21_self_closing | C4 row g21; self-closing meta parses normally. Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 0, "findings": []}` |
| g22_single_quotes | C4 row g22; attribute parsing, not text matching. Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 0, "findings": []}` |
| g23_noarchive_ignored | C4 row g23; A3 noarchive is an ignored rule, nosnippet is effective. Amendment 4: any finding means exit 1. | `{"effective": ["nosnippet"], "exit": 1, "findings": ["meta_robots_ignored_rule"]}` |
| g24_trailing_comma | C4 row g24; empty tokens are ignored (not all-empty). Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 0, "findings": []}` |
| g25_nosnippet_dominates | C4 row g25; A5 explicit nosnippet drops numeric max-snippet. Amendment 4: any finding means exit 1. | `{"effective": ["nosnippet"], "exit": 0, "findings": []}` |
| g26_max_snippet_zero_video_minus_one | C4 row g26; A5 max-snippet:0 renders nosnippet and drops the max-snippet numeric, but max-video-preview:-1 is the only declared value of its family and survives (C2.4). Amendment 4: any finding means exit 1. | `{"effective": ["max-video-preview:-1", "nosnippet"], "exit": 0, "findings": []}` |
| g27_indexifembedded | C4 row g27; indexifembedded is non-collapsing, noindex still wins its own pair. Amendment 4: any finding means exit 1. | `{"effective": ["indexifembedded", "noindex"], "exit": 0, "findings": []}` |
| g28_within_content_conflict | C4 row g28; C2.2 collapse applies inside one content. Amendment 4: any finding means exit 1. | `{"effective": ["noindex"], "exit": 0, "findings": []}` |
| g29_max_image_preview_none | C4 row g29; C2.4 none is a valid setting and wins the order. Amendment 4: any finding means exit 1. | `{"effective": ["max-image-preview:none"], "exit": 0, "findings": []}` |
| g30_max_snippet_minus_one | C4 row g30; C2.4 -1 is emitted when it is the only declared value of its family. Amendment 4: any finding means exit 1. | `{"effective": ["max-snippet:-1"], "exit": 0, "findings": []}` |
| g31_missing_content | C4 row g31; B6 missing content is equivalent to empty content, default effective. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 1, "findings": ["meta_robots_empty_content"]}` |
| g32_nocache_ignored | C4 row g32; A3 nocache is an ignored rule; C2.6 default. Amendment 4: any finding means exit 1. | `{"effective": ["follow", "index"], "exit": 1, "findings": ["meta_robots_ignored_rule"]}` |
| g33_lowercase_t_z | C4 row g33; B6 RFC 3339 lowercase t and z are accepted, rendered as written. Amendment 4: any finding means exit 1. | `{"effective": ["unavailable_after:2020-09-21t15:00:00z"], "exit": 0, "findings": []}` |
| g34_missing_file_exit2 | C4 row g34; C3/C5 the check names page.html in a dir where that file does not exist -> fault. Amendment 4: any finding means exit 1. | `{"error": "missing_file", "exit": 2}` |
| g35_duplicate_id_exit2 | C4 row g35; C3/C5 two checks share one id -> fault. Amendment 4: any finding means exit 1. | `{"error": "duplicate_check_id", "exit": 2}` |

B6 terminals: RFC 822 accepts optional weekday/comma, the specified named/numeric zones; RFC 3339 lowercase t/z is accepted; RFC 850 remains unimplemented. The fixed population does not independently exercise every terminal, timestamp-offset merging, http-equiv-only input, or multi-finding ordering. These are limits, not widened claims.

Input isolation: only page payload and a no-expect manifest are copied to a random opaque scratch input directory. Check ids/URLs are neutralized; oracle bytes stay solely in the matrix. The sibling-expect echo adversary must fail at least one decided case.
