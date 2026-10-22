# Round 29 wave 1 — owned project-site sources and their base-path handling

Read-only scout seat. Nothing in any scanned checkout was written, staged, or fetched.
Revisions pinned at scan time (2026-10-22):

| checkout | HEAD |
|---|---|
| ds4cc-marketplace | `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` |
| burnerchrome | `ee834920de8411f8014236948e2d5b9f5f82dde2` |
| ufo-fsd-alpha | `093edb979559443bca65245fbdd94ac3621446fb` |
| kimi-code | `4c7f2a102ceb7d3ba364d650067a5dbea58a42a6` |
| tog | no `.git` (not a checkout); `dist/index.html` sha256 prefix `80b4e56f38fbea3e` |

## Findings table

| Property | Absolute source path | Pages role | Base setting in source | Built HTML on disk |
|---|---|---|---|---|
| burnerchrome | `/home/vgpnk/Projects/burnerchrome` | **Project site**, repo `VeigaPunk/burnerchrome`, no `CNAME`, Actions source | **None.** Document-relative refs: `href="favicon.svg"`, `href="assets/styles.css"` (`index.html:11-13`); nested pages step up with `../assets/styles.css`, `../favicon.svg`, `../index.html` (`adapters/almanacker.html:9-12,18`) | **Yes** — 10 HTML files (site root + `adapters/`), published as-is from `.` |
| charter-ufo-fsd mirror | `/home/vgpnk/Projects/ufo-fsd-alpha/docs/charter-ufo-fsd` | **Project site** mirror of `veigapunk.github.io/charter-ufo-fsd/` (`README.md:11`), `.nojekyll` present, no `CNAME` | **None.** All refs relative; 0 root-relative refs in `*.html`, 0 `url(/…)` in `style.css`. Canonicals are absolute to the project-site URL (`index.html:8-16,21`) | **Yes** — `index.html` + `style.css`, `main.js`, `i18n.js`, `locales/` |
| ds4cc-marketplace | `/home/vgpnk/Projects/ds4cc-marketplace` | **Custom apex domain, not a project site**: `CNAME` = `ds4cc.com`; workflow deploy URL `https://ds4cc.com/` | **Root-absolute.** `<base href="/omegag/">` (`omegag/index.html:4`); `href="/burnerchrome/"` plus `http-equiv="refresh" … url=/burnerchrome/` (`burnerchrome.html:7,11`); nested subsite canonical `https://ds4cc.com/burnerchrome/` (`burnerchrome/index.html:9`) | **Yes** — 18 HTML files deployed verbatim (`pages.yml:66 path: ./ds4cc-marketplace`) |
| kimi-code docs | `/home/vgpnk/Projects/kimi-code/docs` | **Project site** (fork of `MoonshotAI/kimi-code`); base derived from repo name | **Explicit, CI-injected**: `VITEPRESS_BASE: /${{ github.event.repository.name }}/` (`docs-deploy.yml:34`) → `config.ts:5-12` normalizes missing/duplicate slashes, `config.ts:21` `base,`, `config.ts:26` `${base}favicon.ico` | **No** — `docs/.vitepress/dist` absent; gitignored (`docs/.gitignore:2`) |
| tog (control, not evidenced as Pages) | `/home/vgpnk/Projects/tog` | No workflow, no `CNAME`, no `.nojekyll`, no git remote | **Implicit root**: no `vite.config.*`; default `base: '/'` emits `/assets/index-7l2gFGXS.js` and `/favicon.svg` (`dist/index.html:10-11`) | **Yes** — `dist/index.html` |

## What the source evidence shows

