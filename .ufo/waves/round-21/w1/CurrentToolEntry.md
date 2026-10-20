# Round-21 w1 — freshness-sweep / probe-delta: runnability and metadata-date audit

Scope: `corpus/knowledge/freshness-sweep.md`, `corpus/knowledge/probe-delta-alerting.md`, and their scripts/pins. Read-only. No network probes (default `freshness-sweep` mode runs armed remote checks; not run). No edits to targets. No tools installed or upgraded (node v24.21.0 already present). Scratch outputs written to `/tmp/kake-r21-w1-*` (paths/offline JSON, selftest text) as evidence only.

Note on concurrency: `freshness-sweep.md` and `probe-delta-alerting.md` were modified by sibling seats during this audit (mtimes 05:55:43 / 05:55:56 local, 2026-10-20). The body read at start predates those edits; the provenance headers were re-read after. Re-run the checks below after siblings land.

## 1. Runnable local scripts vs missing webzites source

| Item | Location | Status | Evidence |
|---|---|---|---|
| `freshness-sweep.mjs` | `scripts/` | runnable | `node --check` OK; `--selftest` 15/15, exit 0; `--offline` exit 1 (§paths drift, see F1); `--section=history` exit 0 (SUSPENDED, pin-declared) |
| `probe-delta.mjs` | `scripts/` | runnable, input absent | `node --check` OK; default run and `--json` exit 2 (`ENOENT …/webzites/state/probe-history.jsonl`); `--bogus` exit 64 |
| `freshness-pins.json` | `corpus/knowledge/` | present, parses | `pathsMissSet` 55, `projectsChildrenSet` 14, `pathsFiles` 40, `probeHistoryAbsent: true` |
| `~/Projects/webzites/` (whole tree) | absent | missing | `state/`, `state/probe-history.jsonl`, `bin/webzites.mjs`, `scripts/kimi-surface.mjs`, `scripts/probe-delta.mjs`, `src/cli.mjs`, `src/probe.mjs` all ABSENT (pruned in the 2026-10-12 migration, per in-doc annotations) |
| `~/Projects/plazir-15-site` | absent | missing | cited by PQ-14 / sitemap gap checks |

Consequences:
- `probe-delta.mjs` cannot produce any event or coverage output on this host; every event claim in its doc is historical record only.
- `freshness-sweep` §history is suspended by pin (`probeHistoryAbsent`), so H2/H3/H4 do not evaluate. §armed (A1–A5) cannot evaluate without network and sibling repos; offline it reports `skipped(offline)`, complete=false.
- Runnable surface today is: §paths (offline), selftest, `--json` pin/verdict shape, and `probe-delta` error paths (exit 2/64).

## 2. Findings (severity order)

### F1 — HIGH: §paths is currently exit 1, contradicting the r20 resume claim
- Run: `node scripts/freshness-sweep.mjs --offline` → `VERDICT: DRIFT — §paths: 3 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1, partial: offline)`. JSON: `counts.drift 3`, `missSet 55`, `newMissing 0`, `complete true` for §paths.
- Unannotated occurrences (no absence vocabulary within ±2 lines):
  - `~/Projects/plazir-15-site` → `corpus/knowledge/drift-detection.md:73`, `corpus/knowledge/fleet-registry.md:53`
  - `~/Projects/webzites/bin/webzites.mjs` → `corpus/knowledge/free-read-verbs.md:317`
  - `~/Projects/webzites/scripts/kimi-surface.mjs` → `corpus/lessons/round-6-aggregator-audit.md:48`
- `freshness-sweep.md` resume note (`## Round-20 resume note`) states "the §paths run exits 0 with missSet still 55". That is false as of this run.
- `.ufo/round-20/resume/citation-disposition.json` lists all five locations (lines 30, 38, 94, 126, 166) as dispositioned; the in-file annotations at those lines are absent. `probe-delta-alerting.md` lines 82 and 84 carry annotations for the two webzites citations, but the citing lines that the scanner reads (`free-read-verbs.md:317`, `round-6-aggregator-audit.md:48`) are not in an annotated window. `fleet-registry.md` was modified at 05:55 today (sibling edit in flight) — may resolve itself.
- Recommended disposition for the lane owner: annotate the three sites in place (same rule as the other 26) or record the disposition explicitly; then correct the resume note's "exits 0" sentence. Do not re-pin `missSet` to hide them (doc itself forbids it).

### F2 — MEDIUM: freshness-sweep check table carries stale literals that its own rule forbids
The doc says "never copy a pinned literal into prose"; the table does exactly that and the copies disagree with `freshness-pins.json` (round 18, updated 2026-10-14):

| Doc row | Doc literal | Pins / live |
|---|---|---|
| A1 `charterGhpPin` | `2026-09-26 scribe beat` | pins `2026-09-30 scribe beat` |
| A1 `charterGhpLiveSha` | `fb365e38…` | pins `7c243a1d81…` |
| A1 `charterGhpChurnAfter` | `2026-09-29` | pins `2026-09-30` |
| P2 `pathsMissSet` | `10 entries, r17` | pins 55 |
| P2b `projectsChildrenSet` | `36 entries` | pins 14; live 20 (+6 informational) |
| P3 `pathsFiles` | `39-entry list` | pins 40; live scan 49 (+9 added) |
| Known-limits bullet | "now the real 39-entry list" | as above |

A1 values are the ones the armed watch compares against; a reader trusting the table would believe a different pin. The rows are labelled "r17"/"r16" in places but are presented in present tense in the table.

