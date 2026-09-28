# Ops automation — timers, history, bot fleet

Sources: `~/.config/systemd/user/webzites-{probe,keeper}.{timer,service}`
(read 2026-09-28), `~/Projects/webzites/state/probe-history.jsonl` (77 rows,
09-20→09-28; r13 re-read), `bin/webzites.mjs --help` (2026-09-28),
`reports/keepers/grokbot-*.log.md`.

## The fleet is already being watched — do not re-probe blindly

| unit | cadence | ExecStart | notes |
|---|---|---|---|
| `webzites-probe.timer` | `OnUnitActiveSec=6h`, `OnBootSec=5min`, `Persistent=true` | `webzites probe --all --quiet` | `SuccessExitStatus=1` — exit 1 means "probe ran and found violations", recorded normally; any other exit is a real failure |
| `webzites-keeper.timer` | `OnCalendar=daily` | `webzites grokbot tick --quiet` | probe+reconcile+append per-site keeper log; same `SuccessExitStatus=1` convention — **status (r12): loaded, DISABLED, inactive (dead), zero journal entries; has never fired.** Keeper logs frozen at 2026-09-21T03; keeper rounds are manual/round-driven only — `corpus/knowledge/keeper-timer-inert.md` |

Install/refresh: `webzites install [--timer] [--enable] [--force]` writes
these user units. **Before running your own `probe --all`, check
`state/probe-latest.json` age** — a <6h-old run is usually already there;
`webzites status` prints it.

## probe-history.jsonl — semantics and the transitions it recorded

77 rows 2026-09-20→09-28 (r12: line 77 = the r11 sanctioned `total:1` spot
row, 2026-09-28T21:31:26.591Z; no fleet row since 18:51Z). Format per row:
`{"at", "total", "ok", "violated":[ids], "errors":[ids]}`.
`total` counts probed rows (14→15→17→18 as rows were added); `ok` counts only
passes — `total - ok` = violated+errors. Single-row probes write
`total:1` rows — distinguish them from fleet runs before trend-reading.
**The 6h cadence is the timer's, not the file's** (round-9 review; r13
detector re-run: 66 full sweeps, 11 spot, 0 malformed on 77 rows) — of 77
rows only 66 are fleet runs; median inter-run gap 0.45h, only 20/65 gaps in
the 5–7h band, largest hole 42.7h (09-21T04:14→09-22T22:58). Treat
`probe-history.jsonl` as an event log whose sampling is bursty — never
back-calculate "time in violated" from row counts alone.

Observed transitions (all UTC, from the file itself):

- **`veigapunk-page` flipped violated→ok** between the 2026-09-21T03:32:06
  and 2026-09-21T04:14:50 full sweeps — the human publish click landed; a
  successful restore looks like the id silently leaving `violated[]`.
  *(r10 correction: the earlier "04:14→09-22T22:58" bounds were the 42.7h
  sampling hole's endpoints — those two rows carry identical `violated[]`
  sets, zero delta. Verified against the raw rows 2026-09-28 by
  `scripts/probe-delta.mjs`; see `corpus/knowledge/probe-delta-alerting.md`.)*
- **`charter-ghp` entered violated[]** between 09-27T00:22 and 09-27T06:22 —
  the scribe-beat marker churned (PQ-12) while the site stayed up; a marker
  FAIL appears identical to an outage in history rows — resolution needs
  `probe-latest.json` per-row detail (`fail[]` reasons), not the summary.
- **`lucario` entered violated[]** between 09-27T12:22 and 09-27T16:38 —
  the *row* was added to the config mid-day (total 17→18); a new row
  appearing already-violated is a registration event, not a regression.
- `xsnapshot-app` has been in `errors[]` on **every full sweep since
  2026-09-21T01:34:20Z** (present also on the 09-20T23:47:10 bootstrap row;
  absent on 11 earlier full sweeps, last 09-21T01:33:49) — intended NXDOMAIN
  tripwire, PQ-7. **A constant errors[] entry is armed-tripwire baseline,
  not noise to fix** — but judge constancy on full sweeps only: spot
  (`total:1`) rows trivially omit every other site.
