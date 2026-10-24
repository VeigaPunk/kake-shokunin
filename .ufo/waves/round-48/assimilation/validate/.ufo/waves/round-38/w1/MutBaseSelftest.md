# MutBaseSelftest — 25 single-point base-tool mutants
Axes: operability (fixture sensitivity); freshness (frozen source/detector provenance). Advisory mutation findings only, not a round verdict.
Scope: base tool af43a50fa399881eead9381d835b78a015e277a6, contracts (c)/(d); detector cloned at 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1. No selftest edits.
Sandbox: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest`. All 25 independent mutant artifacts are linked below; exact before/replacement text is in `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/inventory.json:1`.
Expected detector: the frozen 137-fixture black-box selftest should exit 1 on a contract-breaking mutant; exit 0 with 137/137 means survived, not correctness.
Observed: every one of 25 pristine runs and 25 exact-byte restored runs exited 0, 137/137. Mutated: 15 killed, 10 survived, 0 inconclusive.
Survivors: M04, M06, M11, M15, M16, M21, M22, M23, M24, M25. All ten also changed contract-predicted outputs on independent local witnesses.

## Commands and observed exits
Setup (exit 0, no output): `timeout 90s prlimit --as=4000000000 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE sh -c 'mkdir -p /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/tmp /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/evidence && export TMPDIR=/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/tmp && git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/clone && git -C /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/clone checkout -q 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1'`.
Frozen-byte comparison (exit 0, empty diff): `timeout 20s prlimit --as=4000000000 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/tmp git -C /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/clone diff af43a50fa399881eead9381d835b78a015e277a6 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1 -- scripts/robots_audit.py scripts/robots_audit_selftest.py`.
All detector commands ran with cwd `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/clone`; TMPDIR stayed under the sandbox. Each batch used two workers (at most eight command-tree processes), 4 GB address-space limits, and per-detector 180-second deadlines.
`timeout --kill-after=5s 850s prlimit --as=4000000000 env TMPDIR=/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/run_batch.py pristine` — batch exit 0; individual detector exits recorded below and in receipts.
`timeout --kill-after=5s 850s prlimit --as=4000000000 env TMPDIR=/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/run_batch.py mutated` — batch exit 0; individual detector exits recorded below and in receipts.
`timeout --kill-after=5s 850s prlimit --as=4000000000 env TMPDIR=/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/run_batch.py restored` — batch exit 0; individual detector exits recorded below and in receipts.
Inner command, identical across the three phases: `timeout --kill-after=5s 180s prlimit --as=4000000000 python3 -B scripts/robots_audit_selftest.py --tool /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/probes/Mxx.py`; actual M01–M25 argv/cwd/exits/stdout/stderr are in each receipt. Retained mutant artifacts have the exact tested hashes.
`timeout --kill-after=5s 180s prlimit --as=4000000000 env TMPDIR=/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B /fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/run_witnesses.py` — exit 0; all ten pristine/mutant/restored witnesses matched their expected complete JSON reports.

## Full mutant table
| Mutant artifact | Base line / single defect | Selftest passed; exit | Verdict (first failing fixture) | Mutant SHA-256 |
|---|---|---|---|---|
| [M01](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M01-ua-shorter-substring.py) | 257: ua-shorter-substring | 136/137; 1 | killed (c12) | `f08aefeefaa5a4636f97e3a7f15c2c47975891406c45ddd273047968b30d54e6` |
| [M02](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M02-ua-longer-substring.py) | 257: ua-longer-substring | 136/137; 1 | killed (c09) | `c66ef3af504c6b7bb5b48c532611737641da32526257772892de824fd8272525` |
| [M03](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M03-unicode-group-folding.py) | 256: unicode-group-folding | 136/137; 1 | killed (c10) | `d11f49d8794986cb3aaabd94a26dd8a4734dd99b5da591b551d2414feac0b43a` |
| [M04](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M04-unfolded-check-token.py) | 247: unfolded-check-token | 137/137; 0 | survived (none) | `6c8f2140da637328989628c96d166766d305000430b5e0bc11328c841d07be91` |
| [M05](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M05-last-exact-group-only.py) | 259: last-exact-group-only | 136/137; 1 | killed (c08) | `dd3376a9f5ad90bc7683a01ba0073dcfe1a203908786eb9d91aa2bc75939e8c3` |
| [M06](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M06-first-exact-group-only.py) | 259: first-exact-group-only | 137/137; 0 | survived (none) | `c165011cd94eac19914e66034d37e6c7949f6aee2720a9e4d425b5b58abf26d7` |
| [M07](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M07-star-always-combined.py) | 262: star-always-combined | 134/137; 1 | killed (c05) | `975e595535a6cff999bddaf67d15a551a73e9c99fb2a8cf59924bb2c51a5a21b` |
| [M08](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M08-first-star-group-only.py) | 263: first-star-group-only | 136/137; 1 | killed (c14) | `fd43e94c5a988bf8bc99794648024b82a30bbf709e81aacb6b675213c09cd338` |
| [M09](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M09-empty-group-falls-back.py) | 258: empty-group-falls-back | 136/137; 1 | killed (c15) | `732558d7375cfced06bb31e8163f1c4f0c9e908e19004e9e1438b86576a05299` |
| [M10](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M10-split-consecutive-agents.py) | 188: split-consecutive-agents | 134/137; 1 | killed (b13) | `389a452c08ae7e1cb389265596c53bfe885c20d9f6bfdd97807c803e1496c044` |
| [M11](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M11-blank-comment-ends-continuation.py) | 184: blank-comment-ends-continuation | 137/137; 0 | survived (none) | `95d3f8437a218c4c785f8fc9d954a8cb64307cc8745e62cc85c951c660cf7b94` |
| [M12](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M12-ignored-record-ends-continuation.py) | 205: ignored-record-ends-continuation | 135/137; 1 | killed (b13) | `9083577f2e3c478ffe53a49c7584085f54978ac6c39b7ffb6df4bf8dfddf8c19` |
| [M13](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M13-empty-rule-keeps-continuation.py) | 204: empty-rule-keeps-continuation | 136/137; 1 | killed (c15) | `b22599a0e4b4dab41ec537a3ba8e5db4f57970d82fc35760acc2347a936fc262` |
| [M14](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M14-dollar-excluded-from-length.py) | 225: dollar-excluded-from-length | 136/137; 1 | killed (d13) | `1c4bf3f2fa7f802712ea54b6934ce5ebb7a744398dfd4c24b9119f389e561bf6` |
| [M15](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M15-star-excluded-from-length.py) | 225: star-excluded-from-length | 137/137; 0 | survived (none) | `6a88c49f2c24980d11f19ba52af7abeb1d3a8bb5c2c24fb3cbd62c4426d9cf77` |
| [M16](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M16-escape-counted-as-one.py) | 225: escape-counted-as-one | 137/137; 0 | survived (none) | `fbe068647a5de4b229fb7739439404643c3cafe48de929ae528a476c1c1494c4` |
| [M17](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M17-last-matching-tie-wins.py) | 316: last-matching-tie-wins | 135/137; 1 | killed (d10) | `9b228ffe4cf0673de4887a99fd6dd5f0eb060f86a71028b6788014baedad7e15` |
| [M18](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M18-first-matching-tie-wins.py) | 312: first-matching-tie-wins | 135/137; 1 | killed (b01) | `6023aaa70eb4b69debf19110523bce122aeeae5dcf92e296c89d4c40bf0c918f` |
| [M19](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M19-nonfinal-dollar-anchors.py) | 226: nonfinal-dollar-anchors | 136/137; 1 | killed (d07) | `4d5dcac40c130b1245ca6d40140cd7668c2a364ab1acaca0491e4ff6221cb68f` |
| [M20](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M20-star-must-consume-one.py) | 290: star-must-consume-one | 135/137; 1 | killed (d03) | `d1f301a202b4fb8c07e38982984be74a6a9e22f6a201771fbb70ca6be41fea30` |
| [M21](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M21-anchored-glob-overlap.py) | 298: anchored-glob-overlap | 137/137; 0 | survived (none) | `72596a718ec0ef76feaded19bc61eca2f436048b3d80979afc9e79e2e60f2e8b` |
| [M22](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M22-anchored-glob-no-suffix-check.py) | 298: anchored-glob-no-suffix-check | 137/137; 0 | survived (none) | `a5d9639cd089e922fc300813f65dbe5fb0b8d8db6f051ca8ae94c9f53e75ea9f` |
| [M23](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M23-wildcard-prefix-is-substring.py) | 288: wildcard-prefix-is-substring | 137/137; 0 | survived (none) | `4f0fe66d0bbfb269e42a0c69a1fe055ca5cb6548141c4ebdd4d320b068a2f18e` |
| [M24](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M24-unanchored-segment-order.py) | 300: unanchored-segment-order | 137/137; 0 | survived (none) | `e926a16210c463cc3ccc72e8fd74fc2094bd0ba5b80dba974319cb11bc649bde` |
| [M25](/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/mutants/M25-anchored-segment-order.py) | 294: anchored-segment-order | 137/137; 0 | survived (none) | `dbe4aa93c1451e51b93e22d2ec4a689336e992a02773c19194bba75078f72852` |

## Surviving mutants: sentence broken and non-equivalence witnesses
All witness checks expect allow and evaluate exactly one check. Exit 1 = failed-policy with one blocked finding for the mutant id; exit 0 = clean with no findings. P/M/R are actual pristine/mutant/restored exits; all three full outputs and source hashes are retained per witness.
| Survivor | Broken contract sentence / clause (SCORECARD.md:1826–1838) | Local witness | P/M/R |
|---|---|---|---|
| M04 | (c) UserAgent equals a group name “compared ASCII case-insensitively.” | UA `BoT`, group `bot`, `Disallow: /x`, path `/x` | 1/0/1 |
| M06 | (c) “The rules of every matching group are combined.” | First bot group `Allow: /a`; later bot group `Disallow: /x`; path `/x` | 1/0/1 |
| M11 | (c) “blank, comment and ignored lines between them do not count” toward ending consecutive user-agent records. | `bot`, blank, comment, `other`, `Disallow: /x`; UA bot, path `/x` | 1/0/1 |
| M15 | (d) Longest normalized value decides, “* and $ included”. | `Allow: /ab`; `Disallow: /a*b`; path `/ab` | 1/0/1 |
| M16 | (d) Longest normalized value is “counted in octets”. | `Allow: /*x`; `Disallow: /%2Fx`; path `/%2Fx`; normalized escape occupies three ASCII octets | 1/0/1 |
| M21 | (d) “* in a rule matches any sequence of characters (also none)”; literal prefix and suffix cannot overlap. | `Disallow: /ab*bc$`; path `/abc` | 0/1/0 |
| M22 | (d) A last `$` “anchors the match at the end of the path”. | `Disallow: /a*b$`; path `/abx` | 0/1/0 |
| M23 | (d) Match a prefix “starting at its first character”. | `Disallow: /a*b`; path `/x/ab` | 0/1/0 |
| M24 | (d) “* in a rule matches any sequence of characters (also none)”; intervening literals remain ordered. | `Disallow: /a*b*c`; path `/acb` | 0/1/0 |
| M25 | (d) “* in a rule matches any sequence of characters (also none)”; anchored middle literals cannot reuse prefix characters. | `Disallow: /ab*b*c$`; path `/abc` | 0/1/0 |

## Evidence and restoration
Pristine and restored SHA-256 for every probe, also the unchanged clone base tool: `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`. Every detector receipt includes before/after hashes; all restored runs observed this exact hash.
Frozen unchanged selftest `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/clone/scripts/robots_audit_selftest.py` SHA-256: `01c61297987f043f3bdc80612e50f744ac6f84605c43963c63fc87e1e6151df4`.
Exact mutation definitions and absolute artifact paths: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/inventory.json:1`, SHA-256 `f093456dd72b28cdd6f5467ebfff4f5af32b3505fd034b6f820891e693a75bf1`.
Complete verdicts, all failing fixture names, and phase receipt paths: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/results.json:1`, SHA-256 `79486d3e4b677167b5143a911ff6fc418b9a814e1809d969cf567e05cf19f8a8`.
318-artifact absolute-path SHA-256 index: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/SHA256SUMS:1`, index SHA-256 `6c209f8efc158e07e290ad4746cce0dbe439deb8935f97e0badd8a0b5336e3e8`.
Behavioral runner: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/run_batch.py:1`, SHA-256 `78c5b304e367a8340b6f491e25a39d42ec306afd24c4b133b1916ec3fcb1ff2a`; witness runner: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/run_witnesses.py:1`, SHA-256 `abdf1d555b0fa5d3d6e3a811ae1ac6e8ce0d56896e9d5d483ba3bb48346e65bd`.
All ten witness manifests and robots bytes: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/witnesses/specs.json:1`, SHA-256 `e0f94cce8628f012cc51afaee8f7a2374a7a69063c75804893b4fdbaef07529f`; actual command argv/outputs: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/evidence/witnesses/M04.json:1` through the other survivor-id files, and `batch.json`.
Per-mutant raw evidence: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/evidence/{pristine,mutated,restored}/Mxx.{receipt.json,stdout.json,stderr.txt}`; exact restoration transitions: `/fast/scratch/hyaku/kake-r38w1/MutBaseSelftest/evidence/restoration.json:1`, SHA-256 `d857e707326745b9161845409681e3ddc63ee687bd7965e25af16818a7c68d81`.
Probe sources were restored before the restored detector batch; intentionally retained mutant files are separate deliverables, not restored source paths. Each command child process group was cleaned up in a finally block; all batches and witnesses completed.
No sealed trees or round-38 counters touched; no network or owned-site requests; no round-37 counter run, build, integration, or round admission verified. These 25 mutants are a bounded sample, not exhaustive coverage.
Tool installs/updates: none. The fleet/lane source, selftest, Git index and jj state were not mutated; only this scoped lane report was written. Witnesses are proposed fixture inputs, not a changed contract.
