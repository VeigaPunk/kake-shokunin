# CriticOptionTableRejection — round 33 wave 2 (falsify), axis operability

Verdict: the rejection reason is CONFIRMED. A better single-source design exists: read the table from the gate script the run executes, not from the runner's directory. It scores met 4 with guard_ok true. Adopting it trades away one fail-closed property (counterexample 3), so the L1 has to choose; the hard-coded table is not shown to be wrong.

Sandbox: /fast/scratch/hyaku/kake-r33/w2/CriticOptionTableRejection/ (clone at 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0, TMPDIR=<sandbox>/tmp). No tools installed. No lane mutation; this report is the only file written in the lane.

## 1. The wave-1 patch applied at the lane tip
- `git apply --check` of patch.diff (sha256 28fd9adf…d6e) at 0a0acfb: exit 1, because the import block changed (`import tempfile` was added after bc6c4a8).
- `git apply --3way`: one conflict, in the import lines only. I kept both imports and committed sandbox commit b209bcb30a1c249ff7034f55777cded394f9c0ec (scripts/citing_set_selftest.py +28/-11; `from citing_set import build_parser` at line 408).

## 2. Is the rejection reason true? Yes
- `python3 -B .ufo/waves/round-33/c1_code_probe.py --repo <clone> --rev b209bcb` gives exit 0, met 0 of 4, guard_ok false (out/probe-patched.json).
  - pristine exit 1, failing [P1-selftest-argv]; reworded the same.
  - m3 and recoded exit 1, failing [P1, P6]. These are not counted as killed because the failing set is not exactly {P6}.
  - The benign run (runner in export/scripts/, next to citing_set.py) passed 45 of 45.
- Control, same command with `--rev 0a0acfb`: met 4, guard_ok true. pristine and reworded exit 0; m3 and recoded exit 1 with failing [P6] (out/probe-tip.json).
- Cause: the probe writes each variant to `<tmp>/<name>_citing_set_selftest.py`. There, sys.path[0] has no citing_set.py, so the lazy import raises the first time a case argv carries an option token. Hostile spec P1 has such tokens (`--selftest`, `--self`, `--revision HEAD --selftest`).
- A direct temp-dir copy (`cp` the runner to <sandbox>/tmprunner/, then `python3 -B …/citing_set_selftest.py --root <clone> --tmpdir …`) exits 1 with no JSON on stdout. Stderr shows a traceback ending in `ModuleNotFoundError: No module named 'citing_set'` (out/direct-copy.err). Benign fixtures 36, 37 and 42–45 all carry option argv, so every full run reaches the import.
- Secondary harm: the traceback exits 1, which is the runner's exit code for a failed case. A crash therefore looks like a refusal to any reader keyed only on exit code.
- Secondary defect found by running it: the patch reads the table from the runner's sibling gate, not from the `--gate` the run executes. The patched runner, placed next to a pristine citing_set.py and run with `--gate exp/gate_valued_selftest.py`, refused `--selftest` using the sibling's table (out of exp/vs-patched.json; rc 1). So the table and the executed gate can differ.

## 3. Alternative: read the table from the executed gate
- Sandbox commit 21da23cf939f2f24e3fec857867a9f5606505026 on 0a0acfb. Diff at /fast/scratch/hyaku/kake-r33/w2/CriticOptionTableRejection/alt-patch.diff (sha256 daeaa738…ce6e; +35/-15, one file).
- What it changes:
  - `gate_option_names(gate)` compiles and executes the resolved gate file in a private namespace. There is no import and no bytecode write; scripts/__pycache__ is absent after the runs.
  - It partitions `build_parser()._actions` by `nargs == 0` into valued options and flags.
  - `_run` calls it once, after the `gate.is_file()` check. Any exception gives could-not-evaluate (exit 2) with no traceback.
  - The table is passed down through run_case, prepare_case, load_case_setup and argv_refusal.
  - GATE_VALUE_OPTIONS and GATE_OTHER_OPTIONS are deleted, and the module docstring is updated.
- Results (all exit codes as observed):
  - C1 probe `--rev 21da23c`: exit 0, met 4, guard_ok true. pristine and reworded exit 0; m3 and recoded exit 1 with failing [P6] (out/probe-alt.json).
  - Direct temp-dir copy: exit 0, verdict clean, 45 cases, 0 failed, empty stderr (out/direct-copy-alt.json).
  - In-tree runner: exit 0, clean, 45 of 45 (out/intree-alt.json).
  - Hostile selftest (`scripts/citing_set_hostile_selftest.py --root <clone> --tmpdir …`): exit 0, P1 to P6 all passed (out/hostile-alt.json).
- Mutation check of the new code, run through the hostile selftest with `--runner`:
  - Classification inverted (`nargs != 0`): exit 1, failing [P1] (exp/mut_classify.hostile.json).
  - Flags folded into valued options: exit 1, failing [P1] (exp/mut_noflags.hostile.json).
  - P1 still kills drift in how the table is derived.

## 4. Strongest counterexample against any gate-derived design (the tradeoff)
- Setup: a gate copy whose only change makes `--selftest` take a value (`action=StoreOnce`), at exp/gate_valued_selftest.py. Fixture dir exp/fixtures holds the 01-single-literal-clean case plus a copy named zz-valued-selftest with case.json `{"argv": ["--selftest", "x"]}`.
- Alternative runner with `--gate <that gate>`: exit 1. The case was not refused. The runner forwarded `--json --selftest x`, the gate entered `run_selftest`, and it exited 2 (could-not-evaluate) only because the gate copy's directory has no sibling runner. The recorded argv is in exp/vs-citing_set_selftest.py.json.
- Lane-tip runner (hard-coded table), same inputs: exit 1, with the case refused before the gate started: "case.json argv refused: --selftest" (exp/vs-tip_runner.py.json).
- Meaning: when the table comes from the gate, a change to the gate under test can widen the runner's argv allowlist. The hard-coded table fails closed: any unknown option is refused. Its cost is a hand edit when the gate gains a valued option.
- The alternative also depends on argparse's private `_actions` attribute, the same dependency the wave-1 patch had.

## Impacted axes
- Operability: the wave-1 patch breaks every probe and counter that runs a runner copy outside scripts/ (C1 probe met 4 to 0). The alternative keeps met 4 and also works from temporary paths.

## Smallest safe correction
- Keep the lane as it is (rejection upheld; SKILL.md 'Citing-set runner — round 33' and lesson item 7 are accurate), or
- Adopt alt-patch.diff if one source of truth outweighs failing closed on gate drift. Optionally keep a one-name fixed refusal of `selftest` to restore the counterexample-3 floor; that is a deliberate safety floor, not a mirror of the gate's table.

## Not verified
- Concurrency of the alternative.
- The round-31 and round-32 counters and c1_strict_supplement.py were not run against 21da23c.
- No runs without `-B`.
- Time: finished 2026-10-22T20:17Z.
