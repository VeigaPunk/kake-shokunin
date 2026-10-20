# Case06 — `first_base` (matrix case 6 of 32)

Seat: `KakeR22.Case06` — read-only scout. No code, no tests, no lane/jj/git
writes; only this report is written. Lane observed at
`7c61c8cc791bde36dd5e3688bdfea2678d90146c` (matches contract base);
`scripts/canonical_audit.py` and `.ufo/waves/round-22/cases.json` do not exist
at that revision, so everything below is contract/spec-derived, not an
execution result. No installs were needed or made.

Reconciliation note (observed 2026-10-20 18:38): the Matrix seat's private
clone already froze `first_base` with document URL
`https://source.test/from/entry.html`; §2 records those observed bytes. My
earlier same-origin document URL (`https://example.test/docs/guide/page.html`)
is kept in §2 only as an equivalent alternative instantiation.

## 0. Answer in one table

| field | value |
|---|---|
| manifest `url` (document URL) | `https://source.test/from/entry.html` |
| head `<base href>` | `https://example.test/project/` |
| canonical `href` (raw) | `a.html` |
| document base URL (base step) | `https://example.test/project/` |
| resolved canonical | `https://example.test/project/a.html` |
| `expectedCanonical` | `https://example.test/project/a.html` |
| expected exit | **0** (`clean`) |
| expected case finding id | **`clean`** (positive sentinel, Matrix item: "positive id clean") |
| expected findings | `[]` |
| expected stdout shape | `{"verdict":"clean","pagesChecked":1,"findings":[]}` |

The page is a conforming positive control: a single document-level
`<base href>` in the explicit head, placed before the canonical link, changes
the meaning of a relative canonical `href` so that the resolved URL — not the
raw string, and not the document-URL resolution — equals `expectedCanonical`.

## 1. What this case must prove

`first_base` is the matrix's only positive control for "a `<base href>` in the
head establishes the base against which the canonical `href` is resolved". It
must fail three plausible shortcut implementations:

1. **Base ignored** — resolving `a.html` against the document URL
   (`https://source.test/from/entry.html` → `https://source.test/from/a.html`)
   instead of against the head base.
2. **Raw-string comparison** — comparing `"a.html"` to `expectedCanonical`
   instead of resolving first.
3. **Filesystem-relative resolution** — resolving `a.html` against the fixture
   file path or manifest directory instead of the manifest `url` plus the head
   base (the offline path is not the document base). The fixture must be built
   so any implementation that does not apply the head base produces a
   *different* URL (see §4), not the expected one.

It must NOT require base elements at all (absent base is a different case), and
it must not absorb multiplicity (that is `second_base_ignored`, Case07) or
malformed base (`base_invalid`). One base, one canonical link, one verdict.

## 2. Frozen fixture (concrete bytes)

Observed frozen instrument (the Matrix seat's private clone,
`/tmp/kake-r22-Matrix/.ufo/waves/round-22/`: `cases.json` written 18:38,
`fixtures/first_base/` 18:37; not landed in the lane at the frozen base). These
are the bytes L1 will reconcile against; the resolution spec below matches them
exactly.

`fixtures/first_base/manifest.json` (sha256
`e2c3e28d4a40075c62f254b104dd10940fe74f5784d27bf25606a3ac87cb23b1`):

```json
{"version":1,"pages":[{"url":"https://source.test/from/entry.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`fixtures/first_base/page.html` (134 bytes, sha256
`315f76a4c9b9ce5eb51ef85b1e75c58ee8051d952bb6d726bf2670b40fae6c51`):

```html
<!doctype html><html><head><base href="https://example.test/project/"><link rel="canonical" href="a.html"></head><body></body></html>
```

`file` is resolved relative to the manifest directory per contract
`fileResolution`; the fixture must be a regular file, not a symlink. Document
URL, base and href are as in §0; the resolved canonical is
`https://example.test/project/a.html`; exit 0, `clean`, stdout findings `[]`.

