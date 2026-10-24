# Case05 — `scheme_relative`

Read-only scout report. Base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`; no
`scripts/canonical_audit.py` and no `cases.json` exist at that revision, so the
expectation below is derived from the frozen contract and the cited specs, not
from running an implementation. No tests were run; no repo files were edited
except this report.

## Expected result (positive control)

| Field | Value |
|---|---|
| Page URL / document URL | `https://example.test/project/a.html` |
| Canonical href (raw) | `//example.test/project/a.html` (RFC 3986 network-path reference) |
| Resolved canonical | `https://example.test/project/a.html` |
| `expectedCanonical` | `https://example.test/project/a.html` |
| Expected exit | **0** (contract exitMap: `"clean"`) |
| Expected case finding id | **`clean`** (positive sentinel, per Matrix item) |
| Emitted findings | **`[]`** |
| Expected stdout shape | `{"verdict":"clean","pagesChecked":1,"findings":[]}` |

The contract fixes only the `verdict`, `pagesChecked`, and `findings[{id,page}]`
keys, so extra keys, key order, or a more specific clean verdict token are
implementation-defined. `clean` is a case-level sentinel: this page emits no
`canonical_*` finding. If a harness requires a per-page id, it must map the
empty findings array to `clean` rather than expect a synthetic finding row.

Matrix handoff (proposal only; `cases.json` is not this seat's file):

```json
{"name":"scheme_relative","expect_exit":0,"expect_id":"clean","expect_findings":[]}
{"name":"base_scheme_downgrade","expect_exit":1,"expect_id":"canonical_mismatch","expect_findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}]}
```

## Fixture

`<fixture-dir>/manifest.json`:

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"a.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`<fixture-dir>/a.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Project A</title>
<link rel="canonical" href="//example.test/project/a.html">
</head>
<body>
<h1>Project A</h1>
</body>
</html>
```

Fixture hygiene that keeps this case orthogonal:

- No `<base>` element. The scheme must come from the manifest page URL; adding
  a base turns this into `first_base` and changes the expected result (see the
  adjacent attack below).
- Page URL must remain `https:`. A `http:` page URL would resolve the reference
  to `http://example.test/project/a.html` and rightly mismatch.
- Exactly one `<link>` whose rel token list contains `canonical`, inside an
  explicit `<head>`; no comment/script/template decoys.

## Why exit 0 / no finding

1. **Explicit head, one canonical link.** The sole `<link rel="canonical">` is
   inside `<head>`, rel is exactly the single token `canonical`, and `href` is
   present and nonempty. No `canonical_missing`, `canonical_multiple`,
   `canonical_outside_head`, or `canonical_href_missing`.
2. **Base selection.** There is no head `<base href>`, so the contract's
   "first head base href or document URL" rule makes the document URL
   `https://example.test/project/a.html` the base.
3. **The href is a relative reference, not an invalid URL.** RFC 3986 §4.2:
   "A relative reference that begins with two slash characters is termed a
   network-path reference; such references are rarely used." A validator that
   requires the raw href to start with `http://` or `https://` would false-red
   this positive control; the contract requires resolution *before* comparison.
4. **Scheme inheritance.** RFC 3986 §5.2.2 resolves a reference with an
   authority and no scheme by taking the reference's authority and path while
   assigning `T.scheme = Base.scheme`; here that is `https`. The WHATWG URL
   Standard §4.4 agrees: *no scheme state* moves to *relative state* when the
   base scheme is not `file`, and *relative state* step 2 says "Set url's scheme
   to base's scheme." A leading `//` then enters *relative slash state* and,
   for a special URL, *special authority ignore slashes state*, parsing
   `example.test` as the authority.
5. **Result.** Scheme `https` + authority `example.test` + path
   `/project/a.html`, no query, fragment, credentials, port, or dot segments.
   The normalized absolute URL is `https://example.test/project/a.html`, which
   equals `expectedCanonical`.
6. **Exit.** Policy is satisfied for the only page; exit `0`, verdict `clean`,
   empty findings.

A stdlib-only design check (`urllib.parse.urljoin` with the two bases above,
no repo code, no network, no writes) returned
`https://example.test/project/a.html` for this positive and
`http://example.test/project/a.html` for the adjacent attack below. That is a
resolution check, not an acceptance test of the unseen validator; S027 still
warns that `urlsplit()` does not validate and stdlib parsing is not an exact
WHATWG implementation.

## Adjacent false-green attack — `base_scheme_downgrade`

Distinct attack, not one of the frozen 32 cases; proposal only (no fixture or
`cases.json` edit by this seat).

Manifest page URL `https://example.test/project/a.html`,
`expectedCanonical` `https://example.test/project/a.html`, file
`base_scheme_downgrade.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<base href="http://example.test/project/">
<link rel="canonical" href="//example.test/project/a.html">
</head>
<body></body>
</html>
```

**Correct result:** the first head base is `http://example.test/project/`; the
network-path reference inherits the base's scheme `http`, giving
`http://example.test/project/a.html`. That differs from the expected `https`
URL, so the page must exit **1** with **`canonical_mismatch`** (`page` = the
manifest page URL). `http` is a valid HTTP(S) scheme and the base resolves
cleanly, so `base_url_invalid` is not the contract reading; `base_url_invalid`
belongs to malformed/unusable bases such as the `base_invalid` case.

**False-green mechanism:** an implementation that treats a scheme-relative href
as always `https`, or that resolves against the manifest document URL while
ignoring the first head base's scheme, or that normalizes `http` and `https`
into one comparison form, returns the expected URL and exits 0. The positive
`scheme_relative` case only ever exercises https inherited from the document
URL, so such a shortcut passes it. This attack distinguishes "inherit the
effective base's scheme" from "inherit the document's scheme / assume https".

Expected attack stdout shape:

```json
{"verdict":"failed","pagesChecked":1,"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}]}
```

Again, the `failed` token and extra keys follow the implementation's contract
reading; the fixed expectations are exit 1 and `canonical_mismatch`.

**Why adjacent but distinct:** both cases pivot on the same RFC 3986 §4.2 /
WHATWG relative-state rule, but `scheme_relative` has no base and must be clean,
while this attack supplies a base whose scheme changes the resolved URL and
must fail. It also enforces that scheme remains a compared URL component, which
the positive case alone cannot show.

## Sources

Already registered in the lane (quotes as recorded in
`corpus/lessons/round-22.md`; not reopened by me):

- **S020** — RFC 6596 §3,
  `https://www.rfc-editor.org/rfc/rfc6596.html`: "Specify a relative IRI (see
  [RFC3986], Section 4.2)." Relative canonical targets are permitted; the local
  policy is stricter than RFC 6596.
