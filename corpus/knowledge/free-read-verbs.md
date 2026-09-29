# Free-read verbs — `probe` / `status` / `grokbot reconcile` / `sync-check`

Round 11 (2026-09-28) operability axis. These are the four verbs a keeper may run
**without spending a meter, firing a chat, publishing, or writing a keeper log**.
Sources: `~/Projects/webzites/src/{cli,fleet,probe,reconcile}.mjs`,
`~/Projects/webzites/bin/webzites.mjs`, `~/Projects/webzites/scripts/kimi-surface.mjs`
(all read 2026-09-28, line pins re-verified post-draft), plus a live read of
`fleet/fleet.config.json` for the per-verb universe counts. Every live-run value was
observed 2026-09-28T21:31–21:33Z on the real repo (backup-guarded where the verb
writes state; provenance table at the end).

Invocation is always the absolute node path from any cwd — bare `webzites` is not
on PATH on this host (`SKILL.md:56-58`; `bin/webzites.mjs:5-12`).

## Verb table

| verb | rows it touches | reads | writes | exit 1 means |
|---|---|---|---|---|
| `probe [--all\|<id> …] [--json] [--quiet]` | rows with `url` (18/21); `<id>` → that subset only | live GET of each row's `url` | `state/probe-latest.json` (**overwrite, unmerged**), appends 1 line to `state/probe-history.jsonl` | ≥1 probed row `violated`/`error` — **subset-scoped** |
| `status [--json]` | whatever is in `state/probe-latest.json` | that file | nothing | last snapshot contains ≥1 `violated`/`error` |
| `grokbot reconcile [<id> …] [--json]` | **all 21** fleet rows (no-url → `skipped`) | live GET + `sourceDir` walk | nothing | ≥1 row `drift`/`fetch-error`/`source-missing` |
| `kimi-surface.mjs sync-check [<id> …\|--all\|--dead]` | `class == "kimi-surface"` rows — **15**; bare = those with `sourceDir` (**9**); `--dead` = the 6 without | live GET + `sourceDir` walk (same `reconcileSite`) | nothing | any verdict outside `{match, in-sync, no-source, skipped}` |

## Three universes — why every count you see is different

Read straight off `fleet/fleet.config.json` (21 rows, `schema`
`webzites-fleet-v1`, `updatedAt` 2026-09-26): `class` counts are
`{kimi-surface: 15, repo-driven: 3, queued: 3}`; **18** rows carry `url`; all 21
carry `expect`; **13** rows carry `sourceDir` (**9** of them `kimi-surface`).
Reproduce (run 2026-09-28, output `{"rows":21,"url":18,"expect":21,"kimi":15,"kimiSrc":9,"src":13,"kimiNoSrc":6}`):

```bash
cd ~/Projects/webzites && node -e 'const s=JSON.parse(require("fs").readFileSync("fleet/fleet.config.json","utf8")).sites;
console.log(JSON.stringify({rows:s.length, url:s.filter(x=>x.url).length, expect:s.filter(x=>x.expect).length,
 kimi:s.filter(x=>x.class==="kimi-surface").length, kimiSrc:s.filter(x=>x.class==="kimi-surface"&&x.sourceDir).length,
 src:s.filter(x=>x.sourceDir).length, kimiNoSrc:s.filter(x=>x.class==="kimi-surface"&&!x.sourceDir).length}))'
```

- `probe` filters `site.url` only (`src/cli.mjs:75`) → 18 rows — the same 18 that
  `probe-history.jsonl` records as `total:18`.
- `grokbot reconcile` applies **no** class/url/sourceDir filter — every fleet row
  is attempted, so no-url rows land `skipped` and source-less rows `no-source`
  (`src/cli.mjs:263-265`; `src/reconcile.mjs:134-146`).
- `sync-check` loads its own row set, `class === "kimi-surface"`
  (`scripts/kimi-surface.mjs:42-45`), then splits on `sourceDir`
  (`scripts/kimi-surface.mjs:187-190`).

[INFERENCE] Because `sync-check` reuses `reconcileAll` (`scripts/kimi-surface.mjs:192` import / `:194` call)
over that narrower class-filtered set, a `sync-check --all` of 15 rows and a
`grokbot reconcile` of 21 rows are **not** comparable row-for-row; diff the ids,
never the counts.

## Verb card — `probe [--all|<id> …] [--json] [--quiet]`

- **Universe.** `config.sites.filter(site => (requested.size ? requested.has(id) : true) && site.url)`
  (`src/cli.mjs:75`); zero matches → `UsageError` "no sites selected (check ids)"
  (`src/cli.mjs:76`), which `main`'s catch turns into **exit 2 + HELP on stderr,
  no state write** (`src/cli.mjs:1097-1101`).
