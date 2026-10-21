## Verdict

Recommendation: HOLD — no wrong-host acceptance was observed in this scoped operability attack. This is not an independent admission.

## Findings

None (P0–P3). Both the frozen wrong-host case and the nearest-neighbour homograph fixture were rejected with `canonical_mismatch`, as expected.

## Checked and held

- **Frozen expectation, derived before execution:** `.ufo/waves/round-22/cases.json` declares `wrong_host` with `expectedExit: 1` and `expectedFindings: ["canonical_mismatch"]`. Its manifest expects `https://example.test/project/a.html`; its page uses `https://other.test/project/a.html`.
- **Required matrix command:**
  ```text
  python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case wrong_host
  ```
  Exact output:
  ```text
  PASS caseId=wrong_host exit=1 findings=canonical_mismatch
  SUMMARY selection=wrong_host accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
  ```
- **Nearest-neighbour fixture:** `/tmp/kake-r23-Attack23WrongHost-o8YK/manifest.json` expects `https://example.test/project/a.html`; `page.html` supplies `https://XN--EXMPLE-4NF.TEST.:443/project/a.html`. The Punycode hostname encodes the Cyrillic-a homograph `exаmple.test`; the test also includes uppercase, a trailing dot, and the HTTPS default port. Before running, expected exit/id were `1`/`canonical_mismatch`, because this is a different host from the manifest target.
  Command:
  ```text
  python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-Attack23WrongHost-o8YK/manifest.json --json
  ```
  Exact stdout and observed exit:
  ```text
  {"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
  exit code: 1
  ```
- **Candidate identity:** observed working-tree HEAD was `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`, not the named candidate commit. The read-only check `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --quiet 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc -- scripts/canonical_audit.py .ufo/waves/round-22/matrix.py .ufo/waves/round-22/cases.json .ufo/waves/round-22/fixtures/wrong_host; result=$?; printf 'candidate_file_diff_exit=%s\\n' "$result"` emitted `candidate_file_diff_exit=0`, so the tested auditor, matrix, case list, and fixture matched the named candidate commit.
- No tools were installed or updated.

## Limits

The matrix run covered only the frozen `wrong_host` case, not the full matrix; no live web surfaces were checked. One preliminary local alias probe also ran before the final fixture, using the same scratch path before its files were overwritten: manifest target `https://xn--bcher-kva.example.test/project/a.html`, canonical href `https://XN--BCHER-KVA.EXAMPLE.TEST.:443/project/a.html`. The original alias fixture is no longer retained at that path.

Command:
```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-Attack23WrongHost-o8YK/manifest.json --json
```
Exact stdout and observed exit:
```text
{"findings":[{"id":"canonical_mismatch","page":"https://xn--bcher-kva.example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
exit code: 1
```
This alias result was not classified as a defect: the frozen case specifies rejection of a different host but does not say whether a trailing-dot authority must equal its non-trailing-dot form.
