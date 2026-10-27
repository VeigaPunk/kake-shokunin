# MutGuardTool

ATTACKS: 33 independent one-point mutants of B1 `scripts/append_guard.py` across tag syntax/visibility, EOF and DP run logic, tree modes/deletions, glob scope, exit handling, GIT environment scrubbing, and ancestry checks. Ran the pristine `--selftest` and frozen C2 counter first; then ran both detectors on every mutant. All were isolated under `/fast/scratch/hyaku/kake-r60/MutGuardTool/`.

MUTANTS:

- Baseline: `python3 -B append_guard.B1.py --selftest` → `append_guard selftest: 38/38`, exit 0. C2 `python3 -B c60_guard_cases.B1.py --root <B1 shared clone> --revision 8b33fd248d126b48d838af5c38bc175850f41a09 --work <scratch>/baseline-work --tool <pristine>` → `C2 guard-cases 24/24 met=True`, exit 0.
- Detector protocol per mutant: same `--selftest` and same C2 invocation with `--tool <mutant>` and a mutant-specific `--work` directory. A kill means nonzero detector exit.
- 33 mutants were generated and both detectors completed. Both detectors killed 16; 16 survived both; `git-env-not-scrub` was killed by selftest but survived C2. The exact per-mutant exit codes and detector summaries are retained in `MutGuardTool.files/results.json`.

SURVIVORS:

All listed mutants returned 0 from both detectors (selftest 38/38 and C2 24/24):

| Mutant / behavior weakened | Expected detection | Actual output | Verdict |
|---|---|---|---|
| `tag-allow-upper` (case-insensitive tag regex) | selftest/C2 reject non-contract tag spelling | 38/38; 24/24 | survived |
| `tag-one-digit` (zero-length round number accepted) | reject malformed tag | 38/38; 24/24 | survived |
| `tag-date-month-wide` (one-digit month accepted) | reject malformed date | 38/38; 24/24 | survived |
| `tag-drop-closing` (closing `]` no longer required) | reject partial tag | 38/38; 24/24 | survived |
| `comment-ignore` (disable comment-open state handling) | comment-hidden tag must not qualify | 38/38; 24/24 | survived |
| `comment-close-ignore` (do not find comment close on line) | visible tag after closed comment remains recognized | 38/38; 24/24 | survived |
| `run-eof-equal` (`start > last` → `start >= last`) | a run beginning at last matched index must not be treated as EOF append | 38/38; 24/24 | survived |
| `run-require-tag-every-line` (require every line in run tagged) | contract only requires run's first line tagged | 38/38; 24/24 | survived |
| `submodule-mode-accept` (treat mode 160000 as regular blob) | replaced knowledge file reports `deleted` | 38/38; 24/24 | survived |
| `tree-mode-accept` (add mode 040000 to regular modes) | tree/non-regular replacement reports `deleted` | 38/38; 24/24 | survived |
| `scope-star-cross` (single `*` crosses slash) | scope glob must not cross directory separator | 38/38; 24/24 | survived |
| `scope-question-cross` (`?` crosses slash) | scope glob must constrain one character to one path component | 38/38; 24/24 | survived |
| `exit-error-one` (missing base evaluation returns 1) | missing revision/base returns 2 | 38/38; 24/24 | survived |
| `exit-missing-zero` (unresolved revision returns 0) | unresolved revision returns 2 | 38/38; 24/24 | survived |
| `tag-line-mask-index` (test mask byte one position after match start) | reject hidden tag spans / preserve visible tag detection | 38/38; 24/24 | survived |
| `scope-match-search` (use regex search instead of anchored match) | scope must match entire repository-relative path | 38/38; 24/24 | survived |

CASES TO ADD:

- Tag parser: reject case variants, missing round digits, one-digit date fields, and missing closing bracket. Assert visible exact-form tags still pass.
- Visibility: a tag after a closed HTML comment on the same line and across comment-open/close lines; tags split across comments. Current `comment-ignore` and `comment-close-ignore` changes were not exposed by the suite.
- EOF boundary: construct base/revision with duplicate lines so the alternate alignment creates an inserted run exactly at the last matched base index; assert only truly post-last-match runs are EOF-allowed.
- Alignment semantics: tagged first line followed by untagged line(s) in the same insertion run; contract permits run interior lines. Conversely test a tag later in a run does not rescue its untagged first line.
- Mode checks: replace scoped file with a gitlink/submodule and a tree/directory entry; require `deleted`. Existing symlink case does not cover these modes.
- Scope glob semantics: explicit patterns with `*` and `?` adjacent to slash and paths containing extra components; assert slash cannot be consumed. Also distinguish whole-path anchoring from substring matching.
- Exit codes: unresolved base and unresolved revision must each return exactly 2, not merely nonzero or output-shaped results.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | `.ufo/waves/round-60/c60_guard_cases.py` (case table / `case_results`) | Frozen 24-case detector accepts 16/33 plausible weakened implementations, including malformed tag acceptance, scope wildcard semantic drift, EOF-boundary misclassification, and missing-input exit-code regressions. | `python3 -B <counter> --root <B1 clone> --revision 8b33fd248d126b48d838af5c38bc175850f41a09 --work <scratch>/work-<name> --tool <mutant>` → C2 24/24 for each survivor (full list in `SURVIVORS`). | Add the targeted cases listed above; only tighten counter behavior after pinning expected outputs. |
| low | `.ufo/waves/round-60/c60_guard_cases.py` (GIT_* environment case coverage) | GIT environment scrubbing mutant passed C2 24/24 though the tool selftest caught it; C2 does not independently expose this boundary. | `git-env-not-scrub`: selftest exit 1 (37/38); C2 exit 0 (24/24). | Add a C2 case with hostile inherited `GIT_*` pointing to alternate repository/index/config and verify results are unchanged. |

Evidence / restoration: pristine B1 extraction SHA-256 before and after all probes was `2591ce14e6e304252498bc540640f26d01d2929cce7f5a76595fa573b6adca4c`; frozen counter SHA-256 `d6b647793809c322ac0a4334db18c8c27f2115d384655d9b732df3090ecf186b`. Mutants were separate files; pristine source was not overwritten. Baseline detector results establish that the comparison was valid. No source, counter, lane index, or lane jj state was changed.

VERDICT: C2 detects many realistic faults but 16 of 33 tested mutants survived both detectors; coverage gaps are listed above.
