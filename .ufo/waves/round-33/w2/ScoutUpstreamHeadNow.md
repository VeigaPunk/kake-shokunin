# ScoutUpstreamHeadNow — is 7fc6aa2f still the upstream head, and did the forge record anything new?

Seat: KakeR33.ScoutUpstreamHeadNow, wave 2 (falsify), freshness. Lane rev inspected: 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0.
Sandbox: /fast/scratch/hyaku/kake-r33/w2/ScoutUpstreamHeadNow/ (fresh API responses under `fresh/`, retained copies under repo root).
Verdict: **no falsification.** C2's section is not stale as of 2026-10-22T20:15Z; head is unchanged and no new workflow run exists. One repo-metadata event is new and is not a commit.

## Observed facts

1. Remote head unchanged. `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD refs/heads/main` at 2026-10-22T20:14:58Z, exit 0:
   `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 HEAD` and `... refs/heads/main`. Same value at 20:12Z.
2. Runs for the pinned commit are byte-identical to S066's retained bytes.
   `gh api 'repos/.../actions/runs?head_sha=7fc6aa2f...' > fresh/gh-actions-runs-7fc6aa2f.json`, exit 0.
   sha256 fresh = `92bd3b31909ebf657e318c8211980f2007a71c8f03dbd3474f16e4fa4cc1ce1c` = sha256 of the retained
   `.ufo/waves/round-33/sources/gh-actions-runs-7fc6aa2f.json`; normalized JSON diff empty (`IDENTICAL_runs`). total_count 3:
   `39644779805` Test Apps SDK wrapper completed/**failure** created 2026-10-21T17:32:59Z updated 17:33:16Z (run#1000);
   `39644779775` Validate Plugin Manifests completed/success updated 17:33:31Z (run#940);
   `39644779773` Deploy marketplace to GitHub Pages completed/**success** updated 17:33:42Z (run#1003).
3. No workflow run anywhere in the repo after that push. `gh api 'repos/.../actions/runs?per_page=5'`, exit 0: total_count 2945,
   newest created_at = 2026-10-21T17:32:59Z (the three runs above); next is 39572438796 / 39572438737 on 1fbdb8ed at 2026-10-21T08:51Z.
4. `apps-sdk.yml` main-branch list unchanged in content, exit 0: total_count 988 both retained and fresh; newest
   `39644779805` 7fc6aa2f failure run#1000, then 39572438715 (1fbdb8ed), 39570367127 (95dbeb69), 39440278959 (6e888784),
   38642441807 (9ec6e919), 38641094581 (480dd05f). Fresh fetch at per_page=30 (sha `afb54933…`) has 30 runs; the 6 runs in
   S066's retained page match field-for-field with zero differing keys, and all retained ids are present. The hash difference is
   page size only, not changed data.
5. Newest forge event is a ref deletion, not a commit. `gh api repos/.../` gives `pushed_at=2026-10-22T06:13:24Z`,
   `default_branch=main`, open_issues=2. `gh api 'repos/.../issues/4/events'` shows `head_ref_deleted 2026-10-22T06:13:24Z`
   (issue 4 "Add omegaG standalone site at ds4cc.com/omegag/", closed 2026-08-14T20:54:03Z); this is what moved `pushed_at`.
   Branch heads: main 7fc6aa2f, feat/the-sshid-sandbox af234c95 (2026-08-03), fix/xbreed-safe-dispatch 4b941c31 (2026-07-28),
   fleet/canonical-vault-links 4073fac5 (2026-09-25), modelbenx e633b385 (2026-07-31). No branch advanced past the pin.
6. Local checkout still lags as S065 states. `git -C ~/Projects/ds4cc-marketplace rev-parse HEAD` (read-only), exit 0:
   `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`; main's parent is 1fbdb8ed.
7. Retained bytes equal head's tree, so the section still describes head. `git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream
   ls-tree -r 7fc6aa2f` vs lane `ls-tree -r 0a0acfb` under `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/`, exit 0: blob ids equal
   for all four — sitemap.xml `67d8c7a50dc3a3734ce4be97ffa4810e1e257e12`, magga/frostbite/index.html `e0d9ee29…`, classic/index.html
   `12c58e2d…`, remastered/index.html `4e6d70ae…`.
8. Section figures reproduce from retained bytes: XML parse yields 100 `<loc>`; the three frostbite locs sit on file lines 15-17
   (`https://ds4cc.com/magga/frostbite/`, `/classic/`, `/remastered/`); `git show 1fbdb8ed:sitemap.xml | grep -c '<loc'` = 97.
   So "sitemap-locs: 100", "+3 locs", and the three canonical lines match head (C2 knowledge entry lines 203-206 at 0a0acfb).

## Assessment against the item

- 7fc6aa2f is still main's head 26.7 hours after the commit, and is still the newest commit on every branch.
- The forge recorded nothing that contradicts S065/S066: same 3 runs, same conclusions, same totals. The single new datum is a
  branch deletion on an August issue; `pushed_at` is the only field that looks newer, and it is not a push.
- Because retained bytes still equal head's tree, C2's measured numbers (100 locs, three clean canonicals) remain valid without
  re-measurement. I re-derived the loc count and the three URLs independently of the counter.
- Residual freshness risk, advisory only: C2's counter `c2_pin_count.py` tests four offline content/journal conditions and never
  contacts the remote, so a future upstream commit would age the section silently and the counter would still report 4. This does
  not contradict the declared contract, it just means freshness here is a point-in-time fact, not a monitored invariant.
- Not verified: what ds4cc.com actually serves (owned host; not fetched, per bounds), and whether the Deploy Pages run's success
  means the live site reflects 7fc6aa2f. The section disclaims both, so neither is a claim error.

## Commands run (all against read-only sources)

- `mkdir -p .../tmp` + `export TMPDIR=.../tmp`; sandbox clone not needed, no writes outside sandbox and this report.
- `git ls-remote <public repo> HEAD refs/heads/main` — exit 0 (twice).
- `gh api 'repos/.../actions/runs?per_page=5' --jq ...` — exit 0.
- `gh api 'repos/.../actions/runs?head_sha=7fc6aa2f...&per_page=10'` — exit 0.
- `gh api 'repos/.../actions/workflows/apps-sdk.yml/runs?branch=main&per_page=5'` and `&per_page=30` — exit 0.
- `gh api repos/.../`; `gh api 'repos/.../branches?per_page=20'`; `gh api 'repos/.../tags?per_page=5'`; `gh api 'repos/.../issues?state=all&sort=updated&per_page=5'`; `gh api repos/.../issues/4`; `gh api 'repos/.../issues/4/events?per_page=10'` — exit 0.
- `git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream ls-tree -r 7fc6aa2f -- sitemap.xml magga/frostbite`, `git show 1fbdb8ed:sitemap.xml` — exit 0 (read via git show/ls-tree only).
- `git -C <lane> ls-tree -r 0a0acfb -- .ufo/waves/round-33/sources/ds4cc-7fc6aa2f`; `git -C <lane> show 0a0acfb:<file>` — exit 0 (object reads; lane working tree untouched).
- Local read-only `git -C ~/Projects/ds4cc-marketplace rev-parse HEAD` / `log -1` — exit 0, no fetch.
- Tooling: nothing installed or updated.

## Evidence pointers

- Retained run records: `.ufo/waves/round-33/sources/gh-actions-runs-7fc6aa2f.json` (sha 92bd3b31…ce1c),
  `.ufo/waves/round-33/sources/gh-actions-apps-sdk-runs-main.json` (sha f2056e8b…67e4) at 0a0acfb.
- S065, S066: `corpus/SOURCES.md:73`, `:74` at 0a0acfb.
- C2 section: `corpus/knowledge/sitemap-orphan-audit.md:184-215` at 0a0acfb (measured lines 203-206, disclaimer 211-215).
- Retained bytes: `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/{sitemap.xml,magga/frostbite/index.html,magga/frostbite/classic/index.html,magga/frostbite/remastered/index.html}`.
- Sandbox artifacts: `/fast/scratch/hyaku/kake-r33/w2/ScoutUpstreamHeadNow/{retained-runs.json,retained-apps-sdk.json,sitemap-7fc6aa2f.xml,fresh/gh-actions-runs-7fc6aa2f.json,fresh/gh-actions-apps-sdk-runs-main.json}`.