- **`--all` is cosmetic.** It is parsed into flags (`src/cli.mjs:57`) and never
  read by `cmdProbe` (`src/cli.mjs:72-89`) — bare `probe` already means "every
  url-bearing row". `--all` exists in the HELP text (`src/cli.mjs:20`) and in the
  installed unit's `ExecStart= … probe --all --quiet` (`src/cli.mjs:1002`).
- **What it proves.** GET (never HEAD), redirects followed, then up to four checks
  against `expect`: `status`, `finalUrlNot`, `title` regex, `marker` literal
  (`src/probe.mjs:45-55`). A raw 200 proves nothing — marker/title are the proof
  (`src/probe.mjs:1-3`).
- **Verdicts.** `ok` | `violated` (a check failed) | `unchecked` (row has `url`
  but no `expect`) | `skipped` (no `url`) | `error` (fetch/abort caught at
  `src/probe.mjs:74-81`) (`src/probe.mjs:70`, `:24`, `:27`).
- **Output.** Human table via `renderStatus` — `OK `/`FAIL`/`SKIP`/`ERR ` per row
  (`src/fleet.mjs:93-100`); `--json` prints `{at, results}` (`src/cli.mjs:80-81`);
  `--quiet` suppresses stdout but the state write still happens (`src/cli.mjs:78`
  runs before the `if (!flags.quiet)` at `:79`).
- **Exit.** 1 iff the **probed subset** has any `violated`/`error`, with the ids on
  stderr (`src/cli.mjs:83-87`). So `probe ds4cc-com` exits 0 while the
  rest of the snapshot's rows are bad — the exit code describes the subset, and
  (see below) that same subset replaces the fleet snapshot.
- **Side effects.** `saveProbe(ROOT, results)` with the **raw** results
  (`src/cli.mjs:78`) → `probe-latest.json` is overwritten with exactly the probed
  set, and one history line is appended (`src/fleet.mjs:39-52`). This is the
  asymmetry in the state model below.
- **Two clocks.** `probe --json`'s `at` is a fresh `new Date()` (`src/cli.mjs:81`)
  taken *after* `saveProbe` stamped the file's own `at` (`src/fleet.mjs:40`), and
  the history line reuses the report's `at` (`src/fleet.mjs:45`) — three
  timestamps that can differ by milliseconds and MUST NOT be compared for equality.

Live (2026-09-28T21:31:26Z, backup-guarded, real repo): `probe ds4cc-com --json`
→ **exit 0**, `results[]` length 1 (200, title+marker pass, 269 ms);
`probe-latest.json` **18 rows → 1 row** (`at` 18:51:26.128Z → 21:31:26.591Z);
history **76 → 77 lines** (new line 77 =
`{"at":"2026-09-28T21:31:26.591Z","total":1,"ok":1,"violated":[],"errors":[]}`);
restore re-established the fleet snapshot byte-identically
(sha256 `8c5bb8ca…b6591e` before == after). Replica corroboration of the
`--quiet` variant (`/tmp/kake-r11/scout-verbs.md`): state still written, stdout 0 B,
failure line on stderr 57 B. Evidence: `/tmp/kake-r11/probe-ds4cc.out`,
`/tmp/kake-r11/labrat-probe.md`.

## Verb card — `status [--json]`

- **Reads only** `state/probe-latest.json` via `loadLastProbe` (`src/cli.mjs:93`;
  loader `src/fleet.mjs:14-18`; absent file → the "no probe results yet" string,
  `src/fleet.mjs:92`). It never touches the network and never writes.
- **Exit asymmetry — snapshot-relative, not fleet-relative.** `status --json`
  **always exits 0**: the JSON branch returns before the check (`src/cli.mjs:94-97`).
  Plain `status` exits **1 iff the loaded snapshot** has any `violated`/`error`
  (`src/cli.mjs:99`) — so after `probe <healthy-id>` it exits 0 while the
  pre-state snapshot's non-ok rows (5 violated + 1 error,
  `/tmp/kake-r11/probe-latest.backup.json`) are simply not in the file. Never
  read this as an unconditional fleet verdict; read stdout, never gate on the exit
  code (`SKILL.md:100-105`). Either way the check is *after* `loadLastProbe`, so a
  corrupt `probe-latest.json` throws out of `JSON.parse` (`src/fleet.mjs:17`,
  no try/catch) and the bin wrapper exits 1 with a stack (`bin/webzites.mjs:7-12`)
  — a crash code that is indistinguishable from a legitimate tripwire by exit
  status alone.
- **Clobber interaction.** Because `status` renders whatever `probe-latest.json`
  holds, running it right after `probe <id>` prints a 1-row picture and — if that
  one row is `ok` — exits 0. A green `status` is only as wide as the last writer's
  row set.
