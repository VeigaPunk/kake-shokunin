# Case20 — `javascript_url`: canonical href carrying a `javascript:` URL

Seat: `KakeR22.Case20` (scout, leaf, read-only). Snapshot **2026-10-20T21:39Z**.
Lane base `7c61c8cc791bde36dd5e3688bdfea2678d90146c` (= `git rev-parse HEAD` at snapshot).

Files changed: **this report only**. No repository script, matrix, measure, or selftest was run;
no tool was installed or upgraded; no package transaction, service, credential, or live-property
call was made. The only executions were in-memory `urllib.parse` probes in `/tmp` to establish
stdlib behavior (disclosed below); they are not a run of `canonical_audit.py`.

## Contract anchor

Frozen `contract.json` policy, verbatim:

> Exactly one canonical link in explicit head per page, rel ASCII case-insensitive token list;
> resolve href with first head base href or document URL; compare WHATWG-like HTTP(S) normalized
> absolute URL to expectedCanonical, preserve query, reject fragments and credentials.

Exit map: `0` clean · `1` failed policy · `2` could-not-evaluate input/unsupported shape · `64` usage.
Case name in the frozen 32-case matrix: `javascript_url`.

## Concrete fixture

Manifest (path `fixtures/javascript_url/manifest.json`, HTML paths relative to the manifest
directory):

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`fixtures/javascript_url/page.html` — one line plus trailing LF, **104 bytes**, SHA-256
`7b5701679250236f510d32858319a5f81bc0f860089c49816465dd272fe854e7`:

```html
<!doctype html><html><head><link rel="canonical" href="javascript:alert(1)"></head><body></body></html>
```

Readable expansion (same bytes after collapsing the single line):

```html
<!doctype html>
<html>
  <head>
    <link rel="canonical" href="javascript:alert(1)">
  </head>
  <body></body>
</html>
```

| field | value |
|---|---|
| page URL (manifest) | `https://example.test/project/a.html` |
| expectedCanonical | `https://example.test/project/a.html` |
| href | `javascript:alert(1)` |
| canonical links in explicit head | 1 |
| `rel` | `canonical` (single token, lowercase) |
| `<base>` | none — the href is absolute, so base/document resolution cannot change it |
| negative-control sibling | `absolute_match` (identical manifest; only the href differs) |

The fixture is deliberately single-variable: same manifest URL/expectedCanonical and same
one-line HTML shell as `absolute_match`; the only mutation is the `href` value. The
`javascript:` payload is inert data — no validator path executes it, and the contract forbids JS.

## Expected result

| field | expected |
|---|---|
| process exit | **1** |
| finding id (matrix-asserted) | **`canonical_url_invalid`** |
| findings count | exactly 1 |
| stdout JSON | `{"verdict":"failed-policy","pagesChecked":1,"findings":[{"id":"canonical_url_invalid","page":"https://example.test/project/a.html"}]}` |
| stdout/stderr | no traceback; JSON object on stdout |

The `page` value is an implementation choice; the contract only requires each finding to carry
`id` and `page`, and the matrix reads only `findings[].id`. `verdict` spelling is also unconstrained
by the contract; `failed-policy` is the current implementer's value.

## Why exit 1 and this id

1. **The document shape is evaluable.** Explicit `<head>`/`</head>`, one `link` descendant, one
   `rel="canonical"` token, `href` present and non-empty. The bytes are ASCII (valid UTF-8),
   single-line, with no script/template/comment decoys or `<base>`, so no `HTMLParser` limitation
   named in the contract is exercised. Nothing here triggers
   `canonical_missing`, `canonical_multiple`, `canonical_outside_head`, `canonical_href_missing`,
   `base_url_invalid`, or `html_unsupported`.
