# AblateBuilds — C2 full-rule ablation probe
Axes: operability attacked; freshness unchanged (offline only).
Target: pinned SCORECARD claim at /fast/scratch/hyaku/kake-r38w2/AblateBuilds/SCORECARD-tip.md:2237-2251; wave-1 CriticControlReceipts remedy (finding 5).
Expected detector: removing any complete rule (h), (i) or (k) from a genuine three-rule build makes counter v3 score below 20/20.
Observed: 36 detector executions; pristine 12×20/20 exit 0; mutants 12×16/20 exit 1; restored 12×20/20 exit 0. All 12 killed; 0 survived; 0 inconclusive.

## Verdict per attacked statement
| Alleged three-rule build | Pristine | no-(h) | no-(i) | no-(k) | Restored | Verdict / evidence |
|---|---|---|---|---|---|---|
| CtlLabelShortcut-delegate_ceiling | 20 | 16 | 16 | 16 | 20 | holds, bounded; /fast/scratch/hyaku/kake-r38w2/AblateBuilds/probe-results.jsonl:1-3 |
| CtlBaseWrapper-care | 20 | 16 | 16 | 16 | 20 | holds, bounded; /fast/scratch/hyaku/kake-r38w2/AblateBuilds/probe-results.jsonl:4-6 |
| CriticPredicate-rulepatch | 20 | 16 | 16 | 16 | 20 | holds, bounded; /fast/scratch/hyaku/kake-r38w2/AblateBuilds/probe-results.jsonl:7-9 |
| CriticPredicate-rulepatch_pct | 20 | 16 | 16 | 16 | 20 | holds, bounded; /fast/scratch/hyaku/kake-r38w2/AblateBuilds/probe-results.jsonl:10-12 |
Every no-(h) fails exactly j1–j4; every no-(i) exactly u1–u4; every no-(k) exactly r1–r4. All other 16 cases hold. Each receipt has met=false only for its mutant.
No rule-removed tool reaches 20, so this probe finds no class-(6) control meeting C2. This is whole-rule necessity evidence, not proof of every contract edge or a round admission.

## Mutation and restoration
For delegate/care, delete only the dispatch assignment installing the selected JSON, URL or normalized-path wrapper (original delegate lines 175/176/177; care 55/70/71).
For both rulepatch variants, (h) use json.loads(text) without either hook; (i) delete only the two-line url_charset_ok rejection; (k) compare raw path rather than normalize(path), retaining normal rule matching.
Exact 12 diffs: /fast/scratch/hyaku/kake-r38w2/AblateBuilds/ablations.patch:1; original and mutant SHA256 plus paths: /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutations.json:1.
All 12 working tool.py files restored byte-for-byte in finally, then scored at the identical --tool-file paths. Before=restored SHA256 for every probe: /fast/scratch/hyaku/kake-r38w2/AblateBuilds/restoration.json:1 and probe-results.jsonl:1-12.

