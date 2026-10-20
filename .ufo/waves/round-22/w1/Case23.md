# Case23 — matrix case `wrong_host`

**Seat.** `KakeR22.Case23` (scout, leaf). Read-only seat: this report is the only write.
**Contract.** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json`, read 2026-10-20. Lane base observed at `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
**Axis / milestone.** `operability` / `offline-canonical-capability`.
**State at read time.** `scripts/canonical_audit.py`, `.ufo/waves/round-22/matrix.py`, `.ufo/waves/round-22/cases.json`, and `fixtures/` did **not** exist at this base; Implement/Matrix/Measure were still pending. No validator, matrix, fixture, or test was executed. No installs, no package transactions, no services, no git/jj writes, no lane edits.

**Case contract objects used.** `interface.policy`, `interface.outputs`, `interface.exitMap`, `interface.findingIds`, `matrixCases`.

---

## 1. Case definition

| Field | Frozen value |
|---|---|
| case | `wrong_host` |
| manifest page `url` | `https://example.test/project/a.html` |
| HTML file | `wrong_host.html` (relative to the manifest directory) |
| `expectedCanonical` | `https://example.test/project/a.html` |
| canonical `href` in HTML | `https://example.org/project/a.html` |
| expected exit | **1** (`failed policy`) |
| expected finding `id` | **`canonical_mismatch`** |
| expected finding count | exactly **1** |
| `pagesChecked` | **1** |

The fixture changes exactly one URL component: the host (`example.org` vs `example.test`). Scheme (`https`), path (`/project/a.html`), port (default 443), query (none), and fragment (none) are identical. This makes the failure attributable to the host component, not to a second policy defect.

---

## 2. Exact fixture

Recommended lane layout (Matrix owns the final layout; only the manifest-relative `file` invariant matters):

```
/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/wrong_host/manifest.json
/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/wrong_host/wrong_host.html
```

Manifest (exact JSON; pretty-printing is semantically irrelevant):

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"wrong_host.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

