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
| freshness-sweep | gate | `node scripts/freshness-sweep.mjs --offline` for this local-only dispatch; bare form requires authorization for network checks | `0=clean` for evaluated checks only; `1=failed/drift`; `2=could-not-evaluate` (input); `64=could-not-evaluate` (usage). Offline/skipped/suspended sections are never proof of a complete publishing check. | `node scripts/freshness-sweep.mjs --selftest` (`--selftest`); caller must isolate `HOME` and `KAKE_SELFTEST_DIR` to temporary lane-local directories; record variable names and isolation shape only, never assigned values. | `corpus/knowledge/freshness-pins.json`; `node .ufo/round-20/replay-proof.mjs` checks all frozen input digests before baseline/candidate comparison | Normal path reads only; selftest writes isolated fixtures. The known static confinement assertion is not a complete write-free proof. **[r20 resume 2026-10-19: region markers are exact standalone lines and case `e2` plants a write at every out-of-region top-level function (selftest 15/15 at `02b6dd0`, 36/36 at the round-56 base; `node .ufo/round-20/resume/confinement-mutants.mjs` → cb807bc killed 0/25, now 25/25). Still not complete: aliasing, bracket access, multi-line calls, metadata/fd writes and child-process side effects are named residual bypasses.]** | kake |
| c53_gate_truth.py | gate | `python3 -B .ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py --revision <commit>` | `0=all 7 round-53 Gate/refusal checks pass`; `1=measured defect`; `2=unevaluable evidence`; `64=usage` | `python3 -B .ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py --selftest` | `.ufo/waves/round-53/exec-quality-gate/{real-round52-tip.txt,selftest.txt}`; fixed counter input digest is printed by selftest | Normal path is read-only and reads committed Git blobs only; selftest reads frozen lane-local fixtures; neither writes lane content | kake |

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

Round-26 falsify-wave update: the counter also verifies every population fetch
of a row, rejects in-group containment twins, and checks the statement ledger
for duplicate pairs, rows outside the population and unaccounted tags
(`reclassified`). Self-test: 24 cases, fixtures under `TMPDIR`, never the lane.

## Round27 unadmitted candidate — knowledge-file citing-set completeness

Before re-verifying a publishing source, enumerate every knowledge-file
citation, including grouped/range citations, metadata bands and appended
provenance. `used-by` is routing information, never the reviewed denominator.
The range-aware gate compares that finite citing set with a presence ledger;
it cannot determine whether a quote supports its claim. Keep source-specific
adjudications, historical/procedural artifact judgments and UNVERIFIABLE
statement units separate (`corpus/lessons/round-27.md`, `.ufo/waves/round-27/pairs.json`).

Current consumer input is derived from the unchanged r26 pair reviews plus
round27 judgments, not a replacement for the original313-unit statement
ledger:

```sh
python3 -B scripts/citing_set.py --root . --revision <commit> \
  --population .ufo/waves/round-26/population.json \
  --ledger .ufo/waves/round-27/complete-ledger.json --json
```

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| citing-set | gate (syntactic pair completeness only) | command above; omit `--revision` for an explicit working-tree read | 0 clean; 1 failed pair/range finding; 2 could-not-evaluate input; 64 could-not-evaluate usage | `python3 -B scripts/citing_set.py --selftest`; delegates `scripts/citing_set_selftest.py` over `scripts/fixtures/citing-set/` |29 independent consumer-input cases with fixed exits/finding ids; r27 `frozen/expected.json` pins26 corpus inputs + population/ledger,28 total | normal command read-only; selftest scratch below `/fast/scratch/hyaku/kake-r27`, no network, no live Git/index/jj writes | kake |
| knowledge-citing-count | gate (finite round27 measurement) | `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision <commit>` | 0 all scoped pair review/binding conditions met; 1 missing/finding; 2 could-not-evaluate input/usage/frozen mismatch | same script `--selftest`, real disposable Git clones | original57 minimum and inherited population/ledger tied to declaration be375d9; ancestral discoveries accumulate; first committed fetch manifest/raw hashes; unchanged hash-pinned r26 extractor | read-only Git blobs; selftest writes/commits only its owned scratch clone, no network or live lane mutation | kake |
| citing-set-frozen-count | gate (finite round27 capability measurement) | `python3 -B .ufo/waves/round-27/c2_count.py --root . --revision <commit>` | 0 candidate detects exact original16 omissions, no false positives; 1 measurement failed/absent gate; 2 could-not-evaluate input/usage/tampered snapshot | same script `--selftest`, real disposable Git clones and actual gate | original oracle/contract/28-input hash manifest at declaration be375d9; no candidate rewrite can bless new expected values | read-only Git blobs; owned scratch snapshot/clone only; no network | kake |

The original count implementations remain at be375d9; stricter implementations
and reasons are separately recorded before candidate measurement. Green
structural results never retroactively admit r26 or discharge broader corpus,
source-authenticity, live-site or policy-stopped round24 obligations.

Strict intended C1 acceptance never counts UNVERIFIABLE decided. The actual
candidate remains55/58 with7 known units/3 pairs, but cold tests also expose
a shape-only override route to false green; counter exit0 is not unit-resolution
proof. Current interpretation: `.ufo/waves/round-27/current-interpretation.json`.
The older `strict-c1-disposition.json` is historical six/two evidence only;
it and the original measurements remain unchanged, not current authority.

Focused Git-mode regression (part of the citing-set consumer evidence):

```sh
python3 -B .ufo/waves/round-27/git_name_selftest.py \
  --gate scripts/citing_set.py --tmpdir /fast/scratch/hyaku/kake-r27
```

It compares exact missing/clean identities across working-tree and Git modes
for ordinary, spaced, tabbed, newline and non-ASCII filenames. The saved
pre-NUL-framing prototype under round27 `before/` is only a red-before test
input, never a production alias or fallback.

Source-opening retention boundary: `fetch_group.py --selftest` runs only
non-secret offline fixtures. `--sanitize-existing --root .` performs the
offline migration of this round's own captures, not another GET. HTML is
retained as public visible text only; `receivedSha256/receivedBytes` record
an observed body digest/length, while `sha256/bytes` bind the retained
representation. Received HTML bytes/attributes are not retained, cannot be
reconstructed from that view, and are not claimed byte-identical. Plain
action source may retain received bytes as its manifest explicitly states.
The earlier “raw hashes” shorthand refers to decompressed retained input,
not an assertion of whole-HTTP-body retention or authenticity. No account
validity or security incident follows from a public form-field shape.

Final carry correction: the old uncertainty fields sum6, but a report-disclosed
S007 unit was omitted. The strict measurement consumes hash-pinned round27
`carry-errata.json`: known7 units/3 pairs remain undecided. The earlier six
description is not the total. Likewise raw313 is a mixed-convention field
sum, not a semantic unit denominator. Original57 baseline obligations and
the16-pair C2 oracle remain unchanged.

### Final author verdict — honest stop, not capability admission

The original57-pair scope, original counter and16-pair oracle are preserved.
Actual review coverage is58/58; strict status is55/58 and C1 remains
**unprovable**. C2's exact16/16, real29-case fixtures, Git30 checks and mutant
sensitivity are real bounded evidence, not proof of its full input/interface
bar. Cold readers demonstrate false-greens, hangs/JSON-protocol failures,
identity loss and retention-boundary weaknesses. The full C2 claim is also
**unprovable**; no new repertoire entry or score increase is taken.

These scripts are unadmitted round evidence, not a production admission,
arbitrary-root sandbox or general secret-removal guarantee. Actual8 retained
capture representations were independently checked safe/integral, but received
HTML attributes/bytes remain unproved. The unresolved findings are explicit in
the round report and `unresolved-acceptance.json`; no code repair is claimed
from a finite green or from the void stub smoke. Main owns independent closure.

## Field performance triage — round 28

Knowledge: `corpus/knowledge/field-performance-cwv.md` (S036–S039). Judge at
the 75th percentile, per form factor, over the CrUX 28-day window.

| Metric | Good (S036, S037) | Poor (S037) | Between |
|---|---|---|---|
| LCP | ≤ 2.5 s | > 4 s | needs improvement |
| INP | ≤ 200 ms | > 500 ms | needs improvement |
| CLS | ≤ 0.1 | > 0.25 | needs improvement |

| Situation | kake does |
|---|---|
| Page-level CrUX record exists | Report p75 per metric and form factor with the window end date. |
| Only origin-level record exists | Report it as origin data; never present it as the page's result. |
| No CrUX record | Check the S038 exclusions (final status other than 200, `noindex` or equivalent, root page not discoverable); a raw 200 is not proof. Otherwise too few eligible Chrome visitors is likely but unconfirmed (low traffic, or iOS, WebView or other Chromium audiences send no data). Report "no field data", not pass or fail. |
| Only a lab score (Lighthouse, DevTools) | Use it to guide a fix; give no Core Web Vitals verdict (S036). Running the tool is tabi's work. |
| A CrUX API query is needed | Needs an operator-provisioned Google Cloud key (S039); kake holds none and asks the operator. |

## Project-site base-path triage — round 29

