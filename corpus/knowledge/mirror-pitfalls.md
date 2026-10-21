source: Historical kimi-surface-ops.md failure-mode tables, fleet.dedupe-report.md and ufofsdbeta wave evidence cited in this entry; Browser/CDP bullets have no named source here. Metadata authority only: S019 in corpus/SOURCES.md, not platform verification.
verified-at: 2026-09-28 (LOG.md rounds 1–4; ufofsdbeta absence event 2026-09-28T23:51:31Z, r15 sweep) — historical-not-live-reverified
recheck: local historical reading only: `git show 5009ecaa1cce10b895617a585ddd3f7c7c923a84:corpus/knowledge/mirror-pitfalls.md`; the cited webzites and ufofsdbeta source evidence is absent per the entry's dated annotations. Operator must restore and recheck those sources or retire their recipes; no browser operation is authorized here.

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

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/mirror-pitfalls.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [mirror-pitfalls:c1] **HOLD** — The public root currently serves a 612-byte HTML client SPA shell. Surface: `GET https://ufo-fsd.kimi.pro/`.
- [mirror-pitfalls:c2] **HOLD** — The two named public roots currently serve distinct pages: a central vault and a work-in-progress ufofsd landing page. Surface: `GET https://ufo-fsd.kimi.page/; GET https://ufofsd.kimi.page/`.
- [mirror-pitfalls:c3] **UNVERIFIABLE** — The two named Kimi sites have no chat bound to them. Surface: `GET https://plazir15.kimi.page/; GET https://charter-ufo-fsd.kimi.page/`. Unverifiable: Unauthenticated public GET establishes only the current 404 responses, not the private Kimi chat-to-site binding. No authenticated API or browser operation was used.
- [mirror-pitfalls:c4] **STALE** — The frozen three-run copy and its canonical repository path are present locally, with a rel=canonical link from the copy. Surface: `test -e /home/vgpnk/Projects/plazir-15-site/speedrun; test -e /home/vgpnk/Projects/ds4cc-marketplace/speedrun`. Correction: As of 2026-10-21, neither /home/vgpnk/Projects/plazir-15-site/speedrun nor /home/vgpnk/Projects/ds4cc-marketplace/speedrun exists under /home/vgpnk/Projects, so this workstation cannot substantiate the asserted copy or canonical link.
- [mirror-pitfalls:c5] **UNVERIFIABLE** — The named tree is a non-git review snapshot, is not a source, and has remained absent from the filesystem since the r15 sweep. Surface: `test -e /home/vgpnk/Projects/ufofsdbeta-kimi-review; test -e /home/vgpnk/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review; glob /home/vgpnk/Projects/**/ufofsdbeta-kimi-review`. Unverifiable: The unit gives only a relative directory name and makes a filesystem-wide absence/non-git assertion. The checked project-root candidates were absent, but without an exact canonical absolute path or the tree itself I cannot verify the global absence or its former git status.
- [mirror-pitfalls:c6] **UNVERIFIABLE** — Kimi's served bytes are rewritten by the listed mechanisms, making source-versus-served SHA comparison unsuitable without normalization. Surface: `GET https://ufo-fsd.kimi.pro/ plus its raw response; paired pre-publish source bytes unavailable`. Unverifiable: The public response confirms SDK-seed injection on this page, but neither the named historical source documents nor paired pre-publish bytes are available to verify cfemail/entity rewriting or the broader digest conclusion.


## Round-24 path reconciliation

These dated corrections supersede only current local-state readings of the cited lines; original bytes and coordinates are preserved. Evidence: `.ufo/waves/round-24/c1-receipts/` and `corpus/knowledge/freshness-sidecar.json` (lane-relative).

- 2026-10-21: ~/Projects/ds4cc-marketplace/speedrun present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/knowledge/mirror-pitfalls.md:63 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.
