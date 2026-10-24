# Case18 — `href_empty` (matrix case 18/32)

Seat: KakeR22.Case18, read-only scout. Lane base observed `7c61c8cc791bde36dd5e3688bdfea2678d90146c`. No repo/corpus/verifier edits, no installs, no tests of the capability. Platform sources were fetched read-only from the official spec sites into `/tmp/case18-src/` (scratch); local probes below exercise only stdlib URL/parser semantics, not `canonical_audit.py` (which does not exist at base).

## Frozen expectation (proposed `cases.json` entry)

Fixture layout (names arbitrary as long as the manifest resolves; regular file, no symlink, no BOM, LF endings):

- `.ufo/waves/round-22/fixtures/href_empty/manifest.json`
- `.ufo/waves/round-22/fixtures/href_empty/href_empty.html`

`manifest.json`:

```json
{"version":1,"pages":[{"url":"https://example.test/project/href_empty.html","file":"href_empty.html","expectedCanonical":"https://example.test/project/href_empty.html"}]}
```

`href_empty.html`:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>href_empty</title>
<link rel="canonical" href="">
</head>
<body>
<p>href_empty</p>
</body>
</html>
```

Tokenizer shape asserted by this fixture: the `href` **key is present with value `''`** (`[('rel','canonical'),('href','')]`, measured on python 3.14.8). It is not key-absent (that is the `href_absent` fixture) and not a valueless attribute (`('href', None)`); keep exactly this shape so the two fixtures stay distinguishable at the parser boundary.

Expected process exit: **1** (failed policy). Expected stdout finding: exactly one, id **`canonical_href_missing`**, page `https://example.test/project/href_empty.html`; `pagesChecked` 1.

```json
{"verdict":"failed","pagesChecked":1,"findings":[{"id":"canonical_href_missing","page":"https://example.test/project/href_empty.html"}]}
```

`verdict` spelling is not frozen by the contract (only the field name is); the matrix should key on exit + finding id. `"failed"` is proposed to match the exitMap wording.

**Load-bearing detail: `expectedCanonical` MUST equal the page URL.** With no `<base>`, an empty href resolves exactly to the document URL, so a validator that only resolves and compares returns clean here. The case passes only if the audit rejects the raw href value before resolution. If `expectedCanonical` were a different URL, the case would fail with `canonical_mismatch` for the wrong reason and stop discriminating `canonical_href_missing`.

## Why

Observed, normative (WHATWG HTML §4.2.4, the link element; anchor `#attr-link-href`):

> "If the href attribute is present, then its value must be a valid non-empty URL potentially surrounded by spaces."

Observed, definitions (HTML §2.4.1; anchors `#valid-non-empty-url`, `#valid-non-empty-url-potentially-surrounded-by-spaces`):

> "A string is a valid non-empty URL if it is a valid URL string but it is not the empty string."

> "… after stripping leading and trailing ASCII whitespace from it, it is a valid non-empty URL."

Observed, Infra (`#ascii-whitespace`): "ASCII whitespace is U+0009 TAB, U+000A LF, U+000C FF, U+000D CR, or U+0020 SPACE." `href=""` therefore violates the HTML conformance MUST outright. The document is not an evaluable failure of input shape — the defect is deterministic — so exit **1**, not 2 and not 64.

Observed, WHATWG URL Standard §4.4 (`#concept-basic-url-parser`, `#relative-state`): the parser first removes leading/trailing C0 control or space, and the relative state copies base scheme/username/password/host/port/path/query; empty input never overwrites them, so the result equals the base URL. Local corroboration (python 3.14.8, stdlib only):

```
urljoin('https://example.test/project/href_empty.html', '')   -> 'https://example.test/project/href_empty.html'
urljoin(base, '   ')                                          -> same
urlsplit(urljoin(base, '')).geturl()                          -> same
HTMLParser.parse('<link rel="canonical" href="">')            -> [('rel','canonical'), ('href','')]
```

So a resolver sees exact equality with `expectedCanonical`; this case exists to make that false green impossible.

### Finding-id choice (freeze one)

| Input on the one head `link[rel=canonical]` | id | exit |
|---|---|---|
| href key absent | `canonical_href_missing` | 1 |
| href present, value `''` / ASCII-whitespace-only / valueless (`None`) | `canonical_href_missing` | 1 |
| href present, non-empty, not a parseable URL string, or non-HTTP(S) scheme (`javascript:`, `data:`) | `canonical_url_invalid` | 1 |
| resolved URL has a fragment (`#…`) | `canonical_fragment` | 1 |
| no canonical link element at all in the explicit head | `canonical_missing` | 1 |

