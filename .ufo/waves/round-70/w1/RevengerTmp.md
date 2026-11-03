# RevengerTmp — SCORECARD pointer reverse-engineering (kake r70, read-only)

Base `e5f6fd9e4c243d092160bc74e8bea24256087173`; bytes read with `git show e5f6fd9e:<path>`; host measured 2026-11-03T19:40Z; no counter run, no tracked edit, no lane git mutation.

## Reconstructed contract

- Base `SCORECARD.md` (4,727 lines): 11 `/tmp/kake-rNN` occurrences = 9 distinct tokens (r10–r18); 19 `~/...` occurrences = 6 distinct tokens; 5 bare `` `/tmp` `` mentions are excluded by C1 class (c); no `## Pointer calibration (round 70)` section exists, so every dangling token is unannotated.
- Move-log rows 10–18 each cite their own round's scratch dir; r17 is re-cited twice in the round-59 appendix (L4461 audit bullet, L4478 quoted cell). The contract says "12 tokens"; the bytes give 9 occurrences / 9 distinct in those rows (11 in the file) — the counter's regex, not the prose count, defines the population.
- Resolution semantics are existence (`test -e` / `git cat-file -e`), not evidence identity.

## `-S` hits: commit, subject, naming LOG line

| Commit | Subject | LOG.md line naming the round |
|---|---|---|
| `dd4eabff` 2026-09-28 | round-10: probe-delta detector + first checklist-executability audit (operability 6->8) | L15 "…round 10: closed the "alerting on `violated[]` deltas is undecided" gap… → `/tmp/kake-r10/`" |
| `72eb1126` 2026-09-29 | round-17 | L311-312 "round 17: freshness **HOLD 10 — live drift caught and repaired…"; L315-316 "artifacts under `/tmp/kake-r17/`" |
| `b0feb308` 2026-10-14 | round-18: freshness HOLD 10 — W7 mega-prune caught by standing gate; OMP/ufo-fsd re-census | L400-401 "round 18: freshness **HOLD 10 — W7 mega-prune caught by the standing gate…" |
| `ab6e100e` 2026-10-26 | round-59: build — id_resolver K8-K14 + hardening, S425/S426 entries and rows, crawler-identity correction, axis-table evidence cells, lesson, QUALITY/SKILL/README, C7 validation, wave-1 results | L2221 "## Round 59 — 2026-10-27"; L2224 "axis-table evidence cells re-pointed…" |

Introducing: `dd4eabff` (r10 token, SCORECARD created here) and `72eb1126` (r17 token, `~/DIRMAP.md`, `~/projects`); `b0feb308` marks `~/DIRMAP.md` gone and adds r18; `ab6e100e` only re-lists r17 files.

## Per-round table (every /tmp token at base)

No `.ufo/waves/round-{10..18}` exists at base or in history (`git log --all --diff-filter=A -- '.ufo/waves/round-1*'` empty; lowest wave dir is round-21), and `git ls-tree -r e5f6fd9e` holds none of the named basenames (`scout-claims.md`, `claims.tsv`, `claims-delta.tsv`, `reviewer-cites.md`, `scout-pins.md`, `scout-live.md`, `pq2-root.html`, `*-offline.out`). "Committed counterpart" below = surviving record only, never the artifact.

| Row | Token (line) | Cited artifact | Real in named round (evidence) | Committed counterpart | Host | Verdict |
|---|---|---|---|---|---|---|
| 10 | `/tmp/kake-r10/*` (L101) | lane reports, 9 named | LOG:15 (11 L2 probes → dir); lesson r10:4 | lesson `round-10.md` | missing | annotate |
| 11 | `/tmp/kake-r11/` (L100) | 13 L2 artifacts | LOG:17; row 11 names them | LOG r11 only (no lesson) | missing | annotate |
| 12 | `/tmp/kake-r12/` (L99) | 9 L2 artifacts | LOG r12; lesson r12 | lesson `round-12.md` | missing | annotate |
| 13 | `/tmp/kake-r13/` (L94) | 10 L2 artifacts | LOG:25,62 | LOG r13 only | missing | annotate |
| 14 | `/tmp/kake-r14/` (L93) | 12 L2 + sentinel sha pair | LOG:73,123 | LOG r14 only | missing | annotate |
| 15 | `/tmp/kake-r15/` (L92) | 12 L2 + sentinel + fetch bodies | LOG:137,199 | LOG r15 only | missing | annotate |
| 16 | `/tmp/kake-r16/` (L91) | 12 L2 artifacts | LOG:212,227,299; round-21 gate: dir only `selftest/`, no r16 file | lesson `round-16.md` | EXISTS (selftest fixture) | resolves by `test -e`, evidence absent — annotate; predicate cannot force |
| 17 | `/tmp/kake-r17/{…}` (L90,4461,4478) | scout-claims, claims-delta, critic, reviewer-cites, scout-pins, scout-live | LOG:311-397; round-21 gate: absent | lesson `round-17.md` | missing | annotate |
| 18 | `/tmp/kake-r18/` (L89) | before.json/out, after.out, after-offline.out | LOG:400-429; lesson r18:5; round-21 gate: absent | lesson `round-18.md` | missing | annotate |

