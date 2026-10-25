# Simplifier — round 51, wave 1 (C1 wave ledger, C2 quote-truth)

Seat: `L1Kake51.SimplifierCounters-2`. Scope: dead code in
`.ufo/waves/round-51/c51_wave_ledger.py` (297 lines) and `.ufo/waves/round-51/c51_quote_truth.py`
(311 lines). Read-only: the committed files were never opened for write; every experiment ran on
`/tmp/sc51/` copies whose sha256 match the lane files
(`714c1017…60eba7c` ledger, `29a899a0…156f99f` quote-truth, re-checked after the run).

## Axes (named before measuring)

1. **Deletion mass** — lines and redundant operations removed.
2. **Predicate invariance** — `ledger_checks_passed` (0–3) and `conditions_passed` (0–8) must not
   move on any input, passing or failing.
3. **Contract preservation** — the frozen counting command's printed output must stay
   byte-identical; no condition may be weakened.

A deletion that improves axis 1 while moving axis 2 or 3 is a guard removal, not dead code, and
was rejected.

## Method

- Baselines reproduced at `9d13768c…`:
  - `c51_quote_truth.py` → `C2 quote-truth 8/8 met=True`, exit 0.
  - `c51_wave_ledger.py` → `C1 ledger 0/3 met=False`, exit 1 (wave evidence is not committed at
    the tip; this is the dispatch-time state, not a counter defect).
- C2 invariance was measured on the real repo plus seven scratch commits in a `/tmp` shared
  clone: the tip (8/8), and one commit each breaking C3 (`n1`, 7/8), C4 (`n2`, 7/8), C5 (`n3`,
  7/8), C6 (`n4`, 7/8), C7 (`n5`, 7/8), C8 (`n6`, 5/8), C1/C2 (`n7`, 6/8). For every variant the
  default stdout and the full `--json` document were compared byte-for-byte.
- C1 invariance could not be measured on committed evidence (none exists at the tip), so a
  synthetic but fully valid evidence repo was built in `/tmp`: settlement (3 seats, 2 reports,
  1 timeout-dead), dispatch payload, route map with one failing 403 route recorded as a
  deviation, three probe receipts, wave timing, time-accounting artifact, grant file, `LOG.md`
  naming the wall clock, and two `w1/*.md` reports. It scores `C1 ledger 3/3 met=True`, exit 0.
  Ten one-edit mutants of it then fail L1/L2/L3 in ten different ways (non-integer probe status,
  bad `settled_count`, missing grant, missing report, unparsable timing, unrecorded deviation,
  wrong spawn, wrong dead-seat duration, non-JSON probe, wrong `reports_written`). Each variant
  was run against all eleven fixtures and the lane tip.

## Deletion candidates found

| id | file | lines covered | deletion | predicate same? |
|----|------|---------------|----------|-----------------|
| D1 | `c51_wave_ledger.py` | 90 | `AttributeError` from `except (ValueError, AttributeError)` | **yes**, on all 11 fixtures + lane tip |
| D2 | `c51_wave_ledger.py` | 177–179 | duplicated integer-`httpStatus` assertion inside the used-route loop (lines 183–185 repeat it for every receipt, including used ones) | **yes**; only a duplicated diagnostic note collapses |
| D4 | `c51_quote_truth.py` | 142 | `"notes": list(notes)` → `"notes": notes` (the shallow copy guards nothing: `notes` is never appended to after C1) | **yes**, stdout and `--json` byte-identical on all 8 fixtures |
| D5 | `c51_quote_truth.py` | 292 | `"adopted": {sid: ADOPTED[sid] for sid in ADOPTED}` → `"adopted": ADOPTED` (identity copy of a dict built at module load and never mutated) | **yes**, byte-identical on all 8 fixtures |

### D1 — line 90, inert exception class

`parse_ts(value: str)` calls `value.replace(...)` and `datetime.fromisoformat(text)`; both call
sites pass `str(...)` (lines 218–219). `str.replace` cannot raise `AttributeError`, and
`fromisoformat(str)` raises `ValueError`. Probed inputs `''`, `'x'`, `'None'`, `'12345'`,
`'2026-13-01T00:00:00'`, `'2026-10-25T00:00:00Z'` all return `None` or a datetime with both
versions. Inert for every reachable input; no line saving.

### D2 — lines 177–179, duplicated assertion (kept)

```
177        status = receipt.get("httpStatus")
178        if not isinstance(status, int):
179            notes.append(f"probe receipt for {alias} carries no integer httpStatus")
```
When `receipts.get(alias)` is not `None` (line 173–176), that receipt is in `receipts`, so the
second loop (lines 182–185) re-applies the identical predicate and note. On the `m1` fixture the
original prints the note **twice** and the pruned copy once; the unique note set, the L2 verdict
(`2/3`, exit 1) and every other check are identical on all eleven fixtures and the lane tip.
3 lines saved. This is the only place where output is not byte-identical, and only on an already
failing input where the diagnostic was duplicated.

### D4 — line 142, redundant list copy (kept)

