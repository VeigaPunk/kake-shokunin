# URLNormalization — r22 canonical preflight review

**Axis:** operability. **Scope:** URL resolution, normalization, and comparison only. **Review status:** design-risk review; no implementation behavior is confirmed.

## Review basis and limits

The frozen contract is `.ufo/waves/round-22/contract.json` (C1; interface, finding IDs, and cases). The observed tracked diff from base `7c61c8cc791bde36dd5e3688bdfea2678d90146c` adds the r22 quality-bar section to `corpus/QUALITY.md`; it contains no normalizer implementation change. At review time `scripts/canonical_audit.py` was absent (the lane's `scripts/` listing contains only `corpus-contract.mjs`, `freshness-sweep.mjs`, and `probe-delta.mjs`). Therefore there is no implementation to call a defect in, and no result here claims any code or matrix case passes.

The LSP device is unavailable in this environment (`xd://lsp` returned “No such tool”); references, definition, and diagnostics were not available. No tests were run, as requested. The analysis below is a finite falsification target for the implementation once it is present, not test evidence.

## Concrete false-green / false-red risks to falsify

These are conditional risks, not observed implementation bugs.

1. **P1 — query or escaped path data is lost/rewritten before comparison.** The contract explicitly requires query preservation and has `query_preserved` / `wrong_query`; silently dropping a query, sorting parameters, decoding `%26` into `&`, or decoding `%2F` into `/` can turn a different declared URL into a clean match. A valid but different URL must produce exit `1`, `canonical_mismatch`; never compare only scheme/host/path or a decoded query/path. Keep URL components as URL components—do not parse query form data and reconstruct it.

2. **P1 — fragments and credentials are accepted after normalization.** The frozen policy rejects both. In particular, `href="/project/a.html#"` has a fragment delimiter but an empty fragment value; an implementation that only tests whether a parsed fragment string is truthy can falsely accept it. It must report exit `1`, `canonical_fragment`. `href="https://user@example.test/project/a.html"` must not match even if the expected URL is written with the same credentials; report exit `1`, `canonical_url_invalid`. A disallowed scheme such as `javascript:` or `data:` likewise maps to `canonical_url_invalid`, not a mismatching or clean HTTP(S) URL.

3. **P2 — present empty href is accepted as a resolvable reference.** The HTML Standard requires a present `link[href]` value to be a valid non-empty URL potentially surrounded by spaces. `href=""` is non-conforming even though parsing an empty relative reference alone can resolve to the base. Recommended mapping: `href_empty` exits `1` with `canonical_url_invalid`, because the attribute is present but its URL value violates the non-empty requirement; an absent attribute exits `1` with `canonical_href_missing`. Preserve HTMLParser's distinction (`None` versus `''`) and validate non-emptiness before URL resolution.

4. **P2 — resolution uses the wrong base or retries after a bad first base.** The contract names the first head `<base href>` and explicitly includes `first_base`, `second_base_ignored`, and `base_invalid`. Resolve a relative first base against the manifest page URL, then resolve the canonical reference against that result; ignore subsequent base elements. If the first base is invalid, do not silently skip it in favor of the second base or page URL: report `base_url_invalid` (policy failure, exit `1`).

5. **P2 — “WHATWG-like” drifts into raw-string or RFC-only equality.** The policy requires normalized HTTP(S) absolute URL comparison, not string comparison. Check that scheme/host case, default HTTP(S) ports, and dot segments normalize consistently (for example, `HTTPS://EXAMPLE.TEST:443/project/a/../a.html` and `https://example.test/project/a.html`); preserve case-sensitive path distinctions and escaped reserved path/query data. The URL Standard is explicit that parsing, serialization, and equality/canonicalization are algorithmic; a bare `urljoin`/`urlsplit` round trip is not evidence of WHATWG behavior. Conversely, do not claim full WHATWG conformance from a limited stdlib profile: define the accepted/rejected subset and ensure malformed/non-HTTP(S) values fail with `canonical_url_invalid` rather than being “repaired” into a clean match.

## Expected stable IDs for the normalization slice

From the frozen contract's `findingIds` and exit map:

| Case/input | Expected result |
|---|---|
| `absolute_match`, `relative_same_dir`, `relative_parent`, `root_relative`, `scheme_relative`, `first_base`, `second_base_ignored`, `query_preserved` when the resolved URL equals policy | Exit `0`, verdict clean, `findings: []` |
| `wrong_host`, `wrong_path`, `wrong_query` | Exit `1`, `canonical_mismatch` |
| `invalid_url`, `javascript_url`, `data_url` | Exit `1`, `canonical_url_invalid` |
| `fragment_url`, including a bare trailing `#` | Exit `1`, `canonical_fragment` |
| `base_invalid` | Exit `1`, `base_url_invalid` |
| `href_absent` | Exit `1`, `canonical_href_missing` |
| `href_empty` | Exit `1`, `canonical_url_invalid` |
| manifest/file-resolution input failure (for example traversal or symlink HTML) | Exit `2`, `input_invalid` |

For clean output, the contract enumerates finding IDs only for failures; the validator JSON should have no synthetic `clean` finding. A separate matrix may use `clean` as its expected-case sentinel, but keep that sentinel out of `findings`.
The frozen contract names both `canonical_href_missing` and `canonical_url_invalid` but does not explicitly assign `href_empty`. `canonical_url_invalid` is the recommended stable ID for the present-but-empty value; L1 should freeze that mapping in the matrix and selftest. If the local policy instead groups empty and absent under `canonical_href_missing`, it must use that one ID consistently. Either way, empty must fail, never clean.

## Minimum acceptance/rejection pair

Use the same manifest page URL, `https://example.test/project/a.html`, and expected canonical, `https://example.test/project/a.html?view=full&lang=en`:

- **Accept (`query_preserved`):** head contains `<link rel="canonical" href="?view=full&amp;lang=en">`. Expected: exit `0`, clean verdict, empty findings. This verifies relative-reference resolution plus one HTML-attribute entity decode and query retention.
- **Reject (`wrong_query`):** change only the href to `?view=full&amp;lang=fr`, leaving the expected canonical unchanged. Expected: exit `1`, finding ID `canonical_mismatch`. If this becomes clean, query comparison is lossy.

The `href_empty` expectation follows HTML's non-empty `link[href]` requirement, not an assumption that an empty URL reference is unresolvable.

## Bounded falsification recipe (not run)

After the auditor and frozen matrix land, use a temporary directory with only local HTML and manifest files; do not fetch URLs. Run the matrix once, then at most these seven one-page JSON invocations, asserting both exit and finding ID:

1. The acceptance member of the pair above: `0`, no findings.
2. The rejection member: `1`, `canonical_mismatch`.
3. Same host/path but `href` containing `#` and no fragment text: `1`, `canonical_fragment`.
4. Same host/path but with user-info: `1`, `canonical_url_invalid`.
5. First base `/v1/`, second base `/ignored/`, canonical href `a.html`, expected `/v1/a.html`: `0`, no findings; this falsifies later-base selection.
6. Malformed first base followed by a valid second base: `1`, `base_url_invalid`; this falsifies fallback to the later base.
7. Empty-string `href` on a canonical link, with expected canonical equal to the document/base URL: `1`, `canonical_url_invalid`; this falsifies accepting it merely because URL-reference resolution would return the base.

Treat any observed clean result in steps 2–4, 6, or 7 as a concrete false green; any mismatch in steps 1 or 5 as a false red. The frozen 32-case matrix remains the required coverage counter; this bounded supplement does not replace it.

## Source boundary

- Frozen local contract: `.ufo/waves/round-22/contract.json` (policy says WHATWG-like HTTP(S) normalization, preserves query, rejects fragments/credentials; IDs and matrix names are frozen there).
- WHATWG, [URL Standard](https://url.spec.whatwg.org/#concept-basic-url-parser) (Living Standard, last updated 2026-10-19; accessed 2026-10-20): parsing, serialization, and URL equivalence are defined by algorithms. This is the source for the normalization model, not proof that a Python stdlib implementation is equivalent.
- WHATWG HTML, [The `link` element](https://html.spec.whatwg.org/multipage/semantics.html#the-link-element) and [valid non-empty URL potentially surrounded by spaces](https://html.spec.whatwg.org/multipage/urls-and-fetching.html#valid-non-empty-url-potentially-surrounded-by-spaces) (accessed 2026-10-20): a present `link[href]` must be a valid non-empty URL after trimming ASCII whitespace. This distinguishes an empty present value (`canonical_url_invalid`) from a missing attribute (`canonical_href_missing`).
- `w1/GoogleCanonical.md` records that Google supports relative canonical URLs while recommending absolute ones; relativity alone must not be rejected as a Google requirement. It also bounds this tool as policy preflight rather than canonical-selection prediction.
- `w1/RFC6596.md` records relative IRIs as permitted; it does not define resolution/equality. Do not cite RFC 6596 as a URL-normalization algorithm.
