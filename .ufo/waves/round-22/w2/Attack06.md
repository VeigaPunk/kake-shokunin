# Attack06 — frozen case `first_base` (round 22, wave 2)

Seat: KakeR22.Attack06 (leaf attacker). Author-side falsifier, not independent non-author closure.
Measured integrated revision: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (lane HEAD at test time;
`git log -1` observed). Frozen base in shared context `7c61c8cc791bde36dd5e3688bdfea2678d90146c` is the
BEFORE revision. Production source/oracle/fixture bytes untouched; no production file edited, no tool
installed, no package transaction, no network access, no git/jj writes. Scratch data only under
`/tmp/kake-r22-attack06/`.

Evidence digests observed before/after probes (unchanged; read-only use):

```
35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7  scripts/canonical_audit.py
315f76a4c9b9ce5eb51ef85b1e75c58ee8051d952bb6d726bf2670b40fae6c51  .ufo/waves/round-22/fixtures/first_base/page.html
e2c3e28d4a40075c62f254b104dd10940fe74f5784d27bf25606a3ac87cb23b1  .ufo/waves/round-22/fixtures/first_base/manifest.json
```

## 1. Independent derivation (before executing the case)

Sources read: `.ufo/waves/round-22/cases.json` record for `first_base`, the fixture pair, and
`contract.json` policy/interface text; the matrix harness was read only for how it maps observed
findings. Frozen case record:

- `caseId`: `first_base`
- `expectedExit`: `0`
- `expectedFindings`: `["clean"]`
- rationale: "Local publisher policy: resolve the canonical through the first head base href."

Fixture (`fixtures/first_base/`):

- `manifest.json`: `url = https://source.test/from/entry.html`, `file = page.html`,
  `expectedCanonical = https://example.test/project/a.html`.
- `page.html`:
  `<!doctype html><html><head><base href="https://example.test/project/"><link rel="canonical" href="a.html"></head><body></body></html>`

