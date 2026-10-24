# Case22 — `fragment_url` (frozen matrix case)

Read-only scout. No tests/matrix/validator runs, no installs, no lane or jj writes. The only file
written is this report. Observed lane base before any work: `git rev-parse HEAD` =
`7c61c8cc791bde36dd5e3688bdfea2678d90146c`, matching the contract. Interpreter observed locally:
`Python 3.14.8`. Target content was treated as data; nothing in fetched pages was executed or obeyed.

## Contract rules this case adjudicates

From `.ufo/waves/round-22/contract.json` (frozen):

- Policy clause: "Exactly one canonical link in explicit head per page, rel ASCII case-insensitive
  token list; resolve href with first head base href or document URL; compare WHATWG-like HTTP(S)
  normalized absolute URL to expectedCanonical, preserve query, **reject fragments** and credentials."
- Exit map: `0` clean, `1` failed policy, `2` could-not-evaluate input/unsupported shape, `64`
  could-not-evaluate usage.
- Finding id list includes `canonical_fragment` and `canonical_mismatch` as distinct ids.

## Concrete fixture (single defect, no base, no query)

Manifest — `fixtures/fragment_url/manifest.json` (paths relative to the manifest directory,
per contract):

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "fragment_url.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

HTML — `fixtures/fragment_url/fragment_url.html` (explicit head, exactly one canonical link,
absolute href, no `<base>`, no decoys):

```html
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>fragment canonical</title>
<link rel="canonical" href="https://example.test/project/a.html#section-2">
</head>
<body>
<p>fragment canonical fixture</p>
</body>
</html>
```

## Expected result

- **exit `1`** (failed policy)
- **finding id `canonical_fragment`**
- **page** `https://example.test/project/a.html` (the manifest page `url`, not the href)
- stdout (shape per contract): a JSON object with `verdict` non-clean, `pagesChecked: 1`, and
  `findings` containing exactly `{"id": "canonical_fragment", "page": "https://example.test/project/a.html"}`.

The Matrix seat's frozen `cases.json` currently records the same pair for this case
(`expected_exit: 1`, `expected_finding_id: "canonical_fragment"`), independently reached; no conflict
to escalate.

## Why this is exit 1 / `canonical_fragment` (rule chain)

1. **One canonical link in explicit head.** The `<link rel="canonical">` is inside the explicit
   `<head>`, outside any comment/script/template. So `canonical_missing`, `canonical_multiple`, and
   `canonical_outside_head` do not apply.
2. **`href` present and non-empty.** So `canonical_href_missing` does not apply; this is not the
   `href_empty` shape.
3. **Absolute, valid HTTP(S) URL.** `https://example.test/project/a.html#section-2` parses as an
   absolute https URL with a host, no credentials, no bad scheme. So `invalid_url`,
   `canonical_url_invalid`, and scheme cases do not apply. No base element exists, and the href is
   absolute, so base resolution cannot perturb it (`base_url_invalid` not in play).
4. **Fragment gate fails.** The parsed URL has a non-empty fragment (`section-2`). The contract
   explicitly rejects fragments in the canonical target; the dedicated finding id is
   `canonical_fragment`.
5. **Exit 1, not 2.** Everything needed was evaluable: valid manifest, regular readable file, explicit
   head, one canonical link, valid href. Exit 2 is reserved for could-not-evaluate input/unsupported
   shape (e.g. missing head, unreadable/symlink/traversal); exit 64 is CLI usage. A definite policy
   violation is `1` by the frozen exit map.
6. **No `canonical_mismatch` for this fixture.** The fragment-stripped resolved target is exactly
   `expectedCanonical`, so the only defect is the fragment. Intended single-id semantics: the fragment
   rejection gate runs before/replaces the equality comparison, so the case yields one stable id.
   This precedence — and not additionally emitting `canonical_mismatch` — is a local-policy decision
   consistent with the frozen single `expected_finding_id`; the contract text does not spell out
   precedence. **[INFERENCE]**

If an implementation instead strips the fragment and compares, this fixture becomes a **false green**
(exit 0), which is precisely why the case is in the matrix: it forces fragment rejection to be a
separate gate on the resolved canonical target, not a normalization side effect. If an implementation
compares the fragment-bearing serialization it would emit `canonical_mismatch`; that id is wrong for
this case because the contract provides a dedicated fragment id.

