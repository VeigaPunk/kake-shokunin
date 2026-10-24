# Wave 2 (a2): ReviewHostileSelftestCode — can the hostile selftest report a pass that is not earned?

**Verdict: YES — the selftest and the C1 counter both report full pass for a runner that refuses every `h*` case by name without ever building, copying or executing it.** One HIGH finding, plus three smaller spec-validation/discovery defects.

Target files (reviewed at lane tip 92235a0 in sandbox clone): `scripts/citing_set_hostile_selftest.py` (243 lines), `.ufo/waves/round-31/c1_sandbox_probes.py` (306), the five specs `scripts/fixtures/citing-set-hostile/P*/hostile.json`, gate runner `scripts/citing_set_selftest.py`.

## F1 (HIGH): name-based refusal earns a pass — the runner's self-report is trusted, and harm checks only fire if the runner reaches the harm

The spec predicate is `passed = (exit == 1 and "00-benign" not in failed and all(h in failed for h in hostile) and not canary and victimUnchanged)` (`citing_set_hostile_selftest.py:204`). Everything except `canary`/`victimUnchanged` is the runner's own JSON self-report; and a runner that refuses `h*` cases before doing anything never writes the canary and never touches the victim, so both harm checks are trivially satisfied. Nothing checks the refusal *reason*, that the gate ran, or that the refusal came from the containment code under test.

Reproducers (all in `/fast/scratch/hyaku/kake-r31/a2-w2/ReviewHostileSelftestCode/`):

- `variants/v1_namefail.py` — real runner + 4-line patch: `if case_dir.name.startswith("h"): row["reason"]=...; return` inserted after `run_case`'s row dict (lines 521-524). It still copies and runs the gate for benign cases.
- `variants/v2_sham.py` — 60-line sham that never copies a case or runs the gate; fails any name starting with `h`, passes the rest.

Commands and outputs:

    python3 -B clone/scripts/citing_set_hostile_selftest.py --root clone --runner variants/v1_namefail.py --tmpdir $T/v1   → exit 0, all 5 specs passed; every reason is "case name starts with h, refused"
    python3 -B clone/scripts/citing_set_hostile_selftest.py --root clone --runner variants/v2_sham.py --tmpdir $T/v2   → exit 0, all 5 specs passed, canary=false, victimUnchanged=true — a runner that executes nothing "proves" containment.

Counter, full defeat: committed `v2_sham.py` as `scripts/citing_set_selftest.py` in the sandbox clone (rev `72c9bae1`), then

    python3 -B .ufo/waves/round-31/c1_sandbox_probes.py --root . --revision 72c9bae1 --scratch <sb>/counter   → exit 0, "C1 5/5 K1=hold".

Why: the five probes name their hostile cases `h1a..h5`, so `behaviour_ok` (counter line 123) passes on name alone; `hostile_selftest()` is run **against the runner under test** (counter line 278, selftest defaults `--runner` to the export's own runner), so `fixture_ok` (line 291) inherits the sham's self-pass; K1 passes because no committed `citing-set/` case starts with `h` (verified: `ls` → 0 of 45). The counter prints `runnerSha256` (line 297) but compares it to nothing — the swap is visible only to a human reading the receipt. `runnerSha256` sham = `dbf25572…`, real = `5371530d…`.

Consequence: "5/5 hostile spec pass" proves only that *some* runner prints the right failure names; it cannot distinguish the repaired containment from name-matching. Fix direction (advisory): assert refusal reasons match expected substrings per spec (e.g. P1 → "argv refused"), or require evidence the gate ran for hostile cases that got past refusal.

## F2 (MEDIUM): spec-valid case name with embedded NUL crashes the selftest — traceback, exit 1, all results lost

`load_spec` only requires `name.startswith("h")` and no `"/"`. `"h9\0x"` passes validation; `shutil.copytree` inside `build_case` raises `ValueError: mkdir: embedded null character`, which `main` does not catch (only `OSError, RuntimeError, SubprocessError`), so the whole run dies with a traceback instead of exit 2 / per-case failure. Repro: `specs/b11-nul` root + `python3 -B citing_set_hostile_selftest.py --root specs/b11-nul --tmpdir …` → exit 1, `ValueError: mkdir: embedded null character in path` on stderr, no JSON summary.

## F3 (LOW): a symlinked spec directory is silently skipped — the N6 defect shape exists one level up

Spec discovery excludes `p.is_symlink()` (line 220). Root `specs/b10-linkdir` where `B-bad` is a symlink to the real P5 spec → exit 2 "runner, benign fixture or hostile specs missing" (zero specs seen). The shipped fixture check can never silently skip (the counter requires named `P<n>-*` dirs, counter line 291), but any future spec added as a symlink vanishes without a failure — asymmetric with the runner refusing symlinked *cases*.

## F4 (LOW): `citing-set-hostile` itself may be a symlink out of `--root`

`spec_dir.is_dir()` (line 220) follows symlinks. `specs/b12-dirlink` with `citing-set-hostile → <sandbox>/outside-specs` loads and runs specs from outside the root: exit 0, passed (real runner refused them, no unearned pass by itself, but the "specs come from the committed tree" boundary is broken).

## Verified good

- **Benign-case must pass**: `variants/v3_failall.py` (fails every case incl. 00-benign) → exit 1, all 5 specs False, `00-benign` listed among reasons. A fail-everything runner is caught.
- **Harm observables are live** (vs `c1-before-f1ffb81.json` at f1ffb81): P1 `canary:true` (planted script executed — exit was already 1, so canary is load-bearing); P2/P3 `victimUnchanged:false`, runner exit 0 (victim check is what catches them); P4 timed out on the FIFO; P5 `exit 0` silent skip.
- **Spec validation refuses**: non-object, extra spec key, empty cases, name not `h*`, name with `/`, unknown `expected` shape, symlinked `hostile.json`, >64 KiB spec — all exit 2 with a clear error (roots `specs/b1..b8`, messages quoted in transcript).
- **No vacuous pass**: minimal spec `{"cases":[{"name":"h9"}]}` is *accepted* (keys are optional) but correctly fails at runtime — benign copy passes, `h9` absent from failures, exit 1, `passed:false` (real runner).
- **Controls**: selftest on the real runner → exit 0, 5/5 (`out-real.json`); counter at 92235a0 → exit 0, `C1 5/5 K1=hold`, runner sha `5371530d…` (`out-counter-real.json`).

## Not verified

Whether the counter's declared-round usage ever pins `runnerSha256` to a known-good value externally (receipts record it; nothing in the counter enforces it). Whether planted scripts could execute via paths other than the checked canary (e.g. a gate run that reads but never execs fixture scripts — out of the spec model).

## Artifacts (all under /fast/scratch/hyaku/kake-r31/a2-w2/ReviewHostileSelftestCode/)

`clone/` (git clone of the lane at 92235a0 + attack commit 72c9bae1), `variants/v1_namefail.py`, `variants/v2_sham.py`, `variants/v3_failall.py`, `out-real.json`, `out-v1.json`, `out-v2.json`, `out-v3.json`, `out-counter-real.json`, `out-counter-v2.json`, `specs/b1..b12` roots.

Tools installed: none. Python 3.14.8, git 2.x system tools only.
