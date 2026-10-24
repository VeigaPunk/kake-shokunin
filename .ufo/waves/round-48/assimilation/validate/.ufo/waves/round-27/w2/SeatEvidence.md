# SeatEvidence — W1 registry / W2 accounting recount (author-side, freshness)

Seat `KakeR27.SeatEvidence` · leaf, read-only, no source/edit/commit/manifest/route change, no tool install.
Candidate authority: `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. Live tracked tree == candidate (`git status --porcelain --untracked-files=no` empty; `git diff --stat ac46a74` empty). Reports only.

## 1. W1 registry recount — EXPECTED (declared before probing): 67 unique identities, 67 nonempty named reports, role mix summing 67, and every W1 report byte-identical to the candidate blob.

Commands (read-only):
- `python3 -c` over `.ufo/waves/round-27/w1-dispatch.json` (`registry.members`), `w1-assignments.json`, `w1/swarm-registry.json`, `w1-record-result.json`, `w1-outcomes.json`.
- `python3 -c` over `.ufo/waves/round-27/w1/` directory + `git ls-tree`/`git cat-file -p ac46a74:…` for all 68 tracked w1 paths.

OBSERVED:
- Registry/identity counts: `w1-dispatch.json.registry.members` = 67 (agentId null at dispatch time); `w1-assignments.json` = 67 names → **67 unique agentIds** (`KakeR27.<Name>`); `w1/swarm-registry.json` = 67 members, agentId **all populated** (0 null); `w1-record-result.json` = 67 members; `w1-outcomes.json` = 67 rows, `spawned 67`, `identities 67`, `nonemptyReports 67`, all `status: completed`. Name sets identical across all five records (no member outside the assignment map).
- Reports on disk: `w1/` holds **67 `.md` files + `swarm-registry.json`**; every `.md` is nonempty, and all 67 have **distinct content** (67 unique sha256 — no duplicate-content report). Every row's recorded `bytes/lines/sha256` in `w1-outcomes.json` matches the file exactly → **0 mismatches**. All 68 tracked w1 paths (67 md + registry) are byte-identical to the candidate blob.
- Role mix, identical in dispatch registry, settled registry, record-result and outcomes: scout 21, reviewer 18, critic 20, executor 3, connector 1, scribe 2, revenger 1, sentinel 1 = **67**. Axes: 60 freshness / 7 operability (identical in spec, settled registry, record-result).
- Verdict density: all 67 reports contain a HOLD/STALE/UNVERIFIABLE/verdict token (0 verdict-less reports).
- Trailers: only 26 of 67 W1 reports carry a `Report:` trailer (41 do not). W1's own spec asked for the trailer form but did not enforce presence; **observation only, not scored**.

## 2. Three real writer worktrees — EXPECTED: three distinct real worktrees on unique branch/path at observed base `be375d90…`, each holding only its assigned source scope, uncommitted.

OBSERVED (`git -C <wt> rev-parse --abbrev-ref HEAD`, `rev-parse HEAD`, `status --porcelain --untracked-files=all`, `worktree list`):
- `writer-gate` → branch `kake-r27-gate`, HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2`; untracked `scripts/citing_set.py` **+** `.ufo/waves/round-27/git_name_selftest.py` (second file granted later by L1, documented in `residual/GitNameRegression.md`). No tracked diff, no commit.
- `writer-selftest` → branch `kake-r27-selftest`, HEAD `be375d90…`; untracked `scripts/citing_set_selftest.py` only. No out-of-scope path.
- `writer-fixtures` → branch `kake-r27-fixtures`, HEAD `be375d90…`; untracked **only** `scripts/fixtures/citing-set/**` (29 case dirs). `status | grep -v 'scripts/fixtures/citing-set/'` → empty. No tracked diff, no commit.
- Topology: all three are worktrees of the `writer-repo` **clone** (`.git` dir; `origin` = live repo). Live repo `git branch -a` shows **no** `kake-r27-*` branch and no writer commits; live `master == origin/master == ac46a74`. No commit/index/remote leak.
- Scope drift (authoritative bytes): the writer worktree copy `writer-gate/scripts/citing_set.py` sha256 `5b7b1f03…` ≠ candidate `3a361a00…`. Diff (22 lines) shows L1's later pre-freeze fixes applied at integration: `ls-tree -r` → `ls-tree -rz` (NUL framing) and pair-membership `if key in ledger_present` → `if (key, relative) in ledger_present`. Writer worktree copy is a stale intermediate; the **candidate** carries both fixes (candidate gate sha256 `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`).

## 3. Provider death / error / scope-void — EXPECTED: name every such report; BuildSelftest's prohibited stub smoke withdrawn, not PASS; line-bound overruns and unsupported pre-integration observations preserved.

