# Attack05 — frozen case `scheme_relative`

Scope: bounded post-integration falsification of the integrated candidate
`c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (lane HEAD). No production edits, no
git/jj writes, no installs, no builds/lint/formatters. Probes live only under
`/tmp/kake-r22-attack05/`.

Frozen-state evidence (after all probes):

- `sha256(scripts/canonical_audit.py)` = `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7`
- `sha256(.ufo/waves/round-22/fixtures/scheme_relative/page.html)` = `acfac8ed0e75b1ec0a7dd94527e1ac106dcbae7d3f9a71f5850bfd9943cc1b1d`
- `sha256(.ufo/waves/round-22/fixtures/scheme_relative/manifest.json)` = `22d403d63b8397174da5a07849f298cf629f6ef9f7f0be522f4e7d052eb9d3ac`
- `git status --porcelain scripts/ .ufo/waves/round-22/cases.json .ufo/waves/round-22/matrix.py .ufo/waves/round-22/fixtures/` → empty.
  (Pre-existing wave2 dispatch artifacts `w2-spec.json`, `wave-inventory.json`, untracked
  `w2/` were already dirty before this seat started and were not touched.)

## 1. Independent derivation of the frozen case (from sources, not output)

Fixture bytes:

- manifest: `url = https://source.test/project/a.html`,
  `file = page.html`, `expectedCanonical = https://example.test/project/a.html`
- page: `<!doctype html><html><head><link rel="canonical" href="//example.test/project/a.html"></head><body></body></html>`

Derivation:

1. Explicit head contains exactly one `<link>`; `rel` = ASCII `canonical` token → one
   in-head canonical. No body/duplicate/base signal.
2. `//example.test/project/a.html` is a network-path (scheme-relative) reference.
   RFC 3986 §3 (relative-ref = `//` authority path-abempty) and WHATWG both inherit the
   **document** scheme, `https`; authority `example.test`; path `/project/a.html`.
   Independent check with WHATWG implementation Node v24.21.0:
   `new URL("//example.test/project/a.html","https://source.test/project/a.html").href`
   → `https://example.test/project/a.html`.
3. Normalization: host already lowercase, no default port, dot segments already removed,
   no query/fragment/credentials → `https://example.test/project/a.html`.
4. Equals `expectedCanonical`. Contract exitMap: clean = 0; matrix maps zero findings to
   `["clean"]` (`observed_findings`).

**Expected: exit 0, findings `["clean"]`.**

## 2. Frozen matrix run

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 .ufo/waves/round-22/matrix.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --case scheme_relative
```

stdout (exit 0):

```
PASS caseId=scheme_relative exit=0 findings=clean
SUMMARY selection=scheme_relative accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

Same run with `--json` (exit 0) reports the child stdout verbatim:
`{"findings":[],"pagesChecked":1,"verdict":"clean"}`.

Result: frozen case **PASS**, and it is a true positive — the fixture expectation is
correct under the stated policy. The claim clause “classifies every frozen matrix case”
survives for this case (1/1 executed, 0 discrepancies).

## 3. Nearest-neighbor A — scheme inheritance under an `http` document

Files (my tree):

`/tmp/kake-r22-attack05/scheme_nn/page.html`
`<!doctype html><html><head><link rel="canonical" href="//example.test/project/a.html"></head><body></body></html>`

`/tmp/kake-r22-attack05/scheme_nn/manifest.json`
`{"version":1,"pages":[{"url":"http://source.test/project/a.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}`

