# ScribeC1Superseded

Claim C1 (calibration) — drafted the append-only superseded axis-table evidence section for
`SCORECARD.md`. Nothing was appended to the lane file: the section exists only as a draft
(`.files/section.md`) and in the `SECTION:` block below. No lane/fleet file was modified.

## Behavior

Section heading `## Superseded axis-table evidence (round 59)`; appended at EOF (after
`No other comparable previous gate showed a new red.` + blank line), so it closes the
`## Round 58` section without editing a byte of it. Three `### <axis>` blocks, each holding
one full base evidence cell (the third cell of the axis-table row), quoted with a leading
`> ` so no line begins with `|` and the block is not a table row. Preamble: date
2026-10-27 (UTC; round 59 opened 2026-10-26 -03:00), provenance revision
`fd6303ce5c14b3f892dec586297a942ab6e4193b`, base counter path, and the 16-mismatch
decomposition (11 unresolved + 3 rows with no on-axis receipt + 2 rows with no tally).

## SECTION:

```markdown
## Superseded axis-table evidence (round 59)

Appended 2026-10-27 (UTC; round 59 opened 2026-10-26 -03:00), append-only. The three
evidence cells below are reproduced byte-for-byte from the axis table of
`SCORECARD.md` at `fd6303ce5c14b3f892dec586297a942ab6e4193b` (rows 17, 18, 19; third
cell of each row) because round 59's C1 claim (`calibration`) replaced those cells
instead of deleting the history. The frozen base counter
`python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root <lane> --revision fd6303ce5c14b3f892dec586297a942ab6e4193b`
exits 1 with `mismatches=16` (`controls/base-c1-axis-evidence.txt`), decomposed as
11 unresolved pointers + 3 rows with no on-axis receipt + 2 rows with no tally found
in a cited blob:

- operability — 4 unresolved pointers: `cli.mjs:935` ("not a committed path at the
  revision"), and `:836-839`, `:932`, `:393` ("line pointer with no preceding
  resolved file"); no on-axis round receipt; no tally.
- freshness — 7 unresolved pointers: `corpus/claims` ("not a committed path at the
  revision") and six `/tmp/kake-r17/` files — `scout-claims.md`, `claims-delta.tsv`,
  `critic.md`, `reviewer-cites.md`, `scout-pins.md`, `scout-live.md` ("absolute or
  home path (not committed bytes)"); no on-axis round receipt.
- calibration — 0 pointers at all (so none unresolved) and no tally anywhere in the
  cell; no on-axis round receipt.

The quoted cells are historical evidence, not current pointers: do not resolve them
against today's tree and do not count them as a live table row (each is quoted, so it
begins with `>` rather than `|`). Their byte-exactness is what the round-59 C1 counter
checks with `superseded_kept`.

### operability — base score 10, row 17, evidence cell 1060 bytes

> Every free-read verb in the domain is now **live-executed on the real repo with a byte-level write-free proof**: r11 closed probe/status/reconcile/sync-check; r12 closed the last 4 (`status --json` exit 0 with 5 violated+1 error in snapshot; `grokbots --check` exit 1 lucario; `bots list` exit 0 20 keepers; `bots report` exit 1 gaps) — 31-file state sha guard identical before/after, re-verified by 2 independent L2 re-runs. Exit-1 predicates pinned to code (gaps `cli.mjs:935`, stale-only-with-flag `:836-839`/`:932`, checked=21 `:393`); replica edge matrix (corrupt/deleted snapshot, registry faults, `--stale` variants) landed. The automation layer is now runtime-verified, not unit-file-trusted: keeper timer never fired (enable-vs-retire at L0), scribe push-gate failing (N1), lucario registry gap at L0. Corrected cmdProbe merge patch replica-verified and staged for the webzites owner (`corpus/handoffs/cmdProbe-merge-fix.md` — r11 F1 guard refuted on the `probe <id> --all` edge). Full verb free-read/writer classification (35 rows) code-verified.

### freshness — base score 10, row 18, evidence cell 1224 bytes

> **r17 HOLD 10:** the standing instrument caught a real between-sweep world change before prose repair: lowercase `~/projects` was consolidated into `~/Projects` and removed, making a cited descendant miss; cite corrected to the surviving canonical report, `pathsMissSet` 9→10. Full r16 inventory re-run: 160 claims (117/117 HOLD; 15/15 r16 stale repairs still correct; 7 carried UNVERIFIABLE; 21 HISTORICAL-OK) + 16/16 new claims HOLD; 9 new deltas found and resolved/qualified (W6 path+mtime/child rename, ETag edge flip, 2 r17 self-stale counts, inode wording, dangling `corpus/claims`, ledger locus, README range gloss). Instrument integrity also improved: `projectsChildrenSet` 36 informational set; `pathsFiles` count→39-entry evaluated list; bad pins now fail closed exit 2 with a permanent case (`--selftest` **10/10**). Final §paths = 66 targets / 49 resolve / 10 declared-absent / 0 drift / 39 files; 33-file state sha guard identical. Live exit 1 remains solely expected PQ-14 `plazir-live-source-gap`. Evidence: `corpus/knowledge/freshness-sweep.md` §r17, `corpus/lessons/round-17.md`, `LOG.md` r17, `/tmp/kake-r17/{scout-claims.md,claims-delta.tsv,critic.md,reviewer-cites.md,scout-pins.md,scout-live.md}`.

### calibration — base score 2, row 19, evidence cell 450 bytes

> Round-58 calibration move: the receipt-ledger counter's measured population had 19 post-commit receipt events with no ledger disclosures at base; at T1 it independently re-derived all 19 events, verified each note pointer/blob/kind, and found 0 undisclosed. This is a bounded calibration improvement (machine disclosure completeness, not a claim that every past run occurred); the new selftest and residual critic preserve the known note-truth limit.
```