## Commands and actual exits
All commands execute in the isolated clone; GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; TMPDIR=/fast/scratch/hyaku/kake-r38w2/AblateBuilds/tmp. Two concurrent detector commands, no network.
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 120s git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r38w2/AblateBuilds/clone` → exit 0.
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30s git -C /fast/scratch/hyaku/kake-r38w2/AblateBuilds/clone checkout -q adab4c7e9ec2178657395f49346f18800ff4796f` → exit 0.
`timeout 30s git -C /fast/scratch/hyaku/kake-r38w2/AblateBuilds/clone show adab4c7e9ec2178657395f49346f18800ff4796f:SCORECARD.md` → exit 0; captured SCORECARD-tip.md SHA256 59dc78772f32f07fea70e5a04a22c11ff680e7d5c43292477aaf9eeafcdd1f1c.
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r38w2/AblateBuilds/tmp timeout --kill-after=2s 850s prlimit --as=4000000000 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r38w2/AblateBuilds/run-probes.py pristine` → orchestrator exit 0; inner exits 12×0.
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r38w2/AblateBuilds/tmp timeout --kill-after=2s 850s prlimit --as=4000000000 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r38w2/AblateBuilds/run-probes.py mutated` → orchestrator exit 0; inner exits 12×1.
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r38w2/AblateBuilds/tmp timeout --kill-after=2s 850s prlimit --as=4000000000 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r38w2/AblateBuilds/run-probes.py restored` → orchestrator exit 0; inner exits 12×0.
Each exact inner command, cwd, environment, exit and stdout/stderr hash is retained in /fast/scratch/hyaku/kake-r38w2/AblateBuilds/receipts/{pristine,mutated,restored}/execution.json:1 and probe-results.jsonl:1-12.
Inner command: `timeout --signal=TERM --kill-after=2s 180s prlimit --as=4000000000 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r38w2/AblateBuilds/clone/.ufo/waves/round-38/sealed_count_v3.py --root /fast/scratch/hyaku/kake-r38w2/AblateBuilds/clone --tool-file /fast/scratch/hyaku/kake-r38w2/AblateBuilds/probes/NAME/no-RULE/tool.py --key-revision 99357694` (NAME/RULE expanded in those logs).
All 36 stderr files empty; each detector took 0.397–0.974 s. Driver kills its own residual process groups after every command. Initial async bash launch was not started (host background-job cap); the listed executions ran through eval subprocess, not another detector/runtime.
Counter SHA256 28b120a5a38061825094c17f0e978d7e6a5ec3fb131094e2cdfd59360f38f9e4; key SHA256 749ef6a65de67f09abffad33fa6d7efcb1e7f1515b1d2fa51a93ff9977b63aa6.

## Before/restored SHA256 (identical)
- CtlLabelShortcut-delegate_ceiling: `5c80fb01a5714450dfc3678368136c715a6e3796f1bb25d62fd3e5ee5364f0f2`.
- CtlBaseWrapper-care: `3215ae1a2c31538167109c1436d59597742728f381a60f621f6759cc37a9da5a`.
- CriticPredicate-rulepatch: `8a5712b455c3105a39f8191ec5bac7494d8f9564f5a5dde0bbe68ca242b96bc5`.
- CriticPredicate-rulepatch_pct: `b2c86c8c6e0d1d0d952621b2709248f6fa90b3254f701d67cc00137b1079b783`.

## Mutant artifacts and SHA256
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CtlLabelShortcut-delegate_ceiling-no-h.py — `945dcdb1c4da2170611c26fffea50f9f823e53fc2a5d3cdd0fb6bb2480b824cd`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CtlLabelShortcut-delegate_ceiling-no-i.py — `75d88396ebc84140a29bbd8b2366b938033b4e1dbe812f1971a73642104191fd`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CtlLabelShortcut-delegate_ceiling-no-k.py — `336061da5cc6b89a1c664973e3c5e0564c4a2144768ef0489f02e6a3d17e8ff8`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CtlBaseWrapper-care-no-h.py — `c312ddb3c41a28aaef9d9339501b96c65c1b87c8aed011f64ca240a9bb6c4e75`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CtlBaseWrapper-care-no-i.py — `235092ac8dc005d420c2f8eaa91524547e34c1e143b9038efda3b16bab7608d7`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CtlBaseWrapper-care-no-k.py — `8c6b8bdfddf6d61bcb505a5b42e1da2cca994c322f4f854415996627d64671f7`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CriticPredicate-rulepatch-no-h.py — `8a31cf585c0efca569abd6ca8a377a8f702112d954903f89030b636bee4d297e`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CriticPredicate-rulepatch-no-i.py — `b7e5d954e140d073fd2649153f804ca487fb9ef56fc14c5cb5121514a2daf6ce`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CriticPredicate-rulepatch-no-k.py — `e6a7f71df170a858ddbf340005ecb5f5bed7b03790f50e7e4c87dfe5764c27a0`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CriticPredicate-rulepatch_pct-no-h.py — `c5ff35db519a44f352b9f409815476e41a6b98815070e2740a2600254cbbdd57`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CriticPredicate-rulepatch_pct-no-i.py — `e2b69942dfb4c6d81a00b3b6b981e20cb913296923ff4f14571854f2db6070a6`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/mutants/CriticPredicate-rulepatch_pct-no-k.py — `6300c13d22be6e86aebaf52e41a5c31a7a2a441800839b89602f1d343d6817d3`.

## Evidence seals
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/run-probes.py — `4803950e67ad3a7ac66f7345b2261cd8a6f225ae2e593d2cae1fc406e59271fa`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/ablations.patch — `807c09b7cfc08fd40e3689f5ee9fee7226d364e6a2ab7ce4d1a14b2a998c4096`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/probe-results.jsonl — `3d942e09a28cfe6c4a3d7129684d12df104619530c081c7b94d90cf79a0fb64c`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/restoration.json — `77ed61f72f0380f2392cbfd5126205569988ba869e34a4b5395adefeb3ae3d4f`.
- /fast/scratch/hyaku/kake-r38w2/AblateBuilds/SHA256SUMS — `f28cbbfab92b4e011a8b8cd88060efba61d00da40866fd63128197ee908b40ba` (143 absolute-path entries, including all 36 outputs/exits, 12 retained mutants and 12 restored working files).
No installs/updates; existing Python 3.14.8 and bubblewrap 0.13.1. No lane source/index/jj mutations; only this report is written outside the assigned sandbox.
