# Lesson — round 4 (2026-09-28)

Cites: LOG.md round-4 entry; `knowledge/fire-journal-codes.md`;
`~/Projects/webzites/scripts/kimi-surface.mjs` throw sites (grep `code: [0-9]`,
> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*
2026-09-28); `~/Projects/webzites/state/{update,recreate,rebuild}-*.json`;
`state/rebuild-charter-fire.log`; commit `round-4`.

## The gap closed

Rounds 1+3 documented the kimi-surface *verbs* (update/recreate/rebuild) and
probe semantics, but nothing taught how to read a finished run. `state/` holds
15+ run journals whose `error.code` values had no decoder in the corpus —
exit code alone does not reveal whether the metered fire was consumed. An
agent reading code 6 or 7 without the journal could either refire (burning a
second metered chat fire, risking orphaned version cards) or abandon a run
that actually succeeded.

## Evidence mined

- **Code table extracted from throw sites** in kimi-surface.mjs: codes 1–8, 64;
  the decisive split is pre- vs post-`fired` step, not the number.
- **Rebuild end-to-end success pattern** (charter-ufo-fsd-kimi, 09-26):
  version card `efc1830` claimed, preview 200+marker, terminal
  `liveAfter.stillDead:true` — a *successful* recreate/rebuild leaves the
  live slot at 404; the human publish click is the flip.
- **Anomaly signatures**: plazir15 recreate code 6 post-fire ("never
  navigated to /chat/<uuid>"), ds4cc-kimi-mirror update code 7 post-fire
  (session expired at ListVersions baseline) — both consumed fires with
  uncertain card state.

## Learned

- **Meter consumption is a journal fact, not an exit-code fact.** `fire:true`
  + a `fired` step = consumed; codes 5 and pre-`fired` 4s = clean abort.
- **Post-fire codes 6/7 are ANOMALY class** — operator inspects the chat;
  blind refire is the documented mistake.
- **Success looks like failure on the live URL** — `stillDead:true` is the
  correct terminal state pre-publish; teaching this prevents bogus retries.
- Corpus gain pattern: the richest un-mined evidence was `state/*.json`
  run journals — artifacts produced by earlier missions that the playbook
  referenced (verbs) but never decoded (outcomes).

## Gate

Label: retrospective round-21 reconstruction (wave 1, Lesson10 seat), not the original 2026-09-28 admission. This file had no Gate before this append. No live state was re-verified; the webzites checkout remains absent after the 2026-10-12 prune, so the original recipes are historical records only.

Original sections reconstructed: `## The gap closed` (line 9), `## Evidence mined` (line 19), `## Learned` (line 32). Round-21 lesson: no `corpus/lessons/round-21.md` existed at read time (last lesson file: `round-20.md`); this reconstruction is recorded at `.ufo/waves/round-21/w1/Lesson10.md`.

Corpus contract: S019 is the metadata/gate contract named by the round-21 wave spec. It is not present in `corpus/SOURCES.md` at read time (registry ends at S018) and `corpus/CORPUS.md` did not exist, so no claim below rests on S019 content. S019 is metadata authority only, not platform authority.

Candidates considered and outcomes (historically supported only):

- **C-a: code table {1–8, 64} from kimi-surface throw sites; decisive split is pre- vs post-`fired`.** Admitted with qualification. `corpus/lessons/round-4-aggregator-audit.md:30-31` records the `grep -o 'code: [0-9]*'` sweep returning exactly {1..8, 64} on 2026-09-28. The source file is absent now (audit line 32 annotation); the basis is that historical sweep only.
- **C-b: rebuild success pattern (charter-ufo-fsd-kimi, 09-26; card `efc1830`; terminal `liveAfter.stillDead:true`).** Admitted with qualification. Audit `round-4-aggregator-audit.md:41-42` located the state journal and matched the success outcome. Single-instance basis.
- **C-c: anomaly signatures — plazir15 recreate code 6 post-`fired`; ds4cc-kimi-mirror update code 7 post-`fired`.** Admitted with qualification. Audit `:41-42` matched both journals. Qualification: audit `:56-58` reports three `update-ds4cc-kimi-mirror` journals with malformed JSON (no parseable `steps[]`); those are undecodable and this is not a complete census.
- **C-d: meter consumption is a journal fact (`fire:true` plus a `fired` step); code 5 and pre-`fired` 4s are clean aborts.** Unverified. No independent check of the 5 or pre-`fired` 4 semantics is recorded. Related: audit `:49-53` found the lucario "all stopped at canonCheck" generalization over-reached (2 of 3 end at code 1); recorded here, not corrected.
- **C-e: post-fire 6/7 are ANOMALY class; blind refire is the documented mistake.** Unverified as doctrine. Instances exist (C-c); the prescriptive rule was not checked.
- **C-f: success looks like failure on the live URL (`stillDead:true` is correct pre-publish).** Admitted with qualification, on the single C-b instance only.
- **C-g: `state/*.json` run journals were the richest unmined evidence.** Unverified methodological claim; no independent check recorded.

Rejected candidates: not recorded. Neither the original sections nor the audit document a rejection for this lesson.

Outside spot-check: existing independent evidence is `corpus/lessons/round-4-aggregator-audit.md` (2026-09-28; aggregator L1 plus one L2 reviewer, non-author of the audited entries; 16 citations re-executed; overall verdict NOT CONFORMANT at commit `6b1cd07`, driven by a README index defect fixed in round-5 `18537e9` and absent from this lesson). That audit does not record an admit/reject pair for this lesson's claims. Admit/reject spot-check: not recorded.

Open items, not repaired here: the commit cited as `round-4` has no hash (audit `:54-55`; `git rev-parse round-4` failed at audit time; not re-run). The three malformed ds4cc journals (audit `:56-58`) remain undecodable. Original text and line numbers are preserved byte-for-byte; this append is the only change.
