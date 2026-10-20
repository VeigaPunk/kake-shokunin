# Case04 — `root_relative` (matrix case 4 of 32)

Seat: `KakeR22.Case04` — read-only scout. No code, no tests, no matrix/validator/selftest run,
no git/jj/lane writes beyond this report. Lane observed at
`git rev-parse HEAD = 7c61c8cc791bde36dd5e3688bdfea2678d90146c` (matches the frozen contract base).
At observation time `scripts/` held only the three `.mjs` files and `.ufo/waves/round-22/cases.json`
did not exist, so everything here is a contract-derived specification, not a claim about
implementation behavior.

Axis: operability · milestone: offline-canonical-capability · claim C1.

Target of the case: a **root-relative (absolute-path) reference** must resolve to an absolute
HTTP(S) URL by taking **scheme, host and port from the base** and **replacing the whole path** with
the reference's path. It must end with zero findings.

## 1. Frozen fixture (concrete bytes)

Manifest entry (`file` is relative to the manifest directory, per contract `fileResolution`):

```json
{"version": 1, "pages": [{
  "url": "https://example.test/project/sub/a.html",
  "file": "a.html",
  "expectedCanonical": "https://example.test/project/a.html"
}]}
```

Recommended layout: `fixtures/root_relative/manifest.json` + sibling
`fixtures/root_relative/a.html` (UTF-8, ASCII only, explicit tags, no `<base>`, no BOM, regular
file — never a symlink).

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>root relative</title>
<link rel="canonical" href="/project/a.html">
</head>
<body>
<p>root-relative canonical</p>
</body>
</html>
```

Deliberate fixture properties (each removes a confound, like the sibling `Case02` fixture):

- **The file is flat on disk (`a.html`), while the URL path is `/project/sub/a.html`.** The document
  URL is supplied by the manifest, not derived from the filesystem. A validator that builds a URL
  from the fixture path cannot pass.
- **`expectedCanonical` differs from the page URL** (`/project/a.html` vs `/project/sub/a.html`).
  The case therefore forces real href resolution: raw-string comparison, "canonical equals page
  URL", and directory-merge shortcuts all go red, as they should.
- **No `<base>`.** Resolution base is the document URL. Base precedence has its own cases
  (`first_base`, `second_base_ignored`, `base_invalid`); folding a base in here would blur the
  reference-form axis.
- **Single rel token `canonical`, lowercase element and attribute names, no query, no fragment,
  no credentials, one explicit `<head>`, one link.** Those each have their own matrix case.
- **Target `/project/a.html` is one level above the page's directory**, so a resolver that merges
  "all but the last base segment" (the relative-path rule) yields `/project/sub/project/a.html`,
  which is not the expected URL.

Self-referential variant (acceptable but weaker): page `url` =
`expectedCanonical` = `https://example.test/project/a.html`, href `/project/a.html`. It is clean for
the same reason, but it can be satisfied without performing root-relative resolution at all
(compare page URL to expected), so prefer the non-self fixture above. If Matrix freezes the
self-referential form for the `absolute_match`/`relative_same_dir`/`scheme_relative` family, keep
those cases' `url` equal to `expectedCanonical` and note that this case's target differs; the
invariant that matters is §2's resolution trace and §3's verdict.

## 2. Resolution trace (normative mechanics)

Base = document URL `https://example.test/project/sub/a.html`, because no `<base href>` is present
(contract: "resolve href with first head base href or document URL").

Reference `href="/project/a.html"`: no scheme, no authority, path `/project/a.html`, no query, no
fragment. It is an **absolute-path reference** / **path-absolute URL**:

- RFC 3986 §4.2: "A relative reference that begins with a single slash character is termed an
  absolute-path reference."
- WHATWG URL Standard §4.3: "A path-absolute-URL string must be U+002F (/), followed by zero or
  more URL-path-segment strings, separated from each other by U+002F (/)."

