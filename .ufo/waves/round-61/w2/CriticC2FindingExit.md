# CriticC2FindingExit

## Axes
- **Operability:** exit-code contract for unevaluable checks and malformed response receipts.
- **Gate integrity:** whether the frozen H-cases and R3 actually establish C2's predicate.

## Cases exercised
Against the committed `scripts/header_audit.py` and the counter's embedded `REFERENCE` control, extracted without modification from `c61_header_cases.py`, I ran isolated scratch manifests (scratch: `/fast/scratch/hyaku/kake-r61/CriticC2FindingExit`). Results:

| Case | `header_audit.py` | Counter `REFERENCE` | Result |
|---|---|---|---|
| Valid manifest, two missing receipts | exit 1; two `could_not_evaluate`; `checks=2 findings=2` | exit 2; same two classes/summary | **Divergence** |
| One malformed-JSON receipt only | exit 1; `source_invalid_json` | exit 2; `could_not_evaluate` | **Divergence** |
| One unparseable-status receipt only | exit 1; `status_unparseable` | exit 2; `could_not_evaluate` | **Divergence** |
| Mixed clean + policy failure + missing receipt | exit 1; one policy line and one CNE line | exit 1; same two result classes | Agreement |
| Zero checks | exit 0; `checks=0 findings=0` | exit 0; same summary | Agreement; H18 pins this |
| Missing `checks` key | exit 2 | exit 2 | Agreement |
| Mixed good + bad-status receipt | exit 1; one CNE | exit 1; one CNE | Agreement; matches H13's mixed-check semantics |

The frozen counter run at revision `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`, seed 6113, passed H1–H18 (18/18); H13 passed all three subfixtures (missing receipt, non-status string, null status), each with a good sibling. R4 passed. It returned overall `met=false` because R3 failed separately (see below).

## Findings

1. **All-checks-unevaluable exit is not frozen and the tool disagrees with its own counter reference.** The contract says a missing/malformed receipt or unparseable status produces per-check `could_not_evaluate`, with “manifest fault → exit 2 only when NO check is evaluable.” The reference control implements exit 2 for a nonempty manifest with zero evaluable checks; the shipped tool's `run()` instead returns exit 1 whenever the per-check CNE lines exist. The shipped tool's own selftest explicitly expects exit 1 for all-unevaluable checks. H13 only has a bad check alongside a good one, so it cannot adjudicate this all-CNE boundary. The same gap applies to a malformed receipt as the only check. The contract wording is at least ambiguous about whether this is a manifest-level fault or a set of per-check findings; the two committed implementations resolve it differently. **Smallest safe correction:** have the canonical owner clarify the exit mapping, then align tool/reference and add a separate all-CNE fixture (while retaining H13's mixed case). Do not infer a C2 predicate failure from this divergence alone: all scored cases pass, and this edge is unscored.

2. **H13 pins the mixed-case result correctly, but not the summary's finding count.** The counter's `judge(..., "cne", ...)` requires exit 1, exactly one CNE line, no policy lines, and the expected number of checks. It does not compare the summary's `findings` integer (`got[0]` checks only the check count). Thus the line-level “zero policy findings” requirement is pinned; whether `findings=` counts CNE lines is not. The shipped tool reports one finding for one CNE line. **Smallest correction:** if the summary count is contractual, assert `got == (want, 1)` for these one-CNE subfixtures (and corresponding count for any multi-CNE fixture).

3. **Counter R3 currently fails at the tested revision due to manifest discovery scope.** The counter run reports `r3.pass=false` with `ambiguous manifests` including the canonical `capture/manifest.json` plus round-61 w1 evidence-fixture manifests. `materialize()` copies all `.json` files under `.ufo/waves/round-61`, and `pick_manifest()` treats every version-1 manifest anywhere in that tree as a candidate. This contradicts A4's named canonical path `.ufo/waves/round-61/capture/manifest.json` and makes the overall predicate `met=false` despite H1–H18 = 18/18. **Smallest correction:** have R3 read the A4 canonical manifest path directly (or limit candidates to the capture subtree and require that canonical manifest), leaving unrelated fixture manifests outside the candidate set.

## Verdict
VERDICT: H13 correctly pins mixed good/bad checks and H18 correctly pins zero checks; all-CNE/malformed-only exit semantics remain unpinned and conflict between the shipped tool and counter reference, while the measured C2 counter is independently blocked by R3's overbroad manifest discovery.
