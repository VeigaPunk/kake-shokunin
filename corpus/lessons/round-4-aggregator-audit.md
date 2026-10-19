# round-4 aggregator corpus audit — kake

- **Round:** aggregator round-4 (steered; `.ufo/state/aggregator.round`=4), 2026-09-28.
- **Author:** aggregator lane (L1 m_qwen + one L2 `reviewer` subagent; non-author
  of the audited entries). Corrections are this new entry — no lane file edited.
- **Scope:** round-4 commit `6b1cd07` (round-5 `18537e9`, round-6 `8755018`
  excluded from the verdict): `knowledge/fire-journal-codes.md` (new),
  `fleet-registry.md` + `drift-detection.md` (audit fixes), `lessons/round-4.md`,
  `README.md`.
- **Method:** 16 citations independently re-executed against
  `~/Projects/webzites` per `CORPUS.md`. No live URLs hit; file-based probes only. <!-- r18 re-census 2026-10-14: ~/Projects/webzites absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->

**Verdict: NOT CONFORMANT at `6b1cd07`** — one major internal index
inconsistency (same-commit README contradicts the knowledge file it indexes).
**Fixed by the lane in round-5 (`18537e9`) before this lesson landed**; recorded
because the round-4 commit shipped it.

## Major defect (fixed round-5)

1. **Index row contradicted its own file at the same commit**:
   `git show 6b1cd07:corpus/README.md | grep -n '20 rows'` → line 15 "all 20
   rows", while `fleet-registry.md@6b1cd07` says 21 rows and
   `fleet.config.json` parses `len(sites)`=21. The lane corrected
   fleet-registry/SKILL in-round but missed the README mention. Fixed to "all 21
   rows" in `18537e9`. CORPUS.md: *an index row is a claim*; a correction must
   sweep every mention of the old value in the same round.

## What reproduced

- **Exit-code table completeness**: `grep -o 'code: [0-9]*'
  ~/Projects/webzites/scripts/kimi-surface.mjs | sort -u` → exactly {1..8, 64} —
  > *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*
  the corpus table is complete in both directions.
- **Registry census**: 21 rows = 12 live / 3 pruned / 3 broken / 3 queued;
  14 kimi-surface updatePath rows (JSON parse of `fleet/fleet.config.json`).
- **Pruned-semantics negative**: `grep -n pruned ~/Projects/webzites/src/probe.mjs` <!-- r18 re-census 2026-10-14: ~/Projects/webzites/src/probe.mjs absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  → exit 1, no matches — sweep reproduces the absence; fleet-registry documents it.
- **Clone count**: `ls ~/Projects/webzites/repos | wc -l` → 50. <!-- r18 re-census 2026-10-14: ~/Projects/webzites/repos absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
- **app.ds4cc.com rejection of the round-1 aggregator suggestion**: not among
  the 21 registry ids — the lane's rejection stands (AGGREGATE §9.4).
- **Observed-outcome table**: rebuild charter-ufo-fsd `efc1830` success,
  plazir15 code-6 post-`fired`, ds4cc mirror code-7 post-`fired` — journal files
  located under `state/` and match.
- `drift-detection.md` top-level `Source:` line present at `6b1cd07`
  (`git show …| head -6`). Zero-width scan clean.

## Minor defects

- `fire-journal-codes.md`: "lucario ×3 preflight-only / all stopped at
  canonCheck" over-generalizes — 2 of 3 lucario journals end at the lane/lease
  step (code 1); only `recreate-lucario-2026-09-27T153106522Z.json` reaches
  canonCheck with `fire:false` (`for f in state/recreate-lucario-*.json; do jq -r
  '[.steps[].name]|join(",")' "$f"; done`).
- `lessons/round-4.md` cites commit as "round-4" — resolvable by message but no
  hash named (`git rev-parse round-4` fails).
- Three `update-ds4cc-kimi-mirror` journals have malformed JSON (no parseable
  `steps[]`); the corpus ×7 count stands but those journals are undecodable —
  worth a row in the entry.

## Prior-audit defects — all three FIXED at `6b1cd07` (verified)

20→21 rows (`fleet-registry.md`); pruned-branch false mechanism claim (negative
sweep now documented); `drift-detection.md` missing Source: line.

## Gaps filed for next lane round

1. Correct the lucario outcome row (correction entry or lane-owned edit).
2. Note the 3 malformed ds4cc journals in `fire-journal-codes.md`.
3. Cite commit hashes, not subjects, in lessons.
