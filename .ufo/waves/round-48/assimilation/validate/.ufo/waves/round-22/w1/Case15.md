# Case15 — `duplicate_different`

Seat: KakeR22.Case15 (scout, read-only). Lane base observed: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Contract read: `.ufo/waves/round-22/contract.json`. No tests run, no installs, no registry/corpus edits. The only file written is this report.

## Frozen rule being tested

Contract policy: "Exactly one canonical link in explicit head per page, rel ASCII case-insensitive token list; resolve href with first head base href or document URL; compare WHATWG-like HTTP(S) normalized absolute URL to expectedCanonical…".

`canonical_multiple` is a frozen finding id. The cardinality is over **`link` elements whose `rel` token set contains `canonical`**, in the explicit `<head>` — not over distinct resolved URLs. Evidence: the policy says "one canonical link", and `duplicate_same` is itself a matrix case, so equality of `href` cannot make a duplicate acceptable. Confidence: HIGH (contract wording); the `duplicate_same` pairing is HIGH by matrix composition, not by reading another seat's `cases.json`.

## Concrete fixture

Manifest entry:

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "fixtures/duplicate_different.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

`fixtures/duplicate_different.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>duplicate different</title>
  <link rel="canonical" href="https://example.test/project/a.html">
  <link rel="canonical" href="https://example.test/project/b.html">
</head>
<body>
  <p>duplicate_different</p>
</body>
</html>
```

- **URL (manifest):** `https://example.test/project/a.html` — this, not the fixture path, is the document URL used for resolution.
- **expectedCanonical:** `https://example.test/project/a.html`.
- **No `<base>`:** both hrefs are absolute, so resolution is independent of base parsing; this isolates the duplicate rule.
- **First href = expectedCanonical, second differs:** the first canonical matching is deliberate. A first-wins implementation would otherwise produce a false green.
- **Second href is same-origin, different path:** no scheme/host/query/fragment/credential confound. This is not `wrong_host`, `wrong_path`, or `wrong_query`; the only defect is a second declaration.
- Both links are in the explicit head; there is no comment/script/template decoy and no body link.

## Expected result

- **Exit:** `1` (failed policy).
- **Finding id:** `canonical_multiple`.
- **Page:** `https://example.test/project/a.html`.
- **Exactly one finding for this page.** Recommended JSON shape: `{"verdict":"failed","pagesChecked":1,"findings":[{"id":"canonical_multiple","page":"https://example.test/project/a.html"}]}`.

Why not other outcomes:

- **Exit 2 is wrong:** the fixture is evaluable — regular file, explicit head, valid absolute HTTP(S) hrefs, no fragment/credentials, no unsupported shape.
- **Exit 64 is wrong:** the manifest is valid and the CLI invocation is normal.
- **`canonical_mismatch` is wrong:** value comparison must not run, or must not be the reported id, while the declaration is ambiguous. Comparing an arbitrary element (first, last, or each) is unsound. Emitting both `canonical_multiple` and `canonical_mismatch` also breaks the matrix's one stable finding-id-per-case expectation.
- **`canonical_missing` / `canonical_href_missing` / `canonical_outside_head` are wrong:** two canonical links exist, both have hrefs, both are inside head.

Why `canonical_multiple` is correct:

