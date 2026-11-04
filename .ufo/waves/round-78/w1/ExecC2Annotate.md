# ExecC2Annotate — kake round 78, w1, C2 (freshness)

**Verdict: C2 met on the frozen predicate, on the sidecar route — 16 line-hash-bound entries + `~/projects` pinned gives carrier sweep `exit 0`, `drift=0 newMissing=0`, `paths.ok=true`; the revision-bound counter prints `met=true` with `control_exit=1`; the sweep's own `--selftest` stays 36/36. Zero `corpus/**/*.md` bytes changed.**

Lane `/home/vgpnk/Projects/shokunin/kake-shokunin` · base `fe50945399a386b48678b1f2051fdbe8a77b10bd` · carrier = lane worktree (C2 repair uncommitted) · counter measured the scratch fixture revision `e772f5d15df728d0e0ad5521fdac207b4dae4ba6`.

## Route — L1 mid-flight correction applied, no prose edit

The dispatch's inline-suffix route was **not** used. `corpus/QUALITY.md:31-39` (post-review append-only ruling, r20) and `:162` — "Original corpus lines remain byte-identical under the round20 ruling; line-hash-bound sidecars plus separate correction blocks replace suffix edits" — govern, as the L1 confirmed mid-wave. I applied the sidecar route only. **No `corpus/**/*.md` file was modified by this seat** (`git diff --numstat` on my scope is the two JSON files only; the sweep's `occurrences` is 734 before and after, i.e. no citation byte moved). Nothing required reverting.

## Counts — before → after

| term | base (2026-11-04T02:37:44Z) | carrier (02:45:53Z) |
|---|---|---|
| sweep exit | 1 | **0** |
| `drift` | 1 | **0** |
| `newMissing` | 1 | **0** |
| `paths.ok` | false | **true** |
| `declaredAbsent` | 64 | **65** |
| `resolve` | 32 | 32 |
| `declaredAbsentIndirect` | 4 | 4 |
| `unresolved` | 10 | 10 |
| `files` | 205 | 206 ¹ |
| `occurrences` / `uniqueTokens` | 734 / 107 | 734 / 107 |
| `missSet` | 65 | 65 |

¹ `corpus/knowledge/meta-robots-directives.md` (C3 seat) landed between the two runs and carries no absolute-path citation — `occurrences` is unchanged. Base receipt: `.ufo/waves/round-78/controls/base-c2-sweep.txt`.

## 1. Sidecar entries — `corpus/knowledge/freshness-sidecar.json`

Entry count **174 → 190** (+16); `kind=absent` **4 → 20**. Diff **144 insertions(+), 0 deletions(-)** — pure append, no existing entry edited. Each entry binds `file:line` to that line's sha256, `date=2026-11-03`, `kind="absent"`, token `~/projects` (already the canonical `~` spelling, so `canonHome(token) === token`).

| # | file:line | lineSha256 (first 12) |
|---|---|---|
| 1 | `corpus/lessons/round-66-verifier-spotcheck.md:101` | `25c19845e8df` |
| 2 | `corpus/lessons/round-66-verifier-spotcheck.md:102` | `94295b3ee5d1` |
| 3 | `corpus/lessons/round-66.md:69` | `1a182755f680` |
| 4 | `corpus/lessons/round-70.md:119` | `e52c3ace1b60` |
| 5 | `corpus/lessons/round-71.md:73` | `2b6255ed0a9a` |
| 6 | `corpus/lessons/round-73.md:59` | `5d348b60b725` |
| 7 | `corpus/lessons/round-74-verifier-spotcheck.md:36` | `072e235cc239` |
| 8 | `corpus/lessons/round-74-verifier-spotcheck.md:101` | `f2c9bb4c4aa8` |
| 9 | `corpus/lessons/round-74-verifier-spotcheck.md:137` | `d6c68e4f18f0` |
| 10 | `corpus/lessons/round-74-verifier-spotcheck.md:175` | `6a232c8ce7cb` |
| 11 | `corpus/lessons/round-74.md:70` | `8d770da20f62` |
| 12 | `corpus/lessons/round-75-verifier-spotcheck.md:91` | `3e064eb91937` |
| 13 | `corpus/lessons/round-76-verifier-spotcheck.md:99` | `a52bc0363fc5` |
| 14 | `corpus/lessons/round-76.md:127` | `32a7bf822d73` |
| 15 | `corpus/lessons/round-77-verifier-spotcheck.md:97` | `8ba6a34a9820` |
| 16 | `corpus/lessons/round-77.md:108` | `066da72dae5a` |

Note text (one per entry, `<file>:<line>` substituted):

```
2026-11-03: ~/projects absent on this host (test -e exit 1) — the lowercase tree was consolidated into the capital root in W6, the 2026-09-29 03:13–03:14Z lowercase-tree consolidation (corpus/lessons/round-17.md; SKILL.md:310). Citation <file>:<line> is a historical record, not an executable instruction.
```

