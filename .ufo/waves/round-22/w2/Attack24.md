# Attack24 — `wrong_path` and encoded-dot neighbor

## Scope and independent expectation

Test target: the task-designated frozen integrated candidate `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`. No production files were changed; the neighbor fixture lives only under `/tmp/kake-r22-Attack24-neighbor/`.

Before running the case, `.ufo/waves/round-22/cases.json:27` specified `wrong_path` as exit `1` with finding `canonical_mismatch`. Its manifest expects `https://example.test/project/a.html`, while its HTML links to `https://example.test/project/other.html`. The scheme and host agree but the normalized paths do not, so the contract's URL-equality policy independently predicts `canonical_mismatch` and policy exit `1`.

## Frozen case result

Exact command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case wrong_path
```

Observed matrix stdout:

```text
PASS caseId=wrong_path exit=1 findings=canonical_mismatch
SUMMARY selection=wrong_path accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

Matrix process exit: `0` (also confirmed by a second invocation with an exit-status print). The tested public CLI case itself returned the expected exit `1`, as reported by the matrix.

## Nearest-neighbor probe

Created this isolated fixture:

`/tmp/kake-r22-Attack24-neighbor/manifest.json`

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`/tmp/kake-r22-Attack24-neighbor/page.html`

```html
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/other/%2E%2e/a.html"></head><body></body></html>
```

Independent expectation: the case-insensitive encoded `..` segment `%2E%2e` removes the preceding `other` segment, leaving `/project/a.html`; therefore this URL is equivalent to the expected canonical under the candidate's declared dot-segment normalization and should be clean (exit `0`, no findings). This expectation follows the frozen URL-equality policy and the source normalization rule at `scripts/canonical_audit.py:384-405`, not the observed output.

Exact public-CLI command (the shell wrapper prints the CLI status after capturing it):

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack24-neighbor/manifest.json --json; status=$?; printf '\ncommand_exit=%s\n' "$status"; exit "$status"
```

Observed stdout:

```text
{"findings":[],"pagesChecked":1,"verdict":"clean"}

command_exit=0
```

## Verdict and residual risk

The `wrong_path` claim survives this check: the frozen wrong-path fixture is rejected with the independently expected finding, while a textual path containing a normalized encoded-dot segment that resolves to the expected path is accepted. This is a focused probe only; it does not establish the other matrix cases or broader browser/search-engine URL behavior, which the contract expressly limits.

LSP semantic checks were unavailable: attempting to read `xd://lsp` returned “No such tool” and listed mounted devices without an LSP device. No references/definition/diagnostics checks were possible; no grep output was used as semantic proof.