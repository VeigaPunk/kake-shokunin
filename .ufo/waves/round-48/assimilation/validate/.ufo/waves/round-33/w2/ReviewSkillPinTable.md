# ReviewSkillPinTable — SKILL.md "Upstream source moved after a pin — round 33" (SKILL.md:930-946) at 0a0acfb1

Seat: KakeR33.ReviewSkillPinTable (freshness, falsify). Method: clone of the lane at the tip
(`/fast/scratch/hyaku/kake-r33/w2/ReviewSkillPinTable/clone`), L1 upstream clone
`/fast/scratch/hyaku/kake-r33/ds4cc-upstream` (read via ls-tree/show/rev-parse only), plus the
row's own commands re-run. Lane tree touched only for this report.

## Per-row verdicts

**R1 local checkout behind remote — GROUNDED.** `git ls-remote https://github.com/VeigaPunk/ds4cc-marketplace.git HEAD` → `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` (exit 0); `git -C ~/Projects/ds4cc-marketplace rev-parse HEAD` → `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` (exit 0, read-only). `git -C ds4cc-upstream log --oneline 1fbdb8ed..7fc6aa2f` → one commit. Action followed: S065 (SOURCES.md:73) names a sandbox clone; the L1 clone exists and the operator checkout still sits at `1fbdb8ed` (no fetch observed). New bytes came from the sandbox clone (retained dir blob ids below).

**R2 blob-identical read paths — GROUNDED, pointer broken at-rev (F1).** `git rev-parse <old>:<p> <new>:<p>` on the upstream clone for the four S062 paths: render.yaml `d17ab7e5`, apps-sdk/Dockerfile `ee0b6381`, apps-sdk/src/server.ts `649726df`, .dockerignore `d650445a` — identical at both commits; `git diff --stat 1fbdb8ed 7fc6aa2f -- <4 paths>` empty, exit 0. Action followed: S062 row untouched (still `1fbdb8ed`-scoped; the audit section records "changes none of the four files S062 retains", sitemap-orphan-audit.md:194). Caveat: "every path a row reads" covers only S062's four files; `magga/index.html` and `sitemap.xml` did change — their corpus claims are handled by R4, not by this row, which is a fair partition. Cited `w1/ScoutRenderFilesStillCurrent.md` exists in the lane working tree but is untracked at 0a0acfb.

**R3 changed read path — GROUNDED (conditional not triggered).** The `git diff --stat <old> <new> -- <paths>` result is empty for the S062 scope, as stated "(empty this round)"; the repo-level diff has 12 changed files, all under the R4/R5 scope. No re-open/correction was owed.

**R4 sitemap population — GROUNDED.** Retained `sitemap.xml` blob `67d8c7a5` equals the upstream blob at 7fc6aa2f; `grep -c '<loc>'` on retained bytes → 100; upstream `1fbdb8ed:sitemap.xml` → 97; the three added locs are exactly the three frostbite URLs. `python3 -B .ufo/waves/round-33/c2_pin_count.py --rev 0a0acfb1 --repo <clone>` → `met: 4` of 4, exit 0 (c1–c4 all true; observed clean ×3 = stated). Section states `sitemap-locs: 100` beside the commit and marks the 93/97 counts historical (lines 208, 239-244). Action followed.

**R5 new pages under audited path — GROUNDED, pointer broken at-rev (F1).** I ran `scripts/canonical_audit.py --manifest` per page on the retained bytes (manifest in the retained dir, `file` relative to it — absolute paths are refused as `input_invalid`, worth noting): 3 × `{"verdict":"clean"}`, exit 0. `scripts/base_path_audit.py --manifest` with `basePath "/"` over all three pages → `clean`, exit 0, `referencesChecked: 24` (w1 report says "21 relative or same-host" — a counting-basis difference, same verdict, F3). The section's "static result, not a deploy or index claim" framing is honored (line ~216 "Static source parity only"). Cited `w1/ExecNewPagesRefIntegrity.md` exists but is untracked at 0a0acfb.

**R6 whether the commit was published — GROUNDED, re-verified live today.** `gh api 'repos/VeigaPunk/ds4cc-marketplace/actions/runs?head_sha=7fc6aa2fc12451dd451fed5a9ee7125f3a90e884'` (gh 2.102.0, exit 0) → total_count 3: run 39644779773 "Deploy marketplace to GitHub Pages" `success`, 39644779775 "Validate Plugin Manifests" `success`, 39644779805 "Test Apps SDK wrapper" `failure`. Retained `gh-actions-runs-7fc6aa2f.json` sha256 `92bd3b31…ce1c` matches S066's cited prefix; the apps-sdk JSON matches `f2056e8b…67e`… (prefix `f2056e8b` verified). Action framing honored: the corpus says the run record "is GitHub's record of the workflow, not an observation of what ds4cc.com serves now" (sitemap-orphan-audit.md:231-233; corpus/README.md:307).

**R7 live predicate names old state — GROUNDED.** freshness-pins.json:34 `pq2Remote` = `e6bd0718…`, :36 `sitemapStatus` = 404. `git rev-list --count e6bd0718..7fc6aa2f` on the upstream clone → 29 (doc says 29; correct — it was already 28 behind at `1fbdb8ed`). Flagged, not re-pinned: sitemap-orphan-audit.md:245-248 "Not repaired, flagged"; lessons/round-33.md "Carried open" names both pins; pins file still `"round": 24`. The doc honestly notes round-23 live observations (200/96 locs, line 135) already contradicted `sitemapStatus` before this commit, so staleness predates the move — the flag is still correct.

## Findings

- **F1 (moderate): provenance break in the table's own pointers.** `.ufo/waves/round-33/w1/` is entirely untracked at 0a0acfb (`git ls-files --error-unmatch .ufo/waves/round-33/w1/ExecNewPagesRefIntegrity.md` → pathspec error; `git log -- .ufo/waves/round-33/w1` → empty). Every `w1/*.md` citation in the table and its intro (`ScribeSkillPinAdvanceTable` draft, R2, R5) resolves only in the lane working tree — while the round's own counter contract is "reads committed bytes at the revision only; never the working tree". Earlier rounds' w1 reports ARE tracked (`git ls-files .ufo/waves/round-21/w1/` lists them). Either commit the w1 reports or don't cite them as evidence.
- **F2 (minor): scope note on R2/R3.** "Every path a row reads" = S062's four files only. If any future row pins `magga/index.html` or `sitemap.xml`, R3's conditional must fire; currently fair.
- **F3 (cosmetic): reference-count basis.** base_path_audit counts 24 references vs the w1 report's "21 relative or same-host"; both clean, not a defect.
- Observation: the flag line names `pq2Remote`/`sitemapStatus`; the coupled `pq2Unpushed: 20` pin is equally stale (local count is 0) and is carried by the same armed predicate — arguably covered, but the flag doesn't name it.

## Verification gaps

Did not read w1 report contents (untracked; lane WT is not evidence at this rev), so the "21 references" and tree-parity internals are unconfirmed as written. Armed sweep not run (fetches owned sites — out of bounds). No tools installed; `gh` 2.102.0 already present at `~/.local/bin/gh`.
