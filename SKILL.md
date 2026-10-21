---
name: kake-shokunin
description: Domain specialist — web properties & publishing — scopes ds4cc.com, kimi.page/pro mirrors, Pages deploys. Rank: shonen.
---

# kake-shokunin

Playbook for the VeigaPunk property fleet: audit → source fix → operator-gated
publish. Every claim below cites a file or a verified report; verify state with
the probe commands, never with memory.

## Property map (re-probed 2026-09-28; config `updatedAt` can lag live state)

| Surface | Live URL | Source dir | Publish path |
|---|---|---|---|
| ds4cc.com (primary) | `https://ds4cc.com/` | `~/Projects/ds4cc-marketplace` | GH Actions on push to `main` (`CNAME` = ds4cc.com) **[r20-correction 2026-10-19: a repo CNAME sets the domain only for branch publishing; under Actions it is ignored and the domain is a Pages setting (`cname` in the REST API) — S005, S003, S007]** | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| plazir15 GHP front | `https://veigapunk.github.io/plazir-15-site/` | `~/Projects/plazir-15-site` | GH Actions on push to `main` |
| charter GHP front | `https://veigapunk.github.io/charter-ufo-fsd/` | `~/Projects/origin-work/charter-ufo-fsd` | Pages deploy from branch (no workflow file); canonical doc, all kimi variants `rel=canonical` here | <!-- r18 re-census 2026-10-14: ~/Projects/origin-work/charter-ufo-fsd absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| ds4cc kimi mirror | `https://ds4cc.kimi.page/` | `~/Projects/ds4cc-marketplace` | Kimi surface, chat `1a073c43-bf42-874a-8000-0907bd80b9dc` — STALE (~Aug-29 vintage) | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| burnerchrome kimi | `https://burnerchrome.kimi.page/` | `~/Projects/ds4cc-marketplace/burnerchrome` | Kimi surface, chat `1a0ada42-28e2…` |
| vault index | `https://veigapunk.kimi.page/` | none on disk | Kimi surface, chat `1a0c20ea-6372…` — NEVER fire into this chat, it hot-swaps the live vault |
| plazir27.kimi.page | `https://plazir27.kimi.page/` | charter repo | canonical kimi charter mirror (stale: serves 09-18 beat, canonical 09-28) |
| ufo-fsd.kimi.pro | `https://ufo-fsd.kimi.pro/` | none (Vite shell) | Kimi surface, chat `1a0acd51-4122…` (612B SPA shell) |
| plazir15.kimi.page | 404 dead slot | `~/Projects/plazir-15-site` | RECREATE path — no bound chat; vessel `1a0c2186-fa12` is empty *[r20 citation-local 2026-10-19: `~/Projects/plazir-15-site` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]* |
| charter-ufo-fsd.kimi.page | 404 dead slot | charter repo | RECREATE path — no bound chat exists |
| lucario GHP (canonical) | `https://veigapunk.github.io/lucario/` | `~/Projects/lucario` (`site/` + `src/lucario/engine.py`) | Pages branch deploy on push — live 200, verified 09-28 |
| lucario kimi slot | `https://lucario.kimi.page/` — 404, **never published** | `~/Projects/lucario/site` | Kimi surface pending first publish (README: "pending — gated"). Config `status:live` is stale/wrong. **Roster gap (r12):** the fleet row (added 2026-09-27) has no `fleet/grokbots.json` agent — `grokbots --check` exits 1 (`lucario: no registry row`, `src/cli.mjs:361`), no card at `~/.grok/agents/grokbot-lucario.md` (`botCardPath` `src/cli.mjs:444`), no wrapper `~/.local/bin/grokbot-lucario` (`:427`), no keeper log; `bots list` shows 20 keepers, `bots report` prints `card=miss wrapper=miss log=never(?)` (`/tmp/kake-r12/live/`). |
| app.ds4cc.com | `https://app.ds4cc.com/mcp` | `ds4cc-marketplace/apps-sdk` + `render.yaml` | Render web service (`ds4cc-marketplace-app`, Docker) |

Registry of record: `~/Projects/webzites/fleet/fleet.config.json` (21 rows — <!-- r18 re-census 2026-10-14: ~/Projects/webzites/fleet/fleet.config.json absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
`len(sites)` verified 2026-09-28; status 12 live/3 pruned/3 broken/3 queued;
`expect` tripwires, `sourceDir`, `updatePath`, `status`, `priority`). Dead
rows are `status:"pruned"`/`"queued"` — never deleted. Second registry:
`fleet/grokbots.json` (20 roster rows, mtime 2026-09-20) — one row per keeper
bot, a **separate universe** parity-checked in both directions by
`grokbots --check` (`src/cli.mjs:361`, `:389` reverse loop — r16 re-pin, was `:386`); it lags `fleet.config.json`
(`lucario` missing — see the lucario row above). Config `status` is a
**snapshot, not truth** — 2026-09-28 probe proved `lucario` recorded `live`
while never published; always re-probe before acting. `probe.mjs` has no
`pruned` branch — every row with url+expect is probed equally — but the
universe is url-filtered upstream: `probe`/`status` see only rows with `url`
(`src/cli.mjs:75` → **18 of 21**), while `grokbots --check` verifies all 21
(`checked: fleet.sites.length`, `src/cli.mjs:393`). The three url-less rows
(`ds4cc-kimi-mirror-vault-row`, `snapshot-kimi-pro`, `burnerchrome-com`) are
invisible to probe/status by design — never read a snapshot count as the
fleet count (`corpus/knowledge/free-read-verbs.md`).

Non-sources (classification stands; both dirs **absent from the FS since the
2026-09-28T23:51:31Z `~/Projects` drift event** — r15 path sweep):
`~/Projects/ufofsdbeta` was the UFO-FSD *runtime* repo (no Pages site;
`dist/` was JS build output). `~/Projects/ufofsdbeta-kimi-review` was a *[r20 citation-local 2026-10-19: `~/Projects/ufofsdbeta-kimi-review` absent — absent since the 2026-09-28T23:51:31Z `~/Projects` drift event (r15 path sweep); historical record, not an executable instruction.]*
non-git review snapshot — never publishable source; if either returns,
re-verify, don't assume the r1 findings still hold.
`plazir-15-site/speedrun/` is a frozen 3-run copy of `ds4cc.com/speedrun/`
(`rel=canonical` points to ds4cc.com) — update ds4cc's `speedrun/`, not plazir's.

## Audit → source-fix → publish checklist

