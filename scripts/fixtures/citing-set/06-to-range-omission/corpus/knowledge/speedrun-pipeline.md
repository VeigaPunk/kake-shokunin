source: operator-local pipeline evidence cited in-entry - `docs/SPEEDRUN-PROTOCOL.md`, `src/speedrun.mjs`; registry-backed for the round-20 artifact correction.
verified-at: 2026-10-21 - historical record, not live reverified
recheck: on protocol change - `grep -cF 'speedrunStage' scripts/speedrun.mjs` (expect 1)

# Speedrun pipeline

The round-20 correction sweep covers registry rows S001 to S006 of the
artifact-membership block. Every row in that span was opened on the same day
and carries its own anchor.

Round-26 source recheck (2026-10-21, append-only; original lines unchanged).
The correction sweep was re-fetched and judged HOLD at its anchors.
