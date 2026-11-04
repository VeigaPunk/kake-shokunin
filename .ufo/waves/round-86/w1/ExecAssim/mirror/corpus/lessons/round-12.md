# Round 12 — every free-read is now live-proven; two automation myths fell

LOG.md round 12. Axis: operability (the r11 plan's residual branch —
probe-latest 3.4h fresh at open, under the 6h re-probe threshold).

## What the round proved

1. **The last 4 free-read verbs are live-proven write-free.**
   `status --json` / `grokbots --check` / `bots list` / `bots report` ran on
   the real repo (exits 0/1/0/1); the 31-file `state/` sha guard is
   byte-identical before/after (`/tmp/kake-r12/live/`,
   `state-before.sha` == `state-after.sha`; re-run by executor + critic, same
   result). Exit-1 predicates pinned: bots-report gaps
   `!registered || !cardPresent || (!queued && !wrapperPresent)`
   (`src/cli.mjs:935`); stale only with `--stale` (`:836-839`, `:932`);
   `status --json` / `bots list` exit 0 unconditionally.

2. **Myth 1 fell: "the fleet is already instrumented."** The daily
   `webzites-keeper.timer` is loaded but **disabled + inactive (dead), zero
   journal entries — it has never fired**; keeper logs are frozen at the
   2026-09-21T03 mint round (20/21 files; lucario has none; `turn=never` on
   17/21). Only the 6h probe timer and charter-scribe timer run.
   `corpus/knowledge/keeper-timer-inert.md`; enable-vs-retire filed to L0.

3. **Myth 2 fell: "the keeper will re-pin the charter-ghp marker."** The
   marker's writer is the active 6h charter-scribe (beat commit `61d0ce6`);
   the probe FAIL is `fleet.config.json:256` pin lag — and **no webzites code
   writes `fleet.config.json`** (only the reader `src/fleet.mjs:7-11`), so
   PQ-12 is a human/operator config edit, not keeper work. Bonus finding:
   the scribe's push leg is failing (3 beats `pushed:false`,
   `push_blocked: "pull timed out after 60s"` — ledger re-read 22:14Z), so
   marker churn is currently paused.

4. **Roster arithmetic pinned:** fleet.config 21 / grokbots registry 20 /
   probe snapshot 18. 18-of-21 is by-design url filtering (`src/cli.mjs:75`),
   not a coverage hole; the wedge is `lucario` (fleet row 09-27, no registry
   row/card/wrapper/log — `grokbots --check` exit 1). L0 question filed
   (mint or prune).

5. **The r11 F1 patch proposal was itself wrong.** Guard
   `positionals.length > 0 && !flags.all` still clobbers on
   `probe <id> --all` (selection ignores `--all`, which is parsed but never
   read). Corrected one-line merge patch replica-verified (18 rows preserved,
   merged `total:18` history, `node --check` clean) — filed as
   `corpus/handoffs/cmdProbe-merge-fix.md`; webzites source stays untouched
   (operator rule).

## Lesson

- **Verify the automation claim at runtime, not at the unit file.** Two rounds
  of docs said "keeper timer runs daily"; one `systemctl --user status` +
  empty `journalctl` proved it never ran. A documented unit is intent, not
  state — pin runtime state with the read-only verbs before relying on any
  scheduled behavior (`bots report` log ages are the cheap tell).
- **Every handoff patch needs its refutation pass.** The r11→r12 guard fix
  came from a replica edge run (`probe <id> --all`), not from reading the
  proposal again. Ship handoffs with a test recipe that includes the edge the
  patch author did not think of.

Evidence: `/tmp/kake-r12/` (live/, drafts/, critic.md, reviewer.md,
labrat.md, revenger-patch.md + revenger-replica/, scout-verbs3.md,
connector.md, sentinel.md, scribe-report.md); LOG.md round 12.

## Gate

**Retrospective round-21 reconstruction, not the original round-12 admission.** Appended in round 21 under S019 (`corpus/SOURCES.md:27`: provenance metadata and recorded lesson gates recording candidates, admissions, rejections and spot-check state; not platform authority). The original text (lines 1-62, base `5009eca`) contains no `## Gate`. Outcomes below are reconstructed from this lesson's own sections (`## What the round proved` lines 6-46, `## Lesson` lines 48-58, evidence lines 60-62) and the in-tree records cited. They are not new admissions, not a re-verification, and not a live-state re-check: no round-12 runtime fact was re-measured in round 21. The round-21 lesson (`corpus/lessons/round-21.md`) was not present at read time; it is cited by its planned path only. Metadata prefix lines are outside this gate's scope.

