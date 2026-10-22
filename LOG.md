# kake-shokunin — Iteration Log

- 2026-09-28 — round 0: minted as shonen.
- 2026-09-28 — round 1: rewrote SKILL.md as audit→source-fix→operator-gated-publish playbook. Evidence: `~/Projects/webzites/fleet/fleet.config.json` (20-row registry, expect tripwires), `fleet/fleet.dedupe-report.md` (2026-09-26 probe classifications + publish-queue), `fleet/kimi-surface-ops.md` (verified ops manual r1–r4: no non-GUI publish channel, chat→domain map, update/recreate/rebuild verbs), `~/Projects/ds4cc-marketplace/.github/workflows/pages.yml` + `deploy-github-pages.sh` (GHP publish = push to main), `~/Projects/plazir-15-site/.github/workflows/pages.yml`, `plazir-15-site/speedrun/` frozen copy vs `ds4cc-marketplace/speedrun/` canonical (`rel=canonical` in plazir copy), `ufofsdbeta` = runtime repo not a site source, `ufofsdbeta-kimi-review` = non-git snapshot. Publish remains operator-gated throughout.
- 2026-09-28 — round 3: closed the "stale-cited-evidence" gap. Ran `webzites probe --all` (18:51Z: 12 OK, 6 fail) + `kimi-surface.mjs sync-check`. Corrections landed: `lucario` — config claimed live/maintained, actually 404 never-published; canonical is `veigapunk.github.io/lucario/` (verified 200, source `~/Projects/lucario` Pages branch deploy). `charter-ghp` — marker `2026-09-26 scribe beat` stale vs live `2026-09-28` beat (PQ-12 churn confirmed <48h). Added trust-hierarchy rule (probe > config status) + marker re-pin procedure to SKILL.md; corpus entries updated. No deploys.
- 2026-09-28 — round 4: closed the "undecoded fire journals" gap. Extracted the full kimi-surface exit-code table from `~/Projects/webzites/scripts/kimi-surface.mjs` throw sites (codes 1–8, 64) and cross-read 15+ run journals in `~/Projects/webzites/state/` (update/recreate/rebuild, 09-26→09-27). Key facts landed in `corpus/knowledge/fire-journal-codes.md`: meter consumption is a journal fact (`fire` + `fired` step), not an exit-code fact; code 5 = clean pre-send abort (free retry), codes 6/7 post-`fired` = ANOMALY (operator inspects, never blind refire); successful recreate/rebuild terminates `liveAfter.stillDead:true` + claimed version card — live URL stays 404 until the human publish click. Evidence: rebuild-charter-fire.log (version `efc1830`, preview 200+marker, stillDead), plazir15 code-6 post-fire orphan risk, ds4cc-kimi-mirror code-7 post-fire anomaly. SKILL.md gained journal-reading note in the publish checklist + fired-but-orphaned pitfall. No fires, no deploys, no publishes.
- 2026-09-28 — round 5: closed the "ops-automation + Origin-repo layer invisible to corpus" gap. Three new knowledge files landed. `corpus/knowledge/ops-automation.md`: `webzites-probe.timer` (OnUnitActiveSec=6h, `SuccessExitStatus=1`) + `webzites-keeper.timer` (daily `grokbot tick`); `probe-history.jsonl` semantics + observed transitions (veigapunk-page left violated[] 09-21T04:14→09-22T22:58 = human publish click; charter-ghp entered violated[] 09-27T00:22→06:22 = marker churn not outage; lucario appeared violated at total 17→18 = registration event; xsnapshot-app constant errors[] = armed NXDOMAIN baseline); full `webzites.mjs --help` verb table incl. previously-undocumented `bots`/`grokbots`/`speedrun`/`install`/`auth`/`map`. `corpus/knowledge/origin-repos.md`: 50-clone `~/Projects/webzites/repos/` map from wz-repos r1–r8 (terminal round 2026-09-21) — byte-verified canonical writers (ds4cc.com=ds4cc-marketplace sha b6f65899; root=VeigaPunk.github.io sha 20805500; burnerchrome.kimi.page=repos/burnerchrome), name-trap receipts (ds4cc-website sitemap claims ds4cc.com but sha 70b2241e ≠ live; vendored burnerchrome dir ≠ standalone repo), 5 sourceless kimi artifacts (sdk-seed fingerprint, zero clone hits, stable r3→r8), fleet.config sourceDir drift noted. `corpus/knowledge/speedrun-pipeline.md`: the second publish surface — record→report→prep --write→operator push→X draft; fail-closed schema (18-key live-derived intersection), redaction denylist, no HTTP upload API, post only prints. SKILL.md: added instrumentation rule (check probe-latest.json age before re-probing), speedrun gated lane, cited-paths for systemd units/repos/state. README coverage map + gaps rewritten (two prior "gaps" were already answered on disk). No probes fired, no deploys, no metered ops — evidence mining only.
- 2026-09-28 — round 6: closed the "GHP subpath rot invisible" gap (README known-gap). First live baseline: 2 352 sourceDir paths across ds4cc-com / plazir15-ghp / charter-ghp, GET + sha256 vs source AND vs `origin/main` — **0 true rot**; 126 non-clean results all decomposed to git state (ds4cc 20 commits ahead: 120 diffs incl. live-404 `robots.txt`/`sitemap.xml`/`404.html`/`infinizoom/main.js` = unpushed additions; plazir15 5 ahead: 5 diffs; charter 2 behind: 1 diff, index 8.6KB vs live 50.9KB = `b74190e` static-index bake not pulled). Source read of `src/reconcile.mjs` proved it picks ONE scored `index.html` (depth ≤2) — SKILL.md now says "all other paths incl. second index.html" invisible, and flags `in-sync` on GHP as byte-drift masking (precedent: 09-21 keeper log, `git pull` → match). GHP dir-index semantics live-verified (`/dir` 301→`/dir/`→index.html; `.md` served raw). New `corpus/knowledge/ghp-subpath-spotcheck.md` (procedure + classification table + coverage limits); README coverage/gaps updated; `corpus/lessons/round-6.md`. Zero publishes, zero metered ops.

- 2026-09-28 — round 7: closed the "live-only orphan paths" gap (README residual). Evidence: `pages.yml` deploy-graph read (`upload-pages-artifact path: <root>` → GHP deploys are full-tree snapshots, so the served set ≡ `origin/main` tree and deleted-file orphans cannot exist), live sitemap sweep of 103 `<loc>`s across ds4cc-com (staged 93-loc sitemap as pre-push preview), plazir15-ghp (8), charter-ghp (2) → 0 orphans, 0 dead listings. `probe-latest.json` 18:51Z re-verified: charter-ghp marker FAIL for second consecutive probe (live literal `2026-09-28 scribe beat (`; pin still `2026-09-26` — queued for keeper, never self-edited); dead rows unchanged. Landed `corpus/knowledge/sitemap-orphan-audit.md`, SKILL.md drift-table row + ~daily beat-pin cadence, README coverage/gap updates. No deploys, no metered ops.

- 2026-09-28 — round 8: closed the "kimi subpaths" residual (README known-gap). First kimi per-path baseline: live-index link sweeps on all 10 live kimi rows (44 same-origin links, 0 real non-200) + canonical sitemap parity on ds4cc.kimi.page (93 locs → 19 served / 74 missing; `git log --diff-filter=A` classifies every miss as post-vintage — 63×09-23, 10×09-22, 1×09-08 vs publish ~Aug-29 — **0 rot, pure staleness**: PQ-2 delta quantified). Live-proofed the dir-index pitfall: mirror ships `omarchy-usage/`, `omegag/`, `speedrun/` hrefs that 404 on kimi while `*/index.html` serves 200 — permanent until republish-with-rewrite. New fact: `update` transfers index.html-only while `recreate`/`rebuild` zip the whole tree (`kimi-surface.mjs` :459-466 vs :903-908) — subpath richness depends on which verb last fired, and the orphaned 09-26 update fire (code 7) never touched live. Landed `corpus/knowledge/kimi-subpath-audit.md` + `corpus/lessons/round-8.md`, SKILL.md drift-table row + dir-index live proof, README coverage/gaps. Evidence: `/tmp/kimi_audit.py` + `/tmp/kimi-subpath-audit.json`, `state/kimi-map.json` bound-chat updateTimes, `fleet.config.json` rows. Zero publishes, zero metered/browser ops.
- 2026-09-28 — round 9: closed the "publish queue has no readiness ledger" + "JS-rendered surfaces need DOM" gaps (10 read-only L2 probes, zero fires/pushes). Landed `corpus/knowledge/publish-queue.md` (PQ-1..13 gate-class table: PQ-5 = shortest path — rebuild card `efc1830` already verified, needs only human Publish+slug; PQ-2 mirror delta corrected to **75** locs per sitemap commit `f3d2ecd`; bound-chat truth = `state/kimi-map.json` publishedUrl) and `corpus/knowledge/vault-properties.md` (vault PROPERTIES[] is a static literal — no browser needed; 3/10 live-claimed links dead: charter-ufo-fsd/plazir15 404-sentinel sha `93ddca9a`, plazir27.kimi.pro preview-404; lucario absent; extraction recipe for all `sourceDir:null` rows — `cmdUpdate` gate `kimi-surface.mjs:483`, `cmdRecreate` dead-slot gate `:845-849`, plazir27runson needs `--zip-exclude='assets/*.mp4'` vs 32MB `fetchLive` cap `:339`). New platform facts: +157B `sdk-seed.js` tag growth fleet-wide 09-26→09-28 (digests must normalize; bytes carry no freshness), website-id `1a0acf59` collision on ufo-fsd.kimi.pro+.page (2/18; config "1/17" note stale), `webzites` not on PATH (canonical `node ~/Projects/webzites/bin/webzites.mjs`), probe-history is bursty not 6h-regular (median 0.45h, 42.7h hole — ops-automation.md corrected). Keeper queue prepared not applied: charter-ghp pin diff (`fleet.config.json:256`, live `2026-09-28 scribe beat (`), plazir15 chat-binding ambiguity (vessel `1a0c2186` vs `1a0de2ed`). Evidence: `~/Projects/webzites/reports/{r9-publish-queue,r9-stale-markers,dead-slot-recreate-readiness-r9,sentinel-sourceless-extract-r9}.md`; self-verified GETs on vault + 3 dead slots.

- 2026-09-28 — round 10: closed the "alerting on `violated[]` deltas is undecided" gap (README known gap since r5) + first full checklist-executability audit — **operability axis-move, SCORECARD 6→8** (freshness stays 8, no double-count). 11 read-only L2 probes in one batch (planner/scout/executor×2/labrat/revenger/reviewer/critic/connector/sentinel/scribe → `/tmp/kake-r10/`); zero fires, zero pushes, zero browser ops; sentinel sha-verified webzites state unchanged. Landed `scripts/probe-delta.mjs` — runnable history-delta + coverage-hole detector over `state/probe-history.jsonl`: naive consecutive-row diff = **42 events, 40 phantom** (labrat-replicated; spot `total:1` rows vs fleet sweeps fabricate clear/re-enter pairs) → universe-rule diff = **6 events, 0 phantom**, all four r5 ground-truth records reproduced; critic falsifiers closed (exit-64 input validation, `total>1` universe guard, partial-sweep flag). **The detector falsified our own r5 record**: veigapunk-page's real transition is 09-21T03:32:06→04:14:50 (raw rows: 04:14:50 and 09-22T22:58:23 carry *identical* `violated[]` sets — r5 had used the 42.73h coverage hole's endpoints as the transition window); corrected in `ops-automation.md` (also xsnapshot "every run"→"every full sweep since 01:34:20Z"). Checklist audit: 33/33 SKILL.md commands + 60/60 cited paths resolve (scout); 5 verbs executed live (executor-a) → 2 undocumented CLI behaviors landed in SKILL.md (`webzites status` **exits 1 on any violation** `src/cli.mjs:99` — stdout-read, never a gate; `kimi-surface.mjs` has **no `--help`** — usage via unknown verb, exit 64, `:1197-1198`); citation drift fixed (executor-b RED/GREEN: `vault-properties.md` `:891-894`→`:903`; `round-9.md` `:339`→`:342`; SKILL.md cwd-relative kimi-surface invocations → absolute). Revenger recovered writer semantics from `src/fleet.mjs`/`src/probe.mjs`/`src/cli.mjs`: sole writer `saveProbe` `fleet.mjs:39-53`; `grokbot tick`/`bots task` write MERGED fleet-sized rows (stale-carried — detector caveat); deficit rows carry skipped sites; errors[] = catch-block failures ≠ violated[]; era families {1:10,14:4,15:1,17:54,18:7}. New `corpus/knowledge/probe-delta-alerting.md` (rules + baseline + caveats); SKILL.md step-1 wiring (read-only audit semantics per sentinel WARN: never re-run mutating verbs for audit), drift-table row, cited-paths entry; README gap closed; `lessons/round-10.md`; SCORECARD before→after. Honest limits (critic): detector has no consumer yet — detection + checklist wiring only; alert *delivery* (notify/systemd) stays operator/webzites-owner-gated.

