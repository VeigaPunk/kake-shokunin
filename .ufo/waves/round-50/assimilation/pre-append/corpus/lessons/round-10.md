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

## Gate

Label: **retrospective round-21 reconstruction, not the original round-10 admission.** No round-10 gate or candidate ledger existed before this section. Everything below is reconstructed from this lesson's own sections (lines 10-62), `LOG.md:15`, `SCORECARD.md` row 10, `SKILL.md:224`, and the round-10 knowledge entries. Live state was not re-verified.

Metadata/gate contract: S019 (`corpus/SOURCES.md:27`; metadata authority only, not platform evidence) requires knowledge entries to open with `source`, `verified-at` and `recheck`, and round lessons to record candidates, admissions, rejections and spot-check state. The round-21 lesson it names (`corpus/lessons/round-21.md`) was not present in `corpus/lessons/` when this section was written.

Candidates considered (reconstructed):

- **Detector for `violated[]` deltas** (`scripts/probe-delta.mjs`, lines 12-15). Historically supported: **admitted with qualification.** Round-10 run: 76 rows, 6 events, 0 phantom. A later re-run at 78 rows recorded 6/0 (`corpus/knowledge/ops-automation.md:115-119`). Qualifications: no consumer, and alert delivery stays with the webzites owner (`README.md:72-75`, `LOG.md:15`); merged rows from `grokbot tick` / `bots task` cannot be separated by the detector (`corpus/knowledge/probe-delta-alerting.md:88-91`).
- **Running-universe rule** (diff only when `total` equals the running max; the first or `ok:0` row is a baseline, lines 49-52). Historically supported: **admitted with qualification.** It killed 9 bootstrap phantoms (`probe-delta-alerting.md:37-38`); it does not cover merged rows (above).
- **Corrected round-5 veigapunk-page record** (the 04:14:50 to 09-22 transition window, lines 25-30). Historically supported: **admitted as a correction.** Raw rows show the endpoints carried identical `violated[]` sets; the record was corrected in `ops-automation.md:43-47`. The lesson's "a runnable artifact beats an undecided flag" (lines 56-59) rests on the same evidence.
- **Checklist executability: 33/33 SKILL commands and 60/60 paths resolve** (lines 31-32). Historically supported: **admitted for the round-10 measurement only.** The 60/60 claim was later retired by a round-15 measurement (`SKILL.md:203-206`, `corpus/knowledge/freshness-sweep.md:32-34`); it is not re-measured here.
- **Undocumented CLI behaviours** (`webzites status` exits 1 on any violation, `src/cli.mjs:99`; `kimi-surface.mjs` has no `--help`, exit 64, `:1197-1198`). Historically supported: **admitted with qualification.** Landed in SKILL.md per lines 33-36. The round-11 live run recorded status exits 0/1 (`SCORECARD.md` row 11). The source lines were not re-read here.
- **Citation drift fixes** (`vault-properties.md:60`, `lessons/round-9.md:33`, SKILL.md cwd-relative invocations made absolute, lines 37-41). Historically supported: **admitted with qualification.** A later round-20 path sweep lists `corpus/lessons/round-10.md:41` as an indirect declared-absent cite (`.ufo/round-20/resume/paths-before.txt:55`). Recorded, not re-verified.
- **Narrowed xsnapshot-app constancy claim** (full sweeps since 09-21T01:34:20Z only, lines 42-45). Historically supported: **admitted with qualification.** Spot rows omit sites by design, so the claim is judged on full sweeps only.
- **Bookkeeping quirk: 11 history rows with `total` not equal to `ok+|violated|+|errors|`** (lines 53-55). Historically supported: **admitted as an observation.** Documented in `probe-delta-alerting.md:45-47`; the round-6 aggregator audit flagged it as uncorrected at its time (see outside spot-check).
- **Cross-lane check: no sibling collision on probe-history alerting** (lines 60-61). Historically supported: **admitted as reported by one lane.** The connector report is not recorded in the corpus.
- **CDP-9222 lease ownership.** Historically supported: **unverified, open.** The lesson reports it and does not absorb it (line 62).

Rejected candidates (documented reasons only):

- **Naive consecutive-row history diff.** Rejected: 42 events, 40 phantom, from spot rows diffed against fleet sweeps; the fabricated fleet-wide clear/re-enter pairs are the documented reason (lines 19-21).
- **Round-5 "04:14 to 09-22T22:58" transition window.** Rejected: the endpoints of a 42.7h coverage hole, with identical `violated[]` sets and zero delta (lines 25-30).
- **Superseded later, not a round-10 rejection:** “60/60 paths resolve” as a standing claim was rejected in round 15 (`SKILL.md:203-206`); a frozen sample cannot see claim classes it never sampled.

No other rejections are recorded.

Admit/reject spot-check: **not recorded.** Other non-author evidence: `corpus/lessons/round-6-aggregator-audit.md` (aggregator L1 non-author review, scout lane, 2026-09-28, round-10 HEAD `dd4eabf`, lines 3-4) checked corpus rules against round 10 and found: the 11/76 identity mismatch, acknowledged in round 10 but uncorrected at that audit (lines 17-22, 94-97); and round-10 evidence pointers under `/tmp/kake-r10/*`, which a fresh session cannot resolve (lines 76-80, 130, open at that audit). That audit did not spot-check the detector, the 33/33 or 60/60 measurements, or the CLI-behaviour claims. No round-21 non-author spot-check of round-10 admissions is recorded. The round-10 lane reports under `/tmp/kake-r10/` are session-scoped and were not opened for this section.

Known limits: retrospective; the original candidate ledger was not recorded; no live-state re-verification or domain recheck was performed; `probe-latest` and `probe-history` were not read; S019 is format authority only.
