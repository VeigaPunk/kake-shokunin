# ScoutSweepHistory — round-64 wave-1 attack report

Seat: `ScoutSweepHistory` (leaf; no subagents). Lane: `kake-shokunin`.
Scope (assignment): reproduce the `controls/sweep-before.txt` receipt
independently — archive `9f671056` (round-60 tip), `d2da25de` (round-61 base)
and `1a481315` (round-63 base) into scratch and run
`node scripts/freshness-sweep.mjs --offline` in each; all three must exit 2
with the same `paths sidecar binding invalid: SKILL.md:364` fault — and
confirm via git log that `corpus/knowledge/freshness-sidecar.json` was last
modified before this round at `3d07733b` (round-24).

Verdict: **the sweep-before claim reproduces exactly, and the git-log claim
confirms.** All three archives exit 2 with a byte-identical first error line
(`freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364`), the
sidecar blob is unchanged from `3d07733b` until the round-64 build
`4c8295fa`, and the fault is attributable, commit-exactly, to round-54's
`8e408e00` inserting one SKILL.md line. The attack also surfaced **one
factual error in `corpus/lessons/round-64.md` §Mistakes** (attribution of the
first line-shifting edit) — the C3 claim's substance is unaffected.

---

## 1. What I attacked

| # | Target | Attack | Result |
|---|---|---|---|
| A1 | sweep-before receipt at the three named revisions | `git -C <lane> archive <rev> \| tar -x -C <scratch dir>` for `9f671056`, `d2da25de`, `1a481315`, then `node scripts/freshness-sweep.mjs --offline` in each | all three **exit 2**, first line identical to the receipt; only stack-frame paths differ (my scratch dirs) |
| A2 | receipt reproducibility outside `git archive` | fresh `git clone --no-local` + `checkout 1a481315`, same command | exit 2, same fault (`clone-r63`, verified `rev-parse --show-toplevel` = the clone dir) |
| A3 | sidecar git history | `git log -- corpus/knowledge/freshness-sidecar.json`, blob ids at 5 revisions, commit count in `3d07733b..1a481315` | exactly two commits ever touched it: `3d07733b` (round-24) and `4c8295fa` (round-64); blob `53ae3eeb` identical at round-24 tip and all three named revisions; **0 commits** between `3d07733b` and `1a481315` touched it |
| A4 | fault mechanism | read `scripts/freshness-sweep.mjs` `loadPathSidecar` (line 386 throw) + tail catch (`process.exit(2)`); compare sidecar pins vs actual SKILL.md lines per archive | seven SKILL.md pins stale by exactly +1 line; `SKILL.md:364` is the first failing entry in sidecar array order, so it names the fault; script blob `185f0ef2` byte-identical at all four revisions, so stack frames match the receipt's (386/400/1032/1096/1669) |
| A5 | origin of the fault | commit-by-commit sweep over `3d07733b..1a481315` (104 commits, archived+run each) | exit 2 begins exactly at `8e408e00` (round-54 build, 2026-10-25 10:37:55 −03) and holds at every later commit through `1a481315`; parent `acae1dcc` exits 0 |
| A6 | the lesson's causal claim (§Mistakes: shift by round-56 `f8438a28`/`4cb225fb`) | diff hunks of both commits + pinned-line sha at five revisions | **refuted**: both commits' SKILL.md hunks are net-zero (7→7 at line 209) or below the pinned block (767, 1250/1251); SKILL.md line 365 sha `7070c25fb9ab` identical from `8e408e00` through `1a481315` — neither commit shifted any pinned line |
| A7 | the repair (round-64 sidecar) | archive `4c8295fa`, run the sweep; diff old vs new sidecar entry-by-entry | exit 0, `drift 0`; exactly 7 entries differ, **only the `line` field** (364→365, 423→424, 431→432, 445→446, 448→449, 449→450, 450→451); `lineSha256` values unchanged (same content, same byte at the new line); the other 23 entries byte-identical |
| A8 | T0 vs live-lane equivalence | run the sweep in the lane working tree (HEAD `cc8add1f`) and compare with the `4c8295fa` archive | identical §paths numbers (172 files · 679 occurrences · 106 unique tokens; resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10), both exit 0 |

---

## 2. Evidence

Scratch root: `/fast/scratch/hyaku/kake-r64/ScoutSweepHistory/` (archives
`r60tip/`, `r61base/`, `r63base/`, `r64t0/`, `clone-r63/`, `chk-*`,
`tl-*`; deleted before yield — outputs are pasted below).