Independent expectation: the network-path reference inherits `http` from the document
(`new URL(...)` → `http://example.test/project/a.html`), which differs from the `https`
expected URL → `canonical_mismatch`, exit 1.

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-attack05/scheme_nn/manifest.json --json
```

stdout (exit 1):

```
{"findings":[{"id":"canonical_mismatch","page":"http://source.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

Control (same page, expected scheme changed to `http`):
`manifest-control.json` → `{"findings":[],"pagesChecked":1,"verdict":"clean"}`, exit 0.

Result: scheme inheritance is genuinely implemented (not hard-coded `https`) and the
mismatch direction is correctly classified. Claim survives this neighbor.

## 4. Nearest-neighbor B — one character from the frozen fixture: empty authority

`href="///project/a.html"` (frozen fixture has exactly `//`). Same document and expected.

Files:

- `/tmp/kake-r22-attack05/scheme_empty_authority/page.html`
  `<!doctype html><html><head><link rel="canonical" href="///project/a.html"></head><body></body></html>`
- `/tmp/kake-r22-attack05/scheme_empty_authority/manifest.json`
  `{"version":1,"pages":[{"url":"https://source.test/project/a.html","file":"page.html","expectedCanonical":"https://source.test/project/a.html"}]}`

Independent expectation:

- WHATWG (Node v24.21.0): `new URL("///project/a.html","https://source.test/project/a.html").href`
  → `https://project/a.html` (special-authority slash skipping makes `project` the host).
  ≠ expected → `canonical_mismatch`, exit 1.
- Strict RFC 3986 §5.2.2: the reference has a **present but empty** authority, so the
  target is `https:///project/a.html` — not a valid HTTP(S) URL → `canonical_url_invalid`,
  exit 1.
- Either reading requires non-zero exit; the tool's own absolute path agrees (below).

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-attack05/scheme_empty_authority/manifest.json --json
```

stdout (exit 0):

```
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

Controls, same directory and CLI:

| manifest | input | exit | stdout |
|---|---|---|---|
| `manifest-control.json` | `//source.test/project/a.html` (explicit host) | 0 | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` |
| `manifest-abs-empty.json` | `https:///project/a.html` (absolute empty authority) | 1 | `{"findings":[{"id":"canonical_url_invalid","page":"https://source.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}` |
| `manifest-whatwg-expected.json` | `///project/a.html`, expected `https://project/a.html` (WHATWG-resolved value) | 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://source.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}` |

The third row is the divergence in the opposite direction: where WHATWG says the
canonical *matches*, the tool reports `canonical_mismatch`; where the canonical is
actually wrong (row 1 above, expected = document URL), the tool reports **clean**.

Propagation through `<base>` (same root cause):

- `base-propagate.html`: `<head><base href="///project/"><link rel="canonical" href="a.html"></head>`,
  document `https://source.test/project/a.html`, expected `https://source.test/project/a.html`.
- WHATWG: base `///project/` → `https://project/`, canonical → `https://project/a.html`
  → mismatch, exit 1.
- Tool: `{"findings":[],"pagesChecked":1,"verdict":"clean"}`, **exit 0**.

Result: **claim does not survive at this one-character neighbor.** A network-path
reference with an empty authority is silently resolved as “no authority” and inherits the
document host, producing a **false clean** (exit 0) for a canonical destination that is
wrong under both WHATWG and RFC 3986. The same input in absolute form
(`https:///project/a.html`) is correctly rejected as `canonical_url_invalid` by the same
normalizer, so the two paths are internally inconsistent.

Root cause (observed, frozen source): `scripts/canonical_audit.py`

- line 419 `initial = urlsplit(raw)` — for `///project/a.html`, `initial.scheme == ""`
  and `initial.netloc == ""`; the empty netloc is never inspected.
- line 427 `candidate = urljoin(base, raw)` — Python's `urljoin` treats the empty netloc
  as “absent” and substitutes the base netloc (`source.test`).
- line 439 `host, port = _host_and_port(parts.netloc)` then sees the inherited non-empty
  authority, so the empty-authority rejection at line 321–322 is never reached for this
  shape.

No finding id in the contract distinguishes this resolution ambiguity; the observable
contract failure is the exit code (0 instead of 1/2) plus a false `clean` verdict.

## 5. Claim verdict

- Frozen case `scheme_relative`: **survives** — expected (independently derived) =
  observed = exit 0 / `clean`; matrix 1/1 accepted.
- Nearest neighbor A (scheme inheritance, `http` document): **survives** — exit 1 /
  `canonical_mismatch`, with a clean control.
- Nearest neighbor B (`///` empty authority, one character from the frozen fixture):
  **falsified** — silent false `clean` (exit 0) where WHATWG requires `canonical_mismatch`
  and RFC 3986 requires rejection; propagates through `<base href>`.

Assessment for operability: medium severity. The 32-case frozen matrix does not cover
this shape, so C1's counted claim is not contradicted, but the settled policy sentence
“compare WHATWG-like HTTP(S) normalized absolute URL” is not true for network-path
references whose authority is empty. Because the tool deliberately fails closed for
HTMLParser ambiguities, this URL-resolver ambiguity should likewise be explicit.

Suggested L1 remediation (not applied; production frozen): before line 427, reject a raw
reference that begins with `//` while `urlsplit(raw).netloc == ""` (→
`canonical_url_invalid`/exit 1), or implement WHATWG slash-skipping so `///project/...`
yields host `project`. Either removes the false clean; choice of finding id is L1's call.

## 6. Residual unknowns / limits

- Node v24.21.0 was used only as an independent WHATWG oracle; it was already installed,
  nothing was installed or updated. No network access used.
- Not probed: `//` alone, `////host`, empty authority with query-only (`//?x`), or
  `base href="///"` with an absolute canonical. Same root cause is likely; not claimed
  as observed.
- `matrix.py` was run against the live lane root read-only; the validator performs no
  writes in normal mode and production hashes are unchanged.
