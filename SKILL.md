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
| ds4cc.com (primary) | `https://ds4cc.com/` | `~/Projects/ds4cc-marketplace` | GH Actions on push to `main` (`CNAME` = ds4cc.com) |
| plazir15 GHP front | `https://veigapunk.github.io/plazir-15-site/` | `~/Projects/plazir-15-site` | GH Actions on push to `main` |
| charter GHP front | `https://veigapunk.github.io/charter-ufo-fsd/` | `~/Projects/origin-work/charter-ufo-fsd` | Pages deploy from branch (no workflow file); canonical doc, all kimi variants `rel=canonical` here |
| ds4cc kimi mirror | `https://ds4cc.kimi.page/` | `~/Projects/ds4cc-marketplace` | Kimi surface, chat `1a073c43-bf42-874a-8000-0907bd80b9dc` — STALE (~Aug-29 vintage) |
| burnerchrome kimi | `https://burnerchrome.kimi.page/` | `~/Projects/ds4cc-marketplace/burnerchrome` | Kimi surface, chat `1a0ada42-28e2…` |
| vault index | `https://veigapunk.kimi.page/` | none on disk | Kimi surface, chat `1a0c20ea-6372…` — NEVER fire into this chat, it hot-swaps the live vault |
| plazir27.kimi.page | `https://plazir27.kimi.page/` | charter repo | canonical kimi charter mirror (stale: serves 09-18 beat, canonical 09-28) |
| ufo-fsd.kimi.pro | `https://ufo-fsd.kimi.pro/` | none (Vite shell) | Kimi surface, chat `1a0acd51-4122…` (612B SPA shell) |
| plazir15.kimi.page | 404 dead slot | `~/Projects/plazir-15-site` | RECREATE path — no bound chat; vessel `1a0c2186-fa12` is empty |
| charter-ufo-fsd.kimi.page | 404 dead slot | charter repo | RECREATE path — no bound chat exists |
| lucario GHP (canonical) | `https://veigapunk.github.io/lucario/` | `~/Projects/lucario` (`site/` + `src/lucario/engine.py`) | Pages branch deploy on push — live 200, verified 09-28 |
| lucario kimi slot | `https://lucario.kimi.page/` — 404, **never published** | `~/Projects/lucario/site` | Kimi surface pending first publish (README: "pending — gated"). Config `status:live` is stale/wrong. |
| app.ds4cc.com | `https://app.ds4cc.com/mcp` | `ds4cc-marketplace/apps-sdk` + `render.yaml` | Render web service (`ds4cc-marketplace-app`, Docker) |

Registry of record: `~/Projects/webzites/fleet/fleet.config.json` (21 rows —
`len(sites)` verified 2026-09-28; status 12 live/3 pruned/3 broken/3 queued;
`expect` tripwires, `sourceDir`, `updatePath`, `status`, `priority`). Dead
rows are `status:"pruned"`/`"queued"` — never deleted. Config `status` is a
**snapshot, not truth** — 2026-09-28 probe proved `lucario` recorded `live`
while never published; always re-probe before acting. `probe.mjs` has no
`pruned` branch — every row with url+expect is probed equally.

Non-sources: `~/Projects/ufofsdbeta` is the UFO-FSD *runtime* repo (no Pages
site; `dist/` is JS build output). `~/Projects/ufofsdbeta-kimi-review` is a
non-git review snapshot — never treat it as publishable source.
`plazir-15-site/speedrun/` is a frozen 3-run copy of `ds4cc.com/speedrun/`
(`rel=canonical` points to ds4cc.com) — update ds4cc's `speedrun/`, not plazir's.

## Audit → source-fix → publish checklist

