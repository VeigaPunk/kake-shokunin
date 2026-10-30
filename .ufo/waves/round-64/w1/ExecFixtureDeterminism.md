# ExecFixtureDeterminism — round 64

## Verdict

The fixture builder is tree-deterministic across two independent builds: all four repositories had identical `git ls-tree -r HEAD` output between build A and build B. The stub fixture blob also matches the committed `stub_tool.py` source blob exactly in both builds. No tree differences found.

## Evidence

Builder behavior is defined at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/fixtures/build_fixtures.py:75-93` (fixture init/config/add/commit and toplevel assertion), `:96-112` (base-revision inputs and stub bytes), and `:114-141` (the four fixture definitions). The source stub is `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/fixtures/stub_tool.py:1-25`; the builder assigns those bytes to `scripts/quote_class.py` at `build_fixtures.py:111-115`.

Command executed twice, with distinct output directories and explicit lane root:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/fixtures/build_fixtures.py /fast/scratch/hyaku/kake-r64/ExecFixtureDeterminism/build-a --lane /home/vgpnk/Projects/shokunin/kake-shokunin
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/fixtures/build_fixtures.py /fast/scratch/hyaku/kake-r64/ExecFixtureDeterminism/build-b --lane /home/vgpnk/Projects/shokunin/kake-shokunin
```

Both exited 0. Each fixture's toplevel was asserted to resolve to its own fixture directory before recording its `git ls-tree -r HEAD` tree. Recorded revision/tree-blob counts were:

```text
build-a: stub-repo f9a49d7c6ed5eff522c802dae8c29704e209b6e0 (1 blob)
build-a: marker-repo 22859f6631a4d9d645aa1775c04f94f9f23c9bc4 (9 blobs)
build-a: fabrication-repo 5ef5d7d7fdcc0c58ee3c1b0d75d697e8be3fbb3a (9 blobs)
build-a: junk-repo ee53d9772a83916ecd99665ea60e087841214c0e (9 blobs)
build-b: stub-repo f9a49d7c6ed5eff522c802dae8c29704e209b6e0 (1 blob)
build-b: marker-repo 22859f6631a4d9d645aa1775c04f94f9f23c9bc4 (9 blobs)
build-b: fabrication-repo 5ef5d7d7fdcc0c58ee3c1b0d75d697e8be3fbb3a (9 blobs)
build-b: junk-repo ee53d9772a83916ecd99665ea60e087841214c0e (9 blobs)
TREE_COMPARE stub-repo: IDENTICAL
TREE_COMPARE marker-repo: IDENTICAL
TREE_COMPARE fabrication-repo: IDENTICAL
TREE_COMPARE junk-repo: IDENTICAL
```

Stub source comparison used Git's blob hash (not raw SHA-1):

```text
git -C <lane> hash-object .ufo/waves/round-64/fixtures/stub_tool.py
=> 13926364f45db082a11a95bd592a79b1251f3a14

git -C /fast/scratch/hyaku/kake-r64/ExecFixtureDeterminism/build-a/stub-repo rev-parse HEAD:scripts/quote_class.py
=> 13926364f45db082a11a95bd592a79b1251f3a14; match=True

git -C /fast/scratch/hyaku/kake-r64/ExecFixtureDeterminism/build-b/stub-repo rev-parse HEAD:scripts/quote_class.py
=> 13926364f45db082a11a95bd592a79b1251f3a14; match=True
```

The differing commits anticipated by the assignment did not occur in this run: both runs produced the same four commit revisions as well as identical trees. Scratch directories were removed after capturing the results. No tools were installed; no lane files were modified.