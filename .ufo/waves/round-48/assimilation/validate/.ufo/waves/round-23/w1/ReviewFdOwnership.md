## Verdict

Reviewed `scripts/canonical_audit.py` as stored at candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`. Normal success and the exercised open/read/validation exception paths were fd-balanced. One low-probability cleanup gap remains when the intermediate-directory `os.close(old_fd)` raises before closing its descriptor: the new `current_fd` is cleaned up, but `old_fd` is no longer tracked and leaks. This is a scoped reviewer recommendation on operability, not independent admission.

## Findings

### P3 — Intermediate `close(old_fd)` failure can leak the superseded fd

At candidate `scripts/canonical_audit.py:592-593`, ownership is transferred to `current_fd` before `os.close(old_fd)`. The outer `finally` at line 610 closes only `current_fd`. If closing `old_fd` raises while leaving that descriptor open, the `finally` closes the newly opened directory but cannot close the superseded descriptor. `audit_manifest` catches the resulting `OSError` as a page input failure and continues its page loop, so repeated occurrences can accumulate leaked descriptors.

Exact probe command (run from `/home/vgpnk/Projects/shokunin`; the script loads the pinned source using `git show 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc:scripts/canonical_audit.py`):

```text
python /tmp/kake-r23-ReviewFdOwnership-FxTq/probe_fd_ownership.py
```

Exact observed fault-injection output:

```text
close(old_fd) raises before syscall: OSError: [Errno 5] injected close error before syscall; fd_delta=+[4]/-[]; injected=True
```

The injection raises at the Python `os.close` boundary before invoking the syscall; it demonstrates the untracked ownership path, not that this kernel produced an `EIO` closing a directory. Smallest fix: retain both the superseded and replacement descriptors in the cleanup scope until the superseded close succeeds, and on failure attempt cleanup for every still-owned descriptor while preserving the original exception (accounting for an already-closed descriptor).

## Checked and held

The pinned-source probe exercised a one-component file, a three-level directory path, missing first and later directories, a symlink and regular-file intermediate, missing and symlink leaves, a directory leaf, an oversized leaf, injected read and fstat-classification exceptions, injected `dup` and second-hop `open` `EMFILE`, and traversal rejection. Exact output:

```text
single-component success: ok bytes=5; fd_delta=+[]/-[]; manifest_fd=open
three-level success: ok bytes=6; fd_delta=+[]/-[]; manifest_fd=open
missing first intermediate: InputProblem: page path contains a symlink or inaccessible directory; fd_delta=+[]/-[]; manifest_fd=open
missing after one intermediate: InputProblem: page path contains a symlink or inaccessible directory; fd_delta=+[]/-[]; manifest_fd=open
symlink intermediate: InputProblem: page path contains a symlink or inaccessible directory; fd_delta=+[]/-[]; manifest_fd=open
regular file as intermediate: InputProblem: page path contains a symlink or inaccessible directory; fd_delta=+[]/-[]; manifest_fd=open
missing leaf after two intermediates: InputProblem: page file is missing, a symlink, or unreadable; fd_delta=+[]/-[]; manifest_fd=open
symlink leaf: InputProblem: page file is missing, a symlink, or unreadable; fd_delta=+[]/-[]; manifest_fd=open
directory as leaf: InputProblem: page file is not regular; fd_delta=+[]/-[]; manifest_fd=open
oversize leaf: UnsupportedHTML: HTML exceeds 2097152 bytes; fd_delta=+[]/-[]; manifest_fd=open
read raises OSError: InputProblem: page file cannot be read; fd_delta=+[]/-[]; manifest_fd=open
fstat classification raises: RuntimeError: injected fstat check error; fd_delta=+[]/-[]; manifest_fd=open
dup raises EMFILE: InputProblem: manifest directory cannot be reused; fd_delta=+[]/-[]; manifest_fd=open
second intermediate open raises EMFILE: InputProblem: page path contains a symlink or inaccessible directory; fd_delta=+[]/-[]; manifest_fd=open
traversal rejected before opening: InputProblem: empty, dot, or traversal path component; fd_delta=+[]/-[]; manifest_fd=open
close(old_fd) raises before syscall: OSError: [Errno 5] injected close error before syscall; fd_delta=+[4]/-[]; injected=True
```

These results show that tested paths preserve the caller-owned `manifest_dir_fd` and leave no extra or missing fd, including failures after one intermediate directory has already been opened. The candidate function duplicates the caller's directory fd and the candidate `audit_manifest` caller closes its retained directory fd in a `finally` block.

## Limits

- `read xd://lsp` returned `No such tool: xd://lsp`; no LSP status/references/definition/diagnostics endpoint is mounted. Literal search was used only as fallback, not treated as semantic proof. The pinned source itself was read via `git show` in the probe; the caller check above is from the candidate source.
- The close-failure case is injected before the syscall. Kernel `close` error behavior and multithreaded fd reuse were not reproduced; ordinary OS-backed open/read/path failure cases in the probe balanced.
- No build, lint, formatter, or full test suite was run; no tool was installed.
