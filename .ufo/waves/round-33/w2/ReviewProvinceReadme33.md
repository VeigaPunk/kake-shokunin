# ReviewProvinceReadme33 — PROVINCE 'Round-33 frontier step' + corpus/README 'Coverage — round 33'

Reviewed at tip `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` from my own clone
(`/fast/scratch/hyaku/kake-r33/w2/ReviewProvinceReadme33/clone`; base
`5777d5af79cac1ebf9144b348a9d274099e77338`; upstream read-only clone
`/fast/scratch/hyaku/kake-r33/ds4cc-upstream`). Verdict: no defects found.
Every checkable sentence is accurate; the count correction is right.

## Rewrite check (nothing earlier rewritten)
`git diff 5777d5a..0a0acfb -- PROVINCE.md corpus/README.md`: 26 insertions,
0 deletions — both files append-only (PROVINCE +16 at :133, README +10 at
:303). Stale line 122 intentionally untouched; correction lands as a separate
block, matching the corpus convention (QUALITY.md:162 "separate correction
blocks replace suffix edits").

## Count correction
`find scripts/fixtures/citing-set-hostile -maxdepth 1` at tip: six entries,
all type d (P1–P6). `git ls-tree` at base 5777d5af: same six; P6 added by
round-32 commit `2f2f12d` (`git log -- scripts/fixtures/citing-set-hostile/`).
Routed item 5 = "PROVINCE.md:122 still says 'five hostile fixture shapes'"
(round-32-verifier-spotcheck.md:136). Correction accurate.

## Sentence-level checks — PROVINCE append (:134–147)
- "line 122 above says 'five hostile fixture shapes'": PROVINCE.md:122 exact.
- "six since round 32 (P1–P6 under scripts/fixtures/citing-set-hostile/)":
  verified above. Caveat O1 below.
- "keyed P6 on the runner's structured refusal `code` (`reason_code`)":
  P6-commit-before-init/hostile.json carries `"reason_code":
  "setup_commit_before_init"`; selftest :44,:148,:228 consumes it. ✓
- "moved upstream from 1fbdb8ed to 7fc6aa2f (one commit, three
  /magga/frostbite/ pages, sitemap 97 → 100 locs)": upstream `git log -1
  7fc6aa2f` → parent `1fbdb8ed`, 2026-10-21T17:32:55Z; `diff-tree` → A
  magga/frostbite/{index.html,classic/index.html,remastered/index.html} +
  assets; `grep -c '<loc>'` sitemap.xml → 97 at 1fbdb8ed, 100 at 7fc6aa2f. ✓
- "records sitemap, page canonicals and the forge's deploy-run record (S065,
  S066)": sitemap-orphan-audit.md:184,217 sections exist; SOURCES.md:73–74
  rows; all 4 retained blob ids equal upstream blob ids. ✓
- "no operator-owned property was fetched … only network reads were the
  public GitHub repository clone and two GitHub API run listings": consistent
  with retained evidence (S065 clone-based; two `gh-actions-*.json` retained
  per S066). Exclusivity unverifiable from the tree; residual risk only.

## Sentence-level checks — corpus/README append (:303–311)
- Row-1 entry paths/section names/S-ids: all exist (:184, :217, SOURCES:73–74). ✓
- "sitemap 100 locs re-derived from retained bytes": `grep -c '<loc>'` on
  retained sitemap = 100. ✓
- "three new pages' canonicals clean under the offline policy": I re-ran
  `python3 -B scripts/canonical_audit.py --manifest
  .ufo/waves/round-33/sources/ds4cc-7fc6aa2f/canon-manifest.json --json`
  (manifest built in-sandbox, expectedCanonical = each page's sitemap loc):
  `{"findings":[],"pagesChecked":3,"verdict":"clean"}`, exit 0. ✓
- "sitemap-to-tree parity", "Pages deploy run", "failing apps-sdk test
  workflow", "older counts marked historical", "live serving not observed":
  all present in audit :217–244. ✓
- Row-2 vs SKILL.md:948–966: `code`/`reason_code` bullets match runner
  (citing_set_selftest.py:151,817–820 per-run scratch under
  /fast/scratch/hyaku/kake-r27; read_expected OSError reported :451; stray
  non-dir entries reported :739–743 / hostile :248–253; Git-pin mutants
  m3d/m3f/m3g open). ✓
- Trailing pin note: freshness-pins.json:34,36 still carry the stale raw
  values; "flagged stale" = audit :245–248 bullet (pq2Remote e6bd0718 "29
  commits behind" independently verified: `git rev-list --count
  e6bd0718..7fc6aa2f` = 29); "sweep's armed section" exists as
  `--section=armed` (freshness-sweep.md:22, QUALITY.md:414). ✓

## Observations (non-blocking)
- O1 wording: "routed low items repaired" (README :309) — item 7's
  "duplicated option tables" remains open per SKILL.md open bullet; two of
  three lows repaired. Slightly overbroad summary, not a defect.
- O2 wording: "has six since round 32" — true at the round-32 boundary; the
  set was five for most of round 32 (P6 added in 2f2f12d). Not misleading.

## Residual risk / not verified
- Exclusivity of round-33 network reads (negative claim): only recorded
  evidence checked, all consistent; cannot prove no other reads occurred.
- Sitemap-to-tree parity bullet accepted from wave-1 report
  ExecSitemapTreeParity.md as cited; not re-derived independently.
- Receipts under .ufo/waves/round-33/verification/ not re-run (counter runs
  belong to other seats).

## Tooling
None installed or updated; stock git/python3 sufficed (pacman paused anyway).
