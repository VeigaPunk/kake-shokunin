# RerunC1Before — C1 before-measurement rerun at base

Axes: operability (does the declared C1 before-counter reproduce independently
at the base revision, and does the receipt match). Freshness: not attacked here.

## What I did

Re-ran the declared C1 counter at the declared base revision
a0b0dffcd95b2215f638a5ff7591dd4fde325d27 and compared the full JSON output
field-by-field against the L1 receipt
.ufo/waves/round-32/verification/c1-before-a0b0dff.json.

## Setup

- mkdir -p /fast/scratch/hyaku/kake-r32/w1/RerunC1Before/tmp (exit 0)
- git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin
  /fast/scratch/hyaku/kake-r32/w1/RerunC1Before/clone (exit 0)
- git -C clone checkout -q 285abcad632e3c1c57bb402232e7d218054db383 (exit 0;
  clone HEAD verified = 285abcad632e3c1c57bb402232e7d218054db383)
- export TMPDIR=/fast/scratch/hyaku/kake-r32/w1/RerunC1Before/tmp

## Commands and results

Command (run twice from the clone root):
python3 -B .ufo/waves/round-32/c1_m3_probe.py \
  --repo /fast/scratch/hyaku/kake-r32/w1/RerunC1Before/clone \
  --rev a0b0dffcd95b2215f638a5ff7591dd4fde325d27

- Probe exit: 0 on both runs.
- killed: 0
- guard_ok: true
- pristine.exit: 0; specs P1..P5 all true (P1-selftest-argv,
  P2-fixture-dot-git, P3-commit-without-init, P4-expected-json-guard,
  P5-symlinked-case)
- mutant.exit: 0; same P1..P5 specs all true
- benign.exit: 0; cases 45; failed 0
- rev: a0b0dffcd95b2215f638a5ff7591dd4fde325d27 (resolved via rev-parse)
- m3Applied: true
- runnerSha256: 7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969

Comparison: parsed both JSON objects in Python and compared with `==`;
result EQUAL — every field in my rerun matches the receipt exactly
(schema, rev, m3Applied, runnerSha256, all spec tuples, benign counts,
guard_ok, killed). Zero differing fields.

## Evidence

- Rerun output saved at
  /fast/scratch/hyaku/kake-r32/w1/RerunC1Before/rerun-output.json
- Receipt: .ufo/waves/round-32/verification/c1-before-a0b0dff.json
- Probe source read at lane tip: .ufo/waves/round-32/c1_m3_probe.py
  (git-archive export of --rev from --repo, m3 guard deletion by regex,
  three runs: pristine hostile, mutant hostile --runner, benign fixtures;
  exit 0 means the probe ran, 2 means it could not)

## Findings

The declared before-measurement reproduces exactly: at base the m3 mutant is
NOT killed (mutant exits 0, killed = 0), the guard is operative
(guard_ok = true), and the 45 benign fixtures stay clean. The receipt
c1-before-a0b0dff.json is accurate; no field differs. Note the base export
carries only five hostile specs (no P6-commit-before-init), which is exactly
the gap C1 claims to repair — the before-state supports the claim.

## Not verified

- The after-measurement at 2f2f12d (c1-after receipt) — out of my scope.
- Whether the P6 spec's reason_contains matching is correct — out of my scope.
- Lane repo was not mutated: probe exports via git archive into TMPDIR only;
  clone work happened entirely in my sandbox.

## Tooling

No installs or updates; python3 and git already present.
