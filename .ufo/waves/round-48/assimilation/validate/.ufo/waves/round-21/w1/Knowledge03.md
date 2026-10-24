# Knowledge03 — fire-journal-codes.md provenance trio (round 21, w1)

## Behavior
- Target: `corpus/knowledge/fire-journal-codes.md` (only file changed).
- Before: no provenance trio; line 1 was `# kimi-surface fire journals & exit codes`.
- Change: prepended 4 lines (pure `PUT <1:` insertion): `source:`, `verified-at:`, `recheck:`, blank line.
- Prefix length: **726 bytes** (4 lines, each newline-terminated). Old heading now at line 5; old body unchanged (file total now 6790 bytes, so pre-existing content is 6064 bytes at byte offset 726).
- Preserved: all original lines, including the r20 citation-local correction (now line 8), the r16 re-count corrections, the rule/absence flags, and the `Source:` body line (now line 7).
- Not run: the `recheck:` command. No credential or auth paths referenced. No commit, no other files touched.

## Field truth (audit)
- `source:` — names the same evidence the body names: `kimi-surface.mjs` die/throw sites, `state/{update,recreate,rebuild}-*.json` journals, `state/rebuild-charter-fire.log`. Labeled own-work (no SOURCES.md id; S014 is a different own-work row).
- `verified-at:` — 2026-09-28 matches body "throw sites, 2026-09-28"; 2026-09-26/09-27 matches "Observed run outcomes (state/ 09-26→09-27)". Labeled historical-not-live-reverified. The later r16 journal re-count (28 journals) is not in verified-at; noted as limit.
- `recheck:` — read-only `test -e` and `grep -lE '"fire": *true'` over the `recreate-plazir15-*.json` glob (the three fired journals in the body). Script-vanished note gives operator restore-or-retire requirement.

## Metadata authority
- S019: no match in `corpus/` (grep found none in SOURCES.md or any entry); no `CORPUS.md` exists yet (glob empty). Prefix cites S019 as metadata authority only, pending L1 registration. S019 content was not invented or relied on for any claim.

## Findings and limits
- Script `kimi-surface.mjs` absence rests on the preexisting r20 correction (2026-10-19), not re-verified live this round.
- Journal JSON spacing for `"fire": true` is unobserved ([INFERENCE]); the recheck regex may need adjustment if the format is compact.
- No tools installed or updated. No builds, tests, or checks run.
- Coverage counting left to L1.
