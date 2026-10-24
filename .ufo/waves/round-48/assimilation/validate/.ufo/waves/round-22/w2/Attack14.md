# Attack14 — frozen case `duplicate_same` (round 22, wave 2)

Seat: `KakeR22.Attack14` (leaf scout). Author-side falsifier; not independent non-author closure.
Measured integrated revision: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a` (`git rev-parse HEAD` at test time).
Production source/oracle/fixture bytes frozen throughout. No production file edited, no tool installed,
no package transaction, no service, no network. Scratch only under `/tmp/kake-r22-attack14/`; the only
live-lane write is this report.

## 1. Independent derivation (before running the case)

Sources read: `.ufo/waves/round-22/cases.json` (record), `contract.json` line 4 policy and exitMap,
`.ufo/waves/round-22/fixtures/duplicate_same/{manifest.json,page.html}`, and the parser/`evaluate_page`
in `scripts/canonical_audit.py` (read for mechanism, not as the source of the expectation).

Frozen case record:

- `caseId`: `duplicate_same`
- `expectedExit`: `1`
- `expectedFindings`: `["canonical_multiple"]`
- rationale: "Local publisher policy: reject multiple canonical links even when their destinations agree."

Fixture:

- `manifest.json`: `url = expectedCanonical = https://example.test/project/a.html`, `file = page.html`
- `page.html` (185 bytes):
  `<!doctype html><html><head><link rel="canonical" href="https://example.test/project/a.html"><link rel="canonical" href="https://example.test/project/a.html"></head><body></body></html>`

