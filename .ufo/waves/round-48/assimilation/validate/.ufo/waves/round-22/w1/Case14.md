# Case14 — `duplicate_same`

Seat: KakeR22.Case14 (scout, read-only). Lane observed at base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`. `git status` also showed other seats' uncommitted round-22 work (modified `LOG.md`, `PROVINCE.md`, `SKILL.md`, `corpus/{QUALITY,README,SOURCES}.md`; untracked `.ufo/waves/round-22/`, `corpus/knowledge/static-canonical-preflight.md`, `corpus/lessons/round-22.md`); I did not edit any of it. This report is my only write. No implementation, matrix or capability tests were run; only read-only source inspection, public-documentation fetches, and stdlib property checks were executed. No installs, no network writes.

## 1. Frozen rule and the intended reading

Contract policy (`.ufo/waves/round-22/contract.json` line 4, observed):

> Exactly one canonical link in explicit head per page, rel ASCII case-insensitive token list; resolve href with first head base href or document URL; compare WHATWG-like HTTP(S) normalized absolute URL to expectedCanonical, preserve query, reject fragments and credentials. HTMLParser stdlib limitations must be explicit. No automatic fetching, JS, or Google canonical selection claim.

`duplicate_same` is **two `link` elements in the explicit head whose `rel` token sets contain `canonical`, with identical `href` values resolving to the manifest's `expectedCanonical`**. Cardinality is over **link elements**, not over distinct resolved targets. "Exactly one" is violated by the second element even when both agree. Expected: **exit 1, `canonical_multiple`**.

This is the intended reading, not one of two equally valid ones:

- The contract says "exactly one canonical link", not "at most one distinct canonical target".
- The frozen id set separates `canonical_multiple` (cardinality) from `canonical_mismatch` (value difference). `duplicate_same` has no value difference, so only `canonical_multiple` fits.
- The matrix lists both `duplicate_same` and `duplicate_different`. The coherent design is that each kills a different false-green mechanism (URL/target dedupe vs first/last-wins), not that one is a deliberate clean control. `[INFERENCE]` from the contract's case-name composition; I have not seen Matrix's `cases.json`.
- RFC 6596 §3 administrator guidance says: "Specify only one canonical link relation for a resource. (It would be confusing to consider/label/designate more than one IRI as authoritative.)" This is guidance ("ought"), not a MUST; the hard fail is the local contract, so the finding must stay policy-scoped.
- Google's 2013 Search Central blog states: "Specify no more than one `rel=canonical` for a page. When more than one is specified, all `rel=canonical` links will be ignored." Historical/non-normative; the current canonical-URL reference (last updated 2026-07-10) does not restate duplicate precedence. Use as rationale only, never as finding text or as a claim about Google's selection.

**Correlated-error warning for L1:** if Matrix also reads `duplicate_same` as clean and Implement dedupes, `measure.py` can still report 32/32 accepted. The frozen matrix is the only independent guard; freeze this expectation before Matrix writes `cases.json`.

## 2. Concrete fixture

Manifest (HTML path relative to the manifest directory; use the round-22 `fixtures/` convention):

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "fixtures/duplicate_same.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

`fixtures/duplicate_same.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>duplicate same</title>
  <link rel="canonical" href="https://example.test/project/a.html">
  <link rel="canonical" href="https://example.test/project/a.html">
</head>
<body>
  <p>duplicate_same</p>
</body>
</html>
```

- **URL / `expectedCanonical`:** `https://example.test/project/a.html`.
- No `<base>`; both hrefs are absolute, so the duplicate rule is isolated from resolution.
- Both links are in the explicit head; no comment/script/template decoy; no body link; no fragment, query, credential, host or scheme difference.
- The hrefs are **byte-identical**, so both exact-string dedupe and resolved/normalized-URL dedupe are exposed. A differently-spelled-same-URL variant adds nothing here: identical hrefs already collapse under both.

### Expected result

- **Exit:** `1` (failed policy).
- **Finding id:** `canonical_multiple`.
- **Page:** `https://example.test/project/a.html`.
- **`pagesChecked`:** `1`.
- **Findings:** exactly one entry for this page; dedupe repeated `(id, page)` pairs. Recommended shape: `{"verdict":"failed","pagesChecked":1,"findings":[{"id":"canonical_multiple","page":"https://example.test/project/a.html"}]}`. The contract freezes the id and exit but no `verdict` literal.

