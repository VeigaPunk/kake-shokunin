source: Own-work scripts/probe-delta.mjs, ops-automation.md and historical 2026-09-28/29 probe-history results cited below; external history input absent after the 2026-10-12 prune. Metadata authority only: S019 in corpus/SOURCES.md, not re-verification of event counts.
verified-at: original evidence 2026-09-28 (round-10 final run, 76 rows, 6 events / 0 phantom); in-entry re-pins 2026-09-29 (r16, 78 rows) and absence annotations 2026-10-14 (r18) and 2026-10-19 (r20) — historical-not-live-reverified, not a domain recheck
recheck: on detector, history, or repo-script change — `node --check scripts/probe-delta.mjs; test -r ~/Projects/webzites/state/probe-history.jsonl && wc -l ~/Projects/webzites/state/probe-history.jsonl || echo ABSENT`; on ABSENT the operator must restore the history file and re-derive, or retire the run-derived event claims as historical record

# Probe-delta alerting — runnable violated[]-delta + coverage detection

Residual closed 2026-09-28 (round 10): "alerting on `violated[]` deltas (vs
the silent log) is undecided" (README known gap, flagged round 5). The
detection half is now a runnable artifact; alert **delivery** (notify/systemd
fan-out) stays with the webzites owner — this repo never mutates fleet state.

## The artifact

`scripts/probe-delta.mjs` (this repo):

```bash
node scripts/probe-delta.mjs            # table: events + coverage holes
node scripts/probe-delta.mjs --json      # machine output
node scripts/probe-delta.mjs --since 2026-09-27 [--hole-hours H]
```

Reads only `~/Projects/webzites/state/probe-history.jsonl`. Exit 0 = parsed <!-- r18 re-census 2026-10-14: ~/Projects/webzites/state/probe-history.jsonl absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
(this is a report, not a gate); 2 = unreadable input; 64 = bad flag.

## Rules (why naive diffing fails — measured)

- Row shape: `{at,total,ok,violated[],errors[]}`; **spot probes** (`probe
  <id>`) write `total:1` rows, **fleet sweeps** write `total:<universe>` rows
  (14→15→17→18 as rows registered).
- Diffing raw consecutive rows (L1 run + labrat replication, 2026-09-28):
  **42 events, of which 40 phantom** (precision 2/42) — a spot row's tiny
  `violated[]` makes every other fleet member look cleared, then re-entered
  on the next sweep. Naive recall 2/3: it also *missed* the real veigapunk-page
  exit (see ground-truth correction below).
- Correct rule (implemented): universe = running max of `total`; a row is a
  **full sweep** iff `total === universe`; ENTER/EXIT = `violated[]`
  membership delta between consecutive full sweeps; UNIVERSE = total growth
  between consecutive full sweeps (registration; membership delta is only
  partially observable — history rows record `violated[]`+`errors[]`, not the
  roster). **`full[0]` is the bootstrap baseline** (first sweep, `ok:0`):
  never a transition source — its 33s bracket against `full[1]` emits only
  bootstrap phantoms (9 EXITs in the pre-fix run; r10 reviewer rule).
- Coverage: gaps between consecutive full sweeps; hole = gap > 12h (2× the
  6h timer period). Baseline 2026-09-28: 76 rows → 66 full sweeps / 10 spot
  rows skipped; median gap 0.45h; **1 hole: 42.73h** (09-21T04:14:50 →
  09-22T22:58:23). **r16 re-pin (2026-09-29): 78 rows → 67 full / 11 spot,
  0 malformed; 66 full-sweep gaps, 21 in the 5–7h band** — row-relative
  counts rot every sweep; re-derive, never copy.
- Bookkeeping quirk (r10 reviewer): 11 rows (09-20T23:47:43 → 09-21T01:33:49)
  carry `total ≠ ok+|violated|+|errors|` (one unlisted non-ok row each) —
  never trust the summary to reconstruct the roster.

## Baseline output vs ground truth (2026-09-28 final run, 6 events, 0 phantom)

| derived event | ground-truth record | verdict |
|---|---|---|
| `charter-ghp` ENTER 09-27T06:22:33 (prev sweep 00:22:32) | ops-automation.md "entered violated[] 09-27T00:22→06:22" | match |
| `lucario` ENTER 09-27T16:38:27 + UNIVERSE 17→18 | ops-automation.md "entered 09-27T12:22→16:38, total 17→18, registration" | match |
| `veigapunk-page` EXIT 09-21T04:14:50 (prev sweep 03:32:06) | r5 record said "04:14→09-22T22:58" — **r5 was wrong** | see correction |
| xsnapshot-app: no events | constant full-sweep `errors[]` baseline | match (suppressed by design) |

**Ground-truth correction (raw rows, self-verified 2026-09-28):**
`veigapunk-page` was in `violated[]` at the 09-21T03:32:06.747Z sweep and
absent from the 09-21T04:14:50.502Z sweep; the 04:14:50 and 09-22T22:58:23
sweeps carry **identical `violated[]` sets — zero delta**. The r5 record had
used the 42.73h sampling hole's *endpoints* as the transition window.
Corrected in `ops-automation.md` (transition 03:32:06→04:14:50). Two
independent L2 derivations (planner, labrat) + raw-row read agree; the naive
differ misses this pair entirely (recall cost of spot phantoms).

## Companion CLI facts (operability audit, 2026-09-28)

