# Case01 — `absolute_match` (matrix case 1 of 32)

Seat: `KakeR22.Case01` — read-only scout. No code, fixtures, tests, builds, registry/corpus edits, or git/jj writes; this report is the only write. No tool installs.

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`; base observed
`7c61c8cc791bde36dd5e3688bdfea2678d90146c` (matches the frozen contract). At first inspection the
validator, `cases.json`, `matrix.py`, and fixtures were absent; during this read the Matrix seat
landed `.ufo/waves/round-22/{cases.json,matrix.py,fixtures/}` (32 cases), while
`scripts/canonical_audit.py` remained absent. The landed `absolute_match` row and fixture are quoted
below; everything is a contract/spec-derived case specification, not an execution result.

## Verdict summary

| Field | Expected result (landed matrix row + contract) |
|---|---|
| Case kind | Positive control (clean page) |
| Page `url` | `https://example.test/project/a.html` |
| `expectedCanonical` | `https://example.test/project/a.html` |
| Canonical `href` | `https://example.test/project/a.html` (absolute, self-referential) |
| Expected exit | `0` (`clean`) |
| Expected case id | `clean` sentinel; `findings == []` |
| `pagesChecked` | `1` |

## 1. Concrete fixture (landed by Matrix; read-only here)

The Matrix seat landed this fixture during the read; the files below are authoritative and were not
modified by this seat.

- `.ufo/waves/round-22/fixtures/absolute_match/manifest.json` — 147 bytes, sha256
  `5ca6750bf00571943989846490462ca7bbcf372d1ca0c357145a1abc10971423`
- `.ufo/waves/round-22/fixtures/absolute_match/page.html` — 120 bytes, sha256
  `76bc55f0869acb190d4fd821694acae9c211d4dbcb1462159fdc9b8bd363630d`

`manifest.json` (source is one JSON line; pretty-printed here):

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "page.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

`page.html` exact bytes (one line plus a trailing LF):

```html
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a.html"></head><body></body></html>
```

The landed document is minimal: no `meta charset`, no `title`, empty body. None of those is a policy
predicate, so their absence must not produce a finding. A decorated variant that adds
`<meta charset="utf-8">`, `<title>absolute match</title>`, and a body paragraph is semantically
equivalent and must classify identically (my initial sketch used that shape with `a.html`; the
landed `page.html` supersedes it). `file` is manifest-relative and is the only file-resolution
source; the URL path `/project/a.html` is deliberately unrelated to the on-disk name `page.html`, so
a validator that maps URL to disk fails this case. The HTML file is a regular file, not a symlink.

## 2. Invocation and expected stdout

```sh
python3 scripts/canonical_audit.py --manifest <abs>/fixtures/absolute_match/manifest.json --json
```

Exit: `0`. Stdout must be one parseable JSON object; the contract's binding fields:

```json
{"verdict":"clean","pagesChecked":1,"findings":[]}
```

Key order and extra keys are not frozen. The binding assertions are exit `0`, `pagesChecked == 1`,
`findings == []`, and the case-level id `clean`. `clean` is a matrix-level sentinel, not a contract
finding id; it must not appear as an object inside `findings` (consistent convention in Case02,
Case05, Case08, and StdoutExit).

The landed `.ufo/waves/round-22/cases.json` row is:

```json
{"caseId":"absolute_match","manifest":"fixtures/absolute_match/manifest.json","expectedExit":0,"expectedFindings":["clean"],"rationale":"Local publisher policy: the absolute canonical URL matches the manifest target exactly."}
```

`matrix.py`'s `observed_findings()` maps an empty `findings` array to `["clean"]`, and the Matrix
report states clean positive controls use the explicit stable ID `clean`; so
`expectedFindings: ["clean"]` and `findings: []` are the same assertion, not a request for a
synthetic finding object.

## 3. Why the page is clean — check by check

1. **Explicit head.** The document has literal `<head>` and `</head>`; its only `<link>` is inside.
   `HTMLParser` is a tokenizer with no tree construction or implied head, so the audit must track
   head depth itself; this fixture leaves no ambiguity (explicit open and close, no truncation).
