# ReviewSeatBoundsSweep — freshness-sweep.mjs flag/network table (round 30, wave 1)

Static source review only. The script was NOT run in any mode (round-30 bound).
No shell commands beyond one checksum batch (exit 0). No installs performed.

Reviewed at working tip; sha256 of the reviewed bytes:
- scripts/freshness-sweep.mjs `a1aa79d114093cc5b663e811e86a20a57bf37357dd8a3598c9e02084770d8d8b`
- scripts/probe-delta.mjs `aa4fb2a5042996472e2b054f35ab229d0e7c7b80ed75e42c80722c27b6d02bbf` (grep-only posture check)
- scripts/live_snapshot.py `3638891d4107a57b5d3c919da41a33f3a0c97d15db257d1e9070e00f3b462a20` (grep-only)

All line refs below are `scripts/freshness-sweep.mjs` unless prefixed `pins.json:` =
`corpus/knowledge/freshness-pins.json`.

## Flags (parseArgs :137-158; SECTIONS :129 = paths, history, armed, plazir)

| Flag | Line | Effect |
|---|---|---|
| `--json` | :141 | output format only |
| `--offline` | :142 | strips every fetch/ls-remote (all 6 sites gated, see next table); does NOT stop §history child processes (:659 unconditional; :691 runs because analyzeHistory's `offline` param is hardcoded false at :1025) |
| `--selftest` | :143 | dispatches before any section (:1070); hermetic fixtures, see below |
| `--help`, `-h` | :144 | usage text :160-179, exit 0 (:1069) |
| `--repo DIR` / `--repo=DIR` | :145-146 | repo-root override, resolveRepoRoot :181-193 |
| `--section=X` / `--section=X` | :147-148 | one section; `pq14` aliases to `plazir` (:151); invalid → exit 64 (:152-155) |
| unknown flag, `--repo` w/o value | :149-150, :157 | exit 64 (:1068) before any section runs |

Env knobs: KAKE_REPO_ROOT, KAKE_FRESHNESS_PINS, KAKE_PROBE_HISTORY, KAKE_FLEET_CONFIG
(:829), KAKE_R15_SNAPSHOT (:866, default `/tmp/kake-r15/charter-live.html` :58),
KAKE_FETCH_TIMEOUT (:1085, default 15000 ms), KAKE_PLAZIR_LIVE_URL (:759 — re-aims
the plazir GET anywhere; no allowlist), KAKE_SELFTEST_DIR (:1183).

## Network targets — fired ONLY by §armed/§plazir WITHOUT `--offline`

| Check | Kind | Target | Fire site |
|---|---|---|---|
| PQ-12 | GET | https://veigapunk.github.io/charter-ufo-fsd/ (DEFAULT_PINS :77; pins.json has no override) | :839 |
| PQ-5 | GET | https://charter-ufo-fsd.kimi.page/ (:82) | :884 |
| sitemap | GET | https://ds4cc.com/sitemap.xml (:87) | :909 |
| plazir live | GET | https://veigapunk.github.io/plazir-15-site/sitemap.xml (pins.json:39; env KAKE_PLAZIR_LIVE_URL :759) | :763 |
| PQ-2 | git ls-remote origin main | /home/vgpnk/Projects/ds4cc-marketplace (:85) | :896-897 |
| plazir gate | git ls-remote origin main | /home/vgpnk/Projects/plazir-15-site (pins.json:38) | :743-744 |

All four GETs go through fetchBody :724-728 (redirect-follow, AbortSignal.timeout).
Three of four hosts + both ls-remote repos are operator-owned surfaces per the
round-30 bounds. Under `--offline` every one of these six sites is skipped:
armed early-returns at :812-820; plazir gate skipped :739, live skipped :760,
parity skipped :786 (local source sitemap.xml fs count :769-779 still runs).

## Invocation classes

| Invocation | Network | Child processes | Writes | Class for wave contexts |
|---|---|---|---|---|
| `--help` | none | none | none | SAFE |
| bad flag/section (exit 64) | none | none | none | SAFE (exits pre-section :1068) |
| `--section=paths` (± `--json --offline --repo`) | none | none | none | SAFE — §paths is fs-only (scanCitations :384-568: readdir/read/exists; no fetch/execFileSync in range) |
| `--section=history` (± `--json --offline`) | none | spawns scripts/probe-delta.mjs (:590 via :659, unconditional — its own note :1027-1029) and `systemctl --user list-timers` (:603 via :691, fires even under `--offline`) | none | network-free but NOT bounds-clean: probe-delta.mjs is on this round's never-run list |
| default (no section, :129 = all four) without `--offline` | YES — all 6 targets | probe-delta + systemctl (history included) | none | the exact round-29 breach shape |
| `--section=armed` / `plazir` / `pq14` without `--offline` | YES — subset per table | none (no history) | none | breach shape |
| any of the above WITH `--offline` | none | §history children only if history included (default `--offline` still spawns probe-delta + systemctl; `--section=armed --offline` spawns none) | none | network-clean; still forbidden this round ("any mode") |
| `--selftest` | none | node children of SELF with KAKE_IN_SELFTEST=1 (:1190-1192) | /tmp/kake-r16/selftest or $KAKE_SELFTEST_DIR (:1183; write regions :1199-1270, :1557-1623) + $HOME/.kake-freshness-selftest-<pid> (:1215-1217, removed :1628-1630) | offline; writes outside TMPDIR, see F3 |

`--selftest` child census (all 17 `run([...])` sites): §paths ×13 (:1273, 1286,
1298, 1310, 1321, 1332, 1346, 1409, 1422, 1590, 1602, 1613 — 4 of those with
`--offline`), §history ×3 (:1365 malformed→exit before spawn :625; :1377
suspended→:620; :1394 missing→:622 — none reaches runProbeDelta), bogus-flag ×1
(:1433). Zero §armed/§plazir children: as shipped, `--selftest` never fetches,
never ls-remotes, never spawns probe-delta or systemctl. This depends on fixture
content (all three §history cases exit early by design), not on a structural gate.

## Findings

- F1 (high, recurrence): the breach default is still armed. `node
  scripts/freshness-sweep.mjs` with zero flags runs all four sections online and
  fires 4 owned-host GETs + 2 ls-remotes (:839, :884, :909, :763, :897, :744).
  `--offline` is opt-in; there is no default-off, no env kill-switch, no URL
  allowlist. Round-29 recurs on today's tip with one bare invocation. Mitigation
  is procedural: contexts must name ONLY `--section=paths [--json] [--offline]`
  and `--help` as allowed invocations; `--section=history` excluded (probe-delta
  child); `armed`/`plazir`/`pq14`/default excluded (network).
- F2 (medium, doc-vs-behavior): usage :168-169 says `--offline` skips "every
  fetch/ls-remote; §paths + §history still run". True for network, but §history
  under `--offline` still executes probe-delta.mjs and systemctl (the `offline`
  param never reaches analyzeHistory: hardcoded false at :1025). A context that
  reads `--offline` as "no side effects beyond fs" would still launch a
  round-forbidden script. The in-band note :1027-1029 discloses probe-delta but
  not systemctl. Recommendation: never rely on `--offline` to neutralize
  §history; allow-list §paths only.
- F3 (low, sandbox hygiene): `--selftest` writes are not TMPDIR-bound: the
  /tmp/kake-r16/selftest tree is redirectable via KAKE_SELFTEST_DIR (:1183), but
  $HOME/.kake-freshness-selftest-<pid> (:1215) uses os.homedir() directly and
  cannot be redirected; cleanup :1628-1630 runs only on completion, so a crashed
  selftest leaks the $HOME fixture dir. Future waves that legitimately run
  --selftest should set KAKE_SELFTEST_DIR inside their sandbox and know about
  the pid-named $HOME dir.
- F4 (info): `--section=pq14` silently aliases to plazir (:151). Any wave text
  that forbids plazir by name must also name pq14.
- F5 (info, defense-in-depth): fetch targets for pq12/pq5/sitemap/pq2 come from
  DEFAULT_PINS (:77, :82, :85, :87); the runtime pins.json defines none of those
  four keys (grep over pins.json for `Url|Dir`: only plazir keys, :38-40), while
  KAKE_PLAZIR_LIVE_URL (:759) can re-aim the plazir GET at any host with no
  allowlist. "Safe by construction" should eventually mean an explicit URL
  allowlist, not just an opt-in flag.

## Verification gaps

- Static read only; every behavioral claim (exit codes 0/1/2/64, verdicts,
  skip labels) is sourced from code lines cited above, not observed — running
  the script in any mode is forbidden this round.
- probe-delta.mjs was checked for network symbols by grep only (no
  fetch/http/request matches); its full behavior was not audited and is out of
  scope (never run this round).
- The `--selftest`-never-spawns-probe-delta claim rests on the early-exit
  structure of its three §history cases (:620/:622/:625) plus the child census
  above; it was not exercised.
