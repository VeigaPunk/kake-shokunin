## Verdict

HOLD — one low-severity multi-page coverage ambiguity remains in the candidate CLI. The required malformed-input cases otherwise failed closed, and unsupported HTML was not reported clean. This is a recommendation, not independent admission.

## Findings

### P3 — Duplicate page rows can produce a clean result while inflating `pagesChecked`

- **Evidence / exact command:** With two identical page objects (`url=https://example.test/a`, `file=good.html`, `expectedCanonical=https://example.test/a`) in `duplicate_page_entries.json`:

  ```text
  $ /usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/duplicate_page_entries.json --json
  exit=0
  stdout='{"findings":[],"pagesChecked":2,"verdict":"clean"}\n'
  stderr=''
  ```

- **Impact / axis:** Operability. A caller treating `pagesChecked` as distinct-surface coverage can meet a requested count using duplicate rows while leaving a surface unexamined. This behavior is present at candidate commit `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`; manifest validation in `_validate_manifest` checks exact keys, field types, and non-empty pages but not duplicate URLs (`scripts/canonical_audit.py:666-682`).
- **Scope qualification:** Round-23's C2 counter currently constructs a one-page manifest for each frozen surface when reproducing a receipt (`.ufo/waves/round-23/measure_c2.py:65-77`), so this probe does not demonstrate a bypass of that counter. The gap is in the public multi-page CLI contract; the manifest documentation does not state that duplicate rows are forbidden.
- **Smallest fix:** Reject duplicate normalized document URLs during manifest preflight (before accepting a clean result), and add this fixture as a CLI regression case. If duplicates are intentionally supported, document that `pagesChecked` counts entries rather than distinct surfaces and avoid using it as a coverage count.

## Checked and held

- **Candidate identity:** Extracted the target blob with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc:scripts/canonical_audit.py > /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py && sha256sum /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py`; observed `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac  /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py`. The lane checkout was at `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`; its script had the same SHA-256. All CLI probes below ran the extracted candidate blob, not a guessed source version.
- All fixture manifests and HTML files were under `/tmp/kake-r23-BoundaryManifestKeys-DqAK`. The positive control used explicit closed `<head>` markup with a self-canonical link. The policy-negative control used the same page with canonical `https://example.test/wrong` while expecting `https://example.test/a`.

| Case | Exact CLI command | Exit | Exact stdout | Exact stderr |
|---|---|---:|---|---|
| Positive clean control | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/positive_clean.json --json` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` | `''` |
| Negative policy control | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/negative_policy_mismatch.json --json` | 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/a"}],"pagesChecked":1,"verdict":"failed-policy"}\n` | `''` |
| Unknown top-level key | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/unknown_top_level_key.json --json` | 2 | `{"findings":[{"id":"input_invalid","page":null}],"pagesChecked":0,"verdict":"could-not-evaluate"}\n` | `''` |
| Unknown page key | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/unknown_page_key.json --json` | 2 | `{"findings":[{"id":"input_invalid","page":null}],"pagesChecked":0,"verdict":"could-not-evaluate"}\n` | `''` |
| JSON `true` as version | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/boolean_true_version.json --json` | 2 | `{"findings":[{"id":"input_invalid","page":null}],"pagesChecked":0,"verdict":"could-not-evaluate"}\n` | `''` |
| Empty `pages` | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/empty_pages.json --json` | 2 | `{"findings":[{"id":"input_invalid","page":null}],"pagesChecked":0,"verdict":"could-not-evaluate"}\n` | `''` |
| Duplicate exact page entries | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/duplicate_page_entries.json --json` | 0 | `{"findings":[],"pagesChecked":2,"verdict":"clean"}\n` | `''` |
| Non-absolute page URL `/a` | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/relative_page_url.json --json` | 2 | `{"findings":[{"id":"input_invalid","page":"/a"}],"pagesChecked":0,"verdict":"could-not-evaluate"}\n` | `''` |
| Unsupported non-UTF-8 HTML | `/usr/bin/python /tmp/kake-r23-BoundaryManifestKeys-DqAK/canonical_audit.py --manifest /tmp/kake-r23-BoundaryManifestKeys-DqAK/unsupported_non_utf8_html.json --json` | 2 | `{"findings":[{"id":"html_unsupported","page":"https://example.test/a"}],"pagesChecked":1,"verdict":"could-not-evaluate"}\n` | `''` |

The unknown-key, `true`-version, empty-list, and relative-URL inputs all return `input_invalid` / exit 2; the invalid-UTF-8 HTML input returns `html_unsupported` / `could-not-evaluate` / exit 2, not `clean`.

## Limits

- The attempted LSP availability check (`read xd://lsp`) returned `No such tool: xd://lsp`; no LSP status, references, definition, or diagnostics service was mounted, so no semantic LSP checks were available.
- These were local CLI fixtures only. No public URL was fetched and no build, lint, formatter, selftest, or C2 counter was run. No tools were installed or updated.
