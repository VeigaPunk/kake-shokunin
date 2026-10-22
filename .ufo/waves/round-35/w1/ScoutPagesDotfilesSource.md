# Scout — GitHub Pages dotfiles / `.nojekyll` source (round 35, wave 1)

Sealed-key exposure: none. Nothing under `/fast/scratch/hyaku/kake-r35/sealed/` was read, listed or stat'ed.

## Headline

1. The dedicated GitHub Docs page "Bypassing Jekyll with `.nojekyll`" is **gone**: `https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/bypassing-jekyll-with-nojekyll` returns **404** today, no redirect. The current primary source is `creating-a-github-pages-site`.
2. Docs search (`/api/search/v1?query=".nojekyll"&client_name=docs`) finds **exactly 2** pages mentioning it: `creating-a-github-pages-site` (the normative instruction) and `configuring-a-publishing-source...` (external-CI aside). Search for `"include-hidden-files"` on docs.github.com returns **0** hits — the action input has no docs-page corroboration.
3. `.nojekyll` is a **dotfile**, so the action's own default (`include-hidden-files: false`) strips it, and strips `.well-known/` **entirely** — observed locally with the exact tar invocation from `action.yml:39` (GNU tar 1.35). This is directly relevant to C2 (security.txt at `/.well-known/`).
4. S001 is **current but incomplete**: its `v4.0.0` citation cannot evidence "exposes hidden-file inclusion" — that input first appears in v5.0.0. S002 and S006 are **still current, wording unchanged**.

## Candidates (all GET, ordinary curl, 2026-10-22T22:25:06Z–22:27Z UTC)

| # | URL | Status | Quote (≤25 words) | Verdict |
|---|---|---|---|---|
| A | https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site | 200, 151259 B | "Otherwise, disable the Jekyll build process by creating an empty file called `.nojekyll` in the root of your publishing source" | **ADMIT** — normative, current location of the retired bypass page's instruction; scope is "publish from a source branch" |
| B | https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site | 200, 154136 B | "Most external CI workflows deploy ... by committing the build output to the gh-pages branch ... and typically include a `.nojekyll` file" | **ADMIT as supporting** — branch-push pattern only; not a build-exclusion statement |
| C | https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/bypassing-jekyll-with-nojekyll | **404** (502 B body) | — | **REJECT** — retired; no redirect; do not cite |
| D | https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll | 200, 138096 B | "By default, Jekyll doesn't build files or folders that: ... Start with `_`, `.`, or `#`" | **ADMIT** — this is S006's source; currency re-check only |
| E | https://raw.githubusercontent.com/actions/upload-pages-artifact/fc324d3547104276b827a68afc52ff2a11cc49c9/action.yml (v5.0.0) | 200, 2895 B | "Include hidden files and directories (those starting with a dot) in the artifact. Excludes .git and .github regardless." default `"false"` (lines 17-20) | **ADMIT** — latest release tag (tags API: `v5` → fc324d3; `releases/latest` = v5.0.0, 2026-04-10T18:22:59Z) |
| F | https://raw.githubusercontent.com/actions/upload-pages-artifact/main/action.yml | 200, 2895 B | same lines 17-20; exclude at line 39 | **ADMIT** — HEAD = `5f327015a708106f6f1b7c9a633901af30fe80cb` (committed 2026-10-15T14:12:04Z, pushed 2026-10-19T06:30:47Z) |

