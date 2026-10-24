# Attack28 — `script_decoy` falsification

Candidate: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (isolated clone `master` observed at this revision). Production files were not changed.

## Independent expected result

The frozen fixture has one `<link rel="canonical">` in the explicit head with `href="https://example.test/project/a.html"`, matching both the manifest URL and `expectedCanonical`. The other link-looking bytes are inside a `<script>` raw-text element, so they are not an active canonical element. Under the contract's exactly-one-canonical policy, the independently derived result is exit `0`, finding id `clean` (empty findings).

## Frozen case

Command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case script_decoy
```

Exit: `0`

Stdout (exact):

```text
PASS caseId=script_decoy exit=0 findings=clean
SUMMARY selection=script_decoy accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

The observed result matches the independently derived `0` / `clean` expectation.

## Nearest-neighbor probe

Constructed only under `/tmp/kake-r22-Attack28-script-decoy/`. It retains the same manifest target and a canonical-looking matching link inside `<script>`, but removes the active head link. Since script text is not an active link, the independently derived result is exit `1`, finding id `canonical_missing`.

Command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack28-script-decoy/manifest.json --json
```

Exit: `1`

Stdout (exact):

```text
{"findings":[{"id":"canonical_missing","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

## Verdict and residual risk

The claim survives this scoped probe: the frozen decoy does not create a false duplicate, and the neighboring script-only decoy does not satisfy the required canonical. This is limited evidence for the script/raw-text parser boundary, not proof of browser rendering or publishing readiness, and not a full re-run of the matrix.

Report path: `.ufo/waves/round-22/w2/Attack28.md`
