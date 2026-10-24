# Attack30 — `missing_head`

Axis: operability. Candidate revision observed in the required no-hardlinks clone: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`.

## Frozen case

Before running it, `.ufo/waves/round-22/cases.json` independently specifies `missing_head` as `expectedExit: 2` and `expectedFindings: ["html_unsupported"]`. Its fixture is `<!doctype html><html><body><p>This document has no explicit head element.</p></body></html>`; the contract requires exactly one canonical link in an explicit head and classifies unsupported input shapes as exit 2. Therefore the expected result is unsupported, not a policy mismatch.

Command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case missing_head
```

Matrix runner exit: `0`. Exact stdout:

```text
PASS caseId=missing_head exit=2 findings=html_unsupported
SUMMARY selection=missing_head accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

The case's public-CLI result is exit `2`, finding `html_unsupported`; the matrix accepted it with no discrepancy.

## Nearest-neighbor public-CLI probe

Created an isolated fixture under `/tmp/kake-r22-Attack30-neighbor/`. Its page differs in the relevant boundary by adding an explicit empty `<head></head>` before the original body; it contains no canonical link. From the stated policy, this should now be a supported document with a policy finding `canonical_missing`, exit `1` (not `html_unsupported`).

Command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack30-neighbor/manifest.json --json
```

Exit: `1`. Exact stdout:

```text
{"findings":[{"id":"canonical_missing","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

## Verdict

No actionable finding in this scope. The frozen `missing_head` expectation survives, and the one-element neighbor cleanly distinguishes an absent explicit head from an explicit-but-canonical-missing head. No production files were changed; this report is in the assigned cloned workspace.

Residual risk / verification gap: this is one frozen matrix case plus one adjacent fixture only; it does not establish the rest of the 32-case matrix or broader browser/HTML conformance. No build, test suite, lint, or formatter was run.
