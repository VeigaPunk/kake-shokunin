# KakeR35.ScribeMistakeMine — round-35 `## Mistakes` draft

Seat: scribe, wave 1. Swept revision `318561efa67206699fdaf259ffb86e39f2d916a8` in clone
`/fast/scratch/hyaku/kake-r35/w1/ScribeMistakeMine/clone`. Deliverable:
`/fast/scratch/hyaku/kake-r35/w1/ScribeMistakeMine/mistakes.md` (6 rows in the
`corpus/lessons/round-34.md:63` shape, sweep transcript pasted).

## What I built

Six Mistakes rows for the round-35 lesson: the four author defects the round-34 closure routed and
no lesson row mined (published census target, misdescribed lookup control, missing registry row,
S074 overclaim), plus two extra rows this sweep found (carried-open ledger count/pointer errors;
the landing table mined 1 of 5 routed defects). Each row names class, committed evidence, the
criterion or seat that captured it, and the round-35 fix path. Commands and outputs are pasted in
the deliverable; only observed runs are marked observed.

## Findings

1. **All four routed defects are still uncorrected in committed bytes at `318561e`.**
   `git grep -c 'keys on the case directory name' 318561e -- corpus/lessons/round-34.md` → 1;
   `git grep -c 'no og: occurrence' 318561e -- corpus/SOURCES.md corpus/lessons/round-34.md` → 1
   and 1; `git grep -n 'link-preview-audit' 318561e -- SKILL.md` → no match, exit 1. The
   round-35 wave items that fix them now exist as drafts (`ScribeControlCorrection/correction.md`
   8261 B, three append sites; `ScribeSkillRegistryRow/registry.md` 7128 B; `ReviewS074Head/s074-note.md`
   2348 B), but none is landed at `318561e`, so committed text still carries the defects.
2. **The census target is confirmed published.** `.ufo/waves/round-34/verification/c2-at-d08d8de.json:56-63`
   gives seven `census.derived` values; the blob is added at `a2fe31b`, before the entry at
   `9ef758c`. The round-35 C2 counter drops the census condition (grep `census` →
   `.ufo/waves/round-35/sealed_count.py` has none) and its transcription control fails
   (`control-c2-transcript.json`: `probesPassed` 8, target 9, `copiedShare` 0.9951).
3. **`prebuild_leak_check.py` does not work at the revision its own wave item names.** At
   `--receipt-rev d08d8de…` it exits 2, because the receipt is not in that tree. At
   `a2fe31b…` it exits 1 with `matched values: pages=102 … og-url-equals-canonical=87`.
   If QUALITY criterion (b) or the wave report quote the d08d8de form, they are quoting an
   exit that cannot happen. L1 should use `a2fe31b` (receipt added) and cite exit 1.
4. **The lookup control's true bytes are confirmed.** Bundle
   `r34-c1-lookup-dcef39b5.bundle` at `dcef39b5:scripts/link_preview_audit.py:1-16` hashes
   argv plus each relative path and file content; sha256 of the file is
   `a2e274c0ce9168bb10d7217a8c9a09c2516aea1c2c148dbf583306dcc56730ec`, equal to
   `toolSha256` in `control-c1-lookup-dcef39b5.json`. "Keys on the case directory name" is
   false; the retained item's explanation needs the append correction.
5. **S074 confirmed:** 3 `og:` occurrences, all in `<head>` (og:title/og:image/og:description),
   against "no og: occurrence" at `corpus/lessons/round-34.md:41` and `corpus/SOURCES.md:82`.
   No round-35 check enforces absence claims in a Gate reason; the fix is append-only.
6. **Checks shown able to fail (copied, not landed):**
   `registry_row_check.py` exits 1 at `318561e` (`missing tools: scripts/link_preview_audit.py`,
   7 scripts scanned); `control_description_check.py` exits 1 on the round-34 row (anchor
   `dcef39b5`); `prebuild_leak_check.py` exits 1 on the round-34 receipt as in finding 3.
   Script hashes: `checks.sha256` (`28712fbc…`, `fcc77676…`, `b77e3a1f…`).

## Commands and exits

- `git clone` + `git checkout 318561e` in sandbox → exit 0, HEAD `318561ef…`.
- `git fetch …/r34-c1-lookup-dcef39b5.bundle 'refs/heads/*:refs/heads/r34/*'` → exit 0, head
  `dcef39b5f4e8…`.
- `zcat …/S074.html.gz | grep -o 'og:' | wc -l` → 3; head-only → 3.
- `python3 -B checks/registry_row_check.py --repo clone --rev 318561e` → exit 1.
- `python3 -B checks/control_description_check.py --repo clone --bundle …r34-c1-lookup-dcef39b5.bundle
  --revision dcef39b5 --path scripts/link_preview_audit.py --doc corpus/lessons/round-34.md
  --doc-rev 318561e --anchor dcef39b5` → exit 1.
- `python3 -B checks/prebuild_leak_check.py --repo clone --receipt-rev a2fe31b …` → exit 1;
  same command with `--receipt-rev d08d8de` → exit 2.
- `git grep`/`awk`/`sed` sweeps over the closure, lesson and report → outputs in deliverable.

## Touched surfaces

- Lane: this report only (`.ufo/waves/round-35/w1/ScribeMistakeMine.md`). No tracked file, Git
  index, jj state or sibling lane was modified; no commit, push or fetch into the lane.
- Sandbox: `mistakes.md`, `lookup_tool.py`, `checks/` + `checks.sha256`, `clone/`, `tmp/` under
  `/fast/scratch/hyaku/kake-r35/w1/ScribeMistakeMine/`.

## Out of scope / not verified

- No C1 or C2 claim verification; no sealed counter run against the lane; nothing under
  `/fast/scratch/hyaku/kake-r35/sealed/` was read, listed or statted, and no live URL was fetched.
- The correction drafts were read for their sites and claims; the probe results they report
  (28/28 renamed, 7/28 commented) were not rerun. The three checks are wave deliverables, not
  landed at `318561e`, and their exits belong to the pinned copies.
- No tool installs (none needed); no pacman transaction.
