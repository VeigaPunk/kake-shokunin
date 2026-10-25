# SentinelWriteScope — kake round 51, wave 1: seat write-scope audit

Snapshot taken **2026-10-25T03:39:07 → 03:40:15 -03:00** (lane clock; UTC+3h). Seats were still
running and still writing when this closed: the numbers below are a point-in-time snapshot and the
final state must be re-derived at scoring time with §7's commands. No file was deleted, moved or
reverted by this seat; the only path written is this report.

Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`
Lane tip at dispatch, and through §1–§9 of this report: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658`.
HEAD advanced to `907790c` (the wave-evidence commit) at 03:48:10, *after* this audit's body was
written — the landed state and what it does to §4 are recorded in §10.
Round-51 birth (`.ufo/waves/round-51/` dir birth): `2026-10-24T23:16:48 -03:00`.
Wave-1 seat window start (`.ufo/waves/round-51/wave-start-utc.txt` = `2026-10-25T06:32:17Z`): `2026-10-25T03:32:17 -03:00`.

---

## 1. The permitted write set

Every seat's item ends with `Write ONLY <abs path>`. Both the dispatch spec
(`.ufo/waves/round-51/w51-spec.json`) and the swarm registry
(`.ufo/waves/round-51/w1/swarm-registry.json`) were parsed: **48 seats, 48 distinct paths, no
duplicates, no path in one that is absent from the other** (name sets equal; per-name path equality
verified). Every permitted path is `.ufo/waves/round-51/w1/<SeatName>.md`:

```
ConnectorSiblingOverlap.md  CriticAbsence.md             CriticCapability.md
CriticGateCriterion.md      CriticHarm.md                CriticIds.md
CriticQuarantine.md         CriticShape.md               CriticStaleRows.md
CriticTautology.md          CriticZeroControl.md         ExecAccountingPrototype.md
ExecCensusMirrorValidate.md ExecLedgerMutants.md         ExecQuoteCounterMutants.md
ExecQuoteRawScan.md         ExecRegistryDiff.md          ExecRowShape.md
ExecSourceDigest.md         ExecSpecLint.md              MutationDropReport.md
MutationRoute.md            MutationSourceSha.md         MutationSwapIds.md
MutationWallClock.md        RevengerR50.md               ReviewAppendOnly.md
ReviewC1Predicate.md        ReviewC2Conditions.md        ReviewEntryScope.md
ReviewL1Accounting.md       ReviewL2Routes.md            ReviewL3Time.md
ReviewQualityBar.md         ReviewReportContract.md      ReviewShonen.md
ScoutCensusBefore.md        ScoutCounterC1Base.md        ScoutCounterC2Base.md
ScoutCounterC2Tip.md        ScoutMisroot.md              ScoutQuarantineSlice.md
ScribeEntryAudit.md         ScribeLessonShape.md         ScribeReportSources.md
ScribeSourcesCells.md       SentinelWriteScope.md        SimplifierCounters.md
```

At 03:40:15, `w1/` held 39 `.md` reports + `swarm-registry.json`. **Zero files in `w1/` fall outside
the permitted names** — no filename drift, no scratch files, no extra reports. 9 permitted reports
were still unwritten (task in flight). Re-checked at 03:46:05: **48/48 reports present, still zero
extras** (§10).

---

## 2. Out-of-scope writes found

"Out of scope" = any path outside the 48 above with an mtime ≥ round-51 birth. Files written before
03:32:17 are pre-dispatch (L1/planner authoring) and are listed separately, because they cannot be
attributed to a seat; files written at or after 03:32:17 are in the seat window and are the finding.

### 2.1 Seat-window writes (≥ 03:32:17) outside the permitted set — observed up to 03:40:15

