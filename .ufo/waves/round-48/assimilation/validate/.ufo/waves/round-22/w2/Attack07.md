# Attack07 — frozen case `second_base_ignored` (wave 2 falsification)

Author-side falsifier, leaf, post-integration bounded checks only.
Candidate under test: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (live lane HEAD).
BEFORE reference (contract base, tool absent): `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Production source/oracle/fixture bytes unmodified. No tool installs, no builds/lint/tests, no
network. Only this report written in the lane; scratch fixtures under `/tmp/kake-r22-attack07`.

## Frozen inputs

`cases.json`:
`{"caseId":"second_base_ignored","expectedExit":0,"expectedFindings":["clean"],"rationale":"Local publisher policy: ignore later base href elements after the first head base."}`

Fixture `.ufo/waves/round-22/fixtures/second_base_ignored/`:

manifest: `{"version":1,"pages":[{"url":"https://source.test/from/entry.html","file":"page.html","expectedCanonical":"https://example.test/project/a.html"}]}`

page.html:
`<!doctype html><html><head><base href="https://example.test/project/"><base href="https://wrong.test/elsewhere/"><link rel="canonical" href="a.html"></head><body></body></html>`

## Independent derivation (before running the case)

Contract policy: "resolve href with first head base href or document URL".

1. Head is explicit and closed; only supported head children present (`base`, `base`, `link`),
   no raw-text/foreign/template/noscript content → `finish_supported()` true.
2. `scripts/canonical_audit.py:230-234` records the base only when `href` is present and
   `base_seen` is false; later `base` elements are ignored for both resolution and validation.
   So effective base = `https://example.test/project/`; `https://wrong.test/elsewhere/` is inert.
3. Single head canonical, non-empty href `a.html`; no fragment.
4. `urljoin("https://example.test/project/", "a.html")` →
   `https://example.test/project/a.html`, which equals the normalized `expectedCanonical`.
5. No findings → verdict `clean`, exit 0.

**Independently derived expectation: exit 0, finding id `clean`.**

## Required run — frozen case

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 .ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --case second_base_ignored
```
stdout:
```
PASS caseId=second_base_ignored exit=0 findings=clean
SUMMARY selection=second_base_ignored accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```
exit `0`.

Direct public CLI on the frozen fixture:
```
python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/second_base_ignored/manifest.json --json
```
stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}`, exit `0`.

Observed matches the independent derivation. Post-hoc corroboration only: the committed
`matrix-integrated.json` row records the same `PASS ... actualExit 0 ... ["clean"]`.

## Nearest-neighbor fixture (own /tmp tree, same base-selection boundary)

Primary fixture `/tmp/kake-r22-attack07/nn-second-base-invalid/` — one-token perturbation:
keep the first base valid, make the **later** base syntactically invalid. Claim under test:
later head base elements are fully inert, not merely lower priority. A parser that validated
every base would return `base_url_invalid`.

manifest same as frozen fixture (url `https://source.test/from/entry.html`, expected
`https://example.test/project/a.html`), page.html:
`<!doctype html><html><head><base href="https://example.test/project/"><base href="http://[invalid"><link rel="canonical" href="a.html"></head><body></body></html>`

Expected (derived first): exit 0, `clean`.

Run:
```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
python3 scripts/canonical_audit.py --manifest /tmp/kake-r22-attack07/nn-second-base-invalid/manifest.json --json
```
stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}`, exit `0`. Matches expectation.

### Controls (same boundary, prove the observation is not vacuous)

| Fixture | Perturbation | Expected (derived) | Observed stdout | Exit |
|---|---|---|---|---|
| `control-first-base-invalid` | first base invalid `http://[invalid`, second base valid/matching | `base_url_invalid` | `{"findings":[{"id":"base_url_invalid","page":"https://source.test/from/entry.html"}],"pagesChecked":1,"verdict":"failed-policy"}` | 1 |
| `nn-base-without-href` | first `<base>` has no href, second base matching | `clean` (first base *with href* wins) | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |
| `control-base-without-href` | first `<base>` no href, second base `https://wrong.test/elsewhere/` | `canonical_mismatch` | `{"findings":[{"id":"canonical_mismatch","page":"https://source.test/from/entry.html"}],"pagesChecked":1,"verdict":"failed-policy"}` | 1 |
| `nn-selfclosing-base` | `<base href="…project/" />` then wrong base | `clean` (self-closing void base honored) | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |
| `control-selfclosing-base` | self-closing first base wrong, second matching | `canonical_mismatch` | `{"findings":[{"id":"canonical_mismatch","page":"https://source.test/from/entry.html"}],"pagesChecked":1,"verdict":"failed-policy"}` | 1 |
| `nn-second-base-empty-href` | first base matching, second `<base href="">` | `clean` (later empty href must not overwrite) | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` | 0 |

All observed exits/stdout equal the pre-run expectations. The control rows show the base
selection and invalid-base paths are live: swapping the first base flips the verdict, so the
primary `clean` is a real suppression of the later base, not an unvalidated/ignored base path.

## Before/after control on the capability itself

`git -C … cat-file -e 7c61c8…:scripts/canonical_audit.py` →
`fatal: path 'scripts/canonical_audit.py' exists on disk, but not in '7c61c8…'`
(`BASE_TOOL_ABSENT`). The BEFORE revision has no lane-owned runnable validator, consistent with
the claim's before-statement. AFTER (`c0fd6d5`), the frozen case and the nearest-neighbor
fixture both classify as derived.

## Verdict

**Claim survives this attack.** For `second_base_ignored` the frozen case passes with the
independently derived exit/id (0/`clean`); the nearest-neighbor case confirms later head base
elements are inert even when invalid; the paired controls confirm first-base selection and
`base_url_invalid` are enforced rather than skipped.

Remaining unknowns / notes (non-blocking):
- Rationale wording "after the first head base" vs contract wording "first head base href":
  the implementation selects the first base **carrying** `href` (spec-consistent); probes
  `nn-base-without-href`/`control-base-without-href` show that reading. Under the contract
  wording this is conformant; only the frozen rationale sentence is looser.
- Scope remains explicit-head static HTML only; no claim about browsers, JS, HTTP, or search
  engine selection was exercised.
- Live-lane `git status` additionally shows orchestrator wave files (`w2-spec.json`,
  `wave-inventory.json` modified; `w2-dispatch.json`, `measure-after.json`, `w2/` untracked);
  no production file differs and this seat did not write any of them.
- `scripts/__pycache__/canonical_audit.cpython-314.pyc` is also untracked in the lane. It is not
  attributable to this seat's checks: all commands here execute the file as `__main__` or via
  `matrix.py`'s subprocess (also `__main__`), and an isolated `/tmp` control copying the script
  and running it produced no `__pycache__`. It was presumably emitted by a concurrent seat
  importing the module; left untouched.
