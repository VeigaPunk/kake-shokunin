# Round 21 · w1 · Knowledge02 — drift-detection provenance trio

Seat: scribe (leaf). Target: `corpus/knowledge/drift-detection.md` only. No commits, no rechecks run, no subagents.

## File change

- `corpus/knowledge/drift-detection.md`: prefixed 4 lines (`source:`, `verified-at:`, `recheck:`, blank line) before the existing `# Drift detection — live vs source` heading.
- Prefix length: **1108 bytes, 4 lines**. Old file 5795 B → new file 6903 B (5795 + 1108).
- Byte check: `git show HEAD:corpus/knowledge/drift-detection.md | cmp - <(tail -n +5 <file>)` → identical. No pre-existing byte was altered; the in-body absence notes (r18 at lines 4/7, r16 at lines 67–87, r20 at line 95) and the `in-sync*` and r16 "FALSE since 2026-09-26" corrections are untouched.
- The entry was not opened by a trio before this round, so no field-truth audit of existing trio fields was needed.

## Field basis

- **source:** derived from the entry's own evidence, not from any S-row. Named paths: `~/Projects/webzites/{bin/webzites.mjs, scripts/kimi-surface.mjs, src/probe.mjs}`, `state/probe-latest.json` (2026-09-28T18:51Z), `fleet/fleet.dedupe-report.md` (2026-09-26 record), and `~/Projects/plazir-15-site` (r16 2026-09-29 comparison). S019 is named as the metadata contract only and is explicitly not platform authority.
- **verified-at:** 2026-09-29 = latest original evidence date inside the entry (r16 at 2026-09-29T02:2xZ). Marked `historical-not-live-reverified`. It does not name today as a recheck.
- **recheck:** local read-only command `test -f ~/Projects/webzites/state/probe-latest.json && ls -l ...`, not executed. Operator restore-or-retire requirement stated for the vanished trees.

## Evidence the basis rests on (read-only)

- `find / -xdev` for `probe-latest.json`, `fleet.dedupe-report.md`, `kimi-surface.mjs` → no hits. `~/Projects/webzites` and `~/Projects/plazir-15-site` absent (`ls` error); entry's own r18/r20 notes say the same.
- `corpus/SOURCES.md` registry runs S001–S018 only; a grep of `corpus/` returned no S019 row. S019 metadata authority is therefore **not yet registered** in this checkout; the prefix cites it as pending L1 `CORPUS.md` registration, as instructed.
- Format reference: existing trio lines in `crawl-scope-per-host.md`, `ghp-custom-domain.md`, `ghp-etag-anatomy.md`, `ghp-served-set.md` (`source:` / `verified-at:` / `recheck:`).

## Findings / limitations

1. S019 does not exist in `corpus/SOURCES.md` yet. The prefix references it as pending; L1 must register it or this reference dangles.
2. The entry's source line lists `fleet/fleet.dedupe-report.md` without an explicit base; the prefix reads it as relative to `~/Projects/webzites`. Unverifiable since the tree is absent.
3. No domain or source-tree evidence was re-observed in this round; every claim remains historical.
4. Field-coverage counts across knowledge entries are L1's job and were not touched.

## Tools

No installs or upgrades performed by this seat.

## Checks for main agent

- Confirm the 4-line, 1108-byte prefix and `cmp` identity above on integration (no build/test required; markdown only).
- Confirm S019 registration by L1 in `corpus/SOURCES.md` / `CORPUS.md`.
