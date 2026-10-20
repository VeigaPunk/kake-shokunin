# Attack13 — frozen case `missing_link` (author-side falsifier, wave2)

Seat: KakeR22.Attack13 (leaf, no dispatch). Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Frozen integrated candidate / measured revision: `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`
(`git log -1` = `c0fd6d5 round-22: offline canonical publishing preflight`).
Before revision (shared-context base): `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Interpreter: Python 3.14.8 (`/usr/lib/python3.14/html/parser.py`).
No production files changed; no installs were needed or performed.

## 1. Independent pre-run derivation (not read from output)

Fixture bytes (`sha256` page.html `30ea12af…f777`, manifest `5ca6750b…1423`):

- manifest: one page, `url` = `expectedCanonical` = `https://example.test/project/a.html`, `file` = `page.html`
- page: `<!doctype html><html><head><title>No canonical link</title></head><body></body></html>`

Contract policy: "Exactly one canonical link in explicit head per page".
`<head>` is present and explicitly closed; `<title>` is legal head content and is
raw text, so its text contributes no elements. There is no `<link>` at all in head
and none outside head. Therefore zero canonical links are recognized:

- not `html_unsupported` (exit 2): explicit head exists, is closed, and the shape is
  supported (`missing_head` is the absent-head case);
- not `canonical_href_missing`: no canonical element exists to inspect;
- not `canonical_outside_head` / `canonical_multiple`: empty sets of both;
- → `canonical_missing`, a failed-policy verdict → exit 1.

Prediction: exit **1**, findings **["canonical_missing"]**. (This agrees with the
frozen cases.json record and was derived before execution.)

Code path confirmed afterwards (read-only): `evaluate_page` returns
`canonical_missing` at `if not parser.head_canonicals:` (`scripts/canonical_audit.py:567-568`),
guarded by `finish_supported()` requiring `head_seen`/`head_closed`.

## 2. Frozen case execution

Command:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --case missing_link
```

Exit `0`; stdout:

```
PASS caseId=missing_link exit=1 findings=canonical_missing
SUMMARY selection=missing_link accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

Direct public-CLI control on the frozen fixture (`cwd` = lane root, `--json`):

```
python3 scripts/canonical_audit.py \
  --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/missing_link/manifest.json --json
```

Exit `1`; stdout, byte-exact:

```
{"findings":[{"id":"canonical_missing","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
```

stderr: empty. Observed = predicted on both exit and finding id.

## 3. Nearest-neighbor fixture (own /tmp tree, same parser/policy boundary)

Tree `/tmp/kake-r22-Attack13/<probe>/{manifest.json,page.html}`; every manifest is the
same single page (`https://example.test/project/a.html`, expected identical). Each probe
was run with the public CLI:

```
python3 <lane>/scripts/canonical_audit.py --manifest /tmp/kake-r22-Attack13/<probe>/manifest.json --json
```

| probe | page.html body (head only) | independently expected | observed exit | observed stdout verdict/findings | survives? |
|---|---|---|---|---|---|
| **nn_template_only** (primary) | `<template><link rel="canonical" href="https://example.test/project/a.html"></template>` | exit 1, `canonical_missing` (inert template descendant contributes no link) | 1 | `failed-policy`, `["canonical_missing"]` | yes |
| nn_rel_substring | `<link rel="canonicalx" href="https://example.test/project/a.html">` | exit 1, `canonical_missing` (rel is an exact ASCII token, not substring) | 1 | `failed-policy`, `["canonical_missing"]` | yes |
| nn_noncanonical_links | `<link rel="stylesheet" href="…"><link rel="alternate" href="…">` | exit 1, `canonical_missing` (only `canonical` token counts) | 1 | `failed-policy`, `["canonical_missing"]` | yes |
| nn_nbsp_token | `<link rel="canonical\u00a0alternate" href="…">` | exit 1, `canonical_missing` (NBSP is not ASCII-whitespace separator) | 1 | `failed-policy`, `["canonical_missing"]` | yes |
| control_active_canonical | `<link rel="canonical" href="https://example.test/project/a.html">` | exit 0, clean | 0 | `clean`, `[]` | yes (control) |
| nn_title_then_link | `<title>No canonical link</title><link rel="canonical" href="…matching…">` | exit 0, clean (title raw text does not swallow the following link) | 0 | `clean`, `[]` | yes (control) |
| nn_title_markup_only | `<title>No canonical link</title>` | exit 1, `canonical_missing` | 1 | `failed-policy`, `["canonical_missing"]` | yes |
| nn_title_text_decoy | `<title><link rel="canonical" href="…matching…"></title>` | exit 1, `canonical_missing` (markup text inside title is inert) | 1 | `failed-policy`, `["canonical_missing"]` | yes |

Primary neighbor verdict: a canonical-looking link that exists only inside an inert
`<template>` is **not** counted; the tool returns the same `canonical_missing`/exit 1
outcome expected for a genuinely absent canonical. No false-accept (`clean`) and no
fail-closed drift to `html_unsupported` was observed on any neighbor.

## 4. Before/after controls

- **Before** `7c61c8cc…`: `git cat-file -e 7c61c8c:scripts/canonical_audit.py` → exit 128,
  "exists on disk, but not in `<base>`"; the harness reports `tool_missing`.
  `measure-before.json`: `accepted: 0`, `available: false`.
- **After** frozen revision `c0fd6d53…`: `measure-after.json` records two runs of the same
  instrument, each `accepted: 32/32`, `deterministic: true`, `sameInstrumentAsBefore: true`,
  `sourceCommit: c0fd6d53906a42dadfb997ddda2c8162f1adb78a`.
  This seat re-ran only `--case missing_link` (authorized check), not the full matrix.

## 5. Freeze / no-write evidence

- `git diff --stat HEAD -- scripts .ufo/waves/round-22/cases.json .ufo/waves/round-22/fixtures .ufo/waves/round-22/matrix.py`
  → empty (exit 0).
- Frozen `missing_link` fixture mtimes still `2026-10-20 18:40:48` (pre-run).
- `git status --porcelain` shows only pre-existing lane meta changes
  (`w2-spec.json`, `wave-inventory.json`, `measure-after.json`, `w2-dispatch.json`, `w2/`);
  no production/fixture modification was authored by this seat.
- All scratch output is confined to `/tmp/kake-r22-Attack13/`; the CLI ran read-only in
  normal mode (no writes, no network).

## 6. Verdict

**Candidate C1 survives the frozen `missing_link` case and the nearest-neighbor probes.**
Observed exit and finding id match the independently derived expectation exactly
(`1` / `canonical_missing`); the matrix row is `PASS`; the freeze of production bytes holds.
This is a case-scoped result only and does not re-admit the other 31 cases beyond the
frozen `measure-after.json` record.

Falsifiers that were tested and did **not** fire: false `clean` accept from template-only,
substring-rel, non-canonical-rel, or NBSP-token decoys; unsupported (exit 2) drift for an
explicit closed head; global "always missing" behavior (positive/title controls returned
`clean`).

## 7. Residual unknowns / limits

- Only the missing/recognition boundary was probed; duplicate/outside-head/href and URL
  normalization branches were not re-exercised here.
- Python 3.14.8 `html.parser` semantics are the observed basis; cross-interpreter behavior
  was not measured.
- Full-matrix re-execution (32 cases) was intentionally not repeated in this seat; the
  frozen `measure-after.json` two-run record is the aggregate evidence.
