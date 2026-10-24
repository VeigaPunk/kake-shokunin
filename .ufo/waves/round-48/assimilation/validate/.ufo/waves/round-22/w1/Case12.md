# Case12 — `query_preserved`

Seat: `KakeR22.Case12` (scout, leaf). Read-only apart from this report. Lane `kake-shokunin`, base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`; contract read from `.ufo/waves/round-22/contract.json` (C1, matrix case 12 of 32). No tests, no lane scripts, no commits, no installs. Scratch fetches live in `/tmp/kake-r22-case12/` (public official documentation only; no host services, no live properties).

## Result

| Field | Expected |
|---|---|
| Manifest `url` (document URL) | `https://example.test/project/a.html?page=2` |
| Canonical `href` | `?page=2` (query-only relative reference) |
| `expectedCanonical` | `https://example.test/project/a.html?page=2` |
| Exit | **0** |
| Verdict | `clean` (literal inferred from `exitMap`; see unknowns) |
| Finding id | **none** — `findings: []` |
| `pagesChecked` | 1 |

This is the positive control for the contract's "preserve query" clause. It is a declaration/URL-policy case only: it does not claim the page content is duplicative, that a search engine would select this canonical, or that any network/HTTP/JS signal exists.

## Concrete fixture

Manifest entry (matrix-chosen manifest path; HTML paths are relative to the manifest directory):

```json
{"version": 1, "pages": [
  {"url": "https://example.test/project/a.html?page=2",
   "file": "fixtures/query_preserved.html",
   "expectedCanonical": "https://example.test/project/a.html?page=2"}
]}
```

`fixtures/query_preserved.html`:

```html
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link rel="canonical" href="?page=2">
</head>
<body><p>query_preserved positive control</p></body>
</html>
```

Design constraints (so the case stays single-axis):

- Exactly one `link` in an explicit `<head>`; `rel` is the single lowercase token `canonical`; no `<base>`, no fragment, no credentials, no second/decoy link.
- The `href` is a query-only relative reference: no scheme, authority, or path; its query component is defined (`page=2`). That is the component-preservation probe, and RFC 3986 §5.2.2 handles it without path merging.
- The `file` is a regular file; `?page=2` appears only in the manifest `url`, `expectedCanonical`, and the `href`. It must never be appended to the filesystem path.
- `page=2` is already safe for the WHATWG special-query percent-encode set (ASCII alphanumerics and `=` are not encoded), so the only transformation is resolution, not percent-encoding normalization.
- If Matrix prefers to isolate comparison from resolution, use the absolute variant `href="https://example.test/project/a.html?page=2"`; the expected outcome is unchanged. The relative variant is preferred here because it also proves the resolver does not drop the query.

Optional tracking-query variant (selftest/adversarial set, not the frozen case if Matrix enforces `url == expectedCanonical`): set `url` to `https://example.test/project/a.html?utm_source=nav` but keep `expectedCanonical` and `href` at `...?page=2`. Correct result is still clean. This additionally falsifies a validator that ignores the href and compares the document URL, and it exercises query replacement rather than same-value preservation.

## Why exit 0 / clean

1. **Resolution.** RFC 3986 §5.2.2 (transform references): for a reference with no scheme/authority and an empty path, `T.path = Base.path` and `if defined(R.query) then T.query = R.query; else T.query = Base.query`. Here `R.query` is defined (`page=2`), so the target is `https://example.test/project/a.html?page=2`. RFC 3986 §5.3 recomposition appends `?` and the query because the query is defined.
   - Local corroboration (Node 2026-10-20): `new URL("?page=2", "https://example.test/project/a.html?page=2").href` returns `https://example.test/project/a.html?page=2`. CPython 3.14.8 `urllib.parse.urljoin` returns the same.