Why this construction is load-bearing — and stronger than a same-origin
variant: the document origin/path (`source.test/from/`) differs from the base
origin/path (`example.test/project/`), so every wrong base shortcut diverges
from the expectation:

- base ignored → `https://source.test/from/a.html` (document-URL merge);
- base path only, document origin retained → `https://source.test/project/a.html`;
- base ignored and raw href compared → `"a.html"` is not the expected URL.

The cross-origin base also exercises authority inheritance for a bare relative
reference (scheme/host come from the base, URL Standard relative state), which
a same-origin base would leave untested. It does **not** claim Case04's
falsifier: that attack needs a root-relative href (`/project/a.html`) so the
base authority replaces the document authority; here the href is path-relative,
so the authority-reset question is not asked.

Conformance notes: exactly one `<base href>`; it precedes the URL-taking
`<link>` (§4.2.3 ordering); explicit head; one canonical link with one rel
token and a present non-empty href; no comment/script/template decoys. A
minimal head without `<meta charset>`/`<title>` is allowed by the frozen
contract (it requires only an explicit head) and by HTML; do not add
requirements the contract does not state.

Equivalent same-origin instantiation (only for contexts that enforce Case04's
same-origin request strictly): manifest url
`https://example.test/docs/guide/page.html`, same HTML. Same
`expectedCanonical`, exit 0, `clean`; base-resolved
`https://example.test/project/a.html` vs document-resolved
`https://example.test/docs/guide/a.html`. Either instantiation satisfies the
§4 invariant; do not freeze both as separate cases.

Matrix handoff — use the observed schema, not the `expect_*` shape that earlier
case reports proposed:

```json
{"caseId":"first_base","manifest":"fixtures/first_base/manifest.json","expectedExit":0,"expectedFindings":["clean"],"rationale":"Local publisher policy: resolve the canonical through the first head base href."}
```

`expectedFindings:["clean"]` is the case-level positive sentinel; the tool's
stdout `findings` array must still be `[]` per contract, and `matrix.py` must
map the sentinel rather than expect a finding object with `id:"clean"`.

## 3. Why: normative resolution trace

Sources accessed 2026-10-20 (quotes verified against the fetched bytes; exact
anchors in §10).

1. **The base element sets the document base URL.**
   HTML Standard §4.2.3: "The base element allows authors to specify the
   document base URL for the purposes of parsing URLs…" A base's `href`, if
   present, "must contain a valid URL potentially surrounded by spaces." Our
   value is an absolute `https` URL, so it parses without error.
2. **The frozen base URL is computed against the document URL, not itself.**
   §4.2.3: the first base element with `href` in a document tree has a frozen
   base URL, set by "parsing the value of element's `href` content attribute
   with document's fallback base URL" — "Thus, the base element isn't affected
   by itself." Absolute input → unchanged:
   `https://example.test/project/`.
3. **Selection is first-in-tree-order.** §2.4.3 *Document base URLs*: "If
   document has a descendant base element that has an `href` attribute, then
   return the frozen base URL of the first such base element in tree order."
   Only one base exists, so there is no precedence question.
4. **The canonical link's `href` is parsed relative to that document base
   URL.** The URL Standard's basic URL parser takes the input "with an optional
   null or base URL base"; relative input `a.html` inherits scheme and authority
   from the base and merges paths. Base path `/project/` (trailing slash means
   "directory") + `a.html` → `/project/a.html`.
5. **Serialization is exactly the expected string.** URL serializer emits
   scheme, `//`, host, a non-null port only, then path. Result:
   `https://example.test/project/a.html` — lowercase scheme/host, no default
   port, no credentials, no query, no fragment. That is byte-identical to
   `expectedCanonical`.
6. **Canonical policy is satisfied.** HTML §4.6.8.4: "The canonical keyword
   indicates that URL given by the `href` attribute is the preferred URL for
   the current document." One explicit-head canonical; resolved target equals
   the declared expectation; no required finding id fires.