Knowledge: `corpus/knowledge/pages-base-path.md` (S040–S043). A GitHub Pages
project site is served under the owner host plus the repository name — the
default site location is `http(s)://<owner>.github.io/<repositoryname>`
(S040) — while a user or organization site is served at
`http(s)://<owner>.github.io` (S040). On a project site served at its default
location, a root-relative reference that does not start with the base path
(`/style.css`, not `/<repositoryname>/style.css`) points outside the site
[INFERENCE from URL resolution]. Offline gate: `scripts/base_path_audit.py`
(contract frozen in `.ufo/waves/round-29/c2-matrix.json`, `interface` field).

| Symptom | Check | Remedy | Cited ids |
|---|---|---|---|
| Asset 404s only on the project site; the same file loads from a local root server | Run `python3 -B scripts/base_path_audit.py --manifest <dir>/manifest.json` with `basePath` `/<repositoryname>/` and one page per built HTML file; exit 1 with reason `outside_base_path` names the element, attribute and value | Make the reference relative or base-path-prefixed. Jekyll: set `baseurl` and write the reference through `relative_url` (S041, S042). Vite: set `base: '/<REPO>/'` in `vite.config.js` (S043) | S040, S041, S042, S043 |
| Links jump to the owner root (`https://<owner>.github.io/…`) instead of staying under `/<repositoryname>/` | Same audit run: a root-relative `href` such as `/about/` resolves to the owner host root, outside the base path, and is reported as `outside_base_path` | Do not hand-write the project path. Jekyll `relative_url` prepends the `baseurl` config value (S042); Vite `base: '/<REPO>/'` (S043) | S040, S042, S043, S041 |
| Site is correct on its custom domain and broken at the `github.io` project URL (or the reverse) | Compare the URL the site is served under with the configured base path. Vite needs `base: '/'` for `https://<USERNAME>.github.io/` or a custom domain and `base: '/<REPO>/'` for `https://<USERNAME>.github.io/<REPO>/` (S043); Jekyll project output is available under a subpath of the user-pages subdomain "unless a custom domain is specified" (S041) | Set the base path for the mode that is actually serving: custom domain or user site → root base; project site → repository subpath | S040, S041, S043 |
| A `base` element in the head rewrites relative references | Inspect the first `base` element with an `href`; it alone sets the document base (S024), so `base href="/"` moves a relative `style.css` outside the project path even though the reference itself looks relative | Keep the base element inside the base path (or remove it) and re-run the audit; the tool reports the moved reference with reason `outside_base_path` | S040, S024 |
| Local preview is green but the deployed project site is not | A Jekyll preview from the site root cannot show the failure: S041 previews with `bundle exec jekyll serve --baseurl=""` (S041). Whether a Vite preview shows it is not settled by S043 | Treat a root preview as non-evidence for base-path correctness; the audit over built HTML is the check | S040, S041 |
| Audit returns exit 2 `could-not-evaluate` or exit 64 | Read the JSON on stdout: exit 2 means `input_invalid` or `page_outside_base_path`, exit 64 is a usage fault; neither is a clean verdict | Fix the manifest (`version` 1, `basePath` starting and ending with `/`, non-empty `pages`, each page URL under the base path) and re-run; do not report "clean" | S040, S043 |
| The audit reports `outside_base_path` on an `<a href>` pointing to another project on the same owner host (for example `https://<owner>.github.io/<other-repo>/`) | Read the element: a navigation link (`a`, `area`, `form`) to a sibling project is intended to leave this project's base path; a subresource (`link`, `script`, `img`, `source`, `iframe`, `audio`, `video`, `track`, `embed`, `video[poster]`) outside it is the breakage class. Round-29 real-input run: all 4 findings on the round-23 snapshots of three owned project sites were such sibling links (`.ufo/waves/round-29/real-input/out/`) | Keep intended sibling links and record them as reviewed; fix only references meant to stay inside the project | S040 |

### Base-path audit gate registry — round 29

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| base-path-audit | gate (offline static project-site base-path policy) | `python3 -B scripts/base_path_audit.py --manifest <dir>/manifest.json` | 0 clean; 1 failed-policy (`outside_base_path`); 2 could-not-evaluate (`input_invalid`, `page_outside_base_path`); 64 usage | `python3 -B scripts/base_path_selftest.py` over `scripts/fixtures/base-path/` (30 matrix fixtures plus 15 round-29 regression fixtures `X01`–`X15`), comparing exit, verdict and reason tuples | frozen matrix `.ufo/waves/round-29/c2-matrix.json` sha256 `75c08f64…`, counted by `python3 -B .ufo/waves/round-29/c2_matrix_count.py --root . --revision <commit>` | none (reads local files, no network, no writes) | kake |

## Render static-site triage — round 30

Knowledge: `corpus/knowledge/render-static-sites.md` (S049–S052). A Render
static site is served from the build output of a linked Git repository:
“Render automatically updates your site with every push to your specified
branch” (S049), and “Each site receives a unique onrender.com URL” (S049) that
a custom domain can sit in front of. This table is platform semantics read
from Render's own documentation; it measures no owned property and makes no
live request. Retained visible text and receipts:
`.ufo/waves/round-30/sources/` (`S049.txt`…`S052.txt`, `receipts.json`).

| Symptom | Check | Action | Cited ids |
|---|---|---|---|
| The site still serves the previous release after a push to the deployed branch | Read the deploy status of that build first. S049: “each build is fully atomic”, and “we deploy it and immediately invalidate our CDN caches so your users always see the latest working version of your site” — a build that succeeds is published whole and its CDN caches are invalidated at once | A failed build is fixed as a build failure, not as a caching problem. If the build succeeded and the old bytes are still served, [INFERENCE] Render's own invalidation is probably not the cause: look for a CDN, proxy or service worker in front of the site, and for a different branch serving the domain. [INFERENCE — no source here names a cause for stale content after a green build] | S049 (Immediate cache invalidation): “each build is fully atomic”; “we deploy it and immediately invalidate our CDN caches so your users always see the latest working version of your site” |
| A plain HTTP request is not upgraded to HTTPS | Both pages state this as platform behaviour: S049 “Render automatically redirects HTTP traffic to HTTPS”; S052 “All HTTP traffic to a custom domain is automatically redirected to HTTPS” | Do not spend a redirect rule on the upgrade — the platform already does it. If the upgrade does not happen, the request is probably not reaching the Render site (for a custom domain: DNS and verification status), or something in front answers first. [INFERENCE] | S049 (Redirects and rewrites): “Render automatically redirects HTTP traffic to HTTPS”; S052 (Custom Domains on Render): “All HTTP traffic to a custom domain is automatically redirected to HTTPS” |
| A redirect or rewrite rule has no effect on a path that has content | S050: “Render does not apply redirect or rewrite rules to a path if a resource exists at that path” — “Instead, Render simply serves the resource at that path” | Rename or delete the file that occupies the path, or point the rule at a path with no resource. A rule cannot shadow a file that is already deployed; the file wins | S050 (Rule matching and ordering): “Render does not apply redirect or rewrite rules to a path if a resource exists at that path”; “Instead, Render simply serves the resource at that path” |
| A rule for the site root (`/`) cannot be created, or a root rule never fires | S050: “You can't apply redirect/rewrite rules to your domain root”, and “Each Source requires at least one URL path component” | Put the wanted behaviour in the content at the root, or in a rule whose Source carries at least one path component. The domain root is out of scope for rules | S050 (Which action to use?): “You can't apply redirect/rewrite rules to your domain root”; “Each Source requires at least one URL path component” |
| Deep links in a client-side-routed app (react-router, Vue Router) answer 404 | S050 names this case: “you'll handle all requests from a single path like /index.html”; its matching flow ends “Return 404 Not Found” when no rule matches a path | Add a rewrite from `/*` to `/index.html` so every unmatched path serves the app shell. Keep the redirect action for real moves: a redirect “Instructs the browser (or any other client) to switch URLs to the rule's destination via a 301 Moved Permanently response code” (S050) | S050 (Which action to use?, Rule matching and ordering): “you'll handle all requests from a single path like /index.html”; “Return 404 Not Found”; “Instructs the browser (or any other client) to switch URLs to the rule's destination via a 301 Moved Permanently response code” |
| A custom response header is missing, or missing only on the custom domain | S051: “Because static sites don't have a server-side component that can inject custom HTTP response headers”, so headers are defined in the dashboard; “The header path must be a relative path without the domain”; “It will be matched with all custom domains attached to your site”; “The header key is normalized and the value is appended to it to form the response” | Give the header a relative path (no domain in it) so it covers the custom domain as well, and expect the header key in normalized form (S051 says the key is normalized; its example shows lower case, `cache-control: public, max-age=86400`). [INFERENCE] a header missing on one attached custom domain but present on another points at the path rule, since S051 matches a rule against all attached custom domains; S051 says nothing about the onrender.com host | S051 (HTTP Headers for Static Sites, Header syntax): “Because static sites don't have a server-side component that can inject custom HTTP response headers”; “The header path must be a relative path without the domain”; “It will be matched with all custom domains attached to your site”; “The header key is normalized and the value is appended to it to form the response” |
| A newly added custom domain answers 502 Bad Gateway, or verification never completes | S052: “If verification fails, your DNS settings might not have propagated yet”; “If you see a 502 Bad Gateway error, Render might still be updating routing rules for your service” | Treat both as provisioning, not as a broken site: wait a few minutes and press Verify again, and confirm that DNS points at Render. A 502 in the first minutes after adding the domain is the documented state, not a verdict | S052 (3. Verify your domain): “If verification fails, your DNS settings might not have propagated yet”; “If you see a 502 Bad Gateway error, Render might still be updating routing rules for your service” |
| The old `onrender.com` hostname now answers 404 after a custom domain was added | S052: “After you disable your onrender.com subdomain, all requests to it receive a 404 response” — “These requests do not reach your service”; the switch is `renderSubdomainPolicy: disabled` (dashboard: Render Subdomain → Disabled) | If the subdomain was disabled on purpose, the 404 is the expected result, not a fault. Re-enable it (dashboard toggle, `render.yaml` field or API) when the fallback host is wanted again | S052 (Disabling your onrender.com subdomain): “After you disable your onrender.com subdomain, all requests to it receive a 404 response”; “These requests do not reach your service”; “renderSubdomainPolicy” |