| # | Time | Path (relative to lane root) | What changed | Attribution evidence | Severity |
|---|---|---|---|---|---|
| **S1** | 03:36:34 | `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` | mirror replaced: 145 → 143 rows, S262+S263 removed; sha256 `4ea81a5a…` → `cd9ee4cf…` | written 0.19 s apart with S1b by one process; equals `git show 19a99bd:corpus/SOURCES.md`; self-documented in `census-correction.txt` (03:36:45) | **HIGH** |
| **S1b** | 03:36:34 | `.ufo/waves/round-51/assimilation/pre-append/{census-argv,census-stdout,census-stderr}.txt` rewritten; `.…/superseded/{census-argv,census-stdout,census-stderr,census-exit}.txt` created | attempt-1 receipt quartet archived, new receipt written (argv/stdout/stderr end byte-identical to HEAD; mtime-only net effect) | same 187 ms burst as S1 | **HIGH** |
| **S1c** | 03:36:45 | `.ufo/waves/round-51/assimilation/pre-append/census-correction.txt` (2262 B, new) | narrative of the mirror defect and the re-run | file content names seat `ExecRegistryDiff` as finder, not author | MED |
| **S1d** | 03:39:13 / 03:39:24 | `.…/pre-append/census-exit.txt` (this time content returned to `0`, clean vs HEAD); `census-count-{argv,stdout,stderr}.txt` (new, 03:39:24) | exit receipt re-written a third time; `census census --file` baseline added (`rows 143`) | same remediation thread | MED |
| **S2** | 03:39:51 | `corpus/knowledge/canonical-selection.md` (+20/−1) and `corpus/knowledge/crawler-identity.md` (+21/−2), **same nanosecond** | the two admitted C2 entries edited: "quoted raw" → "rendered text", new "Quote classes (round-51 correction)" sections | the inserted text cites `w1/ExecQuoteRawScan.md`, **a report that did not exist at 03:40:15** (seat still mid-flight) | **HIGH** |
| **S3** | 03:33:53 | `.ufo/waves/round-51/__pycache__/c51_wave_ledger.cpython-314.pyc` (19415 B) + `__pycache__/` | bytecode for the C1 counter written beside the counter | pyc header names src mtime `2026-10-24T23:17:30`, size `12364` = the committed counter, so it was compiled from the unmodified source; a compliant `python3 -B` run cannot produce it — something *imported* the counter | MED |
| **S4** | 03:33:56 (+03:34:05) | 1526 loose files under `.git/objects/` + `.git/objects/pack/pack-2afa09c8….pack`; 1 tree at 03:34:05 | 1527 object files rewritten/recreated in the lane's Git object DB, 1.5 min after dispatch | filesystem-level; no git ref/index/reflog change (§3); all content reachable; full `git fsck` passes | MED (unattributed) |
| **S5** | 03:34:47 | `SCORECARD.md` (+33 lines: the round-51 declared-claims section) | planner doc | content is L1 prose ("Predicates were frozen in … contract.json") | LOW — L1 in-bounds, out of every seat's set |
| **S6** | 03:38:13 | `PROVINCE.md` (+15 lines: round-51 frontier step) | planner doc | same L1 authorship signature | LOW — same |
| **S7** | 03:32:17 | `.ufo/waves/round-51/wave-start-utc.txt` | dispatcher timestamp | exactly the declared wave-start instant | none (dispatcher) |
| **S8** | 03:37:08 | `corpus/SOURCES.md` | mtime bumped, **content identical to HEAD** (sha256 `4ea81a5a…` both sides) | a rewrite with zero net change — consistent with an attempted registry edit that was reverted; cannot be proven either way | INFO |
| **S9** | 03:36:34 | `.…/pre-append/superseded/` (new dir) | directory created | — | INFO |

Hard limit of this method: mtime sees retained files only. A seat that wrote and then deleted a
file inside the lane leaves no trace here (`.git`/`.jj` cannot answer for untracked files either);
only S8 is a detected rewrite-with-no-net-change.

### 2.2 Pre-dispatch writes (23:16:48 → 03:32:17), for completeness

**180 files**, all outside the seat set, all before any seat existed — planner/contract/counter
authoring: 175 under `.ufo/waves/round-51/` (contract, both counters, sources/receipts, the
assimilation+pre-append mirror, controls, route probes, `route-map.json`, `w51-spec.json`,
`w51-taskcall.json`, `build_wave_evidence.py`, `make_spec_w1.py`, `wave-grant.txt`), plus
`corpus/knowledge/canonical-selection.md`, `corpus/knowledge/crawler-identity.md`,
`corpus/lessons/round-51.md`, `corpus/SOURCES.md`, `LOG.md`. This is the L1's own round setup and is
not a seat violation; it is listed so the boundary is auditable.

Also in the round-51 window but **before dispatch**: the whole external tree
`/home/vgpnk/Projects/shokuknow/merge/kake/` (incl. `MERGE-REPORT.md/.json`) was written at
`2026-10-24T23:33:20`. The lane's bounds declare that path read-only for this wave; the write
predates seat availability by 4 h, so **no wave-1 seat can be the author**, but it is a write to a
declared read-only path inside round 51 and is flagged for the L1. (The other external path named in
the bounds, `absent-defect-register.md`, is untouched since 2026-10-24T08:37.)

