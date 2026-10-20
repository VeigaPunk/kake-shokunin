# Attack04 — frozen case `root_relative` (nearest-neighbor falsification)

Seat: KakeR22.Attack04 (leaf, author-side falsifier). Wave 2, round 22.
Frozen integrated candidate: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (live lane HEAD).
Contract BEFORE base: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Production bytes were not modified. No installs or package transactions were performed.

## Scope

Task-authorized checks only: read `cases.json` and the `root_relative` fixture, derive the
expected exit/finding id independently, run the matrix for that case, construct nearest-neighbor
fixtures in `/tmp/kake-r22-A04`, run the public CLI, and report. No production edits, no builds,
no lint/format.

## Frozen fixture (read, unmodified)

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/root_relative/manifest.json`

```json
{"version":1,"pages":[{"url":"https://example.test/project/sub/a.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`page.html`

```html
<!doctype html><html><head><link rel="canonical" href="/project/a.html"></head><body></body></html>
```

Hashes (recorded before and after all probes, unchanged):

```
35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7  scripts/canonical_audit.py
4ee05ea47bba49c94f88867ee3aafca57edcaec0d7397bd121ececd630dfb979  .../fixtures/root_relative/page.html
6b4cb96de7759c84340bf399893c6f6f6019ae8524eb03b7d3953f2a6f3155df  .../fixtures/root_relative/manifest.json
```

### Independent expectation (derived before running, not read from output)

Policy in `contract.json`: exactly one canonical link in the explicit head; rel is an ASCII
case-insensitive token list; resolve the href against the first head `base[href]` or the document
URL; compare a WHATWG-like normalized HTTP(S) URL to `expectedCanonical`, preserving query and
rejecting fragments/credentials; exit 0 = clean.

- One `<link rel="canonical" href="/project/a.html">` inside explicit `<head>`; no base; no body/decoy canonical.
- `rel` token `canonical` (ASCII case-insensitive) matches; href is non-empty.
- `/project/a.html` is a path-absolute (root-relative) reference, unambiguous under both RFC 3986 and WHATWG: resolve against `https://example.test/project/sub/a.html` → `https://example.test/project/a.html`.
- No query, fragment, credentials, or non-HTTP scheme; normalized result equals `expectedCanonical`.

Derived expected: **exit 0, findings `["clean"]`** — identical to the frozen record, but reached independently.

## Runs (exact commands)

### 1. Matrix, frozen case

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case root_relative
PASS caseId=root_relative exit=0 findings=clean
SUMMARY selection=root_relative accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
MATRIX_EXIT=0
```

### 2. Public CLI directly on the frozen fixture

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/root_relative/manifest.json --json
EXIT=0
STDOUT={"findings":[],"pagesChecked":1,"verdict":"clean"}
STDERR=
```

The committed instrument agrees: `matrix-integrated.json` (exit 0, accepted 32/32,
discrepancies 0) records `root_relative` PASS with `actualExit 0`, `actualFindings ["clean"]`,
same stdout; `measure-after.json` names `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`,
`deterministic true`, `sameInstrumentAsBefore true`.

**Frozen case verdict: claim survives.** Expected 0/clean was derived independently and observed
exactly as derived; the matrix contributes one real execution (not a tool-missing row).

## Nearest-neighbor fixture (one edit from the frozen href)

Directory `/tmp/kake-r22-A04/triple_slash/`; same manifest bytes as the frozen fixture; the only
change is one inserted `/` in the href.

`page.html`

```html
<!doctype html><html><head><link rel="canonical" href="///project/a.html"></head><body></body></html>
```

### Independent expectation

This is the same parser boundary (leading-slash relative reference resolved against the document
URL), but the extra slash makes the reference ambiguous between RFC 3986 (empty authority, path
`/project/a.html`) and the WHATWG URL algorithm the contract names. WHATWG, verified with an
independent implementation (`node`'s `new URL`, not this repo's code):

```
$ node -e 'console.log(new URL("///project/a.html","https://example.test/project/sub/a.html").href)'
https://project/a.html
```

Under WHATWG the href resolves to a **different origin** (`project` as host), so the canonical does
not equal `expectedCanonical https://example.test/project/a.html`. The policy therefore requires
rejection (`canonical_mismatch`, exit 1) or an explicit ambiguity rejection
(`canonical_url_invalid`, exit 1). A `clean` verdict is a false clean.

### Run

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-A04/triple_slash/manifest.json --json
EXIT=0
STDOUT={"findings":[],"pagesChecked":1,"verdict":"clean"}
STDERR=
```

### Observed mechanism (direct function probe, read-only import)

```
{"href": "/project/a.html",                "normalized": "https://example.test/project/a.html"}
{"href": "///project/a.html",              "normalized": "https://example.test/project/a.html"}
{"href": "////project/a.html",             "normalized": "https://example.test//project/a.html"}
{"href": "///example.test/project/a.html", "normalized": "https://example.test/example.test/project/a.html"}
```

`urllib.parse.urljoin` silently drops the third slash, so `///project/a.html` is read as the path
`/project/a.html` and compared equal. The function docstring promises to "reject parser
ambiguities"; this input is the canonical example of one and is not rejected.

### Discriminating controls (all in `/tmp/kake-r22-A04`)

| Fixture | Independently derived expectation | Observed |
|---|---|---|
| `triple_slash_expected_project` (same page, expected `https://project/a.html`) | mismatch (tool's own reading is example.test) | exit 1, `canonical_mismatch` |
| `four_slash` (`////project/a.html`) | mismatch under any reading | exit 1, `canonical_mismatch` |
| `triple_slash_doc_host` (`///example.test/project/a.html`) | WHATWG → expected URL → clean; RFC/tool → mismatch | exit 1, `canonical_mismatch` (false failure vs WHATWG) |
| `base_origin_root` (base `https://cdn.example.test/assets/` + `/project/a.html`) | base origin applies → mismatch | exit 1, `canonical_mismatch` (correct) |
| `same_origin_root` (base `https://example.test/project/` + `/project/a.html`) | clean | exit 0, clean |

So the false clean is input-specific, not a generally lenient comparison: the tool demonstrably
resolves `///project/a.html` to `example.test`, while WHATWG resolves it to host `project`.
The paired control `triple_slash_doc_host` shows the same one-slash ambiguity also produces a
false **failure** for a page a browser would treat as canonical-correct.

### Selftest control

```
$ python3 scripts/canonical_audit.py --selftest
SELFTEST_EXIT=0   passed=True cases=56   failed=[]
```

No selftest or frozen matrix case exercises a leading `///` reference: the 32-case set has
`scheme_relative` (`//host/path`) but no three-slash form, and the selftest names contain no such
probe.

## Claim assessment

- **Frozen case `root_relative`: survives.** Expected exit 0 / `clean` derived independently;
  matrix PASS and direct CLI exit 0, stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}`.
- **Boundary claim: does not fully survive.** One inserted slash (`///project/a.html`, same
  parser/policy boundary) is classified `clean` although the contract's WHATWG-like comparison
  yields cross-origin `https://project/a.html`. The capability's stated job — reject mismatching
  canonical signals — fails in the unsafe direction here. The inverse fixture is a false failure,
  which is conservative but still non-WHATWG.

Observed vs inference: the URL mappings above are observed (repo code and node's WHATWG parser).
Actual browser behavior is `[INFERENCE]` only in the sense that it follows the same WHATWG URL
algorithm that node implements; no real browser was run. The tool's own documentation states
"This is a conservative RFC-style subset, not a WHATWG URL implementation" (docstring), so L1 must
decide whether `///` rejection is in scope; the contract policy text, however, explicitly says
"WHATWG-like".

## Remaining unknowns / gaps

- Whether L1 treats `///` as in-scope for round 22 or as a documented RFC-style limit; no
  contract-level finding id exists specifically for ambiguous authority (nearest is
  `canonical_url_invalid`, exit 1).
- No HTTP, headers, redirects, or real-browser rendering exercised (out of contract limits).
- Did not run the full 32-case matrix in this seat (bound to the single assigned case); committed
  `matrix-integrated.json` reports 32/32 with the fixed instrument.

## Suggested L1 follow-up (not implemented, production frozen)

1. Decide whether to reject relative references with more than two leading slashes (or more than
   one slash after an explicit scheme) as `canonical_url_invalid`, or resolve authority with
   WHATWG skip-slash semantics. Rejection is the minimal conservative fix and preserves the
   frozen `root_relative` expectation.
2. Add a `triple_slash` probe to the next selftest and a future matrix case; do not edit frozen
   `cases.json` in this round.
3. Re-run `matrix.py --root .` (expect 32/32) and `--selftest` after any change.

## Hygiene

- No production file changed: `git status --porcelain scripts/` empty after probes; audit hash
  unchanged at `35433e50…`.
- One transient `scripts/__pycache__/` was created by the read-only import probe and removed
  immediately; it was the only live-lane write and is gone (`scripts/` now contains only tracked
  files). No git/jj writes were made.
- Scratch data lives only under `/tmp/kake-r22-A04/`.
