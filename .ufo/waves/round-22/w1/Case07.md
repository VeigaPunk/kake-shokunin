# Case07 — `second_base_ignored`

Seat: `KakeR22.Case07` (scout, read-only). Contract: `.ufo/waves/round-22/contract.json`
@ lane `kake-shokunin`, base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Scope: analysis only. No code, fixtures, tests, builds, installs, registry/corpus edits, or
git/jj writes. Only this report was written. No validator or matrix was executed.

At first read the live lane had no `scripts/canonical_audit.py` and no
`.ufo/waves/round-22/cases.json`. While this report was being written, the Matrix and Implement
seats' private clones appeared at `/tmp/kake-r22-Matrix` and `/tmp/kake-r22-Implement`; their
relevant bytes were read (not run) and are cited below as peer-observed, **not landed evidence**.
The expectation here matches the Matrix's frozen entry.

## Verdict summary (frozen expectation)

| Field | Value |
|---|---|
| Case kind | Positive control: the first base element with `href` supplies the base; the second is ignored |
| Page `url` (document URL) | `https://source.test/from/entry.html` |
| `file` | `page.html` (manifest-relative, regular file) |
| `expectedCanonical` | `https://example.test/project/a.html` |
| Expected exit | **0** (`clean`) |
| Expected case finding id | **`clean`** (Matrix sentinel; not a contract `findingIds` member) |
| Emitted findings | **`[]`** |
| `pagesChecked` | `1` |
| Expected stdout invariants | `verdict = <clean>`; the contract does not enumerate the clean verdict token |

Matrix handoff (matches `/tmp/kake-r22-Matrix/.ufo/waves/round-22/cases.json`, read 2026-10-20):

```json
{"caseId":"second_base_ignored","manifest":"fixtures/second_base_ignored/manifest.json","expectedExit":0,"expectedFindings":["clean"]}
```

The Matrix's own rationale: "Local publisher policy: ignore later base href elements after the
first head base." `page` in any emitted finding is assumed to be the manifest page `url`; the
contract fixes the `id` and `page` keys but not the page representation.

## Frozen fixture (Matrix-compatible bytes)

`fixtures/second_base_ignored/manifest.json`:

```json
{"version":1,"pages":[{"url":"https://source.test/from/entry.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`fixtures/second_base_ignored/page.html`:

```html
<!doctype html><html><head><base href="https://example.test/project/"><base href="https://wrong.test/elsewhere/"><link rel="canonical" href="a.html"></head><body></body></html>
```

Whitespace/indentation and a `<title>`/`<meta charset>` are semantically irrelevant to this case;
the binding content is the two `<base href>` values in that order, one `<link rel="canonical"
href="a.html">`, and an explicit `<head>`. The three relevant origins/directories are deliberately
distinct:

| Input | Value | Resolves `a.html` to |
|---|---|---|
| Document URL | `https://source.test/from/entry.html` | `https://source.test/from/a.html` |
| First base with `href` | `https://example.test/project/` | `https://example.test/project/a.html` |
| Second base with `href` | `https://wrong.test/elsewhere/` | `https://wrong.test/elsewhere/a.html` |

Because no two branches coincide, an implementation that ignores all bases, or that uses the last
base, cannot reach the expected URL by accident.

## Resolution proof

1. **One canonical link in explicit head.** Exactly one `<link>` with `rel` = the single ASCII
   token `canonical`; it is inside the explicit `<head>`; `href="a.html"` is present and nonempty.
   No `canonical_missing`, `canonical_multiple`, `canonical_outside_head`, or
   `canonical_href_missing`.
2. **Base selection.** The contract policy is to "resolve href with first head base href or document
   URL". Registered tier-A source **S024** (WHATWG HTML §4.2.3) states: "If there are
   multiple base elements with href attributes, all but the first are ignored." The document-base
   algorithm (§2.4.3) says: "return the frozen base URL of the first such base element in tree
   order." The first base with `href` is `https://example.test/project/`; the
   `https://wrong.test/elsewhere/` base is ignored for base-URL purposes.
3. **The selected base is usable as-is.** It is an absolute `https` URL, so parsing against the
   document's fallback base URL yields itself. It is not a parse failure, `data:`, or `javascript:`
   URL, so the §4.2.3 fallback-to-document-URL branch is not taken. Both base hrefs are valid, so
   `base_url_invalid` is not the reading (that is the separate `base_invalid` case).
