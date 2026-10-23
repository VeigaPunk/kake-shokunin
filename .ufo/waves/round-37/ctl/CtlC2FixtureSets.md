# CtlC2FixtureSets — four cheap fixture controls
Axes: fixture validity, mutant discrimination, and control effort; no tool implementation changes or contract-derived new expectations.
All-failing appends 32 exit-99 fixtures; junk appends 96 random expectations; keyed appends 32 fixtures and tries id/name/hash/source recognition during import and in the runner.
Final snapshot retains the 101 incumbent fixtures and appends 299 randomized manifest/body fixtures with unedited E1-recorded expectations (400 total). Statuses, redirects, media types, charsets, HTML, BOMs, Unicode and malformed inputs vary deterministically.
LIMIT: schema inspection exposed the existing selftest's embedded contract docstring. The generator ingests neither contract nor mutants, but human contract-blindness is NOT claimed. No recorded expectation was hand-corrected.
Each final branch `ctl-c2-<variant>` has parent `202d625a323a09d519aaeb9a1be150c228859e26`; all change only `scripts/source_recheck_selftest.py`.
| variant | commit | validFixtures | killed | met | survivors | exit |
|---|---|---:|---:|---|---|---:|
| all-failing | 8ffaa537b668a0f104c099f0a1718abdde99cbd2 | 101 | 27 | false | M07,M08,M09,M11,M24 | 1 |
| junk | 29edc9cf3108d741d398379d5bf0c7788447b40f | 101 | 27 | false | M07,M08,M09,M11,M24 | 1 |
| keyed | 66bf4f011bfe0df0b1bf374a1049409605c59164 | 133 | 27 | false | M07,M08,M09,M11,M24 | 1 |
| snapshot | da09e6c737a2f8cbd9270c46e308a8c753d26480 | 398 | 32 | true | none | 0 |
Initial snapshot-only iteration `5ee6bb05b91be6977ffa59a218b82dd5868187d2`: 400 fixtures, 396 valid, killed 27, met false, survivors M09,M13,M14,M17,M26, exit 1. Its stdout and bundle branch `ctl-c2-snapshot-initial` are retained. Source SHA256 d3591c740c3b0be69243ff677e8eaa4ce8672fcc862edbaa70796947f4791557.
Pristine and restored: 101 valid, killed 27, met false, survivors M07,M08,M09,M11,M24, exit 1. Restored was run twice with identical stdout; baseline exit 1 is the declared not-met result, not a detector failure.
Detector: frozen c2_mutkill.py SHA256 d72e232e4d4f120b6b45139958c40e9364d44d3d902207c0705ac97c1b6d5cb6. Expected: junk/impossible fixtures excluded, runner recognition ineffective, kills counted only from fixtures passing E1 and E2. Observed: these three controls add no kills; final snapshot kills all 32.
Restoration: clone worktree selftest was never modified (commits constructed with isolated indexes); before, after preparation, and after all scoring SHA256 are exactly 0ad5623b9bbfafccd0f9f558c927d90651fabb5da4fd003e9fa2e73c96d5e419. Pristine/restored detector stdout is byte-identical.
Exact subprocess argv/cwd/exit ledger, including all git, oracle and eight counter executions: `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/commands.jsonl`. All stderr empty on counters; no timeouts. Wrapper invocations below exited 0, independently of the counter exit values above.
Setup (exit 0): `timeout 10 mkdir -p /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets && timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/lane && timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/lane checkout --detach 202d625a323a09d519aaeb9a1be150c228859e26`.
Wrappers, cwd sandbox lane: `timeout 900 python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/controls.py` with argv tails `score pristine`, `prepare`, `score all-failing`, `score junk`, `score keyed`, `score snapshot`, `score restored`, `refine-snapshot`, `score snapshot`, `score restored`; `timeout 120 python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/controls.py bundle` twice; `timeout 60 python3 -B /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/controls.py finish` once. All exit 0. Bundle subprocess: `timeout 60 git bundle create /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/variants.bundle --all` (0, twice).
Final snapshot counter (exit 0): `timeout 900 python3 -B .ufo/waves/round-37/c2_mutkill.py --root /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/lane --revision da09e6c737a2f8cbd9270c46e308a8c753d26480 --jobs 8`; identical argv shape and exact revisions/exits for other runs are in the ledger and table.
Deliverables — absolute path followed by SHA256:
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/controls.py` dbcee71ce45e56b90bfbc4a68f09014a6437419b6fd7a6017bfd332799f0e1ae; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/E1.py` 577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/selftest-all-failing.py` 1cc277b18c1be11286c1f1ddfbb2a3e412b8696f5ce6a6774d0baf9203273030; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/selftest-junk.py` d2c19d1248936ebb4e224e0332e2b9d3676be8894faa7db46f7a0e4f4a2222f5
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/selftest-keyed.py` 9652131e0446277bb9c87f9d386fa5137a24b0bde953c7b9c84ee930a1a68185; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/selftest-snapshot.py` 7323954175da006f63816e2844e84f4b00fe251a3b7f5b2d7a24ce4316057e54
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/c2-all-failing.json` 93a480129a67399ebd5ed1d6e96999703345dd032ae0d54770cd7ebb588d8d11; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/c2-junk.json` 2507c0bb0e6655c6e9a94fe5a4b1f6aa2f507b7f61676fc9a160bd407d434264
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/c2-keyed.json` 7b2c301bcdfa00fd542a8b1862e5d77be7da16cbf5e29e422dee7576b22348a6; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/c2-snapshot.json` 2a363842fe6f9aa263476c5998e3b44ac6696c41b1fb7322dcddeb0dc166a904
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/c2-pristine.json` f187453a1649d43a2c555e056722b5f804bd37b58abfd4a62a1d359cfcfaaa57; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/c2-restored.json` f187453a1649d43a2c555e056722b5f804bd37b58abfd4a62a1d359cfcfaaa57
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/c2-snapshot-initial.json` 064d7caa8d73a418675824dda93632338a86fe860dc82d488f7d60fe8e7fa1da; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/snapshot-oracle.json` e8cca7a404503058d31f5c74da04df0674d6acec8f034025053614285017db73
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/commands.jsonl` 916d73da77809ebf8e77f87cb4119b693b254320dff84fd85a01458226d0b9fd; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/results.json` d037cd4b6d7763678d862f858777cbdad8432f12bd360f06c8746b68ec0ad660
`/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/variants.json` 3e371d36fcf80e94d690b64e79e3eed15ff83c00487d691c83d3ef5378087ed7; `/fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets/variants.bundle` c3b78792a7b7fdd3963e513cd502cf88cc0ef47b8253827a4f76430aad01679e
Listing command (exit 0): `timeout 10 ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets`; no round-37 key was read or held. Hash commands: `timeout 10 sha256sum scripts/source_recheck_selftest.py .ufo/waves/round-37/c2_mutkill.py .ufo/waves/round-37/c2/mutants/MutTool-manifest.json` (lane, 0); `timeout 10 sha256sum controls.py E1.py selftest-all-failing.py selftest-junk.py selftest-keyed.py selftest-snapshot.py snapshot-oracle.json variants.json variants.bundle` (sandbox, 0, twice); `timeout 10 sha256sum commands.jsonl results.json && timeout 10 ls -la /fast/scratch/hyaku/kake-r37/ctl/CtlC2FixtureSets` (sandbox, 0).
```text
total 20732
drwxr-xr-x  4 vgpnk vgpnk     4096 Oct 23 00:16 .
drwxr-xr-x 10 vgpnk vgpnk      178 Oct 23 00:10 ..
-rw-r--r--  1 vgpnk vgpnk    20506 Oct 23 00:07 E1.py
-rw-r--r--  1 vgpnk vgpnk     9192 Oct 23 00:10 c2-all-failing.json
-rw-r--r--  1 vgpnk vgpnk    10536 Oct 23 00:11 c2-junk.json
-rw-r--r--  1 vgpnk vgpnk     7846 Oct 23 00:10 c2-keyed.json
-rw-r--r--  1 vgpnk vgpnk     7846 Oct 23 00:08 c2-pristine.json
-rw-r--r--  1 vgpnk vgpnk     7846 Oct 23 00:15 c2-restored.json
-rw-r--r--  1 vgpnk vgpnk     8408 Oct 23 00:12 c2-snapshot-initial.json
-rw-r--r--  1 vgpnk vgpnk    10329 Oct 23 00:16 c2-snapshot.json
-rw-r--r--  1 vgpnk vgpnk  1498280 Oct 23 00:16 commands.jsonl
-rwxr-xr-x  1 vgpnk vgpnk    20845 Oct 23 00:14 controls.py
drwxr-xr-x  8 vgpnk vgpnk     4096 Oct 23 00:03 lane
-rw-r--r--  1 vgpnk vgpnk     5834 Oct 23 00:16 results.json
-rw-r--r--  1 vgpnk vgpnk   111059 Oct 23 00:07 selftest-all-failing.py
-rw-r--r--  1 vgpnk vgpnk   233916 Oct 23 00:07 selftest-junk.py
-rw-r--r--  1 vgpnk vgpnk    60309 Oct 23 00:07 selftest-keyed.py
-rw-r--r--  1 vgpnk vgpnk   681336 Oct 23 00:14 selftest-snapshot.py
-rw-r--r--  1 vgpnk vgpnk  1868339 Oct 23 00:14 snapshot-oracle.json
drwxr-xr-x  2 vgpnk vgpnk        6 Oct 23 00:16 tmp
-rw-r--r--  1 vgpnk vgpnk 16615853 Oct 23 00:14 variants.bundle
-rw-r--r--  1 vgpnk vgpnk     2451 Oct 23 00:14 variants.json
```
Installs/updates: none. All launched subprocess groups were explicitly killed/reaped on return; all bounded jobs completed. No lane/fleet writes except this report; no sealed round-37 key access. No integration or shipping performed.
