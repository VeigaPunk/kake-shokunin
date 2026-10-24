# C1 sealed-counter guard mutation probe
Axes: operability (reject incorrect measurements); freshness (repeatable frozen-tip/key evidence).
Scope: 14 single-point mutants, isolated sandbox only; no round admission judgment or implementation changes.
`S=/fast/scratch/hyaku/kake-r37w2/MutSealedCounter`; `C=.ufo/waves/round-37/sealed_count.py`.
Frozen tip: `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`; key revision: `424aa248`.
Result: **13 killed; 1 equivalent survivor; 0 inconclusive**, across 42 pristine/mutant/restored counter invocations.
Original and every restored counter SHA256: `2ebb39b585e2a35f16ff71397f2fb22477a7a3c0e95da4415a26b0430b0cf0e3`.
Pinned key SHA256: `93ad9ee64db63b661b408e678f2c6f3d665b7f5c88ef1f977433dbceee8c0a90`.

## Guard table with proving inputs
Outputs below are `passed/exit/met`, in pristine → mutant → restored order; `—/2/—` means expected refusal, not a baseline detector failure.
`R` is the committed reference tool (`S/clone/.ufo/waves/round-37/sealed/reference/ref.py`). Other witnesses are reference-backed constructed tools in `S/tools/<name>.py`; each changes only the described output/eligibility behavior. All use the revealed, pinned 28-case key except M09.
| ID; original site | Single-point mutation | Proving input/tool | Actual output: pristine → mutant → restored | Statement / mutant verdict |
|---|---|---|---|---|
| M01; C:217 | Continue runs after a failed run; last result wins | `fail-invalid`: wrong verdict only for input-invalid runs; g1–g4 end with a correct valid run | 24/1/F → 28/0/T → 24/1/F | all-runs requirement holds; killed |
| M02; C:100 | Project findings by reason only | `wrong-check`: correct reasons, every check replaced by `deliberately-wrong` | 0/1/F → 28/0/T → 0/1/F | check-identity comparison holds; killed |
| M03; C:128 | Preserve original IDs instead of fresh IDs | `original-id-only`: correct only when check IDs are original k1–k8/dupid; otherwise wrong verdict | 0/1/F → 28/0/T → 0/1/F | ID randomization has score effect; holds; killed |
| M04; C:191 | Disable key-visible revision refusal | Measure `scripts/robots_audit.py` at frozen tip, which contains the key | —/2/— → 28/0/T → —/2/— | revision refusal holds; killed |
| M05; C:143 | Ignore exit status | `wrong-exit`: correct JSON, exit 17 on every invocation | 0/1/F → 28/0/T → 0/1/F | exit comparison holds; killed |
| M06; C:149 | Ignore report verdict | `wrong-verdict`: correct findings and exit, false verdict | 0/1/F → 28/0/T → 0/1/F | verdict comparison holds; killed |
| M07; C:101 | Compare sets, not multisets | `duplicate-finding`: append one duplicate of the first finding | 0/1/F → 28/0/T → 0/1/F | multiplicity comparison holds; killed |
| M08; C:109 | Retain original robots basenames | `original-filename-only`: correct only for original r0.txt–r7.txt/outside.txt basenames | 0/1/F → 28/0/T → 0/1/F | filename randomization has score effect; holds; killed |
| M09; C:84 | Disable key hash refusal | R with `S/key-newline.json`: original key plus one newline, identical JSON value | —/2/— → 28/0/T → —/2/— | byte pin holds; killed |
| M10; C:236 | Remove `len(rows) == CASES` | R, unchanged pinned key | 28/0/T → 28/0/T → 28/0/T | holds but redundant on pinned key; survived/equivalent |
| M11; C:52 | Lower TARGET from 25 to 24 | `fail-invalid`, deliberately passing exactly 24 cases | 24/1/F → 24/0/T → 24/1/F | threshold holds; killed (decision changes, raw score does not) |
| M12; C:100 | Ignore finding reason | `wrong-reason`: correct check identities, every reason false | 0/1/F → 28/0/T → 0/1/F | reason comparison holds; killed |
| M13; C:154 | Remove inverse fresh-ID mapping | R emits correct fresh check IDs | 28/0/T → 0/1/F → 28/0/T | ID normalization holds; killed |
| M14; C:128 | Allocate a new ID per occurrence instead of setdefault | R; f1–f4 contain repeated `dupid` | 28/0/T → 24/1/F → 28/0/T | duplicate-ID preservation holds; killed |
M10 equivalence argument: the hash-pinned key contains exactly 28 cases; every completed loop appends one row per case, irrespective of tool output. Thus `len(rows) == 28` is always true on a completed measurement. This is an equivalent survivor, not a detector failure or authorization to alter the contract. Counter-hash metadata necessarily differs.
M04's exact expected error is `key visible at the measured revision`; M09 reports key hash `ca0a1306cb23382212b8ffcf5373f50cc371907393f761be945e6c624ea0aa51 != pinned ...`. Both pristine rejection detectors succeeded.

