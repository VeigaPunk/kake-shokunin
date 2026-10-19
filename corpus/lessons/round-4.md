# Lesson — round 4 (2026-09-28)

Cites: LOG.md round-4 entry; `knowledge/fire-journal-codes.md`;
`~/Projects/webzites/scripts/kimi-surface.mjs` throw sites (grep `code: [0-9]`, *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*
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
