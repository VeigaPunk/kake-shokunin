# ScoutCites — C2 recon (kake round 78, w1)

**Verdict: C2 is reachable exactly on the frozen predicate (proved `met=true` on a committed scratch fixture), but only with BOTH the 16 citations annotated AND the pin insertion; the dispatch's inline-suffix route collides with `corpus/QUALITY.md`'s post-review append-only ruling (sidecar route is the compliant, byte-preserving one), and the dispatch's "since the 2026-10-12" date is wrong for `~/projects` — the lane's own record dates the lowercase-tree removal to 2026-09-29 03:13–03:14Z (W6).**

All paths absolute unless noted; lane = `/home/vgpnk/Projects/shokunin/kake-shokunin`; base = `fe50945399a386b48678b1f2051fdbe8a77b10bd`. Receipts: `.ufo/waves/round-78/w1/ScoutCites/` (22 files, digests in `sha256sums.txt`).

## 1. Measurement at base

`node /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs --offline --json` at the lane root → **exit 1**.
Parsed JSON: `code=1`, `sections.paths.ok=false`, counts `resolve=32 declaredAbsent=64 declaredAbsentIndirect=4 drift=1 unresolved=10 newDrift=1 newMissing=1`; `reasons=["§paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet"]`; `skipped=["§armed (all remote checks)","§history (probe-history source absent — pin-declared)"]`.
Receipt `sweep-base-wt.json` sha256 `24b0f210dcf427696024a48bafa07f79a2fc4494165417cd91ed4150a05f4ebe`.

Revision binding: lane HEAD is `78711a6` (`78711a6 round-78: freeze contract, C1/C2 counters and controls, wave w1 spec`); `git diff --stat fe50945..HEAD` touches only `.ufo/waves/round-78/**`. Every one of the 23 scanned files that cites the token is byte-identical between `git show fe50945:<file>` and the working tree (sha256 checked for all 23, receipt `cites-base.json` carries each blob digest). So the parsed run is the base-revision state.

Scanner population: 205 files (`SKILL.md` + `corpus/**/*.md`), 734 occurrences / 734 rawHits / 107 unique tokens. For `~/projects`: **37 citing lines, 39 literal occurrences** (SKILL.md:309 and :311 carry the token twice: once in prose, once inside their own r20 annotation).

## 2. Population — every `~/projects` cite at base

### 2.1 Unannotated (16) — `unannotatedCites` from the sweep

| cite | line sha256 (12) | line shape |
|---|---|---|
| `corpus/lessons/round-66-verifier-spotcheck.md:101` | `25c19845e8df` | prose |
| `corpus/lessons/round-66-verifier-spotcheck.md:102` | `94295b3ee5d1` | prose |
| `corpus/lessons/round-66.md:69` | `1a182755f680` | prose |
| `corpus/lessons/round-70.md:119` | `e52c3ace1b60` | prose |
| `corpus/lessons/round-71.md:73` | `2b6255ed0a9a` | prose |
| `corpus/lessons/round-73.md:59` | `5d348b60b725` | prose |
| `corpus/lessons/round-74-verifier-spotcheck.md:101` | `f2c9bb4c4aa8` | prose |
| `corpus/lessons/round-74-verifier-spotcheck.md:137` | `d6c68e4f18f0` | **table row, ends `\|`** |
| `corpus/lessons/round-74-verifier-spotcheck.md:175` | `6a232c8ce7cb` | prose |
| `corpus/lessons/round-74-verifier-spotcheck.md:36` | `072e235cc239` | prose |
| `corpus/lessons/round-74.md:70` | `8d770da20f62` | prose |
| `corpus/lessons/round-75-verifier-spotcheck.md:91` | `3e064eb91937` | **table row, ends `\|`** |
| `corpus/lessons/round-76-verifier-spotcheck.md:99` | `a52bc0363fc5` | **table row, ends `\|`** |
| `corpus/lessons/round-76.md:127` | `32a7bf822d73` | **table row, ends `\|`** (461 B) |
| `corpus/lessons/round-77-verifier-spotcheck.md:97` | `8ba6a34a9820` | **table row, ends `\|`** |
| `corpus/lessons/round-77.md:108` | `066da72dae5a` | prose continuation (contains `\|` inside a code span) |