OBSERVED:
- **No provider death, terminal provider error, empty report, or refusal in W1.** `w1-outcomes.json`: `dead: []`, `terminalProviderErrorsObserved: []`; independent scan of all 67 reports found 0 death/error markers, 0 policy-stop acts (only preserved references to the r24 stop, e.g. `Pair08A.md:3`, `PeripheralScope.md:49`), 0 policy refusals. All 67 rows `completed`; no replacement/resume identity (W1 `resumeSends: []`, `resume: 0`).
- **Prohibited scope act (named, void — not PASS):** `w1/BuildSelftest.md` §5 — mid-flight **synthetic stub-gate smoke** (stub gate sha256 `2c5949d4ebf774e5cf6680e2a637ce75823c589d9660b68d91922fa78ede79fb`, 8 synthetic cases, `failed=5`, exit 1) while the parent bound forbade mid-flight checks. The seat itself labelled it "**NOT repo evidence**" and "Not verified: no run against the real `scripts/citing_set.py`". Preserved in the candidate as VOID: `corpus/lessons/round-27.md:60` ("That smoke is VOID as acceptance evidence, not laundered PASS") and `:164` ("the stub smoke remains void acceptance evidence"). Independent check: `git grep 2c5949d4 ac46a74` matches **only** `w1/BuildSelftest.md` (the report itself) — the stub is credited as acceptance nowhere. Real acceptance evidence is separate: `verification/gate-selftest.json` = `python3 -B scripts/citing_set.py --selftest --root /fast/scratch/hyaku/kake-r27/author-candidate`, exit **0**, `cases 29, failed 0`, `meaning "Real29 consumer fixtures, no stub"`. **Not PASS from the stub; PASS only from the real 29-fixture run.**
- **Unsupported pre-integration observations preserved (not laundered):** (a) `BuildGate.md` §"Pre-integration correction" (L1 instruction, same file, no checks run) explicitly marks its range-grammar effect as "(inference, nothing executed)"; (b) `BuildGate.md:41` claims `frozen/expected.json` "pins 25 corpus/knowledge files" — **independent recount: 28 sha256 entries, 26 of them `corpus/knowledge/*`** (+`population.json`,`ledger.json`). The candidate lesson corrects it to "26 corpus files + population + ledger = 28 pinned inputs" (`corpus/lessons/round-27.md:64`), matching the frozen file.
- **Report-line-bound overruns (W1 bound was ≤180 lines, from `w1-spec.json` context):** exactly **2** exceed — `w1/CritIndependence.md` **217** lines, `w1/Pair07A.md` **200** lines (43 of 67 exceed 100; median 129). Both preserved and named in `corpus/lessons/round-27.md:163` ("Two build reports exceeded their180-line bound (Pair07A200, CritIndependence217)").
- **Other preserved L1-side defects (not re-litigated):** integration misroot of fixtures before any check (`lessons:62`); r26 role-floor debt executor 2 vs 3 → r27 dispatched 3 (`lessons:61`); reader pre-fix gate failure 57-missing / 23-of-29 accepted before evidence, no failure-confirmation rerun (`lessons:159-163`).
- **Stale hash in a committed report (finding):** `residual/GitNameRegression.md:10` states the "L1's fixed live gate" sha256 `790d732799510c69cd870ae89a331a2178ce84d6d98cbda13cb50a0aa5f05b92`. **No blob with that hash exists in any commit** (`git rev-list --all` × `cat-file` scan → 0 matches); the candidate gate is `3a361a00…`. The report describes a pre-integration intermediate and is not evidence for candidate bytes. Uncertainty: I cannot prove from the tree alone whether `790d73…` ever existed on disk.

## 4. W2 recount at snapshot — EXPECTED: dispatch/spawn identities and reports observed as they stand; pending reports not treated as complete.

OBSERVED:
- `w2-dispatch.json`: `counts {spawn 85, resume 0, total 85}`, `registry.members` 85 (agentId null at dispatch), `resumeSends: []`, `compaction.applied false`.
- `w2/swarm-registry.json`: **85 members, all 85 agentIds populated** (0 null), `updatedAt 2026-10-21T21:57:41.119Z`.
- `w2-assignments.json`: 85 names → 85 unique agentIds; set-equal to the 85 ids in `w2-spawn-result.json` text.
- **Observed spawn = 85, not 0**: `w2-dispatch-attempts.json` try 1 → `result "Spawned85"`, `spawned 85`, `capacityRefusals 0`, `payloadUnchanged true`, `at 2026-10-21T21:57:41.131723+00:00`; `w2-spawn-result.json` text "Spawned 85 background agents", `details.progress` = **85** entries, `details.results` = 0 (async, still running at spawn), `async.state running`. **Stale field, not an error:** `frozen-candidate.json` still says `actualFreshW2Spawned: 0` / `plannedFreshW2: 85` — written before W2 dispatch; the observed count is 85.
- **Report-file snapshot (2026-10-21T22:14:40Z): 64 `.md` in `w2/`**, 21 registry members **without** a report yet, 0 empty files. Pending seats are **not** counted as complete.
- W2 role mix: reviewer 68, scout 6, mutation-tester 4, critic 3, connector 2, sentinel 1, scribe 1 = 85; axes 42 freshness / 43 operability.
- **W2 line bound ≤100 (from `w2-spec.json` context) — 2 exceed at snapshot:** `w2/BindQuoteS001.md` 115, `w2/BindQuoteS004.md` 106. Live observation while reports are still landing; not final.
- `Report:` trailer present in only **11 of 64** W2 reports so far (W2 context requires a repo-relative trailer). Live observation, not final.
- Note: `w2-attack-design.json` plans 64 seats (`notDispatched: true`, "A design record only, never counted as validated/spawned work"); the actual dispatch was 85. Design-vs-actual gap, design doc self-declared as non-authoritative.

