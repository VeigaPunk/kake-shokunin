# Lesson — round 9 (2026-09-28)

Cites: LOG.md round-9 entry; evidence = 10 delegated read-only probes
(`~/Projects/webzites/reports/r9-publish-queue.md`, `r9-stale-markers.md`, <!-- r18 re-census 2026-10-14: ~/Projects/webzites/reports/r9-publish-queue.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
`dead-slot-recreate-readiness-r9.md`, `sentinel-sourceless-extract-r9.md`) +
self-verified curl GETs on the vault + dead slots. Commit `round-9`. Zero
publishes, zero metered fires, zero browser ops.

## The gap closed

Two coupled residuals: (a) no consolidated publish-queue readiness view — the
dedupe report named PQ-1..PQ-13 but nobody had mapped each item to gate class,
bound chat, and source freshness; (b) README residual "JS-rendered link
surfaces need rendered DOM" — false premise: the vault's link surface is a
static `const PROPERTIES = [...]` literal in the served body.

## What the baseline found

- **PQ-5 is the shortest path to green.** charter-ufo-fsd-kimi's `rebuild`
  already produced a verified version card (`efc1830`, preview 8,323B
  markerPresent, `liveAfter.stillDead:true`) — only the human Publish + slug
  click remains. Journals carry no `error.code`; the pipeline exited clean.
- **PQ-1-class vault rot is real and quantified without a browser.** 3 of 10
  live-claimed PROPERTIES[] links are dead (charter-ufo-fsd + plazir15 → 404
  sentinel sha `93ddca9a`; plazir27.kimi.pro → preview-404 redirect);
  `lucario` isn't in the array at all. `fleet/vault-properties.json` (09-20
  snapshot) still matches the live literal — the drift is upstream claims
  vs live fleet state, not page churn.
- **`sourceDir:null` is the single hard blocker for sourceless rows** —
  `cmdUpdate` refuses at `kimi-surface.mjs:483`, `cmdRecreate` refuses at
  `:845-849` on any live-200 slot. Extraction recipe landed
  (`vault-properties.md`); plazir27runson needs `--zip-exclude='assets/*.mp4'`
  (147MB of films exceed the 32MB `fetchLive` maxBuffer at `:342`, range
  `:339-346`).
- **Two platform shifts since 09-26:** the injected `sdk-seed.js` tag grew
  exactly +157B on every kimi-surface row (digest checks must normalize it —
  byte deltas now carry zero freshness signal), and website-id `1a0acf59…`
  serves on BOTH `ufo-fsd.kimi.pro` and `ufo-fsd.kimi.page` (the config's
  "fleet-unique 1/17" note is stale; an update fire may co-write both).
- **Citation review landed:** ops-automation's "6h cadence" is the timer's,
  not the file's (median gap 0.45h, one 42.7h hole); the "74 missing paths"
  figure is 75 in-repo (commit `f3d2ecd` adds 75 locs); `webzites` is not on
  PATH — canonical invocation `node ~/Projects/webzites/bin/webzites.mjs`.
- **25 unpushed source commits** are the GHP publish bottleneck:
  ds4cc-marketplace +20 (incl. the sitemap commit), plazir-15-site +5;
  charter is *behind* 2 (pull before any publish).
- **Fleet state unchanged**: probe-latest 18:51Z (12 ok / 5 violated / 1
  error), all FAILs match known-stale markers or documented dead slots —
  0 new failures. charter-ghp pin is the sole marker miss; ready diff sits
  in `reports/r9-stale-markers.md` (keeper owns the edit).

## Learned

- **The publish queue's binding truth lives in `state/kimi-map.json`, not the
  config.** Bound chats verified by `publishedUrl` matching, not hosts[] text —
  plazir15 came out ambiguous (vessel `1a0c2186` pristine vs emergent `1a0de2ed`
  with an unpublished version): a fired-orphan artifact, resolve before refire.
- **Read-only sweeps produce publish-ready diffs.** The charter-ghp re-pin is
  a one-line config edit handed to the keeper with exact line + live literal;
  prepare-the-diff beats flag-the-drift.
- **Live-404 sentinels are uniform**: all three dead slots serve the same
  13,409B body (sha `93ddca9a021664d5…`) — `liveBefore` journals pin this hash;
  any non-sentinel 404 on a kimi slot is a different failure class.
- **Cross-lane sweep found no contradictions**, one boundary note: the shared
  burner-chrome lease (CDP 9222) ownership between kake and kagi is unresolved
  — reported up, not absorbed.

