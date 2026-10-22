# Scout — offline facts about the ds4cc-marketplace publishing tree (r35 w1)

Seat: KakeR35.ScoutDs4ccWellKnown. Lane axes: operability + freshness.
Method: `git ls-tree` / `git show` / `git grep` / `git log` / `git ls-remote` only.
Sandbox clone: `/fast/scratch/hyaku/kake-r35/w1/ScoutDs4ccWellKnown/repo`
(`git clone --no-checkout --filter=blob:none https://github.com/VeigaPunk/ds4cc-marketplace.git`).
No request was made to ds4cc.com or any owned host.

## Head under study

- `refs/heads/main` = **`7fc6aa2fc12451dd451fed5a9ee7125f3a90e884`**
  (`git ls-remote --symref https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD`
  → `ref: refs/heads/main` + `7fc6aa2f…	HEAD`).
- 2639 tracked files (`git ls-tree -r --name-only 7fc6aa2f | wc -l`).
- Other remote heads, none deployed by the Pages workflow (it triggers on `main` only):
  `feat/the-sshid-sandbox af234c95`, `fix/xbreed-safe-dispatch 4b941c31`,
  `fleet/canonical-vault-links 4073fac5`, `modelbenx e633b385`.
- The local read-only checkout `/home/vgpnk/Projects/ds4cc-marketplace` sits at
  `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`, **behind** the remote head; every fact below
  is taken from the sandbox clone at `7fc6aa2f`, not from that checkout.

## Observed facts

### 1. No `.well-known/`, no `security.txt`
`git -C repo ls-tree -r --name-only --full-tree 7fc6aa2f | grep -i well-known` → **exit 1** (no match).
`… | grep -i 'security\.txt'` → **exit 1** (no match).
`git grep -I -n -i -e 'security\.txt' 7fc6aa2f -- .` → no hit for that literal.

The only `.well-known` strings in the tree are on a **different host**: the Express app behind
`app.ds4cc.com` serves `/.well-known/openai-apps-challenge` itself —
`git show 7fc6aa2f:apps-sdk/src/server.ts:197` (`app.get("/.well-known/openai-apps-challenge", …)`),
with `apps-sdk/README.md:29`, `apps-sdk/src/server.test.ts:78,191`,
`scripts/smoke-deployment.mjs:26`. That is a server route, not a published file.

### 2. No `_config.yml` anywhere, so no `include:` key exists
`git cat-file -e 7fc6aa2f:_config.yml` → `fatal: path '_config.yml' does not exist`, **ABSENT**
(same for `_config.yaml`). `git ls-tree -r --name-only 7fc6aa2f | grep -E '(^|/)_config'` → **exit 1**.
There is no Jekyll config in the repository at any depth, therefore no `include:` list that could
whitelist `.well-known` under a Jekyll build.

### 3. `.nojekyll` present at root
`git show 7fc6aa2f:.nojekyll` → blob `68a5d3c25536c7a6afad62a0104ef6b625973042`, 51 bytes, one line:
`# keep static files and underscore paths untouched`.
A second, empty one exists: `omegag/.nojekyll` → blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, 0 bytes.

### 4. `CNAME` present, contents `ds4cc.com`
`git show 7fc6aa2f:CNAME` → blob `0883895ee82a66676768a7665488b3dde4089f09`, 9 bytes, `ds4cc.com`
with **no trailing newline** (`cat -A` shows no `$`).

### 5. Publishing workflow: one workflow, `upload-pages-artifact@v3`, `include-hidden-files` unset
`.github/workflows/pages.yml` → blob `38ee04dbf9fa1abeebe5cbe6d71e31253b88e19e`.
Triggers `push: branches: [main]` + `workflow_dispatch`; permissions `contents: read`,
`pages: write`, `id-token: write`; environment `github-pages`, `url: https://ds4cc.com/` (line 22).

- line 61 `uses: actions/configure-pages@v5` — no `with:` (no `enablement`, no generator config)
- line 64 `uses: actions/upload-pages-artifact@v3`
- line 65-66 `with:` / `path: ./ds4cc-marketplace`
- line 69 `uses: actions/deploy-pages@v4`

`include-hidden-files` is **not set**: `git grep -n -i 'include-hidden-files' 7fc6aa2f -- .github` → **exit 1**.
The second checkout (`repository: VeigaPunk/myagents`, lines 29-33) lands at `./myagents`, i.e.
**outside** the uploaded `./ds4cc-marketplace` path, so it is not part of the artifact.
`validate.yml` and `apps-sdk.yml` contain no `upload-pages-artifact` / `deploy-pages` step
(grep at lines shown), so `pages.yml` is the only Pages publisher.

### 6. The pin is `@v3`, and v3 does **not** exclude dotfiles
Lane source evidence, `corpus/knowledge/ghp-served-set.md`:
- lines 21-27: S001/S002 — v4.0.0 excludes `.[^/]*` in all three OS steps, **v3.0.1 does not**;
  v4.0.0 release text “Potentially breaking change: hidden files (specifically dotfiles) will not be
  included in the artifact”; v5.0.0 announces the `include-hidden-files` input.
