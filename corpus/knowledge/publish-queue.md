# Publish-queue readiness ledger (PQ-1..PQ-13)

Source queue: `~/Projects/webzites/fleet/fleet.dedupe-report.md` (r1 lines
46–57, r2 lines 89–106). Config of record: `fleet/fleet.config.json` (21 rows,
`schema:webzites-fleet-v1`; `fleet/fleet.json` is a generated 2026-09-20
snapshot of the vault's *claimed* PROPERTIES[] — the audited input for PQ-1,
NOT a second config). Baseline evidence: `reports/r9-publish-queue.md`,
`reports/r9-stale-markers.md`, `reports/dead-slot-recreate-readiness-r9.md`,
`reports/sentinel-sourceless-extract-r9.md` (all 2026-09-28, read-only).

Gate classes: `metered-fire` (one metered chat fire must be spent),
`human-click` (operator Publish/Share→Update or external action), `missing-chat`
(no chat owns the host per `state/kimi-map.json`), `missing-source`,
`none` (config/policy only). Every publish ends in `human-click` — the
version-card click is never automatable.

## Ledger

| PQ | target | what it fixes | gate class | pre-publish checks | post-publish free reads | residuals / notes |
|---|---|---|---|---|---|---|
| PQ-1 | vault `ufo-fsd.kimi.page` (+ veigapunk-page index, ds4cc-mirror-vault-row) | PROPERTIES[] drift: **3 of 10 live links dead** (charter-ufo-fsd.kimi.page, plazir15.kimi.page → 404; plazir27.kimi.pro → preview-404) + ds4cc row `url:null` while live | `missing-chat` + `missing-source` + human | vault unbound after 200-chat sweep; sourceDir:null — extraction recipe in `vault-properties.md` | live GET + `kimi-map` refresh | blocked hardest: needs source bytes + chat + fire + click |
| PQ-2 | `ds4cc-kimi-mirror` (chat `1a073c43-bf42-874a-8000-0907bd80b9dc`) | stale ~Aug-29 mirror; **75 missing canonical paths** (sitemap f3d2ecd: 18→93 locs — "74" in dedupe is off by one); r13 decomposition: `/speedrun/ /burnerchrome/` 404s are the **kimi dir-index pitfall** (`index.html` twins serve 200 — not staleness), `/iqrunway/` is dead on BOTH surfaces (0 sitemap locs, absent from source) | `metered-fire` + human | `sync-check ds4cc-kimi-mirror` (in-sync* = identity only); bound chat verified | live URL 200 → `GetWebsiteByChatID` PUBLISHED → `sync-check` → `kimi-map` | r13 22:47Z re-verify: **delta UNCHANGED** — 19/93 served, 74 missing by live-GET (75 by f3d2ecd accounting: 5 pre-serve, 4 misses pre-f3d2ecd), 0 per-URL transitions, **mirror root (ds4cc.kimi.page)** content-frozen 74,641B (r14 erratum: r13 said "byte-frozen" — raw sha varies per fetch via Cloudflare cfemail re-encoding, 1 occurrence; valid freeze metric = cfemail-normalized sha `4427b7f8…`, equal across r13+r14 fetches; max embedded date 08-21); `update` verb ships index.html-only (kimi-surface.mjs:459-466) — subpath restore needs recreate-class zip; source `ds4cc-marketplace` is **20 commits unpushed** (live canonical sitemap 404) — pushing GHP first also advances canonical; r14 23:15Z re-verify: **delta unchanged again** — 19/93, 74 missing, 0 transitions, universe identical; mirror `sitemap.xml` itself 404 (0 locs live) — the 93-loc universe is the source-tree sitemap (md5 `0adbb105…`, unchanged vs r13); **r15 00:49Z gate check: remote `e6bd071` unchanged, still 20 ahead — gate CLOSED, delta stands; erratum — the "root" figures above are the MIRROR root (`/tmp/kake-r14/pq2-root.html` fetched ds4cc.kimi.page); canonical `ds4cc.com/` is 79,453B sha `b6f65899…` byte-identical to `origin/main:index.html` (etag `6ab49127-1365d`, last-modified = `e6bd071` commit instant, 0 cfemail → plain sha is its freeze metric); normalization method variance: r14 series computed `4427b7f8…`, r15 series `6a0c24b5…` — same mirror body, different normalizer |
| PQ-3 | `plazir27-kimi-page` (chat `1a0b5f08-fb32-87ba-8000-0907192544b0`) | 09-18-vintage charter mirror vs 09-29 canonical beat | `metered-fire` + human | local charter checkout synced at `9c28d29` as of r14 00:37Z (was behind 5 `b74190e…a8f1e2b` — the 00:06:19Z scribe push cleared it; re-verify `git status -sb` first anyway — beats land ~daily); mirror embedded max date 09-18 | marker re-pin (PQ-12) after publish; `kimi-map` | sequences into PQ-12 |
| PQ-4 | `plazir15` (vessel `1a0c2186-fa12…` 0 versions; emergent `1a0de2ed…` 1 version unpublished — binding UNRESOLVED) | dead slot restore; tree md5-identical to plazir15-ghp (200, 38,337B) | `metered-fire` + human (Publish + SetWebsiteSlug) | journals: last `recreate` exit code 6 post-`fired` — a fire was consumed 09-26T14:46Z with no landed card; resolve chat ambiguity via `kimi-map` before refire | live 404→200 + slug resolve | orphan fire risk documented in `fire-journal-codes.md` |
| PQ-5 | `charter-ufo-fsd-kimi` (rebuild chat `1a0de32f-3f12-8611-8000-0907d06bd2f2`, 2 versions) | dead slot — **fire already done**: version `efc1830` + preview 8,323B markerPresent, `liveAfter.stillDead` | `human-click` only | none — shortest path to a green row; staged zip 2 days stale vs HEAD `61d0ce6` (r13; acceptable for publish; re-stage if restoring from source) | click Publish on version card + set slug `charter-ufo-fsd` → live 200 + slugStatus | r13 22:47Z re-verify: **still pending** — live slot serves the byte-identical 13,409B 404 sentinel (sha `93ddca9a…` == 09-26 journals); zero fires fleet-wide since 09-26T15:34Z; `kimi-map` content is 09-26-vintage (CDP :9222 down — `publishedUrl:null` is NOT same-day evidence); preview `p-bieb65….kimi.page` 200, 8,387B (+64B vs journal 8,323B, unexplained); operator decision restore-vs-retire precedes the click |
| PQ-6 | `plazir27-kimi-pro` | slot never served; `ballot` marker misattributed (r2: 0 hits in plazir27, 35 on plazir15-ghp); provisional `PLAZIR-27` pin + `finalUrlNot:preview-404` already armed | `missing-chat` + `missing-source` + human | 302→`statics.kimi.ai/pages/preview-404-en.html` (5,995B) confirmed 09-28; `kimi-pro-slot` updatePath undocumented (kimi-surface-ops.md:175) | n/a until restored | extraction impossible — no artifact bytes anywhere |
| PQ-7 | `xsnapshot-app` | DNS registration (armed NXDOMAIN tripwire; curl exit 6 since 09-21) | `human-click` (external registration) | none | row leaves `errors[]` in probe-history | constant errors[] is intended baseline until then |
| PQ-8 | vault + `veigapunk-page` canary | decide vault canary treatment; veigapunk carries `WZ-CANARY-FIX-veigapunk` (keeper publish 09-21T03:47Z) | `none` — decision | — | — | execution path feeds PQ-13 verification |
| PQ-9 | fleet-wide | policy: should `probe.mjs` skip `status:"pruned"` rows? — it currently has **no** pruned branch (grep: 0 hits); pruned rows probed equally | `none` — policy | — | — | code change in `src/probe.mjs`, not a publish |
| PQ-10 | ufo-fsd-kimi-pro, xsnapshot-app, snapshot-kimi-pro, plazir27-kimi-pro, charter set | weak/misattributed marker tightening — r2 applied 13 field edits on 11 rows, killed 12 swap-mutations | `none` — config done | — | — | residual: content-level assertions are a probe.mjs feature; **new collision**: `ufo-fsd-kimi-pro` pin `data-kimi-website-id="1a0acf59…"` regressed 1/17 → 2/18 — same site-id serves on `ufo-fsd.kimi.page` AND `.kimi.pro` (keeper re-pin needed); `plazir27runson` marker `Nightcall` case-mismatches served `NIGHTCALL` — passes today only via title regex |
| PQ-11 | `plazir27runs-on` (chat `1a049cb5-47d2-89cb-8000-0907da6e778e`) | extract 63KB doctrine build to Origin repo OR accept surface-only | `missing-source` | config points sourceDir at charter repo but content is a distinct frozen 09-02 artifact — provenance unresolved | — | extraction feasible (self-contained body per sentinel audit) |
| PQ-12 | `charter-ghp` (+ plazir27-kimi-page after PQ-3) | re-pin beat-churn marker: config `2026-09-26 scribe beat` vs live **`2026-09-28 scribe beat (`** (verified r7 + r12 + r13 22:47Z live GET; fleet.config.json:256) | `human` — **operator config edit** (r12 relabel: no webzites code writes `fleet.config.json`, only the `loadFleetConfig` reader `src/fleet.mjs:7-11`; the active scribe, not any keeper, churns the marker — the scribe's push leg is failing (3 beats `pushed:false` since 06:05Z), but r13 found the **human pushed 5 commits directly 18:32–20:43Z** and Pages served them within ~30s: live is deploy-current with `a8f1e2b`, so "churn paused" applies only to the scribe automation, not the repo) | diff in `reports/r9-stale-markers.md` | next probe run flips row ok; procedure `SKILL.md` re-pin section | beats churn ~daily while beats land — see SKILL.md re-pin procedure + r13 addendum in `keeper-timer-inert.md`; keeper-timer dead ≠ the blocker |
| PQ-13 | `veigapunk-page` | conditional verify only — canary row-id pin discriminates by design | `none` — conditional | — | re-GET after any PQ-8 action | only if PQ-8 executes |

## Ordering DAG (evidenced edges only)

- **PQ-3 → PQ-12**: re-pin the kimi charter beat marker after the mirror republish.
- **PQ-8 → PQ-13**: canary verification is conditional on the vault decision.
- **PQ-2 ↔ ds4cc GHP push**: independent queue items but one lever — the 20
  unpushed `ds4cc-marketplace` commits advance BOTH the canonical site and the
  mirror source payload.
- All other items independent; never invent edges between PQ-1/PQ-8 (both
  mention the vault but have no shared precondition).

## Cheapest wins

1. **PQ-12** — one config line (`fleet.config.json:256`), diff supplied.
2. **PQ-5** — version card `efc1830` already built and preview-verified; only
   the human Publish + slug click remains.
3. **PQ-10 residue** — re-pin `ufo-fsd-kimi-pro` marker to a non-colliding
   literal + fix `Nightcall`→`NIGHTCALL` casing (keeper edits).

## What publishes do NOT fix

- `dir/` href rot on kimi mirrors — needs href rewrite at source (permanent
  until republish-with-rewrite; `kimi-subpath-audit.md`).
- Vault PROPERTIES[] rot — needs the extraction+chat path of PQ-1.
- Beat-dated pins — will re-churn ~daily while the scribe beats land.

## r14 re-verification (2026-09-28T23:1xZ, read-only)

- **PQ-5 still pending** (23:11:50Z + 23:13:07Z live GETs): 404, 13,409B,
  sha `93ddca9a…` — byte-identical to r13; zero `fire:true` journals newer
  than 09-26T15:34:24Z; `kimi-map` entry (chat `1a0de32f…`) still
  `publishedUrl:null`, `versionCount:2`, latestVersion `efc1830`.
- **Generic-sentinel caveat (r14 scout):** the 13,409B / sha `93ddca9a…`
  body is the **generic kimi 404 sentinel**, served byte-identically by
  `plazir15.kimi.page`, `lucario.kimi.page` and `charter-ufo-fsd.kimi.page`
  — it cannot discriminate *which* slot a publish landed in. The decisive
  signals are the **404 status flip** and the sync-check
  `unpublished404:true` classification (`kimi-surface.mjs:180`,`:198`),
  never the sentinel sha alone.
- **PQ-12 pin persist — and the loop caught its first transition (r14
  00:37Z):** `fleet.config.json:256` still `2026-09-26 scribe beat` (file
  untouched since 09-27T15:30:57Z). At 23:11Z live carried
  `2026-09-28 scribe beat (` / 53,353B / sha `0decd827…` == `a8f1e2b`,
  remote main `a8f1e2b`, clone behind 5. **Then the 00:06:19Z scribe fire
  pushed for the first time in 4 beats** — ledger `pushed:true`, beat
  `9c28d29` (falsified the r14 `pushed:false` prediction; the
  `pull timed out after 60s` blocker cleared; push leg recovered). Live at
  00:37Z: **`2026-09-29 scribe beat (`**, 53,386B, sha `fb365e38…`;
  remote+local main both `9c28d29` (PQ-3's behind-5 precondition cleared —
  clone synced). Row 78 (00:01:09Z) still violated on the 09-28-vs-09-26
  gap; every next sweep FAILs until the operator edit lands — and the
  correct pin literal is now `2026-09-29 scribe beat`, NOT `2026-09-28`
  (edit-time literal guard below: verify live at edit moment).
- **Canonical side (r14 scout, new):** `ds4cc.com/sitemap.xml` and
  `/robots.txt` are **live 404** (9,379B GH-Pages 404) — both exist only in
  the 20-unpushed-commits working tree (`e82a262`, `f3d2ecd`; `git ls-tree
  origin/main` has neither). The 93-loc canonical URL list is
  **working-tree-only, never on the wire** until the ds4cc push lands —
  PQ-2's canonical reference set is local-only by construction.

### PQ-5 publish-verdict procedure (armed 2026-09-28; run the moment the
### operator clicks Publish on card `efc1830` + sets slug `charter-ufo-fsd`)

**PQ-5 pending-publish watch (armed r14, critic-designed):** bounded,
named trigger + checklist — all free reads, no poller/daemon/metered
verb/lease. Score-eligibility cap: arming alone is a landed capability,
NOT a score move; it becomes move-eligible only if the event fires and the
watch catches it in-round (correctly-attributed EXIT + E1–E5 chain).

NOW-predictions (verified 2026-09-28T23:1xZ — any break ⇒ arming premise
void, pivot to immediate post-publish verification, report loudly):

- **P1** `GET https://charter-ufo-fsd.kimi.page/` → HTTP **404**,
  **13,409B**, sha `93ddca9a0216…ca966` (sentinel; 23:11:50Z).
- **P2** `probe-latest.json` row `charter-ufo-fsd-kimi` = `violated`; id
  present in `violated[]` of every full sweep today (rows 73–76).
- **P3** vault `PROPERTIES[]` (13 members, 10 url-bearing) carries
  `https://charter-ufo-fsd.kimi.page` as a member, currently 404.

EVENT-predictions (check the moment a publish is reported/suspected):

- **E1 — primary discriminator:** the SAME slug URL flips **404→200**; a
  200 on a preview host proves nothing (previews exist independently of
  publish — never claim "published" from preview-host evidence).
- **E2** body leaves the sentinel class (sha ≠ `93ddca9a…`);
  `sync-check charter-ufo-fsd-kimi` drops `unpublished404:true`. Judge by
  title+marker+vintage, NEVER bytes (kimi rewrites bytes).
- **E3** next full sweep → id leaves `violated[]` → probe-delta emits the
  EXIT event (first for this id since its ENTER).
- **E4** vault member link revives 404→200 (dead-link count 3→2 vs the
  r9 baseline; vault body itself unchanged).
- **E5** (conditional, browser-gated) `kimi-map`/`GetWebsiteByChatID` →
  `publishedUrl` + `PUBLISHED` + slugStatus. CDP :9222 was down r13,
  `kimi-map.json` is 09-26-vintage — **never gate "published" on E5 and
  never cite `publishedUrl:null` as evidence of anything** (r13 rule);
  the decoy `ufofsd-charter.kimi.page` publishedUrl belongs to chat
  `1a073c3f…`, NOT this chat — never cross-attribute.

Failure branches (the watch outputs a verdict, never a shrug):

- **F1** preview host 200 + slug host still 404 ⇒ "card published,
  **slug not set**" — report the half-state, never "published".
- **F2** slug host 200 + title/marker mismatch vs source ⇒ wrong version
  published (not `efc1830`) — compare title/marker, not bytes.
- **F3** any NOW-prediction breaks with no operator action reported ⇒
  arming premise falsified ⇒ pivot to immediate post-publish verification.

Post-publish beat churn re-trips the PQ-12-family marker on the NEXT sweep
(expected — see the PQ-12 loop below).

### PQ-12 dated re-check loop (armed 2026-09-28; per-round until the
### operator lands the one-line `fleet.config.json:256` edit)

Each freshness round records, with timestamps: (a) live beat line
(`curl`+`grep -o 'scribe beat[^<]*'`), (b) config pin literal, (c) remote
`main` HEAD, (d) local clone behind-count. Five states: `PERSIST` (pin ≠
live, no edit — expected until the operator acts); `EDIT-LANDED` (pin ==
live → row flips ok on the NEXT full sweep — the first EXIT since
09-27T06:22Z; verify, never assume); `CHURN-AGAIN` (pin == live at read
time but live beat moved before the sweep — re-pin loop, scribe beats land
~daily); `SILENT` (no new sweep row within ~6.5h of the last — timer
health suspect, check `systemctl --user list-timers webzites-probe.timer`);
`ANOMALY` (anything else — e.g. live ≠ remote main: deploy lag, investigate
before recording a verdict).

Edit-time literal guard (r14): a re-pin recipe MUST verify the live literal
equals the pin **at edit moment** — beat pins have bounded shelf life
(the 09-26 pin survived <24h before the 09-27T06:22Z ENTER; beats land
~daily: `c8bbc62` 09-27, `61d0ce6` 09-28; next scribe fire 00:06:19Z with
the push leg failing ⇒ a 09-29 literal can land only via human push or
scribe recovery — the exact r13 pattern). Under read-only contracts, pin
vs live comparison uses the raw.githubusercontent path (proven workable
r14) — any local `git pull`/`fetch` in `origin-work/*` needs explicit
sanction; both write.

### r14 completed baseline (not a move): charter post-push subpath audit

The r13 human-push series `b74190e…a8f1e2b` (5 commits) was never per-path
verified (r6's baseline predates it). Critic-executed 2026-09-28T23:22Z:
trees API `61d0ce6`→`a8f1e2b` = ADDED 3 (`beats/M-scribe-autoclaw-0029.md`
5,066B, `build.js` 9,190B, `src/index.template.html` 12,859B), CHANGED 2
(`index.html` 8,592→53,353; `next-run.md` 13,101→15,241); live GETs —
**5/5 paths byte-identical to raw `a8f1e2b`**; og:image `vessel.webp` 200,
121,710B `image/webp`. NULL result: no rot, no deploy lag — closes the r6
gap for this series; per r6/r7/r8 null-coverage precedent this is a
baseline, not a freshness move.
## r15 re-verification (2026-09-29T00:4x–00:5xZ, read-only)

- **PQ-12 state `PERSIST`:** `fleet.config.json:256` still
  `2026-09-26 scribe beat` (mtime 09-27T15:30:57Z — operator edit not
  landed). Live `2026-09-29T00:48:51Z`: 200, 53,386B, sha `fb365e38…`,
  literal `2026-09-29 scribe beat (` (counts: 09-26=0, 09-28=0, 09-29=1);
  byte-identical to remote `main` HEAD `9c28d29` (ls-remote) and to clone
  `~/Projects/origin-work/charter-ufo-fsd` HEAD/origin-main (behind 0 — the
  scribe's own 00:06:19Z run refreshed FETCH_HEAD at 00:11:30Z; no pull by
  kake). EDIT-LANDED excluded (pin ≠ live); CHURN-AGAIN excluded (pin ≠ live
  at read); SILENT excluded (row 78 at 00:01:09.976Z, ~48min old); ANOMALY
  excluded (live == remote HEAD → deploy-current). Scribe ledger: no beat
  newer than `9c28d29` (rows_newer=0); next fire ~06:06Z (post-round);
  telemetry degraded (grok-web 300s timeout + kimi route failure) — beats
  are local-fallback while routes stay broken. Correct re-pin literal at
  edit moment = `2026-09-29 scribe beat`.
- **PQ-5 still pending** (L1 00:45Z + executor 00:49:37Z live GETs): 404,
  13,409B, sha `93ddca9a…` byte-identical to armed baseline; P2 holds (row
  `charter-ufo-fsd-kimi` violated in row 78); P3 holds (vault GET 200/
  9,966B at 00:50:50Z — member `charter-ufo-fsd` status live, still 404 →
  dead-link count 3/10 unchanged). E1 never fired → watch armed, not
  move-eligible; no half-state.
- **PQ-2 UNCHANGED — gate closed:** remote `main` still `e6bd071`
  (ls-remote 00:49:11Z); none of the 20 unpushed commits (`f3d2ecd` HEAD)
  is an ancestor; live `sitemap.xml`/`robots.txt` still 404 (9,379B GH-
  Pages 404 ×2). Delta stands: 19/93 served, 74 missing, 0 transitions —
  full sweep intentionally not re-run (gate unchanged). Corrections landed:
  PQ-2 cell's "root" disambiguated to the mirror root; canonical-side
  wording "working-tree-only" → both files ARE tracked at local HEAD,
  absent from `origin/main` (unpushed).

### r15 freshness move — path-citation base re-sweep (drift CAUGHT)

Sibling kasegi reported `~/Projects/bounties` (its PROVINCE root) vanished
~2026-09-28T20:51-03:00, actor undetermined (`l0-questions.md` kasegi|r15);
`~/Projects` dir mtime = the same instant (23:51:31Z). Kake re-swept its
whole citation base (r10's "60/60 resolve" had gone stale by fiat, never
re-measured): **49/58 unique cited paths resolve, 9 miss** — 4 are
self-declared-absent citations (`package.json` never existed; 3 lucario
artifacts the corpus calls non-existent) = verified-true claims; **5
genuine danglers**: `~/Projects/ufofsdbeta`, `~/Projects/ufofsdbeta/.ufo`,
`~/Projects/ufofsdbeta-kimi-review` (all verified PRESENT at r1), and
`~/Projects/ephemeral/wz1`, `~/Projects/ephemeral/wz1/ds4cc` (emptied
21:42-03:00 — `ephemeral/` itself still exists). Domain roots webzites /
ds4cc-marketplace / plazir-15-site / origin-work / lucario all alive; kake
cites `bounties` 0 times. Classification claims about the vanished dirs are
annotated (not deleted) — they were true when written. Hazard rule landed
in SKILL.md: `~/Projects` vs `~/projects` are distinct dirs; lowercase-path
ENOENT is a typo, not a vanish.
