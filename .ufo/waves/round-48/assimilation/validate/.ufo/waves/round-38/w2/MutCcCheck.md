# MutCcCheck — QUALITY (j) mutation sensitivity
Axes: operability (detector reliability); freshness held constant (offline; no requests).
Attack: `corpus/QUALITY.md:939-947`, checker at tip `adab4c7e9ec2178657395f49346f18800ff4796f`; only isolated copies mutated.
Verdict — reported selftest 10/10 and round-37 red exit 1: **holds** on pristine and restored bytes.
Verdict — sensitivity: **11 survived, 4 killed, 0 inconclusive**; broad regression assurance would be overstated. This is a coverage finding, not a pristine correctness defect or round-admission judgment.
All 11 survivors preserve both detector outputs, stderr and exits byte-for-byte, yet change their targeted behavioral witness. Every mutant changes exactly one source line.

Commands actually run (cwd `$C`; GIT_* stripped, TMPDIR=`$S/tmp`, PYTHONDONTWRITEBYTECODE=1):
```sh
S=/fast/scratch/hyaku/kake-r38w2/MutCcCheck
C=$S/clone
R=99357694f68886d3175fc6c386979c350be789bc
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=$S/tmp PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=2s 900s python3 -B $S/detector.py pristine # exit 0
 timeout --kill-after=2s 180s python3 -B $S/detector.py mutated # exit 0; same normalized environment via subprocess.run
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=$S/tmp PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=2s 900s python3 -B $S/detector.py restored # exit 0
```
Before the mutated invocation, applied the 15 single-line edits recorded in specs.json; restored all probe bytes in a finally block before the restored invocation.
For each M=M01..M15, the same stage detector executes these actual argv, each with a 60 s subprocess deadline and 4,000,000,000-byte address-space cap:
```sh
prlimit --as=4000000000 -- python3 -B $S/probes/$M.py --selftest
prlimit --as=4000000000 -- python3 -B $S/probes/$M.py --root $C --revision $R --verification .ufo/waves/round-37/verification
prlimit --as=4000000000 -- python3 -B $S/probes/$M.py --root $C --verification $S/fixtures/$M
```
Every pristine/restored selftest: exit 0, `selftest: 10/10 ok`; round 37: exit 1, `RESULT: FAIL exit=1  tainted_counters=1  violations=2` (54 receipts; 7 controls).
Table: S=selftest exit/count; R=round-37 exit; W=targeted witness pristine/mutant/restored exits. Killed/survived uses only S+R, including exact outputs; W proves non-equivalence.
| Mutant:line | Single-point defect | S | R | W | Verdict | Mutant sha256 |
|---|---|---|---|---|---|---|
| M01:86 | canonical `[-_]` -> `-` | 0/10/10 | 1 | 1/0/1 | survived | `58fba7b4a0b551fe2d92e8c286391382f23bd7e7dab633b3c91554f0befe6e5f` |
| M02:88 | remove `controls` directory | 0/10/10 | 1 | 1/0/1 | survived | `94eed1eee93864c466b63204460e9d360fde4ca5e18480869bf7ae512bd80e95` |
| M03:87 | remove optional `rNN-` seat prefix | 0/10/10 | 1 | 1/0/1 | survived | `45c1f4ba142661973c3d4e80f5f7221db50aed1dd1bc1cc8056b1a68b8f3e0a8` |
| M04:87 | remove `critic` seat alternative | 0/10/10 | 1 | 1/0/1 | survived | `05eafd6ae76a012b9060a273dd35ce9c7a58a0dc4da21a1c8b92369f8a81b53b` |
| M05:95 | remove `claim[-_]` alternative | 0/10/10 | 1 | 1/0/1 | survived | `de50b4f53a3ac747a2b411452fc3ea4566da950a8c757b5919f1d190631e6e66` |
| M06:95 | `c\d+` -> `c1` | 0/10/10 | 1 | 1/0/1 | survived | `087b08aef5c0f414d73402e5c91b59730de9ecf659d5dd6c88f8ab08cad33c62` |
| M07:95 | numeric-claim `[-_]` -> `-` | 0/10/10 | 1 | 1/0/1 | survived | `d2eaeb569272f61e3c067acfa0279517e547be36b62bd9eeac3f5fc52135155e` |
| M08:251 | remove control `met is True` guard | 2/9/10 | 1 | 0/1/0 | killed | `01c55ef02d7d9d5fb733c6862237edd7aa7c6bb0df9351159fce74f87edbd7bd` |
| M09:158 | omit counter `.strip()` | 0/10/10 | 1 | 1/0/1 | survived | `dd9d96b6e17f7eb65d61a5a5a6b1311b113e07cf38630e0477feea6a745b5a5d` |
| M10:160 | claim `met` accepts `int` | 0/10/10 | 1 | 2/0/2 | survived | `3fdaad26100f3952518490416d149db7816ad06305f2b778293b0130be0fa25f` |
| M11:146 | malformed-JSON named guard -> `False` | 0/10/10 | 1 | 2/0/2 | survived | `a481c3c75358c0de6e473c93695f33933a329e1b9081666319684d832430b85a` |
| M12:451 | CLI InputError `return 2` -> `0` | 0/10/10 | 1 | 2/0/2 | survived | `41bed3c3544fab8efaa9bbcf8c75701a1e02c6a0c9642baabbd0ef6cf86bd40b` |
| M13:177 | `dirnames.sort()` -> `.clear()` | 2/8/10 | 1 | 1/0/1 | killed | `2ebd102815f7496ff2abb925248daa6a274e7c5fbfae271f76b2d2cff64caf1f` |
| M14:257 | `not r.control` -> `r.control` | 2/7/10 | 0 | 1/0/1 | killed | `cf7441a585d0fcf99b57f8bb1a08f3d32ea2bcfb1230c614c79618d788769dce` |
| M15:163 | disable missing-control-met guard | 2/9/10 | 1 | 2/0/2 | killed | `cf1a97079e1fc24b6f3e5443b0bf5180f8488a4a127601c0d1da74520555d167` |
Each mutant snapshot is `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/mutants/MNN.py`; active `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/probes/MNN.py` copies are restored.
M11 is especially misleading: selftest still prints `ok malformed control -> 2`, but mixed valid-claim + malformed-control input prints `skipped (not a receipt): control-shortcut.json (not JSON)` and PASS exit 0. The selftest masks the lost error through its separate no-receipts branch (checker:349-351,391-406; evidence/mutated-M11.json:25-30,73-78).
M12 still emits “verification directory not found” to stderr but returns 0; the selftest never invokes main for its input-error negatives (checker:391-406,449-451; evidence/summary.json:248-266).
Restoration: all 15 before/after sha256 = `d8415484cb39b55c9347ad2b94e0b6d097fcb6e2544a7c94f99d2d267edf6ee2`; all restored S/R/W outputs and exits exactly match pristine. Evidence/summary.json records this per mutant.
Absolute evidence pointers and sha256 (all commands, full stdout/stderr, exits and byte hashes retained):
- `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/evidence/summary.json:6-24` — `8eb9742331546cde9dfc081485b54dd0a35cc1a227485d9aafadf5e3a1dba224`
- `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/evidence/pristine.json:1` — `71d12eb28419562a8686da317f034d2d84ed8ceb1ef8596b7ec5192c36f7fcc1`
- `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/evidence/mutated.json:1` — `cf8ea4f265092713b0293cae6b9e22ddb563142ac6f4ff9028fb126d9bd60f02`
- `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/evidence/restored.json:1` — `c86156a6b67bb81a3ce513d906230b95918390a8dabc0562bfeaa5840bfd6794`
- `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/specs.json:1` — `6e42effb1695c0170902f83b8e5231509325c047334f7c6d58271e01c0b95537`
- `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/detector.py:33-75` — `8365f7367b6bb55b974ec13999752e5a4ff1c075fbac4d4d5a9b1ddbd784c70c`
- `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/mutant-inventory.json:1` — `4fc47436e5db97dfce03fb1130857f24e490f9fdb9005b9e8d94a8ef28f66004`
- `/fast/scratch/hyaku/kake-r38w2/MutCcCheck/evidence/SHA256SUMS:1` — `41b4064cc43d0c8e3b3f722cef51ef44662804fecaf1352e3a956a2a81950fcf` (absolute paths and hashes for every probe, snapshot, fixture and receipt).
Bounds: 135 child detector invocations completed, no timeout; two workers, with process groups reaped/killed after each invocation. No subagents, network, tool installs, index writes or lane-source changes; only this report is written outside the sandbox.
M09 probes existing whitespace normalization, not an additional promise in QUALITY (j). No contract change or fix is proposed.
