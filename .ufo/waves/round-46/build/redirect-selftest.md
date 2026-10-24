# Redirect selftest mutation probe

Axis: operability.

## Result

**FAIL / blocked for the named attack.** The implementation needed to run the attack (`scripts/redirect_audit.py`) was absent when checked and when the required selftest command was run. Consequently, the baseline selftest and all six mutant probes could not be executed. This is a missing-artifact dependency finding, not evidence that any mutant survives. No implementation file was edited.

## Decisive evidence

Command, from the lane repository root:

```text
python3 -B scripts/redirect_audit.py --selftest
```

Verbatim command output (stderr; stdout was empty):

```text
python3: can't open file '/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/redirect_audit.py': [Errno 2] No such file or directory
```

Exit: `2` (`Command exited with code 2`). A subsequent repository read of the same path returned `Path .../scripts/redirect_audit.py not found`.

## Mutant-kill table

| Mutant | Result | Evidence / blocker |
| --- | --- | --- |
| Drop status check | BLOCKED — not run | No source file to copy or selftest to invoke. |
| Drop first-match order | BLOCKED — not run | No source file to copy or selftest to invoke. |
| Drop existing-resource precedence | BLOCKED — not run | No source file to copy or selftest to invoke. |
| Accept malformed rules | BLOCKED — not run | No source file to copy or selftest to invoke. |
| Always-clean return | BLOCKED — not run | No source file to copy or selftest to invoke. |
| Skip URL-decoding | BLOCKED — not run | No source file to copy or selftest to invoke. |

No mutant copy was made and no mutant is scored killed or survived. The task scratch directory `/fast/scratch/hyaku/kake-r46/ExecRedirectSelftest/` was created and remained empty.

## Commands

```text
mkdir -p /fast/scratch/hyaku/kake-r46/ExecRedirectSelftest
python3 -B scripts/redirect_audit.py --selftest
mkdir -p .ufo/waves/round-46/build
```

No tools were installed. Files written: `.ufo/waves/round-46/build/redirect-selftest.md` and `.ufo/waves/round-46/w1/ExecRedirectSelftest.md`.
