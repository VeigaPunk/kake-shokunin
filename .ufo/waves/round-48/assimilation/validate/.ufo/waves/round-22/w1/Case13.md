# Case13 — matrix case `missing_link`

Status: author-side scoped recommendation. Read-only seat; no lane files, fixtures, registry, verifier or
historical corpus bytes touched. No validator, test, matrix or measure run was executed. Timestamp 2026-10-20.
Frozen authority: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/contract.json`
(base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`; live lane observed at that revision).

## Axes (Godspeed)

1. **Classification correctness** — one exit code and one finding id that cannot be confused with a
   neighbouring failure mode.
2. **Causal discrimination** — the fixture must fail *only* because the canonical element is absent, so an
   A/B sibling page with the same URL and the element present must be clean.
3. **False-green resistance** — name the adjacent shortcut that would return `exit 0` on this page class.
4. **Reproducibility** — exact bytes, regular file, no network, no environment dependence.
5. **Source honesty** — separate pinned contract rules, fetched spec text, and inference.

## Case definition (freeze this)

| Field | Value |
|---|---|
| matrix case | `missing_link` |
| `url` | `https://example.test/project/a.html` |
| `file` | `a.html` (relative to the manifest directory: `fixtures/missing_link/a.html`) |
| `expectedCanonical` | `https://example.test/project/a.html` |
| expected exit | **1** |
| expected finding id | **`canonical_missing`** |
| `page` value in the finding | `https://example.test/project/a.html` (the manifest `url`) |
| `pagesChecked` | `1` |

`url` and `expectedCanonical` are deliberately the same absolute URL as the contract's `absolute_match`
example. The case is then a **differential pair**: identical URL and expected value, only the canonical
`link` element removed. The expected exit difference is caused by the absence alone, not by a URL mismatch,
a relative-resolution difference, a different host, or a base element.

### Fixture bytes — `fixtures/missing_link/a.html`

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>missing_link</title>
</head>
<body>
<h1>No canonical link element</h1>
<p>The head is explicit and complete; only the preferred-URL declaration is absent.</p>
</body>
</html>
```

Properties that matter:

- Literal `<head>` start tag and `</head>` end tag: an **explicit** head exists, so this is not `missing_head`.
- No `<link>` element anywhere, no `<base>`, no comment or script, and no occurrence of the token
  `canonical` in text, attributes or comments. The fixture isolates structural absence; it does not also
  test decoy handling.
- Regular UTF-8 file, LF, no BOM, no symlink, inside the manifest directory; the manifest resolves
  `a.html` relative to itself.

### Manifest bytes — `fixtures/missing_link/manifest.json`

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "a.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

### Expected validator result

```json
{
  "verdict": "<failed vocabulary>",
  "pagesChecked": 1,
  "findings": [
    {"id": "canonical_missing", "page": "https://example.test/project/a.html"}
  ]
}
```

The contract pins `verdict`, `pagesChecked`, `findings[].id` and `findings[].page` but does **not** pin the
verdict string. The matrix must assert on **exit code + finding id** (its own task text: "expected exit AND
stable finding-id per case"); the verdict literal is an inference and should be pinned only if L1 adds it to
the contract. Exactly one finding is recommended so the matrix has a stable cardinality; the contract
requires at least the `canonical_missing` finding.

## Why exit 1 / `canonical_missing`

1. **Policy rule.** Contract: "Exactly one canonical link in explicit head per page" and claim C1 must
   "reject missing/conflicting/mismatching canonical signals". Zero canonical links is a failed policy, so
   exit **1**.
2. **Exit taxonomy.** Contract `exitMap`: `0` clean, `1` failed policy, `2` could-not-evaluate
   input/unsupported shape, `64` usage. This document is fully evaluable — valid UTF-8, regular file inside
   the manifest directory, explicit head, serialized static HTML — so the audit reaches a verdict about the
   content. Exit 2 would misreport a policy failure as an inability to evaluate. Exit 64 is usage-only.
3. **Finding id.** `canonical_missing` is the only id for "zero canonical links". The other structural ids
   must stay disjoint:
   - `canonical_href_missing` = a `link rel=canonical` exists but has no `href` (`href_absent` case);
   - `canonical_outside_head` = a canonical link exists outside the explicit head (`body_link` case);
   - `html_unsupported` = no explicit head / non-HTML shape (`missing_head` case, exit 2);
   - `input_invalid` = manifest/file resolution failure (`manifest_traversal`, `symlink_html`);
   - `canonical_multiple` = two or more canonical links in head (`duplicate_*`).
   `missing_link` has **zero canonical link elements in the whole serialized document**, which is what
   separates it from `body_link`. Recommendation: emit `canonical_missing` only when the document-wide
   canonical count is 0; if any canonical appears outside head, emit `canonical_outside_head` instead.
4. **Implementation trap (the likely false green on this case).** An implementation that only emits
   findings from inside a per-`link`-element loop never executes that branch on this page, so it returns
   `exit 0` with `findings: []`. The absence must be concluded from a document-level state machine
   (`head_seen`, in-head canonical count, out-of-head canonical count) at end of head/document, not from a
   node visit. This is the concrete reason the case exists.
5. **Boundary with `missing_head`.** An empty explicit `<head></head>` is still evaluable and yields
   `canonical_missing` (exit 1). A document with no explicit `<head>` start tag at all is `html_unsupported`
   (exit 2). Without that split, `html_unsupported` has no home in the 32-case matrix and exit 2 collapses
   into `input_invalid`.

## Positive control (proves causality, not required by the matrix name)

Same file plus one line inside head:

```html
<link rel="canonical" href="https://example.test/project/a.html">
```

Expected: exit **0**, `findings: []` (positive id `clean` per the Matrix task text). If the pair cannot be
distinguished, the `canonical_missing` id is not tracking absence and the case is untrustworthy.

## One adjacent false-green attack (distinct from this case)

### `rel` substring decoy — `fixtures/missing_link/rel-substring-decoy.html`

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="canonicalized" href="https://example.test/project/a.html">
<title>rel substring decoy</title>
</head>
<body>
<h1>No canonical link element</h1>
</body>
</html>
```