Analysis computation corroboration (not a test of unseen code, no repo files):
`urllib.parse.urljoin("https://example.test/project/", "a.html")` →
`https://example.test/project/a.html`;
`urljoin("https://source.test/from/entry.html", "a.html")` →
`https://source.test/from/a.html` (base ignored).

## 4. Load-bearing construction (the anti-false-green invariant for THIS case)

The fixture is only meaningful if the base changes the answer:

```
base_resolved   = https://example.test/project/a.html   # expected, clean
doc_resolved    = https://source.test/from/a.html       # base ignored
origin_retained = https://source.test/project/a.html    # base path, doc origin
all three differ
```

If a fixture for `first_base` ever has `base_resolved` equal to `doc_resolved`
(or to `origin_retained`), a validator with that shortcut passes it: a false
green inside the frozen matrix. Matrix/L1 should keep this invariant on the
fixture (assert the values differ at fixture-build time, or encode the two
wrong values as comments); it is cheap and it is the whole point of the case.
Case02's `relative_same_dir` has no base at all, so a base-ignoring
implementation still passes it; `first_base` is the case where reading the base
is load-bearing.

Failure-side expectation, useful for diagnosis and for a local selftest: if the
implementation ignores the base, the emitted finding is `canonical_mismatch`
with exit **1** (the href resolves cleanly; it just resolves elsewhere). It is
not `canonical_url_invalid` (the href is valid), not `base_url_invalid` (the
base is valid), not `html_unsupported`.

## 5. Why exit 0 and not 1/2/64

- **Not 1:** one canonical in explicit head, present non-empty href, base
  valid, resolved HTTP(S) URL equals `expectedCanonical`, no fragment, no
  credentials, no unsupported shape. No policy finding exists to emit.
- **Not 2:** manifest v1 with one page; the file is a regular readable file;
  both base and href are valid; the document has an explicit head; nothing
  forces `input_invalid` or `html_unsupported`.
- **Not 64:** the invocation is the contract CLI form
  (`--manifest <absolute path> --json`).
- `pagesChecked` is `1`; `findings` is `[]`.

The literal `verdict` token for success is not enumerated in the contract
(only "JSON object with verdict"); `"clean"` is the token consistent with
`exitMap` 0 = clean and the Matrix item's positive id. Case02, Case05 and this
report all assume it; Implement/Matrix must pin one token.

## 6. Interpretation note — single base, and the observed Case07 split

Read as: *one* head base that must be applied (name `first_base` = the
first/only base element in head). The frozen Matrix instrument confirms this
reading: `cases.json` freezes `first_base` with exactly one `<base href>` and
`second_base_ignored` as the multiplicity assertion — same document URL and
first base, plus a second `<base href="https://wrong.test/elsewhere/">` — both
expecting exit 0 / `clean`.

That pair is not byte duplication. `second_base_ignored` adds only the second
base; because the document directory (`/from/`) differs from both base
directories, it fails both "last base wins" and "ignore all bases" against the
clean expectation. Case07's report keeps the negative mirror (manifest
`expectedCanonical` = `https://wrong.test/elsewhere/a.html`, correct exit 1
`canonical_mismatch`, last-base implementation false-greens at 0) as its
`--selftest` probe instead of a frozen case. Together they cover both branches:
the clean case catches "ignore all bases", the selftest mirror catches "last
base wins". Accept as frozen; no change requested.

Only if L1 ever flips Case07 to a negative must `cases.json` and the fixture
expectation change together (Case07.md records the exact swap); do not make
`first_base` multi-base in that event.

## 7. Adjacent false-green attack — `template_base_decoy`

**Selected attack.** A `<base href>` inside a `<template>` that sits in the
explicit head must not establish the document base URL. `HTMLParser` reports it
as a normal in-head start tag, so a validator that tracks "inside head" but not
template depth honours a base the document does not have — and can return
`clean` on a page whose canonical does not actually resolve to the expected
URL.

