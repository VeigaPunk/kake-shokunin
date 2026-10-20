# BoundarySymlinks — round-22 wave-2 falsification

Candidate reviewed: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`, in the required no-hardlinks clone `/tmp/kake-r22-BoundarySymlinks`. The frozen contract is `.ufo/waves/round-22/contract.json`; its `fileResolution` clause says HTML paths are relative to the manifest directory and requires regular files while rejecting symlinks and traversal.

## Findings (severity order)

### P2 — A symlink in an ancestor of the manifest directory is followed for page resolution

`read_page_bytes()` opens the manifest directory with `O_DIRECTORY | O_NOFOLLOW` at `scripts/canonical_audit.py:503-507`, then securely opens each component of the page-relative path (`:511-523`). This blocks a symlink used as a page-path component. However, `O_NOFOLLOW` on `os.open(manifest_dir, ...)` only protects the final component of that pathname; it does not reject a symlink in an ancestor component. `_load_manifest()` constructs `manifest_dir` from the lexical `--manifest` argument (`:609-617`), so a caller can pass a manifest through such an ancestor and the page is read through the same symlink while being reported clean.

Reproducer: `/tmp/kake-r22-symlinked-manifest-dir-9sf3_wi_/alias -> real`, with regular `real/sub/{manifest.json,page.html}`; invoke the public CLI using `/tmp/kake-r22-symlinked-manifest-dir-9sf3_wi_/alias/sub/manifest.json`. The exact result was exit `0`, stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n`, stderr empty. The manifest's `file` value was only `page.html`; the absolute path used to reach its manifest directory traversed `alias`.

This is actionable if the contract's “reject symlinks” promise covers the full page-file resolution path, including the manifest-directory prefix (the user-requested attack scope). It otherwise needs an explicit scope decision: currently the caller-visible `file` value contains no symlink component, and the contract does not separately define whether symlinks in the manifest's own path are permitted.

## Controls and exact CLI observations

All probes used only temporary fixture trees under `/tmp` and the public command form `python3 /tmp/kake-r22-BoundarySymlinks/scripts/canonical_audit.py --manifest <absolute-path> --json`. Outputs below are exact stdout, including the trailing newline; stderr was empty in each case.

| Fixture | Exit | Exact stdout | Result |
|---|---:|---|---|
| Regular manifest + regular matching page (positive control) | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` | Clean |
| Final HTML component `page.html -> target.html` | 2 | `{"findings":[{"id":"input_invalid","page":"https://example.test/project/a.html"}],"pagesChecked":0,"verdict":"could-not-evaluate"}\n` | Correctly rejected |
| Page path `alias/page.html`, where `alias -> real/` | 2 | `{"findings":[{"id":"input_invalid","page":"https://example.test/project/a.html"}],"pagesChecked":0,"verdict":"could-not-evaluate"}\n` | Correctly rejected |
| Manifest path ancestor `alias/sub/manifest.json`, where `alias -> real/` | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` | Follows ancestor symlink; finding above |
| Final manifest component `manifest.json -> ../manifest-target/actual.json`, with a regular matching page beside the link | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}\n` | Manifest symlink is followed |

The final-manifest-symlink result is a residual contract-scope question rather than a confirmed finding: `read_manifest_bytes()` uses `os.open(path, O_RDONLY | O_NONBLOCK | O_CLOEXEC)` then `fstat()` (`scripts/canonical_audit.py:471-484`), so it follows a symlink to a regular manifest. The contract explicitly frames its symlink rule as part of HTML-path resolution, and does not state whether the user-supplied manifest itself must be a non-symlink regular file. If no-follow is intended for the manifest too, this is another gap; otherwise the observed acceptance is consistent with the stated scope.

## Relevant implementation and caller checks

- The existing selftest explicitly covers final HTML symlink and a symlink in the relative page path (`scripts/canonical_audit.py:733-735`); the two negative-control results above match those cases.
- The matrix runner resolves and invokes the canonical entry with `--manifest` (`.ufo/waves/round-22/matrix.py:236-275`); this path does not add a separate symlink check.
- LSP was unavailable in this environment: attempts to read `xd://lsp`, `xd://lsp_status`, and `xd://mcp__lsp_status` returned “No such tool” and listed the mounted devices without an LSP route. A literal reference search was used only as fallback; source lines and public CLI behavior above are the evidence, not grep output.

## Residual risk and verification gaps

The manifest-symlink policy remains unspecified by the contract, and the ancestor-symlink case depends on whether the no-symlink guarantee applies only to components of the manifest's `file` value or to the fully resolved page path. The direct final-file and relative intermediate-directory attacks were rejected. No production files were edited; only this assigned report was written in the lane. No packages/tools were installed. No build, full suite, formatter, or linter was run; these targeted CLI probes are the only runtime verification performed.