- `webzites status` **exits 1 whenever the last probe had any
  violated/error row** (`src/cli.mjs:99`) — read its stdout, never its exit
  code, as a gate. (`probe`'s exit 1 is the documented tripwire; `status`'s
  is not in SKILL.md's step 1 — now noted there.)
- `scripts/kimi-surface.mjs` has **no `--help` verb** — the usage string
  prints via the default arm on any unknown verb, exit 64
  (`kimi-surface.mjs:1197-1198`).
- Invoke both from any cwd with absolute paths:
  `node ~/Projects/webzites/bin/webzites.mjs …`,
> *[r20 citation-local 2026-10-19: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*
  `node ~/Projects/webzites/scripts/kimi-surface.mjs …` (bare `webzites` is
> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*
  not on PATH; SKILL.md now carries the absolute form).

## Limits

- Events are bounded by sweep sampling: a transition is only *visible* at the
  next full sweep (the veigapunk-page publish click happened somewhere inside
  03:32→04:14, unresolvable further).
- **Merged-row caveat (revenger r10):** `grokbot tick` / `bots task` write
  MERGED fleet-sized rows — stale results carried for un-probed ids
  (`src/fleet.mjs:30-37` `mergeProbeResults`; callers `src/cli.mjs:289,647`)
  — and history rows carry no provenance, so the detector cannot distinguish
  a merged row from a fresh sweep. On the current 76-row file all 6 events
  match ground truth (no merged-row damage); re-derive with care once tick
  rows appear. Timer path writes fresh full sweeps only (`src/cli.mjs:78`,
  `:1002`); spot `total:1` rows come only from `probe <id>` (last
  2026-09-21T03:52Z).
- **Absence from `violated[]` is NOT proof of ok**: deficit rows
  (`ok+|violated|+|errors| < total`) carry skipped sites — 11 such rows, all
  in the 14/15/17-era (last 09-21T01:33:49); the 18-era has zero skipped.
  All 6 derived events sit on complete rows.
- `errors[]` is a different class from `violated[]` — catch-block failures
  (net/timeout/parse, `src/probe.mjs:79-81`), not semantic violations; the
  detector does not diff it by design (xsnapshot-app armed baseline).
- `UNIVERSE` membership delta is partial (only newly-violated/error members
  are listed); a registered row that lands `ok` is invisible in history.
  Era families on this file (r16, 78 rows): {1:11, 14:4, 15:1, 17:54, 18:8} — 67 full
  sweeps ✓ (r13's {1:10,…,18:7}/66 was the same file at 77 rows — re-derive).
- Marker-churn ENTERs (charter-ghp class) are indistinguishable from outages
  in history rows — resolve with `probe-latest.json` per-row `fail[]` detail.

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/probe-delta-alerting.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [probe-delta-alerting:c1] **HOLD** — The local detector artifact exists in the lane and parses under Node without a syntax error. Surface: `node --check /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/probe-delta.mjs`.
- [probe-delta-alerting:c2] **HOLD** — The canonical history input and the two cited webzites CLI paths remain absent at their documented ~/Projects/webzites locations. Surface: `test -e /home/vgpnk/Projects/webzites/state/probe-history.jsonl; test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs; test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs; test -e /home/vgpnk/Projects/webzites`.
- [probe-delta-alerting:c3] **HOLD** — The current CLI parses valid input into a non-gating report with exit 0, exits 2 for unreadable input, and exits 64 for an invalid flag. Surface: `node scripts/probe-delta.mjs --history /tmp/kake-r23-ProbeDeltaAlerting-DX8R/probe-history-fixture.jsonl --json; node scripts/probe-delta.mjs --json; node scripts/probe-delta.mjs --definitely-not-a-flag`.
- [probe-delta-alerting:c4] **HOLD** — The bare webzites command is not resolvable on PATH at verification time. Surface: `command -v webzites`.
- [probe-delta-alerting:c5] **HOLD** — SKILL.md contains the absolute webzites CLI invocation form; it is documented with an absent/historical-target annotation. Surface: `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:59`.
- [probe-delta-alerting:c6] **STALE** — The cited six-hour probe-timer cadence remains a current installed live schedule in the inspected system and user scopes. Surface: `systemctl show webzites-probe.timer --property=LoadState,ActiveState,UnitFileState,TimersCalendar; systemctl --user show webzites-probe.timer --property=LoadState,ActiveState,UnitFileState,TimersCalendar`. Correction: As of 2026-10-21, system and user systemd both report webzites-probe.timer as LoadState=not-found, and the checked system and user timer-file paths are absent; the cited six-hour cadence is not a current installed timer in those scopes.
- [probe-delta-alerting:c7] **UNVERIFIABLE** — The cited companion webzites source-line behaviors (status exit handling, kimi-surface behavior, merge semantics, probe-error handling and timer writes) are verifiable from the current source tree. Surface: `~/Projects/webzites/src/cli.mjs:99; scripts/kimi-surface.mjs:1197-1198; src/fleet.mjs:30-37; src/probe.mjs:79-81; src/cli.mjs:78,1002`. Unverifiable: The source tree cited for these line-specific behaviors has been pruned and is absent at ~/Projects/webzites, so no live source surface can decide whether the historical implementation details still hold.
- [probe-delta-alerting:c8] **UNVERIFIABLE** — The historical baseline and r16 re-pin row, sweep, event and coverage counts recorded in the unit are correct. Surface: `~/Projects/webzites/state/probe-history.jsonl`. Unverifiable: The canonical history input is absent and no copy was found under /home/vgpnk/Projects, so the historical row/event/coverage totals cannot be re-derived from the designated live surface now.
