# Attack01 — frozen case `absolute_match` (round 22, wave 2)

Seat: KakeR22.Attack01 (leaf reviewer). Author-side falsifier, not independent non-author closure.
Measured integrated revision: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (lane HEAD at test time).
Production source/oracle/fixture bytes frozen; no production file edited, no tool installed, no package
transaction, no network access. Scratch data only under `/tmp/kake-r22-attack01/`.

## 1. Independent derivation (before running anything)

Source read: `.ufo/waves/round-22/cases.json` case record, `.ufo/waves/round-22/fixtures/absolute_match/`
and contract line 4 policy text — not the validator output.

Frozen case record:

- `caseId`: `absolute_match`
- `expectedExit`: `0`
- `expectedFindings`: `["clean"]`
- rationale: "Local publisher policy: the absolute canonical URL matches the manifest target exactly."

Fixture (`manifest.json`, `page.html`, digests below):

- manifest: `url = expectedCanonical = https://example.test/project/a.html`, `file = page.html`
- page: `<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a.html"></head><body></body></html>`

Derivation from contract policy ("Exactly one canonical link in explicit head per page … resolve href with
first head base href or document URL; compare WHATWG-like HTTP(S) normalized absolute URL to
expectedCanonical, preserve query, reject fragments and credentials"):

1. Exactly one `<link rel="canonical">` → not `canonical_multiple`; it is inside `<head>` → not
   `canonical_outside_head` / `canonical_missing`.
2. `href` present, non-empty → not `canonical_href_missing`.
3. Absolute `https` URL, no fragment, no credentials, no query → not `canonical_fragment` /
   `canonical_url_invalid`; no `<base>` → document URL is the base.
4. Normalized canonical equals `expectedCanonical` exactly (same scheme/host/port/path, no query) →
   no `canonical_mismatch`.
5. No findings ⇒ verdict clean ⇒ exit 0 (exitMap `0: clean`).

**Derived expectation: exit 0, findings `["clean"]`.**

## 2. Frozen case execution (public harness)

Command:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --case absolute_match
```

stdout:

```
PASS caseId=absolute_match exit=0 findings=clean
SUMMARY selection=absolute_match accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

exit: `0` (harness exit 0 = no discrepancy).

Same command with `--json`:

```json
{"selection": "absolute_match", "accepted": 1, "total": 1, "executed": 1, "discrepancies": 0, "toolMissing": false, "results": [{"caseId": "absolute_match", "status": "PASS", "expectedExit": 0, "actualExit": 0, "expectedFindings": ["clean"], "actualFindings": ["clean"], "stdout": "{\"findings\":[],\"pagesChecked\":1,\"verdict\":\"clean\"}\n", "stderr": ""}]}
```

exit: `0`.

Direct public CLI on the frozen fixture:

```
python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/absolute_match/manifest.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

exit: `0`.

Matches the independent derivation byte-for-byte on verdict, exit and finding id (`clean` = empty findings
array, as the harness renders it).

## 3. Nearest-neighbor fixture (own `/tmp` tree), same parser/policy boundary

Boundary attacked: the contract's "WHATWG-like HTTP(S) **normalized** absolute URL" claim — specifically
ASCII case-insensitivity of the host and default-port elision. Nearest neighbor keeps the frozen fixture's
document URL, expected canonical and element shape identical, and changes only the spelling of the `href`
authority: uppercase host + explicit `:443`.

`/tmp/kake-r22-attack01/nn/manifest.json` (identical to frozen manifest):

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

`/tmp/kake-r22-attack01/nn/page.html`:

```html
<!doctype html><html><head><link rel="canonical" href="https://EXAMPLE.TEST:443/project/a.html"></head><body></body></html>
```

Independent derivation: WHATWG URL serialization lowercases the host and omits a port equal to the scheme
default (`443` for `https`), so the normalized canonical is `https://example.test/project/a.html`; that
equals `expectedCanonical`, therefore **exit 0 / `clean`**. A strict string comparison would wrongly report
`canonical_mismatch`; that is the falsification target.

Reference check (independent implementation of the same standard, not the candidate):

```
node -e 'const u=new URL("https://EXAMPLE.TEST:443/project/a.html"); console.log(u.href, "|", u.host, "|", u.port==="" ? "<empty>" : u.port)'
https://example.test/project/a.html | example.test | <empty>
```

Command and result:

```
python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack01/nn/manifest.json --json
{"findings":[],"pagesChecked":1,"verdict":"clean"}
```

exit: `0`. Matches derivation; claim survives this boundary.

Negative control at the same boundary — non-default `:8443` must **not** be normalized away
(`/tmp/kake-r22-attack01/ctl/`, same manifest, href `https://EXAMPLE.TEST:8443/project/a.html`):

```
python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack01/ctl/manifest.json --json
{"findings":[{"id":"canonical_mismatch","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

exit: `1`. This shows the clean NN result is discrimination, not blanket acceptance.

Determinism: each of the three manifests was run twice; stdout+exit identical across runs (frozen fixture →
clean/0, NN → clean/0, control → canonical_mismatch/1).

## 4. Mechanism observed in source (explains, does not replace, the executed evidence)

`scripts/canonical_audit.py`:

- `_host_and_port` (≈L320–380): rejects `@` credentials, `\`, `%` authority encodings; `ascii_lower`s a
  non-IPv4 host and validates DNS labels.
- `normalize_http_url` (≈L408–455): scheme restricted to `http`/`https`; default port dropped
  (`authority += ":" + str(port)` only when `port != default_port`); dot segments removed; path/query
  quoted with existing escapes preserved.
- `evaluate_page` (≈L539–585): head-base resolution, single-canonical checks, href emptiness, fragment
  (`canonical_fragment`) vs invalid (`canonical_url_invalid`) vs `canonical_mismatch` ordering.

Both NN normalization facets are implemented for a reason, and the control confirms the port exception.

## 5. Verdict

Claim "classifies every frozen matrix case with expected exit and finding id" **survives** for the
`absolute_match` slice: expected and independently derived `exit 0 / clean` are reproduced by both the
frozen harness (`PASS`, discrepancies 0) and the public CLI, deterministically. The normalization boundary
one step away (host case + default port) also holds, with a discriminating negative control at a
non-default port. No regression or discrepancy observed; nothing to escalate for this case.

## 6. Boundaries and remaining unknowns

- Scope is this one frozen case plus the single nearest neighbor and its control. The other 31 frozen cases
  are peers' assignments and are not claimed here.
- Not exercised: HTMLParser edge shapes outside this fixture, non-ASCII/IDNA hosts, IPv6/IPv4 literals,
  and paths with existing percent-escapes. The `%`-authority rejection means percent-encoded hosts are
  intentionally unsupported.
- "WHATWG-like" is the contract's own wording; the validator implements a documented conservative subset,
  so full WHATWG conformance is not asserted.
- Node used only as an external standard reference; not part of the candidate's dependency set.

## 7. Commands and artifacts (reproduction)

```
matrix:  python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py \
           --root /home/vgpnk/Projects/shokunin/kake-shokunin --case absolute_match [--json]
cli:     python3 scripts/canonical_audit.py --manifest <manifest.json> --json
```

Digests at test time:

```
5ca6750bf00571943989846490462ca7bbcf372d1ca0c357145a1abc10971423  .ufo/waves/round-22/fixtures/absolute_match/manifest.json
76bc55f0869acb190d4fd821694acae9c211d4dbcb1462159fdc9b8bd363630d  .ufo/waves/round-22/fixtures/absolute_match/page.html
35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7  scripts/canonical_audit.py
```

Production cleanliness: `git status --porcelain` for `scripts/canonical_audit.py`,
`.ufo/waves/round-22/fixtures`, `.ufo/waves/round-22/cases.json` is empty. This report is the only file
written by this seat (plus `/tmp` scratch). No installs/updates were needed, so none are recorded.

Checks for L1 to run at integration: full 32-case matrix (`matrix.py --root …` without `--case`) and
`canonical_audit.py --selftest`.
