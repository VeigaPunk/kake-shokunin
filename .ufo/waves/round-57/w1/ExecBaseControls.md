# ExecBaseControls

Seat: W1 base-control replication for round-57 C1/C2/C3. Read-only over the lane; no lane file, index, or jj state touched.
Environment: python3 3.14.8, git 2.56.0, host loaded (every run given a long timeout; no retries).
Clones (both `git clone --no-checkout` from `/home/vgpnk/Projects/shokunin/kake-shokunin`, then `checkout -q`):
- `$D=/tmp/execbasecontrols.5oFArU` at contract commit `b9a5d012f7fd7190bf4d4c6e4d79e9462a6471af` (HEAD of `$D` = contract commit).
- `$E=/tmp/execbasecontrols-head.AhAMwp` at `f7c98ff269286723077848f3caf1422c4004f46d` (dispatch commit; only used for the `--fleet` variant, see DIFFS 2).
All counters run with `-B`. Raw outputs kept in `$D/out/` (scratch only, not part of the lane).

COMMANDS:

1. `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root /tmp/execbasecontrols.5oFArU --revision 28fa0b23e699303725aba2727094531f5e44494d` — cwd `$D`, exit **1**
   first 3:
   ```
   C1 receipt-pins undisclosed_relabels=6 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False  (met: undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1)
     population=45 relabels_in_history=6
     UNDISCLOSED .ufo/waves/round-52/control/c1-ledger-real.txt 3a50ae4321e6 -> 1ae8de5d4dee at a4a890cf1381
   ```
   last 3:
   ```
     UNDISCLOSED .ufo/waves/round-56/controls/after-c1-selftally.txt f8438a282d59 -> 4cb225fb032b at ad06cb8a17bd
     UNDISCLOSED .ufo/waves/round-56/controls/after-c2-quote-truth.txt f8438a282d59 -> 4cb225fb032b at ad06cb8a17bd
     revision: 28fa0b23e699303725aba2727094531f5e44494d
   ```

2. `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root /tmp/execbasecontrols.5oFArU --revision HEAD` — cwd `$D`, exit **1**
   first 3: same predicate line as (1); `  population=50 relabels_in_history=6`; first UNDISCLOSED line identical.
   last 3:
   ```
     UNDISCLOSED .ufo/waves/round-56/controls/after-c1-selftally.txt f8438a282d59 -> 4cb225fb032b at ad06cb8a17bd
     UNDISCLOSED .ufo/waves/round-56/controls/after-c2-quote-truth.txt f8438a282d59 -> 4cb225fb032b at ad06cb8a17bd
     revision: b9a5d012f7fd7190bf4d4c6e4d79e9462a6471af
   ```

3. `python3 -B .ufo/waves/round-57/c57_quote_truth.py --root /tmp/execbasecontrols.5oFArU --revision 28fa0b23e699303725aba2727094531f5e44494d` — cwd `$D`, exit **1** (26 output lines)
   first 3:
   ```
   C3 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)
     C1_entries_exist FAIL
       - S421: knowledge entry corpus/knowledge/baidu-dead-link-types.md absent at the measured revision
   ```
   last 3:
   ```
       - mirror .ufo/waves/round-57/assimilation/pre-append/corpus/SOURCES.md absent at the measured revision
     revision: 28fa0b23e699303725aba2727094531f5e44494d
   EXIT=1
   ```
   (the trailing `EXIT=1` is printed by the counter itself, `c57_quote_truth.py:627`)

4. `python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root /tmp/execbasecontrols.5oFArU --revision 28fa0b23e699303725aba2727094531f5e44494d --fleet /home/vgpnk/Projects/shokunin` — cwd `$D`, exit **64**
   entire output (2 lines):
   ```
   usage: c57_idresolver_gate.py [-h] [--root ROOT] [--revision REVISION]
   c57_idresolver_gate.py: error: unrecognized arguments: --fleet /home/vgpnk/Projects/shokunin
   ```
   The gate at the contract commit has no `--fleet` option (see DIFFS 2). Same argv re-run in `$E` (f7c98ff) reproduces the v1.1 control:

5. `python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root /tmp/execbasecontrols-head.AhAMwp --revision 28fa0b23e699303725aba2727094531f5e44494d --fleet /home/vgpnk/Projects/shokunin` — cwd `$E`, exit **1**
   first 3:
   ```
   C2 id-resolver 0/5 met=False  (met: gate_conditions_passed == 5 of 5)
     G1_tool_present FAIL
       - scripts/id_resolver.py absent at 28fa0b23e699
   ```
   last 3:
   ```
     G5_green FAIL
       - tool absent
     revision: 28fa0b23e699303725aba2727094531f5e44494d
   ```

6. `python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root /tmp/execbasecontrols.5oFArU --revision 28fa0b23e699303725aba2727094531f5e44494d` (no `--fleet`, contract commit) — exit **1**; output byte-identical to (5), 12 lines.

7. `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --selftest` — cwd `$D`, exit **0** (20 output lines)
   first 3:
   ```
   PASS honest, no relabel: met=True undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1
   PASS old relabel undisclosed: met=False undisclosed_relabels=1 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1
   PASS old relabel disclosed with matching errata: met=True undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1
   ```
   last 3:
   ```
   PASS pin line stripped later counts as relabel: met=False undisclosed_relabels=1 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0
   PASS round outside 52-57 is out of population: met=True undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1
   c57 receipt-pins selftest: 19/19
   ```

8. Usage/unevaluable matrix, cwd `$D`, `--root $D` for every line (fleet-variant gate run in `$E`):
   - `c57_receipt_pins.py` (no `--revision`): exit **64**, stderr `usage: --root <lane> --revision <rev> | --selftest`
   - `c57_idresolver_gate.py` (no `--revision`): exit **64**, stderr `usage: --root <lane> --revision <rev>`
   - `c57_quote_truth.py` (no `--revision`): exit **64**, stderr `usage: --revision is required unless --selftest is used`
   - `c57_receipt_pins.py --revision deadbeef`: exit **2**, output `C1 receipt-pins unevaluable: git rev-parse --verify deadbeef^{commit}: fatal: Needed a single revision`
   - `c57_idresolver_gate.py --revision deadbeef`: exit **2**, output `C2 id-resolver-gate unevaluable: revision deadbeef unresolved`
   - `c57_quote_truth.py --revision deadbeef`: exit **2**, output `unevaluable: revision 'deadbeef' does not resolve in '/tmp/execbasecontrols.5oFArU'` then `EXIT=2`
   - `$E` fleet-variant gate (no `--revision`): exit **64**; with `--revision deadbeef`: exit **2**, `C2 id-resolver-gate unevaluable: revision deadbeef unresolved`

DIFFS:

1. `c57_receipt_pins.py --revision 28fa0b23…` vs `controls/base-c1-receipt-pins.txt`: **byte-identical** (`diff -u` empty; control = counter stdout + capture line `EXIT=1`). Zero drift.
2. `c57_idresolver_gate.py` — **argv mismatch at the contract commit.** At `b9a5d01` the gate rejects `--fleet` (exit 64, COMMANDS 4). `git diff b9a5d01 f7c98ff -- .ufo/waves/round-57/c57_idresolver_gate.py` shows the `--fleet` plumbing (argparse option, `evaluate(root, rev, fleet_real)`, fleet default from `args.fleet`) and the matching `contract.md` "Pre-dispatch note" plus `controls/base-c2-idresolver-v1.1.txt` all land in `f7c98ff`, **not** in the contract commit. No condition, expected tuple or predicate changed by that diff (only `fleet_real` sourcing).
3. `c57_idresolver_gate.py` (no `--fleet`, contract commit) vs `controls/base-c2-idresolver.txt`: **byte-identical** (+ `EXIT=1`).
4. `c57_idresolver_gate.py` with `--fleet` at `f7c98ff` vs `controls/base-c2-idresolver-v1.1.txt`: **byte-identical** (+ `EXIT=1`). `controls/base-c2-idresolver.txt` and `controls/base-c2-idresolver-v1.1.txt` are themselves byte-identical.
5. `c57_quote_truth.py --revision 28fa0b23…` vs `controls/base-c3-quote-truth.txt`: **byte-identical**; the control's doubled trailing `EXIT=1` = counter's own `EXIT=1` line + one capture line, reproduced exactly.
6. `c57_receipt_pins.py --selftest` vs `controls/c1-selftest-v1.txt`: **byte-identical** (19/19 PASS; + `EXIT=0`).
7. `--revision HEAD` in the contract clone vs the `--revision 28fa0b23…` run: **two** lines differ — `population=45` → `population=50` (the five receipts committed under `.ufo/waves/round-57/controls/`: `base-c1-receipt-pins.txt`, `base-c2-idresolver.txt`, `base-c3-quote-truth.txt`, `c1-selftest-v1.txt`, `census-before.txt`) and `revision: 28fa0b23…` → `revision: b9a5d012f7fd…`. Every predicate field and all six UNDISCLOSED rows are unchanged; `met=False`, exit 1. So the counter's verdict at the contract commit is the base verdict, as the contract's do-nothing control states.
8. Counter output-shape note (no defect): only `c57_quote_truth.py` prints its own `EXIT=<code>`; `c57_receipt_pins.py` and `c57_idresolver_gate.py` leave exit-code capture to the caller. Control files are consistent with this (C3 has two EXIT lines, C1/C2 one).

EXIT CODES:

| run | expected | observed |
|---|---|---|
| C1 `--revision 28fa0b23…` | 1 (do-nothing control, met=False) | **1** |
| C1 `--revision HEAD` (= b9a5d01) | not specified; met=False | **1** |
| C3 `--revision 28fa0b23…` | 1 (0/8) | **1** |
| C2 `--revision 28fa0b23… --fleet …` at contract commit | not specified; assignment expects a 0/5 run | **64** (option absent) |
| C2 `--revision 28fa0b23… --fleet …` at f7c98ff | 1 (0/5) | **1** |
| C2 `--revision 28fa0b23…` no `--fleet`, contract commit | 1 (0/5) | **1** |
| C1 `--selftest` | 0, 19/19 | **0**, 19/19 |
| C1 / C2 / C3 with no `--revision` | 64 | **64, 64, 64** |
| C1 / C2 / C3 with `--revision deadbeef` | 2 | **2, 2, 2** |
| fleet-variant gate no `--revision` / `deadbeef` | 64 / 2 | **64 / 2** |

FINDINGS / RISKS:

- All three frozen base controls reproduce byte-for-byte from a clean clone of the contract commit (C1 9 lines, C3 26 lines, C2 12 lines) plus the C1 selftest control; no drift, no environment sensitivity observed.
- The contract names `b9a5d012f7fd` as the commit that freezes counters + base controls, but the C2 `--fleet` option, its v1.1 control and the contract's own "Pre-dispatch note" live one commit later (`f7c98ff`). A seat that follows the assignment's literal argv against the contract commit gets 64, not the 0/5 control. Whether that is acceptable (option additive, control text unchanged, v1.1 == base) or must be folded into the frozen commit is the L1's call; recorded, not remediated (leaf bounds).
- `base-c2-idresolver-v1.1.txt` does not exist in the contract commit tree; it was read from the lane working tree (committed at `f7c98ff`) for the diff.
- Scratch clones `$D` and `$E` remain under `/tmp`; nothing was installed or upgraded (no pacman, no uv, no downloads) and no lane path other than this report was written.

VERDICT: All three base controls (C1, C2, C3) and the C1 selftest reproduce byte-identically at contract commit b9a5d01; usage=64 and deadbeef=2 hold for all counters; the only defect found is that `--fleet` (and base-c2-idresolver-v1.1.txt) landed in f7c98ff, so the assignment's C2 argv exits 64 at the contract commit.