Docs pages that do **not** mention `.nojekyll`, `hidden file`, `dotfile` or `well-known` (0 hits in extracted text): `about-github-pages`, `using-custom-workflows-with-github-pages` (S004's source), the Jekyll section landing, `creating-a-github-pages-site` for `hidden file`/`dotfile`/`well-known`. Docs therefore state the `.nojekyll` *mechanism* but nowhere state that dot-paths become *served* once Jekyll is bypassed — a documentation gap, marked [INFERENCE] below.

## S001 / S002 / S006 currency

- **S001 — current, with a citation defect.** Cited main commit `5f32701` **is** current HEAD (`diff action-cited-main.yml action-main.yml` → rc 0, sha256 `e8ce828a…`). Its other citation, v4.0.0 (`7b1f4a7`), has **no** `include-hidden-files` input; v4.0.0 lines 33-35 hard-code `--exclude=".[^/]*"`. `diff` v4→v5 shows the input block added only in v5.0.0 plus `upload-artifact` pin v4.6.2 → v7.0.0. Action: add v5.0.0 `fc324d3` as the released revision; keep v4.0.0 only for the pre-input exclude.
- **S002 — still current.** Verified from artifacts, not notes: v4.0.0 action.yml hard-codes the dot exclude (lines 35/53/71), v5.0.0 adds `include-hidden-files` default `"false"` (17-20). Releases API dates v4.0.0 2025-08-14, v5.0.0 2026-04-10. Claims hold verbatim.
- **S006 — still current.** Live page (200, quote D) still reads "Are located in a folder called `/node_modules` or `/vendor`, Start with `_`, `.`, or `#`, End with `~`, Are excluded by the `exclude` setting", with the "cannot be changed for GitHub Pages sites" context intact. No wording change since the 2026-10-19 fetch.
- Note for freshness: `main` differs from tag `v5.0.0` only at line 84 (`actions/upload-artifact` v7.0.0 → v7.0.1). The hidden-file contract is identical across tag and HEAD.

## Observed tar behaviour (local, sandbox, GNU tar 1.35)

Fixture: `index.html`, `.nojekyll`, `.well-known/security.txt`, `sub/.hidden`, `sub/deep/ok.txt`, `.git/config`, run twice with `action.yml`'s exact flags.
- default (`include-hidden-files` false): archive contains `./index.html`, `./sub/deep/ok.txt` — `.nojekyll`, `./sub/.hidden` and the **whole** `.well-known/` tree are absent.
- `include-hidden-files: true`: `.nojekyll`, `.well-known/security.txt`, `./sub/.hidden` present; `.git/` absent (`.git`/`.github` are unconditional).
- [INFERENCE] Consequently a GitHub Actions Pages deploy at defaults cannot serve `/.well-known/security.txt` or `/.nojekyll`; a publisher needs `include-hidden-files: true`. Branch publishing with `.nojekyll` is the only docs-backed alternative (candidate A).

## Commands (exit codes)

All in sandbox `/fast/scratch/hyaku/kake-r35/w1/ScoutPagesDotfilesSource/`; `TMPDIR` there, no `/tmp`.
- `curl -sS -L -o <file> -w '%{http_code} %{size_download}' <url>` ×3 docs pages → `200 94214`, `200 138096`, `200 141818` (rc 0).
- `curl ... api.github.com/repos/actions/upload-pages-artifact/releases/latest` → 200; `releases?per_page=10` → 200; `tags?per_page=10` → 200; `commits/main` → 200 (`5f32701…`).
- `curl -sS -I` old bypass URL → `HTTP/2 404` (rc 0).
- Docs search API with `client_name=docs`: `nojekyll` → 200, found 2; `".nojekyll"` → 200, found 2; `"include-hidden-files"` → 200, found 0.
- `diff action-v4.0.0.yml v5.0.0-action.yml` → rc 1 (expected, differences listed); `diff action-cited-main.yml action-main.yml` → rc 0.
- `tar --dereference --hard-dereference --directory tartest/site -cf … --exclude=.git --exclude=.github --exclude='.[^/]*' .` → rc 0, listing as above.

## Evidence pointers

- `/fast/scratch/hyaku/kake-r35/w1/ScoutPagesDotfilesSource/creating-a-github-pages-site.html:132` (quote A), sha256 `5f4762d6…`.
- `…/configuring-a-publishing-source-for-your-github-pages-site.html:122` (quote B), sha256 `850f69e7…`.
- `…/about-github-pages-and-jekyll.html:106` (quote D), sha256 `3968a6f0…`.
- `…/v5.0.0-action.yml:17-20,39` sha256 `f84e7590…`; `…/action-v4.0.0.yml:33-35,51-53,69-71` sha256 `4524ed61…`; `…/action-main.yml` = `action-cited-main.yml` sha256 `e8ce828a…`.
- `…/v5.0.0-README.md:46` documents the same input/default (`866ca499…`).

## Not verified

- No live deploy was run, and no owned host was contacted: whether Pages actually serves `/.well-known/` after an `include-hidden-files: true` deploy [INFERENCE from action.yml + tar only].
- Docs page "last updated" timestamps not read; currency is asserted from live 200 bodies, not revision history.
- I did not test macOS `gtar` or Windows tar variants beyond reading their identical lines in action.yml.