### 2.3 Fleet worktree

`/home/vgpnk/Projects/shokunin` (excluding the lane, `.git`, `.jj`, `node_modules`), files with
mtime ≥ round birth: **exactly one** — `MANIFEST.json`, 03:33:51. It is **byte-identical to HEAD**
(`git diff --quiet` clean); the fleet's last commit touching it is
`8052650d1c7655d40e712f896e841877aa34c7d4`, 03:33:29, *"rounds ledger: kama r36 closure (admitted) —
hyaku, non-author"* — i.e. fleet rounds-ledger tooling for the **kama** lane, not a kake seat. No
sibling-lane content was written by this wave's seats within the mtime window.

The fleet's `.ufo/state/*.report-baseline` files are dirty in `git status` but their mtimes are
**older than the round** — pre-existing round-50 drift, out of this window.

---

## 3. What the .git object burst does and does not prove

Facts (S4): 1526 loose object files + one `.pack` carry mtime `03:33:56.11–56.30`; one additional
tree object at `03:34:05`.

Because a loose object's path *is* the SHA-1 of its content, an object file at path `ab/cdef…` can
only be that content. Verification:

- `git ls-tree`/`git rev-list --objects --all` (11 545 reachable OIDs) minus the 1526 new-mtime
  OIDs → **0 unreachable**. No new blob, tree or commit content entered the store.
- full `git fsck --no-progress` (hash-verifying, not just connectivity) → **exit 0**, only
  `dangling tree` lines (normal for this colocated jj/git repo). So no object is corrupt or
  tampered.
- `git count-objects -v` → `count 2537, in-pack 10760, packs 2, garbage 0, prune-packable 0`.
- **No commit, add, checkout, reset or stash happened**: `.git/HEAD`, `.git/refs/heads/master`,
  `.git/logs/HEAD` still carry mtime `23:23:07` and `.git/index` `23:26:34`; HEAD is still
  `9d13768`.

So the burst moved/rewrote existing, reachable bytes inside the object DB (pack ⇄ loose) without
changing repository content. It is still a write to `.git/**`, which is outside every seat's
permitted set. Mechanism not determinable from bytes; candidates, in order of plausibility: a `git
gc/repack/unpack-objects`-class invocation against the lane, a colocated-jj `jj` snapshot/import
(`.jj/repo` and `.jj/working_copy` dir mtimes are `03:33:46`, and `.jj` holds **no file** with
mtime ≥ 03:32:17 — a lock-acquire/release with no op head written), or a host-level copy/backup.
`.git/ORIG_HEAD` (Oct 20) and `.jj/repo/op_heads/heads/*` (23:23:08) are untouched, so the jj op
log did not advance.

---

## 4. The evidence-integrity finding behind S1: the committed pre-append mirror is not pre-append

This is the part of the write-scope audit that changes what the wave may claim.

At the measured tip `9d13768`:

```
git show 9d13768:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | sha256sum
  → 4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3   (258 lines, 145 rows)
git show 9d13768:corpus/SOURCES.md | sha256sum
  → 4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3   (identical)
git show 19a99bd:corpus/SOURCES.md | sha256sum
  → cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117   (143 rows, no S262/S263)
```

The committed "pre-append mirror" is **byte-identical to the post-append registry**: the artifact
that is supposed to witness the *before* state contains the two adopted rows, i.e. it was copied
after the append. Consequences at the tip:

- **C8 is not fooled**, because its implementation reads `show(root, mirror_commit, "corpus/SOURCES.md")`
  — the live registry *at the mirror commit* (`19a99bd`, 143 rows) — not the mirror path. It passes
  legitimately.
- **C7 is fooled, or rather blind**: `census-argv.txt` points at the mirror path, the recorded
  stdout ends `file ok <mirror path>`, and the counter only checks `--file` present, `--root`
  absent, mirror path present, `exit == "0"`, no `E03`/`E04`. It cannot see that the file it attests
  as the pre-append snapshot was the after-state. At the tip, condition C7 (`validate_before_append`)
  therefore passes on a receipt taken over a post-append file.

