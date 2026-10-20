# Attack21 — `data_url` falsification

**Axis:** operability. **Scope:** frozen `data_url` case plus one nearest-neighbor scheme-case probe; no production files changed.

## Independent expected result

Before running the case, `.ufo/waves/round-22/cases.json` specified `data_url` as `expectedExit: 1`, `expectedFindings: ["canonical_url_invalid"]`, because canonical destinations must use HTTP(S), not `data:`. Its manifest targets `https://example.test/project/a.html`; its HTML contains `<link rel="canonical" href="data:text/plain,canonical">`. The frozen contract allows HTTP(S) canonical URLs only. In the implementation, the URL normalizer rejects schemes other than HTTP(S), the page evaluator maps that URL error to `canonical_url_invalid`, and a policy finding maps to exit 1. Thus the independently derived expected result is exit **1**, finding **`canonical_url_invalid`**.

## Frozen matrix invocation

Command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case data_url
```

Observed matrix process exit: **0** (case accepted; zero discrepancies).

Exact stdout:

```text
PASS caseId=data_url exit=1 findings=canonical_url_invalid
SUMMARY selection=data_url accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

## Nearest-neighbor probe

Created an isolated fixture under `/tmp/kake-r22-attack21.b56rTc/` (not in the repository). Its manifest has the same document and expected canonical URLs. Its page changes only the scheme casing from the frozen `data:` fixture to `DaTa:`:

```html
<!doctype html><html><head><link rel="canonical" href="DaTa:text/plain,canonical"></head><body></body></html>
```

Public CLI command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack21.b56rTc/manifest.json --json
```

Observed exit: **1**.

Exact CLI stdout:

```json
{"findings":[{"id":"canonical_url_invalid","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

## Verdict

**C1 survives this scoped attack.** The frozen `data_url` case and the mixed-case nearest neighbor are both rejected with the expected policy finding and exit. This is not evidence for the entire 32-case matrix or other claims; only the assigned case and this one nearby parser/policy input were exercised here. No production source, oracle, or fixture bytes were changed.

## Residual risk and verification gaps

- Only `data_url` and one capitalization neighbor were run by this seat; no full matrix or selftest was run here.
- The `lsp` device is not mounted in this session (`read xd://lsp` returned “No such tool”); consequently no LSP status/references/definition/diagnostics were available. No grep was used as semantic proof.
- No tools were installed or updated.
