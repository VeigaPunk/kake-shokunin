# Attack03 — frozen case `relative_parent` + nearest-neighbor probe

- Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`
- Observed HEAD: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (integrated candidate)
- Production bytes frozen during this seat. No lane edits by this seat except this report.
  Re-hashed after all probes:
  - `scripts/canonical_audit.py` `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7`
  - `fixtures/relative_parent/manifest.json` `ced8886b688d5a07b00b3440d0a45c546ea85463d4f6f5c7e3424633dd4e5253`
  - `fixtures/relative_parent/page.html` `5db6d44b485346cd91c3cc16d43c37162166417261895e8d52c0e5513b26898a`
- Installs/updates: none. No credentials, network, package transactions, or service calls.

## 1. Frozen case — independent derivation first

Read `cases.json` and `fixtures/relative_parent/`:

- manifest `url`: `https://example.test/project/deep/index.html`
- manifest `expectedCanonical`: `https://example.test/project/a.html`
- page: single `<link rel="canonical" href="../a.html">` inside explicit `<head>`; empty body.

Independent expectation, derived from RFC 3986 §5.2.4 merge + remove_dot_segments (not from tool output):
base path `/project/deep/index.html` → drop last segment → `/project/deep/` → append `../a.html`
→ `/project/deep/../a.html` → remove `deep/..` → **`/project/a.html`** on origin `https://example.test`
→ equals `expectedCanonical`. One canonical link, non-empty href, HTTP(S), no fragment, query equal (both absent).
Therefore: **exit 0, finding set `["clean"]`**.

## 2. Commands and observed output (frozen case)

```
$ python3 .ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case relative_parent
PASS caseId=relative_parent exit=0 findings=clean
SUMMARY selection=relative_parent accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
# exit 0
```

```
$ python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/relative_parent/manifest.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
# exit 0
```

`matrix.py --json` (same run) confirms exact-match acceptance, not exit-only:
`accepted=1, discrepancies=0`, `expectedExit=0 actualExit=0 expectedFindings=["clean"] actualFindings=["clean"]`.
Matrix PASS requires both exact exit and findings (`matrix.py:266-269`).

Cross-check with an independent standards implementation (WHATWG parser, not production code):

```
$ node -e 'console.log(new URL("../a.html","https://example.test/project/deep/index.html").href)'
https://example.test/project/a.html
```

Frozen case verdict: **expected 0/clean, observed 0/clean. No discrepancy. Claim instance survives.**

## 3. Nearest-neighbor fixture (own /tmp tree)

Root: `/tmp/kake-r22-attack03/relative_parent_neighbor/`
Same document URL `https://example.test/project/deep/index.html`; expected `https://example.test/project/a.html`
unless noted. Each page carries exactly one canonical in explicit head.

| manifest | href | independent expectation | observed | exit |
|---|---|---|---|---|
| `manifest.json` | `../../project/a.html` | over-root traversal then re-entry → `/project/a.html` → clean | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |
| `manifest_encoded.json` | `%2e%2e/%2e%2e/project/a.html` | WHATWG: encoded dot segments are parent → `/project/a.html` → clean. RFC 3986 literal reading would be a distinct path (see §4) | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |
| `manifest_selfcancel.json` | `../deep/index.html` | `deep/../deep` → document URL itself → clean | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |
| `manifest_clamp.json` | `../../../project/a.html` | traversal clamps at root (WHATWG and RFC) → `/project/a.html` → clean | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |
| `manifest_wrong.json` | `../../b.html` | → `/b.html` ≠ expected → mismatch, exit 1 | `{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/deep/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}` | 1 |
| `manifest_encslash.json` | `%2e%2e%2F%2e%2e%2Fa.html` | encoded slash is not a segment separator → literal segment, mismatch, exit 1 | `canonical_mismatch`, same shape as above | 1 |
| `manifest_backslash.json` | `..\a.html` | browser resolves parent to expected (see §4), tool says invalid | `{"findings":[{"id":"canonical_url_invalid","page":"https://example.test/project/deep/index.html"}],"pagesChecked":1,"verdict":"failed-policy"}` | 1 |
| `manifest_base_parent.json` | `<base href="https://cdn.test/project/deep/">` + `../a.html`, expected `https://cdn.test/project/a.html` | first head base is the resolution base → clean | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |
| `manifest_relbase_parent.json` | `<base href="/project/deep/">` + `../a.html` | base resolves to same path → clean | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |
| `manifest_bare_enc_parent.json` | `%2e%2e`, expected `https://example.test/project/` | WHATWG: parent segment with trailing slash → `/project/` → clean | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |

Negative controls reject: wrong traversal target and encoded-slash literal both exit 1 with the expected id, so
acceptance is not "any traversal is clean". Traversal against the first head base resolves through the base,
not the document URL.

Additional control: `python3 scripts/canonical_audit.py --selftest` → exit 0; parsed JSON reports
`cases=56 ok=56 failed=[]` (includes a `relative_parent` positive control).
Note: `--selftest --json` is usage error exit 64 by documented CLI shape (`--json` only valid with `--manifest`).

## 4. Residual observations (not claim failures)

1. **Encoded dot segments** (`canonical_audit.py:384-406`) treats `%2e`, `%2e%2e`, `.%2e`, `%2e.`
   (ASCII case-insensitive) as dot segments. That is WHATWG URL behavior, and it matches the node oracle,
   so the clean verdicts above are consistent with how browsers/crawlers actually resolve those hrefs.
   The CLI help, however, calls the tool "a conservative RFC-style subset, not a WHATWG URL implementation";
   under RFC 3986 §5.2.4 those encoded forms are ordinary segments. Documentation and behavior diverge on
   this point. Manifest `url`/`expectedCanonical` are normalized by the same rule, so both sides are symmetric
   and no frozen case verdict is affected; no false-clean was found in the frozen matrix.
2. **Backslash traversal** (`..\a.html`): node/WHATWG resolves this to `https://example.test/project/a.html`
   (special-scheme backslash-as-slash), while the tool rejects any backslash as `canonical_url_invalid`
   (exit 1). This is a documented conservative rejection, but it is a false-failure class for pages whose
   crawler-visible canonical target is correct. It does not contradict the frozen contract (no backslash case;
   help text explicitly says backslashes are rejected) and it fails closed, not open.
3. Scope limits of this check: single-page manifests, no HTTP/redirects/real search-engine selection; all
   assertions are local and offline.

## 5. Verdict

Frozen case `relative_parent` classification **survives**: independent derivation (0/clean), matrix
exact-match PASS (`accepted=1, discrepancies=0`), and public CLI (0/clean) agree. The same parser/policy
boundary also survives over-root traversal, root clamping, self-canceling traversal, base-relative traversal,
encoded-dot traversal (browser semantics), encoded-slash literal rejection, and a wrong-target negative control.
Only residual items are the help-text "RFC-style" claim vs WHATWG encoded-dot behavior, and the conservative
backslash false-failure; neither changes a frozen verdict.

L1 checks to rerun after integration (not run by this seat): full `measure.py` count, full 32-case
`matrix.py`, and `canonical_audit.py --selftest`.