## Commands, outputs, and restoration evidence
Setup (all exit 0): unset `GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE`; `timeout 30s mkdir -p "$S/tmp"`; export `TMPDIR="$S/tmp"`; `timeout 120s git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin "$S/clone"`; `timeout 30s git -C "$S/clone" checkout -q 79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`.
Executed from S with the same variables unset/exported: `timeout --kill-after=3s 900s python3 -B /fast/scratch/hyaku/kake-r37w2/MutSealedCounter/probe.py prepare` (exit 0).
Applied the 14 isolated edits with the edit tool, exact old/new text in `S/mutations.json:1-267`; each counter changed at only the table's site (M14 replaces one assignment with two).
Then: `timeout --kill-after=3s 900s python3 -B /fast/scratch/hyaku/kake-r37w2/MutSealedCounter/probe.py challenge` (exit 0; summary `errors: []`).
Every phase invokes the identical witness command: `timeout --kill-after=3s 90s /usr/bin/python3 -B S/counters/<ID>.py --root S/clone <source-arguments> <key-arguments>`. Exact expanded argv/cwd, exits, SHA256s, stdout and stderr paths are retained at `S/evidence/<ID>/<pristine|mutant|restored>.receipt.json:1`; raw outputs are sibling `.stdout.json`/`.stderr.txt` files.
Full mutation definitions, tool paths/hashes and argument exceptions: `S/mutations.json:1-267`. Detector and process-group cleanup: `S/probe.py:75-117`; finally-restoration and restored reruns: `S/probe.py:143-188`.
All 14 source copies were restored byte-for-byte in `finally`; all 14 restored output hashes equal their pristine output hashes. `S/summary.json` records each exact restoration and all three receipts. `S/counters/<ID>.py` is restored; `S/mutants/<ID>.py` preserves the challenged bytes for reproduction.
Mutant SHA256s (before/after restoration hash is the common original hash above):
- M01 `de78769df61e2a52776a2497b056fc45f4903037103408c8b46e14f7d3969542`
- M02 `472b06d9b1d64d494a8a6231d100f86b342ad3ffd1d43d27f311d023ad893b74`
- M03 `6c01d771e4fca077d02688dcf1ede928102667b2fc72b39f83b7afe61e91eb47`
- M04 `3e62be6a05515da7852d5831a454aaca0604cc455fee45c6da3c414909aff54c`
- M05 `3d19a8bd19f939540a9181fc188a80c7b42433a951f2f08ed16489408b7eacb6`
- M06 `91e3fcceaf385ec17b141bca003c24b8a5915b73d5d988c8118c01166c2ff8fe`
- M07 `543ac9b5aa6d4c73fe245e40b847b2d82cf11f98a967c408526aebec7339ed06`
- M08 `6d5771edc5c2a843acee50dd2160f6e888b049e1de1363388d34201f216de376`
- M09 `d3ba60ab3f3ee945fc57215529d69cf947f7ede6b29cbcd53b575433168c2cc0`
- M10 `0648f8f0f3f4cfad88f6449c2f7413d210b3149051479355631556430f0b5efc`
- M11 `e88acde0cf69e06b1752d5b859dc855980900c239816ff091994b5e17b9b6582`
- M12 `316a17dbdc614d60254d475eef538b74a4de94295c8075a7f596f8abc33f97b8`
- M13 `f3771f68296607720c7cb50fe19a47709c9679e56760142359adbc09f84d53e3`
- M14 `23b2b86d11af33c7a0da89ab66b8acee9527b8e47f91195046f1242f59b845c0`
No network, subagents, tool installations, or background services; one counter active at a time. Existing tools: Python 3.14.8, bubblewrap 0.13.1, Git 2.56.0. Fleet writes were limited to this report.