WHATWG basic URL parser walk (this is the step that distinguishes `root_relative` from
`relative_same_dir` and from `scheme_relative`):

1. No-scheme state: the input does not begin with an ASCII alpha; base's scheme is not `file`, so
   the parser enters *relative state*.
2. *Relative state*, step 3: "If c is U+002F (/), then set state to relative slash state." The
   leading `/` is consumed; the pointer is now on `p`.
3. *Relative slash state*: c is `p`, not `/` or `\`, so the `//`-authority branch is not taken.
   Branch 3 applies: it copies base's username, password, **host** and **port**, sets state to
   *path state*, and rewinds the pointer. Critically, it does **not** copy base's path.
4. *Path state* parses the remaining input into path segments `project`, `a.html`; query is null,
   fragment is null.
5. Result URL record: scheme `https`, host `example.test`, port null, path `/project/a.html`,
   query null, fragment null → serialized `https://example.test/project/a.html`.

RFC 3986 §5.2.2 gives the equivalent branch: `if (R.path starts-with "/") then T.path =
remove_dot_segments(R.path)` (no dot segments here); then `T.authority = Base.authority`,
`T.scheme = Base.scheme`, `T.query = R.query` (undefined), `T.fragment = R.fragment` (undefined).
§5.2.3's merge routine is not reached: "merge" is only the else-branch for references whose path
does not start with `/`.

Normalization is identity on this fixture: scheme and host are already lowercase, no default port,
no dot segments, no percent-encoding, no query, no fragment, no userinfo. The serialized result
equals `expectedCanonical` byte for byte.

Observed corroboration (analysis computation only, not a validator run): Python 3.14.8
`urllib.parse.urljoin("https://example.test/project/sub/a.html", "/project/a.html")` returns
`https://example.test/project/a.html`; `html.parser.HTMLParser` reports
`('link', [('rel', 'canonical'), ('href', '/project/a.html')])` for the HTML above.

## 3. Expected result

| field | expected |
|---|---|
| exit code | **0** (`clean`) |
| `verdict` | `"clean"` |
| `pagesChecked` | 1 |
| `findings` | `[]` (empty array) |
| case-scoped finding id | **`clean`** sentinel only; must NOT appear inside `findings` |

`clean` is not in the contract's `findingIds` array; it is the positive sentinel named by the
Matrix item ("positive id clean"), consistent with sibling `Case02`/`Case10`/`Case22`. The literal
JSON value `"clean"` for `verdict` is `[INFERENCE]` from the frozen `exitMap` word "clean"; the exit
code and empty `findings` are contract-derived. Whatever token Implement freezes, Matrix must use
the same token.

Why not the other exits:

- **Not 1:** exactly one canonical link is in the explicit head; `href` is present and non-empty; it
  resolves to a valid HTTP(S) absolute URL; no fragment, no credentials, no query defect; the
  normalized result equals `expectedCanonical`. Relative form is not a failure: RFC 6596 §3 lists
  under "The target (canonical) IRI MAY:" — "Specify a relative IRI (see [RFC3986], Section 4.2).";
  Google says "Even though relative paths are supported by Google, they can cause problems in the
  long run" and recommends absolute URLs — a recommendation, not a validity rule. Encoding Google's
  preference as a failure would make this case a false red.
- **Not 2:** the shape is supported: manifest v1 object, one page, regular readable file, explicit
  `<head>`/`</head>`, one parsed `link`, valid URL. Nothing needs `input_invalid` or
  `html_unsupported`.
- **Not 64:** Matrix invokes the contract CLI form (`--manifest <path> --json`), so the usage exit
  is not in play.

The relevant contract rules: one canonical link in explicit head, `rel` ASCII case-insensitive
token list, resolve with first head base or document URL, WHATWG-like HTTP(S) normalized absolute
URL compared to `expectedCanonical`, preserve query, reject fragments and credentials.

## 4. What this case catches (false reds)

A validator that fails this case is wrong; these are the concrete wrong implementations:

