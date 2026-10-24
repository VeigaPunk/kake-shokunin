## Verdict

C1 T05 is absent locally at the observation time, and its sole cite is already accurately annotated as unverifiable for current publishing configuration. The live `--section=paths` sweep nevertheless reports the target as `newMissing` because the exact file token is not in `pins.pathsMissSet` (the parent checkout token is pinned). Recommend integrating the observed miss into that set; no cite-line append is warranted. This is author-side evidence, not independent admission.

## Findings

- **P2 — C1 freshness pin omits an observed missing target.** Exact command: `node scripts/freshness-sweep.mjs --section=paths --json` (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`). Exact output: exit `1`; `sections.paths.setDelta.newMissing` includes `~/Projects/plazir-15-site/.github/workflows/pages.yml`. The round-open `pathsMissSet` contains `~/Projects/plazir-15-site` but not this file token. Impacted claim/axis: C1, freshness. Smallest fix: add `~/Projects/plazir-15-site/.github/workflows/pages.yml` to `corpus/knowledge/freshness-pins.json` `pathsMissSet`, backed by this receipt.

  The single cite is `SKILL.md:461`; the full ±3-line context is lines 458–464. Its absence language is on the citing line itself (`absent locally`), satisfying the sweep's per-citation annotation rule. The precise cite classification and C1 receipt are:

```json
{
  "id": "T05",
  "token": "~/Projects/plazir-15-site/.github/workflows/pages.yml",
  "class": "newMissing",
  "observedAt": "2026-10-21T11:49:43Z",
  "state": "absent",
  "observation": {
    "commands": [
      "date -u +%Y-%m-%dT%H:%M:%SZ",
      "test -e /home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml",
      "stat -c '%n %w %y' /home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml",
      "ls -la /home/vgpnk/Projects",
      "git -C /home/vgpnk/Projects/plazir-15-site log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/plazir-15-site remote -v"
    ],
    "output": "2026-10-21T11:49:43Z; test_exit=1; stat: cannot stat '/home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml': No such file or directory (os error 2); stat_exit=1; ls -la /home/vgpnk/Projects: 0 files, 24 dirs, no plazir-15-site entry; ls_exit=0; git log and remote both failed with fatal: cannot change to '/home/vgpnk/Projects/plazir-15-site': No such file or directory; each exit 128. Output abbreviated faithfully."
  },
  "event": "W7 ~/Projects prune/migration: later lane annotations attribute the removal to 2026-10-12; the primary round-18 census records the checkout absent on 2026-10-14 after the round-17 present observation (~2026-09-29), so the exact removal time is not independently established.",
  "cites": [
    {
      "cite": "SKILL.md:461",
      "lineText": "- [property-map:c40] **UNVERIFIABLE** — The front is currently published by GitHub Actions on pushes to `main`. Surface: `/home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml`. Unverifiable: The mapped checkout and workflow are absent locally; the one public page GET confirms served HTML but cannot establish the current GitHub Actions or Pages deployment configuration.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    }
  ]
}
```

## Checked and held

- Current filesystem: `test -e /home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml` returned `test_exit=1`; `stat -c '%n %w %y' /home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml` returned `stat: cannot stat '/home/vgpnk/Projects/plazir-15-site/.github/workflows/pages.yml': No such file or directory (os error 2)`. The nearest existing ancestor is `/home/vgpnk/Projects`; `ls -la` showed 24 directories, 0 files, and no `plazir-15-site`. Its observed mtime was `2026-10-21 05:19:01.033916520 -0300` (the ds4cc reappearance time); this bounds only subsequent top-level changes, not the earlier removal.
- The target directory is not a local Git repository: `git -C /home/vgpnk/Projects/plazir-15-site log -3 --format='%H %cI %s'` and `git -C /home/vgpnk/Projects/plazir-15-site remote -v` each returned exit 128 with `fatal: cannot change to '/home/vgpnk/Projects/plazir-15-site': No such file or directory`. No local commit history or remote configuration can be inspected there.
- Historical existence is evidenced in lane records: `corpus/lessons/round-7.md:27–28` / `corpus/knowledge/sitemap-orphan-audit.md:27–28` say both Pages workflows, including `plazir-15-site/.github/workflows/pages.yml`, were read on 2026-09-28; `corpus/knowledge/drift-detection.md:77–83` records a source-side check on 2026-09-29; `SCORECARD.md:85` says the checkout was live at the round-17 close. Round-23 `ReverifyPropertyMapRegistry.md:50` records a public raw-workflow GET with `on` / `push` / `branches: [main]`; `SurfacePlazir15Ghp.md:20–25` records the separate single public page GET as HTTP 200 `text/html`.
- Removal timing: `LOG.md:400–412` records the round-18 census at 2026-10-14, a 36-to-14 `~/Projects` child change, and `plazir-15-site` among removed roots. `corpus/lessons/round-18.md:10–16` narrows this only to sometime after r17 (2026-09-29) and by the r18 census. Later r20 annotations label the prune as 2026-10-12, but I found no primary timestamp for the actual deletion; the exact date is therefore an attribution, not independently established by the primary census.
- The existing c40 annotation is truthful: local checkout/workflow absence is verified; the round-23 public page GET verifies served HTML but cannot by itself prove the active publishing configuration. The separate raw-workflow GET verifies remote repository content and the push trigger, not that the workflow is the active/successful deployment mechanism. No append-only text is proposed (`action: none`).
- The round-open `pathsMissSet` includes `~/Projects/plazir-15-site` at `paths-before.json:1887`, but not T05's file token; the fresh paths-sweep `newMissing` list includes T05.

## Limits

- The exact disappearance timestamp is unknown within the interval after the r17 present observation (~2026-09-29) and by the r18 absent observation (2026-10-14 12:40Z); 2026-10-12 is the later lane's prune attribution.
- No tools were installed. No build, lint, formatter, or broad tests were run. The paths sweep was the one targeted CLI probe used for this C1 target.
- I inadvertently ran `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --short --untracked-files=no` while checking the lane revision; it emitted no status lines (`status_exit=0` from the command pipeline). `git status` may refresh the index cache. I made no deliberate lane production-file or index edits and did not inspect or attempt to undo any possible cache refresh.
