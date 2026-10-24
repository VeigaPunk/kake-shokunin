# Knowledge10 — provenance trio for `corpus/knowledge/ghp-subpath-spotcheck.md`

## Behavior

- Target: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/ghp-subpath-spotcheck.md` (read whole entry before edit, anchor `CC46`).
- Pre-edit state: no provenance trio. Line 1 was `# GHP subpath spotcheck — the blind spot behind \`probe\`/\`reconcile\``. The trio was therefore prepended.
- Change: pure prefix addition of **4 lines / 1026 bytes** (`source:`, `verified-at:`, `recheck:`, blank line), measured with `sed -n 1,4p | wc -c`. Former line 1 is now line 5, text unchanged. Former line 4 (the `r18 re-census` absence comment) is now line 8. The `Round-20 corrections` bullet that was line 91 is now line 95, text unchanged, including its `[r20-correction 2026-10-19 …]` flag. No other file was edited. No commits.

## Prefix content and evidence basis

| field | content basis |
|---|---|
| `source:` | Entry-specific evidence that the body itself cites: `/tmp` baseline audit 2026-09-28 (~16:45Z, 2 352 paths); `~/Projects/webzites/src/reconcile.mjs:55-107`; `fleet/fleet.config.json`; live GHP fetches 2026-09-28. Registry-backed only for the round-20 correction (`S001`, `S005`, both present in `corpus/SOURCES.md` rows dated 2026-10-19). `S019` named as metadata authority, not platform authority. |
| `verified-at:` | Original evidence date 2026-09-28; states `historical-not-live-reverified`. Webzites revision not recorded in the entry, so it says so. Notes the r18 re-census (2026-10-14) observation that `reconcile.mjs` was absent. Never claims a 2026-10-19 domain recheck. |
| `recheck:` | Local-only reading command: `test -f` then `sed -n '55,107p'` on `reconcile.mjs`, else an echo instructing operator restore-or-retire. States that the `/tmp` baseline and live GHP figures have no recorded local path, so operator restore-or-retire is required where source vanished. No credential/auth files referenced. Not executed. |

## Field-truth audit (pre-existing content)

- `reconcile.mjs` absence is corroborated by the entry's own r18 flag and by a read-only existence check: `/home/vgpnk/Projects/webzites/src/reconcile.mjs` and `/home/vgpnk/Projects/webzites/fleet/fleet.config.json` are both missing (the glob reported them as skipped). This was an existence check, not a recheck run; the recheck command was not executed.
- The `/tmp` baseline has no recorded directory in the entry, so it cannot be located from the entry alone. Flagged in `recheck:`.
- `S019` is **not present** in the tree: `corpus/CORPUS.md` does not exist and the `corpus/SOURCES.md` registry ends at `S018`. The reference is forward-pointing per the assignment; L1 must register it. Until then the `S019` mention is unresolved and should be checked when CORPUS.md lands.
- Body claims about GHP path semantics (`/dir` 301, `404.html`, raw `.md`) rest on 2026-09-28 live fetches; no registry row covers directory-redirect behavior. Left unchanged; the trio marks them historical.
- Round-20 correction (`CNAME` under Actions is an unverified prediction) is preserved verbatim; the new `source:` line cites `S001, S005`, consistent with that correction.

## Tooling

No installs or upgrades. Read-only tools only.

## Out of scope / not touched

No SCORECARD, LOG, QUALITY, SOURCES, README, SKILL edits. No lessons edited. No network reads. No rechecks run. Field coverage counting is L1's job.

## Checks for main agent

- Confirm `corpus/CORPUS.md` registers `S019` as the metadata contract; if its contract differs from the trio format used here, adjust the prefix (the body is unaffected).
