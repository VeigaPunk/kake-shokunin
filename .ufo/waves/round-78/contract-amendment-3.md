# kake round 78 — contract amendment 3 (terms only, before any after-state)

Recorded 2026-11-03 in answer to ExecC3Matrix's five blocking questions. No C3 after-state exists
when this is written. C1 and C2 untouched.

## C1 — the frozen case count is 36, not 34

Amendment 2 §B4's list is authoritative: `g01–g19` (with `g12` split three ways) = 21,
`g21–g27` = 7, `g28–g35` = 8 → **36 ids**. The literal `34` in B4's sentence and in B5's
predicate is corrected here; the list itself is unchanged. `[r78-correction 2026-11-03]`

**Predicate (final):** `met <=> cases == 36 and decided == 36 and correct == 36 and
constants_failed == 4 and selftest_ok`.

## C2 — the effective set is the declared-after-collapse set, default when nothing valid is declared

The tool is a **declaration audit**, not a crawler simulation. For each check:

1. Collect the valid declared rules from every matching element (see B6 for matching).
2. Collapse the two binary families to the most restrictive member actually declared:
   `index`/`noindex` → `noindex` if declared anywhere, else `index` if declared anywhere,
   else absent; `nofollow` beats `follow` the same way. `none` expands to `noindex` + `nofollow`;
   `all` expands to `index` + `follow`.