2. **Query is a URL component.** WHATWG URL §4.1: "A URL's query is either null or an ASCII string." §4.4 query state appends the query text; §4.5: "If url's query is non-null, append U+003F (?), followed by url's query, to output." §4.6 defines URL equality as equality of serializations. The resolved serialization is exactly the expected string.
3. **The expected string is already normalized.** Lowercase scheme/host, no default port, no dot segments, no percent-encoding change. There is no host, scheme, port, or path axis to confound the query.
4. **Canonical semantics.** RFC 6596 §3: the target canonical IRI MAY "Specify a relative IRI (see [RFC3986], Section 4.2)." §4's worked example uses a query-bearing canonical target `http://www.example.com/page.php?item=purse`, with duplicate IRIs carrying extra query parameters, and a relative form `<link rel="canonical" href="page.php?item=purse">`. A canonical target with a query, declared relatively, is explicitly in scope and is the canonical relation's primary use case (session/tracking parameters).
5. **HTML shape.** HTML Standard §4.6.8.4: "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." §4.6.8: "Keywords are always ASCII case-insensitive, and must be compared as such." `canonical` is not in the body-ok list, so explicit-head placement is the conforming/policy shape. Google Search Central corroborates that the `rel="canonical"` link element is "used in the `head` section" and "is only accepted if it appears in the `<head>` section"; it also says not to use a fragment. None of those negative conditions apply.
6. **Exactly one canonical signal.** One link, no duplicate, no body/comment/script/template decoy. Under the frozen policy the page is clean: exit 0, `pagesChecked: 1`, `findings: []`.

## Discrimination analysis

What this fixture catches:

- A resolver that treats `?page=2` as a path or drops the query when joining (path-only join, string concatenation on the path, splitting at `?` and rejoining without the query).
- A comparator that omits the query component from normalized equality (path-only comparison).
- A parser that treats `?` as a fragment delimiter or rejects a query-only relative reference as invalid/unsupported.

What it cannot catch by itself:

- **Symmetric query stripping.** If the validator strips the query from both the resolved href and `expectedCanonical`, both become `https://example.test/project/a.html` and this case returns clean for the wrong reason. Only a query-negative case (`wrong_query`, or the attack below) makes that observable. The frozen matrix must pair `query_preserved` with a query-negative case; a positive-only suite cannot prove query significance.
- **Href-ignoring.** Because `url == expectedCanonical`, a validator that never reads the href and compares the document URL to expected also returns clean. The optional tracking-query variant closes that gap; if Matrix keeps the primary fixture, do not claim this case proves href use.

This is the correct place for the positive expectation: mapping `query_preserved` to exit 1/`canonical_mismatch` would bless query dropping as correct.

## Adjacent false-green attack (distinct from this case)

**Name:** `empty_query_delimiter` (not one of the 32 frozen names).

**Manifest:**

```json
{"version": 1, "pages": [
  {"url": "https://example.test/project/a.html",
   "file": "fixtures/query_empty_delimiter.html",
   "expectedCanonical": "https://example.test/project/a.html"}
]}
```

**HTML:**

```html
<!doctype html>
<html>
<head>
<link rel="canonical" href="https://example.test/project/a.html?">
</head>
<body></body>
</html>
```

**Correct expectation:** exit **1**, finding **`canonical_mismatch`**, page `https://example.test/project/a.html`.

**Why that is the correct verdict:**

- The resolved href has a query component that is present but empty: `https://example.test/project/a.html?`. The expected URL has no query component: `https://example.test/project/a.html`.
- RFC 3986 §5.3 says recomposition appends `?` iff the query is defined, and explicitly preserves "the distinction between a component that is undefined ... and a component that is empty." §6.2.3: "Normalization should not remove delimiters when their associated component is empty unless licensed to do so by the scheme specification. For example, the URI `http://example.com/?` cannot be assumed to be equivalent to any of the examples above."
- WHATWG URL §4.1/§4.5/§4.6: empty query is non-null, the serializer appends `?`, and equality is serialization equality. Observed locally (Node 2026-10-20): `new URL("https://example.test/project/a.html?").href` returns `"https://example.test/project/a.html?"`; without `?` it returns `"https://example.test/project/a.html"`.
- Both are valid HTTP(S) URLs, so the correct classification is a comparison failure (`canonical_mismatch`), not `canonical_url_invalid` and not exit 2.

**False-green mechanism.** CPython 3.14.8 `urllib.parse.urlsplit` cannot represent the difference: `urlsplit("...?")` and `urlsplit("...")` both yield `query=''`; `SplitResult.geturl()` and `urlunsplit()` drop the empty query (observed locally). Worse, the official Python 3.14 `urllib.parse` docs call a `?` with an empty query an "unnecessary delimiter" and state "the RFC states that these are equivalent" (`urlunsplit`/`urlunparse` entries). An audit that normalizes each side through `urlsplit`/`urlunsplit` (or compares `parsed.query` or the WHATWG `URL.search` getter, which also returns `""` for both forms while `.href` preserves the `?`) therefore collapses both URLs to `https://example.test/project/a.html` and returns clean — a false green.