Equivalent variants (same verdict, for matrix-build flexibility): relative `href="a.html#section-2"`
and fragment-only `href="#section-2"` both resolve to the same fragment-bearing document URL and must
also yield exit 1 / `canonical_fragment`. Keep the frozen fixture absolute so no base or relative
resolution is needed and the only defect is the fragment.

## Adjacent false-green attack: trailing empty fragment (`#`)

**Distinct from `fragment_url`** (which carries a non-empty fragment catchable by truthiness) yet
adjacent: the same `canonical_fragment` rule, defeated by the null-vs-empty fragment distinction.

Fixture variant:

```json
{"version": 1,
 "pages": [{"url": "https://example.test/project/a.html",
            "file": "empty_fragment.html",
            "expectedCanonical": "https://example.test/project/a.html"}]}
```

```html
<!doctype html>
<html><head>
<meta charset="utf-8">
<link rel="canonical" href="https://example.test/project/a.html#">
</head><body><p>empty fragment</p></body></html>
```

**Why a plausible validator passes it (false green).** Observed on the local Python 3.14.8 stdlib:

- `urljoin("https://example.test/project/a.html", "https://example.test/project/a.html#")` returns
  `"https://example.test/project/a.html#"` (the `#` survives resolution).
- `urlsplit("https://example.test/project/a.html#")` gives `fragment=''`, indistinguishable by value
  from a URL with no `#`; `urlsplit(...)` results for the two forms compare **equal**.
- `urlunsplit` drops the empty fragment, serializing to `"https://example.test/project/a.html"`.

So an implementation that checks `if parsed.fragment:` and/or compares `urlunsplit(parsed)` to the
normalized `expectedCanonical` emits **no finding and exits 0** — even though the href ends in `#`.

**Correct verdict under the frozen policy: exit `1`, `canonical_fragment`.**

- WHATWG URL Standard: a URL's fragment "is either null or an ASCII string … It is initially null";
  parsing U+0023 (`#`) sets it "to the empty string" (i.e. non-null). The serializer appends `#` when
  the fragment is non-null, and URL equivalence with the default `exclude fragments = false` treats
  `…a.html#` and `…a.html` as unequal.
- Google's canonical guidance bans a "URL fragment" with no non-empty carve-out, and the contract says
  "reject fragments" without one.
- **[INFERENCE]** Extending rejection to the zero-length fragment is a policy reading, not a direct
  Google statement; it is the strict reading and the only one consistent with treating `#` as present.
  L1 should freeze it explicitly (see below) because a validator cannot recover presence from a Python
  `SplitResult` after the fact.

**Detection obligation.** Check for fragment presence on the resolved URL before normalization —
e.g. the residual `#` in the resolved string (a literal `#` in a valid URL always begins the fragment;
`%23` is percent-encoded path/query data and must NOT count) or a parser that preserves null vs empty
fragment. Do not rely on `.fragment` truthiness or on `urlunsplit()` round-tripping. Note that
`urljoin` preserves the trailing `#`, so a pre-normalization presence check on the resolved href
works for both the non-empty and empty variants; the failure mode is normalizing/rebuilding first.

**Why not the entity-obfuscation variant.** `href="…a.html&#35;frag"` (a character reference for
`#`) survives to the audit already decoded: Python `html.parser` decodes character references in
attribute values regardless of `convert_charrefs` (values observed as `…a.html#frag`), and the contract
mandates HTMLParser-based parsing. It therefore collapses into `fragment_url` and adds nothing as a
separate attack; raw-regex attribute scanners are already out of policy, not merely untested.

## Sources (official documentation; access date 2026-10-20)

All fetched by this seat during this task; quotes verified in the fetched pages. Marked `[INFERENCE]`
where the claim is a policy mapping rather than source text.

1. **WHATWG HTML Living Standard, §4.6.8.4 "Link type `canonical`"**
   `https://html.spec.whatwg.org/multipage/links.html#link-type-canonical`
   Exact: "The canonical keyword indicates that URL given by the href attribute is the preferred URL
   for the current document." (The spec defers detail to RFC 6596; it does not itself ban fragments.)
   Use: establishes that the canonical target is the *document's* preferred URL; a fragment names a
   sub-resource within the document, so a fragment-bearing target is not that preferred URL.
   **[INFERENCE]** for the fragment framing.
