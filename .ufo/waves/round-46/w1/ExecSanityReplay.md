# ExecSanityReplay — C1 after-state replay

## Finding

**FAIL — acceptance not met.** The replay comparison could not run because the matrix artifact is missing; this is not evidence that two receipts disagree. Operability axis: blocked by absent executable. Replay-determinism axis: unmeasured. No matrix receipts or normalized diff were produced.

The requested script path `.ufo/waves/round-46/c46_matrix.py` was absent, and a repository-wide filename search found no copy. The lane revision resolved at the attempt was `ded938d2f23aba265d1acf1fdd4b3ab028020037`.

## Exact command and decisive output

```text
python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision ded938d2f23aba265d1acf1fdd4b3ab028020037 --stage after
```

```text
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/c46_matrix.py': [Errno 2] No such file or directory

Command exited with code 2
```

Only the executable-availability attempt ran; it did not create a receipt. No second invocation was made because the executable is absent. No build, lint, test, or formatter was run, and no tool was installed.

## Files written

- `.ufo/waves/round-46/build/replay-proof.md` — requested replay-proof artifact; records absent receipts/diff and the blocker.
- `.ufo/waves/round-46/w1/ExecSanityReplay.md` — this scoped finding report.

## Blocker

The C1 matrix script must be present in the lane checkout before the two fresh-output after-stage invocations and normalized comparison can be performed. This seat did not wait for or modify another seat's work.