`notes` is appended to only in the C1 loop (lines 139–141) and read once at line 142; every later
condition uses its own `c*_notes` list. Dropping `list(...)` changes no bytes; verified on all
eight C2 fixtures (`8/8`, five `7/8`, `6/8`, `5/8`), default and `--json` identical.

### D5 — line 292, identity comprehension (kept)

`ADOPTED` is never mutated, so the comprehension produces an equal dict; `--json` output is
byte-identical on all eight fixtures.

### Combined kept set

Ledger `D1+D2`: 297 → **294 lines** (−3). Quote-truth `D4+D5`: 311 lines, two redundant
operations removed (line count unchanged). Predicate identical on: C1 — 11 fixtures + lane tip
(0/3 → 0/3); C2 — 8 fixtures (8/8, 7/8 ×5, 6/8, 5/8). No condition is weakened.

## Candidates examined and rejected (not dead)

| id | file | lines | why it is not deletable |
|----|------|-------|-------------------------|
| R1 | ledger | 128–129 | `settled_count + dead_count == len(seats)` is not in the frozen L1 sentence, but removing it flips fixture `m2` (settled_count=5) from `L1 FAIL` to `1/3` overall — a predicate change. It is a guard, not dead code. |
| R2 | ledger | 252–256 | Wave-grant check is also outside the frozen L3 sentence, but removing it flips `m3` (grant file deleted) from `2/3` to a pass. Guard. |
| R3 | quote-truth | 226–227 | The `receipts["sources"]` unwrap is **live**: the committed `sources/receipts.json` nests its two entries under `sources`, so deleting the unwrap turns the measured revision from `8/8` to `7/8` (C6 fails). Measured, not assumed. |
| R4 | quote-truth | 69–71 (`show`); 74–79 (`show_bytes`) | Re-implementing `show()` on `show_bytes()` dedups a subprocess shape but grows the 2-line body to 3 lines (311 → 311) and changes newline handling (`text=True` universal-newline translation vs raw decode). No win, one semantic delta. |
| R5 | both | ledger 31–32, quote 32–33 | Docstring exit contract is false, see below — a doc claim to fix, not code to delete. |

`facts` (ledger 115–123, 170, 221–226, plus the `facts` third element in the three returns, the
`dict` annotations at 97/145/200, eight `…, {}` early returns at 102/104/149/152/207/209/211/213
and lines 270–271) is **predicate-invariant** — removing it is 297 → 281 and leaves the default
counting output byte-identical on all eleven fixtures — but it is **not kept**: on a pass the
ledger prints only `L1 pass` + `L2 pass` + `L3 pass`, and `facts` is the only place the re-derived
seat counts, route counts and wall-clock/aggregate seconds are actually shown. The claim's title
is "re-derives the round's own seat accounting, route deviations and time accounting"; deleting
the re-derived numbers trades that auditability for 16 lines. Improves axis 1, harms axis 3.

Vulture 2.16 at `--min-confidence 60` and pyflakes 4.0.3 (run through `uvx`, not installed) report
nothing else: no unused imports, constants, functions or locals in either file. Both pruned
variants lint clean.

## Documentation claim that no condition needs

Both docstrings assert four exit codes; the code implements two:

- `ledger:31–32`, `quote_truth:32–33`: "2 the evidence cannot be evaluated, 64 usage error."
- Measured: usage error exits **2** (argparse), never 64; no path returns 2 for unevaluable
  evidence (`check_*` return `False` + notes, and `main` returns `0`/`1` only). So "2" is
  unreachable for its stated meaning and "64" is unreachable entirely.

Deletion candidate (documentation, not code): replace both lines with the true contract, e.g.
`Exit codes: 0 the predicate is met, 1 it is not, 2 usage error (argparse).` I did not apply it —
the files are frozen and out of my write scope.

## Adjacent observation (not a deletion)

`list_paths` (ledger 79–84) returns `[]` when `git ls-tree` fails, so an unreadable revision is
reported as "0 committed report files" (an L1 failure note) instead of the docstring's
"evidence cannot be evaluated" state. The counter never mistakes that for a pass, so the frozen
predicate is unaffected; it is the same conflation the false exit-code claim describes.

## Tools

Nothing installed. `uvx pyflakes 4.0.3` and `uvx vulture 2.16` were run transiently (uv cache);
no pacman, no `uv tool install`, no host change.

## Limits

- C1 invariance rests on a synthetic valid evidence repo plus ten single-edit mutants, because no
  wave evidence is committed at `9d13768c…` (ledger 0/3 at dispatch, as declared). The lane tip
  comparison shows the pruned ledger still prints `0/3`, byte-identical.
- The mutation fixtures are mine, not the round's; they exercise the branches the frozen
  conditions name (and the two guards R1/R2), not every conceivable settlement shape.
- Scratch (`/tmp/sc51/`, including `led_KEEP.py`, `led_P123.py`, `qt_Q3.py` and the eight
  fixture repos) is disposable and outside the lane; confirmed present at 03:46. Nothing here
  depends on it surviving a sweep: every deletion is specified in this report by original line
  range plus the literal replacement, so the changes are re-appliable without the scratch copy.
- My own report lands in `w1/`, so it is one of the committed seat reports the L1's
  `reports_written` / report-file ledger will count; it should be settled as this seat's report.
