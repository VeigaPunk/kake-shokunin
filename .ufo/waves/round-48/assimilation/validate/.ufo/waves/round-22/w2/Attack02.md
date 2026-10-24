# Attack02 — frozen case `relative_same_dir`

Seat: KakeR22.Attack02 (fresh author-side falsifier, leaf). Lane:
`/home/vgpnk/Projects/shokunin/kake-shokunin`. Observed lane revision
`c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (`round-22: offline canonical publishing
preflight`); production bytes were read only, never edited. No installs, no builds, no
formatters. Scratch tree: `/tmp/kake-r22-attack02`.

## Question

Does the frozen case `relative_same_dir` hold in the integrated candidate: does
`scripts/canonical_audit.py` resolve a same-directory relative canonical against the
document URL and classify it clean (exit 0, finding `clean`)?

## Independent derivation (made before running the tool)

Sources: `.ufo/waves/round-22/contract.json` (interface, `exitMap`, policy),
`.ufo/waves/round-22/cases.json` (frozen expectation), fixture bytes
`fixtures/relative_same_dir/{manifest.json,page.html}`.

- Fixture manifest: `url = https://example.test/project/index.html`,
  `file = page.html`, `expectedCanonical = https://example.test/project/a.html`.
- Fixture HTML: `<!doctype html><html><head><link rel="canonical" href="a.html"></head><body></body></html>`.
- The head is explicit and closed; it contains exactly one canonical link. `rel` is a
  single ASCII token `canonical`; `href` is present and non-empty.
- RFC 3986 §5.3 resolution against the document URL: base path `/project/index.html`,
  relative reference `a.html` merges to `/project/a.html`; the reference has no query
  or fragment, so the target is `https://example.test/project/a.html` with no query.
- That equals `expectedCanonical`. HTTP(S), no fragment, exactly one head canonical,
  host/path/query all match.
- Contract exit map: clean → exit 0. No finding id is emitted for a clean page; the
  matrix's `observed_findings` maps an empty `findings` array to the synthetic id
  `clean` (`matrix.py:observed_findings`). So the expected pair is **(exit 0, `clean`)**.

This derivation uses only the contract, case rationale, and fixture bytes, not the
tool's observed output.

## Frozen-case execution

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 .ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case relative_same_dir
PASS caseId=relative_same_dir exit=0 findings=clean
SUMMARY selection=relative_same_dir accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
EXIT=0
```

Direct public CLI, same fixture:

```
$ python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/relative_same_dir/manifest.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
EXIT=0
```

Observed: exit 0, empty `findings`, `verdict=clean`, `pagesChecked=1`. Matrix verdict
`PASS`, `accepted=1 total=1 executed=1 discrepancies=0`. This matches the independent
derivation exactly. `--selftest` also exits 0 with every selftest record `ok: true`.

Committed deterministic record (read-only), `measure-after.json`:

- `sourceCommit = c0fd6d53906a42dadfb997ddda2c8162f1adb78a`, two runs with identical
  argv/stdout, `deterministic: true`, `sameInstrumentAsBefore: true`, both run exits 0,
  `accepted = 32`, `total = 32`, `matrixExitCode = 0`.
- Row: `caseId=relative_same_dir`, `status=PASS`, `expectedExit=0`, `actualExit=0`,
  `expectedFindings=["clean"]`, `actualFindings=["clean"]`,
  `stdout={"findings":[],"pagesChecked":1,"verdict":"clean"}\n`, `stderr=""`.

## Nearest-neighbor fixture attacking the same boundary

Boundary under attack: relative-reference resolution against the document URL — here
the two non-trivial rules the frozen fixture does not exercise: explicit dot-segment
(`./`) collapse and **non-inheritance of the document URL's query string**. A resolver
that merged the base query into the relative target (a common RFC 3986 §5.3 bug) would
return `.../a.html?ref=feed`.

Fixture tree `/tmp/kake-r22-attack02/relative_same_dir_nn/` (own /tmp, no lane writes):

`page.html`
```html
<!doctype html><html><head><link rel="canonical" href="./a.html"></head><body></body></html>
```

`manifest.json` — deliberately declares the query-keeping target as expectation (NN-2):
```json
{"version":1,"pages":[{"url":"https://example.test/project/index.html?ref=feed","file":"page.html","expectedCanonical":"https://example.test/project/a.html?ref=feed"}]}
```

`manifest-positive.json` — positive control (NN-1):
```json
{"version":1,"pages":[{"url":"https://example.test/project/index.html?ref=feed","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

Pre-run derivation (stdlib `urljoin`, run separately, no tool import):
`urljoin("https://example.test/project/index.html?ref=feed", "./a.html")`
= `https://example.test/project/a.html`. Therefore:

- NN-1 expected: resolved target equals declared expectation → **exit 0, clean**.
- NN-2 expected: resolved target (no query) ≠ declared expectation (with
  `?ref=feed`) → **exit 1, `canonical_mismatch`**. A query-inheriting implementation
  would instead return clean, so NN-2 discriminates the bug.

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack02/relative_same_dir_nn/manifest-positive.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
EXIT=0
$ python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack02/relative_same_dir_nn/manifest.json --json
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html?ref=feed"}],"pagesChecked":1,"verdict":"failed-policy"}
EXIT=1
```

Both observed results match the independently derived expectations. The candidate
resolves `./` same-directory references correctly and does not leak the document URL's
query into a path-relative target; the mismatch is reported as policy exit 1, not as an
input/unsupported exit 2.

## Verdict

**Claim survives.** For frozen case `relative_same_dir` the integrated candidate
`c0fd6d5` emits exit 0 with an empty findings array (`clean`) exactly as independently
derived from the contract policy and fixture bytes. The matrix harness marks it
`PASS` (`accepted=1 total=1 executed=1 discrepancies=0`), the direct public CLI agrees,
and the committed two-run deterministic measure record confirms the same row at the
measured revision.

Observed facts: the three commands above and their exits/stdout; the `measure-after.json`
row. Inference: none required for the verdict. Remaining unknowns: this seat did not
re-run the full 32-case matrix (out of scope; `measure-after.json` records 32/32) and
did not probe whitespace-padded `href`, which the tool documents as rejected by policy
(`canonical_url_invalid`) rather than browser-style stripped; that is a documented
boundary choice outside the frozen case and outside this seat's authorization.
