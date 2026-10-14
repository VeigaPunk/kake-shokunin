# Keeper timer inert — `webzites-keeper.timer` loaded, disabled, never fired

Round 12 (2026-09-28) operability axis. The daily keeper tick documented in
`corpus/knowledge/ops-automation.md` (r5) **has never run from systemd**: the
timer is loaded but disabled + inactive (dead), with zero journal entries. Every
observation below is a read-only `systemctl`/`journalctl`/file read — no timer
was enabled, started, or stopped by this lane (kake constraint; the decision is
filed for the operator, see the last section).

Sources: `systemctl --user status|show|list-timers`, `journalctl --user -u
webzites-keeper.service`, `~/.config/systemd/user/webzites-keeper.{timer,service}` <!-- r18 re-census 2026-10-14: ~/.config/systemd/user/webzites-keeper.service · ~/.config/systemd/user/webzites-keeper.timer absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
— captured 2026-09-28T22:18Z on this host (verbatim below; the L1 pack recorded
the same state at 22:14Z) — plus `/tmp/kake-r12/live/bots-report.out`,
`/tmp/kake-r12/live/bots-list.out`, `~/Projects/webzites/reports/keepers/`. <!-- r18 re-census 2026-10-14: ~/Projects/webzites/reports/keepers absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->

## Verbatim state (read-only, 2026-09-28T22:18Z)

```text
$ systemctl --user status webzites-keeper.timer   # rc=3
○ webzites-keeper.timer - Run the webzites keeper tick daily
     Loaded: loaded (/home/vgpnk/.config/systemd/user/webzites-keeper.timer; disabled; preset: enabled) <!-- r18 re-census 2026-10-14: ~/.config/systemd/user/webzites-keeper.timer absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
     Active: inactive (dead)
    Trigger: n/a
   Triggers: ● webzites-keeper.service

$ systemctl --user show webzites-keeper.timer
Triggers=webzites-keeper.service
ActiveState=inactive
UnitFileState=disabled
NextElapseUSecRealtime=        # empty
LastTriggerUSec=               # empty

$ systemctl --user is-enabled webzites-keeper.timer   # rc=1 → disabled
$ systemctl --user is-active  webzites-keeper.timer   # rc=3 → inactive
$ journalctl --user -u webzites-keeper.service        # "No entries" → never fired
$ systemctl --user list-timers --all                  # 3 listed: ai-usage.timer,
                                                      # webzites-probe.timer (next 21:00:59 -03),
                                                      # charter-scribe.timer — keeper absent
```

Contrast, same minute — the probe half is alive: `webzites-probe.timer` is
`enabled`, `active (waiting) since Mon 2026-09-28 02:55:28 -03`, next trigger
`21:00:59 -03`; `charter-scribe.timer` next `21:06:19 -03`.

Unit files (read 2026-09-28): `webzites-keeper.timer` = `OnCalendar=daily`,
`Persistent=true`, `[Install] WantedBy=timers.target`; `webzites-keeper.service`
= `Type=oneshot`, `ExecStart=…/bin/webzites.mjs grokbot tick --quiet`,
`SuccessExitStatus=1`, `WorkingDirectory=/home/vgpnk/Projects/webzites` — i.e. <!-- r18 re-census 2026-10-14: ~/Projects/webzites absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
the intended daily probe+reconcile+per-site-log round (`ops-automation.md:13`).

[INFERENCE] `Persistent=true` cannot rescue this: catch-up semantics require the
timer to be (re)started at some point; a disabled timer is never pulled in by
`timers.target`, so there is no missed trigger to catch up on. Observable basis:
zero journal entries, empty `LastTriggerUSec`, and absence from
`list-timers --all` over the unit's whole observed lifetime.

## Consequence chain