Candidates:

- **C1** (§1) `status --json`, `grokbots --check`, `bots list`, `bots report` are write-free on the real repo, exits 0/1/0/1; 31-file `state/` sha guard unchanged.
- **C2** (§2) "The fleet is already instrumented": myth; `webzites-keeper.timer` loaded, disabled, inactive, zero journal entries.
- **C3** (§3) "The keeper will re-pin the charter-ghp marker": myth; marker writer is charter-scribe; PQ-12 is an operator config edit; scribe push leg failing.
- **C4** (§4) Roster arithmetic 21 / 20 / 18; `lucario` is the wedge.
- **C5** (§5) r11 F1 guard proposal wrong on `probe <id> --all`; corrected one-line patch filed as handoff, not shipped.
- **C6** (Lesson, bullet 1) Verify automation claims at runtime, not at the unit file.
- **C7** (Lesson, bullet 2) Every handoff patch needs a refutation pass.

Historically supported outcomes:

- **C1: admitted with qualification.** Recorded at `corpus/knowledge/free-read-verbs.md:338-348,362-406,417-423` and the round-12 operability row in `SCORECARD.md`. Qualification: `/tmp/kake-r12/` is absent at round-21 read, so the replay cannot be inspected here; the "re-run" was same-round L2 seats (executor, critic), not an outside check; `src/cli.mjs` pins were not re-checked.
- **C2: admitted with qualification.** Dated read 2026-09-28T22:18Z (`corpus/knowledge/keeper-timer-inert.md:3-16`). Later in-tree notes repeat the state as history (`corpus/knowledge/ops-automation.md:14,111-114`); not re-verified in round 21.
- **C3: admitted with qualification for the classification; unverified for the negative sub-claim.** Config-lag and human-edit classification and the failing push leg are recorded (`corpus/knowledge/keeper-timer-inert.md:83-109`; `corpus/knowledge/publish-queue.md:32`). "No webzites code writes `fleet.config.json`" rests on a `src/fleet.mjs:7-11` read; `SKILL.md:30` records `fleet.config.json` absent after the 2026-10-12 prune. Unverified in round 21.
- **C4: admitted with qualification for counts; line anchors unverified.** Universes 18/20/21 recorded at `corpus/knowledge/free-read-verbs.md:408-411` and `corpus/README.md:34`. `src/cli.mjs` anchors not re-checked in round 21.
- **C5: admitted with qualification.** Refutation and corrected patch recorded at `corpus/knowledge/free-read-verbs.md:425-434` and `corpus/handoffs/cmdProbe-merge-fix.md:24-73`. Patch not shipped (webzites source read-only to kake). Replica directory `/tmp/kake-r12/revenger-replica` absent at round-21 read; replica result unverified here.
- **C6, C7: process guidance, no separate admission recorded.** Lesson text only (`round-12.md:50-58`). Whether either was promoted to `corpus/QUALITY.md` is not recorded: no round-12 reference was found in `corpus/QUALITY.md` at round-21 read.

Rejected candidates (documented only):

- C2 framing "the daily keeper ticks": refuted by the systemd read (`round-12.md:18-20`; `corpus/knowledge/ops-automation.md:14`).
- C3 framing "the keeper re-pins": refuted by the critic's config-lag refutation (`corpus/knowledge/keeper-timer-inert.md:83-87`).
- C5 r11 F1 guard: refuted by the `probe <id> --all` replica edge run (`round-12.md:40-46`).
- Two wrong citations and two count errors caught and fixed before landing (`SCORECARD.md:95`, round-12 row). Reason: reviewer/critic/scribe checks.
- Any other rejected candidate: not recorded.

Outside spot-check: not recorded. Round-12 evidence cites same-round executor, critic, reviewer and labrat seats (`corpus/knowledge/free-read-verbs.md:417-423`); none is a non-author outside spot-check. `corpus/lessons/round-20-verifier-spotcheck.md` covers round 20 only.