Full 37-row table (status + evidence + hash) in `cites-table.md`; per-cite windows in `cites-evidence.json`.

### 2.2 Already annotated (21) — for contrast

- **Direct (9)** — an ABSENT_RE word on the citing line: `SKILL.md:309`, `SKILL.md:311` (`absent`); `corpus/lessons/round-17.md:9` (`vanished`), `:16`, `:23`, `:25`, `:88` (`absent`); `corpus/lessons/round-69.md:65` (`absent`); `corpus/lessons/round-70.md:14` (`dangling`).
- **Window-only (12)** — the word sits at ±1/±2 only: `freshness-sweep.md:114`←L113, `freshness-sweep.md:54`←L52/53, `publish-queue.md:240`←L238, `round-1-aggregator-audit.md:10`←L11, `round-17.md:15`←L14/16, `round-17.md:22`←L23, `round-17.md:24`←L23/25, `round-59-verifier-spotcheck.md:42`←L43, `round-69-verifier-spotcheck.md:75`←L77, `round-70-verifier-spotcheck.md:40`←L38/39, `round-73-verifier-spotcheck.md:100`←L99, `round-73.md:19`←L17.

## 3. Annotation contract, and why each of the 16 is unannotated

`scripts/freshness-sweep.mjs`:

- `ABSENT_RE` — `scripts/freshness-sweep.mjs:133`: `/absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i`.
- `annotate()` — `:326-352`: every window line has `PATH_RE` replaced with `«cite»` first (`:328`), so an absence word *inside* a cited path never counts; direct match on the citing line wins (`:329`); otherwise the loop covers `i-2 … i+2` skipping `i` (`:334-335`) and takes the first matching line. The strict pin is opt-in and absent from `freshness-pins.json` (`grep -c pathsAbsenceStrictSameLine` → 0), so `:467` runs the loose window.
- Per-citation AND — `:517` `unannotatedCites = cites.filter(c => !rec.annotatedCites.has(c))`; `:529` `missSet = [...declaredAbsent, ...drift]`; classification at `:549-556` (exists → `resolve`; all cites annotated → `declaredAbsent`; any unannotated → `drift`).
- Exit predicate — `:588` `ok: drift.length === 0 && newMissing.length === 0`.

**For all 16 cites: the citing line carries no ABSENT_RE word, and no ±2 neighbour carries one either** (replayed `annotate()` exactly, with the same blanking; `cites-evidence.json` records `window_absent: []` for each). They are unannotated because the window is genuinely empty, not because a neighbour word was rejected. The nearest candidate vocabulary is *not* matched by `ABSENT_RE`: `unannotated` and `NEW MISS` appear around `round-66-verifier-spotcheck.md:101-102` (L99 `NEW MISS`, L103 `unannotated`), `drift` appears around `round-74.md:70` and `round-77.md:108`, and `unchanged` around `round-75-verifier-spotcheck.md:91` — `ABSENT_RE` matches `missing`, not `miss`, and has no alternative for these forms. No cite sits inside a fenced code block (checked per cite); 5 of the 16 terminate a markdown table row with `|`.

## 4. Proposed annotation text — and the route conflict

**Canonical inline text** (one bracketed, dated suffix; `annotation-suffix.txt`, sha256 `9f1466af…`), appended to the citing line with one leading space:

```
 *[r78 citation-local 2026-11-03: `~/projects` absent on this host — gone in W6, the 2026-09-29 03:13–03:14Z lowercase-tree consolidation; the 2026-10-12 prune/migration postdates it and removed capital-tree children; historical record, not an executable instruction.]*
```

It keeps the cited token and the sentence unchanged, adds only the one token already under test (no new path token), contains the sweep-required word `absent`, and carries the exact phrase the sidecar validator requires (`historical record, not an executable instruction`, `:386`).

**Conflict to route to the L1 before ExecC2Annotate applies a suffix.** `corpus/QUALITY.md:35-39` (post-review append-only ruling, round 20): *"a suffix changes the original line's bytes and hash even if its old text survives. Superseding rule: preserve every prior lesson/knowledge line byte-identically; use pure new-line additions or end-of-file correction blocks… An adjacent standalone note is allowed only with an inbound-anchor movement census and corrections for moved pointers."* `corpus/QUALITY.md:162` repeats it: *"Original corpus lines remain byte-identical under the round20 ruling; line-hash-bound sidecars plus separate correction blocks replace suffix edits."* All 16 lines are lesson lines. So the dispatch's "one bracketed suffix on the citing line" is precisely the mechanism the lane's own quality bar replaced; round 66 cleared 144 cites through the sidecar (`corpus/lessons/round-66.md:62-71`).

