# UnsupportedMarkup — critic report on claim C1

Seat: `KakeR22.UnsupportedMarkup` (critic, leaf, read-only). Axis: operability.
Milestone: offline-canonical-capability. Frozen contract:
`.ufo/waves/round-22/contract.json` @ base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
SCORECARD and `corpus/lessons/round-21-verifier-spotcheck.md` read: operability
sits at the 10/10 saturation line; C1 may only enter a *capability* row, never a
numeric move, and only if the capability actually runs (AXES.md rule cited in
SCORECARD §Capabilities). The r21 verifier's own method — re-measure with an
independent counter over committed blobs, verify byte preservation, re-open
sources — is the bar this attack assumes.

## Attack surface assigned

Where markup the stdlib `html.parser.HTMLParser` cannot model lets the
validator silently emit a wrong verdict instead of `html_unsupported` (exit 2)
or a correct policy finding. Distinct from sibling seats: `HeadBoundary` owns
head-region policy semantics, `ParserScope` owns parser-selection design,
`Matrix`/`Measure` own fixture/counting mechanics, `Filesystem*`/`PathTraversal`/
`SymlinkSafety` own input-path safety. This report owns **markup classes whose
grammar the tokenizer diverges on**, and the `html_unsupported` escape-hatch
itself.

## Empirically verified divergences (python3 = CPython 3.14.8, lane host)

Each was executed locally; these are facts, not speculations:

| # | Markup | HTMLParser observed | Browser-correct per HTML5 | Validator consequence if unguarded |
|---|---|---|---|---|
| D1 | `<head><noscript><link rel=canonical href=B></noscript><link rel=canonical href=A></head>` | emits link B **and** link A starttags | with scripting enabled (default in readers/screenshot pipelines), noscript content is raw text → only A | false `canonical_multiple`; or **false clean** when the *only* canonical is inside noscript — worst direction |
| D2 | `<head><template><link rel=canonical href=B></template><link rel=canonical href=A></head>` | emits B and A | template contents are a separate DocumentFragment, not document children | `template_decoy` fails as `canonical_multiple` instead of pass; naive head-scanner false-green |
| D3 | `<head><svg><link rel=canonical href=B></svg><link rel=canonical href=A></head>` | emits B and A | the svg `<link>` is an SVG-namespaced element, not HTML `link` | false `canonical_multiple`; `<svg>`-wrapped-only page → false clean |
| D4 | `<head><img src=x><link rel=canonical href=A></head>` | link inside head region | spec closes head implicitly at `<img>`; link lands in body → `canonical_outside_head` | literal `</head>` scanner says clean; **contract ambiguity** — "explicit head" must decide serialized-region vs spec-DOM and declare it |
| D5 | `<link rel="canonical" rel="nofollow" href=…>` | attrs list keeps **both** rel pairs in order | spec: first attribute occurrence wins → link IS canonical | `dict(attrs)` last-wins → rel=nofollow → false `canonical_missing`. First-wins dict construction is required |
| D6 | `<link rel="can&#111;nical" href=…>` | attrs arrive pre-unescaped as `rel=canonical` | same | **correct** behavior, but only if implementation relies on parser attrs; a raw-regex/attr-string implementation silently misses it. Also `&Tab;`→tab inside href (urlsplit strips ASCII whitespace — a live divergence) |
| D7 | `<![CDATA[<link rel=canonical …>]]>` in head | swallowed to first `>` as unknown_decl | bogus comment in HTML content → same | correct by accident; inside `<svg>` CDATA would be literal text — still swallowed to first `>`. Divergence must be documented |
| D8 | `<link rel="canonical" href="x <link rel="canonical" href="y">` | one link, `href="x <link rel="` | same quoting rules | correct; good — but proves attr-value `<` handling only holds via HTMLParser, never via regex |
| D9 | `<title>`/`<textarea>` contents | **not tokenized** on 3.14 (`RCDATA_CONTENT_ELEMENTS`) | RCDATA raw text → same on 3.14 | **version trap**: `RCDATA_CONTENT_ELEMENTS` is new in Python 3.14; on older interpreters the same fixture emits a spurious link → false green. The capability's verdicts are interpreter-version-dependent unless the validator forces RCDATA handling itself or pins the version |
| D10 | `</script>` inside a JS string | ends script element early | spec-identical | not a defect — list to preempt a false "fix" |

## Falsifiable acceptance constraints (wave-1 gate)

C1's capability is falsifiable and must not be admitted unless all hold:

- **AC1 — no dodge via could-not-evaluate.** For every frozen matrix case the
  observed (exit, primary finding id) equals the frozen expectation.
  `html_unsupported`/exit-2 is an acceptable observed outcome only where the
  case is *defined* as an unmodelable-markup case — and none of the 32 named
  cases is so defined. If `cases.json` freezes exit 2 for `template_decoy`,
  `script_decoy`, `comment_decoy`, or `missing_head`, the matrix itself is
  self-falsified: the capability would be green while never proving it can
  reject the exact signals it exists to police.