### What this table does not settle

- These are Render's platform pages, opened once each at 2026-10-22T11:49Z
  (HTTP 200). They say what the platform documents, not what any owned property
  does; no live request to an owned site was made for this table.
- The pages describe the static-site side only. S049: “Deploying a dynamic
  site, such as a Rails app? Create a web service instead of a static site” —
  the fleet's Render surface in this playbook is a web service
  (`app.ds4cc.com`, `ds4cc-marketplace-app`, Docker), so the static-site rows
  do not transfer to it.
- Nothing here covers the build output, the repository, the DNS provider's
  console, or the onrender.com fallback host's own content. Rows that need one
  of those say which side to look at; they do not guess the answer.
- Freshness: re-open the four pages before citing them again. The learning-claim
  counter for this round is
  `python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision <commit>`.

## Citing-set reason-code registry — round 30

Gate `scripts/citing_set.py`; fixture runner `scripts/citing_set_selftest.py`
over `scripts/fixtures/citing-set/` (45 cases at the round-56 tip; 41 when this sentence was written). A case's `expected.json` lists
findings either as finding-id strings (legacy: the runner compares the sorted
id multiset) or as `{"id": …, "reason": …}` objects (the runner compares the
sorted multiset of (id, reason) pairs exactly); one form per case. An optional
`case.json` builds run-time inputs (a FIFO, an empty directory, a Git commit,
a nested repository root, extra arguments) in a copy under `--tmpdir`; the
committed fixture is never changed. Since round 30 the gate also refuses
duplicate JSON member names (`document_duplicate_key`) and NaN, Infinity,
-Infinity or overflowing numbers (`document_nonfinite_number`) at any depth;
population ids must match `S` plus three or more digits; any of `--root`,
`--revision`, `--population` or `--ledger` given twice (any spelling,
abbreviations included) is a usage error, exit 64; the corpus walk is
iterative; and every input-document open adds `O_NOCTTY`.

| Reason code | Fixture case(s) naming it |
|---|---|
| `document_not_regular_file` | `30-document-not-regular-file` |
| `document_not_json` | `15-invalid-json-population`, `31-document-not-json` |
| `corpus_directory_missing` | `32-corpus-directory-missing` |
| `corpus_empty` | `33-corpus-empty` |
| `not_a_directory` | `34-not-a-directory` |
| `population_id_unreachable` | `35-population-id-unreachable`, `40-population-id-short-digits` |
| `revision_not_found` | `36-revision-not-found` |
| `root_not_repository_top_level` | `37-root-not-repository-top-level` |
| `document_duplicate_key` | `38-document-duplicate-key` |
| `document_nonfinite_number` | `39-document-nonfinite-number`, `41-document-nonfinite-overflow` |
| `descending_range` | `13-descending-range` |
| `span_too_large` | `14-oversize-range` |
| `document_shape_invalid` | `16-invalid-population-shape` |

Codes the gate can emit that no committed fixture names yet (12):
`absolute_path_not_allowed`, `corpus_directory_unreadable`,
`corpus_file_not_utf8`, `document_not_utf8`, `document_unreadable`,
`empty_path`, `git_command_failed`, `git_unavailable`, `not_a_regular_file`,
`path_escapes_root`, `root_not_a_directory`, `symlink_rejected`. They are
uncovered behaviour, not regression coverage (`corpus/QUALITY.md`, "A
committed fixture asserts the reason code"). Self-test:
`python3 -B scripts/citing_set_selftest.py --root . --tmpdir <dir>` (exit 0
clean, 1 a case mismatched, 2 could not evaluate). Round-30 evidence:
`.ufo/waves/round-30/c1_reason_count.py` and `c1_strict_checks.py`.

## Render web service and Blueprint triage — round 31

Source entry: `corpus/knowledge/render-web-services.md` (S057–S060). Use it
for the lane's one Render property, the `app.ds4cc.com` Docker web service
(`render.yaml` in `~/Projects/ds4cc-marketplace`). Read-only: kake prepares
and checks, the operator deploys.

| Symptom | Check first | Source |
|---|---|---|
| Deploy never goes live and is cancelled | Do all new instances pass the health check together? A deploy that does not reach that within 15 minutes is cancelled and the old instances keep serving | “If this condition is not met within 15 minutes, Render cancels the deploy and continues routing traffic to your service's existing instances.” (S060) |
| Service gets no public traffic | Does the app listen on host 0.0.0.0, on the port Render expects (default 10000)? | “Your web service must bind to a port on host 0.0.0.0 to receive HTTP requests from the public internet.” (S058) |
| Health check fails although the route exists | Does the route answer 2xx or 3xx within five seconds, and does the app accept the Host header Render sends (a verified custom domain, else the onrender.com host)? | “For HTTP checks , Render considers a check successful if the instance responds with a 2xx or 3xx status code within five seconds.” (S060) |
| A running instance drops out, then restarts | Failing checks for 15 seconds stop routing; 60 seconds restart it | “If an instance fails consecutive health checks for 60 seconds, Render automatically restarts the instance .” (S060) |
| A secret changed in render.yaml did not reach the service | `sync: false` values are asked for only when the Blueprint is created; set them in the dashboard | “When you update an existing Blueprint, Render ignores any environment variables with sync: false .” (S057) |
| Build cannot find the Dockerfile | `dockerfilePath` is relative to the repository root; default `./Dockerfile` | “The path to the service's Dockerfile , relative to the repo root.” (S057) |
| A file the image needs is missing at build | `.dockerignore` filters the build context; `dockerContext` defaults to the repository root | “Render omits files and directories from your build context based on your .dockerignore file.” (S059) |
| A secret appears in image layers | Service variables become build arguments; use secret files for build-time secrets | “In your Dockerfile, do not reference any build arguments that contain sensitive values (such as passwords or API keys).” (S059) |

What this table does not settle: the live service's plan, region, deploy
trigger and attached domains (omitted keys keep their current values, S057),
health-check interval and timeout settings (not in the retained pages), and
whether the service is deployed at all. Nothing here was observed live.

## Citing-set runner containment — round 31

`scripts/citing_set_selftest.py` refuses, as a failed case and before the
gate starts:

- a `case.json` `argv` option that is not `--name` or `--name=value` with
  `name` a prefix of root, revision, population or ledger and of no other gate
  option (json, selftest, help); values (tokens not starting with "-") pass.
  `--selftest`, `--self`, `--json`, `-h` are refused. Option values are not
  restricted: a case could still pass `--root=/elsewhere`; that path is read
  only (wave-1 `ReviewHostileContract` F2, not routed).
- a case directory holding an entry named `.git` at any depth;
- a `git_commit` with no earlier `git_init`; setup Git commands name
  `--git-dir`/`--work-tree` inside the copy and set `GIT_CEILING_DIRECTORIES`
  to the copy's parent; the gate subprocess gets `GIT_CEILING_DIRECTORIES` set
  to the scratch case root;
- an `expected.json` that is a symlink, not a regular file, or over 1 MiB
  (opened with `O_NOFOLLOW | O_NONBLOCK | O_NOCTTY`);
- a symlink in the fixture directory (a failed case, never a skip).

Check the refusals:

    python3 -B scripts/citing_set_hostile_selftest.py --root <tree> --tmpdir <scratch dir> [--runner <path>]

Exit 0 every hostile spec refused with no harm; 1 a spec not refused (or harm
seen); 2 bad input. Specs live in `scripts/fixtures/citing-set-hostile/P<n>-*/hostile.json`;
the hostile files themselves are built at run time, never committed. Probe
numbers follow the specs, not the closure's gap numbers: P1=N1, P2=N2, P3=N3,
P4=N5, P5=N6.

Still open, carried by name (none closed this round): the round-27
IDENTITY-PATHS, RETENTION-FRAGMENT, RETENTION-TRUST-BOUNDARY and
C1-UNIT-OVERRIDE families; the socket `document_unreadable` label; 12 of 25
reason codes without a fixture; deep corpus and `O_NOCTTY` guarded by round
counters only; the four round-30 strict-checker holes; runner mutants m2, m4
and m5 (still surviving at `f1ffb81`, wave-1 `ScoutOpenFamiliesLedger`). New
this round, not repaired: a setup `fifo` step on `.gitattributes` makes a
later `git add -A` block until the case timeout (wave-1
`ConnectSiblingOverlap`), and the gate's own Git calls have no timeout.

## Citing-set runner containment — round 31, wave-2 repairs and narrowings

Round-31 wave 2 (attempt 2, `.ufo/waves/round-31/a2-w2/`) attacked the section
above. Repairs in `scripts/citing_set_selftest.py`:

- A symlink in the fixture directory is now a failed case even when its name
  starts with "." (before, a dot-named symlink such as `.h5` was skipped
  silently: `CriticSymlinkCases`, `CriticC1Wording`). Spec P5 gained the
  variant `.h5b`; the earlier runner fails it.
- An `argv` option name must be a prefix of exactly one valued gate option, so
  the ambiguous `--r` is refused by the runner instead of the gate's exit 64
  (`CriticArgvAllowlist`, wave-1 `ReviewHostileContract` F1).
- A `--tmpdir` whose scratch case path contains `os.pathsep` (":") is refused
  as could-not-evaluate: Git splits `GIT_CEILING_DIRECTORIES` on it with no
  escape, which switched the ceiling off (`CriticGitPins`).
- The `expected.json` open error says "symlinks are refused" only for ELOOP
  (`CriticExpectedRead`).

Narrowings of the section above:

- `--root=/elsewhere` cannot pass: the runner already passes `--root`,
  `--population` and `--ledger`, and the gate refuses a repeated option (exit
  64). Only `--revision` takes a value from a case (`CriticArgvAllowlist`,
  `CriticC1Wording`).
- The Git pins (`--git-dir`/`--work-tree`, setup and gate
  `GIT_CEILING_DIRECTORIES`, the `GIT_DIR`/`GIT_WORK_TREE` drop) are not
  probed: a runner without them still scores the C1 counter 5/5 and passes the
  hostile selftest (`CriticC1Wording` mutant). The specs cover the five routed
  shapes only; `--json`, `-h` and a nested `.git` are refused by code, not by a
  committed spec.
- "a FIFO cannot block the run" holds for a FIFO at `expected.json` only.

Still open, added to the carried list: a setup `fifo` on `.gitignore` blocks
`git add` like `.gitattributes` (`CriticOpenItemsCarried`); a Git process the
gate starts may outlive the gate's timeout, since the runner kills only the
gate [INFERENCE, not run]; runner mutants m2, m4 and m5 also survive at the
`c88b97e` runner (`5371530d…`); dot-named real directories, regular files and
FIFOs at the top of the fixture directory are skipped (harmless, documented
here).

Correction to "Render web service and Blueprint triage — round 31" (wave-2
`ReviewSkillTriageTable` F1): the `dockerContext` row's default ("defaults to
the repository root") comes from S057 (“If omitted, Render uses the repo
root.”), not S059. The port row's default 10000 is S058's “The default value
of PORT is 10000 for all Render web services.”