Derivation from the contract policy ("**Exactly one** canonical link in explicit head per page, rel ASCII
case-insensitive token list; resolve href … compare … to expectedCanonical"):

1. Fixture has **two** `<link rel="canonical">` elements, both inside the explicit `<head>`, both with
   `rel` token `canonical` (exact-case here). Policy quantifier is "exactly one", so two is a violation
   irrespective of whether the two `href` values are equal. Equality of destinations is a red herring for
   this case — the rationale and the quantifier both say the duplicate itself is the defect.
2. Therefore a policy failure, not a could-not-evaluate: exit `1` (exitMap `1: failed policy`).
3. Finding id must name the multiple-canonical condition. The freeze names it `canonical_multiple`
   (corroborated by sibling id vocabulary `canonical_missing`, `canonical_outside_head`), and the frozen
   expectation is `["canonical_multiple"]` only — no mismatch finding, because under this policy the
   duplicate is rejected before destination equality is even the deciding signal.

**Derived expectation: exit `1`, findings exactly `["canonical_multiple"]`.**

## 2. Frozen case execution (public harness)

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --case duplicate_same
```

stdout:

```
PASS caseId=duplicate_same exit=1 findings=canonical_multiple
SUMMARY selection=duplicate_same accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

exit: `0` (harness exit 0 = no discrepancy).

Same command with `--json`:

```json
{"selection": "duplicate_same", "accepted": 1, "total": 1, "executed": 1, "discrepancies": 0, "toolMissing": false, "results": [{"caseId": "duplicate_same", "status": "PASS", "expectedExit": 1, "actualExit": 1, "expectedFindings": ["canonical_multiple"], "actualFindings": ["canonical_multiple"], "stdout": "{\"findings\":[{\"id\":\"canonical_multiple\",\"page\":\"https://example.test/project/a.html\"}],\"pagesChecked\":1,\"verdict\":\"failed-policy\"}\n", "stderr": ""}]}
```

exit: `0`.

Direct public CLI on the frozen fixture (cwd = lane root):

```
python3 scripts/canonical_audit.py --manifest .ufo/waves/round-22/fixtures/duplicate_same/manifest.json --json
{"findings":[{"id":"canonical_multiple","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

exit: `1`; stderr empty.

Matches the independent derivation on exit, verdict and finding id. Harness and direct CLI agree
byte-for-byte on the embedded stdout.

## 3. Nearest-neighbor fixtures (own `/tmp` tree), same parser/policy boundary

Boundary attacked: **counting canonical link *elements* vs. counting canonical *signals*** — i.e., the
duplicate rule must be lexical/tree-based (two distinct link elements), must not collapse merely because
destinations agree, and must not fire on inert or attribute-level repetition. Every fixture below uses the
identical manifest to the frozen case; only `page.html` shape changes. Exact exit was read with
`rc=0; cmd || rc=$?` immediately after the command (not after an `echo`).

Tree: `/tmp/kake-r22-attack14/<name>/{manifest.json,page.html}`.

| NN | `page.html` head (manifest target `https://example.test/project/a.html`) | Derived | Observed exit | Observed stdout |
|---|---|---|---|---|
| `nn_selfclosing` | two canonical links, second written `<link … />` self-closing | multiple → 1 / `canonical_multiple` | `1` | `{"findings":[{"id":"canonical_multiple","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}` |
| `nn_token_list_dup` | one `rel="canonical"`, one `rel="alternate CANONICAL"`, same href | multiple → 1 / `canonical_multiple` | `1` | same `canonical_multiple` JSON |
| `nn_comment_between` | two canonical links separated by `<!-- second copy -->` | multiple → 1 / `canonical_multiple` | `1` | same `canonical_multiple` JSON |
| `nn_base_between` | `<base href="/project/">` then `href="a.html"` + absolute same target | multiple → 1 / `canonical_multiple` | `1` | same `canonical_multiple` JSON |
| `nn_second_href_missing` | canonical with href, second `<link rel="canonical">` with **no** href | multiple → 1 / `canonical_multiple` (multiple precedes href validation) | `1` | same `canonical_multiple` JSON |
| `nn_body_sibling` | one canonical in head, one identical in body | one in head but outside-head signal → 1 / `canonical_outside_head` | `1` | `{"findings":[{"id":"canonical_outside_head",…}],"pagesChecked":1,"verdict":"failed-policy"}` |
| `nn_template_inert` | one real canonical + one **inside `<template>`** in head | template contents inert → 1 canonical element → 0 / clean | `0` | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` |
| `nn_dup_attrs` | **single** `<link>` with duplicated `rel`/`href` attributes (first-wins: `canonical` / target) | one element → 0 / clean | `0` | `{"findings":[],"pagesChecked":1,"verdict":"clean"}` |

Interpretation:

- The duplicate rule is element-count based and destination-blind: agreeing hrefs (`selfclosing`,
  `token_list_dup`, `comment_between`, `base_between`) still fail as `canonical_multiple`. This is exactly
  the frozen case's claim, including the "even when their destinations agree" clause.
- Precedence is deliberate and observable: `canonical_multiple` is decided before href presence/validity
  (`nn_second_href_missing` → multiple, not `canonical_href_missing`), so the reject cannot be laundered by
  giving the duplicate an unusable href.
- Discrimination holds in the other direction: inert template content and same-element duplicate
  attributes do **not** manufacture a false `canonical_multiple` (both clean exit 0). The duplicates rule
  is not a blanket "any two strings 'canonical' on the page".

Negative control at the same boundary: `nn_body_sibling` has two identical hrefs but only **one** head
canonical, and the tool reports the placement-specific id `canonical_outside_head` (exit 1) rather than
`canonical_multiple`. That confirms the multiple-id is keyed to the head-element count, not to duplicate
destination text.

Ordering nuance observed (documented, not escalated): with an invalid first `<base>` plus two identical
head canonicals, `nn_invalid_base_dup` yields `base_url_invalid` exit `1` — the base-resolution failure is
reported before the multiple check. The page is still rejected (failed-policy), so admission is unchanged;
only the id precedence differs. The frozen matrix has no invalid-base+duplicate case, so no frozen case is
contradicted.

Determinism: `nn_template_inert`, `nn_dup_attrs`, and the matrix case were each run twice; stdout bytes
identical across runs
(`nn_template_inert`/`nn_dup_attrs` sha256 `10cb9056…5fe3f9`; matrix run sha256 `4fa388fc…09b11e`).

## 4. Mechanism observed in source (explains, does not replace, executed evidence)

`scripts/canonical_audit.py`:

- `_record_link` (≈L164–168) appends every `link` whose first-wins attribute map satisfies
  `is_canonical_relation` (ASCII-lower token list contains `canonical`) to `head_canonicals` when inside
  head, `outside_canonicals` otherwise. It does not compare hrefs at record time.
- `evaluate_page` (≈L556–561) returns `canonical_multiple` when `len(parser.head_canonicals) > 1`, **before**
  `canonical_outside_head`, `canonical_missing`, href-emptiness and URL normalization; base resolution
  (`base_url_invalid`) runs earlier still (≈L552–556). This is the exact precedence measured above.
- `handle_startendtag` (≈L250–255) routes void elements (including `link`) through `handle_starttag`, so
  self-closing duplicates count once each (`nn_selfclosing`). `handle_starttag` early-returns on non-zero
  `template_depth` (≈L171–178), so template descendants never reach `_record_link` (`nn_template_inert`).
- `attrs_first_wins` (≈L125–131) collapses duplicate attributes before relation checking
  (`nn_dup_attrs` / selftest `duplicate_attrs_first_wins`).

Selftest cross-check (public CLI, `/tmp` scrape): 56 cases, `all_ok=True`, including
`duplicate_same {exit 1, canonical_multiple}` and `duplicate_different {exit 1, canonical_multiple}`.

## 5. Verdict

Claim "rejects multiple canonical links even when destinations agree" for `duplicate_same`
**survives**. Independently derived `exit 1 / canonical_multiple` is reproduced by the frozen harness
(`PASS`, discrepancies 0, 32-case contract slice intact) and by the public CLI directly, deterministically.
The same boundary holds in both directions in the nearest neighborhood: agreeing duplicates still fail,
while inert-template and duplicate-attribute shapes stay clean. No discrepancy to escalate for this case.

## 6. Boundaries and remaining unknowns

- Scope is this frozen case plus the eight `/tmp` neighbors and one ordering probe. The other 31 frozen
  cases are peers' assignments and are not claimed here.
- Not exercised: SVG/MathML-namespaced links, more than two canonicals, and non-UTF-8 encodings.
  `nn_noscript_head` (probed here) gave exit `2` with
  `{"findings":[{"id":"html_unsupported","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"could-not-evaluate"}`:
  the parser deliberately fails closed on canonical links inside `<noscript>`, the documented
  `HTMLParser`/scripting-flag limitation rather than a silent classification.
- The invalid-base+duplicate precedence (`base_url_invalid` over `canonical_multiple`) is noted above; it
  does not change admission, only which failed-policy id is reported.
- Author-side result only; L1 owns integration and admission.

## 7. Commands and artifacts (reproduction)

```
matrix:  python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py \
           --root /home/vgpnk/Projects/shokunin/kake-shokunin --case duplicate_same [--json]
cli:     python3 scripts/canonical_audit.py --manifest <manifest.json> --json
selftest:python3 scripts/canonical_audit.py --selftest
NN:      /tmp/kake-r22-attack14/nn_{selfclosing,token_list_dup,comment_between,base_between,
         second_href_missing,body_sibling,template_inert,dup_attrs,invalid_base_dup}/manifest.json
```

Digests at test time:

```
35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7  scripts/canonical_audit.py
5ca6750bf00571943989846490462ca7bbcf372d1ca0c357145a1abc10971423  .ufo/waves/round-22/fixtures/duplicate_same/manifest.json
38b6a54e96dcd68618273fe41c51ee344c1bc8c97f8c35388fb9618b296c5aea  .ufo/waves/round-22/fixtures/duplicate_same/page.html
28a49013d3aaf72b0e1c3801fd5359592602e079408d9a71c99f2df03d1cbeb6  .ufo/waves/round-22/cases.json
```

`git status --porcelain` over `scripts/canonical_audit.py`, `.ufo/waves/round-22/fixtures`,
`.ufo/waves/round-22/cases.json`, `.ufo/waves/round-22/contract.json`: empty. Installs/updates: none
(no tool needed), hence none recorded.

Checks for L1 at integration: full 32-case matrix (`matrix.py --root …` without `--case`),
`canonical_audit.py --selftest`, and (if desired) re-run `measure.py` on the frozen revision.
