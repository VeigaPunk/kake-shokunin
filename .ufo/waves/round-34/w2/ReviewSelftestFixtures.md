# Round 34 wave 2 — ReviewSelftestFixtures (operability)

Attacked: committed `scripts/link_preview_selftest.py` + 29 fixtures at `24a1647`. Sandbox clone `/fast/scratch/hyaku/kake-r34/w2/ReviewSelftestFixtures/clone` (checkout 24a1647). Verdict: all 29 `expected.json` are correct per `c1-matrix.json` "interface"; zero fixtures copy a matrix case (exact, whitespace-normalized, or HTML-only compare — script output: `EXACT input copies: []`, `WHITESPACE-NORM copies: []`, no HTML-identical lines). Selftest on the landed tool: `python3 -B scripts/link_preview_selftest.py` → exit 0, `29/29 clean`.

## Per-fixture table

| fixture | rule exercised | expected correct? | copies matrix? |
|---|---|---|---|
| canonical_first_mismatch | first canonical link wins; og:url differs → og_url_not_canonical | yes | no (D8-like expectation, different input) |
| clean_first_canonical | first canonical wins; later decoy ignored | yes | no |
| clean_markup_variants | case-insensitive tags/attrs, attr order, self-close, entity | yes | no |
| clean_multiple_images | repeated og:image allowed | yes | no |
| clean_relative_canonical | `../../about` resolves to `cards.example/about` = og:url | yes | no |
| clean_without_canonical | no canonical → no comparison (K4-like) | yes | no |
| content_ascii_whitespace | whitespace-only og:title content is missing | yes | no |
| input_empty_pages | empty pages → input_invalid | yes | no |
| input_invalid_page_url | ftp page URL → input_invalid | yes | no |
| input_malformed_manifest | truncated JSON → input_invalid | yes | no |
| input_missing_manifest | argv `--manifest absent.json` → input_invalid | yes | no |
| input_missing_page | listed file absent → page_unreadable | yes | no |
| input_path_escape | `../outside.html` → input_invalid | yes | no |
| input_policy_suppressed_on_input | input finding suppresses policy findings; exit 2 | yes | no |
| missing_all | all four required missing (4 findings) | yes | no |
| missing_empty_type | whitespace og:type → og_required_missing og:type | yes | no |
| missing_image_name_only | `name=` does not satisfy `property=` | yes | no |
| missing_title | `name=og:title` ignored → og:title missing | yes | no |
| missing_url | og:url absent; canonical alone not a substitute | yes | no |
| mixed_pages_findings | 3 pages: clean, missing title + dup type, rel og:url | yes | no |
| multiple_types | two non-empty og:type → og_type_multiple | yes | no |
| nested_pages_clean | nested file path resolves | yes | no |
| property_case_sensitive | `OG:title` ≠ `og:title` → missing | yes | no |
| url_ftp | ftp og:url → og_url_not_absolute | yes | no |
| url_query_differs | query diff vs canonical → og_url_not_canonical | yes | no |
| url_query_fragment_equal | exact query+fragment equality → clean | yes | no |
| url_relative | relative og:url → og_url_not_absolute | yes | no |
| usage_no_args | argv `[]` → exit 64 | yes | no |
| usage_unknown_flag | `--not-a-real-option` → exit 64 | yes | no |

Expectation overlap with matrix `expect` objects exists (e.g. clean↔K1–K6) but inputs differ in every case; "copies matrix" means input duplication, none found.

## Runner defects, ranked

1. **Moderate — interface fields `page`, `id`, `pagesChecked` are never verified.** `finding_signature` projects to (reason[, property]); `pagesChecked` unchecked. Demonstrated: `tmp/stripped_tool.py` (real auditor minus id/page/pagesChecked) → exit 0, `29/29 clean`; a bogus `"page":"https://bogus.example/WRONG"` planted in `mixed_pages_findings/expected.json` → still `29/29 clean`. This matches the matrix "comparison" contract verbatim (exit+verdict+projected findings only), so the gap is contract-level, shared with the C1 counter — but the one multi-page fixture cannot detect wrong-page attribution.
2. **Moderate — non-UTF-8 tool stdout crashes the whole run.** `subprocess.run(text=True)` decode error escapes `check_case`'s `except (OSError, TimeoutExpired)`; observed `UnicodeDecodeError` traceback, no JSON summary emitted (runner promise "emits one JSON summary" broken). Repro: `tmp/binary_tool.py` writes `b'\xff\xfe'`; run `python3 -B tmp/selftest_t2.py --tool tmp/binary_tool.py --fixtures tmp/onefx2` → traceback, exit 1.
3. **Low — serial 120 s/case timeout**: a hanging tool costs up to ~58 min (29×120 s) before verdict `failed`. Patched-constant probe (TIMEOUT_SECONDS=2) shows the path works: per-case `tool could not run: ... timed out`, exit 1.
4. **Low — exit↔verdict coherence is fixture-trusted, not enforced.** A fixture could declare `exit:0, verdict:"failed-policy"` and a compliant-emitting tool would pass it; interface fixes 0→clean, 1→failed-policy, 2→could-not-evaluate. All 29 landed fixtures are coherent; latent only.
5. **Low/cosmetic —** preflight failures report `failed:1, cases:0, "0/0"`; when expected exit is 0/1/2 but actual is 64 the runner also reports "stdout is not one JSON object" (stderr-only usage text → empty stdout parse error); stderr never inspected; bool/number argv items silently stringified.

## Verified failure modes
- missing tool → `could-not-evaluate`, exit 2; missing fixtures dir → exit 2; <20 case dirs → exit 2 (all observed).
- non-JSON stdout tool → per-case `exit mismatch` + `stdout is not one JSON object`, verdict `failed`, exit 1 (observed, `0/29`).
- timeout path → per-case `tool could not run`, exit 1 (observed at 2 s).
- Runner comparison code matches the matrix "comparison" string exactly (exit equal; verdict+projected multiset for 0/1/2; exit only for 64).

## Not verified / notes
- No build/lint run (none applies). Tools installed: none. Receipts and sandbox artifacts under `/fast/scratch/hyaku/kake-r34/w2/ReviewSelftestFixtures/`.
- Residual risk: blindness in defect 1 means the selftest cannot catch wrong-page or missing-id findings; combined with the lookup-table counter weakness already disclosed, the round's evidence chain does not pin finding attribution at all.