Attack manifest (not part of the frozen 32; proposal only):

```json
{"version":1,"pages":[{"url":"https://source.test/from/entry.html","file":"template_base_decoy/page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`template_base_decoy/page.html` (the frozen `first_base` page with only the
base wrapped in a template):

```html
<!doctype html><html><head><template><base href="https://example.test/project/"></template><link rel="canonical" href="a.html"></head><body></body></html>
```

Correct policy result: **exit 1**, finding **`canonical_mismatch`**, page
`https://source.test/from/entry.html`, findings length 1.

Why: template contents are not part of the document tree. HTML §4.12.3: "The
template contents of a template element are not children of the element
itself." The document base URL algorithm (§2.4.3) looks for a "descendant base
element"; the frozen-base rule (§4.2.3) speaks of the first base "in a document
tree". A base inside template contents is neither a descendant of the document
nor in the document tree, so the document base URL is the fallback base URL —
the document URL. `a.html` resolves to
`https://source.test/from/a.html`, which differs from
`expectedCanonical` → `canonical_mismatch`, exit 1. The base `href` is a valid
URL and the element is merely out of scope, so `base_url_invalid` is wrong
here; the page is supported serialized HTML, so exit 2/`html_unsupported` is
wrong too.

False-green mechanism (the defect this catches): `html.parser.HTMLParser` is a
tokenizer, not a tree builder; it has no template-contents model. Local probe
on the exact fixture (Python 3.14.8, stdlib only, no lane code):

```
H head []
H template []
H base [('href', 'https://example.test/project/')]
H link [('rel', 'canonical'), ('href', 'a.html')]
end head
```

A validator that resolves the canonical against the first `base` token seen
while its own `in_head` flag is true — or that regex-scans the head substring —
uses `https://example.test/project/` and returns `https://example.test/project/a.html`,
equal to `expectedCanonical` → exit 0, `findings: []`. The publisher then ships
a page whose real canonical (in a browser) points at
`https://source.test/from/a.html`, and the preflight said clean.

Why it is distinct:

- From `first_base`: that is a real, document-level, conforming base that must
  be honoured; this is a template-scoped base that must be ignored. Opposite
  expectations on the same mechanism.
- From frozen `template_decoy`: that case wraps the *canonical link* in a
  template; this attack leaves a real canonical in head and wraps only the
  *base*. A validator that special-cases links for template depth (because
  `template_decoy` forces it) can still fail this attack while passing
  `template_decoy` — exactly the partial-fix risk.
