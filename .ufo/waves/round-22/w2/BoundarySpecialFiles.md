# Special-file boundary review — Kake r22

## Scope and evidence

- Axis: operability. Milestone: `falsify-canonical-capability`.
- Frozen contract: `.ufo/waves/round-22/contract.json`; its manifest interface requires regular-file inputs, rejects non-regular page files, and maps unreadable/unsupported inputs to exit 2 (`input_invalid` / `html_unsupported`).
- Candidate source: `scripts/canonical_audit.py`, at integrated revision `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (`git rev-parse HEAD`). No production source was modified.
- LSP: `read xd://lsp` returned “No such tool” and listed the mounted devices without an LSP device. Thus status/references/definition/diagnostics could not be requested; grep was used only to locate literal line numbers, not as semantic proof. Review conclusions below are based on the source read and the bounded CLI observations.
- Runtime checks used one private `/tmp` fixture tree, `python3 -B scripts/canonical_audit.py --manifest <path> --json`, and a 3-second subprocess timeout per invocation. No FIFO writer was opened. All six calls returned in 0.033–0.034 seconds; none timed out. The temporary tree was removed after the checks.

## Code review

No actionable special-file handling defect was identified.

- `read_manifest_bytes` opens with `O_NONBLOCK` (`scripts/canonical_audit.py:471-475`) before checking the opened descriptor with `fstat`/`S_ISREG` (`:476-478`). A FIFO with no writer therefore does not block on open, and a directory or FIFO is rejected as `InputProblem` before reading.
- `read_page_bytes` opens the final page component with `O_NONBLOCK` (`:503-504`) and checks `S_ISREG` on the descriptor before bounded reading (`:523-524`). Directories and FIFOs are rejected as `InputProblem`; the existing descriptor-relative, no-follow traversal is retained.
- `audit_manifest` maps manifest open/shape errors to `could-not-evaluate`, `pagesChecked: 0`, `input_invalid`, exit 2 (`:620-630`); it maps page open/shape errors to a page-scoped `input_invalid`, and input findings take precedence for the verdict/exit (`:638-652`). `main` emits the public JSON object and returns that code (`:862-873`).

## Bounded public-CLI observations

Every invocation below used a 3-second timeout. Stderr was the empty string (`""`) for each. Outputs are recorded exactly, including their trailing newline.

| Case | Manifest argument | Elapsed | Timed out | Exit |
|---|---|---:|---|---:|
| Positive regular-file clean control | `/tmp/kake-r22-boundary-special-files-zg8_n7a_/positive-clean/manifest.json` | 0.033s | no | 0 |
| Negative regular-file policy control | `/tmp/kake-r22-boundary-special-files-zg8_n7a_/negative-policy/manifest.json` | 0.034s | no | 1 |
| Directory passed as manifest | `/tmp/kake-r22-boundary-special-files-zg8_n7a_/directory-manifest` | 0.033s | no | 2 |
| FIFO passed as manifest (no writer) | `/tmp/kake-r22-boundary-special-files-zg8_n7a_/fifo-manifest/manifest.json` | 0.034s | no | 2 |
| Directory referenced as HTML page | `/tmp/kake-r22-boundary-special-files-zg8_n7a_/directory-html/manifest.json` | 0.033s | no | 2 |
| FIFO referenced as HTML page (no writer) | `/tmp/kake-r22-boundary-special-files-zg8_n7a_/fifo-html/manifest.json` | 0.033s | no | 2 |

Exact stdout for positive regular-file clean control:

```text
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

Exact stdout for negative regular-file policy control:

```text
{"findings":[{"id":"canonical_missing","page":"https://boundary.test/site/page.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

Exact stdout for directory manifest and FIFO manifest (same result for both):

```text
{"findings":[{"id":"input_invalid","page":null}],"pagesChecked":0,"verdict":"could-not-evaluate"}
```

Exact stdout for directory HTML and FIFO HTML (same result for both):

```text
{"findings":[{"id":"input_invalid","page":"https://boundary.test/site/page.html"}],"pagesChecked":0,"verdict":"could-not-evaluate"}
```

These controls distinguish the intended clean and policy-failure paths (0 / 1) from special-file refusal (2). Both directory positions and both no-writer FIFO positions refused within the timeout.

## Findings by severity

None. The observed behavior and the reviewed open/fstat/error-mapping path satisfy this assignment’s FIFO/directory refusal boundary.

## Residual risk and verification gaps

- This is a bounded Linux CLI check, not a race-stress test or a cross-platform guarantee. No whole-host write/network confinement claim is made.
- The script selftest includes a FIFO HTML case (`scripts/canonical_audit.py:736`) but does not itself enumerate directory or FIFO-manifest inputs. Those shapes were exercised here through the public CLI; no full selftest/matrix run was performed.
- No LSP checks were possible because the LSP device is unavailable.

Report: `.ufo/waves/round-22/w2/BoundarySpecialFiles.md`