## Gate

Label: **retrospective round-21 reconstruction, not original admission.** This
file had no gate section at round 9. The outcomes below are reconstructed in the
round-21 kake wave from this file's original sections (`Cites`, `The gap
closed`, `What the baseline found`, `Learned`) and the LOG.md round-9 entry
(`LOG.md:13`). They state only what those sources support.

Outcome vocabulary: **admitted with qualification** = stated with cited evidence
paths in the original text or corpus; **unverified** = cited evidence is absent,
or the claim depends on live state that was not re-read here.

Candidates and reconstructed outcomes:

- **a. Consolidated publish-queue readiness view** (PQ-1..13 mapped to gate
  class, bound chat, source freshness). Admitted with qualification: landed as
  `corpus/knowledge/publish-queue.md` (LOG.md:13). That ledger now holds PQ-1..14
  plus later addenda (r13, r16) that supersede round-9 row states; it is not a
  round-9 state snapshot.
- **b. README residual "JS-rendered link surfaces need rendered DOM" is a false
  premise**: the vault link surface is a static `const PROPERTIES = [...]`
  literal. Admitted with qualification (`The gap closed` (b); LOG.md:13 "no
  browser needed"). The premise check rests on 2026-09-28 reads and was not
  re-read here.
- **c. PQ-5 is the shortest path to green** (charter-ufo-fsd-kimi, card
  `efc1830`, preview 8,323B markerPresent, `liveAfter.stillDead:true`; only human
  Publish + slug remain). Admitted with qualification as a 2026-09-28 baseline
  (`What the baseline found`, bullet 1). Later: publish-queue.md PQ-5 r13 22:47Z
  row records it still pending with the 13,409B sentinel served. The source
  journals and preview artifact are not in this corpus.
- **d. Vault rot**: 3 of 10 live-claimed PROPERTIES[] links dead (charter-ufo-fsd
  and plazir15 → 404 sentinel `93ddca9a`; plazir27.kimi.pro → preview-404
  redirect); `lucario` absent from the array; `fleet/vault-properties.json`
  (09-20 snapshot) matches the live literal. Admitted with qualification
  (`What the baseline found`, bullet 2; corroborated by LOG.md:13 and
  publish-queue.md PQ-1, PQ-6). The GETs are 2026-09-28 self-verified reads; the
  snapshot-matches-literal check was not re-read here.
- **e. `sourceDir:null` as the single hard blocker** for sourceless rows, with
  the extraction recipe and the `--zip-exclude='assets/*.mp4'` rule for
  plazir27runson. Admitted with qualification as a code-location finding
  (`What the baseline found`, bullet 3; LOG.md:13). Pin drift is already on
  record: `round-10.md:38` moves the 32MB `fetchLive` maxBuffer literal from
  `:339` to `:342` (range `:339-346`), so the `:339` in LOG.md:13 is
  pre-correction. The webzites line numbers were not re-read.
- **f. Platform shifts**: `sdk-seed.js` tag +157B on every kimi-surface row
  (digests must normalize; byte deltas carry no freshness signal); website-id
  `1a0acf59` serves on both `ufo-fsd.kimi.pro` and `ufo-fsd.kimi.page` (config
  "1/17" note stale). Admitted with qualification (`What the baseline found`,
  bullet 4; LOG.md:13). Later: publish-queue.md PQ-10 records the same id at 2/18
  and asks for a keeper re-pin.
- **g. Citation review**: ops-automation "6h cadence" is the timer's, not the
  file's (median gap 0.45h, one 42.7h hole); "74 missing paths" is 75 in-repo
  (commit `f3d2ecd`); `webzites` is not on PATH (canonical
  `node ~/Projects/webzites/bin/webzites.mjs`). Admitted with qualification as
  in-corpus corrections: `knowledge/ops-automation.md:30-33`,
  `knowledge/kimi-subpath-audit.md:39-41`, publish-queue.md PQ-2. The reviewer of
  these corrections is not recorded as independent.
- **h. 25 unpushed source commits** are the GHP publish bottleneck (ds4cc-marketplace
  +20, plazir-15-site +5; charter behind 2). Admitted with qualification for
  plazir-15 only: publish-queue.md PQ-14 records 5 commits ahead, all dated
  2026-09-26 (r16). The ds4cc +20 and charter -2 counts are unverified; no
  corresponding record was read in this reconstruction.
- **i. Fleet state** (probe-latest 18:51Z: 12 ok / 5 violated / 1 error; all
  FAILs match known-stale markers or documented dead slots; charter-ghp pin the
  sole marker miss). Unverified as a current claim. The probe state file is not
  in this corpus, and the diff it cites (`reports/r9-stale-markers.md`) is absent
  (see Evidence limits). The charter-ghp pin finding is consistent with
  publish-queue.md PQ-12, which records the same literal mismatch at r7/r12/r13.
- **j. Binding truth** lives in `state/kimi-map.json` (publishedUrl matching, not
  hosts[] text); plazir15 is ambiguous (vessel `1a0c2186` pristine vs emergent
  `1a0de2ed` with an unpublished version), a fired-orphan risk to resolve before
  refire. Admitted with qualification (corroborated by publish-queue.md PQ-4).
  The state file was not read here; publish-queue.md notes that kimi-map content
  was 09-26-vintage and CDP :9222 was down at r13.
- **k. Read-only sweeps produce publish-ready diffs** (charter-ghp re-pin as a
  one-line edit with exact line and live literal). Admitted with qualification as
  a method. The handoff recipient changed: publish-queue.md PQ-12 (r12 relabel)
  assigns the edit to the operator, not the keeper, and the diff file is absent.
- **l. Live-404 sentinels are uniform** (13,409B, sha `93ddca9a021664d5…`); any
  non-sentinel 404 on a kimi slot is a different failure class. Admitted with
  qualification; publish-queue.md PQ-5 (r13) records the same sha as the 09-26
  journals.
- **m. Cross-lane sweep found no contradictions**; burner-chrome lease (CDP 9222)
  ownership between kake and kagi unresolved, reported up, not absorbed.
  Unverified: the sweep artifact is not in this corpus. The lease-ownership item
  is an open boundary as recorded; no resolution was checked in this
  reconstruction.

Rejected candidates: not recorded. Neither this file nor the LOG.md round-9 entry
records a rejected candidate or a reason. None are inferred.

Outside spot-check: not recorded. No independent non-author verifier of this
file appears in the corpus or the round-21 wave artifacts read.
`corpus/lessons/round-9-aggregator-corpus-verdict.md` shares the "Round 9" label
but is a different artifact (kake HEAD `a209441`, 2026-09-29, a rule-10
conformance verdict over the corpus). It does not spot-check these claims and is
not cited as one. The in-corpus corrections in item g are not recorded as
independent review.

Evidence limits (historical, not live-reverified):

- Verified-at: 2026-09-28, original round (10 read-only L2 probes, self-verified
  GETs; zero publishes, fires, browser ops). The round-21 reconstruction
  re-verified nothing live; every claim above is historically supported only.
- Vanished sources: `~/Projects/webzites/reports/r9-publish-queue.md` and
  `r9-stale-markers.md` are absent (annotation at this file's line 4; r18
  re-census 2026-10-14). The fleet dedupe report is absent (publish-queue.md:3).
  Operator requirement: restore these from history or retire the citations.
- Not checked in this reconstruction: `reports/dead-slot-recreate-readiness-r9.md`
  and `reports/sentinel-sourceless-extract-r9.md`. Their status is unknown here.
- Recheck (not run; local historical reading only): `git show 5009ecaa1cce10b895617a585ddd3f7c7c923a84:corpus/lessons/round-9.md`. The external readiness reports require operator restoration and direct re-evaluation or explicit retirement; no present availability is inferred here.

Contract references:

- **S019 metadata contract**: `.ufo/waves/round-21/wave1-spec.json` names S019 as
  the metadata authority that L1 will register in a canonical CORPUS.md. At this
  reconstruction no `S019` row exists under `corpus/` (`SOURCES.md` ends at
  S018) and no `corpus/CORPUS.md` exists. S019 is therefore not cited as
  satisfied here. It is metadata authority, not platform authority.
- **Round-21 lesson**: no `corpus/lessons/round-21*.md` exists at read time. The
  round-21 artifacts cited instead are `.ufo/waves/round-21/initial.json:41`
  (round-9.md listed as a round input) and `.ufo/waves/round-21/wave1-spec.json`
  (Lesson15 entry).
- **Pre-edit identity**: round-9.md was 66 lines, 4,173 bytes, sha256
  `b613ce951eb78996c0ecd02ac2c3e21a9850aef48ff68985f7a62b21d39846e2`, matching
  the value in `.ufo/round-20/measured-corpus-inputs.json` (measured 2026-10-15).
