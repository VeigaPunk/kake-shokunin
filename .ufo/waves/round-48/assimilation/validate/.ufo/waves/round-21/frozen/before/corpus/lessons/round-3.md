# Lesson — round 3 (2026-09-28)

Cites: LOG.md round-3 entry; `drift-detection.md` fresh-probe table;
probe run `webzites probe --all` 2026-09-28T18:51Z; commit `round-3`.

## The gap closed

Round-1 corpus shipped citations only as fresh as 2026-09-26 fleet evidence.
This round ran the real probes (`webzites probe --all`,
`kimi-surface.mjs sync-check`) and found the snapshot stale in 48h:

- `lucario` config `live/maintained` vs reality: `lucario.kimi.page` never
  published (404); canonical moved to `veigapunk.github.io/lucario/` —
  fleet.config.json needs a row split or status fix (publish-queue item).
- `charter-ghp` marker `2026-09-26 scribe beat` already dead — daily scribe
  beats churn beat-dated pins within 48h (PQ-12 is real, not hypothetical).

## Learned

- **`status:live` in config is an assertion, not a fact** — it encoded
  intent ("should be live") for lucario. Probe verdicts are the only
  state worth citing; config fields are provenance.
- **Marker pins on rolling content (beats, dates, versions) decay
  guaranteed-fast** — pin-value choice should prefer content-stable literals
  over date-scoped ones where a stable literal exists; where none exists,
  budget a re-pin step in the republish runbook.
- **Corpus self-audit via its own commands** — the playbook's own step 1
  (`probe, don't guess`) caught round-1's stale claims. Eating the playbook's
  dogfood is the iteration loop.