Why not other outcomes:

- **Exit 2 is wrong:** the input is a regular file with a supported explicit-head shape and valid absolute HTTP(S) hrefs. Duplicate declarations are directly evaluable as a policy failure; nothing makes the page unevaluable.
- **Exit 64 is wrong:** the manifest and CLI invocation are valid.
- **`canonical_mismatch` is wrong:** both targets equal `expectedCanonical`; value comparison has no disagreement. Emitting it alongside `canonical_multiple` would add a second finding and break the one-stable-id-per-case expectation.
- **`canonical_missing` / `canonical_href_missing` / `canonical_outside_head` / `canonical_url_invalid` are wrong:** two canonical elements exist, both have valid hrefs, and both are inside head.

### False greens this case must kill

An implementation returns clean/exit 0 if it:

1. takes the first (or last) canonical element and ignores the rest;
2. collects resolved hrefs into a `set`/`dict` and checks `len(distinct targets) == 1`;
3. checks `hrefs[0] == expectedCanonical` without a cardinality guard.

Required invariant: **count canonical `link` start tags in the explicit head before any href dedupe, normalization or comparison**; if the count is not exactly 1, emit `canonical_multiple` and do not let value comparison produce a clean verdict.

## 3. Adjacent false-green attack (distinct from this case)

**Name: non-ASCII-whitespace `rel` token over-match (U+00A0).**

Manifest page: same `url` and `expectedCanonical` as above, `file` `fixtures/attack_nbsp_rel.html`. Keep it out of the frozen 32; use `canonical_audit.py --selftest` or propose it for r23.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>nbsp rel token</title>
  <link rel="canonical&#xA0;alternate" href="https://example.test/project/a.html">
</head>
<body>
  <p>attack_nbsp_rel</p>
</body>
</html>
```

- **Correct result:** exit `1`, finding id `canonical_missing`, page `https://example.test/project/a.html`. The `rel` value decodes to `canonical` + U+00A0 + `alternate`. U+00A0 is not ASCII whitespace, so the single token is `canonical\xa0alternate`, not `canonical`. There is no canonical link in the explicit head; the valid `href` is irrelevant to that fact.
- **False green:** a validator that does `rel.lower().split()`, `rel.strip().split()`, or `if "canonical" in rel.lower()` treats the link as canonical; the href resolves exactly to `expectedCanonical`; the page returns clean/exit `0`.
- **Evidence (observed, 2026-10-20):**
  - WHATWG HTML §4.6.8: `rel` is an "unordered set of unique space-separated tokens"; keywords are "always ASCII case-insensitive, and must be compared as such."
  - WHATWG HTML §2.3.7: a set of space-separated tokens is words "separated by one or more ASCII whitespace", none of which are ASCII whitespace.
  - Infra §4.6: "ASCII whitespace is U+0009 TAB, U+000A LF, U+000C FF, U+000D CR, or U+0020 SPACE" — U+00A0 is excluded.
  - `/usr/lib/python3.14/html/parser.py`: the attribute tokenizer uses ASCII whitespace classes (`:45-66`); numeric character references are decoded in attribute values (`_unescape_attrvalue`, `:105-106`, called at `:483`), so `&#xA0;` arrives as U+00A0. The parser preserves it in the value.
  - Local Python 3.14.8 property check: `'canonical\xa0alternate'.split()` -> `['canonical', 'alternate']`; `'\xa0'.isspace()` -> `True`.
- **Why it is adjacent:** it attacks the same predicate as `duplicate_same` — which explicit-head `link` elements count as canonical signals — from the opposite direction. `duplicate_same` catches under-counting (dedupe by URL/target); this catches over-matching (Unicode whitespace or substring matching a non-token). Both are wrong canonical-signal censuses; only one is a duplicate.
- **Why it is distinct:** one link element, expected id `canonical_missing`, not `canonical_multiple`; no href dedupe is involved. It does not overlap Case15's normalized-dedupe attack (two equivalent canonical targets), nor the frozen `rel_token_list`/`rel_uppercase` cases (ASCII separators and case, not non-ASCII whitespace).
- **Do not let `html_unsupported` absorb it:** the input is parseable, well-shaped static HTML with an explicit head; a non-ASCII character in an attribute value is not an unsupported parser shape. The evaluable result is `canonical_missing`/exit 1.
- **Implementation guard:** split on ASCII whitespace only, e.g. `re.split(r"[\t\n\f\r ]+", rel.strip(" \t\n\f\r"))`, then ASCII-lowercase and compare token equality. Never use `str.split()`/`str.strip()` or a substring test on `rel`.