1. **A project site passes only if every internal reference is document-relative or base-injected.** `burnerchrome` and the charter mirror satisfy this with plain relative paths: `grep -rno -E '(src|href)="/[^/]'` returns **0** for both (`burnerchrome`, `ufo-fsd-alpha/docs/charter-ufo-fsd`).
2. **`ds4cc-marketplace` is the counterexample in the same fleet.** It returns **2** root-relative refs (`omegag/index.html:4`, `burnerchrome.html:11`), and that is correct *only* because `CNAME` pins an apex domain (`CNAME:1` = `ds4cc.com`, 51 bytes, no newline). Served as a project site, `/omegag/` and `/burnerchrome/` both leave the site.
3. **The same omegag component already ships to three different base paths**, and its source hardcodes one of them: `omegag/README.md:16-17` lists `https://veigapunk.github.io/omegag-site/` and `https://vgpnk-holdings-llc.github.io/omegaG/`, while `omegag/README.md:22` instructs "keep `<base href="/omegag/">`". The apex copy and the two project-site copies cannot all be right without a rewrite step; the repo has none.
4. **`kimi-code` is the only tool that computes the base instead of assuming it.** `docs-deploy.yml:34` passes the repo name as VitePress `base`; the config defaults to `/` locally (`config.ts:5-12`). Markdown has **0** root-absolute links (`grep -c '](/' docs/en/**/*.md` → 0), so links move with `base`.
5. **The failure mode is visible locally.** `tog` builds with Vite's default base and its `dist/index.html:10-11` contains `/assets/index-7l2gFGXS.js`, `/assets/…css`, `/favicon.svg` — exactly the artifact that would 404 under `https://<owner>.github.io/tog/`. This is a worked example, not an owned Pages property.
6. **Deployment mechanism splits three ways**: Actions artifact (`burnerchrome/.github/workflows/pages.yml:59-66`, `upload-pages-artifact path: .`), Actions artifact for a subdirectory (`ds4cc-marketplace/.github/workflows/pages.yml:61-69`), and build-then-artifact (`kimi-code/.github/workflows/docs-deploy.yml:39`). Only the build path has a base knob; the two static-repo publishes rely entirely on the HTML being relative.

## Cross-property absolute links that assume a base

- `/home/vgpnk/Projects/burnerchrome/install.html:118` installs from `https://veigapunk.github.io/ds4cc-marketplace/.kimi-plugin/marketplace.json`. That repository carries `CNAME ds4cc.com`, so the `github.io/<repo>` form is subject to GitHub's custom-domain redirect. Whether it resolves is **unverified** (no network probe permitted); the file `.kimi-plugin/marketplace.json` does exist locally (7455 bytes).
- `/home/vgpnk/Projects/ds4cc-marketplace/README.md:359` points at `veigapunk.github.io/xbgst-site/`; `omegag/README.md:16` at `veigapunk.github.io/omegag-site/`; `speedrun/README.md:48` at `veigapunk.github.io/plazir-15-site/512qa/`. **None of those three source checkouts exists under `/home/vgpnk/Projects`** (directory listing shows no `xbgst-site`, `plazir-15-site`, `omegag-site`), so their base handling is unknown here.
- The charter mirror README (`README.md:13-20`) says the published URL serves a loader over a CDN-pinned gold copy while the mirror "may be newer"; the local `index.html` contains no loader (`grep -E 'cdn|jsdelivr|unpkg|loader'` → no match). Local source is therefore not byte-identical to the served artifact; this seat did not fetch the live URL.

## Verification actually run

```
cd /home/vgpnk/Projects
find . -maxdepth 4 -name .nojekyll -not -path '*/node_modules/*'      # exit 0 → 3 hits
find . -maxdepth 4 -name CNAME -not -path '*/node_modules/*'          # exit 0 → 1 hit
find . -path '*/.github/workflows/*' -type f                          # exit 0 → burnerchrome, ds4cc, kimi-code only
find . -maxdepth 5 \( -name 'vite.config.*' -o -name 'astro.config.*' -o -name '_config.yml' \) -not -path '*/node_modules/*'  # exit 0 → 3 vite configs, all kimi-code webviews, none with `base`
grep -rno -E '(src|href)="/[^/]' --include='*.html' <site>            # burnerchrome 0, charter 0, ds4cc 2
grep -rn 'VITEPRESS_BASE' kimi-code --exclude-dir=node_modules         # exit 0 → workflow:34, config.ts:5
for d in */; do git -C "$d" branch -a | grep -c gh-pages; done        # exit 1 → no gh-pages branch anywhere
grep -rn --include='*.config.*' -E '^\s*base\s*:' burnerchrome ds4cc-marketplace ufo-fsd-alpha kimi-code tog --exclude-dir=node_modules  # exit 0, no match; the only base key in any build config is kimi-code/docs/.vitepress/config.ts:21 (`base,`)
```

Not verified: no live fetch of any `github.io` URL, no build executed, no Git mutation, no `lsp` requests (no language server answers plain static HTML/config trees; text grep is the whole tool for this question, and every claim above is a literal line match, not a semantic inference).

Confidence: **high** for the table rows (direct file reads at pinned revisions); **medium** for the cross-property link axis (targets absent locally, redirect behavior unprobed).

Remaining unknowns: base handling of `xbgst-site`, `plazir-15-site`, `omegag-site`; whether the `veigapunk.github.io/ds4cc-marketplace/…` URL actually redirects to `ds4cc.com`; whether the charter mirror's published loader applies its own base.
