# Commit anatomy — 7fc6aa2f (ds4cc-marketplace)

Read in /fast/scratch/hyaku/kake-r33/ds4cc-upstream (L1 clone; git show/ls-tree/cat-file only).
Commit 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884, parent 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28,
author=committer `Claude <noreply@anthropic.com>` 2026-10-21T17:32:55Z, subject
`magga: Frostbite — Classic & Remastered at /magga/frostbite/`. 12 files, +3,734 / −0; no renames,
deletions or mode changes; `magga/frostbite/` is absent at the parent (ls-tree count 0).

| path | kind | size / lines | blob | lane area | claim status |
|---|---|---|---|---|---|
| sitemap.xml | M +3 | 7,810 B (parent 7,614 B); 97→100 `<loc>` | 67d8c7a | sitemap, canonical | holds |
| magga/index.html | M +9 | 28,250 B | 1215ae3 | magga subpath | holds |
| magga/README.md | M +15 | 12,264 B; new section `:141`, copy claim `:154` | 0a30979 | served set (raw .md), subpath doc | holds except F4 |
| magga/frostbite/index.html | A | 14,488 B / 262 | e0d9ee2 | base path, canonical, served set | holds |
| magga/frostbite/classic/index.html | A | 8,019 B / 158 | 12c58e2 | canonical, served set, base path | holds |
| magga/frostbite/remastered/index.html | A | 16,494 B / 277 | 4e6d70a | canonical, served set, base path | holds |
| core.js / shell.js / classic.js / remastered.js | A | 20,428 / 12,860 / 22,379 / 67,716 B | 485a082 / e34f33e / b523966 / 742859e | served set (assets) | holds: no external URL |
| covers/classic.png / covers/remastered.jpg | A | 5,336 B 960×768 / 94,669 B 1280×800 | ff2ac8b / b8c1595 | served set (images) | png attrs wrong, F1; jpg exact |

- **sitemap.** Three `<loc>` inserted between the v2 and enduro blocks: `/magga/frostbite/`,
  `/magga/frostbite/classic/`, `/magga/frostbite/remastered/`. No other line changed; still zero
  `<lastmod>` (pre-existing). Locs use `https://ds4cc.com/…`, matching `CNAME` = `ds4cc.com` in the
  same tree. Each new loc maps to a committed `index.html`: no dead listing, no orphan added.
- **canonical.** Each new page has exactly one absolute `<link rel="canonical">`, no fragment, no
  `<base>`; canonical == `og:url` == its sitemap `<loc>` byte for byte. Lane tool
  `scripts/canonical_audit.py` (rev bc6c4a8) on a 3-page manifest: `{"findings":[],
  "pagesChecked":3,"verdict":"clean"}`, exit 0. Static-canonical-preflight's policy is satisfied.
- **GHP served set.** No dot path and no `_`-prefixed name is added, so nothing here is dropped by
  artifact filtering or Jekyll defaults. `pages.yml` at this commit pins
  `actions/upload-pages-artifact@v3` (`:64-66`, `path: ./ds4cc-marketplace`) and `deploy-pages@v4`;
  `.nojekyll` exists at root. Per ghp-served-set.md:21-23 the dotfile exclusion is a v4/main property,
  so for this row the served set at the pin is the checkout tree minus `.git` and `.github` — all 12
  files are in it, `magga/README.md` as raw text. The action-tag and upload-path halves of the Named
  debt at ghp-served-set.md:56 are thus answerable at a pinned commit (live behavior still unverified).
- **base path.** Domain root, no `/docs` or project prefix. Chooser fonts
  `../assets/fonts/JetBrainsMonoNLNerdFontMono-{Regular,Bold}.woff2` resolve to `magga/assets/fonts/`,
  where both exist in-tree. `../` from each game page resolves to `/magga/frostbite/`; `./classic/`,
  `./remastered/`, `./covers/*` resolve. Game pages carry no `@font-face` and no external URL.
- **magga subpath.** Catalog card, README section, sitemap locs and the three directories agree on
  `magga/frostbite/`; the card's "AVAILABLE NOW" is backed by three committed pages; its id
  `dlc-frostbite-title` occurs once. Classic canvas is 320×192 (2× the stated 160×192 frame).

## Findings

- **F1 (minor, real).** `magga/frostbite/index.html:208` declares `width="1280" height="960"` for
  `covers/classic.png`, whose bytes are 960×768 (1.25 vs 1.333 ratio). `remastered.jpg` attrs match
  exactly. CSS `:116-120` (`width:100%;height:auto;aspect-ratio:16/10;object-fit:cover`) governs the
  rendered box, so there is no layout-shift path; the attributes are wrong for consumers that read
  intrinsic size, and the 5:4 PNG is top-center cropped into 16:10. Not a served-set or canonical defect.
- **F2 (freshness, arithmetic on existing records, no fetch).** Source sitemap = 100 locs / 7,810 B at
  this pin; lane records live 96 locs / 7,565 B at 2026-10-21 (sitemap-orphan-audit.md:135,
  kimi-subpath-audit.md:96, publish-queue.md:293). Source is 4 locs / 245 B ahead — deploy-lag class,
  not rot. The 93-loc and 97-loc numbers inside sitemap-orphan-audit.md (`:48`, `:70`, `:74`, `:145`)
  are historical, not the current source count.
- **F3 (adjacent, not caused by this commit).** `freshness-pins.json` still carries `sitemapStatus: 404`
  (round 24) while three knowledge entries record live 200 on 2026-10-21; the A4 predicate
  `200 → LISTED-LIVE` (freshness-sweep.md:62) would fire on an already-true antecedent. For the pin owner.
- **F4 (scope).** The new README section publishes the upstream slug `VeigaPunk/MAKEARMORGAMESGREATAGAIN`
  and its `games/frostbite/` path on a file that is itself served; recorded as a live-visible byte change.

## Commands (in the clone unless noted; all exit 0)

`git show --stat/--shortstat`; `git diff-tree --name-status/--numstat 7fc6aa2f^ 7fc6aa2f`;
`git ls-tree -r --long 7fc6aa2f:magga/frostbite`; `git show 7fc6aa2f:sitemap.xml | grep -c '<loc>'`
= 100 vs 97 at `1fbdb8ed`; the equality probe (canonical ⊆ locs, canonical == og:url, `<base>` absent);
`file` plus PNG IHDR / JPEG SOF0 parse on the covers; `git show …:pages.yml | grep -nE
'upload-pages-artifact|path:|deploy-pages'`; external-URL grep over the four JS files (no matches).
From kake-shokunin at bc6c4a8 in my sandbox: `python3 scripts/canonical_audit.py --manifest
$PWD/fm/manifest.json --json` → clean/3, exit 0.

## Not verified / out of bounds

- Any live request to ds4cc.com (owned property): serving, deploy of this commit, and the live loc
  count are unmeasured.
- README's "byte-for-byte copy" against `VeigaPunk/MAKEARMORGAMESGREATAGAIN` — github reads are
  bounded to ds4cc-marketplace for this seat, so the claim is unverified, not refuted.
- Upstream motion past the pin: refs show `origin/main = 7fc6aa2` but no fetch timestamp exists
  (no `FETCH_HEAD`), so "still current upstream" is unestablished.
- No tool installs or updates were needed. This file is 79 lines in .ufo/waves/round-33/w1/.
