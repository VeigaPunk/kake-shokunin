# ReviewC1Before: C1 counter re-run at base 035668132250b75b38d399e86e540b0a0371efbc

Seat: KakeR30.ReviewC1Before (leaf reviewer). Judged on: operability. Milestone: r30-build.

Result: the base run reproduces the committed receipt byte for byte, so the 0/14 base reading is correct. The counter has two coverage gaps (F04, F02) that let a gate which breaks the contract pass those families. Fix them before the C1 14/14 claim is read as proof of the contract.

## 1. Commands run (sandbox /fast/scratch/hyaku/kake-r30/w1/ReviewC1Before/; clone HEAD 4580c78cca1185d059efa6970722bbcf2f9c1b0f; Python 3.14.8)

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | git clone -q of the lane into ReviewC1Before/clone | 0 | HEAD 4580c78cca1185d059efa6970722bbcf2f9c1b0f |
| 2 | sha256sum of lane counter, gate, runner; git show 035668...:scripts/citing_set.py and citing_set_selftest.py | 0 | counter be2a1287...bcc53e; gate d7e79ba1...3479d48; runner 3c167895...dd62a1c (all equal the receipt) |
| 3 | cd clone; python3 -B .ufo/waves/round-30/c1_reason_count.py --root . --revision 035668132250b75b38d399e86e540b0a0371efbc --scratch ReviewC1Before/count | 1 | 12.4 s; stderr: C1 0/14 at 035668132250b75b38d399e86e540b0a0371efbc (controls True, constant gates rejected True) |
| 4 | Same command, --scratch ReviewC1Before/count2 | 1 | stdout byte-identical to run 3 |
| 5 | cmp run-3 stdout with verification/c1-before-0356681.json | 0 | BYTE-IDENTICAL (555 lines) |
| 6 | Recursive leaf diff of receipt and run 3 (script in sandbox) | 0 | 253 leaves, 0 differences |
| 7 | shutil.rmtree on a 1000-deep tree, Python 3.14.8 | 0 | removed; count/ and count2/ empty after runs |
| 8 | Base gate on a 1000-deep corpus (sandbox exp/f05) | 1 | RecursionError at citing_set.py:286 (relpath), reached through _walk recursion at :290 |
| 9 | Synthetic-gate probes, section 3 (exp/probe-f04.json, exp/probe2.json) | 0 | see section 3 |

Read-only checks: no .gitattributes at base, so nothing is export-ignored; no symlinks under scripts/; 250 files mode 100644 and 11 mode 100755; 29 expected.json files in the base tree and in the export.
No installs or updates (no pacman, uv, npm or cargo). No network. Nothing written in the lane except this report. No lane git or jj command that mutates.

## 2. Field-by-field comparison with verification/c1-before-0356681.json

All fields match.
- counterSha256 be2a1287...bcc53e: match (lane file, clone file, receipt).
- revision 035668132250b75b38d399e86e540b0a0371efbc: match.
- gateSha256 d7e79ba1...3479d48 and runnerSha256 3c167895...dd62a1c: match. python 3.14.8: match.
- passed 0, total 14, rPassed 0, fPassed 0, controlsHold true: match.
- Controls: K1 exit 0 clean; K2 exit 0 clean; K3 exit 1 failed with unadjudicated_citing_pair. Match.
- runnerBaseline: exit 0, 29 cases, 0 failed. Match.
- constantGates: constantClean 0 (runnerExit 1); refuseEverything 0 (runnerExit 1); constantGatesRejected true. Match.
- R01 to R08 each: parts behaviour true, fixture false, compared false; mutant exit 0, 29 cases, 0 failed; renamedOccurrences 1,1,2,1,2,1,2,1. Match.
- F01: behaviour false (2 cases, exit 0 clean). F02: behaviour false (3 cases, exit 0 clean). F03: 2 cases exit 0. F04: 4 cases exit 0 (want 64). F05: exit 1, traceback on stderr. F06: exit 2, device /dev/pts/1, ttyNr 34817 (tty_nr not 0). Match, including the device, in both runs.

## 3. Counter defects and gaps (.ufo/waves/round-30/c1_reason_count.py)

[run] = shown by an experiment in the sandbox. [read] = shown by reading the code only.