1. **Raw-string comparison** of `href` (`/project/a.html`) against `expectedCanonical`
   (`https://example.test/...`).
2. **Rejecting relative canonicals as invalid** because Google recommends absolute paths (or
   because `rel=canonical` "should" be absolute). RFC 6596 and Google both support relative.
3. **Filesystem-style merge** — `os.path.join(dirname(url_path), href)` or concatenating the base
   directory and the href. For this fixture that yields `/project/sub/project/a.html` (or a
   filesystem path), neither of which is the expected URL.
4. **Resolving against the fixture file path / manifest directory** instead of the document URL.
   The flat `a.html` fixture makes any such derivation visible.
5. **Requiring the canonical to equal the page URL** (self-reference only). Here the canonical
   points one level up; that is a legal canonical declaration (RFC 6596: the target may be
   self-referential, but need not be; it may even exist on a different hostname or domain).
6. **Prefix/suffix or startswith checks** on the URL string instead of URL equality.
7. **Scraping raw source with a regex** instead of the parsed attribute stream: `html.parser`
   lowercases tag/attribute names and decodes attribute values, so a raw scan for `rel="canonical"`
   or exact attribute ordering is a different (and wrong) parser.

## 5. Adjacent false-green attack (distinct from this case)

**Name: `foreign_base_authority`** — a valid `<base href>` on a foreign origin plus a root-relative
canonical. The leading slash resets only the **path**; scheme, host and port still come from the
base. A validator that resolves root-relative hrefs against the document URL "because the leading
slash already starts at the root" reports clean, but the declared canonical is on a different
origin than `expectedCanonical` and the page must fail.

Concrete attack fixture (own manifest entry; same page URL/expected as the positive case):

```json
{"version": 1, "pages": [{
  "url": "https://example.test/project/sub/a.html",
  "file": "a.html",
  "expectedCanonical": "https://example.test/project/a.html"
}]}
```

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<base href="https://evil.test/">
<link rel="canonical" href="/project/a.html">
</head>
<body><p>foreign base</p></body>
</html>
```

Expected result: exit **1**, finding id **`canonical_mismatch`**, `pagesChecked: 1`, `findings:
[{"id": "canonical_mismatch", "page": "https://example.test/project/sub/a.html"}]`. The page field
is the manifest page URL `[INFERENCE]` from the contract's "id and page" shape; sibling
`Case22` records the same convention.

Why the correct resolved URL is `https://evil.test/project/a.html`:

- HTML §2.4.3: the document base URL is "the frozen base URL of the first such base element in tree
  order" when a descendant `<base href>` exists; otherwise the fallback base URL (the document URL).
- HTML §4.2.3: a single `<base href="https://evil.test/">` is conforming (valid URL, in head, before
  URL-taking elements); a cross-origin base is not restricted. `urlRecord` is a valid https URL and
  is neither `data:` nor `javascript:`, so the frozen base URL is set to it.
- URL Standard *relative state* → *relative slash state* → branch 3 copies `base`'s host and port
  (`evil.test`, null) and starts a fresh path; the path becomes `/project/a.html`. Result:
  `https://evil.test/project/a.html`.
- RFC 3986 §5.2.2: `T.authority = Base.authority` and `T.scheme = Base.scheme`, with
  `T.path = remove_dot_segments(R.path)`.

Why a plausible validator is falsely green: it computes/uses the base only for **path-relative**
references (where the base directory matters) and, for an **absolute-path** reference, resolves
against the document URL (or replaces only the path on the document origin). Both write
`https://example.test/project/a.html`, compare equal to `expectedCanonical`, and emit exit 0 with
no findings. The bug is a single wrong choice of record; the path logic is already correct.

Why this is distinct from `root_relative`: the positive case has no base and expects exit 0; the
attack has one valid foreign base and expects exit 1/`canonical_mismatch`. A validator can pass
`root_relative` while failing this attack, which is exactly the coverage gap it adds.

