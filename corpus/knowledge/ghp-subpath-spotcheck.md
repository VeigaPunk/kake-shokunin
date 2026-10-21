source: entry-specific evidence — /tmp baseline audit 2026-09-28 (~16:45Z, 2 352 paths across the three GHP rows); ~/Projects/webzites/src/reconcile.mjs:55-107 (absent since the 2026-10-12 prune); fleet/fleet.config.json; live GHP fetches 2026-09-28. Registry-backed only for the round-20 correction: S001, S005 (corpus/SOURCES.md). S019 is metadata authority, not platform authority.
verified-at: 2026-09-28 baseline audit and GHP fetches; webzites revision not recorded; source absence annotated at the r18 re-census. Historical-not-live-reverified. S019 in corpus/SOURCES.md governs metadata only.
recheck: local only — test -f ~/Projects/webzites/src/reconcile.mjs && sed -n '55,107p' ~/Projects/webzites/src/reconcile.mjs || echo 'reconcile.mjs absent: operator must restore webzites or retire the selection-code claims'; the /tmp baseline and live GHP figures have no recorded local path, so operator restore-or-retire is required where source vanished

# GHP subpath spotcheck — the blind spot behind `probe`/`reconcile`

Evidence: `/tmp` baseline audit 2026-09-28 (~16:45Z, 2 352 paths across the
three GHP rows), `~/Projects/webzites/src/reconcile.mjs` source read, <!-- r18 re-census 2026-10-14: ~/Projects/webzites/src/reconcile.mjs absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
`fleet/fleet.config.json`, live fetches (curl/python-urllib).

## What the existing verbs cover — and what they can't see

| verb | actually compares | blind spot |
|---|---|---|
| `webzites probe <id>` | the row's single `site.url` (status, final URL, title regex, marker literal) | every subpath; content rot under a passing root |
| `webzites grokbot reconcile <id>` | `site.url` body vs **ONE picked** `index.html` (BFS depth ≤ 2, hidden/`node_modules` skipped, best-scored by marker+title) | all other paths; `in-sync` masks byte drift |
| `kimi-surface.mjs sync-check <id>` | live kimi title+marker vs source | all kimi subpaths too (same shape) |

`reconcile` selection code (`src/reconcile.mjs:55-107`): collects
`index.html` files to depth 2, picks ONE by score (marker +2, title +1,
shallow tiebreak), compares only that file. A `match`/`in-sync` verdict
means *one file* matched — the rest of the tree is unobserved.

## `in-sync` masks byte drift on GHP

Verdict ladder: `match` needs byte equality; `in-sync` needs only
`titleEqual` + marker parity. On kimi rows that's correct (bytes churn
+~157B class). **On GHP rows it is not** — GHP serves artifact bytes
verbatim, so equality is achievable and `in-sync` means "same title,
different bytes" = real drift being waved through. 2026-09-28 evidence:
`charter-ghp` reported `in-sync` while live index was 50 919 B vs local
source 8 592 B (local HEAD 2 behind origin — `b74190e` baked a 50 KB
static index). A GHP `in-sync` should trigger `git fetch` in sourceDir
first, not confidence.

Precedent in keeper log (`grokbot-charter-ghp.log.md`, 2026-09-21): tick
said `reconcile=in-sync` while sourceDir was 10 commits behind;
`git pull --ff-only` → `match identical bytes`. `in-sync` on GHP is a
lag detector, not a pass.

## Spotcheck procedure (no new tooling needed; ~30 lines of python)

1. Enumerate `sourceDir` files (skip `.git`/`.github`/hidden/`node_modules`).
   For catch-all coverage include `.md` — GHP serves them raw (confirmed:
   `charter…/beats/*.md` → 200).
2. GET `live_url + rel` per file (concurrency ~12, UA-tagged, timeout 25 s).
   Record: status, redirect flag, sha256(live) == sha256(source).
3. **Normalize against `origin/main`, not the working tree** —
   `git -C <sourceDir> show origin/main:<rel>`. Classify:

   | live 200 + sha == origin/main | clean |
   | live ≠ origin/main | TRUE ROT — investigate |
   | live ≠ working tree but file absent on origin/main | local-ahead; the delta resolves on next operator push |
   | live 404 + file absent on origin/main | local-ahead (file unpushed) |
   | live 404 + file present on origin/main | TRUE ROT |

4. Report only the TRUE ROT rows + file them against the publish queue.

Working-tree noise is the normal case, not the exception: at baseline
time `ds4cc-marketplace` was **20 commits ahead** of `origin/main`
(120 working-tree diffs, all resolved by the `origin/main` compare —
including `robots.txt`, `sitemap.xml`, `404.html`, and
`marketplace/plugins/infinizoom/main.js` serving live-404 because they
are unpushed), `plazir-15-site` 5 ahead (5 diffs), `charter-ufo-fsd`
2 behind (1 diff). True rot found: **0**.

## GHP path semantics verified 2026-09-28 (contrast with kimi)

