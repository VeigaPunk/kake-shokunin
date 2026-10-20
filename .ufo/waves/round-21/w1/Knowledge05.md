# Knowledge05 — free-read-verbs.md provenance trio

Target: `corpus/knowledge/free-read-verbs.md` (only file edited).

## Axes

1. **Freshness** — provenance trio opens the entry; `verified-at` dates the original evidence, not today.
2. **Operability** — `recheck:` gives a safe local read command plus the operator restore-or-retire requirement.

## State found

- Pre-edit: 479 lines, 33 728 bytes, sha256 `ec9f788536f635ce1cd693f9985be53a946ec2a8f340cbc7e521e02d465a6971` (prefix absent; first line `# Free-read verbs — …`).
- Trio was not present, so the prefix was added.
- Edit: pure head insertion (`PUT <1:`), 4 lines, **1 028 bytes** (3 metadata lines + one blank line, all `\n`-terminated).
- Post-edit: 483 lines, 34 756 bytes (= 33 728 + 1 028). Original line 1 is now line 5, unchanged. No old byte altered; in-body corrections and absence flags (r18/r20 HTML comments, `r20 citation-local` blockquote, r16 re-read notes) retained.

## Field evidence basis

| field | basis in the entry itself |
|---|---|
| `source:` | Entry header cites `~/Projects/webzites/{src/cli,fleet,probe,reconcile}.mjs`, `bin/webzites.mjs`, `scripts/kimi-surface.mjs`, and live read of `fleet/fleet.config.json` (lines 5–8). Metadata contract cited as S019; S019 row in `corpus/SOURCES.md` (own-work, tier A, scope limited to "provenance metadata and recorded lesson gates … not verification of historical platform claims") — used as metadata authority only, not platform authority. |
| `verified-at:` | Original read/live runs `2026-09-28T21:31–21:33Z` (line 8–9); `fleet.config.json` `updatedAt 2026-09-26` (line 27–28); r16 re-read `2026-09-29T02:35Z` (line 174). Webzites revision is **not recorded** in the entry; stated as such. Marked `historical-not-live-reverified`. Absence notes 2026-10-14 (r18) and 2026-10-19 (r20) labelled citation-local, not a domain recheck. |
| `recheck:` | Command `ls -l ~/Projects/webzites/bin/webzites.mjs ~/Projects/webzites/src/cli.mjs ~/Projects/webzites/scripts/kimi-surface.mjs` — local read, no credential/auth file, no network. Operator requirement: tree absent since 2026-10-12 `~/Projects` prune → restore and re-run cited verbs, or retire live-run claims and counts. |

## Verification performed

- Commands run: read of target (full), `sha256sum`/`wc`/`od` of target, `head -4 | wc -lc` for prefix length, `grep S019` in `corpus/SOURCES.md` (row confirmed present), read of `CORPUS.md` contract (`kimi-shokunin/skills/shokunin/protocol/CORPUS.md` lines 18–20, 162–165) for trio-first rule.
- **Not run:** the `recheck:` command itself, any `probe`/`status`/`reconcile`/`sync-check` verb, any network request, any build/test.
- Installs/updates: none.

## Findings

- Field truth: `source:` and `verified-at:` match the entry's own evidence and date; `verified-at` does not claim today as a domain recheck.
- Limitation (honest): the live-run captures in `/tmp/kake-r11`, `/tmp/kake-r12` are not durable and are not re-checked here; the entry labels them historical.
- Limitation: webzites revision unknown from entry; not inferred.
- No other corpus files, SOURCES, CORPUS, LOG, QUALITY, README, SKILL, or lessons touched.
