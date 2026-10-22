# MutCriteriaChecks — mutation testing of the three round-35 criteria checks

Attacks the strength of `.ufo/waves/round-35/criteria/*.py`: do the six recorded receipts in `.ufo/waves/round-35/verification/criterion-*.txt` detect a broken check? Axes: operability (registry row, control description) and freshness (prebuild leak).

## Method

Sandbox only: `/fast/scratch/hyaku/kake-r35/w2/MutCriteriaChecks/`. Clone of the lane repo at `0d52173`; pristine bytes copied to `base/`, hashing equal to the lane files (`registry_row_check.py` `7282950a…`, `control_description_check.py` `fcc77676…`, `prebuild_leak_check.py` `b77e3a1f…`). Each mutant is a separate patched copy under `mutants/<id>/`; the pristine files are never edited, so restoration is by construction. Harness `mutate.py` re-runs each receipt's recorded command against the mutant and compares stdout and exit code with the receipt text; killed = at least one receipt stops reproducing. JSON `results.json` (sha256 `c31986a6…`).
Baseline first: all six receipts reproduce byte-for-byte, exit codes as recorded (registry 318561ef exit 1, registry fd0d53b2 exit 0, ctrl-desc r34-row4 exit 1, ctrl-desc r35-correction exit 0, leak c1 exit 0, leak c2 exit 1). Example command: `python3 -B mutants/R4-name-column-match-dropped/registry_row_check.py --repo clone --rev 318561ef` → exit 1 (the receipt expects exit 1 listing only `scripts/link_preview_audit.py`; the mutant adds three selftest scripts). 32 mutants: 12 registry, 11 control-description, 9 prebuild-leak. Longer per-mutant intents and full stdout: sandbox `final-table.md`.

## Mutant table (killed yes/no)

`rec` = killed by a recorded receipt; `fix` = killed by a fixture proposed below; `eq` = equivalent mutant, no verdict change possible.

| check | mutant | rec | fix | check | mutant | rec | fix |
|---|---|---|---|---|---|---|---|
| registry | `R1-docstring-exit-contract-ignored` | no | yes `5eda26e` | ctrl-desc | `C1-line-number-not-required` | no | yes `8b32cbd` |
| registry | `R2-every-script-requires-a-row` | no | yes `f216a3b` | ctrl-desc | `C2-line-number-off-by-one` | yes | n/a |
| registry | `R3-selftest-scripts-included` | yes | n/a | ctrl-desc | `C3-minimum-quote-length-dropped` | no | yes `e58f561` |
| registry | `R4-name-column-match-dropped` | yes | n/a | ctrl-desc | `C4-bundle-fetch-skipped` | yes | n/a |
| registry | `R5-kebab-name-conversion-dropped` | yes | n/a | ctrl-desc | `C5-ambiguous-anchor-last-block-wins` | no | yes `a7fe8bd` |
| registry | `R6-doc-exit-regex-narrowed` | no | yes `5eda26e` | ctrl-desc | `C6-minimum-length-raised` | yes | n/a |
| registry | `R7-exit-contract-doc-and-const-removed` | no | yes `8485ebd` | ctrl-desc | `C7-line-number-patterns-narrowed` | no | yes `79c5ccc` |
| registry | `R8-constant-name-prefix-loosened` | no | yes `bc09c8a` | ctrl-desc | `C8-source-line-stripped-comparison` | yes | n/a |
| registry | `R9-exit-code-set-narrowed` | no | yes `5eda26e` | ctrl-desc | `C9-anchor-first-match-only` | no | yes `a7fe8bd` |
| registry | `R10-row-name-case-sensitive` | yes | n/a | ctrl-desc | `C10-whole-line-quote-not-required` | yes | yes `3f71a26` |
| registry | `R11-table-separator-not-skipped` | no | eq | ctrl-desc | `C11-doc-and-source-rev-swapped` | yes | n/a |
| registry | `R12-path-pattern-boundary-dropped` | no | yes `e4fe2c1` | leak | `P1-receipt-values-not-nested` | yes | n/a |
| leak | `P2-substring-match-on-raw-json` | yes | n/a | leak | `P6-key-only-value-match` | yes | n/a |
| leak | `P3-partial-leak-tolerated` | no | yes leakfix | leak | `P7-only-first-pair-checked` | yes | n/a |
| leak | `P4-multiple-entry-lines-allowed` | no | yes leakfix | leak | `P8-entry-regex-ignored` | no | yes leakfix |
| leak | `P5-boolean-rendering-changed` | no | yes leakfix | leak | `P9-value-normalization-stripped` | no | eq |

