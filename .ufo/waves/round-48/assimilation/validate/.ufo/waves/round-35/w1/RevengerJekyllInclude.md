# RevengerJekyllInclude — `.well-known/` and `include` in the Pages branch Jekyll build

Seat KakeR35.RevengerJekyllInclude, wave 1, 2026-10-22. Attacked the round-35 freshness ground
(S078–S085, S006, S080) from the code GitHub Pages actually runs: github/pages-gem plus the
Jekyll version it pins. Sealed directory untouched. No lane git state touched; clones and
deliverables live only under /fast/scratch/hyaku/kake-r35/w1/RevengerJekyllInclude/. No tool
installs were needed (none recorded).

## Named commits
- github/pages-gem master HEAD, fetched 2026-10-22: `cd7369a21e3ec3f20753012da8e312859dca41a4` (2024-11-27).
- Latest release tag v232 = `c34277c8ff6a2c86bfb19f17f35de573e796f030`; same pin:
  `lib/github-pages/dependencies.rb:10` `"jekyll" => "3.10.0"` at both commits (verified on both).
- Jekyll tag v3.10.0 (the pinned version, only 3.10.x tag on jekyll/jekyll per ls-remote):
  `715f33b874445a8e5d0adf36e0ffa67f7d7627d3`.

## Commands (exit codes in parens)
1. `git clone -q --depth 1 https://github.com/github/pages-gem pagem` (0)
2. `git clone -q --depth 1 --branch v3.10.0 https://github.com/jekyll/jekyll jekyll310` (0); HEAD 715f33b8
3. `cat -n` of pages-gem `github-pages.gemspec`, `lib/github-pages/configuration.rb`; jekyll `lib/jekyll/entry_filter.rb`, `reader.rb`, `configuration.rb` ranges, `utils.rb` ranges (0)
4. `git ls-remote --tags` both repos (0); `git fetch --depth 1 origin c34277c8…` + `git show c34277c8:lib/github-pages/dependencies.rb` (0)
5. `grep -ri nojekyll` over the full pages-gem clone and full jekyll clone (exit 1 both = no matches); grep over lane `.ufo/waves/round-35/sources/` (exit 1)

## Q1 — does `.well-known/` publish by default on a branch Jekyll build? NO
- `lib/jekyll/reader.rb:42` (715f33b8): `dot = Dir.chdir(base) { filter_entries(Dir.entries("."), base) }` — every source-root entry passes through EntryFilter; survivors split at `:43-53` into dirs/pages/static files. Rejected entries are never read into the site.
- `lib/jekyll/entry_filter.rb:6-8`: `SPECIAL_LEADING_CHARACTERS = [".", "_", "#", "~"]`.
- `entry_filter.rb:48-51`: `special?` is true when entry or basename starts with one of those chars, so `.well-known` is special.
- `entry_filter.rb:32-41` `filter`: keeps included entries first, then rejects `special?(e) || backup?(e) || excluded?(e)`; `excluded?` (`:57-66`) consults only `site.exclude`.
- So a root `.well-known` is dropped unless it is in `include`. Matches retained S006 (GitHub Docs, About GitHub Pages and Jekyll): "By default, Jekyll doesn't build files or folders that … Start with `_`, `.`, or `#` … use the `include` setting".

## Q2 — does GitHub Pages add default `include` entries? NO
- pages-gem `lib/github-pages/configuration.rb:15-30` DEFAULTS (cd7369a2): `"jailed"`, `"plugins"`, `"future"`, `"theme"`, `"markdown"`, `"kramdown"`, `"exclude" => ["CNAME"]` (line 29) — no `"include"` key.
- `configuration.rb:49-63` OVERRIDES: `"lsi"`, `"safe" => true`, `"plugins_dir"`, `"whitelist"`, `"highlighter"`, `"kramdown"`, `"gist"` — no `"include"` key.
- `configuration.rb:84`: pages defaults are deep-merged over `Jekyll::Configuration::DEFAULTS`; Jekyll 3.10.0 `lib/jekyll/configuration.rb:20` is the only default include: `"include" => [".htaccess"]`.
- `utils.rb:57-59` (mergable? = Hash/Drop only): arrays are replaced, not merged — a user `include:`/`exclude:` replaces those defaults entirely (`configuration.rb:96` merges user_config over defaults; `:107` merges OVERRIDES last).

## Q3 — does `include: [".well-known"]` override the dot exclusion? YES
- `entry_filter.rb:36-37`: `next false if included?(e)` short-circuits BEFORE the `special?`/`excluded?` rejection at `:39`.
- `entry_filter.rb:43-46`: `included?` matches the entry or its basename against `site.include`.
- `entry_filter.rb:117-120`: glob match is `File.fnmatch? || start_with?` on full paths, so including `.well-known` also keeps `.well-known/security.txt` (prefix `…/.well-known`).
- Caveats: (a) include does not rescue symlinks — pages OVERRIDES forces `"safe" => true` (`configuration.rb:51`) and `entry_filter.rb:73-75` rejects outside-source symlinks regardless of include; (b) `include: [".well-known"]` drops Jekyll's default `[".htaccess"]` (arrays replace, Q2); (c) user `exclude:` also drops pages' `["CNAME"]`, re-added only when the user exclude equals Jekyll's default (`configuration.rb:158-163`).

## Q4 — what does `.nojekyll` do? Not in any code Pages runs here [pipeline behavior = INFERENCE]
- grep for `nojekyll` over the full pages-gem clone at cd7369a2 and the full jekyll clone at 715f33b8: zero matches (exit 1), including pages-gem README/docs. The gem "Bootstrap[s] the GitHub Pages Jekyll environment locally" (`github-pages.gemspec:13`).
- Inference: the bypass is implemented in the closed-source Pages build pipeline before the gem runs — a root `.nojekyll` skips this Jekyll build and publishes branch files verbatim (dotdirs included), which also removes the whole include/exclude question. Grounded only in the code-level absence above plus GitHub's public docs guidance; no retained round-35 row contains the string "nojekyll" (grep over `sources/` exit 1), so this answer has no retained-row ground yet — freshness gap the L1 may want to close.

## Freshness deltas vs retained rows
- S080 is Jekyll 4.4.1 documentation ("With Jekyll 4, the include configuration option entries override the exclude option entries"; ".htaccess is a good example since dotfiles are excluded by default"). Pages runs 3.10.0: same practical outcome, but via filter ordering (`entry_filter.rb:36-39`) where include also beats exclude/special at 3.10; Jekyll's built-in include of `.htaccess` (`configuration.rb:20`) explains the S080 example.
- Read-back to C2: S079 says "Create a text file called security.txt under the .well-known directory of your project". On a branch-built Pages site that path is NOT served by default (Q1); the publisher needs `include: [".well-known"]` in `_config.yml` or a root `.nojekyll`. `/security.txt` (top-level, non-dot) survives the default build (S081 notes both locations).

## Not verified
- Production pipeline `.nojekyll` handling (closed source; docs.github.com not fetched — not a named URL for this seat).
- rubygems.org latest `github-pages` release number (git tags only: v232 latest).
- `actions/jekyll-build-pages` / upload-artifact behavior (not named for this seat; S001/S002 territory).

Every claim above is a quoted line at a named commit except the three marked INFERENCE/not-verified items.