- 2026-09-28 — round 11: closed the "3 of ~20 free-read verbs never live-run" residual (r10 audit) — **operability axis-move, SCORECARD 8→9** (freshness stays 8; probe-latest 2.6h fresh at round open, operability picked per plan). 13 read-only L2 probes in one batch (planner/scout/revenger/labrat×3/executor×2/critic/reviewer/connector/sentinel/scribe → `/tmp/kake-r11/`); zero fires, zero pushes, zero browser ops; the only webzites state delta = one sanctioned `total:1` history append + a backup-guarded clobber→byte-identical restore (sentinel-audited). Central finding: **`probe <id>` clobbers the 18-row fleet snapshot to 1 row** (live: 18→1 rows, `webzites status` exit 1→0 while clobbered, masking 5 violated + 1 error; `--quiet` doesn't prevent it — `cli.mjs:78` saves before the quiet gate) — **unintended defect, not spot semantics**: `mergeProbeResults` intent comment `fleet.mjs:27-29` ("must not erase every other site's verdict"), the r2-era fix covered `tick`/`bots task` (`cli.mjs:289`,`:647`) but left `cmdProbe:78` raw (webzites-side archaeology `/tmp/kake-r11/revenger-merge.md`; 11 `total:1` rows in history). Live exit contracts: probe subset-scoped exit 1, unknown-id exit 2 + HELP **no write** (`cli.mjs:1097-1101`); `status --json` always 0 (`:94-97`), plain status **snapshot-relative** (`:99`, critic-refuted unconditional wording); reconcile read-only, exit 1 only on drift/fetch-error/source-missing — `NOSRC`/`no-source-file` silent 0 (`:269-272`), unknown-id = crash exit 1 + stack (un-awaited `:1086`); sync-check stricter bad-set (`kimi-surface.mjs:206`), `--all`/`--dead` undocumented selectors (`:184-190`), stale ~Aug-29 mirror verdicts **in-sync exit 0** (vintage invisible), `liveSha256` nondeterministic per fetch (abf822c7→440e3cba→5a80ee93 — never alert on sha deltas). Landed: `corpus/knowledge/free-read-verbs.md` (4 verb cards + 3-universe model + state-persistence model + provenance table); SKILL.md step-1 spot-probe trap + backup/restore recipe, status-exit sharpening, write-path cite fix (`cli.mjs:998-1002` was the install unit template → real write path `:78`), 3 drift-table rows, cited-paths entry. Reviewer corrections applied (7 off-by-N fleet.mjs/cli pins, bin import :5, reconcile verdict fork `reconcile.mjs:171-173`); connector: no sibling overlap (kumitate has zero webzites-verb vocabulary; kagi CDP-lease contested-scope boundary respected). r12 planned: freshness re-probe + PQ/marker re-verification if probe-latest stale at open, else remaining free-reads live + webzites-owner handoff for the cmdProbe merge fix (patch proposal `/tmp/kake-r11/scout-verbs.md` F1 — kake never edits webzites source).

- 2026-09-28 — round 12: closed the "4 remaining free-read verbs replica-verified only" residual + falsified two automation myths — **operability axis-move, SCORECARD 9→10** (freshness stays 8; probe-latest 3.4h fresh at open → operability per r11 plan; next 6h sweep 00:00:59Z). 9 read-only L2 probes in one batch (scout/executor/scribe/critic/reviewer/connector/sentinel/revenger/labrat → `/tmp/kake-r12/`); zero fires, zero pushes, zero browser ops, zero systemctl mutations (sentinel PASS ×2 passes; 31-file state sha guard byte-identical before/after the 4 live verb runs — exits 0/1/0/1: `status --json` (18 rows, 5 violated+1 error, exit 0), `grokbots --check` (exit 1, `lucario: no registry row`, checked 21), `bots list` (exit 0, 20 keepers, cards 20/20, wrappers 17/20 — misses all queued), `bots report` (exit 1 gaps lucario; log=8d on 20/21, turn=never 17/21)). Central findings: (1) `webzites-keeper.timer` is loaded+DISABLED+inactive(dead), zero journal — **the daily keeper tick has never fired**; keeper logs frozen at 2026-09-21T03 mint round → r5 ops-automation + SKILL claims corrected (`corpus/knowledge/keeper-timer-inert.md`); enable-vs-retire filed to L0. (2) Critic refuted r7+r12-L1 "keeper re-pins charter-ghp marker": the writer is the ACTIVE 6h charter-scribe (beat commit `61d0ce6`), the probe FAIL is `fleet.config.json:256` pin lag, and **no webzites code writes fleet.config.json** (only reader `src/fleet.mjs:7-11`) → PQ-12 relabeled human/operator edit; new defect N1: scribe push-gate failing (3 beats since 06:05Z `pushed:false` `push_blocked: pull timed out after 60s` — ledger `~/Projects/origin-work/ufo-fsd-alpha/.ufo/charter-scribe/ledger.jsonl`). (3) Roster arithmetic pinned: fleet.config 21 / grokbots registry 20 / probe snapshot 18; 18-of-21 is by-design url filtering (`src/cli.mjs:75`), the wedge is lucario (fleet row 09-27, no registry row/card/wrapper/log — L0 mint-or-prune). (4) Revenger REFUTED the r11 F1 guard (`positionals.length>0 && !flags.all` still clobbers on `probe <id> --all` — `--all` is parsed but never read); corrected one-line merge patch replica-verified (subset probe keeps 18 rows, merged `total:18`, `node --check` clean) → filed as `corpus/handoffs/cmdProbe-merge-fix.md` (webzites source stays read-only per operator rule). (5) Labrat replica matrix: corrupt probe-latest crashes all status/bots-report forms exit 1 before the `--json` branch (`fleet.mjs:14-18`); deleted snapshot → `{"probe":null}` exit 0 / plain status exit 0 "no probe results yet"; empty registry = SyntaxError exit 1 (NOT UsageError; `cli.mjs:340`), missing/wrong-schema = UsageError exit 2; `--stale 24`/`--stale 1` indistinguishable on uniformly 8d logs. Quality gates: reviewer 22 OK / 2 WRONG / 1 wrong-as-worded (mergeProbeResults `fleet.mjs:30-37` not 39-51; turn=never 17/21 not 13/21; 20/21 logs not "all") — all folded; scribe caught the same count error pre-landing; critic re-ran the 4 verbs independently matching the guard. 3 L0 items live (keeper timer, lucario, cmdProbe patch routing). Landed: `corpus/knowledge/keeper-timer-inert.md`, free-read-verbs r12 append + F1 guard addendum, `corpus/handoffs/cmdProbe-merge-fix.md`, `corpus/lessons/round-12.md`, publish-queue PQ-12 relabel, SKILL.md r12 amendments (half-instrumented, lucario roster gap, second-registry paragraph, url-filter fact, drift-table rows, cited paths), corpus README coverage/gaps, ops-automation keeper-timer status + 77-row history note.

- 2026-09-28 — round 13: freshness re-verification round (probe-latest 3.9h
  fresh at open — the planned >6h-stale trigger never materialized; score
  stays 8, no falsifiable move existed per critic falsification). 10
  read-only L2 probes in one batch (scout + executor×4 + labrat + revenger
  + critic + reviewer + connector + sentinel → `/tmp/kake-r13/`); zero
  fires, zero pushes, zero systemctl mutations, zero webzites-state writes
  (sentinel 33-file sha guard baseline; the only git actions repaired the
  MISSING round-12 commits in both repos — kake head was round-11, main
  head round-6, connector corroborated kasegi hit the same gap). Findings:
  (1) pattern HELD — timer sweeps 06:00:46.703Z/12:00:53.973Z/18:01:09.822Z
  (r14 erratum: r13 wrote 06:00:36Z — that is the journal `Starting` line,
  the history `at` rows are :46.703/:53.973/:09.822) + off-cadence
  manual re-probe 18:51:26Z (r3 vintage, NOT the timer) all identical
  12-ok/5-violated/1-error; independent 18-curl live replication 22:50Z =
  0 verdict diffs. (2) PQ-5 still pending — live slot serves the
  byte-identical 13,409B 404 sentinel (sha `93ddca9a…` == 09-26 journals);
  zero fires fleet-wide since 09-26T15:34Z; `kimi-map` content is
  09-26-vintage (CDP :9222 down — `publishedUrl:null` is NOT same-day
  evidence); preview 8,387B (+64B vs journal, unexplained). (3) PQ-2
  unchanged — 19/93 served, 74 missing live-GET (75 by f3d2ecd accounting:
  5 pre-serve), 0 per-URL transitions, root content-frozen 74,641B (r14
  erratum: r13 said "byte-frozen" — raw sha varies per fetch via Cloudflare
  cfemail re-encoding, 1 occurrence; the valid freeze metric is the
  cfemail-normalized sha `4427b7f8…`, equal across r13+r14 fetches; max
  embedded date 08-21); `/speedrun/`+`/burnerchrome/` 404s are the
  dir-index pitfall (`index.html` serves 200), `/iqrunway/` dead on BOTH
  surfaces. (4) charter-ghp: pin-lag persists BUT live is deploy-current —
  the HUMAN pushed 5 commits 18:32:06–20:43:21Z (`b74190e` bake →
  `d69dd22` og-block → `0c767c2` window sync → `b9db4b1` CORRECTION →
  `a8f1e2b` fixup), Pages served each within ~30s (live sha `0decd827…`
  == `a8f1e2b`, 53,353B); "churn paused" rescoped to the scribe automation
  only; local clone lags 5 (`61d0ce6`). (5) r13 draft error caught by critic
  pre-landing: `observed:"absent"` = exact-pin `includes()` miss
  (`src/probe.mjs:55`), NOT the beat line vanishing — withdrawn, semantics
  rule landed in SKILL.md. (6) at-vs-mtime rule: probe-latest mtime
  21:31:45Z (r11 restore) vs `at` 18:51:26Z (2h40m apart) — freshness MUST
  read `at`; birth-time = clobber instant; sha proved the restored file ==
  r11 backup. (7) 4 stale citations fixed (PQ-3 behind 2→5, PQ-6
  `:189`→`:175`, PQ-5 zip 1→2 days, ops-automation 76→77 rows). (8) keeper
  timer unchanged (never fired, 26 boots zero journal); L0 kake round-12
  question still unanswered. (9) detector upheld: 6 events/0 phantom on 77
  rows. Evidence: `/tmp/kake-r13/` (scout-sweep, executor-charter,
  executor-pq5, executor-pq2, labrat-timers, revenger-history, critic,
  reviewer, connector, sentinel + sentinel-before.sha);
  corpus/knowledge/{publish-queue,ops-automation,keeper-timer-inert}.md
  updates; SKILL.md r13 amendments (at-vs-mtime, absent-semantics,
  every-row-since-ENTER pin framing).

- 2026-09-29 — round 14: freshness axis-move — **re-verification +
  armed watches** (probe-latest 4.6h fresh at open — 00:00:59Z sweep
  landed mid-round, captured live). 12 read-only L2 probes in one batch
  (scout + executor×3 + labrat + revenger + critic + reviewer +
  connector + sentinel + scribe + planner → `/tmp/kake-r14/`); zero
  fires, zero pushes, zero systemctl mutations, zero webzites-state
  writes (sentinel PASS: 45/47 files byte-identical across the round —
  only the timer-owned `probe-latest.json` + `probe-history.jsonl`
  changed, exactly the 00:01:09.976Z sweep: history 77→78 rows, new row
  `total:18` **12 ok / 5 violated / 1 error — identical set**,
  probe-latest `at` matched the row to the ms). Findings: (1) pattern
  HELD for the 5th consecutive sweep-day (06:00:46.703Z / 12:00:53.973Z
  / 18:01:09.822Z / 00:01:09.976Z + manual 18:51:26Z all 12/5/1);
  labrat independent 18-curl replication 23:1xZ = 18/18 MATCH, 0 diffs;
  probe-delta on 78 rows = **6 events / 0 phantom** (last ENTER lucario
  09-27). (2) PQ-5 still pending (23:11Z: 404 / 13,409B / sha
  `93ddca9a…` byte-identical; zero `fire:true` journals since
  09-26T15:34:24Z; kimi-map 09-26-vintage) → **the pending-publish watch
  is now armed** (publish-queue.md §r14): P1–P3 NOW-predictions verified;
  E1 slug-404→200 is the primary discriminator (preview-host 200 proves
  nothing; `kimi-map` E5 never gates); named half-states F1
  card-published-slug-not-set, F2 wrong-version; F3 premise-void pivot.
  (3) **PQ-12 dated re-check loop armed AND caught a transition
  in-round:** `fleet.config.json:256` pin still `2026-09-26 scribe beat`
  (operator edit not landed) but the 00:06:19Z scribe fire pushed
  `pushed:true` for the first time in 4 beats — beat `9c28d29` (falsified
  the round's own `pushed:false` prediction; `pull timed out` blocker
  cleared). Live now `2026-09-29 scribe beat (` / 53,386B / `fb365e38…`
  == `9c28d29`; clone synced (PQ-3's behind-5 gate cleared); row 78 stays
  violated on the pin gap — correct re-pin literal is now `2026-09-29`,
  not `2026-09-28` (edit-time literal guard). (4) PQ-2 unchanged again —
  19/93 served, 74 missing, 0 per-URL transitions (two independent
  sweeps: executor 23:15Z + reviewer 23:19–21Z; raw 15/78 + 4 dir-index
  twins = 19/74); mirror sitemap.xml itself 404 (0 locs live). (5) New
  observations landed: the 13,409B `93ddca9a…` body is the GENERIC kimi
  404 sentinel (same sha on plazir15.kimi.page + lucario.kimi.page — it
  cannot discriminate slots; decisive = 404 flip + `unpublished404`);
  `ds4cc.com/sitemap.xml` + `/robots.txt` live-404 — the 93-loc canonical
  list is working-tree-only (unpushed `e82a262`/`f3d2ecd`). (6) Charter
  post-push subpath audit (b74190e…a8f1e2b series) = NULL: 5/5 paths
  byte-identical live==raw + og:image 200/121,710B — completed baseline,
  not a move. (7) 12 stale citations fixed: r13 06:00:36Z clock-mix
  (journal Starting vs history `at` — LOG + ops-automation:96-99 +
  r13-report errata); byte-frozen→content-frozen cfemail rule; ops-
  automation "earlier sweeps" + denominator basis (65 full-sweep gaps);
  free-read-verbs ×9 line cites (`:193`→`:192`, `:1190`→`:1184`, SKILL
  renumbering incl. missed `SKILL.md:76-100`→`:122-128,:155-158`);
  keeper-timer-inert ×3 (procedure cite + 2 historical annotations).
  (8) Critic pre-adjudication: "pattern held" = verification, not a move;
  score stays 8 — armed capability only becomes move-eligible when a
  watch **catches** the event in-round. (9) Protocol repair: r13's
  report was **untracked in the main repo** (its "commits in both repos"
  claim was false on the main half) — filed this round alongside r14's.
  (10) Keeper timer still inert; L0 kake round-12 question unanswered.
  Evidence: `/tmp/kake-r14/` (scout-claims, executor-charter,
  executor-pq5, executor-pq2, labrat-replicate, revenger-history,
  critic, reviewer-cites, connector-sib, sentinel + sentinel-{before,
  after}.sha, planner-move, scribe-draft);
  corpus/knowledge/{publish-queue,ops-automation,keeper-timer-inert,
  free-read-verbs}.md + SKILL.md step-4 watch wiring.

- 2026-09-29 — round 15: freshness **axis-move, drift CAUGHT — SCORECARD
  8→9** (critic-adjudicated: dated external FS-drift event + complete sweep
  catches genuine previously-cited misses + corrections landed and
  re-verified; the watch-read half was re-verification only). probe-latest
  `at` 00:01:09.976Z = 0.7h fresh at open (watchdog launched 00:44:25Z).
  12 read-only L2 probes in one batch (planner + scout + executor×3 +
  labrat + revenger + sentinel + critic + connector + reviewer + scribe →
  `/tmp/kake-r15/`); zero fires, zero pushes, zero systemctl mutations,
  zero webzites-state writes — sentinel: **47/47 state+fleet files
  byte-identical across the whole round** (no sweep or scribe fired inside
  it). Findings: (1) **premise drift** — the r14 plan predicted "r15 opens
  after the 06:00:59Z sweep, two rows landed"; actual launch 00:44:25Z is
  ~5.3h BEFORE it, only row 78 present (r16 plan re-anchored: first post-
  06:00:59Z round carries row 79, post-12:00:59Z carries 80). (2) **PQ-12
  `PERSIST`** — pin `2026-09-26 scribe beat` (config untouched since
  09-27T15:30:57Z) vs live `2026-09-29 scribe beat (` / 53,386B / sha
  `fb365e38…` (00:48:51Z; 09-26=0,09-28=0,09-29=1 counts); live ==
  remote HEAD `9c28d29` (ls-remote) == clone HEAD (behind 0 — the scribe's
  own 00:06:19Z run refreshed FETCH_HEAD 00:11:30Z; kake pulled nothing).
  Scribe ledger: 0 beats newer than `9c28d29`; next ~06:06Z post-round;
  telemetry degraded (grok-web 300s timeout, kimi route failure →
  local-fallback). Correct edit-moment literal: `2026-09-29 scribe beat`.
  (3) **PQ-5 still pending** — 404/13,409B/sha `93ddca9a…` byte-identical
  (L1 00:45Z + executor 00:49:37Z); P2 violated in row 78; P3 vault
  200/9,966B, member still 404 (dead links 3/10). E1 never fired → armed,
  not move-eligible. (4) **PQ-2 gate CLOSED, unchanged** — remote `e6bd071`
  (ls-remote 00:49:11Z), 0/20 of the unpushed commits landed;
  `sitemap.xml`+`robots.txt` live 404 (9,379B GH 404 ×2); 93-loc sweep
  correctly skipped. Errata caught: the PQ-2 cell's "root content-frozen
  74,641B" is the **mirror root** (r14's own artifact fetched
  ds4cc.kimi.page — my round brief mislabeled it canonical); canonical
  `ds4cc.com/` = 79,453B sha `b6f65899…` byte-identical to
  `origin/main:index.html` (etag `6ab49127-1365d`, 0 cfemail → plain sha
  is the freeze metric); normalized-sha values differ by normalizer
  (r14 `4427b7f8…` vs r15 `6a0c24b5…` — freeze-equal within each series);
  "working-tree-only" → sitemap+robots ARE tracked at local HEAD
  `f3d2ecd`, absent from `origin/main`. (5) **path-sweep = the move** —
  all 58 unique cited paths (95 occurrences / 8 roots) re-tested:
  **49 resolve, 9 miss = 4 self-declared-absent (verified-true claims:
  webzites `package.json`, 3 lucario artifacts) + 5 genuine danglers**:
  `~/Projects/ufofsdbeta`, `…/.ufo`, `ufofsdbeta-kimi-review` (verified
  PRESENT at r1, lessons/round-1-aggregator-audit.md:34-35) and
  `ephemeral/wz1` + `wz1/ds4cc` (`ephemeral/` exists, emptied
  21:42-03:00). The ufofsdbeta pair vanished inside `~/Projects` mtime
  20:51:31-03:00 — the exact instant kasegi reported `bounties` gone
  (l0-questions.md; same-window corroboration, actor still undetermined).
  Annotations landed (SKILL.md:48-52,118-120,266-279,328-330;
  mirror-pitfalls:3-6,29-30; publish-channels:15-18) — dated flags, never
  silent deletion; per-round re-sweep rule armed in SKILL.md §traps;
  r10's "60/60" superseded. Post-fix re-check: annotations present,
  danglers still absent, guard 47/47. (6) timers — probe healthy (row 78
  = 00:01:09.976Z, next 06:01Z = systemd "06:00:59Z"), keeper/reaper
  journals still empty; L0 r12 keeper+lucario questions still unanswered.
  (7) history/detector — 78 rows (77 = sanctioned r11 total:1 clobber,
  not a sweep); probe-delta on 78 = **6 events / 0 phantom**, last ENTER
  lucario 09-27T16:38:27Z, 0 transitions this round. (8) adjacency —
  `bounties` has 0 kake citations; kake's own danglers sit inside the
  same drift window; connector bounded it to ≤23:32–23:51:31Z (~19m,
  kasegi last-alive→mtime) and flagged `.git` mtimes as contaminated
  (permitted `git status` reads refresh index metadata — not actor
  evidence). kotoba r14:108-112 routes a probe-delta.mjs complaint (exit
  0 on any nonempty parse) to kake — received, dispositioned **by
  design** (probe-delta.mjs:26 documents "report, not a gate"; exit-2/64
  reserved for real failures — r10 contract). (9) critic arc — initial
  ruling "re-verification only" (sample-bounded C6: 10/10 resolve);
  ScoutPaths' complete enumeration flipped C6 to REFUTED → move-eligible,
  freshness 8→9 (predicate: dated drift + complete sweep catches genuine
  previously-cited miss + correction landed + post-fix verify). The
  watch-read half (PQ-12 PERSIST / PQ-5 pending / PQ-2 closed) stays
  re-verification per r14 precedent. Evidence: `/tmp/kake-r15/`
  (planner-move, scout-paths, executor-pq12, executor-pq5, executor-pq2,
  labrat-timers, revenger-history, critic + addendum, connector-sib,
  reviewer-cites, scribe-draft, sentinel-before.sha, sentinel-after.sha,
  charter-live.html, p1-body.bin, mirror-root.html, final-{root,sitemap,
  robots}.html); corpus edits `publish-queue.md` §r15 + PQ-2 cell erratum,
  `SKILL.md` ×4, `mirror-pitfalls.md` ×2, `publish-channels.md` ×1;
  l0 corroboration line appended.

- 2026-09-29 — round 16: freshness axis-move **9→10** — drift detection
  widened from path-citations-only to **all quantified standing claims**, and
  made reproducible. Articulated by 12 read-only L2 probes in one batched call
  (planner + scout-paths + scout-claims + executor×2 + labrat + revenger +
  critic + reviewer + connector + sentinel + scribe → `/tmp/kake-r16/`); zero
  fires, zero pushes, zero systemctl mutations, zero webzites-state writes
  (state-dir sha `15a5c47f…4669cb2` identical at open and after every
  instrument run). (1) **Instrument landed** — `scripts/freshness-sweep.mjs`
  (read-only, zero deps, exit 0/1/2/64, `--json`/`--offline`/`--section`/
  `--selftest`) + `corpus/knowledge/freshness-pins.json` + runbook
  `corpus/knowledge/freshness-sweep.md`; sections: §paths (every `~/…`
  citation resolves; frozen `pathsMissSet` = 9 annotated misses; a NEW miss is
  drift), §history (row floor 78, last-at ceiling 6h20m, fleet-shape set
  equality, `probe-delta` exact event count 6 + last ENTER lucario
  @09-27T16:38:27Z, phantom max 0), §armed (PQ-12/PQ-5/PQ-2/ds4cc-sitemap/
  PQ-14). `--selftest` 9/9 (declaredAbsent exit-neutral; unannotated miss →
  1; interior-tampered history → 1; malformed JSONL → 2; unknown flag/section
  → 64; write-API confinement). (2) **Claim-class sweep = the move evidence**
  — 160 quantified claims enumerated with one live recipe each
  (`/tmp/kake-r16/scout-claims.md` + `claims.tsv`): **117 HOLD / 15 STALE / 7
  UNVERIFIABLE / 21 HISTORICAL-OK**. All 15 stale items fixed or re-pinned:
  `ops-automation.md` 77→78 rows ×5 + 66→67 full sweeps + 65→66 gaps +
  20/65→21/66 band (`:4,22,29-31,112`); `probe-delta-alerting.md` 76→78 /
  66→67 / 10→11 spot + era families {1:10→11, 18:7→8} (`:40,102`);
  `keeper-timer-inert.md:65` + `free-read-verbs.md:373` log-age 20/21→19/21
  (the widened `log=8d(` pattern keeps 20 — `veigapunk-page` ends `e2e fix`);
  `free-read-verbs.md:212-216` sync-check bare sample ok:3→4 + attention 6→5
  (plazir27runs-on now in-sync) and `:166-171` reconcile fleet 7→6 ids /
  6→5 DIFF (both re-run live at 02:35Z, exits 1 re-proven — exit-code-only
  re-checks would have called these "unchanged"); `fire-journal-codes.md:7-13`
  journal top-level key union (measured over all 28 journals: exactly
  `site,mode,startedAt,steps[],fire[,error]` — `newVersion`/`preview`/
  `operatorNext`/`liveAfter` were listed as top-level and are not) and `:55`
  `recreate plazir15` fired ×2→**×3** (`fire:true` in c7/c4/c6 journals);
  `publish-queue.md` PQ-10 `Nightcall` clause (body now carries both cases)
  and the bounties self-cite erratum `:213→:214` (reviewer-caught);
  `SKILL.md` pins `cli.mjs:1086`→`:1087` and `:386`→`:389`. **S11 refuted on
  re-measurement:** the ETag is `6ab49127-1365d` in 7/7 L1 fetches (matching
  the file); recorded as a rule instead — ETags are edge-unstable identifiers,
  never freeze metrics (the sha is). (3) **In-round domain catch (PQ-14)** —
  `~/Projects/plazir-15-site` is **5 commits ahead of `origin/main`** (HEAD
  `c814526`, remote `bd02d10`, all 5 dated 2026-09-26), so live serves the
  pre-push tree: live `sitemap.xml` **8 locs** incl. `/tetris/` (sha
  `3eb1722c…`) vs source **7** (`8e162356…`), live `snake/` has 0 `og:url` vs
  source 1, live `speedrun/` canonical self vs source `ds4cc.com`; all 8 live
  locs 200 → **stale-not-rot**; invisible to `probe`/`reconcile` (root
  `index.html` not in the lag set → `in-sync`). Falsifies `drift-detection.md`
  "plazir15-ghp tree byte-identical to live" (corrected + §r16 proof);
  ledgered **PQ-14** (`publish-queue.md`); the instrument now reproduces the
  catch mechanically (`PQ-14 … sitemap LIVE-SOURCE-GAP !! DRIFT`, exit 1, run
  02:4xZ). r7's "103 locs" is now written as **103 live-side / 102
  source-side — the delta IS the gate** (`sitemap-orphan-audit.md`, SKILL.md
  :194, README). (4) **Armed watches, re-verification only** — PQ-12
  `PERSIST` (pin `2026-09-26` @`fleet.config.json:256`, mtime unchanged
  09-27T15:30:57Z; live `2026-09-29 scribe beat (` 200/53,386B/sha
  `fb365e38…` == r15 == remote+clone `9c28d29`; EDIT-LANDED/CHURN-AGAIN/
  SILENT/ANOMALY each excluded with evidence; scribe ledger 28 beats, newest
  00:06:19.897Z `pushed:true`, none newer than `9c28d29`); PQ-5 `PENDING`
  (404/13,409B/`93ddca9a…` identical to the armed baseline; E1 never fired;
  P3 vault 200/9,966B/`d93d6a0c…`, 13 PROPERTIES, 3/10 dead — unchanged; the
  twin `veigapunk.kimi.page` is 10,059B, do not swap the two); PQ-2
  `GATE-CLOSED` (remote `e6bd071`, local `f3d2ecd`, 20 unpushed,
  sitemap/robots 404/9,379B). (5) **Path base STABLE** — full re-sweep at
  02:36:54Z: 59 targets, 49 resolve, 10 declared-absent, **0 new dangling**;
  all 5 r15 danglers still absent; 4 new targets in-round
  (`~/Projects/bounties`, `speedrun-r1.md`, `~/projects`, `open-bug-bounties`)
  — all resolving/annotated; kake's 4 domain roots untouched by both windows
  (A 23:51:31.175Z, B 01:45:06.815Z) and the lowercase dir is a distinct inode
  (27238 vs 101125103). (6) **Sibling/hazard** — kasegi's two loss reports
  (bounties r15, groknight −681f/41d/14MB r16 01:45:06.815Z) have **0 kake
  citation descendants** (connector), but revenger bounded a LIVE escalating
  prune regime on `~/Projects` roots inside r16 (W1 ≤23:51:31Z, W2 00:42:39Z,
  W3 01:45:06Z, W4 `.ufo-missions` 262→2 dirs ≤02:05:07Z, W5 02:19:20Z) with
  the actor still undetermined and all `.git` mtimes contaminated → L0
  corroboration line appended (kake | round-16); the kasegi fleet-GC
  hypothesis is NOT confirmed (0 groknight/prune mentions in
  dispatcher-daemon.out / fleet-ledger.jsonl). kotoba r14's probe-delta
  exit-0 complaint stays dispositioned by design. (7) **Adjudication** —
  critic's first two rulings: freshness 9→10 NOT-ELIGIBLE (no trigger;
  instrument = operability per r10 precedent) with two instrument
  suppression paths proven (interior-history tamper absorbed; ±2-line/OR
  `declaredAbsent` mislabel); both were closed (exact `deltaEventsExact`/
  `deltaLastEvent` pins, armed set-delta gate, opt-in
  `pathsAbsenceStrictSameLine`, 9/9 selftest) and the critic then re-ruled
  **MOVE-ELIGIBLE on both independent branches** (complete-claim sweep; the
  unledgered plazir live/source drift) with the predicate: "complete live
  standing-claim sweep flags a previously unmeasured stale/unverifiable claim
  with raw evidence OR catches previously unledgered live/source drift and
  repairs/ledgers; instrument alone remains operability-only." Reviewer
  verdict `concerns` (1 FAIL: the self-cite line number) — fixed in-round;
  its 3 low residue items are pre-r15 conventions, recorded not fixed.
  Evidence: `/tmp/kake-r16/` (planner.md, scout-paths.md + 4 target lists,
  scout-claims.md + claims.tsv + raw recipes, freshness-sweep.mjs,
  freshness-pins.json, executor-instrument.md, executor-arms.md,
  labrat-timers.md, revenger-history.md, critic.md, reviewer-cites.md,
  connector.md, scribe-draft.md, sentinel-{before,after}.sha,
  raw/final-{bare,offline,selftest}.out); repo edits: SKILL.md ×6,
  corpus/README.md ×4, corpus/lessons/round-16.md, corpus/knowledge/
  {freshness-sweep.md, freshness-pins.json, ops-automation.md,
  probe-delta-alerting.md, drift-detection.md, publish-queue.md,
  sitemap-orphan-audit.md, keeper-timer-inert.md, free-read-verbs.md,
  fire-journal-codes.md}, SCORECARD.md 9→10, LOG.md r16.