- `map` shares the same input and inherits the same narrowing: it renders "not
  probed" for every id missing from the snapshot and prints
  `Last probe: … (N/M ok)` with M = snapshot size (`src/cli.mjs:102-108`;
  `src/fleet.mjs:61`, `:65-70`).

Live (2026-09-28T21:31Z): while clobbered, `webzites status` printed **1 OK row
and exited 0** — 5 violated + 1 error fleet rows invisible; post-restore it
printed **18 rows and exited 1** (true fleet state 12 ok / 5 violated / 1 error).
Evidence: `/tmp/kake-r11/labrat-probe.md` steps 4/6,
`/tmp/kake-r11/status-restored.out`.

## Verb card — `grokbot reconcile [<id> …] [--json]`

- **Universe.** All 21 rows unless ids are named (`src/cli.mjs:263-265`).
- **Method.** Fetches live bytes (GET, redirect follow, 20 s timeout,
  UA `webzites-reconcile/1.0`, `src/reconcile.mjs:113-129`), picks ONE
  `index.html` under `sourceDir` (depth ≤ 2, breadth-first, hidden dirs and
  `node_modules` skipped, `src/reconcile.mjs:57-63`) by score = marker present (+2)
  + title regex match (+1) − depth/100 (`src/reconcile.mjs:86-108`), then compares
  sha256 of the two bodies.
- **Verdicts** (fork at `src/reconcile.mjs:171-173`, plus the earlier exits):
  `match` (byte-identical) · `in-sync` (title equal **and** marker parity when a
  marker exists) · `drift` (neither) · `no-source` (row has no `sourceDir` —
  "live surface is the only truth") · `source-missing` (`sourceDir` absent) ·
  `no-source-file` (no `index.html` found) · `fetch-error` · `skipped` (no url /
  no expect). Human marks: `OK / SYNC / DIFF / LIVE / NOSRC / NODIR / ERR / SKIP`
  (`src/reconcile.mjs:200-212`).
- **`in-sync` is the trap.** Kimi rewrites served bytes, so byte equality is not
  the contract (`src/reconcile.mjs:1-5`) — and on GHP rows `in-sync` masks real
  byte drift; treat it as "git fetch + spotcheck" (`SKILL.md:183`;
  `corpus/knowledge/ghp-subpath-spotcheck.md`).
- **Exit.** 1 iff any row is `drift`/`fetch-error`/`source-missing`
  (`src/cli.mjs:269-272`). **`no-source-file` is not in that set** — a sourceDir
  whose root page is missing exits 0 (and renders `NOSRC`). [INFERENCE] That is a
  silent blind spot: reconcile reports it, the tripwire ignores it.
- **Writes nothing.** Unlike `grokbot tick` — which probes, merges, reconciles and
  appends a keeper entry per site (`src/cli.mjs:281-333`, entry writer
  `src/cli.mjs:565`) — `reconcile` is a pure read.
- **Unknown id is a trap.** `cmdGrokbot` is dispatched **un-awaited**
  (`src/cli.mjs:1086`), so its `UsageError` ("no sites selected (check ids)",
  `src/cli.mjs:265`) escapes `main`'s catch (`src/cli.mjs:1097`) and surfaces as
  the bin wrapper's crash path — **exit 1 with a raw stack**
  (`bin/webzites.mjs:7-12`), colliding with the legitimate drift exit 1. Live
  evidence: `/tmp/kake-r11/scout-verbs.md` F2 (516 B stderr, stack).

Live (2026-09-28T21:31-32Z, real repo, zero writes — isolated marker re-test
found **0 files touched** under `state/`/`reports/`/`fleet/`):
`reconcile ds4cc-com` → **exit 0, SYNC**, live 79 453 B vs source 79 422 B
(byte inequality is the kimi/GHP norm, title+marker agree);
`reconcile plazir15-ghp --json` → **exit 0, match** (sha `d82af77a…`, 38 337 B
both sides — live bytes == local `sourceDir`, regardless of the 5-commit local
lead over `origin/main`: reconcile compares live vs **local sourceDir**, never
git-vs-origin); fleet-wide 21-row sweep → **exit 1**, 7 attention ids
(`ufofsd-charter, plazir27-kimi-page, plazir27runs-on, plazir15,
charter-ufo-fsd-kimi, xsnapshot-app, lucario` — 6 DIFF + 1 ERR). **r16 re-read
(2026-09-29T02:35Z, exit 1 re-proven): 6 attention ids — `plazir27runs-on`
dropped; verdicts `{no-source:6, in-sync:4, drift:5, match:2, fetch-error:1,
skipped:3}` of 21, i.e. 5 DIFF + 1 ERR; re-run before citing**.
Evidence: `/tmp/kake-r11/reconcile-ds4cc.out`, `/tmp/kake-r11/reconcile-plazir15.json.out`,
`/tmp/kake-r11/labrat-reconcile.md`.

