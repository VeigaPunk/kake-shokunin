# Attack22 — fragment_url boundary falsification (Kake r22, wave2)

Seat: KakeR22.Attack22 · frozen candidate c0fd6d53906a42dadfb997ddda2c8162f1adb78a · production untouched (read-only lane; probes in /tmp/kake-r22-attack22).

## 1. Independent derivation (before any run)

Fixture `fixtures/fragment_url/`: manifest target `https://example.test/project/a.html`, page canonical `href="#section"`.
Contract policy: "resolve href with first head base href or document URL; compare WHATWG-like HTTP(S) normalized absolute URL … reject fragments". Resolving `#section` against the document URL yields `https://example.test/project/a.html#section` — fragment present → policy **reject**.
**Derived expectation: exit 1, finding `canonical_fragment`** (from contract.json + cases.json rationale only; not read off any actual output).

## 2. Frozen matrix case

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 .ufo/waves/round-22/matrix.py --root . --case fragment_url
PASS caseId=fragment_url exit=1 findings=canonical_fragment
SUMMARY selection=fragment_url accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
EXIT=0
```

Matches derivation. Control (instrument not vacuously passing):

```
$ python3 .ufo/waves/round-22/matrix.py --root . --case absolute_match
PASS caseId=absolute_match exit=0 findings=clean
SUMMARY selection=absolute_match accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
EXIT=0
```

**Frozen-case claim survives.**

## 3. Nearest-neighbor probes (same parser/policy boundary, public CLI)

Implementation boundary: raw scan `if "#" in raw: raise URLFragment` in `normalize_http_url` (scripts/canonical_audit.py:410-411), *before* resolution; document-side `URLFragment`→`canonical_fragment` (:581-582); manifest-side `expectedCanonical` normalization at :637 falls to the generic `ValueError` catch → `input_invalid`; base-with-fragment → `base_url_invalid` (:561).

| probe | page canonical (vs target `…/a.html`) | derived expectation | observed |
|---|---|---|---|
| expected_fragment | href `…/a.html#section`; expectedCanonical `…/a.html#section` | fragment must be rejected; contract ambiguous: `input_invalid`(2) or `canonical_fragment`(1); clean/mismatch would falsify | `{"findings":[{"id":"input_invalid","page":"…/a.html"}],"pagesChecked":0,"verdict":"could-not-evaluate"}` EXIT=2 |
| empty_fragment | href `…/a.html#` | WHATWG `#` = non-null empty fragment → `canonical_fragment`(1) | `{"findings":[{"id":"canonical_fragment",…}],"verdict":"failed-policy"}` EXIT=1 |
| encoded_fragment | href `…/a%23b.html` | `%23` is literal path bytes, not a fragment → clean(0) | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` EXIT=0 |
| base_fragment | `<base href="…/index.html#frag">` + `href="a.html"` | WHATWG HTML strips base fragment → resolves to `…/a.html` → clean(0); conservative-subset reading: `base_url_invalid`(1) | `{"findings":[{"id":"base_url_invalid",…}],"verdict":"failed-policy"}` EXIT=1 |

Probe command shape (each):
```
$ python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack22/<probe>/manifest.json --json
<stdout above> EXIT=<code>
```

## 4. Verdict

**Claim C1 survives this attack.** No probe produces a wrong classification under the contract's declared conservative subset; the frozen case and both controls behave exactly as independently derived.

Boundary observations (residual risk, none falsifying within stated limits):
1. **Manifest-side fragment classifies as `input_invalid` (exit 2), not `canonical_fragment`** — defensible (the target itself is malformed), and the signal is still rejected, but the finding id differs from the document-side path; contract does not pin this.
2. **Base href carrying a fragment is rejected (`base_url_invalid`, exit 1) whereas WHATWG browsers strip the base fragment and would accept the page.** Explicitly disclaimed in the tool's `--help` ("conservative RFC-style subset, not a WHATWG URL implementation"; "invalid first base is base_url_invalid, not browser fallback"), so it is a documented limitation, not a contract violation.
3. `pagesChecked=0` on input findings is consistent across probes; no over-broad false positive (encoded `%23` stays clean).

## 5. Verification gaps

- Only selections `fragment_url` + `absolute_match` of the matrix were run from this seat; full 32-case sweep belongs to the integration owner.
- Probe 4's WHATWG-divergence is judged against declared help text, not a browser runtime (out of scope, network/browser runs forbidden).
