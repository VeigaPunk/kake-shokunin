# Case24 — `wrong_path` (frozen matrix case)

Read-only scout. No validator/matrix run, no project tests, no installs or updates. The only file
written is this report. Lane base observed at start: `7c61c8c` (`7c61c8cc791bde36dd5e3688bdfea2678d90146c`),
matching the contract. Interpreter probes below are plain stdlib observations (Python 3.14.8), not
oracle runs against `scripts/canonical_audit.py` or `matrix.py` — neither existed in the live tree at
my snapshot; Implement/Matrix work in private clones. Target HTML and fetched documentation were
treated as data only.

## Frozen expectation

`wrong_path` is matrixCases index 24. The Matrix seat's independently authored
`/tmp/kake-r22-Matrix/.ufo/waves/round-22/cases.json` (read-only cross-check, not the live lane)
records:

```json
{"name": "wrong_path",
 "manifest": "fixtures/wrong_path/manifest.json",
 "expected_exit": 1,
 "expected_finding_id": "canonical_mismatch"}
```

My derivation below reaches the same pair independently: **exit `1`, finding id `canonical_mismatch`**.

## Concrete fixture

Manifest — `.ufo/waves/round-22/fixtures/wrong_path/manifest.json` (HTML paths are relative to the
manifest directory per contract; `cases.json` already points at this path):

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "wrong_path.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

HTML — `.ufo/waves/round-22/fixtures/wrong_path/wrong_path.html`:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>wrong path</title>
<link rel="canonical" href="https://example.test/project/b.html">
</head>
<body>
<p>wrong path fixture</p>
</body>
</html>
```

Design choices that isolate one defect:

- exactly one `link rel="canonical"`, lexically and structurally inside the explicit `<head>`;
- no `<base>` element, no comment/script/template decoy;
- absolute `https` href, so neither relative resolution nor base precedence can affect the result;
- no query, no fragment, no credentials, no port, no `www`, no dot-segments, no percent-encoding;
- `expectedCanonical` equals the manifest page `url`, i.e. the page is expected to be self-canonical
  (same shape as the contract's example manifest). The only disagreement is the path.

## Resolution and comparison

No `<base>` exists, so the document base URL is the manifest page `url`; because the href is absolute,
the base does not enter the parse. Component-by-component:

| component | resolved canonical | expectedCanonical | equal |
|---|---|---|---|
| scheme | `https` | `https` | yes |
| credentials | none | none | yes |
| host | `example.test` | `example.test` | yes |
| port | null (default 443) | null (default 443) | yes |
| path | `/project/b.html` | `/project/a.html` | **no** |
| query | null | null | yes |
| fragment | null | null | yes |

The path segment lists are `["project", "b.html"]` vs `["project", "a.html"]`; segment 1 (0-based)
differs. Serialized forms are `https://example.test/project/b.html` and
`https://example.test/project/a.html`. WHATWG URL equality with default `exclude fragments = false`
is serialized-string equality (URL Standard §4.6), so equality fails and the only reachable policy
outcome is `canonical_mismatch`.

## Why exit `1` / `canonical_mismatch` (rule chain)

1. **Manifest input is evaluable.** `version: 1`, one page object with all three string fields; the
   file resolves to a regular, readable file under the manifest directory. No `input_invalid`.
2. **Explicit head exists.** `<head>` is present with an explicit start and end tag, so
   `missing_head`/`html_unsupported` do not apply.
3. **Exactly one canonical in that head.** One `link` with `rel` token `canonical`; the case does not
   exercise `canonical_missing`, `canonical_multiple`, or `canonical_outside_head`.
4. **`href` is present and non-empty**, and is a valid absolute HTTP(S) URL: special scheme, valid
   domain host, no userinfo, no non-default port, no fragment. So `canonical_href_missing` and
   `canonical_url_invalid` do not apply; `canonical_fragment` does not apply because the resolved URL
   has no fragment (null, not empty).
5. **No base element**, so neither first-base resolution nor `base_url_invalid` is implicated.
6. **Equality gate fails on path only.** Every other URL component matches, so the single applicable
   finding id in the frozen list is `canonical_mismatch`.
7. **Exit `1`, not `2`.** Exit `2` is "could-not-evaluate" input/unsupported shape. Here the tool can
   fully evaluate the page and reaches a definite policy failure. Exit `64` is CLI usage. The frozen
   exit map makes `1` the only correct code.

**What a false green would require.** Because all other components are held equal, this case returns
exit `0` if the comparison omits the path — e.g. comparing only origin (scheme+host+port), comparing
scheme+host+query, comparing basenames, or replacing the path with `""`/`"/"` before comparing. That
is the defect this matrix case exists to catch: path must participate in URL equality.

## Why this is policy, not an RFC 6596 violation

