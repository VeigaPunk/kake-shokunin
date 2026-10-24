# Attack20 — `javascript_url`

## Result

**No actionable finding; the bounded attack claim survives.** Independently derived expected result: exit `1`, finding `canonical_url_invalid`. The frozen contract limits canonical destinations to HTTP(S) and maps failed policy to exit 1; `cases.json` assigns `javascript_url` the same exit and finding. The fixture uses `href="javascript:alert(1)"`, while its manifest expects `https://example.test/project/a.html` (`contract.json:4`, `cases.json:23`, `fixtures/javascript_url/page.html`, `fixtures/javascript_url/manifest.json`). This derivation did not use runtime output.

## Frozen matrix case

Command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case javascript_url; rc=$?; printf '\nPROCESS_EXIT=%s\n' "$rc"
```

Process exit: `0` (matrix harness). The case's reported exit is `1`.

Exact stdout:

```text
PASS caseId=javascript_url exit=1 findings=canonical_url_invalid
SUMMARY selection=javascript_url accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0

PROCESS_EXIT=0
```

## Nearest-neighbor probe

Created an isolated fixture under `/tmp/kake-r22-Attack20-probe/javascript-url-neighbor/`. It differs at the same scheme-policy boundary by changing only the scheme casing:

```html
<!doctype html><html><head><link rel="canonical" href="JaVaScRiPt:alert(1)"></head><body></body></html>
```

Manifest: `{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}`

Command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack20-probe/javascript-url-neighbor/manifest.json --json; rc=$?; printf '\nPROCESS_EXIT=%s\n' "$rc"
```

Process exit: `1`.

Exact stdout:

```text
{"findings":[{"id":"canonical_url_invalid","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}

PROCESS_EXIT=1
```

The casing-only neighbor is independently expected to remain a non-HTTP(S) canonical and therefore fail with `canonical_url_invalid`; the public CLI agrees. Thus both the frozen `javascript_url` case and this nearest-neighbor probe support the bounded canonical-policy claim. This single neighbor does not establish general URL-parser conformance. No production files were changed.
