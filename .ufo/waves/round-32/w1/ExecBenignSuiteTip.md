# ExecBenignSuiteTip — C1 no-harm: benign suite and gate selftest delegation, tip vs base

Seat: KakeR32.ExecBenignSuiteTip (executor, leaf). Axis: operability. Milestone: r32-build.
Sandbox `/fast/scratch/hyaku/kake-r32/w1/ExecBenignSuiteTip/` (clone = tip, clone-base = base). No tool installed, no lane file written other than this report, no git mutation in the lane.

## 1. Benign fixture suite — tip and base agree (acceptance met)

Tip `285abcad632e3c1c57bb402232e7d218054db383`, base `a0b0dffcd95b2215f638a5ff7591dd4fde325d27`.

- `python3 -B clone/scripts/citing_set_selftest.py --root clone --tmpdir <sandbox>/b` → exit 0, `verdict clean`, `cases 45`, `failed 0`, `failedCases 0`, `failures []`, `notes []` (`tip-benig.json` sha256 `51019912ff03d0b5…80f7c`).
- `python3 -B clone-base/scripts/citing_set_selftest.py --root clone-base --tmpdir <sandbox>/bbase` → exit 0, `verdict clean`, `cases 45`, `failed 0`, `failedCases 0`, `failures []`, `notes []` (`base-benig.json` sha256 `7a99e77a7eb80764…8b1c`).

Row-by-row over the 45 `results` rows on the semantic fields (`ok, passed, reason, expected, actual`): **0 differing rows**; raw rows differ only in `argv` path strings. Expected/actual exit histograms identical at both revisions: exit 1 ×22, exit 2 ×14, exit 0 ×5, exit 64 ×4; verdicts failed ×22, could-not-evaluate ×18, clean ×5; case-name lists equal (45 names, `01-…`..`45-…`).

Runner and gate bytes are unchanged between the revisions (`sha256 scripts/citing_set_selftest.py` = `7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969` at both; `scripts/citing_set.py` = `dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02` at both), and the benign fixture tree hash is byte-identical (`find scripts/fixtures/citing-set -type f | xargs sha256sum | sha256sum` = `010b6b718311671b…69de` at both). `git diff --name-status base tip -- scripts/` lists only `M scripts/citing_set_hostile_selftest.py` and `A scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json` — round 32 touched the benign path in no way. 3 sequential runs at tip → `clean`, 45, 0 failed each time.

## 2. The gate's own selftest delegation — works, at both revisions

`scripts/citing_set.py --help` shows `--selftest  delegate to the sibling selftest runner`.

- `python3 -B clone/scripts/citing_set.py --selftest` (tip) → exit 0, runner summary `verdict clean`, `cases 45`, `failed 0` (`gate-tip.json` sha256 `85d23b78003f14cf…f269`).
- `python3 -B clone-base/scripts/citing_set.py --selftest` (base) → exit 0, `verdict clean`, `cases 45`, `failed 0` (`gate-base.json` sha256 `bf059b40d06bfb70…f2ca`).

Both ran inside `unshare -rm` with the runner's scratch default `/fast/scratch/hyaku/kake-r27` bind-mounted onto a sandbox dir, so the shared host path was not written. The delegation strips `--root` and re-passes it (`citing_set.py:849-865`); `--root <clone>` also works (`clean` 45/0). `--selftest --revision HEAD` is accepted by the gate parser but meaningless for a fixture run: the runner logs `notes: ["ignored unknown arguments: --revision HEAD"]` and still reports 45/0 clean.

Cross-check with the lane's own counter at the tip (read-only): `python3 -B .ufo/waves/round-32/c1_m3_probe.py --rev 285abcad632e3c1c57bb402232e7d218054db383` → exit 0, `killed 1`, `guard_ok true`, `benign {exit 0, cases 45, failed 0}`, `m3Applied true` (`c1-tip.json` sha256 `87543cf8fd81c92b…3706`) — the new P6 spec does not disturb the 45 benign cases.