2. **Exactly one canonical link.** One `<link>` element; `rel="canonical"` splits on ASCII
   whitespace into `["canonical"]`; link-type keywords are ASCII case-insensitive and one token
   matches. No `canonical_missing`, `canonical_multiple`, or `canonical_outside_head`.
3. **Head placement is required and satisfied.** `canonical` is not a body-ok link type, and
   Google states the element "is only accepted if it appears in the `<head>` section"; the sole
   link is in head.
4. **`href` present, non-empty, absolute.** The HTML spec requires a `link` `href` to be a "valid
   non-empty URL potentially surrounded by spaces"; this absolute HTTP(S) URL qualifies. It is not
   `canonical_href_missing`.
5. **Resolution is identity.** There is no `<base>`, so the manifest `url` is the base; because the
   reference already has a scheme it is not a relative reference and no merge occurs. RFC 6596 §3
   explicitly permits a self-referential target, so the policy cannot reject this shape.
6. **URL is admissible.** Scheme `https` is in the contract's HTTP(S) set; host `example.test` is
   non-empty; no username/password, no port, path `/project/a.html`, no query, no fragment. Nothing
   triggers `canonical_url_invalid` or `canonical_fragment`.
7. **Normalized serialization equals `expectedCanonical`.** WHATWG serialization is exactly
   `https://example.test/project/a.html` (scheme/host already lowercase, no default port, path
   unchanged, no query/fragment). URL equivalence is defined by comparing serializations
   (optionally excluding fragments); the two serializations are byte-equal. No `canonical_mismatch`.
8. **No finding, exit 0.** Every policy predicate passes, so the page contributes no finding; a
   fully clean evaluated set maps to exit `0` / `clean` per the contract exit map.

This is a genuine positive control, not a tautology: it is the self-referential form RFC 6596
permits and Google recommends, and it exercises the absolute-href path with the exact expected
serialization. A validator that false-reds a compliant absolute canonical is caught here.

## 4. What this case discriminates — and what it cannot

**Discriminates:**

