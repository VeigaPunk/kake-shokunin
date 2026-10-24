# ExecRegistryRowCheck

Axis: operability. Built `/fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/registry_row_check.py` (SHA-256 `7282950aac2708d5e51b334b65faddd8c6a32863bbb87263135fd708a3fb594e`). It reads `scripts/*.py` and `SKILL.md` from the requested Git commit/tree, ignores names containing `selftest`, and considers a tool covered only by a markdown table row under exact `Name` and `Entry command` headers. The row must match its kebab name or name the exact script path in Entry command. It exits 1 for missing rows, 0 when none are missing, and 2 for unreadable inputs.

## Baseline evidence

Command: `python3 -B /fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/registry_row_check.py --repo /fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/clone --rev 318561efa67206699fdaf259ffb86e39f2d916a8`

Observed output:
```
revision: 318561efa67206699fdaf259ffb86e39f2d916a8
scripts scanned: 7
missing tools:
scripts/link_preview_audit.py
```
Process exit: **1**. This was the only flagged tool; the non-registry Round-34 evidence table's `Evidence command` cell does not satisfy the Name/Entry command table-row rule. Receipt: `/fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/baseline.receipt.txt` (SHA-256 `c4449a231cdac5628c62bea7bd52cd3bc18adc01b2d142eb29f72d71c82a6f9d`).

## Sample row evidence

To honor the seat's no-commit rule, used a temporary clone and an uncommitted tree snapshot, not a sandbox commit. Added a sample row at `sample-clone/SKILL.md:412` in the sandbox copy. `git -C /fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/sample-clone add -- SKILL.md && git -C /fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/sample-clone write-tree` exited 0 and returned tree `1fb671cd48f317d0769ff8b02cf94841655c7cd1`.

Command: `python3 -B /fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/registry_row_check.py --repo /fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/sample-clone --rev 1fb671cd48f317d0769ff8b02cf94841655c7cd1`

Observed output:
```
revision: 1fb671cd48f317d0769ff8b02cf94841655c7cd1
scripts scanned: 7
missing tools: none
```
Process exit: **0**. Receipt: `/fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/sample-tree.receipt.txt` (SHA-256 `b01b0c9749f3f078bdfa157ff8b704b55f0e7812f870fc9a55ed8cf727b3ce02`).

## Input error evidence and limits

Command: `python3 -B /fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/registry_row_check.py --repo /fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/absent-repo --rev 318561efa67206699fdaf259ffb86e39f2d916a8`

Observed stderr: `registry_row_check: repository path is not a directory`; process exit: **2**. Receipt: `/fast/scratch/hyaku/kake-r35/w1/ExecRegistryRowCheck/unreadable.receipt.txt` (SHA-256 `6921e590ae66bcaf446136d276aa4af942f1dab003f8d494a00c88b4758fea3c`).

No build, lint, formatter, or formal selftest was run. LSP was unavailable in this seat's exposed tools. No tools were installed. The required sandbox-commit variant was not created; the sample-tree evidence above is the no-commit alternative.