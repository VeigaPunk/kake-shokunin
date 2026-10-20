# HeadBoundary — surgical design review (kake r22, wave 1)

Seat: KakeR22.HeadBoundary (reviewer, read-only). Date: 2026-10-20.
Contract: `.ufo/waves/round-22/contract.json` @ base 7c61c8cc791bde36dd5e3688bdfea2678d90146c. Frozen, unmodified.
Godspeed axes: (1) **boundary correctness** — explicit-head scope never misclassifies a link's side; (2) **finding-id determinism** — every boundary shape maps to exactly one contract vocabulary id + exit; (3) **version honesty** — stdlib parser behavior pinned to the runtime that will execute it.

Tooling directive ledger: no tools installed or updated this session (none needed; pure stdlib + repo reads).

## Scope

Head-boundary policy only: which serialized tokens open/close "explicit head" scope, which `<link rel=canonical>` / `<base>` tokens count inside it, decoy suppression at the boundary (comment / raw-text / template), malformed boundary shapes, and the deterministic mapping to contract finding ids (`canonical_outside_head`, `canonical_missing`, `canonical_multiple`, `canonical_href_missing`, `base_url_invalid`, `html_unsupported`, `input_invalid`).
Not mine (adjacent seats): URL resolution/normalization (URLNormalization), manifest schema (ManifestSchema), file resolution safety (PathTraversal, SymlinkSafety), stdout/exit plumbing (StdoutExit), general parser research (ParserScope), byte-level unsupported-shape attacks (UnsupportedMarkup), static-vs-crawl boundary (CrawlScope).

Status: `scripts/canonical_audit.py` does not exist yet at review time (checked lane `scripts/`: only corpus-contract.mjs, freshness-sweep.mjs, probe-delta.mjs). This is a design review of the Implement slice's stated approach (stdlib HTMLParser, "explicit-head bounded serialized HTML; ignore comments/raw script/template descendants"). **No implementation was run; nothing here claims unseen code passes.**

## Grounded stdlib facts (probed, python3 = 3.14.8, only python3.x on host)

Raw `html.parser.HTMLParser` probes, quoted because every finding below depends on them:

| # | Input shape | Observed tokens |
|---|---|---|
| P1 | `<head>…</head><head><link2></head>` | two full head scopes; link2 emitted as ordinary start |
| P2 | `<head><base …><body><link …>` (head never closed) | `<body>` emitted as plain start while scope "open"; link emitted after it |
| P3 | `<link>` before `<head>` | link before head-start token |
| P4 | `</head><link><body>` (after-head zone) | link outside any head scope |
| P5 | `<script>` never closed | CDATA to EOF; **every later token swallowed** |
| P6 | `<title><link rel=canonical …></title>` | link content arrives as **data**, not a start tag — 3.14 has `RCDATA_CONTENT_ELEMENTS = ("textarea", "title")`; ≤3.12 had no such handling |
| P7 | `<!-- <head><link> -->` | comment event; tags suppressed |
| P8 | `<head/>` | `startendtag`, no scope events beyond it |
| P9 | `<LINK REL="Canonical  INDEX" HREF=…>` | tag/attr names lowercased; **attr values keep case**, incl. internal double space |
| P10 | `<!>` in head | bogus comment (empty), parsing continues |
| P11 | `<template><link></template>` | plain nested tokens, no special parser state |
| P12 | `<script/>` self-closed | `startendtag`, **no CDATA mode** (browser HTML5 would raw-text-swallow to EOF — divergence, see HB-07) |
| P13 | `</SCRIPT>` | upper-case end tag correctly exits CDATA |
| P14 | `</body>` inside head | plain end tag; head scope unaffected (matches HTML5 "ignore") |
| P15 | unterminated comment before head | single comment to EOF; all head content swallowed |

Also grounded: 3.14 `CDATA_CONTENT_ELEMENTS = ("script", "style", "xmp", "iframe", "noembed", "noframes")` — wider than the ≤3.12 `("script","style")`.

## Findings (by severity)

