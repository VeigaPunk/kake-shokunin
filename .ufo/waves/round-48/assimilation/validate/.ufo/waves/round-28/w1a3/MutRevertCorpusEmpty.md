# MutRevertCorpusEmpty — C1 counter sensitivity probe

Round 28 (attempt 3), wave 1. Seat: mutation tester (leaf). Lane repo: kake-shokunin.

## Mutation

Target: `WorkingTreeSource.corpus_files` in `scripts/citing_set.py` (repaired gate at b5d423fc).
One mutation: drop the `corpus_empty` check (`if not found: raise InputInvalid("corpus_empty", ...)`).

```
diff --git a/scripts/citing_set.py b/scripts/citing_set.py
index c26fcd4..766c515 100755
@@ -256,8 +256,6 @@ class WorkingTreeSource:
             raise InputInvalid("not_a_directory", CORPUS_DIR, "corpus")
         found = []
         self._walk(base, found)
-        if not found:
-            raise InputInvalid("corpus_empty", CORPUS_DIR, "corpus")
         return sorted(found)
```

Evidence: mutation diff at `/fast/scratch/hyaku/kake-r28a3/w1/MutRevertCorpusEmpty/mutation.diff`.
Blob hashes: pristine (b5d423fc) `scripts/citing_set.py` = `c26fcd498f1974265e6bb80dca8e102f57eb7b5f`; mutant = `766c51574c5b38969fcf1766ef2e6c7407d775df`; mutant working-tree sha256 = `1a39c0195e081dec99ad545219a94c2280fbe7f06a17880cc15e06fbb46ae5a7`.

## Commands

```
git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin \
  /fast/scratch/hyaku/kake-r28a3/w1/MutRevertCorpusEmpty/clone
# clone HEAD = b5d423fc02057f67a6f3a255808313ce40d29069, status clean
# edit clone/scripts/citing_set.py (drop corpus_empty check), then:
git -c user.name=mut -c user.email=mut@invalid commit -qam mut      # exit 0 -> f3d6e89
python3 -B .../c1_interface_count.py --root clone --revision HEAD \
  --scratch .../count-mutant                                      # exit 1
python3 -B .../c1_interface_count.py --root clone --revision b5d423fc... \
  --scratch .../count-ref                                          # exit 0
```

## Observed outputs

Mutant `f3d6e89c020b9a12af72693dec9c74082810b1be`:
- **14/15 passed**; defect 10/11; control 4/4; counter exit 1.
- Failing check: `A3-corpus-empty-working-tree` [defect]: reasons `exit 0, want 2; verdict 'clean', want 'could-not-evaluate'; no input_invalid finding`.
- Controls K1–K4 all passed (including K4 fixture selftest).

Reference `b5d423fc02057f67a6f3a255808313ce40d29069` (unmutated repaired gate):
- **15/15 passed**; defect 11/11; control 4/4; counter exit 0.

Outputs: `.../count-mutant.json`, `.../count-ref.json` (counter JSON, includes per-case reasons).

## Verdict

Mutant **killed**: the counter catches removal of the corpus_empty check (fails A3; controls stay green). No surviving mutant. Counter sensitivity confirmed: repaired gate 15/15; the smallest behavior-bearing relaxation of the working-tree empty-corpus gate drops to 14/15 with exactly A3 failing.

## Restoration

Scratch clone is task-declared disposable; pristine bytes are the committed blob at b5d423fc (`c26fcd4...`), re-measured byte-identical by the reference run (15/15). Lane repo, sibling lanes, jj state, and Git index untouched — only file written in the lane is this report. No installs performed (none needed). Not verified: I did not run any other wave's counters or the L1 integration runs.