**Recommended route: 16 line-hash-bound sidecar entries** in `corpus/knowledge/freshness-sidecar.json` (174 → 190). Exact entries are in `sidecar-entries-proposed.json`; each was computed with the sweep's own algorithm (validated against an existing entry: recomputed `lineSha256` matches). Note template (per cite, with its own `file`, `line`, `lineSha256`):

```
2026-11-03: ~/projects absent on this host (test -e exit 1; the capital root is a different directory, inode 27238). Gone in W6, the 2026-09-29 03:13-03:14Z lowercase-tree consolidation; the 2026-10-12 capital-tree prune/migration postdates it and removed children of the surviving root. Citation <file>:<line> is a historical record, not an executable instruction.
```

Both routes were proved end-to-end in scratch (`$.ufo`-external copies of the base tree):
- sidecar + pin (exact textual edits, `pin-diff.txt` / `sidecar-diff.txt`): sweep **exit 0**, `drift=0 newMissing=0 paths_ok=true declaredAbsent=65` (`repair-sidecar-sweep.json`, sha256 `a0889527…`); all 23 SKILL.md/corpus files that cite the token remain **byte-identical to base** (only the two JSON files change).
- inline suffix + pin: also **exit 0** (`repair-suffix-sweep.json`, sha256 `a562f4b7…`), but 16 base lines change bytes, i.e. it fails the QUALITY r20 test.

For the 5 table rows, a naive append lands after the trailing `|` and risks a column-count/render change; table-aware placement would have to edit the last cell — still a byte change.

## 5. Truth check — `~/projects` vs `~/Projects`

`host-truth.txt` (sha256 `2fcc8711…`), on this host (Linux 7.2.11-arch1-1, 2026-11-04T02:41Z):

- `test -e /home/vgpnk/projects` → **rc=1**; `ls -d /home/vgpnk/projects` → **rc=2**, `No such file or directory`.
- `test -e /home/vgpnk/Projects` → **rc=0**; `ls -d` → rc=0; `stat` → **inode 27238, drwxr-xr-x**.
- `find /home/vgpnk -maxdepth 1 -iname projects` → only `/home/vgpnk/Projects inode=27238`.

So the lowercase path is absent and the capital path exists with the same inode the lane recorded at r16 — the host is case-sensitive and `test -e` is the oracle. The token is **not** a never-existed path: it existed with inode `101125103` at r16 (`SKILL.md:309`), so the cites are annotatable historical records, not fabrications.

Mixed-case history in the lane:
- `SKILL.md:309-312` — filesystem traps: `~/Projects` inode `27238`, lowercase `~/projects` inode `101125103`; **W6 (2026-09-29 03:13–03:14Z) absorbed the lowercase tree's children into the capital root, then removed `~/projects`**; `~/DIRMAP.md` gone in W7, the 2026-10-12 `~/Projects` prune/migration.
- `corpus/lessons/round-17.md:9-27` (the W6 vanish, mtimes 03:13:18–03:14:07Z), `:64` (*"the lowercase projects tree was consolidated into the capital Projects tree then removed in the recorded 2026-09-29 window"*), `:88`.
- `corpus/lessons/round-18.md:1`, `:16`, `:39` — the 2026-10-12 W7 mega-prune markers; every r18 marker in SKILL.md (`:16,18,19,30,157,283,334,343,365,370`) annotates a **`~/Projects/*`** cite, none the lowercase twin.
- `corpus/lessons/round-66.md:55-72` and `corpus/lessons/round-66-verifier-spotcheck.md:99-104` — the r66 pin diff: `recovered == exactly ~/projects`; the round-69 lesson (`round-69.md:65`) records that r66/r67's offline green was host-relative (case-insensitive filesystem), and that **this Linux host is red** on the token; open L0 `kake | round-69`.