Hostile selftest control (wave-2 `ReviewHostileSelftestCode` F1, F2): each
spec run now also holds `h0-control`, a benign copy named like a hostile case
that must not fail, so a runner that refuses cases by name no longer passes
(`verification/a2-fixes/hostile-selftest-control-name-sham.json`: exit 1;
the `c88b97e` selftest passed the same sham, exit 0). A spec case name with
NUL is refused at load. The frozen round-31 C1 counter still trusts the
runner's reported failure names, so a sham committed as the runner can still
score it 5/5; read the counter with the hostile selftest and the code review.
Open: symlinked spec directories are skipped, and the spec directory itself
may be a symlink (F3, F4).

## Upstream source moved after a pin — round 33

Grounded in one observed case: S062 pins ds4cc-marketplace at `1fbdb8ed`;
upstream `main` moved one commit to `7fc6aa2f` (S065, S066); the local
checkout `~/Projects/ds4cc-marketplace` stayed at `1fbdb8ed`. Draft by wave-1
seat `ScribeSkillPinAdvanceTable` (`.ufo/waves/round-33/w1/`), trimmed by the
L1. Counts stay dated measurements (r16 rule above).

| Observation | Action | Evidence command (round-33 result) |
|---|---|---|
| Local checkout behind the remote | Read the checkout as a witness of its own commit only; get new bytes from a sandbox clone; never fetch into the operator's checkout | `git ls-remote <url> HEAD` vs `git -C <checkout> rev-parse HEAD` (`7fc6aa2f` vs `1fbdb8ed`) |
| Remote moved, but every path a row reads is blob-identical | Keep the old row and its statements at their commit scope; record a HOLD note; no correction | `git rev-parse <old>:<path> <new>:<path>` per path (four S062 paths identical; `w1/ScoutRenderFilesStillCurrent.md`) |
| Remote moved and a read path changed | Re-open that path at the new commit with a located quote; append a correction only where a sentence is wrong at its stated scope | `git diff --stat <old> <new> -- <paths>` (empty this round) |
| Sitemap population changed | Re-derive the count from retained bytes at the new commit, state it with the commit beside it, mark older counts historical | XML-parse `<loc>` of the retained sitemap (97 → 100; `c2_pin_count.py` c4) |
| New pages under an audited path | Run the offline canonical and base-path audits on the retained pages; `clean` is a static result, not a deploy or index claim | `scripts/canonical_audit.py --manifest <m>` (3 × clean); `scripts/base_path_audit.py` base `/` (clean; `w1/ExecNewPagesRefIntegrity.md`) |
| Whether the new commit was published | Read the forge's own run record for that commit; it says the workflow ran, not what the host serves now | `gh api repos/<o>/<r>/actions/runs?head_sha=<sha>` (Pages deploy success, run 39644779773; S066) |
| A live predicate in `freshness-pins.json` names the old state | Flag it; re-pin only in a round that runs the sweep's armed section | `pq2Remote` `e6bd0718`, `sitemapStatus` 404 flagged, not re-pinned this round |

## Citing-set runner — round 33

- The runner reports `code` next to `reason` for setup refusals
  (`setup_commit_before_init`, `setup_commit_without_repo`, `setup_failed`;
  other refusals `null`). A hostile spec pins the refusing layer with
  `reason_code` (P6). Probe: `.ufo/waves/round-33/c1_code_probe.py --rev <rev>`
  (four variants; a kill counts only with `guard_ok`); strict supplement
  `.ufo/waves/round-33/c1_strict_supplement.py --rev <rev>`.
- Without `--tmpdir` the runner now uses a private directory under
  `/fast/scratch/hyaku/kake-r27` and removes it, so concurrent
  `citing_set.py --selftest` runs no longer collide (four concurrent runs:
  0 of 4 failed after; 3 of 4 failed at base `5777d5a`; round 32 saw 4 of 4;
  `.ufo/waves/round-33/verification/concurrency-*.txt`). The selftest scratch still lives below that root.
- `read_expected` OSErrors and stray non-directory fixture-root entries are
  reported, not raised or skipped. The hostile selftest refuses
  non-directory or symlinked entries in its spec directory (exit 2) and
  whitespace-only `reason_contains`/`reason_code` values, which closes the
  round-31 "symlinked spec directories are skipped" note above for entries
  inside the spec directory; a symlinked spec directory itself is still not
  refused.
- Open: Git-pin mutants m3d, m3f and m3g (round-33 lesson); the runner's
  option allowlist still duplicates the gate's option names (a patch deriving
  it from the gate parser was rejected: it imports `citing_set` from the
  runner's own directory, which breaks runner copies the probes run from a
  temporary path).

Round-33 wave-2 corrections to "Citing-set runner — round 33" above
(`w2/CriticC1Verdict.md`, `w2/ExecStrayEntriesRepro.md`,
`w2/MutStrayEntriesCheck.md`, `w2/ExecReadExpectedRepro.md`):
- "for setup refusals" is too broad: only the load-time commit-before-init
  check and apply-time setup failures carry codes; the other `case.json`
  load checks, argv refusals and copy failures report `code` null.
- Concurrency units: round 33 counts failing runs in one trial of four
  concurrent default runs; round 32's "4 of 4" counted two-run pairs.
- Stray fixture-root entries: at `e490381` a dangling symlink or a symlink to
  a file also made the run exit 2; since the follow-up commit a symlink of
  any kind is again a per-case refusal (exit 1), and only regular files and
  FIFOs make the run exit 2. Dot-named directories are skipped by design. No
  committed check fails when the stray-entry refusal is removed.
- The `read_expected` change is defensive: no tried shape (mode 000,
  directory, FIFO, dangling symlink) raised an OSError at base either.
- The hostile selftest now reports an unreadable spec directory as exit 2
  with a JSON error instead of a traceback (`w2/ReviewHostileHardening.md`
  F1).

## Link-preview metadata — round 34

Grounded in S067 (ogp.me), S068 (Facebook sharing guide), S069 (Slack robots), S070
(Mastodon PreviewCard), and the tool contract in `.ufo/waves/round-34/c1-matrix.json`
(key `interface`, 28 frozen cases). Phrases are quoted verbatim from the retained visible
text (`.ufo/waves/round-34/sources/S0xx.txt`, one line per file; offsets are byte offsets)
or from the interface text. Counts are dated measurements (r16 rule, `SKILL.md:201`).

