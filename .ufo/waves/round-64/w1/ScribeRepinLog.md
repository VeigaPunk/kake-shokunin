# ScribeRepinLog — §2b old→new audit of the round-64 sidecar re-pin

Seat: ScribeRepinLog (leaf, no subagents). Scope: `corpus/lessons/round-64.md` §Mistakes re-pin table
vs `.ufo/waves/round-64/controls/sidecar-repin-map.txt` vs
`git diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- corpus/knowledge/freshness-sidecar.json`.
Base = round-63 tip `1a481315`; T0 = `4c8295fa`; pin commit = `3d07733b` (round-24, 2026-10-21).

## Verdict

- **Every changed sidecar cell is logged old→new exactly once, and every logged line change was made.** PASS for the 7 `line` cells.
- **No unlogged sidecar change.** The diff touches exactly 7 cells, all `line`, all `SKILL.md`. PASS.
- **Logged-but-unmade (partial FAIL, documentation only).** The lesson re-pin table and the map file both present a "new lineSha256" for all 7 entries. For all 7 entries the `lineSha256` cell is byte-identical to the round-24 pin value (`3d07733b`) and to T0. Zero `lineSha256` cells changed. The logged "new" digest is the unchanged pinned digest. The digest matches the line now at the new position, which is a true fact, but the table reads as a re-pinned digest. Kill rule not triggered: the contract permits `line` and/or `lineSha256` changes, and the lesson table is not a sidecar cell.
- **"23 further entries byte-identical" — PASS.** Verified at byte level, not only by JSON equality (see §3).
- The contract's "changes only `line` and `lineSha256`" overstates the actual change set. Real change set = `line` only.

## 1. Sidecar diff, cell level (T0 vs base)

Command (read-only lane access):
```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --numstat 1a481315… 4c8295fa… -- corpus/knowledge/freshness-sidecar.json
→ 7	7	corpus/knowledge/freshness-sidecar.json
git diff -U0 … | grep -c '^@@'      → 7 hunks
git diff -U0 … | grep '^[-+][^-+]'   → only `"line"` rows:
-   "line": 364,   +   "line": 365,
-   "line": 445,   +   "line": 446,
-   "line": 448,   +   "line": 449,
-   "line": 449,   +   "line": 450,
-   "line": 450,   +   "line": 451,
-   "line": 423,   +   "line": 424,
-   "line": 431,   +   "line": 432,
```
Source lines at T0: `freshness-sidecar.json` line 60 (`"line": 365`), line 96 (`"line": 451`); the other five are at the matching positions in hunks 2–7 of the same diff.

Structured audit (`audit_repin.py`, scratch; JSON-parsed both revisions, 30 entries each, same order):
- changed fields across all entries: `['line']` only; changed cells = 7; entries changed = 7; files = `['SKILL.md']`
- entry count base 30 → T0 30; top-level keys and `schema` (`kake-paths-sidecar-v1`) identical
- no `kind`, `date`, `note`, `token`, `file`, or `lineSha256` cell changed

## 2. Three-way cross-check (lesson table ↔ map file ↔ sidecar diff)

Lesson table, `corpus/lessons/round-64.md` lines 38–44 (7 rows, one per changed entry):

| row | lesson line | old→new | sha12 |
|---|---|---|---|
| ds4cc-marketplace source row | 38 | 364→365 | 7070c25fb9ab |
| property-map:c2 | 39 | 423→424 | 97576af9b60a |
| property-map:c10 | 40 | 431→432 | f2d75f797445 |
| property-map:c24 | 41 | 445→446 | f08a35d9d8cb |
| property-map:c27 | 42 | 448→449 | 6e1baa1fa1e9 |
| property-map:c28 | 43 | 449→450 | cfb08909875e |
| property-map:c29 | 44 | 450→451 | c16c7a6a684c |

Map file, `.ufo/waves/round-64/controls/sidecar-repin-map.txt` lines 3–9: same 7 `(old→new)` pairs, same sha prefixes, same `kind` (`restored`) and tokens.

Checks:
- lesson (old,new,sha12) set == map (old,new,sha12) set → True; 7 == 7 rows.
- map `(new line, sha)` == T0 sidecar `(line, lineSha256)` for the 7 entries → True.
- Each row appears once in the lesson table (exactly once, no duplicate).
- Label↔content: at T0, SKILL.md line 365 = `ds4cc-marketplace source row`; 424 = `[property-map:c2]`; 432 = `[property-map:c10]`; 446 = `[property-map:c24]`; 449 = `c27`; 450 = `c28`; 451 = `c29` (`git -C <lane> show 4c8295fa…:SKILL.md | sed -n '365p;424p;432p;446p;449p;450p;451p'`). All labels match their entries.
- Token and `kind` per entry unchanged.