Why this is distinct from the frozen base cases:

- `first_base` / `second_base_ignored` test **which** base wins (precedence). Here there is exactly
  one base; the failure is using the wrong record for authority.
- `base_invalid` tests an unusable/malformed base. Here the base is valid.
- Do **not** freeze this attack as `base_url_invalid`. HTML's frozen-base algorithm falls back to
  the document URL only for parse failure, `data:`/`javascript:` schemes, or a CSP
  `Is base allowed for Document?` block. A cross-origin https base is valid and must be honored;
  CSP is not evaluable from offline HTML bytes and the contract has no CSP input, so it must not be
  modeled. `[INFERENCE]` on the CSP boundary; the fallback conditions are spec text.
- RFC 6596 §3 also lists that the target (canonical) IRI MAY "Exist on a different hostname or
  domain", so the validator must not treat cross-origin canonicals as inherently invalid — the
  finding here is a mismatch against `expectedCanonical`, not a cross-origin rule.

Same-host, different-port variant (`<base href="https://example.test:8443/">`, expected canonical
without a port) is equally green-making for the same bug and is a useful second probe; expected id
is again `canonical_mismatch` because the default-port rule does not erase an explicit 8443.

A nearby but already-claimed variant is **not** the named attack here: `href="/project/a.html#"`
(empty fragment) is a real false green — a fragment is non-null and serializes with `#`, while
`urllib.parse.urlsplit(...).fragment` is `''` and `urlunsplit` drops it — but sibling `Case22`
already owns the fragment axis (`fragment_url` + empty-fragment), and it does not test base or
authority selection. Keep the two attacks separate.

Coverage note: sibling `Case06` confirmed by message that its `first_base` fixture is same-origin
(`<base href="https://example.test/project/">`, document
`https://example.test/docs/guide/page.html`, href `a.html`) and that its adjacent attack is
template-scope, so the foreign-authority falsifier above stays unclaimed by the frozen matrix.

## 6. Stdlib boundaries this case touches

The contract requires stdlib Python and asks that `HTMLParser` limitations be explicit.

`html.parser.HTMLParser`:

- Reports tags as they are read; **it builds no tree**. "Explicit head" scope must be tracked
  manually (`<head>` … `</head>`, and `<body>`/end-of-head boundary); the case's link is a plain
  child of the explicit head, so no implied-tag handling is needed here.
- Lowercases element and attribute names and decodes character references in attribute values
  (observed: `('link', [('rel', 'canonical'), ('href', '/project/a.html')])`). Details in sibling
  `PythonParser.md`/`Case10.md`.
- Does **not** resolve URLs, apply `<base>`, or enforce head-only placement; those are the
  validator's own logic. It also reports markup inside `<template>` as ordinary start tags
  (`HTMLTemplate.md`), which is why template scope must be tracked separately (not this case).
- Self-closing `<link … />` arrives via `handle_startendtag`, whose default implementation calls
  `handle_starttag`; do not treat the synthesized end event as leaving the head.

`urllib.parse`:

- `urljoin` is RFC 3986-based, and the module docs say it "has been designed to match the internet
  RFC on Relative Uniform Resource Locators" while the security section says the functions
  "incorporate some aspects of both, but cannot be claimed compliant with either" (WHATWG/RFC).
  For `root_relative`, RFC 3986 and the URL Standard agree, so `urljoin` is enough for this one
  case — **passing this case does not prove WHATWG behavior** for backslashes, tabs/newlines,
  encoded delimiters, IDNA and similar edges. Document the accepted subset and any deliberate
  divergence.
- `urlsplit()` "does not perform validation" (docs); the validator must implement the scheme
  allowlist, host presence, credentials rejection and port checks explicitly.
- Compare normalized serialized components, not a `geturl()` round trip; `urlsplit`/`urlunsplit`
  silently drop empty components (relevant to the `#` attack owned by `Case22`).

