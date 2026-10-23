# CriticContractAmbiguity — public C1 contract review

Axes: freshness and operability. Static criticism only; no implementation or round verdict.

## Deliverable

- `/fast/scratch/hyaku/kake-r36w1/CriticContractAmbiguity/ambiguity.json`
- 47 concrete inputs; each contains exact manifest text/UTF-8 bytes, body bytes in hex, two readings with expected reports/exits, a decider or `undecided`, evidence, and a smallest correction.
- One filesystem-dependent input also specifies an entirely in-directory symlink fixture.
- All proposed outputs are explicitly `[INFERENCE]`, not observed executions.
- SHA-256: `7b6be0a4b47f0b271e0d797a22000cac934793f2a089cd9d0bd199e59df89ce3`.

| Primary bullet | Inputs | Undecided | Resolved by text/source |
|---|---:|---:|---:|
| (a) Final status | 4 | 1 | 3 |
| (b) Redirects | 6 | 2 | 4 |
| (c) HTML text | 11 | 4 | 7 |
| (d) Quote match | 4 | 0 | 4 |
| (e) Media types | 5 | 2 | 3 |
| (f) Decoding | 7 | 2 | 5 |
| (g) Input faults | 8 | 7 | 1 |
| Verdict | 2 | 0 | 2 |
| Total | 47 | 18 | 29 |

## Strong counterexamples and smallest safe corrections

All JSON line pointers below refer to the absolute ambiguity.json path above.
- **G08, line 2756:** final `hops:[{"status":200}]`, readable matching body. The displayed hop schema includes `location:string`, but the prose specifically requires it on redirects. Readings: clean/0 versus check_invalid/2. Clarify whether location is optional on non-redirect hops. Contract: frozen SCORECARD lines 1606–1610.
- **E01, line 1578:** final 200, `application/pdf; charset=not-a-label`. Readings: unsupported_type only/1 versus unsupported_type plus charset_unsupported/2. State whether unsupported media types skip decoding entirely. Contract: 1611–1613, 1633–1644.
- **F06, line 2209:** body byte `80`, quote euro, `text/plain; charset=utf-8; charset=windows-1252`. First-wins yields quote_missing/1; last-wins yields clean/0. Declare duplicate-charset policy or a named fault. Contract: 1633–1643.
- **G02, line 2402:** duplicate root `checks` members, first containing a 404 check and second empty. Last-member-wins yields clean/0; duplicate rejection yields input_invalid/2. Declare JSON duplicate-member policy; SOURCES.md:42 explicitly describes rejection as local policy, not a universal JSON requirement.
- **C05/C06, lines 908/966:** `head<template>needle` and `head<!-- needle`. Pair-only deletion yields clean/0; suppression to EOF yields quote_missing/1. Specify unmatched-opener behavior. Contract: 1623–1626.
- **A01, line 3:** final 404 supplies a missing optional body path. Ignore non-200 body fields: gone/1; validate every supplied body field: check_invalid/2. Define non-200 extra-body validation. Contract: 1608–1613, 1647–1650.
- **B05, line 531:** Location `/two words`. String-only/tolerant resolution yields moved/1; URI-reference validation yields check_invalid/2. Define malformed-Location disposition, not just the resolution algorithm. Contract: 1606–1607, 1615–1617.
- Additional undecided cases cover non-HTTP redirect targets, lexical versus contextual comment/script recognition, Unicode trimming, spaces around charset `=`, numeric version/status representations, initial-URL grammar, symlink identity, and manifest BOM handling. The evidence index names every case.

These are fixable specification questions, not demonstrated tool failures. Adopt explicit public examples before relying on implementation defaults; do not silently modify the frozen acceptance contract or infer anything about sealed-case coverage.

## Explicit tradeoffs, not new defects to repair silently

- C07/C08/C11: next-end-tag suppression, next-`>` tag removal, and XHTML processing-instruction retention are consequences of the declared lexical pipeline, not browser-visible-text extraction. Replacing it with a DOM/XML parser changes authority and outputs.
- D01: a whitespace-only but raw non-empty quote becomes an empty substring and holds under the stated rule. A normalized-non-empty requirement would be a new rule, not an implementation correction.
- G01: duplicate check ids are not forbidden. Adding uniqueness changes the contract; existing finding ids alone cannot establish which duplicate registry identity produced a finding.
- Ordered comments, uppercase SCRIPT, spaced end tags, empty Location, defined-empty query, BOM-plus-invalid bytes, single-quoted charset, text/plain references, and mixed-verdict precedence all have concrete inputs and competing readings in the artifact. The 29 resolved boundaries are not counted as 29 contract defects.

## Evidence and execution limits

- Frozen contract: `/fast/scratch/hyaku/kake-r36w1/CriticContractAmbiguity/SCORECARD.frozen.md:1597-1656`, revision `cd3212796cab7a2afa03b638dbfafe7194df9629`.
- Frozen file SHA-256: `07401885b17e124cf13aff87a92bb31056275f1bb940401f47d1eed46048f883`.
- `/fast/scratch/hyaku/kake-r36w1/CriticContractAmbiguity/source-excerpts.json` retains local S088/S089/S090/S092 excerpts with original file hashes, source line 1, and character offsets; registry S025/S033/S034 evidence is at corpus/SOURCES.md:33,41–42.
- `/fast/scratch/hyaku/kake-r36w1/CriticContractAmbiguity/evidence-index.json` records counts, all undecided ids, and JSON line pointers.
- Preparation command: `timeout 30 mkdir -p /fast/scratch/hyaku/kake-r36w1/CriticContractAmbiguity/tmp` — exit 0; no stdout.
- Capture command: `timeout 60 git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cd3212796cab7a2afa03b638dbfafe7194df9629:SCORECARD.md` — subprocess exit 0; 1707 lines. GIT_DIR, GIT_WORK_TREE, and GIT_INDEX_FILE were removed; TMPDIR was the sandbox tmp directory.
- Artifact construction used bounded Python Eval cells and tool.write; observed successful ambiguity.json write: 126892 bytes. No audit program, counter, judge, tests, or other runtime was invoked for scoring.
- Not verified: proposed tool behavior, fixture materialization/execution, sealed cases, live freshness, or canonical admission. No network requests, sealed-tree access, tool installs, tracked-lane/index mutations, or processes left running. The assigned report is the only lane file written.
