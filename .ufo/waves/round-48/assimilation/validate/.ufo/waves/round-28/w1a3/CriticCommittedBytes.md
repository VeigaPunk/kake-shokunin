# CriticCommittedBytes — C1 counter integrity (round 28 attempt 3, wave 1)

Target: `.ufo/waves/round-28/c1_interface_count.py` (blob 2efe60e8b8c11241a7e0375f88bd2162e1495526, identical to the copy committed at 84ea5b1).
Axis judged: operability. Scratch: /fast/scratch/hyaku/kake-r28a3/w1/CriticCommittedBytes (TMPDIR set there). No lane file other than this report was written. No tool was installed.

## Verdict in one paragraph
The declared numbers reproduce exactly: base 4/15, repair 15/15. The counter ignores the working tree and the working-tree `.gitattributes`, and parallel runs do not collide. But 15/15 can be reached for the wrong reason in four ways, all shown below: a gate that leaves the Git-mode defects unfixed, a commit with one fixture case, a stub selftest runner, and repo-local Git config that rewrites the exported bytes. An inherited `GIT_DIR` also makes the counter measure, and commit into, a repository other than `--root`. None of this falsifies b5d423f itself: its finding reasons match each attacked defect. The defects are in the counter's ability to tell a correct 15/15 from a wrong one.

## Reproduction (both runs in parallel on the same `--scratch .../count`)
- `python3 -B .ufo/waves/round-28/c1_interface_count.py --root . --revision 22c1669c... --scratch $S/count` exited 1 with 4/15 (0/11 defect, 4/4 control). The FIFO cases U1 and U2 each hit the 20 s timeout.
- The same command at `--revision b5d423fc...` exited 0 with 15/15. The defect reasons were `document_not_regular_file` ×2, `document_not_json` ×2, `corpus_directory_missing` ×2, `corpus_empty`, `not_a_directory`, `population_id_unreachable`, `revision_not_found` and `root_not_repository_top_level`. Every reason matches the defect its case attacks.
- Wall time for the parallel pair was 41 s. With stderr and stdout heads removed, both outputs equal the recorded evidence (`verification/c1-before.json` sha256 ce4103ed…, `c1-after-b5d423f.json` sha256 65acffdf…). My after-run output was byte-identical to the recorded file.
- `git archive` bytes equal the committed blobs at both revisions: 127 of 127 `scripts/` blobs matched by `git hash-object` against `git ls-tree`, with 0 mismatches. On this host today, the export is faithful.

## Attacks (sandbox clone at $S/clone; the counter was run from the lane path with `--root <clone>`)
| ID | Setup | Result | Meaning |
|---|---|---|---|
| WT | Clone at b5d423f. Working-tree `scripts/citing_set.py` replaced by the base gate, plus an uncommitted `scripts/.gitattributes` with export-ignore on both scripts. | exit 0, 15/15, K4 cases 29 | Working tree and working-tree attributes ignored (good) |
| X5 | Commit 00fca127 deletes `scripts/fixtures/citing-set` | exit 1, 14/15, K4 `selftest exit 2` | K4 cannot pass with zero cases (good) |
| X4 | Commit c5014bec keeps only fixture 01 | exit 0, 15/15, K4 `cases: 1` | K4 passes with 1 of 29 cases |
| X6 | Commit 4dcd8ff5 replaces `citing_set_selftest.py` with `sys.exit(0)` | exit 0, 15/15, K4 has no case count | K4 trusts the measured commit's own oracle |
| X7 | Commit 023209fa: the b5d423f gate with its three GitSource fixes reverted (top-level check, corpus-as-blob check, empty-tree check), plus `if source.mode == "git" and not ledger_entries: raise InputInvalid("ledger_empty")` | exit 0, 15/15. A2, A4 and A7 report `ledger_empty`. | Wrong-reason 15/15 |
| FILTER | Second clone with `.git/info/attributes` `scripts/citing_set.py filter=swap` and `git config filter.swap.smudge "cat repaired.py"`; run at 22c1669 | exit 0, 15/15, `"revision": "22c1669c..."` | Uncommitted repo state turns base into 15/15 under the base's identity |
| GIT_DIR | `GIT_DIR=$S/clone3/.git python3 -B ... --root <lane> --revision 023209fa...` | exit 0, 15/15 for a commit absent from the lane repo. clone3 went from 91 to 96 commits, all `c1-count case`. Its index now shows `D ledger.json`, `D population.json`, … | The measured repo is not `--root`, and the counter writes into whatever repo `GIT_DIR` names |