Lineage of the seven shifts (verified with per-line sha256 over `git show <rev>:SKILL.md`):
- For each of the 7 entries, the stored `lineSha256` equals sha256 of SKILL.md line `old` at the pin commit `3d07733b`, and of line `old+1` at base `1a481315` and T0. So the +1 shift happened between the pin and base, not in this round. Base→T0 SKILL.md diff is `@@ -1361,2 +1361,4 @@` (two inserted gate-registry rows after line 1361), which is below every pinned line (max 451), so it does not move any pinned line.
- The old lines at base (364, 423, 431, 445, 448, 449, 450) carry the wrong content. The new lines (365, 424, 432, 446, 449, 450, 451) carry the pinned content. Consistent with the table.

## 3. "23 further entries byte-identical" — PASS

- 30 entries total = 7 changed + 23 unchanged. JSON-equal check: 23 unchanged entries (3 SKILL.md: pinned lines 16, 19, 20; 20 corpus/knowledge and corpus/lessons entries).
- Byte-level: `git diff -U0` shows only the 7 hunks above; stripping the `"line": N,` field from base and T0 and running `cmp` → IDENTICAL. Both files: 275 lines, same trailing bytes (`}\n`).
- Pin binding of the 23: at T0, each of the 23 entries' `lineSha256` still equals sha256 of its pinned line (`further_entries_binding_ok_count` = 23 of 23).

## 4. Sweep consequence (falsification test of the re-pin)

Scratch exports (`git archive`, no lane writes): `tree-base`, `tree-t0`, `tree-t0-basesidecar` (T0 tree with base sidecar bytes).
- `node scripts/freshness-sweep.mjs --offline` (node v24.21.0, pre-existing):
  - base tree → `freshness-sweep: Error: paths sidecar binding invalid: SKILL.md:364`, exit 2 (matches `controls/sweep-before.txt`).
  - T0 tree → `§paths 172 files · 679 occurrences · 106 unique tokens`, `drift 0 · unresolved 10`, `VERDICT: OK (exit 0, partial: offline)`, exit 0 (matches `controls/sweep-after.txt` VERDICT). Note `§armed` and `§history` are skipped offline and `complete=false`; this is the pre-existing offline mode, not introduced here.
  - T0 SKILL.md + base sidecar → same fault `SKILL.md:364`, exit 2. The seven `line` cells are necessary and sufficient for the binding fix.

## 5. Observations (not defects under the contract)

1. `lineSha256` column mislabel (the partial FAIL above). Suggested wording for a future edit, not made here: "lineSha256 (unchanged from round-24 pin; matches the line at the new position)". Lesson and map are frozen for this round; not edited.
2. Contract C3 says the re-pin "changes only `line` and `lineSha256`". Observed change set is `line` only (7 cells). Consistent with the kill rule (no cell other than the seven `line` pairs changed), but the wording is looser than the data.
3. The seven entries' notes still say e.g. `prior local-state annotations at SKILL.md:364 are historical` (date-stamped 2026-10-21, i.e. the pin-time coordinate). Contract forbids note changes; the reference is date-accurate, so no defect. Readers should not take it as the current line.
4. The T0 sweep reports `unresolved 10` in §paths. Outside this seat's scope; not a kill-rule term (kill rule is drift count only).

## 6. Commands and environment

- All lane access read-only: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show|diff|cat-file|archive`. No mutating git. Nothing written to the lane except this report.
- Scratch: `/fast/scratch/hyaku/kake-r64/ScribeRepinLog/` (audit script, JSON output, sidecar copies, three `git archive` trees, sweep outputs). Deleted before yield after the evidence above was recorded.
- Tools installed/updated: none. Used pre-existing `python3` (3.14 stdlib) and `node` v24.21.0.
- Sidecar sha256 (from scratch copies of `git show`): base `b09849f0698db1d81ca6218a316c3dde729c6a8294d209cb793868f6d0a974ac`, T0 `23234e04fb8b819d6ea3f015d70dbb4fd9192a8ed317e7412c43e7e14ca02a00`.