3. Leave the non-collapsing tokens present/absent as declared: `nosnippet`, `noimageindex`,
   `notranslate`, `indexifembedded`. `nosnippet` dominates: if `nosnippet` is declared, no
   `max-snippet:` or `max-video-preview:` token is emitted (the source's own example).
4. Collapse the numeric families to the most restrictive declared value:
   `max-snippet` / `max-video-preview` take the smallest non-negative integer; `-1` ("no limit")
   is emitted only when it is the only declared value of that family; `max-image-preview` takes
   `none < standard < large`.
5. `max-snippet:0` is rendered `nosnippet` (the source's stated equivalent), so it participates in
   rule 3.
6. **Default:** if no valid effective rule survives steps 2–5 (absent element, empty or missing
   content, or only invalid/unknown/ignored tokens), the effective set is the default pair
   `["follow","index"]`. An element is never silently dropped: the reason is a finding.
7. Emit the sorted list. `unavailable_after` renders as `<input trimmed as written>` prefixed with
   `unavailable_after:`.

This freezes g06 = `["noindex"]`, g07 = `["nofollow"]`, g23 = `["nosnippet"]`,
g25 = `["nosnippet"]`, g28 = `["noindex"]`, g27 = `["indexifembedded","noindex"]`.

## C3 — exit-2 error vocabulary

`missing_file` (a check's local file cannot be read), `duplicate_check_id` (two checks share an id),
`bad_manifest` (JSON or schema fault). The tool prints `{"version":1,"error":"<code>"}` and exits 2;
the matrix compares the exit code and the `error` string for g34/g35.

## C4 — frozen expectation table (36 cases)

`page` is shorthand for the one HTML file of the case; `agents` is the manifest's list; findings
are the sorted de-duplicated ids of B2. Every page also carries `<head>` and body boilerplate with
no other `meta name=robots`-family element unless stated.

| id | page declares (inside head unless said) | agents | exit | effective | findings |
|---|---|---|---|---|---|
| g01_absent_tag | nothing | ["robots"] | 0 | follow,index | — |
| g02_noindex | `noindex` | ["robots"] | 0 | noindex | — |
| g03_none_expansion | `none` | ["robots"] | 0 | nofollow,noindex | — |
| g04_all_default | `all` | ["robots"] | 0 | follow,index | — |
| g05_index_follow_one | `index, follow` | ["robots"] | 0 | follow,index | — |
| g06_conflicting_noindex | `index` tag + `noindex` tag | ["robots"] | 0 | noindex | — |
| g07_conflicting_nofollow | `follow` tag + `nofollow` tag | ["robots"] | 0 | nofollow | — |
| g08_max_snippet_two | `max-snippet:50` tag + `max-snippet:20` tag | ["robots"] | 0 | max-snippet:20 | — |
| g09_max_image_preview_two | `max-image-preview:large` tag + `max-image-preview:standard` tag | ["robots"] | 0 | max-image-preview:standard | — |
| g10_max_video_no_limit | `max-video-preview:-1` tag + `max-video-preview:30` tag | ["robots"] | 0 | max-video-preview:30 | — |
| g11_max_snippet_invalid | `max-snippet:abc` | ["robots"] | 0 | follow,index | invalid_value |
| g12a_unavailable_datetime | `unavailable_after: 2020-09-21T15:00:00Z` | ["robots"] | 0 | unavailable_after:2020-09-21T15:00:00Z | — |
| g12b_unavailable_date | `unavailable_after: 2020-09-21` | ["robots"] | 0 | unavailable_after:2020-09-21 | — |
| g12c_unavailable_rfc822 | `unavailable_after: 25 Jun 2010 15:00:00 PST` | ["robots"] | 0 | unavailable_after:25 Jun 2010 15:00:00 PST | — |
| g13_unavailable_invalid | `unavailable_after: 2020-13-40` | ["robots"] | 0 | follow,index | invalid_value |
| g14_uppercase | `NOINDEX` on `name="ROBOTS"` | ["robots"] | 0 | noindex | — |
| g15_empty_content | `name="robots"` with `content=""` | ["robots"] | 0 | follow,index | empty_content |
| g16_unknown_directive | `nosuchthing` | ["robots"] | 0 | follow,index | unknown_directive |
| g17_googlebot_ignored | `name="googlebot"` `content="noindex"` | ["robots"] | 0 | follow,index | — |
| g18_googlebot_with_agents | `name="googlebot"` `content="noindex"` | ["robots","googlebot"] | 0 | noindex | — |
| g19_body_tag_respected | `noindex` element in the body | ["robots"] | 0 | noindex | tag_outside_head |
| g21_self_closing | `<meta name="robots" content="noindex" />` | ["robots"] | 0 | noindex | — |
| g22_single_quotes | `<meta name='robots' content='noindex'>`, no spaces around `=` | ["robots"] | 0 | noindex | — |
| g23_noarchive_ignored | `noarchive` tag + `nosnippet` tag | ["robots"] | 0 | nosnippet | ignored_rule |
| g24_trailing_comma | `noindex,` | ["robots"] | 0 | noindex | — |
| g25_nosnippet_dominates | `nosnippet` tag + `max-snippet:50` tag | ["robots"] | 0 | nosnippet | — |
| g26_max_snippet_zero_video_minus_one | `max-snippet:0, max-video-preview:-1` | ["robots"] | 0 | max-video-preview:-1,nosnippet | — |
| g27_indexifembedded | `noindex, indexifembedded` | ["robots"] | 0 | indexifembedded,noindex | — |
| g28_within_content_conflict | `index, noindex` in one content | ["robots"] | 0 | noindex | — |
| g29_max_image_preview_none | `max-image-preview:none` | ["robots"] | 0 | max-image-preview:none | — |
| g30_max_snippet_minus_one | `max-snippet:-1` | ["robots"] | 0 | max-snippet:-1 | — |
| g31_missing_content | `<meta name="robots">` (no content attribute) | ["robots"] | 0 | follow,index | empty_content |
| g32_nocache_ignored | `nocache` | ["robots"] | 0 | follow,index | ignored_rule |
| g33_lowercase_t_z | `unavailable_after: 2020-09-21t15:00:00z` | ["robots"] | 0 | unavailable_after:2020-09-21t15:00:00z | — |
| g34_missing_file_exit2 | a check naming a file that does not exist | ["robots"] | 2 | — | error=missing_file |
| g35_duplicate_id_exit2 | two checks with the same id | ["robots"] | 2 | — | error=duplicate_check_id |

Every exit-0 case's `expect.json` carries `{"exit":0,"effective":[…],"findings":[…]}`; the two
exit-2 cases carry `{"exit":2,"error":"…"}`. A case whose `page.html` or `manifest.json` does not
match this table is a case defect, not a contract ambiguity.

## C5 — case directory shape

Each case is `.ufo/waves/round-78/cases/<id>/` with `page.html`, `manifest.json` (no `expect`) and
`expect.json` (the table's row). g34's manifest names `page.html` under a path that does not exist;
g35's manifest names the same existing page twice with one id.

## C6 — frozen case set vs the matrix

The matrix's `--cases` directory must hold exactly the 36 ids of C4; a missing or extra id is a
named finding (`case_set_mismatch`) and `met=false`. `cases` is printed from the frozen list.
