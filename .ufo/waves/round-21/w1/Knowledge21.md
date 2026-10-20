# Knowledge21 — vault-properties.md provenance trio

## Scope
- Target: `corpus/knowledge/vault-properties.md` (only file touched).
- Whole entry read before editing (87 lines, 4467 bytes at HEAD).

## Gate state
- Before edit: no provenance trio (line 1 was `# Vault PROPERTIES[] — ...`). Prefix was therefore required.
- After edit: trio opens the file. Field truth audit below.

## Exact file change
- Prepended 4 lines (3 metadata lines + one blank line) = **974 bytes** (`head -n 4 | wc -c`).
- File grew 4467 -> 5441 bytes (5441 - 974 = 4467).
- Verified: `tail -c +975` of the current file is byte-identical to `git show HEAD:corpus/knowledge/vault-properties.md` (`cmp` silent). No old byte altered; no body line changed; existing corrections and absence flags (`lucario` absent, `url:null` rows, `sourceDir:null` blocker, +157B seed note, site-id collision) are untouched.

## Prefix content and evidence basis
- `source:` — entry-specific evidence taken from the entry's own text: `fleet/vault-properties.json` (mtime 2026-09-20, generatedAt 23:40:17Z), the live PROPERTIES[] literal of veigapunk.kimi.page and ufo-fsd.kimi.page (self-verified GETs 2026-09-28), kimi-surface.mjs lines 339-346, 483, 817-822, 845-849, 903-921, and fleet.config.json:298. S019 is cited as the metadata-contract authority only, not as a platform-fact authority.
- `verified-at:` — 2026-09-28, pinned to kake commit `dd4eabf` (latest commit touching the entry; `git log -1` date 2026-09-28T18:24:51-03:00). Explicitly marked historical-not-live-reverified; not a 2026-10-20 domain recheck.
- `recheck:` — states historical-only status; records that no local copy of `fleet/vault-properties.json` or `kimi-surface.mjs` exists in this checkout, so the operator must restore the fleet tree or retire the entry. Gives one local reading command for after restoration (`node -p` reading `generatedAt` and `properties.length`, expecting 13). The live GET Method block is noted as operator-run and was not run.

## Checks performed (all read-only)
- Existence checks for the cited fleet paths: `~/Projects/webzites/fleet/vault-properties.json`, `.../fleet/fleet.config.json`, `.../fleet/kimi-surface.mjs`, `~/Projects/webzites/scripts/kimi-surface.mjs`, `~/Projects/kimi-surface`, and `find ~/Projects -maxdepth 4` for `kimi-surface.mjs` and `vault-properties.json`. All absent or not found.
- `git log` on the target for commit/date revision.
- Grep for `S019` across `corpus/`, `.ufo/waves/round-21/`, and handoffs: **no match**. `corpus/CORPUS.md` does not exist (glob, no result). S019 is therefore referenced as the metadata authority named in the assignment but is not yet registered in this checkout. L1 must register it; if L1 uses a different id, the `source:` line needs the same update.
- No live network reads. No recheck command executed. No credential/auth files read.

## Field truth audit (prefix fields only; body not audited)
- `source:` names sources that are absent from this checkout. This is stated in the line rather than hidden, which is the restore-or-retire condition.
- `verified-at:` date (2026-09-28) matches the entry's own baseline GET date and the entry's own "Residual README gap closed 2026-09-28". Not elevated to a current check.
- `recheck:` command is local and does not reference credential or auth files.
- Count field coverage is L1 scope and was not checked.

## Out of scope / not touched
- No edits to SCORECARD, LOG, QUALITY, SOURCES, README, SKILL, CORPUS.md, or other knowledge/lesson files.
- No commits.

## Tools
- None installed or updated.

## Checks for main agent
- Confirm L1 registers S019 in `corpus/CORPUS.md`, or amend the `source:` line if the id or authority name differs.
- Confirm the byte-prefix check (974 bytes, old body identical to HEAD) if re-verification is desired after integration.