## Verb card — `kimi-surface.mjs sync-check [<id> …] [--all|--dead]`

- **Universe.** `class === "kimi-surface"` rows (`scripts/kimi-surface.mjs:42-45`):
  bare → those with `sourceDir` (9), `--all` → all 15, `--dead` → the 6
  source-less ones (`:184-190`). No matching row → `die` with "no kimi-surface site
  in ids: …" or "no kimi-surface site has a sourceDir", exit 1
  (`scripts/kimi-surface.mjs:191`, `:34`).
- **Method.** Same engine as `grokbot reconcile` — it imports `reconcileAll`
  (`scripts/kimi-surface.mjs:192`), so the title+marker byte semantics and every
  verdict above apply unchanged (`scripts/kimi-surface.mjs:174-179`).
- **Extra field.** `unpublished404: true` when the live body's sha256 equals the
  13 409-byte Kimi 404 sentinel (`S404_SHA256`, `scripts/kimi-surface.mjs:180`,
  `:198`) — a live 404 that a status-only check would misread. The JSON **drops**
  `markerSource` (never pushed into the result object, `:196-203`), so a `drift`
  row with `titleEqual:true` + `markerLive:true` means the **source-side marker
  is missing**, not live rot.
- **Output.** JSON only, no human table: `{at, results[{id,url,verdict,
  unpublished404,status,liveBytes,liveSha256(16),srcSha256(16),srcFile,titleEqual,
  markerLive,firstDiffLine,note}], summary:{ok,attention[]}}`
  (`scripts/kimi-surface.mjs:194-206`).
- **Exit.** 1 iff any verdict falls outside `{match, in-sync, no-source, skipped}`
  (`scripts/kimi-surface.mjs:206`, `:208`) — note this set is **stricter** than
  `grokbot reconcile`'s: `no-source-file` and `source-missing` do fail here.
- **No `--help`.** Usage prints via the default arm on any unknown verb, exit 64
  (`scripts/kimi-surface.mjs:1197-1198`; dispatch at `:1184`;
  `corpus/knowledge/probe-delta-alerting.md`).
- Pure HTTP: no browser, no lease needed (`SKILL.md:108-112`). The browser-gated
  kimi verbs (`update`/`recreate`/`rebuild`, `kimi-map`) are out of scope here.

