# Case02 — `relative_same_dir` (matrix case 2 of 32)

Seat: `KakeR22.Case02` — read-only scout. No code, no tests, no lane/jj/git writes.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`; observed `HEAD = 7c61c8cc791bde36dd5e3688bdfea2678d90146c`
(matches contract base; the tree also shows uncommitted work by other seats, untouched here).
No installs, no network beyond official documentation fetches listed below.

## 1. What the case must prove

A relative reference that resolves to the page's own URL is a **valid, clean canonical
declaration**. The case is a positive control: it forces the validator to run the full
resolve-then-compare pipeline, yet must end with zero findings. It must fail a validator that
(a) compares the raw `href` string to `expectedCanonical` (`"a.html"` != absolute URL), or
(b) cannot resolve relative references at all.

It must NOT be "passed" by a shortcut that assumes any relative reference is self-referential;
that shortcut is exactly the adjacent false green in §6.

## 2. Frozen fixture (concrete bytes)

Manifest entry (file path is relative to the manifest directory, per contract `fileResolution`):

```json
{"version": 1,
 "pages": [{
   "url": "https://example.test/project/a.html",
   "file": "fixtures/relative_same_dir/a.html",
   "expectedCanonical": "https://example.test/project/a.html"
 }]}
```

`fixtures/relative_same_dir/a.html` (UTF-8, ASCII only, explicit tags, no `<base>`, no BOM):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>relative same dir</title>
<link rel="canonical" href="a.html">
</head>
<body>
<p>relative same dir</p>
</body>
</html>
```

Committed fixture must be a regular file (not a symlink). `a.html` is reused as the *published
basename* only; it is not resolved through the filesystem.

Equivalent literals: `./a.html` and `././a.html` resolve to the same URL by RFC 3986 §5.2.4
dot-segment removal. The frozen fixture should use plain `a.html` so dot-segment behavior stays
tested by `relative_parent` rather than duplicated here; any of the three literals is still a
valid instantiation of this case with the same expected exit/id.

## 3. Resolution trace (normative mechanics)

