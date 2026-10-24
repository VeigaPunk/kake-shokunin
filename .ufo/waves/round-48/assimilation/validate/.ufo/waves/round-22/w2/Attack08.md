# Attack08 — `rel_token_list` falsification (post-integration, frozen candidate)

Seat: `KakeR22.Attack08` (scout, leaf). Frozen contract: `.ufo/waves/round-22/contract.json`.
Measured candidate revision: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (lane master observed via
`git rev-parse HEAD`).
Scope: read-only attack on one frozen case plus bounded `/tmp` probes of the same parser boundary.
No production source/fixture/oracle bytes, tests, registry, or git/jj state were changed; the only
lane write is this report. No tool installs were performed.

## Verdict

**Claim survives.** Frozen case `rel_token_list` is accepted with the independently expected
exit/id, and nearest-boundary probes behave exactly as the contract policy requires. No
falsification found for this case.

## 1. Independent derivation (read before running the CLI)

Inputs read: contract `interface` (entry/CLI/exitMap/findingIds/policy), `cases.json`,
`fixtures/rel_token_list/{manifest.json,page.html}`.

Fixture bytes:

```json
{"version":1,"pages":[{"url":"https://example.test/project/index.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```
```html
<!doctype html><html><head><link rel="alternate canonical" href="a.html"></head><body></body></html>
```

Derivation, independent of any actual output:

1. Exactly one `<link>` in an explicit, closed `<head>`; its `rel` is the ASCII-whitespace token
   list `alternate canonical`, one token of which is ASCII-case-insensitively `canonical`
   (contract: “rel ASCII case-insensitive token list”). So exactly one canonical link exists.
2. No `base` element, so `href="a.html"` resolves against the document URL
   `https://example.test/project/index.html` to `https://example.test/project/a.html`.
3. That equals `expectedCanonical`, query absent, no fragment/credentials/default port.
4. Therefore: `findings == []`, verdict `clean`, **exit 0**; finding id none.

`cases.json` independently freezes `expectedExit: 0`, `expectedFindings: ["clean"]`, rationale
“accept canonical as one ASCII-whitespace-separated rel token” — consistent with the derivation
above (the matrix treats an empty `findings` array as the `clean` sentinel).

## 2. Frozen case through the matrix instrument

Exact command (run from `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case rel_token_list
```

stdout (exit `MATRIX_EXIT=0`, no stderr):

```
PASS caseId=rel_token_list exit=0 findings=clean
SUMMARY selection=rel_token_list accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

`--json` form, exit `0`, one result row:

```json
{"selection": "rel_token_list", "accepted": 1, "total": 1, "executed": 1, "discrepancies": 0, "toolMissing": false, "results": [{"caseId": "rel_token_list", "status": "PASS", "expectedExit": 0, "actualExit": 0, "expectedFindings": ["clean"], "actualFindings": ["clean"], "stdout": "{\"findings\":[],\"pagesChecked\":1,\"verdict\":\"clean\"}\n", "stderr": ""}]}
```

The nested validator stdout is
`{"findings":[],"pagesChecked":1,"verdict":"clean"}` — matches derivation.

## 3. Nearest-neighbor fixture attacking the same boundary

Boundary under attack: the phrase “ASCII … token list”. HTML splits `rel` only on ASCII
whitespace (space, tab, LF, FF, CR). A validator that splits on Python/Unicode whitespace would
wrongly accept `canonical` separated by U+00A0 NO-BREAK SPACE, which is not an ASCII-whitespace
separator. The frozen fixture differs from this attack by **one character class**.

Attack fixture (scratch; `/tmp/attack08-rel-token-boundary/attack/`):

```json
{"version":1,"pages":[{"url":"https://example.test/project/index.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```
```html
<!doctype html><html><head><link rel="alternate&#160;canonical" href="a.html"></head><body></body></html>
```

Independent expectation: HTMLParser unescapes `&#160;` to U+00A0 in the attribute value, so the
decoded `rel` is `"alternate\xa0canonical"`; ASCII-whitespace split yields the single token
`"alternate\xa0canonical"`, not `canonical`. Zero canonical links in head →
finding id **`canonical_missing`**, verdict failed policy, **exit 1**. (The `href` would otherwise
match, so the probe isolates token recognition.)

Matched control differing only by the separator (ASCII space), `/tmp/attack08-rel-token-boundary/control/`:

```html
<!doctype html><html><head><link rel="alternate canonical" href="a.html"></head><body></body></html>
```

Independent expectation: tokens `alternate`, `canonical` → one canonical, `href` resolves to the
expected canonical → **exit 0**, `clean`.

Exact commands (cwd `/tmp`):

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/attack08-rel-token-boundary/attack/manifest.json --json
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/attack08-rel-token-boundary/control/manifest.json --json
```

Observed:

| fixture | exit | stdout |
|---|---|---|
| attack (NBSP separator) | `1` | `{"findings":[{"id":"canonical_missing","page":"https://example.test/project/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}` |
| control (ASCII space) | `0` | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` |

Observed matches independent expectation in both directions; stderr empty. An independent
`html.parser` probe (not the validator) confirmed the decoded values:
`'alternate\xa0canonical'` → ASCII tokens `["'alternate\\xa0canonical'"]`,
`exact_canonical_token=False`; control → `["'alternate'", "'canonical'"]`,
`exact_canonical_token=True`.

### Acceptance-side probes of the same boundary (controls)

Same fixture shape, separator supplied as a character reference; independent expectation is
`clean`/exit 0 because all are ASCII whitespace:

- tab: `rel="alternate&#9;canonical"` → exit `0`, `{"findings":[],"pagesChecked":1,"verdict":"clean"}`
- form feed: `rel="alternate&#12;canonical"` → exit `0`, `{"findings":[],"pagesChecked":1,"verdict":"clean"}`

So the tokenizer rejects a non-ASCII separator and accepts the non-space ASCII-whitespace members,
i.e. it tracks the contract’s ASCII token-list rule rather than Python `str.split()` semantics.
Because a raw substring test (`"canonical" in rel`) would also have accepted the NBSP form, the
observed `canonical_missing` additionally rules out substring-based relation matching.

## 4. Operability controls retained

- Determinism: three repeat CLI runs on the attack manifest were byte-identical
  (`cmp` equal), each exit `1`, each stderr 0 bytes.
- No writes: `sha256sum -c` over `manifest.json`/`page.html` passed after the CLI run and the
  fixture directory listing was unchanged (no new files).
- Before/after measurement (read, not re-run): `measure-before.json` at base
  `7c61c8c…` reports `"accepted": 0, "available": false`; `measure-after.json` at
  `c0fd6d5…` contains two runs, both exit 0, `accepted: 32, total: 32, available: true`;
  `matrix-integrated.json` records exit 0, `accepted: 32, total: 32, executed: 32,
  discrepancies: 0`, with the `rel_token_list` row expected/actual exit 0 and
  expected/actual findings `["clean"]`.

## 5. Confidence, limits, remaining unknowns

- Confidence: high for this case and boundary (direct execution, matched one-variable control,
  independent parser-value proof, deterministic repeats).
- Remaining unknowns / outside this attack: the matrix compares only exit code and finding ids,
  not the `verdict` string (observed in `matrix.py`); for this case the actual verdict is also
  `clean`, so nothing is masked here. `findings[].page` serializes the page URL, not the file path;
  the contract requires only a `page` member, so this is not a defect for this case. Static
  explicit-head HTML only, as the contract limits state — no HTTP/JS/rendering behavior was
  exercised, and none was claimed.
