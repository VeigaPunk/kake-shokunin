CONFORMANT — report-input task complete; no round verdict.

Axes: operability, freshness.

Behavior: drafted the three requested input artifacts from committed source bytes and frozen receipts; no product code or round report edited.

Artifacts:
- `/fast/scratch/hyaku/kake-r43/ScribeReportInputs/sources-frontier.txt`
- `/fast/scratch/hyaku/kake-r43/ScribeReportInputs/measurements.txt`
- `/fast/scratch/hyaku/kake-r43/ScribeReportInputs/waves.txt`

Commands and outcomes:
- Source rows: `timeout 30 prlimit --as=8000000000 -- python3 -c '<committed git-show row parser>'` over `61046fcffa23898cd93b7a5a0af4906dac9926c9` and `b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee`; output 128→130, S129/S130 added (A/mined), touched `[]`. Exact command/output is in `sources-frontier.txt`.
- Pin count: `timeout 30 prlimit --as=8000000000 -- python3 -c '<git-show pins.pathsMissSet counter>'`; output 63 (base)→65 (freeze), both added strings found only at freeze. Exact command/output is in `measurements.txt`.
- Roster: `timeout 30 prlimit --as=8000000000 -- python3 -c '<git-show JSON items extractor>'`; output `seat_count 66` and all ordered names/roles are in `waves.txt`.
- Committed freshness receipts, not rerun: `sweep-before.exit` says exit 1; `sweep-after.txt` ends `VERDICT: OK (exit 0)`.

Findings / checked statements:
- Registry 128→130 at the freeze: holds. The 119→128 correction in SCORECARD is a separate comparison against 1ef7a0e9.
- C1 met flags/equalRuns in the JSON receipts hold (ref false; builds 1–3 true, each 11/11). SCORECARD.md:3216-3224 ratio summaries conflict with committed JSON/log ratios; exact verbatim values and receipt paths are in `measurements.txt`. Unresolved for canonical judgment.
- C2 §paths exit 1→0 is supported by the committed outputs. The 63→65 pin-array delta re-derives from the two commits, but `sweep-before.txt:74` itself prints `missSet 65`; the files do not establish why. Do not present that before receipt as a direct rendering of the 61046fc pins.
- Census exit 0 before/after is stated at SCORECARD.md:3273-3276. Both census output receipts end in `kake ok`, but neither records process exit; the exit is not independently re-derived here.
- Wave spec is committed at `eddbbf607fd9069028d8c67b682582fd17881d02`, after freeze b49; its absence at b49 is consistent with the stated freeze-before-dispatch sequence. Roster source and extraction output are recorded in `waves.txt`.

Touched surfaces: only the three scratch artifacts and this report. Lane source, receipts, SCORECARD, Git index/state were read-only. No tool installed; no C1/C2 rerun, build, test, network access, or scoring performed. The scoped findings are draft inputs, not a round verdict.