It satisfies every `loadPathSidecar` conjunct (`scripts/freshness-sweep.mjs:359-395`): date present, `ABSENT_RE` word `absent` in the note *after* `PATH_RE` blanking, and the exact phrase `historical record, not an executable instruction`. Independent cross-check: ScoutCites derived the same 16 cites **and the same 16 line shas** from the sweep's own `unannotatedCites` (`.ufo/waves/round-78/w1/ScoutCites.md` §2.1); the two derivations agree entry for entry.

Helper (new, adapted from round 66 with `--date` and a truthful per-token cause): `.ufo/waves/round-78/sidecar_from_drift.mjs`, sha256 `cc4883bea676835b5888e9ebb616e61ac7554c35ccd3fbca65e975edcb0f304d`. Idempotence re-run after the append: `before=190 added=0 skipped-existing=16 after=190 dry=true`.

## 2. Pin diff — `corpus/knowledge/freshness-pins.json`

`pathsMissSet` **93 → 94**, sorted (`m == sorted(m)`; `~/projects` sorts last, after every `~/Projects/…`). Metadata bumped per the file's own convention (every prior pin edit does this, e.g. `4b03efe1`):

```diff
- "updated": "2026-11-01",
- "round": 67,
+ "updated": "2026-11-03",
+ "round": 78,
@@ -147,7 +147,8 @@
    "~/Projects/webzites/state/probe-latest.json",
-   "~/Projects/webzites/state/rebuild-charter-fire.log"
+   "~/Projects/webzites/state/rebuild-charter-fire.log",
+   "~/projects"
   ],
```

File sha256 after: `c3def789fda4bd94353e3197c9ce077e8ec0103fb92e9b960f7037669e2505c8`. Note: the L1's message estimated `94 → 95`; the file measured **93 → 94**.

## 3. Receipts (all under the lane; sha256 of retained bytes)

| receipt | command | exit | sha256 |
|---|---|---|---|
| `.ufo/waves/round-78/controls/after-c2-sweep.txt` | `node scripts/freshness-sweep.mjs --offline` and `… --offline --json` (cwd = lane) | 0 / 0 | `ea5227262ab67816c04e71668351ca88b43ed89d12714576af6cf40364f55fa3` |
| `.ufo/waves/round-78/w1/ExecC2Annotate/after-sweep-selftest.txt` | `TMPDIR=<scratch>/tmp KAKE_SELFTEST_DIR=<scratch>/selftest node scripts/freshness-sweep.mjs --selftest` → `selftest: 36/36 passed` | 0 | `8e2238b1488a59140d2c81d135658514268c14d2cefaaa544e1f6ea34e047b37` |
| `.ufo/waves/round-78/w1/ExecC2Annotate/negative-control.txt` | `python3 -B .ufo/waves/round-78/c78_sweep_truth.py --root <fixture> --revision e772f5d1… --work <scratch>` | 0 | `148be33bbff9a263df3d5fbb1c525712f7aa8e52a67761be72c25d073e3c926c` |
| `.ufo/waves/round-78/w1/ExecC2Annotate/sidecar-append.txt` | helper apply + idempotence + per-entry shas | 0 | `22fa7b83db9efdb269740adc6d19db5c2fab140f1f19aa6d1aa9191b2254afe1` |
| `.ufo/waves/round-78/w1/ExecC2Annotate/pins-diff.txt` | `git diff -- corpus/knowledge/freshness-pins.json` | 0 | `b3fd4c0266a00c018254be4edd3e0362aa1a3b2a14769e2734a774cd0012e56d` |

Counter output verbatim (`.ufo/waves/round-78/c78_sweep_truth.py`, sha256 `46acb450a2042249d0b589ed6614ab0c83e67e48da3eb5da69efd2ecbadb2821`, run from the worktree):

```
C2v1 revision=e772f5d15df728d0e0ad5521fdac207b4dae4ba6 sweep_exit=0 drift=0 new_missing=0 paths_ok=true skipped=2 control_exit=1 control_drift=1 tree_identity=d2279c72c195f7af met=true
```

**Why a fixture revision:** the counter was patched at 23:42 (after I first read it) to measure `git archive <rev>`, never the worktree (`c78_sweep_truth.py:5-6, 83-138`). My repair is uncommitted and I never commit, so I snapshotted the carrier into a scratch repo — `git init` + `git -C <lane> archive HEAD(c758904c)` + the carrier bytes of `freshness-sidecar.json`, `freshness-pins.json` and the helper — and measured that commit (`tree=a3c068ca…`). Fixture identity `d2279c72…`; **lane worktree identity at read time `36715895…`, differing in exactly one input: `corpus/README.md`, a concurrent C3 append.** Every C2 input (SKILL.md, pins, sidecar, sweep script, all other `corpus/*.md`) hashed identical. Re-cut on the landed revision: `python3 -B .ufo/waves/round-78/c78_sweep_truth.py --root . --revision <landed rev> --work <scratch>`.

## 4. Gate not loosened (four independent controls)