- `/dir` → 301 → `/dir/` → serves `dir/index.html`. `href="dir/"` works.
  **kimi has no directory indexes** (`dir/` 404, `dir/index.html` 200) —
  this asymmetry is why mirror nav links must be explicit `index.html`
  paths. Verified live: `plazir-15-site/snake`, `ds4cc.com/magga` both
  redirect-serve.
- `404.html` at root is honored as the custom 404 body (file present in
  `plazir-15-site`; not yet pushed for ds4cc — currently serves the
  stock GitHub 404).
- `.md`, `.json`, `.txt`, `.xml`, `.webmanifest` all served raw.
- Non-existent paths → 200-style GHP 404 page body with status 404
  (`title "Page not found"`); status alone is the check — unlike kimi's
  soft-200 preview-404, GHP returns a real 404 status.

## What this does NOT cover

- Live-only paths not in sourceDir (orphan files stay served after
  source deletion until a redeploy — detection needs sitemap crawl, not
  source walk).
- `.github/`, CNAME, workflow files — never servable.
- Binary assets spot-checked by hash only if enumerated; large trees
  (ds4cc: 2 614 files, ~1 874 text) take ~1 min at concurrency 12.
- kimi rows: same gap, but byte equality is meaningless there —
  kimi subpath coverage would need title+marker per path, not sha.

## Round-20 corrections (append-only; base `cb807bc`)

- Base `corpus/knowledge/ghp-subpath-spotcheck.md:83`: **[r20-correction 2026-10-19: CNAME is not in upload-pages-artifact's .git/.github/dotfile exclusion set; whether Actions serves /CNAME is an unverified prediction requiring an operator-authorized free read — S001, S005]**

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/ghp-subpath-spotcheck.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [ghp-subpath-spotcheck:c1] **HOLD** — The cited local reconcile source path is absent at this recheck. Surface: `/home/vgpnk/Projects/webzites/src/reconcile.mjs`.
- [ghp-subpath-spotcheck:c2] **UNVERIFIABLE** — The current webzites behavior is as documented: probe checks only the row root URL, reconcile selects one shallow index.html, and in-sync can accept title/marker parity without byte equality, masking GHP byte drift. Surface: `command -v webzites; /home/vgpnk/Projects/webzites/src/probe.mjs; /home/vgpnk/Projects/webzites/src/reconcile.mjs`. Unverifiable: The cited implementation files and webzites executable are absent locally; no current implementation surface can decide these behaviors. The historical 2026-09-28 byte example also has no reproducible audit-file path.
- [ghp-subpath-spotcheck:c3] **HOLD** — Current GHP slashless /snake and /magga paths redirect to slash URLs, whose response bytes match their explicit index.html paths. Surface: `https://veigapunk.github.io/plazir-15-site/snake; https://ds4cc.com/magga; both slash and index.html forms`.
- [ghp-subpath-spotcheck:c4] **HOLD** — The Plazir Pages site serves its root 404.html bytes for missing routes; ds4cc.com does not expose a 404.html file and currently returns the stock GitHub Pages 404 body. Surface: `https://veigapunk.github.io/plazir-15-site/404.html; https://veigapunk.github.io/plazir-15-site/__r23-nonexistent-20261021__; https://ds4cc.com/404.html; https://ds4cc.com/__r23-nonexistent-20261021__`.
- [ghp-subpath-spotcheck:c5] **STALE** — The current Plazir GHP missing-page document title is `Page not found`. Surface: `GET https://veigapunk.github.io/plazir-15-site/__r23-nonexistent-20261021__; raw GET https://veigapunk.github.io/plazir-15-site/404.html`. Correction: As of 2026-10-21, the missing path returns HTTP 404 with bytes identical to /404.html, whose HTML title is `Not found — Plazir-15`; the body still contains the words `Page not found`.
- [ghp-subpath-spotcheck:c6] **STALE** — The note's unresolved `/CNAME` availability question is still open for the current ds4cc.com deployment. Surface: `https://ds4cc.com/CNAME`. Correction: As of 2026-10-21, GET https://ds4cc.com/CNAME returns HTTP 200 with raw body `ds4cc.com`, so the current ds4cc.com deployment exposes `/CNAME`; this does not establish which publishing workflow supplied it.
- [ghp-subpath-spotcheck:c7] **HOLD** — The current ds4cc Kimi mirror reproduces the directory-index contrast on its linked omarchy-usage path: the directory URL is 404 while explicit index.html is 200. Surface: `https://ds4cc.kimi.page/omarchy-usage/; https://ds4cc.kimi.page/omarchy-usage/index.html`.

## Round-26 source recheck

- Round-26 source recheck (2026-10-21, append-only; original lines unchanged). The round-20 correction lines in this entry cite S001 and S005 (line 95). Each was judged against bytes re-fetched 2026-10-21 (`.ufo/waves/round-26/fetched/`, receipts `.ufo/waves/round-26/rechecks/S0NN.json`) and holds: `CNAME` is not matched by S001's `.git`, `.github` or `.[^/]*` exclusions; S005 still says the CNAME file is ignored under a custom Actions workflow. Whether Actions serves `/CNAME` stays an unverified prediction. Ledger pairs in `.ufo/waves/round-26/statements.json`; found by the falsify wave (w2/CounterCritic.md).
