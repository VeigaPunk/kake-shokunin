# C1 probe variant construction audit

Axis: operability. Scope: variant construction/diffs only; no lane source was changed.

Baseline runner was extracted from `5777d5af79cac1ebf9144b348a9d274099e77338` to the isolated sandbox. `pristine.py` SHA-256: `7a6365e0e72fa513136d433b4dc3d382c8ca4812076e52a49836668f1c68827f`. Probe SHA-256: `74bf1f80d79e830d2a5c30a711dad3172f79135af1212e998860afb653b9e047`. Source pointers: `pristine.py:363-367`; probe docstring `clone/.ufo/waves/round-33/c1_code_probe.py:7-30`, regex/constants `:51-57`, helper `:83-93`, construction `:131-136`.

## Variant diffs and verdicts

- `pristine`: applicable; exact; empty unified diff (0 lines). Variant SHA-256 equals baseline.
- `reworded`: applicable; exact; only the requested guard message fragment changes (7 unified-diff lines):

```diff
--- pristine.py
+++ reworded.py
@@ -365,3 +365,3 @@
         if step["op"] == "git_commit" and not initialized:
-            raise ValueError("%s setup op 'git_commit' needs an earlier 'git_init'" % CASE_SETUP_FILE)
+            raise ValueError("%s setup op 'git_commit' requires a prior git_init step" % CASE_SETUP_FILE)
     return {"argv": argv, "root": root, "setup": setup}
```

- `m3`: applicable; exact; only the guard `if` and its one-line `raise` are deleted (7 unified-diff lines):

```diff
--- pristine.py
+++ m3.py
@@ -364,4 +364,2 @@
             initialized = True
-        if step["op"] == "git_commit" and not initialized:
-            raise ValueError("%s setup op 'git_commit' needs an earlier 'git_init'" % CASE_SETUP_FILE)
     return {"argv": argv, "root": root, "setup": setup}
```

- `recoded`: not applicable on the baseline because that guard has no `"setup_commit_before_init"` literal; exact per the docstring's absent-pattern rule; no diff is produced. This means its killed expectation is unmet on this legacy runner.

## Contract-shaped guard check

Hand-constructed guard raise line:

```python
raise SetupRefusal(code="setup_commit_before_init", message="%s setup op 'git_commit' needs an earlier 'git_init'" % CASE_SETUP_FILE)
```

`replace_in_guard` found one guard and returned an applicable recoded source. Its 7-line diff changed only `"setup_commit_before_init"` to `"setup_commit_recoded"`. Contract-shaped source SHA-256: `1c99f7b051bbb410239acef96e88a6d4cde217816e9f9e0e8ec5aba4e9f8d22d`; recoded SHA-256: `59038ea821e9af1ec932890379da73e6d0221bde24bff4f307aabd7bc5698cff`. This was a source-shape check, not execution of the runner or hostile selftest.

## Commands and observed results

1. `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; mkdir -p /fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/tmp; export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/tmp; git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/clone && git -C /fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/clone checkout -q bc6c4a8d435473f3c30903210be30d9d6e3ef750` — exit 0.
2. `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/tmp; git -C /fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/clone show 5777d5af79cac1ebf9144b348a9d274099e77338:scripts/citing_set_selftest.py > /fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/pristine.py && sha256sum /fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/pristine.py` — exit 0; printed the baseline hash above.
3. `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/tmp; python3 -B /fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/variant_audit.py` — exit 0; output showed the diffs and applicability results above. Audit source: `/fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/variant_audit.py`.

4. `sha256sum /fast/scratch/hyaku/kake-r33/w1/MutC1ProbeVariants/pristine.py` — exit 0; output matched the baseline hash above.

The pristine runner bytes were never edited; before/after SHA-256 is identical (`7a6365e0e72fa513136d433b4dc3d382c8ca4812076e52a49836668f1c68827f`), so no restoration was needed. Behavioral detector verdict is inconclusive/not run; the exact/inexact findings above are source-construction results only.
