# MutRevertGitBlobEmpty — C1 counter sensitivity probe (round 28, wave 1a3)

## What was attacked
C1 (operability, repair-first) counter sensitivity. One mutation in the repaired
gate `scripts/citing_set.py`: dropped the `not_a_directory` and
`corpus_directory_missing` checks in `GitSource.corpus_files` (the two checks the
round-27 routed defect 1 repair added at b5d423f). No other behavior touched.

## Mutation (exact diff)
Commit `24f4afcade7a40bc8225045e291fb2e1f70ed54d` in scratch clone; `scripts/citing_set.py`
only, 4 deletions (blob `c26fcd4..5e35f72`):

```
@@ -354,15 +354,11 @@ class GitSource:
             if not separator or len(fields) < 2:
                 raise InputInvalid("not_a_regular_file", path or None, "corpus")
             mode, kind = fields[0], fields[1]
-            if path == CORPUS_DIR:
-                raise InputInvalid("not_a_directory", CORPUS_DIR, "corpus")
             if mode == "120000":
                 raise InputInvalid("symlink_rejected", path or None, "corpus")
             if kind != "blob" or mode == "160000":
                 raise InputInvalid("not_a_regular_file", path or None, "corpus")
             files.append(path)
-        if not files:
-            raise InputInvalid("corpus_directory_missing", CORPUS_DIR, "corpus")
         return sorted(files)
```

## Commands and exit codes
| Step | Command | Exit |
|---|---|---|
| Clone | `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitBlobEmpty/clone` | 0 |
| Mutate (edit tool) | CUT lines `357.=358` and `362.=363` in `clone/scripts/citing_set.py` | n/a |
| Commit | `git -C clone add -A && git -C clone -c user.name=mut -c user.email=mut@invalid commit -qam mut` | 0 |
| Reference counter | `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-28/c1_interface_count.py --root clone --revision b5d423fc02057f67a6f3a255808313ce40d29069 --scratch .../count-ref` | **0** |
| Mutated counter | same, `--revision HEAD --scratch .../count` | **1** |

## Observed outputs
- Reference b5d423f: **15/15** — 11/11 defect, 4/4 control. All cases green.
- Mutated HEAD 24f4afc: **13/15** — 9/11 defect, 4/4 control. Failing exactly:
  - `A2-corpus-absent-git` — reasons: `exit 0, want 2`, `verdict 'clean', want 'could-not-evaluate'`, `no input_invalid finding`
  - `A4-corpus-blob-git` — same three reasons
  - Controls pass unchanged: K1-valid-clean-working-tree, K2-valid-clean-git,
    K3-valid-failed-missing-pair, K4-fixture-selftest.
- Stderr of both counter runs: 0 bytes.

## Verdict
**Mutant killed.** The counter drops from 15/15 to 13/15 and flags exactly the two
defect cases the removed checks enforce (A2 absent corpus surface at a revision;
A4 corpus surface committed as a blob), each failing as a false green (`clean`,
exit 0). Controls K1–K4 still pass, so the counter is not over-sensitive to this
mutation. Baseline was green (15/15 at b5d423f), so the failures are attributable
to the mutation — not inconclusive.

## Restoration / hash evidence
- Scratch clone is the disposable sandbox the tasking designates for this mutation
  (commit explicitly requested); no restoration required.
- Lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin` was not written by me
  except this report; no mutating git command was run on it (status --porcelain
  showed 10 lines, all from other seats' concurrent work).
- Hashes of `scripts/citing_set.py`:
  - before (b5d423f): blob `c26fcd498f1974265e6bb80dca8e102f57eb7b5f`, sha256 `28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415`
  - after (HEAD): blob `5e35f725770d05cd36eb5f03ba9e92e0769e3e8f`, sha256 `9ca7f1ff1fcf2b60620696bbb65bdfc41dbbf3d9e16a0d693134f36c9c4a0954`
- Clone working tree clean after commit (0 porcelain lines).

## Evidence pointers
- Reference output: `/fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitBlobEmpty/count-ref.json`
  (`passed 15`, `total 15`)
- Mutated output: `/fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitBlobEmpty/count-mut.json`
  (`passed 13`, `total 15`, failing A2/A4)
- Mutation diff: `/fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitBlobEmpty/mutation.diff`
- Clone: `/fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitBlobEmpty/clone` at `24f4afc`

## Tooling
No installs or upgrades performed (none needed). No network access used.
