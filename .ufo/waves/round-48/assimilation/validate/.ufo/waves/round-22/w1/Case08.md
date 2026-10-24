# Case08 — `rel_token_list` (positive control: `rel` is a token list)

Seat: `KakeR22.Case08` (scout, read-only). Contract: `.ufo/waves/round-22/contract.json` @ lane `kake-shokunin`, base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Scope: analysis only. No code, fixtures, tests, builds, installs, registry/corpus edits, or git/jj writes. This report is the only file written.

## Verdict summary

| Field | Frozen expectation |
|---|---|
| Case kind | Positive control (clean page) |
| Page `url` | `https://example.test/project/a.html` |
| `expectedCanonical` | `https://example.test/project/a.html` |
| Expected exit | `0` |
| Expected finding id | none — `findings == []` |
| `pagesChecked` | `1` |

The contract's `findingIds` list is closed and contains no "ok" member. A clean case therefore has **no finding id**; if `cases.json` needs a scalar, freeze `null` (or a single frozen `clean` sentinel) — do not invent a new id.

## 1. Proposed frozen fixture (for the Matrix executor; not created by this seat)

`rel_token_list.html` — UTF-8, no BOM, LF line endings, one trailing newline:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>rel token list</title>
<link rel="alternate canonical" href="https://example.test/project/a.html">
</head>
<body>
<p>rel token list</p>
</body>
</html>
```

Manifest page record (`file` is resolved relative to the manifest's own directory; co-locate manifest and fixture):

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "rel_token_list.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

Expected stdout invariants (exit is the binding signal; the contract does not enumerate the verdict string, so freeze one token in `cases.json` at integration):

```json
{"verdict": "<clean>", "pagesChecked": 1, "findings": []}
```

Expected exit: `0`.

## 2. Why this must be clean — authority chain

1. **`rel` is a token list, not a string.** HTML Standard, §4.2.4 *The link element*, `rel` attribute: its value "must have a value that is a `unordered set of unique space-separated tokens`" (verbatim, including the spec's article). A single U+0020-separated pair is the minimal non-trivial instance of that grammar.
2. **Tokens become keywords by ASCII-whitespace splitting.** HTML Standard, §4.6.8 *Link types*: "To determine which link types apply to a `link`, `a`, `area`, or `form` element, the element's `rel` attribute must be split on ASCII whitespace. The resulting tokens are the keywords for the link types that apply to that element." Splitting `alternate canonical` yields exactly `["alternate", "canonical"]`; no token contains the other.
3. **Matching is per token and ASCII case-insensitive.** Same section: "Keywords are always ASCII case-insensitive, and must be compared as such. Thus, `rel="next"` is the same as `rel="NEXT"`." The lowercase fixture needs no case folding, keeping the case axis with `rel_uppercase` (Case09).
4. **ASCII whitespace is a five-code-point set.** Infra Standard, §4.6 / `#ascii-whitespace`: "ASCII whitespace is U+0009 TAB, U+000A LF, U+000C FF, U+000D CR, or U+0020 SPACE." The `#split-on-ascii-whitespace` algorithm skips leading/trailing ASCII whitespace and emits non-empty token runs only — so a well-formed token list can never yield an empty token here.
5. **`canonical` applies to `link` and creates a hyperlink.** HTML Standard, §4.6.8.4: "The `canonical` keyword may be used with `link` element. This keyword creates a hyperlink." and "The `canonical` keyword indicates that URL given by the `href` attribute is the preferred URL for the current document." The link here is a `link` element inside explicit `<head>`.
6. **Multiple keywords on one `link` are explicitly supported.** HTML Standard, §4.2.4: "One `link` element can create multiple links ... User agents must process the links on a per-link basis, not a per-element basis," with the worked example "if a single `link` element has a `rel` attribute with the value `next stylesheet`, it creates both a hyperlink ... and an external resource link ...". A validator may not treat `rel="alternate canonical"` as malformed, nor as two canonical links.
7. **Policy is satisfied exactly once.** Contract policy: "Exactly one canonical link in explicit head per page". Here exactly one `link` element has `canonical` in its token set; it is inside the explicit `<head>`; it has an `href`; the resolved absolute URL equals `expectedCanonical`.
8. **`alternate` is a safe second token.** It is a defined link type with a Hyperlink effect on `link` (§4.6.8 table), so the pair is a realistic document, not a synthetic unknown-keyword test.
9. **`canonical` is deliberately second.** The spec calls `rel` an unordered set; placing `canonical` after `alternate` makes the case discriminate order-sensitive logic (`split()[0]`, `startswith`) instead of only whole-string equality.
10. **URL comparison is isolated from normalization.** No `<base>` element, so the document URL is the base; the `href` is an absolute HTTP(S) URL that is already the WHATWG-serialized form of `expectedCanonical`: scheme `https`, host `example.test`, default port omitted, path `/project/a.html`, no query, no fragment, no credentials. Resolution/normalization is an identity operation, so a failure on this case can only come from the `rel` axis.