1. **Probe, don't guess.** `node ~/Projects/webzites/bin/webzites.mjs probe --all`
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
   **The fleet is already instrumented** — `webzites-probe.timer` runs
   `probe --all` every 6h (`SuccessExitStatus=1`) into
   `state/probe-history.jsonl`, and `webzites-keeper.timer` runs
   `grokbot tick` daily. Check `state/probe-latest.json` age before
   re-probing; read `corpus/knowledge/ops-automation.md` for history
   semantics (constant `errors[]` on xsnapshot-app = armed NXDOMAIN
   tripwire, not a regression; single-row `total:1` rows are spot
   probes). **History transitions without re-probing:**
   `node scripts/probe-delta.mjs` (this repo, read-only over
   `state/probe-history.jsonl`) — suppressed-spot-rule diffing; naive
   consecutive-row diffing emits 42 events of which 40 are phantom. Do NOT
   re-run mutating verbs for audit (`probe --all` writes
   `probe-latest.json` + appends history — `src/fleet.mjs:40-45`,
   `src/cli.mjs:998-1002`); cite LOG.md rounds instead. `webzites status`
   also **exits 1 whenever the last probe had any violation/error**
   (`src/cli.mjs:99`) — read its stdout, never gate on its exit code.
   Runbook: `corpus/knowledge/probe-delta-alerting.md`.
2. **Check live-vs-source drift** per the table below. Kimi rows:
   `node ~/Projects/webzites/scripts/kimi-surface.mjs sync-check [<id>]` (run
   from any cwd — the script has **no `--help` verb**; usage prints via any
   unknown verb, exit 64; pure HTTP, no browser;
   title+marker verdict — bytes never equal, see pitfalls). GHP rows:
   `webzites grokbot reconcile <id>` compares live bytes vs `sourceDir`.
3. **Fix in the source repo**, commit path-scoped. Never edit live bytes,
   never push from a foreign clone. For no-push workspaces
   (`~/Projects/ephemeral/wz1/*`): deliver `git format-patch` series +
   `publish/APPLY.md`; verify `git am --check` against a fresh clone.
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
     `sync-check <id>` → marker verdict, `kimi-map` refresh.
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
     `~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md`; decoded:
     `corpus/knowledge/speedrun-pipeline.md`.
5. **Lease before browser.** `webzites lease acquire --owner <name>
   --ttl-ms 900000`; release in `finally`. The shared burner chrome
   (`the-musketeer` profile, CDP `127.0.0.1:9222`) serializes the whole
   kimi fleet — one op at a time, machine-wide.
6. **Re-pin markers after republish.** `expect.marker` literals are
   deployment-scoped: canary/website-id pins churn per publish; beat-dated
   charter markers (`2026-09-26 scribe beat`, `On 2026-09-18 the grok-web
   scribe transcribed`) churn per scribe beat — 2026-09-28 evidence: the
   `2026-09-26` pin failed on two consecutive probes (round-3 extraction +
   round-7 FAIL at 18:51Z, live literal `2026-09-28 scribe beat (`), i.e.
   beat pins die ~daily while the daily scribe lands. Procedure: on a FAIL
   whose only miss is a stale pin, extract the new live literal
   (`grep -o 'scribe beat[^<]*'` on the fetched body), then fix the
   `expect.marker` in `fleet.config.json` — file that edit as a
   publish-queue item (webzites keeper owns it), never edit it silently.

## Live-vs-source drift detection

