# ManifestSchema — offline canonical preflight review

Axes: **operability** (primary), deterministic classification, and fail-closed input handling.

## Review basis and limits

The frozen contract is `.ufo/waves/round-22/contract.json` at base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`. Its manifest interface gives `version: 1` and `pages` entries with `url`, `file`, and `expectedCanonical`; it specifies manifest-relative HTML paths, the exit map, JSON result fields, and the allowed finding IDs. The frozen 32-case list covers policy and file-resolution cases but no malformed JSON, wrong version type, missing manifest fields, duplicate JSON member names, or empty `pages` array.

At inspection time `scripts/canonical_audit.py` was absent both from the lane and `/tmp/kake-r22-Implement/scripts/`, so these are contract/design findings, not claims about implementation behavior. No tests were run. The `lsp` device is not mounted (`xd://lsp` returned “No such tool”), and no source was available for caller/definition/diagnostics checks.

## Findings, by severity

### High — Manifest-shape rules leave a vacuous or malformed input able to look clean

**Evidence:** `contract.json` → `interface.manifest`, `interface.outputs.exitMap`, and `interface.policy`; `matrixCases` has no schema-invalid case other than path traversal.

The frozen interface does not say whether `pages: []` is valid, whether `version` must be the exact JSON integer `1` (rather than `true` or `1.0`), whether each page must contain all three fields as non-empty strings, whether unknown keys are errors, or how invalid `url` / `expectedCanonical` values are handled. Those gaps permit divergent implementations: an empty manifest can yield a vacuous clean result, a mistyped field can be coerced or skipped, or a missing field can escape as an exception instead of a stable result. For a versioned preflight, specify strict field types and required fields; reject empty `pages`, invalid manifest URLs, and unknown fields rather than silently ignoring them. Reject duplicate JSON object member names rather than accepting whichever value a parser happens to retain. These are manifest failures, not page-policy failures.

**Expected stable classification:** schema/parse/manifest-URL failures → exit `2`, finding `input_invalid`; do not use `canonical_url_invalid`, which describes an HTML canonical `href`. A valid matching one-page manifest → exit `0`, no findings (`clean`). The output contract also needs to pin `findings[].page` for a manifest-level error (for example, `null`) and define a stable page identity for per-page findings; otherwise consumers cannot reliably attribute an error when there is no valid page record.

**Minimum acceptance/rejection pair:**

- Accept a manifest with exactly `version: 1` and one page whose three fields are strings, with `url` and `expectedCanonical` both `https://example.test/project/a.html`; use `a.html` containing an explicit-head canonical link to that same URL. Expect exit `0`, `pagesChecked: 1`, and no findings.
- Reject the same manifest after changing `expectedCanonical` to `null` (and, separately, try `pages: []`). Expect exit `2`, `input_invalid`, and `pagesChecked: 0`; no page-policy finding should be emitted. These probes are additions to the frozen matrix, not currently frozen cases.

### Medium — Manifest-level invalid findings lack a fully specified diagnostic shape

**Evidence:** `contract.json` → `interface.outputs.stdout` promises each finding contains `id` and `page`, while `input_invalid` covers input that may fail before a page can be identified. The contract does not define whether `page` is a URL, file path, index, object, or nullable value, nor how a JSON parse error satisfies that required field.

This makes otherwise stable finding IDs insufficient for callers to distinguish affected pages and makes exact output expectations implementation-dependent. Define one deterministic `page` representation for valid page findings and a fixed sentinel (preferably JSON `null`) for manifest-wide failures. Keep diagnostics out of the stable ID; the ID remains `input_invalid`.

## Bounded falsification recipe (not run)

After the implementation lands, create a temporary directory and a single `a.html` with one matching canonical link. Run the CLI once on the valid manifest above and require exit `0`, `pagesChecked: 1`, and an empty `findings` array. Run it on three temporary invalid manifests: `expectedCanonical: null`, `pages: []`, and duplicate top-level `pages` members with one malformed and one clean value. Require exit `2`, exactly the stable `input_invalid` classification, and `pagesChecked: 0` for each; confirm the result does not become clean by last-key-wins parsing. Use only local temporary files, no network, and do not modify the source tree.