### HB-01 — critical — unclosed `<head>` must be terminated by `<body>` start (and EOF)
A bare scope-flag that only closes on `</head>` leaves in-head=True forever in shape P2, classifying the body canonical as in-head → `body_link` matrix case can false-clean. Required rule set: head scope opens on `<head>` start; closes on `</head>`, on `<body>` **start**, or at EOF (P14 shows `</body>` must **not** close it — HTML5 ignores it there; matching that is correct). Expected mapping: link after implicit close → `canonical_outside_head`, exit 1; nothing about this shape is could-not-evaluate.
Evidence: P2, P14.

### HB-02 — critical — `<head/>` (startendtag) must open and immediately close scope
P8: `<head/>` emits only `startendtag`. A design handling only `handle_starttag` leaves in-head stuck True for the rest of the document → every subsequent link counts in-head → false clean. `handle_startendtag` (or its default delegation) must be routed through the same scope transitions: open, then close. Expected: link after `<head/>` → `canonical_outside_head`, exit 1.
Evidence: P8.

### HB-03 — high — head re-opened after `<body>` start is a no-op
P-F-shape (`</head><body></body><head><link></head>`): browsers ignore a head-start token in body; the canonical there is not honored. Once the first `<body>` start is seen, later `<head>` starts must not reopen scope; links inside → `canonical_outside_head`, exit 1. Without this pin the tool false-cleans a page every browser reads as canonical-less.
Evidence: design rule grounded on HTML5 tree construction; token sequence observable via P4+P2 combination.

### HB-04 — high — repeated head tokens before body: second `<head>` start no-op, first `</head>` closes, stray `</head>` no-op
P1: naive toggling on each head token yields scope thrash and nondeterministic classification of link2. Pin: `<head>` start while already in head → ignore; `</head>` while in head → close; `</head>` while not in head → ignore. Consequence, pinned as the serialized-policy stance: both pre-body head scopes' canonicals are candidates → double-head page yields `canonical_multiple`, exit 1. HTML5 would instead call link2 a body link; verdict direction (reject) is identical, the finding id differs — document this divergence in the script's limitations block, per contract "HTMLParser stdlib limitations must be explicit".
Evidence: P1.

### HB-05 — high — RCDATA/raw-text element sets are version-sensitive; pin ≥3.13 or self-suppress
P6: on 3.14 a canonical inside `<title>` is invisible (RCDATA) — correct. On ≤3.12 the same bytes emit a real start tag → false in-head candidate → false clean. Same class: 3.14's CDATA list gained `xmp/iframe/noembed/noframes`. The audit script MUST either (a) document minimum Python ≥3.13 and assert it at startup, or (b) implement its own title/textarea suppression so behavior is version-independent. Recommendation: (b) — it is ~10 lines and removes the runtime dependence entirely; then state the 3.13+ equivalence in limitations. Expected mapping either way: canonical only inside `<title>` → `canonical_missing`, exit 1 (browser-equivalent: it is text, not a signal).
Evidence: P6 + inspected `RCDATA_CONTENT_ELEMENTS`/`CDATA_CONTENT_ELEMENTS` in installed 3.14.8 source.

### HB-06 — high — template descendants are inert: depth counter, nested + self-closed + stray-end
P11/P-E-shape: `<template>` produces plain tokens; only an explicit depth counter (increment on start/startend? no — startend increments and immediately decrements; increment on start, decrement on matching end) suppresses links inside. Links inside template, even inside head, are NOT canonical candidates and NOT base candidates. Page whose only canonical-shaped link is inside a template → `canonical_missing`, exit 1. `template_decoy` matrix case with an additional real head canonical → clean, exit 0. Stray `</template>` at depth 0 → ignore (never negative).
Evidence: P11, P12-series probes.

### HB-07 — medium — script/style raw-text at the boundary: three pinned sub-cases
- Unterminated `<script>` inside head swallows the remaining document (P5) → all later head signals invisible → `canonical_missing`, exit 1. This is browser-equivalent (HTML5 raw text to EOF) and must NOT be escalated to `html_unsupported`/exit 2.
- Case-insensitive end tag works (P13) → properly closed `script_decoy` with a real in-head canonical → clean, exit 0.
- `<script/>` self-closing divergence (P12): html.parser leaves CDATA mode immediately; HTML5 browsers keep swallowing raw text to EOF. The tool therefore sees signals a browser does not — worst case the tool accepts a page a browser treats as canonical-less. Document in limitations; do not try to emulate (out of static scope). Note the error direction is safe-side-invisible (tool never misses a real in-head canonical because of it); the unsafe direction is only false-clean vs browser semantics, which the limitations block must name.