2. **Google Search Central, "How to specify a canonical URL with rel="canonical" and other methods"**
   `https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls`
   Exact, "Best practices": "Don't specify a URL fragment as canonical, as Google generally doesn't
   support URL fragments."
   Use: direct authority for the frozen policy's "reject fragments" rule and the `canonical_fragment`
   finding. Also "The rel="canonical" link element is only accepted if it appears in the `<head>
   section`" (supports explicit-head scope) and "use absolute paths" (a recommendation, not a validity
   rule — the contract nevertheless accepts relative hrefs by resolving them).
3. **WHATWG URL Standard** `https://url.spec.whatwg.org/`
   - §4 URLs: "A URL's fragment is either null or an ASCII string … It is initially null."
   - §4.2/§4.3 parsing: on U+0023 (`#`), "set url's fragment to the empty string".
   - §4.5 URL serializing, step 6: "If exclude fragment is false and url's fragment is non-null, then
     append U+0023 (#), followed by url's fragment, to output."
   - §4.6 URL equivalence, default `exclude fragments = false`: serialized equality includes the
     fragment, so `…a.html` and `…a.html#` are not equal.
   Use: establishes that empty-after-`#` is still a present fragment and a distinct URL, grounding the
   empty-fragment attack. `[INFERENCE]` only for adopting strict rejection.
4. **RFC 6596, "The Canonical Link Relation"** `https://www.rfc-editor.org/rfc/rfc6596`
   Exact: "The target (canonical) IRI MUST identify content that is either duplicative or a superset
   of the content at the context (referring) IRI." Also "Specify only one canonical link relation for
   a resource."
   Use: canonical is a content-identity declaration; RFC 6596 is **silent** on fragments and on
   non-HTTP(S) schemes — do **not** cite it as the fragment ban. Consistent with sibling scout
   `RFC6596.md` (line 42 reads the same gap).
5. **Python `urllib.parse` documentation** (3.14/3.15 pages, fetched via `docs.python.org`): `urlsplit`
   "does not perform validation"; rebuilt URLs may drop empty components and be "a slightly different,
   but equivalent URL". Corroborated locally with Python 3.14.8 as observed behavior (not a project
   test run). Use: explains why the empty-fragment trap is easy to hit, and why `urlsplit` alone cannot
   be the validity oracle. Sibling `PythonURL.md` documents the same source and quotes.

## Guidance for L1 / matrix freeze

- Keep `fragment_url` as: manifest page `https://example.test/project/a.html`, absolute canonical href
  with non-empty fragment (`#section-2`), `expectedCanonical` fragmentless; `expected_exit: 1`,
  `expected_finding_id: "canonical_fragment"`; no `<base>`, no query, one link — isolates the defect.
- Freeze fragment handling as a gate on the **resolved** href (base applied where relative), before
  equality comparison; a fragment-bearing canonical yields `canonical_fragment` and no concurrent
  `canonical_mismatch`. The contract does not state precedence; this is the reading that makes the
  frozen single id deterministic. **[INFERENCE]**
- Decide explicitly whether a **zero-length** fragment (`href="…/a.html#"`) is a failure. Strict
  reading: yes, `canonical_fragment` (spec treats `#` as a present, empty fragment; policy has no
  carve-out). If L1 chooses otherwise, a validator must still not conflate absent with empty when
  normalizing; document the choice, because Python's `urlsplit` cannot distinguish them.
- Do not accept fragment-stripping normalization as sufficient: that is exactly the false green this
  case exists to catch.

## Remaining unknowns / non-claims

- The exact `verdict` string for failure is not fixed by the contract excerpt beyond the exit map; only
  exit and `id`/`page` are normative here.
- Precedence between multiple simultaneous policy failures is unspecified by the contract; this fixture
  deliberately has only one defect.
- Nothing here was executed against the matrix or validator (per assignment). Observed facts are the
  stdlib probes above and the fetched documentation; all policy extensions are labeled `[INFERENCE]`.

Report: `.ufo/waves/round-22/w1/Case22.md`
