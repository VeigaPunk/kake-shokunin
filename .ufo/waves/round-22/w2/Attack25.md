# Attack25 — `wrong_query` and duplicate-query neighbor

## Scope and independent expectation

Test target: the task-designated frozen integrated candidate `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (the observed `.ufo` Git `HEAD` was the same revision). No production files or frozen fixtures were changed; the added neighbor fixture is only under `/tmp/kake-r22-Attack25/`.

The frozen manifest sets both the document URL and expected canonical to `https://example.test/project/a.html?x=expected`; the frozen page uses `href="?x=wrong"`. A query-only reference replaces the document URL's query while retaining its scheme, authority, and path. Thus its resolved URL ends in `?x=wrong`, not `?x=expected`. Under the contract's complete-URL comparison this is `canonical_mismatch`, a policy failure (exit `1`). This expectation follows the manifest/page URL resolution and the contract's query-preservation and exit-map rules, not observed CLI output. The `cases.json` expected record agrees.

## Frozen case result

Exact command (status-printing shell wrapper included):

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case wrong_query; rc=$?; printf '\n[exit=%s]\n' "$rc"
```

Observed stdout:

```text
PASS caseId=wrong_query exit=1 findings=canonical_mismatch
SUMMARY selection=wrong_query accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0

[exit=0]
```

Matrix process exit: `0`. The matrix accepted the case's expected public-CLI result: exit `1`, finding `canonical_mismatch`.

I also invoked the public CLI directly on the frozen negative fixture:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/wrong_query/manifest.json --json; rc=$?; printf '\n[exit=%s]\n' "$rc"
```

Observed stdout:

```text
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html?x=expected"}],"pagesChecked":1,"verdict":"failed-policy"}

[exit=1]
```

As a matching-query positive control, the frozen `query_preserved` fixture has a canonical whose resolved URL equals its manifest target, including `x=1&y=2`:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/query_preserved/manifest.json --json; rc=$?; printf '\n[exit=%s]\n' "$rc"
```

Observed stdout:

```text
{"findings":[],"pagesChecked":1,"verdict":"clean"}

[exit=0]
```

## Nearest-neighbor probe

To test the same query-equality boundary for duplicate-parameter loss, I created this isolated fixture:

`/tmp/kake-r22-Attack25/manifest.json`

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html?x=expected","file":"page.html","expectedCanonical":"https://example.test/project/a.html?x=expected"}]}
```

`/tmp/kake-r22-Attack25/page.html`

```html
<!doctype html><html><head><link rel="canonical" href="?x=expected&x=wrong"></head><body></body></html>
```

Independent expectation: resolving the query-only href retains the full query `x=expected&x=wrong`; that is not the expected query `x=expected`. Exact URL comparison therefore predicts `canonical_mismatch`, exit `1`. This neighbor is deliberately close to `wrong_query`: it preserves the expected first value and adds a duplicate key/value, catching a policy/parser path that might discard or collapse duplicate query parameters.

Exact public-CLI command (status-printing shell wrapper included):

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack25/manifest.json --json; rc=$?; printf '\n[exit=%s]\n' "$rc"
```

Observed stdout:

```text
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html?x=expected"}],"pagesChecked":1,"verdict":"failed-policy"}

[exit=1]
```

## Verdict and residual risk

The assigned `wrong_query` claim survives this falsification: its independently expected policy failure is returned, the frozen matching-query control is clean, and the duplicate-query neighbor is rejected rather than silently accepted. This is scoped evidence for query preservation/equality only; it does not independently validate the other 31 matrix cases, the complete C1 capability, browser URL edge cases, or search-engine behavior.

LSP semantic checks were unavailable: `read xd://lsp` returned “No such tool” and listed mounted devices without an LSP device. No references/definition/diagnostics checks were possible; no grep output was used as semantic proof. No tool installs were made.

Report: `.ufo/waves/round-22/w2/Attack25.md`