X7 leaves a live false green. In a nested repo (top: entry cites S001, ledger pairs S001; sub: entry cites S002, ledger pairs S001 to another file), the gates gave these results:
- b5d423f gate with `--root sub --revision HEAD`: exit 2, `root_not_repository_top_level`.
- X7 gate, same command: **exit 0 `clean`**.
- X7 gate on the same root in working-tree mode: exit 1, `failed` (`unadjudicated_citing_pair`, `ledger_pair_not_cited`).

So X7 scores 15/15 while still reading the wrong surface. The gap: every Git-mode defect case (A2, A4, A7) uses an empty ledger, and no control combines Git mode with an empty ledger. All 29 fixtures run in working-tree mode, because the selftest never passes `--revision`.

## Specific questions
- **Committed bytes only?** Yes against the working tree (WT row). No against repo-local Git state. `export_scripts` (counter lines 282-294) runs `git archive`, which honours `$GIT_DIR/info/attributes`, repo `.git/config` filters, and `GIT_DIR` and related variables from the environment. The `GIT_ENV` scrub (lines 50-57) applies only to the case-repo helper `git()` (lines 79-83), and even there it does not remove `GIT_DIR`. The global config defines `filter.lfs.*`, but no attribute selects it today.
- **Timeouts.** 20 s per gate (line 40) and 600 s for the selftest. On timeout, `subprocess.run` kills the child and the case fails (lines 101-102 and 122-123), so a timeout can only lower the count, never raise it. The b5d423f gate answered the 200 000-deep JSON input in 33-34 ms across 3 runs, so a load-induced false fail is unlikely.
- **Gate crash.** A traceback exits 1 with non-JSON stdout, which fails every defect case (want exit 2 and JSON) and every control case. A crash cannot pass.
- **K4 with zero fixture cases.** It cannot pass: the runner exits 2 (X5). It passes with one case (X4) or with a stub runner (X6). The counter labels K4 "the 29 fixture outcomes" (line 278) but judges only `exit_code == 0` (line 277), never passes `--min-cases`, and ignores `cases` and `failed`.
- **Parallel collisions.** None observed across 2 and then 7 concurrent runs on one `--scratch`. Each run uses `run-<pid>` (line 305) and the directory was empty afterwards. A crash leaves `run-<pid>` behind, because cleanup at line 330 is not in a `finally`. A later run with the same PID deletes it at line 307. Harmless.
- **Defect judge.** `defect()` accepts any `input_invalid` reason (lines 140-143), which is what lets X7 through.

## Smallest safe corrections (counter only; none applied)
1. Run all counter and gate git subprocesses with an environment scrubbed of `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_COMMON_DIR` and `GIT_ALTERNATE_OBJECT_DIRECTORIES`. Export blobs with `git ls-tree -rz` plus `git cat-file --batch` (raw objects, no filters or attributes). Alternatively, after `git archive`, assert that every exported file's `git hash-object` equals its `ls-tree` blob id, and exit 2 on any mismatch.
2. Pin K4 to the base oracle: export `citing_set_selftest.py` and `fixtures/citing-set` from 22c1669 and run them against the measured gate with `--gate`. Pass `--min-cases 29` and require the summary to show `cases == 29` and `failed == 0`.
3. Add a per-case expected `reason` to each defect case (for example A7 → `root_not_repository_top_level`). Or add a Git-mode control with a non-empty ledger and a nested root that must not be `clean`. Either one rejects X7.

## Not verified
- I did not run the counter on any revision other than the ones listed above.
- I did not test a `core.attributesFile` attack or a system-level gitattributes file. Both are inferred to behave like the FILTER row [INFERENCE].
- I did not test `GIT_WORK_TREE` alone.
- I did not review the C2 counter.
- The lane HEAD moved to e57f601 and then 8ecbefe (a C1 follow-up that changes the top-level check) while I worked. I did not run the counter at either commit. The findings above are about the counter, and they hold regardless of which gate commit is measured.
- All adversarial commits live only in $S/clone and $S/clone2; $S/clone3 was deleted after the GIT_DIR run.
