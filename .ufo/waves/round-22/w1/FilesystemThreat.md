# Filesystem threat review — offline canonical preflight

## Scope and evidence

The frozen r22 contract defines manifest `pages[].file` paths as relative to the manifest directory, requires regular files, rejects symlinks and traversal, and prohibits network access and normal-mode writes. The implementation brief additionally calls for bounded serialized HTML. The contract's 32-case matrix includes `manifest_traversal` and `symlink_html`, but no special-file or oversize-input case.

At review time, `scripts/canonical_audit.py` was absent from both the lane and the prescribed `/tmp/kake-r22-Implement/scripts/` path. These are therefore conditional threat findings and acceptance requirements, not claims that unseen implementation code is vulnerable or passes. No program, fixture, or live target was executed; no network access or installs were made.

## Findings

### F1 — High when attacker-controlled manifests run in a privileged CI context; otherwise Medium: file-path escape / symlink traversal

- **Exploit path:** A manifest supplies `file: "../../private/config"`, an absolute path, or a path whose final or intermediate component is a symlink to an external file. Checking only the final resolved path can also accept an in-root symlink even though the contract rejects symlinks outright. A check-then-open sequence can be raced if an untrusted writer can change the manifest directory.
- **Evidence:** The frozen contract explicitly requires relative HTML paths, regular files, and rejection of symlinks and traversal; the existing matrix exercises traversal and a symlink HTML path but not intermediate/in-root symlinks or a race. Implementation behavior is unobserved.
- **Impact:** Reads outside the manifest tree violate the boundary and can expose data available to the validator's OS account. Whether any bytes can be exfiltrated depends on output/error behavior; do not echo source contents or raw exceptions.
- **Smallest remediation:** Reject absolute paths and any `..` path component before resolution; do not URL-decode filesystem paths. Reject symlinks at every path component, not just escaping links. For directories writable by an adversary during the run, resolve/open relative to a held directory descriptor with no-follow semantics, then verify the opened descriptor is a regular file before reading. Apply the same regular-file/no-symlink policy to the caller-supplied manifest, or explicitly document that its path is trusted.

### F2 — Medium: unbounded manifest/HTML input can exhaust memory or CPU

- **Exploit path:** Supply a very large JSON manifest, many page records, or a huge HTML file; a whole-file read followed by JSON decoding/parsing can exhaust memory before a useful result is returned.
- **Evidence:** The implementation brief says “bounded” but supplies no numeric caps; the frozen contract specifies neither input-size nor page-count limits. No implementation was available to inspect.
- **Impact:** Local denial of service, especially in automated publishing/CI runs; memory copies during byte decoding and parsing can multiply the input footprint.
- **Smallest remediation:** Make explicit limits part of the CLI contract, enforce them by reading at most `limit + 1` bytes (not trusting `stat` alone), stop before opening pages when the count exceeds its limit, and process/release one page at a time. Suggested starting ceilings: manifest 1 MiB, at most 1,000 pages, at most 10 MiB per HTML file, and at most 64 MiB total HTML bytes per invocation. Exceeding a ceiling is an input failure (exit 2, `input_invalid`), not a policy failure.

### F3 — Medium: special files can block or invoke unintended device behavior

- **Exploit path:** Point `--manifest` or a page `file` at a FIFO, directory, socket, or device node. Opening a FIFO for reading before checking its type can block indefinitely; opening a device can have effects before a later `fstat` rejects it.
- **Evidence:** The contract says HTML regular files only; it does not state a manifest-file type rule or cover special files in the frozen 32 cases. Source behavior is unobserved.
- **Impact:** A stuck preflight, unintended reads, or access to device interfaces under the validator's account.
- **Smallest remediation:** Require a regular file for both manifest and HTML inputs. Avoid blocking opens (`O_NONBLOCK` where available), reject symlinks, and verify the opened descriptor with `fstat` before reading. Return exit 2 / `input_invalid` on non-regular inputs.

### F4 — Low / acceptance boundary: accidental code or network execution

- **Exploit path:** An implementation that launches a browser, evaluates scripts, imports manifest-controlled code, or dereferences URL-valued attributes turns hostile local HTML into code/network input. This is not needed to compare declared canonical URLs.
- **Evidence:** The contract explicitly forbids network access and limits the tool to static HTML; the requested parser is Python's standard-library `HTMLParser`. No implementation was available to verify imports/call sites.
- **Impact:** Violates offline/read-only guarantees and could make attacker-controlled HTML trigger local or remote side effects.
- **Smallest remediation:** Keep the path to `open` + bounded decode + `HTMLParser` + URL string parsing only; never call a URL fetcher, browser, shell, or evaluator. Normal mode must not write files.

## Required bounded fixture set

Keep the frozen 32 policy cases unchanged; add these as supplemental filesystem-safety checks:

1. **Control:** A regular same-directory HTML file and regular JSON manifest produce the expected static result, without writes.
2. **Traversal:** In a temporary tree, create `outside.html` containing a unique `OUTSIDE_CANARY`; try `../outside.html` and an absolute path. Require exit 2 / `input_invalid`; stdout/stderr must not contain the canary.
3. **Symlinks:** Test final-file symlinks to an external file, an in-root file, and a dangling target, plus an intermediate directory symlink. Every symlink is rejected (not merely the one escaping the root), exit 2 / `input_invalid`.
4. **Special files:** Test a FIFO created under the temporary tree, a directory, and (where supported) a Unix-domain socket for both manifest and HTML roles. Run the FIFO case under a short subprocess timeout so a blocking regression fails promptly. Do not create/open device nodes; a symlink-to-device case should be rejected as a symlink before target access.
5. **Size boundaries:** Verify exact-limit input is handled and limit-plus-one is rejected for manifest bytes, a single HTML file, aggregate HTML bytes, and page count. Use a sparse file for the oversized HTML case; ensure rejection occurs without reading it all. Keep the proposed limits above explicit and stable in the tool's help/report.
6. **No execution/fetch:** Include inert `<script>`, `<iframe src>`, `<img src>`, `<meta http-equiv="refresh">`, and URL-looking canonical values in a local HTML fixture. The validator must only parse bytes and compare strings; do not resolve URLs or launch a browser. This fixture uses no live host.

A successful static-policy result establishes only the declared-source comparison in the frozen contract; it does not establish browser rendering, HTTP behavior, Google canonical selection, freshness, or publishing readiness.