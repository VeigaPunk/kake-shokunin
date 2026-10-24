# MutRevertGitTopLevel — C1 counter sensitivity probe (round 28, wave 1a3)

- Seat: KakeR28a3.MutRevertGitTopLevel (leaf mutation tester)
- Subject claim: C1 (operability, repair-first), counter `.ufo/waves/round-28/c1_interface_count.py` (15 checks: U1–U4, A1–A7, K1–K4)
- Probe: one mutation — drop the `_require_top_level(root)` call in `GitSource.__init__` (scripts/citing_set.py:295), the gate added by repair commit b5d423f.

## Commands run (all in scratch clone; lane repo / Go state untouched)

```text
git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin \
  /fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitTopLevel/clone        # exit 0
git rev-parse HEAD   # b5d423fc02057f67a6f3a255808313ce40d29069 (repair commit)
sha256sum scripts/citing_set.py   # 28ba996524b444b2e1c23e3751f3fa662a9a44adbfcb6337a0d23fcebaf8f415
# edit: deleted line 295 (self._require_top_level(root)) — single-line mutation
git -c user.name=mut -c user.email=mut@invalid commit -qam mut        # exit 0 -> 8d25063fde3f15f2e26d374cf5d03574496429a0
sha256sum scripts/citing_set.py   # 6856a9b757d8b17fd574a3caacc742aa00c0937dcfc8e578d41f6d879acf10fd

python3 -B .ufo/waves/round-28/c1_interface_count.py --root /fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitTopLevel/clone \
  --revision HEAD --scratch /fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitTopLevel/count-mut   # EXIT=1 (output: count-mut.json)
python3 -B .ufo/waves/round-28/c1_interface_count.py --root /fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitTopLevel/clone \
  --revision b5d423fc02057f67a6f3a255808313ce40d29069 --scratch /fast/scratch/hyaku/kake-r28a3/w1/MutRevertGitTopLevel/count-ref   # EXIT=0 (output: count-ref.json)
```

## Results

| Run | Revision | Passed/Total | Defect | Control | Exit | Failing ids |
|---|---|---|---|---|---|---|
| Mutated | 8d25063 (HEAD) | **14/15** | 10/11 | 4/4 | 1 | **A7-nested-git-root** |
| Reference | b5d423f | 15/15 | 11/11 | 4/4 | 0 | none |

- A7 failure observed (mutated): exit 0 (want 2), verdict `clean` (want `could-not-evaluate`), no `input_invalid` finding. The removed gate is exactly the behavior A7 probes — the counter catches it.
- Controls K1–K4 all still pass on the mutant (4/4), so the drop is not a blanket refuse/fail artifact.
- Reference run passes all 15 including A7 (`root_not_repository_top_level`), confirming the unmutated repair behavior is intact in b5d423f.

## Verdict

**Mutant killed.** C1 counter is sensitive to removal of the `_require_top_level` gate; A7 is the targeted check. No surviving-mutant counter gap found.

## Restoration / integrity evidence

- Mutation diff (single deletion) as committed in scratch clone:

```diff
@@ -292,7 +292,6 @@ class GitSource:
     def __init__(self, root, revision):
         self.root = root
         self.revision = self._resolve(root, revision)
-        self._require_top_level(root)
```

- Lane repo untouched: scripts/citing_set.py SHA-256 `28ba9965...` (identical to pristine clone before mutation; `_require_top_level` still called at line 295); lane repo HEAD still b5d423f.
- Mutant remains committed in scratch clone at 8d25063 as evidence (scratch only; lane repo not modified).

## Not verified

- I did not run the counter against any other revision or mutation; only the two runs above.
- No tool installed; no pacman/uv/npx action needed.
