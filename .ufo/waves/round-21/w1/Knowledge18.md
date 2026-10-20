# Knowledge18 — round-21 w1 report

Seat: scribe, leaf. Target: `corpus/knowledge/publish-queue.md` only. No commits; no other file edited.

## Behavior

- Read the whole entry (278 lines, 25,435 bytes at HEAD `5009eca`). It did not open with a provenance trio, so the prefix path was taken (not the audit-only path).
- Prepended four lines: `source:`, `verified-at:`, `recheck:`, and one blank line.
- No old byte changed. Verified by `git diff --stat` (4 insertions, 0 deletions) and a `tail -c +1186 | cmp` against `git show HEAD:` (byte-identical).

## Exact change

- Prefix length: **1,185 bytes, 4 lines** (3 metadata lines + blank). File grew 25,435 → 26,620 bytes.
- Old line 1 (`# Publish-queue readiness ledger (PQ-1..PQ-14)`) is now line 5. Existing corrections and absence flags (line-3 `r18 re-census` HTML comment, PQ-2/PQ-3/PQ-4/PQ-5 and PQ-14 annotations, `r20 citation-local` note at the r16 block) preserved byte-identically.

## Field basis

- **source:** `S019` referenced as metadata contract only (format authority, not platform authority), mirroring the convention already used by `corpus/knowledge/origin-repos.md`. Entry-specific evidence retained by name, rooted at `~/Projects/webzites` (round-9 lesson `round-9.md` line 4 and `freshness-pins.json` lines 84–101 both cite `~/Projects/webzites/reports/r9-*.md` and `fleet/fleet.config.json`). Also listed: `fleet/fleet.json` (2026-09-20 snapshot, entry line 5), `reports/r9-stale-markers.md`, `reports/dead-slot-recreate-readiness-r9.md`, `reports/sentinel-sourceless-extract-r9.md` (entry lines 7–9), `state/kimi-map.json` (entry line 13, 09-26 vintage).
- **verified-at:** names the latest in-entry live read, r16 (`2026-09-29`, `02:1x–02:3xZ`), with baseline r9 `2026-09-28`, charter `origin/main 9c28d29`, and plazir-15-site `origin/main bd02d10` vs HEAD `c814526`, as recorded in the entry itself. Marked `historical-not-live-reverified; no live domain recheck performed this round`. Today's date is not presented as a recheck.
- **recheck:** a local, read-only `test -e` loop over `fleet/fleet.config.json` and `reports/r9-publish-queue.md` under `~/Projects/webzites`, followed by the operator restore-or-retire requirement (sources vanished in the 2026-10-12 `~/Projects` prune). **Not executed** — no rechecks run, per assignment.
- No credential/auth files are referenced anywhere in the prefix or in this report.

## Evidence checked (local, read-only)

- `~/Projects/webzites`, `~/Projects/webzites/fleet`, `~/Projects/webzites/reports`: all absent (`ls` ENOENT). `~/Projects` listing also has no `webzites`, `plazir-15-site`, or `origin-work`.
- `corpus/CORPUS.md`: absent. `S019` is not in `corpus/SOURCES.md` (S001–S018 only) nor elsewhere in the repo outside `.ufo/waves/round-21/*.json` (boilerplate assignments).
- `git status` before the edit: `publish-queue.md` clean; only `origin-repos.md` was modified (a sibling).

## Out of scope / not done

- Count field coverage: L1 job; not touched.
- No change to SCORECARD, LOG, QUALITY, SOURCES, README, SKILL, or CORPUS (L1-owned). No change to `origin-repos.md` or any sibling.

## Limitations

1. **S019 not yet registered.** `corpus/CORPUS.md` does not exist at the time of this edit, and S019 is not in `SOURCES.md`. The `source:` line names S019 as the metadata authority per the assignment; L1 must register it in CORPUS.md this round or the reference dangles.
2. **Root inference.** `reports/*` root is `~/Projects/webzites/` (inferred from round-9 lesson and freshness-pins.json, not from the entry itself, which cites `reports/...` unrooted). `state/kimi-map.json` root is **not** verified — the entry cites it without a root and `freshness-pins.json` has no `kimi-map` entry; I wrote it under the webzites tree without a root claim in the prefix. Flagged here.
3. **Dates are historical.** `verified-at` is the r16 read of 2026-09-29; the r18 (2026-10-14) and r20 (2026-10-19) annotations in the body are absence notes, not re-verifications, and are not presented as such.
4. **Recheck not executed**, per assignment. The command is syntactically checked only by reading.

## Installs / updates

None.

## Artifacts

- Edited: `corpus/knowledge/publish-queue.md` (prefix only, +1,185 bytes, +4 lines).
- Report: `.ufo/waves/round-21/w1/Knowledge18.md` (this file).

## Checks for main agent

- Confirm `corpus/CORPUS.md` lands with S019 registered; if not, the `source:` line on `publish-queue.md` must be revisited.
- Optional: `git diff --stat -- corpus/knowledge/publish-queue.md` should report `4 insertions(+)` and nothing else.