**Routed discrepancy:** the seat prompt's "absent on this host since the 2026-10-12 `~/Projects` prune/migration" is contradicted by that record — the 2026-10-12 event pruned *capital-tree children* after the lowercase tree was already gone (2026-09-29). The proposed text therefore names the W6 event and says the 10-12 prune postdates it. If the L1 wants the 2026-10-12 phrasing anyway, that would put a false dated claim into the corpus; recommend correcting the dispatch instead.

## 6. `pins.pathsMissSet`

`corpus/knowledge/freshness-pins.json`: **93 entries, sorted** (`m == sorted(m)`); `~/projects` is **not** in it; `pathsCitedSet` *does* already contain it. Insertion index **93 (append at end)** — `"~/projects"` sorts after every `"~/Projects/…"` entry (lowercase `p` > uppercase `P`) and after `"~/DIRMAP.md"`; `m + ["~/projects"] == sorted(m + ["~/projects"])`.

Exact edit (`pin-diff.txt`, sha256 `a7b8872f…`, 12 lines):

```diff
@@ -147,7 +147,8 @@
    "~/Projects/webzites/state",
    "~/Projects/webzites/state/probe-history.jsonl",
    "~/Projects/webzites/state/probe-latest.json",
-   "~/Projects/webzites/state/rebuild-charter-fire.log"
+   "~/Projects/webzites/state/rebuild-charter-fire.log",
+   "~/projects"
   ],
   "projectsChildrenSet": [
```

Set-delta rules (`scripts/freshness-sweep.mjs`): `:544` `newMissing = missSet.filter(t => !pins.pathsMissSet.includes(t))`; `:547` `recovered = pins.pathsMissSet.filter(t => !missSet.includes(t))`; `:588` `ok = drift==0 && newMissing==0`. A token annotated at every cite moves from `drift` to `declaredAbsent`, but `declaredAbsent` is still in `missSet` (`:529`), so without the pin it becomes `newMissing=1` and stays red; with the pin it is a declared, pinned miss. Both halves are required — proved: annotated-but-unpinned → exit 1, `drift=0 newMissing=1` (`ctl-annotated-unpinned.json`, sha256 `847fcf80…`); pinned-but-unannotated → exit 1, `drift=1 newMissing=0` (`ctl-pin-only-repro.json`, matching `controls/ctl-c2-pin-only.txt`).

## 7. The gate can still fail

- `node scripts/freshness-sweep.mjs --selftest` → **exit 0**, `selftest: 36/36 passed` (`selftest.txt`, sha256 `ba3e7fe7…`); no case removed.
- Round-78 control `controls/ctl-c2-pin-only.txt` (read, not edited): `exit=1`, `C2ctl drift=1 newMissing=0 paths_ok=false code=1 met=false`. Independently reproduced on a base archive + pin only: `drift=1 newMissing=0 paths.ok=false code=1` (`ctl-pin-only-repro.json`).
- **New unannotated cite of the already-pinned token after the repair**: on the repaired tree, one bare `~/projects` cite on a new line → **exit 1**, `drift=1 newMissing=0`, `reasons=["§paths: 1 unannotated miss · 0 NOT in pins.pathsMissSet"]`, drift entry `~/projects` with the new cite (`ctl-new-same-token-cite.json`, sha256 `9171e93b…`). Pinning does not absorb unannotated cites; the per-citation AND keeps the gate armed.
- The C2 counter's own negative control on a *repaired* revision (base archive of the annotated tree + planted `~/Projects/kake-r78-control-absent/nothing-here.md`) → **exit 1**, `drift=1 newMissing=1` (`ctl-c2-on-repaired.json`, sha256 `24229b38…`).
- Full frozen predicate on a committed scratch fixture (16 sidecar entries + pin, commit `35bf725f`, throwaway identity inside the fixture only): `c78_sweep_truth.py` → **exit 0**, `C2v1 revision=35bf725f… sweep_exit=0 drift=0 new_missing=0 paths_ok=true skipped=2 control_exit=1 control_drift=1 tree_identity=1cbb0e6b46ce9d44 met=true` (`c78-predicate-on-fixture.txt`, sha256 `8c23a5e5…`); counter `--selftest` **6/6 passed**, exit 0 (`c78-selftest.txt`). Counter digest run: `c78_sweep_truth.py` sha256 `46acb450…` (note: `git status` shows it **M** — it changed during the round, not by this seat; my run used the landed working-tree version with the `tree_identity` conjuncts).

