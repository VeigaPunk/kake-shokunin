# Knowledge19 — sitemap-orphan-audit.md provenance trio (round 21, w1)

## Behavior
- Target: `corpus/knowledge/sitemap-orphan-audit.md` (only file changed by this seat).
- Pre-edit state: no provenance trio; first line was the H1 heading. Trio was absent, so it was prepended.
- Change: pure head insertion of 4 lines (3 trio lines + one blank line). Prefix = **1093 bytes**, 4 lines.
- Verified after edit: `current=9384`, `HEAD=8291`, prefix 1093 bytes; the suffix from byte 1094 onward is byte-identical to `git show HEAD:` for that path (`cmp` exit 0). Only the file's own status shows `M`.
- Preserved unchanged: the whole body, including the r20-correction block at lines ~114-123 and all absence flags, the baseline table, and the "Charter marker churn" section.

## Prefix contents and evidence basis
1. `source:` — entry-specific evidence named in the body: `/tmp/orphan-check.mjs` baseline 2026-09-28 (103 sitemap locs), `pages.yml` deploy-graph reads for ds4cc-marketplace and plazir-15-site, `fleet.config.json`, live sitemap.xml fetches. Plus S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections, with the S001 pinned `action.yml` URL at `7b1f4a7` §Archive artifact. S001/S002/S004/S006 are registered in `corpus/SOURCES.md` (rows S001, S002, S004, S006 read this round). The pinned-URL form follows `ghp-served-set.md`'s trio.
2. `verified-at:` — original evidence date 2026-09-28 (~20:20Z), r16 re-read 2026-09-29T02:2xZ (copied as written in the body), r20 quote corrections 2026-10-19 with base `cb807bc`. Marked `historical-not-live-reverified`; no live fetch or domain recheck was made this round.
3. `recheck:` — trigger, a local reading command run from kake-shokunin (`grep -nF 'include-hidden-files' corpus/knowledge/ghp-served-set.md corpus/SOURCES.md`; verified locally to match, never executed as a recheck), and a source-vanished clause.

## Source-vanished findings (operator action required)
Checked with `test -e` / `find` on this workstation; not present:
- `/tmp/orphan-check.mjs` — absent.
- `ds4cc-marketplace/.github/workflows/pages.yml` and `plazir-15-site/.github/workflows/pages.yml` — absent under `/home/vgpnk/Projects/` (repo checkouts not present; `find` depth 6 found only `burnerchrome`'s pages.yml, unrelated).
- `fleet.config.json` — not located under `/home/vgpnk/Projects/shokunin` (glob) or depth-6 find.
- `docs/FLEET-MAP.md` — absent from kake-shokunin.
- Operator requirement (recorded in the `recheck:` line): restore these at the cited paths or retire the 2026-09-28 baseline counts (103 / 93 / 8 / 2) from the entry.

## S019 metadata contract — not available
- `corpus/CORPUS.md` does not exist yet (glob of `corpus/` shows QUALITY.md, README.md, SOURCES.md only).
- `S019` appears in no file under `corpus/`; `SOURCES.md` registers only S001-S018. The only `S019` text is in round-21 dispatch/spec files.
- Consequence: the trio shape was copied from the sibling entries that already carry it (`ghp-served-set.md`, `ghp-custom-domain.md`, `crawl-scope-per-host.md`), not from a readable S019 contract. L1 should confirm the shape once CORPUS.md is registered; if it differs, this entry's 3 lines need a prefix-only update.
- S019 is not cited as a platform authority in the entry. Source lines cite only S001/S002/S004/S006 and entry-specific local evidence.

## Verification performed
- Read target fully before editing; read `ghp-served-set.md` as the trio precedent; checked SOURCES rows S001-S006 and S017-S018 (all pre-existing rows; no edits to SOURCES).
- No rechecks run; no credential/auth files read; no network calls; no `omp` CLI launched; no subagents spawned.

## Tools
- None installed or updated.

## Files changed
- `corpus/knowledge/sitemap-orphan-audit.md` — 4-line head prefix (1093 bytes). No other files written except this report.

## Checks for main agent
- Confirm `grep -c '^verified-at:\|^recheck:\|^source:' corpus/knowledge/sitemap-orphan-audit.md` equals 3 (done implicitly by edit; not re-run here).
- Once CORPUS.md lands, reconcile trio shape with S019 (see above).
- Count-field coverage is L1's job; not touched.

## Limitations
- Trio is historical metadata only; nothing live was re-verified.
- The prefix relies on sibling precedent because S019 is unreadable this round.