- lines 38-41: recheck loop counts `v3.0.1 0`, `v4.0.0 3`, `main 3` for `.[^/]*`; and
  `v3.0.1 3`, `v4.0.0 3`, `main 3` for `--exclude=.github`.
- lines 43-51: local tar fixture with `--exclude=.git --exclude=.github '--exclude=.[^/]*'`
  drops `.nojekyll`, `.well-known/x`, `a/.keep`.

So under the **current** `@v3` pin the only exclusions are `.git` and `.github`.

### 7. Renovate is armed on `^@actions/`
`git show 7fc6aa2f:renovate.json`: `enabledManagers: ["npm", "github-actions"]`,
`packageRules` with `matchPackagePatterns: ["^@actions/"]`, `groupName: "GitHub Actions"`.
The v3 pin was introduced 2026-07-21 (`5889f86`, pickaxe `-S'upload-pages-artifact@v3'`);
`pages.yml` last touched `fe379aa` 2026-09-26.

### 8. No security contact surface exists to source an RFC 9116 `Contact:`
- No `SECURITY.md` / security policy file: `ls-tree -r | grep -i 'SECURITY(\.md)?$|security'` → **exit 1**.
- `git show 7fc6aa2f:sitemap.xml` lists 100 `<loc>` entries, **none** matching
  `security|contact|privacy`.
- `git show 7fc6aa2f:index.html` has no `mailto:` at all; its only "security" strings are a
  catalog chip `data-cat="security"` and one plugin record (`{ n: "spoderman", …, cat: "security" }`).
- `robots.txt` = `User-agent: *` / `Allow: /` / `Sitemap: https://ds4cc.com/sitemap.xml`.

### 9. Other publishing paths in the tree are not the apex site
- `render.yaml` deploys `apps-sdk/Dockerfile` as a Render web service (`ds4cc-marketplace-app`,
  `APP_ORIGIN=https://app.ds4cc.com`) — a different host, not Pages.
- `deploy-github-pages.sh` writes `CNAME` and pushes `main`, and its own output says
  “Pages deploys via .github/workflows/pages.yml (Source = GitHub Actions).” Legacy/leftover.
- History shows a branch-publishing era: `fb43ded` 2026-07-21 “restore GitHub Pages deploy and bind
  ds4cc.com”, `d3ecc83` 2026-07-21 “drop dead ds4cc.com CNAME so github.io serves assets”.

## What this implies for serving `https://ds4cc.com/.well-known/security.txt`

1. **The only possible mechanism is a committed file at repo root `.well-known/security.txt`.**
   The apex site is a static artifact upload; there is no server route at `ds4cc.com` (the only
   `.well-known` route in the tree belongs to the separate `app.ds4cc.com` Express app).
   `[INFERENCE]` from facts 1 and 5.
2. **Under the current `@v3` pin it would ship.** v3.0.1 excludes only `.git`/`.github`, so a
   committed `.well-known/` directory and its `security.txt` would be packed and deployed at the
   exact RFC 9116 path. `[INFERENCE]` from facts 5 and 6; the corroborating repro is the lane's tar
   fixture (`ghp-served-set.md:43-51`), which drops dotfiles **only when** `--exclude=.[^/]*` is present.
3. **The live hazard is an automated bump, not today's pin.** Renovate groups `^@actions/`
   (fact 7); a bump to `@v4`/`@v5` makes dotfiles excluded by default, and because `pages.yml:65-66`
   carries only `path:`, the file would vanish from the artifact with a **green** workflow and no
   error. Guard: add `include-hidden-files: true` beside `path:` (v5), or pin `@v3` deliberately with
   a comment. `[INFERENCE]` from facts 5-7.
4. **`.nojekyll` does not gate this path.** Under artifact deployment Jekyll is not the build step,
   so `.nojekyll` is inert for `.well-known`; it would only matter if publishing reverted to
   branch/Jekyll mode, where Jekyll's dot-prefix skip (S006) would otherwise drop `.well-known`
   entirely. `[INFERENCE]` — the lane corpus does not assert the "no Jekyll on artifact deploys"
   premise; it is stated here as an unverified premise, and note that the root `CNAME` is likewise
   reported by S005 to be ignored for Actions-published sites (domain comes from Pages settings/API).
5. **`Contact:` has no existing source.** Nothing in the tree names a security address or handler
   (fact 8), so the knowledge entry cannot point at a page that already publishes one; the publisher
   must create the contact (or use an existing reachable URI) before the file is valid under
   RFC 9116. `[INFERENCE]` from fact 8.

## Not verified

- No request was made to `ds4cc.com`; whether the live site currently 404s
  `/.well-known/security.txt` is **unverified**.
- Pages settings `build_type` / the Pages API `cname` field were not read (no API call this seat).
- `actions/upload-pages-artifact@v3/action.yml` was not re-fetched this round; the v3 semantics above
  rest on the lane recheck recorded at `corpus/knowledge/ghp-served-set.md:21-27,38-41`.
- The `contact`/`Expires` content of a real security.txt is out of scope for this seat.

## Tooling

Nothing installed or updated; `git` from the host was sufficient. No pacman ran (transactions paused).