## 8. Proof matrix (all runs, verbatim exits)

| tree | edits | exit | drift | newMissing | paths_ok | receipt |
|---|---|---|---|---|---|---|
| lane working tree (= base content) | none | 1 | 1 | 1 | false | `sweep-base-wt.json` |
| base archive | pin only | 1 | 1 | 0 | false | `ctl-pin-only-repro.json` |
| base archive | sidecar only (no pin) | 1 | 0 | 1 | false | `ctl-annotated-unpinned.json` |
| base archive | 16 sidecar + pin (exact textual edits) | **0** | 0 | 0 | true | `repair-sidecar-sweep.json` |
| base archive | 16 inline suffixes + pin | **0** | 0 | 0 | true | `repair-suffix-sweep.json` |
| repaired tree | + 1 new unannotated `~/projects` cite | 1 | 1 | 0 | false | `ctl-new-same-token-cite.json` |
| repaired tree | + planted absent token (C2 control) | 1 | 1 | 1 | false | `ctl-c2-on-repaired.json` |
| committed fixture | 16 sidecar + pin, `c78_sweep_truth.py` | **0** | 0 | 0 | true | `c78-predicate-on-fixture.txt` (`met=true`) |

## 9. Residuals (named, not fixed by C2's predicate)

1. **QUALITY-level annotation quality is not met by the sweep's window alone.** 12 of the 21 "annotated" cites are window-only; four window words are unrelated to the token: `round-59-verifier-spotcheck.md:42`←L43 (`cli.mjs` "absent from the base tree"), `round-69-verifier-spotcheck.md:75`←L77 ("the r15 **absent** branch"), `round-73.md:19`←L17 (`dangling` in a c70 pointer row), `round-70-verifier-spotcheck.md:40`←L38/39 (`dangling=17` audit count). `corpus/QUALITY.md:14` explicitly rejects window-only words. C2's frozen predicate does not touch these; they remain routed debt.
2. `corpus/lessons/round-69.md:65` is classified *direct* by the sweep, but its word `absent` refers to **`pins.pathsMissSet` membership**, not filesystem absence — a false direct annotation under `QUALITY.md:14`.
3. 548 literal `~/projects` occurrences exist in the base tree outside the sweep's population (`.ufo/**` logs/receipts/frozen copies, `LOG.md`, `SCORECARD.md`); they are not scanned and are not annotated by design (the §paths population is SKILL.md + `corpus/**/*.md`).
4. `~/projects` appears only in historical/narrative statements at all 16 unannotated cites (measured-vs-base counts, rejection lines, residual lists); none is an executable recipe, so the annotation does not silence a live instruction.

## 10. Post-recon observation (not this seat's edit)

At `2026-11-04T02:52Z` the lane working tree already carried the compliant sidecar route, applied by a concurrent seat: `corpus/knowledge/freshness-sidecar.json` 174 → 190 entries (16 with token `~/projects`), `pathsMissSet` 93 → 94 with `~/projects` at the sorted end, `_round` 67 → 78 and `_updated` 2026-11-03, and **zero** files under `corpus/lessons/` modified (`git diff --stat corpus/`, `git status --porcelain`). A read-only sweep at that state: **exit 0**, `paths.ok=true drift=0 newMissing=0 declaredAbsent=65` (`sweep-at-recon-close.json`, sha256 `aaf15919…`). This matches §4's recommended route and §6's exact insertion point; ownership stays with ExecC2Annotate, and the state was in flux (other seats were writing `PROVINCE.md`, `SHONEN.md`, `corpus/README.md` at the same moment).

## Tooling / scratch

No tool installed or upgraded (node `v24.21.0`, python3 as shipped). Scratch root `$HYAKU_SCRATCH/kake-r78/ScoutCites` (`HYAKU_SCRATCH` defaulted to `/fast/scratch/hyaku`); every fixture was created there, the git fixture's `rev-parse --show-toplevel` was asserted equal to its own directory before commit, and the whole scratch tree was deleted with `rm -rf` after the receipts were copied into the lane — `test -e` on the scratch dir returns rc=1 afterwards.
