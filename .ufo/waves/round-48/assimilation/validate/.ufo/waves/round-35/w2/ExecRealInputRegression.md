# C1 real-page harm: 102 retained ds4cc pages

Axis: operability. Result: no observed per-page finding change; no unexplained changes (NO).

## Evidence and result

Ran the round-34 runner in a clean sandbox clone at `b1cbbc39` and `318561ef`, with the same census receipt (`.ufo/waves/round-34/verification/c2-at-76fac3b.json`). Each runner exited 0 and reported `agrees: true`, `pagesChecked: 102`, tool exit 1, verdict `failed-policy`, and the same 146 findings: missing `og:image` 101; missing `og:title`, `og:type`, and `og:url` 15 each. The tool exit 1 is the expected policy result, not a runner failure.

Full tool reports for all pages are saved at:
- `/fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/evidence/per-page/findings-318561ef.json`
- `/fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/evidence/per-page/findings-b1cbbc39.json`

Their SHA-256 is identical: `6e40a7bdfbb0e2a934748312f32593a2ab7bb48b3beaec78f3f19c8a700ccdd3`. `diff -u` exit 0. The saved summary (`.../per-page/diff-summary.json`, SHA-256 `76da914dee260475d0e2b77762ed5d55a82971a0fdac2b36c00c603cc90df5b1`) records 0 changed pages. Both raw tool stdout files also match (SHA-256 `9e017350400f8deb26ce46023e6d786a8bccf9839bef830cf6247b5a92a6399e`).

The runner receipts differ only in the `revision` label: baseline receipt SHA-256 `f216248fc27d1a13e4828bafce5d47b57ef481f17d68634a668385cff7a05d1d`; repaired receipt SHA-256 `410808b5e8c15f58cf61fad313916f38126c6a6285dbbd73ac77ccbe1dd0b46b`. Their saved outputs and exit receipts are under `/fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/evidence/`.

## Contract interpretation

C1 rules are (a) report multiple non-empty `og:url`, (b) ignore metadata inside open template/svg/math, and (c) continue auditing readable pages when one is unreadable (`corpus/lessons/round-35.md:15-18`). No page findings changed under (a) or (b); the repaired distribution has no `og_url_multiple` or other new reason (`.../per-page/diff-summary.json:2-27`). The run does not show harmful real-page regressions from those rules. For (c), both reports checked all 102 pages with no input finding; the unreadable-page case was not exercised. The repaired code paths are documented at `scripts/link_preview_audit.py:98-117,219-245,270-277,302-305`; baseline exits before auditing documents if any page is unreadable (`/fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/clone/scripts/link_preview_audit.py:202-216`).

## Commands and exits

Common setup: `mkdir -p /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/tmp /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/evidence`; unset `GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE`; set `TMPDIR=/fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/tmp`.

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/clone && git -C /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/clone checkout -q b1cbbc39` — exit 0.
- `python3 -B .ufo/waves/round-34/real_input_run.py --root /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/clone --revision b1cbbc39 --census /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/verification/c2-at-76fac3b.json` — exit 0; saved as `runner-b1cbbc39.json` (tool exit 1).
- `git -C /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/clone checkout -q 318561ef && python3 -B .ufo/waves/round-34/real_input_run.py --root /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/clone --revision 318561ef --census /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/verification/c2-at-76fac3b.json` — exit 0; saved as `runner-318561ef.json` (tool exit 1).
- `python3 -B /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/per_page_diff.py /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/clone /fast/scratch/hyaku/kake-r35/w2/ExecRealInputRegression/evidence/per-page` — exit 0; helper SHA-256 `c21911f5b0755f5c26a2fc28d0430ef3096f6dd17c266d6ae32c81af7f3443fa`.
- `diff -u .../findings-318561ef.json .../findings-b1cbbc39.json` — exit 0, no diff.
- `diff -u .../runner-318561ef.json .../runner-b1cbbc39.json` — diff exit 1; sole difference is the expected revision label.

No installs, builds, tests, linters, or formatters run.