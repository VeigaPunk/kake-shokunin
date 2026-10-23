# MutEntryNumbering — r39-controls-a3
Axes: operability (exact finding identity), isolation (key blindness and byte restoration), coverage (single-point faults).
Built nine full-copy, single-point mutants. All nine differ behaviorally from the reference on their included minimal witnesses.
No sealed key, counter, lane implementation, network or sibling source was read/run/modified. Sealed-key outcomes remain for L1.
Manifest: /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants.json
Manifest sha256: d8921ba97018bfe0860ebdc439b8df5b0da7e3dbb640f706aa040b0e090602f2
Each manifest record includes contract sentence numbers, exact change, witness manifest/XML, both full outputs, phase commands/exit codes, and hashes.
Reference sha256 before/after every probe: 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8
Baseline and restored detections passed 10/10 each. All 30 tool invocations exited 1, the expected failed-policy exit; no baseline was counted as a kill.
Local witness verdicts: 9 killed, 0 inconclusive. EQ01 survived as equivalent (identical-pair duplication); its source was deleted, not shipped.
Only the public witnesses were evaluated; these results do not assert sealed-key discrimination.

## Mutants (absolute path, sha256, source location and observed reference → mutant finding sets)
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M01.py:151 | sha256 2e6c259dbb4fe825b5645d3181e73fa0f61026e6dabfeefa16598ae8f393275c | (loc_missing,1) → (loc_missing,0) | killed
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M02.py:151 | sha256 bf48b6d0adb326e241a4e7656044a722077a137d92d84c7ba949a9c870caad11 | (loc_missing,1) → (loc_missing,2) | killed
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M03.py:151 | sha256 bec6aaef0cfcb47f4558eff47f9fcfa5ce73c74527c73ea2ad20792743ed4e56 | (element_unexpected,null), (loc_missing,1) → (element_unexpected,null), (loc_missing,2) | killed
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M04.py:151 | sha256 5f895ff9f3db6f407706e3635d15178b121ced448ca999cd76eed5e0eb95bd65 | (loc_missing,1) → (loc_missing,0) | killed
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M05.py:223 | sha256 5508a2ab6e4ea189c77a4ea1e7733b3801582f97e2867c090ca6afc9e8ec5bdb | (no_entries,null) → (no_entries,0) | killed
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M06.py:145 | sha256 3e688a6f1ca7f8d9521792df0c260cc8a39bd33c6b4e9d497fce3d51d19280fb | (element_unexpected,null) → (element_unexpected,1) | killed
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M07.py:223 | sha256 84522c0f6f08a91b3a1dbe20be7eb48e863b4222c08e5ae17aa77c10e3e5ea19 | (loc_missing,1) → (loc_missing,null) | killed
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M08.py:185 | sha256 1f25190fc07fad871b013df6dac99f4f805e99796079501e29dacedb6227dd76 | (loc_missing,1), (loc_missing,2) → (loc_missing,2) | killed
- /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M09.py:185 | sha256 083487bca238c640676eb8aabf4a4c8a821b128bb6f438e6a295003a3642db5f | (loc_not_absolute,1), (priority_invalid,1) → (priority_invalid,1) | killed

## Commands and receipts
`timeout 10s sha256sum /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py` → exit 0, assigned hash matched.
`timeout 10s sh -c 'command -v python3; command -v timeout; command -v prlimit; command -v bwrap; python3 --version'` → exit 0; Python 3.14.8, all runners present.
Executed M01 command (same exact command for pristine/mutated/restored bytes): `timeout 10s prlimit --as=4000000000 -- bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /bin --dir /tool --ro-bind /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/active/M01/tool.py /tool/tool.py --ro-bind /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/witnesses/M01 /work --tmpfs /tmp --chdir /work /usr/bin/python3 -B /tool/tool.py --manifest /work/manifest.json` → exit 1 on every phase.
Exact commands and exits for all 30 runs: /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants.json, each record's detector_runs; raw captured tool outputs: /fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/receipts/{M01..M09,EQ01}-{pristine,mutated,restored}.json.
Every run: 10s timeout, 4,000,000,000-byte address-space cap, network unshared, environment cleared, read-only /usr, /tool and witness /work; private /tmp. At most two concurrent detectors.

## Scoped findings and restoration
/fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M02.py:151 and M03.py:151 expose ignored/unexpected preceding-root-child numbering faults; M04.py:151 isolates index-only zero-basing.
/fast/scratch/hyaku/kake-r39a3w1/MutEntryNumbering/mutants/M08.py:185 and M09.py:185 expose wrong finding deduplication keys without changing verdict or exit.
EQ01 retained duplicate identical pairs; raw arrays differed but the contract set did not. This is equivalent, not a key-coverage finding.
All mutable slots were restored to the exact supplied hash and rerun successfully before deletion. The local reference.py, all ten restored active tool copies and EQ01.py were removed via edit.
Only mutants, witness fixtures, JSON receipts and mutants.json remain as deliverables; no process remains running. No tools were installed or upgraded.