`canonical_href_missing` is correct for empty because the defect is *no href value*, not an unparseable URL: with a base the empty string parses successfully to the document URL, so `canonical_url_invalid` would misdescribe the parse result, and the element is still covered by the link-element rules (only "both href and imagesrcset absent" makes it not define a link), so `canonical_missing` is wrong. The frozen `findingIds` list has no separate empty id, and `href_absent` (Case17, confirmed by that seat) uses the same id — this is one policy clause with one author remedy. If L1 instead freezes validity-first classification (`canonical_url_invalid` for empty), that is defensible but must be one id across the pair and must not collide with `invalid_url`/`javascript_url`/`data_url`.

### Contested mapping in this wave (needs an explicit L1 freeze)

Peer reports read the same clause differently, so this must not be silently merged:

- `URLNormalization.md` P2 (reviewer; amended report after rechecking WHATWG HTML §4.2.4 and the valid-non-empty-URL definition): now agrees `href=""` must not resolve clean; recommends exit 1 with `canonical_url_invalid` (present value violates the non-empty `link[href]` requirement), keeps absent attribute as `canonical_href_missing`, and flags the mapping for L1 to freeze across matrix and selftest.
- `Case13.md` (missing_link): defines `canonical_href_missing` as "a `link rel=canonical` exists but has no `href` (`href_absent` case)".
- `Case02.md` §7.1 (relative_same_dir): "Resolve only a **present, non-empty** `href`. Absent → `canonical_href_missing`; empty → the same family, never 'resolves to document URL'. Empty resolution is the cheap false green."

Adjudication — reject with exit 1, and prefer `canonical_href_missing`:

1. WHATWG HTML §4.2.4 makes `href=""` non-conforming ("must be a valid non-empty URL potentially surrounded by spaces"); C1's after-state says the validator "rejects missing/conflicting/mismatching canonical signals", and this is a *publishing preflight*, so printing clean for a shape the HTML Standard forbids is a false green that defeats the stated capability.
2. The frozen `findingIds` has no empty-specific id. `canonical_url_invalid` is defensible but less precise for empty: with a base, `""` parses successfully to the document URL, so nothing fails to parse — the failed check is the non-emptiness/presence check that runs before any URL is formed. `canonical_missing` is wrong (the element is present). `canonical_href_missing` is the only id that says "no usable href value", covers absent/empty/valueless with one policy clause, and matches Case02's "same family".
3. The contract never reserves any id for absent only; `href_absent` and `href_empty` are distinct *case names/fixtures* (tokenizer shapes), not necessarily distinct findings. `PythonParser.md` item 4 only says the parser *can* separate the shapes; it does not assign ids. The reviewer's distinct-id proposal is a taxonomy preference, not a contract requirement.

If L1 instead freezes the validity-first reading (the amended `URLNormalization.md`/`Case13.md` position), `canonical_url_invalid` is the only admissible alternative (empty parses, so `canonical_mismatch` would report a wrong target). The outcome both sides reject is clean/exit 0: it would make `href_empty` a positive control and let the preflight bless a declaration with no explicit target. Whatever is frozen, `href_absent`, `href_empty`, `invalid_url`, `javascript_url`, `data_url` need disjoint expectations, and the empty id/exit must be identical across `cases.json`, `matrix.py`, and the script's own `--selftest` expectations — a selftest/matrix drift is itself an operability defect.

RFC 6596 does **not** supply this rejection: its target MAY be relative and self-referential, and an empty relative reference legally denotes the current document. The basis is the HTML `href` conformance MUST; the finding text must not claim RFC non-conformance. Google's guidance (already landed: `GoogleCanonical.md`) recommends absolute paths and endorses self-referential canonicals but says nothing about empty values — do not extrapolate a Google behavior claim; the contract's "no selection claim" limit applies.

## Adjacent false-green attack (distinct from this case)

`href_ws.html`, same head shape, page `https://example.test/project/href_ws.html`, `expectedCanonical` the same self URL:

```html
<link rel="canonical" href="  ">
```

Expected: exit **1**, id **`canonical_href_missing`**.

Attack: the value is byte-non-empty, so `if href == ""` (and even `if not href`) does not catch it, while `urljoin(base, "  ")` still returns the document URL — a clean false green. HTML's strip-ASCII-whitespace-then-non-empty rule makes it the same MUST violation. It is distinct from the frozen case (different input class), from `href_absent` (Case17: key absent), and from `fragment_url` (matrix case); it is not in the 32-case list, so it is a synthetic adversarial probe, not a replacement case.