- **AC2 — `html_unsupported` is real and correctly routed.** ≥1 selftest
  fixture provably produces it, with exit **2**, never 1. `input_invalid`
  (manifest/IO/encoding failures) and `html_unsupported` (markup the parser
  cannot model) must be distinct finding ids; an undecodable-bytes file is
  `input_invalid`, not a markup complaint.
- **AC3 — declared-boundary list is load-bearing.** The contract requires
  "HTMLParser stdlib limitations must be explicit." Concrete minimum: a doc
  enumerating D1–D4 (noscript/scripting-mode, template, foreign content,
  implicit head closure) plus the D9 interpreter-version note, each mapped to
  "detected → `html_unsupported`" or "accepted divergence, rationale". An
  undetected divergence is a defect; an unlisted accepted one is an overclaim.
- **AC4 — dup-attribute first-wins.** `<link rel="canonical" rel="nofollow">`
  must not degrade to `canonical_missing`; attr dict construction must keep the
  first occurrence (spec order).
- **AC5 — no traceback.** No input byte string produces a traceback or nonzero
  exit outside {0,1,2,64}. Empty file → `canonical_missing` (it is parseable
  markup with no canonical), not `html_unsupported`.
- **AC6 — independence.** matrix.py's expected ids/exits must not be derived
  from canonical_audit.py's output on the same fixture (author-side
  self-agreement). measure.py must materialize fixtures from git blobs
  (`--revision`), not working tree, matching the r21 verifier's committed-blob
  method.
- **AC7 — capability row, not axis move.** SCORECARD may gain a Capabilities
  row + `operability 10→10 (HOLD)` only; any numeric delta or
  "operability improved" beyond bounded-local is an overclaim at the declared
  saturation line.
- **AC8 — write-free proof.** Same byte-level state-digest guard pattern as
  r20/r21 (state sha identical before/after run), since the capability's
  premise is "read-only local validator".

## Overclaims to reject

1. "Classifies every frozen matrix case" + any `html_unsupported` answer on a
   named case → the claim's own "0 accepted cases → all classified" wording is
   violated; reject unless cases.json independently justifies it.
2. "Explicit-head" read as spec-DOM correctness: the tool can only see the
   serialized head region; D4 means it diverges from browser head membership.
   Any report text implying browser-equivalent canonical extraction → reject.
3. "HTMLParser limitations explicit" satisfied by a docstring while D1/D2/D3
   miscount silently → reject; limitations must be *behaviorally* handled
   (detect-and-exit-2) or the divergence enumerated with rationale.
4. Selftest-only evidence: `--selftest` proves the CLI wiring, not the frozen
   matrix; 32/32 on author-agreement fixtures is the capability, not selftest.
5. "No writes" by assertion: require the digest-before/after run, as r21's
   verifier required committed-blob provenance rather than lane-script trust.
6. Green by population collapse: if `pagesChecked` < manifest page count or
   findings are deduplicated so `canonical_multiple` cannot fire, the count is
   cosmetic (overlaps `PopulationDenominator`'s seat — flag for integration).
7. Any freshness-adjacent framing (e.g., "verifies live canonicals") → reject:
   contract limits forbid network freshness; this is policy comparison only.

## Distinct wave-2 attack (assigned follow-up, not wave-1 work)

**Adversarial-markup battery against the landed validator.** Build a fixture
pack of D1–D9 plus: non-UTF-8/UTF-16 page bytes, NUL-in-tag, unterminated tag
at EOF, CDATA-in-svg, `<noscript>`-only canonical (false-green direction),
5–20 MB oversized input, duplicate-attribute both orders. Pre-register each
fixture's expected (exit, id) *before* the wave-2 validator exists — freezing
expectations post-hoc is the r20 false-green failure mode. Required outcome:
every fixture yields its frozen (exit, id) or `html_unsupported`/exit-2;
**zero** false clean, zero traceback, zero exit outside {0,1,2,64}. Add the
r16-style byte-identical digest guard around the run. Kill test: invert one
expectation (e.g., call template_decoy clean) and confirm the matrix turns red —
a matrix that cannot go red is not evidence.

## Smallest safe corrections

- Extend `html.parser` minimally rather than replace it: track a
  `template`/`svg`/`noscript` depth stack; suppress link/base events at
  depth>0, or emit `html_unsupported` when the suppressed element carried
  `rel=canonical`. This is ~30 lines and converts D1–D3 from silent miscounts
  into declared outcomes.
- Decide "explicit head" = serialized head region, state D4 as a named
  accepted divergence, and add one fixture proving the declared reading.
- Build attr dicts first-occurrence-wins (D5).
- Emit `html_unsupported` on `HTMLParser` `error`/exception or non-UTF-8
  decode failure → exit 2, distinct from `input_invalid` (AC2/AC5).

## Boundaries

Read-only: no code was run against the (not-yet-landed) validator; all parser
facts were reproduced on the host's CPython 3.14.8 in-memory. No files outside
this report written; no installs. Findings are author-side; independent
admission remains with the non-author verifier per r21 precedent.

Trailer: `.ufo/waves/round-22/w1/UnsupportedMarkup.md`