1. **Probe, don't guess.** `node ~/Projects/webzites/bin/webzites.mjs probe --all` *[r20 citation-local 2026-10-19: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*
   (or `probe <site-id>`) — the bare `webzites` name is NOT on PATH on this
   host (`command -v webzites` = empty; sibling audits confirm); all commands
   below abbreviate it to `webzites` for readability but the real invocation
   is the node path. GET +
   canary tripwire (`expect.status`, final URL, title regex, marker literal);
   exit 1 on any violation. `webzites status` for last results. Raw `200` is
   not proof: kimi-pro serves `200 + 5995B preview-404 body` — trust `expect`,
   not status alone. **Trust hierarchy: live probe > config fields.**
   `status`/`lastChecked` are snapshots (probe 2026-09-28: config said
   `lucario` live+ maintained, URL had never been published — 404). On any
   conflict, the probe wins and the config row is stale; record it.
   **The fleet is half-instrumented** — `webzites-probe.timer` runs
   `probe --all` every 6h (`SuccessExitStatus=1`) into
   `state/probe-history.jsonl`; `webzites-keeper.timer` is **loaded +
   disabled + inactive (dead), zero journal entries — the daily
   `grokbot tick` has never fired** (r12 systemd read; keeper logs frozen
   at 2026-09-21T03; `corpus/knowledge/keeper-timer-inert.md`). Do not
   expect fresh per-site keeper logs; enable-vs-retire is an operator
   decision (`.ufo/l0-questions.md`, kake round-12 — still unanswered at
   r13 22:5xZ). Check `state/probe-latest.json` age before re-probing —
   **read the `at` field, never the file mtime** (r13 forensics: after the
   r11 clobber + manual `cp` restore, mtime 21:31:45Z vs `at` 18:51:26Z,
   2h40m apart; birth-time = the clobber instant, sha proved the restored
   file IS the r11 backup). Then read
   `corpus/knowledge/ops-automation.md` for history
   semantics (constant `errors[]` on xsnapshot-app = armed NXDOMAIN
   tripwire, not a regression; single-row `total:1` rows are spot
   probes). **Spot-probe trap:** `probe <id>` does NOT merge — `cmdProbe`
   passes the RAW probed subset straight to `saveProbe` (`src/cli.mjs:78`),
   which overwrites `state/probe-latest.json` with only those rows
   (`src/fleet.mjs:39-52`); a 1-id run shrinks the 18-row fleet snapshot to
   `total:1` until the next sweep/tick, while `grokbot tick`
   (`src/cli.mjs:289`) and `bots task` (`src/cli.mjs:647`) merge via
   `mergeProbeResults` (`src/fleet.mjs:30-37`; live-proofed r11:
   `corpus/knowledge/free-read-verbs.md`). Recipe: `cp
   state/probe-latest.json /tmp/probe-latest.backup.json` → run → `cp` back;
   the one appended `total:1` history line is permanent and expected
   (spot-rule suppresses it in deltas). **History transitions without re-probing:**
   `node scripts/probe-delta.mjs` (this repo, read-only over
   `state/probe-history.jsonl`) — suppressed-spot-rule diffing; naive
   consecutive-row diffing emits 42 events of which 40 are phantom. Do NOT
   re-run mutating verbs for audit (`probe --all` writes
   `probe-latest.json` + appends history — `src/fleet.mjs:39-52`,
   `src/cli.mjs:78`); cite LOG.md rounds instead. `webzites status`
   also **exits 1 iff the surviving snapshot has any violated/error row**
   (`src/cli.mjs:99`; snapshot-relative — `probe <healthy-id>` narrows the
   snapshot and flips status to exit 0 while 5 violated + 1 error sit
   fleet-wide; `status --json` always exits 0, `:94-97`) — read its
   stdout, never gate on its exit code.
   Runbook: `corpus/knowledge/probe-delta-alerting.md`.
2. **Check live-vs-source drift** per the table below. Kimi rows:
   `node ~/Projects/webzites/scripts/kimi-surface.mjs sync-check [<id>]` (run *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*
   from any cwd — the script has **no `--help` verb**; usage prints via any
   unknown verb, exit 64; pure HTTP, no browser;
   title+marker verdict — bytes never equal, see pitfalls). GHP rows:
   `webzites grokbot reconcile <id>` compares live bytes vs `sourceDir`.
3. **Fix in the source repo**, commit path-scoped. Never edit live bytes,
   never push from a foreign clone. For no-push workspaces
   (`~/Projects/ephemeral/wz1/*` — **wz1 emptied 2026-09-28T21:42-03:00**;
   recipe only if the workspace is re-created): deliver `git format-patch`
   series + `publish/APPLY.md`; verify `git am --check` against a fresh clone.
4. **Publish stays operator-gated.**
   - GHP rows: the publish verb is `git push origin main` — operator action.
     `deploy-github-pages.sh` (ds4cc) is a *setup* script (CNAME, remote, DNS
     print-out), not the deploy mechanism; `.github/workflows/pages.yml` does
     the deploy on push.
   - kimi-surface rows: prepare/verify only. `sync-check`, `kimi-map`,
     `update|recreate|rebuild <id> --chat=<uuid>` *preflight* are free; any
     `--fire` run consumes ONE metered chat fire and requires `--confirm=<id>`.
     The version-card **Publish / Share→Update click is human** — no verified
     automated publish exists; `PublishApp`/`PublishDeployment` RPCs exist but
     are banned from fleet code. `kimi-webbridge` is unsupported on this Linux
     host; `kimiraikkoner` is DOM chat automation, not a site-ops channel.
  - After the operator clicks publish, verify (all free reads): live URL →
    200, `GetWebsiteByChatID` → `publishedUrl` host + `PUBLISHED`,
    `sync-check <id>` → marker verdict, `kimi-map` refresh. **For
    `charter-ufo-fsd-kimi` (PQ-5) use the armed watch** —
    `corpus/knowledge/publish-queue.md` §r14: E1 (slug URL 404→200) is the
    primary discriminator — a preview-host 200 proves NOTHING; judge body
    by title+marker+vintage, never bytes; `kimi-map` (E5) is browser-gated
    and NEVER gates the "published" verdict; half-states have named
    verdicts (F1 card-published-slug-not-set, F2 wrong-version) — report
    the state, never round up to "published".
   - **Read run journals before judging a fire.** `state/{update,recreate,
     rebuild}-*.json` carries `steps[]`, `fire`, `error.code`. Exit codes
     lie about meter consumption: 5 = aborted before send (free retry),
     6/7 post-`fired` = anomaly, fire consumed, operator inspects.
     Successful recreate/rebuild ends `liveAfter.stillDead:true` + claimed
     version card — the live URL stays 404 until the human publish click.
     Decoder table: `corpus/knowledge/fire-journal-codes.md`.
   - **ds4cc.com/speedrun has its own gated lane.** Keeper:
     `speedrun record → report → prep --write` (fail-closed schema check
     vs authority `speedrun/data/run-*.json`, redaction denylist, stages
     run/curve/manifest bodies under `<out>/prep/`). Operator: `cp` the
     bodies into `ds4cc-marketplace/speedrun/data/`, append the manifest
     entry, `git push origin main`; then `speedrun post` prints the X
     draft (never posts). No HTTP upload API. Full runbook:
     `~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md`; decoded: <!-- r18 re-census 2026-10-14: ~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
     `corpus/knowledge/speedrun-pipeline.md`.
5. **Lease before browser.** `webzites lease acquire --owner <name>
   --ttl-ms 900000`; release in `finally`. The shared burner chrome
   (`the-musketeer` profile, CDP `127.0.0.1:9222`) serializes the whole
   kimi fleet — one op at a time, machine-wide.
6. **Re-pin markers after republish.** `expect.marker` literals are
   deployment-scoped: canary/website-id pins churn per publish; beat-dated
   charter markers (`2026-09-26 scribe beat`, `On 2026-09-18 the grok-web
   scribe transcribed`) churn per scribe beat — 2026-09-28 evidence: the
   `2026-09-26` pin has failed in **every full-universe row since the
   09-27T06:22Z ENTER** (through 18:51:26Z; 22:47Z live re-reads agree),
   i.e. beat pins die ~daily while beats land. **`observed: "absent"`
   semantics:** the marker check is an exact-literal `includes()`
   (`src/probe.mjs:55`) — "absent" means the *pin* wasn't found, never
   that the beat line vanished (r13: live carried
   `2026-09-28 scribe beat (` on every measured shape while pinned to
   `2026-09-26`); pair it with the fuzzy read below before judging.
   Procedure: on a FAIL
   whose only miss is a stale pin, extract the new live literal
   (`grep -o 'scribe beat[^<]*'` on the fetched body), then fix the
   `expect.marker` in `fleet.config.json` — file that edit as a
   publish-queue item (webzites keeper owns it), never edit it silently.

## Freshness sweep — run this before citing anything below

```bash
node scripts/freshness-sweep.mjs            # exit 0 clean · 1 drift · 2 bad input · 64 usage
node scripts/freshness-sweep.mjs --offline  # §paths + §history without any fetch
```

Read-only, zero deps. It re-derives the lane's standing claims against
`corpus/knowledge/freshness-pins.json` in three sections: **§paths** (every
`~/…` citation resolves; an absent target is drift if **any citing location
lacks its own absence annotation**, even when another occurrence is historical
or the target is already in `pathsMissSet`; the frozen set independently
catches *new* misses), **§history** (`probe-history.jsonl` row floor + last-row age + fleet
shape set + `probe-delta` event/last-event pins), **§armed** (PQ-12 beat pin,
PQ-5 E1 watch, PQ-2 gate, ds4cc sitemap, PQ-14 plazir gate + live/source
sitemap gap). Runbook, check-id table and re-pin procedure:
`corpus/knowledge/freshness-sweep.md`.