4. **Canonical href is resolved before comparison.** URL Standard §4.4: the parser "takes a scalar
   value string input, with an optional null or base URL base". Resolving `a.html` against
   `https://example.test/project/` yields `https://example.test/project/a.html` (the base's final
   empty segment is the directory; no query, fragment, credentials, port, or dot segments are
   introduced).
5. **Comparison succeeds.** The normalized resolved URL equals `expectedCanonical` exactly, so the
   page satisfies the local policy: exit **0**, `verdict = <clean>`, `pagesChecked: 1`,
   `findings: []`.
6. **Not exit 2.** The manifest, file resolution, explicit head, canonical count, `href`, both base
   URLs, and scheme are all evaluable. Exit 2 is reserved for cannot-evaluate input/unsupported
   shape, which this is not.

Note on conformance: the fixture contains two `<base>` elements, and HTML §4.2.3 also says "There
must be no more than one base element per document." That is an authoring-conformance violation,
but the URL-resolution algorithm still defines first-base-with-`href` behavior, and the frozen
matrix cannot express `second_base_ignored` with a conforming document. The validator is a policy
comparator, not an HTML conformance checker: it must **not** reject this page as `html_unsupported`
or `input_invalid`, and the frozen finding-id set has no id for an extra base. `[INFERENCE]` from
the contract's explicit inclusion of this case plus the absence of such a finding id.

## Discrimination (what a clean expectation catches)

| Implementation branch | Resolved canonical | Actual result | Matrix result |
|---|---|---|---|
| First base with `href` (correct) | `https://example.test/project/a.html` | 0 / clean | **pass** |
| Last base wins / overwrite on each `<base>` start tag | `https://wrong.test/elsewhere/a.html` | 1 / `canonical_mismatch` | **fail** (false red; expected 0) |
| All bases ignored; resolve against document URL | `https://source.test/from/a.html` | 1 / `canonical_mismatch` | **fail** (false red; expected 0) |
| Duplicate-base document rejected as unsupported | none | 2 / `html_unsupported`/`input_invalid` | fail (wrong classification) |

Both common base bugs are therefore detected as deviations from the expected clean result. The
honest limit: because the expectation is clean, the case catches a last-base bug only in the
false-*red* direction. It does not prove that a validator refuses to approve a page whose
second-base resolution is the tempting declared expectation; that is the adjacent attack below.

## Why clean is the right frozen expectation

1. **It complements `first_base`.** The Matrix's `first_base` fixture (`base href=
   https://example.test/project/`, same document URL and expected URL) proves first-base
   application. `second_base_ignored` adds the second base and proves it does not perturb the same
   clean result. `base_invalid` is the negative base case (`base_url_invalid`, exit 1). The three
   form accept/resolve/reject coverage without duplicating one verdict.
2. **It is non-vacuous.** Document, first-base, and second-base directories are all different, so
   an ignore-all-bases implementation fails as a false red, and a last-base implementation fails as
   a false red. A clean fixture whose document directory equalled the first-base directory would
   let ignore-all-bases pass for the wrong reason; this fixture avoids that.
3. **It matches the frozen matrix.** The Matrix's private-clone `cases.json` freezes
   `expectedExit: 0`, `expectedFindings: ["clean"]` with the exact fixture above. The round-22
   knowledge entry frames the proof as a "frozen failure case plus a clean positive control"; this
   is the positive-control side of the base rule.

A negative mirror (expect the second-base URL, exit 1) is defensible in isolation, but it would
duplicate the rejection direction already supplied by `base_invalid`/`wrong_*` and would weaken the
positive-control coverage. Keep the frozen clean expectation; use the mirror as the probe below.

### Cross-case coordination with Case06 (`first_base`)

Case06 confirmed the Matrix bytes directly (`cases.json` 18:38, `fixtures/first_base` 18:37),
recorded them with sha256 in Case06.md §2, and accepts the clean/clean pair: the frozen
`second_base_ignored` catches ignore-all-bases, while this report's negative selftest mirror
catches last-base. No flip is requested. The `first_base` and `second_base_ignored` entries share
document URL `https://source.test/from/entry.html`, first base
`https://example.test/project/`, and `expectedCanonical
https://example.test/project/a.html`; `second_base_ignored` only adds the
`https://wrong.test/elsewhere/` base. That is not byte duplication: the added base is the entire
multiplicity assertion, and the fixture's document directory (`/from/`) differs from both base
directories, so both last-base and ignore-all-bases implementations fail against the clean
expectation (as false reds). The first base is also cross-origin from the document
(`source.test` → `example.test`), so the fixture additionally exercises cross-origin base
acceptance/authority inheritance for a path-relative canonical; it does not claim the
root-relative authority falsifier owned by Case04. Any flip still moves `cases.json` and the
fixture expectation together (the adjacent probe below already contains the exact negative fixture
and expected id); this report's frozen section follows the current Matrix entry.