## 5. PrivacyBoundary residual executor + round spend — EXPECTED: PrivacyBoundary is one ordinary residual executor, separate worktree at base `9ba102d…`, NOT in the W1 registry; round spend with 85 W2 spawns = 153, not 151.

OBSERVED:
- `residual-identities.json`: `additionalFreshIdentity` = PrivacyBoundary / `KakeR27.PrivacyBoundary` / role executor / spawned 1 / completed true / worktree `/fast/scratch/hyaku/kake-r27/writer-privacy` / branch `kake-r27-privacy` / **observedBase `9ba102d4a0175c927adb54a005464ce2aa722099`** / report `residual/PrivacyBoundary.md` (100 lines).
- Independently confirmed: `writer-privacy` worktree exists, branch `kake-r27-privacy`, HEAD = `9ba102d4a0175c927adb54a005464ce2aa722099` — the **strict-status-enforcement commit, not** the three writers' `be375d90…` base; it is a separate worktree of the same clone. It is **absent** from the W1 registry (W1 assignments/registry/outcomes contain 67 names, none `PrivacyBoundary`) → **not** a W1 seat, and not a W2 seat.
- `sameIdentityResumption`: BuildGate was **resumed under the same identity** (no new identity, no restart). It therefore adds **0** to the identity count.
- **Round spend, recounted from observed artifacts: 67 (W1) + 1 (PrivacyBoundary) + 85 (W2) = 153 unique identities**, and the three sets are pairwise disjoint (`w1∩w2 = ∅`, `w1∩pb = ∅`, `w2∩pb = ∅`). **153 confirmed; 151 is wrong.** "151" is reachable only by dropping two identities (e.g. omitting the residual executor and one W2 seat, or counting 84 W2 spawns) — no such omission is supported by the dispatch/assignment/registry/spawn artifacts.
- Cross-check of spend-adjacent counts: W1 registry 67 + residual 1 = **68 unique author identities before W2** (matches `residual-identities.json.uniqueAuthorIdentitiesBeforeW2: 68` and `frozen-candidate.json.actualAuthorIdentitiesBeforeW2: 68`).

## 6. Incidental consistency checks (no defect found)
- Candidate `scripts/citing_set.py` = `3a361a00…`; `scripts/citing_set_selftest.py` = `3c167895…`; both equal the blobs in `ac46a74` and the `author-candidate` checkout. All 29 fixture files in `writer-fixtures` are byte-identical to the candidate blobs (0 diffs).
- `frozen/expected.json` sha `628b7a05…` and `frozen/ledger.json` `c2026376…`, `frozen/population.json` `16330e1e…` are **unchanged** across `be375d9 → 08014ce → 9ba102d → ac46a74` (original 16/28 inputs not rewritten).
- Counter evolution (distinct): `count_c1.py` `a1e46d19(be375d9) → 26fd8bbb(08014ce) → f2632131(9ba102d) → 8d4c22ef(ac46a74)`; `c2_count.py` `93f39b0f(be375d9) → 913a797f(08014ce, unchanged through ac46a74)`. Original counter bytes still differ from the candidate versions, as declared.
- C1 candidate measurement stands at `decided 55 / reviewedPairs 58 / citingPairs 58`, exit 1, 7 known-unverifiable units in 3 pairs (`verification/c1-current-candidate.json`); C2 = 16/16 detected, 0 false positives, exit 0; gate selftest 29/29; Git-name 30/30 after vs 10/30 failed before (isolated before-variant, not a failure-confirmation rerun). I did not re-run these; I only read the recorded artifacts.
- r26 tree unchanged: `git diff --stat 83528f7 ac46a74 -- .ufo/waves/round-26/` → empty.

## 7. Uncertainties
1. W2 is mid-flight: report count (64), line overruns (2) and trailer coverage (11/64) are a 2026-10-21T22:14:40Z snapshot and will move. No W2 seat is scored here.
2. `790d73…` (residual/GitNameRegression.md) cannot be located in any commit; whether it ever existed on disk is unprovable from the tree.
3. `w1-outcomes.json`'s `dead: []` / `terminalProviderErrorsObserved: []` is an L1 record; my independent scan of the 67 reports found no contradicting artifact, but I cannot query retired agent sessions, so a death that produced no report artifact would be invisible to me.
4. I did not execute r24 code, old stopped work, or any r26 replay; no tool install was needed or performed.

Report: .ufo/waves/round-27/w2/SeatEvidence.md