### 2.1 The three required reproductions (A1)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ for pair in "9f671056...:r60tip" "d2da25de...:r61base" "1a481315...:r63base"; do ...
    git archive $rev | tar -x -C $S/$name; done
$ for n in r60tip r61base r63base; do (cd $S/$n && node scripts/freshness-sweep.mjs --offline; echo "exit=$?"); done
=== r60tip ===
freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364
    at loadPathSidecar (file:///fast/scratch/hyaku/kake-r64/ScoutSweepHistory/r60tip/scripts/freshness-sweep.mjs:386:13)
    at scanCitations (.../r60tip/scripts/freshness-sweep.mjs:400:19)
    at runSections    (.../r60tip/scripts/freshness-sweep.mjs:1032:56)
    at main           (.../r60tip/scripts/freshness-sweep.mjs:1096:24)
    ...
exit=2
=== r61base ===  (same first line, frames 386/400/1032/1096/1669 at .../r61base/...) exit=2
=== r63base ===  (same first line, frames 386/400/1032/1096/1669 at .../r63base/...) exit=2
```

Committed receipt
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/sweep-before.txt`
(10 lines, sha256 `18eecc6b9d22e5cc9bdc889fce3b85ac980fcd5a272ab9f7669426a690ea72a8`)
has the identical first line and identical frame line numbers; it was captured
from the round builder's own scratch (`/fast/scratch/hyaku/kake-r64/l1/sweep-base/...`),
which is the only textual difference from my runs — exactly what a faithful
reproduction predicts.

### 2.2 Clone cross-check (A2)

```
$ git clone -q --no-local /home/vgpnk/Projects/shokunin/kake-shokunin clone-r63
$ cd clone-r63 && git checkout -q 1a48131577ba82c967650561be34e8dba909432a
$ git rev-parse --show-toplevel   -> /fast/scratch/hyaku/kake-r64/ScoutSweepHistory/clone-r63
$ git rev-parse HEAD              -> 1a48131577ba82c967650561be34e8dba909432a
$ node scripts/freshness-sweep.mjs --offline
freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364
exit=2
```

So the fault is a property of the committed tree content, not an artifact of
`git archive`.

### 2.3 Sidecar git history (A3)

```
$ git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --oneline -- corpus/knowledge/freshness-sidecar.json
4c8295fa round-64: build — repaired calibration counter (...) sidecar re-pin (7 entries, sweep exit 2->0) ...
3d07733b round-24: reconcile observed path drift without rewriting history
$ git log -1 --format='%H %ad %s' --date=iso -- corpus/knowledge/freshness-sidecar.json   (pre-round tip = 1a481315)
3d07733b... 2026-10-21 round-24: reconcile observed path drift without rewriting history
$ git log --oneline 3d07733b..1a481315 -- corpus/knowledge/freshness-sidecar.json | wc -l
0
$ git rev-parse <rev>:corpus/knowledge/freshness-sidecar.json
3d07733b -> 53ae3eeb79a3cbdc35bf726e6b6560cb5c78f101
9f671056 -> 53ae3eeb79a3cbdc35bf726e6b6560cb5c78f101
d2da25de -> 53ae3eeb79a3cbdc35bf726e6b6560cb5c78f101
1a481315 -> 53ae3eeb79a3cbdc35bf726e6b6560cb5c78f101
4c8295fa -> 0fa3d87acf17a01a932e0efd009de34a1161c96f
```

Confirmed: the sidecar's last modification before this round is `3d07733b`
(round-24, 2026-10-21), and it is the same blob at the round-60 tip, the
round-61 base and the round-63 base.

### 2.4 Fault mechanism (A4)

- `scripts/freshness-sweep.mjs:386` throws
  `` `paths sidecar binding invalid: ${e.file}:${e.line}` `` on the first
  sidecar entry whose pinned line is missing, whose sha256 mismatches, or
  whose token is not among the line's extracted path tokens; the tail
  `main().catch(...)` maps it to `process.exit(2)` (line 1669).
- Sidecar `kake-paths-sidecar-v1` has 30 entries; the 10 SKILL.md entries sit
  in array order `16, 19, 364, 445, 448, 449, 450, 20, 423, 431`. In every
  archive the lines pinned at 364/423/431/445/448/449/450 are stale by
  exactly one position (the pinned content lives at 365/424/432/446/449/450/451
  with the identical bytes), while entries at 16/19/20 still bind — so the
  first thrown entry is `SKILL.md:364`, which is the fault string in the
  receipt.
- The script blob is identical at all four revisions
  (`git rev-parse <rev>:scripts/freshness-sweep.mjs` → `185f0ef2c765ea71679ab80f7587bdff8c64894b`
  at `9f671056`, `d2da25de`, `1a481315`, `4c8295fa`), so the receipt's stack
  frames (386/400/1032/1096/1669) match my runs' frames exactly.

### 2.5 Origin bisect (A5) — every commit from pin to base, archived and run

104 commits in `3d07733b..1a481315`, each extracted via
`git archive <rev> | tar -x` and measured with the same command. The exit-code
timeline (full 104-row table was captured; key transitions):

| range | exit | notes |
|---|---|---|
| `3d07733b` … `7697990c` (round-24 pin → round-29 integrate) | 0 | sidecar binds; `3d07733b` itself exits 0 |
| `d8cd2e45` … `61046fcf` (round-29 wave-2 → round-42 verifier) | 1 | evaluable **drift** (`§paths: 1–2 unannotated miss`), repaired at round-43 `b49cba9c` ("C2 misroot-cite annotations + pins (sweep 1->0)") |
| `b49cba9c` … `acae1dcc` (round-43 → round-54 freeze) | 0 | healthy |
| `8e408e00` … `1a481315` (round-54 build → round-63 base) | **2** | `paths sidecar binding invalid: SKILL.md:364` at **every** commit, including the three named revisions |

```
acae1dcc 2026-10-25 round-54: freeze claims and calibration controls          -> exit 0
8e408e00 2026-10-25 round-54: repair S374 calibration and settle r53 ops debt -> exit 2 (SKILL.md:364)
```

`8e408e00`'s SKILL.md diff is a single insertion at hunk `@@ -210,6 +210,7 @@`
(the `c53-gate-truth` gate-registry row), pushing every SKILL.md line below
213 down by one — the exact mechanism that staled the seven pins.

### 2.6 The lesson's causal claim is wrong (A6)

`corpus/lessons/round-64.md:30` (§Mistakes, row 1) says:

> "SKILL.md growth after that (first post-pin edits `f8438a28`/`4cb225fb`,
> round 56, 2026-10-25) shifted seven pinned lines by +1"

