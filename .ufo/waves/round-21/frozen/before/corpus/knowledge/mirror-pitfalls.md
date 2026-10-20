# Mirror pitfalls — observed, not hypothetical

Sources: `fleet/kimi-surface-ops.md` failure-mode tables (r1–r4),
`fleet.dedupe-report.md`, `ufofsdbeta/.ufo/` wave evidence — `ufofsdbeta/`
absent from FS since 2026-09-28T23:51:31Z (r15 sweep); wave evidence now
citation-only.

## Kimi static surface

- **Bytes are rewritten.** sdk-seed.js injection + cfemail/entity rewriting →
  sha comparison impossible; normalized-digest + marker + vintage instead.
- **No directory indexes.** `dir/` → 404, `dir/file` → 200. GHP-style
  `href="snake/"` links die on kimi; emit explicit `index.html` paths.
- **One chat = one publish slot + one custom slug.** Firing an update into a
  chat bound to another site hot-swaps that live site. Banned fire targets:
  `1a0c20ea-6372…` (veigapunk.kimi.page), `1a049cb5-47d2…` (plazir27runs-on).
- **`publishedUrl` via `GetWebsiteByChatID` is the only authoritative binding**
  — a `hosts[]` text mention never authorizes a fire.
- **Dead slots need `recreate`/`rebuild`, not `update`.** plazir15.kimi.page
  and charter-ufo-fsd.kimi.page have no bound chat; `.kimi.pro` is
  Function-Compute ingress where an unclaimed slot serves preview-404.

## Name traps

- `plazir27runson` (Night Trilogy) ≠ `plazir27runs-on` (charter doctrine) —
  different sites, hyphen matters.
- `ufo-fsd.kimi.page` = vault twin; `ufofsd.kimi.page` = frozen landing;
  `ufo-fsd.kimi.pro` = 612B SPA shell. Three different artifacts.
- `ufofsdbeta-kimi-review/` = non-git review snapshot, never a source —
  **absent from FS since 2026-09-28T23:51:31Z** (r15 sweep).
- `plazir-15-site/speedrun/` = frozen 3-run copy; canonical is
  `ds4cc-marketplace/speedrun/` (`rel=canonical` in the plazir copy confirms).

## Browser/CDP lane

- Lease first: `webzites lease acquire --owner <n> --ttl-ms 900000`; release
  in `finally`. One op at a time on the shared burner profile.
- `t<N>` indices renumber on open/close — re-derive via `/json/list` URL match.
- `agent-browser open --wait` is a silent no-op → `agent-browser wait <ms>`.
- `[role=menu]` open swallows Enter — assert count 0 before submit.
- Composer: `div.chat-input-editor` (sole contenteditable+textbox; zero
  `textarea`). Send = click `.send-button-container` (disabled is a CSS class,
  not attribute). Enter submit never verified.
- Dead session can pass avatar check — `browser status` requires a 401
  must-fail + 200 must-pass pair. Single mid-poll 401 = token-refresh flake;
  retry once.
- `SingletonLock` after chrome crash is tolerated; `browser ensure` rebinds.
  `(musketeer-chrome &)` dies with the shell — `setsid -f musketeer-chrome`.
- Chat fires are metered: ~1 per site update; `--fire --confirm=<id>`
  double-gate; preflight path is free.
