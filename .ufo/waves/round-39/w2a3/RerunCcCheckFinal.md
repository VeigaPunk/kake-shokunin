# RerunCcCheckFinal — QUALITY (j) v2.1
Axes: operability (receipt accounting and mutation sensitivity); freshness unchanged (offline).
Scope: replay A/B and all eight wave-1 selftest survivors, including M07/M09 already killed by wave-1 receipt replay; no round verdict.
`S=/fast/scratch/hyaku/kake-r39a3w2/RerunCcCheckFinal`; `L=/home/vgpnk/Projects/shokunin/kake-shokunin`. Paths below are relative to S unless prefixed L.
Pinned checker: L/.ufo/waves/round-39/criteria/control_consequence_check.py, last-changing revision `77b2a86ea101922977f5a99b5320a828969006fc`; pristine.py SHA256 `5952be5a3e39c594ffcfd9373c621690da9189a0d0d0b9fd1adf7b4f902ff33b`.
Copied all 77 final a3 receipt JSONs byte-for-byte; manifest.json records every source/copy path, byte size and equal SHA256. No receipt rows/why were displayed; the checker alone consumed their contents.
Counter copied as counter.py, SHA256 `f3a0cd6053497cd05b6a57ab712552146960c1efe2f8fb50eee36bace6084593`; read as constants only, NEVER executed.
## Commands and actual outputs
`timeout --kill-after=5s 60s prlimit --as=4000000000 python3 -B /fast/scratch/hyaku/kake-r39a3w2/RerunCcCheckFinal/setup.py` → 0; four bounded fixture Git commands → 0 each (manifest.json).
`timeout --kill-after=5s 300s prlimit --as=4000000000 python3 -B /fast/scratch/hyaku/kake-r39a3w2/RerunCcCheckFinal/probe.py` → 0; two workers, per-detector process-group deadlines 20s, AS=4000000000.
A: `timeout --kill-after=2s 20s prlimit --as=4000000000 python3 -B $S/pristine.py --root $L --counter $S/counter.py --receipts $S/rx` → 1.
> receipts read 77; build receipts meeting 0; oracle-exempt 0; controls meeting 17; problems 0
B: same exact argv plus `--oracle-sha 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8` → 1.
> receipts read 77; build receipts meeting 0; oracle-exempt 1; controls meeting 16; problems 0
> EXEMPT /fast/scratch/hyaku/kake-r39a3w2/RerunCcCheckFinal/rx/ref.json (oracle 663e051e10b9)
A = reference + 15 mutants + CtlRegexTweak; B exempts only reference. Both recorded readings **hold**; full stdout/stderr/argv/exits: logs/reading-A.txt and logs/reading-B.txt.
## Identical pristine → mutant → restored detectors
Each stock subject used `timeout --kill-after=2s 20s prlimit --as=4000000000 python3 -B $S/subjects/<artifact>.py --selftest` in all three phases; all pristine/restored runs printed `PASS 20/20`, exit 0.
One-point mutations match wave-1 exactly; M09/M10 move to v2.1's shared exit_code, not an invented CLI-only override. Source locations below refer to the pinned checker.
| Artifact under mutants/ | Point / attacked statement | Mutant output; exit | Verdict / statement | Mutant SHA256 |
|---|---|---|---|---|
| M05_ignore_key.py | :67 foreign key rejected | PASS 19/20; 1 | killed; holds | 2b8aec039245ae99e085360d3e528b7edcff43e3bc3fb4bcbe5d93aac720c843 |
| M06_revision_identity.py | :107 revision resolved to bytes | PASS 20/20; 0 | survived stock selftest; coverage overstated, byte-identity behavior holds in focused check | 8dfe25b60db4216abe150447f566cdc02c41ecf9df5959bcfb03d29a8327e86a |
| M07_implicit_oracle.py | :85 ref label not an exemption | PASS 19/20; 1 | killed; holds | 685e542b129fa82dfecc5c668b42bbde776eb22bf75fae152daaf9c879d279ab |
| M09_swap_control_exit.py | :125 control/clean exit mapping | PASS 8/20; 1 | killed; holds | 11c610cd5b63738c1a44a3b347c17387a95bfd5ab80c8fd3c39c99e8b0342773 |
| M10_problem_exit_one.py | :124 problems exit 2 | PASS 12/20; 1 | killed; holds | 94b96bed88483ee6ce05314b72738b2d1c0437e4921310974fc441c82293bbb3 |
| M11_rows_plus_one.py | :76 exact row count | PASS 19/20; 1 | killed; holds | 95e099a1bb71abb9ee713672a03b14152cac2a5c5ccdd6dff32fd38df052790d |
| M12_ignore_target.py | :68 target pin checked | PASS 19/20; 1 | killed; holds | d549ae8431743bd4bbadbcb81595e7efdbc2130926583b3ce0b3e4420b6a6809 |
| M14_ignore_passed.py | :77 passed total checked | PASS 19/20; 1 | killed; holds | eb78fb4d39eb1f27906f517897c7d8089759ba2cee68ef3134de477490a6731d |
Actual killing outputs include `FAIL foreign key sha: exit 1 want 2`, `FAIL label 'ref' without --oracle-sha is a control: exit 0 want 1`, `FAIL extra row is not a meet: exit 2 want 0`, `FAIL foreign target: exit 1 want 2`, `FAIL passed total contradicts rows: exit 1 want 2`; all complete outputs retained in logs/.
Result: stock v2.1 kills 7/8 prior selftest survivors; M06 survives. No inconclusive baselines.
## M06 killing fixtures and sandbox patch
Finding: L/.ufo/waves/round-39/criteria/control_consequence_check.py:174 passes a precomputed B directly to evaluate, bypassing main's revision lookup at :107.
Authored synthetic-only fixtures/build-root Git repository and fixtures/{same_bytes_build,foreign_bytes_control}/r.json; no claimed tool/reference/key implementation used or executed.
For M06 the identical three-phase command was `timeout --kill-after=2s 20s prlimit --as=4000000000 python3 -B $S/subjects/M06_revision_identity.py --root $S/fixtures/build-root --counter $S/fixtures/counter.py --receipts $S/fixtures/<F> --build-revision <R>`.
F=same_bytes_build, R=HEAD: pristine/restored `build receipts meeting 1; ... controls meeting 0`, exit 0; mutant `build receipts meeting 0; ... controls meeting 1`, exit 1 — **killed**.
F=foreign_bytes_control, R=HEAD: all phases CONTROL-MEETS, exit 1 (negative guard, not itself a kill).
F=same_bytes_build, R=__missing_fixture_revision__: pristine/restored `cannot evaluate: ... exit status 128`, exit 2; mutant CONTROL-MEETS, exit 1 — **killed**.
`killing-fixtures.patch` adds three main-path fixtures only; sandbox patched/control_consequence_check.py:179-212 constructs the synthetic Git object and checks matching bytes, different bytes and unresolved revision.
Augmented subject P_M06_revision_identity used the same bounded --selftest command in all phases: pristine `PASS 23/23` exit 0 → mutant `PASS 21/23` exit 1 → restored `PASS 23/23` exit 0 — **killed**.
Actual failures: `FAIL main recognizes build bytes through HEAD: exit 1 want 0`; `FAIL main rejects an unresolved build revision: exit 1 want 2`.
## Hashes, restoration, bounds
All eight stock subjects' before/after SHA256 equal `5952be5a3e39c594ffcfd9373c621690da9189a0d0d0b9fd1adf7b4f902ff33b`; augmented subject before/after equal `03419ef0a38e837af7676ae526a77a5df704bb9e6c8b2e92b6dd5275ae37e5aa` (patched pristine).
Augmented mutant patched/M06_revision_identity.py SHA256 `5cb6038d11c502bcaab320822d91a01e77742f7aaf87b85bc690c89ec70b7411`; immutable mutant artifacts intentionally retained; every mutable subject restored in finally, including behavioral reruns.
Patch SHA256 `583f541564d816b6bd10e009678d606f99fb6185b116c73488916a10b9b7ab3e`; generation `diff -u --label a/.ufo/waves/round-39/criteria/control_consequence_check.py --label b/.ufo/waves/round-39/criteria/control_consequence_check.py $S/pristine.py $S/patched/control_consequence_check.py` → 1 (differences, expected).
results.json SHA256 `f19cd10947407168361c70b9c3ef9d993812f7f54ca7ba71f5aabd17d221ebe2`; contains every absolute argv/stdout/stderr/exit, before/mutant/after hash and verdict.
manifest.json SHA256 `1089eab2392d95f419864ada78738ea8bd58efc7b04b0e65cd8af6de5ba2427f`; probe.py SHA256 `c8ddbc8ebf94fdbb02c1308ec501414e8f4bb0caddfdf5c145a07facf4c4d2cf`.
logs/reading-A.txt SHA256 `e41ed39c9a84ffdfa33424f8ed3dc10984b5c69374a45db2a0f9728b23a041d4`; logs/reading-B.txt SHA256 `f4bba9673ffc65ce401cebdad87dfc52ae002922d340ea65b6f76a708c505f70`.
Tools: bounded `python3 --version` and `git --version` → 0 each: Python 3.14.8, Git 2.56.0; no installs/updates. Bounded read-only git log → 0. Scratch total 965878 bytes; process groups killed after each run, active groups empty at completion.
Only sandbox and this report written; no counter run, sealed-key access, network, lane integration or sibling edits. Patch is ready for L1 review, not applied to lane.
