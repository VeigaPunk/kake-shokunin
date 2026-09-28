# Lesson — round 1 (2026-09-28)

Cites: LOG.md round-1 entry; this repo's `SKILL.md` rewrite commit `round-1`;
report `.ufo/reports/round-1/web-properties-publishing.md`.

## Worked

- **Fleet registry as ground truth.** `fleet.config.json` + dedupe-report
  gave verifiable per-row state (status/priority/expect/sourceDir) — no
  oral context needed. Every SKILL.md claim cites a file.
- **`sourceDir` null = republish hazard.** Rows without local source (vault,
  ufofsd, plazir27runson, kimi.pro slots) can only be republished from
  extracted live bytes; recorded so nobody retypes content from memory.
- **Publish-gate documentation.** kimi-surface-ops.md already proves the
  publish click is human; SKILL.md encodes prepare/verify as agent work and
  the click/​push as operator work.

## Failed / surprised

- **grep found ~40 site clones** under `webzites/repos/` — far more than the
  4 `~/Projects` candidates in the task brief. Lesson: `ls ~/Projects`
  undercounts; the registry's `sourceDir` fields are the real map.
- **`ufofsdbeta` looked like a site repo from its name** but is the UFO-FSD
  runtime (no `.github`, `dist/` is JS output). Lesson: name-matching site
  repos is unreliable; check for CNAME/workflows/index.html.
- **Byte equality is the wrong drift primitive on kimi** — injection +
  entity rewriting make it impossible by construction; only
  identity+vintage works. Cost a wrong instinct before reading the ops manual.

## Open

- `ds4cc.kimi.page` is ~18+ revs stale (PQ-2) — needs an operator-gated
  `update` fire + publish click.
- `plazir15.kimi.page` / `charter-ufo-fsd.kimi.page` 404s — `recreate` path
  documented, awaits operator fire + slug click.
- Probe tripwires still blind to content-level rot inside passing markers
  (needs `probe.mjs` feature work, not config).