1. **Keeper logs are frozen at the 2026-09-21T03 manual round.** All 20
   `reports/keepers/grokbot-*.log.md` files exist; their newest entries are the
   mint-round bullets (`## 2026-09-21T03:32:50.726Z` … `- round 2026-09-21T03:28Z:
   probe=ok …` — e.g. the tail of `grokbot-charter-ghp.log.md`), and the newest
   file mtimes are `2026-09-21 00:32–00:47 -03` (= 03:32–03:47Z).
   `/tmp/kake-r12/live/bots-report.out` (report stamped 2026-09-28T22:14:48.869Z)
   shows `log=8d(round 2026-09-21T03)` on **19/21** rows and `log=never(?)` on
   `lucario`, which has **no log file at all** (r16 correction: `20/21` holds
   only under the widened `log=8d(` pattern — `grokbot-veigapunk-page.log.md`
   ends `log=8d(e2e fix)`; the live `bots report` still reads
   `19 log=8d(round` / `1 log=8d(e2e` / `1 log=never(?`, identical to this
   capture)
   (`reports/keepers/grokbot-lucario.log.md` absent — `ls` 2026-09-28).
   `turn=never` on **17/21** rows (counted: `grep -c 'turn=never'
   /tmp/kake-r12/live/bots-report.out` → 17; the four rows with a turn age —
   vault, veigapunk-page, ufofsd, plazir15 — stopped ~8d ago too).
   *(L1-pack reconciliation: "ALL keeper logs" is 20 of 21 — lucario has none;
   the pack's "turn=never on 13/21" is superseded by the capture count 17/21.)*
2. **No per-site keeper rounds happen.** probe+reconcile+append-per-site never
   runs on schedule; `webzites-probe.timer` covers only the probe leg
   (`ops-automation.md:12`). Corollary: any freshness gate on keeper logs
   (`bots report --stale N`, `src/cli.mjs:932`) would fail fleet-wide today —
   all existing logs are 8d old (labrat r12: `--stale 24` on uniformly 8d-old
   logs marks all 21 STALE and exits 1).
3. **The charter-ghp beat-pin story is a config-lag, not a keeper-timer block
   (round-12 critic refutation of the r7/r12-L1 framing).** The pin in
   `fleet/fleet.config.json` is `expect.marker: "2026-09-26 scribe beat"`
   (`fleet.config.json:256`); the live literal has churned to
   `2026-09-28 scribe beat (` (r7 + r12 live GET), so the row verdicts
   `violated` with `marker: absent` (`/tmp/kake-r12/live/status-json.out`).
   The marker's actual writer is the **charter-scribe**, not the keeper:
   `charter-scribe.timer` (enabled, active, 6h;
   `ExecStart=…/origin-work/ufo-fsd-alpha/scripts/charter-scribe/sync.mjs`) beat
   commit `61d0ce6 "charter: scribe beat 2026-09-28"` exists in the charter repo
   (`~/Projects/origin-work/charter-ufo-fsd`, 00:04Z push). And **no webzites <!-- r18 re-census 2026-10-14: ~/Projects/origin-work/charter-ufo-fsd absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
   code writes `fleet.config.json` at all** — `src/` contains only the
   `loadFleetConfig` reader (`src/fleet.mjs:7-11`); no verb can re-pin the
   marker, so PQ-12's r9 gate class "keeper config edit" (historical r9
   phrasing — r14 annotation: `corpus/knowledge/publish-queue.md:32` now
   reads "**operator config edit**", the r12 relabel) is **not implementable
   as coded**:
   the re-pin is a one-line human/operator edit of `fleet.config.json:256`
   (procedure: `SKILL.md:159-172` — r14: renumbered after SKILL grew). The keeper timer being dead changes none of
   that — r7's "queued for keeper" was wrong on both causality and mechanism.

## What still works (blast radius = exactly the keeper tick)

- `webzites-probe.timer` — enabled, active, 6h cadence; the state history shows
  the expected 00/06/12/18Z pattern (`ops-automation.md:8-19`, `:27`).
