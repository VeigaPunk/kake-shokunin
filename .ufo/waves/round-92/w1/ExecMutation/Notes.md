# ExecMutation — notes (round 92, item A)

## Design of the runner (`integration/mutate-tip.py`)

- Check = the gate's own conformance run: `scripts/cache_key_conformance.py --candidate scripts/cache_key.py --work <scratch> --seed 92`.
  `scripts/cache_key.py` is the conforming candidate: the gate scores it `met=true` (seed 1 and seed 92; `run.log` [2], base verdict in `mutant-out/base.out`).
- `base` runs the unmutated gate. `survived rc=0` iff the gate exits 0 (its own last line reads `met=true`).
- `M<nn>` applies one literal replacement to a copy of the gate in a scratch directory. The replacement must match exactly once; a mismatch exits 2 with no verdict, so an anchor error can never read as a verdict. Verdict: `killed rc=<gate rc>` if nonzero, `survived rc=0` if zero.
- The table `MUTANTS` (30 rows) was fixed by reading the gate before any run; it was not adjusted after results. Its order is the table order: M01 is the drop-sort mutant. That choice is deliberate; see counter defect D2.
- Fixed `SEED=92` so base and every mutant see the same generated population. This makes the run a differential rather than a random sample. Only one seed was run per mutant (no repeat runs).
- Scratch: `$HYAKU_SCRATCH` else `$TMPDIR`; `/tmp` is refused. Output: context lines first, verdict last. Exit 0 once a verdict prints.
- Stdlib only (`argparse, os, shutil, subprocess, sys, tempfile`; `re` is imported but unused — dead weight, left in place so the run log matches the bytes that produced it: `sha256sums.txt`).

## What the kills measure (important limit)

The spec's verdict semantics are: a mutant is `killed` when the mutated gate **fails on a conforming candidate**. That is sensitivity of the conformance run to its own mutation. It is not a measure of whether the gate rejects non-conforming candidates; a survivor in this table is a mutation the conforming run cannot see.

Breakdown of the 20 kills:
- 17 are caught by the gate's **reference self-check** (`rc=2`, M01–M17): the mutated reference disagrees with the contract's hand cases before any candidate runs. These measure the self-check, not the conformance judgment.
- 3 kill by a crash or a sandbox event (`rc=1`): M18, M19 (TypeError inside the self-check) and M20 (every stdlib file read denied → `sandbox=violation`, the gate's real judgment path).

The 10 survivors are: sandbox denial branches that only bite on adversarial candidates (M21–M25, the conforming candidate never triggers them); the `met` and `generated` conjuncts and self-check skip (M26–M28); the refusal stdout judge (M29); and clause last-wins (M30). These are the gate's adversarial power, which this runner does not exercise. K/N = 20/30 is therefore **not** evidence of adversarial strength. A stronger successor would score mutants against a non-conforming candidate set (each mutant should be killed by at least one adversarial fixture), which is a different check than the spec asks for.

## Counter defects found (frozen `c92_defects.py`; routed, not repaired)

- **D1 — item A admits an unexecuted verdict for every unsampled mutant.** Lines 155, 169, 175: the counter executes only `sorted(verdicts)[0]` (M01) and compares its observed verdict with its log line. The other 29 log lines are never re-derived. Evidence: forged scratch fixture `cbe74334`, where the log reads `M30 verdict=killed rc=1` (the runner observes `survived rc=0`) and the receipt reads `killed=21 survivors=9`; `counter/counter-forge.out` = `C1v92 … open=0 closed=3 … met=true`, exit 0. This is the same K91-1 class ("receipt with no execution") the claim says is closed. The claim is not closed for unsampled lines.
- **D2 — item A's differential assumes the sampled mutant is a killer.** Line 173: if the first sorted id survives, base and mutant both read `survived rc=0` and item A is refused as "canned output", even when the runner is genuinely differential. The table's M01 is a killer, so the frozen counter passes; with a survivor first, a correct runner would be rejected. Both the table order and this counter behaviour were checked by reading, not by a constructed case.
- **D3 — `--skip-battery` reads `met=true` and `differential=ok` without measuring either.** Line 421 sets `battery_ok = True` by default, line 432 folds it into `met`, and line 438 prints `differential=ok` whenever `battery_ok` holds. Observed: `counter/counter-skipbattery.out` = `… battery=skipped differential=ok self=ok met=true`, exit 0. The spec's required invocation therefore prints `met=true` on a predicate that is not the frozen one; the verifier should count the battery run (`counter/counter-full.out`: `battery=exact … met=true`, exit 0), not the skip run.
- **D4 — item C's carrier is the clone's `master`, not `--revision`.** `clone_at` (lines 111–115) points the clone's `master` at the root's `master` and then checks out `--revision` detached. `run_controls.sh` line 15 derives `CARRIER` from `master`, and the counter does not pass `CARRIER`. Item C therefore replays the root's master whenever `--revision` ≠ master tip. I made the fixture consistent by pointing its master at the fixture commit (per the seat spec); a counting command against the lane with `--revision <freeze or other>` would replay the lane's master. [INFERENCE from reading the code; not exercised with a non-tip `--revision`.]
- Item B is satisfied only by a row in the scratch fixture (`clone/SKILL.md` line 1615). I did not land a SKILL.md row in LANE; that is another seat's item.

## Honest limits

- One run per mutant; no repeat, no timing or seed sensitivity beyond the seed-1 base probe.
- Only one conforming candidate (`scripts/cache_key.py`). Its conformance to the contract is whatever the gate says; I did not re-derive it.
- The 17 self-check kills mean the table's "killed" column is dominated by reference drift; read the breakdown above before quoting K.
- The first runner probe showed a harness bug (base killed by a missing work dir). It was fixed before the table run; the broken probe's receipts are not in `mutant-out/`.
- No mutant verdict was undetermined: 30 of 30 printed a verdict; base printed one.
- No tool installed, upgraded or removed. No network. No git mutation in LANE. The LANE working tree gained only the three integration files (plus this wave directory).
