# KakeR21.Lesson05 — round-17 historical Gate (C2)

## Behavior

- Target: `corpus/lessons/round-17.md`. Read in full before editing.
- Preexisting `## Gate` heading: **absent** (no line matched `^## Gate`). The append path was taken.
- Old line count: **56** (`wc -l`, and the read showed 56 lines ending in a newline).
- New line count: **88**. Change: pure EOF addition, one blank line then `## Gate` and its body (lines 57–88). Lines 1–56 are unchanged; the edit anchor was the pre-edit tag `#E0DC`, and the edit was a `PUT >56` insertion, not a rewrite.
- No live-state re-verification, no check re-run, no build/lint/test.

## Gate contents

- Clear label: "Retrospective round-21 reconstruction, not an original round-17 admission."
- Candidates C1–C8, drawn from the original sections (§What happened 1–3, §Verification, §Rule learned):
  - C1 W6 event attribution — admitted with qualification (exact actor/command unproven, per LOG r17).
  - C2 cite repair and `pathsMissSet` 9→10 — admitted with qualification (lane-run output, not re-run).
  - C3 `projectsChildrenSet` 36 + informational P2b — admitted with qualification.
  - C4 `pathsFiles` 38 → 39-file array — admitted with qualification.
  - C5 `loadPins` fail-closed exit 2 — admitted with qualification.
  - C6 six plazir pins moved into evaluated-key set — **unverified** (asserted; recorded output does not show the header line).
  - C7 33-file state guard sha identity — **unverified in this corpus** (evidence lives in `/tmp/kake-r17/`, not read).
  - C8 "inert-by-type pin" rule — admitted with qualification as a lesson-level rule.
- Axis outcome as recorded: freshness HOLD 10 (lesson title/§Verification; LOG r17; SCORECARD row 17, which labels r17/r18 figures legacy, not current proof) — admitted with qualification.
- Rejected: **gating P2b** only, with the reason recorded in the original lesson (§What happened 2: operator churn would false-positive a gate). All other rejected candidates: not recorded; none invented.
- Outside spot-check: **not recorded.** `corpus/lessons/round-20-verifier-spotcheck.md` covers round 20 only; LOG r17 lists in-round L2 dispatches (critic, connector, reviewer, scribe) whose artifacts are in `/tmp/kake-r17/`, which are lane-internal and not counted (QUALITY.md "Admission authority").

## Evidence basis

- Original lesson sections: `## What happened` 1–3, `## Verification`, `## Rule learned` (lines 1–56 as read).
- Round-21 lesson: `corpus/lessons/round-21.md` is the used-by entry of S019. It was **not present** in the corpus at write time (glob returned none), so no claim depends on it.
- S019 metadata/gate contract: `corpus/SOURCES.md:27`, tier A, scope = provenance metadata and recorded lesson gates; explicitly **not** verification of historical platform claims. The canonical anchor (`kimi-shokunin/.../protocol/CORPUS.md`) was not opened; the registry row is the cited evidence.
- Gate convention: `SCORECARD.md` Planned item 2 (`## Gate` heading on every lane-authored lesson; count command `grep -l '^## Gate'`). Pattern matched to `corpus/lessons/round-20.md` §Gate.
- Corroborating corpus: `LOG.md` round 17 (around lines 311–333 and 380–398); `SCORECARD.md` row 17; `corpus/knowledge/freshness-sweep.md` §r17 (lines 106–145).

## Findings and limits

- Gate completeness: all four required parts (candidates, admitted/unverified outcomes, rejected with reasons or "not recorded", outside spot-check status) are present. The gate records no independent review and no admission beyond what the original round recorded.
- Two candidates (C6, C7) are unverified and say so. Both are the weakest items; a future reviewer with the `/tmp/kake-r17/` artifacts could close C7, and the C6 header line could be read from the sweep output if it still exists.
- The file contains lane-era inline annotations (`r18`, `r20 citation-local`) that were preserved byte-for-byte. Those annotations are dated corrections by other rounds, not part of this gate.
- Live state is not verified. Paths named absent in the lesson (`~/DIRMAP.md`, `~/projects`, `~/Projects/webzites/state/`) are cited only as the lesson's own annotations.

## Tools

- No tools installed or upgraded.

## Out of scope

- No other lesson edited. No SCORECARD, LOG, QUALITY, SOURCES, README, or SKILL edits. No commits. No subagent dispatch (leaf member). No credential or auth files read.
