# Attack11 — `entity_href` falsification (round 22, wave 2)

Frozen candidate: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (lane HEAD, `git rev-parse HEAD`
observed as that value; `git diff HEAD` empty for `scripts/canonical_audit.py`,
`.ufo/waves/round-22/cases.json`, and `fixtures/entity_href`).
Environment: Linux, Python 3.14.8. No production bytes changed; probe fixtures live under
`/tmp/kake-r22-attack11/`. No subagents, no installs, no network, no git/jj writes, no lane
edits beyond this report. Axis under test: **operability** (capability claim C1), milestone
`falsify-canonical-capability`.

## Independent expectation (derived before running)

Contract policy: exactly one canonical link in an explicit head; `rel` is an ASCII
case-insensitive token list; resolve `href` against the first head `base href` or the document
URL; HTTP(S) only; fragments and credentials rejected; normalized URL compared to
`expectedCanonical` with query preserved.

Frozen fixture `fixtures/entity_href/page.html` (raw bytes, digest
`967d0653d4669556648a96b891fad90b98386d3eb7c847713172e1cdc4adc393`):

```html
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a&amp;b.html"></head><body></body></html>
```

Manifest digest `035b95d22c5d16f3d864845e3c1ee2b704e2955b842c7e66a25b62d7b6a8dbd4`; document
`https://example.test/project/index.html`; `expectedCanonical` is the JSON literal
`https://example.test/project/a&b.html`.

HTML character-reference semantics: `&amp;` in an attribute value is one character reference
and decodes to `&`. The href therefore becomes
`https://example.test/project/a&b.html`. It is already absolute HTTP(S), has no fragment, no
credentials, no whitespace, and the tool's conservative query/path spelling preserves the
literal `&`. The normalized canonical equals the normalized expected URL, so no finding is
emitted → verdict `clean`, exit **0**, findings `[]`. The matrix renders empty findings as the
single id `clean`.

Both fixture digests match `frozen/expected.json.inputs` entries exactly (verified with
`sha256sum`).

Parser mechanism context (stdlib, independent of the tool):

```
'https://example.test/project/a&amp;b.html'  -> 'https://example.test/project/a&b.html'
'https://example.test/project/a&amp;amp;b.html' -> 'https://example.test/project/a&amp;b.html'
'https://example.test/project/a&#x2F;b.html' -> 'https://example.test/project/a/b.html'
'https://example.test/project/a&zzz;b.html' -> 'https://example.test/project/a&zzz;b.html'
```

## Assigned run

Command:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case entity_href
```

stdout:

```
PASS caseId=entity_href exit=0 findings=clean
SUMMARY selection=entity_href accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

Exit: **0** (harness). Matches the independent expectation exactly.

Direct public CLI on the frozen fixture:

```
python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/entity_href/manifest.json --json
```

stdout: `{"findings":[],"pagesChecked":1,"verdict":"clean"}` — exit **0**.

## Nearest-neighbor attack — exactly-once decoding of a double-escaped href

Fixture `/tmp/kake-r22-attack11/nn_double_entity/`, one page, same document URL and the
nearest byte-level variant of the assigned case (one inserted `amp;`):

```html
<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a&amp;amp;b.html"></head><body></body></html>
```

`expectedCanonical`: `https://example.test/project/a&amp;b.html` (literal five-character
`&amp;`, not `&`).

Independent expectation: one character-reference decode of `&amp;amp;` yields the literal
`&amp;`. The resolved href is `https://example.test/project/a&amp;b.html`; normalization
keeps `&` and `;` (both are in the conservative safe set), so it equals the normalized
expected URL → `clean`, exit **0**, findings `[]`.

Command:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r22-attack11/nn_double_entity/manifest.json --json
```

stdout: `{"findings":[],"pagesChecked":1,"verdict":"clean"}` — exit **0**.

Discriminating power: a no-decode implementation would compare `a&amp;amp;b.html` against
`a&amp;b.html` (mismatch, exit 1); a double-decoding implementation would compare
`a&b.html` against `a&amp;b.html` (mismatch, exit 1). Only exactly-once decoding produces the
observed clean, so the result is not explained by "any decoding happened".

## Additional bounded probes at the same boundary

### 1. Decode before URL-structural parse (`&#x2F;`)

`/tmp/kake-r22-attack11/probe_hex_sep/` page href:
`https://example.test/project/a&#x2F;b.html`; expected
`https://example.test/project/a/b.html`.

Derivation: `&#x2F;` is a numeric character reference for `/`; decoded href is
`https://example.test/project/a/b.html` → clean, exit **0**. If decoding were skipped, the
literal attribute string contains `#` (from `&#x2F;`), which the tool rejects as a fragment
before parsing → `canonical_fragment`, exit 1.

stdout: `{"findings":[],"pagesChecked":1,"verdict":"clean"}` — exit **0**. Matches; decoding
occurs before URL normalization for a URL-structural delimiter.

### 2. No repeated decoding (`&amp;#x2F;`, false-clean vector)

`/tmp/kake-r22-attack11/probe_double_decode/` page href:
`https://example.test/project/a&amp;#x2F;b.html`; expected
`https://example.test/project/a/b.html`.

Derivation: one decode turns `&amp;` into `&` and leaves the literal `#x2F;`, so the href
contains a literal `#` → `canonical_fragment`, exit **1**. A double-decoding implementation
would produce `.../a/b.html` and wrongly report `clean` (false acceptance).

stdout:

```
{"findings":[{"id":"canonical_fragment","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

Exit: **1**. Matches; the false-clean path is closed.

### 3. Wrong-operand control — `expectedCanonical` is not HTML-decoded

`/tmp/kake-r22-attack11/control_expected_literal/` page href:
`https://example.test/project/a&zzz;b.html` (no such named reference, stays literal);
expected: `https://example.test/project/a&amp;zzz;b.html` (literal).

Derivation: actual `a&zzz;b.html` ≠ expected `a&amp;zzz;b.html` → `canonical_mismatch`, exit
**1**. If the tool unescaped `expectedCanonical` as HTML (JSON is not HTML), expected would
collapse to `a&zzz;b.html` → false clean.

stdout:

```
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

Exit: **1**. Matches; character-reference decoding is scoped to the HTML href operand.

## Before/after controls

- BEFORE revision `7c61c8cc791bde36dd5e3688bdfea2678d90146c`: `git cat-file -e` on
  `scripts/canonical_audit.py`, `.ufo/waves/round-22/cases.json`, and both
  `fixtures/entity_href` files exits **128** (paths absent), consistent with the claim's before
  state "no lane-owned runnable canonical-policy validator".
- AFTER candidate `c0fd6d5`: matrix PASS and direct CLI clean above; `git diff HEAD` for the
  tool, cases, and fixture is empty, and the tool/fixture digests equal the frozen
  `expected.json.inputs` values.

## Verdict

**Claim survives** for `entity_href`. Expected exit/id derived independently (0 / `clean`)
equals observed in both the frozen matrix and the direct public CLI. Four same-boundary probes
behave per policy and collectively pin exactly-once HTML character-reference decoding before
URL normalization, with decoding applied only to the HTML href and no false acceptance via
repeated decoding.

Residual unknowns (not gates for this case): author-side post-integration evidence, not
independent non-author closure; only CPython 3.14.8 exercised; scope remains static
`HTMLParser` input, not browser/HTML5 tree-builder conformance, and no search-engine
selection claim. No production file was edited; no additional frozen cases were run.

Suggested L1 checks after the wave: full 32-case matrix plus `measure.py --revision
c0fd6d5...`, `replay.py`, and `--selftest`; this seat changed only this report.
