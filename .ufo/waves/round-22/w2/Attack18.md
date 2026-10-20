# Attack18 — `href_empty`

Axis: operability. Scope: the frozen `href_empty` case and one nearest-neighbor probe of the same empty-destination boundary. No production or oracle files were changed; the report is in the private clone at the observed frozen candidate revision `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`.

## Expected result, derived before execution

`.ufo/waves/round-22/cases.json` assigns `href_empty` exit `1` and `canonical_href_missing`; its rationale says an empty `href` is a missing destination even when URL resolution could return the document URL. The fixture has one canonical link in the explicit head with `href=""`, and its manifest's document URL and `expectedCanonical` are both `https://example.test/project/href_empty.html`. Therefore the independent expected result is exit `1`, finding `canonical_href_missing` for that page, not clean/self-canonical. This expectation comes from the frozen case policy, not the run output.

## Frozen public matrix run

Command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case href_empty
```

Process exit: `0`.

Stdout, exactly:

```text
PASS caseId=href_empty exit=1 findings=canonical_href_missing
SUMMARY selection=href_empty accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

Stderr: empty.

## Nearest-neighbor public CLI probe

Created a separate fixture under `/tmp/kake-r22-attack18-sBFu6b/`, with one literal ASCII space (`U+0020`) in the canonical `href` value:

`page.html`:

```html
<!doctype html><html><head><link rel="canonical" href=" "></head><body></body></html>
```

`manifest.json`:

```json
{"version":1,"pages":[{"url":"https://example.test/project/neighbor.html","file":"page.html","expectedCanonical":"https://example.test/project/neighbor.html"}]}
```

Before execution, I expected exit `1` with `canonical_href_missing`: the page has no non-empty canonical destination, and an empty/whitespace-only value must not become a false self-canonical merely because URL resolution can yield the document URL. This expectation follows the frozen non-empty-destination policy applied to the nearest whitespace-only value.

Command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack18-sBFu6b/manifest.json --json
```

Process exit: `1`.

Stdout, exactly:

```json
{"findings":[{"id":"canonical_href_missing","page":"https://example.test/project/neighbor.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

Stderr: empty.

## Assessment

The claim survives this scoped attack: the frozen `href_empty` row matched its expected exit/finding, and the whitespace-only neighbor was rejected with the same missing-destination finding. This is evidence for the tested boundary only, not a conclusion about the other 31 matrix cases or broader publishing readiness. No tools were installed or updated.