- `ufo-fsd-kimi-pro` oscillated errors→ok on 09-21 and 09-26/27 — transient
  FC-ingress fetches; single-run errors on that row are flake, two+
  consecutive are signal.

## CLI surface beyond probe/reconcile (`bin/webzites.mjs --help`, verbatim)

| verb | what it does | gate |
|---|---|---|
| `status [--json]` | last probe results from `state/probe-latest.json` | free |
| `map` | regenerate `docs/FLEET-MAP.md` | free |
| `auth [--json]` | surface matrix: CDP, grok/kimi tabs, grok CLI, grok-bot app, origin | free |
| `lease acquire\|release\|status --owner N --ttl-ms` | serializes the shared burner chrome machine-wide | free; release in `finally` |
| `install [--timer --enable --force]` | writes the systemd user units above | mutates systemd |
| `speedrun record\|report\|post\|prep` | telemetry → run JSON/curve/manifest → X draft | `prep --write` stages; post only *prints* (never posts) |
| `ask "<prompt>" [--json]` | one-shot `grok -p` CLI turn, tools off | free |
| `grokbot start [--dry-run]` | spawn Grok Bot app on Hyprland ws 3, silent/unfocused | GUI lane |
| `grokbot log <id> --note "…"` | append dated keeper entry | free write |
| `grokbot reconcile [ids]` | live bytes vs `sourceDir/index.html` | free |
| `grokbot tick [ids] [--digest]` | one keeper round: probe+reconcile+log per site | free |
| `grokbots [--check\|--status]` | keeper roster health: cards, registry drift, last probe | free |
| `bots list` / `bots run` / `bots task` / `bots mint` / `bots digest` / `bots report` | per-site grok-bot keeper fleet: card+wrapper per registry row; `task`/`digest` probe + bot-summarize verdicts; `mint` idempotent repair | never publishes; `digest`/`task --log` write keeper logs |

## Keeper log format (`reports/keepers/grokbot-<id>.log.md`)

Daily tick appends `## <ISO ts>` + `- tick: probe=<verdict>
reconcile=<verdict>`; manual `grokbot log --note` adds freeform entries
(e.g. 2026-09-21 charter-ghp: sourceDir 10 commits behind origin,
`git pull --ff-only`, re-reconcile=match — the keeper self-heals source
lag without pushing). Read the site's log before editing its `sourceDir`:
recent `reconcile=drift` + no note = live-vs-source problem; drift + a
"git pull" note = the pull already resolved it.

## r13 re-verification (2026-09-28T22:4x–22:5xZ, read-only)

- **probe timer healthy, cadence confirmed:** `webzites-probe.timer` enabled
  + `active (waiting)`; today's triggers 06:00:36Z, 12:00:53Z, 18:01:09Z
  (history lines 73–75), next 2026-09-29T00:00:59Z. The 18:51:26.128Z
  full-universe row (line 76) is an **off-cadence manual `probe --all`**
  (kake round-3 vintage; timer rows land :00:4x–:01:1x) — do not cite it as
  the timer's work. All three full rows today carry the identical
  12 ok / 5 violated / 1 error set; an independent 18-curl live replication
  at 22:50Z reproduced it with **0 verdict diffs** (pattern stable, not
  stale). Line 77 (21:31:26.591Z, `total:1`) = the r11 sanctioned
  `probe ds4cc-com` spot row.
- **keeper timer unchanged from r12:** disabled + inactive(dead),
  `LastTriggerUSec` empty, zero journal lines across 26 recorded boots —
  has still never fired. L0 question (kake round-12) still unanswered at
  22:5xZ.
- **detector upkeep:** `node scripts/probe-delta.mjs` on 77 rows = 6 events
  / 0 phantom (r10 baseline holds on the +1 spot row; universe rule
  suppressed it, naive diff would have fabricated 6 EXIT phantoms).
- **freshness-read rule (r13 forensics):** read `probe-latest.json`'s `at`
  field, never its mtime — after the r11 clobber + manual restore, mtime
  21:31:45Z vs `at` 18:51:26Z (2h40m apart); birth-time equals the clobber
  instant, and the restored bytes are sha-identical to the r11 backup
  (`8c5bb8ca…b6591e`).