## BYTE CHECK:

`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show fd6303ce5c14b3f892dec586297a942ab6e4193b:SCORECARD.md`
→ base blob (4410 lines); cells taken with the counter's own `axis_table()` splitting/stripping,
so the compared unit is exactly what `bc[2] in outside` tests. Check script and output are
scratch-only (`/fast/scratch/hyaku/kake-r59/ScribeC1Superseded/`), copied to
`.files/byte-check.out`.

```text
cmd: python3 -B <check built from the counter's own axis_table()/measure(), scratch only>
[1] each base evidence cell (third cell of the row, as the counter splits and strips it) present byte-exactly:
  operability  chars=1056 bytes=1060 occurrences=1 lines=[30] prefixed_with_quote_marker=True
  freshness    chars=1218 bytes=1224 occurrences=1 lines=[34] prefixed_with_quote_marker=True
  calibration  chars= 450 bytes= 450 occurrences=1 lines=[38] prefixed_with_quote_marker=True
[2] no line of the section starts with '|': none
[3] section lines: 38 bytes: 4629 single trailing newline: True
[4] counter 'outside' simulation (base table unchanged, section appended): table_span=(14, 19) rows=3 superseded_kept=3
[5] counter measure() at SIM (show() overridden for SCORECARD only; blobs read at base; NOT an after-state):
    mismatches=16 unresolved=11 rows_no_receipt=3 receipts_off_axis=0 tallies_unfound=0 rows_no_tally=2 rows=3 scores_held=2 superseded_kept=3 met=False
    per-row (axis, pointers, unresolved, tallies): [('operability', 5, 4, 0), ('freshness', 10, 7, 4), ('calibration', 0, 0, 0)]
```

Reading of the check (observed, not inferred): each cell occurs exactly once in the section,
on the line that starts with `> `, with no reflow inside the cell (single line per cell); no
section line starts with `|`; appending the section to the unchanged base table moves only
`superseded_kept` 0→3 while every other counter field is identical to
`controls/base-c1-axis-evidence.txt`. The `measure()` run at the synthetic revision `SIM` is a
byte-property check over synthetic text, not an after-state measurement: no after-state score
is claimed by this seat.

## DEAD POINTERS:

Resolved as dead at `fd6303c` by the frozen counter (quoted reasons verbatim from
`controls/base-c1-axis-evidence.txt`); each is listed with the axis whose cell carries it:

