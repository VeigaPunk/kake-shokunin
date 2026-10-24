# KakeR35.CriticHarmPlan — which existing measures the C1 repair could harm

I did not touch /fast/scratch/hyaku/kake-r35/sealed/. I did not run sealed_count.py (it needs the sealed key). Sandbox: /fast/scratch/hyaku/kake-r35/w1/CriticHarmPlan/ (clone at 318561ef, outputs in out/). No tools were installed.

## Runners that execute scripts/link_preview_audit.py (from `git grep` at 318561ef)
1. Round-34 matrix counter `.ufo/waves/round-34/c1_matrix_count.py` (sha256 fc72d855…). It runs 28 frozen cases and 4 constant gates. It projects findings on the keys in each expected finding: (reason, property), or reason only for input cases (c1_matrix_count.py:71).
2. Selftest `scripts/link_preview_selftest.py` (9eefc787…) with 35 fixtures in scripts/fixtures/link-preview/. It projects input findings to (reason) and policy findings to (reason, property), never page (selftest:32-37).
3. Round-34 real-input run `.ufo/waves/round-34/real_input_run.py` (ef795091…). It runs on 102 retained ds4cc pages and checks the result against the census in c2-at-d08d8de.json (26b67e64…).
4. Round-35 sealed counter `.ufo/waves/round-35/sealed_count.py c1` (c4d58dae…). Not run here. The tool at 318561ef has the same bytes as the base tool (cccc3a17…), so receipt verification/control-c1-base-tool.json (14 of 24, exit 1) also covers 318561ef.
No other script, workflow or import calls the tool.

## Commands for wave 2 (R = landed repair commit; run before with R=318561ef)
Run these in a clean clone checked out at R (`git -C <clone> checkout -q R`). Runners 1 and 2 read the matrix, fixtures and default tool from disk, not from git.
- M: `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root <clone> --revision R`
- S: `python3 -B scripts/link_preview_selftest.py`. For a revision-pure run, add `--tool <git show R:scripts/link_preview_audit.py> --fixtures <git archive R scripts/fixtures/link-preview>`.
- X: `python3 -B .ufo/waves/round-34/real_input_run.py --root <clone> --revision R --census <clone>/.ufo/waves/round-34/verification/c2-at-d08d8de.json`
- K (L1 only): `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root <clone> --revision R --key-revision <reveal>`

## Before outputs at 318561ef (Python 3.14.8), with predicted after values
| Run | Before (exit) | Predicted after at R |
|---|---|---|
| M | 28/28; constant gates 6/0/6/1 of 28, all rejected (exit 0) | Unchanged: 28/28, exit 0. No case has template, svg or math, or more than one og:url. In I4-page-file-missing, the readable page is clean, so rule (c) adds no findings. The note on case I4, "policy findings are not reported with them", goes stale. The matrix is pinned by digest, so leave it unedited. |
| S | 35/35, verdict clean (exit 0) | 34/35, exit 1, unless the fixture is updated. `input_policy_suppressed_on_input` fails because partial.html has only og:title. Its new expected value is page_unreadable plus og_required_missing for og:type, og:image and og:url, with exit 2 and could-not-evaluate. With that update: 35/35, exit 0. |
| X | agrees true; tool exit 1; pagesChecked 102; missing og:image 101, og:title, og:type and og:url 15 each (exit 0) | Unchanged. Scan: 0 non-UTF-8 pages, 0 pages with more than one og:url, 0 og or canonical tags inside a foreign element, 49 svg start tags, all balanced, none before the page's last og or canonical tag (out/archive-scan.txt). |
| K | 14/24 (receipt, not rerun) | at least 22/24 is the claim |

Before files: out/before-r34-matrix.json, out/before-selftest.json, out/before-real-input.json.

## Predictions checked on a sandbox reference repair (not a deliverable)
- Sandbox commits are in out/sandbox-commits.txt:
  - A 618e8a7e: tool only, with rules a, b and c (+21/−4 lines).
  - B 0594c9b4: A plus the updated fixture expectation.
  - M 0337325b: A with a mutant where foreign elements never close.
- A: M 28/28 (exit 0); S 34/35, failing exactly input_policy_suppressed_on_input as predicted (exit 1); X agrees true (exit 0).
- B: M 28/28; S 35/35; X agrees true. All exits 0.
- **Counterexample, mutant M: same results as A on all three public runners** (M 28/28, S 34/35, X agrees; out/after-M-*.json). After an `<svg>`, `<template>` or `<math>`, the mutant ignores every later meta and link tag. On real pages this produces false og_required_missing findings. Only the sealed cases could catch it.

## Findings
1. HIGH, operability. None of the public measures covers rules a, b or c. The matrix and the selftest have no template, svg or math markup and no second og:url. On the real pages, every svg comes after the metadata. A repair that over-suppresses with rule (b), the "never closes" mutant above, passes everything except K. After the reveal, rule (b) regressions have no permanent regression guard.
   Smallest fix: in the repair commit, add public selftest fixtures for these cases:
   - metadata after a closed `<svg>…</svg>` still counts;
   - metadata after a self-closed `<svg/>` still counts;
   - for nested `<template><template></template>`, metadata is still suppressed until the outer end tag;
   - a second og:url gives og_url_multiple;
   - one unreadable page plus one readable page with findings.
   None of these may copy sealed cases.
2. MEDIUM, operability. None of the public projections includes page. The selftest and matrix compare input findings by reason only and policy findings by (reason, property). Under rule (c), a repair that attaches the readable page's findings to the unreadable page, or drops `page`, still passes M and S. Only K projects page (sealed_count.py:114). Smallest fix: make the new mixed-input fixture page-sensitive, either with a selftest projection that includes page for that case, or with one readable page and one unreadable page whose findings differ.
3. LOW, docs. The repair makes these statements false; update them in the repair commit:
   - link_preview_audit.py:33-35 says a canonical link inside template or svg counts;
   - :29 says a second og:url is not compared; it now produces og_url_multiple;
   - SKILL.md:1010 says "Exit 2 reports input findings only";
   - the capability row at SCORECARD.md:195 lists reasons without og_url_multiple.
   Rename `input_policy_suppressed_on_input`; its name states the old behaviour.
4. Pre-existing gap, not fixed by me. M and S read their inputs from disk, not from git, so a dirty tree or the lane working tree can change their results. Wave 2 should run them in a clean clone at R.

## Not verified
- K before and after; the sealed cases are out of scope.
- Rule (b) attribute and case edge cases, and pagesChecked semantics beyond the reference repair (CriticC1ContractAmbiguity's lane).
- The landed repair itself (not landed when I ran).