Reproduced at the tip, **after** the 03:39:51 entry edits (counters read `git show`, not the
worktree):
`python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768` → `8/8 met=True`, exit 0;
`python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768` → `0/3 met=False`, exit 1
(`L1` and `L3`: settlement absent; `L2`: route map absent) — dispatch state unchanged.

The wave's own remediation (S1/S1b/S1c, worktree only, uncommitted) replaces the contaminated mirror
with the true pre-append bytes (`cd9ee4cf…` = registry at `19a99bd`) and archives attempt 1 under
`superseded/`. That is truthful, and it is also an **in-place rewrite of a committed, scored
artifact**, performed from the seat pool's own user account with no distinguishing marker of who ran
it.

---

## 5. Trust boundary: 48 writers, one account, one directory

- Every seat and the L1 run as UID `vgpnk`. `.ufo/waves/round-51` is `drwxr-xr-x`, `w1/` is
  `drwxr-xr-x`, reports are `-rw-r--r--`. There is no per-seat isolation: any of the 48 concurrent
  seats can overwrite, truncate or forge any other seat's report, and can write any claim input
  (contract, counters, registry rows, entries, receipts, mirror).
- The permitted set is **textual** (`Write ONLY <path>` in the item), not enforced by a sandbox.
  S1–S4 are the proof: three distinct classes of write landed outside it during a single wave.
- `c51_wave_ledger.py`'s L1 check is stronger than a bare glob: it compares the *set* of seat names
  marked `report: true` against the *set* of `w1/*.md` basenames, so extra or missing report files
  are caught (`committed report files for unknown seats` / `seats marked with a report but no
  committed file`). What it **cannot** detect is a report whose name is right and whose content was
  written by another seat, and it cannot detect evidence files being rewritten *before* the evidence
  commit.
- The two counters are honest about their input: both resolve every byte through
  `git -C <root> show <rev>:<path>` (verified in `read_blob`/`show`/`show_bytes`; no `open()` of a
  worktree file). That is the only reason S1/S1b/S2 did not move the score.

**Exploit path (stated, not executed):** the wave scores a *commit* the L1 is about to create from a
worktree that 48 seats can write. A seat that edits `corpus/SOURCES.md`, `corpus/lessons/round-51.md`,
the pre-append mirror, a receipt or either counter between the last read and the L1's `git add -A`
+ commit changes what the "committed bytes" prove — with no scope check on the commit itself. S1 and
S2 are exactly that shape of write, made in good faith; the boundary does not distinguish good faith.
For this wave the concrete lived instance is S2: two admitted entry bodies were edited mid-wave by a
seat that cited its own not-yet-written report.

---

## 6. Not found

- No out-of-permitted filename in `w1/`; no extra report, no `*.tmp`, no scratch directory there.
- No sibling-lane or fleet files written by this wave's seats in the mtime window (only fleet
  `MANIFEST.json`, attributed to kama rounds-ledger tooling, content unchanged).
- No commit, tag, ref move, index change or reflog entry in the lane during the wave.
- No new/unreachable Git object content, no repository corruption (`git fsck` clean).
- No modification of `corpus/lessons/round-51.md`, `sources/S262.html`, `sources/S263.html`,
  `sources/receipts.json`, `contract.json`, either counter, or `w51-taskcall.json` (all verified
  byte-equal to `9d13768` blobs at 03:35 and again re-read before this report; the only claim inputs
  that differ are S1/S1b/S2/S8 above).

---

## 7. Commands used (all read-only; no `git add/commit/stash/checkout/reset`, no `jj` invocation)

