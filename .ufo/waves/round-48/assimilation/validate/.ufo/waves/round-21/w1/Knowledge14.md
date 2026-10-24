# Knowledge14 — ops-automation.md provenance trio (round 21, w1)

## Behavior
- Target: `corpus/knowledge/ops-automation.md` (only file edited).
- Starting state: no provenance trio; line 1 was `# Ops automation — timers, history, bot fleet`. Entry read in full (124 lines, 8841 bytes).
- Action: prepended `source:`, `verified-at:`, `recheck:` and one blank line before line 1 (pure prefix insertion, `PUT <1`).
- Result: 128 lines, 10001 bytes. Prefix = **4 lines, 1160 bytes**.

## Gates (run by me, read-only)
- Pre-edit sha256: `cf0d37d7b5e053c4ef47c0353012ba65c3d71de63a56ebb1ed44d6884515cb87` (124 lines, 8841 bytes).
- Post-edit: `tail -c +1161 | sha256sum` = `cf0d37d7b5e053c4ef47c0353012ba65c3d71de63a56ebb1ed44d6884515cb87`. All pre-existing bytes preserved byte-identically.
- Prefix line count verified as 4 (`grep -c ''` on head -n 4).
- No rechecks run. No credential/auth files read. No build/lint/test run.

## Metadata content and evidence basis
- `source:` derived from the entry's own evidence: systemd user units `webzites-{probe,keeper}.{timer,service}` (read 2026-09-28), `~/Projects/webzites/state/probe-history.jsonl` (78 rows, 09-20→09-29), `bin/webzites.mjs --help` (2026-09-28), `reports/keepers/grokbot-*.log.md`. States explicitly no corpus/SOURCES.md S-id applies. S019 cited as metadata-format authority only, not platform authority.
- `verified-at:` names original evidence dates (r13 2026-09-28T22:4x–22:5xZ; r16 probe-history re-read 2026-09-29T02:2xZ), records no git revision (none in entry), notes the r18 2026-10-14 absence annotation, and states `historical-not-live-reverified`, not a 2026-10-20 domain recheck.
- `recheck:` gives a read-only local command (`ls -l` on the three cited paths with `2>&1`) and an operator restore-or-retire requirement because the sources are absent since the 2026-10-12 prune/migration.

## Field-truth audit (no body edits)
- Local filesystem check (existence only, not a domain recheck): `~/Projects/webzites` absent; no `webzites*` entries under `~/.config/systemd/user/`. Consistent with the entry's pre-existing r18 absence annotations (lines 3–4 and 13–14 in the original). Those annotations were left untouched.
- `corpus/knowledge/keeper-timer-inert.md` and `corpus/knowledge/probe-delta-alerting.md` cited in the body both exist.
- Body claims (probe cadence, keeper DISABLED status, history row counts) were not re-derived; they remain historical.

## Out of scope / findings
- **S019 is not yet registered**: not present in `corpus/SOURCES.md`, and `corpus/CORPUS.md` does not exist yet. The `source:` line references it as pending L1 registration. L1 must register it before the metadata reference resolves.
- Count-field coverage is L1's job; not audited here.
- No other corpus files touched. SCORECARD, LOG, QUALITY, SOURCES, README, SKILL untouched.

## Tooling
- No installs or upgrades performed.

## Artifacts
- Edited: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/ops-automation.md`
- Report: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-21/w1/Knowledge14.md`
