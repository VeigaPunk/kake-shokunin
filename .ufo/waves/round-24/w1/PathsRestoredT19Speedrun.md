## Verdict

T19 `~/Projects/ds4cc-marketplace/speedrun` is **present** at the 2026-10-21T11:50:29Z observation. The best-supported reappearance event is a fresh clone of `https://github.com/VeigaPunk/ds4cc-marketplace.git` recorded by the repository reflog at 2026-10-21T05:19:05-03:00, matching the directory birth time. This is a C1 freshness receipt only; no lane corpus file was edited.

### C1 target receipt

```json
{
  "id": "T19",
  "token": "~/Projects/ds4cc-marketplace/speedrun",
  "class": "recovered",
  "observedAt": "2026-10-21T11:50:29Z",
  "state": "present",
  "observation": {
    "commands": [
      "date -u +%Y-%m-%dT%H:%M:%SZ",
      "test -e ~/Projects/ds4cc-marketplace/speedrun && echo 'present ~/Projects/ds4cc-marketplace/speedrun' || echo 'absent ~/Projects/ds4cc-marketplace/speedrun'",
      "stat -c '%n %w %y' ~/Projects/ds4cc-marketplace/speedrun",
      "ls -la ~/Projects/ds4cc-marketplace",
      "git -C ~/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'",
      "git -C ~/Projects/ds4cc-marketplace remote -v",
      "git -C ~/Projects/ds4cc-marketplace reflog -8 --date=iso-strict"
    ],
    "output": "2026-10-21T11:50:29Z; present ~/Projects/ds4cc-marketplace/speedrun; stat: /home/vgpnk/Projects/ds4cc-marketplace/speedrun 2026-10-21 05:19:05.120101209 -0300 2026-10-21 05:19:05.121140881 -0300; ls -la parent includes drwxr-xr-x ... 112 ... speedrun; log -3: 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 (14 omp-metered providers, how it works, working install; 95dbeb69b2db413f00f5310a171334967c368924 2026-10-21T05:21:55-03:00 os-tuning: add gkeep (local post-it notes for the Omarchy bar); 6e888784ac1bac9d341cc9af7fe12f9c5d83f31f 2026-10-20T14:33:09Z magga: Enduro — Classic & Remastered (7 games); remote: origin https://github.com/VeigaPunk/ds4cc-marketplace.git (fetch), same (push); reflog includes 6e88878 HEAD@{2026-10-21T05:19:05-03:00}: clone: from https://github.com/VeigaPunk/ds4cc-marketplace.git."
  },
  "event": "2026-10-21T05:19:05-03:00: the ds4cc-marketplace reflog records a clone from https://github.com/VeigaPunk/ds4cc-marketplace.git at the same timestamp as the speedrun directory birth (05:19:05.120101209 -0300). This supports a fresh clone as the reappearance event; it does not establish byte continuity with the pre-prune checkout.",
  "cites": [
    {
      "cite": "corpus/knowledge/mirror-pitfalls.md:63",
      "lineText": "- [mirror-pitfalls:c4] **STALE** — The frozen three-run copy and its canonical repository path are present locally, with a rel=canonical link from the copy. Surface: `test -e /home/vgpnk/Projects/plazir-15-site/speedrun; test -e /home/vgpnk/Projects/ds4cc-marketplace/speedrun`. Correction: As of 2026-10-21, neither /home/vgpnk/Projects/plazir-15-site/speedrun nor /home/vgpnk/Projects/ds4cc-marketplace/speedrun exists under /home/vgpnk/Projects, so this workstation cannot substantiate the asserted copy or canonical link.",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace/speedrun is present; its top-level children are README.md, assets/, data/, docs/, index.html, main.js, scripts/, and style.css. The r23 receipt was committed at 2026-10-21T07:26:49Z (its observedAt is date-only), before the 08:19:05-03:00 clone. This check does not verify the Plazir copy or its rel=canonical link, so the combined three-run-copy claim remains unverified.]*"
    },
    {
      "cite": "corpus/knowledge/speedrun-pipeline.md:1",
      "lineText": "source: operator-local webzites evidence cited in-entry — `~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md`, `~/Projects/webzites/src/speedrun.mjs`, `agents/webzites-speedrun.md`, `reports/keepers/speedrun-r1.md` (webzites-relative), `~/Projects/ds4cc-marketplace/speedrun/`; in-entry r18 absence flags (re-census 2026-10-14) cover SPEEDRUN-PROTOCOL.md, speedrun.mjs and ds4cc-marketplace/speedrun, while the keeper card and speedrun-r1 carry no absence flag; S001, S002, S004 (corpus/SOURCES.md) for the round-20 upload-artifact correction",
      "authored": "lane",
      "status": "annotated-true",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: ~/Projects/ds4cc-marketplace/speedrun/ is present at the 2026-10-21T11:50:29Z observation (birth 2026-10-21T08:19:05-03:00); the r18 census description remains a dated historical record. This observation verifies only the ds4cc path, not the referenced webzites protocol, implementation, keeper card, or keeper report.]*"
    },
    {
      "cite": "corpus/knowledge/speedrun-pipeline.md:13",
      "lineText": "`~/Projects/ds4cc-marketplace/speedrun/` ONLY; `plazir-15-site/speedrun/` <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace/speedrun absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: ~/Projects/ds4cc-marketplace/speedrun/ is present at this observation; its index.html declares https://ds4cc.com/speedrun/ canonical. The r18 2026-10-14 census remains historical, and this presence check does not establish exclusive authority or verify the Plazir copy's canonical relationship.]*"
    },
    {
      "cite": "corpus/knowledge/speedrun-pipeline.md:3",
      "lineText": "recheck: on speedrun lane or webzites/ds4cc-marketplace source change — `for p in ~/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md ~/Projects/webzites/src/speedrun.mjs ~/Projects/ds4cc-marketplace/speedrun; do test -e \"$p\" && echo \"present $p\" || echo \"absent $p\"; done`; paths absent since the 2026-10-12 prune: operator must restore the source tree or retire this entry",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: ~/Projects/ds4cc-marketplace/speedrun is present (birth 2026-10-21T05:19:05-03:00); the ds4cc clone reflog records a same-time clone from origin. The 2026-10-12 prune statement is now historical for this path; the two webzites paths are not reassessed by this correction.]*"
    },
    {
      "cite": "corpus/knowledge/speedrun-pipeline.md:78",
      "lineText": "- [speedrun-pipeline:c3] **HOLD** — The historically designated local authority path remains absent. Surface: `/home/vgpnk/Projects/ds4cc-marketplace/speedrun`.",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: /home/vgpnk/Projects/ds4cc-marketplace/speedrun is present in the 2026-10-21T11:50:29Z check; the directory birth and clone reflog coincide at 2026-10-21T05:19:05-03:00. This is a current presence observation only; exclusive authority and byte continuity with the earlier pre-prune tree remain unverified.]*"
    }
  ]
}
```

## Findings

### P2 — Current state supersedes ds4cc absence assertions in four cited lines

- **Exact command:** `test -e ~/Projects/ds4cc-marketplace/speedrun && echo 'present ~/Projects/ds4cc-marketplace/speedrun' || echo 'absent ~/Projects/ds4cc-marketplace/speedrun'`
- **Exact observed output:** `present ~/Projects/ds4cc-marketplace/speedrun`
- **Exact command:** `stat -c '%n %w %y' ~/Projects/ds4cc-marketplace/speedrun`
- **Exact observed output:** `/home/vgpnk/Projects/ds4cc-marketplace/speedrun 2026-10-21 05:19:05.120101209 -0300 2026-10-21 05:19:05.121140881 -0300`
- **Impacted claim/axis:** C1 freshness. `mirror-pitfalls.md:63`'s round-23 correction and `speedrun-pipeline.md:3,13,78`'s old prune/r18/r23 state do not describe current ds4cc path presence. The round-23 receipt commit is `83098b5a59b180946a34103a439531a35276d1d5`, committed at `2026-10-21T04:26:49-03:00` (07:26:49Z), before the clone at 08:19:05Z. `speedrun-pipeline.md:1` remains an accurate description that the r18 census flags occur in the file, but still needs a restoration correction because T19 is recovered.
- **Smallest fix:** Append the five exact line-specific texts in the receipt; retain every earlier observation unchanged. All five files are lane-authored, so the action is `append-inline`.

### P2 — Reappearance is a fresh clone; content continuity with the earlier local checkout is unproven

- **Exact command:** `git -C ~/Projects/ds4cc-marketplace reflog -8 --date=iso-strict`
- **Exact observed output:** `6e888784 HEAD@{2026-10-21T05:19:05-03:00}: clone: from https://github.com/VeigaPunk/ds4cc-marketplace.git`
- **Exact command:** `git -C ~/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'`
- **Exact observed output:** top commit `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` at `2026-10-21T05:51:24-03:00`; prior entries `95dbeb69b2db413f00f5310a171334967c368924` and `6e888784ac1bac9d341cc9af7fe12f9c5d83f31f`.
- **Impacted claim/axis:** C1 freshness. The restored directory is backed by a repository clone, but the corpus's earlier local HEAD/pin facts are not automatically facts about this clone. The current `origin/main` and local `main` refs were both `1fbdb8ed`; the pinned `e6bd071887bfaa87eff07ab03d323d5b92760fba` is an ancestor 28 commits behind current HEAD. `f3d2ecd`, `e82a262`, and `0de5eb9` were not valid objects in this clone when checked. Thus current content does not prove byte continuity with the previous local tree or retain the prior unpushed commit identities.
- **Smallest fix:** In each restoration note distinguish current path/content evidence from historical checkout identity; do not claim pre-prune byte continuity or transfer the old HEAD/unpushed count to this clone.

