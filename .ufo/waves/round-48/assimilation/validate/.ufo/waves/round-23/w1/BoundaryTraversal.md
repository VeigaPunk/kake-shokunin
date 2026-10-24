## Verdict

No actionable finding in the assigned page-path and manifest-relative confinement operability slice. This scoped result is not an independent lane admission.

## Findings

None (P0–P3).

## Checked and held

- Ran the exact candidate snapshot `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc` of `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py`, copied from `git show` into `/tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py`. SHA-256: `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac`. The lane checkout itself was at `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`; the probes below invoked the candidate snapshot, not that checkout.
- Source evidence in the candidate: `/tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py:563-575` rejects empty, POSIX/Windows absolute, drive-qualified, backslash, empty-component, dot-component, and parent-component paths. Lines `579-610` open each directory and file relative to the retained manifest directory descriptor with `O_NOFOLLOW`, then require a regular file. Lines `731-741` keep input/unsupported findings at `could-not-evaluate` / exit 2, distinct from policy failure and clean.
- Positive control manifest used `file: "nested/good.html"`, a valid canonical document nested under the manifest directory:
  - Command: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/positive-nested-relative.json --json`
  - stdout: `{"findings":[],"pagesChecked":1,"verdict":"clean"}`; stderr: empty; exit: `0`.
- Negative policy control used the same page with expected canonical `https://other.test/`:
  - Command: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/negative-policy-mismatch.json --json`
  - stdout: `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}`; stderr: empty; exit: `1`.
- Path attacks and confinement controls were independent manifests under `/tmp/kake-r23-BoundaryTraversal-imqJ/run/`. For each exact command below, stdout was `{"findings":[{"id":"input_invalid","page":"https://example.test/a.html"}],"pagesChecked":0,"verdict":"could-not-evaluate"}`, stderr was empty, and exit was `2`:
  - POSIX absolute file value `/tmp/kake-r23-BoundaryTraversal-imqJ/run/nested/good.html`: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/attack-posix-absolute.json --json`
  - Parent traversal `../outside.html`: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/attack-parent.json --json`
  - Dot component `./nested/good.html`: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/attack-dot.json --json`
  - Backslash path `nested\good.html`: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/attack-backslash.json --json`
  - Windows drive absolute `C:/outside.html`: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/attack-windows-drive-absolute.json --json`
  - NUL-containing value `bad\u0000name.html` (JSON-escaped NUL): `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/attack-nul.json --json`
  - Final-component symlink `escape.html` to a file outside the manifest directory: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/confinement-final-symlink.json --json`
  - Intermediate-directory symlink `linkdir/page.html` to an outside directory: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/confinement-directory-symlink.json --json`
- Non-clean outcome controls:
  - Unsupported SVG-before-head-close fixture: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/unsupported-svg.json --json` → stdout `{"findings":[{"id":"html_unsupported","page":"https://example.test/a.html"}],"pagesChecked":1,"verdict":"could-not-evaluate"}`, stderr empty, exit `2`.
  - Mixed valid page plus `../outside.html`: `python3 /tmp/kake-r23-BoundaryTraversal-imqJ/canonical_audit.py --manifest /tmp/kake-r23-BoundaryTraversal-imqJ/run/mixed-clean-and-parent.json --json` → stdout `{"findings":[{"id":"input_invalid","page":"https://example.test/a.html"}],"pagesChecked":1,"verdict":"could-not-evaluate"}`, stderr empty, exit `2`. Thus a partially checked manifest with an invalid page is not presented as clean.

## Limits

- The `lsp` device was unavailable: `read xd://lsp` returned the exact prefix `No such tool: xd://lsp. Mounted devices:` and listed mounted devices without `lsp`. Therefore no LSP status, references, definition, or diagnostics were available; no grep output was used as semantic proof.
- Probes ran on the supplied Linux workstation and did not attempt concurrent filesystem mutation/race injection or alternate-OS behavior. No build, lint, formatter, or broad selftest was run; this report covers only the requested public-CLI path/confinement probes.