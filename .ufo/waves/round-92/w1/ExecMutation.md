VERDICT: item A artifacts land and measure as specified (N=30 K=20 S=10 met=true; base survived, M01 killed; frozen counter `--skip-battery` exit 0 met=true), but the frozen counter's item A checks only one mutant verdict against an execution, so C1 is not closed for unsampled lines (forged M30 admitted, met=true).

# ExecMutation — round 92, item A (C1, K91-1)

Seat: ExecMutation (executor, leaf; no subagent). Freeze `a5640ca02c20f94a0fa03af41b977b46ae99808e`; lane master at start `f0b2dc63`. Gate blob `scripts/cache_key_conformance.py` sha256 `d7bca38ec146727087a2d2e37a64c5154214e2dd069553fb5594372d2064b65e` at freeze, master and working tree (equal).

## Deliverables (in LANE)

- `.ufo/waves/round-92/integration/mutate-tip.py` — stdlib runner, `--mutant base|M<nn>`, 30-row frozen `MUTANTS` table, exactly-once anchors, scratch refused under `/tmp`.
- `.ufo/waves/round-92/integration/mutation-tip.log` — 30 lines, `M<nn> verdict=killed|survived rc=<int>`, base excluded.
- `.ufo/waves/round-92/integration/mutation-tip.txt` — line 1 `gate_sha256=d7bca38e… mutants=30 killed=20 survivors=10 met=true`, then one line per mutant with its mutation.
- `.ufo/waves/round-92/w1/ExecMutation/{run.log,Notes.md}` plus receipts (`mutant-out/`, `counter/`, `sha256sums.txt`).

## Results

Verdicts (from `w1/ExecMutation/mutant-out/*.out`, last line):

| Mutants | Verdict | rc | What catches it |
|---|---|---|---|
| base | survived | 0 | conforming run, `met=true` |
| M01–M17 | killed | 2 | reference self-check drift (17) |
| M18, M19 | killed | 1 | TypeError in self-check |
| M20 | killed | 1 | sandbox violation (stdlib roots emptied) |
| M21–M30 | survived | 0 | sandbox denial branches, `met`/`generated`/self-check skip, refusal judge, clause last-wins |

Counts (computed from the log): N=30, K=20, S=10, S==N−K, N≥20, K≥18. Every mutant printed a verdict; none undetermined.

Differential (`run.log` [11]): `--mutant base` → `verdict=survived rc=0`; `--mutant M01` → `verdict=killed rc=2`; these differ. Survivor control M21 → `verdict=survived rc=0`.

## Frozen counter acceptance

Command (exit codes shown):

    python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-92/c92_defects.py --root <clone> --revision 371f9eb73dba244ad0f786878d26b39d15dac01a --work $S/w --skip-battery   → exit 0
    C1v92 revision=371f9eb73dba244ad0f786878d26b39d15dac01a items=3 open=0 closed=3 battery=skipped differential=ok self=ok met=true

Full battery (no `--skip-battery`), same revision → exit 0, `battery=exact differential=ok self=ok met=true` (`w1/ExecMutation/counter/counter-full.out`). Selftest `12/12`, exit 0. The fixture is scratch commit `371f9eb7` (4 files on the freeze; 0 deletions vs base `e143faff`); its SKILL.md row sits only in that scratch clone.

## Findings (defects, all routed; no frozen instrument edited)

- **D1 (item A, K91-1 not closed for unsampled lines).** `c92_defects.py` lines 155/169/175 execute only `sorted(verdicts)[0]` (M01). Forged scratch fixture `cbe74334`: log `M30 verdict=killed rc=1` (runner: `survived rc=0`), receipt `killed=21 survivors=9`. Counter `--skip-battery` → exit 0, `met=true` (`w1/ExecMutation/counter/counter-forge.out`). Routed: item A must re-run or bind every log line (e.g. per-mutant execution log bound by digest, as K91-1 asked).
- **D2 (item A differential).** Line 173 refuses base-vs-sampled equality as "canned output"; if the first sorted mutant survives, a genuinely differential runner is refused. This passes here only because M01 is a killer by table choice (stated in `Notes.md`).
- **D3 (`--skip-battery` reads met=true).** Lines 421/432/438: `battery_ok` defaults true and is printed as `differential=ok` with no differential run (`counter-skipbattery.out`: `battery=skipped differential=ok … met=true`, exit 0). The spec's required command prints the frozen `met` label on an unmeasured predicate; use the battery run for the claim.
- **D4 (item C carrier is `master`, not `--revision`).** `clone_at` lines 111–115 and `run_controls.sh` line 15 derive CARRIER from the root's `master`; the counter never passes `--revision` to the replay. Item C replays the root's master whenever `--revision` is not the tip. [INFERENCE from reading; not exercised with a non-tip revision.] The fixture is consistent only because I pinned its master to the fixture commit, as the seat spec directed.
- **D5 (kill semantics in the spec, measured here).** The spec's verdict (`killed` = mutated gate fails on a conforming candidate) makes 17 of 20 kills self-check drift, and the 10 survivors are adversarial-only branches the conforming candidate never exercises. K/N is sensitivity to reference mutations, not adversarial strength. Detail in `Notes.md`.
- Trivial: `mutate-tip.py` imports `re` unused. Left unchanged so the log matches the bytes that produced it.

## Honest limits

- One run per mutant; single conforming candidate `scripts/cache_key.py` (gate `met=true` at seeds 1 and 92); not re-derived against the contract.
- The first runner probe had a harness bug (missing gate `--work` dir → base `killed rc=1`). Fixed before the table run; its outputs are not in `mutant-out/`.
- Two runner-file edits were needed (one misplaced edit broke parsing, then repaired). The final runner is the file the table ran against: `sha256sums.txt` records `e163b591…`.

## Tooling and channel record

No tool installed, upgraded or removed. Python 3.14.8 (`/usr/bin/python3`), stdlib only. No network GET. No pacman. No git mutation in LANE; the scratch clone and forge clone were committed under the fixture identity only. Scratch `/fast/scratch/hyaku/kake-r92/ExecMutation` deleted after receipts were copied.

## Checks for the main agent

- `python3 -B .ufo/waves/round-92/integration/mutate-tip.py --mutant base` (lane cwd) → last line `verdict=survived rc=0`.
- Re-run the runner on M01 and M21 for the differential.
- Treat the counter's `met=true` for item A as provisional until D1 is routed (see D1).
