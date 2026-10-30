# MutLedger — round-64 mutation test of the S432 ledger (C1)

Seat: MutLedger (leaf, no subagents). Claim attacked: C1 calibration, via the
ledger file `.ufo/waves/round-63/quote-class/quote-classes.json` as read by the
frozen counter `.ufo/waves/round-64/c64_calibration.py`
(sha256 `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`, verified
before and after the run; not edited). Measured revision T0 `4c8295fa`, base `1a481315`.

## Verdict

- **Frozen counter: 9/9 single-field ledger corruptions give `met=false`, exit 1.**
  Every one is named by the file-level pin: `pins=0 pin_drift=drift:ledger`.
  The control, unmutated ledger, gives `met=true`, exit 0, matching
  `controls/after-c1.txt` line for line (only the revision string differs).
- **Attack via a scratch copy of the counter with `LEDGER_SHA` re-pinned to the
  mutant bytes (the frozen constant is not touched): 5/10 killed, 5 survive.**
  Survivors are the row fields the counter never reads (see Finding 1). Under the
  frozen pin they are caught only because the whole file is pinned. This is a
  coverage gap, not a frozen-counter green: the frozen counter gives `met=false`
  for all of them. A survivor needs a counter edit (a re-pin), which the contract
  forbids.
- No mutant produced a traceback. No mutant produced `met=true` against the frozen
  counter.

## Mechanism of the frozen counter's ledger read (read, not assumed)

`c64_calibration.py` reads only these ledger fields:
- `classes` must be a list: line 140-141, `ledger_classes_not_list`.
- the row with `id == "S432"`, first match via `next(...)`: lines 142-146,
  `no_s432_row` / `ok`.
- `matchClass`: line 239.
- `locatedRawLines`: line 241.

It never reads `rawSha256`, `textSha256`, `rawPath`, `textPath` or `quote`. A grep
for those names finds no reads. The class check uses the constant `FROZEN_QUOTE`
(line 71-75, used at 237), not the row's `quote`.

The file-level pin is `LEDGER_SHA` at line 68 and `PIN_SHAS["ledger"]` at line 93;
the drift test is at line 207.

## Kill matrix

Commands (per fixture; `TMPDIR` set to scratch so the counter's `mkdtemp` stays out
of `/tmp`):

    TMPDIR=/fast/scratch/hyaku/kake-r64/MutLedger/tmp \
      python3 -B .ufo/waves/round-64/c64_calibration.py --root <fixture> --revision HEAD

Repin layer: a copy of the frozen counter in scratch with the line
`LEDGER_SHA = "5f48…"` replaced by the mutant's sha256, run the same way.

Fixtures are one-commit git repos under
`/fast/scratch/hyaku/kake-r64/MutLedger/fixtures/`. Each was checked with
`git -C <dir> rev-parse --show-toplevel` before its commit. The base files come from
`git archive 4c8295fa` of the nine S432-chain paths. The lane tree was not written.

| # | Mutation (ledger row / bytes) | Frozen counter | Repin attack |
|---|---|---|---|
| C0 | none (control) | met=true exit 0 | — |
| M1 | `rawSha256` last hex char `b`→`c` | exit 1, pin_drift=drift:ledger | **exit 0 met=true (survives)** |
| M2 | `textSha256` = sha256("") | exit 1, pin_drift=drift:ledger | **exit 0 met=true (survives)** |
| M3 | `matchClass` `collapsed-only`→`raw-substring` | exit 1, pin_drift=drift:ledger | exit 1, class_match=0 (killed) |
| M4 | `quote` U+2019 → U+0027 | exit 1, pin_drift=drift:ledger | **exit 0 met=true (survives)** |
| M5 | `locatedRawLines` `6150-6154`→`6150-6156` | exit 1, pin_drift=drift:ledger | exit 1, located=mismatch:6150-6154 class_match=0 (killed) |
| M6 | bogus `S999` row appended | exit 1, pin_drift=drift:ledger | **exit 0 met=true (survives)** |
| M6b | duplicate `S432` row, `raw-substring`, placed before the real one | exit 1, pin_drift=drift:ledger | exit 1, class_match=0 (killed: first-match picks the duplicate) |
| M6c | duplicate `S432` row, `raw-substring`, placed after the real one | exit 1, pin_drift=drift:ledger | **exit 0 met=true (survives: first-match picks the real row)** |
| M7 | `classes` replaced by an object, not a list | exit 1, pin_drift=drift:ledger | exit 1, ledger_state=ledger_classes_not_list (killed) |

Frozen-counter output, representative (M1; the other frozen rows differ only in the
revision and in the `ledger_state` label, see Finding 2):

    revision=afae2ff4… disagreements=1 pins=0 pin_drift=drift:ledger recipe_rederive=0
    ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable
    quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
    exit=1

Repin-layer output for M1 (survivor), in full:

    revision=afae2ff4… disagreements=1 pins=1 pin_drift=none recipe_rederive=1
    ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154
    quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
    exit=0

Repin-layer output for M7 (killed), in full:

    revision=9be0ddd9… disagreements=1 pins=1 pin_drift=none recipe_rederive=0
    ledger_state=ledger_classes_not_list derived=unevaluable class_match=0
    located=unevaluable quote_correction=1 criterion=1 lesson_gate=1 source_row=1
    unresolved=0 met=false
    exit=1

## Findings

**1. Ledger row fields are not bound (survivors under repin; frozen pin covers them).**
`rawSha256`, `textSha256`, `quote`, `rawPath` and `textPath` are never compared to
the pinned constants or to the blobs. The counter depends on the whole-file sha
(`LEDGER_SHA`, line 68) for all of them. Any future legitimate re-pin of the ledger
(a round-65 edit to the file, say, with a bumped constant) would accept a corrupt
`rawSha256` / `textSha256` / `quote` silently. A duplicate `S432` row placed after the
real row is also silently ignored. The fix would be to bind those fields to the
pinned sha constants and to the frozen quote in the counter. That is a counter edit,
so it is for a later round, not this one. Severity: latent coverage gap; the
frozen C1 verdict is not affected.

**2. Misleading `ledger_state` label on pin failure (diagnostic only).**
Line 220, `parse_ledger(blobs["ledger"] if pins else None)`, passes `None` whenever
any pin fails. `parse_ledger` then returns `ledger_absent` (line 136). So every
pin-failed run reports `ledger_state=ledger_absent` even when the ledger exists and
has drifted. The committed receipt `controls/control-ledger-mut.txt` shows this:
`pin_drift=drift:ledger ... ledger_state=ledger_absent`. The `pin_drift` field names
the true mechanism, so the kill is still correct; the `ledger_state` field is wrong
for that case.

**3. Frozen-counter kill mechanism is pin-only for every ledger corruption.**
Within the frozen counter, the class and located checks (lines 237-243) are never
reached by a ledger corruption, because the file pin fails first (line 221 gates
the recipe and class path on `pins`). So the "class/located mismatch" kill path
is only exercised by the re-pinned attack variant, not by the frozen counter itself.

## Scope and boundaries

- No files in the lane were written. The scratch tree
  `/fast/scratch/hyaku/kake-r64/MutLedger/` was deleted after this report was
  written (see the trailing command).
- Tools: none installed; the run used the system `python3` already present.
- Nothing in the frozen counter, controls, receipts, contract or lesson was
  edited.
- I did not attack the recipe, the S432 text or the spot-check; those belong to other
  seats.