## 7. Sources (official documentation; fetched 2026-10-20 UTC)

| ID | Source and locator | Exact text used | Use |
|---|---|---|---|
| S1 | WHATWG URL Standard §4.3 URL strings — https://url.spec.whatwg.org/#path-absolute-url-string | "A path-absolute-URL string must be U+002F (/), followed by zero or more URL-path-segment strings, separated from each other by U+002F (/)." | Classifies `/project/a.html` as an absolute-path reference |
| S2 | WHATWG URL Standard §4.4 relative state — https://url.spec.whatwg.org/#relative-state | "If c is U+002F (/), then set state to relative slash state." | Leading `/` branches to relative slash, not path-relative merging |
| S3 | Same, relative slash state — https://url.spec.whatwg.org/#relative-slash-state | "Otherwise, set url's username to base's username … url's host to base's host, url's port to base's port, state to path state" | Base authority is inherited; base path is not copied |
| S4 | WHATWG URL Standard §4.1 URL representation — https://url.spec.whatwg.org/ (section 4.1) | "A URL's fragment is either null or an ASCII string … It is initially null." | Fragment null/empty distinction (secondary note) |
| S5 | WHATWG URL Standard §4.5 URL serializing — https://url.spec.whatwg.org/#concept-url-serializer | "If exclude fragment is false and url's fragment is non-null, then append U+0023 (#), followed by url's fragment, to output." | Empty-fragment note (Case22 axis) |
| S6 | WHATWG HTML Standard §2.4.3 Document base URLs — https://html.spec.whatwg.org/multipage/urls-and-fetching.html#document-base-url | "return the frozen base URL of the first such base element in tree order"; fallback base URL is the document's URL | Base selection when a base exists; document URL otherwise |
| S7 | WHATWG HTML Standard §4.2.3 The `base` element — https://html.spec.whatwg.org/multipage/semantics.html#the-base-element | "If there are multiple base elements with href attributes, all but the first are ignored." / "must contain a valid URL potentially surrounded by spaces" / fallback on parse failure, `data:`/`javascript:`, CSP block | Foreign-base validity and fallback boundary |
| S8 | RFC 3986 §4.2 — https://www.rfc-editor.org/rfc/rfc3986#section-4.2 | "A relative reference that begins with a single slash character is termed an absolute-path reference." | Terminology and reference class |
| S9 | RFC 3986 §5.2.2 — https://www.rfc-editor.org/rfc/rfc3986#section-5.2.2 | "if (R.path starts-with "/") then T.path = remove_dot_segments(R.path)" plus `T.authority = Base.authority`, `T.scheme = Base.scheme` | Independent normative resolution trace |
| S10 | RFC 3986 §5.2.3 — https://www.rfc-editor.org/rfc/rfc3986#section-5.2.3 | "return a string consisting of the reference's path component appended to all but the last segment of the base URI's path" | Merge applies only to non-`/`-leading paths |
| S11 | RFC 6596 §3 — https://www.rfc-editor.org/rfc/rfc6596#section-3 | "Specify a relative IRI (see [RFC3986], Section 4.2)." / "Exist on a different hostname or domain." / "Specify only one canonical link relation for a resource." | Relative canonicals are permitted; cross-origin targets are permitted; one-link policy |
| S12 | Google Search Central, "How to specify a canonical URL with rel="canonical" and other methods" — https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | "Use absolute paths rather than relative paths with the rel="canonical" link element." / "Even though relative paths are supported by Google, they can cause problems in the long run" / "The rel="canonical" link element is only accepted if it appears in the <head> section of the HTML" / "Don't specify a URL fragment as canonical" | Absolute is a recommendation, not a validity rule; head-only; fragment ban |
| S13 | Python `urllib.parse` docs — https://docs.python.org/3/library/urllib.parse.html (page served as 3.15.0 at fetch; local interpreter 3.14.8) | "The module has been designed to match the internet RFC on Relative Uniform Resource Locators." / "These functions incorporate some aspects of both, but cannot be claimed compliant with either." / "urlsplit() does not perform validation." | Stdlib profile limits; no full WHATWG claim |
| S14 | Python `html.parser` docs — https://docs.python.org/3/library/html.parser.html | "The name will be translated to lower case" (attribute names; values decoded) | Parser behavior relied on by the implementation |