**Rule (r16):** never copy a pinned literal into prose — cite the check-id and
the pins file. Counts of files that grow on a timer (probe-history rows,
full/spot splits, era families) are **floors or dated measurements, never
constants**; verb-outcome samples (attention lists, ok counts) are **dated
samples** and MUST be re-run before being cited. A frozen sample cannot see
the claim classes it never sampled: r10's "60/60 paths resolve" was retired by
r15 for exactly that reason, and r16's first complete claim sweep (160 claims)
found 15 stale literals in classes no earlier round had a recipe for.

### Owned freshness gate registry

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| freshness-sweep | gate | `node scripts/freshness-sweep.mjs --offline` for this local-only dispatch; bare form requires authorization for network checks | `0=clean` for evaluated checks only; `1=failed/drift`; `2=could-not-evaluate` (input); `64=could-not-evaluate` (usage). Offline/skipped/suspended sections are never proof of a complete publishing check. | `node scripts/freshness-sweep.mjs --selftest` (`--selftest`); caller must isolate `HOME` and `KAKE_SELFTEST_DIR` to temporary lane-local directories; record variable names and isolation shape only, never assigned values. | `corpus/knowledge/freshness-pins.json`; `node .ufo/round-20/replay-proof.mjs` checks all frozen input digests before baseline/candidate comparison | Normal path reads only; selftest writes isolated fixtures. The known static confinement assertion is not a complete write-free proof. **[r20 resume 2026-10-19: region markers are exact standalone lines and case `e2` plants a write at every out-of-region top-level function (selftest 15/15; `node .ufo/round-20/resume/confinement-mutants.mjs` → cb807bc killed 0/25, now 25/25). Still not complete: aliasing, bracket access, multi-line calls, metadata/fd writes and child-process side effects are named residual bypasses.]** | kake |

Where to learn more: `corpus/SOURCES.md` (scoped-tier source registry; platform-mechanism claims cite a tier-A row there — `corpus/QUALITY.md` §Platform mechanism).

## Live-vs-source drift detection

