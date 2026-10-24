## Verdict

Counterexample found: a P3 file-descriptor leak on an interrupted intermediate-directory close. The manifest-directory symlink scope change is **not** a regression against `contract.json`’s `fileResolution`.

## Findings

### P3 — `read_page_bytes` can leak the newly opened directory fd

At `scripts/canonical_audit.py:562-563`, the code closes `current_fd` before assigning `next_fd` to it. If that close raises after releasing the old fd, the outer `finally` retries the old fd and never closes the untracked `next_fd`.

**Reproducer command:**
```text
python3 /tmp/kake-r22a2-manifestfd-WZmc/audit_close_interrupt_probe.py /tmp/kake-r22a2-manifestfd-WZmc
```

The harness imports a checksum-matching temp copy and injects an `InterruptedError` after the intermediate-directory fd is opened and the old fd is closed.

**Exact observed output:**
```text
{'before_fds': 6, 'after_audit_before_cleanup': 7, 'leaked_fd': 5, 'result': {'verdict': 'could-not-evaluate', 'pagesChecked': 0, 'findings': [{'id': 'input_invalid', 'page': 'https://example.test/a.html'}], 'exit_code': 2}, 'leaked_fd_count': 1}
```

The impact is on C1’s operability/input-error handling: `audit_manifest` classifies the page as `input_invalid`, but leaves a descriptor open. Smallest fix: transfer ownership before closing the old fd, e.g. `old_fd, current_fd = current_fd, next_fd; os.close(old_fd)`, so the `finally` owns the new fd if close raises.

## Checked and held

- Ordinary manifest/page error paths showed no fd-count change in the repeated harness checks; injected read, parse, `fstat`, page-open, and page-read exceptions were balanced.
- Manifest symlink, directory, FIFO, `/dev/null`, `/dev/zero`, and a trailing-slash manifest path returned exit 2 / `input_invalid`. A relative manifest path succeeded. Page traversal, symlink, FIFO, and directory cases returned `input_invalid`; the FIFO probes completed without hanging. A 500-page manifest returned clean with `pagesChecked: 500`.
- `alias/manifest.json` (where `alias` is the final directory component and a symlink) returned clean. This is **not** a contract regression: `fileResolution` restricts HTML paths relative to the manifest directory; the symlink is in the caller-selected manifest path prefix, which the CLI documents as followed. Page-relative symlinks and traversal remain rejected.
- Frozen matrix command: `cd /home/vgpnk/Projects/shokunin/kake-shokunin && timeout 280 python3 .ufo/waves/round-22/matrix.py --root . --json > /tmp/kake-r22-matrix-out.json; echo "exit=$?"`. Observed `exit=0`; summary: `accepted=32`, `total=32`, `executed=32`, `discrepancies=0`, `toolMissing=false`. Both `symlink_html` and `manifest_traversal` were PASS with actual exit 2 and `input_invalid`.

## Limits

- The fd leak was demonstrated with fault injection modeling an interrupted close; I did not induce an actual signal during the kernel close.
- The `lsp` device is unavailable (`No such tool: xd://lsp`); review used direct source inspection and targeted CLI probes. No builds or linters were run.