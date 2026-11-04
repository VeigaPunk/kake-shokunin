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
   > *[r20 citation-local 2026-10-19: `~/DIRMAP.md` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*
   `~/projects` (r16 inode `101125103`) were absorbed into the existing capital
   > *[r20 citation-local 2026-10-19: `~/projects` absent — gone in W6, the 2026-09-29 03:13–03:14Z lowercase-tree consolidation; historical record, not an executable instruction.]*
   root (inode `27238` before and after), then lowercase was removed; parent
   mtimes narrow the transition to 03:13:18–03:14:07Z. `magga-2`→`magga`
   also moved in-window. Fix: cite
   corrected to the canonical uppercase path (the round-1 report exists at
   `~/Projects/shokunin/.ufo/reports/round-1/web-properties-publishing.md`) +
   W6 note; `pathsMissSet` re-pinned 9→10 with `~/projects`.
   > *[r20 citation-local 2026-10-19: `~/projects` absent — gone in W6, the 2026-09-29 03:13–03:14Z lowercase-tree consolidation; historical record, not an executable instruction.]*
2. The same run proved a coverage gap: `~/projects` was caught only because a
   > *[r20 citation-local 2026-10-19: `~/projects` absent — gone in W6, the 2026-09-29 03:13–03:14Z lowercase-tree consolidation; historical record, not an executable instruction.]*
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
- State guard: `~/Projects/webzites/state/` 33-file sha256 set byte-identical <!-- r18 re-census 2026-10-14: ~/Projects/webzites/state absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  before/after every run (`/tmp/kake-r17/sentinel-{before,after}.sha`).

## Rule learned

A pin whose *type* doesn't match the evaluator is silently inert — same class
as a pin that's never read. When adding a pin, run once and grep the output for
the delta line; absence of the line = inert pin, regardless of the value.

## Gate

> **Retrospective round-21 reconstruction, not an original round-17 admission.** Written by round-21 wave w1 (Lesson05) from this lesson's own sections (§What happened 1–3, §Verification, §Rule learned) and the S019 registry row in `corpus/SOURCES.md`. It restates what the round-17 record supports. It re-runs no check, re-verifies no live state, and adds no admission or independent review that the original round did not record.

Candidates considered (from the original sections):

- **C1 — W6 event attribution:** the lowercase projects tree was consolidated into the capital Projects tree then removed in the recorded 2026-09-29 window. Outcome: historically documented timing/inode evidence, not an original admission. The exact actor and command remain unproven.
- **C2 — cite repair and pin move:** the citation was corrected to the surviving fleet report; `pathsMissSet` moved 9→10 to include the removed lowercase tree. Outcome: historical measurement in the lesson's Verification section; no current-state recheck.
- **C3 — child-coverage pin:** `projectsChildrenSet` (36 entries) plus P2b, informational and never gating. Source: §What happened 2. Outcome: **admitted with qualification.** §Verification records `~/Projects children: 36 — set MATCH`; the informational-only classification is the lane's stated design choice.
- **C4 — `pathsFiles` type fix:** bare count `38` replaced by the 39-file array so `set-delta files +0/-0` prints. Source: §What happened 3, first bullet. Outcome: **admitted with qualification.** §Verification records the offline run printing the delta line.
- **C5 — `loadPins` fails closed:** an unparsable pins file exits `2` with the error on stderr instead of silent defaults. Source: §What happened 3, second bullet. Outcome: **admitted with qualification.** §Verification records `--selftest` 10/10 including malformed pins → exit 2, and one live observation of the old silent path.
- **C6 — header classification of six plazir pins:** moved into the evaluated-key set. Source: §What happened 3, third bullet. Outcome: **unverified.** The lesson asserts it, but its recorded verification output does not show the header line. `corpus/knowledge/freshness-sweep.md:64-65` restates the fix without output. Not re-checked here.
- **C7 — state guard:** `~/Projects/webzites/state/` 33-file sha256 set byte-identical before and after every run. Source: §Verification, third bullet. Outcome: **unverified in this corpus.** The evidence is `/tmp/kake-r17/sentinel-{before,after}.sha`, outside the repository; this reconstruction did not read it. The lesson's own r18 annotation records that the path is absent today; that is cited as recorded, not re-verified.
- **C8 — rule learned:** a pin whose type does not match its evaluator is silently inert; check the delta line after adding a pin. Source: §Rule learned. Outcome: **admitted with qualification** as a lesson-level rule. It generalizes C4's recorded evidence and is not a separate measurement.

Axis outcome as recorded: freshness **HOLD 10** (lesson title and §Verification; `LOG.md` round 17; `SCORECARD.md` row 17). `SCORECARD.md` labels round-17/18 figures as legacy assessments, not current proof, so this outcome is admitted with qualification.

Rejected candidates:

- **Gating P2b** (making `projectsChildrenSet` a gate): rejected in the original lesson, §What happened 2. Reason as recorded: operator churn would false-positive a gate; reporting is enough.
- Any other rejected candidate: not recorded. No other rejection appears in the original sections, `LOG.md` round 17, or `SCORECARD.md` row 17, and none is invented here.

Outside spot-check: not recorded. The corpus holds no independent non-author spot-check of round 17. `corpus/lessons/round-20-verifier-spotcheck.md` covers round 20 only. `LOG.md` round 17 lists in-round L2 dispatches (critic, connector, reviewer, scribe) whose artifacts sit under `/tmp/kake-r17/`. Those are lane-internal and are not counted here, consistent with the Admission authority row in `corpus/QUALITY.md`.

Basis and contract:

- Original sections cited: `## What happened` items 1–3, `## Verification`, `## Rule learned`.
- Round-21 lesson: `corpus/lessons/round-21.md` is the lesson named as S019's used-by entry. It was not present in the corpus when this section was written, so no claim here depends on it.
- Metadata and gate contract: S019 in `corpus/SOURCES.md:27` (canonical Shokunin corpus contract, tier A). Its scope is provenance metadata and recorded lesson gates (candidates, admissions, rejections, spot-check state), explicitly **not** verification of historical platform claims. The canonical anchor was not opened by this reconstruction; the registry row is the cited evidence.
- Gate convention: `SCORECARD.md` Planned item 2 requires an appended `## Gate` heading on every lane-authored lesson.
- Live state: nothing was re-verified. Paths named as absent (`~/DIRMAP.md`, `~/projects`, `~/Projects/webzites/state/`) are cited only as the lesson's own dated annotations.