## Adjacent false-green attack — `second_base_expected_flip`

Distinct attack, not one of the frozen 32 cases; proposal only (no fixture or `cases.json` edit by
this seat). Use the **same `page.html` bytes** and flip only the manifest's `expectedCanonical`:

```json
{"version":1,"pages":[{"url":"https://source.test/from/entry.html","file":"page.html","expectedCanonical":"https://wrong.test/elsewhere/a.html"}]}
```

**Correct result:** the first base with `href` supplies the base, so the canonical resolves to
`https://example.test/project/a.html`, which differs from the expected second-base URL
`https://wrong.test/elsewhere/a.html` → exit **1**, `canonical_mismatch`.

**False-green mechanism:** an implementation that overwrites the base on every `<base>` start tag
(last-write-wins / `bases[-1]`) resolves `a.html` against `https://wrong.test/elsewhere/`, matches
`expectedCanonical`, and reports **exit 0 / clean**. That is a false approval of a page whose
spec-resolved canonical is on a different origin. The clean frozen case cannot expose this
direction because the same bug there appears as a harmless false red.

**Why it is distinct from this case.** The page bytes are identical; the frozen case declares the
first-base resolution as its expectation (clean), while this probe declares the second-base
resolution as its expectation (must fail). The probe therefore tests the base-selection rule from
the rejection side and pins the dangerous false-green direction. It is not `wrong_host` or
`wrong_path`: the canonical href is relative and the only variable is which `<base>` supplied the
base URL.

**Placement.** Run it as an adversarial probe in `canonical_audit.py --selftest` (or the reviewer
recipe), **not** as a 33rd matrix case (the matrix is frozen at 32). If the implementation already
uses first-base-with-`href` selection, the probe is a regression guard rather than a discovery.

