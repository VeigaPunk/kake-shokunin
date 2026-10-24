# Attack19 — `invalid_url`

Axis: operability. Scope: frozen `invalid_url` case plus one adjacent URL-parser/policy probe. No production files changed; the added probe is under `/tmp/kake-r22-Attack19/nearest-invalid-port/`.

## Independent expected result

The frozen fixture's canonical href is `http://[invalid`. The unmatched bracket makes the absolute URL malformed; `normalize_http_url` converts URL parsing errors to `URLProblem`, and `evaluate_page` maps that `ValueError` to `canonical_url_invalid`. `audit_manifest` classifies that finding as failed policy (`EXIT_POLICY = 1`). Expected CLI result: exit 1, finding ID `canonical_url_invalid`.

## Frozen matrix case

Command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case invalid_url
```

Matrix process exit: **0**.

Exact stdout:

```text
PASS caseId=invalid_url exit=1 findings=canonical_url_invalid
SUMMARY selection=invalid_url accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

The matrix accepted the case with the independently expected target CLI exit and finding.

## Nearest-neighbor probe

Created a temporary manifest for `https://example.test/project/a.html` with an explicit-head canonical link to `http://example.test:65536/project/a.html`. This is adjacent to the malformed-authority case but exercises the parser's explicit out-of-range-port rejection (`65536`) before the same policy classification.

Public CLI command (the invocation was followed by a shell status-capture suffix, which is not part of the CLI argv):

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack19/nearest-invalid-port/manifest.json --json
```

CLI process exit: **1**. CLI stderr: empty (the capture wrapper separately printed the exit marker).

Exact CLI stdout:

```json
{"findings":[{"id":"canonical_url_invalid","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

## Result

**The scoped claim survives:** both malformed bracket syntax and an out-of-range port are rejected as `canonical_url_invalid`, with policy exit 1. No actionable finding from these probes.

Residual risk / verification gap: these checks cover only the frozen malformed-bracket input and one neighboring invalid-port input. They do not independently establish behavior for other URL parser edge cases or repeat the full matrix; the frozen integrated matrix record reports the 32-case result. No build, lint, formatter, or test suite was run. No tools installed.
