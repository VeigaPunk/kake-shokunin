# ScribeRows — round-75 w1: `### Round 75 gate registry additions` (draft)

Seat: leaf scribe, read-only. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`; the item's base
revision `c9c5e484c533aa65f4374b841a3edcf572ed19a9`. Contract `.ufo/waves/round-75/contract.md`
§C1 read first and untouched; amendments 1–3 (`.ufo/waves/round-75/amendment-{1,2,3}.md`) landed in
the lane while this seat ran and are cited where they change a cell. No lane file was edited,
created, staged or committed by this seat; no `git`/`jj` mutation was run in the lane; nothing
outside `.ufo/waves/round-75/w1/ScribeRows.md` and the scratch tree was written.

Axes named before drafting: (a) **claim truth** — every number a cell records must re-derive under
the shipped counter, so a tally is only written after execution; (b) **supersession discipline** —
the old cells are never edited, and each new row names its predecessor and the class; (c) **pin
hygiene** — every control and path a cell cites exists at the landing revision and is the one that
actually carries the value; (d) **landing fit** — the section appends below the sidecar pin and its
rows parse as 8-cell table rows.

Scratch: `/fast/scratch/hyaku/kake-r75/ScribeRows` (`mkdir -p`; four `git clone --shared` trees,
their `--work` dirs and the two counters' selftest work dirs; removed before yield, §Scratch).

## Draft

Land the bytes **inside** the fence, unfenced in `SKILL.md`. The registry counters parse a row as a
line starting with `|` that carries at least six pipes inside a `### Round <N> gate registry
additions` section, so a fenced landing hides every row (round-74 precedent, and the round-70
fenced-line rule). Append after the current last line with one blank line before the heading; do not
touch any line ≤ 935.

````markdown
### Round 75 gate registry additions

Round 75 supersedes two rows the round-74 section landed and registers this round's instruments. The
section is appended at EOF (after line 1436 at `c9c5e484`), below line 935 — the largest `.line`
pinned for `SKILL.md` in `corpus/knowledge/freshness-sidecar.json` — so no pinned line moves; a
future row keeps this append-at-EOF discipline or re-points the sidecar pin in the same commit.
Effective row: rows are grouped by instrument file and the last row naming an instrument wins; a
superseded row is replaced by a new row that names its predecessor and the class, and the old cell is
never edited in place. The frozen population is contract §C1's 16 live instrument files at the
round-open revision `c9c5e484`; amendment 1 (`.ufo/waves/round-75/amendment-1.md`) makes that list a
floor, so a derived file beyond the 16 is in-population and must re-derive like the rest, and the
claim fails only when a frozen path disappears (`missing_frozen>0`). This section supersedes exactly
two of those rows — `c69_tmp_honour.py` (Kind demoted from `gate` to `instrument`, round-74 closure
R2: PROTOCOL §Gate self-test not met) and `c74_registry_gap.py` (Self-test cell corrected from five
to the eight fixtures the counter actually runs, round-74 closure R1) — and registers this round's
own two instruments, which are in-population by that clause. Withdrawal rule: a row goes when its
instrument leaves the tree; a superseded row is replaced by a new row that names its successor and
the class, and the old cell is never edited in place.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| c69_tmp_honour.py | instrument (live; no self-test mode — demoted from gate per round-74 closure R2: PROTOCOL §Gate self-test not met; its three terms are exercised by the base and after controls; supersedes the `gate (live)` row of the round-74 section for this file) | `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root <lane> --revision <rev> --work <scratch dir> [--baseline <rev>]` | `0=met` (`tmp_literals=0 selftest_under_tmpdir=true offline_unchanged=true`); `1=not met or runtime fault` (a failed `git show`, a missing `node`, or an absent sweep file raises a message and exits 1 — no separate fault code, named limitation); `2=usage` (argparse) | none (no self-test mode; `--selftest` is an argparse error, exit 2 — observed at `c9c5e484`: `the following arguments are required: --root, --revision, --work`; the counter's own three terms are exercised by the base and after controls, and its nested sweep `--selftest` is not a counter fixture suite) | predicate frozen `.ufo/waves/round-69/contract.md` section C2 plus Amendment 1 (`offline_exit=0` replaced by `offline_unchanged=true` against the frozen baseline); do-nothing control `.ufo/waves/round-69/controls/c2-base.txt` at `4d188f94` (`tmp_literals=2 selftest_under_tmpdir=false offline_unchanged=true`, exit 1); after `.ufo/waves/round-69/controls/c2-after-t1.txt` at `c182f579` (`tmp_literals=0 selftest_under_tmpdir=true offline_unchanged=true`, exit 0); the sweep side of the third term is pinned by `.ufo/waves/round-71/controls/sweep-offline-base.txt` and `.ufo/waves/round-71/controls/sweep-offline-after.txt` (both `DRIFT 1`, exit 1, unchanged); round-74 base `ced2878a` green; round-75 base `.ufo/waves/round-75/controls/base-c1-row-truth.txt` at `c9c5e484` carries the E1 finding this row removes, exit 1 | offline; materialises the revision tree with `git archive` under `--work`; runs `node scripts/freshness-sweep.mjs` in that tree; writes nothing outside `--work` | kake round 69 (counter by wave-1 seat ExecC2Fix; row by the L1 in round 74; Kind demoted and row superseded by the L1 in round 75) |
| c74_registry_gap.py | gate (live; offline over committed SKILL.md and counter-tree bytes; calibration: each of the eight counters the round-69 to round-73 contracts name has at least one gate-registry table row containing its exact filename, every such row's counter path resolves at the measured revision, and the round-74 section's own row names this counter; supersedes the round-74 row for this file, whose Self-test cell counted five) | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --root <lane> --revision <rev> [--json]` | `0=met` (`unregistered=0` and `own_row=true` and every population line `file_exit=0`); `1=not met`; `2=unevaluable` (unresolvable revision, unreadable `SKILL.md`, or a missing or renamed population counter file — never silently met); `64=usage` | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --selftest` → `selftest 8/8`, exit 0 (eight frozen fixtures: f1 an unregistered population counter is a finding; f2 a row naming a counter in a non-first cell counts as registered; f3 a prose-only mention does not count as a registry row; f4 a row whose entry-command path does not resolve fails conjunct 2; f5 a missing or renamed counter file is `unevaluable`, never silently met; f6 a table row inside a fenced code block is documentation, not a registry row; f7 a filename only in the Pinned-values cell does not register the counter; f8 a dump row naming two population counters in its credited cells credits none; the executed `FIXTURES` tuple is f1–f8, while the module docstring still says "builds the five contract fixtures f1-f5" and the `--selftest` help says "run contract fixtures f1-f5" — stale draft lines, so this cell takes its count from the observed `selftest 8/8`) | predicate frozen `.ufo/waves/round-74/contract.md` section C1; do-nothing control `.ufo/waves/round-74/controls/base-c1-registry.txt` at `ced2878a` (`population=8`, `c73_tmp_v3.py rows=1`, the seven other counters `rows=0`, `unregistered=7 met=false`, exit 1); after-state `.ufo/waves/round-74/controls/after-c1-registry-final.txt` (`unregistered=0 own_row=true met=true`, exit 0); round-75 re-derivation at `c9c5e484` in wave 1 reproduces `selftest 8/8`, exit 0 | read-only over committed bytes (`git show` and `git cat-file -e`); writes nothing; no network | kake round 74 (counter delivered by wave 1; row by the L1); Self-test cell superseded by the L1 in round 75 (round-74 closure R1) |
| .ufo/waves/round-75/c75_row_truth.py | gate (live; calibration: every live gate-registry row's claim re-derives by execution — E1 own self-test or a declared differential, E2 recorded tally, E3 fixture-id count, E4 path resolution over every live row — with the append-only conjunct and amendment 1's frozen floor, over the lane tree at `--revision`; amendment 2 A3 binds E1 and E2 to this instrument's own `--selftest`) | `python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision <rev> --base c9c5e484c533aa65f4374b841a3edcf572ed19a9 --work <scratch dir outside the lane> [--json]` | `0=met` (`mismatches=0`, `append_only=true` and `missing_frozen=0`; line `C1v1 revision=<rev> rows=N live=N files=F mismatches=0 classes=- append_only=true met=true missing_frozen=0`); `1=not met`; `2=unevaluable` (`--root` is not a repository toplevel, or `--revision` does not resolve); `64=usage` (missing `--work`, or argparse; `--emit-population` needs no `--work`) | `python3 -B .ufo/waves/round-75/c75_row_truth.py --selftest --work <dir>` → `C1v1 selftest fixtures=26 passed=26 failed=0` then `selftest 26/26`, exit 0 (fixture repositories under `--work`: one red and one green fixture per E-rule, a superseding-row fixture, a deleted base-row fixture, a relabelled-to-historical frozen-path fixture, the distinct fixture-id count, and the frozen-floor, emit-population and usage cases; observed 2026-11-03 at the wave's latest delivered bytes, and the landing commit re-runs it and corrects this count if the landed bytes differ — a tally that does not re-derive is an E2 finding) | predicate frozen `.ufo/waves/round-75/contract.md` section C1 with `.ufo/waves/round-75/amendment-1.md` A1 (the frozen 16 is a floor; `missing_frozen` is the conjunct) and `.ufo/waves/round-75/amendment-2.md` A3-A5 (own-instrument self-test, E4 over every live row); do-nothing control `.ufo/waves/round-75/controls/base-c1-row-truth.txt` at `c9c5e484` (`rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false`, exit 1); cheap-content control `.ufo/waves/round-75/controls/ctl-cheapcontent.txt` (`mismatches=2`, exit 1); deletion control `.ufo/waves/round-75/controls/ctl-deletion.txt` (`mismatches=2 append_only=false`, exit 1) | offline over committed bytes (`git show`, `git clone --shared` of `--root`); runs every recorded Self-test command inside that clone with a fresh `HOME` and `TMPDIR` under `--work` and inherited `GIT_*` scrubbed; writes only under `--work`; no network | kake round 75 (counter by wave-1 seat ExecC1Counter; row drafted by seat ScribeRows) |
| scripts/instrument_receipts.py | gate (live; operability: every live registry instrument is bound to a committed receipt carrying its sha256, byte length and static `--selftest` registration, and `--check` re-derives all three from the committed blob at the receipt's revision; population is the §C1 derivation with amendment 1's floor, so a live-row instrument beyond the frozen 16 is in-population) | `python3 -B scripts/instrument_receipts.py --root . --revision <rev> --check` (write mode `--write --date 2026-11-03`) | `0=met` (`bound` equal to `population`, `mismatches=0` and `missing_frozen=0`; line `C2v1 revision=<rev> population=<derived> bound=<derived> mismatches=0 met=true`); `1=not met` (includes a receipt that exists only in the working tree — amendment 3 A6 reads the receipt from committed bytes — and a declared revision that does not resolve or is not an ancestor of the measured revision, A7); `2=unevaluable`; `64=usage` (argparse, `--write` without `--date`, `--selftest` without `--work`) | `python3 -B scripts/instrument_receipts.py --selftest --work <dir>` → `selftest: 17/17`, exit 0 (isolated fixtures: a receipt committed after its revision, a receipt at another revision with a changed blob, the strict `--require-committed` pair, a fabricated 16-path receipt, a live row beyond the frozen 16, `missing_frozen=1` with `bound=16`, the static registration classifier over `add_argument` calls, comparisons, docstrings, argv lists and `.mjs` sources, and the usage exits; observed 2026-11-03 at the wave's latest delivered bytes, after five byte-states in the edit window, and the landing commit re-runs it and corrects this count if the landed bytes differ — a tally that does not re-derive is an E2 finding) | predicate frozen `.ufo/waves/round-75/contract.md` section C2 plus `.ufo/waves/round-75/amendment-1.md` A2; base control `.ufo/waves/round-75/controls/base-c2-receipts.txt` at `c9c5e484` (receipt `corpus/knowledge/instrument-receipts.json` absent, `population=16 bound=0 mismatches=16 met=false`, exit 1); receipt schema `instrument-receipts/v1` with `path`, `sha256`, `bytes`, `selftest_mode`; the fabricated-digest and dropped-path controls land under `.ufo/waves/round-75/controls/`; the delivered file sits in the wave tree and its Entry path resolves only from the commit that lands it at `scripts/` | `--check` reads committed blobs (`git show`) and writes nothing; `--write` writes only `corpus/knowledge/instrument-receipts.json`; `--selftest` writes only under `--work`; no network | kake round 75 (tool by wave-1 seat ExecC2Tool; row drafted by seat ScribeRows) |

**How to verify.** Run `python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision <rev> --base c9c5e484c533aa65f4374b841a3edcf572ed19a9 --work <scratch dir outside the lane>`; it must exit 0 with `mismatches=0`, `classes=-`, `append_only=true`, `met=true` and `missing_frozen=0`.
Expected after line: `C1v1 revision=<rev> rows=N live=N files=F mismatches=0 classes=- append_only=true met=true missing_frozen=0`, exit 0.
Base control: the same command at `c9c5e484` reproduces `.ufo/waves/round-75/controls/base-c1-row-truth.txt` — `rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false`, exit 1.

Run `python3 -B scripts/instrument_receipts.py --root . --revision <rev> --check`; it must exit 0 with `bound` equal to `population`, `mismatches=0` and `met=true`, and the receipt it reads must be committed at a revision that resolves and is an ancestor of the measured revision (amendment 3 A6/A7 — a receipt that exists only in the working tree is `met=false`).
Expected after line: `C2v1 revision=<rev> population=<derived> bound=<derived> mismatches=0 met=true`, exit 0.
Base control: the same command at `c9c5e484` reproduces `.ufo/waves/round-75/controls/base-c2-receipts.txt` — `population=16 bound=0 mismatches=16 met=false`, exit 1 (the receipt file is absent).
````

## Checks run

| # | Command (lane unless stated) | Exit | Observed |
|---|---|---|---|
| 1 | `mkdir -p /fast/scratch/hyaku/kake-r75/ScribeRows` | 0 | scratch created; no inherited `TMPDIR` used (every run set `TMPDIR` explicitly) |
| 2 | `git show c9c5e484:SKILL.md \| wc -l`; heading grep | 0 | `1436` lines; 10 sections matching `^### Round [0-9]+ gate registry additions` |
| 3 | `python3 -c` over `corpus/knowledge/freshness-sidecar.json`, `file == "SKILL.md"` | 0 | 25 pinned entries, largest `.line` = 935 (inside the prose paragraph at `SKILL.md:933-936`); an EOF append moves no pinned line |
| 4 | counter parser imported with `-B` over base `SKILL.md` | 0 | `rows 28 live 16 files 16` — equal to `controls/base-c1-row-truth.txt` |
| 5 | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --selftest --work <scratch>` | 0 | `selftest 8/8`; `FIXTURES` at `:491-492` is f1–f8 while the docstring (`:25`) and the `--selftest` help (`:536`) still say five / f1-f5 |
| 6 | `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --selftest` | 2 | `c69_tmp_honour.py: error: the following arguments are required: --root, --revision, --work` (no self-test mode) |
| 7 | `python3 -B .ufo/waves/round-75/w1/ExecC1Counter/c75_row_truth.py --selftest --work <scratch>` | 0 | `C1v1 selftest fixtures=19 passed=19 failed=0` at sha256 `5055230b…`; `fixtures=26 passed=26 failed=0` + `selftest 26/26` at `0699a672…` |
| 8 | `python3 -B .ufo/waves/round-75/w1/ExecC2Tool/instrument_receipts.py --selftest --work <scratch>` ×5 | 0,0,1,1,0 | totals 14 (`62b795ea…`), 15 (`8fbbb23b…`), 2 (`db128079…`), 4 (`a2005c6a…`), 17 (`162dd685…`) — the file was being written during the seat |
| 9 | scratch clone + counter, supersession rows only (`177a6103`, v0 counter) | 0 | `rows=30 live=18 files=16 mismatches=0 classes=- append_only=true met=true` |
| 10 | scratch clone, final draft, counter `0699a672` + tool `162dd685` (`7163e03e`) | 0 | `rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0` |
| 11 | scratch clone with row D but without `scripts/instrument_receipts.py` (`8ae1e83e`, v0 counter) | 1 | `mismatches=1 classes=E4 met=false`, finding `E4 path scripts/instrument_receipts.py does not resolve at …` |
| 12 | scratch clone `instrument_receipts.py --write --date 2026-11-03` then `--check` (`162dd685`) | 0/0 | write `population=18 missing_frozen=0`; check `C2v1 … population=18 bound=18 mismatches=0 met=true`, `receipt: source=committed`, `declared_valid=true`, `beyond_frozen=2` |
| 13 | lane, read-only: counter at landed `f1fc5d0a` and at tip `4e3fc159` | 0/0 | `rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0` at both |
| 14 | lane, read-only: `scripts/instrument_receipts.py --check` at `f1fc5d0a` and at `4e3fc159` | 1/0 | at `f1fc5d0a`: `population=18 bound=0 mismatches=18 met=false`, `receipt source=uncommitted`; at `4e3fc159`: `population=18 bound=18 mismatches=0 met=true`, `receipt source=committed declared=f1fc5d0a declared_valid=true` |
| 15 | `git cat-file -e HEAD:<path>` over the 15 non-instrument paths the draft cites | 0 | all 15 resolve at `9a9c4a6f`; the two instrument paths resolve from the commit that lands them |
| 16 | counter parser over the draft | 0 | 4 rows × 8 cells; c74 `fids=8`, pair `(8,8)`; c75 pair `(26,26)`; C2 pair `(17,17)`; c69 no command, 0 f-ids |

No tool install was needed, so the tooling authorization records nothing.

## Findings

1. **R1 is real and is a prose defect, not a counter defect.** `c74_registry_gap.py` executes eight
   fixtures (`FIXTURES`, `:491-492`) and prints `selftest 8/8`, exit 0 (check 5), while its docstring
   (`:25`) and its `--selftest` help (`:536`) still say five / `f1-f5`. The superseding cell records
   f1–f8 with the observed `8/8` and names both stale lines so the next reader does not "fix" the
   count back.
2. **R2 is real: `c69_tmp_honour.py` has no self-test mode.** `--selftest` exits 2 (check 6); at base
   its Kind still says `gate`, which is exactly the E1 finding the round-75 base control records.
   The demotion is a label change only: the counter's three terms still have no fixture suite, and
   the row says so instead of implying one exists.
3. **The freeze v0 counter and amendment 1 diverged.** `.ufo/waves/round-75/c75_row_truth.py` at
   `88f2e05f` has no `missing_frozen` term and no `--population` flag; amendment 1 requires both
   (`A1`), and the shipped counter prints `missing_frozen=N` at the end of the summary line and
   supports `--population`/`--emit-population`. The row therefore describes the shipped CLI, and its
   verdict map quotes the shipped line order (measured in check 10 and 13).
4. **The population grows to 18 and that is the amended rule, not a leak.** With the two new
   instrument rows the derived set is 18 files: `frozen=16`, `missing_frozen=0`, `beyond_frozen=2`
   (the two round-75 instruments), measured by both counters (checks 10, 12, 13, 14). Without
   amendment 1 the frozen kill-rule text ("differs from the 16") would have contradicted the
   contract's own after-state plan; the section's intro states the floor rule so a later reader does
   not mistake the growth for scope creep.
5. **Amendment 2 A3 is what makes the c74 row safe to keep as `gate`.** Its Self-test command names
   `c74_registry_gap.py` itself; had the cell run another file's self-test it would now be a finding
   whatever its exit code. Every drafted Self-test cell names its own instrument, and the c69 cell
   records `none`, so no cell borrows a green.
6. **The C2 tool was moving while this seat ran** (five byte-states, totals 14, 15, 2, 4, 17). The
   cell pins the last observed `17/17` and instructs the landing commit to re-run and correct it; a
   pinned count that no longer re-derives is exactly the defect class this round removes, and E2
   makes the staleness loud instead of silent.
7. **No round-70 control bears on `c69_tmp_honour.py`.** `grep -l 'sweep\|honour'
   .ufo/waves/round-70/controls/*` is empty; the sweep-side receipts are round-71's
   `controls/sweep-offline-base.txt` and `sweep-offline-after.txt` (both `DRIFT 1`, exit 1,
   unchanged). The row cites the round-69 counter receipts plus that round-71 pair and does not
   invent a round-70 pin.
8. **The lane already carries an assembled section** (commit `f1fc5d0a`, `SKILL.md` +19 lines) with
   the same four rows, and it is green: C1 `met=true` at `f1fc5d0a` and at `4e3fc159` (check 13).
   Its cells are a condensation of this draft: the Verdict maps are the bare code lists, the Write
   scope cells are the literal word `lane`, the Owner cells are `kake`, the c69 Pinned cell drops
   the round-71 sweep receipts and the round-75 base control, and the c74 Pinned cell drops the
   round-74 after-state receipt. Nothing in the landed text is false; the draft carries the pins
   that make each value traceable, which is what spliced rows can reuse.
9. **C2 at `f1fc5d0a` is red for a real reason and green one commit later.** At `f1fc5d0a` the
   receipt existed only in the worktree: `population=18 bound=0 mismatches=18 met=false`,
   `receipt source=uncommitted`, one finding per file (check 14) — amendment 3 A6 in action. At
   `4e3fc159` the same check is `bound=18 mismatches=0 met=true` with `declared=f1fc5d0a`,
   `declared_valid=true`.
10. **The section must land unfenced and below line 935.** The counters read `|`-leading lines
    outside fenced blocks only (check 4/16 parse the fence-free text); the sidecar's largest
    `SKILL.md` pin is line 935 (check 3), far above the new section's position.

## Landing notes for the L1

- Append after the last line with one blank line before the heading; leave every line ≤ 935 and every
  round-74 cell untouched — the two corrections are new rows, never in-place edits.
- Land `scripts/instrument_receipts.py` in the same commit as the section: its Entry path must
  resolve at the measured revision (E4 covers every live row, amendment 2 A4). A section that lands
  first is red — measured at `8ae1e83e`: `mismatches=1 classes=E4 met=false`, exit 1.
- Keep the two new instrument rows at `gate` only while each file's own `--selftest` exits 0, and
  keep the demoted `c69_tmp_honour.py` at `instrument` unless a self-test mode is added to it.
- Re-run `c75_row_truth.py --selftest` and `instrument_receipts.py --selftest` on the landed bytes
  and correct the two tallies in the Self-test cells (`26/26` and `17/17` were the last observed);
  E2 turns a stale pair into a finding rather than a silent falsehood.
- Run the two `How to verify` commands at the tip and paste the observed lines into the wave
  receipts; the expected shapes are in the block above.

## Out of scope / not done

- No lane production edit, no `SKILL.md` write, no commit/push/jj, no fetch, no tool install.
- The after-state receipts belong to the L1: the counters were run here read-only with `--work`
  outside the lane, and the receipt live in a scratch clone only — `corpus/knowledge/
  instrument-receipts.json` was not written by this seat.
- Nothing was measured about other lanes, other hosts, or later rounds; the c71/c70 `historical`
  rows are outside this item and were left alone.
- The C2 tool's A6/A7 implementation was observed but not audited; this seat reports its output,
  not its correctness.

## Scratch

`/fast/scratch/hyaku/kake-r75/ScribeRows` was created with `mkdir -p` and held four `git clone
--shared` trees (`sim-a`, `sim-final`, `sim-v2`, `sim-v3`), their `--work`/`--selftest` dirs and one
saved green copy of the C2 tool. Every fixture commit named `-C <clone>` and used a fixture identity
inside that clone only; `git -C <clone> rev-parse --show-toplevel` printed the clone's own root for
all four (verified before deletion). Removed with `rm -rf -- /fast/scratch/hyaku/kake-r75/ScribeRows`,
exit 0; `test -e` exit 1 afterwards. No tree of this seat remains under `/fast/scratch/hyaku/
kake-r75/`. If a later reader finds one, that is this seat's defect.