Two cautions the attack pins down:
- "ASCII whitespace" is exactly the five characters above. Bare Python `str.strip()` also removes U+00A0 and other Unicode spaces, so `href="\u00a0"` would be misclassified as missing; per HTML the strip leaves it and the URL parser percent-encodes it (a mismatch, not `href_missing`).
- Valueless `<link rel=canonical href>` arrives as `('href', None)` per the Python docs ("For empty attributes, value is None.") and is the same href missing class; distinguish key presence (absent) from value shape (None/''/whitespace) but map all three to the same id, matching Case17's boundary.

## Source record

| Source | Locator | Accessed | Use |
|---|---|---|---|
| WHATWG HTML Living Standard, §4.2.4 the link element | https://html.spec.whatwg.org/multipage/semantics.html#the-link-element (and `#attr-link-href`) | 2026-10-20 | href MUST be valid non-empty URL potentially surrounded by spaces; "does not define a link" clause |
| WHATWG HTML, §2.4.1 terminology | https://html.spec.whatwg.org/multipage/urls-and-fetching.html#valid-non-empty-url | 2026-10-20 | valid non-empty URL; strip leading/trailing ASCII whitespace |
| WHATWG URL Standard, §4.4 URL parsing | https://url.spec.whatwg.org/#concept-basic-url-parser and `#relative-state` | 2026-10-20 | empty input resolves to base; leading/trailing C0-control-or-space strip |
| Infra Standard, ASCII whitespace | https://infra.spec.whatwg.org/#ascii-whitespace | 2026-10-20 | exact five-character set |
| WHATWG HTML, §4.6.8.4 canonical link type | https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | 2026-10-20 | keyword binds the preferred URL to the href attribute; defers to RFC 6596 |
| RFC 6596 §3 (Informational) | via `.ufo/waves/round-22/w1/RFC6596.md` | 2026-10-20 (peer-verified) | relative/self target permitted; no basis to reject empty on its own |
| Google Search Central canonical guidance | via `.ufo/waves/round-22/w1/GoogleCanonical.md` | 2026-10-20 (peer-verified) | absolute-path recommendation, self-referential canonical; no empty-href rule |
| Python `html.parser` docs | via `.ufo/waves/round-22/w1/PythonParser.md` | 2026-10-20 (peer-verified) | attribute values decoded; empty attributes → `None`; invalid markup parsed |

Quotes above are verbatim contiguous spec text with line wraps rejoined. Everything about the chosen finding id and matrix encoding is C1 local policy, marked as recommendation, not spec.

## Confidence

- Normative rule and resolution behavior: **high** (verbatim definitions + parser algorithm + local probe).
- Expected exit 1: **high** (deterministic policy failure, fully evaluable).
- Expected id `canonical_href_missing`: **medium-high** — the frozen id set supports it, but it is contested in this wave (`URLNormalization.md` amended P2 and `Case13.md` favor `canonical_url_invalid` for present-but-empty; `Case02.md` §7.1 favors the same family); the adjudication above is a recommendation to L1, and the freeze must be explicit and consistent with Case17/Case19.
- Adjacent attack: **high** that it false-greens a literal-empty-only check; its expected id inherits the same mapping decision.

## Remaining unknowns

- Verdict string spelling (`"failed"` vs other) is not contract-frozen; matrix should not over-assert it.
- Whether `matrix.py`/`measure.py` assert single-finding cardinality per page (recommended) or only id membership.
- `invalid_url` fixture boundary belongs to Case19; if that case uses an ASCII-whitespace-only value, the two partitions collide — keep whitespace-only under `href_empty`/`canonical_href_missing`.
- Contested id: both sides now agree empty fails (exit 1); the split is `canonical_href_missing` (Case02 §7.1, this report) vs `canonical_url_invalid` (amended `URLNormalization.md` P2, `Case13.md`). L1 must adjudicate before `cases.json` freezes the id; a silent matrix choice would make the case self-fulfilling.

## Checks for main agent

- Re-open the three spec anchors and confirm the quoted sentences still appear (they are Living Standard text).
- Record the case with expected exit 1 + id `canonical_href_missing`, and keep `expectedCanonical == url`.
- Verify the implementation checks the raw href (ASCII-whitespace strip, exact five chars) before `urljoin`, and treats key-absent/None/empty alike.
- Adjudicate the contested id (URLNormalization P2 vs Case02 §7.1) before freezing `cases.json`; if L1 chooses `canonical_url_invalid`, update `href_empty` and `href_absent` together. Clean/exit 0 is the one outcome this report argues against.
- Ensure the script's own `--selftest` asserts the same href-empty exit/id as `cases.json`; the contract requires `--selftest`, and drift between selftest and matrix is itself a defect.
- Run the built matrix/measure once after integration; do not accept this report as runtime evidence.