| Situation | What to check / action | Evidence command (round-34 result) | Grounding phrase |
|---|---|---|---|
| A page change could alter how a shared URL previews | Run the offline audit before and after the change; manifest is version 1, each page has `file` relative to the manifest directory and an absolute `url`; no network is involved | `python3 -B scripts/link_preview_audit.py --manifest <dir>/manifest.json` (`invocation`, c1-matrix.json) | interface: `manifest v1: {version:1, pages:[{file: relative path inside the manifest directory, url: absolute http(s) page URL}]}` |
| Someone wants to claim the tool meets its whole contract | Run the frozen counter at the landed commit; it reads the tool from `git show <rev>:scripts/link_preview_audit.py`, never the working tree, and four constant gates must each fail a case | `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root <repo> --revision <commit>` (at `d08d8de`: 0/28, `toolPresent:false`, `byKind` 0/6 control, 0/13 defect, 0/7 input, 0/2 usage; `constantGatesAllRejected:true`; `verification/c1-at-d08d8de.json`) | counter docstring: `each must fail at least one case, so a counter that a constant could satisfy is reported as broken` |
| Exit 1, `og_required_missing`, `property` names one of the four | Add that one property to the page source; `name=` does not count, and content that is only ASCII whitespace counts as empty | re-run the audit; the finding clears only for the named property (D1–D6, D7 exit 1 `og_required_missing og:image`; K6 exit 0) | S067.txt@955 `The four required properties for every page are:`; interface `name= attributes do not count` |
| A page carries the other three but no `og:image` | Treat it as the census's dominant defect, not a per-page accident: 101 of the retained 102 ds4cc pages lack a non-empty `og:image` property, and only 1 has all four | census line, not the tool; see the census rows below | S067.txt@955 (same four-property sentence); S068.txt@6801 `Images are cached based on the URL and won’t be updated unless the URL changes` |
| Exit 1, `og_type_multiple` | Keep exactly one `og:type`; repeated `og:image` is not a finding, so do not generalise the check to every property | re-run the audit (D10 `og_type_multiple og:type`; K2 repeated `og:image` exit 0 clean) | S068.txt@3896 `Each URL should be a single object, so multiple og:type values are not possible.` |
| Exit 1, `og_url_not_absolute` | Rewrite `og:url` as an absolute `http`/`https` URL with a host; a relative value never passes | re-run the audit (D9 `og_url_not_absolute og:url`) | interface `og_url_not_absolute (og:url value is not an absolute http or https URL with a host)`; S067.txt@1303 `og:url - The canonical URL of your object that will be used as its permanent ID` |
| Exit 1, `og_url_not_canonical` | Compare `og:url` with the first `<link rel=canonical href>`, resolved against the page `url`; exact string match after stripping ASCII whitespace, so a scheme-only difference still fails, while a relative canonical that resolves equal passes | re-run the audit (D8 and D12 fail; K3 relative canonical resolved equal exit 0; K4 no canonical link exit 0) | interface `first canonical link wins; exact string comparison after stripping ASCII whitespace`; S068.txt@2626 `og:url The canonical URL for your page. This should be the undecorated URL` |
| Exit 2, `could-not-evaluate` | Fix the input, never the page: `input_invalid` (bad JSON, version other than 1, empty pages, non-http page url, `file` escaping the manifest directory) or `page_unreadable` (not UTF-8). Exit 2 reports input findings only | re-run the audit (I1–I7: 6 `input_invalid`, 1 `page_unreadable`) | interface `exit 2 verdict could-not-evaluate (any input finding; then only input findings are reported, reasons input_invalid or page_unreadable)` |
| Exit 64 | Fix the argv (missing `--manifest`, unknown argument); no JSON is produced, so nothing is known about any page | re-run the audit (U1, U2) | interface `exit 64 usage (missing --manifest, unknown argument)` |
| Reading the census line | Read `ds4cc-7fc6aa2f-og-census: pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87` as a recount of retained HTML at `7fc6aa2f`; `og:X` counts pages with a `<meta property="og:X">` whose stripped content is non-empty; the canonical side is resolved against `https://ds4cc.com/<path>` with a trailing `index.html` removed, which is the census's own base, not the manifest's page URL | `python3 -B .ufo/waves/round-34/c2_source_census.py --root <repo> --revision <commit>` (met 0/5 at `d08d8de`, census block still derived: `verification/c2-at-d08d8de.json` `census.derived`) | c2_source_census.py docstring condition (e): `og:X = pages with a <meta property="og:X"> whose content is non-empty after stripping ASCII whitespace` |
| Quoting those numbers as a preview verdict | Do not: the census says what the retained bytes contain, not what any crawler fetches or renders, and it covers only the four properties, only `.html`, only that commit | restate the commit and the dated-measurement status beside the number | S069.txt@685 `we are looking for oEmbed and Twitter Card / Open Graph tags`; S070.txt@3020 `Represents a rich preview card that is generated using OpenGraph tags from a URL` |
| A card looked wrong live, or a fixed page still previews the old title/image | Prepare the source change and the exact URL, then ask the operator: a re-scrape is a live request to an owned property, and image caches key on the image URL, not the page | operator action (Sharing Debugger); do not fire from a seat | S068.txt@4546 `The debugger also triggers a scrape of your page`; S069.txt@974 `Responses to these requests are cached globally across the service for around 30 minutes` |
| Someone wants to widen the source set to X or GitHub card docs | Do not: S071 is a generic developer-docs index with no card markup URL, and S072 documents a repository Settings image upload, not page-level Open Graph tags. Keep S067–S070 | read the retained text, not the intended target | S071.txt@0 `X Developer Platform - X Documentation Index`; S072.txt@0 `Customizing your repository's social media preview` |

## Per-row grounding, condensed

1 manifest v1 — interface; 2 constant gates — counter docstring; 3 four required/name= —
S067@955 + interface; 4 og:image floor — S067@955 + S068@6801 (101/102 arithmetically from
census `og:image=1` of `pages=102`); 5 single object — S068@3896; 6 absolute — interface +
S067@1303; 7 canonical compare — interface + S068@2626; 8 exit 2 — interface; 9 exit 64 —

Round-34 additions after wave 1: the committed selftest `python3 -B scripts/link_preview_selftest.py` (29 fixtures under `scripts/fixtures/link-preview/`, none copied from the matrix) runs the tool at `scripts/link_preview_audit.py` or `--tool <path>`; a 28/28 counter score alone does not show a working audit (a lookup-table tool also scores it, `corpus/lessons/round-34.md` mistake row 4), so read the tool and run the selftest. Discord reads `name=` before `property` (S073), so the tool's property-only rule is stricter than that consumer.

Round-34 wave-2 corrections to the table above: the four S068 byte offsets
are stale; the phrases sit at 6821, 3906, 2634 and 4558 (wave-2
`ReviewSkillTable34`). The selftest has 35 fixtures at `76fac3b`. The tool
now counts `og:image:url` as `og:image` and keeps the first of duplicated
attributes; for `bloat.html` and `exa.html`, fix the canonical-versus-sitemap
split before adding `og:url` (`corpus/knowledge/link-preview-metadata.md`,
wave-2 corrections).


### Link-preview audit gate registry — round 35

Offline static Open Graph link-preview policy over a version-1 JSON manifest of local HTML
pages: `scripts/link_preview_audit.py`. The round-35 contract (SCORECARD "Round 35 — declared
claims", C1 contract bullets a–c) landed at `b1cbbc39`. This row closes round-34 closure routed
defect 3. `.ufo/waves/round-35/criteria/registry_row_check.py` flags the missing row at
`318561ef` and passes once it exists.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| link-preview-audit | gate (offline static Open Graph link-preview policy; no network) | `python3 -B scripts/link_preview_audit.py --manifest <dir>/manifest.json` | `0=clean`; `1=failed-policy` (`og_required_missing`, `og_type_multiple`, `og_url_not_absolute`, `og_url_not_canonical`, and `og_url_multiple` from round 35); `2=could-not-evaluate` (`input_invalid` manifest-level, `page_unreadable` per page); `64=usage` (message on stderr, no JSON on stdout) | `python3 -B scripts/link_preview_selftest.py` (`--tool`, `--fixtures`) over `scripts/fixtures/link-preview/` (45 fixture directories at `b1cbbc39`, `MIN_FIXTURES` 20), comparing each case's exit, verdict and finding (reason, property) tuples; exit `0` all pass, `1` a case fails, `2` could-not-evaluate (tool or fixture root absent, fewer than 20 fixtures) | frozen round-34 matrix `.ufo/waves/round-34/c1-matrix.json` sha256 `246a6a3ba67a842c408f56b0240d2ad36969330c5a414b715f04b7e56fac14f7`, counted by `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision <commit>`; receipt `.ufo/waves/round-34/verification/c1-at-76fac3b.json` (28/28, four constant gates rejected); selftest receipt `.ufo/waves/round-34/verification/selftest-link-preview-at-76fac3b.txt`; round-35 sealed cases `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision <commit> --key-revision <reveal commit>` (target `passed` ≥ 22 of 24; reveal commit `4c6be2bd`; at `b1cbbc39` 24 of 24, receipt `.ufo/waves/round-35/verification/c1-at-b1cbbc39.json`), pre-build control receipts `.ufo/waves/round-35/verification/control-c1-*.json` | none: reads the manifest and the pages it names, never opens a network connection, never writes to disk, and `PYTHONDONTWRITEBYTECODE=1` in the self-test runner's tool environment | kake |

Correction to the "Exit 2, `could-not-evaluate`" row above (appended in round 35; that row
stays as landed). From `b1cbbc39` on, exit 2 with `page_unreadable` no longer means input
findings only. The readable pages are still audited, and their policy findings are listed beside
the input findings. `pagesChecked` counts the readable pages. A manifest-level `input_invalid`
still reports that finding alone and audits nothing. Two more round-35 rules: `og_url_multiple`
(exit 1) when a page has more than one non-empty `og:url`, and metadata inside an open
`<template>`, `<svg>` or `<math>` element is ignored. The round-34 fixture
`input_policy_suppressed_on_input` keeps its name but now expects the readable page's findings.

### Source re-check audit gate registry — round 36

Offline re-check of a `SOURCES.md` row's Gate quote against a recorded fetch of its source:
`scripts/source_recheck.py` (round-36 C1, built at `4d5b3d55` by wave-1 `ExecToolBuild`). The
contract is SCORECARD "Round 36 — declared claims", bullets (a)–(g). A `clean` report means the
recorded quote occurs in the recorded text under the contract's rules (NFKC, every whitespace
character deleted, case-sensitive); it does not mean the quote is complete or reader-visible.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| source-recheck-audit | gate (offline source-quote re-check against recorded fetches; no network) | `python3 -B scripts/source_recheck.py --manifest PATH` | `0=clean`; `1=failed-policy` (`gone`, `http_error`, `moved`, `quote_missing`, `unsupported_type`); `2=could-not-evaluate` (`input_invalid`, `check_invalid`, `charset_unsupported`); `64=usage` | `python3 -B scripts/source_recheck_selftest.py` (106 fixtures) | `python3 -B .ufo/waves/round-36/sealed_count.py --root . --revision <rev> --key-revision fd1fb723`; predicate `met: passed >= 25 of 28 sealed cases` | none (reads the manifest and its named body files) | kake |
| source-snapshot | probe (live GET recorder; network) | `python3 -B scripts/source_snapshot.py --input IN.json --out-dir DIR --manifest DIR/manifest.json` | writes a version-1 manifest plus bodies; skipped checks go to its receipts file | offline local-server test in `.ufo/waves/round-36/w1/ExecSnapshotFetcher.md` | none | `--out-dir` only | kake |

