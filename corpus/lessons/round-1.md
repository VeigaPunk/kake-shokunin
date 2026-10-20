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

## Gate

Retrospective round-21 reconstruction, not original admission. This lesson was written 2026-09-28 without a gate section. The gate below is reconstructed from the existing record in round 21. It claims no new verification and no live-state recheck (historical-not-live-reverified).

Candidates (from the original sections):
- Worked: fleet registry as ground truth (lines 8-10); `sourceDir` null as republish hazard (lines 11-13); publish-gate documentation with the human publish click (lines 14-16).
- Failed / surprised: "~40 site clones" and `ls ~/Projects` undercounting, with the registry `sourceDir` fields as the real map (lines 20-22); `ufofsdbeta` is the runtime, not a site repo (lines 23-25); byte equality as the wrong drift primitive on kimi (lines 26-28).
- Open: `ds4cc.kimi.page` ~18+ revs stale, PQ-2 (lines 32-33); `plazir15` / `charter-ufo-fsd` kimi.page 404s (lines 34-35); probe tripwires blind to content-level rot (lines 36-37).

Historically supported outcomes (basis: `corpus/lessons/round-1-aggregator-audit.md`, 2026-09-28, aggregator L1 with an independent L2 reviewer lane):
- Worked, registry as ground truth: admitted with qualification. The audit re-observed the registry schema and vintage (`webzites-fleet-v1`, `updatedAt: 2026-09-26`) and the 14 kimi rows. Audit defect 1 found 21 registry rows, not the 20 used in other documents, so "ground truth" holds for per-row state only.
- Worked, publish gate: admitted with qualification. The audit re-observed the `scripts/kimi-surface.mjs` header ("publish is never automated"). The audit did not re-quote the human-click proof in `kimi-surface-ops.md`.
- Worked, `sourceDir` null as republish hazard: unverified. Not covered by the audit.
- Failed, "~40 site clones": not admitted as stated. The audit observed 50 clones under `webzites/repos/` at audit time (defect 2).
- Failed, `ls ~/Projects` undercounts and the registry `sourceDir` fields are the real map: qualified. The audit's gap list says a per-row `sourceDir` map covering all 50 clones does not exist; the registry covers only a subset.
- Failed, `ufofsdbeta` is runtime, not a site repo: admitted. The audit observed no `.github` workflow, `dist/` present, and `ufofsdbeta-kimi-review` not a git repo.
- Failed, byte equality on kimi: unverified. Not covered by the audit.
- Open, `ds4cc.kimi.page` stale: unverified and still open. The audit states the stale and broken states are 2026-09-26 report-sourced, not re-probed.
- Open, `plazir15` / `charter` 404s: unverified. The audit re-observed a preview-404 body size for the plazir27 entry only, which is a different row.
- Open, probe tripwires blind to content-level rot: admitted as an open problem, not resolved. The audit re-observed the marker check as a case-sensitive substring test (`probe.mjs:55`) and listed marker-inside rot as unseen.

Rejected candidates: not recorded. No rejection appears in lines 1-37, in `round-1-aggregator-audit.md`, or in the visible part of `LOG.md` line 4.

Outside spot-check: existing independent evidence is present in `corpus/lessons/round-1-aggregator-audit.md` (2026-09-28; aggregator L1 with an independent L2 reviewer lane; no network probe, deploy, or publish). It is a full audit with a NOT-conformant verdict, not an admit/reject spot-check sample. No separate round-1 spot-check record was found. `round-20-verifier-spotcheck.md` covers round 20 only.

Original-section cites: header lines 3-4 (`LOG.md` round-1 entry; `SKILL.md` rewrite commit `round-1`, which the audit resolves to `cd5b381`; report `.ufo/reports/round-1/web-properties-publishing.md`, whose cite the audit records as moved in r17); Worked lines 6-16; Failed / surprised lines 18-28; Open lines 30-37.

Round-21 lesson: not present in `corpus/lessons/` when this gate was written. The round-21 contract is `.ufo/waves/round-21/` (Lesson01 entry in `wave1-spec.json`).

Metadata and gate contract: S019 (`corpus/SOURCES.md` row S019, grade A) names the canonical Shokunin corpus contract. It requires round lessons to record candidates, admissions, rejections, and spot-check state. S019 is metadata authority, not platform authority. The canonical CORPUS.md was not readable at its registered path from this seat, so only the SOURCES.md row is cited.

Limits: historical-not-live-reverified; no domain recheck is claimed. The `~/Projects` paths cited by the audit are absent per its r18 annotations. Restore-or-retire is operator-owned.
