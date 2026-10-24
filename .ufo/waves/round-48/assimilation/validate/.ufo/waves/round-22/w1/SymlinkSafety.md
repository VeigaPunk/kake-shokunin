# Symlink-safety review — round 22

## Scope and evidence

- Axis: operability. Milestone: `offline-canonical-capability`.
- Frozen source: `.ufo/waves/round-22/contract.json` at the required base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
- The contract requires HTML paths relative to the manifest directory, regular files only, and rejection of symlinks and traversal. The independent matrix case table pins `symlink_html` to exit 2 / `input_invalid`; its runtime fixture creates a final-component symlink to a regular target in the same temporary directory. `input_invalid` is the applicable stable finding ID; there is no symlink-specific ID.
- The initial review snapshot lacked `canonical_audit.py`; it later appeared in the author clone at `/tmp/kake-r22-Implement/scripts/canonical_audit.py`. Static review covered its page resolver, audit caller, CLI output path, and selftest fixtures (lines 466–513, 595–635, 803–814, and 701–728). The LSP device is unavailable (`read xd://lsp` returned “No such tool”), so status/references/definition/diagnostics could not be requested. No tests or runtime checks were run; the clone candidate is not present in the lane.

## Static implementation review

No actionable symlink-resolution defect was identified in the candidate source. `read_page_bytes` (466–513) rejects absolute/platform-ambiguous paths and empty, `.` or `..` components; opens each intermediate component relative to the held directory descriptor with `O_DIRECTORY | O_NOFOLLOW`; opens the final component with `O_NOFOLLOW | O_NONBLOCK`; and checks the opened descriptor is regular before bounded reading. `audit_manifest` maps `InputProblem` and relevant OS/path errors to `input_invalid` for the page and exit 2 (595–635); `main` emits the JSON result and returns that exit (803–814). The selftest declares both final-file and parent-directory symlink cases (705–728). These are source observations only, not an execution claim.

The concrete false-green if that chain were reduced to final-path or containment-only checks is recorded as the matrix-under-coverage evidence in `PathTraversal.md` H3: the frozen `symlink_html` fixture is an in-root final symlink, and its expected result is exit 2 / `input_invalid`. The candidate’s descriptor-relative no-follow chain addresses the final and intermediate page-path components; no second finding is raised here.

### Low scope boundary — caller-supplied manifest symlink

The page-file rule does not separately prohibit a symlink supplied as `--manifest`. The candidate opens that path without `O_NOFOLLOW` and requires its opened target to be regular (450–463); `_load_manifest` bases page files on the parent of the supplied, `abspath`-normalized pathname rather than the symlink target’s parent (584–592). This is a concrete behavior, not an asserted contract violation: keep the manifest as operator input and document this base-path choice. A symlinked manifest parent directory may instead be rejected when `read_page_bytes` opens the page-root directory with `O_NOFOLLOW`; the contract does not pin that case.

## Minimum acceptance/rejection pair

Use one temporary directory with a regular manifest and a valid `page.html` whose explicit head has a canonical link equal to the page URL and `expectedCanonical`:

1. `file: "page.html"` names a regular file: accept as clean (exit 0, no findings).
2. `file: "alias.html"` names a symlink to that exact in-tree file: reject with exit 2 and `input_invalid` for the page.

The identical target bytes isolate symlink handling from URL/HTML policy. In particular, the second case must not pass because the resolved target remains within the manifest directory.

## Bounded falsification recipe (not run)

In one temporary directory, use a regular manifest and the page above. Invoke normal mode once with `file: "page.html"` and once with `file: "alias.html"` where `alias.html -> page.html`; pass the absolute manifest path and `--json`. Expected: exit 0 / clean / no findings for the regular file, then exit 2 / `input_invalid` for the symlink page. A clean result for the second invocation falsifies the frozen symlink policy. This pair verifies the observable classification; it does not alone prove the target was never opened, which requires source review of the no-follow check. Do not add symlinks or fixtures to the lane and do not access the network.

## Residual risk and verification gap

The frozen matrix covers only a final-component in-root symlink; the candidate selftest also declares a parent-directory symlink, while `PathTraversal.md` carries the broader traversal and escaping-link falsifiers. The component-by-component descriptor chain is present in source, but was not exercised. Manifest-path symlink semantics remain outside the frozen page-file rule. The candidate has not been integrated into the lane, and no tests, builds, linters, formatters, or runtime checks were run. LSP semantic checks were unavailable as recorded above.