**Secondary probe (lower priority) — first base without `href`.** Document URL
`https://source.test/from/entry.html`; head:
`<base target="_top"><base href="https://example.test/project/"><link rel="canonical" href="a.html">`;
`expectedCanonical` = `https://source.test/from/a.html`. Correct: the href-less base does not
supply the base (§2.4.3 "the first such base element"; S024 "Only the first base element with href
supplies the base"), so the second base applies → `https://example.test/project/a.html` ≠ expected
→ exit 1, `canonical_mismatch`. A validator that captures the first `<base>` element's maybe-missing
`href` and falls back to the document URL yields `https://source.test/from/a.html` = expected →
exit 0, a false green. The Implement clone's code already guards this (`"href" in normalized`), but
the probe remains a cheap selftest guard. It is distinct from `second_base_ignored` (the first base
there has `href`) and from `base_invalid` (nothing is malformed).

## Sources

Registered tier-A rows available in the lane working tree at report time (`corpus/SOURCES.md` was
being integrated during this run; S024 is **not** in base `7c61c8c` and must be committed by L1):

- **S024** — WHATWG HTML, §4.2.3 "The base element",
  `https://html.spec.whatwg.org/multipage/semantics.html#the-base-element`, spec, tier A,
  Living Standard accessed 2026-10-20. Exact quote (15 words): "If there are multiple base
  elements with href attributes, all but the first are ignored." Registry scope: "Only the first
  base element with href supplies the base; later base href values are ignored."
- **S023** — WHATWG HTML, §4.6.8.4 canonical link type,
  `https://html.spec.whatwg.org/multipage/links.html#link-type-canonical` (canonical declaration
  semantics; not base selection).
- **S026** — Python `html.parser`, `https://docs.python.org/3/library/html.parser.html` (tokenizer,
  not an HTML5 tree builder; the audit must track explicit head/base state itself).

Newly opened official documentation for this case (accessed 2026-10-20; **not in
`corpus/SOURCES.md`**, no registry edit made):

| Source | Location and exact quote |
|---|---|
| WHATWG HTML, §2.4.3 "Document base URLs" | `https://html.spec.whatwg.org/multipage/urls-and-fetching.html#document-base-url`; Living Standard "Last Updated 20 October 2026". Quote (14 words): "return the frozen base URL of the first such base element in tree order". |
| WHATWG HTML, §4.2.3 "The base element" (frozen-base rule) | `https://html.spec.whatwg.org/multipage/semantics.html#the-base-element`; same document. Quote (23 words): "A base element that is the first base element with an href content attribute in a document tree has a frozen base URL." Also: "There must be no more than one base element per document." |
| WHATWG URL Standard, §4.4 "URL parsing" | `https://url.spec.whatwg.org/#concept-url-parser`; Living Standard "Last Updated 19 October 2026". Quote (21 words): "The URL parser takes a scalar value string input, with an optional null or base URL base (default null)". Base URL concept: "A base URL is useful for the URL parser when the input might be a relative-URL string." |

No live property was probed; only public official documentation was fetched. No tool was installed
or upgraded.

Peer artifacts observed (read-only, **not landed evidence**; private author clones):

- `/tmp/kake-r22-Matrix/.ufo/waves/round-22/cases.json` and
  `fixtures/second_base_ignored/{manifest.json,page.html}` — froze exit 0, `["clean"]`, and the
  bytes quoted above (read 2026-10-20).
- `/tmp/kake-r22-Implement/scripts/canonical_audit.py` — base handling reads
  `if "href" in normalized and not self.base_seen` before recording `base_href`, i.e. first
  base-with-`href` wins and href-less bases are skipped (read, not executed; not a landed claim).

## Observed vs inference

| Claim | Status |
|---|---|
| Contract text: one canonical link in explicit head, first head base href or document URL, exitMap 0/1/2/64, closed finding-id set | Observed in `.ufo/waves/round-22/contract.json` |
| First-base-with-href and document-base-URL algorithm; URL parser base parameter | Observed, fetched 2026-10-20 (quotes above) |
| Matrix freezes this case as exit 0 / `["clean"]` with the quoted fixture | Observed in the Matrix private clone (not landed) |
| Resolution arithmetic (`example.test/project/a.html`, `wrong.test/elsewhere/a.html`, `source.test/from/a.html`) | Spec derivation (URL §4.4 directory semantics); not executed |
| `S024` present in the lane working tree but absent at base `7c61c8c` | Observed (`git show 7c61c8c:corpus/SOURCES.md` has no S024 row; working file does) |
| Last-base overwrite and first-base-element-without-href are plausible implementation bugs | `[INFERENCE]` code-shape inference; the Implement clone's read logic appears to avoid both |
| `page` = manifest `url`; clean verdict token unspecified | `[INFERENCE]` / contract gap; freeze at integration |
| Clean expectation is the intended frozen direction | Observed matrix entry plus contract pairing; not an admission decision |

## Remaining unknowns (for L1 / Implement / Matrix)

1. Verdict vocabulary: the contract names the `verdict` field but not its clean/failed tokens;
   `cases.json` and the validator must agree on one string. `matrix.py` must map the
   `expectedFindings: ["clean"]` sentinel to an empty stdout `findings` array, not an
   `id: "clean"` finding object (Case06 reached the same reading).
2. `page` representation in findings (URL vs file path vs index); this report assumes the manifest
   `url`, matching sibling Case05's proposal.
3. Manifest layout: one aggregate manifest for all 32 pages or one manifest per case. The Matrix
   clone uses per-case manifests under `fixtures/<case>/`; the fixture content is layout-independent.
4. Multi-base authoring non-conformance: the contract should state explicitly that duplicate
   `<base>` is processed by first-with-`href`, not rejected as `html_unsupported`; no finding id
   exists for the extra base.
5. `S024` is uncommitted in the live lane at report time; L1 owns committing the registry rows and
   the `static-canonical-preflight.md` entry.
6. Whether the adjacent expected-flip probe belongs in `--selftest` this round or is held for r23;
   it must not change the frozen 32-case expectation.

## Scope and limits

- Read-only: no validator run, no matrix run, no fixture or `cases.json` created, no lane file
  edited except this report; no git/jj writes; no subagents; no installs.
- Network: three official documentation fetches (HTML `semantics.html`, HTML
  `urls-and-fetching.html`, URL Standard) on 2026-10-20; no live site, domain, or property was
  probed.
- Resolution arithmetic is spec-derived, not executed; peer clone contents are private-workspace
  observations, not landed evidence, and no behavior is claimed from executing them.

Report: `.ufo/waves/round-22/w1/Case07.md`
