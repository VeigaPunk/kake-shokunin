# Attack31 — `manifest_traversal`

## Finding
No actionable defect found in this scope. The traversal-rejection claim survives both the frozen case and the nearest-neighbor probe.

## Independent expected result
The frozen contract says HTML paths are relative to the manifest directory and rejects traversal (`contract.json:4`). The fixture at `fixtures/manifest_traversal/manifest.json` names `../escape.html`, so the path contains a parent component and must be rejected as unevaluable before reading a page: expected exit `2`, finding `input_invalid`. This is derived from the path-policy contract, not from the observed CLI output. The frozen rationale agrees (`cases.json:34`).

The live lane Git HEAD observed read-only was `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`, the frozen integrated candidate.

## Frozen case
Command executed:

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 .ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case manifest_traversal
```

Matrix stdout:

```text
PASS caseId=manifest_traversal exit=2 findings=input_invalid
SUMMARY selection=manifest_traversal accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

Matrix process exit: `0` (the shell wrapper also printed `MATRIX_EXIT=0`). The case returned the independently expected exit and finding.

## Nearest-neighbor fixture and controls
Created only under `/tmp/kake-r22-attack31/`. The probe manifest uses `file: "sub/../page.html"`; `sub/` and `page.html` both exist, and the path would resolve to the in-manifest `page.html` if normalized. That page deliberately has a mismatching canonical, making a page read observable as exit `1`/`canonical_mismatch`. Policy still requires rejecting the `..` component before any page read. Direct-path mismatch, clean-page, and legal `a..b/` component controls check both the read path and the boundary against over-rejecting a non-traversal name.

1. Probe command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack31/manifest_probe_inside.json --json
```

Stdout:

```json
{"findings":[{"id":"input_invalid","page":"https://example.test/site/page.html"}],"pagesChecked":0,"verdict":"could-not-evaluate"}
```

Exit: `2` (expected `input_invalid`).

2. Direct-path mismatch control:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack31/manifest_control_mismatch.json --json
```

Stdout:

```json
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/site/page.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

Exit: `1`. This confirms the same existing page is read and evaluated when addressed directly.

3. Clean direct-path control:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack31/manifest_control_clean.json --json
```

Stdout:

```json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

Exit: `0`.

4. Legal component containing `..` as a substring (`a..b`, not the `..` component):

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack31/manifest_dotdot_substring.json --json
```

Stdout:

```json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

Exit: `0`.

All four outputs matched their independently derived expectations. The probe's `pagesChecked:0`, contrasted with the same `page.html` producing `pagesChecked:1` via the direct-path mismatch control, is consistent with pre-read rejection. Source inspection corroborates the boundary: `scripts/canonical_audit.py:487-499` rejects path components `""`, `"."`, and `".."` before the first `os.open` at line 506; `InputProblem` is mapped to `input_invalid`/exit `2` in `audit_manifest` (`:632-660`).

## Verification gaps / residual risk
The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”), so LSP status/references/definition/diagnostics checks were unavailable; no grep output is used as semantic proof. This is a bounded attack of the specified case and one neighboring lexical form, not a rerun of the full matrix or proof over every filesystem/platform race. No production files were changed; no tools were installed.