| Row class | Command | What it catches | Blind spot |
|---|---|---|---|
| Any row | `webzites probe <id>` | status, redirect-to-soft-404, title, marker loss | content rot inside a passing marker |
| kimi row + `sourceDir` | `node scripts/kimi-surface.mjs sync-check <id>` | title/marker vs source; "in-sync*" = identity OK, **freshness unknown** | byte drift — kimi rewrites bytes (sdk-seed.js, cfemail, entity encoding); decide republish by *vintage evidence* not digest |
| GHP row + `sourceDir` | `webzites grokbot reconcile <id>` | root URL body vs ONE scored `index.html` (depth ≤2): match/in-sync/drift | all other paths incl. second `index.html`s; **`in-sync` on GHP masks byte drift** — treat as "git fetch sourceDir + spotcheck," see `corpus/knowledge/ghp-subpath-spotcheck.md` |
| kimi bindings | `node ~/Projects/webzites/scripts/kimi-surface.mjs kimi-map` | chat→domain truth: publishedUrl, publishState, version ids; sweeps project chats top-level ListChats misses | chats beyond sweep pages |
| probe-history deltas | `node scripts/probe-delta.mjs` (this repo; `--since`, `--hole-hours`, `--json`) | violated[] ENTER/EXIT, registrations (UNIVERSE), coverage holes >12h; spot-probe + bootstrap phantoms suppressed (naive diff = 42 events, 40 phantom; r10 baseline: 6 events, 0 phantom) | transitions bounded by sweep sampling; marker churn vs outage needs `probe-latest.json` — `corpus/knowledge/probe-delta-alerting.md` |
| Whole fleet | `webzites grokbot tick` | probe + reconcile + keeper log per site | — |
| Byte-twin copies | `grep -F '<marker>'` + sha256 over fetched body | duplicate slots serving same/foreign content | marker-only equality ≠ byte equality |
| GHP subpaths | walk `sourceDir` → GET `<url>/<rel>` → sha vs `git show origin/main:<rel>` | subpath 404s/rot probe+reconcile can't see (first baseline 2026-09-28: 2 352 paths, 0 true rot, 126 diffs all local git lead/lag) | procedure in `corpus/knowledge/ghp-subpath-spotcheck.md` |
| URL lists (sitemap) | GET every `<loc>` + sourceDir membership | dead listings, foreign content, pre-push listing preview (baseline 2026-09-28: 103 locs, 0 orphans/dead) | unlisted paths invisible; GHP live-only orphans impossible by construction (deploy artifact = full tree snapshot) — `corpus/knowledge/sitemap-orphan-audit.md` |
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
- **Dead slots (r9 readiness — `~/Projects/webzites/reports/dead-slot-
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
- **Source traps.** `ufofsdbeta-kimi-review` (no .git) is a snapshot, not a
  source. `plazir-15-site/speedrun/` is a frozen copy; its canonical lives in
  `ds4cc-marketplace/speedrun/`. Rows with `sourceDir: null` (vault, ufofsd,
  plazir27runson, kimi.pro slots) have no local source — republish needs
  extracted bytes first, never retype from memory.
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

- `~/Projects/webzites/` — mission root: `bin/webzites.mjs` (CLI),
  `scripts/kimi-surface.mjs` (sync-check/kimi-map/update/recreate/rebuild),
  `fleet/fleet.config.json` (registry), `fleet/fleet.dedupe-report.md`
  (classifications + publish-queue PQ-1…PQ-13), `fleet/kimi-surface-ops.md`
  (verified ops manual, rounds 1–4), `src/probe.mjs` (tripwire impl),
  `src/speedrun.mjs` (record/report/prep/post), `docs/SPEEDRUN-PROTOCOL.md`,
  `repos/` (50 read-only Origin evidence clones — map:
  `corpus/knowledge/origin-repos.md`), `state/probe-history.jsonl`
  (6h cadence), `reports/keepers/repos-r{1..8}.md` (wz-repos lane),
  `~/.config/systemd/user/webzites-{probe,keeper}.{timer,service}`,
  `agents/webzites-{kimi,polish,repo,speedrun}.md` (keeper cards).
- `scripts/probe-delta.mjs` (this repo) + `corpus/knowledge/probe-delta-alerting.md`
  — runnable history-delta + coverage-hole detector; rules, baseline,
  naive-diff phantom mechanism.
- `~/Projects/ds4cc-marketplace/` — ds4cc.com source: `.github/workflows/
  pages.yml`, `CNAME`, `deploy-github-pages.sh` (setup only), `speedrun/`,
  `burnerchrome/`, `render.yaml` + `apps-sdk/` (app.ds4cc.com Render service).
- `~/Projects/plazir-15-site/` — plazir15 GHP source: `.github/workflows/
  pages.yml`, `speedrun/` (frozen mirror copy).
- `~/Projects/origin-work/charter-ufo-fsd/` — charter document source.
- `~/Projects/lucario/site/` — lucario.kimi.page source.
- `~/Projects/ufofsdbeta/.ufo/` — wz0/wz1 mission prompts, probe snapshots,
  and wave evidence backing this playbook.

Hard rule, repeated: publish stays operator-gated. Never `git push`, never
click Publish, never call `PublishApp`/`PublishDeployment`/`UnpublishApp`
from fleet code; prepare, verify, and hand the human a clean recipe.
