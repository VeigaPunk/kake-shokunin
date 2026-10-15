# Freshness sweep — the standing-claim drift instrument

> Round-20 correction: the r16/r17 measurements and copied table baselines
> below are historical, not current expectations; load
> `corpus/knowledge/freshness-pins.json`. The P1 OR-over-cites rule and its
> old “Known limits” paragraph are superseded by the citation-local rule
> at the end of this entry. Other annotation-window limitations remain.

`scripts/freshness-sweep.mjs` (read-only, node ≥18, zero deps) +
`corpus/knowledge/freshness-pins.json` (the pinned baselines). One command
re-derives every standing claim family this lane owns and returns a
machine verdict:

```bash
node scripts/freshness-sweep.mjs            # all sections, human lines
node scripts/freshness-sweep.mjs --json     # one JSON object (gate pins, sets, verdicts)
node scripts/freshness-sweep.mjs --offline  # §paths + §history only; armed checks = skipped(offline)
node scripts/freshness-sweep.mjs --section=paths|history|armed
node scripts/freshness-sweep.mjs --selftest # hermetic fixtures, proves the exit contract
```

**Exit contract:** `0` every checked claim at its pinned expectation ·
`1` drift (unannotated non-resolving citation, history shape change, detector
delta, armed-watch state change) · `2` unreadable/invalid input — **including a
pins file that exists but fails to parse** (r17: `loadPins`'s catch used to
degrade silently to defaults, turning every gate inert under a "gates inert"
footnote; an invalid pins file now exits 2 with the parse error on stderr) ·
`64` usage error. Read-only: it writes nothing (no temp files, no state).

## Why it exists (r16, freshness 9→10)

r10–r15 re-verified drift ad hoc and **path-only**: r10's "60/60 paths
resolve", r15's "58 cited-path targets" sweep. Both were true when written and
both rotted — r15 had to retire the 60/60 claim by measurement. A frozen
sample cannot see the claim classes it never sampled: counts, byte sizes,
shas, ETags, code-line pins, verb *outcomes* (ok/attention lists), journal
structure. r16 enumerated **160 quantified standing claims** with one live
recipe each (`scout-claims.md` in `/tmp/kake-r16/`) and found **15 STALE + 7
UNVERIFIABLE** — including classes no earlier round swept (a verb-outcome
literal, a journal top-level key union that was wrong when written, an ETag
literal, a fire-count undercount). This instrument is the standing half: the
same checks, pinned, every round, exit-coded.

## Check-id table (what fails and why)

| id | section | tests | pinned baseline | drift predicate |
|---|---|---|---|---|
| P1 | paths | every `~/…` / `/home/vgpnk/…` token in `SKILL.md` + `corpus/**/*.md` resolves | — | token non-resolving with no absent-word within ±2 lines on any citing line → `1` |
| P2 | paths | the frozen miss set | `pathsMissSet` (10 entries, r17) | any *new* miss (`newMissing`) → `1`; a recovered path is informational |
| P2b | paths | `~/Projects` direct-children set (r17: closes the uncited-child-loss gap — W6 `~/projects` was caught only via a cited descendant) | `projectsChildrenSet` (36 entries) | **informational, never gating** — removed/added children printed each run |
| P3 | paths | the scanned file set | `pathsFiles` (39-entry list — r17: was pinned as the bare count `38`, which `Array.isArray` silently skipped → gate inert-by-type; now the real list, delta printed) | informational only (file moves are reported, never fatal) |
| H2 | history | last full-sweep shape | `fleetTotal` 18 / `fleetOk` 12 / `violated[]` / `errors[]` sets | any set inequality → `CHANGED`, `1` (both sides printed — an improvement is distinguishable from a regression) |
| H3 | history | fleet full/spot split | `probeFullSweeps` 67 / `probeSpotProbes` 11 | informational (re-pin each round; count rots by design) |
| H4 | history | `scripts/probe-delta.mjs` over the history | `deltaEventsExact` 6, `deltaLastEvent`, `deltaPhantomMax` 0 | event count/set mismatch or a tampered interior row → `1` |
| A1 | armed | PQ-12 charter-ghp beat pin | `charterGhpPin` `2026-09-26 scribe beat`, `charterGhpLiveSha` `fb365e38…`, `charterGhpDeploy` `9c28d29`, `charterGhpChurnAfter` `2026-09-29` | verdict ∈ `{PERSIST, EDIT-LANDED, CHURN-AGAIN, SILENT, ANOMALY}`; a stale live-sha pin becomes a drift reason so a fired watch cannot go silently green |
| A2 | armed | PQ-5 kimi dead slot (E1 watch) | `pq5Status` 404 / `pq5Bytes` 13409 / `pq5Sha` `93ddca9a…` | `200` → `E1-FIRED` (event, `1`) |
| A3 | armed | PQ-2 ds4cc push gate | `pq2Remote` `e6bd071` / `pq2Unpushed` 20 | remote moved → `GATE-OPENED` (event, `1`) |
| A4 | armed | ds4cc sitemap/robots pre-push state | `sitemapStatus` 404 | `200` → `LISTED-LIVE` |
| A5 | armed | PQ-14 plazir15-ghp push gate + live/source sitemap gap | `plazirRemote` `bd02d10` / `plazirUnpushed` 5 / `plazirLiveSitemapLocs` 8 / `plazirSourceSitemapLocs` 7 | remote moved → `GATE-OPENED`; live loc count ≠ pin or ≠ source → `LIVE-SOURCE-GAP` (the r16 catch) |

