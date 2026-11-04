# MutationTesterC2 — round 75, wave w1

Seat: mutation tester (attack seat). Lane checkout read-only; every mutation ran in
scratch clones under `/fast/scratch/hyaku/kake-r75/MutationTesterC2/` (deleted before
yield). No lane file was edited; no git/jj mutation ran in the lane.

## 1. Targets and pinned bytes

| Target | sha256 | size | Provenance |
|---|---|---|---|
| C2 tool | `162dd6852cd5f6adbf278405365464f0b2f5c5d66100883a0974c32b0e6a68e7` | 48 856 B / 1153 lines | `.ufo/waves/round-75/w1/ExecC2Tool/instrument_receipts.py`; hash identical before and after the 43.8 s mutant run |
| C1 counter, frozen | `43538343c1f26e15a795f5486a6daca977c88ef5fa4458adacd2c68a00a596ce` | 10 405 B / 263 lines | `git show 88f2e05f:.ufo/waves/round-75/c75_row_truth.py` — the bytes the contract §C1 controls measured |
| C1 counter, hardened | `0699a672bc51311e4074ac17733b38954892d0b87084b7c9aa7b414f1716a501` | 45 406 B / 1016 lines | Lane working tree at measurement time (file replaced between 21:12 and 21:14 while this seat ran; `git status` shows the counter path modified/untracked under `w1/ExecC1Counter/`) |
| C1 counter, landed | `63e321b28e509781405f1b4209a66b99460bc2512c92a8615fec06f2423e944b` | 1051 lines | Landed by commit `abfbfaac` ("final C1 counter (29/29)"); identical to the lane working tree at report close; selftest 29/29 |

All three counter byte-sets are tested. The frozen set is the contract's instrument
and its mutants are what §C1's controls can be re-derived from; the two hardened sets
are successive lane states of the replacement the L1 will land. `[INFERENCE]` the
hardened file is the landed replacement; it is the only one present when this report
was written. The frozen set's mutants do not transfer to the hardened sets: the code
was rewritten, so `H-M*` was cut separately from each hardened snapshot.

The C2 tool also moved while this seat worked (observed `60312744…`, 1081 lines, then
`162dd685…`, 1153 lines). Every C2 verdict below is against `162dd685…`; the run
recorded the source hash before and after and they are equal.

## 2. Verdict summary

- **C2, 12 mutants:** 6 killed by the tool's own `--selftest` (17/17 green at base);
  **6 survived** it and are caught only by independent state probes:
  M3 (missing entry), M6 (worktree blob), M8 (unsorted write), M9 (no trailing
  newline), M10 (git fault reported met), M12 (one entry covering two paths).
- **C1 frozen, 7 mutants (+1 redundant variant):** no mutant flips the base verdict
  (`met=false` stays for all seven), so the contract's base measurement alone kills
  none. Five survive every check the controls apply — M1 (append-only, state C),
  M3 (E3, state A2), M5 (exit 0 without tally, state F), M6 (`differential` outside
  Kind, state A3), M7 (E1 skipped, state A3). M2 and M4 are caught only because they
  change a correct state (M2 turns a superseded-row green red, state G; M4 invents
  E2 findings, state E and the real base `mismatches=4`). The counter also has a
  predicate-level hole no mutant needed to create: E4 checks only the instrument
  file, not every `.py`/`.mjs` token.
- **C1 hardened, 8 mutants:** at snapshot `0699a672…` (26-case selftest) 5 killed,
  **3 survived**: H-M4 (tally from the whole cell), H-M5 (exit 0 without tally), H-M6
  (`differential` outside Kind). At the **landed** bytes `63e321b2…` (29-case
  selftest, commit `abfbfaac`) H-M6 is killed by the new f22 fixture; **H-M4 and
  H-M5 still survive**, and the Verdict-cell placement of the H-M6 defect still
  greens a state f22 does not cover.

No baseline failure was treated as a kill: every state set was first run with the
pristine instrument and the pristine verdict is recorded beside each mutant verdict.

## 3. Method and command log

C2 probes are commits in a `git clone --shared` of the lane at
`c9c5e484c533aa65f4374b841a3edcf572ed19a9`; every receipt is committed (the landed
tool reads committed bytes only), declares the base commit as its revision (an
ancestor of every carrier commit), and the worktree is pinned per state. A mutant
*runs the tool's `--selftest` first* (case-level parsing) and is then probed on 12
states whose correct verdicts are the pristine tool's verdicts. A mutant survives
when the selftest is green and a state that should be red reports `met=true`, or a
green state's `bound`/`population` moves.