Procedure:
1. Build `IN.json` (`id`, `url`, `quote`) from the lesson Gate lines; never include an
   operator-owned host (`corpus/knowledge/freshness-pins.json`).
2. Record with `source_snapshot.py`, then run `source_recheck.py --manifest` on the result.
3. `moved`: verify the destination and record the new URL by an appended correction or a
   superseding row; never edit the source cell in place.
4. `gone`: flip the row's status in the next round's Gate and log old→new.
5. `quote_missing`: re-open the source by hand before any change; the quote may have moved
   inside the page.
6. Exit 2 or 64 is never clean: fix the input and run again.

### Robots.txt expectation audit gate registry — round 37

Offline check that the robots.txt a publisher will serve allows or disallows the URLs it intends:
`scripts/robots_audit.py` (round-37 C1, built at `9dbc88bb` by wave-1 `ExecRobotsTool`; wildcard
matcher made linear after measurement at `b99b6679`). The contract is SCORECARD "Round 37 —
declared claims" (RFC 9309, S011, with lane readings marked in
`corpus/knowledge/robots-txt-rules.md`). A `clean` report means every check's decision under the
contract equals its declared expectation; it says nothing about a fetch, a redirect, a cache or
what any particular crawler does.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| robots-expectation-audit | gate (offline; no network) | `python3 -B scripts/robots_audit.py --manifest PATH` | `0=clean`; `1=failed-policy` (`blocked`, `exposed`); `2=could-not-evaluate` (`input_invalid`, `check_invalid`); `64=usage` | `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` (204 fixtures) | `python3 -B .ufo/waves/round-37/sealed_count.py --root . --revision <rev> --key-revision 424aa248`; predicate `met: passed >= 25 of 28 sealed cases` (does not separate the contract from the stock Python parser; the selftest does) | none (reads the manifest and its named robots files) | kake |

Procedure:
1. Record the served `/robots.txt` (status and body) of the host; for an operator-owned host only
   with an operator-authorized read (`.ufo/waves/round-37/realrun/fetch_robots.py` shows the shape).
2. Write one check per (product token, URL, intended decision); quote the robots line that should
   decide it, and say so when the decision is "no rule matches".
3. `blocked`: the publisher's file disallows a URL it wants crawled; `exposed`: it allows a URL it
   wants kept out — fix the file, never the expectation, unless the intent changed.
4. 3xx statuses are check faults: record the final status after redirects yourself.
5. Exit 2 or 64 is never clean: fix the input and run again.

### Robots.txt expectation audit — round-38 amendment to the gate registry row

The `robots-expectation-audit` row above holds, with three amendments. Contract: SCORECARD
"Round 37 — declared claims" plus "Round 38 — declared claims" (h), (i), (k), with the C2
clarifications. Tool: `scripts/robots_audit.py` at `3ed8e15c` (sha256 `f4d057c4…baace`). Selftest:
`scripts/robots_audit_selftest.py`, 194 fixtures. Frozen proof: `.ufo/waves/round-38/sealed_count_v3.py`
(key `99357694`), 20 of 20, plus the round-37 counter 28 of 28 run in `--tool-file` mode. Revision mode
refuses any revision that holds a revealed key. Round-37 C1 was not admitted; the 28-of-28 control
that met it was the stdlib parser plus six patches (`CtlC1Shortcut-followup`), not the stock
parser (20 of 28).

The robots selftest now has 204 fixtures (round 39, routed defect 3): ten fixtures for the round-38
declared sentences and the six MutBuildTool survivors; the tool bytes are unchanged (`f4d057c4…`).

### Sitemap file audit — round 39 (exploratory capability)

Use it before publishing a sitemap or sitemap index, or when a crawl report says a sitemap was
rejected. Contract: `.ufo/waves/round-39/c1-contract.md` (sentences 1–34, rules (a)–(k); sources
S102–S108, lane readings marked). Tool `scripts/sitemap_audit.py` at `565ef4c9` (sha256
`6d86c8ce…a240ec`).

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| sitemap-file-audit | gate (offline; no network) | `python3 -B scripts/sitemap_audit.py --manifest PATH` (manifest v1: checks of `id`, `file`, `sitemapUrl`) | `0=clean`; `1=failed-policy` (findings such as `loc_out_of_scope`, `lastmod_invalid`, `too_large`); `2=could-not-evaluate` (`input_invalid`, `check_invalid`, `file_unreadable`); `64=usage` | `python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` (235 fixtures, all 34 sentences) | none admitted: the sealed 24-case counter (`.ufo/waves/round-39/sealed_count.py`, key `aa73d919`) does not separate the contract from a regex reader or from 15 single-sentence mutants; use the selftest | none (reads the manifest and the files it names) | kake |

Procedure:
1. Put the sitemap's served URL in `sitemapUrl` (scope is judged against its directory, sentence 25;
   an index only needs the same scheme, host and port, sentence 27).
2. Run it on the uncompressed file (gzip is out of scope). `loc_out_of_scope` most often means
   `http` versus `https` or another host (round-39 real run: fsf.org 212, nodejs.org 8).
3. A clean report is a protocol check, not an engine's acceptance: Yandex splits the 2,048-character
   `loc` limit (S109) and engines may ignore optional tags (S102).

### Sitemap file audit — round-40 repairs (amendment to the row above)

Tool `scripts/sitemap_audit.py` sha256 `03a8fba4…7b22b` (round 40). Three repairs, each red on the
round-39 bytes and green now in the selftest (now 179 fixtures, `r40_*`): UTF-16 without a BOM gives
`xml_malformed` (it decodes as UTF-8 but carries U+0000, not an XML Char, S110); a `loc` or
`sitemapUrl` with TAB, CR or LF anywhere, or a `sitemapUrl` starting with a C0 control or space, is
judged as written, not as `urlsplit` cleans it (S111): `loc_not_absolute` / `check_invalid`; a check
repeating the string `id` of an earlier invalid check is `check_invalid` (sentence 4). Decided by
source, not changed: `version="1.1"` with 1.0 content stays clean (S110 §2.8; guard
`.ufo/waves/round-40/criteria/d1_check.py`), and `doctype_present` still wins over a malformed
remainder (sentence 9 reading). Proof status: exploratory — the round-40 30-witness counter was met by
27 controls before the build (SCORECARD "Round 40 — kill rule (1) fired"); use the selftest, not the
counter.

Round-40 revision after the residual attack (`CriticBetterClaim`): tool sha256 `4de35f8c…1460e`. The
UTF-16 check now runs after the declared-encoding and DOCTYPE checks (a non-UTF-8 declaration still
gives `encoding_invalid`, a DOCTYPE still gives `doctype_present`, as before round 40), and element values
leave out elements of other namespaces with their text (sentence 14), so a TAB inside an ignored
extension element no longer makes a `loc` invalid. Selftest 183 fixtures.

### Sitemap file audit — round-41 URL rule (amendment to the rows above)

