# ExecIndependentOracle — round 35, wave 1

Axis: operability. Built an independent offline oracle at
`/fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/oracle.py`, using the
lxml HTML tree builder. The committed sandbox copy is byte-identical. It implements
the round-34 manifest, findings, CLI and exit rules, plus C1(a-c): duplicate
non-empty `og:url` with first-value checks; exclusion under open template/SVG/Math
ancestors; and continued auditing/reporting of readable pages beside unreadable
page findings.

## Commands and retained evidence

- `mkdir -p /fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/tmp && unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/clone && git -C /fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/clone checkout -q 318561efa67206699fdaf259ffb86e39f2d916a8` — exit 0.
- `uv run --with lxml python .ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/clone --revision cd5f8189da40ac7d56dfbd26137ab343072a026c` — exit 0; `C1 28/28`; control 6/6, defect 13/13, input 7/7, usage 2/2; constant gates all rejected (6/28, 0/28, 6/28, 1/28). Counter SHA-256 `fc72d855cde3656fe74ab8372ae57dca39ff2d7cebc5e5e4aced6e483b71c51e`; matrix SHA-256 `246a6a3ba67a842c408f56b0240d2ad36969330c5a414b715f04b7e56fac14f7`; tool SHA-256 `fe522e5a9ddef3702ff56d4578dbbe72641e1cacbff3fd8767044a736b530c1c`.
- Fixture runs: `uv run --with html5lib python -c <fixture driver>` and final `uv run --with lxml python -c <fixture driver>` — both exit 0 after the initial parser error noted below. Each invoked all 35 cases; the base tool matched 35/35, and the final oracle matched 33/35 expected projections. The two differences below are contract-supported. Initial differential output: `artifact://37588:4-6`; final output: `artifact://38068:4-6`.
- The complete fixture set was: `canonical_first_mismatch`, `canonical_unparsable_href`, `clean_first_canonical`, `clean_image_url_alias`, `clean_markup_variants`, `clean_multiple_images`, `clean_relative_canonical`, `clean_without_canonical`, `content_ascii_whitespace`, `duplicate_attribute_first_wins`, `input_empty_pages`, `input_invalid_page_url`, `input_malformed_manifest`, `input_missing_manifest`, `input_missing_page`, `input_page_not_utf8`, `input_path_escape`, `input_policy_suppressed_on_input`, `missing_all`, `missing_empty_type`, `missing_image_name_only`, `missing_title`, `missing_url`, `mixed_pages_findings`, `multiple_types`, `nested_pages_clean`, `property_case_sensitive`, `url_case_differs`, `url_ftp`, `url_query_differs`, `url_query_fragment_equal`, `url_relative`, `url_trailing_slash_differs`, `usage_no_args`, `usage_unknown_flag`.

## Disagreements and contract decision

1. `clean_image_url_alias`: retained expected and base tool say exit 0 clean; oracle says exit 1 with `og_required_missing` / `og:image`. The page has only `property="og:image:url"` (`clone/scripts/fixtures/link-preview/clean_image_url_alias/index.html:1`). The contract supports the oracle: matrix interface line 10 requires the property to equal `og:image` exactly.
2. `input_policy_suppressed_on_input`: retained expected and base tool report only `page_unreadable`; oracle reports that plus missing `og:type`, `og:image`, and `og:url` for the readable page, exit 2, `pagesChecked=1`. The contract supports the oracle: `clone/SCORECARD.md:1387-1392` requires continuing across unreadable pages and reporting readable-page policy findings beside input findings.

## Public C1 probes

- `uv run --with lxml python /fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/clone/scripts/link_preview_audit.py --manifest manifest.json` (cwd `/fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/tmp/public-r35-probes/multiple_url_uses_first`) — exit 1; findings `og_url_multiple` and `og_url_not_canonical`, proving the first URL drives comparison.
- The same command (cwd `/fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/tmp/public-r35-probes/tree_suppression_and_svg_selfclose`) — exit 0, clean; nested template/SVG/Math metadata and the self-closed SVG did not suppress outside metadata.
- `uv run --with lxml python /fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/clone/scripts/link_preview_audit.py --manifest scripts/fixtures/link-preview/input_policy_suppressed_on_input/manifest.json` (cwd `/fast/scratch/hyaku/kake-r35/w1/ExecIndependentOracle/clone`) — exit 2; readable page policy findings plus `page_unreadable`, `pagesChecked=1`.
- Baseline read-bound samples via `sys.executable -B <clone>/scripts/link_preview_audit.py --manifest <generated-manifest>`: 16,777,216-byte page exit 0/clean; 17,000,000-byte page exit 2/`page_unreadable`. Oracle uses an inclusive 16 MiB limit (`oracle.py:30,98-108`).

Contract anchors: `clone/SCORECARD.md:1378-1395`; round-34 interface is
`clone/.ufo/waves/round-34/c1-matrix.json:6-12`. Oracle implementation anchors:
`oracle.py:59-95` (manifest), `98-110` (bounded UTF-8 reads), `123-153` (tree
filter), `156-190` (policy), `207-249` (result and CLI). Sandbox revision:
`cd5f8189da40ac7d56dfbd26137ab343072a026c`, based on `318561efa67206699fdaf259ffb86e39f2d916a8`.

## Risks and limits

- Runtime dependency: lxml 6.1.3, installed transiently through `uv run --with lxml` for the required tree builder. An initial html5lib 1.1 probe was replaced after its tree builder relocated metadata out of SVG/Math ancestors. Both versions were obtained with uv; no host-wide tool install.
- Initial html5lib fixture run exited 1 on `canonical_unparsable_href` (`ValueError: Invalid IPv6 URL`); the oracle now treats an unresolvable canonical href as not-canonical, matching the retained contract fixture.
- The sealed round-35 counter was not run; no sealed directory content was accessed. No other build, lint, formatter, or test suite was run. No LSP tool was exposed; this is a new standalone file, with no existing symbol refactor.
- Blockers: none.