2. **The href is a syntactically valid URL — not a parse error.** WHATWG URL defines a valid
   `absolute-URL string` to include "a URL-scheme string that is not an ASCII case-insensitive
   match for a special scheme, followed by U+003A (:) and one of: a scheme-relative-URL string, a
   path-absolute-non-authority-URL string, or an opaque-path-URL string"
   (<https://url.spec.whatwg.org/#valid-url-string>, accessed 2026-10-20). `javascript` is not a
   special scheme; the special-scheme table lists only `ftp`, `file`, `http`, `https`, `ws`, `wss`
   (<https://url.spec.whatwg.org/#special-scheme>). `javascript:alert(1)` is therefore a valid
   absolute URL with an opaque path. HTML's `link` requirement — "If the href attribute is present,
   then its value must be a valid non-empty URL potentially surrounded by spaces"
   (<https://html.spec.whatwg.org/multipage/semantics.html#the-link-element>, accessed 2026-10-20)
   — is satisfied. Consequently `canonical_url_invalid` here means **outside the tool's explicit
   HTTP(S) subset**, not "unparseable URL". The finding text must not claim malformed syntax.
3. **Parser-only or exception-driven validation false-greens.** CPython's `urlsplit()` "does not
   perform validation" (`PythonURL.md` Q1/Q3, docs accessed 2026-10-20). Observed on the host
   interpreter (3.14.8): `urlsplit("javascript:alert(1)")` returns
   `scheme='javascript', netloc='', path='alert(1)'` without raising, and
   `urljoin("https://example.test/project/a.html", "javascript:alert(1)")` returns the href
   unchanged because it is absolute. The rejection must be an explicit scheme allowlist
   (`scheme in {"http","https"}`) applied to the parsed href.
4. **The policy comparison cannot succeed.** The contract compares an HTTP(S) normalized absolute
   URL to `expectedCanonical`; a `javascript:` URL has no HTTP(S) normalization, so policy fails
   before (and independently of) any host/path/query comparison. Under a component-wise comparison
   the schemes already differ (`javascript` vs `https`), so exit 0 is impossible without a
   shortcut (see the attack below).
5. **Exit 1, not exit 2.** The file is readable, the HTML is in-scope explicit-head serialized
   markup, and the href is syntactically decidable. Exit 2 is reserved for "could-not-evaluate
   input/unsupported shape" — unreadable/unsafe input, missing head, unsupported document shape.
   A well-formed page that violates URL policy is exactly what exit 1 is for. Sibling case
   `invalid_url` is also exit 1, confirming that URL admissibility (syntax or scheme) is policy,
   not input-shape. Routing bad schemes to exit 2 would let a publisher evade the policy gate by
   changing the canonical scheme — a fail-open.
6. **Authority boundary.** RFC 6596 §3 is silent on non-HTTP schemes and has no HTML mechanics
   (`RFC6596.md`: "neither permits nor forbids them by name"); the HTML spec defines the canonical
   relation but not scheme restrictions (`HTMLLink.md`); Google's guidance requires `<head>` and
   recommends absolute URLs but defines no `javascript:` canonical case (`GoogleCanonical.md`). The rejection
   is the frozen contract's local HTTP(S) policy, reinforced by the implementation brief's
   "Reject URL credentials/fragments/bad schemes/authority". Do not label it an RFC or HTML
   conformance violation.

## Finding-id stability (operability-critical)

- `canonical_url_invalid` is the broad "URL is outside the supported HTTP(S) subset" bucket,
  deliberately shared with `invalid_url` and `data_url`. The independent matrix snapshot at
  2026-10-20T21:39Z already freezes `caseId: "javascript_url"`, `expectedExit: 1`,
  `expectedFindings: ["canonical_url_invalid"]`, rationale "canonical destinations must use
  HTTP(S), not the javascript scheme." The implementer snapshot at the same time emits
  `canonical_url_invalid` for its `javascript_url` selftest. **Do not introduce a parallel
  `canonical_url_scheme` id at this point** — the matrix is the measuring oracle and the two sides
  currently agree. If L1 prefers a sharper id, change Matrix and Implement together before the
  first measured run.
- Do **not** emit `canonical_mismatch` here. Exit would remain 1, but the id would not match the
  frozen oracle, and review would lose the distinction between "wrong destination" and "not an
  HTTP(S) destination".
- Precedence note (static reading of the implementer snapshot, not executed): the normalizer checks
  for a literal `#` before parsing the scheme, so a hypothetical
  `href="javascript:alert(1)#x"` would produce `canonical_fragment`, not
  `canonical_url_invalid`. The frozen fixture has no fragment, so Case20 is unaffected; document
  the precedence before adding any combined-violation fixture.
- Wording note: the id is `..._invalid`, but the URL is syntactically valid. If the JSON schema
  ever gains a `detail`/message field, use "scheme is not http/https", never "malformed URL".

## Adjacent false-green attack (one, distinct from the case)

**Fixture `javascript_url_embedded`** — same manifest, page:

```html
<!doctype html><html><head><link rel="canonical" href="javascript:https://example.test/project/a.html"></head><body></body></html>
```

Expected: exit **1**, finding id **`canonical_url_invalid`**.

Why it is adjacent and distinct: the frozen case's payload `alert(1)` contains neither the
expected URL nor its path or basename, so it mainly proves the scheme check exists (or forces the
id distinction). The embedded payload places the **exact expected canonical string** inside the
`javascript:` URL's opaque path. Observed on the host interpreter:
`urlsplit("javascript:https://example.test/project/a.html")` returns
`scheme='javascript', path='https://example.test/project/a.html'`. This false-greens
implementations that:

- strip a `javascript:` (or any `scheme:`) prefix as "sanitization" and compare the remainder;
- use `href.endswith(expected)`, `expected in href`, or another containment/suffix shortcut;
- compare only a trailing path segment/basename (`a.html`) or otherwise ignore the scheme.

Correct handling: apply the scheme allowlist to the parsed href **before** any comparison, and
compare component tuples (scheme, host, port, path, query) — never containment, prefix-strip, or
basename equality. The static implementer snapshot already applies its scheme allowlist before
comparison (`normalize_http_url`, scheme check at the static line ~388), so this is a regression
pin, not a live defect claim. Place it in `--selftest` (isolated `mkdtemp` tree) and/or a reviewer
falsification; do **not** add a 33rd case to the frozen matrix.

Related but not the chosen attack: a manifest whose `expectedCanonical` is itself
`javascript:...` must not define the policy. The expected answer is exit 2 with an input finding
(cannot evaluate against a non-HTTP expectation), never clean. The current implementer normalizes
`expectedCanonical` with `absolute=True`, which would raise the input path; the contract does not
spell this case out, so it stays a documented boundary rather than a matrix expectation.

## Observed vs inference

Observed (with sources):

- Contract policy, exit map, and case name (frozen `contract.json`).
- WHATWG URL scheme/valid-URL-string/special-scheme text (live official fetch, 2026-10-20).
- HTML `link` href requirement and §4.6.8.4 canonical keyword (live official fetch; `HTMLLink.md`).
- HTML `<base>` fallback for `javascript:` base URLs (`HTMLBase.md` §4.2.3) — cited only to keep
  base degradation separate from canonical scheme rejection.
- RFC 6596 silence on non-HTTP schemes (`RFC6596.md`).
- Google head-only/absolute-URL guidance (`GoogleCanonical.md`).
- CPython `urlsplit` non-validation and `urljoin` absolute-URL escape (`PythonURL.md`), plus the
  three local `urlsplit`/`urljoin` observations above.
- Matrix and implementer snapshots at 2026-10-20T21:39Z (scratch clones; timestamped, not authority).

Inference (not executed):

- That the fixture's single finding is exactly one `canonical_url_invalid` under the current
  implementer; this follows from static reading, not a run.
- That the embedded-expected variant would defeat containment/suffix comparators; the payload's
  parse shape is observed, the comparator failure is a design inference.
- That exit 2 is wrong for bad schemes (argued from the exit map and `invalid_url` precedent).
- That no 33rd matrix case is needed (the frozen matrix is fixed at 32 by contract).

Remaining unknowns: the contract does not define the `page` field's exact value, a
`detail`/message field, or the precedence among simultaneous URL violations; it also does not
define behavior when `expectedCanonical` itself is non-HTTP(S).

## Checks for L1 (run once, after integration; not run here)

1. `python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/javascript_url/manifest.json --json`
   → exit 1; stdout parses as one JSON object; `pagesChecked == 1`; exactly one finding with
   `id == "canonical_url_invalid"`; no stderr traceback.
2. `python3 .ufo/waves/round-22/matrix.py --root <lane>` → `javascript_url` PASS; summary
   `discrepancies=0` for the frozen cases that are actually executable. Then the contract's
   measurement command `python3 .ufo/waves/round-22/measure.py --root . --revision <master-tip>`
   → output with `revision`, `available`, `accepted`, `total` (=32), and `results`, where
   `javascript_url` is accepted and not a failure; `measure.py` exits nonzero on a failed matrix.
   If the fixtures are not integrated yet, point the case check at the Matrix seat's `cases.json`
   root while `measure.py` stays revision-bound.
3. Positive control `absolute_match` → exit 0, `findings: []`, `verdict: "clean"` (proves the
   fixture shell itself is not the cause of the failure).
4. `data_url` → exit 1 with the same id, confirming the shared scheme bucket; `invalid_url` →
   exit 1 with the same id, confirming URL-policy failures are not exit 2.
5. `--selftest` covers `javascript_url` and the embedded-expected variant with literal expected
   exits/ids; confirm the selftest writes only under `mkdtemp` and not into the lane.
6. Confirm manifest mode performs no network and no writes (static inspection of imports/calls;
   optional `strace -f -e trace=network,openat` during the matrix run if wanted).
7. Confirm the matrix's `expectedFindings` and the script's emitted ids are byte-identical before
   the measured run — the id string, not the exit, is the failure-prone half of this case.

## Tooling

No installs, upgrades, or package transactions. Reads used the existing `read`, `grep`, `ls`,
`cat`, `sha256sum`, and `python3` stdlib only; no repository test, matrix, or validator execution.