| Row class | Command | What it catches | Blind spot |
|---|---|---|---|
| Any row | `webzites probe <id>` | status, redirect-to-soft-404, title, marker loss; exit 1 on any violated/error in the **probed subset**, exit 2 = unknown id / no sites (usage on stderr, **no write**) | content rot inside a passing marker; **writes state** — `probe <id>` overwrites `state/probe-latest.json` with only the probed row (`src/cli.mjs:78` → `src/fleet.mjs:39-52`; no merge, unlike `tick`/`bots task` `src/cli.mjs:289`,`:647`) + appends a `total:1` history line; backup/restore first or `webzites status` narrows to that row until the next sweep — `corpus/knowledge/free-read-verbs.md` |
| kimi row + `sourceDir` | `node scripts/kimi-surface.mjs sync-check <id>` | title/marker vs source; "in-sync*" = identity OK, **freshness unknown** (live r11: ~Aug-29 mirror verdicts in-sync, exit 0); **exit 1 unless every row ∈ {match,in-sync,no-source,skipped}** (`scripts/kimi-surface.mjs:206-208`); `unpublished404:true` = live body is the 13 409B Kimi 404 sentinel sha `93ddca9a…` (`:180`,`:198`) — dead slot, NOT rot; unknown id exits 1 (`die` `:34`), unknown verb exits 64 (`:1198`) | byte drift — kimi rewrites bytes (sdk-seed.js, cfemail, entity encoding); decide republish by *vintage evidence* not digest; JSON drops `markerSource` → `drift` **with** `titleEqual:true`+`markerLive:true` = source-side marker missing (live r11: ufofsd-charter, plazir27-kimi-page, plazir27runs-on); read-only, never touches state |
| GHP row + `sourceDir` | `webzites grokbot reconcile <id>` | root URL body vs ONE scored `index.html` (depth ≤2): match/in-sync/drift — **read-only** (never touches `probe-latest.json`); labels `src/reconcile.mjs:200-212` (`OK/SYNC/DIFF/LIVE/NOSRC/NODIR/ERR/SKIP`); **exit 1 only on drift/fetch-error/source-missing** (`src/cli.mjs:269-272`) — `no-source`/`no-source-file`/`skipped` exit 0, so `NOSRC` is silent; unknown id = crash exit 1 + stack (un-awaited dispatch `src/cli.mjs:1087` — r16 re-pin, was `:1086`) | all other paths incl. second `index.html`s; **`in-sync` on GHP masks byte drift** — treat as "git fetch sourceDir + spotcheck," see `corpus/knowledge/ghp-subpath-spotcheck.md` |
| kimi bindings | `node ~/Projects/webzites/scripts/kimi-surface.mjs kimi-map` | chat→domain truth: publishedUrl, publishState, version ids; sweeps project chats top-level ListChats misses | chats beyond sweep pages |
| probe-history deltas | `node scripts/probe-delta.mjs` (this repo; `--since`, `--hole-hours`, `--json`) | violated[] ENTER/EXIT, registrations (UNIVERSE), coverage holes >12h; spot-probe + bootstrap phantoms suppressed (naive diff = 42 events, 40 phantom; r10 baseline: 6 events, 0 phantom) | transitions bounded by sweep sampling; marker churn vs outage needs `probe-latest.json` — `corpus/knowledge/probe-delta-alerting.md` |
| Whole fleet | `webzites grokbot tick` | probe + reconcile + keeper log per site | tick is **manual/round-driven only** — the daily keeper timer is disabled and has never fired (`corpus/knowledge/keeper-timer-inert.md`); running it writes state + appends per-site keeper logs |
| Roster/ops reads (r12) | `webzites status --json` · `webzites grokbots --check` · `webzites bots list` · `webzites bots report [--stale N]` | snapshot verdicts (status); registry/card/log parity across all 21 fleet rows (`--check`, exit 1 on gaps); card+wrapper state across the 20 registry rows (list); per-site probe/log/turn ages + gap/stale verdicts (report, exit 1 iff gaps or `--stale` tripped) | all four read-only local reads (r12 sha guard, zero state delta — `/tmp/kake-r12/live/`); `status --json` and `bots list` **always exit 0** — read stdout only; `bots report` probe column is snapshot-relative (inherits the `probe <id>` clobber); queued wrapper-misses are not gaps (`src/cli.mjs:935`); `--stale` never trips unless passed (`src/cli.mjs:836-839`, `:932`) — with the keeper timer inert, any threshold flags all logs STALE |
| Byte-twin copies | `grep -F '<marker>'` + sha256 over fetched body | duplicate slots serving same/foreign content | marker-only equality ≠ byte equality |
| GHP subpaths | walk `sourceDir` → GET `<url>/<rel>` → sha vs `git show origin/main:<rel>` | subpath 404s/rot probe+reconcile can't see (first baseline 2026-09-28: 2 352 paths, 0 true rot, 126 diffs all local git lead/lag) | procedure in `corpus/knowledge/ghp-subpath-spotcheck.md` |
| URL lists (sitemap) | GET every `<loc>` + sourceDir membership | dead listings, foreign content, pre-push listing preview (baseline 2026-09-28: 103 locs **live-side** = 93 ds4cc-staged + 8 plazir-live + 2 charter; source-side re-derivation r16 = 102 — the delta IS the unpushed plazir gate, PQ-14; name the side) | unlisted paths invisible; GHP live-only orphans impossible by construction (deploy artifact = full tree snapshot) — `corpus/knowledge/sitemap-orphan-audit.md` **[r20-correction 2026-10-19: the orphan direction must be checked against the actual uploaded/deployed artifact or build output, not inferred from the checkout; upload-pages-artifact excludes .git/.github and v4 excludes hidden paths by default (v5 adds include-hidden-files); branch builds also apply Jekyll's default exclusions — S001, S002, S004, S006]** |
| kimi subpaths | live-index same-origin link sweep + canonical `sitemap.xml` parity (`dir/`→`dir/index.html`), classify misses by `git log --diff-filter=A` vs publish vintage | per-path staleness quantified (ds4cc mirror 2026-09-28: **75**/93 canonical locs missing — sitemap commit `f3d2ecd` adds 75; "74" in older docs was off by one — **all post-vintage, 0 rot**); `dir/` href rot | byte drift meaningless; `${...}` template literals are noise — `corpus/knowledge/kimi-subpath-audit.md` |
| Vault PROPERTIES[] | `node -e` eval the `const PROPERTIES = [...]` literal in the fetched body + GET each `url` | rendered-link rot WITHOUT a DOM (r9 baseline: 3/10 live-claimed links dead; lucario absent) | PROPERTIES[] is the only link surface — vault body has no other links; `corpus/knowledge/vault-properties.md` |

Vintage evidence that beats digests: dedupe report sha table, keeper logs
(`webzites/reports/keepers/grokbot-<site>.log.md`), max embedded date in DOM,
`kimi-map` version timestamps.

Publish-queue readiness ledger — what each PQ item fixes, its gate class,
source freshness, and verification: `corpus/knowledge/publish-queue.md`.

## Mirror pitfalls (all observed, not hypothetical)

- **Bytes never equal on kimi.** Kimi injects `sdk-seed.js` and rewrites
  cfemail/entities; normalized digest differs by a fixed ~+157B class.
  2026-09-28 evidence: the seed tag itself grew +157B fleet-wide
  (`data-kimi-disable-watermark/analytics/website-env` attributes added) —
  post-publish digest checks MUST normalize the seed tag, and byte deltas
  cannot carry freshness evidence at all. `data-cfemail` was the *only*
  allowed churn class — anything else is real drift. Never sha-compare kimi
  rows; use title+marker+vintage.
- **Site-ids are not host-unique.** `data-kimi-website-id="1a0acf59…"` serves
  on BOTH `ufo-fsd.kimi.pro` AND `ufo-fsd.kimi.page` (2/18, not the "1/17" the
  config note claims) — an `update` fire on one may co-write the other; never
  trust a website-id pin alone.
- **Live 200 slots block `recreate`; `sourceDir:null` blocks `update`.**
  `cmdRecreate` refuses code 3 when the slot isn't the dead-slot sentinel
  (`kimi-surface.mjs:845-849`); `cmdUpdate` refuses at `:483` without
  `sourceDir/index.html`. Sourceless-row recipe (body→`index.html`→set
  `sourceDir`, `--canonical` for the vault twin, `--zip-exclude='assets/*.mp4'`
  for plazir27runson's 147MB films): `corpus/knowledge/vault-properties.md`.
- **Vault PROPERTIES[] needs no browser.** The rendered link surface is a
  `const PROPERTIES = [...]` literal in the fetched body — `node -e` eval +
  GET each `url`. Baseline 2026-09-28: 3/10 live-claimed links dead
  (charter-ufo-fsd.kimi.page, plazir15.kimi.page → 404; plazir27.kimi.pro →
  preview-404); lucario absent from the array entirely.
- **No directory indexes on kimi statics.** `dir/` → 404 while `dir/file` →
  200. GHP is the opposite: `/dir` → 301 → `/dir/` → serves `index.html`
  (verified 2026-09-28: `/plazir-15-site/snake`, `ds4cc.com/magga`). Nav
  links like `href="snake/"` work on GHP, 404 on kimi — convert to
  explicit `dir/index.html` before mirroring. Live proof of the rot class:
  ds4cc.kimi.page's index ships `omarchy-usage/`, `omegag/`, `speedrun/`
  hrefs — all 404 today while their `index.html` twins serve 200; broken
  since publish, unfixable by anything short of a re-publish with
  rewritten hrefs (see `corpus/knowledge/kimi-subpath-audit.md`).
- **One chat = one publish slot + one custom slug.** Firing an update into a
  chat bound to another live site hot-swaps that site. Never fire into
  `1a0c20ea-…` (veigapunk.kimi.page) or `1a049cb5-…` (plazir27runs-on).
- **Similar names, different sites.** `plazir27runson` (Night Trilogy, 15.7KB)
  ≠ `plazir27runs-on` (charter doctrine build, 63KB). `ufo-fsd.kimi.page`
  (vault, byte-twin of veigapunk.kimi.page) ≠ `ufofsd.kimi.page` (frozen
  landing) ≠ `ufo-fsd.kimi.pro` (612B SPA shell). Resolve `publishedUrl` via
  `GetWebsiteByChatID`, not by hosts[] text mention.
- **Dead slots (r9 readiness — `~/Projects/webzites/reports/dead-slot- <!-- r18 re-census 2026-10-14: ~/Projects/webzites/reports/dead-slot-recreate-readiness-r9.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  recreate-readiness-r9.md`).** `plazir15`, `charter-ufo-fsd`, `lucario`
  `.kimi.page` all still 404 (verified 2026-09-28). Charter's `rebuild`
  already produced a verified version card (`efc1830`, preview 8,323B
  markerPresent) — its only remaining gate is the human Publish + slug click.
  plazir15's chat binding is UNRESOLVED (vessel `1a0c2186` pristine vs
  emergent `1a0de2ed` with one unpublished version) — run `kimi-map` before
  any refire. lucario has no bound chat and zero consumed fires (all 3
  journals died at lease-refusal, code 1). Dead slot + empty chat →
  `recreate`; bound-but-unpublished chat with versions → `rebuild`.
  `plazir27.kimi.pro` = Function-Compute ingress serving preview-404.
- **Session/browser traps.** Dead sessions can pass avatar checks (`browser
  status` probes a 401 must-fail + 200 must-pass). Transient 401 mid-poll is
  token-refresh flake — retry once. `t<N>` tab indices renumber on
  open/close — re-derive targets from `/json/list` URLs. `agent-browser open
  --wait` is a silent no-op — use `wait <ms>`. Open `[role=menu]` swallows
  Enter — assert menu count 0. Composer `div.chat-input-editor`; send is a
  click on `.send-button-container` (Enter unverified). `SingletonLock` after
  a crash is tolerated — `browser ensure` rebinds.
- **Source traps.** `ufofsdbeta-kimi-review` (was: no .git; snapshot, not a
  source) — **absent since 2026-09-28T23:51:31Z** (r15 sweep).
  `plazir-15-site/speedrun/` is a frozen copy; its canonical lives in
  `ds4cc-marketplace/speedrun/`. Rows with `sourceDir: null` (vault, ufofsd,
  plazir27runson, kimi.pro slots) have no local source — republish needs
  extracted bytes first, never retype from memory.
- **Filesystem traps.** Case distinguished two real dirs at r16:
  `~/Projects` inode `27238`, lowercase `~/projects` inode `101125103`. *[r20 citation-local 2026-10-19: `~/projects` absent — gone in W6, the 2026-09-29 03:13–03:14Z lowercase-tree consolidation; historical record, not an executable instruction.]*
  W6 (2026-09-29 03:13–03:14Z) absorbed the lowercase tree's children into
  the existing capital root, then removed `~/projects`; `~/Projects` kept *[r20 citation-local 2026-10-19: `~/projects` absent — gone in W6, the 2026-09-29 03:13–03:14Z lowercase-tree consolidation; historical record, not an executable instruction.]*
  inode `27238` (`~/DIRMAP.md:1,7,27`; `magga-2`→`magga` in-window). *[r20 citation-local 2026-10-19: `~/DIRMAP.md` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*
  Therefore lowercase ENOENT is **not safely classifiable as a typo** — check
  `projectsChildrenSet`, `~/DIRMAP.md`, and parent mtimes before deciding.
  Whole cited roots also vanish: r15 caught `ufofsdbeta`,
  `ufofsdbeta-kimi-review` + `ephemeral/wz1` gone inside the
  09-28T23:51:31Z `~/Projects` mtime window — the same instant sibling kasegi
  lost its `bounties` root (L0). ⇒ re-sweep the citation base every freshness
  round; never freeze r10's “60/60 resolve.”
- **Weak markers.** `sdk-seed.js`, `PLAZIR-27`, `ballot`, `snapshot.` are
  boilerplate/misattributed/redundant — they passed 12 cross-body swap
  mutations. Keep the r2 tightened set in `fleet.config.json`; a `null`
  marker is worse (foreign-200 serves flip to silent pass).
- **Fired-but-orphaned runs.** A metered fire that dies before `versionWait`
  (journal `error.code` 4/6/7 after a `fired` step) can leave a version card
  in an unknown chat — 2026-09-26 evidence: plazir15 `recreate` hit code 6
  ("never navigated to /chat/<uuid>") post-fire; ds4cc-kimi-mirror `update`
  consumed a fire then hit code 7 at ListVersions. Recovery is `kimi-map`
  + match by fire-description timestamp, never a blind refire. Full code
  table: `corpus/knowledge/fire-journal-codes.md`.

## Cited paths

- `~/Projects/webzites/` — mission root: `bin/webzites.mjs` (CLI), <!-- r18 re-census 2026-10-14: ~/Projects/webzites absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  `scripts/kimi-surface.mjs` (sync-check/kimi-map/update/recreate/rebuild),
  `fleet/fleet.config.json` (registry), `fleet/fleet.dedupe-report.md`
  (classifications + publish-queue PQ-1…PQ-13), `fleet/kimi-surface-ops.md`
  (verified ops manual, rounds 1–4), `src/probe.mjs` (tripwire impl),
  `src/speedrun.mjs` (record/report/prep/post), `docs/SPEEDRUN-PROTOCOL.md`,
  `repos/` (50 read-only Origin evidence clones — map:
  `corpus/knowledge/origin-repos.md`), `state/probe-history.jsonl`
  (6h cadence), `reports/keepers/repos-r{1..8}.md` (wz-repos lane),
  `~/.config/systemd/user/webzites-{probe,keeper}.{timer,service}`, <!-- r18 re-census 2026-10-14: ~/.config/systemd/user/webzites-keeper.service · ~/.config/systemd/user/webzites-keeper.timer · ~/.config/systemd/user/webzites-probe.service · ~/.config/systemd/user/webzites-probe.timer absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  `agents/webzites-{kimi,polish,repo,speedrun}.md` (keeper cards).
- `scripts/probe-delta.mjs` (this repo) + `corpus/knowledge/probe-delta-alerting.md`
  — runnable history-delta + coverage-hole detector; rules, baseline,
  naive-diff phantom mechanism.
- `scripts/freshness-sweep.mjs` (this repo) + `corpus/knowledge/freshness-sweep.md`
  + `corpus/knowledge/freshness-pins.json` — the standing-claim drift
  instrument: §paths/§history/§armed, exit 0/1/2/64, `--selftest`, pinned
  baselines in JSON. Run it before citing anything in this file (r16).
- `corpus/knowledge/free-read-verbs.md` — the four free-read verbs
  (`probe`/`status`/`grokbot reconcile`/`sync-check`): per-verb universes,
  live-verified exit contracts, the `probe <id>` snapshot-clobber trap +
  merge asymmetry, `probe-history.jsonl` writer semantics. Live-evidenced
  r11 (`/tmp/kake-r11/` artifacts). r12 adds the roster/ops free-reads
  (`status --json`/`grokbots --check`/`bots list`/`bots report`): live
  exit codes, gap/stale predicates, zero-delta sha guard
  (`/tmp/kake-r12/live/`).
- `corpus/knowledge/keeper-timer-inert.md` — the daily keeper timer is
  loaded/disabled/inactive and has never fired; keeper logs frozen at
  2026-09-21T03; charter-ghp beat-pin is a **config-lag + human-edit item**
  (no webzites code writes `fleet.config.json`; scribe push-gate currently
  failing), not a keeper automation block.
- `~/Projects/ds4cc-marketplace/` — ds4cc.com source: `.github/workflows/ <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  pages.yml`, `CNAME`, `deploy-github-pages.sh` (setup only), `speedrun/`,
  `burnerchrome/`, `render.yaml` + `apps-sdk/` (app.ds4cc.com Render service).
- `~/Projects/plazir-15-site/` — plazir15 GHP source: `.github/workflows/
  pages.yml`, `speedrun/` (frozen mirror copy).
- `~/Projects/origin-work/charter-ufo-fsd/` — charter document source. <!-- r18 re-census 2026-10-14: ~/Projects/origin-work/charter-ufo-fsd absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
- `~/Projects/lucario/site/` — lucario.kimi.page source.
- `~/Projects/ufofsdbeta/.ufo/` — wz0/wz1 mission prompts, probe snapshots,
  and wave evidence backing this playbook. **ABSENT since
  2026-09-28T23:51:31Z** (r15 sweep); wave evidence now citation-only.

Hard rule, repeated: publish stays operator-gated. Never `git push`, never
click Publish, never call `PublishApp`/`PublishDeployment`/`UnpublishApp`
from fleet code; prepare, verify, and hand the human a clean recipe.

## Publishing-corpus contract gate — round 21

S019 scopes this gate to evidence discoverability, not live publishing
readiness. Historical metadata remains historical; reconstructed lesson gates
do not manufacture old decisions or non-author review.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| corpus-contract | gate | `node scripts/corpus-contract.mjs --json` | `0=clean` structural census; `1=failed` missing fields/gates; `2=could-not-evaluate` input/read error; `64=could-not-evaluate` usage | `node scripts/corpus-contract.mjs --selftest` (`--selftest`), isolated generated fixtures only | `.ufo/waves/round-21/frozen/before/expected.json`; `node .ufo/waves/round-21/replay-proof.mjs` verifies every snapshot digest before checking the expected red baseline | Normal invocation read-only; selftest owns and removes temporary fixtures only | kake |

Round-21 counting and pointer-audit helpers under `.ufo/waves/round-21/`
are evidence tools, not publishing gates. `measure.mjs` reports the revision
or working-tree input population; `anchor-census.mjs` maps preserved old
lines after metadata prefixes. Their outputs never admit a round.

## Static canonical publishing preflight — round 22

Use `corpus/knowledge/static-canonical-preflight.md` (S020/S021/S026/S027)
for a source-backed offline publisher-policy check over a named set of built
HTML files. This does not restore the old source trees or probe live properties.
Canonical declarations are signals, not guarantees of Google's selection.

| Situation | Decision |
|---|---|
| Built static HTML and explicit expected canonical policy are available | Run `python3 scripts/canonical_audit.py --manifest /absolute/path/to/manifest.json --json`; retain revision and JSON receipt |
| One supported head canonical matches local policy | Local policy clean, not complete publication readiness |
| Missing, conflicting or mismatching declaration | Correct source or justify a policy change; do not silently rewrite expected values |
| Unsupported HTML, invalid manifest or unreadable input | Could not evaluate; use a proper HTML5/browser audit rather than calling it clean |
| Need Google-selected canonical, HTTP headers, redirects, content duplication or JS state | This tool cannot establish it; route browser work to tabi, publishing/account actions to the operator |

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| canonical-audit | gate | `python3 scripts/canonical_audit.py --manifest <local-manifest> --json` | `0=clean` named static publisher policy; `1=failed` policy finding; `2=could-not-evaluate` input/unsupported HTML; `64=could-not-evaluate` usage (stdout still one JSON object, empty findings) | `python3 scripts/canonical_audit.py --selftest` (`--selftest`), isolated local fixtures | Manifest `expectedCanonical` values; committed `.ufo/waves/round-22/cases.json`, `frozen/expected.json`; `python3 .ufo/waves/round-22/replay.py --root .` verifies input digests, then compares every case's exit and finding ids with the pinned cases.json oracle as well as the aggregate exit/accepted/total | Normal invocation read-only, network-free; selftest owns temporary local fixtures only | kake |

The independent matrix/measurement/replay helpers are evidence tools, not
additional domain gates. A missing tool on the baseline is capability absent,
not 32 observed classification mistakes. Legacy paths gate and anchor-census
debts remain exactly as bounded by the round21 non-author verifier.

## Live re-verification — round 23 (property map, 2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/property-map.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [property-map:c1] **HOLD** — The public ds4cc and plazir-15 repositories currently have Pages workflows triggered on push to main, and the ds4cc root CNAME contains ds4cc.com; this verifies repository content, not the live Pages custom-domain setting. Surface: `GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/.github/workflows/pages.yml; GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/CNAME; GET https://raw.githubusercontent.com/veigapunk/plazir-15-site/main/.github/workflows/pages.yml`.
- [property-map:c2] **STALE** — The mapped local source directories for the active plazir front, burnerchrome, and lucario (including lucario/site) are absent; the explicit-path test output is recorded below. The missing ds4cc and charter roots and the plazir dead-slot path are separately annotated as historical/unavailable in the source map. Surface: `test -e /home/vgpnk/Projects/plazir-15-site; test -e /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome; test -e /home/vgpnk/Projects/lucario; test -e /home/vgpnk/Projects/lucario/site`. Correction: As of 2026-10-21, `/home/vgpnk/Projects/plazir-15-site`, `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome`, `/home/vgpnk/Projects/lucario`, and `/home/vgpnk/Projects/lucario/site` are absent, so these mapped local source paths need a verified replacement or an explicit unavailable/history annotation.
- [property-map:c3] **UNVERIFIABLE** — The pathless source declarations (`none on disk`, `none (Vite shell)`) and Kimi chat-binding/empty-vessel claims in the map cannot be decided by the required directory tests or a non-mutating public repository read; no Kimi interaction or MCP call was made, and page-serving status is left to sibling checks. Surface: `SKILL.md rows 19-25; no specific local path for `test -e` and no read-only chat-binding surface used`. Unverifiable: There is no named filesystem path for the pathless source declarations, and verifying Kimi chat bindings would require a separate read-only authority not used or exposed in this lane; chat writes and page-status rechecks are outside scope.
- [property-map:c4] **HOLD** — The charter repository's public README says GitHub Pages deploys from main/root, and its main-branch `.github/workflows` listing returns HTTP 404, consistent with branch deployment without a workflow file. Surface: `GET https://github.com/VeigaPunk/charter-ufo-fsd; GET https://github.com/VeigaPunk/charter-ufo-fsd/tree/main/.github/workflows`.
- [property-map:c5] **UNVERIFIABLE** — The current lucario Pages deployment mode cannot be reverified from the local source or the guessed public repository URL. Surface: `test -e /home/vgpnk/Projects/lucario; GET https://github.com/VeigaPunk/lucario`. Unverifiable: The local checkout is absent and the public GitHub URL returned 404, which does not establish whether the repository is private, renamed, or removed; no live Pages settings authority was available.
- [property-map:c6] **HOLD** — The public Render descriptor points at a Docker web service and `./apps-sdk/Dockerfile`; the cited Dockerfile is present, and one GET to the MCP route receives an HTTP response. Surface: `GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/render.yaml; GET https://raw.githubusercontent.com/veigapunk/ds4cc-marketplace/main/apps-sdk/Dockerfile; GET https://app.ds4cc.com/mcp`.
- [property-map:c7] **HOLD** — The first registry path is absent locally, and the map explicitly marks it as gone and retained only as a historical record. Surface: `test -e /home/vgpnk/Projects/webzites/fleet/fleet.config.json`.
- [property-map:c8] **STALE** — Interpreting the relative second-registry path under the same `~/Projects/webzites` root, the file is absent and the paragraph does not annotate that registry as historical. Surface: `test -e /home/vgpnk/Projects/webzites/fleet/grokbots.json`. Correction: As of 2026-10-21, `/home/vgpnk/Projects/webzites/fleet/grokbots.json` is absent, so mark this second-registry location unavailable/historical or replace it with a verified current absolute path.
- [property-map:c9] **HOLD** — The property map's burnerchrome Kimi surface URL is live. Surface: `https://burnerchrome.kimi.page/`.
- [property-map:c10] **STALE** — The map's listed source directory is present as a current local source path. Surface: `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome`. Correction: As of 2026-10-21, the mapped ds4cc-marketplace/burnerchrome path is absent, but a surviving source candidate is /home/vgpnk/Projects/burnerchrome (VeigaPunk/burnerchrome, commit ee834920de8411f8014236948e2d5b9f5f82dde2); its title and h1 match the live page, not a proved deployment binding.
- [property-map:c11] **HOLD** — The live surface is Kimi-published, as the map's Kimi-surface designation implies. Surface: `https://burnerchrome.kimi.page/ (served HTML head)`.
- [property-map:c12] **UNVERIFIABLE** — The specific owning Kimi chat is 1a0ada42-28e2… Surface: `Public page and read-only Kimi surface only; chat interaction prohibited`. Unverifiable: The public page does not expose its owning chat id, and verifying that binding would require Kimi chat/account access or sending into a Kimi chat, which is outside the read-only bounds.
- [property-map:c13] **HOLD** — The charter GHP front is live at the mapped URL and the final URL matches it. Surface: `https://veigapunk.github.io/charter-ufo-fsd/`.
- [property-map:c14] **HOLD** — The mapped local source directory is absent, matching the row's adjacent historical-record annotation. Surface: `/home/vgpnk/Projects/origin-work/charter-ufo-fsd`.
- [property-map:c15] **HOLD** — The GHP page confirms the canonical-document target locally: its explicit head has one canonical equal to the mapped GHP URL. Surface: `https://veigapunk.github.io/charter-ufo-fsd/`.
- [property-map:c16] **UNVERIFIABLE** — The mapped branch-publishing mechanism is not established by the fetched page or the absent local source directory. Surface: `https://veigapunk.github.io/charter-ufo-fsd/`. Unverifiable: The live HTML does not identify the Pages deployment source, and the mapped source checkout is absent; no authoritative public deployment configuration was queried.
- [property-map:c17] **UNVERIFIABLE** — Every Kimi charter variant currently declares the GHP URL as its canonical. Surface: `https://veigapunk.github.io/charter-ufo-fsd/ (variant pages not fetched)`. Unverifiable: A GHP response cannot establish canonical declarations on separate Kimi variant pages; those URLs were not fetched in this single-surface check.
- [property-map:c18] **HOLD** — The property map assigns charter Kimi variants to the charter GitHub Pages front as their canonical destination. Surface: `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md`.
- [property-map:c19] **HOLD** — The property map identifies the charter Kimi URL as a 404 dead slot. Surface: `https://charter-ufo-fsd.kimi.page/`.
- [property-map:c20] **HOLD** — The property map documents RECREATE as the route for this dead slot. Surface: `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md`.
- [property-map:c21] **UNVERIFIABLE** — No Kimi chat is bound to this charter slot. Surface: `https://charter-ufo-fsd.kimi.page/`. Unverifiable: A public unauthenticated GET cannot determine private Kimi chat binding. No account/API or chat surface was accessed.
- [property-map:c22] **HOLD** — The property map designates ds4cc.com as primary, supporting https://ds4cc.com/ as this mirror's local canonical target; this is a local policy designation, not independent search-engine validation. Surface: `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:16`.
- [property-map:c23] **HOLD** — The mapped DS4CC Kimi mirror URL remains publicly reachable at its listed URL. Surface: `https://ds4cc.kimi.page/`.
- [property-map:c24] **HOLD** — The map's annotation that the listed source directory is absent remains true locally. Surface: `/home/vgpnk/Projects/ds4cc-marketplace`.
- [property-map:c25] **UNVERIFIABLE** — The referenced Kimi chat is still at the approximately Aug-29 vintage recorded by the map. Surface: `https://ds4cc.kimi.page/ (public page; chat not accessed)`. Unverifiable: The public page does not expose the cited chat's content/version history. No Kimi chat was accessed or written to, so its current vintage cannot be established from this allowed surface.
- [property-map:c26] **HOLD** — The property map identifies https://ds4cc.com/ as the primary surface; the single observed GET still reaches it successfully and its head declares the same self-canonical URL. Surface: `https://ds4cc.com/`.
- [property-map:c27] **HOLD** — The property map explicitly preserves the mapped source path as historical after its removal; the corresponding local path is still absent. Surface: `/home/vgpnk/Projects/ds4cc-marketplace`.
- [property-map:c28] **UNVERIFIABLE** — The map's stated GH Actions-on-main publishing mechanism could not be reverified against current source configuration. Surface: `/home/vgpnk/Projects/ds4cc-marketplace`. Unverifiable: The mapped checkout is absent, and the checked public homepage does not disclose the current deployment workflow; no current repository/workflow URL is present in this property-map row to decide this from the assigned surface.
- [property-map:c29] **UNVERIFIABLE** — The map's Actions-versus-branch-publishing custom-domain distinction remains documented but was not independently reverified against current GitHub Pages configuration. Surface: `/home/vgpnk/Projects/ds4cc-marketplace`. Unverifiable: The mapped checkout is absent, and the checked public homepage cannot reveal whether current Pages settings still match this historical configuration note.
- [property-map:c30] **HOLD** — The property map designates the Lucario GHP URL as the canonical surface; this is the correct local expectedCanonical for this surface. Surface: `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md`.
- [property-map:c31] **STALE** — The property map names a local Lucario source checkout with `site/` and `src/lucario/engine.py`. Surface: `/home/vgpnk/Projects/lucario`. Correction: The mapped checkout, its site directory, and its engine file were absent at the checked paths on 2026-10-21; update the source location only after identifying the current checkout.
- [property-map:c32] **UNVERIFIABLE** — The map states that pushes to a Pages branch deploy this surface. Surface: `https://veigapunk.github.io/lucario/`. Unverifiable: The public page response establishes that the URL currently serves content but cannot identify its publishing branch or push trigger, and the mapped local checkout is absent.
- [property-map:c33] **HOLD** — The mapped live-200 status remains true at re-verification. Surface: `https://veigapunk.github.io/lucario/`.
- [property-map:c34] **HOLD** — The mapped Kimi slot currently responds HTTP 404. Surface: `https://lucario.kimi.page/`.
- [property-map:c35] **UNVERIFIABLE** — The historical assertion that this slot was never published is not established by a single current 404. Surface: `https://lucario.kimi.page/`. Unverifiable: A current 404 cannot establish that the URL has never been published historically; no Kimi publication history was available in the checked sources.
- [property-map:c36] **STALE** — The property-map source directory is present at its recorded local path. Surface: `/home/vgpnk/Projects/lucario/site`. Correction: As of 2026-10-21, `/home/vgpnk/Projects/lucario/site` is absent on this host, so the property-map source path is stale here.
- [property-map:c37] **UNVERIFIABLE** — The referenced README still documents a pending, gated first publish. Surface: `/home/vgpnk/Projects/lucario/site/README.md`. Unverifiable: The mapped source directory and README are absent at this host, and the live 404 cannot determine whether the upstream README's publish gate remains pending.
- [property-map:c38] **HOLD** — The property-map GHP front URL is live and its page declares one self-canonical in the head. Surface: `https://veigapunk.github.io/plazir-15-site/`.
- [property-map:c39] **STALE** — A local source checkout is present at the property-map path `~/Projects/plazir-15-site`. Surface: `/home/vgpnk/Projects/plazir-15-site`. Correction: As of 2026-10-21, the mapped local source checkout `/home/vgpnk/Projects/plazir-15-site` is absent on this workstation.
- [property-map:c40] **UNVERIFIABLE** — The front is currently published by GitHub Actions on pushes to `main`. Surface: `/home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml`. Unverifiable: The mapped checkout and workflow are absent locally; the one public page GET confirms served HTML but cannot establish the current GitHub Actions or Pages deployment configuration.
- [property-map:c41] **HOLD** — The property map designates https://veigapunk.github.io/plazir-15-site/ as the plazir15 GHP front and records GH Actions on push to main. Surface: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d599e19bead54b96f589444e9ec64cdf67c28a:SKILL.md > /tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md`.
- [property-map:c42] **HOLD** — The property map records plazir15.kimi.page as a 404 dead slot with a RECREATE path and no bound chat. Surface: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d599e19bead54b96f589444e9ec64cdf67c28a:SKILL.md > /tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md`.
- [property-map:c43] **HOLD** — The mapped public Kimi URL still returns a 404, matching the map's dead-slot status. Surface: `https://plazir15.kimi.page/`.
- [property-map:c44] **HOLD** — The source directory mapped to this Kimi surface is absent on this host, consistent with the row's historical absence note. Surface: `test -d /home/vgpnk/Projects/plazir-15-site`.
- [property-map:c45] **UNVERIFIABLE** — [INFERENCE] For a recreated mirror, the GHP front is the intended canonical target; no current Kimi mirror declaration is established. Surface: `https://plazir15.kimi.page/`. Unverifiable: The URL serves the provider's 404 page rather than mirror content, so no live mirror declaration exists to verify the intended canonical relationship.
- [property-map:c46] **HOLD** — The property map designates the charter GHP URL as canonical for all Kimi variants, so it is the correct local expectedCanonical for plazir27.kimi.page. Surface: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d599e19bead54b96f589444e9ec64cdf67c28a:SKILL.md`.
- [property-map:c47] **STALE** — The property map's plazir27 Kimi URL is presently serving the described charter mirror. Surface: `GET https://plazir27.kimi.page/`. Correction: As of 2026-10-21, the listed URL returns HTTP 404 with the generic Kimi 404 body (sha256 93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966), so it is not serving a live charter mirror.
- [property-map:c48] **STALE** — The current Kimi response serves the 09-18 charter beat with a 09-28 canonical. Surface: `GET https://plazir27.kimi.page/`. Correction: As of 2026-10-21, the listed URL returns a 404 page whose explicit head has no canonical link, so neither the stated 09-18 content nor its 09-28 canonical is present in the live response.
- [property-map:c49] **HOLD** — The mapped live URL remains reachable at the listed root URL. Surface: `https://ufo-fsd.kimi.pro/`.
- [property-map:c50] **HOLD** — The mapped 612B SPA-shell description still matches the public response. Surface: `https://ufo-fsd.kimi.pro/`.
- [property-map:c51] **UNVERIFIABLE** — The map's source-directory field remains `none` for this surface. Surface: `https://ufo-fsd.kimi.pro/`. Unverifiable: A public page response cannot establish whether a local source directory exists; the map provides no path to test, and no local source inventory was checked.
- [property-map:c52] **UNVERIFIABLE** — The surface remains bound to the property-map chat ID `1a0acd51-4122…`. Surface: `https://ufo-fsd.kimi.pro/`. Unverifiable: The page exposes a Kimi website ID, not a chat-to-published-URL binding; the property map says website IDs are not host-unique, and no permitted public response here proves that binding.
- [property-map:c53] **HOLD** — The property-map vault-index URL still serves a live page at its mapped URL. Surface: `https://veigapunk.kimi.page/`.
- [property-map:c54] **UNVERIFIABLE** — The vault has no local source directory available for maintenance. Surface: `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:21`. Unverifiable: The row names no concrete source path to test; the public page cannot establish whether an unregistered local source now exists, and guessing a filesystem scope would not be a bounded re-verification.
- [property-map:c55] **UNVERIFIABLE** — Firing into the named chat can hot-swap the live vault. Surface: `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:21`. Unverifiable: Verifying that side effect would require a chat operation, which is prohibited; the public page does not expose the chat-to-site binding.

## Round 23 gate registry additions and corrections (2026-10-21)

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| live-snapshot | evidence tool (network GET) | `python3 scripts/live_snapshot.py --population <pop.json> --out <dir>` (`--reaudit` offline) | `0` every surface attempted (verdicts are data); `2` bad input (unsafe id, userinfo/non-http URL, duplicate id); `64` usage | none of its own; `.ufo/waves/round-23/counter_selftest.py` exercises its receipts through `measure_c2.py` | `.ufo/waves/round-23/c2-population.json` (sha256 pinned in `measure_c2.py`) | writes only `<dir>/<id>/`; GET only, no credentials; operator-owned surfaces read-only | kake |

- [r23-correction] The `canonical-audit` row above says `replay.py --root .`
  verifies the frozen round-22 matrix. Round-22 replay pins the validator digest
  of `b539cc1` (`5de32200…`); after round 23's validator change it exits 2
  (`snapshot_tampered`) at the tip by design. Run it against a `git archive
  b539cc1` extract to reproduce round 22; at the current tip use
  `python3 .ufo/waves/round-22/matrix.py --root .` (32/32) plus
  `python3 scripts/canonical_audit.py --selftest`.
- canonical-audit verdict-map addition: SVG/MathML and self-closed void tags
  after a closed head are evaluated; any `<base>` after the head is unsupported
  (see `corpus/knowledge/static-canonical-preflight.md` §Round 23).

- [property-map:c56] **STALE** — The Function-Compute ingress fingerprint in SKILL.md still describes plazir27.kimi.pro. Surface: `https://plazir27.kimi.pro/`. Correction: As of 2026-10-21, plazir27.kimi.pro redirects to the Kimi static preview-404 page rather than serving the old Function-Compute response; the historical ingress diagnosis at SKILL.md line 292 is superseded.
- [property-map:c57] **STALE** — The mapped app.ds4cc.com source lives at ds4cc-marketplace/apps-sdk. Surface: `/home/vgpnk/Projects/ds4cc-marketplace/apps-sdk`. Correction: As of 2026-10-21, the mapped apps-sdk source path is absent; HTTP reachability of app.ds4cc.com/mcp does not identify a current local source or deployment configuration.

- [r23-recovery registry clarification] `live-snapshot` exit 2 covers caught
  input, output-I/O and stored-snapshot integrity errors, including a non-string,
  non-null `contentType`; it is not a claim that arbitrary malformed records
  have been exhaustively tested. Run from the lane root:
  `python3 .ufo/waves/round-23/snapshot_probe.py --snapshot-script scripts/live_snapshot.py --validator scripts/canonical_audit.py`
  (targeted loopback regression, 12 cases).
  The retained counter selftest still covers receipt replay, not network truth.


## Round-24 path reconciliation

These dated corrections supersede only current local-state readings of the cited lines; original bytes and coordinates are preserved. Evidence: `.ufo/waves/round-24/c1-receipts/` and `corpus/knowledge/freshness-sidecar.json` (lane-relative).

- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:16 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:19 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:364 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:445 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:448 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:449 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:450 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace/burnerchrome present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:20 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace/burnerchrome present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:423 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
- 2026-10-21: ~/Projects/ds4cc-marketplace/burnerchrome present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at SKILL.md:431 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.

- Additional round-23 correction [property-map:c57] at line 496: the apps-sdk subtree and Dockerfile are present at checkout `1fbdb8ed`; current Render binding remains unverified (w1/R23ReceiptsDs4ccStale.md).

### Preservation-safe paths workflow — round 24

1. Run `node scripts/freshness-sweep.mjs --section=paths --json` and retain its code and full JSON. Re-observe every newMissing/recovered target before changing a pin.
2. Correct original citations through `corpus/knowledge/freshness-sidecar.json` (schema `kake-paths-sidecar-v1`: file, line, token, lineSha256, kind, date, note) and a matching EOF correction block, never by editing original lesson/knowledge lines. Immutable non-author notes live in `corpus/lessons/round-24.md`.
3. Record dated observations; remove recovered targets from `pathsMissSet` to re-arm their next disappearance; add newly cited misses only with a receipt. The gate is local citation conformance, not source restoration or permission to publish.
4. Re-run the paths gate. The target reconciliation counter is `python3 -B .ufo/waves/round-24/measure_c1.py --root . --revision <commit> --json`; exit0 means all 19 frozen targets reconcile and paths exits0, exit1 a failed criterion, exit2 unreadable inputs. Selftest: `python3 -B .ufo/waves/round-24/c1_selftest.py`. Pins: `.ufo/waves/round-24/c1-population.json` and `corpus/knowledge/freshness-pins.json`; scratch writes only to temporary directories; owner kake.
5. New sidecar/vocabulary/recovered-list fixtures are part of `node scripts/freshness-sweep.mjs --selftest`; no domain source tree is written. The current correction-register proof is revision-bound: later source changes require new dated observations, not retroactive rewrites.


### Maintained receipt replay registry — round 24

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| receipt-replay | gate | `python3 -B scripts/receipt_replay.py c1` or `c2 --root . --revision <commit> --json` (both modes require root/revision) | 0 clean receipts; 1 failed receipt criterion; 2 could-not-evaluate input/usage/internal error | `python3 -B scripts/receipt_replay.py --selftest` | round23 populations/digests and BASE embedded in reader; round24 malformed-case population and matrix receipts | Git blobs read-only; isolated temporary validator inputs; no network | kake |
| receipt-replay-matrix | gate (round measurement) | `python3 -B .ufo/waves/round-24/measure_c2.py --root . --revision <commit> --json` | 0 all frozen expectations; 1 failed expectation; 2 could-not-evaluate | same script `--selftest` | `.ufo/waves/round-24/c2-population.json` sha256 checked by matrix; original fixtureBase round23 | disposable clone commits only; never lane Git/jj writes | kake |

Current replay commands supersede the historical round23 readers for new validation; historical examples remain tied to their original revision/digest. Source rationale and exact per-field limits: `corpus/knowledge/static-canonical-preflight.md` Receipt replay hardening (S032–S034). The gate proves structure/replay consistency, never GET provenance, live truth, domain identity or permission to publish.

## Publisher accessibility review preparation — round 25

Use `corpus/knowledge/accessibility-review-packet.md` (S035) to prepare a
publisher-side WCAG 2.2 A/AA review work item. Each criterion card supplies a
manual check, needed evidence, failure example and explicit limitation.
No page is assessed by this packet: every card stays `not-assessed`.
Source inspection or a complete inventory is not WCAG conformance. Rendering,
interaction and assistive-technology observations require separate authorized
evaluation; browser execution remains adjacent ownership and publication
remains operator-gated.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| accessibility-packet | gate (packet structure only) | `python3 -B scripts/accessibility_packet.py --root . --json` | 0 structurally clean; 1 failed packet requirement; 2 could-not-evaluate input; 64 could-not-evaluate usage. Every JSON result keeps websiteConformance=not-assessed. | `python3 -B scripts/accessibility_packet.py --selftest`; focused CLI cases `python3 -B .ufo/waves/round-25/packet_selftest.py --root .` | `.ufo/waves/round-25/population.json`, source-wcag22.html and frozen/expected.json; revision-bound `measure.py` evidence in round25 lesson | ordinary path read-only; selftest synthetic in-memory fixtures; focused tests temporary fixtures; no network or website | kake |

Round-25 current handoff: `corpus/handoffs/accessibility-preparation.md`.
The operator authorizes a named property/build/process scope; tabi receives
authorized browser/AT evaluation, kagi owns any credential custody, and
publishing stays operator-owned. Display actual card instructions with
`python3 -m json.tool corpus/knowledge/accessibility-review-cards.json`.
The packet gate checks structure and quotation binding, not prose semantics
or WCAG conformance. The finite counter pins the source-reviewed card bytes;
new prose requires new source review rather than automatic admission.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| accessibility-packet-counter | gate (round measurement) | `python3 -B .ufo/waves/round-25/measure.py --root . --revision <commit>` | 0 clean fixed packet; 1 capability/packet failed; 2 could-not-evaluate Git/input/pin/tool disagreement; 64 could-not-evaluate usage | same script `--selftest` invokes isolated counter_selftest.py | population/source/reviewed-card SHA256 constants; final corrected snapshot `frozen-final/expected.json`; original frozen/ remains historical structure evidence | read-only Git blobs; candidate execution temporary snapshot; selftest Git writes only a disposable temporary repository with isolated config, never lane index/jj | kake |

The packet row's current frozen proof is
`python3 -B .ufo/waves/round-25/frozen_replay.py --frozen .ufo/waves/round-25/frozen-final`.
Its `--selftest` on that snapshot checks both a clean replay and
snapshot_tampered exit2. Quote and fixture-coverage proofs under round25
are subordinate fixed-fixture evidence, not website checks.

## Source recheck — round 26

Re-verify cited sources from retained bytes, not memory: re-fetch each
recorded URL once (`.ufo/waves/round-26/fetch_sources.py --root . --out <dir>`),
judge each row at its anchor with a row-specific ≤25-word quote, and append
`[r26-recheck S0NN STALE]` corrections to the citing entry only when a
statement is wrong at its own stated scope (QUALITY round-26 adjudication).
Living documents are judged by quote at anchor, never by sha equality.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| source-recheck-counter | gate (round measurement) | `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>` | 0 all 32 rows decided and every adjudicated STALE statement corrected; 1 undecided/finding; 2 could-not-evaluate (Git/input/tampered bytes); 64 could-not-evaluate usage | same script `--selftest` (temporary fixture repository under the wave directory); `.ufo/waves/round-26/text_selftest.py` for the extractor | population sha256 constant; manifest sha256 per fetch; receipts and statements ledger at the measured revision | read-only Git blobs; selftest writes only a disposable fixture repo; no network | kake |
