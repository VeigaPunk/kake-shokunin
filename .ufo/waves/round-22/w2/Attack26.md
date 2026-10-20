# Attack26 — `base_invalid`

Axis: operability. Tested frozen master candidate `c0fd6d53` (round-22 integrated candidate).

## Finding

No actionable defect found in this scoped attack; the claim survives the frozen case and the nearest-neighbor probe.

Before running either CLI, I derived the frozen case result from the contract policy and fixture: the first head `<base>` has malformed URL `http://[invalid`, and the canonical href `a.html` is relative, so resolution requires an invalid base. Expected result: exit **1**, finding **`base_url_invalid`**. This matches the case rationale in `cases.json` and the contract's policy/finding ID.

## Frozen case reproduction

Exact command:

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 .ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case base_invalid; echo "MATRIX_EXIT=$?"
```

Matrix stdout:

```text
PASS caseId=base_invalid exit=1 findings=base_url_invalid
SUMMARY selection=base_invalid accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
MATRIX_EXIT=0
```

The matrix command exited **0** (the requested case was accepted); its observed public-CLI case result was exit **1**, finding **`base_url_invalid`**.

I also ran the public CLI directly:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/base_invalid/manifest.json --json
```

CLI stdout:

```json
{"findings":[{"id":"base_url_invalid","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

CLI exit: **1**.

## Nearest-neighbor probe

Created an isolated fixture under `/tmp/kake-r22-Attack26/base_invalid_port/`. Its manifest targets `https://example.test/project/index.html` with expected canonical `https://example.test/project/a.html`; its HTML uses `<base href="https://example.test:65536/project/">` followed by the relative canonical `a.html`. Before running it, expected exit **1**, finding **`base_url_invalid`**: the first base has an out-of-range port and is required to resolve the relative canonical.

Exact public CLI command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack26/base_invalid_port/manifest.json --json
```

CLI stdout:

```json
{"findings":[{"id":"base_url_invalid","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

CLI exit: **1**. The nearest neighbor agrees with the independently derived expectation. The relevant implementation validates out-of-range ports in `scripts/canonical_audit.py:370-380` and classifies an invalid first base as `base_url_invalid` in `scripts/canonical_audit.py:555-561`.

## Residual risk and verification gaps

This is one adjacent malformed-base probe, not proof of complete WHATWG URL-parser equivalence; the contract explicitly limits the capability to its stated static policy. No production files were changed and no build, lint, formatter, or broader test suite was run. The LSP device was unavailable (`read xd://lsp` returned “No such tool”), so no LSP caller/definition/diagnostics checks were possible; no grep output was used as semantic evidence. No tools were installed or updated.