HTML (exact bytes recommended: UTF-8/ASCII, LF, no BOM, no trailing spaces):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>wrong host fixture</title>
<link rel="canonical" href="https://example.org/project/a.html">
</head>
<body>
<p>wrong_host</p>
</body>
</html>
```

Fixture properties, deliberately chosen to stay inside the contract's supported shape:

- explicit `<head>` … `</head>`, so the explicit-head gate is satisfiable and `missing_head` is not in play;
- exactly one `link` element in the head, `rel="canonical"` exactly (closed token list, no extra tokens), so `rel_token_list`/`rel_uppercase` are not exercised;
- `href` is present, non-empty, absolute `https`, lowercase scheme/host, default port omitted, no dot segments, no percent-encoding, no query, no fragment, no userinfo;
- no `<base>`, so resolution is the document URL and the absolute `href` is unchanged;
- no comments, `<script>`, `<template>`, duplicate attributes, or duplicate canonicals; no other element can be mistaken for a canonical signal.

**Paired clean control (recommended, not a 33rd matrix case).** The same document with only `href="https://example.test/project/a.html"` must yield exit **0** and `findings: []`. That control proves the failing fixture is not red because of head/parser/fixture malformation.

---

## 3. Expected stdout and exit

Exit **1**. The contract freezes `verdict`, `pagesChecked`, and `findings[]` with `id` and `page`; it does not freeze the literal `verdict` token or the `page` field source. A conforming shape is:

```json
{"verdict":"failed","pagesChecked":1,"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}]}
```

- `verdict`: literal is **not** frozen by the contract; `failed` is a recommendation. `cases.json` should not assert it unless the implementer pins it. [INFERENCE]
- `page`: expected to be the manifest `url`, not the filesystem name. The contract does not state this explicitly; pin the convention in `cases.json`/measure if asserted. [INFERENCE]
- The matrix's frozen assertions should be: exit `1`, exactly one finding, `id == "canonical_mismatch"` (and, if pinned, `pagesChecked == 1`).

---

## 4. Why this is the correct result (policy trace)

1. **Manifest evaluable.** `version` is 1; one page; `file` is a relative regular file under the manifest directory. No traversal and no symlink. This is not an `input_invalid` / exit-2 shape.
2. **Explicit head.** `<head>` and `</head>` are present and unambiguous. The only `link` is inside the head. Therefore: not `canonical_missing`, not `canonical_multiple`, not `canonical_outside_head`.
3. **`rel` semantics.** `rel="canonical"` is the ASCII case-insensitive token list `{canonical}`; no duplicate token, no extra token. Valid per contract policy and HTML's `rel` token rules.
4. **`href` present.** It is present and non-empty. Not `canonical_href_missing`.
5. **URL shape.** The target is a valid absolute HTTP(S) URL with a non-empty authority, `https` scheme, no username/password, no fragment, no non-default port. Not `canonical_url_invalid`, not `canonical_fragment`. (The scheme is HTTP(S), so this is not an unsupported-scheme `javascript_url`/`data_url` shape.)
6. **Resolution.** No `<base>` exists; the absolute `href` resolves to itself. Not `base_url_invalid`.
7. **Normalization.** Scheme and host are already lowercase; there is no default port to drop; there are no dot segments, percent-encodings, query, or fragment. Normalized canonical target = `https://example.org/project/a.html`.
8. **Comparison.** The contract's oracle is `expectedCanonical`, i.e. `https://example.test/project/a.html`. The normalized target differs only in the host: `example.org` vs `example.test`. The full normalized absolute URLs are unequal, so the policy comparison fails.
9. **Finding.** The closed `findingIds` list has no host-specific id. A well-formed HTTP(S) target whose only defect is differing from the expected URL is `canonical_mismatch`. It is **not** `canonical_url_invalid` (the URL is valid) and **not** `canonical_outside_head` (it is in the head).
10. **Exit.** Policy failure ⇒ exit `1`. Exit `2` is wrong because the input is fully evaluable; exit `64` is wrong because the invocation is correct.

**Expected id, restated:** `canonical_mismatch`, exit `1`, one finding, one page checked.

---

## 5. Non-overclaim: RFC 6596 permits a cross-host canonical

RFC 6596 §3 says the canonical target **MAY** be on a different hostname or domain and **MAY** use a different scheme. Therefore:

- `https://example.org/project/a.html` is not an invalid canonical under RFC 6596, and this fixture is not evidence of RFC non-conformance.
- The failure is **local policy**: the frozen manifest declares `expectedCanonical` as the required target, and the validator is specified to compare the normalized absolute URL against it exactly.
- Finding text and reports must say "canonical does not match expectedCanonical", not "cross-host canonical is invalid" or "RFC 6596 violation". This is also consistent with the contract limit: policy comparison, not search-engine canonical selection.

A corollary for the implementation: do not add a same-origin rule and do not reject cross-host targets as malformed. The only correct rejection here is the expected-URL mismatch.

**Coverage caveat.** In this fixture `url == expectedCanonical`. A validator that wrongly compared the canonical `href` to the manifest `url` instead of `expectedCanonical` would still return `canonical_mismatch`, because the href differs from both. So this case proves host inequality is rejected; it does **not** prove `expectedCanonical` is the oracle. That oracle precedence is a separate coverage question (see boundary notes).

---

## 6. Adjacent false-green attack (the one selected)

### Name: same-authority cross-scheme target (`http` canonical for an `https` expected URL)

Same manifest as the case:

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"wrong_scheme.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

Same HTML as the case, with only the `href` changed:

```html
<link rel="canonical" href="http://example.test/project/a.html">
```

**Correct result:** exit **1**, finding **`canonical_mismatch`**. Normalized target `http://example.test/project/a.html` differs from expected `https://example.test/project/a.html` in the scheme. HTTP and HTTPS are distinct special schemes with distinct default ports (80 vs 443). The contract allows both schemes but requires exact agreement with `expectedCanonical`; there is no http→https equivalence rule. Exit `2` is also incorrect: `http` is an allowed scheme, so this is an evaluable mismatch, not an unsupported shape.

**False-green mechanisms this attack catches:**

- comparison of `(netloc, path, query)` or `(hostname, path, query)` that drops `scheme`;
- an "upgrade" normalization that rewrites `http` → `https` before comparing (tempting because RFC 6596 permits a different scheme and HTTPS is the preferred transport);
- an origin/host-plus-path check that never inspects the full normalized absolute URL.

Any of these returns exit `0` with an empty `findings` array for a definite policy failure — the exact false green the case matrix is supposed to prevent. **Attack framing:** a page or compromised build step can declare the `http://` target to move the canonical onto an insecure/downgraded origin while the publisher's manifest still requires `https://`; a scheme-blind comparator reports the page clean, so the policy evasion is invisible. Because `http` is an allowed HTTP(S) scheme, the validator cannot classify this as unsupported; only the full-URL mismatch check catches it.

**Why it is adjacent.** It is the same single-component substitution in the same normalized-URL equality step: the fixture, manifest shape, expected finding id, and expected exit are identical to `wrong_host`. The only difference is which component is changed.

**Why it is distinct from this case.** The `wrong_host` fixture keeps the scheme, path, query, and port equal and changes the host. This attack keeps the host, path, query, and port equal and changes the scheme. A comparator that catches `wrong_host` by comparing hosts can still miss this attack unless it compares the full normalized URL.

**Matrix coverage.** The frozen 32 names contain no scheme-mismatch case: `scheme_relative` resolves to the document URL's scheme (the contract's manifest example is `https`), so it tests scheme inheritance, not a scheme disagreement with `expectedCanonical`; no `wrong_scheme` name exists. On the face of the contract and case names, a scheme-dropping comparator would not be caught by the frozen matrix. [INFERENCE: fixtures were not yet built at read time; this is a claim about the case names/contract, not an observed run.] Recommendation: add this as an isolated negative in `scripts/canonical_audit.py --selftest` (temp manifest + HTML), with a clean `https` control. Do **not** add it to `cases.json` as a 33rd frozen case; the 32-case matrix is frozen. If L1 wants it in the matrix, that is an explicit contract change, not a scout-side edit.