Tool `scripts/sitemap_audit.py` sha256 `50287ac6…1dde7d` (round 41; revised after wave 2 so TAB, LF or CR
inside an IP literal stays invalid). A `loc` (after sentence 21's strip)
or a manifest `sitemapUrl` is first judged as written against RFC 3986 `URI` with an authority and a
non-empty host (S117, Appendix A; S102 "follow the RFC-3986 standard for URIs"); only then does `urlsplit`
split it for the scope rule. So a space, `"<>\^`{|}`, DEL, a C0 control (in `sitemapUrl`; in a `loc`
the XML parser already gives `xml_malformed` for C0 other than TAB, LF, CR), a `[` or `]` in the path,
query or fragment, a second `#`, an `@` inside userinfo, or a `%` not followed by two hex digits gives
`loc_not_absolute` / `check_invalid`, where the round-40 tool accepted them (selftest `r41_*`, 225
fixtures). Unchanged on purpose, and not claimed as conformance: code points U+0080 and above are still
accepted wherever RFC 3986 allows `unreserved` (broader than RFC 3987 `ucschar`); ports above 65535 are
still judged by `urlsplit` (it rejects them, RFC 3986 does not), and so is an IP literal's shape — but
characters outside the RFC 3986 IP-literal repertoire plus `%` (TAB, LF, CR, non-ASCII, `|` in a zone id)
are now rejected inside the brackets, where the round-40 tool accepted some of them.
Proof status: exploratory — the round-41 oracle counter (`.ufo/waves/round-41/c1_count.py`, labels from
abnf 2.9.1's RFC 3986 grammar, S118) was met by 15 of 141 wave-1 controls before the build (SCORECARD
"Round 41 — kill rule (1) fired"); use the selftest, and treat the counter as information.

### Sitemap file audit — round-42 scanner (amendment to the rows above)

Tool sha256 `914ebdee…cd021` (build `020bc457`): the round-41 URL rule is unchanged in what it judges, but it
is matched by a byte-table scanner instead of one regular expression whose `\u0080-\U0010ffff` class made
long values slow (round 41: ×4–10 the round-40 CPU on long adversarial values). The zone-id behaviour is
declared, not accidental: RFC 9844 (S124) obsoletes RFC 6874's zone-id URI syntax, so rejecting a non-ASCII
character or `|` inside `[ ]` rejects only values RFC 3986 does not allow; `%25eth0` and `%eth0` stay
accepted (legacy laxity). Python 3.10 still runs it (selftest 235 fixtures, ten `r42_*` guards).
Measured by `.ufo/waves/round-42/c42_count_v3.py` (no `--seed`): output equal to the round-41 tool on ten
generated runs and CPU ≤ 2.0× the round-40 tool on five timing shapes (SCORECARD round 42).

### Round 47 gate registry additions (r46 closure routed defect R1)

Neither round-46 tool carried a registry row at landing; this section closes
that defect. Receipts for both rows' selftests are committed under
`.ufo/waves/round-47/verification/` (routed defect R2); the completeness
counter is `.ufo/waves/round-47/c47_registry_count.py` (2/2 rows, 2/2
receipts at the round-47 tip).

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| redirect-expectation-audit | gate (offline; no network) | `python3 -B scripts/redirect_audit.py --manifest PATH` (manifest v1: `rules`, `resources`, `checks`; `resourcePrecedence` and `defaultStatus` host fields) | `0=clean`; `1=failed-policy` (a check's decided outcome differs from its expectation); `2=could-not-evaluate` (input); `64=usage` | `python3 -B scripts/redirect_audit.py --selftest` (23/23; receipt `.ufo/waves/round-47/verification/selftest-redirect-audit.txt` names tool path + sha256 + tally) | `python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision <rev> --stage before\|after` — 11/11 witnesses caught, 0 clean false positives, 3/3 controls rejected, wall <120 s; contract `corpus/knowledge/redirect-rewrite-rules.md` (S050, S135) | reads the manifest; writes only an optional `--json` report path | kake |
| commit-citation-lint | gate (offline; no network) | `python3 -B scripts/citation_lint.py --root . [--revision REV] [--adjudications PATH]` (frozen population {SCORECARD.md, LOG.md}) | `0=clean` (no unadjudicated violation); `1=violations found` (file, line, token); `2=could-not-evaluate` (population unreadable); `64=usage` | `python3 -B scripts/citation_lint.py --selftest` (9/9; receipt `.ufo/waves/round-47/verification/selftest-citation-lint.txt` names the round-47 tool sha256 `3c78a0a8…` and its then-tally 8/8; the current selftest prints 9/9) | base `7cdbaefd…`: exit 1, 28 violations (17 unique tokens); tip `ee43e66…`: exit 0, 30 adjudicated occurrences — receipts `.ufo/waves/round-46/verification/c2-{before,after}-*.json`; adjudication ledger `corpus/quality/citation-adjudications.md` | reads population + ledger; writes only an optional `--json` report path | kake |

### Round-46 residual scope note (advisory; round 47)

The round-46 `c46_matrix.py` figures above are observed fixture outcomes, not a semantic certificate or evidence of an independent publisher-intent oracle. The orchestrator-dispatched R46 residual reports found that fixtures mirror `redirect_audit.py::_witnesses()`, W12 expects unsupported redirect status 200, a basename matcher/doctored-index control can pass, and three decision-logic mutants survive the matrix and tool selftest. Read the pinned 11/11 and 3/3 values as bounded counts only; R47's C1 claim is registry/receipt delivery, not a claim that these semantic-oracle gaps are closed. Durable summary: `corpus/lessons/round-47.md` §Inherited R46 residual scope.


### Round 52 gate registry additions (r51 closure routed defect 1)

Round 51 shipped two counters with no registry row, no self-test and no frozen baseline, so
PROTOCOL §Gate graded them non-conformant as gates and their junk controls named revisions the
repo does not contain (r51-4). This section registers both instruments at the registry home and
replaces the junk controls with a replayable mutation ladder. Receipts: `.ufo/waves/round-52/control/`.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| wave-evidence-ledger | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --root . --revision <commit>` | `0=met` (`ledger_checks_passed == 3 of 3`); `1=not met` (any L1/L2/L3 sub-condition fails, including absent evidence); `2=could-not-evaluate` (malformed JSON, unparsable numbers, exception); `64=usage` | `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` (19 fixtures, sandbox repos; receipt `.ufo/waves/round-52/control/c1-ledger-selftest.txt`) | `.ufo/waves/round-52/baselines.json` pins the counter sha256 and the nine round-51 input blob sha256s; `python3 -B .ufo/waves/round-52/c52_mutation_ladder.py` is the red-before ladder (13 of 18 families rejected by this counter and accepted by `c51_wave_ledger.py`; receipt `control/c1-mutation-ladder.json`) | read-only `git show`/`git ls-tree`; selftest writes only sandbox fixture repos under `.ufo/waves/round-52/selftest/` and removes them | kake |
| quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-52/c52_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1–C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, exception); `64=usage` | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` (18 fixtures, sandbox repos; the leading pin fixes the fixture revision — without it the fixtures rebuild from `HEAD` and the pass case fails; receipt `.ufo/waves/round-52/control/c2-quote-selftest.txt`) | `.ufo/waves/round-52/baselines.json` pins the counter sha256, the three retained-body sha256s, the mirror-pin sha256 and both receipt digests; C8 reads the mirror BYTES (`show(root, rev, MIRROR)`) and requires append-only equality with the measured registry minus the adopted rows | read-only `git show`/`git ls-tree`/`git log`; selftest writes only sandbox fixture repos under `.ufo/waves/round-52/selftest/` and removes them | kake |

The completeness counter is `.ufo/waves/round-52/c52_gate_registry.py`
(`python3 -B … --root . --revision <commit>`): it requires both rows to carry all eight cells
with the counter path named, both `--selftest` modes to be present, both committed selftest
receipts to hash to their pinned digests and to report exit 0, and both counter scripts to hash
to their pinned baselines. Withdrawal rule: the row goes when the counter leaves the tree.

### Round 55 gate registry additions

Round 55 ships two counters whose predicates are frozen in `.ufo/waves/round-55/contract.json`
before any data, each attacked by a critic and a mutation-tester before it scored (version 2,
committed before any build was measured; version-1 receipts stay as history). Both are offline
and read committed bytes only. Receipts: `.ufo/waves/round-55/controls/`.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| readme-index-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <commit>` | `0=met` (`index_mismatches == 0 AND knowledge_files >= 46`); `1=not met` (any unindexed, multi, thin, duplicate, head_changed, deleted or dangling item, or fewer than 46 knowledge files); `2=could-not-evaluate` (tree or `corpus/README.md` unreadable, no or more than one `## Coverage map` section, no table); usage errors also exit 2 (`ap.error`) | `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` (44 fixtures, generated sandbox repos; receipt `.ufo/waves/round-55/controls/c1-selftest-v2.txt`) | `contract.json` `claims.C1.predicate`; base control `.ufo/waves/round-55/controls/base-c1-readme-index-v2.txt` (`index_mismatches=21`, exit 1 at `fcaf4b85`); version-1 control kept as history | none (reads `git show` / `git ls-tree` only; selftest writes only `mktemp -d` sandboxes) | kake |
| yahoo-robots-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1–C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, an exception); usage errors also exit 2 (`ap.error`) | `KAKE_R55_SELFTEST_REV=64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6 python3 -B .ufo/waves/round-55/c55_quote_truth.py --selftest` (54 sandbox-repo fixtures built from the committed round-55 evidence at the pinned revision, including 3 unit-rule checks; receipt `.ufo/waves/round-55/controls/c2-selftest.txt`) | `contract.json` `claims.C2`; base control `.ufo/waves/round-55/controls/base-c2-quote-truth-v2.txt` (`0/8`, exit 1); retained-body receipts `.ufo/waves/round-55/sources/receipts.json`; pre-append mirror pin `.ufo/waves/round-55/assimilation/mirror-pin.json` | none (reads `git show` / `git log` only; selftest writes only `mktemp -d` sandboxes) | kake |

C7 is a receipt check: it certifies that the committed census receipt, the validated scratch registry
and the landed registry agree, not that the census ran. `.ufo/waves/round-55/validate_append.sh`
regenerates the receipts and must be re-run after any edit to `corpus/SOURCES.md` or the three
adopted entries. No round-55 gate-completeness counter exists (round 52 shipped
`c52_gate_registry.py` for its own two rows); the eight-cell schema of these rows is checked by
reading, not by code. Withdrawal rule: a row goes when its counter leaves the tree.

### Round 56 gate registry additions

Round 56 ships two counters whose predicates are frozen in `.ufo/waves/round-56/contract.json` before any data (version 2 of
each, after the wave-1 attacks; version-1 receipts stay as history); both are offline and read committed bytes only. C1 calibrates
the ten self-test tallies in the registry above (the round-55 routed defect) and C2 is the freshness claim for three Yahoo! JAPAN
crawl-handling entries. Receipts: `.ufo/waves/round-56/controls/`. `scripts/landed_check.py` is a tool, not a gate: it compares the commit
hashes a report cites with branch ancestry (considerthese proposal 1).

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| selftest-tally-counter | gate (offline, committed bytes only; runs the ten documented selftests in a clone of the revision) | `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision <commit>` | `0=met` (`tally_mismatches == 0 AND rows_checked == 10`); `1=not met` (any row_missing, duplicate_row, command_missing, command_invalid, command_ambiguous, claim_missing, claim_ambiguous, tool_changed, selftest_failed, claim_ne_observed or command_unrunnable); `2=could-not-evaluate` (revision unresolved, clone failure, unparsable tally, timeout); `64=usage` (an argparse error exits 2) | `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` (59 checks, generated sandbox repos) | `contract.json` `claims.C1`; base control `.ufo/waves/round-56/controls/base-c1-selftally-v2.txt` (`tally_mismatches=7 rows_checked=10`, exit 1 at `e48354b7c26b`); population is ten named rows (link-preview-audit excluded: its row counts fixture directories, not cases) | none (clones the revision under `mktemp -d`) | kake |
| yahoo-crawl-handling-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1-C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, an exception); usage errors also exit 2 (`ap.error`) | `KAKE_R56_SELFTEST_REV=f8438a282d5946b386812d784cc617edcbc9201d python3 -B .ufo/waves/round-56/c56_quote_truth.py --selftest` (86 checks: 83 sandbox-repo fixtures built from the committed round-56 evidence at the pinned revision, plus 3 unit-rule checks) | `contract.json` `claims.C2`; base control `.ufo/waves/round-56/controls/base-c2-quote-truth.txt` (`0/8`, exit 1); retained bodies `.ufo/waves/round-56/sources/` with `receipts.json`; held-row body pin `HELD_BODY_SHA256` (S367); pre-append mirror pin `.ufo/waves/round-56/assimilation/mirror-pin.json` | none (reads `git show` / `git log` only; selftest writes only `mktemp -d` sandboxes) | kake |

