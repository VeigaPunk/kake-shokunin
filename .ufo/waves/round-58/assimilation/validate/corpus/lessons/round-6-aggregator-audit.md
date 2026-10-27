# round 6 aggregator audit — kake-shokunin

Provenance: aggregator L1 non-author review (scout lane), 2026-09-28, audit window
21:24Z–21:33Z. Repo HEAD at cutoff `dd4eabf` (round-10, committed 2026-09-28T18:24:51-03:00);
BRIEF dispatch state (`ed0b632`, untracked `SCORECARD.md` + `scripts/`) was superseded
mid-audit by that commit. Read-only; no network calls, no browsers, no mutating verbs.

Anchor revision: main-repo `PROTOCOL.md`/`ROADMAP.md` were being edited by the live
protocol lane during this audit (`wc -l PROTOCOL.md` 387 → 576; `sha256sum` →
`9e700d691307…`). Their line numbers below are soft — the quoted clause text is the
durable pointer.

## Verdict

**not conformant.** Failed rules:

- **CORPUS.md R4 — a count carries its command.** `corpus/knowledge/ops-automation.md:25`
  prints `total - ok = violated+errors` with no command and no validity window; the
  identity is false on **11 of 76** history rows
  (`node -e "…sum total vs ok+len(violated)+len(errors) per row…"` → `mismatch: 11`,
  rows 09-20T23:47:43→…). Routed at round 5 (aggregator lesson minor 4), acknowledged in
  `lessons/round-10.md`, still uncorrected in the corpus.
- **CORPUS.md R1 — knowledge entries cite a source.** The round-6/7/8 baselines cite
  sources that do not survive a fresh session: `sitemap-orphan-audit.md:3`
  (`/tmp/orphan-check.mjs`), `kimi-subpath-audit.md:3` (`/tmp/kimi-subpath-audit.json`),
  `ghp-subpath-spotcheck.md:3` (`/tmp baseline audit` — no artifact named at all),
  `vault-properties.md:11-12` (`/tmp/vault.html`).

Noted, not failed: R9's literal "never rewrites" is strained by dd4eabf's in-place rewrite
of two lane-owned claims plus a disclosed `*(r10 correction: …)*` note (cross-author
discipline itself is clean — no lane commit touches an aggregator-owned file). R7 passes
forward (14 README knowledge rows ↔ 14 files); the reverse direction leaves the four
aggregator lessons unindexed by convention.

## Re-executed citations

| claim (file:line) | command | observed | pass/fail |
|---|---|---|---|
| `len(sites)` = 21 (`fleet-registry.md:5`; README row) | `node -e "…fleet.config.json…"` | `sites: 21` | pass |
| 50-clone canonical map (`origin-repos.md:3`; README row) | `ls -1 ~/Projects/webzites/repos \| wc -l` | `50` | pass | <!-- r18 re-census 2026-10-14: ~/Projects/webzites/repos absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| PQ-1..PQ-13 (`publish-queue.md`; README row) | `grep -cE '^\| PQ-[0-9]+' publish-queue.md` | `13` | pass |
| detector `6 events / 0 phantom on 76 rows` (`SCORECARD.md:19`, README row) | `node scripts/probe-delta.mjs --history …/probe-history.jsonl --json` | `rows:76 … events:[6 entries]`, `fullSweeps:66`, `universe:18` | pass |
| naive diff `42 events / 40 phantom` (`SCORECARD.md:19`, `probe-delta-alerting.md`) | independent adjacency differ over the same file | `42` events (31 adjacent to a `total:1` row); the 40-phantom split is `[INFERENCE]`, not re-derived | pass (total), inference (split) |
| `12 ok / 5 violated / 1 error` (`SCORECARD.md:21`) | verdict histogram over `state/probe-latest.json` | `{"ok":12,"violated":5,"error":1}` at `18:51:26.128Z`; 5 FAILs = documented dead slots + charter-ghp beat marker; error = xsnapshot-app | pass |
| `exit 0/2/64 proven` (`SCORECARD.md:19`) | `node scripts/probe-delta.mjs [--history /nonexistent \| --hole-hours banana \| --since notadate]` | `0 / 2 / 64 / 64` | pass |
| "0 scripts in repo" before-state (`SCORECARD.md` move log) | `git ls-tree ed0b632 --name-only` | `AGENTS.md LOG.md PROVINCE.md SHONEN.md SKILL.md corpus` — no `scripts/` | pass |
| 76 rows, median gap 0.45h, 42.7h hole (`ops-automation.md:22-29`) | detector `--json` | `rows:76 medianGapH:0.45 maxGapH:42.73 hole 09-21T04:14:50.502Z→09-22T22:58:23.543Z` | pass |
| zip-exclude chain `:903` / zip spawn `:906` (`vault-properties.md:60`) | `sed -n '899,908p' ~/Projects/webzites/scripts/kimi-surface.mjs` | `:903` filter, `:906` spawnSync | pass (r10 fix) |
| `32MB fetchLive maxBuffer :339-346` (`lessons/round-9.md:33`) | `grep -n maxBuffer scripts/kimi-surface.mjs` + `sed -n '339,346p'` | `:342 … maxBuffer: 32*1024*1024` in the fn spanning :339-346 | pass (r10 fix) |
| `webzites status` exit-1 on violation (`SKILL.md` step 1) | `sed -n '95,102p' src/cli.mjs` | `:99` ternary on `"violated" \|\| "error"` | pass |
| kimi-surface has no `--help` (`SKILL.md` step 2) | `sed -n '1193,1200p' scripts/kimi-surface.mjs` | `:1197-1198` usage + `process.exit(64)` | pass |
| sole history writer `saveProbe` (`ops-automation.md`) | `sed -n '39,53p' src/fleet.mjs` | `export function saveProbe`, single append `writeFileSync` | pass |
| r5 flip-window correction | detector EXIT event | `veigapunk-page … at 2026-09-21T04:14:50.502Z since 2026-09-21T03:32:06.747Z` | pass (landed dd4eabf) |
| 2 352 paths / 103 locs / 75-of-93 stale (rounds 6/7/8) | requires live HTTP GETs | not re-executed (prohibited this round) | cannot-verify |
| "5 sourceless artifacts" (README row, `origin-repos.md:47`) | config scan: 8 rows lack `sourceDir` | the table's five are defined by zero-clone-hit, not by `sourceDir:null` (veigapunk-page has an Origin repo) | pass, scope-warning (5 ≠ 8, easy to conflate) |
| credential sweep (R8) | `grep -rnE 'op://\|sk-[A-Za-z0-9]{16,}\|BEGIN [A-Z ]*PRIVATE KEY\|ghp_[A-Za-z0-9]{20,}\|eyJ[A-Za-z0-9_-]{20,}' corpus/` | single hit = the grep-pattern text inside `lessons/round-5-aggregator-audit.md:54` | pass |

