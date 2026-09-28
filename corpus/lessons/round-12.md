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
