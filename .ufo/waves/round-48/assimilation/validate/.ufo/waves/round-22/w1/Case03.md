# Case03 — `relative_parent`

Seat: `KakeR22.Case03`, read-only scout. Lane `kake-shokunin`, observed base `7c61c8cc791bde36dd5e3688bdfea2678d90146c` (matches the frozen contract). Contract read from `.ufo/waves/round-22/contract.json` (round 22, claim C1, matrix case 3 of 32). No tests run, no validator executed (none exists at this base), no installs or updates, no registry/corpus edits. The only file written is this report. Public spec/docs fetched read-only; target content was treated as data, never as instructions.

## Result

| Field | Value |
|---|---|
| Matrix case | `relative_parent` (positive control, case 3 of 32) |
| Manifest `url` | `https://example.test/project/sub/a.html` |
| Manifest `file` | `fixtures/relative_parent.html` (regular file, manifest-relative; the file path is not the URL) |
| `expectedCanonical` | `https://example.test/project/a.html` |
| Expected exit | **0** (`clean`) |
| Expected finding id | **none** — `findings: []`; no finding id applies |
| `pagesChecked` | `1` |
| Confidence in exit 0 / no finding | **HIGH** — contract policy plus URL resolution below; not a measured run |

The HTML bytes and file path are a recommended fixture shape. `url`, the href form `../a.html`, and `expectedCanonical` are load-bearing; Matrix may relocate the fixture file. The verdict literal `"clean"` is `[INFERENCE]` from the contract's exit map (see Remaining unknowns).

## Concrete fixture

Manifest entry (the harness may place this page in a shared manifest):

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/sub/a.html",
      "file": "fixtures/relative_parent.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

`fixtures/relative_parent.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>relative parent positive control</title>
<link rel="canonical" href="../a.html">
</head>
<body><p>relative_parent positive control</p></body>
</html>
```

Design constraints that keep this case single-axis:

- The page is a **file-style URL** two path levels deep (`/project/sub/a.html`), so the reference has a directory to climb out of and a real file segment to drop.
- Exactly one explicit `<head>`, one `link`, one canonical token. No `<base>`, no second link, no body link, no comment/script/template decoy, no fragment, no credentials, no query. `base`, token-list, case, entity, query and duplicate behavior belong to their own matrix cases.
- `expectedCanonical` is the absolute, already-normalized parent URL; it is **not** the page URL. RFC 6596 permits a canonical target that differs from the context IRI (self-reference is only one allowed shape), so this positive control also proves the validator does not invent a "canonical must equal page URL" rule. Content-level supersession is out of scope (contract limits: policy comparison, not publishing readiness).

### Fixture algebra (avoid a broken positive)

From a base path `/P/S/F`, the relative reference `../F` first drops `F` (directory semantics) and then drops `S`, yielding `/P/F`. Therefore:

- page `/project/sub/a.html` + href `../a.html` → `/project/a.html` (this fixture);
- page `/project/a.html` + href `../a.html` → `/a.html` — that would be a mismatch, not this positive;
- page `/project/sub/a.html` + href `../project/a.html` → `/project/project/a.html` — wrong href.

A directory-style page URL (`https://example.test/project/sub/`) with `../a.html` also yields `/project/a.html`, but the file-style page URL is recommended because it avoids ambiguity about whether the base path's last segment is a file or a directory.

## Resolution walkthrough (spec-derived, no experiment)

No head `<base>` exists, so the base for resolving the href is the document URL, `https://example.test/project/sub/a.html`. The contract fixes that offline model; the HTML Standard's fallback base URL is also the document's URL when no base element with `href` exists (S6).

1. **Relative state.** The URL parser clones the base URL's path, `["project","sub","a.html"]`, and because the input does not begin with `/`, `\`, `?`, `#` or EOF, sets the query to null and shortens the cloned path once, removing `a.html`: `["project","sub"]` (S1, S3).
2. **Path state, `..` segment.** The next segment is exactly `..`, a double-dot URL path segment. The parser shortens the path again, removing `sub`: `["project"]` (S2, S4).
3. **Path state, `a.html` segment.** The final segment is appended: `["project","a.html"]` (S2).
4. **Serialization and comparison.** Scheme `https`, host `example.test`, path `/project/a.html`, no credentials, no port, no query, no fragment. The serialized absolute URL is `https://example.test/project/a.html`, byte-identical to `expectedCanonical`. Equality holds.