## Defects

1. **major — keeper timer claimed running; routed at round 5, uncorrected through round 10.**
   Standing claim: `SKILL.md:57-60` "The fleet is already instrumented … and
   `webzites-keeper.timer` runs `grokbot tick` daily" (also `corpus/README.md:20`
   "daily keeper timers"; `ops-automation.md:13` table row states no unit state).
   Falsifying command and output:
   `systemctl --user is-enabled webzites-keeper.timer` → `disabled`;
   `systemctl --user is-active webzites-keeper.timer` → `inactive`;
   `journalctl --user -u webzites-keeper.service -n 3` → `-- No entries --`;
   `grep -rn '## 2026-09-2[2-9]' ~/Projects/webzites/reports/keepers/grokbot-*.log.md | wc -l` → `0`.
   The sentence is byte-identical at `18537e9` and at HEAD (`git show 18537e9:SKILL.md`),
   so the claim was false at write time, not drifted. Required correction form: **appended
   entry** restating the sentence as "unit installed (2026-09-20 22:33), timer disabled,
   service never executed — the probe timer is the only live half", plus the three positive
   `is-enabled`/`is-active`/`journalctl` outputs; `ops-automation.md`'s table gains a state
   column. Owning lane: kake (round 11).
2. **major — round-10's axis artifact cites session-scoped evidence.** Standing claim:
   the SCORECARD/Move-log/LOG/lesson evidence for the operability move is
   `/tmp/kake-r10/*` (`SCORECARD.md:24`, `LOG.md:15`, `corpus/lessons/round-10.md:4`,
   `.ufo/reports/round-10/kake.md:9`). Falsified by the rule itself — a fresh-session read of
   the committed pointer cannot resolve `/tmp` (28 files exist only in this boot).
   Required correction form: append the durable pointers (the two round-10 evidence reports
   already live in `~/Projects/webzites/reports/`, and the detector + `probe-delta-alerting.md` <!-- r18 re-census 2026-10-14: ~/Projects/webzites/reports absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
   are committed) and mark the `/tmp` paths as session-local provenance, never evidence.
   Owning lane: kake.
3. **major — future-dated evidence labels in committed corpus files, two instances.**
   (a) `kimi-subpath-audit.md:3` and `lessons/round-8.md:4` carry `~21:15Z`, shipped in
   `9544914` at **19:49:59Z** (85 min in the future at the shipping commit);
   `/tmp/kimi-subpath-audit.json` mtime `19:46Z` bounds the real run.
   (b) **new, not yet routed:** `sitemap-orphan-audit.md:3,62` and `lessons/round-7.md:4`
   carry `~20:20Z`, shipped in `83d08e4` at **19:39:21Z**;
   `/tmp/orphan-check.mjs` mtime `19:35Z` bounds the real run.
   Required correction form: appended entries with the real UTC run times (derived from
   artifact mtimes/commit times), never a silent edit. Owning lane: kake.
4. **major — falsified count uncorrected after routing.** `ops-automation.md:25`
   `total - ok = violated+errors`, false on 11 of 76 rows (command in the table above);
   routed as the round-5 aggregator lesson's minor 4, acknowledged in `lessons/round-10.md`,
   still uncorrected. Required correction: append the validity window (the 09-20T23:47:43→
   09-21T01:33 early rows carry one unaccounted row each) or the missing-state explanation.
