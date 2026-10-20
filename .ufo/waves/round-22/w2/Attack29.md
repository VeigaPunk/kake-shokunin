# Attack29 — `template_decoy`

**Axis:** operability  
**Scope:** frozen integrated candidate `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`; template-content canonical signals only. No production files were changed. The only created fixture is under `/tmp/kake-r22-attack29-template-neighbor/`.

## Expected result, derived before execution

`cases.json:32` sets `template_decoy` to exit `0`, expected finding ID `clean`, and says template content is not an active canonical element. The fixture manifest sets both the document URL and expected canonical to `https://example.test/project/a.html`; the HTML contains one wrong canonical inside `<template>` followed by one matching canonical outside it. Under the frozen contract's exactly-one-canonical-in-explicit-head policy, the template link is inert, leaving exactly one matching active link: expected exit `0`, finding ID `clean` (empty public `findings` array). The fixture's expected result is therefore derived from the case definition, manifest, fixture, and contract—not from observed output.

## Executions

1. Frozen matrix case, exact command:

   ```text
   python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case template_decoy
   ```

   **Exit:** `0` (the observed summary reports `discrepancies=0`; `matrix.py:329` returns `0` when discrepancies are zero).  
   **stdout:**

   ```text
   PASS caseId=template_decoy exit=0 findings=clean
   SUMMARY selection=template_decoy accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
   ```

2. Frozen fixture through the public CLI as a baseline control:

   ```text
   python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/template_decoy/manifest.json --json
   ```

   **Exit:** `0`. **CLI stdout:** `{"findings":[],"pagesChecked":1,"verdict":"clean"}`.

3. Nearest-neighbor fixture through the same public CLI. The `/tmp` page places wrong canonical links in an outer template and a nested template, with the matching canonical still outside both; the manifest's URL and expected canonical are unchanged. The contract therefore independently predicts exit `0`, ID `clean` (empty `findings`).

   ```text
   python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack29-template-neighbor/manifest.json --json
   ```

   **Exit:** `0`. **CLI stdout:** `{"findings":[],"pagesChecked":1,"verdict":"clean"}`.

## Verdict and gaps

**No actionable finding in this scope.** The `template_decoy` claim survives: the frozen case passed, and the nested-template nearest neighbor also produced the independently expected clean result. The parser's template-depth handling is visible at `scripts/canonical_audit.py:161-195,257-262`; the frozen expectation and rationale are at `.ufo/waves/round-22/cases.json:32`.

Residual risk: this is one additional static-parser boundary probe, not browser/WHATWG conformance or an exhaustive malformed-template corpus; the contract expressly limits the capability to explicit-head serialized static HTML. No LSP device was exposed in the available tool inventory, so LSP status/references/definition/diagnostics were unavailable; no grep was used and no caller-map claim is made. No tools were installed.