### HB-08 — medium — rel tokenization: exact token match after ASCII whitespace split, ASCII-case-insensitive
P9: attr values keep author case and internal spacing. Rules: split `rel` value on ASCII whitespace; a link is a canonical candidate iff any token ASCII-case-insensitively equals `canonical`. Must not substring-match (`rel="noncanonical"` is not canonical); empty/absent rel is not canonical; multi-token (`rel="index, canonical"`, `REL="Canonical  INDEX"`) is canonical (`rel_token_list`, `rel_uppercase`, `attr_uppercase` cases). Tag/attr names may be compared lowercased (parser already lowercases them; values must not be lowercased wholesale before tokenizing — harmless for ASCII but the pin avoids Unicode-locale hazards).

### HB-09 — medium — per-page finding precedence and dedupe inside one page
Total, deterministic rules to pin:
- Zero canonical-shaped signals anywhere in head or elsewhere → `canonical_missing`, exit 1.
- Signal(s) outside head, none inside → exactly `canonical_outside_head`, exit 1; `canonical_missing` suppressed (missing is subsumed; avoids double-counted pages in the denominator).
- ≥1 in-head candidate + ≥1 outside-head signal → evaluate the in-head candidate(s) normally AND emit `canonical_outside_head`, exit 1 either way.
- ≥2 in-head candidates → `canonical_multiple`, exit 1. **No href-equality dedupe**: `duplicate_same` and `duplicate_different` both → `canonical_multiple`. Rationale: contract says "exactly one canonical link in explicit head"; two elements are two signals regardless of href equality, and a publishing preflight must not bless a page search engines treat as conflicting.
- `href` attribute absent on an in-head candidate → `canonical_href_missing`, exit 1 (`href_absent`). `href=""` is NOT href-missing — it is an invalid URL → `canonical_url_invalid`, exit 1 (empty string is not a valid absolute canonical). This empty-vs-absent split must be pinned; it is the easiest off-by-one in the id map.
Multiple findings on one page are allowed by the contract shape (findings array, each with id + page); at most one finding per (page, id).

### HB-10 — medium — base boundary
Only the first `<base href>` token inside explicit head scope becomes the resolution base (`first_base`); every later base anywhere is ignored (`second_base_ignored`). A `<base>` outside head, inside a template, or before `<head>` is silently non-resolving and emits **no finding** (contract finding list has no `base_outside_head`; silence is the only contract-consistent behavior). In-head `<base>` without `href` is not the resolving base (first base **with** href). `base_url_invalid`, exit 1, applies only to the chosen in-head base (URLNormalization owns the URL validity itself; the boundary condition — which base is even eligible — is this slice).

### HB-11 — low — boundary shapes never produce exit 2
Every shape in P1–P15 is tokenizable, so the head boundary always classifies; exit 2 (`html_unsupported`/`input_invalid`) belongs to byte-level and manifest-level failures (UnsupportedMarkup / ManifestSchema slices). Cross-slice assumption, one line in the integration contract: exit precedence 2 > 1 > 0 when pages mix classes. Falsifiable consequence: a boundary-only probe suite must never observe exit 2.

### HB-12 — low — `<html>`/`<body>` wrappers are not required
A standalone `<head>…</head>` fragment is evaluable (stdlib emits the same tokens); missing wrappers must not trigger `html_unsupported`. Only scope tokens matter.

## Minimum acceptance / rejection pair

- **Accept**: `relative_same_dir` — canonical in explicit head, resolves to expected → exit 0, findings `[]`. Proves the boundary does not over-reject a plain valid page.
- **Reject**: `body_link` — exit 1, findings exactly `[canonical_outside_head]` and **no** `canonical_missing`. Proves both directions at once: the body link is seen and correctly placed outside, and the suppression rule (HB-09) prevented a phantom second finding.

## Expected stable mapping, boundary subset of the frozen matrix

