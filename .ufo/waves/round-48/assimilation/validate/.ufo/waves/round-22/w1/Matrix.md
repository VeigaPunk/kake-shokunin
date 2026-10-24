# Round 22 Matrix seat report

## Scoped files

Authored in the private clone only:

- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/cases.json`
- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/matrix.py`
- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/fixtures/<caseId>/manifest.json` for all 32 frozen cases.
- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/fixtures/<caseId>/page.html` for 30 serialized HTML cases; `manifest_traversal` has no page file in its case directory and points through `../escape.html`.
- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/fixtures/symlink_html/target.html` supplies the symlink target.
- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/fixtures/escape.html` is the existing traversal target and contains a matching canonical.
- This report: `/tmp/kake-r22-Matrix/.ufo/waves/round-22/w1/Matrix.md`.

No symlink is committed. The `symlink_html` runner copies its manifest and target into a temporary directory, creates `linked.html` there, and invokes the audit using that temporary absolute manifest path. The traversal manifest's `../escape.html` target exists so the expected `input_invalid` result requires traversal rejection, not an incidental missing-file failure.

## Behavior delivered

`matrix.py --root <root>` loads independent per-case manifests and compares both the subprocess exit code and exact finding-ID list to `cases.json`. It invokes `<root>/scripts/canonical_audit.py --manifest <absolute-path> --json`, emits one `PASS`, `FAIL`, or `NOT_RUN` row with `caseId`, then a summary. The default denominator is the frozen 32-case set. `--case <caseId>` runs exactly one case and reports `total=1`; unknown case IDs are rejected. The case-set check compares IDs against the exact frozen contract name tuple embedded in the runner. The runner's own `--json` mode emits one JSON object containing the counts, per-case expected and actual results, and complete captured stdout/stderr; default mode remains text.

`cases.json` v1 records `caseId`, `manifest`, `expectedExit`, `expectedFindings`, and a `rationale` beginning `Local publisher policy:` for every case. Clean positive controls use the explicit stable ID `clean`. Frozen expected finding IDs:

- `clean`: `absolute_match`, `relative_same_dir`, `relative_parent`, `root_relative`, `scheme_relative`, `first_base`, `second_base_ignored`, `rel_token_list`, `rel_uppercase`, `attr_uppercase`, `entity_href`, `query_preserved`, `comment_decoy`, `script_decoy`, `template_decoy`.
- `canonical_missing`: `missing_link`.
- `canonical_multiple`: `duplicate_same`, `duplicate_different`.
- `canonical_outside_head`: `body_link`.
- `canonical_href_missing`: `href_absent`, `href_empty`.
- `canonical_url_invalid`: `invalid_url`, `javascript_url`, `data_url`.
- `canonical_fragment`: `fragment_url`.
- `canonical_mismatch`: `wrong_host`, `wrong_path`, `wrong_query`.
- `base_url_invalid`: `base_invalid`.
- `html_unsupported`: `missing_head` (exit 2).
- `input_invalid`: `manifest_traversal`, `symlink_html` (exit 2).

The `href_empty` expectation is frozen as exit 1 / `canonical_href_missing`: local publisher policy requires a non-empty canonical destination even though URL resolution of an empty reference could produce the page URL. The auditor implementer confirmed this behavior before any matrix run.

When `scripts/canonical_audit.py` is absent, the runner prints every selected case as `NOT_RUN`, returns 2, and reports `accepted=0` and `executed=0`; absence is not presented as observed behavior.

## Retained evidence and verification status

- The private clone command returned both `master` and `HEAD` as `7c61c8cc791bde36dd5e3688bdfea2678d90146c`, matching the required base.
- Read the frozen contract at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json`; its `matrixCases` contains the exact 32 names encoded in `FROZEN_CASE_NAMES`, and its declared exits/finding IDs were used as the authority for the frozen expectations.
- A glob lookup in the private base clone found no `scripts/canonical_audit.py`; no canonical-audit output was therefore observed and the matrix was not run.
- No build, test, lint, formatter, or runtime check was run in this editing wave. L1 owns the post-integration gate.
- No tools were installed or updated. No LSP interface is exposed in the available tool inventory; there were no existing symbols or call sites to navigate/refactor in the assigned new files.
- Repository guidance asks for a `LOG.md` entry, but the wave’s stricter assigned-path boundary permits only the implementation files above and this exclusive report; `LOG.md` was left untouched.

## Risks and blockers

The round-22 auditor was absent at the required base, so these are independent frozen expectations and fixture cases, not a claim that the capability passed. The result may expose disagreements between implementation and the stated local policy; resolve those against the frozen contract and this matrix without changing expectations to match observed output. No blocker remains for this seat’s scoped deliverable; run the full matrix and selected cases after integration.