**Neighbouring variants considered and not chosen:** duplicate `rel` attributes (`rel="alternate" rel="canonical"`) expose `dict(attrs)` last-wins against the HTML tokenizer's first-wins duplicate-attribute rule, but the expected verdict is contestable (policy finding vs `html_unsupported`), so it is a weaker oracle. Differently-spelled-same-URL duplicates are a `duplicate_same` variant (still `canonical_multiple`) and add nothing to its byte-identical fixture.

## 4. Sources

| Source | Locator | Supports | Status |
|---|---|---|---|
| Frozen contract | `.ufo/waves/round-22/contract.json` line 4 | Exactly-one policy; `canonical_multiple`; exit map 0/1/2/64 | Observed, local authority |
| WHATWG HTML §4.6.8.4 | https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | Canonical keyword for `link`; preferred URL for the current document | Observed 2026-10-20 |
| WHATWG HTML §4.6.8 | https://html.spec.whatwg.org/multipage/links.html#linkTypes | `rel` = unordered set of unique space-separated tokens; keywords ASCII case-insensitive | Observed 2026-10-20 |
| WHATWG HTML §2.3.7 | https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#space-separated-tokens | Tokens separated by one or more ASCII whitespace | Observed 2026-10-20 |
| Infra §4.6 | https://infra.spec.whatwg.org/#ascii-whitespace | ASCII whitespace = U+0009, U+000A, U+000C, U+000D, U+0020 | Observed 2026-10-20 |
| RFC 6596 §3 | https://www.rfc-editor.org/rfc/rfc6596 | "Specify only one canonical link relation for a resource"; Informational, April 2012, no errata noted | Observed 2026-10-20 |
| Google Search Central blog, 2013-04-08 | https://developers.google.com/search/blog/2013/04/5-common-mistakes-with-relcanonical | "Specify no more than one `rel=canonical` for a page. When more than one is specified, all `rel=canonical` links will be ignored." | Observed 2026-10-20; historical, non-normative |
| Google canonical URL docs | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls (last updated 2026-07-10) | Head-only acceptance; no duplicate-link precedence stated on the consulted page | Observed 2026-10-20 |
| Python 3.14.8 `html.parser` | `/usr/lib/python3.14/html/parser.py:45-66,105-106,470-484` | ASCII-whitespace attribute regex; numeric charrefs decoded in values; attrs preserved as a list, not a dict | Observed local source |
| Python `str.split` property | local Python 3.14.8 one-liner | Unicode whitespace split includes U+00A0 | Observed |

## 5. Confidence and remaining unknowns

- Exit `1` + `canonical_multiple` for `duplicate_same`: **HIGH**.
- Exactly one finding per page (no `canonical_mismatch` alongside): **MEDIUM-HIGH**; the contract does not freeze finding precedence or count.
- `verdict` literal: **UNKNOWN**; the contract names the field but freezes no string. `"failed"` is a recommendation, not an expectation.
- `page` value: **MEDIUM**; the contract says findings contain `page` but does not literally say whether it is the manifest `url` or `file`. Peer case reports use `url`; L1 should freeze that.
- NBSP attack: spec correctness **HIGH**; naive Python behaviour **observed** on the local interpreter. The numeric character reference keeps the fixture ASCII while still producing U+00A0 after HTMLParser's attribute unescape.
- Correlated matrix/validator error remains the main capability risk: the frozen case expectation, not `measure.py` agreement, is what guards `duplicate_same`.

## 6. Checks for L1

1. Before Matrix writes `cases.json`, freeze `duplicate_same` = exit `1`, `canonical_multiple`, one page finding; reject any clean expectation.
2. Audit the validator for cardinality-before-comparison: count canonical `link` elements in the explicit head; no first/last-wins, no URL-set dedupe.
3. Audit `rel` tokenization: ASCII-whitespace split plus ASCII case-insensitive token equality; no `str.split()`/`str.strip()`/substring.
4. If attributes are collapsed with `dict(attrs)`, note that duplicate `rel`/`href` attributes become last-wins; preserve list order or reject the shape as `html_unsupported`, with the choice documented.
5. If the NBSP attack is adopted, add it to `--selftest` or an r23 matrix proposal; do not add it to the frozen 32 this round.