```bash
# permitted set, from both authorities, and their agreement
python3 -c 'import json,re; ...'   # parse "Write ONLY (\S+)" from w51-spec.json items and
                                   # swarm-registry.json members; assert 48/48 names and paths equal
# windows
stat -c '%w | %y | %n' .ufo/waves/round-51 .ufo/waves/round-51/w1   # round birth 23:16:48
cat .ufo/waves/round-51/wave-start-utc.txt                          # 06:32:17Z = 03:32:17 -0300

# lane: every file with mtime >= round birth, minus the 48, split at the seat window
find . -xdev \( -path './.git' -o -path './node_modules' \) -prune -o -type f \
     -newermt '2026-10-24 23:16:48' -printf '%T@ %p\n'
find .git/objects -type f -newermt '2026-10-25 03:32:17' | wc -l        # 1527
find .git -type f -newermt '2026-10-25 03:32:17' -printf '%TY-%Tm-%TdT%TH:%TM:%TS %p\n'
stat -c '%y %n' .git/HEAD .git/refs/heads/master .git/index .git/logs/HEAD .git/ORIG_HEAD
stat -c '%y %n' .jj .jj/repo .jj/working_copy .jj/repo/op_heads/heads/*

# git object burst: content, reachability, integrity
git count-objects -v
git rev-list --objects --all | awk '{print $1}' | sort -u > /tmp/r51_reachable.txt
find .git/objects -type f -newermt '2026-10-25 03:32:17' ! -path '*/pack/*' | sed 's#.*/objects/##;s#/##' \
  | sort -u > /tmp/r51_new_sorted.txt
comm -23 /tmp/r51_new_sorted.txt /tmp/r51_reachable.txt | wc -l        # 0
git fsck --connectivity-only --no-progress ; git fsck --no-progress    # both exit 0
git verify-pack -v .git/objects/pack/pack-2afa09c8….idx | tail -3     # "…pack: ok"

# pyc provenance
python3 -c 'import struct; print(struct.unpack("<4sIII", open(".ufo/waves/round-51/__pycache__/c51_wave_ledger.cpython-314.pyc","rb").read(16)))'

# tracked drift and blob equality
git status --porcelain
git status --porcelain | grep -E '^( M|M |MM| D|D |R )'
git hash-object <path>  vs  git rev-parse 9d13768:<path>
git diff --stat -- <path> ; git diff -U1 -- corpus/knowledge/canonical-selection.md
sha256sum .ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md
git show 9d13768:.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md | sha256sum
git show 19a99bd:corpus/SOURCES.md | sha256sum
git log -1 --format='%H %ci %s' -- .ufo/waves/round-51/assimilation/pre-append/

# fleet worktree, excluding the lane
cd /home/vgpnk/Projects/shokunin && find . -mindepth 1 -maxdepth 1 -name kake-shokunin -prune \
  -o \( -name .git -o -name node_modules -o -name .jj \) -prune \
  -o -type f -newermt '2026-10-24 23:16:48' -printf '%TY-%Tm-%TdT%TH:%TM:%TS %p\n'
git -C /home/vgpnk/Projects/shokunin status --porcelain MANIFEST.json
git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %ci %s' -- MANIFEST.json

# external read-only paths
stat -c '%y %n' /home/vgpnk/Projects/shokuknow/merge/kake/
find /home/vgpnk/Projects/shokuknow/merge/kake -type f -printf '%TY-%Tm-%TdT%TH:%TM:%TS %p\n' | sort -r | head
stat -c '%y %n' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md

# the two counters, at the tip (no bytecode written: -B and PYTHONDONTWRITEBYTECODE=1)
PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/waves/round-51/c51_quote_truth.py --root . --revision 9d13768
PYTHONDONTWRITEBYTECODE=1 python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root . --revision 9d13768
```

Tooling: nothing installed or upgraded; no package manager was invoked.

---

## 8. Smallest remediation (owner: L1)

1. **Before the evidence commit**, assert the claim inputs are clean:
   `git diff --quiet -- corpus/SOURCES.md corpus/lessons/round-51.md corpus/knowledge/canonical-selection.md corpus/knowledge/crawler-identity.md .ufo/waves/round-51/contract.json .ufo/waves/round-51/c51_*.py`
   and `git diff --quiet HEAD -- .ufo/waves/round-51/assimilation/pre-append`. Any non-empty result
   must be *reviewed*, not committed blind. Today's result is non-empty: S1, S2, S5, S6.
2. Decide explicitly whether S2 (the two entry corrections) and S1 (mirror correction) are part of
   the round's landed bytes. If yes, commit them **with the correction narrative** (`census-correction.txt`,
   already written) so the delta is auditable; if no, restore them from `9d13768` and re-earn the
   correction in a later round. Do not leave them as uncommitted drift that a later `git add -A`
   sweeps in silently.