**Why the contract, not the stdlib doc, governs.** The frozen policy requires a "WHATWG-like HTTP(S) normalized absolute URL" comparison and says "preserve query." That makes null and empty query distinct. The Python doc's parenthetical is an implementation-doc claim about equivalence, not a policy rule, and it conflicts with RFC 3986 §6.2.3 and the WHATWG serializer. An implementer must not adopt it as the audit's equality rule.

**Fix direction (implementation constraint, not prescriptive code).** Carry query presence separately from the parsed query value (for an HTTP(S) URL, the first `?` before any `#` marks a query component, including an empty one), or use a WHATWG-faithful serializer that models `query = null | ""`. Do not round-trip through `urlsplit`/`urlunsplit`/`geturl` for equality, and do not compare the WHATWG `search` getter or `parse_qs` maps.

**Why it is distinct from `query_preserved`:**

- `query_preserved` has a non-empty query and expects clean; this attack has an empty query versus no query and expects a mismatch.
- A validator can pass `query_preserved` (even `urljoin` preserves the trailing `?`) and still false-green this attack if it normalizes through `urlunsplit` or compares components afterward.
- It is not `wrong_query` (no parameter value differs), not `fragment_url` (no `#`), not `duplicate_*`, and not `href_empty` (the href is non-empty and parses to a valid URL).
- It is not in the frozen 32 names; use it as an extra selftest/adversarial assertion, not as a substitute for any frozen case.

**Additional hazard (not the named attack).** Comparing parsed query maps conflates distinct serializations: on CPython 3.14.8, `parse_qs("a=1&b=2") == parse_qs("b=2&a=1")` is `True`, and `parse_qs("q=a+b") == parse_qs("q=a%20b")` is `True` (observed locally). WHATWG equality is serialized-string equality; query order, `+` versus `%20`, and duplicate keys are significant. A fixture with href `...?b=2&a=1` against expected `...?a=1&b=2` must be `canonical_mismatch`, not clean.

## Stdlib / HTMLParser limits that apply here

- `html.parser.HTMLParser` is a tokenizer, not a tree builder. It reports `link` with lowercase attribute names and already-decoded attribute values; it does not report whether the element is in `<head>`. The explicit-head state machine is audit-side (PythonParser.md documents this). The fixture's single explicit head keeps that state machine trivial.
- `href="?page=2"` arrives unchanged as the attribute value (observed locally: `('href', '?page=2')`); no character-reference decoding changes the `?` or the query.
- The primary fixture uses `<link ...>` rather than `<link ... />`. If `<link ... />` is used, `handle_startendtag` defaults to `handle_starttag` + `handle_endtag`; the audit must not double-count the link or pop `<head>` on the void element.
- Successful parsing is not validation. `HTMLParser` accepts malformed markup and truncated input without raising; the audit must apply the contract's checks explicitly.

## Sources (official; fetched 2026-10-20 UTC)

