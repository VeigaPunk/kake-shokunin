# Lesson — round 18 (2026-10-14): OMP/ufo-fsd re-census — W7 mega-prune caught standing

Cites: LOG.md round-18; `scripts/freshness-sweep.mjs`;
`corpus/knowledge/freshness-pins.json`; run artifacts `/tmp/kake-r18/`
(`before.json`, `before.out`, `after.out`, `after-offline.out`, `p.json`).

## The catch

The standing sweep was run at round open (2026-10-14T12:40Z) and exited 2 —
its biggest catch yet. Sometime between r17 (2026-09-29) and today the
`~/Projects` tree was pruned/migrated ("W7"): **33 of 36 pinned children
removed, 11 added.** Gone: `webzites` (the lane's instrument host — CLI,
fleet registry, probe history, keeper reports), `ds4cc-marketplace`,
`plazir-15-site`, `lucario`, `origin-work` wholesale (charter-ufo-fsd,
open-bug-bounties, and the ufo-fsd-alpha copy the corpus cited), plus the
`webzites-{probe,keeper}` systemd units, `~/DIRMAP.md` <!-- r18 re-census 2026-10-14: ~/DIRMAP.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->, and every keeper
report. `ufo-fsd-alpha` now lives directly at `~/Projects/ufo-fsd-alpha`
(same repo, HEAD `964f443e`) — but **without** `.ufo/charter-scribe/` or a
`ledger.jsonl`, so the scribe-ledger cite is dead, not moved.

## What the instrument proved before any repair

- `§paths`: 36 unannotated misses + 45 beyond the pinned miss set — the
  set-delta gate caught the class it was built for.
- `§history`: unreadable `probe-history.jsonl` failed closed at exit 2.
- `§armed` still ran the parts that can run: PQ-12's armed watch FIRED —
  live marker moved `2026-09-26` → `2026-09-30 scribe beat` (sha
  `7c243a1d…`, 53 660 B) with `fleet.config.json` gone, so the CHURN-AGAIN
  reading is "edit landed while the registry file was unverifiable". PQ-5
  still `PENDING` 404/13 409B/`93ddca9a…`; ds4cc sitemap still `PRE-PUSH`
  404/9 379B.
- `--selftest` regressed 10/10 → 8/10: fixture A cited `~/Projects/
  > *[r20 citation-local 2026-10-19: `~/Projects/webzites` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*
  webzites/fleet` as its guaranteed-resolving path — a fixture that
  trusted the world, which is exactly what fixtures must not do.

## Repairs (this commit)

- 63 cite lines across 22 files carry an inline `<!-- r18 re-census … -->`
  erratum marking each gone path absent and keeping the cite as a
  historical record (append-only; no claim deleted). Three multi-token /
  multi-line cites were repaired by hand after the blanket annotation
  broke brace-list grammar.
- `freshness-pins.json` re-measured in one pass: `pathsMissSet` 10 → 55,
  `projectsChildrenSet` 36 → 14, `charterGhpPin`/`-LiveSha`/`-ChurnAfter`
  re-baselined to the observed 2026-09-30 marker; new
  `probeHistoryAbsent: true` declares the suspended §history source.
- `freshness-sweep.mjs`: `pins.probeHistoryAbsent` turns a pin-declared
  absent history source into `SUSPENDED` (loud skip, listed under
  `skipped(...)`, never counted as pass) instead of unreadable-input
  exit 2. Selftest re-anchored to `~/Projects/ufo-fsd-alpha`.

## Carried debt (named, per term)

- **PQ-2** — `~/Projects/ds4cc-marketplace` gone; gate reads `ANOMALY`,
  exit 1 by design. Unblock: repo restored or PQ-2 declared dead.
- **PQ-14** — `~/Projects/plazir-15-site` gone; gate `ANOMALY` +
  sitemap `NOT-EVALUATED`. Unblock: source repo restored.
- **§history** — suspended; needs a re-anchored probe-history source or a
  declared end of the timer era. Unblock: webzites tree restored or
  `KAKE_PROBE_HISTORY` pointed at a surviving copy.

Final state: bare run exit 1 (DRIFT = the two unresolvable armed gates,
correct and loud), `--offline` exit 0, `--selftest` 10/10.

## Gate

Retrospective round-21 reconstruction, not original admission. The 2026-10-14 round-18 record carries no gate section: neither this lesson nor the `LOG.md` round-18 entry (starts line 400) records an admit/reject ledger. This section is a label-only reconstruction from the lesson's own sections, the LOG round-18 entry, and later on-disk references. No live state was re-verified, no check was re-run, and no `/tmp/kake-r18/` artifact was opened.

Original sections cited: `## The catch` (lines 7-19), `## What the instrument proved before any repair` (21-35), `## Repairs (this commit)` (37-52), `## Carried debt (named, per term)` (53-61), final-state line (63-64).

Round-21 lesson: `corpus/lessons/round-21.md` is not on disk at read time (`corpus/lessons/` lists round-1 through round-20 only). The round-21 contract is `.ufo/waves/round-21/wave1-spec.json` (Lesson06 item; reportDir `.ufo/waves/round-21/w1`).

