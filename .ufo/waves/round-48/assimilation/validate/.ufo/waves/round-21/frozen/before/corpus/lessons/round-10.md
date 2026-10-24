# Lesson — round 10 (2026-09-28)

Cites: LOG.md round-10 entry; evidence = 11 delegated read-only L2 probes
(`/tmp/kake-r10/`: planner, scout-inventory, executor-a/b, labrat, reviewer,
connector, sentinel, scribe-manifest) + L1 self-runs (naive differ, raw-row
greps, detector runs). Commit `round-10`. Zero fires, zero pushes to fleet
sources, zero browser ops, zero webzites-state mutations (sentinel-verified:
probe-history + probe-latest sha identical before/after).

## The gap closed (operability — lowest axis, 6/10)

"Alerting on `violated[]` deltas is undecided" (README known gap since r5) +
SKILL.md/checklist executability never measured as a suite. Landed
`scripts/probe-delta.mjs` + `corpus/knowledge/probe-delta-alerting.md` +
checklist-audit fixes; SCORECARD 6→8.

## What the round measured

- **Naive history diffing is unusable**: 42 events, 40 phantom (labrat
  replication; L1 run) — spot (`total:1`) rows against fleet sweeps fabricate
  fleet-wide clear/re-enter pairs. Phantom class killed by the
  running-universe rule; final run: **6 events, 0 phantom**, all four r5
  ground-truth records reproduced (sentinel: detector "reproduces all four
  ops-automation.md r5 truths").
- **The r5 veigapunk-page record was wrong** — raw rows: violated at
  09-21T03:32:06.747Z, clean at 04:14:50.502Z; the 04:14:50→09-22T22:58:23
  pair carries *identical* `violated[]` sets (zero delta). r5 had used the
  42.73h sampling hole's endpoints as the transition window. Corrected in
  `ops-automation.md`; planner + labrat + reviewer + L1 raw-row read all
  agree. Lesson: **a coverage hole's endpoints are not a transition window**.
- **Checklist executability**: Scout 33/33 SKILL.md commands + 60/60 paths
  resolve (r9 PATH fix held); ExecutorA executed 5 live commands — 2
  undocumented behaviors found: `webzites status` **exits 1 on any
  violation** (`src/cli.mjs:99` — stdout-read, never a gate) and
  `kimi-surface.mjs` has **no `--help`** (usage via unknown verb, exit 64,
  `:1197-1198`). Both landed in SKILL.md.
- **Citation drift found + fixed**: `vault-properties.md:60` `:891-894`→
  `:903` (zip-exclude chain); `lessons/round-9.md:33` `:339`→`:342` (32MB
  maxBuffer literal, range `:339-346`); SKILL.md cwd-relative
  `node scripts/kimi-surface.mjs` invocations → absolute
  `~/Projects/webzites/scripts/…` (a reader outside that cwd got ENOENT).
- **xsnapshot-app "every run since 09-21" was loose**: constant on every
  *full sweep* since 09-21T01:34:20Z (absent on 11 earlier full sweeps;
  present on the 09-20T23:47:10 bootstrap row). Judge constancy on full
  sweeps only — spot rows trivially omit every other site.

## Learned

- **Diff event logs by universe, not by adjacency.** Any per-row log that
  mixes single-item and full-universe rows (probe-history class) must gate
  diffs on `total === running max` — and treat the first/`ok:0` row as
  baseline, never a transition source (9 bootstrap phantoms killed).
- **Bookkeeping quirks surface under audit**: 11 history rows carry
  `total ≠ ok+|violated|+|errors|` — summaries can't reconstruct rosters;
  event derivation must not depend on the sum.
- **A runnable artifact beats an "undecided" flag**: the README gap lived
  five rounds as prose; one read-only script turned it into measured output
  (and exposed a wrong corpus record on its first run — the detector
  falsified our own r5 documentation).
- **Cross-lane check**: connector found no sibling collision on
  probe-history alerting (kumitate/kagi/kasegi tooling adjacent only);
  CDP-9222 lease ownership still unresolved — reported, not absorbed.