Manifest entry: `url` `https://example.test/project/a.html`, `expectedCanonical`
`https://example.test/project/a.html`, expected exit **1**, expected id **`canonical_missing`**.

Why this is the false green: the page contains a `link` element whose `href` already equals
`expectedCanonical`; the only defect is the `rel` value. An implementation that tests the substring
`"canonical" in rel.lower()` (or a regex `canonical` anywhere in the attribute) accepts the element,
resolves the href, compares equal, and returns **exit 0** — while the document declares no canonical at all.
The correct rule is exact token typing: split `rel` on ASCII whitespace, ASCII-lowercase each token, require
a token equal to `canonical`. Variants of the same bug class: `rel="not-canonical"`, `rel="xcanonical"`,
`rel="canonical2"`.

Spec basis (WHATWG HTML Standard, fetched 2026-10-20):
- Link types are resolved by splitting `rel` into tokens: "the element's `rel` attribute must be *split on
  ASCII whitespace*. The resulting tokens are the keywords for the link types that apply to that element."
  (links.html, "Link types")
- "Keywords are always ASCII case-insensitive, and must be compared as such."
- On `link`: "If the `rel` attribute is absent, has no keywords, or if none of the keywords used are
  allowed according to the definitions in this specification, then the element does not create any links."
  (semantics.html, `link` element) Therefore `rel="canonicalized"` creates no link and no canonical signal.
- "The `canonical` keyword may be used with `link` element. ... indicates that URL given by the `href`
  attribute is the preferred URL for the current document." (links.html §4.6.8.4, link type "canonical")

Why it is distinct: it is not `body_link` (the element is in head), not `comment_decoy`/`script_decoy`/
`template_decoy` (the element is live markup), not `href_absent`/`href_empty` (an href exists), not
`duplicate_*` (one element), and not `rel_uppercase`/`rel_token_list` (those are positives: a real
`canonical` token in different case or alongside other tokens must pass). It only fails if `rel` is typed by
token equality; no named matrix case exercises that negative path.

## Sources

**Fetched by this seat, 2026-10-20** (official documentation; no live properties contacted):
- WHATWG HTML Standard, "Link types" and §4.6.8.4 "Link type `canonical`":
  <https://html.spec.whatwg.org/multipage/links.html#linkTypes>, `#link-type-canonical`.
  Quotes: "The `canonical` keyword may be used with `link` element."; "indicates that URL given by the
  `href` attribute is the preferred URL for the current document."; "must be split on ASCII whitespace";
  "Keywords are always ASCII case-insensitive, and must be compared as such."
- WHATWG HTML Standard, `link` element `rel` requirement:
  <https://html.spec.whatwg.org/multipage/semantics.html#the-link-element>. Quote: "must have a value that
  is an unordered set of unique space-separated tokens"; "then the element does not create any links."
- Python 3 documentation, `html.parser`: <https://docs.python.org/3/library/html.parser.html>, plus local
  interpreter 3.14.8. Quotes: `HTMLParser(convert_charrefs=True, scripting=False)`; "If *scripting* is
  false (the default), the content of the `noscript` element is parsed normally"; "This parser does not
  check that end tags match start tags or call the end-tag handler for elements which are closed implicitly
  by closing an outer element"; `handle_startendtag()` defaults to `handle_starttag()` + `handle_endtag()`
  (verified in the local stdlib source). Consequence: no implied `head`/`body` synthesis, so the explicit-head
  test must be literal; end-of-document, not end-tag matching, is the correct place to conclude absence.

**Already available in this wave, not re-fetched by this seat** (sibling-verified 2026-10-20):
- Google Search Central, "How to specify a canonical URL with rel=canonical":
  <https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls>, quote via
  `w1/GoogleCanonical.md`: "The rel="canonical" link element is only accepted if it appears in the <head>
  section of the HTML"; self-referential canonical recommended. Platform guidance, not a conformance
  authority: it does not require a canonical to exist, so `canonical_missing` is **C1 local policy**.
- RFC 6596, *The Canonical Link Relation* (Informational, April 2012), via `w1/RFC6596.md`: §3 defines the
  relation and its single normative MUST (target identifies duplicative or superset content); presence is
  not mandated, and "specify only one" is administrator guidance. Confirms the id is policy-scoped, not an
  RFC non-conformance claim.

## Remaining unknowns / open seams for L1

- Verdict string vocabulary is unpinned; matrix should compare exit + id only (inference from the Matrix
  task text).
- Finding cardinality for this case (recommended exactly one) is not stated in the contract.
- `missing_link` vs `missing_head` exit split is contract-implied (`html_unsupported` + exit 2), not
  spelled out per case; Matrix and Implement must freeze the same split or the measure disagrees.
- No test or matrix execution was performed by this seat; exit/id claims are design recommendations plus
  spec/policy reasoning, not observed validator output.