Base URL = document URL, because there is no `<base href>` (contract: "resolve href with first
head base href or document URL").

- Reference `a.html`: no scheme, no authority, path `a.html`, no query, no fragment.
- RFC 3986 §5.2.3 merge: "return a string consisting of the reference's path component appended to
  all but the last segment of the base URI's path" → `/project/` + `a.html` = `/project/a.html`.
- RFC 3986 §5.2.4 dot-segment removal: no `.`/`..` segments; unchanged.
- Recomposition against base scheme/authority → `https://example.test/project/a.html`.
- Normalization: scheme already lowercase, host already lowercase, default port absent, path kept
  byte-for-byte (case preserved), no query, no fragment, no userinfo.
- Equality with `expectedCanonical` (same serialization) → no finding.

Corroboration from the HTML Standard §4.2.3 example (accessed 2026-10-20): with
`<base href="https://www.example.com/news/index.html">`, the spec states the link "would be a link
to" `https://www.example.com/news/archives.html` for `<a href="archives.html">`.
That is the same directory-merge behavior (last segment replaced), applied here without a base.

Fetch check performed here: `urllib.parse.urljoin("https://example.test/project/a.html","a.html")`
returns `https://example.test/project/a.html`. That is an analysis computation, not a test run of
the (not yet existing) tool.

## 4. Expected result

| field | expected |
|---|---|
| exit code | **0** (`clean`) |
| `verdict` | `"clean"` |
| `pagesChecked` | `1` |
| `findings` | `[]` |
| case-scoped finding id | **`clean`** (sentinel; must NOT appear as an object inside `findings`) |

`clean` is not in the contract's `findingIds` array; it is the mandated positive sentinel from the
Matrix item ("positive id clean"). Any `findings` entry with `id: "clean"` is contract-invalid.
Findings are objects with at least `{id, page}`; a clean page contributes none.

## 5. Why exit 0 and not 1/2/64

- **Not 1:** the resolved canonical equals `expectedCanonical`; there is no missing, conflicting,
  invalid, fragment, credential, or mismatching signal. Relative form alone is not a policy
  failure. RFC 6596 §3 lists under "The target (canonical) IRI MAY:" — "Specify a relative IRI
  (see [RFC3986], Section 4.2)." (8 words, accessed 2026-10-20). Google's current guidance says
  "Even though relative paths are supported by Google, they can cause problems in the long run"
  (GoogleCanonical report, §2) — a recommendation to prefer absolute, not a validity rule.
- **Not 2:** the input is a supported shape: valid manifest v1 object, one page, regular file,
  explicit `<head>`/`</head>`, one canonical link in head, present non-empty `href`, HTTP(S)
  target, no fragment/credentials. Nothing requires `html_unsupported` or `input_invalid`.
- **Not 64:** CLI invocation is the contract form with `--manifest <path> --json`.

Supporting normative text (all accessed 2026-10-20):
- HTML Standard §4.6.8.4: "The canonical keyword indicates that URL given by the href attribute is
  the preferred URL for the current document." (19 words)
- HTML Standard §4.2.4 (`link` element): "If the href attribute is present, then its value must be
  a valid non-empty URL potentially surrounded by spaces." (19 words) — a relative reference qualifies;
  only absent/empty is excluded (that is `href_absent`/`href_empty`, not this case).
- HTML Standard §4.2.3: "If there are multiple base elements with href attributes, all but the
  first are ignored." (15 words) — irrelevant here (no base), but the same resolver step must not
  accidentally reach for a base that is not in head.
- HTML Standard §2.4.3: document base URL is "the frozen base URL of the first such base element
  in tree order", else the fallback base URL (the document URL).

## 6. Adjacent false-green attack (distinct from this case)

**Attack name: path-case collapse.** A comparator that lowercases (or casefolds) the whole URL, or
compares `urlsplit(...).path` case-insensitively, reports `clean` for a canonical that points to a
different, case-sensitive resource. `relative_same_dir` cannot catch it, because its two strings
already match in case.

Fixture (manifest `expectedCanonical` and page `url` deliberately mixed case):

```json
{"version": 1,
 "pages": [{
   "url": "https://example.test/project/A.html",
   "file": "fixtures/relative_case_trap/A.html",
   "expectedCanonical": "https://example.test/project/A.html"
 }]}
```

HTML file identical to §2 except `<title>case trap</title>` and the same
`<link rel="canonical" href="a.html">`.

Correct behavior: merge gives `/project/a.html` (the href is the whole last segment; base case is
irrelevant to the merge), serialized as `https://example.test/project/a.html`, which is **not**
equal to `https://example.test/project/A.html`: HTTP(S) paths are case-sensitive. Expected
`canonical_mismatch`, exit **1**.

False green: a validator that normalizes with `url.lower()` before equality sees
`https://example.test/project/a.html` on both sides and emits exit 0 / no findings. The publisher
then ships a page whose declared canonical is an alias or 404 while the preflight says clean.
The fix is narrow: lowercase only scheme and host (and, if pinned, percent-triplet hex); keep path
and query case-sensitive. RFC 3986 §6.2.2.1: "the scheme and host are case-insensitive ... The
other generic syntax components are assumed to be case-sensitive unless specifically defined
otherwise by the scheme" (accessed 2026-10-20).

Why this stays distinct from the frozen matrix: it is not any of the 32 names, and
`relative_same_dir` passes exact-case equality, so it cannot exercise case handling. Coverage note
for the Matrix seat: keep `wrong_path` a **non-case** difference (e.g. `other.html`) so it does not
silently absorb this attack; otherwise the case02 falsifier must move to the percent variant below.

Related normalization ambiguity — do NOT freeze without a policy decision: `href="%61.html"` resolves
to `/project/%61.html`, not `/project/a.html`. WHATWG URL parsing preserves the percent-encoded
octet in the serialized path, but RFC 3986 §6.2.2.2 says unreserved percent-encoded octets "should
be normalized by decoding". Either rule is defensible; the tool must pick one and apply it to both
sides. It is therefore unsuitable as a frozen false-green fixture until `scripts/canonical_audit.py`
declares its normalization policy (contract says "WHATWG-like", which implies preserve, i.e.
`canonical_mismatch` / exit 1). [INFERENCE: "WHATWG-like" != a full URL Standard implementation;
the Implement seat must state the chosen rule explicitly.]

## 7. Implementation constraints this case imposes

1. Resolve only a **present, non-empty** `href`. Absent → `canonical_href_missing`; empty → the
   same family, never "resolves to document URL". Empty resolution is the cheap false green that
   would let `href_absent`/`href_empty` pass.
2. Base selection: first `base[href]` inside the explicit head; otherwise the manifest `url`.
   Never the manifest file path, manifest directory, or filesystem location.
3. Use RFC 3986 §5.2 merge/remove-dot-segments semantics (`urljoin` is RFC 3986). Document any
   deliberate non-WHATWG divergences (backslashes, tabs/newlines, IDNA); none are exercised here.
4. Compare normalized **serialized strings**; scheme/host ASCII-lowercase only, default port
   omitted, path/query byte-preserved, fragment/credentials already rejected.
5. Emit `findings: []`, `verdict: "clean"`, `pagesChecked: 1`, exit 0. Keep stdout a single valid
   JSON object.

## 8. Limits of this analysis

- No code exists yet (`scripts/canonical_audit.py` absent at base), so no behavior is claimed; this
  is a contract-derived specification, not an execution result.
- The exact token for `verdict` on success is not enumerated in the contract; `"clean"` is the only
  value consistent with `exitMap` 0 = clean and the Matrix "positive id clean". Implement/Matrix
  must use one token consistently.
- `urljoin` was computed, not the tool; no `measure.py`/`matrix.py` run (forbidden for this seat).
- Dynamic freeze semantics (base inserted/changed after parse) are out of scope; contract limits to
  serialized static HTML.

## 9. Installs

None. No package transactions, services, or environment changes were made.

## Remaining unknowns

- Whether Matrix's `wrong_path` fixture uses a case-only difference (decides whether §6 is still an
  uncovered attack or already covered; recommendation above).
- The literal `verdict` value Implement chooses for exit 0.
