# RerunC2Counter: C2 count re-derived at fe1805cf and 7697990

Seat: KakeR29.RerunC2Counter (leaf, wave 2, falsify). Axis: operability. Milestone: r29-falsify.
Lane HEAD (read-only rev-parse): 7697990cbca20291f3b0367b8ff4220e93b38b03.
Sandbox: SB=/fast/scratch/hyaku/kake-r29/w2/RerunC2Counter with clone (checked out at 7697990) and base-clone (checked out at fe1805cf). Both trees clean, ignored files included. SB/tmp is empty after the runs; nothing was written to /tmp.
Installs: none. Interpreters used were already present (uv-managed): Python 3.10.22, 3.11.17, 3.12.15, 3.13.16, 3.15.0, plus host 3.14.8. No network use.

## Blob and ancestry checks
- `git ls-tree` at d18bbf3, f8675e5, 98dbab2 and 7697990 gives the same blob ids:
  - .ufo/waves/round-29/c2_matrix_count.py 58dde0628c3e40a9794c93b03c3b9f6e665173fc (100755)
  - .ufo/waves/round-29/c2-matrix.json 0687433ecd7cd14eb90287121f82a99074503b84 (100644)
  - .ufo/waves/round-29/c1_quote_truth.py 139ede1efbbfeed612201239a4244b43aeda855d (100755)
- `git diff --quiet d18bbf3 7697990 -- <those three paths>`: exit 0.
- `git log --oneline d18bbf3..7697990 -- <those paths>`: no output, exit 0.
- `git merge-base --is-ancestor`: d18bbf3 and fe1805cf are both ancestors of 7697990 (exit 0, 0).
- Matrix sha256 75c08f641a31356d0f3446d9e6e435c44ee02bc4cf49102904e2466dbac2e84a equals MATRIX_SHA256 (counter line 28). The matrix has 30 unique case ids: kinds control 7, defect 14, input 8, usage 1; expected exits 0, 1, 2, 64 with the same counts.
- Audit tool scripts/base_path_audit.py: blob e5167fa13dab6af9b7b4f99b9ee2099a8efe302d at 98dbab2 and 7697990; absent at d18bbf3 and fe1805cf. sha256 e32646159b652710be4053bbdb001c3d11929ef63b055b7f57545231ac6965aa.

## Commands and exit codes
All runs set TMPDIR=$SB/tmp. Output goes to $SB/out-*.json and $SB/err-*.txt.
1. In clone: `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision 7697990cbca2…` gives exit 0, stderr "C2 30/30 at 7697990…".
2. Same command again gives exit 0. JSON identical to run 1 (`diff -q` exit 0).
3. In clone: `… --root $SB/base-clone --revision fe1805cf32a7…` gives exit 1, "C2 0/30 at fe1805cf…". The counter file comes from the 7697990 tree because it is absent at fe1805cf.
4. In clone: `… --root . --revision fe1805cf32a7…` (reads the object store) gives exit 1, "C2 0/30". JSON identical to run 3.
5. In base-clone, the literal declared command `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision fe1805cf…` gives exit 2: "can't open file … No such file or directory".
6. In clone, the 7697990 command under Python 3.10.22, 3.11.17, 3.12.15, 3.13.16 and 3.15.0 gives exit 0 each with "C2 30/30 at 7697990…". Each JSON is identical to run 1 (`diff -q` exit 0).

## Summary of outputs
| Run | Exit | toolPresent | passed | byKind | constant gates (clean / failed-empty / refuse) | all constants rejected |
|---|---|---|---|---|---|---|
| 7697990 (runs 1, 2, 6) | 0 | true | 30/30 | control 7/7, defect 14/14, input 8/8, usage 1/1 | 7/30, 0/30, 7/30 | true |
| fe1805cf (runs 3, 4) | 1 | false | 0/30 | control 0/7, defect 0/14, input 0/8, usage 0/1 | 7/30, 0/30, 7/30 | true |

Every fe1805cf case fails with detail "tool absent or timed out", and toolSha256 is null. The matrix sha256 is the same in every output.

## Diff result
- Run 1 vs run 2 (7697990): identical.
- fe1805cf base-clone vs object-store run: identical.
- fe1805cf vs 7697990 JSON: 204 diff lines. They differ in revision, toolPresent, toolSha256, passed, byKind and the 30 case rows. Constant-gate values match, as expected, because they do not read the tool.
- Committed evidence: verification/c2-after-98dbab2.json matches the 7697990 rerun on toolPresent, toolSha256, matrixSha256, passed, total, byKind, constantGatesPassed, constantGatesAllRejected and all 30 case rows. Only the revision label differs (98dbab22 vs 7697990; same tool blob). verification/c2-before-fe1805c.json matches the fe1805cf rerun on every checked field and all 30 case rows.

## Findings
1. holds: after-value 30/30 re-derived at 7697990 (exit 0), with byKind and constant gates as in the table. Matches SCORECARD.md:626 and :635.
2. holds: base 0/30 re-derived at fe1805cf (exit 1), constant gates identical. Matches SCORECARD.md:635.
3. holds: counter, matrix and C1 counter blobs unchanged from d18bbf3 to 7697990.
4. limit to state: the declared counting command (SCORECARD.md:626) runs only where .ufo/waves/round-29/c2_matrix_count.py exists, that is at 7697990 or later with `--revision fe1805cf…`. Inside the fe1805cf tree it exits 2 (run 5). The base count is unaffected (runs 3 and 4).
5. limit to state, wording: SCORECARD.md:632-633 says "finding reason tuples (reason codes, not ids)". The counter's project() (counter line 64) compares (reason, element, attribute, value) for 18 expected findings and (reason) alone for 8. No id field is compared. The "not ids" part is right, but the tuple is wider than reason codes.
6. limit to state: the usage case (exit 64) passes on exit code alone (counter lines 81-82). It is 1 of 30 cases and follows the counter's stated design.

## Not verified
- Whether the tool could special-case matrix inputs was not tested semantically. A text grep of scripts/base_path_audit.py at 7697990 for case-id patterns, "matrix" and "expect" found no hits, apart from the reject_constant JSON hook. That is a text check only.
- The counter was not run directly at d18bbf3 or 98dbab2; blob identity covers it.
- The real-input run, C1 and the selftest are outside this target and were not run.
- fe1805cf was not run under other interpreters. The tool is absent there, so the result follows the missing-tool path.

Verdict on the attacked item: holds. The re-derived after-value is 30/30 at 7697990, and the counter and matrix blobs are unchanged since d18bbf3. Limits 4 to 6 are for the L1 to record; they are not defects.