RFC 6596 §3 is consistent but not the tokenization authority: it permits relative and self-referential targets and says administrators "ought to" specify only one canonical relation; it says nothing about `rel` token lists. The token-list semantics above are HTML Standard/Infra language. (Sibling report `RFC6596.md` reaches the same scope split.)

## 3. What this case discriminates (false-red traps it must catch)

| Wrong implementation | Result on this fixture | Contract-correct result |
|---|---|---|
| `rel.strip().lower() == "canonical"` (whole-attribute equality) | `canonical_missing`, exit 1 | clean, exit 0 |
| `rel.split()[0].lower() == "canonical"` or `rel.lower().startswith("canonical")` (first token only) | `canonical_missing`, exit 1 | clean, exit 0 |
| Counting keywords/tokens or all links created by the element as "canonical links" | `canonical_multiple`, exit 1 | clean, exit 0 (one canonical-typed link) |
| Splitting on the literal U+0020 only (`rel.split(" ")`) | clean (this fixture has one space) — a coverage gap, not a discriminator; ASCII TAB/LF/FF/CR variants are untested by this case | clean |
| Substring/word-boundary matching, e.g. `"canonical" in rel` | clean by accident — see §4, where it becomes a false green | clean |

The second row is the reason the fixture uses `alternate canonical` and not `canonical alternate`. The third row is the reason the expected payload asserts `findings == []` rather than only exit 0: an element with two hyperlink keywords creates links for both keywords, but only one of them is the canonical link.

Related policy edge not exercised by this case (recommend freezing a rule at integration): `rel="canonical canonical"` duplicates the keyword, which HTML says "must not be specified more than once per `rel` attribute". No finding id exists for a duplicate keyword, and `canonical_multiple` should mean more than one canonical link, not a duplicated token on one element. Recommended behavior: deduplicate per-element tokens and stay clean. `[INFERENCE]` — policy gap, not a spec requirement of the contract.

## 4. Adjacent false-green attack (one): `rel_near_miss_token`

**Attack fixture** `rel_near_miss_token.html` (same URL and `expectedCanonical`; only the `rel` value changes):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>rel near-miss token</title>
<link rel="canonical-alternate" href="https://example.test/project/a.html">
</head>
<body>
<p>no canonical link</p>
</body>
</html>
```

Manifest page record: identical to §1 except `"file": "rel_near_miss_token.html"`.

| Outcome | Exit | Findings |
|---|---|---|
| Correct | `1` | `[{"id": "canonical_missing", "page": "https://example.test/project/a.html"}]` |
| Buggy (false green) | `0` | `[]` |

**Why it false-greens.** Any matcher that uses string containment rather than token equality accepts the single token `canonical-alternate` as if it contained a canonical keyword: `"canonical" in rel`, `re.search(r"\bcanonical\b", rel)`, or `rel.lower().startswith("canonical")`. The `href` is then compared and matches `expectedCanonical`, so the page reports clean even though it declares **no canonical link at all**. `\b` is especially dangerous here because `-` is a non-word character, so `\bcanonical\b` matches inside `canonical-alternate`.

**Why it is distinct from Case08.** Case08 is a positive control with a real canonical link (exit 0); this attack has no canonical link (exit 1 + `canonical_missing`). The two differ only in whether `canonical` is a whole ASCII-whitespace-delimited token. Case08 proves extra *valid* tokens are accepted; the attack proves a token that merely *contains* the keyword is not.

**Why it is adjacent.** Same element, same attribute, same `href`, same expected URL, same head position. The sole variable is the token boundary, i.e. the exact rule the Case08 fixture relies on.

**Spec basis.** HTML §4.6.8: the tokens split from `rel` *are* the keywords, and keywords are compared ASCII case-insensitively as keywords — `canonical-alternate` is a different token, not an alias of `canonical`. HTML §4.2.4: if `rel` is absent, has no keywords, or "none of the keywords used are allowed according to the definitions in this specification, then the element does not create any links"; an unknown keyword therefore creates no canonical link. RFC 8288 §2.1 ABNF (`reg-rel-type = LOALPHA *( LOALPHA / DIGIT / "." / "-" )`) shows a hyphenated relation type is syntactically well formed, so the fixture cannot be dismissed as `input_invalid` or `html_unsupported`; it is a valid document with an unknown link type and no canonical.

**Matrix gap.** The frozen 32-case list names only `rel_token_list`, `rel_uppercase`, and `attr_uppercase` on the `rel` axis; no near-miss/keyword-boundary case exists. Do **not** add it to the frozen matrix this round; run it as an adversarial probe in `--selftest` (or hold for r23) so a substring implementation cannot pass the matrix while green-lighting pages with no canonical.

**Why it matters for operability.** `rel_token_list` and this probe are a matched pair: together they pin "token membership" from both sides. A validator that passes Case08 via `"canonical" in rel` would also pass this attack, and the matrix alone would not reveal it.

## 5. Non-chosen variant worth keeping as a probe: non-ASCII whitespace

Python-specific hazard adjacent to the same split rule, observed on local CPython 3.14.8 (not the chosen attack):

- Fixture `rel="canonical&#160;alternate"` (U+00A0 NO-BREAK SPACE via numeric reference).
- `HTMLParser` decodes the attribute to `canonical\xa0alternate` (observed: `link {'rel': 'canonical\xa0alternate', ...}`).
- Infra ASCII whitespace excludes U+00A0, so the value is **one** token → no canonical keyword → contract-correct exit `1`, `canonical_missing`.
- Python `str.split()` with no argument splits on Unicode whitespace including U+00A0 (observed: `['canonical', 'alternate']`) → a membership check built on `.split()` false-greens the same way as §4.
- Negative result worth recording: `html.unescape('&#11;')` returns `''` on CPython 3.14.8 (U+000B is dropped, not preserved), so a vertical-tab fixture built from `&#11;` is not viable; use a literal byte or the NBSP form if this variant is ever frozen.

