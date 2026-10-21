## Verdict

Recommend HOLD on operability for candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`: one P2 false-clean remains for raw Unicode C1 control characters in URL paths. This is an author-side recommendation, not independent admission. The lane HEAD observed was `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`; all candidate CLI probes used `scripts/canonical_audit.py` extracted from the exact candidate commit into `/tmp/kake-r23-BoundaryURLAuthority-VFrZ/`.

## Findings

### P2 — Raw C1 controls in canonical paths are percent-escaped and accepted as clean

- **Evidence:** `scripts/canonical_audit.py:459-460` rejects code points `<= 0x20` and exactly `0x7f`, but not U+0080–U+009F. At `:493-498`, path and query values are passed through `quote`, which UTF-8 percent-escapes U+0080–U+009F instead of rejecting them. `evaluate_page` at `:655-663` returns no finding when that normalized value equals the expected canonical URL.
- **Fixture:** A canonical `href` containing raw U+0085 (Unicode category `Cc`) was compared against the equivalent percent-encoded expected URL `.../a%C2%85b.html`. RFC 3987 §2.2 excludes U+0080–U+009F from `ucschar` (the listed range begins at U+00A0), so this raw C1 control is outside the advertised conservative RFC-style IRI subset. Public source: <https://www.rfc-editor.org/rfc/rfc3987#section-2.2>.
- **Exact command:**
  ```text
  python3 -B /tmp/kake-r23-BoundaryURLAuthority-VFrZ/candidate_canonical_audit.py --manifest /tmp/kake-r23-BoundaryURLAuthority-VFrZ/report-fixtures/c1_control/manifest.json --json
  ```
- **Exact observed output:** exit 0; stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}`; stderr empty.
- **Range confirmation:** The public CLI was also run against all 32 U+0080–U+009F C1 code points as raw canonical path characters, with expected values percent-encoded. Exact command: `python3 -B /tmp/kake-r23-BoundaryURLAuthority-VFrZ/prepare_c1_sweep.py && python3 -B /tmp/kake-r23-BoundaryURLAuthority-VFrZ/candidate_canonical_audit.py --manifest /tmp/kake-r23-BoundaryURLAuthority-VFrZ/report-fixtures/c1_sweep/manifest.json --json`. Exact stdout: `prepared 32 C1 control pages` followed by `{"findings":[],"pagesChecked":32,"verdict":"clean"}`; exit 0.
- **Impacted claim/axis:** Operability. A URL containing a raw control in the canonical path is reported `clean`, rather than rejected as an invalid URL; the output does not mark the case unsupported or otherwise distinguish it from a valid matching URL.
- **Smallest fix:** Extend the raw-character guard to reject the C1 range as well (e.g. reject `0x80 <= ord(ch) <= 0x9f` in addition to the existing C0/DEL check) before `urlsplit`/`quote`; cover both path and query inputs.

## Checked and held

- **Positive control:** Matching ordinary HTTPS URL through the public CLI returned exit 0 and `{"findings":[],"pagesChecked":1,"verdict":"clean"}`.
- **Negative control:** Wrong-host canonical URL returned exit 1 and `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}`.
- Credential-bearing canonical `href` was rejected as `canonical_url_invalid` (exit 1, `failed-policy`). Credential-bearing manifest document/expected URLs produced `input_invalid` (exit 2, `could-not-evaluate`, `pagesChecked:0`).
- Empty-host URLs were rejected: canonical `href` `https:///project/a.html` produced `canonical_url_invalid`; the same malformed URL as the manifest document URL produced `input_invalid`/`could-not-evaluate`.
- Invalid ports (`:abc`, `:65536`) and a 100,000-digit all-9 port were rejected as `canonical_url_invalid` (exit 1). IPv6-zone forms with both raw `%` and RFC 6874 `%25` were rejected as `canonical_url_invalid`; the normal bracketed IPv6 control was clean. Boundary checks for ports 0 and 65535, an empty port, and a 100,000-zero prefix before a valid port were clean; they were not treated as invalid-port defects.
- ASCII space, tab, NUL, and DEL in canonical `href` values were rejected as `canonical_url_invalid`. NBSP and EM SPACE in paths were percent-escaped and matched; these printable non-ASCII path characters were held as consistent with the documented non-ASCII path behavior, not conflated with C1 controls.
- No URL probe was classified as `html_unsupported`; malformed canonical URLs produced policy findings, while malformed manifest URLs produced `could-not-evaluate` input findings.
- No source, index, or lane state was changed. Only this report was written inside the lane. The preliminary dynamic fixture runners briefly created `TemporaryDirectory` fixtures under `/tmp/url-authority-*` and `/tmp/url-matched-*`, outside the requested scratch prefix; their Python context managers removed them after each case. Retained fixtures/runners are under `/tmp/kake-r23-BoundaryURLAuthority-VFrZ/`. No tool was installed or updated.

## Limits

- LSP is not mounted in this environment: `read xd://lsp` returned `No such tool: xd://lsp` and listed the mounted devices without an LSP device. Thus no LSP status, references, definition, or diagnostics checks were available. Text search was used only to locate source regions; semantic conclusions above are based on the candidate source lines and public-CLI observations, not grep output.
- This was a targeted offline fixture/CLI review. No build, lint, general self-test, publishing action, or live web-property check was run. Python runtime observed: `Python 3.14.8`.