3. C7 should stop being blind to provenance: add to condition C7 (or to C2's docstring) that the
   mirror's bytes at the measured revision equal `show(mirror_commit, "corpus/SOURCES.md")`. That is
   a one-line equality that would have caught the contaminated mirror at the tip, with no other
   condition touched.
4. Have every counter invocation carry `-B` (or export `PYTHONDONTWRITEBYTECODE=1`) — the contract's
   counting command already does; the S3 pyc shows a raw import path exists in practice.
5. Give reports provenance cheaply: require each `w1/<SeatName>.md` to state its seat name and the
   `Write ONLY` path it was given, and have L1 assert the first line matches the basename. This does
   not stop a same-UID writer, but it makes an overwritten report visible.
6. Confirm or refute the external `shokuknow/merge/kake` write of 23:33:20 with the operator; it is
   outside this wave's authorship but inside a path the lane's bounds call read-only.

---

## 9. Limitations of this report

- **Two snapshots, both kept.** The body of this report (§1–§7) describes the state at 03:40:15, when
  39/48 reports existed and S2 had landed 24 s earlier; §10 adds 03:46:30 (48/48 reports, eight
  further out-of-scope files) and then the 03:48:10 evidence commit, at which both frozen claims
  verify `true`. Re-run §7 at scoring time. Anything written after 03:48:10 is in neither count.
- **Attribution is inferential for S1–S4.** Bytes show *what* and *when*, not *who*: all writers are
  UID `vgpnk`. S1/S1b are a single 187 ms process burst in the `pre-append` tree; S2 is one
  nanosecond-identical pair across two corpus files; S4 is a filesystem-level burst with no git
  command trace. I state the candidates and the evidence for each rather than naming a seat.
- **No history was read.** No harness transcript, shell history or `agent://` output was consulted;
  nothing here repeats another seat's conclusion — the two counter runs quoted in §4 are my own.
- **One unrun check:** I did not attempt to reproduce S4's mechanism (running `git gc`/`jj` against
  the lane would have mutated the very bytes this audit measures), and I did not verify the
  pre-append census re-run byte-for-byte against the corrected mirror — `census-count-stdout.txt`
  reports `rows 143`, which matches the corrected file, but I did not re-run
  `sources-census.sh validate` myself because it is outside this seat's assigned surface.

---

## 10. Post-snapshot delta (03:40:15 → 03:48:10) — the wave finished, then landed its commit

Everything below was re-derived with §7's commands after the snapshot; nothing earlier in this
report is retracted.

**Reports.** `w1/` reached **48/48** `.md` reports (`w1/` dir mtime `03:45:00`), and the file set is
still **exactly** the permitted 48 + `swarm-registry.json` — no extra name, no missing name.

**Eight further out-of-scope files, all after the snapshot:**

| Time | Path | Note |
|---|---|---|
| 03:40:16 | `.ufo/waves/round-51/assimilation/quarantine-slice.raw` (new) | byte-identical to the round-50 slice; `diff` exit 0 per `w1/ScoutQuarantineSlice.md` |
| 03:40:16 | `.ufo/waves/round-51/assimilation/quarantine-slice.argv.txt` (new) | self-documents the writing command: `awk -F"|" -v l=kake …absent-defect-register.md -> …/assimilation/quarantine-slice.raw` |
| 03:42:03 | `.…/pre-append/census-correction.txt` (rewritten) | same remediation thread as S1c |
| 03:42:03 | `.…/pre-append/census-count-exit.txt` (new) | `census --file` exit receipt |
| 03:43:14 | `.ufo/waves/round-51/settlement.json` (new) | L1 wave evidence (`spawn 48`) |
| 03:43:14 | `.ufo/waves/round-51/wave-timing.json` (new) | L1 wave evidence |
| 03:43:14 | `.ufo/waves/round-51/round-time-accounting.json` (new) | L1 wave evidence |
| 03:43:14 | `.ufo/waves/round-51/settled-utc.txt` (new) | L1 wave evidence |

