# ScribeKnowledgeDelta: round-23 parser boundary and live-snapshot handoff

Author-side draft. I did not edit `corpus/knowledge/static-canonical-preflight.md`, any production file, or any lane git state. Independent admission is not claimed.

Candidate: `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc` (base `b5d599e19bead54b96f589444e9ec64cdf67c28a`). Lane HEAD at observation: `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`. `4e7dd1d` touches only `.ufo/waves/round-22/**` and `corpus/QUALITY.md`, so the validator is the same at both. Validator sha256 at the candidate: `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac`.

## Verdict

- Parser change: behaves as the candidate's own usage text states. Selftest passes. I found one fail-open gap that predates round-23 and is not covered by the new text (F3).
- Operability (C2): not met at the candidate revision. `measure_c2.py --revision 4d95d2e…` reports `accepted 0 / total 12`, because the `live/` receipts are untracked. In a scratch-clone simulation with `live/` committed and nothing regenerated, the counter reports `accepted 8 / total 12`. The four failing surfaces are the ones whose stored receipts were produced by the base validator (F1, F2).
- The draft section below is ready for the integrator once the `S###` placeholders are assigned and F1/F2 are handled. Its claims are limited to observed behaviour listed under Checked and held.

## Draft appended section (for the integrator to paste; S### to be assigned)

```markdown
## Round 23: foreign content, void self-closing, live snapshot

Source for the HTML-side rules: S### (HTML Standard, tree construction and
foreign content); S### (HTML Standard, void elements and the self-closing flag);
S### (HTML Standard, the base element and document base URL); S### (HTML
Standard, the "in head" insertion mode and implied head/body closure). Section
numbers are to be verified when the S### IDs are assigned. Parser basis: S026.

This tool still is not an HTML5 tree builder. Round 23 changes only which
body-level constructs are evaluated after an explicitly closed head. Everything
else in "Parser and proof boundaries" holds.

Evaluated after `</head>` (no head still open):

- SVG and MathML subtrees (`<svg>`, `<math>`) that contain no canonical-looking
  link. Their descendants contribute nothing to the canonical decision. A
  self-closed `<svg/>` or `<math/>` opens nothing.
- HTML void elements written self-closed (`<input />`, `<br/>`, `<img />`, and
  the other void elements in the tool's list). They are accepted without an
  implied close. A self-closed non-void element (`<div/>`) stays unsupported.

Still `html_unsupported` (exit 2):

- Any `<svg>` or `<math>` opened before the explicit head closes, including one
  inside `<head>`. The implied-head and foreign-content breakout rules are not
  modelled, so the tool does not guess.
- Any canonical-looking `<link rel="canonical">` inside SVG/MathML, whether it
  is written self-closed or not.
- A foreign element still open at end of input.

Unchanged: a canonical `<link>` in `<body>` outside the head is a policy finding
(`canonical_outside_head`, exit 1), not an unsupported input.

Known gap (open finding F3): a `<base>` element after the closed head is neither
evaluated nor rejected. A publisher must not treat a clean receipt as proof
against a body-level base until F3 is closed.

### Live-snapshot handoff (C2)

1. `python3 scripts/live_snapshot.py --population .ufo/waves/round-23/c2-population.json --out .ufo/waves/round-23/live`
   issues one GET per surface (no cookies, no body, at most 5 redirects, 2 MiB,
   20 s). Per surface it writes `fetch.json`, and `page.html` only for a 2xx
   `text/html` response, plus `manifest.json` and `audit.json`. A non-served
   surface records `{"verdict":"not-served","status":N,"exit":null}`. Network
   access happens only in this step; `canonical_audit.py` stays offline.
2. Re-run the integrated validator over each stored `manifest.json` (no network)
   and write `audit.json` as `{"exit","result"}` so it matches the counter's
   reproduction. Do not refetch to refresh a receipt, because the bytes would no
   longer match `fetch.json`.
3. Commit `live/` at the integrated revision. `measure_c2.py` reads committed
   blobs with `git show <revision>:…`; working-tree files do not count.
4. `python3 .ufo/waves/round-23/measure_c2.py --root . --revision <commit>`.
   Exit 0 requires 12/12.

Expected verdict changes from the base to the candidate validator, computed on
the stored bytes fetched 2026-10-21T06:33Z:

| Surface | Base | Candidate |
|---|---|---|
| ds4cc-primary | could-not-evaluate (html_unsupported) | clean |
| plazir15-ghp | could-not-evaluate (html_unsupported) | clean |
| ds4cc-kimi | could-not-evaluate (html_unsupported) | failed-policy (canonical_missing) |
| burnerchrome-kimi | could-not-evaluate (html_unsupported) | failed-policy (canonical_missing) |
| charter-ghp | clean | clean |
| lucario-ghp | failed-policy (canonical_missing) | failed-policy (canonical_missing) |
| ufo-fsd-kimi-pro | failed-policy (canonical_missing) | failed-policy (canonical_missing) |
| vault-index-kimi | failed-policy (canonical_missing) | failed-policy (canonical_missing) |
| lucario-kimi, plazir15-kimi, plazir27-kimi, charter-kimi | not-served (404) | not-served (404) |

The `canonical_missing` rows are publisher-policy findings, not tool defects.
Those pages carry no `rel="canonical"` link in their bytes. Route them to the
operator; do not weaken the policy.
```

