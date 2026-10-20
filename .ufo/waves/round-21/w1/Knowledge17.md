# Knowledge17 — publish-channels.md provenance trio (round 21, w1)

## Behavior
- Target: `corpus/knowledge/publish-channels.md` (relative to kake-shokunin root).
- Pre-state: the entry opened directly with `# Publish channels (verified)`; no `source:` / `verified-at:` / `recheck:` trio existed. Audit-of-fields branch did not apply; prefix branch applied.
- Post-state: a four-line prefix (`source:`, `verified-at:`, `recheck:`, blank) was prepended before the original heading.

## Exact change
- Prefix length: 4 lines, **1342 bytes** (measured with `head -n 4 | wc -c`; includes the trailing newline of the blank line).
- Old content: HEAD blob is 3959 bytes; `tail -n +5` of the edited file is 3959 bytes and `cmp` against `git show HEAD:…` reports identical. All pre-existing bytes, including the round-20 corrections (lines 54–57 of the old file) and the absence flags (line 31, line 50 HTML comment), are preserved byte-identically.
- Nothing else touched. No commits.

## Evidence basis for the prefix
- `source:` — S001, S002, S003, S005, S007 are the sources the entry's own round-20 corrections cite (old lines 54–57 cite S001/S002, S003/S005/S007 and S003/S005). Registry rows confirmed in `corpus/SOURCES.md` (S001 pinned at 7b1f4a7 / 5f327015; S002 v4.0.0/v5.0.0 notes; S003, S005, S007 fetched 2026-10-19). Entry-specific local evidence named explicitly: ds4cc-marketplace `pages.yml`, `render.yaml`, `deploy-github-pages.sh`; plazir-15-site `pages.yml`; webzites `scripts/kimi-surface.mjs`, `fleet/kimi-surface-ops.md`.
- `verified-at:` — original evidence dates: 2026-09-26 (kimi-webbridge "not supported on Linux", stated in entry); 2026-09-28 (round-1 commit `cd5b381` per `git log`, which introduced the file; wz1-ds4cc emptied `2026-09-28T21:42-03:00`, stated in entry); round-20 correction date 2026-10-19 with S001–S007 opened that day (per SOURCES.md). Marked `historical-not-live-reverified`; no domain recheck is claimed.
- `recheck:` — local read-only `ls` of the cited source paths plus operator restore-or-retire requirement. The command was **not run** by me.

## Absence / source-vanished findings (read-only glob, round-21 audit)
- `~/Projects/ds4cc-marketplace/.github/workflows/pages.yml`, `…/render.yaml`, `…/deploy-github-pages.sh`: not found.
- `~/Projects/plazir-15-site/.github/workflows/pages.yml`: not found.
- `~/Projects/webzites/scripts/kimi-surface.mjs`, `~/Projects/webzites/fleet/kimi-surface-ops.md`: not found (consistent with the entry's existing r18/r20 absence flags).
- Glob `~/Projects/*ds4cc*`, `*plazir*`, `*webzites*`: no matches.
- Operator action required: restore those trees or retire the dependent sections (GitHub Pages, Render, Kimi). This is recorded in the `recheck:` line; I did not act on it.

## Limitations
- **S019 not yet resolvable.** `corpus/CORPUS.md` does not exist (corpus/ contains only QUALITY.md, README.md, SOURCES.md), and S019 is absent from `SOURCES.md`. The prefix references S019 as the metadata contract, labelled "not platform authority", per the assignment. L1 must register the canonical CORPUS.md this round; until then the S019 reference is unresolved in-tree.
- The ds4cc and plazir roots were assumed to be `~/Projects/<name>`; the entry gives no root. Glob with wildcards found no ds4cc/plazir dirs anywhere under `~/Projects`, so the conclusion holds for this host.
- The Kimi verb table and the GitHub Pages workflow reads carry no own date in the entry; `verified-at` therefore cites the earliest dated evidence (2026-09-26/28) and the r20 date. This is a stated limit, not a verified date for the table itself.
- The entry's "base cb807bc" was not checked by me; the prefix does not depend on it.
- Round-20 correction line 56 duplicates line 54 text (both cite S001/S002) and is not mine to alter.
- Field-coverage counting across the knowledge set is L1's job; not done here.

## Tools
- None installed or updated.

## Checks for main agent
- `head -n 4 kake-shokunin/corpus/knowledge/publish-channels.md` shows the trio; expect 1342 bytes.
- Once L1 registers `CORPUS.md` with S019, confirm the S019 reference in the `source:` line resolves.