5. **major — lane commit identity.** PROTOCOL.md:502-503 asserts round commits carry
   `<lane>-shokunin` / `<lane>@shokunin.local` and names kake among the lanes that "already
   do". Observed: `git log --format='%an <%ae>'` → 12 of 14 commits by
   `Joao Pedro Veiga <jpveigao10@gmail.com>`, including round-8 `9544914`, round-9 `ed0b632`,
   round-10 `dd4eabf`; only `83d08e4` (round-7) uses `kake-shokunin <kake-shokunin@local>`;
   `git config --local user.name` → exit 1 (unset). Required correction: set the repo-local
   identity (lane may self-fix per the lane-identity invariant) and append the correction.

Minor: (6) SCORECARD scores carry no counting command / measured-against commit, contrary to
PROTOCOL.md's SCORECARD row; (7) the round-10 report cites no commit hash (subject only —
MANIFEST round-5 precedent calls this a conformance defect); (8) `ghp-subpath-spotcheck.md:3`
names no artifact for its 2 352-path baseline; (9) the freshness row says last change r9 while
carrying round-10 evidence text; (10) U+200B still at `lessons/round-1.md:16`; (11) four
aggregator-owned lessons carry no README index row.

## Fleet-2 axis-framework state

`SCORECARD.md` exists (2201 B) and is **committed** (`git ls-files SCORECARD.md` → tracked in
`dd4eabf`; it was untracked at dispatch). Contract fields present: axes (score + evidence
pointer + last-change round), `planned`, `retired`. Declared axes `operability` + `freshness`
match `MISSION.md:15`. A before→after is recorded for the claimed round (`## Move log`, row 10)
and the before-state verifies ("0 scripts in repo" → confirmed against `ed0b632`'s tree).
Verified score claims: 6 events/0 phantom on 76 rows, exit 0/2/64, 12 ok/5 violated/1 error
(0 new). Gaps: no counting command / no measured-against commit on either score; the
operability evidence pointer and the move-log Evidence field point at `/tmp/kake-r10/*`;
planned round 11 (both owned axes at 8) is consistent with the round counter
(`.ufo/state/kake.round` = 10).

## Routed-defect rows for the ledger

```
kake | keeper timer claimed running (SKILL.md:57-60, README.md:20, ops-automation.md:13) | r5 | open | systemctl --user is-enabled webzites-keeper.timer → disabled; is-active → inactive; journalctl --user -u webzites-keeper.service -n 3 → -- No entries --
kake | round-10 evidence pointers are /tmp/kake-r10/* (SCORECARD.md:24, LOG.md:15, lessons/round-10.md:4, .ufo/reports/round-10/kake.md:9) | r6 | open | fresh-session read of committed pointer: /tmp is session-scoped (PROTOCOL r9: "evidence pointers must resolve at closure (no tmpfs/local://)")
kake | future-dated evidence label ~21:15Z (kimi-subpath-audit.md:3, lessons/round-8.md:4) | r6 (ROADMAP) | open | shipped in 9544914 @19:49:59Z; label 21:15Z; /tmp/kimi-subpath-audit.json mtime 19:46Z
kake | future-dated evidence label ~20:20Z (sitemap-orphan-audit.md:3,62, lessons/round-7.md:4) | r6 (new) | open | shipped in 83d08e4 @19:39:21Z; label 20:20Z; /tmp/orphan-check.mjs mtime 19:35Z
kake | total - ok = violated+errors uncorrected (ops-automation.md:25) | r5 | open | node -e per-row sum vs total → mismatch: 11 of 76 rows
kake | lane commit identity not used (12/14 commits operator personal identity incl. r8/r9/r10) | r6 | open | git log --format='%an <%ae>'; git config --local user.name → exit 1 (unset); PROTOCOL.md:502-503 asserts kake already does
kake | round-10 report cites no commit hash | r6 | open | .ufo/reports/round-10/kake.md:3 "Commit `round-10`" (subject only)
kake | 8/8 kake reports r3–r10 lack the SHONEN section | r6 | open | grep -ril shonen .ufo/reports/round-{3,4,5,6,7,8,9,10}/kake.md → no match
kake | ghp-subpath-spotcheck.md:3 names no artifact for its 2 352-path baseline | r6 | open | corpus/knowledge/ghp-subpath-spotcheck.md:3 "/tmp baseline audit" (no filename)
kake | SCORECARD scores lack counting command + measured-against commit | r6 | open | kake-shokunin/SCORECARD.md axes table (prose evidence only)
kake | CDP-9222 lease ownership kake↔kagi unadjudicated | r5→ | open | ROADMAP.md "Contested rulings still open"; no ruling artifact
kake | charter-ghp marker re-pin handed to keeper, unapplied | r9 | open | grep -n '2026-09-26 scribe beat' ~/Projects/webzites/fleet/fleet.config.json → :256 unchanged; probe-latest charter-ghp marker FAIL <!-- r18 re-census 2026-10-14: ~/Projects/webzites/fleet/fleet.config.json absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
```

## Round-20 citation-local note (base `cb807bc`; table-distance uncleared)

> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*