The same result follows under RFC 3986 §5.2–5.2.4 (merge, then remove dot segments), so this fixture does not depend on the WHATWG-vs-RFC choice for the common `../` case. Sibling `RFC6596.md` independently records that `relative_same_dir`, `relative_parent`, `root_relative` and `scheme_relative` are valid declarations when they resolve to `expectedCanonical`.

## Expected exit 0 / no finding, and why

The contract policy requires: one canonical link in the explicit head; an ASCII case-insensitive `rel` token list; href resolution against the first head base or the document URL; an HTTP(S) normalized absolute comparison to `expectedCanonical`; query preservation; rejection of fragments and credentials (contract). Every predicate is satisfied:

- **Input is evaluable:** version-1 manifest, regular non-symlink fixture, no traversal; exit 2 and exit 64 are wrong.
- **One signal:** exactly one `link` whose `rel` token list contains `canonical`, inside the explicit head. `canonical_missing`, `canonical_multiple` and `canonical_outside_head` are wrong.
- **Href present and usable:** the href exists, is non-empty, and is a valid relative reference. A relative href is **not** an invalid URL: RFC 6596 §3 says the canonical target MAY "Specify a relative IRI" (S8). Emitting `canonical_url_invalid` or `canonical_href_missing` for this fixture would be a false red.
- **Resolved value equals the oracle:** after resolution, the normalized absolute URL is `https://example.test/project/a.html`, exactly `expectedCanonical`. `canonical_mismatch` is wrong.
- **No fragment/credential/query confound:** there is no `#`, no userinfo, and no query to preserve.

Binding expectation: **exit 0, `findings: []`, `pagesChecked: 1`**. The literal JSON `verdict` token is not frozen by the contract; `"clean"` is the natural reading of the exit map.

## Adjacent false-green attack (distinct from this case)

**Name:** `pct_encoded_parent_separator` — a parent-traversal canonical whose path separator is percent-encoded so it is **not** a `../` reference at all.

**Fixture** (same manifest `url` and `expectedCanonical` as the positive case):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>encoded parent separator attack probe</title>
<link rel="canonical" href="..%2Fa.html">
</head>
<body><p>attack probe, not part of the frozen 32-case matrix</p></body>
</html>
```

**Correct result:** exit **1**, finding id **`canonical_mismatch`**.

- `%2F` is a percent-encoded solidus inside a single path segment. It is not a path delimiter and does not create a `..` segment.
- The relative reference is one segment, `..%2Fa.html`. Relative state drops `a.html` from the base path, yielding `["project","sub"]`; path state does not match the buffer to a single-dot or double-dot segment, so it appends it: `["project","sub","..%2Fa.html"]`.
- Serialized result: `https://example.test/project/sub/..%2Fa.html`, which is not `https://example.test/project/a.html`.
- This is a value mismatch, not an invalid URL: the reference is well formed, so `canonical_url_invalid` is not the right id.

**False-green mechanism:** an implementation that percent-decodes the href before resolving it (for example `unquote(href)` and then `urljoin`) turns `..%2Fa.html` into `../a.html`, resolves it to `https://example.test/project/a.html`, and returns exit 0 with `findings: []`. The same false green appears if the implementation decodes the resolved URL and then applies dot-segment removal in a second normalization pass. A plain stdlib `urljoin` without an explicit unquote does not exhibit the bug, so this attack specifically probes a normalization layer that decodes for "friendlier" comparison.

**Why the decoded form is wrong under both models:**

- RFC 3986 §2.2: "URIs that differ in the replacement of a reserved character with its corresponding percent-encoded octet are not equivalent" and decoding a reserved character's octet "will change how the URI is interpreted by most applications" (S11). `/` is a gen-delim reserved character.
- RFC 3986 §2.4: components must be parsed and separated before percent-encoded octets are decoded, "as otherwise the data may be mistaken for component delimiters" (S11).
- WHATWG URL path state does not decode `%2F`; the parser preserves the percent triplet in the path and the serializer emits it (S1, S2). The conclusion that the serialized path retains `..%2Fa.html` is `[INFERENCE]` from the algorithm text, not an executed probe.

**Why it is distinct from this case:**

