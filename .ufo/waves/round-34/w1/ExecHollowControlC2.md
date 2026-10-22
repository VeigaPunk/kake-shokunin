Axes: freshness (C2 claim discrimination) and operability (control-check/counter interface).

## Work
- Built three commits from base `a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f` in `/fast/scratch/hyaku/kake-r34/w1/ExecHollowControlC2/clone`; lane history/index were not changed.
- Honest synthetic after: `1a70a870760ec4f40e46de26802323cd948b9a9e`; source-backed rows, interpretation, four exact retained-text quotes, and derived census; scored 5/5.
- Round-33-style hollow: `0a066208bcaa07f6f74c92ee04f2aca2e7ee9554`; moved S067-S070 text to `sources/decoys/S099.txt`…`S102.txt`, added fabricated S099-S102 rows and unrelated mentions/quotes. Each expected ID had all four checks false; census alone passed, yielding 1/5.
- Strongest hollow: `6040cb1d53d0fa525154de0ed4fe86489ff0a95e`; placeholder registry fields, ID-only citations, quote-only lesson, and copied census, with no study prose. It scored 5/5. This shows the counter validates structural identity, retained bytes/quotes, and census equality, but not whether the entry contains substantive interpretation or learning.

## Interface adaptation
`counter_control_check.py` accepts `--counter/--repo/--before/--after/--hollow` but invokes the counter with `--rev/--repo` (usage/implementation: `.ufo/waves/round-33/criteria/counter_control_check.py:4-13,21-23`). C2 instead requires `--root/--revision` (`.ufo/waves/round-34/c2_source_census.py:43-45`). The direct attempt using the C2 path as `--counter` exited 1: `FATAL: counter gave no JSON for before (a2fe31b2d1d2) exit=2`. I used the sandbox adapter `counter_flag_adapter.py:8-18` to translate those flags; it invokes the unchanged C2 counter.

## Commands and observed results
1. `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-33/criteria/counter_control_check.py --counter /fast/scratch/hyaku/kake-r34/w1/ExecHollowControlC2/clone/.ufo/waves/round-34/c2_source_census.py --repo /fast/scratch/hyaku/kake-r34/w1/ExecHollowControlC2/clone --before a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f --after 1a70a870760ec4f40e46de26802323cd948b9a9e --hollow 0a066208bcaa07f6f74c92ee04f2aca2e7ee9554` — exit 1; output: `FATAL: counter gave no JSON for before (a2fe31b2d1d2) exit=2`; `CHECK_EXIT=1`.
2. `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-33/criteria/counter_control_check.py --counter /fast/scratch/hyaku/kake-r34/w1/ExecHollowControlC2/counter_flag_adapter.py --repo /fast/scratch/hyaku/kake-r34/w1/ExecHollowControlC2/clone --before a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f --after 1a70a870760ec4f40e46de26802323cd948b9a9e --hollow 0a066208bcaa07f6f74c92ee04f2aca2e7ee9554` — exit 0. Output:
   `before a2fe31b2d1d2 -> met=0 exit=1`
   `after  1a70a870760e -> met=5 exit=0`
   `hollow 0a066208bcaa -> met=1 exit=1`
   `after=5 before=0 hollow=1`
   `PASS: hollow scores below the after-value; the counter pins identity`
   `CHECK_EXIT=0`
3. `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecHollowControlC2/clone/.ufo/waves/round-34/c2_source_census.py --root /fast/scratch/hyaku/kake-r34/w1/ExecHollowControlC2/clone --revision 0a066208bcaa07f6f74c92ee04f2aca2e7ee9554` — exit 1; JSON reported met=1/5, S067-S070 each failed a_row, b_entry_body_cites, c_gate_quote, d_quote_in_retained_text; census passed. Stderr: `C2 1/5 at 0a066208bcaa07f6f74c92ee04f2aca2e7ee9554`.
4. Same C2 command with `--revision 6040cb1d53d0fa525154de0ed4fe86489ff0a95e` — exit 0; JSON reported met=5/5, all four IDs and census passed, `controlBroken=false`. Derived and stated census matched: pages=102, og:title=87, og:type=87, og:image=1, og:url=87, all-four=1, og-url-equals-canonical=87. Stderr: `C2 5/5 at 6040cb1d53d0fa525154de0ed4fe86489ff0a95e`.

## Evidence and limits
- Criterion: `corpus/QUALITY.md:590-604`; C2 checks/score: `.ufo/waves/round-34/c2_source_census.py:11-37,217-247` (counter SHA256 `ee7461b9e3a33949174591c527ccbf2854ca178c41638f71b5128cbd57e5f892`).
- Strongest hollow content in sandbox clone: `corpus/SOURCES.md:76-79`, `corpus/knowledge/link-preview-metadata.md:7-13`, `corpus/lessons/round-34.md:5-8`. Baseline derived census receipt: `.ufo/waves/round-34/verification/c2-at-d08d8de.json:54-65`.
- No tools were installed. No build, lint, or other tests were run. No blockers. The direct checker invocation mismatch is handled above; its documented result is based on the translating adapter.