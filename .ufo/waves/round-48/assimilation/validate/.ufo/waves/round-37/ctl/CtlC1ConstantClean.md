# Control Receipt — `CtlC1ConstantClean`

- **Control name:** `CtlC1ConstantClean` (C1 constant-clean control)
- **What it skips:** Skips all C1 manifest/check validation and all RFC 9309 `robots.txt` rules ((a) access status 200–299/400–499/500–599, (b) line/BOM/500 KiB parsing, (c) `user-agent` grouping, (d) longest-match wildcard/`$` rules, (e) URL path+query percent-normalization and `/robots.txt` exemption, (f) `check_invalid` faults, and (g) `input_invalid` faults). Honors only the CLI usage line (`--manifest PATH`, exit `64` otherwise), optionally counts `checks` if the manifest is a readable JSON object (`0` on any fault), never opens any `robots` file, and unconditionally outputs `{"version":1,"verdict":"clean","checksEvaluated":N,"findings":[]}` with exit `0`.
- **Tooling installs/updates:** None.

## Deliverables (absolute path and SHA-256)

- `/fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean/robots_audit.py`
  `96c8e7399650e156bc5c46c99872066c719d9a6c90782317f8f88d62ed93618b`
- `/fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean/manifest_1.json`
  `b11e9e0255b9ab9796a5ea26f07833b70e0ada56b91cc0d50c7fbfc559d22189`
- `/fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean/manifest_2.json`
  `57ec141e618d3c8e2c2c1357e9dcc57d8c9d8e8be7eff7b595902b4b6c29131a`

## Commands Run and Exit Codes

1. `timeout 30s python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean/robots_audit.py --manifest /fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean/manifest_1.json`
   - stdout: `{"version":1,"verdict":"clean","checksEvaluated":2,"findings":[]}`
   - exit: `0`
2. `timeout 30s python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean/robots_audit.py --manifest /fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean/manifest_2.json`
   - stdout: `{"version":1,"verdict":"clean","checksEvaluated":3,"findings":[]}`
   - exit: `0`
3. `timeout 30s python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean/robots_audit.py --bad-arg`
   - stdout: *(empty)*
   - exit: `64`

## Score & Critic Review

- **Own score:** Unscored locally (sealed key not accessed; L1 scores via `sealed_count.py --tool-file`). Expected score under declared C1 case structure (`SCORECARD.md` lines 1778–1779: every case has at least one check that does not hold or a fault): `0 / 28` (`met: false`).
- **Counterexample:** `manifest_2.json` (404 with `expect: "disallow"`, 500 with `expect: "allow"`, and 200 with missing `robots` file) requires `verdict: "could-not-evaluate"` (exit `2`) with `exposed`, `blocked`, and `check_invalid` findings, whereas `CtlC1ConstantClean` returns `verdict: "clean"` (exit `0`, `findings: []`).
- **Evidence:** `sealed_count.py` lines 141–157 compare exit code, `verdict`, and `(check, reason)` multiset against `exp`. Any sealed case whose expected verdict is `"clean"` (`findings: []`, exit `0`) is trivially passed by this no-op tool.
- **Impacted axes:** C1 operability / counter falsifiability (`scripts/robots_audit.py`, `.ufo/waves/round-37/sealed_count.py`).
- **Smallest safe correction:** None required if L1's sealed run confirms `passed == 0` (every sealed case expects a non-empty finding set and non-zero exit); if any sealed case passes under `CtlC1ConstantClean`, add at least one failing check to that case before freeze so no case has an all-clean expectation.

## Sandbox Directory Listing (`ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC1ConstantClean`)

```text
total 12
drwxr-xr-x 2 vgpnk vgpnk   75 Oct 23 00:04 .
drwxr-xr-x 5 vgpnk vgpnk   73 Oct 23 00:04 ..
-rw-r--r-- 1 vgpnk vgpnk  398 Oct 23 00:04 manifest_1.json
-rw-r--r-- 1 vgpnk vgpnk  601 Oct 23 00:04 manifest_2.json
-rwxr-xr-x 1 vgpnk vgpnk 1322 Oct 23 00:04 robots_audit.py
```