1. **Sweep selftest** `36/36 passed`, exit 0 — no case removed (`after-sweep-selftest.txt`).
2. **Counter selftest** `6/6 passed`, exit 0, including `t4 control green means the gate was loosened → met=False` and `t5 control that reports no drift is not proof → met=False`.
3. **Negative control** on the repaired revision: planting one unannotated cite of an absent target returns `exit 1`; the red is **attributable** — `DRIFT_TOKEN ~/Projects/kake-r78-control-absent/nothing-here.md`, `unannotated ['corpus/lessons/ctl-r78-unannotated-miss.md:6']`, `drift=1 newMissing=1` (`negative-control.txt` §attribution; `test -e` on the planted target → exit 1).
4. **Base reproduced** on the current counter: `sweep_exit=1 drift=1 new_missing=1 paths_ok=false control_exit=1 control_drift=2 met=false` — identical verdict to `controls/base-c2-sweep.txt`. Only its `tree_identity` digest differs (`c07506ac` now vs `ba1f923a` in the receipt): that receipt is 38 s older than the 23:42 counter patch, so the digests are not comparable while the verdict is.

Also: on the repaired tree the sweep still reports `missSet 65` and the pin only absorbs the *declared* token; per-citation AND (`:517`) is untouched — one new unannotated `~/projects` cite would re-open drift (ScoutCites §7 measured exactly that: `drift=1 newMissing=0`, exit 1).

## 5. What the repair exposed

1. **12 files, not 11.** The dispatch said "11 historical lesson files"; the measured population is **16 cites across 12 files** (round-74-verifier-spotcheck.md alone holds 4).
2. **Five of the 16 are table rows** (`74v:137`, `75v:91`, `76v:99`, `76:127`, `77v:97`). A naive inline suffix would land after the trailing `|` — a column change, which `QUALITY.md:37` forbids ("Never split a table"). The sidecar route avoids the class entirely.
3. **Annotations were already partial: 21 of 37 cites were annotated, 16 were not.** Nine direct, twelve window-only (ScoutCites §2.2). `declaredAbsentIndirect` stayed at 4, so the 16 new entries added no indirect/bleed classifications.
4. **No new token.** `~/projects` was already in `pathsCitedSet`; it was a first-seen *miss*, not a new citation. The only new cited token this round is `~/.omp/agent/config.yml` (`setDelta.citedAdded`; informational). Each of the 16 lines carries exactly one absolute-path token, so no neighbour could be re-classified by the append.
5. **The dispatch's cause date is wrong; I recorded the lane's own event.** The 2026-10-12 `~/Projects` prune/migration postdates the lowercase tree's removal. The record is W6, 2026-09-29 03:13–03:14Z (`corpus/lessons/round-17.md:9-21`; `SKILL.md:309-311`). ScoutCites §5 derives the same correction independently. Putting 2026-10-12 in the note would have written a false dated claim into the ledger.
6. **L0 `kake | round-69` is still unanswered** (fleet `.ufo/l0-questions.md:260` carries no ANSWER marker). The frozen round-78 contract orders its option (a) ("annotate and pin"); the earlier lane record (`corpus/lessons/round-76.md:127`) had refused to pin unilaterally while the L0 was open. Report-only — the pin now exists, and **the next round that corrects the corpus to `~/Projects` must remove `~/projects` from `pathsMissSet`**, or its next disappearance is masked.
7. **Stale non-gating pins.** `pathsFiles` is pinned at 179 against a live 206 (`filesAdded=27`, `filesRemoved=0`; 179 + 27 = 206); `filesAdded` is informational in `verdictOf`. Not re-pinned — outside this seat's scope, and a re-pin belongs with the round's corpus-file census.
8. **Receipt vintage.** `controls/base-c2-sweep.txt` predates the counter's 23:42 patch by 38 s; its `tree_identity` cannot be compared to the current counter's digest (verdict reproduces exactly). Worth a note in the L1's closure so a critic does not read the digest mismatch as drift.

## Tooling / scratch

No install or upgrade (node `v24.21.0`, system `python3`). Scratch root `/fast/scratch/hyaku/kake-r78/ExecC2Annotate` (`$HYAKU_SCRATCH` default), used for the carrier fixture repo, counter `--work`, sweep `TMPDIR`/`KAKE_SELFTEST_DIR`, and JSON dumps; the fixture's `git rev-parse --show-toplevel` was asserted equal to its own directory before the single commit. The whole scratch tree was removed after the receipts were copied into the lane (verified: `test -e` → 1).

Files this seat wrote: `corpus/knowledge/freshness-sidecar.json` (M, +144/−0), `corpus/knowledge/freshness-pins.json` (M, +4/−3), `.ufo/waves/round-78/sidecar_from_drift.mjs` (new), `.ufo/waves/round-78/controls/after-c2-sweep.txt` (new), and the four receipts under `.ufo/waves/round-78/w1/ExecC2Annotate/`. `scripts/freshness-sweep.mjs` untouched (sha256 `4bd99b04…`).