| ID | Source and locator | Exact text used | Use |
|---|---|---|---|
| S1 | RFC 6596 §3, https://www.rfc-editor.org/rfc/rfc6596.html | "Specify a relative IRI (see [RFC3986], Section 4.2)." | Relative canonical targets are permitted |
| S2 | RFC 6596 §1 | "Common implementations ... specify the preferred version of an IRI from duplicate pages created with the addition of IRI parameters (e.g., session IDs)" | Query-parameter duplicates are the canonical relation's primary use case |
| S3 | RFC 6596 §4 | "Two IRIs with additional query parameters, making them the non-preferred version of the content (duplicates)"; example target `http://www.example.com/page.php?item=purse`; relative form `<link rel="canonical" href="page.php?item=purse">` | Canonical target with a query, including relative declaration |
| S4 | RFC 3986 §3.4, https://www.rfc-editor.org/rfc/rfc3986.txt | "The query component contains non-hierarchical data that, along with data in the path component ... serves to identify a resource" | Query is part of resource identity |
| S5 | RFC 3986 §5.2.2 | "if defined(R.query) then T.query = R.query; else T.query = Base.query;" (inside the empty-path branch) | Resolution of `?page=2` |
| S6 | RFC 3986 §5.3 | "we are careful to preserve the distinction between a component that is undefined ... and a component that is empty"; recomposition appends `?` iff the query is defined | Empty query versus absent query |
| S7 | RFC 3986 §6.2.3 | "Normalization should not remove delimiters when their associated component is empty ... the URI `http://example.com/?` cannot be assumed to be equivalent to any of the examples above." | Empty-query attack is a mismatch |
| S8 | WHATWG URL §4.1, https://url.spec.whatwg.org/#url-representation | "A URL's query is either null or an ASCII string. It is initially null." | Query is a first-class component |
| S9 | WHATWG URL §4.4, query state | "set url's query to the empty string and state to query state" on `?` | Empty query is non-null |
| S10 | WHATWG URL §4.5, URL serializing | "If url's query is non-null, append U+003F (?), followed by url's query, to output." | Serializer preserves `?`, including empty query |
| S11 | WHATWG URL §4.6, URL equivalence | "Return true if serializedA is serializedB; otherwise false." | Equality is serialization equality |
| S12 | HTML Standard §4.6.8.4, https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." | Canonical keyword semantics |
| S13 | HTML Standard §4.6.8 | "Keywords are always ASCII case-insensitive, and must be compared as such."; "The body-ok keywords are dns-prefetch, modulepreload, pingback, preconnect, prefetch, preload, and stylesheet." | `rel` token matching; `canonical` is not body-ok |
| S14 | Google Search Central, "How to specify a canonical URL with rel=canonical and other methods", https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | "an element used in the `head` section"; "only accepted if it appears in the `<head>` section"; "Don't specify a URL fragment as canonical"; relative paths "are supported by Google" but not recommended; duplicate example `https://example.com/dresses/cocktail?gclid=ABCD` versus the clean product URL | Platform corroboration of head-only/no-fragment and query-bearing duplicates; not URL-equality authority |
| S15 | Python 3.14.8 docs, `urllib.parse.urlunsplit`/`urlunparse`, https://docs.python.org/3.14/library/urllib.parse.html | "may result in a slightly different, but equivalent URL, if the URL that was parsed originally had unnecessary delimiters (for example, a ? with an empty query; the RFC states that these are equivalent)" | Documented false-green trap (conflicts with S7/S10) |
| S16 | Local observations, 2026-10-20: Node `new URL`; CPython 3.14.8 `urlsplit`/`urlunsplit`/`urljoin`/`parse_qs`; `html.parser` probe | `...?` serializes with `?` in WHATWG; `urlsplit`/`urlunsplit` drop it; `urljoin` preserves it; `parse_qs` conflates order and `+`/`%20`; `HTMLParser` yields `('href', '?page=2')` | Corroborates the platform/stdlib behavior; not a substitute for the quoted specs |

Google's absolute-URL recommendation does not override the contract: RFC 6596 §3 permits relative IRIs, the contract explicitly supports resolution, and Google itself says relative paths are supported. The validator must accept the relative fixture.

## Remaining unknowns / explicit inferences

- The literal `verdict: "clean"` is `[INFERENCE]` from `exitMap`'s "0: clean"; the contract does not enumerate verdict values. Exit 0, `pagesChecked: 1`, and `findings: []` are contract-derived.
- The `page` value in a finding is assumed to be the manifest `url` (page identity), not `file`; the contract says each finding contains `id` and `page` but does not define the value. The attack expectation uses the URL.
- Fixture paths/bytes are recommendations; Matrix owns the final frozen fixtures. The matrix may require `url == expectedCanonical` for positive cases; the primary fixture respects that. The tracking-query variant is optional and must not silently replace the frozen case.
- Whether a positive case's "id" is represented as a `clean` sentinel or only as an empty `findings` array is not specified; keep both consistent.
- The lane interpreter is CPython 3.14.8; the 3.15 docs add `keep_empty`/`missing_as_none`, but 3.14 has neither. Delimiter tracking cannot depend on 3.15-only parameters; it must work on 3.14.
- No implementation (`scripts/canonical_audit.py`, matrix, measure) exists at base; no test, CLI, or matrix run was performed. All expectations here are static policy analysis.

## Checks for L1 (not run here)

1. Freeze `query_preserved` as exit 0, `pagesChecked: 1`, `findings: []`, with a non-empty matching query in the fixture.
2. Reject any matrix expectation that maps `query_preserved` to exit 1/`canonical_mismatch`; that would encode query dropping as correct.
3. Ensure at least one query-negative case remains (`wrong_query` and/or the empty-query attack); without it, symmetric query stripping is unobservable.
4. Inspect the audit for `urlsplit`/`urlunsplit`/`geturl` round-trips, `URL.search` equality, or `parse_qs` equality; run `https://example.test/project/a.html?` against the same URL without `?` and require `canonical_mismatch`.
5. Confirm `file` resolution never appends the manifest query to the filesystem path, and findings use the manifest `url` as `page`.
6. Confirm this seat wrote only this report and no lane/registry/corpus bytes.
