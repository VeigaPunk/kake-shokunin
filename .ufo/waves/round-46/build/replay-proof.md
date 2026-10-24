# C1 after-state replay proof

**Result: FAIL — acceptance not met; replay determinism is unmeasured.** This is a missing-artifact finding, not an observed replay disagreement.

The requested matrix script is absent at `.ufo/waves/round-46/c46_matrix.py`; a repository-wide filename search found no copy. The lane revision resolved before the attempt was `ded938d2f23aba265d1acf1fdd4b3ab028020037`.

Attempted command:

```text
python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision ded938d2f23aba265d1acf1fdd4b3ab028020037 --stage after
```

Verbatim output:

```text
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/c46_matrix.py': [Errno 2] No such file or directory

Command exited with code 2
```

No matrix run completed, so there are no receipts or normalized diff, no counted fields can be compared, and no fresh matrix output directories were produced. A second run was not attempted because the requested executable is absent. The item's named replay-divergence attack cannot be judged from this evidence; do not treat this as a determinism pass.

Files written:
- `.ufo/waves/round-46/build/replay-proof.md`
- `.ufo/waves/round-46/w1/ExecSanityReplay.md`