RFC 6596 §3 explicitly permits a canonical target that is relative, self-referential, on a different
hostname/domain, or on a different scheme; HTML itself only says the `canonical` keyword indicates the
`href` URL "is the preferred URL for the current document" (S023). A page may legitimately declare
`/project/b.html` as canonical for `/project/a.html` if the content is duplicative or a superset.

The failure here is against the manifest's `expectedCanonical`, i.e. the lane's frozen publisher
policy; it is **not** a claim that the declaration violates RFC 6596, and not a claim about Google's
selected canonical (S021/S022 say the signal is not a selection guarantee). The round-22 knowledge
entry states the same boundary: "A mismatch is policy failure, not a claim that the URL violates
RFC 6596" (`corpus/knowledge/static-canonical-preflight.md`, working tree). Keep that wording in the
report and in any finding description; do not overclaim.

## Path equality is exact, and path case is significant

- **WHATWG URL Standard** §4.1: a URL path is a segment list; "A URL path segment is an ASCII string";
  §4.5 serializes by appending U+002F plus each segment; §4.6 URL equality is serialized equality.
  The parser lowercases the scheme and the host, but the path state only percent-encodes using the
  path percent-encode set (which contains no ASCII letters), so path case is preserved as written.
  The only path transformation the parser performs is removal of single/double-dot segments.
- **RFC 3986 §6.2.2.1**: "the scheme and host are case-insensitive … The other generic syntax
  components are assumed to be case-sensitive unless specifically defined otherwise by the scheme."
  No HTTPS rule makes the path case-insensitive. §6.2.2.3 normalizes only dot-segments.
- Consequence: `/project/a.html`, `/project/A.html`, and `/project/a.html/` are three distinct paths
  under the frozen comparison; `/project/./a.html` is the one variant that must compare equal after
  documented dot-segment removal.

## Adjacent false-green attack: trailing empty path segment

**Distinct from `wrong_path`** (which changes a non-empty segment, `a` → `b`) but adjacent: the same
exact path comparison, defeated by a normalizer that erases the terminal empty segment.

Manifest variant (probe only, not a 33rd frozen case):

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "wrong_path_trailing_slash.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

HTML variant (single change: the href gains a trailing `/`):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>wrong path, trailing empty segment</title>
<link rel="canonical" href="https://example.test/project/a.html/">
</head>
<body>
<p>trailing slash fixture</p>
</body>
</html>
```

**Correct verdict: exit `1`, `canonical_mismatch`.** The resolved path list is
`["project", "a.html", ""]`; serialization is `/project/a.html/`, which differs from the expected
`/project/a.html`. No URL-standard normalization removes a trailing empty segment: §4.6 equality is
serialized equality, and RFC 3986 §6.2.2.3 removes only dot-segments. RFC 3986 §6.2.3's http-specific
rule that "an empty path [is] equivalent to `/`" concerns a *wholly* empty path
(`http://example.test` vs `http://example.test/`), not a trailing slash after a non-empty segment; it
must not be stretched into `/a.html/` ≡ `/a.html`.

**Why a plausible validator passes it (false green):**