Tally: 14 of 32 killed by the recorded receipts, 18 survived; 16 of the 18 are killed by the fixtures below, 2 (`R11`, `P9`) are equivalent mutants, not coverage gaps.

## Findings

1. **The receipts are direction tests, not strength tests.** Each pins one PASS and one FAIL case, so any mutant that only weakens behaviour between those corners reproduces both unnoticed: 18 of 32 slipped through. They catch crashes and gross inversions, not graded weakening.
2. **The exit-contract rule is the weakest link of `registry_row_check.py`.** R1, R6, R7, R8, R9 survive: the two live signals (the `EXIT_` constant, the docstring sentence) are individually untested, and `has_exit_contract` gates which scripts need a registry row at all. R2 shows the gate itself is unpinned: removing it flags a plain script with no exit contract.
3. **`control_description_check.py` does not check that the quoted line is the one numbered.** C1 survives: a paragraph backticking a real source line but naming the wrong line passes once the line-number requirement goes. C7 leaves the accepted citation spellings unpinned; C9/C5 leave the "exactly one block" ambiguity guard unpinned.
4. **`prebuild_leak_check.py` does not pin partial leaks.** P3 survives: tolerating one unmatched value reproduces both receipts, because the round-34 C1 receipt has all seven values absent and the C2 receipt all seven present, so a six-of-seven leak is invisible. P4/P8 leave the "exactly one matching entry line" rule unpinned.
5. `R11` cannot change any verdict (a markdown separator cell can never equal a kebab name or hold a script path; checked over all 48 `SKILL.md` revisions in lane history, 0 differences). `P9` is a no-op (`PAIR_RE`'s value class `[A-Za-z0-9_.:+-]` excludes whitespace; 20 000 random strings, 0 values differing under `.strip()`). Not coverage gaps.

## Proposed fixtures for the survivors

Built by `fixtures.py`, committed in the throwaway clone `/fast/scratch/hyaku/kake-r35/w2/MutCriteriaChecks/fixtures/repo` (nothing written to the lane repo); JSON `fixture-results.json` (sha256 `123cf2b5…`). Each is a pass/fail pair: the pristine check keeps its verdict, the mutant flips. Example: `FIXTURE-KILLS R12-path-pattern-boundary-dropped` — pristine exit 1 lists `scripts/const_only_tool.py` and `scripts/doc_only_tool.py`; the mutant stops listing `scripts/archived_probe.py`.

```
f216a3b  plain_helper.py, no exit contract, no registry row                  -> R2
5eda26e  doc_only_tool.py, exit contract only in the docstring                -> R1, R6, R9
8485ebd  const_only_tool.py, exit contract only in EXIT_CLEAN/EXIT_POLICY     -> R7
bc09c8a  exitcode_tool.py, constant EXITCODE (no underscore)                  -> R8
e4fe2c1  archived_probe.py, registry row names only archived_scripts/...      -> R12
8b32cbd  paragraph quotes `import hashlib, json, os, sys`, names line 7       -> C1
e58f561  paragraph quotes the 19-character line `argv = sys.argv[1:]`          -> C3
79c5ccc  paragraph cites the line as `lines 15`                               -> C7
a7fe8bd  same anchor in two paragraphs with different line numbers            -> C5, C9
3f71a26  paragraph names line 15 without backticks                            -> C10
00ea241  receipt missing og:image, two-line entry, boolean entry, non-matching entry line -> P3, P4, P5, P8
```

## Bounds and what was not verified

- The lane repo was not mutated by this seat: no commit, checkout, index write or jj. The three criteria files still hash `7282950a…`, `fcc77676…`, `b77e3a1f…`; `git -C clone status --porcelain` is empty; `base/*.py` hashes still equal the lane files.
- Not verified: mutants were not run against the sealed counter, the round-34 matrix, or the C1/C2 controls — this item covers only the three criteria checks. The fixtures were not run against a second implementation of the checks. No build, lint or formatter was run.
- `dcef39b5` is reachable only through the round-34 bundle, so every run set `TMPDIR=/fast/scratch/hyaku/kake-r35/w2/MutCriteriaChecks/tmp` and passed `--bundle`.
- No tools were installed or updated for this item.
