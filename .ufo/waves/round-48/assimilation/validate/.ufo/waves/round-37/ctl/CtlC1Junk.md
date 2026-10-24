# CtlC1Junk — fixed non-JSON controls
Axes: malformed-output rejection, cheap control fidelity, byte-exact restoration/isolation.
Skips all manifest/body/robots reads, validation and audit logic; both 69-byte tools always print `not a report\n`, stderr empty, and exit 1 (observed).
Exit choice: [INFERENCE] public C1 allocates 20 policy cases (a–e) versus 8 fault cases (f–g), with mixed holding/failing checks; failed-policy/1 is the strongest honest majority guess, not knowledge of the key.
Item 2 round-36 score: passed=0, cases=28, met=false, counter exit=1; exact stdout in r36-junk.json and exit in r36-junk.exit. Item 1 is for L1 scoring; I did not run its sealed counter.
Mutant: only the disposable probe copy’s __main__ dispatch changed to print junk and exit 1. Expected detector: frozen round-36 counter rejects non-JSON even with policy-failure exit.
Observed same detector on pristine → mutant → restored: 28/28, met=true, exit=0 → 0/28, met=false, exit=1 → 28/28, met=true, exit=0. Verdict: KILLED; not an inconclusive baseline failure.
Probe before/after SHA256: 3e5457a9b72afbded2b4f39bb9efc069ea7e642c1593b0536bd65a612fd788b9 (exact match); mutant SHA256: f0767439c33467bea160a272e4dc43311168295df0fdfa823e9d242bd66682cf.
No round-37 key/private path read or copied; only the explicitly authorized revealed round-36 key revision was consumed by its counter. No source outside my scratch changed; no processes/jobs remain; no tools installed or updated.
## Deliverables — absolute path and SHA256 (lane/ is only the working clone)
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/robots_audit.py — `4c23062f6e2dd2890e10bf69e2b08dfe789eb1ceaa03ee9be59bf118b8fcb33e`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/source_recheck_junk.py — `4c23062f6e2dd2890e10bf69e2b08dfe789eb1ceaa03ee9be59bf118b8fcb33e`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-junk.json — `b5535cc3f8140b1c0dd7273fd9c92eac3728501bb95c43247beb508c44c2ae67`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-junk.exit — `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-pristine.json — `9994e17ae6a29e1e850fd6827705b51291542b52b5f67865fbb9eae452a466b5`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-mutated.json — `669fefc1f717a2e3c4e9ddd085ed2d22190d994072d7ea8064d129c3d79513f2`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-restored.json — `9994e17ae6a29e1e850fd6827705b51291542b52b5f67865fbb9eae452a466b5`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/probe_source_recheck.py — `3e5457a9b72afbded2b4f39bb9efc069ea7e642c1593b0536bd65a612fd788b9`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/mutation-evidence.json — `b0f273e17c8fffcbc8afba6450b4b6f22d81ed48a4c2520f282fa97eab757a12`
/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/commands.json — `09e83258538d177333d02b7adfa9042bfd4ec411c591e34e9512a9186940ce60`
## Exact commands and exits
Counter/smoke/restore cwd: /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane; env: TMPDIR=/fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/tmp, PYTHONDONTWRITEBYTECODE=1; GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset. Other command cwd: sandbox root, except clone setup cwd=/home/vgpnk/Projects/shokunin.
`timeout 20 mkdir -p /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk && timeout 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -c core.hooksPath=/dev/null clone /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane && timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane -c core.hooksPath=/dev/null checkout --detach 202d625a323a09d519aaeb9a1be150c228859e26` → exit 0
`timeout 20 mkdir -p /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/tmp && timeout 20 cp -p /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane/scripts/source_recheck.py /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/probe_source_recheck.py` → exit 0
`timeout 10 python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/source_recheck_junk.py` → exit 1
`timeout 10 python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/robots_audit.py` → exit 1
`timeout 600 python3 -B .ufo/waves/round-36/sealed_count.py --root /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane --tool-file /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/source_recheck_junk.py --key-revision fd1fb723624b742a00a6e8e908f3b42901d627f8` → exit 1
`timeout 600 python3 -B .ufo/waves/round-36/sealed_count.py --root /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane --tool-file /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/probe_source_recheck.py --key-revision fd1fb723624b742a00a6e8e908f3b42901d627f8` → exit 0
`timeout 600 python3 -B .ufo/waves/round-36/sealed_count.py --root /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane --tool-file /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/probe_source_recheck.py --key-revision fd1fb723624b742a00a6e8e908f3b42901d627f8` → exit 1
`timeout 20 cp -p /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane/scripts/source_recheck.py /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/probe_source_recheck.py` → exit 0
`timeout 600 python3 -B .ufo/waves/round-36/sealed_count.py --root /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/lane --tool-file /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/probe_source_recheck.py --key-revision fd1fb723624b742a00a6e8e908f3b42901d627f8` → exit 0
`timeout 20 sha256sum /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/robots_audit.py /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/source_recheck_junk.py /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-junk.json /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-junk.exit /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-pristine.json /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-mutated.json /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/r36-restored.json /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/probe_source_recheck.py /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/mutation-evidence.json /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk/commands.json` → exit 0
`timeout 20 ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC1Junk` → exit 0; output below. Commands.json preserves raw process stdout/stderr; detector stdout files were written without alteration.
## Sandbox root listing
```text
total 80
drwxr-xr-x 4 vgpnk vgpnk  4096 Oct 23 00:06 .
drwxr-xr-x 7 vgpnk vgpnk   112 Oct 23 00:05 ..
-rw-r--r-- 1 vgpnk vgpnk 13244 Oct 23 00:06 commands.json
drwxr-xr-x 8 vgpnk vgpnk  4096 Oct 23 00:03 lane
-rw-r--r-- 1 vgpnk vgpnk   520 Oct 23 00:05 mutation-evidence.json
-rwxr-xr-x 1 vgpnk vgpnk 20831 Oct 23 00:03 probe_source_recheck.py
-rw-r--r-- 1 vgpnk vgpnk     2 Oct 23 00:06 r36-junk.exit
-rw-r--r-- 1 vgpnk vgpnk  1648 Oct 23 00:04 r36-junk.json
-rw-r--r-- 1 vgpnk vgpnk  1649 Oct 23 00:05 r36-mutated.json
-rw-r--r-- 1 vgpnk vgpnk  1621 Oct 23 00:04 r36-pristine.json
-rw-r--r-- 1 vgpnk vgpnk  1621 Oct 23 00:05 r36-restored.json
-rwxr-xr-x 1 vgpnk vgpnk    69 Oct 23 00:04 robots_audit.py
-rwxr-xr-x 1 vgpnk vgpnk    69 Oct 23 00:04 source_recheck_junk.py
drwxr-xr-x 2 vgpnk vgpnk     6 Oct 23 00:05 tmp
```
