# Case09 — `rel_uppercase` (positive control: the `rel` keyword is ASCII case-insensitive)

Seat: `KakeR22.Case09` (scout, read-only). Lane `kake-shokunin`, base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`. Contract read from `.ufo/waves/round-22/contract.json` (round 22, C1, `matrixCases[8]`). Scope: analysis only. No code, fixtures, tests, builds or installs were run; no lane or registry files were edited, and this report is the only file written. No git/jj writes.

## Result

| Field | Frozen expectation |
|---|---|
| Case kind | Positive control (clean page) |
| Manifest `url` | `https://example.test/project/a.html` |
| `expectedCanonical` | `https://example.test/project/a.html` |
| Expected exit | `0` |
| Expected finding id | none emitted — `findings == []` (`cases.json` may use its frozen `clean` sentinel; the contract's `findingIds` list has no "ok" member) |
| `pagesChecked` | `1` |

The expected value is contract- and platform-derived, not an observation of an implementation. The literal JSON `verdict` token (`"clean"` below) is `[INFERENCE]`: the contract maps exit `0` to the label "clean" in `exitMap` but does not enumerate the string vocabulary.

## Concrete fixture (recommendation for the Matrix executor; not created by this seat)

Layout consistent with the observed per-case manifest convention (`fixtures/<case>/manifest.json`, HTML co-located so the manifest `file` field is a bare name):

- `.ufo/waves/round-22/fixtures/rel_uppercase/manifest.json`
- `.ufo/waves/round-22/fixtures/rel_uppercase/rel_uppercase.html`

`rel_uppercase.html` — UTF-8, no BOM, LF line endings, one trailing newline, ASCII-only:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>rel keyword uppercase</title>
<link rel="CANONICAL" href="https://example.test/project/a.html">
</head>
<body>
<p>rel keyword uppercase</p>
</body>
</html>
```

`manifest.json`:

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "rel_uppercase.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

Design constraints that keep this case single-axis:

- Exactly one explicit `<head>`, one `link`, one `rel` token. The only perturbed variable is the **value case of the keyword** (`CANONICAL`).
- No `<base>`, no body link, no comment/script/template decoy. The `href` is absolute and already the normalized form of `expectedCanonical`: scheme `https`, host `example.test`, default port omitted, path `/project/a.html`, no query, no fragment, no credentials. Resolution and normalization are identity operations, so a failure here can only come from the `rel` axis.
- The element name and attribute names are lowercase. Attribute-name case is `attr_uppercase`; `rel` token-list grammar is `rel_token_list`. Do not fold those axes into this fixture.

## Expected observation

- Exit `0`.
- One parseable JSON object on stdout, e.g. `{"verdict": "clean", "pagesChecked": 1, "findings": []}` (verdict literal `[INFERENCE]`; exit and empty findings are contract-derived).
- No `canonical_*` finding. Do not synthesize a "clean" finding inside `findings`.

## Why this must be clean

1. **`rel` is a set of space-separated tokens.** HTML Standard §4.6.8: the element's `rel` attribute "must be split on ASCII whitespace. The resulting tokens are the keywords for the link types that apply to that element." Here the sole token is `CANONICAL`.
2. **Keyword matching is ASCII case-insensitive.** HTML Standard §4.6.8: "Keywords are always ASCII case-insensitive, and must be compared as such." Infra §4 defines the predicate precisely: "A string A is an ASCII case-insensitive match for a string B, if the ASCII lowercase of A is the ASCII lowercase of B." So `CANONICAL` and `canonical` are the same keyword.
3. **RFC 8288 agrees for registered relation types.** §2.1: "Registered relation type names MUST conform to the `reg-rel-type` rule (see Section 3.3) and MUST be compared character by character in a case-insensitive fashion."
4. **The keyword is `canonical` on a `link` in the head.** HTML Standard §4.6.8.4: "The `canonical` keyword may be used with `link` element. … The `canonical` keyword indicates that URL given by the `href` attribute is the preferred URL for the current document." The element is inside the explicit `<head>`, and it is the only canonical link on the page, satisfying the contract's "exactly one canonical link in explicit head per page".
5. **The declared URL matches policy.** The `href` is present, absolute, HTTP(S), with no fragment and no credentials. The normalized URL equals `expectedCanonical` exactly (case included), so neither `canonical_mismatch` nor `canonical_fragment`/`canonical_url_invalid` applies.
6. **The parser preserves the value case; the validator must fold it.** CPython `html/parser.py` lowercases attribute *names* but not values: line 484 appends `(attrname.lower(), attrvalue)`. A local probe (Python 3.14.8) of `<link REL="CANONICAL" HREF="…">` returned `('rel', 'CANONICAL')` and `('href', '…')`. A validator that assumes `HTMLParser` has already lowercased the `rel` value will emit `canonical_missing` — a false red. The token comparison, not the parser, owns the ASCII case folding.

Boundary: this is publisher-policy comparison, not assertion of Google's selected canonical. RFC 6596 §3 permits applications to ignore improper canonical designations and this capability does not claim search-engine selection. (Sibling reports `RFC6596.md`, `GoogleCanonical.md` reach the same scope split.)

## Adjacent false-green attack (one): `href_path_case`

Chosen deliberately outside the frozen 32-case list and distinct from the rel-token-boundary and non-ASCII-whitespace probes already identified in sibling report `Case08.md`; this one tests the *scope* of the case-insensitivity rule that makes `rel_uppercase` pass. Do **not** add it to `cases.json` this round: the matrix counter is frozen at 32. Run it as an adversarial probe (temporary manifest, or a `--selftest` addition only if L1 explicitly widens scope).

### Attack fixture

Same manifest `url` and `expectedCanonical`; HTML differs only in the `href` path letter case (and stays with the uppercase `rel` tied to this case):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>href path case</title>
<link rel="CANONICAL" href="https://example.test/Project/A.html">
</head>
<body>
<p>declared canonical differs only by path letter case</p>
</body>
</html>
```

| Outcome | Exit | Findings |
|---|---|---|
| Contract-correct | `1` | `[{"id": "canonical_mismatch", "page": "https://example.test/project/a.html"}]` |
| False green | `0` | `[]` |

### Why the false green happens

A validator that normalizes by lowercasing the **whole serialized URL** (or compares `href.lower() == expectedCanonical.lower()`) maps `/Project/A.html` to `/project/a.html` and reports clean. The bug is plausible precisely because the implementer has just added case folding to satisfy `rel_uppercase`: one shared "make case-insensitive" helper applied to both the keyword and the URL. URL normalization libraries do not prevent it — a post-hoc `.lower()` on the serialized string does exactly this damage.

### Why exit 1 / `canonical_mismatch` is correct

- RFC 3986 §6.2.2.1: "When a URI uses components of the generic syntax, the component syntax equivalence rules always apply; namely, that the scheme and host are case-insensitive and therefore should be normalized to lowercase. … The other generic syntax components are assumed to be case-sensitive unless specifically defined otherwise by the scheme." The HTTP(S) scheme does not define its path as case-insensitive: RFC 9110 §4.2.3 states that for `http`/`https`, "The scheme and host are case-insensitive and normally provided in lowercase; all other components are compared in a case-sensitive manner." A WHATWG URL parse lowercases scheme and host (host through the domain parser) but preserves path case in the path state and serializer.
- The contract compares the "WHATWG-like HTTP(S) normalized absolute URL" to `expectedCanonical`. After normalization the declared URL is still `https://example.test/Project/A.html`, which is not equal to `https://example.test/project/a.html`. Policy violation: exit `1`, `canonical_mismatch`, page = the manifest `url`.
- It is not `canonical_url_invalid`: the URL is a syntactically valid HTTP(S) URL with no credentials or fragment. It is not `canonical_missing`: a valid canonical link exists. It is not `wrong_path` duplication: `wrong_path` changes path characters; this changes only case, which is invisible to whole-URL lowercasing but visible to component-wise comparison.

### Why it is distinct and adjacent

- From `rel_uppercase`: that case has a matching path and must be clean; this one has a case-only path difference and must fail. Only the URL comparison changes.
- From `wrong_path`/`wrong_host`/`wrong_query`: those change visible characters, so even a whole-URL lowercaser rejects them; none of the 32 frozen cases exercises a case-only URL difference.
- From `Case08.md`'s `rel_near_miss_token` and its non-ASCII-whitespace variant: those probe `rel` token boundaries; this probes where case-insensitivity is allowed to apply after the keyword has been accepted.
- From `URLNormalization.md` risk P2: that note says "preserve case-sensitive path distinctions" as a general falsification target; this supplies the concrete paired probe and its frozen exit/id, which P2 leaves otherwise unmeasured.
- Adjacency to this case: the page keeps `rel="CANONICAL"` and only perturbs the path case, so the property under test is exactly the boundary of the rule that makes `rel_uppercase` a positive control — keyword matching is ASCII case-insensitive, URL path comparison is not.

### Paired control (not a second attack)

To distinguish a correct component-aware normalizer from a raw-string comparator, run the same page with `href="HTTPS://EXAMPLE.TEST/project/a.html"` (path unchanged). Expected: exit `0`, clean, because scheme and host are case-insensitive and normalize to lowercase (RFC 3986 §6.2.2.1). `[INFERENCE]` only on the lane's accepted WHATWG-like normalization profile; the path rule itself is explicit. A raw-string comparator would false-red this control; a whole-URL lowercaser would false-green the attack. The pair pins the exact boundary.

## Observed vs inference

| Claim | Status |
|---|---|
| Contract policy, exit map, finding IDs, case name | Observed in `.ufo/waves/round-22/contract.json` |
| HTML/Infra/RFC quotes in "Why" and the attack | Observed, fetched 2026-10-20 UTC from official public documentation (`html.spec.whatwg.org`, `infra.spec.whatwg.org`, `rfc-editor.org`, `url.spec.whatwg.org`); no live property probed |
| `HTMLParser` preserves attribute-value case and lowercases attribute names | Observed locally on CPython 3.14.8 (`/usr/lib/python3.14/html/parser.py:483-484` plus a one-line probe) |
| `rel_uppercase` must be exit 0 / no finding | Contract policy + spec derivation; high confidence |
| `href_path_case` must be exit 1 / `canonical_mismatch` | Spec derivation (RFC 3986 component rules) + contract comparison rule; high confidence |
| Exact `verdict` strings and `cases.json` clean sentinel | Unknown/`[INFERENCE]`; contract names the fields but not the literal vocabulary |
| Fixture bytes and manifest location | Recommendation; Matrix owns final bytes, provided the single-axis constraints hold |
| Google canonical selection, browser rendering, HTTP behavior | Out of scope by contract; not claimed |

## Remaining unknowns (for L1 / Implement / Matrix)

1. Frozen verdict token for exit 0 and for exit 1; `cases.json` and the validator must agree, and the matrix should not depend on a token the contract does not enumerate.
2. Whether Matrix co-locates the HTML beside `manifest.json` (recommended, keeps `file` a bare name) or uses another manifest layout. The invariant is the fixture content, not the path.
3. Whether the implementation normalizes `expectedCanonical` with the same routine as the declared `href`. It should; otherwise a manifest whose expected value contains uppercase scheme/host would create a false red.
4. Whether the validator's URL comparator is component-wise or serialized-string based. The attack exists to falsify the latter only if it lowercases the whole string; a plain raw string comparator would pass the attack but fail the paired control (false red on uppercase scheme/host).
5. No implementation existed at this base; this report specifies expectations only and ran no tests.

## Checks for L1 (not run by this seat)

- Encode `rel_uppercase` as exit `0` with no finding (or the matrix's frozen `clean` sentinel) and an uppercase-`rel` positive fixture with a single canonical link in the explicit head.
- Reject any matrix entry that expects `canonical_missing`/exit `1` for `rel_uppercase`; that would bless value-case-sensitive keyword matching.
- Verify the implementation ASCII-folds the `rel` **value** token(s) itself; `HTMLParser` lowercases names, not values.
- Run the `href_path_case` attack as an out-of-matrix probe: exit `1`, `canonical_mismatch`. Run the uppercase-scheme/host paired control: exit `0`, clean. Do not add either to the frozen 32-case matrix this round.
- Confirm the URL comparator preserves path case and does not lowercase the serialized URL as a shortcut; scheme/host normalization must be component-aware. If `urllib.parse` is used, local observation on CPython 3.14.8: `urlsplit("HTTPS://EXAMPLE.TEST/Project/A.html")` yields `.scheme == "https"`, `.hostname == "example.test"`, but `.netloc == "EXAMPLE.TEST"` and `.path == "/Project/A.html"`; comparing `SplitResult`, `.netloc`, or `urlunsplit(...)` strings is therefore wrong in both directions. Compare `(scheme, hostname, port, path, query)` component-wise and keep `path`/`query` byte-exact.
- Confirm this seat wrote only this report (no lane/corpus edits, no git/jj writes).

## Sources

Fetched 2026-10-20 (UTC) by this seat from official public documentation. The working-tree `corpus/SOURCES.md` (round-22 additions) registers S023 WHATWG HTML canonical/link types — including the ASCII case-insensitive keyword statement — plus S026 Python `html.parser` and S027 Python `urllib.parse`; those are the lane-available citations. RFC 8288 §2.1, RFC 3986 §6.2.2.1, RFC 9110 §4.2.3 and the Infra Standard ASCII-case-insensitive definition have no registered `SOURCES.md` row at this read, so those quotes are fresh official-documentation corroboration, not lane-admitted entries. No registry edits were made.

Lane entry `corpus/knowledge/static-canonical-preflight.md` states the policy requires "exact agreement with the manifest's expectedCanonical after its documented URL normalization", consistent with case-sensitive path comparison; it does not itself enumerate rel/path case rules.

- WHATWG HTML Standard, §4.6.8 *Link types* — https://html.spec.whatwg.org/multipage/links.html#linkTypes. Quotes: "must be split on ASCII whitespace. The resulting tokens are the keywords for the link types that apply to that element."; "Keywords are always ASCII case-insensitive, and must be compared as such."
- WHATWG HTML Standard, §4.6.8.4 *Link type "canonical"* — https://html.spec.whatwg.org/multipage/links.html#link-type-canonical. Quotes: "The `canonical` keyword may be used with `link` element."; "The `canonical` keyword indicates that URL given by the `href` attribute is the preferred URL for the current document."
- WHATWG Infra Standard, §4 *Strings* — https://infra.spec.whatwg.org/#ascii-case-insensitive and https://infra.spec.whatwg.org/#ascii-whitespace. Quotes: "A string A is an ASCII case-insensitive match for a string B, if the ASCII lowercase of A is the ASCII lowercase of B."; "ASCII whitespace is U+0009 TAB, U+000A LF, U+000C FF, U+000D CR, or U+0020 SPACE."
- RFC 8288, *Web Linking*, §2.1 — https://www.rfc-editor.org/rfc/rfc8288.html#section-2.1. Quote: "Registered relation type names MUST conform to the `reg-rel-type` rule (see Section 3.3) and MUST be compared character by character in a case-insensitive fashion."
- RFC 3986, *URI Generic Syntax*, §6.2.2.1 *Case Normalization* — https://www.rfc-editor.org/rfc/rfc3986.html#section-6.2.2.1. Quote: "the scheme and host are case-insensitive and therefore should be normalized to lowercase. … The other generic syntax components are assumed to be case-sensitive unless specifically defined otherwise by the scheme."
- RFC 9110, *HTTP Semantics*, §4.2.3 *http(s) Normalization and Comparison* — https://www.rfc-editor.org/rfc/rfc9110.html#section-4.2.3. Quote: "The scheme and host are case-insensitive and normally provided in lowercase; all other components are compared in a case-sensitive manner."
- WHATWG URL Standard, host parsing and serialization — https://url.spec.whatwg.org/#concept-host-parser (scheme/host normalization model; path state preserves case). Used as the model for "WHATWG-like" normalization, not as proof of a Python stdlib implementation.
- Local corroboration: CPython 3.14.8 `/usr/lib/python3.14/html/parser.py:483-484` (`attrs.append((attrname.lower(), attrvalue))`) and one-line probes in this seat's scratch space; sibling reports `Case08.md`, `Case10.md`, `URLNormalization.md`, `PythonParser.md` in this wave.

Report: `.ufo/waves/round-22/w1/Case09.md`
