# ReviewRoutedItemsStatus — round-31 routed items not claimed in round 32

Seat: KakeR32.ReviewRoutedItemsStatus. Checked at lane tip
`285abcad632e3c1c57bb402232e7d218054db383` vs round-31 closure
`corpus/lessons/round-31-verifier-spotcheck.md` "Routed defects" (items 1, 3, 4,
6, 7; items 2 and 5 are this round's declared claims). Read-only checks over
committed bytes; no lane mutation. Sandbox /fast/scratch/hyaku/kake-r32/w1/ReviewRoutedItemsStatus/ unused (no writes needed).

## Status

1. **OPEN (defect standing; new counter partially conforms).** Item: any future
   containment counter must carry a benign hostile-named control. The round-32
   counter `.ufo/waves/round-32/c1_m3_probe.py` counts on exit codes
   (`killed` = mutant exit 1, line 95; `guard_ok` = pristine+benign exit 0,
   line 94), not runner-reported failure names; the hostile selftest still
   carries `h0-control` (citing_set_hostile_selftest.py:81), so the benign
   hostile-named control the item demanded is present in the counted path. The
   underlying disclosure — P6's kill rests on `reason_contains` reason text —
   is declared in SCORECARD round-32 and stays an open trust limit.

3. **OPEN (all four sub-items unrepaired).** Runner at `285abca` is
   byte-identical to round-31 tip: sha256 `7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969`
   (`git show 285abca:scripts/citing_set_selftest.py | sha256sum`; `git diff
   a0b0dff 285abca -- scripts/` touches only citing_set_hostile_selftest.py and
   the new P6 spec).
   - `read_expected` OSError still escapes: `os.fstat`/`handle.read` sit in the
     `try/finally` at selftest.py:405-414 with only the `os.open` wrapped
     (400-404); `run_case` catches `ValueError` only (542-545), so an OSError
     there propagates out of `main`'s per-case loop.
   - Fixture-root discovery still skips silently: `main` 692-696 keeps only
     symlinks and non-dot dirs; stray regular files, FIFOs, sockets at the
     fixture root are ignored with no note.
   - `GATE_VALUE_OPTIONS`/`GATE_OTHER_OPTIONS` (selftest.py:143-144) still
     hand-duplicate the gate parser table.
   - Symlink docstring wording unchanged (397).

4. **ADDRESSED for this round's claim; deferred by design.** Item: a
   truth-sampling step belongs in the next learning claim's declaration.
   Round-32 C2 is a retention claim, not a learning claim; its declaration
   explicitly discharges the routed item by checking byte identity via blob id
   "not by quote matching" (SCORECARD.md, "Truth step (routed item 4)").
   A future learning claim still owes the sampling step.

6. **ADDRESSED.** Guidance was "never cite seat transcripts as evidence; commit
   the needed excerpt." No new `history://` reference entered the lane this
   round: `git diff a0b0dff 285abca | grep 'history://'` → exit 1 (no match).
   The only live hit stays the round-31 report's own disclosure that the
   KakeR30 pointers do not resolve (`.ufo/reports/round-31/kake.md:34`); the
   MANIFEST.json hit is that lesson's text. No seat transcript is cited as
   round-32 evidence.

7. **OPEN.** Item: screen at least one non-primary candidate so the reject
   side has new decisions. `git ls-tree -r 285abca .ufo/waves/round-32/` holds
   no `screened/` receipts; `SOURCES.md` gained exactly one row this round,
   S062 (operator's own ds4cc-marketplace blobs, tier A, `mined`,
   SOURCES.md:70) — primary material, no screened non-primary candidate, no new
   reject decision. Row count 61 → 62 (grep -c '^| S0').

## Commands run

- `git log --oneline -5`; `git rev-parse HEAD` → tip `285abca` (exit 0).
- `git show 285abca:scripts/citing_set_selftest.py | sha256sum` → `7c95a18e…88969` (exit 0).
- `git diff --stat a0b0dff 285abca -- scripts/` → hostile selftest + P6 only (exit 0).
- `git ls-tree 285abca:scripts/fixtures/citing-set-hostile/` → P1…P6 (exit 0).
- `git diff a0b0dff 285abca | grep 'history://'` → no match (exit 1).
- `git show 285abca:corpus/SOURCES.md | grep -c '^| S0'` → 62; S062 row at :70.
- `git show 285abca:SCORECARD.md` (round-32 section) — declaration read.
- `git show 285abca:scripts/citing_set_hostile_selftest.py` — `h0-control` at
  :81, `reason_contains` key at :84,142-144,218.
- `git show 285abca:.ufo/waves/round-32/verification/c1-after-2f2f12d.json` —
  `killed 1`, `guard_ok true`, mutant fails P6 only.

## Not verified

- No counter or selftest was executed (status read from committed bytes and
  committed receipts only).
- Item 4's future obligation is untestable until a learning claim is declared.
- No live or local fetch of ds4cc-marketplace (out of scope for this item).

Tools installed/updated: none (pacman paused host-wide; none needed).