Observed facts:

- `git show f8438a28 -- SKILL.md` hunks: `@@ -209,7 +209,7 @@` (net-zero
  replacement), `@@ -767,7 +767,7 @@`, `@@ -1250,7 +1250,7 @@`;
  `git show 4cb225fb -- SKILL.md` hunk: `@@ -1251,7 +1251,7 @@`. **No net line
  insertion anywhere; nothing above line 451 shifted.**
- SKILL.md line 365 (the re-pinned target of entry 364) has sha
  `7070c25fb9ab…` — byte-identical — at `8e408e00`, `f8438a28`, `4cb225fb`,
  `9f671056`, `d2da25de` and `1a481315`. The shift happened before both of
  those commits and they did not move it.
- The exit-2 fault already exists at `8e408e00` (round-54) and at every
  commit after it; the round-56 commits are ten commits into the fault window.

So the first post-pin line-shifting edit is round-54's `8e408e00`
(2026-10-25 10:37:55 −0300), not round-56's pair; and the could-not-evaluate
window is rounds **54–63** (ten round labels, 2026-10-25 → 2026-10-27), not
"~8 rounds" starting at 56. The lesson's row is right about everything it
pins (sidecar last re-pinned at `3d07733b`; fault string; the three named
revisions; the re-pin map) and wrong only about the attribution. C3's frozen
predicate does not depend on that attribution sentence, so C3 itself is
unaffected; but the §Mistakes row's "Captured-by evidence" cell misstates the
first defect-bearing commit, which is exactly the kind of provenance cell
this lane pins elsewhere.

### 2.7 The repair is minimal and sufficient (A7)

`git archive 4c8295fa` → run: `VERDICT: OK (exit 0, partial: offline)`,
§paths `resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10` — so all 30
entries (the 7 re-pinned and the 23 untouched) bind at T0.