C1 runs the counter twice: on the real lane base (`--root <lane> --revision
c9c5e484… --base c9c5e484…`, 16 files, ~29 s per run) and on a fixture registry with
one live row per predicate dimension (states A/B/A2/A3/C/E/F/G/H, §5).

| Command (scratch paths abbreviated) | Exit | Observed |
|---|---|---|
| frozen counter, real base | 1 | `rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false` — reproduces `controls/base-c1-row-truth.txt` |
| hardened counter, real base | 1 | `mismatches=2 classes=E1 E3 append_only=true met=false missing_frozen=0` — same control |
| frozen counter `--selftest` | 2 | `error: unrecognized arguments: --selftest` (no self-test mode) |
| hardened counter `--selftest` (`0699a672…`) | 0 | `C1v1 selftest fixtures=26 passed=26 failed=0` |
| hardened counter `--selftest` (`63e321b2…`) | 0 | `selftest 29/29` |
| C2 tool `--selftest` (pinned bytes) | 0 | `selftest: 17/17` |
| C2 tool `--check` on base clone (no receipt) | 1 | `population=16 bound=0 mismatches=16 met=false` |
| `mutc1.py` (frozen source via `C75=`), 9 states × 8 mutants | 0 | matrix §5 |
| `c1real.py`, 8 mutants on the real base | 0 | table §5.1 (257 s) |
| `mutc2_real.py`, 12 states × 12 mutants | 0 | table §4 (44 s) |
| `mutc1_hard.py`, 8 mutants, `0699a672…` | 0 | table §6 |
| `mutc1_hard.py`, 8 mutants, `63e321b2…` (`C1HARD=`) | 0 | table §6.2 |
| `c1hard_states.py`, 3 states, both hardened byte-sets | 0 | S1/S2/S3 §6.1 |

No tool was installed or upgraded; nothing was changed in any PATH directory.

## 4. C2 — landed tool (`162dd685…`)

### 4.1 Pristine state grid (16-file population at base)

| State | Correct verdict (pristine) | What it is |
|---|---|---|
| `good` | exit 0, `bound=16 met=true` | receipt written and committed by the tool |
| `fab_digest` | exit 1, `bound=15` | one entry's sha256 replaced with zeros, bytes correct |
| `fab_bytes` | exit 1, `bound=15` | one entry's `bytes` +7, digest correct |
| `mode_false` / `mode_true` | exit 1, `bound=15` | a `selftest_mode` flipped either way |
| `missing` | exit 1, `bound=15` | one entry deleted (contract control (2)) |
| `outside` | exit 0, `bound=16`, `outside:` line | extra entry for a path outside the population |
| `duplicate` | exit 1, `bound=15` | same path twice, bad entry first |
| `combined` | exit 1, `bound=14` | one entry names two population paths |
| `dirty` | exit 1, `bound=15` | receipt records the working-tree bytes; the committed blob differs |
| `stale` | exit 1, `bound=15` | receipt pins base; a population blob moved in a later commit |
| `fault` | exit 2, no verdict line | unresolvable revision |

### 4.2 Mutants

| id | mutation (pinned line) | tool `--selftest` | probe result | verdict |
|---|---|---|---|---|
| C2-M1 | skip digest compare — `if False and entry["sha256"] != digest:` (:518) | FAIL 3 cases | `fab_digest` green | killed |
| C2-M2 | integrity = byte length, digest ignored (:518/523) | FAIL 2 cases (`wrong digest`, `wrong byte count`) | `fab_digest` green | killed |
| C2-M3 | missing entry increments `bound` (:488) | **pass 17/17** | `missing` and `combined` → `bound=16 met=true` | **SURVIVED** |
| C2-M4 | outside paths added to `bound` (:479) | FAIL `path outside population` | `outside` → `bound=17` | killed |
| C2-M5 | `selftest_mode` forced true (:514) | FAIL 10 cases | green state `bound=14` | killed |
| C2-M6 | population blobs read from the worktree (:227) | **pass 17/17** | `dirty` and `stale` → `bound=16 met=true` | **SURVIVED** |
| C2-M7 | blobs derived at the declared revision (:480) | FAIL `declared revision…changed blob` | `stale` green | killed |
| C2-M8 | receipt written in reverse path order (:608) | **pass 17/17** | write probe `sorted=false` | **SURVIVED** (selftest hole) |
| C2-M9 | trailing newline dropped (:635) | **pass 17/17** | write probe `newline=false` | **SURVIVED** (selftest hole) |
| C2-M10 | `Unevaluable` path prints `met=true`, exit 0 (:1147) | **pass 17/17** | `fault` → exit 0, `met=true` | **SURVIVED** |
| C2-M11 | duplicate path dropped, last entry wins (:475) | FAIL `duplicate path` | `duplicate` green | killed |
| C2-M12 | entry path split on `,`, both parts credited (:475) | **pass 17/17** | `combined` → `bound=16 met=true` | **SURVIVED** |