## Home pointers (19 occurrences, 6 tokens)

| Token (lines) | Count | Host | Verdict |
|---|---|---|---|
| `~/Projects` (L66,77,89,90×2,92,4478) | 7 | exists | resolves — no action |
| `~/Projects/ds4cc-marketplace` (L60) | 1 | exists (36 entries, mtime 2026-10-27) | resolves — no action; row-19 "gone" is the 2026-10-14 record |
| `~/Projects/ufo-fsd-alpha` (L67,89) | 2 | exists | resolves — no action |
| `~/Projects/plazir-15-site` (L62,4261) | 2 | missing | annotate: 2026-10-12 W7 prune; no committed tree; live record in `publish-queue.md` |
| `~/DIRMAP.md` (L76,89) | 2 | missing | annotate: 2026-10-12 W7; no committed copy in the lane |
| `~/projects` (L77,90,4478,4642,4715) | 5 | missing | annotate; removal is W6 2026-09-29, not W7 (divergence 3) |

## Verdict per class

- `/tmp/kake-r10…r18`: annotation is the honest fix; re-pointing is impossible (no committed artifact copy, no wave dir ever). Each row: historical, non-executable, class "scratch-discipline cleanup" (session-scoped `/tmp`), cross-ref the lesson where one exists (10, 12, 16, 17, 18) or the LOG row otherwise (11, 13, 14, 15).
- Home: the 10 resolving occurrences need nothing; the 3 missing tokens get annotation rows too — a host tree has no repo-relative equivalent, and the nearest committed record (lesson/LOG/publish-queue) changes the claim, so re-pointing would be a content change, not a repair.
- No pointer in this population is repairable by re-pointing.

## SKILL.md /tmp cites (routed item 2)

L95 (run-time backup recipe), L356 (`/tmp/kake-r11/` historical live evidence), L359 (`/tmp/kake-r12/live/`) — plus L27/L227 `/tmp/kake-r12/live/` and L463-464 command strings — are procedure/historical, outside C1's population (enumerated from `SCORECARD.md` bytes only).
**Next round, not this one:** C1 is frozen to `SCORECARD.md` and neither claim's file set includes `SKILL.md`; editing it now is unmeasured scope that no predicate verifies.

## Divergences

1. The contract's "point at the committed counterpart where one exists" branch is empty for rounds 10–18: no wave dir, no committed artifact basename.
2. `/tmp/kake-r16` resolves but is not evidence: dir created 2026-11-03T18:50Z holding sweep selftest fixtures (`pins.json`, `sidecar/`, `annotated-only/`), matching base `scripts/freshness-sweep.mjs:1208` default `path.join(os.tmpdir(),'kake-r16','selftest')`; [INFERENCE] a `--selftest` run created it today. Round-21 recorded the same class on 2026-10-20 (only `selftest/`, `LatestGateRejections.md:11`). C1's `test -e` passes r16 unannotated; the base control stays red on the other 8 tokens; r16's status flips with selftest runs, so measurement order matters.
3. `~/projects` removal is W6 2026-09-29 (`SCORECARD` row 17; `LOG.md:311-316`), not the 2026-10-12 W7 prune; naming W7 would add a false date. Round-66's migration cell (2026-11-01) records `~/projects` as the exactly-recovered path (`SCORECARD:4642`): name W6 for removal, migration for this-host absence.
4. `~/Projects/ds4cc-marketplace` resolves again (36 entries, mtime 2026-10-27) though rows 18/19 record it gone in W7 — not dangling; the prose remains a true 2026-10-14 record.
5. Inline "pruned 2026-10-12" at L4261 is prose, not a calibration row; `~/Projects/plazir-15-site` still needs an exact-token row.
6. The frozen regex truncates `/tmp/kake-r10/*` to `/tmp/kake-r10` and `/tmp/kake-r17/{a,b}` to `/tmp/kake-r17`: no token is lost, per-artifact names are outside the population.
7. Contract count "12 tokens" ≠ measured 9 distinct / 11 occurrences.

## Confidence

- High: commit/LOG/path facts, token counts, host existence, absence of committed counterparts (all re-runnable with the commands quoted above).
- Medium: "real in round" for r16–r18 rests on LOG/lesson text plus the round-21 committed gate; production-time `/tmp` state is not observable now.
- No edits, no counter run; `/tmp/sc_base.md` deleted on exit.