1. Two `link` elements carry the `canonical` token. That alone violates "exactly one canonical link"; the href comparison is downstream and cannot rescue the page.
2. RFC 6596 §3 administrator guidance says to "Specify only one canonical link relation for a resource. (It would be confusing to consider/label/designate more than one IRI as authoritative.)" This is guidance ("ought"), not a MUST; the hard-fail is the local contract, so the finding id must stay policy-scoped and must not claim RFC non-conformance. [Observed: RFC Editor, accessed 2026-10-20.]
3. Google Search Central's canonical-URL page states no duplicate-`link` precedence; its head-only rule is about placement, not multiplicity. Duplicate rejection is therefore the contract's choice, not a Google-sourced rule. [Observed via the wave's already-available `GoogleCanonical.md`; peer quote, not independently re-fetched.]
4. `html.parser` is a tokenizer, not a tree builder, and emits both `link` start tags; it does not deduplicate elements or attributes. The implementation must count observed canonical link elements. There is no parser-level excuse for first-wins or href-keyed collapse. [Observed via the wave's already-available `PythonParser.md`; official Python docs URL/access date recorded there.]

## Adjacent false-green attack (distinct from this case)

**Name:** normalized-dedupe collapse.

Same manifest (`url` and `expectedCanonical` = `https://example.test/project/a.html`), fixture body:

```html
<!doctype html>
<html lang="en">
<head>
  <link rel="canonical" href="https://example.test/project/a.html">
  <link rel="canonical" href="https://example.test/project/./a.html">
</head>
<body></body>
</html>
```

- **Correct result:** exit `1`, finding id `canonical_multiple` (two link elements).
- **False green:** an implementation that collects canonical targets into a `set`/dict keyed by the *resolved, normalized* URL sees one value, treats the page as having one canonical, and returns clean/exit `0`. The two raw hrefs are textually different, so exact-string deduplication would not collapse them; only "count distinct normalized targets" does.
- **Why it is distinct from this case:** `duplicate_different` has two hrefs that remain different after normalization (`/project/a.html` vs `/project/b.html`), so a normalized-value count still sees two and fails. The attack requires two spellings that normalize to one serialization; it tests element cardinality, not value difference. It is also distinct from `duplicate_same` as a fixture if that case uses byte-identical hrefs: exact-string dedupe catches byte-identical, but not dot-segment-equivalent spellings.
- **Source basis:** the WHATWG URL Standard defines path shortening/dot-segment handling and the `https` default port as 443; `https://example.test/project/./a.html` and `https://example.test/project/a.html` share one serialization. The equivalence itself is [INFERENCE] from those URL parser rules, not a quoted sentence about canonical links. The element-count rule is the contract's, and RFC 6596's single-relation guidance supports treating multiple declarations as a defect even when they denote the same target.
- **Placement:** the 32-case matrix is frozen, so do not silently add this as a 33rd case. Put it in `canonical_audit.py --selftest` (when Implement's script permits), or propose it as an r23 matrix case. Expected id/exit are already frozen-compatible: `canonical_multiple` / `1`.

## Sources and availability

| Source | Locator | What it supports | Status |
|---|---|---|---|
| Frozen contract | `.ufo/waves/round-22/contract.json` line 4 | Policy cardinality, finding ids, exit map | Observed, local authority |
| RFC 6596, §3 | https://www.rfc-editor.org/rfc/rfc6596.html, accessed 2026-10-20 | "Specify only one canonical link relation for a resource…" — guidance, not MUST; applications may ignore improper declarations | Observed (fetched by this seat); Informational, no errata noted in wave report |
| Google Search Central, consolidate duplicate URLs | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls, accessed 2026-10-20 per wave report | Head-only acceptance of the link element; no duplicate-link precedence; absolute-URL recommendation | Observed via already-available `.ufo/waves/round-22/w1/GoogleCanonical.md` (peer; not re-fetched here) |
| WHATWG HTML Standard, §4.6.8.4 | https://html.spec.whatwg.org/multipage/links.html#link-type-canonical, accessed 2026-10-20 | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." Defers behavior to RFC 6596; no multiplicity algorithm | Observed (fetched by this seat) |
| WHATWG URL Standard | https://url.spec.whatwg.org/, accessed 2026-10-20 | Special-scheme default ports (`https` 443), path shortening/dot segments; basis for the adjacent attack's normalized equivalence | Observed for the port table and path-shortening text; equivalence [INFERENCE] |
| Python `html.parser` docs | https://docs.python.org/3/library/html.parser.html, accessed 2026-10-20 per wave report | Tokenizer, not tree builder; both canonical link start tags are delivered; no attribute dedupe | Observed via already-available `.ufo/waves/round-22/w1/PythonParser.md` (peer; not re-fetched here) |

## Confidence and remaining unknowns

- Expected exit `1` / id `canonical_multiple`: HIGH.
- Exactly one finding per page (no `canonical_mismatch` alongside): MEDIUM-HIGH. The contract defines the finding-id set but not precedence/multiplicity; L1 should freeze "cardinality error suppresses value comparison" so Implement and Matrix cannot diverge.
- Verdict string: UNKNOWN. The contract names a `verdict` field but freezes no literal; `"failed"` above is a recommendation, while exit `1` and `canonical_multiple` are the binding expectations.
- `duplicate_same` expected id: not read from another seat's artifacts (independence preserved). Inferred: same as this case, because the policy counts elements.
- Google's own duplicate handling/precedence: not stated on the consulted page; no claim made. This report does not assert Google's selected canonical or any indexing outcome.