Keep this out of the frozen 32 unless L1 wants an explicit "ASCII whitespace, not Python whitespace" case; it is the same proof obligation as §4 and belongs in the adversarial probe set.

## 6. Observed vs inference

| Claim | Status |
|---|---|
| HTML/Infra/RFC quotes and section anchors in §2, §4 | Observed, fetched 2026-10-20 from `html.spec.whatwg.org`, `infra.spec.whatwg.org`, `rfc-editor.org` |
| `rel="alternate canonical"` must be clean under the contract's token-list policy | Observed contract text + spec derivation (high confidence) |
| `HTMLParser` preserves attribute-value case and decodes `&#160;`; `.split()` splits U+00A0 | Observed on local CPython 3.14.8 (one-line probes; no lane files touched) |
| `&#11;` is dropped by `html.unescape` | Observed on local CPython 3.14.8 |
| Duplicate-token rule (dedupe, stay clean) | `[INFERENCE]` policy gap; no finding id exists |
| Exact clean verdict string and `cases.json` scalar for a clean case | Unknown; contract does not enumerate them — freeze at integration |

## 7. Remaining unknowns (for L1 / Implement / Matrix)

1. Clean verdict token: contract names the field but not its vocabulary; `cases.json` and the validator must agree on one string.
2. `cases.json` representation of "positive id clean": `null`, omitted field, or a frozen sentinel.
3. Fixture manifest layout: whether the per-case manifest sits beside its HTML under `fixtures/` (recommended, keeps `file` a bare filename) or one aggregate manifest is generated.
4. `canonical_multiple` counting rule: distinct `link` elements carrying `canonical` vs links created per keyword. Recommended: count canonical-typed links, which equals the number of distinct elements for this keyword; the Case08 fixture still expects one.
5. Whether L1 ratifies the duplicate-token dedupe rule in §3.

## Sources

All fetched 2026-10-20 (UTC); official public documentation, no live property was probed.

- WHATWG HTML Standard, §4.2.4 *The link element*, `rel` attribute — https://html.spec.whatwg.org/multipage/semantics.html#attr-link-rel (quotes: "unordered set of unique space-separated tokens"; "One `link` element can create multiple links"; `next stylesheet` example).
- WHATWG HTML Standard, §4.6.8 *Link types* — https://html.spec.whatwg.org/multipage/links.html#linkTypes (quotes: split on ASCII whitespace; keywords ASCII case-insensitive; keyword not more than once per `rel`).
- WHATWG HTML Standard, §4.6.8.4 *Link type "canonical"* — https://html.spec.whatwg.org/multipage/links.html#link-type-canonical.
- WHATWG Infra Standard, `#ascii-whitespace` and `#split-on-ascii-whitespace` — https://infra.spec.whatwg.org/ (ASCII whitespace definition; split algorithm).
- RFC 6596, *The Canonical Link Relation*, §3 and §5 — https://www.rfc-editor.org/rfc/rfc6596.html#section-3 (relative/self-referential/cross-host target permissions; single-canonical guidance).
- RFC 8288, *Web Linking*, §2.1 — https://www.rfc-editor.org/rfc/rfc8288.html#section-2.1 (`reg-rel-type` ABNF; case-insensitive comparison).
- Local corroboration: sibling reports `HTMLLink.md`, `RFC6596.md`, `PythonParser.md` in this wave; local CPython 3.14.8 one-line probes recorded in §5.

Corpus note: `corpus/SOURCES.md` has no registered HTML/Infra/rel-token source (only an unopened Google canonicalization lead), so this report supplies fresh citations; no registry edits were made by this seat.

Report: `.ufo/waves/round-22/w1/Case08.md`