- `charter-scribe.timer` — active, 6h; next `2026-09-28 21:06:19 -03`. The
  scribe keeps writing new beats — precisely why the frozen pin keeps failing.
  **r12 addendum (critic N1):** the scribe's *push* leg is currently failing —
  last 3 ledger beats (06:05:59Z, 12:06:02Z, 18:06:19Z) are
  `pushed:false, push_blocked: "pull timed out after 60s"` with
  `scribe_route_failure: "grok-web empty or ceiling response"` (ledger
  `~/Projects/origin-work/ufo-fsd-alpha/.ufo/charter-scribe/ledger.jsonl`, <!-- r18 re-census 2026-10-14: ~/Projects/origin-work/ufo-fsd-alpha/.ufo/charter-scribe/ledger.jsonl absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  re-read 22:14Z; live marker still `2026-09-28 scribe beat (`). Until a push
  succeeds, the pin churn pauses anyway.
- Manual `grokbot tick` / `grokbot log` still work (they are what stamped the
  2026-09-21 logs) — but only when a human or a round runs them.

## Correction to r5 `corpus/knowledge/ops-automation.md`

r5 documented the keeper timer as part of the watching fabric — "## The fleet is
already being watched — do not re-probe blindly" with
`| webzites-keeper.timer | OnCalendar=daily | webzites grokbot tick --quiet | …`
(`ops-automation.md:8-13`) — read as "runs daily". The row's *intent* is
accurate; the *status* is not: it has never fired. Same correction for SKILL.md
step 1 ("The fleet is already instrumented … `webzites-keeper.timer` runs
`grokbot tick` daily", `SKILL.md:58-61` — pre-amendment r5 line numbers,
historical; the r12 amendment that replaced it lives at `SKILL.md:68-75` —
r14). Exact replacement text:
`/tmp/kake-r12/drafts/skill-amendments.md` P1 (landed r12).

## Operator decision — filed, not executed

`.ufo/l0-questions.md` (line `kake | round-12`): *"webzites-keeper.timer (daily
grokbot tick) is loaded but DISABLED+inactive … Enable the timer, or retire the
keeper-tick automation path? Kake will not toggle system state itself."*

- **Enable:** `webzites install --timer --enable` (documented refresh path,
  `ops-automation.md:15`) or `systemctl --user enable --now
  webzites-keeper.timer`. Post-enable check: `systemctl --user list-timers
  webzites-keeper.timer` shows a next trigger, and the first tick appends fresh
  `grokbot-*.log.md` entries.
- **Retire:** drop the "already being watched" framing for the keeper half;
  keeper rounds stay round-driven/manual.

Kake constraint (this round): no `systemctl enable/start` from the lane — state
toggling is operator-only. Zero writes were made by this verification: the
`state/*.json`+`state/*.jsonl` sha guard is byte-identical before/after
(`/tmp/kake-r12/state-before.sha` vs `state-after.sha` hash sets equal;
ExecutorDrafts re-check `/tmp/kake-r12/executor-now.sha`, sorted diff clean).

## r13 addendum (2026-09-28T22:4xZ read-only) — "churn paused" was imprecise

The r12 line above ("Until a push succeeds, the pin churn pauses anyway")
held only for the *scribe automation*: its ledger still shows
`pushed:false` beats (`pull timed out`), head `ee907f1`, 0 commits. But
between 18:32:06Z and 20:43:21Z the **human pushed 5 commits directly to
`origin/main`** of `~/Projects/origin-work/charter-ufo-fsd` <!-- r18 re-census 2026-10-14: ~/Projects/origin-work/charter-ufo-fsd absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
(`b74190e` bake gold snapshot → `d69dd22` og/twitter/hreflang → `0c767c2`
window sync → `b9db4b1` CORRECTION → `a8f1e2b` fixup), and Pages served
them live within ~30s of each push: live `index.html` sha
`0decd827…56716` == `raw.githubusercontent.com/…/a8f1e2b` (53,353B,
last-modified 20:43:51Z) — **deploy lag NONE**, superseding r6's
"bake not pulled" framing. The live beat line remains
`2026-09-28 scribe beat (` (verified 22:47Z) while the pin stays
`2026-09-26`, so charter-ghp stays `violated` — PQ-12 is still a one-line
operator edit of `fleet.config.json:256`. The local clone now lags origin
by 5 (`main` = `61d0ce6`) — `git pull --ff-only` before any local charter
work (the keeper-log self-heal pattern, ops-automation.md:82-84).