## Findings

### F1 — P1 — operability (C2): live receipts uncommitted, counter 0/12 at the candidate

Exact command: `python3 -B .ufo/waves/round-23/measure_c2.py --root . --revision 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`

Exact output (abbreviated, all 12 rows identical in shape):

```
{"accepted": 0, "revision": "4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc", ... "total": 12, "validatorSha256": "d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac"}
  ds4cc-primary  pass False  problems ['fetch.json or audit.json missing']
  … (all 12 surfaces)
```

Supporting observation: `git status --short -- .ufo/waves/round-23` lists `?? .ufo/waves/round-23/live/` and `?? .ufo/waves/round-23/live-summary.json`. `git ls-tree -r --name-only 4d95d2e… -- .ufo/waves/round-23` contains only the contract, populations, census, and the two `measure_*.py` scripts.

Impacted claim: C2 "every surface has a committed read-only snapshot … and an audit receipt".

Smallest fix: the integrator commits `live/` (fetch.json, page.html, manifest.json, audit.json) at the integrated revision after F2 is resolved. Do not commit `live-summary.json` as a receipt; it is a convenience summary with no counter role.

### F2 — P1 — operability (C2): four stored receipts were produced by the base validator and do not reproduce at the candidate

Evidence: re-running the base and candidate validators on each stored `manifest.json` (`python3 -B <validator> --manifest <dir>/manifest.json --json`) reproduces the stored `audit.json` exactly under the base validator for all 8 served surfaces. Under the candidate, these four change:

- ds4cc-primary: base `exit 2 html_unsupported` → candidate `exit 0 clean`
- plazir15-ghp: base `exit 2 html_unsupported` → candidate `exit 0 clean`
- ds4cc-kimi: base `exit 2 html_unsupported` → candidate `exit 1 canonical_missing`
- burnerchrome-kimi: base `exit 2 html_unsupported` → candidate `exit 1 canonical_missing`

Simulation, not a lane change: in a scratch clone (`/tmp/kake-r23-ScribeKnowledgeDelta-sim-dQcQ/clone`, commit `32255a8`, which exists only there) I committed the `live/` tree and ran `measure_c2.py --revision HEAD`. Output: `"accepted": 8, "total": 12`. The four failures are exactly the four rows above, for example:

```
ds4cc-primary False clean ["audit.json {'exit': 2, 'result': {... 'html_unsupported' ...}} != reproduced {'exit': 0, 'result': {'findings': [], ... 'verdict': 'clean'}}"]
```