- **S021** — Google Search Central:
  "Even though relative paths are supported by Google, they can cause problems
  in the long run". Relative support does not make absolute form mandatory; the
  contract compares the resolved URL.
- **S023** — WHATWG HTML §4.6.8.4: "The canonical keyword indicates that URL
  given by the href attribute is the preferred URL for the current document."
- **S024** — WHATWG HTML §4.2.3: "If there are multiple base elements with href
  attributes, all but the first are ignored."
- **S027** — Python `urllib.parse`: "urlsplit() does not perform validation."
  A successful join is not a validity or WHATWG-equivalence proof.

Newly opened official documentation for this case (accessed 2026-10-20; **not
in `corpus/SOURCES.md`**, no registry edit made):

| Source | Location and exact quote |
|---|---|
| RFC 3986, https://www.rfc-editor.org/rfc/rfc3986.txt | §4.2: "A relative reference that begins with two slash characters is termed a network-path reference; such references are rarely used." §5.2.2: for a reference with authority and no scheme, "T.authority = R.authority;" and after the scheme branch, "T.scheme = Base.scheme;". |
| WHATWG URL Standard, https://url.spec.whatwg.org/ | §4.4 *relative state*: "Set url’s scheme to base’s scheme." *no scheme state*: "Otherwise, if base’s scheme is not “file”, set state to relative state and decrease pointer by 1." *relative slash state* sends special schemes to *special authority ignore slashes state*. |

Registry gap for L1, not a blocker: S020's quote already points at
[RFC3986] §4.2, but RFC 3986 itself has no SOURCES row, and the WHATWG URL
Standard has no row. If the knowledge entry needs these mechanisms sourced,
they are candidates for new rows; I made no registry edits.

## Confidence and unknowns

**Observed (this session):**

- Contract text: one canonical link in explicit head, first head base or document
  URL, resolution before comparison, exitMap 0 = clean.
- RFC 3986 §4.2/§5.2.2 and WHATWG URL §4.4 text quoted above.
- `scripts/canonical_audit.py` and `cases.json` are absent at base
  `7c61c8c`; the lane working tree carries L1's uncommitted round-22
  documentation changes, which this seat did not touch.
- `urllib.parse.urljoin` resolved the network-path reference to the expected
  `https` URL for the positive and to the `http` URL for the attack.

**Inference (not observable without the implementation):**

- The exact stdout serialization beyond the contract keys, verdict token casing,
  and validation order.
- The false-green mechanism is a plausible implementation shortcut, not an
  observed defect; no validator existed to exercise.
- Whether an implementer gates on the raw href scheme or resolves against a
  filesystem path; both would be wrong under the contract but neither was seen.

**Open gaps / handoff:**

- Matrix/L1 must decide whether `clean` is a case-level sentinel (this report's
  reading) or emitted as a finding row; the contract's findings array points to
  the former.
- If the adjacent attack is adopted, its expected id is `canonical_mismatch`
  unless L1 explicitly declares non-`https` bases unsupported, which the frozen
  contract does not do.
- RFC 3986 and the WHATWG URL Standard are unregistered source candidates for
  L1; this seat made no registry or `SOURCES.md` edit.

**Scope limits:** no validator run, no matrix run, no fixture committed, no
network beyond the two official documentation reads above, no installs, no
lane state or index writes; only this report was written.