- Absolute `href` accepted; a validator that requires a relative form false-reds.
- Exactly-one counting, head placement, and single-token `rel` filtering basics.
- File resolution through the manifest `file` field, not through the URL path (the two differ by
  design in the contract's own example).
- Minimal-document tolerance: the landed page has no `<title>`, no `meta charset`, and an empty
  body; the policy does not require them, and their absence is not `html_unsupported` (the head and
  link are parseable), so a validator that demands a "complete" HTML document false-reds.
- No false red on a page with no `<base>`, one link, and no query/fragment/credentials/port.

**Cannot:**

- Distinguish raw-string equality from normalized equality: `href`, `url`, and `expectedCanonical`
  are identical, so a raw `href == expectedCanonical` check passes.
- Prove the validator reads the `href` at all: a validator that compares the manifest `url` to
  `expectedCanonical` and ignores the document also passes. Pair this case with `wrong_host` /
  `wrong_path` (and Case21's `data_url` negative twin) built so the page `url` equals
  `expectedCanonical` and only the `href` differs. Otherwise the positive control cannot detect a
  no-op. This is a Matrix-design requirement, not a defect in this case.
- Exercise normalization: with identical canonical strings there is nothing to normalize; case,
  port, and dot-segment behavior belong to other cases/probes.
- Prove read-only or no-network behavior; that is the NoWrites slice.

## 5. Adjacent false-green attack — `absolute_port_collapse`

Outside the frozen 32; run as a `--selftest` adversarial assertion (or hold for r23), not as a
33rd `cases.json` entry.

Attack fixture (temp copy; not committed by this seat): same manifest with
`"file": "attack_port.html"`, and `attack_port.html` containing the landed page shape with this
href:

```html
<link rel="canonical" href="https://example.test:8443/project/a.html">
```

Expected: exit `1`; exactly one finding
`{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}`; `pagesChecked: 1`.

**Why correct.** `https` is a special scheme whose default port is 443. The WHATWG parser nulls the
port only when it equals the scheme's default, so 8443 is retained; the serializer emits `:8443`;
URL equivalence compares serializations, and
`https://example.test:8443/project/a.html` is not equal to the port-less expected URL. The URL is
syntactically valid and HTTP(S), so `canonical_url_invalid` is wrong; it is a valid URL that differs
from `expectedCanonical`, hence `canonical_mismatch` (the same class as `wrong_host` / `wrong_path`
/ `wrong_query`; Case23's boundary note independently reaches the same classification).

**Why it false-greens.** A component comparator that compares
`(scheme, hostname, path, query)` and omits `.port` sees equality. CPython `urlsplit` exposes
`username`, `password`, `hostname`, and `port` as separate attributes and explicitly does not
validate, so omitting one field is a local mistake, not an exotic parser gap. A host-only
same-origin helper, or a normalizer that strips any `:port`, also accepts it. Raw `netloc`
equality would reject it, so this attack specifically targets component-wise comparators — the
implementation path the lane's own PythonURL report recommends ("compare on components, not on
`geturl()` text") and for which it lists port handling as a requirement.

**Paired control (opposite direction).** The same fixture with
`href="https://example.test:443/project/a.html"` must be **clean** (exit `0`): the parser nulls the
default port before serialization/equivalence. CPython's `urlsplit` exposes `.port` but its
documentation makes no WHATWG default-port elision claim, so a component comparator that tests
`.port` against `None` can false-red (implementation hazard, not observed behavior). The
`:8443` / `:443` pair pins under- and over-normalization of the port component.
URLNormalization.md independently expects `HTTPS://EXAMPLE.TEST:443/project/a/../a.html` to
normalize to the expected URL.

**Distinctness.** Only the port is added to `absolute_match`; scheme, host, path, and query are
identical. It is not `wrong_host` (host unchanged), not `wrong_path` / `wrong_query`, not
credentials or fragment, and no frozen matrix name covers a port-only authority difference. No
sibling report selects a port-only attack as its adjacent false green (Case23 lists it only as a
boundary note; Case04 uses a same-host/different-port variant only inside its base-authority
fixture). Choosing it keeps the selected attack set disjoint instead of duplicating the contract's
credentials clause (Case19, Case21) or the already-selected scheme (Case05, Case23), path-case
(Case02), empty-query (Case12), empty-fragment (Case22), and terminal-empty-segment (Case24)
probes. If Matrix builds `wrong_host` with a port-only difference, the port axis is conflated:
keep `wrong_host` a hostname difference and leave port to this probe.

**Non-chosen variants.** (a) Credentials `https://user:pass@example.test/project/a.html` is a
strong policy-explicit false green, but Case19 and Case21 already chose it; duplication adds no
coverage. (b) Percent-encoded path `%61` is preserved by WHATWG parsing, but Case02 flags the
preserve-vs-decode choice as a normalization-policy decision that must be declared before freezing.
(c) Backslash authority confusion such as `https://evil.test\@example.test/...` exposes
urllib-vs-WHATWG divergence, but Case02's implementation constraints already list backslashes as a
divergence the validator must document; it is a parser-profile probe, not a clean policy
assertion.

## 6. Handoff and residual ambiguity

- Fixture layout is settled by the landed Matrix artifact:
  `fixtures/absolute_match/{manifest.json,page.html}` with `file: "page.html"`. Keep resolution
  manifest-relative; do not derive it from the URL path.
- Clean token: the landed matrix fixes the convention as `expectedFindings: ["clean"]`;
  `matrix.py` maps an empty `findings` array to `["clean"]`. The validator must emit `findings: []`;
  `clean` must stay out of the findings array. `verdict` is not enumerated; use `clean` for a clean
  evaluated set.
- Any finding's `page` is the manifest `url`, not the file name (Case21 / StdoutExit convention).
- "WHATWG-like" is a subset, not a conformance claim. Implement must document its accepted subset
  (default ports, backslash, percent, IDNA). This case exercises only a canonical http(s) URL with
  no edge normalization.
- `scripts/canonical_audit.py` was absent when this report closed (the Implement work lives in a
  private clone). `cases.json`, `matrix.py`, and `fixtures/` landed during the read and were used
  read-only. No matrix, selftest, or interpreter probe was run; no implementation is claimed to
  pass.

## 7. Sources

All official pages fetched 2026-10-20; no live property was probed.

| Source | Location and exact quote (≤25 words) |
|---|---|
| WHATWG HTML Standard §4.6.8.4 | https://html.spec.whatwg.org/multipage/links.html#link-type-canonical — "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." and "The canonical keyword may be used with link element. This keyword creates a hyperlink." |
| WHATWG HTML Standard §4.6.8 | Same page, `#linkTypes` — "Keywords are always ASCII case-insensitive, and must be compared as such." Also: `rel` is split on ASCII whitespace; the resulting tokens are the keywords. The summary table marks `canonical` as not body-ok. |
| WHATWG HTML Standard §4.2.4 | https://html.spec.whatwg.org/multipage/semantics.html#the-link-element — "If the href attribute is present, then its value must be a valid non-empty URL potentially surrounded by spaces." |
| Google Search Central | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls — `The rel="canonical" link element is only accepted if it appears in the <head> section of the HTML`; `Do include a rel="canonical" link on the canonical page itself (also known as a self-referential canonical).`; absolute paths are recommended. |
| RFC 6596 §3 | https://www.rfc-editor.org/rfc/rfc6596.html#section-3 — the target MAY "Be self-referential (context IRI identical to target IRI)" and MUST identify duplicative-or-superset content. |
| WHATWG URL Standard §4.2, §4.4, §4.5, §4.6 | https://url.spec.whatwg.org/ — special scheme `https` default port `443`; parser sets port to null when equal to the default; serializer appends `:port` only when non-null; URL equivalence compares serializations. |
| CPython `urllib.parse` | https://docs.python.org/3/library/urllib.parse.html — "urlsplit() does not perform validation."; `netloc` is broken into `username`, `password`, `hostname`, `port`; "Percent-encoded sequences are not decoded." |
| CPython `html.parser` | https://docs.python.org/3/library/html.parser.html — attribute names are lowercased, quotes removed, character/entity references replaced; empty attributes yield `None`. |

Author-side lane artifacts consulted read-only (not independent authority):
`w1/PythonURL.md` (component comparison; explicit port handling), `w1/URLNormalization.md`
(default-port normalization; wrong_* → `canonical_mismatch`; clean sentinel), `w1/Case21.md`
(`page` = manifest `url`; `data_url` as the negative twin; credentials attack already chosen),
`w1/Case02.md` (path-case attack; percent-encoding ambiguity), `w1/StdoutExit.md` and
`w1/Case05.md` (clean token conventions), and `w1/Matrix.md` (landed fixture layout; explicit
`clean` ID for positive controls; `observed_findings()` maps empty to `clean`).
`corpus/lessons/round-22.md` rows S020–S027 register the same spec sources.

**Inference markers.** The mapping of the case name to "URL, href, and expectedCanonical are all
equal" is `[INFERENCE]` from the contract's manifest example and the case name; Matrix may use any
concrete values with the same structure. The failure modes above are plausible implementation
shapes, not observed defects. The `canonical_mismatch` id for the port probe follows the contract's
ID taxonomy and URLNormalization.md; the 32-case matrix does not contain the probe. The exact
`verdict` token is not enumerated by the contract; `clean` is the consensus choice.

## 8. Changes and tooling

Only this report was written: `.ufo/waves/round-22/w1/Case01.md`. The Matrix seat's landed
`cases.json`, `matrix.py`, and `fixtures/absolute_match/` were read only. No installs or package
transactions; no services; no registry, corpus, lesson, verifier, or lane-state edits; no tests,
matrix, selftest, or interpreter probes run; no credentials or live properties touched.