| case | expected exit | expected finding id | rule |
|---|---|---|---|
| body_link | 1 | canonical_outside_head | HB-01/09 |
| missing_head | 1 | canonical_outside_head | HB-09 (assumes fixture carries a link outside any head; Matrix owns fixture bytes — falsification step R0 asserts this assumption on the fixture, not the tool) |
| duplicate_same | 1 | canonical_multiple | HB-09 no-dedupe |
| duplicate_different | 1 | canonical_multiple | HB-09 |
| comment_decoy | 0 | (none) | P7 suppression + real in-head canonical |
| script_decoy | 0 | (none) | P5/P13 suppression |
| template_decoy | 0 | (none) | HB-06 (real canonical present) |
| first_base / second_base_ignored | per URL | (none, or canonical_mismatch if fixture intends mismatch) | HB-10 |
| href_absent | 1 | canonical_href_missing | HB-09 |
| href_empty | 1 | canonical_url_invalid | HB-09 |

Rows marked "per URL" are co-owned with URLNormalization; this review pins only the scope/eligibility half.

## Bounded falsification recipe (for Matrix/wave-2; NOT executed here — no tests yet)

All offline, stdlib-only, `/tmp/hb-probes/`, no network, no writes outside /tmp. Divergence on any probe = the named HB defect confirmed against real code.

- **R0 (fixture assumption, run against fixtures not tool)**: assert `missing_head` fixture bytes contain a canonical-shaped link and no `<head>` token; assert decoy fixtures contain a real in-head matching canonical. Without R0 the mapping table above is unfounded.
- **R1**: emit 8 boundary probes: `double_head` (P1, expect 1/canonical_multiple), `reopen_head_after_body` (HB-03, 1/canonical_outside_head), `unclosed_head_with_body` (HB-01, 1/canonical_outside_head), `selfclosed_head` (HB-02, 1/canonical_outside_head), `link_between_head_and_body` (P4, 1/canonical_outside_head), `title_wrapped_link` (HB-05, 1/canonical_missing), `template_only_link` (HB-06, 1/canonical_missing), `unterminated_comment_head` (P15, 1/canonical_missing). Run `canonical_audit.py --manifest probes.json --json`; compare exit + id set per page.
- **R2**: run the frozen 32-case matrix; assert the 10 boundary-subset rows above match exit + id exactly (not substring, no extra findings).
- **R3 (negative control for suppression)**: inject `rel="noncanonical"` and `data-rel="canonical"` head links into a copy of a clean fixture; expect still clean (HB-08 substring guard).
- **R4 (version pin)**: run R1 once under the interpreter that measure.py will use; if any 3.13-conditional behavior differs from the pin (HB-05), that alone is a finding.

Cost: 8 probes + 10 assertions + 2 negative controls; seconds of runtime; no lane mutations.

## Residual risk

- Decoy-case semantics live in Matrix's fixture bytes; if a decoy fixture lacks a real in-head canonical, the "clean" expectation inverts to `canonical_missing`. R0 catches this before it wastes an integration cycle. [INFERENCE from case names; fixture bytes not yet written at review time.]
- `duplicate_same` as `canonical_multiple` is the strict-textual reading; a reviewer preferring browser semantics (honored head link) would expect clean. Contract's "exactly one" wording supports strict; flagged so L1 can pin deliberately, not accidentally.
- html.parser does no HTML5 tree construction; any shape not enumerated here (e.g., `<noscript>` variants, foreign content `<svg><link>`) follows raw token scope. SVG-embedded link in head would count in-head under this design; browsers do not honor it. Out of frozen matrix; noted for UnsupportedMarkup's wave-2 attack surface, not a gate for r22.

## Verification gaps

- No implementation existed to inspect; every "expected" row is a design pin, not an observation of `scripts/canonical_audit.py`.
- Stdlib probes were run under python3.14.8 only (sole python3.x on host); HB-05's ≤3.12 claims come from the documented absence of `RCDATA_CONTENT_ELEMENTS` before 3.13, not from an executed ≤3.12 interpreter here.
- Matrix fixtures and measure.py not yet present; R0–R4 unexercised.

— HeadBoundary, read-only review. Report path: `.ufo/waves/round-22/w1/HeadBoundary.md`.