Informational pins (reported by the claim sweep, not this gate):
`vaultBytes`/`vaultSha`/`vaultUrlBearing`/`vaultDeadLinks`,
`fleetSites`/`fleetStatus`, `grokbotsRows`, `reposClones`. `--json` lists
truly unevaluated pins under `pins._unused`; r17 fixed a label bug that put
A5's six consumed plazir pins in that list even while they drove the verdict.

## Pins: how to re-pin

1. Run the instrument; every drift line prints expected vs observed.
2. Decide per line: **world moved** (re-pin here + fix the prose in the same
   commit) or **claim was wrong** (fix the prose; the pin stays).
3. Edit `freshness-pins.json` (`round` + `updated` fields are the re-pin
   stamp), then re-run `--selftest` and the live run.
4. Never copy a pinned literal into prose — prose cites this file and the
   check-id (e.g. "see A5"), because a copied literal is exactly the rot class
   this instrument exists to catch.

## r16 run — first complete pass (2026-09-29T02:4xZ, read-only)

```
paths  62 targets · resolve 47 · declaredAbsent 9 (+3 indirect) · drift 0 · unresolved 6 (globs/placeholders)
       files 36 · missSet 9 (all annotated) · set-delta: no new miss
history 78 rows (floor 78) · full 67 · spot 11 · malformed 0 · last 2026-09-29T00:01:09.976Z (age 2.6h)
       last total 18 / ok 12 / violated {plazir15, charter-ufo-fsd-kimi, charter-ghp, plazir27-kimi-pro, lucario} / errors {xsnapshot-app} → MATCH
       probe-delta 6 events (max 12) · phantom 0 · last ENTER lucario @2026-09-27T16:38:27.135Z
armed  PQ-12 PERSIST · PQ-5 PENDING · PQ-2 GATE-CLOSED · ds4cc sitemap PRE-PUSH
       PQ-14 plazir15-ghp GATE-CLOSED · sitemap LIVE-SOURCE-GAP  ← DRIFT, exit 1 (live 8 vs source 7)
VERDICT DRIFT (exit 1: plazir-live-source-gap)
```

**Exit 1 is currently the EXPECTED verdict.** PQ-14's gap is an open drift: the
published plazir sitemap has 8 locs while its source has 7, because
`~/Projects/plazir-15-site` is 5 commits ahead of `origin/main`. The instrument
does not green-light a live≠source state — that is the whole point of the
§armed section. Use `--section=paths` / `--section=history` / `--offline` to
isolate the other sections, and expect the drift line to disappear (gate
`GATE-OPENED`, sitemap `MATCH`) once the operator pushes.

Selftest: 9/9 (declaredAbsent is exit-neutral; an unannotated miss exits 1;
an interior-tampered history row exits 1 via the exact event/last-event pins;
malformed JSONL exits 2; unknown flag/section exits 64). State guard: the
`~/Projects/webzites/state/` sha list is byte-identical before/after every run <!-- r18 re-census 2026-10-14: ~/Projects/webzites/state absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
(r16 sentinel, 33/33 files).