- `relative_parent` contains a literal `/` after `..` and must resolve to the expected parent and exit 0. The attack contains no literal `/` in the href, must remain one segment, and must exit 1.
- It is not the frozen `invalid_url` case (the reference is valid), not `wrong_path` (the failure is introduced by an incorrect decode, not by a visibly different path), and not `entity_href` (HTML entity decoding is correct and required; percent-decoding of reserved delimiters is not).
- No frozen matrix case **name** denotes percent-encoded path delimiters. If the frozen `fragment_url` or `wrong_path` fixtures happen to use percent-encoding, the overlap must be checked by Matrix; this attack's expected id is already frozen-compatible (`canonical_mismatch`, exit 1).

**Placement:** the 32-case matrix is frozen. Do not add this as a 33rd case. Add it to `scripts/canonical_audit.py --selftest` (as an adversarial check) or propose it for r23. A clean `relative_parent` plus this failing probe proves the resolver distinguishes a real dot segment from an encoded solidus.

**Alternative not selected:** a valid head `<base href="https://example.test/other/sub/">` combined with `../a.html` would also be falsely green if the implementation ignores `<base>` and resolves against the document URL (correct: `https://example.test/other/a.html`, `canonical_mismatch`, exit 1). It is not the named attack because it is the same base-application feature that `first_base` / `second_base_ignored` are meant to cover. If those frozen fixtures do not make the base change the resolved target, they cannot catch a base-ignoring implementation; L1 should verify their fixtures, and the base-hijack probe is a worthwhile selftest addition either way.

## Boundaries and limitations

- **Offline document-URL model:** the manifest `url` is the document URL for resolution. A real browser loading a local file would use a `file:` fallback base URL; the contract deliberately substitutes the manifest URL, so this is a local policy model, not browser navigation. `[INFERENCE]` only in the sense of mapping the contract's phrase "document URL" to the manifest field; the contract states the model.
- **Head-only base:** the contract says "first head base href"; the HTML Standard's document base URL uses the first descendant base element with `href` in tree order, which is normally in head (S6, S7). A body `<base>` is outside this contract's supported shape; it is a known contract/HTML divergence, not part of this case. This fixture has no base at all.
- **No content semantics:** the tool does not verify that the parent URL's content duplicates or is a superset of the page. RFC 6596's single MUST is content-level and cannot be established statically (S8); only the declared-URL policy is checked.
- **No network, JS, headers, redirects, or search-engine selection:** per contract limits. No server-side decoding of `%2F` is modeled; the attack is a static declaration mismatch, not a claim about what a particular host would serve.
- **Parser boundary:** Python `HTMLParser` is a tokenizer, not an HTML5 tree builder; the explicit-head supported subset is the contract's interface. This fixture is plain, well-formed markup, so no parser recovery behavior is exercised.

## Sources (official, fetched 2026-10-20 UTC)

| ID | Source and locator | Text used | Use |
|---|---|---|---|
| S1 | WHATWG URL Standard, §4.4 URL parsing, relative state, https://url.spec.whatwg.org/#relative-state (Living Standard last updated 19 Oct 2026) | "Set url's path to a clone of base's path" and "Shorten url's path" | Base-path drop before path state |
| S2 | Same, path state, https://url.spec.whatwg.org/#path-state | "If buffer is a double-dot URL path segment, then: Shorten url's path." | `..` removes the preceding segment |
| S3 | Same, §4.2 shorten a URL's path, https://url.spec.whatwg.org/#shorten-a-urls-path | "Remove path's last item, if any." | Dot-segment removal mechanics |
| S4 | Same, §4.1 double-dot URL path segment, https://url.spec.whatwg.org/#double-dot-path-segment | A double-dot segment is `..` or an ASCII case-insensitive match for `.%2e`, `%2e.`, `%2e%2e` | `..` qualifies; `..%2Fa.html` does not |
| S5 | WHATWG HTML Standard, §4.6.8.4 link type `canonical`, https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." | Canonical link semantics; deferred to RFC 6596 |
| S6 | WHATWG HTML Standard, §2.4.3 document base URLs, https://html.spec.whatwg.org/multipage/urls-and-fetching.html#document-base-url | "return the frozen base URL of the first such base element in tree order"; otherwise fallback base URL = document URL | Base precedence; no-base case |
| S7 | WHATWG HTML Standard, §4.2.3 base element, https://html.spec.whatwg.org/multipage/semantics.html#the-base-element | "If there are multiple base elements with href attributes, all but the first are ignored." | First-base rule; invalid base falls back to document URL |
| S8 | RFC 6596, §3, https://www.rfc-editor.org/rfc/rfc6596 | "Specify a relative IRI (see [RFC3986], Section 4.2)." plus cross-host/self-reference allowances and single-canonical guidance | Relative canonical is permitted; target may differ from page URL |
| S9 | Frozen contract, `.ufo/waves/round-22/contract.json` line 4 | Policy, exit map, finding ids, 32-case list, limits | Local authority for expected exit/id |
| S10 | Sibling wave reports `.ufo/waves/round-22/w1/RFC6596.md`, `HTMLBase.md`, `PythonURL.md` | Relative cases are valid when they resolve to `expectedCanonical`; first-base/fallback semantics; stdlib non-validation | Cross-check only; expectations above do not depend on their bytes |
| S11 | RFC 3986, §2.2 and §2.4, https://www.rfc-editor.org/rfc/rfc3986 | "URIs that differ in the replacement of a reserved character with its corresponding percent-encoded octet are not equivalent"; components must be separated before decoding | Percent-encoded solidus is data, not a delimiter |

