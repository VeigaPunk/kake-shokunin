# Attack16 — frozen case `body_link` (offline static canonical preflight)

Seat: leaf author-side falsifier. Read-only wrt production; only this report written in the lane.

## Target identity

- Integrated candidate measured revision (live lane HEAD observed): `c0fd6d53906a42dadfb997ddda2c8162f1adb78a`
  (`git rev-parse HEAD`, subject `round-22: offline canonical publishing preflight`).
- Before base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`: `git ls-tree` for
  `scripts/canonical_audit.py`, `.ufo/waves/round-22/matrix.py`, `.ufo/waves/round-22/cases.json`
  returned no entries, i.e. the capability under test did not exist at base. This is the
  before/after control; no base checkout was created and no git writes were issued.
- Frozen bytes used (sha256): validator `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7`;
  fixture `page.html` `eb19bf0416fa250a263c9f142ebf5969e31b46f3c9a87ca1b6de462a1020ac28`;
  fixture `manifest.json` `5ca6750bf00571943989846490462ca7bbcf372d1ca0c357145a1abc10971423`.
  Scoped `git status --porcelain` over validator/cases/matrix/fixtures: empty (unchanged).

## Independent derivation (before observing output)

`fixtures/body_link/page.html`:

```
<!doctype html><html><head><title>Canonical is outside head</title></head><body><link rel="canonical" href="https://example.test/project/a.html"></body></html>
```

`manifest.json` requires one page with document URL and `expectedCanonical` both
`https://example.test/project/a.html`.

Contract policy: exactly one canonical link in an **explicit head** per page; a canonical
`link` in the body is outside the required explicit head. The body link's href matches the
expected canonical, but placement alone is the violation (`body_link` rationale in
`cases.json`). Therefore the required classification is finding id `canonical_outside_head`,
verdict failed policy, exit **1** with empty stderr. `canonical_mismatch`/`canonical_missing`
are not applicable because the structural outside-head signal dominates and the head link is
absent-by-design. No other finding is warranted (head is explicit and closed; title text is
inside a raw-text title element; no base present).

## Exercise 1 — frozen matrix case

Command (exact):

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin --case body_link
```

Observed (exit of matrix itself = 0):

```
PASS caseId=body_link exit=1 findings=canonical_outside_head
SUMMARY selection=body_link accepted=1 total=1 executed=1 discrepancies=0 tool_missing=0
```

Repeat run with `--json` produced byte-identical rows twice (deterministic):

```json
{"selection":"body_link","accepted":1,"total":1,"executed":1,"discrepancies":0,"toolMissing":false,"results":[{"caseId":"body_link","status":"PASS","expectedExit":1,"actualExit":1,"expectedFindings":["canonical_outside_head"],"actualFindings":["canonical_outside_head"],"stdout":"{\"findings\":[{\"id\":\"canonical_outside_head\",\"page\":\"https://example.test/project/a.html\"}],\"pagesChecked\":1,\"verdict\":\"failed-policy\"}\n","stderr":""}]}
```

Direct public-CLI control on the frozen fixture:

```
python3 scripts/canonical_audit.py --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/fixtures/body_link/manifest.json --json
EXIT=1
stdout={"findings":[{"id":"canonical_outside_head","page":"https://example.test/project/a.html"}],"pagesChecked":1,"verdict":"failed-policy"}
stderr=<empty>
```

## Exercise 2 — nearest-neighbor fixtures (own /tmp tree)

Tree: `/tmp/kake-r22-attack16/<probe>/{manifest.json,page.html}`. Each manifest is the
contract shape with `url=expectedCanonical=https://example.test/project/a.html`. Probe HTML
and the independently derived expectation precede the observed result. All runs used:

```
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py \
  --manifest /tmp/kake-r22-attack16/<probe>/manifest.json --json
```