Live (2026-09-28T21:31-33Z, real repo, zero writes):
`sync-check ds4cc-kimi-mirror` → **exit 0, in-sync**, 200 / 74 641 B, ~2.0 s —
the mirror is a **~Aug-29 stale vintage with 75/93 canonical locs missing**
(`corpus/knowledge/kimi-subpath-audit.md`) yet still verdicts in-sync: vintage lag
is invisible to this verb; `sync-check burnerchrome-kimi` → **exit 0, in-sync**
(1.6 s); bare 9-row fleet run → **exit 1**, `summary {ok:3, attention:
[ufofsd-charter, plazir27-kimi-page, plazir27runs-on, plazir15,
charter-ufo-fsd-kimi, lucario]}` — 3 of the 6 attention rows are 404-sentinel
dead slots (`unpublished404:true`, sha `93ddca9a…`), 3 are real 200/titleEqual
drift with source-side marker missing; **r16 re-read (2026-09-29T02:35Z, exit 1
re-proven): `{ok:4, attention:[ufofsd-charter, plazir27-kimi-page, plazir15,
charter-ufo-fsd-kimi, lucario]}` — `plazir27runs-on` flipped to `in-sync` (the
marker's served casing changed), so the count is 3 sentinel + 2 real drift of
5; every attention-list literal in this file is a dated sample, re-run the verb
before citing it**; verdict lines **identical across two
consecutive runs**; `--dead` (6 rows) → **exit 0**; unknown id → **exit 1**
(`kimi-surface: no kimi-surface site in ids: …`); unknown verb → **exit 64**.
`liveSha256` is **nondeterministic run-to-run** (ds4cc mirror:
`abf822c7` → `440e3cba` → `5a80ee93` across fetches — kimi seed-tag injection +
rotating `data-cfemail`): never alert on live-sha deltas.
Evidence: `/tmp/kake-r11/labrat-sync.md`, `/tmp/kake-r11/sync-*.out`,
`/tmp/kake-r11/err.txt`.

## State-persistence model (the part that bites)

### 1. `probe-latest.json` — whole-file overwrite, no merge on the `probe` path

`saveProbe` builds `{at, results}` from **exactly what it is handed** and rewrites
the file atomically (tmp + `renameSync`, `src/fleet.mjs:20-25`, `:39-42`), then
appends one history line (`src/fleet.mjs:44-51`). `cmdProbe` hands it the **raw**
probed subset (`src/cli.mjs:78`).

Therefore `probe <id>` replaces the 18-row fleet snapshot with a
**1-row** file; `status`/`map`/`grokbots --status`/`bots report` (readers of
`loadLastProbe`: `src/cli.mjs:93,104,402,893`) then see only that row, and the only
way back to a full snapshot is another full run — `probe` (all url rows) or
`grokbot tick`. **Live-confirmed 2026-09-28: 18 rows → 1 row, restore
byte-identical** (see the `probe` verb card above).

### 2. The merge asymmetry — `src/cli.mjs:78` vs `:289` / `:647`

`saveProbe` has exactly three call sites (`src/cli.mjs:78`, `:289`, `:647`):

| call site | verb | argument | effect on un-probed rows |
|---|---|---|---|
| `src/cli.mjs:78` | `probe` | `results` (raw) | **erased** — file narrows to the probed subset |
| `src/cli.mjs:289` | `grokbot tick` | `mergeProbeResults(loadLastProbe(ROOT), probeResults, fleet.sites.map(s => s.id))` | **preserved**, re-sorted into fleet order |
| `src/cli.mjs:647` | `bots task` | `mergeProbeResults(loadLastProbe(ROOT), [probe], fleet.sites.map(c => c.id))` | **preserved** (single-site probe keeps the fleet snapshot) |

`mergeProbeResults` keys previous entries by `id`, overwrites them with fresh ones,
and sorts by the fleet id order so `status` still reads in fleet order
(`src/fleet.mjs:30-37`). Its own intent comment says site-specific verbs
"must not erase every other site's verdict" (`src/fleet.mjs:27-29`) — `cmdProbe`'s
raw path violates exactly that criterion, and the webzites-side archaeology
(`/tmp/kake-r11/revenger-merge.md`) proves the clobber was noticed and fixed for
`bots task`/`tick` in the r2 era (bots-create-r2.md:73-75 "fixes the pre-round
clobber where one site-scoped probe erased the fleet snapshot") while `cmdProbe`
was left raw: **unintended defect, not spot-probe semantics**. Consequences:

- A `grokbot tick` that probes 18 sites still records `total:18` in history even
  though it also reconciles all 21 rows — `total` counts **probe** results only
  (`src/cli.mjs:289`; `src/fleet.mjs:46`).
- A merged row carries **stale** entries for ids it did not probe, and history rows
  carry no provenance — `scripts/probe-delta.mjs` cannot tell a merged row from a
  fresh sweep (`corpus/knowledge/probe-delta-alerting.md`, "Merged-row caveat").
- `grokbot reconcile` and `sync-check` write nothing at all (`src/cli.mjs:261-274`;
  `scripts/kimi-surface.mjs:192-208`) — running them can never disturb the snapshot.

### 3. `probe-history.jsonl` — append-only summary lines, incl. `total:1` spot rows

Line shape: `{"at","total","ok","violated":[ids],"errors":[ids]}` with
`total = results.length` of whatever was saved (`src/fleet.mjs:44-51`). Hence:

- **Full sweep** (bare `probe`, timer `probe --all --quiet`, `src/cli.mjs:1002`) →
  `total:18` on the current registry.
- **Spot row** (`probe <id>`) → `total:1`, `ok:1` typically, `violated:[]` —
  mechanically identical to "the whole fleet just went green" if read naively.
  Spot rows are why naive consecutive-row diffing emits 42 events of which 40 are
  phantom (`corpus/knowledge/probe-delta-alerting.md`; r10 baseline: **10 spot rows
  in 76**; archaeology: 11 of 77 incl. round-11's, `/tmp/kake-r11/revenger-merge.md`).
- **Merged rows** (`grokbot tick`, `bots task`) also write `total:18`, so `total`
  alone cannot separate fresh from merged.
- `saveProbe` never rewrites or truncates the file — write is
  `writeFileSync(history, line, { flag: "a" })` (`src/fleet.mjs:51`). Only the
  `probe-latest.json` half of a probe is reversible; a history line is permanent
  (round-11 live confirmation: the backup-guarded spot probe left one extra
  `total:1` line — line 77 — that no restore removes).
- A row is only trustworthy when `total == ok + |violated| + |errors|`; 11 early
  rows violate that (deficit rows carry skipped sites)
  (`corpus/knowledge/probe-delta-alerting.md`).

### 4. Reader contract (one line each)

- Snapshot width = last writer's width → check `probe-latest.json` row count before
  trusting `status`/`map`/`bots report` (`src/fleet.mjs:14-18`).
- `status`'s exit code is **snapshot-relative** ("exit 1 iff the surviving snapshot
  has a violated/error row", `src/cli.mjs:99`) — say it that way, never as an
  unconditional fleet iff (round-11 critic audit, `/tmp/kake-r11/critic.md` claim 4).
- History = event log with bursty sampling; never back-calculate dwell time from row
  counts (`corpus/knowledge/ops-automation.md`). `saveProbe` is its **sole** writer
  (`src/fleet.mjs:42-51`).
- Three universes, three exit-code sets (`src/cli.mjs:83-87`, `:99`, `:269-272`;
  `scripts/kimi-surface.mjs:206`) — never reuse one verb's exit code as another's gate.

## Round-11 live-run provenance

| slot | command under test | evidence artifact |
|---|---|---|
| probe | `node ~/Projects/webzites/bin/webzites.mjs probe ds4cc-com --json` | `/tmp/kake-r11/probe-dscc.out` → `/tmp/kake-r11/probe-ds4cc.out` (1-row JSON), `probe-ds4cc.err`, `/tmp/kake-r11/labrat-probe.md` (step log incl. the restore + re-verified sha); `probe-latest.json` row count/sha before–after; the new `probe-history.jsonl` line |
| status | `… webzites status` **while clobbered**, then again post-restore | clobbered run: `/tmp/kake-r11/labrat-probe.md` step 4 (transcript block + `EXIT=`, no raw capture file); restored run: `/tmp/kake-r11/status-restored.out` (18 rows) |
| reconcile | `… webzites grokbot reconcile ds4cc-com`, then `reconcile plazir15-ghp --json` | `/tmp/kake-r11/reconcile-ds4cc.out`, `/tmp/kake-r11/reconcile-plazir15.json.out`, `/tmp/kake-r11/labrat-reconcile.md` (run 3 isolation re-run + write-verification) |
| sync-check | `node ~/Projects/webzites/scripts/kimi-surface.mjs sync-check <ids>` / bare | `/tmp/kake-r11/labrat-sync.md` (per-row exits + verdicts, exit-code table, fs-write isolation proof, nondeterminism caveat); `/tmp/kake-r11/sync-all.out` + `sync-all-2nd.out` (repeat determinism), `sync-fleet.json`, `sync-fleet.err`, `sync-burnerchrome.out`, `sync-ds4cc-mirror.out`; unknown-id path (EXIT=1) in `/tmp/kake-r11/err.txt` |

Pre-state baseline for the probe experiment (recorded by L1 before the run,
21:30Z): `probe-latest.json` sha256 `8c5bb8ca…b6591e`, `probe-history.jsonl`
sha256 `31b8be9f…fb2492`, 76 history lines; backup at
`/tmp/kake-r11/probe-latest.backup.json`. Post-run reconciliation
(sentinel-audited 21:34Z): `probe-latest.json` restored **byte-identical**
(sha equal to pre-state; `cmp` clean vs backup), `probe-history.jsonl` **77
lines** with exactly one new `total:1` line — the sanctioned steady state.
The first `sync-*.out` captures at 18:31Z were a `/usr/bin/time` wrapper defect
(that binary is absent on this box, EXIT=127) and are **not** evidence — use the
21:32+ re-runs above. Independent replica runs of every variant (including
`--quiet`, unknown-id, corrupt-snapshot) live in `/tmp/kake-r11/scout-verbs.md`
(byte-identical isolated copy, real repo untouched).

## Round-12 append: the roster/ops free-reads (`status --json`, `grokbots --check`, `bots list`, `bots report`)

Round 12 (2026-09-28) operability move: the four remaining replica-verified
roster/ops verbs were live-run on the real repo. All four are pure local reads:
L1's sha guard over `state/*.json` + `state/*.jsonl` is byte-identical
before/after (`/tmp/kake-r12/state-before.sha` vs `state-after.sha`: same 31
hash lines, sorted diff clean), and an ExecutorDrafts re-run (~22:20Z) left the
same 31 files byte-identical (`/tmp/kake-r12/executor-now.sha`, sorted diff
clean vs `state-after.sha` — raw line order differs, the hash set is what
matches). None of the four bodies contains a write call — fs access is
`existsSync`/`readFileSync`/`statSync` only (`src/cli.mjs:93-99`, `:345-424`,
`:578-611`, `:888-958`; critic independently re-ran all four and matched the
guard, `/tmp/kake-r12/critic.md` claim 1).

| verb | rows it touches | reads | writes | exit 1 means |
|---|---|---|---|---|
| `status [--json]` | the `state/probe-latest.json` snapshot only | that file | nothing | (plain) ≥1 `violated`/`error` in the **surviving snapshot** (`src/cli.mjs:99`); `--json` **always exits 0** (`src/cli.mjs:94-97`) |
| `grokbots [--check\|--status] [--json]` | `--check`: every fleet row — **21**, url-less included (`src/cli.mjs:355`) | `fleet/grokbots.json` + each card `~/.grok/agents/grokbot-<id>.md` (`:364`, `:444`) + keeper logs | nothing | ≥1 failure: registry-row absence (`:361`), agentPath/agentName/url/class/updatePath drift (`:365-369`), card missing/unparseable/oversize/not-naming-site (`:370-382`), `duties[]` bad (`:383`), log missing (`:384`), registry-row-without-fleet-row (`:386`) — return `:399` |
| `bots list [--json]` | the **20** `registry.agents` rows (`src/cli.mjs:579-580`) | registry + card existence + wrapper exec-bit (`:582-583`; paths `:427-433`, `:444`) | nothing | never — returns 0 unconditionally (JSON `:598`, human `:610`) |
| `bots report [--json] [--stale N]` | every fleet row — **21** (`src/cli.mjs:894`) | snapshot (`:893`) + keeper-log entries (`:846-863`) + card/wrapper state (`:911-914`) | nothing | `gaps.length > 0 \|\| stale.length > 0` (`src/cli.mjs:958`) |

Live results 2026-09-28 (L1 22:14Z; exits re-measured by ExecutorDrafts 22:20Z,
critic 22:2xZ — all three agree):

- `status --json` → **exit 0** while the snapshot holds **5 violated + 1 error**
  (18 rows; `plazir15, charter-ufo-fsd-kimi, charter-ghp, plazir27-kimi-pro,
  lucario` violated; `xsnapshot-app` error; snapshot stamped
  `2026-09-28T18:51:26.128Z` — `/tmp/kake-r12/live/status-json.out`).
- `grokbots --check` → **exit 1** — `FAIL lucario: no registry row`;
  JSON `{ok:false, checked:21, failures:["lucario: no registry row"]}`
  (`/tmp/kake-r12/live/grokbots-check.out`, `grokbots-check-json.out`).
  **checked-count fact:** `checked` is `fleet.sites.length` (`src/cli.mjs:393`)
  over the `fleet.sites` loop (`:355`) — **21, url-less rows included**, never
  18; the `&& site.url` filter (`src/cli.mjs:75`) belongs to `probe` only.
  **Checked does NOT mean covered:** `grokbots --check` never touches wrapper
  presence (`botWrapperPath` `:427` unused in the check loop `:354-391`) — a
  missing wrapper on a non-queued site passes `--check` while failing
  `bots report`'s gap predicate (r12: latent only; the 3 missing wrappers are
  all queued).
- `bots list` → **exit 0** — `20 keepers (cards 20/20, wrappers 17/20)`
  (`/tmp/kake-r12/live/bots-list.out`), registry-driven (20 rows; `lucario` is
  not listed). The 3 wrapper misses are exactly the queued rows
  `xsnapshot-app`, `snapshot-kimi-pro`, `burnerchrome-com` (all `(queued)`).
- `bots report` → **exit 1** — stderr `webzites bots report: 1 site(s) with
  identity gaps: lucario`; stdout 21 rows: `probe=<verdict>(3.4h)` for the 18
  snapshot rows, `probe=never` for the 3 url-less rows; `log=8d(round
  2026-09-21T03)` on 19/21 (r16 correction — the widened `log=8d(` pattern
  gives 20/21, `veigapunk-page` ends `e2e fix`; lucario `log=never(?)` — no log file);
  `turn=never` on **17/21** (counted on the capture; the four with turn ages —
  vault, veigapunk-page, ufofsd, plazir15 — are 8d); `card=miss wrapper=miss`
  only on lucario.

Exit-1 predicates, exactly:

- `bots report` gaps = rows failing `!registered || !cardPresent || (!queued &&
  !wrapperPresent)` (`src/cli.mjs:935`) — **queued wrapper-misses are exempt**
  (that is why only lucario gaps while `bots list` renders 3 wrapper misses).
- `stale` is computed **only when `--stale <hours>` is passed**:
  `parseBotsStaleHours` returns null without the flag (`src/cli.mjs:836-839`),
  per-row flag `staleHours !== null && (logAgeHours === null || logAgeHours >
  staleHours)` (`:932`). Bare `bots report` can never fail on log age; with
  all 20 logs 8d old (keeper timer inert —
  `corpus/knowledge/keeper-timer-inert.md`), any `--stale` threshold ≥1h fails
  fleet-wide (labrat r12: `--stale 24` and `--stale 1` both mark all 21 STALE
  and exit 1 — indistinguishable on uniformly old logs;
  `/tmp/kake-r12/labrat.md`).
- `bots list` never fails on content (`:598`, `:610`); `status --json` never
  fails on content (`:94-97`) — a corrupt `probe-latest.json` still crashes
  both `status` forms exit 1 with a `SyntaxError` **before** the flag branch
  (`src/fleet.mjs:14-18` → `bin/webzites.mjs:8-11` rejection handler; labrat
  r12 live-confirmed the r11 claim).

Universes update (r12): probe/status snapshot **18** (`site.url` filter
`src/cli.mjs:75`) · `bots report` rows **21** (`fleet.sites.map` `:894`) ·
`grokbots --check` `checked` **21** (`fleet.sites.length` `:393`) · `bots
list`/registry **20** (`registry.agents` `:579-580`). The wedge is `lucario`:
added to `fleet.config.json` 2026-09-27 (mtime 12:30:57 -03), never registered
in `fleet/grokbots.json` (mtime 2026-09-20) — no row, no card, no wrapper, no
log. 18-of-21 probe coverage is **by-design url filtering, not a coverage
hole**; never read a snapshot count as the fleet count.

Round-12 live-run provenance: `/tmp/kake-r12/live/` (status-json, grokbots-check
{plain,json}, bots-list, bots-report {out,err}); zero-delta guard
`/tmp/kake-r12/state-before.sha` == `state-after.sha`; replica edge matrix
`/tmp/kake-r12/labrat.md` (corrupt/deleted snapshot, empty/missing registry,
`--stale` variants, `grokbots --status`); critic re-runs `/tmp/kake-r12/critic.md`;
citation verification `/tmp/kake-r12/reviewer.md` (22 OK / 2 WRONG / 1
wrong-as-worded — all three corrections folded here).

### r11 F1 guard addendum — the proposed fix was itself wrong

The r11 F1 handoff (`/tmp/kake-r11/scout-verbs.md:126`) proposed guarding the
merge with `positionals.length > 0 && !flags.all`. Round-12 revenger
**refuted that guard on a replica**: selection (`src/cli.mjs:75`) ignores
`--all` (the BOOL is parsed at `:57` and reaches `cmdProbe` via `:1070-1071`
but is never read — grep: 0 uses of `flags.all`), so `probe <id> --all` still
probes a subset; under the r11 guard that run **clobbers exactly as before**
(replica: 18→1 rows). Correct one-line fix, replica-verified
`/tmp/kake-r12/revenger-patch.md` + `/tmp/kake-r12/revenger-replica`:

```js
// src/cli.mjs:78 — replace:  saveProbe(ROOT, results)
saveProbe(ROOT, positionals.length > 0 ? mergeProbeResults(loadLastProbe(ROOT), results, config.sites.map((site) => site.id)) : results)
```

(`mergeProbeResults` `src/fleet.mjs:30-37` — not `:39-51`, which is `saveProbe`;
both already imported at `src/cli.mjs:7`. Replica result: subset probe keeps 18
rows + 5 violated, refreshes only the probed row, history records merged
`total:18` like tick/`bots task`; `probe <id> --all` edge stays 18 rows.
`node --check` clean. webzites is read-only to this lane — the patch ships in
the round report for the webzites source owner.)

## Limits

- **The `probe <id>` clobber is live-confirmed** (18→1 rows, status exit 1→0 while
  clobbered); the remaining [INFERENCE]-tagged cells are code-derived and await
  their own live trigger (e.g. corrupt `probe-latest.json` crash path — replica-
  confirmed in `scout-verbs.md`, not yet on the real repo).
- **No writer restores a narrowed snapshot implicitly.** Recovery from
  `probe <id>` requires an explicit full `probe` or `grokbot tick`; nothing
  self-heals `probe-latest.json` — except the 6h `webzites-probe.timer` sweep,
  which re-widens it to 18 rows on schedule.
- **`in-sync` is not freshness.** A stale `sourceDir` mirror still verdicts
  `in-sync` with exit 0 whenever title+marker agree — byte drift and vintage lag
  are invisible to `sync-check` (verdict precedence `src/reconcile.mjs:171-173`;
  live 2026-09-28: the ~Aug-29 ds4cc mirror with 75/93 canonical locs missing
  verdicts in-sync, exit 0 — `/tmp/kake-r11/labrat-sync.md`). Decide republish
  from vintage evidence, not the verdict (`SKILL.md:182`).
- **`sync-check` has no `--help`** (`scripts/kimi-surface.mjs:1197-1198`) — use the
  header comment (`scripts/kimi-surface.mjs:1-20`) as its usage; `--all`/`--dead`
  are real but absent from the usage line (F5, `/tmp/kake-r11/scout-verbs.md`).
- Universe counts (18/21/15/9/6, class split, 13 sourceDirs) are a snapshot of
  `fleet/fleet.config.json` `updatedAt: 2026-09-26` read 2026-09-28; print the
  command with any count you cite (`corpus/knowledge/fleet-registry.md` counting
  rule).
- **Not covered here:** `grokbot tick` / `bots task|run|digest|mint` (mutating or
  metered — see `corpus/knowledge/ops-automation.md`), `kimi-surface
  update|recreate|rebuild|kimi-map` (browser + lease, `SKILL.md:122-128`,
  `:155-158`), and
  `speedrun *` (`corpus/knowledge/speedrun-pipeline.md`).
