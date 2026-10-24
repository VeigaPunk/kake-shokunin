## Verdict

Counterexample found: the live lane’s validator digest no longer matches its frozen pin, so replay currently cannot evaluate. A separate `/tmp` probe demonstrated that the new per-case check rejects a corrupted case row even when the old aggregate-only replay matches.

## Findings

- **P1 — Frozen validator pin is stale for the current working tree.**
  - Command: `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py`
  - Output: `b0c4c1cc6f24cfa862bca8eb7abe0c036cce9d0cc6e3ea22a13f024943b9ad15`
  - The pin in `.ufo/waves/round-22/frozen/expected.json` remains `aa1ff6ad1a4aaf76d81ca4b95551cf3cae10b999a08ef428563e86cac1f26c4d`.
  - Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/replay.py --root /home/vgpnk/Projects/shokunin/kake-shokunin`
  - Exact output: `{"verdict": "could-not-evaluate", "id": "snapshot_tampered", "error": "snapshot member digest mismatch"}`; exit **2**.
  - **Impacted claim/axis:** C1’s frozen replay cannot establish the current 32-case result.
  - **Smallest fix:** reconcile the pin with the reviewed validator revision—restore the previously pinned bytes or review the current bytes and update the pin—then rerun replay. Do not treat the earlier clean run as evidence for the current bytes.

## Checked and held

- `git diff c0fd6d53906a42dadfb997ddda2c8162f1adb78a -- .ufo/waves/round-22/frozen/expected.json` showed only the validator pin changing from `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` to `aa1ff6ad1a4aaf76d81ca4b95551cf3cae10b999a08ef428563e86cac1f26c4d`. The old hash matches the c0fd6d5 validator.
- `git diff c0fd6d5 -- .ufo/waves/round-22/cases.json .ufo/waves/round-22/matrix.py .ufo/waves/round-22/fixtures` was empty. At the earlier observation, the working-tree validator hash was `aa1ff6ad…`, and replay was `clean` with 69 inputs verified, 32 cases compared, no per-case mismatches, exit 0. The later observed hash change to `b0c4…` invalidates that result for the current tree.
- **Honesty judgment:** the one-line re-pin to `aa1ff6ad…` was honest for the bytes it matched: the cases, matrix, fixtures, and aggregate oracle were unchanged. It does not validate the current `b0c4…` bytes; re-pinning those is honest only after reviewing that revision.
- In a `/tmp` copy, a wrapper corrupted only the `missing_link` row’s reported findings while preserving the real matrix’s aggregate (`accepted=32`, `total=32`, exit 0), then re-pinned the scratch matrix digest. The new replay reported `missing_link: actual 1/['canonical_multiple'] != oracle 1/['canonical_missing']` and returned `failed` (exit 1). The c0fd6d5 aggregate-only replay returned `clean` (exit 0) on the same report. This demonstrates the per-case check can fail independently of the aggregate.

## Limits

The lane was not modified. The fail-capability probe and its pin changes were confined to `/tmp`; no tools were installed. No builds, linters, or formatters were run.