---

## 7. Boundary notes (not the selected attack; listed only to bound this fixture)

- **Port-only difference** (`https://example.test:8443/project/a.html` vs default 443) is a separate authority component. It should also be `canonical_mismatch`/exit 1, and a `hostname`-only comparator would false-green on it. The `wrong_host` fixture does not exercise it.
- **Userinfo and lookalike hosts** (`https://example.test@evil.test/project/a.html`, `https://example.test.evil.test/project/a.html`) defeat prefix/substring host matchers. They are deliberately not used as the adjacent case: the credential-bearing shape has unpinned finding-id precedence (no dedicated credentials id in `findingIds`; `canonical_url_invalid` is the likely mapping [INFERENCE]), so its expected id would be ambiguous.
- **Trailing-dot host / IDNA / punycode** equivalence requires a normalization decision the contract does not freeze. Do not improvise an expectation for those shapes in this case.

---

## 8. Sources (primary unless marked)

| Claim used | Source and exact locator | Access | Status |
|---|---|---|---|
| Policy: exactly one canonical in explicit head, resolve with first base/document URL, compare normalized absolute URL to `expectedCanonical`, preserve query, reject fragments/credentials; closed finding ids; exit map; 32 case names | `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json`, `interface.policy`, `interface.findingIds`, `interface.exitMap`, `matrixCases` | 2026-10-20, local | Frozen contract (primary for this lane) |
| `rel=canonical` names the preferred URL for the current document; keyword applies to `link` and creates a hyperlink | WHATWG HTML Standard §4.6.8.4, https://html.spec.whatwg.org/multipage/links.html#link-type-canonical — quote: "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." (the missing "the" before "URL" is in the source) | 2026-10-20 | Living standard, primary |
| Canonical `link` element is only accepted in `<head>`; absolute paths are recommended, relatives supported but discouraged; fragments not canonical; self-reference recommended | Google Search Central, "How to specify a canonical URL…", https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls — quotes: "The rel="canonical" link element is only accepted if it appears in the <head> section of the HTML"; "Use absolute paths rather than relative paths with the rel="canonical" link element."; "Even though relative paths are supported by Google, they can cause problems in the long run"; "Don't specify a URL fragment as canonical, as Google generally doesn't support URL fragments." | 2026-10-20 | Primary platform guidance; policy still contract-owned |
| Canonical target MAY be on a different hostname/domain and MAY use a different scheme | RFC 6596 §3, https://www.rfc-editor.org/rfc/rfc6596.html — bullets under "The target (canonical) IRI MAY:": "Exist on a different hostname or domain."; "Have different scheme names, such as "http" to "https" or "gopher" to "ftp"." | 2026-10-20 | Informational RFC, primary; supports non-overclaim only |
| Host parser/serializer; special schemes with default ports `http` 80 and `https` 443; credentials definition | WHATWG URL Standard §3.5 Host parsing, §3.6 Host serializing, special schemes table, https://url.spec.whatwg.org/ — quotes: "The host serializer takes a host host and then runs these steps. They return an ASCII string."; "A URL includes credentials if its username or password is not the empty string."; table rows `http` 80 / `https` 443 | 2026-10-20 | Living standard, primary |
| `urlsplit()` does not validate; `urljoin` keeps an absolute URL's host/scheme; stdlib is not a WHATWG/RFC 3986 compliance claim | In-lane peer report `.ufo/waves/round-22/w1/PythonURL.md` (cites CPython `urllib.parse` docs) | 2026-10-20, in-lane | Secondary; implementation caution only, not canonical policy |
| `HTMLParser` is a token stream, lowercases attribute names, decodes attribute entities, does not check matching tags or implicit closures | In-lane peer report `.ufo/waves/round-22/w1/PythonParser.md` (cites CPython `html.parser` docs) | 2026-10-20, in-lane | Secondary; bounds the supported fixture shape |