with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`; stderr was empty for every probe.

| probe | HTML core (after `<head>`/`</head>`) | derived | observed exit | observed findings | match |
|---|---|---|---|---|---|
| `nn0_body_link_exact` | frozen fixture reproduced verbatim | exit 1 `canonical_outside_head` | 1 | `canonical_outside_head` | yes |
| `nn1_head_and_body_same` | head has valid canonical + body has same canonical | exit 1 `canonical_outside_head` (conflicting signals rejected; one in head but a second outside it) | 1 | `canonical_outside_head` | yes |
| `nn2_between_head_body` | valid head canonical + `link` immediately after `</head>`, before `<body>` | exit 1 `canonical_outside_head` (outside explicit head, no body needed) | 1 | `canonical_outside_head` | yes |
| `nn3_template_in_body` | valid head canonical + `<body><template><link rel=canonical href=https://wrong.test/></template></body>` | exit 0 clean (inert template content is not an active canonical, consistent with `template_decoy`) | 0 | none (`verdict:"clean"`) | yes |
| `nn4_textarea_rawtext` | no head canonical + `<body><textarea><link rel=canonical href=…></textarea></body>` | exit 1 `canonical_missing` (raw-text content is text, not an element) | 1 | `canonical_missing` | yes |
| `nn5_upper_selfclose` | no head canonical + `<body><LINK REL='alternate CANONICAL' HREF='…' /></body>` | exit 1 `canonical_outside_head` (attr/tag ASCII case-insensitive; token list; void self-close) | 1 | `canonical_outside_head` | yes |
| `nn6_open_head_body` | `<head><link rel=canonical …><body><link rel=canonical …>` (no `</head>`) | exit 2 `html_unsupported` per documented closed-head limitation (open head is not evaluable) | 2 | `html_unsupported` | yes |
| `nn7_body_javascript` | no head canonical + body link `href=javascript:alert(1)` | outside-head is structural; expected exit 1 `canonical_outside_head` (URL validity not reachable) | 1 | `canonical_outside_head` | yes |
| `nn8_body_invalid_base` | broken head `<base href="https://[broken">` + body canonical, no head canonical | both `base_url_invalid` and outside-head are true; exit 1 expected, id ordering under-determined | 1 | `base_url_invalid` | exit yes / id precedence |
| `nn9_body_href_absent` | no head canonical + `<body><link rel=canonical></body>` | outside-head dominates missing href; expected exit 1 `canonical_outside_head` | 1 | `canonical_outside_head` | yes |
| `nn10_body_comment` | no head canonical + body comment containing `link` markup | exit 1 `canonical_missing` (comment is not an element) | 1 | `canonical_missing` | yes |

## Findings

1. **Frozen claim survives.** `body_link` is classified exactly as independently derived:
   exit 1, sole finding `canonical_outside_head`, clean stderr, matrix PASS twice with
   identical bytes. The detection path is the parser's `outside_canonicals` list, populated
   for `link` elements after `</head>` (including between head and body), and evaluated
   before the missing/mismatch URL checks.
2. **Boundary is placement-based, not body-based.** `nn2` shows a canonical between
   `</head>` and `<body>` is also rejected. `nn3` shows inert `<template>` content in body
   is correctly ignored (clean positive control preserved). `nn4`/`nn10` show raw-text and
   comment decoys do not fabricate links.
3. **Observation (not a falsification): violation precedence is single-id and partly
   unspecified.** With an additional independent violation the tool emits one id:
   `base_url_invalid` before outside-head (`nn8`), outside-head before URL validity
   (`nn7`) and before missing href (`nn9`). Exit is 1 in all cases. The frozen contract does
   not state multi-violation precedence, and no frozen case combines signals, so this is an
   under-determined ordering choice, not a contradiction of C1.
4. **Observation (not a falsification): omitted `</head>` yields exit 2.** A browser closes
   head implicitly at `<body>`, so a real publisher page with an unclosed head produces
   `html_unsupported` rather than the body-link finding (`nn6`). The validator's help text
   and module docstring state "closed head markup with supported head children is
   evaluated", i.e. this is an explicit, declared HTMLParser-shape limitation required by
   the contract, and it does not touch the frozen fixture (which closes head).
5. **Read-only discipline held.** No production/oracle/fixture bytes changed (scoped status
   clean, sha256 recorded above); all scratch data lives in `/tmp/kake-r22-attack16`; the
   matrix and CLI runs perform no writes and no network access was observed.

## Verdict for C1 (`body_link` slice)

Claim **survives**: the frozen case's expected exit and finding id are independently
reproduced, the same parser/policy boundary rejects 7 of 7 nearest-neighbor outside-head
shapes with exit 1, and clean/decoy neighbors stay clean or classify as inert/missing
without false outside-head findings.

## Remaining unknowns

- Multi-violation precedence (base vs outside-head; URL-invalid/fragment vs outside-head;
  href-missing vs outside-head) is not frozen by the contract; only exit code is pinned.
- Whether the closed-head-only policy is acceptable for real publisher corpora is a product
  decision, already declared in the tool's own documentation and outside this case's frozen
  shape.
- No whole-matrix or measure rerun was performed here (outside this ticket's authorization);
  existing `measure-before.json`/`measure-after.json` remain the L1 evidence base.

## Installs

None. No package, tool, service, or environment change was made for this task.
