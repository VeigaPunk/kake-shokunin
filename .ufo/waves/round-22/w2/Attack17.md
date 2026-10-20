# Attack17 — `href_absent`

## Independent expected result

Before executing the candidate, I read the frozen contract, `cases.json`, and `fixtures/href_absent/{page.html,manifest.json}`. The page contains exactly one `<link rel="canonical">` inside an explicit `<head>`, but the element has no `href` attribute. The case rationale requires a non-empty href destination; the contract maps policy failure to exit 1. Expected case result: exit **1**, finding **`canonical_href_missing`** (not missing-link, duplicate, or unsupported-input).

## Frozen matrix run

Command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case href_absent; rc=$?; printf 'EXIT=%s\n' "$rc"
```

Harness exit: **0**. Exact matrix stdout:

```text
PASS caseId=href_absent exit=1 findings=canonical_href_missing
SUMMARY selection=href_absent accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

The fixture result matches the independent expected exit and ID.

## Public CLI control and nearest neighbor

I copied the frozen case into `/tmp/kake-r22-attack17/control/`; its page and manifest SHA-256 values match the frozen fixture (`e8784318226423ae0f061541c1833f52f27c8841adfe94a62f100a531f9ede8b` and `5ca6750bf00571943989846490462ca7bbcf372d1ca0c357145a1abc10971423`, respectively). I constructed one nearest-neighbor fixture in `/tmp/kake-r22-attack17/ws_href/page.html` by changing the absent attribute to ASCII-whitespace-only `href="   "`; it uses the same document URL and expected canonical as the frozen manifest. This attacks the same missing-destination boundary. Expected result by policy: exit **1**, `canonical_href_missing`.

Exact commands and stdout:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack17/control/manifest.json --json; rc=$?; printf 'EXIT=%s\n' "$rc"
```

```json
{"findings":[{"id":"canonical_href_missing","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

CLI exit: **1**.

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack17/ws_href/manifest.json --json; rc=$?; printf 'EXIT=%s\n' "$rc"
```

```json
{"findings":[{"id":"canonical_href_missing","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

CLI exit: **1**.

## Assessment

No actionable defect found for this case or its whitespace-only-href nearest neighbor. The tested claim survives this scoped attack: both absent and whitespace-only hrefs are rejected with the expected policy finding. This does not independently establish the rest of the 32-case matrix or broader publishing readiness.