The tool's selftest coverage is strong on the dimensions the contract names (digest,
bytes, mode, duplicate, outside, declared-revision ancestry, missing receipt,
fabricated receipt, frozen floor) and blind on the six dimensions above.

### 4.3 Survivors — the check each defeats and a proposed kill

- **C2-M3** (`entry = entries.get(path); if entry is None: bound += 1; continue`).
  Defeats: the receipt-omits-a-path control named in contract §C2 ("a receipt that
  drops one path → bound=15") — the selftest has no such case, only the absent
  *receipt* case. Kill: add the dropped-entry fixture (write, delete one entry,
  expect `bound=15 mismatches=1 met=false`).
- **C2-M6** (worktree overlay in `read_population_blobs`). Defeats: blob provenance.
  The selftest has no uncommitted-edit case; a receipt written against a dirty
  working tree binds. Kill: commit blob X, edit the worktree to Y, commit a receipt
  recording Y for one path, expect `class=digest bound=15` at the carrier commit.
- **C2-M8 / C2-M9** (unsorted files, missing newline). Defeat: the write-format
  promise in the tool's own docstring; the green case compares two writes for
  equality only. Kill: in the green case, assert `files == sorted(paths)` and
  `raw.endswith(b"\n")` and ASCII-only bytes.
- **C2-M10** (`except Unevaluable: print(… met=true); return 0`). Defeats: the
  "never silently met" rule for faults. The selftest checks `check()` at the function
  level, not `main`'s exit code. Kill: run the CLI at an unresolvable revision and
  assert exit 2 and no `met=true` in stdout.
- **C2-M12** (combined path split and credited). Defeats: one-entry-per-file binding.
  Kill: receipt with one entry `"a.py, b.py"` and both real entries removed, expect
  `bound=14 mismatches=2`.

## 5. C1 — frozen counter (`43538343…`)

### 5.1 Real lane base (16 files)

| Run | Exit | mismatches | classes | met |
|---|---|---|---|---|
| pristine | 1 | 2 | `E1 E3` | false |
| C1-M1 (append-only block removed) | 1 | 2 | `E1 E3` | false |
| C1-M1b (append-only dropped from `met` only) | 1 | 2 | `E1 E3` | false |
| C1-M2 (first row wins) | 1 | 2 | `E1 E3` | false |
| C1-M3 (E3 ignored) | 1 | 1 | `E1` | false |
| C1-M4 (tally from whole row) | 1 | 4 | `E1 E2 E3` | false |
| C1-M5 (no-tally accepted) | 1 | 2 | `E1 E3` | false |
| C1-M6 (`differential` anywhere) | 1 | 2 | `E1 E3` | false |
| C1-M7 (E1 skipped) | 1 | 1 | `E3` | false |

The base state alone kills none of the seven (met never flips) and mis-scores M4
(two invented E2 findings — a false red that would block a correct after-state).
All mutants remain subclasses of the same base defect pair.

### 5.2 Fixture registry matrix

Rows: one live row per dimension; `--base` is state A's commit throughout.

| State | What it is | Pristine | Mutants that diverge |
|---|---|---|---|
| A | base: gate without self-test (E1) + 3 ids vs 2/2 (E3) | red 2 `E1 E3` | M3→1, M7→1 (still red) |
| B | both rows superseded honestly | green | — |
| A2 | E3 only (a.py superseded, b.py still enumerates f1 f2 f3) | red 1 `E3` | **M3 → `met=true`** |
| A3 | E1 only; `differential` in the Verdict cell, Kind is `gate` | red 1 `E1` | **M6 → `met=true`**, **M7 → `met=true`** |
| C | B minus the c.py row (mismatches=0, append_only=false) | red, `append_only=false` | **M1 → `met=true`** |
| E | green, with a pinned `4/4` tally outside the Self-test cell | green | M4 → red (false positive) |
| F | gate claims `selftest 2/2`; command exits 0 printing no tally | red 1 `E2` | **M5 → `met=true`**, M4 → 2 findings |
| G | superseded bad row before its good replacement | green | M2 → red (false positive) |
| H | instrument resolves; Pinned cell names a dead `.py` token | **green** | none (all inherit the hole) |

### 5.3 Survivors — exact mutant, defeated check, proposed kill

- **C1-M1** — delete the `if args.base:` block and its finding (`:241`). Defeats the
  append-only conjunct: on a state where every E1–E4 claim holds and one base row is
  deleted, the mutant reports `mismatches=0 met=true`. The contract's deletion
  control does not isolate this (its deletion state still carries two findings), so
  the base measurement cannot kill M1. Kill: a `--selftest` state with a deleted base
  row and zero predicate findings, asserting `append_only=false met=false`.
- **C1-M3** — `ids = set()` (`:202`). Defeats E3: a row enumerating `f1 f2 f3` against
  an observed total of 2 passes. Kill: E3-only fixture.
- **C1-M5** — drop the `elif pair and not obs:` branch (`:198`). Defeats E2: a row
  claiming `2/2` whose command exits 0 without printing a tally passes. Kill: the F
  fixture.
- **C1-M6** — `'differential' not in ' '.join(row['cells'])` (`:183`). Defeats E1's
  "Kind cell declares" rule: a `gate` row that mentions `differential` in its Verdict
  cell is exempted. Kill: the A3 fixture.
- **C1-M7** — `if fam == 'gate' and False:` (`:181`). Defeats E1 entirely. Kill: the
  A3 fixture (or A).
- **C1-M2** — `row = groups[f][0]` (`:162`). Does not miss a red state, but turns a
  correct after-state red because a superseded row stays effective. Kill: the G
  fixture.
- **C1-M4** — `claim_pair(' '.join(row['cells']))` (`:193`). Invents E2 findings from
  receipt-history/pinned values (2 extra on the real base; false red on state E).
  Kill: the E fixture.
- **Counter-level E4 hole (no mutant needed).** The frozen counter's E4 checks only
  the effective instrument path (`git cat-file -e rev:<instrument>`), while contract
  §C1 requires every `.py`/`.mjs` token in the row's cells to resolve. State H — a
  row whose Pinned cell names a dead `.py` token while the instrument resolves — is
  reported **green** by the pristine frozen counter. Kill: resolve every token of
  every live row (the hardened counter already does; its fixtures f09/f19 cover it).
  Note M1b is inert: dropping `append_only` from the `met` expression alone changes
  nothing because the append-only finding already keeps `met=false`; the conjunct and
  the finding are double-guarded.

## 6. C1 — hardened counter (snapshot `0699a672…`, landed `63e321b2…`)

Snapshot `0699a672…`: `--selftest` 26/26, exit 0; real base `mismatches=2 classes=E1
E3 append_only=true met=false missing_frozen=0`, exit 1. The hardened counter closes
the frozen counter's E4 hole and the E1 command-binding hole. The landed bytes
`63e321b2…` pass 29/29 and are tabled in §6.2.

| id | mutation | selftest | verdict |
|---|---|---|---|
| H-M1 | append-only block disabled | FAIL f11 | killed |
| H-M2 | first row wins | FAIL f10 | killed |
| H-M3 | E3 ignored | FAIL f05 | killed |
| H-M4 | tally parsed from the whole cell, not the claim segment (`:307`) | **pass 26/26** | **SURVIVED** |
| H-M5 | exit 0 without the claimed tally accepted (`:439`) | **pass 26/26** | **SURVIVED** |
| H-M6 | `differential` searched in every cell (`:385`) | **pass 26/26** | **SURVIVED** |
| H-M7 | E1 skipped | FAIL f01/f16 | killed |
| H-M8 | E4 only on the instrument file | FAIL f09/f19 | killed |

### 6.1 Demonstrated survivor states (pristine vs mutant, same commit)

| State | Pristine | H-M5 | H-M6 | H-M4 |
|---|---|---|---|---|
| S1 `no_tally`: gate claims `selftest 2/2`, command exits 0 with no tally | `mismatches=1 classes=E2 met=false` | **`mismatches=0 met=true`** | same as pristine | same as pristine |
| S2 `differential_outside_kind`: word only in the Verdict cell | `classes=E1 met=false` | same | **`mismatches=0 met=true`** | same |
| S3 `history_pair`: claim segment `3/3`, receipt-history `9/9` after `;` | `mismatches=0 met=true` | same | same | **`classes=E2 met=false`** |

Proposed kills for `0699a672…`: add S1, S2 and S3 as `_selftest_cases` entries —
the three classes the 26-case suite omits among the seat's mutant list.

### 6.2 Landed bytes (`63e321b2…`, 1051 lines, selftest 29/29, commit `abfbfaac`)

| id | mutation | selftest | verdict |
|---|---|---|---|
| H-M1 | append-only block disabled | FAIL f11 | killed |
| H-M2 | first row wins | FAIL f10 | killed |
| H-M3 | E3 ignored | FAIL f05 | killed |
| H-M4 | tally parsed from the whole cell | **pass 29/29** | **SURVIVED** (S3 still red under the mutant) |
| H-M5 | exit 0 without the claimed tally accepted | **pass 29/29** | **SURVIVED** (S1 still green under the mutant) |
| H-M6 | `differential` searched in every cell | FAIL f22 | killed |
| H-M7 | E1 skipped | FAIL f01/f18/f22 | killed |
| H-M8 | E4 only on the instrument file | FAIL f09/f19 | killed |

H-M6 is now killed, but the killing fixture f22 places the word in the Pinned cell
only. The S2 state places it in the Verdict cell and still reports
`mismatches=0 met=true` under H-M6 (pristine: `classes=E1 met=false`), so the
exemption search remains position-sensitive: a row with the word only in the Verdict
cell would be laundered by the mutant. Proposed kill: one row per non-Kind cell
position, or a single row carrying the word in the Verdict, Self-test and Pinned
cells.

## 7. Routed items (next round)

1. C2 selftest: dropped-entry case (M3), uncommitted-edit case (M6), write-format
   assertions (M8/M9), CLI-level fault case (M10), combined-path case (M12).
2. C1: the frozen counter is superseded by the landed `63e321b2…`; if the frozen
   bytes are ever measured again, add the A2/A3/C/E/F/G fixtures as `--selftest`
   cases. The landed counter must be the one the round's controls are re-derived
   with — the control in `controls/base-c1-row-truth.txt` was produced by
   `43538343…`, not by the landed file.
3. C1 hardened: S1 (no-tally) and S3 (history pair) cases; extend f22 to the Verdict
   cell (the Pinned-cell placement alone leaves the H-M6 class live).
4. Contract-level note: the frozen E4 sentence is stronger than the frozen counter's
   implementation; if `43538343…` lands, the claim's E4 term is under-measured.

## 8. Evidence index (all under `.ufo/waves/round-75/w1/MutC2/`)

- `c1/C1-M*.py` — 8 frozen-counter mutants; `c1-frozen/c75_row_truth.py` — the
  frozen source they were cut from.
- `c1-hard/H-M*.py` — 8 hardened-counter mutants at `0699a672…`;
  `c1-hard/pristine-c75_hard.py`.
- `c1-hard-latest/H-M*.py` — the same 8 mutants re-cut at `63e321b2…`;
  `c1-hard-latest/pristine-c75_hard_63e321b2.py`.
- `c2/C2-M*.py` — 12 landed-tool mutants; `c2/pristine-instrument_receipts.py`.
- `harness/` — `mutc1.py`, `c1real.py`, `mutc1_hard.py`, `c1hard_states.py`,
  `mutc2_real.py`, plus `harness/ref/instrument_receipts.py` (contract-spec reference
  implementation used while the executor's tool was absent; its own 12 mutants are in
  `results/c2mut-results.json`).
- `results/` — `c1mut-results.json` (fixture matrix), `c1real-results.json` (real
  base), `c1hard-results.json`, `c1hard-states.json`, `c2real-results.json`,
  `receipts/<state>.json` (the 11 committed receipt states probed).

Scratch tree `/fast/scratch/hyaku/kake-r75/MutationTesterC2/` was removed after these
artifacts were copied; no scratch tree is left on disk.
