# ReviewSpotcheckDisposition — routed/carry disposition check (r36 w1)

Scope: every round-35 closure routed defect and Conformance defect, the round-35 lesson
"Carried open" list, and every round-34 carried item → round-36 wave-1 item or `none`.
Sources read: `corpus/lessons/round-35-verifier-spotcheck.md` (Defects i-iii :43-47, Routed
defects 1-5 :183-200), `corpus/lessons/round-35.md` (Carried open :118-132, wave-2 carried
items :167-206), `corpus/lessons/round-34.md` ("Carried open" :119-129), `w1-spec.json`
(36 items, names+targets). Item pointers are w1-spec.json `items[i].name`.

## Round-35 closure — Conformance defects

| defect | w1 item | note |
|---|---|---|
| (i) report's C2-counter-change claim — ruled (:44, ruling :80-91) | ExecCriterionVersionBump | forward fix: v-bump check, r35 v1 vs v2 able-to-fail case |
| (ii) tip entry 1557 > declared 1500 words (:45) | ExecCriterionVersionBump (partial) | cap loosening is covered; the "post-measurement appends are re-measured" half has no item — flag |
| (iii) `0b7779dc` clone held `sealed/c2-probes.json` (:46) | ExecCriterionControlTree | exactly that case as able-to-fail |

## Round-35 closure — Routed defects

| # | defect | w1 item |
|---|---|---|
| 1 | seal what the claim names, not topics; bare id line ≠ cites | ScribeQualityCriteria (drafts criterion (1)); n/a this round — no knowledge-entry claim |
| 2 | no unforced loosening in a version bump | ExecCriterionVersionBump + ScribeQualityCriteria (2) |
| 3 | C1 target slack; seal ≥1 nesting case | ExecCriterionAblation + ReviewAblationDesign (maps ablations to rules, finds uncovered ones); "seal a nesting case" n/a — r36 sealed set is external |
| 4 | control key-blindness | ExecCriterionControlTree + ScribeQualityCriteria (4) |
| 5 | gate-line nits (S084 "whole served body"; S079 cite) | ScribeCorrectionsR35 (both corrections, verbatim) |

## Round-35 lesson — Carried open (:118-132)

| item | w1 item | note |
|---|---|---|
| C2 limits v2: reword passes `copied`, junk rows pass `cites`, truth not probed | none | r36 makes no knowledge claim; `knowledge_control_check.py` exists but no item re-attacks these shapes — flag |
| C1 contract ambiguity (7-8 undecided, link_preview tool) | none | CriticContractAmbiguity attacks the *new* r36 contract, not the carried r35 tool points — flag |
| rule (b) literal vs HTML5 tree builder | none | same carried point, uncovered — flag |
| `CriticSealedDesign` auto-switch hold — not retried | — | honoured; no retry item exists |

## Round-34 carried items (round-34.md:119-129, spotcheck :243-246)

| item | w1 item | note |
|---|---|---|
| C2 counter D1-D4 | — | retired in r35 ("that counter is retired, not reused"); r36 counter is a new C1 design |
| first-og:url-only, template/svg accept | — | closed by r35 C1 repair (24/24 sealed) |
| non-UTF-8 page stops manifest | — | closed by r35 rule (c) |
| Git-pin mutants (runner codes) | none | flag |
| duplicated option tables | none | flag |
| NUL-byte runner crash; `code` null on run-failure | none | flag — ReviewCounterV2 checks r36 counter error exits but not the runner |
| freshness-pins.json re-pin (three values) | none | flag |
| round-31 QUALITY F1-F3 | none | flag |

## Round-35 wave-2 carries appended to the lesson (:167-206)

| item | w1 item | note |
|---|---|---|
| counter-v2 evasions (hidden closers, fences, substring matches, unpinned texts) | — | dispositioned by design: r36 has no knowledge-entry counter; CriticPredicateIdentity audits predicate/constant drift |
| counter crash paths (non-UTF-8 stdout → exit 1 traceback, not 2) | ReviewCounterV2 (partial) | reviews new counter error exits — flag residual |
| `<template/>` self-close; stale comment at link_preview_audit.py:71-72 | none | flag |
| criteria-check false passes (registry_row, control_description, prebuild_leak) | none | flag |

## Flags — defects no item addresses
post-append re-measurement rule (ii); r35 C2 counter evasion shapes (only retired); old
link_preview contract-ambiguity/rule-(b) points; Git-pin mutants; option tables; NUL-byte/
null-code runner crash; freshness-pins re-pin; round-31 F1-F3; criteria-check false passes;
`<template/>` self-close + stale comment. All predate this round's scope (r36 claims only a
new C1 tool), but none has a disposition item in this wave.