### F3 — MEDIUM: pin provenance stamp under-reports verification
- `freshness-pins.json` stamp: `"round": 18`, `"updated": "2026-10-14"`. The r20 correction (2026-10-19) re-verified `pathsMissSet` size 55 and the §paths result, but the stamp was not advanced. The pins' own comment says `round`+`updated` are "the re-pin stamp … every value carries the round that last verified it". Either re-stamp (no value changed, so this is a stamp-only edit in the pins file, same commit rule applies) or state in the pins file that stamp = last value change.
- `pathsFiles` is 40 entries in pins but the doc says 39 — the doc's count is from r17 and was never reconciled with the pinned list.
- `probeHistoryAbsent: true` has no date. The suspension of §history (which yields exit-0 `OK` in `--section=history`) is therefore undated and unexplained inside pins; the only date is in prose (2026-10-12 prune).

### F4 — LOW/MEDIUM: §history "SUSPENDED" yields OK verdict; historical counts non-reproducible
- `--section=history` → `VERDICT: OK (exit 0)` while the section is SUSPENDED. OK here means "nothing evaluated". Operators reading only the verdict see green. The `--offline` path correctly prints `complete=false` for §history; the `--section=history` path does not carry `complete=false`. Note for the lane owner, not a code claim I verified beyond this run.
- Every history-derived number in both docs (76/78 rows, 66/67 full sweeps, 6 events, 42.73h hole, "age 2.6h") is now unreproducible; `probe-delta-alerting.md` verified-at header already says "historical-not-live-reverified", which is accurate.
- Approximate timestamps `2026-09-29T02:4xZ` and `2026-09-29T03:2xZ` (freshness-sweep.md lines 78, 106) are placeholder-minute values; they are not reproducible stamps. Fine as prose, but they cannot be used as provenance.

### F5 — LOW: S019 contract path in both headers does not resolve under `corpus/`
- Both `verified-at`/`source` headers cite "metadata contract S019 (corpus/CORPUS.md, L1 registration pending)". `corpus/CORPUS.md` does not exist (`ls` and grep both fail). Candidate locations that do exist: `/home/vgpnk/Projects/shokunin/CORPUS.md` (lane root) and the canonical S019 input named in `corpus/SOURCES.md:27`, `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` (stat OK, mtime 2026-10-19 21:21). Path in headers should be corrected to the one L1 registers. (L1 owns SOURCES/README/SKILL; flag only.)

### F6 — LOW: consistency checks that pass
- Both `recheck:` commands are valid for this host: `grep -cF 'function scanCitations' scripts/freshness-sweep.mjs` returns 1; the probe-delta recheck's `test -r … || echo ABSENT` correctly reports ABSENT.
- `git log -1 -- scripts/freshness-sweep.mjs` → `02b6dd0` (2026-10-19 19:38), matching the header's "last touched in 02b6dd0"; the script is not in `git status`.
- Exit contract in both docs matches runs: freshness-sweep 0/1/2/64 (selftest proves 2 and 64); probe-delta 2 on unreadable, 64 on bad flag.
- `freshness-pins.json` `probeRowsFloor` 78, `probeFullSweepsFloor` 67, `probeSpotProbes` 11, `deltaEventsExact` 6, `pq2Remote`, `pq5Sha`, `plazirRemote`, `plazirUnpushed` 5, `plazirLiveSitemapLocs` 8 / `plazirSourceSitemapLocs` 7 all agree with the doc's table.
- `.ufo/round-20/{baseline-proof,candidate-proof}.json`, `.ufo/round-20/frozen/citation-locality/expected.json`, `.ufo/round-20/routing-blocker.json`, `.ufo/round-20/resume/citation-disposition.json` all exist.

## 3. Metadata date semantics (pair)

| Element | Value | Semantics check |
|---|---|---|
| `freshness-sweep.md` `verified-at` | 2026-10-19 (r20 correction + S014 run; r16/r17 records) | Matches r20 artifacts; but the §paths result claimed in the same entry no longer holds (F1). |
| `probe-delta-alerting.md` `verified-at` | original 2026-09-28, re-pins 2026-09-29 (r16), absence annotations 2026-10-14 (r18) and 2026-10-19 (r20) | Consistent with in-body annotations. Best-formed of the pair. |
| `freshness-pins.json` `updated` / `round` | 2026-10-14 / 18 | Not advanced for r20 verification (F3). |
| In-body "r18 re-census 2026-10-14" / "r20 citation-local 2026-10-19" | inline annotations | Dates match the headers; annotations in `freshness-sweep.md` line 94 and `probe-delta-alerting.md` lines 82/84 are correct about pruned paths. |
| Row/run dates: 2026-09-26 / 09-27 / 09-28 / 09-29 | prose | Historical; several conflict with pins (F2). |

## 4. Verification gaps / limitations
- Did not run default `freshness-sweep` (armed checks = network probes + sibling repo reads); armed verdicts are unverified.
- No webzites or plazir source tree on host; no history file; probe-delta event output unverifiable here.
- Two sibling edits landed mid-audit; F1 disposition for `fleet-registry.md:53` may change.
- Did not check git history beyond the single commit lookup.

## 5. Checks the main agent should run once siblings land
- `node scripts/freshness-sweep.mjs --section=paths --json` — expect exit 0 iff F1 is dispositioned; currently exit 1.
- `node scripts/freshness-sweep.mjs --selftest` — expect 15/15, exit 0 (passes now).
- `node scripts/probe-delta.mjs --json` — expect exit 2 while history absent.
- `grep -n "charterGhp" corpus/knowledge/freshness-sweep.md` vs `freshness-pins.json` (F2).

## 6. File changes by this seat
None to repo targets. Scratch only: `/tmp/kake-r21-w1-paths.json`, `/tmp/kake-r21-w1-offline.json`, `/tmp/kake-r21-w1-selftest.txt`, `/tmp/kake-r21-w1-paths.err`. Installs/updates: none.
