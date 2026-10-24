# Knowledge12 — kimi-subpath-audit.md provenance trio

Seat: KakeR21.Knowledge12 (scribe, leaf). Parent: KakeR21. Target: `corpus/knowledge/kimi-subpath-audit.md` only.

## Field truth audit (before edit)

- The entry opened with the body title on line 1. No `source:`, `verified-at:` or `recheck:` line existed. Trio was absent, so prepend was the required action.
- Pre-edit state: 4064 bytes, sha256 `de44691bce467a99c2b84e3b9b169e70af71058ed9081bd49617dd17503f860c`. This matches `.ufo/waves/round-21/frozen/before/expected.json`.

## Edit performed

- Prefix: 4 lines, **845 bytes**, prepended before line 1 (hashline `PUT <1`).
  - Line 1 `source:` — own-work, no S### row: kimi subpath baseline 2026-09-28 ~21:15Z; read-only same-origin GETs on 10 live kimi rows; ds4cc sitemap.xml parity (93 locs, sitemap commit f3d2ecd); git log --diff-filter=A miss classification; transient /tmp/kimi_audit.py + /tmp/kimi-subpath-audit.json.
  - Line 2 `verified-at:` — original evidence 2026-09-28 ~21:15Z, source revision f3d2ecd, `historical-not-live-reverified`; no GET repeated this round.
  - Line 3 `recheck:` — local-only `git -C ds4cc-marketplace show f3d2ecd:sitemap.xml | grep -c '<loc>https://ds4cc.com'` (expect 93 per entry evidence); operator restore-at-f3d2ecd-or-retire requirement; metadata contract S019 named.
  - Line 4 blank line.
- Old bytes verified: `tail -c 4064` sha256 = `de44691b…f860c`, identical to pre-edit. Body byte-identical. No body line changed, no correction or absence flag removed. The body already carries its own round-9 errata (74 → 75).
- Post-edit size 4909 bytes = 4064 + 845.
- Post-edit tag: `[kake-shokunin/corpus/knowledge/kimi-subpath-audit.md#FD0F]`.

## Evidence basis for the trio

- Source line: entry lines 3–5, 9–22, 24–43, 71–86 (method, baseline table, errata, recipe) and `corpus/knowledge/mirror-pitfalls.md` / `LOG.md` round-8 cross-references. The 10-row count comes from `LOG.md` round-8 (9 table rows plus ds4cc).
- Verified-at: entry line 3 (`First baseline: 2026-09-28 ~21:15Z`) and line 41 (`f3d2ecd` source commit).
- Recheck: the command is read-only and local. It was **not run**, per instruction.

## Operator-facing findings

- **Source vanished (local FS, this round).** A name search over `/home/vgpnk` (pruned of caches, `.omp`, `.kimi-code`, secrets dirs) found none of: `ds4cc-marketplace`, `kimi_audit.py`, `kimi-surface.mjs`, `kimi-surface-ops.md`, `kimi-map.json`, `fleet.config.json`, `fleet.dedupe-report.md`. `/tmp/kimi-subpath-audit.json` is absent. Operator must restore the ds4cc checkout at `f3d2ecd` or retire the recheck line.
- **S019 unregistered.** `S019` does not exist in `kake-shokunin/corpus/` (grep found no match; `SOURCES.md` stops at S018). It is cited as metadata authority only, per assignment. L1 registers the canonical `CORPUS.md`.
- **No S### row for this own-work capture.** The source line says "own-work, no SOURCES.md S### row". `CORPUS.md` names external sources as the case that must cite an S row. S014 (`own-work`) is the precedent for own-work. L1 decides whether to add an own-work row. I did not invent an S-ID.
- Source line cites entry-specific evidence, not S019. S019 appears only in the recheck tail as contract authority.
- No field-count coverage work performed (L1 scope).

## Out of scope / not touched

- No other file edited. No SCORECARD, LOG, QUALITY, SOURCES, README, SKILL changes. No commits.
- No network reads. No credential or auth files read. omp CLI not launched. No subagent dispatch.

## Tooling

- No installs or upgrades performed. No pacman/uv/npm/cargo activity.
