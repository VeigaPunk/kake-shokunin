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

## Gate

Retrospective round-21 reconstruction, not original admission. The original lesson (commit `ddf40e2`, subject `round-3`, 2026-09-28; 29 lines before this Gate) recorded no candidates list, no rejects, and no spot-check. Everything below was reconstructed on 2026-10-20 from `corpus/lessons/round-3.md` §The gap closed (lines 6-16), §Learned (lines 18-29), `LOG.md:5`, `corpus/knowledge/drift-detection.md:4,46-56`, and `corpus/lessons/round-7.md:29-34`. No probe, fetch, or live-state re-verification was run for this Gate. The round-21 lesson file `corpus/lessons/round-21.md` does not exist yet; `S019` names it as its `used-by`, so the round-21 provenance cited here is the wave contract `.ufo/waves/round-21/wave1-spec.json` (context C2).

Candidates and historically supported outcomes (2026-09-28 snapshot only):

- **Lucario row:** config `status: live/maintained` contradicted by the 2026-09-28T18:51Z probe (404, never published); canonical moved to `veigapunk.github.io/lucario/`. **Admitted with qualification** as a 2026-09-28 snapshot finding (`drift-detection.md:46-56`, `LOG.md:5`). The `fleet.config.json` row split or status fix named in the lesson is **unverified**: no corpus record shows it landed, and that config lives outside this corpus.
- **charter-ghp beat marker:** pin `2026-09-26 scribe beat` dead within 48h. **Admitted with qualification**: fresh-probe row (`drift-detection.md:56`) and second consecutive failure (`round-7.md:29-34`). Round-7 records that the round-3 re-pin "was extracted but never landed in `fleet.config.json`" and was recorded, not edited. That is a documented non-landing, not a round-3 claim.
- **Learned: `status:live` is an assertion; probe verdicts are the only citable state:** **Admitted with qualification** as method. `SKILL.md:67` carries "Trust hierarchy: live probe > config fields" at read time.
- **Learned: prefer content-stable literal pins; otherwise budget a re-pin step:** historically documented method. `corpus/knowledge/publish-queue.md:32` at baseline 5009eca (PQ-12; current line 36) is consistent with it. The “budget a re-pin step” clause remains unverified: no runbook location was checked.
- **Learned: corpus self-audit via its own commands (step 1 caught round-1 stale claims):** **Unverified** as a measured outcome. It rests on the `LOG.md:3-5` narrative only; no independent check exists in the corpus.

Rejected: not recorded. Neither the original lesson nor `LOG.md:5` lists rejected candidates or reasons.

Outside spot-check: **not recorded.** No non-author verifier entry for round-3 was found in `LOG.md`, `corpus/lessons/`, or `.ufo/`. `corpus/lessons/round-20-verifier-spotcheck.md` is round-20 scoped by name and was not opened or cited here.

Scope limits: the evidence is time-scoped to the 2026-09-28 probe run. The r18 re-census (2026-10-14, `drift-detection.md:4`) records the webzites tree as absent after the 2026-10-12 `~/Projects` prune, so no original source path can be re-read now. This Gate makes no present-day claim about lucario, charter-ghp, or any row.

Corpus contract: `S019` (`corpus/SOURCES.md:27`; tier A; scope "provenance metadata and recorded lesson gates ... not verification of historical platform claims") is the metadata authority for this section. Its scope claims no platform authority, and this Gate claims none.

Net: round-3's freshness correction for the 2026-09-28 snapshot is admitted with qualification. The config-row fix, the runbook budget clause, and the self-audit outcome are unverified. The outside spot-check is not recorded.
