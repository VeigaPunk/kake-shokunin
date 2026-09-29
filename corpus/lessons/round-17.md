# Round 17 — freshness: W6 caught; two suppression paths + one label defect closed

Axis worked: **freshness** (score held at 10 — the standing instrument caught a
live drift event and two of its own suppression paths).

## What happened

1. `node scripts/freshness-sweep.mjs` at 03:20:19Z exited 1 with a NEW §paths
   drift: `~/projects` (the lowercase twin of `~/Projects`) vanished between
   the r16 sweep (~02:4xZ) and 03:20Z → the descendant cite at
   `corpus/lessons/round-1-aggregator-audit.md:10` became an unannotated miss.
   **W6** of the `~/Projects` cleanup/prune regime (W1–W5 ledgered in r16).
   `~/DIRMAP.md:1,7,27` resolves the event: children from lowercase
   `~/projects` (r16 inode `101125103`) were absorbed into the existing capital
   root (inode `27238` before and after), then lowercase was removed; parent
   mtimes narrow the transition to 03:13:18–03:14:07Z. `magga-2`→`magga`
   also moved in-window. Fix: cite
   corrected to the canonical uppercase path (the round-1 report exists at
   `~/Projects/shokunin/.ufo/reports/round-1/web-properties-publishing.md`) +
   W6 note; `pathsMissSet` re-pinned 9→10 with `~/projects`.
2. The same run proved a coverage gap: `~/projects` was caught only because a
   descendant was *cited*. A `~/Projects` child with zero cites could vanish
   invisibly. Closed with pin `projectsChildrenSet` (36 entries) + P2b —
   **informational, never gating** (operator churn would false-positive a gate;
   reporting is enough, this round proved it).
3. Two latent suppression paths and one pin-classification defect closed:
   - `pathsFiles` was pinned as the bare count `38`; the evaluator requires an
     array → the file-set delta was inert-by-type since r16. Re-pinned to the
     live 39-file list (the added r17 lesson is entry 39);
     `set-delta files +0/-0` now prints.
   - `loadPins`'s `catch` degraded an unparsable pins file to silent defaults
     (all gates inert) — observed live this round when an edit dropped a `const`
     and the run emitted "gate pins absent" instead of failing. Now exits `2`
     (the documented invalid-input code) with the error on stderr.
   - Header classification named A5's six consumed plazir pins as
     “not evaluated” because they are absent from `DEFAULT_PINS`; they now sit
     in the evaluated-key set, while genuinely unused pins remain explicit.

## Verification

- `node scripts/freshness-sweep.mjs` post-fix: `VERDICT: DRIFT — §armed:
  plazir-live-source-gap (exit 1)` — only the expected open PQ-14 drift remains.
- `--selftest` 10/10 (including malformed pins → exit 2); `--offline` exit 0 with
  `set-delta files +0/-0` and `~/Projects children: 36 — set MATCH` printed.
- State guard: `~/Projects/webzites/state/` 33-file sha256 set byte-identical
  before/after every run (`/tmp/kake-r17/sentinel-{before,after}.sha`).

## Rule learned

A pin whose *type* doesn't match the evaluator is silently inert — same class
as a pin that's never read. When adding a pin, run once and grep the output for
the delta line; absence of the line = inert pin, regardless of the value.