Sibling wave-1 reports that independently reach the same conclusions (not load-bearing, cited for
consistency): `Case02.md` (resolve-then-compare positive discipline), `HTMLBase.md` (first-base and
frozen-base semantics), `PythonURL.md` (stdlib non-compliance and escape warnings), `GoogleCanonical.md`
(relative supported, absolute recommended), `Case22.md` (fragment/empty-fragment).

## 8. Remaining unknowns and explicit inferences

- **Verdict token literal**: the contract fixes exit `0` = "clean" in `exitMap` only; the JSON
  `verdict` string `"clean"` is `[INFERENCE]` from that wording. Exit code, `pagesChecked: 1`, and
  empty `findings` are contract-derived.
- **Fixture layout/literal**: the bytes and paths above are recommendations; Matrix may place the
  fixture elsewhere provided (a) the document URL comes from the manifest, not the file path;
  (b) `href` is `/project/a.html` (or another root-relative path) and resolves to
  `expectedCanonical`; (c) `expectedCanonical` differs from the page URL to force resolution.
- **Self-referential alternative** accepted if the matrix family convention requires it; the verdict
  stays exit 0 / no finding.
- **Attack id mapping**: `canonical_mismatch` is the only contract id that fits a valid foreign base
  yielding a URL different from `expectedCanonical`. If L1 instead wants foreign bases rejected as
  unsupported, that is a new policy axis (not in the contract's ids) and must be declared; it would
  also contradict HTML's valid-base model and RFC 6596's cross-origin allowance.
- **CSP**: `base-uri` blocking is not evaluable from offline bytes and is not an input in the
  contract; the validator must state it does not model CSP.
- **Not verified**: `scripts/canonical_audit.py`, `matrix.py`, `cases.json`, `measure.py` were absent
  at observation time; no behavior is claimed. Two stdlib probes (urljoin, HTMLParser) were
  computations for this report, not tests of the deliverable.

## 9. Checks for L1 (not run here)

1. Freeze `root_relative` as exit **0**, no finding id (or the matrix's `clean` sentinel), with a
   root-relative `href`, no `<base>`, and `expectedCanonical` equal to the resolved absolute URL.
2. Reject any expectation mapping `root_relative` to `canonical_missing`/`canonical_url_invalid`/
   `canonical_mismatch` — those encode a broken resolver or a "relative is invalid" policy.
3. Confirm the fixture's `file` is regular and flat/independent of the URL path, so file-path
   URL derivation is falsified.
4. Add the `foreign_base_authority` falsifier (foreign `<base href>` + `/`-leading href) as a
   post-matrix probe: expected exit 1 / `canonical_mismatch`. If the integrated validator returns
   exit 0 here, the root-relative branch is resolving against the document URL instead of the
   document base URL.
5. Confirm the implementation documents its RFC 3986 vs WHATWG subset and does not infer WHATWG
   conformance from `urljoin` passing this case; confirm `urlsplit` is not treated as a validator.

## 10. Changes and tooling

- Files written: this report only, `.ufo/waves/round-22/w1/Case04.md`.
- Lane/worktree: no source, script, fixture, matrix, registry, knowledge or lesson edits; no git/jj
  writes; no lane state changes.
- Tools installed or updated: **none** (no package transactions, no services, no credentials).
- Coordination sent (non-blocking): `KakeR22.Matrix` (fixture invariant and expected verdict) and
  `KakeR22.Case06` (keep `first_base` same-origin so the foreign-authority falsifier stays
  uncovered; Case06 acked and confirmed its own adjacent attack is template-scope).