## 3. New operability defect (present at both revisions, so not round-32 harm)

**The runner's scratch default is a fixed shared absolute path, and the gate's `--selftest` delegation cannot redirect it, so two concurrent runs corrupt each other and report false failures.**

Mechanism (committed bytes):
- `scripts/citing_set_selftest.py:133` — `DEFAULT_TMPDIR = "/fast/scratch/hyaku/kake-r27"` (the `--tmpdir` default at `:166`); a constant, not derived from `TMPDIR`.
- `scripts/citing_set_selftest.py:701` — `cases_root = <tmpdir>/citing-set-selftest/cases`; `:509-510` — `prepare_case` does `shutil.rmtree(work_dir)` then `shutil.copytree(case_dir, work_dir)`, so two runs on one scratch root delete and re-create each other's per-case copies.
- `scripts/citing_set.py:882-884` — the gate parses its own argv *before* the `--selftest` branch and `GateParser.error` (`:785-797`) rejects anything the gate does not define. Verified: `python3 scripts/citing_set.py --selftest --tmpdir <d>` → exit 64, JSON `{"verdict":"could-not-evaluate","error":"usage: unrecognized arguments: --tmpdir <d>"}`; same for `--timeout 20`, `--min-cases 12`, `--fixtures scripts/fixtures/citing-set` (all exit 64). The documented delegation therefore always uses the shared default scratch.

Reproduction: per pair, two `citing_set.py --selftest` processes started simultaneously, the scratch default bind-mounted to a per-iteration sandbox dir so the host path stays untouched. Tip `285abcad`: 4 of 4 iterations produced a false failure; base `a0b0dff`: 4 of 4. Failure reasons observed: `case copy failed: [Errno 17] File exists: …/cases/01-single-literal-clean`; `case copy failed: [Errno 39] Directory not empty: …`; `exit mismatch: expected 1, observed 2` (case `17-ledger-row-outside-population`); `finding mismatch` (case `35-population-id-unreachable`). One process in each pair reported `verdict failed` while the other reported `verdict clean`; the failing side names cases that pass in isolation. A cross-revision pair (tip + base on one scratch root) collided the same way. Control: the same two concurrent runs with **distinct** `--tmpdir` → both `clean`, 45, 0 failed. The runner also ignores the `TMPDIR` env var for its own scratch: with `TMPDIR=<sandbox>/envtest` and no `--tmpdir` that dir stayed empty while copies landed in the shared `/fast/scratch/hyaku/kake-r27/citing-set-selftest/cases` (46 entries there, incl. a stray `x/` left by another seat at 15:58).

Severity: identical at base and tip → **not** round-32 harm, and it does not affect the declared counters — `c1_m3_probe.py` uses `tempfile.TemporaryDirectory` with explicit `--tmpdir` values (`:64-88`) and `citing_set_hostile_selftest.py` requires `--tmpdir` (`:229`). It does affect operators and the integration gate: any seat or human running the documented `scripts/citing_set.py --selftest` while another does the same (normal in a parallel wave) can get a `verdict failed` benign suite that is an artefact of the shared scratch, not of the code. Scope note: not the held `KakeR31.CriticC1Counter` (a counter trusting runner-reported failure names) and not the held `KakeR31.CriticSandboxThreatModel` (fixture-driven escape routes; its route list R1-R7 does not mention the runner's own shared default scratch or cross-run interference). A distinct operability line; I did not judge whether to route it.

## 4. Not verified / out of scope

- No build, lint, test-suite or formatter run; other seats' counters not re-run.
- Hostile selftest run once at tip (6 specs, all `passed`, `error null`) and once at base (5 specs, all `passed`) as parity only; the m3 kill was measured by the lane's own counter, not by me.
- No network resource opened; no operator-owned web property touched.
- Lane `git status` shows `M .ufo/waves/round-32/w1/ExecBaseRunnerVsP6.md` and `M .ufo/waves/round-32/w1/MutM3Variants.md`; those are other seats' files, not mine.