- From `comment_decoy`/`script_decoy`: those hide the link; comments and raw
  script text already cannot produce start tags in `HTMLParser` (comments go to
  `handle_comment`; script/style content is "returned as is, without further
  parsing"). The base-in-template token *is* emitted, so it is the live one.
- From `second_base_ignored`/`base_invalid`: those are document-level,
  tree-order and parse-failure semantics; this is tree membership.
- From Case05's `base_scheme_downgrade` (real base, scheme effect) and Case04's
  foreign-authority base (real base, authority reset): the base here is
  inapplicable, not effective.

Guard and cost: because the frozen matrix is exactly 32 names, do not add a
33rd case. Put this fixture in `--selftest` as an internal adversarial
positive/negative pair (Implement owns the script; this is a recommendation),
or hold it as a wave-2 uncovered falsifier. The audit-side fix is one stack:
increment on `handle_starttag("template")`, decrement on
`handle_endtag("template")`, and ignore `base`/`link` tokens while depth > 0 —
plus the same suppression for raw `script`/`style` (already structural in
`HTMLParser`) and comments.

## 8. Boundaries and deferred questions (must not be absorbed into this case)

- **Body `<base>`.** The contract's resolver is "first head base href or
  document URL"; the HTML spec's document base URL algorithm accepts any
  descendant base with `href` (a `<base>` in body still affects resolution,
  though it is non-conforming). This case keeps the base in head, so it does
  not decide the body-base question. L1 must state the chosen rule; do not let
  a body-base fixture leak into `first_base` (it would change the expected exit).
- **Base after the link.** §4.2.3's ordering sentence is authoring conformance,
  but the processing algorithm keys only on first-in-tree-order. So a base
  placed after the canonical link still sets the document base URL, even though
  the document is non-conforming. A streaming resolver would use the document
  URL and could false-green a manifest whose `expectedCanonical` equals the
  document-URL resolution. This is a real uncovered probe, but its expected
  class is debatable (policy finding vs conformance finding; there is no
  frozen id for "late base"), so it is **not** the selected attack. `first_base`
  deliberately uses the conforming order.
- **Invalid / `data:` / `javascript:` base.** §4.2.3: if the base `href` is a
  parse failure, has scheme `data` or `javascript`, or is CSP-blocked, the
  frozen base URL becomes the fallback base URL — a bad base degrades to the
  document URL. The matrix nevertheless has a `base_invalid` case and a
  `base_url_invalid` finding id, which is a stricter local policy choice, not
  browser behaviour. `first_base` must stay away from this: its base is valid,
  so no `base_url_invalid` may fire.
- **Relative base `href`.** Permitted and resolved against the document URL
  (two-step). This fixture uses an absolute base to isolate one mechanism;
  relative-base resolution is a separate probe.
- **Trailing slash sensitivity.** `https://example.test/project/` (directory)
  vs `https://example.test/project` (file-like last segment) resolve `a.html`
  differently (`/project/a.html` vs `/a.html`). Any implementation that "adds
  a slash" or concatenates strings is wrong in general; it happens to pass
  this fixture, so do not treat this fixture as evidence for merge semantics.
- **Manifest URL vs file path.** The base for `a.html` is the manifest `url`
  (plus base element), never the manifest directory or the fixture file path.
  A relative href must not be resolved against the filesystem location.
- **CSP `base-uri`** delivered by header or meta is not modelled by an offline
  static reader; out of scope here and unstated by the contract. `first_base`
  assumes no policy blocks the base.
- **No network, no fetch, no JS.** Absolute base resolution is pure
  serialization; nothing here touches the limits the contract excludes
  (HTTP headers, redirects, rendering, freshness).

## 9. Implementation constraints this case imposes

1. Two-step resolution: parse the base `href` against the document URL
   (absolute here, but the code path must exist), then parse the canonical
   `href` against the resulting document base URL. Do not splice strings.
2. Only a head-scoped, document-level base may be used; template descendants,
   comments, and raw script/style content are outside the document tree.
   Track template depth in the audit, not in `HTMLParser`.
3. `rel` is a token list compared ASCII case-insensitively; `href` presence
   and non-emptiness are checked before resolution (`first_base` has one token
   and a present non-empty value).
4. Compare serialized absolute URLs, not raw `href` text; scheme/host
   ASCII-lowercased, default port omitted, path/query case-preserved, no
   fragment or credentials.
5. Emit `findings: []`, `verdict: "clean"`, `pagesChecked: 1`, exit 0; stdout
   stays one valid JSON object.
6. Never resolve against the manifest directory or fixture path; `file` is
   only the byte source, `url` is the document identity.

## 10. Sources

Primary, opened this session, access date 2026-10-20; living standards, so
anchors + fetch digest pin the read:

| ID | Source | Exact quote used | Fetch sha256 |
|---|---|---|---|
| S023 | WHATWG HTML §4.6.8.4, https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." | `82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7` (`html-links.html`) |
| S024 | WHATWG HTML §4.2.3, https://html.spec.whatwg.org/multipage/semantics.html#the-base-element | "If there are multiple base elements with href attributes, all but the first are ignored." | `fd9ae4b6a2e12472ae6f61c52b4ef32751e63f8262cea997d8c6056eba2db959` (`html-semantics.html`) |
| — | WHATWG HTML §2.4.3, https://html.spec.whatwg.org/multipage/urls-and-fetching.html#document-base-urls | "return the frozen base URL of the first such base element in tree order" | `6df35203c062d1cbd67948a2d09ace198c62dece7465fd7c51e886b895650def` (`urls-and-fetching.html`) |
| S025 | WHATWG HTML §4.12.3, https://html.spec.whatwg.org/multipage/scripting.html#the-template-element | "The template contents of a template element are not children of the element itself." | `5854951bbabbdca6b5ea365edd1e2f14e342bc51e77353469d21e46f859abe43` (`scripting.html`; matches HTMLTemplate seat's digest) |
| S026 | Python `html.parser`, https://docs.python.org/3/library/html.parser.html | "This parser does not check that end tags match start tags"; "The content of elements like script and style is returned as is, without further parsing" | `17ee043413e8cd0aa50fd10a9425b3dde7c1d13347b86988110ae94af98045e0` |
| — | WHATWG URL Standard, https://url.spec.whatwg.org/#concept-basic-url-parser and #concept-url-serializer | basic parser takes input "with an optional null or base URL base"; serializer emits scheme, `//`, host, "If url's port is non-null" | `08cb42a9a8575dab006676378c846fdd8a72d06897c27929aa51eaf099656be4` |

Also read locally (no new claims): `corpus/SOURCES.md` rows S020–S027,
`corpus/knowledge/static-canonical-preflight.md` ("Comments, raw script text
and template descendants cannot supply a document-head canonical"), and sibling
reports `HTMLBase.md`, `HTMLTemplate.md`, `PythonParser.md`, `Case02.md`,
`Case05.md`. The S026 raw-text quote matches PythonParser's recorded quote but
came from my own fetch; the Python docs page is 3.15.0 while the local
interpreter is 3.14.8 — the cited behaviours are documented as stable.

Additional §4.2.3 sentences relied on (same fetch): "There must be no more than
one base element per document."; "A base element must have either an href
attribute, a target attribute, or both."; "The href content attribute, if
specified, must contain a valid URL potentially surrounded by spaces."; "A base
element, if it has an href attribute, must come before any other elements in
the tree that have attributes defined as taking URLs."; "A base element that is
the first base element with an href content attribute in a document tree has a
frozen base URL."

## 11. Confidence and remaining unknowns

**Observed (contract/spec/probe):** contract matrix name, exitMap, finding ids,
manifest shape, and "first head base href or document URL" string; the S023/S024
and §2.4.3/§4.2.3/§4.12.3 quotes; the Matrix private clone's frozen
`first_base` manifest/page bytes and `cases.json` schema, read directly from
`/tmp/kake-r22-Matrix` at 18:37–18:38 (digests in §2; not present at the lane
base revision); `HTMLParser` emits a template-contained `base` as an in-head
start tag (Python 3.14.8 probe) and emits nothing for the comment/script bases;
`urljoin` values in §3; absence of `canonical_audit.py` and `cases.json` in the
lane at the base revision.

**Inference (not observable until Implement lands):** which shortcut an actual
implementation takes; whether it tracks template depth for `base` tokens as
well as `link` tokens; the literal clean verdict token; whether Matrix encodes
the load-bearing invariant of §4 or only `expectedCanonical`.

**Open handoffs:** (a) Matrix must keep `first_base` single-base and load-bearing,
and keep Case07 distinct; (b) L1 must decide body-base and late-base policy
(neither is this case); (c) Implement should add `template_base_decoy` to
`--selftest` (not to the frozen 32) if the interface allows internal fixtures;
(d) the clean verdict token should be pinned once.

## 12. Hygiene

Only file written: this report. No repo source, registry, corpus, verifier, or
lesson edits; no git/jj writes in the lane; no tests, matrix, or measure runs.
No credentials, accounts, host services, package transactions, or installs. All
network reads were official documentation (`html.spec.whatwg.org`,
`url.spec.whatwg.org`, `docs.python.org`); no live property was checked.