F1 (medium) [run] F04 cannot see the --name=value form or identical repeats. Its variants (lines 304-312) use only the space form and only conflicting values. Probe gates: exp/gate_a.py (rejects conflicting repeats only) and exp/gate_b.py (rejects any space-form repeat, ignores =) both score 4/4 on F04 (exp/probe-f04.json). Both exit 0 on --population=population.json --population=population.json; gate_a exits 0 on identical space-form repeats. The contract requires 64 for both. So F04 can pass a gate that breaks the contract.

F2 (low-medium) [read] F04 accepts any JSON object on stdout (lines 313-322, check at 318-319). It never checks the usage object (verdict could-not-evaluate, error starting "usage:"). Probe exp/gate_d.py prints {"note": "repeated --population"} with exit 64 and scores 4/4 (exp/probe2.json).

F3 (low-medium) [run] F02 puts NaN only in the population document (lines 276-283). The contract says NaN, Infinity and -Infinity "anywhere". Probe exp/gate_c_population_only_nonfinite.py refuses NaN in population only and scores 3/3 on F02. A ledger with "weight":NaN returns verdict clean, exit 0, through both the base gate and gate_c (exp/ledger-nan/root). F02 would pass a gate with this gap.

F4 (low) [read] compared (lines 448-449) accepts any non-zero runner exit, including exit 2 (the runner's own could-not-evaluate). It should require exit 1 with failed of at least 1.

F5 (low) [read] Mutation renames double-quoted literals only (lines 429, 431). A reason literal in single quotes survives the rename, so a correct gate could fail compared (false negative). The text-mode rewrite (lines 427-431) is harmless.

F6 (low) [read] Cleanup at line 541 is not in a finally block. ignore_errors=True (lines 496 and 541) hides cleanup errors. Normal path verified: the 1000-deep tree was removed on both runs. An exception or Ctrl-C leaves run-<pid>, including the 1000-deep tree, under --scratch. Not exercised.

F7 (doc) [read] F05 docstring (lines 37-39) says "a corpus directory 1000 levels deep". Code (lines 326-331) builds 1000 levels below corpus/knowledge, which is 1002 below the root. Usage line 57 omits --scratch. Default SCRATCH (line 76) is the shared path /fast/scratch/hyaku/kake-r30/c1-count.

F8 (note, no fix needed) [read] F06 exercises only the population open, because evaluate() reads population first (lines 475-478). A tty cannot reach the ledger or corpus opens: containment (citing_set.py:225) and the population-first order block it.

F9 (note) [read] Each reason code is exercised on one document only (R01 population, R02 ledger, F02 population). F3 shows the gap is real for per-document repairs.

Runner note (scripts/citing_set_selftest.py:49): DEFAULT_TMPDIR is still /fast/scratch/hyaku/kake-r27. The counter passes --tmpdir, so this does not affect C1.

## 4. Checked and sound

- Python 3.14.8 removes a 1000-deep tree with shutil.rmtree (run 7).
- The counter is deterministic: runs 3 and 4 are byte-identical.
- git archive export matches committed bytes (gate and runner hashes equal; 29 fixtures present).
- Base F05 fails for the reason the receipt records: recursive _walk (citing_set.py lines 273-290), RecursionError at lines 286 and 290.
- Constant-gate stubs score 0 each; controls K1 to K3 hold.

## 5. Not verified

- No repaired gate or runner was built. Repair checks belong to the writers.
- F06 device numbers depend on the host. Verified here only.
- F6 exception-path cleanup, and F4 and F5, rest on reading.
- The C2 counter and other lanes' receipts are out of scope.

## 6. Advisory changes for the L1 (no edits made)

1. F04: add --name=value and identical-value repeats for all four options; check the usage object (verdict and error prefix).
2. F02: add NaN, Infinity and -Infinity inside the ledger and nested in a row, not only at population top level.
3. compared: require runner exit 1 and failed of at least 1.
4. Put cleanup in finally; stop using ignore_errors, or report leftovers.

## Evidence (absolute paths)

- /fast/scratch/hyaku/kake-r30/w1/ReviewC1Before/count-stdout.json, count-stderr.txt, count-exit.txt
- /fast/scratch/hyaku/kake-r30/w1/ReviewC1Before/count2-stdout.json, count2-stderr.txt
- /fast/scratch/hyaku/kake-r30/w1/ReviewC1Before/compare-vs-committed.txt
- /fast/scratch/hyaku/kake-r30/w1/ReviewC1Before/exp/gate_a.py, gate_b.py, gate_c_population_only_nonfinite.py, gate_d.py
- /fast/scratch/hyaku/kake-r30/w1/ReviewC1Before/exp/probe-f04.json, probe2.json