- 2026-09-29 — round 17: freshness **HOLD 10 — live drift caught and
  repaired; instrument suppression paths closed.** Nine L2s dispatched in one
  valid batched call (planner, scouts ×2, revenger, labrat, critic, connector,
  reviewer, scribe) plus the separately re-run live-surface scout after the
  first batch's invalid-agent preflight; all read-only, artifacts under
  `/tmp/kake-r17/`. (1) **W6 caught before repair** — baseline
  `node scripts/freshness-sweep.mjs` at 03:20:19Z exited 1 with a NEW §paths
  miss: the round-1 lesson cited lowercase
  `~/projects/shokunin/.ufo/reports/round-1/web-properties-publishing.md`,
  but `~/projects` had disappeared since the r16 ~02:4xZ sweep. Baseline:
  38 files / 65 tokens / resolve 47 / declaredAbsent 10 / drift 1 /
  missSet 11. The report survives at the canonical uppercase path; cite fixed
  and `pathsMissSet` re-pinned 9→10. R16 raw evidence resolves the inodes:
  `~/Projects` = 27238 and lowercase = 101125103; capital stayed 27238.
  `~/DIRMAP.md:1,7,27` records the cleanup — lowercase children absorbed into
  the existing capital root, then lowercase removed; capital/home mtimes bound
  it to 03:13:18–03:14:07Z; `magga-2`→`magga` also moved. This is W6 in the
  broader cleanup/prune regime, but unlike W1–W5 the cited report was
  preserved. Exact command/actor remains unproven. L0 corroboration updated.
  (2) **Complete claim-class re-sweep** — all r16 inventory rows re-ran:
  117/117 HOLD; 15/15 r16 stale repairs still correct; 7 UNVERIFIABLE carried;
  21 HISTORICAL-OK; plus 16/16 new r16/r17 claims HOLD. Nine new deltas were
  surfaced and closed/qualified in this commit: W6 inode/mtime/path + child
  rename; edge ETag flip (`6ab49127` in r16's 7/7, back to `6ab49126` in
  r17's 8/8 → ETag never a freeze metric); r17's self-stale 38/380 and
  38-file literals; wrong inode wording; nonexistent `corpus/claims` cite;
  unnamed scribe ledger locus (verified at
  `origin-work/ufo-fsd-alpha/.ufo/charter-scribe/ledger.jsonl`: 28 rows,
  newest 00:06:19.897Z `pushed:true`); and README's range gloss over missing
  lesson rounds. Final corpus wording matches live evidence.
  (3) **Instrument hardening** — P2b `projectsChildrenSet` pins the 36 direct
  `~/Projects` children and prints added/removed names, informational by
  design (critic: blanket-gating operator churn is false-positive-prone;
  gate only a future protected web-root set). `pathsFiles` was a bare number
  `38`, but its evaluator requires an array: the delta had been
  **inert-by-type** since r16. It is now the evaluated 39-file list and prints
  `+0/-0`. `loadPins` previously caught any parse/ReferenceError and silently
  fell back to defaults, making all gates inert; invalid pins now fail closed
  with exit 2. Permanent malformed-pins case added: selftest **10/10**. The
  header also falsely called A5's six live plazir pins “not evaluated”; their
  consumed-key classification is now correct, while truly unused pins stay
  explicit.
  (4) **Final measured gate** (04:18Z) — offline exit 0: §paths 39 files /
  160 occurrences / **66 targets / 49 resolve / 10 declaredAbsent / 0 drift /
  7 unresolved**, missSet 10, relative-cite matcher 382 lines, file set
  `+0/-0`, children 36 MATCH; §history 78 rows / 67 full / 11 spot / 6
  events / 0 phantom / last ENTER lucario. Live exit 1 **only** for expected
  PQ-14 `plazir-live-source-gap`; no other reason. `webzites/state/` 33-file
  sha set byte-identical before/after every run. Independent relative-cite
  scout: sample 30/30 accounted for, 0 substantive misses; full-tree 438 true
  occurrences, all 10 unresolved tokens non-cites/foreign-base/declared
  absent. All 8 informational pins HOLD (vault 9,966B/sha/10 URLs/3 dead;
  fleet 21 with 12/3/3/3 statuses; grokbots 20; clones 50).
  (5) **Armed watches unchanged** — PQ-12 `PERSIST` (live GHP
  200/53,386B/`fb365e38…`, literal 2026-09-29 vs config pin 2026-09-26);
  PQ-5 `PENDING` 404/13,409B/`93ddca9a…`; PQ-2 `GATE-CLOSED` remote
  `e6bd071`, HEAD `f3d2ecd`, 20 unpushed, sitemap+robots 404/9,379B;
  PQ-14 `GATE-CLOSED`, 5 ahead, live/source sitemap 8/7. PQ-3 checkout
  `main...origin/main`, HEAD `9c28d29`. Probe timer next 06:00:59Z; row 79
  has not landed. Keeper timer disabled/inactive, empty LastTriggerUSec;
  keeper reports still frozen 09-21.
  (6) **Adjudication/review** — critic: **MOVE-ELIGIBLE, score holds 10**:
  instrument work alone is operability, but the before-sweep W6 catch is the
  required freshness trigger. Initial reviewer FAIL (two stale 38/380
  literals) repaired; final reviewer **PASS** after fresh reproduction.
  Its two residual numeric nits (38→39 file list, 438→436 true relative
  occurrences) and two older line-pin drifts (round-1 audit, SKILL push rule)
  were also fixed before commit. No sibling independently reported W6; kake
  has zero
  citations into kasegi's lost groknight descendants. Connector found kagi
  r16's citation into the edited round-1 lesson shifted from its asserted
  lines; reported, not absorbed. No L0 answer to keeper enable-vs-retire or
  earlier prune entries.
  (7) **Operator relay, reported not absorbed** — effective config has
  `modelRoles.m_swe = devin/swe-2:max`, but
  `retry.fallbackChains.m_swe = null`; the requested exact
  `m_swe → openai-codex/gpt-daybreak-blue-latest:max` final-only chain is not
  visible. No genuine m_swe capacity failure occurred, so runtime advancement
  to Daybreak was not observed; no failure forced and no frozen contract/config
  changed. Evidence: `/tmp/kake-r17/` (`baseline.{out,json}`,
  `final-{live,offline,selftest}.{out,json}`, `scout-{live,pins,claims}.md`,
  `claims-delta.tsv`, `revenger-w6.md`, `labrat-timers.md`, `critic.md`,
  `connector.md`, `reviewer-{cites,final}.md`, `planner.md`,
  `scribe-draft.md`, `sentinel-before.sha`, `raw*/`); repo edits:
  `scripts/freshness-sweep.mjs`, `corpus/knowledge/{freshness-pins,
  freshness-sweep,publish-queue}.md`, `corpus/lessons/{round-1-aggregator-audit,
  round-8-aggregator-box3-coldrun,round-16,round-17}.md`, `corpus/README.md`,
  `SKILL.md`, `SCORECARD.md`, `LOG.md`.

- 2026-10-14 — round 18: freshness **HOLD 10 — W7 mega-prune caught by the
  standing gate before any repair; re-census completed, three debts
  carried.** OMP/ufo-fsd re-census round (fleet directive): the substrate
  moved — `~/Projects/origin-work/ufo-fsd-alpha` gone, same repo re-rooted
  at `~/Projects/ufo-fsd-alpha` HEAD `964f443e` (no
  `.ufo/charter-scribe/ledger.jsonl` on the new tree). (1) **Baseline
  sweep 12:40Z → exit 2**: §paths 36 unannotated misses + 45 beyond the
  pinned miss set; §history `probe-history.jsonl` unreadable; §armed
  PQ-12 CHURN-AGAIN (live `2026-09-30 scribe beat`, 53 660 B, sha
  `7c243a1d…`), PQ-2 + PQ-14 ANOMALY (repos gone), PQ-5 PENDING, ds4cc
  sitemap PRE-PUSH. `~/Projects` children went 36 → 14 (33 removed incl.
  `webzites`, `ds4cc-marketplace`, `plazir-15-site`, `lucario`,
  `origin-work` wholesale, `~/DIRMAP.md`, the probe/keeper systemd units;
  11 added). (2) **Repair** — append-only errata: 63 cite lines in 22
  files now carry inline `r18 re-census 2026-10-14` markers (absent,
  historical record; zero claims deleted; 3 multi-token/multi-line cites
  hand-repaired after the blanket pass broke brace-list grammar).
  `freshness-pins.json` re-measured in one pass: `pathsMissSet` 10→55,
  `projectsChildrenSet` 36→14, `charterGhp{Pin,LiveSha,ChurnAfter}`
  re-baselined to the observed 2026-09-30 beat, `probeHistoryAbsent`
  added. `freshness-sweep.mjs`: pin-declared absent history source →
  `SUSPENDED` (loud skip line, never counted as pass) instead of exit 2;
  selftest fixture re-anchored `webzites/fleet` → `ufo-fsd-alpha`.
  (3) **Verdicts** — bare: `VERDICT: DRIFT — §armed: PQ-2 ANOMALY,
  plazir-gate-anomaly (exit 1)`; `--offline`: `VERDICT: OK (exit 0,
  partial)`; `--selftest`: 10/10; §paths drift 0 / newMissing 0 /
  children MATCH. (4) **Carried debt** — PQ-2 + PQ-14 ANOMALY (source
  repos gone; exit 1 stands, correct) and §history SUSPENDED; each named
  with unblock in SCORECARD `## Planned`. Evidence: `/tmp/kake-r18/`;
  `corpus/lessons/round-18.md`; files: `scripts/freshness-sweep.mjs`,
  `corpus/knowledge/freshness-pins.json`, `corpus/README.md`, 21 corpus
  md errata files, `SCORECARD.md`, `LOG.md`.

## 19 — re-census round (freshness axis-move)

2026-10-14 · steered round 19 · axis: freshness · 32-lane fleet wave + parent integration.

Full round detail: `corpus/lessons/round-19-recensus.md`. Advisory inventories:
`../.ufo/waves/shokunin12h-20261014-p1-repair/members/`.

## 2026-10-15 — round 16 continuation: citation-local absence evidence

- Steer: round 16, despite inherited records through round 19. Historical
  entries/report remain intact; no counter or routing mutation. Both owned
  axes score 10; freshness wins the tie on the falsifiable false-green below.
- Motivating baseline: `20d13115323fba21bb3d63204cce13425feaf399`.
  `node scripts/freshness-sweep.mjs --section=paths --json`, run from an
  isolated `git archive` snapshot of that commit on the live filesystem,
  returned exit 0: resolve 5, declaredAbsent 55, drift 0, newMissing 0,
  files 41. The preexisting working-tree edit to `SKILL.md` was excluded.
- Counterexample: the absent webzites CLI is still invoked at
  `SKILL.md:59`; its local annotation window has no absence declaration.
  A historical annotation in `corpus/knowledge/free-read-verbs.md:5-6`
  marks the same target elsewhere. `scanCitations` ORs those declarations
  across all occurrences, hiding the unannotated instruction. An actual CLI
  invocation over a two-file fixture reproduced exit 0 for mixed annotated
  and unannotated occurrences, including the canonical-home alias variant;
  the all-annotated control also returned 0.
- Single correction: retain annotation evidence per citation location.
  A missing target with any locally unannotated occurrence is drift;
  JSON/human diagnostics identify the offending occurrences. Existing
  per-citation annotation windows, normalization, miss pins, history and
  publishing gates are intentionally unchanged. This improves detection,
  not source restoration or wholesale corpus repair.
- Required L2 dispatch: one native OMP batch, nine seats (planner,
  connector, executors ×3, scribe, scout, reviewer, critic), using unchanged
  host role overrides. It is not a claimed validated UFO uniform wave.
  The score remains capped at 10; measured outcomes and final verification
  are recorded in the completion entry below.

## 2026-10-15 — round 20 interactive reconciliation and WWKD plan

- The preceding uncommitted “round 16 continuation” section came from the
  interrupted headless worker. Its label is not a completed-round counter
  and is not authority for this dispatch. Existing owned history reaches
  `20d13115323fba21bb3d63204cce13425feaf399` (round-19 correction), with
  the fleet's `.ufo/reports/round-19/kake.md` recording the actual round.
  That history and the inherited three-file patch are preserved.
- Current round attempt: **20**, freshness (both LIVE owned axes scored 10;
  the target-wide annotation suppression defect breaks the tie). Plan:
  `plans/wwkd-round-20-citation-locality.md`. `corpus/QUALITY.md` and
  `MINT.md` were absent in the lane inventory at activation.
- Dispatch precondition fails: effective `cfg://task/agentModelOverrides`
  routes content through `@m_mid`/`@m_fast`, audit through mixed
  `@m_fast`/`@m_mid`/`@m_strong`, connector through `@m_mid`.
  Required bindings are content `@m_composer`, audit `@m_grok`, connector
  `@m_antigravity` with `@m_zfl` fallback; the effective Antigravity
  fallback chain is empty. No route/config mutation or substitute dispatch.
  This attempt earns no verified-round credit without the actual required
  wave. Local verification and truthful continuation remain reachable.

## 2026-10-15 — round 20 local proof, blocked admission

- Motivating evidence: round-19 lesson's unmarked publishing instructions
  plus the actual baseline CLI false-green, not a recalled launch counter.
  Baseline program revision:
  `20d13115323fba21bb3d63204cce13425feaf399`. Retained inherited
  per-location annotation sets in `scripts/freshness-sweep.mjs`;
  simplified its new human diagnostic and removed the incidental
  first-evidence ordering assertion from case M. The preceding nine-seat
  dispatch note is inherited history, not a compliant 32-seat dispatch or
  evidence that this interactive session launched specialists.
- Smoke: `.ufo/round-20/{baseline-proof,candidate-proof}.json` contain
  actual CLI argv/full output/exits. Mixed, distant same-file, home-alias,
  brace-expanded and strict-mode cases changed false-green exit 0 to drift
  exit 1; all-annotated and present-target controls stayed exit 0.
  `node .ufo/round-20/replay-proof.mjs` verifies committed input digests
  before comparing both programs: `CITATION_LOCALITY_PROOF: PASS
  (cases=7, failures=0)`, exit 0. The permanent case M checks actionable
  locations and unchanged annotated controls, not evidence-record ordering.
- Acceptance: isolated-HOME selftest `14/14`, exit 0. Baseline program on
  the same measured candidate corpus: drift 0 / declaredAbsent 55, exit 0.
  Candidate path gate: 7 missing targets / 26 locally unannotated locations /
  declaredAbsent 48 / newMissing 0, exit 1. Offline exit 1 with history
  SUSPENDED and all armed HTTP checks skipped. Full verdict lines/exits:
  `.ufo/round-20/acceptance.json`; input hashes:
  `.ufo/round-20/measured-corpus-inputs.json`; actionable debt:
  `.ufo/round-20/citation-debt.json`. Candidate script SHA-256:
  `816bbe688d54761930726c7196a6bf37ff3bc4bbdfbcd896ea7e1a5f4d1a6463`.
- Canonical wave plan/render: exit 0, exactly 32 distinct names/scopes and
  32 leading Godspeed invocations; **zero native task calls**, no registry
  persistence. Held payload and validation live under `.ufo/round-20/wave/`.
  Effective alias/fallback mismatch remains the blocker. No new routing
  overlay, global change, external request, source repair, or push.
- Docs: `SKILL.md` records citation-local P1 and the owned gate registry;
  the runbook preserves but explicitly supersedes the old OR rule and
  historical copied baselines. `corpus/QUALITY.md` grounds admission
  criteria in the measured lesson; `corpus/README.md` indexes them and names
  the frontier. `corpus/lessons/round-20.md` records candidates, admits,
  rejects, the missing non-author spot-check, and measured verdicts.
- Per-axis outcomes: freshness improved locally; operability unchanged.
  Learning trends: expansion unchanged, quality improved locally,
  discernment unchanged. **Blocked/unadmitted; no new verified-round credit,
  no promotion, no native judgment.** Existing numeric ratings stay legacy.
- Named debt/unblock: host owner restores required existing role bindings
  and Antigravity→ZFL fallback; kake triages each emitted citation location;
  operator restores or retires missing publishing sources/history; kake
  separately addresses the previously reported confinement-assertion
  weakness; a non-author checks an admit and reject. The interactive wall
  row has no applicable task/expected receipt binding
  (`.ufo/round-20/receipt-binding.json`), so no receipt was fabricated and
  Sighting remains incomplete. The report/continuation land after the
  owned work commit; a fresh session resumes this actual round, not round 21.

## 2026-10-15 — round 20 shape-only evidence erratum

- Review found a dispatch-contract violation in
  `f405166a33878cab32bff18dce3f39c9d9d3e463`: acceptance evidence stored
  controlled fixture override values, captured stdout repeated derived
  fixture paths, and the SKILL selftest command embedded assignments.
  Generated lane-local values are still environment material; the
  shape-only rule was not satisfied by that initial landing.
- Follow-up correction, not amend/history rewrite:
  `.ufo/round-20/{acceptance,baseline-proof,candidate-proof}.json` replace
  captured override paths with symbolic placeholders and retain only
  variable names/isolation shape. Ordinary frozen fixture metadata remains
  available for replay. SKILL now names isolation requirements without
  assigned values. The previously stated “full output” means sanitized
  output after this erratum, never byte-verbatim raw environment values.
- Verification: structured evidence reserialized and captured JSON outputs
  parsed; all stored verdict lines and exit codes compared unchanged before
  and after the redaction. `.ufo/round-20/redaction-validation.json`
  records PASS. No program/fixture changes and no runtime gate rerun.
- `corpus/lessons/round-20.md` records this rejected representation;
  `corpus/QUALITY.md` adds its grounded shape-only criterion. The original
  commit remains in ancestry and is not claimed conformant or scrubbed.
  No new round credit, admission, receipt or Sighting completion follows.

## 2026-10-15 — round 20 blocked report and fresh-session handoff

- Local work commit: `f405166a33878cab32bff18dce3f39c9d9d3e463`;
  evidence-format correction:
  `9825b2ab5cd429647c09fb4964ec17e2db615e35`. The latter preserves exact
  verdicts/exits while recording the former's shape-only conformance defect.
- Publication paths, inside the lane only:
  `.ufo/reports/round-20/kake.md` and
  `.ufo/round-20/continuation.json`. They name both commits, full verdict
  lines/exits, provisional axes/trends, zero new verified-round credit,
  exact role/fallback blockers, citation debt and receipt prerequisite.
- Handoff structure checked: actual round 20, roundComplete false,
  verifiedRoundsAdded 0, 32 planned members, zero native task calls, next
  fresh session resumes 20 rather than advancing to 21. Runtime/gate checks
  were not re-run for this bookkeeping publication.
- No applicable receipt was minted or validated because the real task/key
  binding is absent; no fabricated replacement, Sighting completion,
  fleet ledger edit or push. Restore authorized existing host bindings and
  applicable receipt metadata outside this lane before a fresh session
  executes the required complete wave and seeks round admission.

## 2026-10-16 — protocol conformance: SCORECARD contract fields

- Operator amendment of 2026-10-16 (fleet root `84bade0`) requires the
  SCORECARD.md contract fields `axes`, `capabilities`, `planned`,
  `saturation`, `retired`. This lane already carried `axes`, `## Planned`
  and `## Retired` as real sections before this rollout.
- This rollout is additive scaffolding only: `## Capabilities` (empty
  repertoire table) and `## Saturation` (declaration deferred to the lane's
  next round). No axis claim was made and no score moved; no verdict or
  last-change round changed. No round credit follows.

## 2026-10-19 — round 20 resume (kaika campaign): three claims landed

- Motivating evidence: the round's own named debt — §paths drift 7 targets /
  26 unannotated locations (`.ufo/round-20/citation-debt.json`), the r19
  confinement erratum (`corpus/lessons/round-19-recensus.md:44`), and the W1
  ART dossier's K1–K3 contradictions of standing GHP claims
  (`kaika-w1/kake-art.md` §4, fleet ledger). Fresh session resuming round 20
  per `LOG.md:542`; base `cb807bc`.
- Swarm: one batched call of 10 L2 seats (planner, connector, scout, scribe,
  reviewer, critic, 4 executors), each prompt led by `/skill:godspeed` plus the
  verbatim directive; no model passed. Executor seats hit provider limits
  (`resource_exhausted`, then `turn_rate_limit_exceeded`) and were re-spawned
  in batched calls; a post-land reviewer/critic/mutation-tester batch followed.
  Record: `.ufo/round-20/resume/swarm-dispatch.json`.
- C1 freshness: 26/26 locations annotated in place (target + dated event +
  non-executable wording); `node scripts/freshness-sweep.mjs --section=paths`
  exit 1 → 0, drift 7 → 0, missSet 55 → 55, newMissing 0.
- C2 operability: exact-marker `writeConfinement()` + mutation case `e2`;
  isolated selftest 14/14 → 15/15; `confinement-mutants.mjs` killed 0/25 →
  25/25; replay-proof PASS; child-process/alias writes named residual.
- C3 capability: `corpus/SOURCES.md` 18 opened rows (census clean), 4 new
  knowledge entries with `source:`/`verified-at:`/`recheck:` headers, 27
  appended `r20-correction` tails; superseded literals uncorrected 9 → 0
  (`sh .ufo/round-20/resume/old-strings.sh`).
- Supporting: `PROVINCE.md` Core/Frontier/Adjacent/Surfaces appended;
  `corpus/README.md:60` continuation restored (dropped in `dd4eabf`); 7
  `QUALITY.md` criteria from mined mistakes; saturation line + window
  declared; round-21 plan. Lesson: `corpus/lessons/round-20.md`
  §Round-20 resume, §Gate — round-20 resume, §Mistakes.
- Pre-commit catches by the L1: S009 line anchor (lead said 1671; `grep -nF`
  at `481d28cb` → 1708); an inserted backtick and two dropped table pipes in
  append-only lines; a duplicate executor seat that overwrote the disposition
  ledger and kept editing after cancellation (ledger rebuilt from the 27
  tails; an indentation change reverted). Post-land review: mutation probe
  9/18 killed → e2 hardened (API list pinned, marker-error, anchoring and
  boundary fixtures; all 8 survivors re-run killed); citation-local notes
  made reader-visible (inside the last table cell); one broken table header
  repaired (`drift-detection.md:73`).
- No push (standing operator rule). No live-target probe. Non-author
  verification is the orchestrator's, after landing.

## Round 20 — post-review fixes (2026-10-19)

- Append-only ruling implemented: historical lesson/knowledge lines restored
  byte-identically; standalone notes and EOF correction blocks replace suffix
  tails; no gate change, no table split. C1 is improved-bounded (annotation
  only), 22/26 cleared, 4 remaining / 3 drift targets; missSet stays 55.
- Pointer errata for this LOG at `02b6dd0`: line 232's
  `free-read-verbs.md:373` now resolves at `:374`; line 237's
  `fire-journal-codes.md:7-13` now resolves at `:8-14`.
  Full 148-occurrence movement register: `corpus/lessons/round-20.md`
  §Inbound-pointer correction register; proof JSON
  `.ufo/round-20/resume/post-review-anchors.json` (942 line matches, 0 misses).
- Four SCORECARD narrative lines restored; empty capability placeholder was
  current state, intentionally replaced. Source errata appended for S007
  quote representation and S008's unsupported 1.35 label.
- C2 coverage explicitly bounded (aliases, split calls, child-process writes
  unchecked). Expansion basis corrected: registry capability + crawl-scope
  frontier entry; other three entries supersede covered ground.
- `TZ=UTC bash <fleet-census>/scripts/sources-census.sh validate
  <kake-worktree>`: `kake-shokunin ok`, exit 0. No push.

- 2026-10-17 — README: Devin wiki link. Operator directive (2026-10-17):
  insert the Devin wiki link into the README header of every repository
  with a generated wiki. `README.md` created (lane-header convention) with a `**Wiki:**` link to
  https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/kake-shokunin?branch=master.
  Evidence: the org's Devin wiki index lists this repo's generated wiki;
  sibling lane READMEs carry the same `**Wiki:**` header.
  Documentation-only change; no round run, no axis moved.

## Round 21 — historical publishing evidence made discoverable (2026-10-20)

- Motivation: SCORECARD's round-21 planned claims; baseline
  `5009ecaa1cce10b895617a585ddd3f7c7c923a84`; canonical CORPUS contract S019.
  The recorded initial census is `.ufo/waves/round-21/initial.json`:
  four complete provenance trios among twenty-one knowledge entries and
  one exact Gate among fifteen baseline lane-authored lessons.
- C1 freshness: seventeen pure four-line metadata prefixes expose original
  evidence dates, entry-local source provenance and safe recheck/restore-or-
  retire requirements. No old domain observation is promoted to current.
- C2 operability: fourteen EOF Gate reconstructions plus the new round-21
  Gate expose historical candidate decisions without inventing missing
  admissions/rejections or independent review. The lane-local
  `scripts/corpus-contract.mjs` makes missing sections fail visibly.
- Proof/evidence tooling: `.ufo/waves/round-21/measure.mjs`,
  `anchor-census.mjs`, `replay-proof.mjs`, frozen before inputs/digests and
  the validated single 64-seat wave. Registry home: SKILL.md's appended
  Publishing-corpus contract gate; no existing freshness pins are weakened.
- Operator wrap-up arrived after wave 1 dispatch; no further workers were
  dispatched. Planned wave 2 is skipped by that directive. L1 holds planner;
  seats are author-side, not independent closure reviewers.
- Source registry: S019 is new scoped own-work evidence; no old row's
  status/recheck/used-by changes. Census-start output is committed in
  `.ufo/waves/round-21/census-before.txt`.
- Previous outside review is carried forward via
  `corpus/lessons/round-20-verifier-spotcheck.md`: round 20 admitted with
  bounded citation/confinement assurance. Its older “still owed” statements
  are historical, not current. The round-21 lesson records reviewer findings,
  rejected draft metadata, known residuals and integration rulings.
- Domain-facing actions remain operator-owned. This work is local
  preparation/verification/handoff; no domain source push, publish, browser
  authentication or host package transaction is part of the round.

### Round-21 measured closure (same round)

- Measured commit `df6196b022a7fe9ac9a88af1293dc377a8197652` versus baseline
  `5009ecaa1cce10b895617a585ddd3f7c7c923a84`: exact independent counter
  trios 4/21→21/21; baseline lesson set Gate coverage 1/15→15/15
  (current total 16/16). `measure-before.json`/`measure-after.json` under
  `.ufo/waves/round-21/` record argv/stdout/stderr/exits 1→0.
- Corpus gate selftest 7/7 exit 0; frozen red-before replay PASS (36 inputs,
  two stable red runs, zero failures); current structural gate exit 0.
  Gate script SHA-256 and source revision are persisted in `gate-digest.json`.
- Existing offline paths gate stays exit 1: three drift targets, four old
  unannotated locations, newMissing 0, missSet 55. No new miss was pinned.
  Broad anchor audit preserves every prior byte (zero violations); its
  78 baseline-inapplicable author-report diagnostics remain visible, exit 1.
  The helper's stdout-flush defect was repaired after its first incomplete
  JSON receipt; no gate implementation or historical corpus byte changed.
- Source census exit 0→0, rows 18→19 (A16→17/C2→2,
  mined14→15/queued2→2/rejected2→2); complete counts/commands in source-rows
  receipts. S019 adds no publishing-domain coverage or new capability credit.
- Mandatory fleet misroot sweep found four owned seat reports; each copied
  into the lane, cmp verified, then its fleet copy removed. Full receipt:
  `.ufo/waves/round-21/misroot-sweep.json`. All sixty-four reports now local.
- Per-axis: freshness improved-bounded HOLD 10; operability improved-bounded
  HOLD 10. Trends: expansion unchanged, quality improved (bounded evidence),
  discernment unchanged pending independent orchestrator-dispatched review.
  Wave 2 was skipped by operator wrap-up; no new worker followed that order.
- Tool installs/updates: none. New L0 questions: none; inherited operator
  restore-or-retire decisions and independent closure remain open. No domain
  source tree was edited, committed, pushed or published.

## Round 22 — static canonical publishing preflight (2026-10-20)

- Motivation: SCORECARD's post-round21 capability/frontier plan and
  `corpus/lessons/round-21-verifier-spotcheck.md`: the old corpus maintenance
  claims were admitted but did not add publishing capability. Saturation
  nudge permits a new capability after round21's one-round stagnation window.
- Frozen C1: operability, offline publisher-policy comparison of canonical
  declarations over a named static-file population. Contract/case names were
  frozen before dispatch in `.ufo/waves/round-22/contract.json`; baseline
  master `7c61c8cc791bde36dd5e3688bdfea2678d90146c` has no canonical tool.
  Capability absence is not 32 observed wrong classifications.
- Sources: S020–S027 opened RFC 6596, Google guidance, WHATWG HTML and Python
  parser/URL docs. Exact short located quotes/access date are in round22's
  Gate. New knowledge entry `static-canonical-preflight.md` distinguishes
  documented platform semantics from stricter local publisher policy.
- One validated 64-seat build wave, L1-held planner, separate private clones
  for the three code writers, single L1 integration owner. Four scribe
  startup deaths remain dead/uncredited (`w1-deaths.json`); no replacement.
- Review learning: QUALITY now records reconstructed-Gate source ordering,
  canonical signal versus selection, and the rule that broad pointer-census
  diagnostics are not domain gate claims. Existing historical corpus bytes,
  protected verifier notes and the round21 correction register stay intact.
- Boundaries: no live property/auth/account/publishing/host-package/service
  operation; old paths gate reds, missing sources/history and SHONEN debt
  are not relabelled as new improvements. Final measurement and falsification
  receipts are recorded in the appended round22 measured entry.

## Round 22 — recovery attempt 2: falsification integrated and measured (2026-10-21)

- Motivation: attempt 1 ended without a report (`.ufo/watchdog.log`
  `lane-dead-no-report kake round=22`, 2026-10-21T02:47:17). Its wave-2
  reports (`.ufo/waves/round-22/w2/`, 43 of 64 seats; 21 dead, uncredited, not
  respawned) named a false clean for `///path` canonical/base references
  (Attack05), usage-output and repeated-`--manifest` gaps (BoundaryCLIErrors),
  manifest symlink scope (BoundarySymlinks), a counter that repeated its
  instrument's declared numerator and exited 0 on an unmeasurable baseline
  (FalsifyCounting), and aggregate-only replay plus dead-seat wording
  (FalsifyAdmissions). Eight residual seats (`.ufo/waves/round-22/residual/`)
  added lexical `..` path collapse and a self-consistent stub matrix.
- Landed `b539cc17c25e5f42fe8803e2aa42b4574c4b44c6`: validator, counter and
  replay fixes, failure-capable probes (`postfix/`), S028/S029, QUALITY
  "derived counts and resolver neighbours", knowledge-entry boundaries.
- Measured C1 at that commit: 0/32 → 32/32 (`measure-before-v2.json`,
  `measure-after-v2.json`). Correction to the round-22 entry above: its
  "appended round22 measured entry" is this entry; the receipts are those
  files plus `postfix/`, not attempt-1's `measure-after.json`.
- Unchanged debts: paths gate red (3 targets, missSet 55), anchor census not
  a gate, SHONEN unpromoted. No live property, account, publishing or host
  operation; no tool installs.


## Round 23 — live re-verification and canonical preflight (2026-10-21)

- Declared before dispatch: C1 freshness (17 frozen units: 16 historical knowledge entries + property map), C2 operability (12 frozen owned page URLs). Base `b5d599e`; freeze `6847479d404d1dd93ecb59f99ff735bd7f010a4a`. Counts and populations in `.ufo/waves/round-23/contract.json`. No live writes, accounts, publishing or domain-source edits.
- End-to-end domain task: ran `scripts/live_snapshot.py` GET-only against the 12 owned URLs, committed response metadata and the eight served HTML bodies, then audited/replayed them offline. Outcomes: 3 clean, 5 canonical_missing, 4 not-served (404). Charter, ds4cc primary and Plazir GHP are clean under the explicit local policy; ds4cc Kimi, burnerchrome, vault index, ufo-fsd pro and lucario GHP lack a canonical. Upstream repairs are documented, never applied.
- Live re-verification receipts cover 176 selected claims: 79 HOLD, 55 STALE with dated corrections, 42 UNVERIFIABLE with reasons; original knowledge bytes remain historical. A surviving burnerchrome source candidate was found at `~/Projects/burnerchrome`; its title/h1 match the served page, not a proved deploy binding.
- Routed corrections `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`: inverted QUALITY predicate corrected by named append; lane-root misroot copies moved under round-22 evidence; tmp runner reproduction recorded. `4d95d2e9…` introduced real-page parsing; `83098b5a…` integrated wave 1; `5e5afb9e…` fixed the counter selftest; `1b309c93fb0b2007ef15587100e7a1cdb9ef5573` integrates falsifier corrections, snapshot integrity and omitted C1 claims.
- Final counters measured at `5bef55b1464d7ccbff802edab400d138597a621c`: C1 0/17→17/17; C2 0/12→12/12 (`measure-{c1,c2}-{before,after}-v2.json`, same final runner both sides, two identical runs). Same-byte diagnostic: evaluator 4/8→8/8 at `1b309c93…` (`evaluability.json`, validator unchanged by the later metadata fix). New capability row in SCORECARD.
- Failure-capable evidence: snapshot probe 2/11→11/11; relaxation probe 3/13→13/13; canonical selftest 82/82 (`postfix/stable-smoke.txt`), counter selftest 28/28 (`postfix/counter-selftest-final.json`). Final suite: corpus contract exit 0, frozen matrix32/32; paths red old3 unchanged, expanded missSet69 with14 new explicitly absent targets and old pin55 unchanged (`final-suite.json`).
- Sources S030/S031 opened (WHATWG void syntax/foreign parsing); S021/S023–S026 re-opened without row changes. Source digest/locator and unquoted-attribute caveat corrected after falsification. Meta-refresh readiness is explicitly outside the canonical-policy claim.
- No packages/global tools installed by L1. One seat used official npm/npx Eleventy3.1.2 for an actual two-page generator probe (clean), no pacman. Full seat inventory and failures are in the round-23 evidence.
- Residual `FixSnapshotReview` exposed altered finalUrl metadata and JSON-array input; `5bef55b1…` checks redirect-chain consistency and metadata shape, with failure-capable regressions. No change to captured bytes or policy outcomes.

### Round-23 same-claim replacement coordinator — KakeR23 (2026-10-21)

- Inherited the pushed implementation through
  `5bef55b1464d7ccbff802edab400d138597a621c` and unlanded final bookkeeping,
  wave-2 reports and measurement artifacts; reused them after the bounded
  recovery checks below, without repeating round 22 or either swarm wave.
- Re-executed both frozen-revision counters: C1 0/17→17/17 (exits 1→0),
  C2 0/12→12/12 (exits 1→0), with the same final runner on each side.
  `.ufo/waves/round-23/recovery-counts.json` retains full command outputs.
- One final recovery run of canonical/counter selftests, snapshot/relaxation
  probes, corpus-contract and the old canonical matrix exited 0 for each
  command; `.ufo/waves/round-23/recovery-verification.json`. No new live page
  capture occurred; original dates and received bytes remain unchanged.
- Reopened S030/S031 primary pages and ran the source census, exit 0.
  `.ufo/waves/round-23/recovery-source-counts.json` derives 29→31 source rows
  from the base and measured commit. No old mutable registry cell changed.
  `.ufo/waves/round-23/recovery-frontier.json` records a fleet-root sweep with
  no owned misroot files. Driver state and operator scripts were untouched.
- The six inherited residual seats plus three read-only recovery audits are
  author-side, never independent admission. Dead-seat coverage remains
  explicitly incomplete; no replacement was dispatched. No source tree,
  publishing account or host package/service was modified by this recovery.

- RecoveryDocsAudit corrections: the earlier phrase "frozen matrix32/32"
  means the current-validator 32-case matrix run, not a successful historical
  digest-pinned replay; that separate replay stays pinned to `b539cc1`.
  Its append-only finding also restores the original committed round-23
  Gate lines and supersedes their source/count errors with an EOF register.
- RecoveryDocsAudit identified a remaining contentType field-shape crash.
  Two executor dispatches were refused by the host cap, spawning zero seats;
  the parent explicitly directed a bounded coordinator implementation.
  Added the non-string/non-null contentType check and one targeted loopback
  regression. Same probe: 11/12, exit 1 → 12/12, exit 0; malformed field
  now returns the named JSON input error, exit 2, rather than exit 1.
  Evidence: `.ufo/waves/round-23/snapshot-field-{before,after}.json`.
  No broad malformed-metadata or network-authentication claim is added.

- Committed recovery re-measured at
  `dd58390d3a0b2942ffdd8f0330c0da3dda7b87e1`: C1 17/17 exit 0,
  C2 12/12 exit 0 (`.ufo/waves/round-23/recovery-final-counts.json`).
  The fixed snapshot producer does not alter received page bytes, the
  canonical validator, the claim populations or expected canonical policy.


## Round 24 — paths reconciliation and receipt replay (2026-10-21)

- Declared two causally separable claims on tied-lowest owned axes: C1 freshness (19 flagged path targets), C2 operability (malformed receipt rejection). Contract and preservation amendment: `.ufo/waves/round-24/{contract,contract-amendment}.json`.
- Motivating evidence: round-23 non-author closure MANIFEST rounds[394] routed the lexical observedAt and contentType counter gaps plus retained paths debt. Round-open `paths-before.json` also caught the restored ds4cc checkout before repair: drift3/newMissing12/recovered4; no domain tree was changed by this lane.
- Frozen-population landing ab85dbdba4499f35f7dab9c9635b9b605679dbe5; actual before measurements: C1 0/19, sweep exit1; C2 81/130 (61/110 rejection expectations,20/20 acceptance controls), exit1. Exact argv/stdout/stderr: `measure-c1-before.json`, `measure-c2-before.json`.
- C1 implementation retains every original corpus line; 30 correction-sidecar records plus EOF blocks replace the rejected suffix plan. Twelve observed misses enter the pin and four recovered tokens leave it (55→63). Nineteen dated target receipts include four direct coordinator observations after provider deaths. Source observations, not re-pinning alone, justify the changes.
- Source rows S032–S034 were opened this round and ground the C2 grammar choices; lesson Gate has URLs, dates and short located quotes. The remaining outside admit/reject spot-check is not self-granted.
- Wave1: 72 validated seats, L1-held planner; solutionSpace was the only host-required addition to rendered tasks. Provider deaths stay uncredited; recovered scratch code is reviewed/integrated by the coordinator, never represented as a completed seat.

- Independently landed C1 at 3d07733b482f88c42cb008397188237c80e42b67: accepted19/19, sweep exit0; same C2 matrix remains81/130 on that C1-only revision. Receipts: `measure-c1-c1-only.json`, `measure-c2-c1-only.json`.
- C2's executor died with provider429; recovered its uncommitted clone script as candidate code, then coordinator integrated the null-header, 204-body, UTC-bound and safe-URL corrections. `scripts/receipt_replay.py` is the maintained successor; original round23 counters/receipts and populations remain untouched. Source-backed knowledge, QUALITY criteria and SKILL gate registry are updated. Its 130-case after result is recorded only after execution against the landed revision.

### Round-24 replacement recovery — policy-stop disposition

- Original coordinator KakeR24 had already pushed C1
  `3d07733b482f88c42cb008397188237c80e42b67` and C2
  `faace82dcf50e1c563d437f2caecb77a9a865880`. Its after measurements were
  C1 19/19 exit0 and C2 130/130 exit0, with pristine replay controls17/17
  and12/12. Those executions predate its provider `cyber_policy` error;
  `.ufo/waves/round-24/implementation-suite.json` retains exact outputs.
- Same round24 attempt1 replacement KakeR24R audited measurement receipts,
  frozen population/counter digests and commit timestamps; no refused probe
  or interrupted falsify assignment was rerun, rephrased, rerouted or replaced.
  `.ufo/waves/round-24/recovery/provenance-audit.json` distinguishes
  documentary review from new execution.
- Reconciled original wave outcomes:72 build seats,55 reports/17 deaths;
  64 falsify seats,0 completed reports (62 aborted,1 connector429,1
  interruption without final). Two new documentary recovery audits are
  author-side, not replacement falsifiers; total138. Exact seat errors:
  `recovery/interruption-inventory.json` under round24 wave evidence.
- Source registry31→34, A29→32; original31 rows unchanged. Source census
  exit0→0, with W04 duplicated RFC9110 URL across distinct scopes disclosed.
  `recovery/source-census.json` records the command, output and histograms.
  Added the missing bounded source search-log note without altering rows.
- Appended SCORECARD/lesson recovery records, preserving earlier bytes.
  C1/C2 local measured improvements are not full-round admission:
  unfinished falsification, outside admit/reject review and independent
  no-harm remain debt. L0 question begins “Policy-stop disposition”.
  No SHONEN promotion, new round, account/publication/domain-source action,
  host package install or global configuration change occurred in recovery.
- Documentary audits `recovery/{docs-audit,evidence-audit}.md` confirm
  measurement units and disclose retained shape-only selftest-path output
  as a conformance defect (not silently rewritten). Contract count strings
  are shorthand; receipt argv is exact. Original tool-event timestamps
  12:18:27.711Z–12:19:08.152Z confirm both after counters completed before
  the12:22:15.004Z policy error; see provenance-audit.json.
- Tool-install disclosure for the original build: SourcePythonDatetime
  installed CPython3.10.22 and3.15.0 via uv0.13.0's managed interpreter
  channel (`uv python install 3.10 3.15`) to compare pre-3.11/current-doc
  datetime behavior. Recovery installed nothing; no pacman/system upgrade.

## Round 25 — publisher accessibility preparation (2026-10-21)

- Declared C1 operability capability in `.ufo/waves/round-25/contract.json`:
  a fixed WCAG 2.2 A/AA manual-review packet and offline structural inventory.
  Both owned axes tie at legacy10; no scalar increase is asserted. Baseline
  branch tip was `6883f1d580d811f7c434d1db4642596362f822b1`.
- Opened W3C's pinned 12 December2024 Recommendation, source S035.
  The first read adapter returned abstract/metadata only; raw official HTML
  supplied normative source, retained as source-wcag22.html with digest.
  Source population and source-backed knowledge entry advance preparation
  ground from the existing WCAG frontier, not website conformance.
- Built a validated64-seat wave:55 criterion scouts,3 executors,2 connectors,
  1 scribe,1 reviewer,2 critics. L1 holds the frozen planner seat. Separate
  sandbox checkouts isolate implementation; read-only seats own only reports.
  PacketTool died on Codex capacity (`turn_rate_limit_exceeded`, five retries);
  no replacement. L1 authored the residual validator. Specs, registry and
  dispatched payload are in `.ufo/waves/round-25/`.
- Assembled the55 criterion-specific cards into
  `corpus/knowledge/accessibility-review-cards.json`. Every status remains
  not-assessed. `scripts/accessibility_packet.py` validates packet structure,
  never a website. Execution measurements are recorded only after running.
- Updated SKILL registry, province boundary, corpus index and QUALITY with
  complete-source-read and no-conformance-overclaim rules grounded in
  `corpus/lessons/round-25.md`; original corpus bytes remain untouched.
- Round24 C1/C2 remain unadmitted candidate debt. No refused/interrupted
  assignment, probe or counter is repeated, rephrased, rerouted or replaced.
  The existing L0 policy-stop question is retained and restated for round25;
  this unrelated packet neither resolves it nor grants old-round credit.

### Round-25 author-side falsification integration

- Candidate landed `9f62cda0a6b71a9c0c86d2088f01673f25787715`.
  Fresh W2 concluded64 seats:56 completed and8 capacity deaths, no
  replacements; terminal errors and report digests are in w2-outcomes.json.
  L1 completed the eight uncovered card reviews, not new seat identities.
- Integrated source-semantic findings and common detached-card
  authorization/record boundaries; the exact before/after fields and a
  rejected false quote-count finding are in card-corrections.json.
  All55 identities and not-assessed statuses are retained. The corrected
  frozen-final snapshot is new; original frozen/ bytes remain intact.
- Fixed packet JSON/CLI and counter boundaries found by ReviewTool,
  ReviewCounter and ReviewSelftest: strict parsing, JSON usage/help output,
  duplicate-option rejection, no fixture fallback for a present-tool
  candidate, typed Git/tool disagreement, complete heading/status fixtures,
  and exact reviewed-card pinning. Tests/proofs are implemented here;
  observed execution is recorded only after the coordinator suite.
- Delivered `corpus/handoffs/accessibility-preparation.md` to the property
  operator as preparation, with named tabi/kagi boundaries, no target
  evaluation or publishing authority. Updated the knowledge entry, registry,
  QUALITY and source-study path without rewriting historical corpus lines.
- W1/W2 report findings are author-side. Old round24 remains held; no old
  interrupted probe/counter was executed, no model/provider policy was
  bypassed, no seat replaced, and no system/tool install performed.

### Round-25 coordinator suite correction

- Source landed `6cb08a40d72d657628f9a0334417901cdc97c732`.
  `verification/suite.json` records the initial executed suite and its two
  failures: focused35/36 and counter8/9 on the2000-level JSON assumption.
  Python3.14.8 parsed that input rather than throwing RecursionError;
  the observed shape-failure exit1 is preserved, not called a crash.
- Added an explicit local64-level bound with boundary/string controls in
  both new parsers and corrected the pin-only proof's preserved-card control.
  The source profile and lesson explain the change; old evidence is not
  overwritten. Targeted postfix verification follows on a pushed revision.

### Round-25 measured closure

- Source pushed `be362b7808ea2350a4340cfa2cfde481269037f4`; the identical
  revision-bound measure command observes baseline6883f1d0/55 exit1 →
  source55/55 exit0. Exact receipts are in
  `.ufo/waves/round-25/postfix-verification/{measure-before,measure-after}.json`.
- Targeted postfix checks pass: unit16/16, focused39/39, counter11/11;
  corrected frozen replay clean, tamper exit2, quote/pin repair oracle
  red-before1→green-after0, three regression changes caught by strengthened
  fixtures. Initial failed checks remain under verification/, not erased.
- Recorded the working preparation capability in SCORECARD (round25,
  operability10→10 HOLD). Concrete source S035, cards and operator handoff
  establish preparation only; no website or account is evaluated/published.
- Source census exit0→0 with inherited W04; source rows34→35, old34 rows
  unchanged, newA/mined S035. Five located Gate quotes and source bytes
  rechecked; static preservation/old-code/knowledge checks are clean.
  No old policy-interrupted command is executed.
- Both validated waves64+64=128 conclude; dead1+8=9 remain uncredited,
  no replacements. Retained reports120 include the late uncredited W1
  PacketTool artifact; credited completions119. L1 supplies residual work,
  not new seat identities. Root misroot sweep found no untracked file;
  only driver-owned tracked changes were present and left untouched.
- Learning: expansion improved, quality improved boundedly, discernment
  unchanged pending non-author closure; no SHONEN promotion/round-credit
  assertion. Policy-stop L0 remains open for round24, with no provider or
  routing bypass. No installation or host/global-config change this round.

Measurement notation: the exact baseline is
`6883f1d580d811f7c434d1db4642596362f822b1`, with accepted0/55.
The compact baseline6883f1d0/55 wording above is not a different commit.

## Round 26 — source recheck (2026-10-21)

- Declared C1 freshness (`.ufo/waves/round-26/contract.json`): re-verify the
  32 previously opened external SOURCES rows. Motivation: MANIFEST
  rounds[420] recorded quality unchanged in round 25 because no prior entry
  was re-verified. Base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
- Re-fetched 34 recorded URLs once each (S008 retried once after a timeout;
  inline command preserved as `fetch_retry.py`), retained gzip bytes and
  sha256. Census start exit 0 with inherited W04 (`census-before.txt`).
- W1: validated 64 seats (32 row scouts, 25 pair reviewers, 1 SKILL/README
  reviewer, 2 executors, 2 critics, 1 connector, 1 scribe) after five
  job-cap refusals (`w1-dispatch-attempts.json`); no deaths. One report was
  misrooted at the fleet root and moved byte-exact (`misroot-RowS012.txt`).
- Row receipts: 32/32 HOLD. Statement reviews: 276 statements, 22 proposed
  STALE, 8 admitted and appended as `[r26-recheck S0NN STALE]` blocks in
  ghp-served-set, ghp-etag-anatomy and static-canonical-preflight; 14
  rejected with reasons (`statements.json`). Dated HOLD sections appended to
  all five citing entries. No SOURCES row cell changed.
- Critics drove counter rules (row-specific quotes, statement ledger) and an
  extractor fix (double entity decode; before copy retained). QUALITY,
  README, SKILL registry and SCORECARD appended. Measurements follow
  execution on a pushed revision.

### Round-26 resume and falsify-wave integration (2026-10-21)

- Replacement L1 KakeR26-2 reconstructed the dead KakeR25 session from durable
  transcript/seat files (`.ufo/waves/round-26/resume-evidence.json`). W1
  reported 64/64; W2 never spawned before death, so its validated payload was
  dispatched unchanged (64 seats, `w2-spawn-result.json`). No dead-seat item
  was replaced. One attempted residual executor dispatch was refused by the
  background-job cap (spawned nothing); L1 did the integration.
- Falsify findings: 37 more row-statement units judged, 4 prior STALE tags
  reclassified as precision notes, S001 attribution and two S024 scope errors
  appended; ledger now 313 units, 7 new STALE corrections, 4 reclassified
  tags, 6 UNVERIFIABLE units. Earlier 8/8 figures are the pre-W2 candidate,
  not final. S021 fragment wording is STALE already corrected in r23, not a
  rejected finding (`statements.json`).
- Fetch notation correction: 34 recorded row/index fetch slots, 33 distinct
  URLs (S028/S033 share one), plus S008 retry = 35 attempts. Initial window
  15:09-15:10 UTC; retry at 15:11 UTC. 32 row verdicts remain HOLD.
- Counter and extractor selftests strengthened; 24 counter cases, 74 text
  cases; 12/12 counter mutants killed plus the surviving HTML-sniff mutant
  killed. Evidence: `verification/counter-mutation-replay.json`,
  `verification/extractor-sniff-mutant.json`. Locator prose errata and
  scratch-bound deviations retained in the lesson, not hidden.
- The old `adjudicatedBy: KakeR25` was accurate for W1; the ledger now names
  both coordinators and dates the new adjudication. No tools installed.

- W2 UncoveredLessonCites additionally found the stale S024/S025 `used-by`
  cells: lesson-only → knowledge-entry plus lesson (old→new in round-26
  lesson). Cells repaired under SOURCES v1; no row/status/recheck change.

### Round-26 measured outcome (2026-10-21)

- Measured source revision `b44daedc9658d86374f1c3e3cdfc3a6951d0bdf6` (landed implementation):
  baseline `97404de4ff73d6c8a4f87385cf5fdf36dca7f006` 0/32 exit 1 → 32/32 HOLD exit 0,
  ledger 313 units / 7 STALE corrections / 4 reclassified tags; no findings.
  Command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.
  Full captures: `verification/measure-before-final-counter.json`, `measure-final.json`.
- Sandboxed gates at the landed implementation: counter selftest 24/24 exit 0;
  extractor selftest 74/74 exit 0; corpus contract exit 0, 0 findings;
  offline freshness sweep exit 0. Red-before extractor has 22 failures
  against the old extractor; green-after has none. Initial red-before
  scratch-layout error was repaired before the retained failure witness.
- End census exit 0 with the inherited W04 S033 duplicate URL warning;
  35→35 rows (A33/C2; mined31/queued2/rejected2), added by tier 0/0/0.
  Only S024/S025 used-by cells changed as logged. Preservation check at
  `verification/no-harm-final.json`: every original knowledge-file byte
  remains a prefix; no existing domain source or gate behaviour changed.

- W2 complete: 64/64 reports, zero dead seats (w2-outcomes.json); round total
  128 seats (64 inherited W1 + 64 newly dispatched W2). L1 holds planner.
  W1 had only two executor seats, below the prompt's three-executor role
  minimum; this inherited conformance deficit is reported, not padded.
- Final scratch disclosure additionally includes S032's transient /tmp file
  (self-reported deleted). No seat/provider death and no tool install reported.


## Round27 — frozen independent claims and oracles

Repair-first motivation: corpus/lessons/round-26-verifier-spotcheck.md:9–13,117–123; r26 C1 was rejected, not completed by the green32 counter. Base83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba. C1 freshness: full inherited32-row citing-set adjudication41/57→all57 minimum; historical metadata/EOF prose included, discoveries monotonically add obligations. C2 operability capability: frozen-r26 missing-pair detection0/16→16/16, independent of C1 additions. Contract, counting commands, baseline outputs and expected16 pairs in .ufo/waves/round-27/ committed before implementation. Legacy ratings10/10 held. No other active kake source writer at proc census; lane clean; r24 stopped work untouched.

### Round27 — counting implementation corrections, targets unchanged

W1 CritIndependence/CritDenominator/CritClaimFit supplied consumer-input failures: shrinking citations erased obligations, inherited-ledger laundering passed, self-artifact evidence passed, UNVERIFIABLE overrides retained old credit, mutable frozen expectations could bless edits. The stricter counting implementation is committed before candidate measurement; original code remains at be375d90afc6fc7aca369ab3cf5247bf460aeed2. Exact hashes/diff and reasons: `.ufo/waves/round-27/oracle-implementation-corrections.json` and `oracle-implementation-diff.patch`. No original target, original16 missing-pair oracle, frozen input byte or r26 filed record is rewritten. New selftests consume real disposable Git clones, not stub-gate echoes. Positive results remain unasserted until executed. A conservative embedded evidence-file discovery grows C1's knowledge-file obligation57→58; it is an artifact-reference review, not S013 teaching served-set semantics.

### Round27 — source adjudication and consumer gate implementation

The original missing16 knowledge-file pairs now have explicit source/artifact
judgments in `.ufo/waves/round-27/pairs.json`, plus one conservatively included
embedded report reference and one override for a newly found numbered-step
attribution. This is18 new review records, not a rewrite of r26's313 units.
Three STALE attribution corrections are appended in preflight, sitemap metadata
and served-set; source-specific holds, rejected alternate interpretations and
historical dates remain explicit. Motivation: the r26 non-author rejection and
W1 Pair03/07/08/06B findings. Source row routing changes S001–S006 are logged
old→new in `corpus/lessons/round-27.md`; immutable row cells are preserved.

Three isolated executor worktrees supplied `scripts/citing_set.py`,
`scripts/citing_set_selftest.py` and29 independent fixture cases. L1 integrated
only their assigned files. The new gate is registered in SKILL.md; its
presence-only input `complete-ledger.json` does not claim semantic truth.
QUALITY.md and the corpus index record the grouped-citation lesson and r26's
rejected status. Broader outside-knowledge corpus policy and excluded-source
populations are disclosed, not silently retired. No claim of successful
measurement or new capability credit precedes the actual consumer-visible
baseline/after runs and fresh falsification evidence.

### Round27 — strict supported verdict is not review existence

The frozen C1 after-clause (contract.json:10/13) requires HOLD or supported
STALE and explicitly never counts UNVERIFIABLE decided. Main relayed an
independent prospective-controls lead; direct author inspection of the actual
contract and r26 pair reports confirms that the41 baseline are review records,
including two partially UNVERIFIABLE pairs. The counting implementation now
separates reviewedPairs from strictly decided and returns non-clean for those
unresolved units. Original41/57 baseline bytes, target, denominator and r26
records are preserved; no review-complete green substitutes for the frozen bar.
Details: `.ufo/waves/round-27/strict-c1-disposition.json`.

Six inherited units remain explicit (S001/ghp-served-set3 and S033/canonical
entry3). C1 is unprovable if these remain unresolved; no r24 stopped
probe/counter/target is retried to force a pass. The grouped-source repair and
independent presence-only C2 capability continue; neither is relabelled full
strict C1 completion. Arithmetic before execution is labelled inference in
the disposition; real outputs are retained after runs.

### Round27 — retention boundary and Git-mode regression

A shape-only scan of the new uncommitted HTML observed two authenticity-form
input shapes, never their values. Before committing captures, one bounded
residual executor implemented public-visible-text HTML retention with separate
received/retained digests and an offline migration. L1 ran that migration:
exit0,8 records, eight own old filenames removed, no network helper loaded
(`retention-shape-before.json`, `retention-migration.json`). This is data
minimization, not an account-validity/security-incident inference or history
purge; r26 filed bytes are untouched and HTML attributes/bytes not retained
remain unproved. Actual selftests and independent checks are still required.

L1 corrected a pre-integration manifest-path join in the delivered oracle
selftest and made the retention note conditional for byte-preserved code.
The source-opener/selftest remain real implementations, not stub output.
Separately, static review found Git ls-tree text quoting unsafe for regular
special-character filenames; L1 switched the new gate to NUL framing.
The existing BuildGate identity authored a real isolated Git/working-tree
identity regression without executing it. Source/report:
`git_name_selftest.py`, `residual/GitNameRegression.md`; old prototype retained
only as the explicit red-before input. No new identity or role replacement
was counted for this same-identity resumption.

### Round27 full-barrier corrections (original measurements preserved)

All67 build identities completed with67 nonempty reports; no death/replacement.
The final CarryLedger receipt identifies a lost S007 historical-Markdown
uncertainty in its original r26 report. This supersedes the prior **known**
six-unit/two-pair description: the immutable ledger fields still sum6, but
known uncertainty is7 units across3 pairs. New hash-pinned `carry-errata.json`
records the missing unit; no r26 byte or original57/16 oracle is rewritten.
Strict C1 remains unprovable; revised arithmetic before execution is38/57
strictly decided at base and55/58 at candidate, alongside41/57→58/58 reviews.

The same audit reconciles raw sum(statements)=313 against318 report-attributed
units and310 decided units inside that raw sum; one additional S025 HOLD unit
was omitted by the ledger. These are accounting conventions, not a new semantic
denominator. The original313 sum stays true and preserved, not relabelled.

CarryLedger's reported pre-fix gate57-findings/23-of29 failures are accepted
as before evidence, not rerun to confirm. L1 corrected the actual row-key
versus pair-membership comparison. Author after-runs and the fresh85 payload
will grade the fixed candidate; no pre-fix failure is laundered PASS.
The Git-name before variant has that independent pair fix applied so its
controlled before/after differs only in NUL-framed path enumeration.

### Round27 final falsification and author closure

The one unchanged validated fresh85 payload actually spawned85 unique
identities on its first attempt after the200-seat grant; all85 completed
with85 reports. Round actual identities153=67build+1privacy+85falsify,
no death/replacement or terminal provider error observed. Same-identity
BuildGate resumptions are already among67. Event-derived handoff counts
were sent to Main, not inferred from report presence.

At measured ac46a7472d945a6d7ff135e4d7f07b0b6913d835: C1=58 reviewed/55
status-decided,7 unknown units/3 pairs, exit1. C2 finite16/16,0 false positives,
consumer58/58 presence, real gate29/29, Git-name30/30, C1 counter14/14,
C2 counter3/3, privacy9/9. Four source mutants were killed by real behavior.
The controlled Git-name before has10/30 failures; it is not a rerun to
confirm the reader's separate57/23 failure.

Cold readers also falsified full-interface/safety claims (false greens,
FIFO hangs, JSON protocol/identity/path failures and retention weaknesses).
Neither full claim is called verified or admitted. The scripts remain
unadmitted candidate evidence; the bounded numeric successes are not a
global native verdict. No code repair is claimed for those open failures.
Explicit current interpretation and debt: current-interpretation.json and
unresolved-acceptance.json. Source record wording/anchors are corrected in
a new commit without changing keys/verdicts, original oracles or r26 bytes.

Outside-scope policy debt stays explicit. No r24 stopped work/target was
retried, no next round/state/admission/promotion was dispatched by this L1.
Main owns independent closure; the author ends this round honestly stopped.

### Round27 — independent non-author closure (hyaku)

Parent (Main), on three independent advisories, closed round 27 rejected-honest-stop /
admitted false — C1 freshness and C2 operability both unprovable, other axes unchanged,
no-harm bounded to measured surfaces, expansion unchanged, no scalar grant. Pins: base
`83528f7c…` prior closed negative base (r26 was rejected too); declarations `be375d90…`
pre-implementation targets/oracles; candidate `ac46a74…` measured pin with the bounded
after-receipts; `cd2e95b…` final C1 measurement revision; head `62aeddf…` final lane head.
Review was canonical read-only; Parent publication is the new verifier note plus append-only
LOG/index entries, prior records untouched. The 153/0-dead/0-replacement census comes
from recorded registries/outcomes; the three Root advisories are separate late seats, not
pre-wave ids. No candidate gate/counter/fixture re-executed, no cleanup, no r24 retry,
no dispatch claimed; detail: `corpus/lessons/round-27-verifier-spotcheck.md`.

### Round 28 — attempt 3 (hyaku, in-session L1 KakeR28a3)

Claims declared at `84ea5b1` before implementation and kept unchanged:
C1 (operability, repair-first) repairs round-27 routed defect 1 in
`scripts/citing_set.py`; C2 (freshness, frontier) adds field-performance
knowledge from four Google documentation pages opened this round.

- Inherited from attempt 2 and re-verified: repair commit `b5d423f` (C1
  counter re-run 15/15, same per-case vector as the attempt-2 receipt; base
  `22c1669` re-run 4/15), source snapshots S036–S039 (all 16 receipt quotes
  found again on a fresh GET at 09:29Z), the 38-seat wave spec (re-rendered
  as `w1a3-spec.json` with attempt-3 names and scratch paths). The refused
  attempt-2 dispatch record and its spec are kept as evidence.
- Wave 1 (`w1a3`, 38 seats, v1 policy): 11 scribes, 8 reviewers, 8
  mutation-testers, 4 critics, 4 executors, 2 connectors, 1 scout; 0 dead.
  All 7 C1 revert mutants and both constant gates were killed by the counter.
  Falsifiers found an over-refusal in `b5d423f` (bare repositories,
  trailing-space roots) and several adjacent gaps.
- Residual call (8 seats: 5 reviewers, 3 critics; 0 dead) attacked the C2
  entry, rows, Gate quotes, counters, criteria and no-harm scope.
- Landed: `e57f601` (C2 entry, S036–S039 rows, lesson, QUALITY criteria,
  README, SKILL table, PROVINCE pointer); C1 follow-ups `8ecbefe`
  (top-level check by `--show-prefix`), `5a83d13` (inherited Git variables
  ignored), `e73d48b` (MemoryError and corpus-path reason labels); then the
  review corrections to the entry, lesson, QUALITY section and S037 anchor,
  this LOG entry, the SCORECARD record and the wave evidence.
- Motivating evidence: `corpus/lessons/round-27-verifier-spotcheck.md`
  routed defects; `PROVINCE.md` Frontier listed field performance as open
  ground; `corpus/SOURCES.md` had only a rejected S018 row on it.
- Measurements: C1 4/15 at `22c1669` → 15/15 at `b5d423f`, `8ecbefe`,
  `5a83d13` and `e73d48b`; C2 0/4 at `b5d423f` → 4/4 at `e57f601` and at
  the final lane commit (see SCORECARD "Round 28 — measured results").
- Open, not repaired: see `corpus/lessons/round-28.md` "Open findings".
- No misroot: no kake round-28 seat file landed at the fleet root.

### Round 29 — attempt 1 (hyaku, in-session L1 KakeR29)

Claims declared at `d18bbf3` before implementation, with notes at `9e541a1`
before any after-measurement: C1 (freshness, frontier) adds project-site
base-path knowledge from four primary pages opened this round; C2
(operability, capability) adds an offline base-path audit with a frozen
30-case matrix. The citing-set gate worked in rounds 27 and 28 was left alone
(session drift sentinel); its routed defects 1 and 2 are carried as named debt.

- Motivating evidence: `PROVINCE.md` Frontier listed "Jekyll/base-path build
  tooling" as open; `corpus/` had no `baseurl` or `relative_url` statement
  (wave-1 `ScoutPriorSubpathKnowledge`); round-28 routed defects 3 and 4
  (counters checked ids and quote shape; the source gate rejected nothing).
- Wave 1 (`w1`, 32 seats, v1 policy): 11 scribes, 5 critics, 5 reviewers, 4
  scouts, 3 executors, 2 connectors, 2 mutation-testers; 0 dead.
- Wave 2 (`w2`, 39 seats, v1 policy): 18 reviewers, 15 critics, 4
  mutation-testers, 1 sentinel, 1 scout; 0 dead. Round total 71 seats.
- Landed: `d18bbf3` declaration and counters; `e58b66c` source openings;
  `9e541a1` declaration notes; `f8675e5` entry, S040–S048 rows, lesson gate;
  `98dbab2` tool, selftest, fixtures, real-input run; `7697990` SKILL,
  README, PROVINCE, QUALITY, lesson mistakes, wave-1 evidence; `d8cd2e4`
  wave-2 repairs and evidence; then this LOG entry and the SCORECARD record.
- Measurements: C1 0/4 at `fe1805cf` → 4/4 at `f8675e5`, `98dbab2`,
  `7697990`, `d8cd2e4`; C2 0/30 → 30/30 at `98dbab2`, `7697990`,
  `d8cd2e4` with all constant gates rejected. Census exit 0 before and
  after (only the pre-existing W04 warning); registry rows 39 → 48.
- Also fixed: `.gitignore` now ignores `__pycache__/` and `*.pyc`, and the
  untracked round-26 bytecode directory was removed (round-28 routed defect 5).
- Misroot: one wave-2 seat wrote a report copy at the fleet root and removed
  it itself; the L1 sweep before the report found no round-29 kake file
  there (`corpus/lessons/round-29.md` Mistakes).

### Round 30 — attempt 1 (hyaku, in-session L1 KakeR30)

Claims declared at `4580c78` before implementation, with notes and a strict
C1 supplement at `04637bd` before any after-measurement: C1 (operability,
repair) makes the citing-set runner compare reason codes with committed
fixtures and repairs the round-27 families round 28 routed; C2 (freshness,
frontier, learning claim) adds Render static-site knowledge from four Render
Docs pages opened this round (S049–S052).

- Motivating evidence: round-29 spot-check routed defects 1–5
  (`corpus/lessons/round-29-verifier-spotcheck.md:230-248`); `PROVINCE.md`
  Frontier listed Render deploy semantics as open.
- Wave 1 (`w1`, 34 seats, v1): 10 scribes, 8 reviewers, 5 critics, 4 scouts,
  3 executors, 3 mutation-testers, 1 connector; 0 dead.
- Wave 2 (`w2`, 34 seats, v1): 19 reviewers, 7 critics, 6 mutation-testers, 1
  sentinel, 1 scout; 15 returned, 19 cancelled by the L1 at wrap-up (run
  budget), 0 dead. Round total 68 seats.
- Landed: `4580c78`, `04637bd`, `71c6bfa` (C1), `451e98f` (C2 and evidence),
  `1c7773e` and `f80bd8f` (wave-2 repairs), then this record. Foreign commit
  in range: `636dddd` (operator daily reflection).
- Measurements: C1 0/14 → 14/14 (strict 0/6 → 6/6); C2 0/4 → 4/4. Census
  exit 0 before and after (only the pre-existing S033 W04 warning); registry
  rows 48 → 56.
- Base mutant ledger: 23 reason-code renames, 0 killed at `0356681`
  (`.ufo/waves/round-30/mutant-ledger/`).

### Round 31 — attempt 1 (hyaku, in-session L1 KakeR31)

Claims declared at `a16602a` before implementation, with a C2 strict
supplement at `b801ac8` before any C2 after-measurement: C1 (operability,
repair) makes the citing-set fixture runner refuse the five hostile fixture
shapes the round-30 closure routed (N1, N2, N3, N5, N6), each with a committed
hostile spec and selftest; C2 (freshness, frontier, learning claim) adds
Render web-service and Blueprint knowledge from four Render Docs pages opened
this round (S057–S060) and checks the lane's own `render.yaml` key by key.

- Motivating evidence: at base `f1ffb81` the C1 counter showed each routed
  gap doing harm (a planted script ran, two victim repositories gained
  commits, a FIFO hung the runner, a symlinked case vanished;
  `.ufo/waves/round-31/verification/c1-before-f1ffb81.json`). `PROVINCE.md`
  listed Render web services and the Blueprint file as open.
- Wave 1 (`kake-r31-w1`, 33 seats): 18 seats on the executor, scribe and
  mutation-tester roles died at spawn with "No model selected"
  (`.ufo/waves/round-31/w1/dead-seats.json`); one critic was refused by a
  provider cyber-content filter, and one returned after a safety filter
  switched its model (`w1/seat-status.json`). The L1 wrote the runner repair,
  the hostile selftest, the entry, rows, lesson and docs itself.
- C1 after: 5/5 with K1 holding at `c88b97e`
  (`verification/c1-after-c88b97e.json`); the hostile selftest exits 1
  against the base runner and 0 against the repaired one
  (`verification/hostile-selftest-*.json`).
- Round-30 routed defects: (1) C1; (2) open families carried by name in SKILL
  "Citing-set runner containment — round 31"; (3) and (4)
  `render-static-sites.md` "Round-31 corrections" and S061, with the S053 and
  S054 flips resolved (both stay rejected); (5) `.ufo/waves/round-30/w2/partial-reports.json`
  (15 complete, 5 partial); (6) the declared closure command names files and
  was shown to pass as written and able to fail
  (`verification/closure-command-check.txt`).

### Round 31 — attempt 2 (hyaku, in-session L1 KakeR31a2)

Attempt 1 died in an omp process restart at 17:26Z after landing `92235a0`.
Attempt 2 re-measured the inherited tip (C1 5/5 K1 holds, C2 4/4, strict
5/5; `verification/*-a2-at-92235a0.json`), committed the two inherited
untracked paths, and ran wave 2 (falsify) as `kake-r31-a2-w2`: 36 seats
(23 reviewer, 11 critic, 1 scout, 1 mutation-tester), dispatched 18:04Z.

- Motivating evidence for the repairs: a dot-named symlinked case was still
  skipped (`a2-w2/CriticSymlinkCases.md`); `--r` passed the allowlist and
  reached the gate (`CriticArgvAllowlist.md`); a ":" in the scratch path
  switched the Git ceiling off (`CriticGitPins.md`); a runner that refused
  cases by name passed the hostile selftest and the C1 counter
  (`ReviewHostileSelftestCode.md`); the entry marked a stated fact (PORT) as
  inference and contradicted S059 on secret files (`CriticLearningClaimAfter.md`,
  `CriticEntryInferences.md`).
- Landed at `9a7f5be`: runner and selftest repairs, P5 `.h5b`, appended
  corrections to the entry, SKILL, QUALITY, PROVINCE, README and SOURCES, four
  lesson Mistakes rows, census-mode receipts, fix receipts
  (`verification/a2-fixes/`). After: C1 5/5 K1 holds, hostile selftest exit 0
  (base runner exit 1), 45 fixtures clean, C2 4/4, strict 5/5
  (`verification/*-a2-at-9a7f5be.json`).
- Not repaired, named in SCORECARD "Round 31 — attempt 2 re-measure and
  wave-2 repairs": the frozen C1 counter trusts reported names; the strict
  C2 supplement passes hollow commits; mutant m3 survives.

### Round 32 (hyaku, in-session L1 KakeR32)

Two routed repairs from the round-31 closure
(`corpus/lessons/round-31-verifier-spotcheck.md`, "Routed defects" items 2 and 5),
declared at `5b32cc7` with both counters before any measurement.

- Motivating evidence, C1: round-31 `a2-w2/MutRunnerGuards.md` — m3 (drop the
  load-time "git_commit needs an earlier git_init" guard) survived the hostile
  selftest with exit 0; the apply-time re-check and Git pins still refused the
  shape, so only the refusal reason distinguished it. Before at `a0b0dff`:
  killed 0 (`verification/c1-before-a0b0dff.json`). Landed at `2f2f12d`:
  `reason_contains` spec key and P6; after: killed 1, guard_ok true
  (`verification/c1-after-2f2f12d.json`).
- Motivating evidence, C2: the round-31 closure said the entry's
  ds4cc-marketplace `render.yaml` facts rest on an external blob the lane does
  not retain (`d17ab7e5`). Before at `a0b0dff`: met 0/3. Landed at `2f2f12d`
  (+ `285abca` census fix): retained render.yaml and Dockerfile, S062, entry
  append; after: met 3/3 (`verification/c2-after-2f2f12d.json`).
- Mistake mined: an estimated declaration time (18:58Z vs commit 18:54:19Z);
  QUALITY round-32 criterion with a check shown able to fail
  (`verification/declared-time-check.txt`, exit 1).
- Wave 1 `kake-r32-w1`: 34 seats dispatched (16 reviewer, 5 critic,
  4 mutation-tester, 3 executor, 3 scribe, 2 scout, 1 connector).

### Round 33 (hyaku, in-session L1 KakeR33)

Declared at `bc6c4a8` (both counters frozen there, before any run).

- Motivating evidence, C1: round-32 closure routed items 2 and 3
  (`corpus/lessons/round-32-verifier-spotcheck.md`): the P6 kill rested on
  message text, and a reworded load-time message failed a correct runner
  (`.ufo/waves/round-32/w1/ExecBaseRunnerVsP6.md`). Before at `5777d5a`: met
  2 of 4 (`verification/c1-before-5777d5a.json`). Landed at `b1752a2`:
  runner `code` field, hostile `reason_code`, P6 keyed on it; after met 4 of
  4, guard_ok true; strict supplement 4 of 4 (`c1-strict-at-*.json`).
- Motivating evidence, C2: upstream ds4cc-marketplace moved to `7fc6aa2f`
  while the corpus and the local checkout stayed at `1fbdb8ed`
  (`git ls-remote` at round start). Before: met 0 of 4. Landed at
  `b1752a2`: four retained blobs, S065, section; `e490381` adds S066 (Pages
  deploy run record, failing apps-sdk test workflow) and the wave-1
  additions; after met 4 of 4.
- Routed repairs landed outside the claims: per-run default scratch
  (`e490381`; concurrency 3 of 4 failing at base → 0 of 4,
  `verification/concurrency-*.txt`), `read_expected` OSError, stray
  fixture-root entries, hostile spec-dir strays and whitespace keys
  (`1cf452e`), PROVINCE count correction.
- Mistake mined: a repair counter scored a faked repair at its after-value
  (round-32 C2); QUALITY round-33 criterion with a check shown failing on
  the bundled hollow commit.
- Wave 1 `kake-r33-w1`: 35 seats (11 executor, 6 scribe, 6 reviewer,
  5 scout, 3 critic, 2 mutation-tester, 1 connector, 1 revenger).
- Wave 2 `kake-r33-w2`: 34 seats (17 reviewer, 6 executor, 5 critic,
  4 mutation-tester, 2 scout), all returned. Repairs landed at `3abfc44`:
  stray symlinks back to per-case refusals, unreadable hostile spec
  directory exit 2, docstrings; corrections appended to SKILL, SCORECARD,
  PROVINCE, the entry and the lesson. Receipts at `3abfc44`: C1 4 of 4,
  strict 4 of 4, C2 4 of 4, concurrency 0 of 4 failing.

### Round 34 (hyaku, in-session L1 KakeR34)

- Base `1e54c89515b0b1f7c9d7d10e6232d15e43320713`; declaration, frozen
  matrix, both counters and retained sources at `d08d8de`. Frontier move off
  the citing-set gate (rounds 31–33 used it; hyaku goal-file drift rule):
  link-preview metadata (Open Graph), a lane-new area.
- Motivating evidence, C1: no lane tool checked the metadata a shared URL
  exposes. Screening of ds4cc-marketplace at `7fc6aa2f` (upstream head,
  unchanged since round 33) found Open Graph tags on 87 of 102 pages but
  `og:image` on one. Landed `scripts/link_preview_audit.py` at `5613071`
  (wave-1 `ExecLinkPreviewGate`; docstring sourcing corrected by the L1):
  C1 counter 0 of 28 → 28 of 28 with all four constant gates rejected.
  Committed selftest `scripts/link_preview_selftest.py` (29 fixtures, wave-1
  `ExecLinkPreviewSelftest`) 29 of 29 against the landed tool.
- Motivating evidence, C2: the corpus held no Open Graph knowledge (wave-1
  `CriticFrontierNovelty`). Landed `corpus/knowledge/link-preview-metadata.md`
  (wave-1 `ScribeEntryDraft`), rows S067–S077 (5 mined, 4 rejected, 2 queued)
  and the round-34 lesson at `9ef758c`: C2 met 0 of 5 → 5 of 5. Census line
  `pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1
  og-url-equals-canonical=87`, matched by an independent lxml recount and by
  the landed tool's real-input run.
- Round-33 routed defects: sandbox-only evidence retained in
  `.ufo/waves/round-34/retained/` (`a2fe31b`); the Gate records four rejects;
  two checks shown able to fail (`criteria/gate_reject_check.py`,
  `criteria/receipt_presence_check.py`); hollow shapes carried by name.
- Mistake mined in-round: both declared counters give full score to a
  control that does none of the work (C1 lookup tool `dcef39b5` 28/28; C2
  transcription `0cce15f0` 5/5); QUALITY round-34 criterion (d) with
  `criteria/lookup_control_check.py`, exit 1 on the frozen C1 counter.
- Seat boundary: wave-1 `MutC2CounterConditions` briefly wrote rows into the
  lane's `corpus/SOURCES.md` and removed them (self-disclosed; restored hash
  equals `a2fe31b`; the committed `9ef758c` file holds the L1's rows).
- Wave 1 `kake-r34-w1`: 32 seats (10 executor, 7 scribe, 5 scout,
  4 reviewer, 3 critic, 2 mutation-tester, 1 connector), all returned.

- Wave 2 `kake-r34-w2`: 35 seats (19 reviewer, 5 executor, 5 critic,
  3 mutation-tester, 2 scout, 1 sentinel), all returned. Repairs landed at
  `76fac3b`: tool (first-wins attributes, `og:image:url` alias, FIFO and
  oversized pages, unparsable canonical, repeated `--manifest`, duplicate
  JSON keys), six selftest fixtures (35 total; the three mutants that
  survived the counter and the selftest are now killed), criterion-check
  repairs (fenced Gate lines, status-word reasons, text receipts, lookup
  check exit contract), S077 tier A. Receipts at `76fac3b`: C1 28 of 28,
  C2 5 of 5, selftest 35 of 35, real-input agrees. Corrections appended to
  SCORECARD, the entry, the lesson, QUALITY and SKILL.

## Round 35 (2026-10-22) — sealed targets: link-preview audit repair and a security.txt entry

- Repair-first after the round-34 honest stop. Declared at `81d9fd74` with sealed C1 cases and
  C2 probes pinned by sha256, outside the lane until the reveal `4c6be2bd`. Controls were scored
  before any build (`318561ef`): C1 base 14, lookup `dcef39b5` 7, constant 7 of 24 against
  target 22; C2 junk 0, keyword 3, transcription 8 of 12 probes (copied fails).
- Wave 1 `kake-r35-w1` (36 seats). `CriticC2Conditions` showed hidden bytes passing C2 version
  1, so counter version 2 (`bd14096a`) cleans comments and format characters before any build
  was measured. All controls were rescored, plus a reworded-transcription control (6 probes).
- C1 build `b1cbbc39` (wave-1 `ExecToolRepair`): `og_url_multiple`, template/svg/math metadata
  ignored, unreadable page no longer stops the audit; selftest 45/45; round-34 matrix 28/28.
  Sealed 14 → 24 of 24.
- C2 build `95abec21` (wave-1 `ScribeEntryDraft`, unedited): `corpus/knowledge/security-txt-publishing.md`,
  rows S078–S087 (8 mined, 2 rejected), S006 re-opened (used-by). Sealed met false → true,
  12 of 12 probes.
- Round-34 routed defects: SKILL registry row (`fd0d53b2`); S074 correction note; `dcef39b5`
  description corrected by append; three criteria checks shown able to fail
  (`.ufo/waves/round-35/criteria/`).
- Hold: wave-1 `CriticSealedDesign` ended in an automatic model switch after a safety filter.
  It is not evidence and is not retried.
- Wave 2 `kake-r35-w2` (35 seats) attacked the landed work. Every measured value reproduced.
  C1's 22 can be met with bullet (c) skipped, and the sealed set holds no nested container.
  C2's counter meets an inverted-facts entry and a topic-list entry with landed row ids (lesson
  mistake row 5; QUALITY (e) with `criteria/knowledge_control_check.py`). Entry truth was read
  sentence by sentence; two Pages sentences were corrected by append. Added fixture
  `og_url_multiple_first_value_checked` (selftest 46/46). S001 and S002 used-by cells now name
  the entry. SKILL exit-64 label and S074 note wording fixed in place.