Derivation from frozen contract policy ("Exactly one canonical link in explicit head per page, rel ASCII
case-insensitive token list; resolve href with first head base href or document URL; compare WHATWG-like
HTTP(S) normalized absolute URL to expectedCanonical, preserve query, reject fragments and credentials"):

1. One `<link rel="canonical">` inside an explicit, closed `<head>` → not `canonical_multiple`,
   `canonical_outside_head`, or `canonical_missing`; `href="a.html"` present and non-empty → not
   `canonical_href_missing`.
2. First head base is absolute `https://example.test/project/`, no fragment, credentials, whitespace, or
   backslash → valid base, so not `base_url_invalid`. Effective base equals the base href.
3. RFC 3986/WHATWG path merge of relative `a.html` against `/project/` (trailing slash ⇒ last path
   segment is a directory) yields `/project/a.html`. No query in either input, so no query is carried.
4. Normalized canonical `https://example.test/project/a.html` equals `expectedCanonical` exactly → no
   `canonical_mismatch`. No other finding class applies.
5. No findings ⇒ verdict clean ⇒ exit 0 (exitMap `0: clean`). Matrix alias for the empty findings array
   is `["clean"]`.

**Derived expectation: exit 0, findings `["clean"]`.**

## 2. Frozen case execution (public harness)

Command (exact):

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --case first_base
```

stdout:

```
PASS caseId=first_base exit=0 findings=clean
SUMMARY selection=first_base accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

exit: `0` (harness exit 0 = no discrepancy).

Same command with `--json` (exact stdout):

```json
{"selection": "first_base", "accepted": 1, "total": 1, "executed": 1, "discrepancies": 0, "toolMissing": false, "results": [{"caseId": "first_base", "status": "PASS", "expectedExit": 0, "actualExit": 0, "expectedFindings": ["clean"], "actualFindings": ["clean"], "stdout": "{\"findings\":[],\"pagesChecked\":1,\"verdict\":\"clean\"}\n", "stderr": ""}]}
```

Direct public-CLI probe of the frozen fixture (cwd = lane root):

```
python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/first_base/manifest.json --json
```

stdout:

```
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

exit: `0`. No stderr. Observed behavior equals the independent derivation.

## 3. Nearest-neighbor fixture (own /tmp tree, same boundary)

The attacked boundary is *first head base selection and its use for relative resolution*. One-character
neighbor: remove the trailing slash from the base href so the base path ends in a file-like segment.

Fixture (`/tmp/kake-r22-attack06/nn_base_no_slash/page.html`):

```html
<!doctype html><html><head><base href="https://example.test/project"><link rel="canonical" href="a.html"></head><body></body></html>
```

Independent expectation (RFC 3986 §5.3 merge, same subordinate rule the candidate's own docs claim:
"conservative RFC-style subset"): base path `/project` has no trailing slash, so its last segment is
replaced, yielding `https://example.test/a.html`; a naive base+href concatenation would wrongly yield
`https://example.test/project/a.html`.

Positive-control manifest (`manifest-positive.json`) sets
`expectedCanonical = https://example.test/a.html`.
Negative-control manifest (`manifest-negative.json`) sets
`expectedCanonical = https://example.test/project/a.html` (the naive-prefix URL).

Commands (exact) and observed stdout:

```
python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack06/nn_base_no_slash/manifest-positive.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
EXIT=0

python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack06/nn_base_no_slash/manifest-negative.json --json
{"findings":[{"id":"canonical_mismatch","page":"https://source.test/from/entry.html"}],"pagesChecked":1,"verdict":"failed-policy"}
EXIT=1
```

Both match independent derivation. The negative control confirms the validator actually resolved through
the base and compared a normalized URL instead of rubber-stamping or prefix-joining.

Secondary probe of the same boundary — base appears after the canonical link (document-order
independence of the document base URL):

`/tmp/kake-r22-attack06/nn_base_after_link/page.html`:

```html
<!doctype html><html><head><link rel="canonical" href="a.html"><base href="https://example.test/project/"></head><body></body></html>
```

manifest `expectedCanonical = https://example.test/project/a.html`.

```
python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack06/nn_base_after_link/manifest.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
EXIT=0
```

Matches the HTML document-base-URL rule (first base element with href defines the base for the document,
not only for later siblings) and the contract wording "resolve href with first head base href".
[INFERENCE] The contract does not state ordering explicitly; this probe is interpretive but consistent
with the candidate's lazy, whole-document resolution and with browser behavior.

## 4. Verdict for the frozen case

Claim **survives**. For `first_base` the candidate returns exactly the independently derived exit `0` and
finding set `["clean"]`, with empty stderr; the matrix reports `PASS` and zero discrepancies; the public
CLI on the same fixture agrees. The nearest-neighbor positive/negative control pair shows the first-base
resolution is real (not concatenation, not unconditional acceptance), and the order variant stays clean.

No falsifying observation was found at this boundary, so nothing was changed in production (none of the
three probe directories is inside the lane; all scratch lives in `/tmp/kake-r22-attack06/`).

## 5. Remaining unknowns / not claimed

- Not a full 32-case rerun: the committed matrix-integrated/measure-after evidence is untouched and out
  of this seat's scope; only `first_base` and the /tmp neighbors were executed.
- The candidate's declared conservative subset (usage text) rejects URLs containing whitespace, e.g. a
  hand-written `<base href=" https://example.test/project/ ">`, as `base_url_invalid`, whereas browsers
  trim surrounding spaces. This is explicitly documented ("Credentials, fragments, backslashes,
  whitespace … are rejected"; "not a WHATWG URL implementation"), so it was noted but not scored as a
  contradiction of the frozen policy; it remains an operability edge for whitespace-polluted publisher
  HTML.
- `second_base_ignored` precedence, relative/scheme-relative base hrefs, and base in body/noscript were
  not probed here beyond the order variant; they belong to sibling seats.
- No installs or updates were performed (tooling directive: nothing needed).