The C1 counter runs each row's documented self-test command from the row's `Self-test` cell (a leading `KAKE_R5N_SELFTEST_REV=<hex>`
word is part of the command; the environment is otherwise fixed) in a `git clone` of the measured revision and compares the claim in that
cell with the printed tally. A rewritten selftest is a different claim: the pinned script and every `*.py` beside it must be byte-equal
to their blobs at `e48354b7c26b`. Round 56 rewrote the seven Self-test cells whose claim disagreed with the printed tally and left the three
that agreed. C7 of the C2 counter is a receipt check: `.ufo/waves/round-56/validate_append.sh` regenerates the receipts and must be re-run
after any edit to `corpus/SOURCES.md` or the three adopted entries. Withdrawal rule: a row goes when its counter leaves the tree.

### Round 57 gate registry additions

Round 57 ships three counters whose predicates are frozen in `.ufo/waves/round-57/contract.json` before any data (version 2 of each, after the
wave-1 attacks; version-1 receipts stay as history); all three are offline and read committed bytes (C2 also reads the sibling lanes' registries at
their `HEAD`). C1 calibrates the revision pins of the measurement receipts (the round-56 routed defect), C2 gates the new tool `scripts/id_resolver.py`
(considerthese proposal 2), C3 is the freshness claim for two Baidu dead-link entries. Receipts: `.ufo/waves/round-57/controls/`; a receipt that carries
a `revision:` line is never rewritten, a re-run lands under a new name.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| receipt-pin-counter | gate (offline, committed bytes only; whole-ancestry history walk) | `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision <tip>` | `0=met` (`undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1`); `1=not met`; `2=could-not-evaluate` (revision unresolved, malformed `receipt-errata.json` or `measured.json`, git failure); `64=usage` | `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --selftest` (71 checks, generated sandbox repos including merges, renames, a branched receipt and the CLI exit codes) | `contract.json` `claims.C1`; base control `.ufo/waves/round-57/controls/base-c1-receipt-pins-v2.txt` (`undisclosed_relabels=6`, exit 1); `receipt-errata.json`; `measured.json` (lands with the C1 receipt: the measured revision and the commit the counters were frozen at) | none (read-only; its selftest builds `mktemp -d` repos) | kake |
| id-resolver-gate | gate (differential: a reference implementation inside the gate against the tool, over randomised fixtures and the real revisions; reads sibling registries) | `python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root . --revision <commit> [--fleet <fleet root>]` | `0=met` (`gate_conditions_passed == 5 of 5`); `1=not met` (G1 tool present, G2 selftest, G3 fixtures, G4 red-before at `3994101`, G5 green at the measured revision); `2=could-not-evaluate` (revision unresolved, no sibling registries, live sibling ownership differs from `sibling-snapshot.json`); `64=usage` | the gate has no selftest of its own; the tool it gates has `python3 -B scripts/id_resolver.py --selftest` (49 checks, generated sandbox lanes and siblings); measured on the shipped gate by `.ufo/waves/round-57/w2/ExecGateFlake.md`: the genuine tool 5/5 in ten of ten runs, a constant printer 2/5, a working-tree reader 4/5, and a green-only printer failing G3, G4 and G5 (`w2/ReviewerQualitySkill.md`) | `contract.json` `claims.C2`; base control `.ufo/waves/round-57/controls/base-c2-idresolver-v2.txt` (`0/5`, exit 1); `sibling-snapshot.json` | none (clones into `mktemp -d`) | kake |
| baidu-dead-link-quote-truth-counter | gate (offline, committed bytes only; no network) | `python3 -B .ufo/waves/round-57/c57_quote_truth.py --root . --revision <commit>` | `0=met` (`conditions_passed == 8 of 8`); `1=not met` (any C1-C8 sub-condition fails); `2=could-not-evaluate` (malformed receipt or mirror-pin JSON, an unreadable base revision, an exception); `64=usage` (a missing `--revision` or any argparse error) | `KAKE_R57_SELFTEST_REV=b9a5d012f7fd python3 -B .ufo/waves/round-57/c57_quote_truth.py --selftest` (120 checks: 105 sandbox-repo fixtures built from the retained round-57 bodies at the pinned revision, plus the unit-rule, kill-matrix, unreadable-base and usage-exit checks) | `contract.json` `claims.C3`; base control `.ufo/waves/round-57/controls/base-c3-quote-truth-v2.txt` (`0/8`, exit 1); retained bodies pinned by sha256 in the counter; `sources/receipts.json`; `assimilation/mirror-pin.json` | none (read-only; its selftest builds `mktemp -d` repos) | kake |
| source-id-resolver | tool (read-only; stdlib python) | `python3 -B scripts/id_resolver.py --root . [--revision REV] [--fleet FLEET]` (lists every `S###` id cited in `corpus/knowledge/**/*.md` that the lane registry lacks and names the sibling registries that hold it) | `0=no dangling id`; `1=dangling ids found` (one `DANGLING` line each, then `ids_cited=N ids_resolved=N dangling=N owned_elsewhere=N unowned=N`); `2=could-not-evaluate` (revision unresolved, registry absent, no knowledge file); `64=usage` | `python3 -B scripts/id_resolver.py --selftest` (49 checks) | red-before: at lane revision `3994101` it reports exactly S367 S372 S373 S390 S409, each held by kotodama-shokunin (`.ufo/waves/round-57/w1/ExecResolverGroundTruth.md`, gate condition G4) | none | kake |

The C1 counter reads receipt bodies: after-c2 and after-c3 must start with their counter's `met=True` report line; after-c1 carries `tip: <T0>` and the
line this counter re-derives for T0. It certifies that the pin matches what the receipt's history and body say, not that a counter ran; a relabel of a
round-57 receipt is never disclosable. Withdrawal rule: a row goes when its counter leaves the tree.