## Remaining unknowns / explicit inferences

- **Positive-control classification:** the contract lists the 32 case names but no per-case expectations. `relative_parent` is read as a positive control because it sits in the leading resolution family (`absolute_match`, `relative_same_dir`, `relative_parent`, `root_relative`, `scheme_relative`), while `wrong_path`/`wrong_host`/`wrong_query` own the mismatch direction, and sibling `RFC6596.md` independently classifies it as valid when it resolves to `expectedCanonical`. Confidence HIGH; still `[INFERENCE]`, not a frozen per-case cell.
- **Verdict literal:** the contract's exit map says `0: "clean"` but freezes no JSON string. `"clean"` is `[INFERENCE]`; exit 0 and empty findings are contract-derived.
- **Clean-case id schema:** `cases.json` does not exist at this base. If the matrix schema requires an expected id for positives, use a clean sentinel (`null` or `"clean"`), never a finding id. `[INFERENCE]`; L1 should freeze this in the matrix schema.
- **Page field for findings:** not exercised here (no findings). For the attack, the `page` value is presumably the manifest URL, as recommended by sibling Case15; the contract only says each finding contains `id` and `page`. `[INFERENCE]`.
- **Matrix fixture literal:** the HTML, file path, and exact page URL are recommendations. The binding constraints are: page URL two levels deep, href exactly `../a.html`, no base, one canonical link in head, expectedCanonical the absolute parent URL. If Matrix chooses a self-canonical variant instead, the algebra changes (for example page `/project/a.html` with href `../project/a.html`); that is a different fixture and should be stated explicitly so the expected value is not inferred from the case name.
- **Validator behavior not observed:** `scripts/canonical_audit.py`, `cases.json`, `matrix.py` and `measure.py` were absent from the lane and tracked files at this base. This report specifies expectations only; it does not claim any fixture passes.
- **Percent-decoding conclusion:** the URL Standard algorithm text supports preservation of `%2F`, but no interpreter probe was run (per the read-only/no-tests instruction). The attack's expected mismatch is `[INFERENCE]` from S1/S2/S4/S11, with HIGH confidence because RFC 3986 independently forbids decoding reserved delimiters before component separation.

## Checks for L1 (not run by me)

1. When `cases.json` lands, confirm `relative_parent` is encoded as **exit 0 with no finding id** and uses a page URL deep enough that `../a.html` resolves to `expectedCanonical`; reject any expectation that maps it to `canonical_url_invalid` or `canonical_mismatch` (that would encode resolve-before-compare failure or an absolute-only rule).
2. Confirm the fixture has no `<base>`, no second canonical link, and no body link; those confounds belong to other cases.
3. Confirm the implementation resolves before comparing and does not require `expectedCanonical` to equal the page URL; RFC 6596 permits a non-self target.
4. Consider adding `pct_encoded_parent_separator` to `--selftest` (or r23): expected exit 1, `canonical_mismatch`. Confirm the implementation does not `unquote` reserved delimiters before path splitting or dot-segment removal.
5. If `first_base` / `second_base_ignored` fixtures use a base that does not change the resolved target, add a base-hijack selftest: page `/project/sub/a.html`, `<base href="https://example.test/other/sub/">`, canonical `../a.html` → resolved `https://example.test/other/a.html`, `canonical_mismatch`, exit 1, even though document-URL-only resolution would produce the expected URL.
6. Confirm no lane edits beyond this report were made by this seat.
