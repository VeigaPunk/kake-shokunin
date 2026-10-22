# Round 34 wave 1 — link-preview selftest

Axes: this lane owns operability and freshness; this move supports operability. Freshness was not assessed.

## Deliverables
- Runner: `/fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewSelftest/clone/scripts/link_preview_selftest.py`
- Fixtures: `/fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewSelftest/clone/scripts/fixtures/link-preview/` (29 case directories; each has `expected.json` and its manifest/pages, including named absent-manifest and usage cases).
- Runner default is the adjacent `link_preview_audit.py`; `--tool` overrides it. Each fixture runs with its own directory as cwd. For exits 0/1/2 the runner compares one JSON object's verdict and sorted finding multiset (policy: reason+property; input: reason); exit 64 compares exit only. It emits one JSON summary and returns 0 only if all fixtures pass.

## Fixture coverage
- `canonical_first_mismatch` — first of multiple canonical links governs comparison; og:url matches only the later link.
- `clean_first_canonical` — first relative canonical resolves equal; later decoy ignored.
- `clean_markup_variants` — uppercase tags/attrs, single quotes, reordered attrs, self-closing meta, entity content.
- `clean_multiple_images` — repeated og:image is allowed.
- `clean_relative_canonical` — relative canonical resolves against page URL.
- `clean_without_canonical` — no canonical means no comparison; query and fragment in absolute og:url.
- `content_ascii_whitespace` — whitespace-only content is missing.
- `input_empty_pages` — empty page list is input_invalid.
- `input_invalid_page_url` — ftp page URL is input_invalid.
- `input_malformed_manifest` — malformed manifest JSON is input_invalid.
- `input_missing_manifest` — explicitly requested absent manifest is input_invalid.
- `input_missing_page` — missing listed file is page_unreadable.
- `input_path_escape` — page path outside manifest directory is input_invalid.
- `input_policy_suppressed_on_input` — input finding suppresses otherwise reportable policy findings.
- `missing_all` — all four required properties missing.
- `missing_empty_type` — empty og:type content is missing.
- `missing_image_name_only` — name=og:image does not satisfy property=og:image.
- `missing_title` — name=og:title does not satisfy property=og:title.
- `missing_url` — required og:url missing.
- `mixed_pages_findings` — three nested pages combine clean, missing-title, duplicate-type, and relative-url findings.
- `multiple_types` — more than one non-empty og:type.
- `nested_pages_clean` — nested page path reads cleanly.
- `property_case_sensitive` — uppercase property value does not equal og:title.
- `url_ftp` — non-http(s) absolute og:url is not absolute by policy.
- `url_query_differs` — query difference from canonical is an exact-string mismatch.
- `url_query_fragment_equal` — exact query+fragment equality with canonical is clean.
- `url_relative` — relative og:url produces og_url_not_absolute.
- `usage_no_args` — no arguments returns exit 64.
- `usage_unknown_flag` — unknown argument returns exit 64.

## Exercised evidence
- Correct throwaway auditor: `python3 -B scripts/link_preview_selftest.py --tool /fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewSelftest/tmp/link_preview_audit_correct.py` from the clone, exit **0**; stdout summary `cases=29 passed=29 failed=0 passedOverTotal=29/29 verdict=clean` (full stdout artifact `artifact://25790`).
- Deliberately wrong throwaway auditor: same command with `link_preview_audit_wrong.py`, exit **1**; stdout summary `cases=29 passed=7 failed=22 passedOverTotal=7/29 verdict=failed` (full stdout artifact `artifact://25791`).
- Exact commands and retained output summaries: `/fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewSelftest/tmp/selftest-run-evidence.txt:1-11`, SHA-256 `8c196527f3529ee96289d0bcef0fdbd345d4ac9a56b92f80ae15b7bdad8b352c`.
- Runner source: `scripts/link_preview_selftest.py:11-16` defaults/constants; `:26-43` finding projection; `:46-109` cwd invocation and comparisons; `:112-178` CLI, JSON summary, and exit contract. SHA-256 `9eefc787570335a2851ba0bf372f068cf20947d6cc33cdfb6d8e8421ea96c1b2`.
- Fixture-tree digest, normalized tar stream: `tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - scripts/fixtures/link-preview | sha256sum` → `d3bdb258063cc9e40044ab3e150918f73ce723a525f4589e38a63c47e32cc9e8`.
- Representative fixture evidence: `scripts/fixtures/link-preview/clean_markup_variants/{manifest.json,expected.json,pages/launch.html}:1`; mixed-pages manifest/expectation/pages are under `scripts/fixtures/link-preview/mixed_pages_findings/:1`.

## Limits
- The tests used the required temporary correct and wrong implementations, not the separate production auditor; the L1 should run this selftest against the integrated `link_preview_audit.py`.
- No build, lint, formatter, or unrelated tests were run. No tools were installed. LSP was not applicable: this adds a standalone script/fixtures and changes no existing symbols.
- Temporary auditor scripts were removed after the runs. No blocker to this scoped deliverable.