The `quarantine-slice.*` pair is the one **seat-attributed** out-of-scope write in this audit, though
not by name: `w1/ScoutQuarantineSlice.md` (03:42:47) records that "another seat wrote untracked
`assimilation/quarantine-slice.raw` plus `.argv.txt`". Severity **LOW** — it duplicates an external
read-only register into the lane, touches no claim input and no committed blob. The four
`settlement/timing/accounting/settled-utc` files are the L1 authoring the C1 evidence (in-bounds for
the L1, outside every seat's set); they do not change C1's score at `9d13768`, which remains 0/3
because they are uncommitted.

**The wave-evidence commit landed while this was being written (03:48:10).** HEAD advanced from
`9d13768` to `907790c` — *"round-51: land the wave evidence, the ledger verdict and the mirror
repair"*, 88 files, +14301/−5. Verified at that commit with my own runs of both counters:

- **`C1 ledger 3/3 met=True` (L1, L2, L3 all pass)** and **`C2 quote-truth 8/8 met=True`**. The two
  frozen claims hold at the landed revision.
- **§4's C7 provenance defect is repaired in the landed bytes.** The mirror at `907790c` is
  `cd9ee4cf951f9708…` — 143 rows, **zero** adopted ids — not the contaminated `4ea81a5a…`; the
  committed `census-exit.txt` is `0`. C7 now attests a genuinely pre-append file. The defect was
  real at `9d13768` and is closed at `907790c`; both statements are true of their own revisions.
- S2's corrected entries are the landed entries (`e167e3ee…`, `2ea606a0…`); `corpus/lessons/round-51.md`
  (+85) and `LOG.md` (+19, wall clock **897 s**) are landed; `settlement.json` carries
  `spawn 48 / settled 48 / dead 0 / reports_written 48`.
- **The LOG verdict precedes the commit that makes it true by 11 s** (`LOG.md` mtime 03:47:59;
  commit 03:48:10). At the observation instant, "`C1 ledger 3/3 met=True` … at the round-51 commit"
  named a commit that did not exist, and the only existing revision (`9d13768`) printed 0/3. It is
  true at `907790c` and derivable now. Recorded as an ordering fact, not an accusation.
- **This report is inside that commit**, at the revision preceding this addendum
  (sha256 `3fad33d0a68c58bb21d75637c6069dc610b4f2c8b5308f7b654040df031659ea`). The addendum is
  worktree-only until/unless the L1 commits again; a reader diffing committed against live sees
  exactly this delta.
- Worktree after the commit: two seats rewrote **their own** reports post-commit
  (`w1/CriticZeroControl.md`, `w1/ReviewC2Conditions.md`). In-scope writes, but the live text now
  differs from the committed bytes the ledger scored — the same "report body is the durable locus"
  point, one layer up.

**Stable through 03:47:47.** Between the 03:40:15 snapshot and the commit, HEAD stayed `9d13768`
(no add, ref or index change), and the tracked-modified set grew from five to seven only with the
L1's own evidence assembly: `LOG.md` (C1-L3's named figure, 03:47:59) and
`corpus/lessons/round-51.md` (+85, "Corrections — attempt 2 (append-only)", 03:47:47).

**On the sibling-lane scratch relocation — not kake, and a move, not a deletion.** Two peer messages
about `.ufo/waves/round-35/scratch/` (first "removed by an external sweep", then corrected to
"moved") were checked independently, and the second is right. In
`/home/vgpnk/Projects/shokunin/mado-shokunin`: `.ufo/waves/round-35/scratch` is absent,
`.ufo/waves/round-35/scratch-evidence` exists (mtime `03:45:56`, **59** seat dirs), and
`scratch-evidence/RevQuoteS210/{rederive.sh,rederive.out}` are 3727 B / 2714 B with sha256
`468c54a6e2e2e2c79931ea416cadd4f027655199c4bcfb6e40174b90b6e675df` /
`4b7b77d6d3fd8bc661a61d5b02c53feebd4db68fbca3b8ad860649911c0a2026` — the peer's figures, reproduced
from the files themselves. The tree was relocated; nothing was lost.

**No kake lane involvement.** kake's `.ufo/waves/round-35/` has no `scratch*` directory at all
(`find .ufo/waves -maxdepth 2 -type d -name 'scratch*'` → empty), and round 51 has none either. This
report cites no `.ufo/waves/*/scratch/` path, so it has no dangling reference to fix: its evidence is
committed blobs, `git show` output and re-runnable commands. Scratch used during this audit lives in
`/tmp/r51_*`, is still present at 03:46, and is not cited as evidence — only the commands that
produced it are. Worth recording as a design signal for the wave itself: a scratch tree under
`.ufo/waves/` is neither stable nor access-controlled (the sibling lane reports seat dirs re-created
at 03:46 and swept again), which is exactly why the report body, not a scratch directory, has to be
the durable evidence locus.

**Effect on §9's unrun check.** `census-count-stdout.txt` now reports `file rows 143`, consistent
with the corrected mirror; `census-count-exit.txt` appeared at 03:42:03. I still did not execute
`sources-census.sh` myself, so the census's own verdict remains the L1's and the sibling seats'
evidence, not mine.
