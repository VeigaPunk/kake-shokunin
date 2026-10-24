# Knowledge11 — keeper-timer-inert provenance trio (round 21, wave 1)

## Scope
- Target: `corpus/knowledge/keeper-timer-inert.md` (only file changed).
- Entry read in full before editing (174 lines, 11485 bytes at HEAD).
- Starting state: no provenance trio present (first line was the `# Keeper timer inert` heading). Field-truth audit of existing trio: not applicable.

## File change
- Prepended exactly 4 lines (3 trio lines + one blank line): `source:`, `verified-at:`, `recheck:`, blank.
- **Prefix length: 1049 bytes** (`grep -b` offset of the heading line; the heading now begins at byte 1049, line 5). File grew 11485 → 12534 bytes (= 11485 + 1049).
- No pre-existing byte altered. Check: `tail -c +1050 | sha256sum` = `a7f8379f14c829a0…`, identical to `git show HEAD:corpus/knowledge/keeper-timer-inert.md | sha256sum` (same prefix `a7f8379f14c829a0…`). Byte-identity verified against HEAD.
- Preserved intact: all r12/r13/r16/r18 in-file annotations, the "Correction to r5" section, the operator-decision section, and the L0 question reference.

## Trio content and evidence basis
- `source:` — own-work, derived from the entry's own evidence: read-only `systemctl --user` status/show/is-enabled/is-active/list-timers captures and `journalctl --user -u webzites-keeper.service` ("No entries"), plus unit files read 2026-09-28. S019 cited as metadata contract only (metadata authority, not platform authority). S019 is not yet registered: `corpus/SOURCES.md` lists S001–S018 only, and no `CORPUS.md` exists in the tree yet (L1 registers it this round).
- `verified-at:` — original capture 2026-09-28T22:18Z; r13 re-read 2026-09-28T22:4x–22:5xZ; in-file revisions r12–r18. Marked `historical-not-live-reverified`. No current-host or domain recheck is claimed; "today" is not used as a verification date.
- `recheck:` — states the source vanished (r18 re-census 2026-10-14: unit files absent after the 2026-10-12 `~/Projects` prune, as the entry's own annotations record). Concrete safe local reading command: `systemctl --user is-enabled webzites-keeper.timer; test -e ~/.config/systemd/user/webzites-keeper.timer && echo present || echo absent`. Operator restore-or-retire requirement stated explicitly. The command was not run.

## Evidence locations
- Target lines 3–14 (sources and r18 annotations), 16–55 (verbatim state), 120–151 (r5 correction and operator decision).
- Registry: `corpus/SOURCES.md` (S001–S018 only; no S019 row).
- Convention references: `corpus/SOURCES.md` S014 (own-work source form), `.ufo/waves/round-21/wave1-spec.json` (Knowledge11 item, metadata contract text).

## Tools
- No tools installed or updated.

## Limitations
- Operator-side constraints honored: no rechecks run, no `/tmp/kake-r12` reads, no credential/auth files read, no `omp` CLI launched, no systemctl state changed.
- S019 is referenced but unresolvable until L1 registers `CORPUS.md`; the source line flags this rather than inventing a registry row.
- The `.ufo/l0-questions.md` decision file cited by the entry was not opened by this seat.
- Field coverage counts across the corpus are L1's job and were not audited here.

## Checks for main agent
- Confirm S019 registration in `CORPUS.md` matches the metadata contract wording used here.
- Confirm the prefix line count (4) against the round-21 C1 "first 8 lines" target (heading lands on line 5).