| Axis | Pointer | Why |
|---|---|---|
| operability | `cli.mjs:935` | not a committed path at the revision (the `cli.mjs` source tree is no longer in the lane) |
| operability | `:836-839` | line pointer with no preceding resolved file |
| operability | `:932` | line pointer with no preceding resolved file |
| operability | `:393` | line pointer with no preceding resolved file |
| freshness | `corpus/claims` | not a committed path at the revision |
| freshness | `/tmp/kake-r17/scout-claims.md` | absolute or home path (not committed bytes); `/tmp` is never citable |
| freshness | `/tmp/kake-r17/claims-delta.tsv` | absolute or home path (not committed bytes) |
| freshness | `/tmp/kake-r17/critic.md` | absolute or home path (not committed bytes) |
| freshness | `/tmp/kake-r17/reviewer-cites.md` | absolute or home path (not committed bytes) |
| freshness | `/tmp/kake-r17/scout-pins.md` | absolute or home path (not committed bytes) |
| freshness | `/tmp/kake-r17/scout-live.md` | absolute or home path (not committed bytes) |

The other five of the sixteen mismatches are not pointers: `rows_no_receipt=3` (all three
rows — their only resolved blobs, `corpus/handoffs/cmdProbe-merge-fix.md` for operability and
`corpus/knowledge/freshness-sweep.md`, `corpus/lessons/round-17.md`, `LOG.md` for freshness,
are not `.ufo/waves/round-N/` receipts, and calibration resolves nothing) and
`rows_no_tally=2` (operability and calibration; freshness's four tallies 117/117, 15/15,
16/16, 10/10 are all found in its cited blobs). Those four blobs were checked read-only with
`git cat-file -t` and are still `blob` at the base revision.

## Placement / integration note for the L1

- Append target `SCORECARD.md` is byte-identical between base `fd6303c` and lane HEAD
  `cb685273cc9e331b51f45485793d5d1c91184b3a` (`git diff --stat fd6303c HEAD -- SCORECARD.md`
  empty), so the quoted rows are still 17/18/19 and the section appends cleanly today.
- The base file has exactly two fence lines (145 and 154), both closed, so an EOF append
  cannot land inside a code fence.
- The section must stay outside the axis table (counter `outside` = everything but header
  line through last row) and must never be edited afterwards: the counter tests
  `bc[2] in outside`, i.e. one contiguous byte-identical copy per axis.

## Touched surfaces

- Read-only: lane `SCORECARD.md` blob at `fd6303c`, `.ufo/waves/round-59/c59_axis_evidence.py`,
  `contract.md` §Axis declaration/C1, `.ufo/waves/round-59/controls/base-c1-axis-evidence.txt`,
  read-only `git show/cat-file/log/diff`.
- Written: `/fast/scratch/hyaku/kake-r59/ScribeC1Superseded/{base_scorecard.md, cells.json,
  section.md, byte-check.out, check.out}`, then
  `.ufo/waves/round-59/w1/ScribeC1Superseded.files/{section.md, byte-check.out}` and this
  report. No product code, no counter, no judge, no git index, no jj state, no fleet repo.
- Scratch dir `/fast/scratch/hyaku/kake-r59/ScribeC1Superseded` removed after the report.

## Findings for wave 1 (no after-state claimed)

1. A quoted block with a `> ` prefix satisfies `bc[2] in outside` while remaining
   non-table; an indented (4-space) block would too. Fenced code would also, but the task
   named quoted/indented, and quoting keeps the section readable as prose history.
2. The three superseded cells cannot be resolved as live pointers (11 dead, 0 round
   receipts); any later reader/validator that re-resolves them will report the same 11
   dead pointers. That is the historical text, not a regression.
3. The calibration cell (450 bytes) carries no pointer and no `d/d` tally at all, so the
   repaired calibration row needs a receipt *and* a tally from elsewhere — the superseded
   block cannot supply either.
4. Residual limit of this seat: byte-exactness was proven against the `fd6303c` blob and a
   synthetic append; the real append must be re-verified after the L1 writes the new table,
   because `outside` then spans a different file (the guarantee, not the bytes, carries over).

VERDICT: Section drafted and byte-verified (3/3 cells exact, `> `-quoted, superseded_kept 0→3 on synthetic append); lane untouched.