**Inferences explicitly marked:** the `verdict` literal and `page` field source are not frozen; the absence of a scheme-mismatch case in the frozen matrix is inferred from the 32 names and contract (fixtures not yet built); the credentials-id mapping (`canonical_url_invalid`) is inferred because no dedicated id exists.

---

## 9. Checks for L1 (after integration; not run by this seat)

1. **Case assertion.** `wrong_host` → exit `1`, exactly one finding with `id == "canonical_mismatch"`, `pagesChecked == 1`; reject any run that also emits `canonical_url_invalid`, `canonical_outside_head`, `base_url_invalid`, `input_invalid`, or `html_unsupported`.
2. **Paired control.** Failing fixture's href host `example.test` → exit `0`, `findings: []`. This isolates host as the cause.
3. **Adjacent negative in selftest.** Same-authority `http://` target → exit `1`, `canonical_mismatch`; a clean `https://` control → exit `0`. Keep this out of the frozen 32-case `cases.json`.
4. **Output pinning.** If `cases.json` asserts `verdict` or `page`, pin their literals/conventions once; otherwise assert exit + stable id only, per the Matrix prompt.
5. **No-side-effect check.** Normal invocation reads only the manifest and regular HTML files; no network, no writes, no live property, no browser/JS. The fixture uses only reserved example names and is local.
6. **Record** `python3 --version` in the measurement output; no installs or package transactions were performed by this seat.