### P3 — Local publishing inputs match several citations, but deployment and the mirror claim remain unverified

- **Exact command:** `cat -A ~/Projects/ds4cc-marketplace/CNAME`
- **Exact observed output:** `ds4cc.com` (the file is 9 bytes).
- **Exact command:** `cd ~/Projects/ds4cc-marketplace && grep -n -E "path:|speedrun|exclude|include|upload" .github/workflows/pages.yml 2>&1 | head -30`
- **Exact observed output:** `64: uses: actions/upload-pages-artifact@v3` and `66: path: ./ds4cc-marketplace`.
- **Impacted claim/axis:** C1 freshness / publishing. The checkout's CNAME and workflow text are consistent with the cited domain and static-tree publication story, but neither proves the currently deployed artifact or the combined three-run Plazir-copy/canonical-link claim.
- **Smallest fix:** Keep the receipt's correction scoped to the observed ds4cc source tree; leave live-serving, successful deployment, and the Plazir copy relationship explicitly unverified.

## Checked and held

- **Cited contexts:** Read `mirror-pitfalls.md:60-66` and `speedrun-pipeline.md:1-6,10-16,75-81`; these include ±3 lines around each cite. T19's population entry lists exactly these five citations and labels the target `recovered`.
- **Classifications:** `speedrun-pipeline.md:1` is `annotated-true`: it describes the existence of dated r18 census flags, not a present-day filesystem result. The other four are `annotated-stale` for the ds4cc portion because they contain prior absence/current-state claims contradicted by today's presence. For `mirror-pitfalls.md:63`, the ds4cc half of the r23 correction is stale; the Plazir path was also tested and returned `absent`, so the combined copy/link claim is not established by T19.
- **Restored tree:** `ls -la` showed top-level `README.md`, `assets/`, `data/`, `docs/`, `index.html`, `main.js`, `scripts/`, and `style.css`; `assets/` contains `fonts/`, `data/` contains `artifacts/` and `manifest.json`, and `scripts/` contains two poller `.mjs` files plus the latency probe. The repo's tracked `speedrun/` tree includes these files.
- **CNAME/canonical:** CNAME content is `ds4cc.com` (9 bytes). `speedrun/index.html` contains `rel="canonical"` and `og:url` for `https://ds4cc.com/speedrun/`.
- **Local data structure:** The manifest has nine string-valued `runs[]` paths, each resolves to a file; all nine `run-*.json` files are listed. Their shared top-level-key intersection is 18; `budget_usd` is null in 4/9. These local results match those corpus counts but do not verify the served response bytes.
- **Other current code-level observations:** `main.js` uses `fetch(path, { cache: "no-store" })`; this client source does not establish that no separate upload endpoint exists. Both local poller scripts declare `INTERVAL_MS = 5 * 60 * 1000`; the actual scheduler/association to the cited board poller remains unverified. Current `origin/main` matched local `main` at `1fbdb8ed` in the observed refs.
- **No lane production files, index, or jj state were changed; no tools were installed.**

## Limits

- No live website requests were made. The public site's served files, current Pages deployment, byte equality with the local tree, and public API behavior remain unverified.
- The check of `~/Projects/plazir-15-site/speedrun` returned `absent`; this target report does not adjudicate its copy contents or link semantics. The keeper-card and keeper-report files were not checked here. The `webzites` protocol and implementation paths returned `absent` in the separate 11:46:59Z loop, but their current content/behavior is outside T19.
- The reflog supports a fresh clone event and the directory birth time corroborates it; it cannot establish where the earlier checkout's unpushed commits went or that the current clone's bytes match that checkout.
- **Report:** `.ufo/waves/round-24/w1/PathsRestoredT19Speedrun.md`