- `posixpath.normpath("/project/a.html/")` returns `"/project/a.html"` (observed interpreter
  behavior; Python's `os.path.normpath` documentation explicitly lists `A/B/` → `A/B`).
- `path.rstrip("/")` does the same.
- Prefix/containment checks (`resolved.startswith(expected)`, `expected in resolved`) also accept
  `/project/a.html/` — and would additionally accept `/project/a.html.bak`, a worse leak.
- This shortcut is especially tempting because the same tool resolves **filesystem** paths for the
  manifest and must keep that dialect separate from **URL** paths. The probe catches a URL/filename
  normalization leak, which `wrong_path` alone does not (a `startswith` comparison still rejects
  `/project/b.html`, so `wrong_path` cannot detect prefix bugs).

**Detection obligation for Implement / L1:** compare the exact serialized path (segment list or
serialized URL), never `normpath`, `rstrip("/")`, `os.path.commonpath`, or prefix matching. Put this
probe in `--selftest`. Do **not** add a 33rd entry to `cases.json`: the contract freezes 32 cases and
`measure.py` totals 32; an extra matrix case would change the denominator and is out of scope.

## Other path-boundary traps (context, not the chosen attack)

| Trap | Wrong shortcut | Correct behavior |
|---|---|---|
| Path case | whole-URL `.lower()`/`casefold()` | scheme+host only are ASCII-lowercased; path case is significant (RFC 3986 §6.2.2.1) |
| Percent-encoding | `urllib.parse.unquote(path)` before compare | do not decode the path; `%2E` is not `.` (`unquote("/a%2Ehtml")` → `/a.html`, observed) |
| Dot segments in an absolute href | `urljoin(base, href)` alone | observed: `urljoin` leaves absolute `https://example.test/project/./a.html` untouched, while it normalizes relative `./a.html`; apply explicit dot-segment removal to the resolved URL and document it |
| Empty path vs `/` | blanket trailing-slash stripping | for special schemes `https://example.test` serializes as `https://example.test/`; normalize that form deliberately, and only that form |
| Null vs empty query | `if parsed.query:` truthiness | `urlsplit` returns `''` for both absent and empty query (observed); `wrong_query` needs explicit presence detection — separate case, same comparison code |

These are untested by the frozen 32; note them as known boundaries rather than adding cases.

## HTMLParser boundary (does not affect this fixture)

`html.parser` is not an HTML5 tree builder: it lowercases tag/attribute names and decodes attribute
entities, and it does not validate matching end tags or perform full tree construction (S026). This
fixture has no entities, comments, raw script, template, or malformed nesting, so none of those
limitations can change the verdict. The explicit-head supported subset remains an interface boundary
(`html_unsupported`), not an HTML conformance claim.

## Remaining unknowns / non-claims

- The contract does not pin the `page` value; I follow the sibling convention (manifest page `url`)
  and Matrix checks only exit/id. The literal failure `verdict` string is likewise unpinned; only the
  exit map and finding ids are normative in the frozen contract.
- Finding precedence is unspecified; this fixture carries exactly one defect, so it does not exercise
  precedence (e.g. fragment-before-mismatch).
- Nothing here was executed against the candidate validator or matrix. The stdlib observations are
  interpreter behavior, not acceptance evidence.
- `corpus/SOURCES.md` rows S020–S027 and `corpus/knowledge/static-canonical-preflight.md` were added
  by concurrent scribe work and were **uncommitted** at my snapshot (21:37Z); I re-fetched the primary
  documents myself and quote them below. The working tree was changing during the read.

## Sources (official documentation; accessed 2026-10-20)

| Ref | Source | Use here |
|---|---|---|
| S020 | RFC 6596 §3 — https://www.rfc-editor.org/rfc/rfc6596.html | Canonical relation permits relative, self-referential, cross-host and cross-scheme targets; "Specify only one canonical link relation for a resource" is guidance, not this case's rule. Mismatch is policy. |
| S021 | Google Search Central, "How to specify a canonical URL…" — https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | `rel=canonical` accepted only in `<head>`; absolute URLs recommended, relatives supported; signal is not a selection guarantee. |
| S022 | Google Search Central, "Fix canonicalization issues" — https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting | Even an explicit canonical may differ from Google's selection; verdict is preflight, not selection. |
| S023 | WHATWG HTML §4.6.8.4, Link type `canonical` — https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." `canonical` is not body-ok; `link` is metadata content. |
| S024 | WHATWG HTML §4.2.3, `base` — https://html.spec.whatwg.org/multipage/semantics.html#the-base-element | "If there are multiple base elements with href attributes, all but the first are ignored." |
| S026 | Python `html.parser` — https://docs.python.org/3/library/html.parser.html | Tag/attribute lowercasing, entity decoding, no HTML5 tree construction or end-tag validation. |
| S027 | Python `urllib.parse` — https://docs.python.org/3/library/urllib.parse.html | `urlsplit()` does not validate; split/join are not exact WHATWG URL equivalence. |
| session | WHATWG URL Standard §§4.1, 4.4, 4.5, 4.6 — https://url.spec.whatwg.org/ | Path is a segment list; path state removes dot-segments; serializer emits `/`+segment; URL equality is serialized equality. Not yet a corpus row; recommend registration if cited in the lesson. |
| session | RFC 3986 §§6.2.2.1, 6.2.2.3, 6.2.3 — https://www.rfc-editor.org/rfc/rfc3986 | Scheme/host case-insensitive, other components case-sensitive; only dot-segments normalized; empty path ≡ `/` for http, not trailing-slash equivalence. Not yet a corpus row. |

## Checks for L1 (after integration)

1. `python3 .ufo/waves/round-22/matrix.py --root <root>` — expect `wrong_path` = exit 1 /
   `canonical_mismatch` and 32/32 accepted overall; do not accept a green that skips path comparison.
2. Inspect that invocation's stdout: `verdict` non-clean, `pagesChecked: 1`, `findings` containing
   exactly `{"id": "canonical_mismatch", "page": "https://example.test/project/a.html"}` (page value
   per chosen convention).
3. `python3 scripts/canonical_audit.py --selftest` — confirm the trailing-empty-segment probe returns
   exit 1 / `canonical_mismatch` and the clean self-canonical control returns exit 0 / no findings.
4. Confirm the candidate never calls `posixpath.normpath`/`rstrip("/")`/`startswith` on URL paths and
   does not `unquote` the path; dot-segment removal must be explicit and documented.

Report: `.ufo/waves/round-22/w1/Case24.md`