Impacted claim: C2 reproducibility. The counter compares `audit.json` to a re-run of the revision's validator, and that is the reason it does not accept these four.

Smallest fix: regenerate those four `audit.json` files offline from the stored `manifest.json` and `page.html` under the integrated validator, then commit. The fix is a receipt refresh, not a change to the validator. The two `canonical_missing` results are then honest policy findings for the operator (see the table above). Do not edit the policy to clear them.

### F3 — P2 — parser boundary: a `<base>` after the closed head is silently accepted (pre-existing at base)

Parser location: `canonical_audit.py` candidate, `handle_starttag` post-head branch (around lines 276–283). It handles `tag == "head"`, `"body"`, and `"link"`, and has no `base` branch. `base` is recorded only inside `head_open` (lines 265–269). The `noscript` branch rejects `base`, but the body branch does not.

Exact command and output (candidate, the fixture is written into a scratch directory):

```
fixture: <head><link rel="canonical" href="a.html"></head><body><base href="https://other.test/x/"><p>x</p></body>
URL https://example.test/project/a.html, expected https://example.test/project/a.html
CAND: exit=0 clean []
```

Base gives the same `exit=0 clean []`, so this is not a round-23 regression. It is inside the boundary the round-23 text describes, though: the text says only explicit, properly closed head markup is evaluated, and it cannot be assumed that a relative head canonical resolved against the document URL is what a browser would use when a body base is present. The HTML-side rule (S### document base URL) must be checked before this is stated as a browser fact. The tool does not run a browser. [INFERENCE] under the HTML base-URL rule, a body base may change the resolution of the head canonical; that is not verified here.

Impacted claim: "fails closed" for base outside head.

Smallest fix (integrator): in the post-head `handle_starttag` branch, add `if tag == "base": self.unsupported = True`, and add a selftest fixture with a body base expecting `html_unsupported`. I did not implement this.

### F4 — P3 — live_snapshot.py: validator failures abort the run without a summary

`audit()` calls `subprocess.run(..., timeout=60)` and `json.loads(done.stdout)` without a guard. A timeout or a non-JSON stdout raises out of `main()` and the summary is never printed; earlier surfaces keep their receipts, and later ones are not written. Smallest fix: catch `subprocess.TimeoutExpired` and `json.JSONDecodeError` in `audit()` and record a `{"verdict":"could-not-evaluate","exit":null,"error":…}` receipt. Not verified by execution; read from source only.

### F5 — policy findings for the operator (not tool defects)

- lucario-ghp: `canonical_missing`. The property map's basis is "lucario GHP is canonical," but the stored bytes have no `rel="canonical"` link.
- ufo-fsd-kimi-pro and vault-index-kimi: `canonical_missing` with a self-canonical policy basis.
- ds4cc-kimi and burnerchrome-kimi: `canonical_missing` (their mirror and self-canonical policies). Previously hidden behind `html_unsupported`.

## Checked and held

- Selftest, candidate: `python3 -B canonical_audit.py --selftest` (scratch copy of `git show 4d95d2e:scripts/canonical_audit.py`) → exit 0, output ends `"passed": true`. Base selftest also exit 0 with `"passed": true`.
- Boundary fixtures, base vs candidate (each run via `--manifest … --json`, URL `https://example.test/project/a.html`, expected the same URL):

| Fixture | Base | Candidate |
|---|---|---|
| plain head canonical, `<p>` in body | clean | clean |
| `<svg>` before `<head>` | html_unsupported (exit 2) | html_unsupported (exit 2) |
| `<svg>` inside open head | html_unsupported | html_unsupported |
| `<svg viewBox><path d/></svg>` in body after head, no link | html_unsupported | clean |
| `<math><mi>x</mi></math>` in body after head | html_unsupported | clean |
| `<svg><link rel=canonical href=evil/></svg>` (not self-closed) after head | html_unsupported | html_unsupported |
| `<svg><link rel=canonical href=evil/></svg>` (self-closed link) after head | html_unsupported | html_unsupported |
| `<svg><title></svg><link rel=canonical href=evil></body>` | not run | html_unsupported |
| `<svg><p><link rel=canonical href=evil></p></svg>` | not run | html_unsupported |
| `<svg><![CDATA[<link rel=canonical href=evil>]]></svg>` | not run | html_unsupported |
| `<svg><g></body>` (unclosed) | html_unsupported | html_unsupported |
| `<svg/><link rel=canonical href=evil>` in body | not run | failed-policy canonical_outside_head (exit 1) |
| `<template><svg><link rel=canonical href=evil/></svg></template>` after head | not run | clean (template descendants contribute nothing) |
| `<input type=checkbox /><br/><img src=a.png />` after head | html_unsupported | clean |
| `<input type=checkbox><br>` (no slash) after head | clean | clean |
| `<meta charset=utf-8/>` in open head | clean | clean |
| `<br/>` in open head | html_unsupported | html_unsupported |
| `<div/>` after head | html_unsupported | html_unsupported |
| `<base href=https://other.test/x/>` in body after head | clean | clean (F3) |

- Live snapshot, stored receipts: the 8 manifests in `live/` (burnerchrome-kimi, charter-ghp, ds4cc-kimi, ds4cc-primary, lucario-ghp, plazir15-ghp, ufo-fsd-kimi-pro, vault-index-kimi). Re-running the base validator reproduces each stored `audit.json` exit and result. The other four surfaces are `not-served` 404s with no manifest.
- Stored `fetch.json` metadata: all 12 have `method` GET and `fetchedAt` 2026-10-21T06:33:03Z–06:33:20Z. That is before the candidate commit (06:36Z), consistent with F2.
- Served status: ds4cc-primary, plazir15-ghp, charter-ghp, ds4cc-kimi, burnerchrome-kimi, vault-index-kimi, ufo-fsd-kimi-pro, lucario-ghp all 200. lucario-kimi, plazir15-kimi, plazir27-kimi, charter-kimi all 404.
- Foreign-content bypass shapes (title breakout, `<p>` breakout, CDATA, unclosed svg) all fail closed. No head canonical was reachable through them.
- Per-page parser state (candidate, stored bytes): none of the 8 served pages has `foreign_depth`, `template_depth`, `noscript_depth`, or `raw_head_element` left open at the end, and none reports `unsupported` from the parser itself. The base's four `html_unsupported` receipts trace to body constructs the base rejects and the candidate accepts, found by a grep of each page after `</head>`: ds4cc-primary and ds4cc-kimi contain self-closed `<br/>` and `<input/>`; plazir15-ghp contains a body `<svg>` plus self-closed `<img/>`, `<input/>`, `<path/>`, `<rect/>`, `<circle/>`; burnerchrome-kimi contains a body `<svg>`. The grep is a heuristic, not parser output; the parser-level causes were not isolated per element.

## Limits

- No browser run. The HTML-side claims (foreign-content breakout, void self-closing, the base-URL rule) are reasoning about the HTML Standard, not observed browser output. They are marked `[INFERENCE]` in the text. Each S### source must be opened and its section checked before the S### placeholders are assigned.
- The F3 browser effect is not tested. It is only a fail-open in the tool.
- The C2 simulation is a scratch clone (`/tmp/kake-r23-ScribeKnowledgeDelta-sim-dQcQ/clone`, commit `32255a8`). It is evidence for the counter's behaviour only and must not be integrated.
- `live_snapshot.py` was read, not executed. I did not run it, because it issues network GETs and the stored snapshot is current for this round.
- `measure_c1.py` was not run; C1 is outside this scribe's assignment.
- Scratch files live under `/tmp/kake-r23-ScribeKnowledgeDelta-*`. Nothing was written under the lane except this report.
- Tooling: no tools were installed or updated. Pacman was not used.