S019 metadata/gate contract: the round-21 wave spec states "Reference S019 for metadata contract (L1 will register canonical CORPUS.md opened this round); source must retain entry-specific evidence, S019 is metadata authority not platform authority." The canonical text located at read time is `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md`: lines 18-20 (`lessons/round-<N>.md` carries `## Gate`: candidates, admitted, rejected with reasons, spot-check result); lines 112-115 (rule 1: the round lesson's `## Gate` records URL, access date, and a ≤25-word quote for each new SOURCES row); lines 162-165 (knowledge entries open with the provenance trio). Also `LEARNING.md` lines 42-46 (at least one admit and one reject spot-checked from outside) and lines 71-73 (lesson `## Gate` content). No S019 row exists in `corpus/SOURCES.md` at read time; this section cites none and adds none (L1 owns SOURCES). This lesson is not a knowledge entry, so this gate carries no `verified-at:` field.

### Candidates and historically supported outcomes

| # | Candidate (original section) | Outcome | Basis |
|---|---|---|---|
| C1 | Standing sweep exit 2 at round open; W7 prune removed 33 of 36 pinned children and added 11 (`## The catch`, lines 9-19) | admitted with qualification | The lesson and LOG round-18 item (1) record the same counts and exit. Internally consistent: 36 − 33 + 11 = 14, matching LOG `36 → 14`. Qualification: `/tmp/kake-r18/` artifacts are not in the repo and were not opened here. |
| C2 | §paths: 36 unannotated misses + 45 beyond the pinned set (lines 23-24) | admitted with qualification | Same figures in LOG round-18 item (1). 10 + 45 = 55 matches the later `pathsMissSet` 10→55 repair (line 45). Qualification: not re-measured here. |
| C3 | §history: unreadable `probe-history.jsonl` fails closed exit 2 (line 25); pin-declared absent source becomes `SUSPENDED` (lines 48-51) | admitted with qualification; superseded in part | Round 19 narrowed suspension to the canonical default only; an explicit bad override stays exit 2 (`round-19-recensus.md:6-18`, Landed change items 1 and 3). The round-18 record stays as historical. |
| C4 | §armed PQ-12 watch fired: marker `2026-09-26` → `2026-09-30 scribe beat`, `fleet.config.json` gone (lines 26-31) | unverified as interpretation | Observation recorded in the lesson and LOG round-18 item (1). The reading "edit landed while the registry file was unverifiable" is the lesson's own interpretation; no outside check exists. |
| C5 | Selftest 10/10 → 8/10: fixture A trusted the vanished webzites fleet directory (lines 32-35) | documented finding; repaired | Cause named in the lesson; repaired by re-anchoring to ufo-fsd-alpha (lines 48-51). Round 19 made the selftest hermetic and removed the live-host-tree dependency. |
| C6 | 63 cite lines across 22 files carry inline `r18 re-census` markers; 3 hand-repaired (lines 39-43) | admitted with qualification | Qualification 1: LOG round-18 item (2) says "21 corpus md errata files" plus `SCORECARD.md` and `LOG.md`; the 22-file count is not reconciled here. Qualification 2: round-19's dead-path sweep found `keeper-timer-inert.md:91` and `publish-queue.md:167` unmarked and present-tense (`round-19-recensus.md:50-60`); no repair is recorded in round 18 or round 19. |
| C7 | `freshness-pins.json` re-measured in one pass: `pathsMissSet` 10→55, `projectsChildrenSet` 36→14, `charterGhp*` re-baselined, `probeHistoryAbsent: true` (lines 44-47) | admitted with qualification | A re-measurement, not a re-pin to green: bare run stays exit 1 (line 63). Later: round 19 found `freshness-sweep.md:43-53` still quotes pre-r18 pin literals as the current baseline (`round-19-recensus.md:48`). The round-20 Gate rejects re-pinning to recover green (`round-20.md`, `## Gate — round-20 resume`, lines 182-196); round 18 did not reach green, so that rejection is noted, not applied. |
| C8 | Verdicts: bare exit 1 (`DRIFT`, PQ-2 ANOMALY, plazir-gate-anomaly), `--offline` exit 0, `--selftest` 10/10 (lines 63-64) | unverified here; historical observation | Same verdict lines in LOG round-18 item (3). Not re-run. Later rounds report different selftest counts (round 19: 13/13, `round-19-recensus.md:22`); the round-18 values are historical. |
| C9 | Carried debt: PQ-2 and PQ-14 ANOMALY, §history SUSPENDED, each with an unblock (lines 55-61) | carried, not closed | Round 19: "Do not re-pin to silence them" (`round-19-recensus.md:34`). Round 20 names the same debt (`round-20.md`, `## Named debt and unblock`, line 62). |

### Rejected candidates (only those documented)

- Not recorded. The round-18 lesson and LOG round-18 entry name no rejected alternative. "Correct and loud" (line 63) states the outcome of the bare exit 1; it is not recorded as a rejected candidate and is not restated here as one.

### Outside spot-check

Not recorded for round 18. No non-author admit or reject sample of round-18 gate decisions exists in this lesson, the LOG round-18 entry, or `corpus/lessons/round-20-verifier-spotcheck.md` (round 20 only). Material touching round-18 outputs: `round-19-recensus.md` `## Independent audit erratum` (lines 42-44), `### Audit detail` (46-48), and `### Dead-path sweep` (50-60), all dated 2026-10-14, author not named in the file. These audit round-19 changes and round-18 marker coverage; they are not a spot-check of round-18 admit/reject decisions and are not counted here as agree or disagree.

### Gate completeness

Gaps: no admit or reject row is recorded for C1-C9; no outside spot-check of round-18 decisions exists; the 22-file (lesson) and 21-file (LOG) counts are unreconciled; `keeper-timer-inert.md:91` and `publish-queue.md:167` are a round-19 finding with no recorded repair; C4 and C8 are unverified. Nothing in this section changes the original sections, and no live state was re-measured.