Entry-by-entry diff of the sidecar blob `53ae3eeb` (base) vs `0fa3d87a` (T0),
keyed on (file, token, kind, date, note): 30↔30 entries, 0 added, 0 removed,
exactly 7 changed, and for each of the 7 the only differing field is `line`
(364→365, 423→424, 431→432, 445→446, 448→449, 449→450, 450→451). The
`lineSha256` values are byte-identical old→new (e.g. `7070c25fb9ab` →
`7070c25fb9ab`), matching `controls/sidecar-repin-map.txt`'s
`sha256(new line)` column, which repeats the old sha — a pure content-move
re-pin. The contract's clause "changes only `line` and `lineSha256` of seven
SKILL.md entries" is therefore satisfied a fortiori: the actual change-set
(`line` only) is a strict subset of the allowed set, and no note/kind/date/
token cell changed.

### 2.8 After-state cross-check (A8)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && node scripts/freshness-sweep.mjs --offline
§paths  172 files · 679 occurrences · 106 unique tokens
  resolve 31 · declaredAbsent 65 · drift 0 · unresolved 10
VERDICT: OK (exit 0, partial: offline)
exit=0
```

Identical numbers to the `4c8295fa` archive run — the after-state is
environment-independent. Note: the committed receipt
`controls/sweep-after.txt` (6 lines) is an **excerpt**, not a verbatim
capture — it omits the script header, the pins line and the entire §paths
block (including the `drift 0` line the contract's kill rule references).
The VERDICT line it does contain (`VERDICT: OK (exit 0, partial: offline)`)
implies drift 0 (a non-zero drift count forces exit 1), so the receipt is
not false — but it is not the raw output either. Flagging for the C3
reviewer seat; the raw output above supplies the missing block.

---

## 3. Judgment

- **Sweep-before receipt: REPRODUCED.** All three required revisions exit 2
  with the identical fault string `paths sidecar binding invalid:
  SKILL.md:364`; clone-based reproduction confirms it is tree-content, not
  archive-mechanism.
- **Git-log claim: CONFIRMED.** Sidecar last modified pre-round at `3d07733b`
  (round-24, 2026-10-21); identical blob at all three named revisions; zero
  intervening commits.
- **Origin: pinned commit-exactly.** The fault was introduced by round-54's
  `8e408e00fbe1c5908df62ba79e78c944bda479e2` (2026-10-25 10:37:55 −0300, one
  SKILL.md gate-registry row inserted at line 213) and stood at every commit
  through the round-63 base — rounds 54–63, ten round labels.
- **Lesson defect found (non-blocking for C3):** `corpus/lessons/round-64.md:30`
  §Mistakes attributes the first line shift to round-56's `f8438a28`/
  `4cb225fb`; both commits are provably shift-free (net-zero hunks; pinned
  line 365 sha constant from `8e408e00` onward). Recommended fix for the
  round settlement: correct the attribution cell to `8e408e00` (round-54) and
  the window to rounds 54–63.
- **Repair: minimal and verified.** The seven-entry re-pin changes only
  `line` values (sha cells unchanged); the sweep evaluates again at T0
  (exit 0, drift 0) in both the archive and the live lane.

Confidence: high — every claim above is backed by an exact command output,
git object id or byte-level sha comparison run inside this seat. The only
inference is the attribution mechanism (that `8e408e00`'s single-row
insertion is what staled the pins), which follows from the +1 line shift
observed at exactly that commit boundary plus the constant line-365 sha
afterward.

Remaining unknowns: none material for this seat. (Not audited here, by
scope: the C1/C2 counters, the S432 provenance, and the remaining C3
kill-rule clauses — other seats.)

---

## 4. Discipline

- No git/jj mutating command was run anywhere; no commit, no push, no
  `git bisect` (the origin scan used per-commit `git archive` extraction).
  The lane working tree is untouched: `git -C <lane> status --porcelain`
  shows only the orchestrator's pre-existing untracked wave files plus this
  seat's report file `.ufo/waves/round-64/w1/ScoutSweepHistory.md`.
- No frozen claim, counter, receipt, contract or lesson was edited.
- Scratch: everything lived under
  `/fast/scratch/hyaku/kake-r64/ScoutSweepHistory/` (archives, clone, scan
  dirs, `timeline.sh`); deleted before yield; all load-bearing outputs are
  pasted in this report.
- **No tools installed or upgraded** for this seat (node v24.21.0, git,
  python3, bash — all pre-existing); no `/home/vgpnk/.omp/agent/RULES.md`
  action needed.