## r17 run (2026-09-29T03:2xZ, read-only)

```
paths  66 targets · resolve 49 · declaredAbsent 10 · drift 0 · files 39 · relativeCites 382
       BEFORE the fix: the lowercase `~/projects` tree (r16 inode 101125103)
       was absorbed into existing `~/Projects` (inode 27238 unchanged), then
       removed between r16 ~02:4xZ and r17 (03:13–03:14Z cleanup window) →
       1 unannotated descendant miss (round-1-aggregator-audit.md:10); cite
       corrected to the canonical uppercase path + absence annotated,
       missSet re-pinned 9→10. ~/Projects children set MATCH (P2b).
history 78 rows · last 00:01:09.976Z · MATCH · probe-delta 6 events · 0 phantom
armed  PQ-12 PERSIST · PQ-5 PENDING · PQ-2 GATE-CLOSED · ds4cc sitemap PRE-PUSH
       PQ-14 GATE-CLOSED · sitemap LIVE-SOURCE-GAP  ← expected open drift, exit 1
VERDICT DRIFT (exit 1: plazir-live-source-gap only)
```

Selftest 10/10 (r17 adds malformed-pins → exit 2). State guard:
`~/Projects/webzites/state/` 33-file sha set byte-identical before/after <!-- r18 re-census 2026-10-14: ~/Projects/webzites/state absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
(`/tmp/kake-r17/sentinel-{before,after}.sha`).

## Known limits

- Non-`~/`-prefixed citations (`fleet/…`, `src/cli.mjs`) are outside the
  resolver: 382 lines with ≥1 `REL_PATH_RE` match (r17 recount; the scanner
  runs one non-global `exec` per line, so this is a line count, not 436 true
  occurrences), reported as `relativeCites`, never resolved or gated. Their
  line-level correctness is the reviewer's job each round.
- The absent-word window is ±2 lines with an OR over cites (deliberate:
  collective annotation, e.g. `publish-queue.md` §r15 lists five vanished
  paths under one sentence). `pathsAbsenceStrictSameLine: true` opts into
  same-line-only semantics — stricter, but it falsely rejects that block, so
  it is off by default and the ambiguity is printed.
- Pins are literals in the repo: they re-rot if nobody re-pins. The instrument
  cannot detect its own staleness — a green run against stale pins is exactly
  the failure the round-sweep cadence exists to prevent.

- r17 additions to the hazard ledger: (a) `pathsFiles` pinned as a bare count
  (`38`) instead of the file list evaluated inertly — `Array.isArray` guards
  mean a wrong-*type* pin silently disables its delta (now the real 39-entry
  list); (b) P2b is informational by design — a gate on `~/Projects` children
  would flag legitimate operator churn the lane cannot adjudicate; W6 showed
  the reporting-only variant was enough to catch the loss the same round.

## Round-20 correction — citation-local absence evidence

Source: `scripts/freshness-sweep.mjs` (`scanCitations`, `printPaths`, selftest
case M); measured CLI evidence and input digests:
`.ufo/round-20/{baseline-proof,candidate-proof}.json` and
`.ufo/round-20/frozen/citation-locality/expected.json`.

P1 now requires **every occurrence of a missing normalized target** to
satisfy its own existing local annotation rule. One historical occurrence
cannot excuse another unannotated occurrence, including a home-alias
spelling or an already-pinned miss. JSON `drift[].unannotatedCites` lists
the actionable locations; `cites` keeps the full context. Human output
reports the unannotated subset.

The local rule itself has not tightened: the default still accepts absence
vocabulary in the citing line's ±2-line window; strict mode remains opt-in.
This is annotation coverage, not semantic proof that every historical
recipe is safe or executable. A present target resolves before annotation
classification; a missing target whose occurrences are all annotated
remains exit-neutral. Globs/placeholders remain unresolved.

The round-20 local proof removes a false-green; it does not restore deleted
publishing sources, authorize HTTP probes or deployment, repair corpus
citations wholesale, or complete a training round. Required specialist
dispatch is blocked by the effective host bindings recorded in
`.ufo/round-20/routing-blocker.json`. Do not re-pin existing misses to hide
the newly visible unannotated occurrences.