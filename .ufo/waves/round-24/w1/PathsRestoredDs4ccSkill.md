## Verdict

T16 (`~/Projects/ds4cc-marketplace`, class `recovered`) was present at observation time. Its seven lane-authored `SKILL.md` cites each need an appended restoration correction. The r18 local-state notes and the property-map HOLD/UNVERIFIABLE conclusions that rely on the earlier checkout state are historical; the live Kimi, Pages, and Render facts listed below remain unverified.

## Findings

- **P2 — C1 freshness; T16 current filesystem state.** Exact commands: `test -e /home/vgpnk/Projects/ds4cc-marketplace; echo "test -e exit=$?"`; `stat -c '%n %w %y' /home/vgpnk/Projects/ds4cc-marketplace`; `ls -la /home/vgpnk/Projects`; `git -C /home/vgpnk/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'`; `git -C /home/vgpnk/Projects/ds4cc-marketplace remote -v`. Exact observed output: `test -e exit=0`; `/home/vgpnk/Projects/ds4cc-marketplace 2026-10-21 05:19:01.033916520 -0300 2026-10-21 05:21:03.733544920 -0300`; the parent listing included `drwxr-xr-x 1 vgpnk vgpnk 902 Oct 21 05:21 ds4cc-marketplace/` and ended `0 files, 24 dirs`; log began `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 (14 omp-metered providers, how it works, working install)`, followed by `95dbeb69b2db413f00f5310a171334967c368924 2026-10-21T05:21:55-03:00 os-tuning: add gkeep (local post-it notes for the Omarchy bar) at /gkeep/` and `6e888784ae1bac9d341cc9af7fe12f9c5d83f31f 2026-10-20T14:33:09Z magga: Enduro — Classic & Remastered at /magga/enduro/`; remotes were `origin https://github.com/VeigaPunk/ds4cc-marketplace.git (fetch)` and `origin https://github.com/VeigaPunk/ds4cc-marketplace.git (push)`. The reflog records `6e88878 HEAD@{2026-10-21 05:19:05 -0300}: clone: from https://github.com/VeigaPunk/ds4cc-marketplace.git`. Impacted claim/axis: T16 / freshness. Smallest fix: append the dated restoration notes in the receipt below; do not rewrite old observations.

- **P2 — C1 freshness; cited tree properties.** Exact observed commands: `git -C /home/vgpnk/Projects/ds4cc-marketplace show HEAD:CNAME`; `git -C /home/vgpnk/Projects/ds4cc-marketplace for-each-ref '--format=%(refname)%09%(objectname)%09%(committerdate:iso-strict)'`; `git -C /home/vgpnk/Projects/ds4cc-marketplace rev-list --count origin/main..HEAD`; `git -C /home/vgpnk/Projects/ds4cc-marketplace rev-list --count HEAD..origin/main`. Exact outputs: `ds4cc.com`; `refs/heads/main`, `refs/remotes/origin/HEAD`, and `refs/remotes/origin/main` each point to `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`; both commit counts were `0`. The target directory listing showed `.github/`, `apps-sdk/`, `burnerchrome/`, `speedrun/`, `CNAME`, `deploy-github-pages.sh`, and `render.yaml`. `render.yaml` contains `dockerfilePath: ./apps-sdk/Dockerfile` and `APP_ORIGIN=https://app.ds4cc.com`; `apps-sdk/Dockerfile` was present in the read-only HEAD/worktree inventory. The local `.github/workflows/pages.yml` says `on: push: branches: [main]`; the setup script says it prints that Pages deploys via this workflow. Impacted claim/axis: presence-dependent claims at T16 cites / freshness. Smallest fix: append restoration notes distinguishing local source evidence from live publishing and service state.

- **P2 — C1 freshness; previous HEAD/content references are not all current-state proof.** The current full HEAD `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` matches the round-open record's `1fbdb8ed`; the local origin/main reflog says it was updated by push at `2026-10-21 05:51:26 -0300`. The older `e6bd071887bfaa87eff07ab03d323d5b92760fba` pin is an ancestor of current HEAD (`git merge-base --is-ancestor ... HEAD` exited `0`), not current HEAD. The local `CNAME` and `git show HEAD:CNAME` both read `ds4cc.com`. The old corpus row's truncated `live index sha b6f65899…` was not verifiable from this checkout: the current Git blob for `index.html` is `587288b86c91d6fddc60bea0ffa8e56ad468bc8c`, its SHA-256 is `d0a2f357b19832e8ec8b0cbf80fa045734eff8a63d28e040434b9dcb5790f1d9`, and `git cat-file -t b6f65899` returned `fatal: Not a valid object name b6f65899`. The row supplies only a truncated digest and no algorithm; I did not fetch the live page. Impacted claim/axis: T16 restoration comparison / freshness. Smallest fix: retain the old digest as historical and remeasure it only with the live bytes and digest method in scope.

- **P2 — C1 freshness; exact cite treatment.** `SKILL.md:16`, `:19`, and `:364` each contain an r18 local-state annotation made stale by the restored directory; classify `annotated-stale`. `SKILL.md:445`, `:448`, `:449`, and `:450` assert or depend on the checkout's prior local state; classify `presence-claim-stale`. All seven cites are authored in the lane, so `action` is `append-inline`. Smallest fix: append the exact texts below at each cited line's end.

## Checked and held

- Read the frozen contract, T16 population entry, round-open paths evidence, and each assigned `SKILL.md` cite with surrounding context. T16 is `recovered`; its assigned cites are precisely `SKILL.md:16,19,364,445,448,449,450`.
- Observed the dated clone event in the target's local reflog; the cause/actor beyond that logged operation is unknown. The repo's current `HEAD`, local main, and local `origin/main` are `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`. A read-only worktree/blob comparison reported `HEAD tracked blob entries: 2630`, `worktree files matching HEAD blob: 2630`, `HEAD blobs missing from worktree: 0`, `content mismatches vs HEAD: 0`, and six untracked `__pycache__` files.
- Local `CNAME` matches the corpus value `ds4cc.com`; the cited workflow, `speedrun/`, `burnerchrome/`, `render.yaml`, `apps-sdk/`, and `apps-sdk/Dockerfile` are present. The local workflow config supports the source-level claim that the workflow triggers on push to `main`.
- Presence-dependent claims that remain unverified: whether the named Kimi chat is bound to the mirror and its current vintage; the live GitHub Pages custom-domain setting, actual deployment, and currently served index bytes; and the live Render service state. Local config establishes only the present checkout's declarations. Local remote-tracking refs/reflog do not independently establish present GitHub remote state.
- No tools were installed or updated.

```json
{
  "id": "T16",
  "token": "~/Projects/ds4cc-marketplace",
  "class": "recovered",
  "observedAt": "2026-10-21T11:50:42Z",
  "state": "present",
  "observation": {
    "commands": [
      "test -e /home/vgpnk/Projects/ds4cc-marketplace; echo \"test -e exit=$?\"",
      "stat -c '%n %w %y' /home/vgpnk/Projects/ds4cc-marketplace",
      "ls -la /home/vgpnk/Projects",
      "ls -la /home/vgpnk/Projects/ds4cc-marketplace",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace remote -v",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace reflog show --date=iso -n 12",
      "git -C /home/vgpnk/Projects/ds4cc-marketplace show HEAD:CNAME"
    ],
    "output": "test -e exit=0\n/home/vgpnk/Projects/ds4cc-marketplace 2026-10-21 05:19:01.033916520 -0300 2026-10-21 05:21:03.733544920 -0300\nls -la /home/vgpnk/Projects: ...\ndrwxr-xr-x 1 vgpnk vgpnk 902 Oct 21 05:21 ds4cc-marketplace/\n...\n0 files, 24 dirs\nls -la /home/vgpnk/Projects/ds4cc-marketplace: total 268; entries include .github/, apps-sdk/, burnerchrome/, speedrun/, CNAME (9B), deploy-github-pages.sh, render.yaml; 23 files, 21 dirs\n1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 (14 omp-metered providers, how it works, working install)\n95dbeb69b2db413f00f5310a171334967c368924 2026-10-21T05:21:55-03:00 os-tuning: add gkeep (local post-it notes for the Omarchy bar) at /gkeep/\n6e888784ae1bac9d341cc9af7fe12f9c5d83f31f 2026-10-20T14:33:09Z magga: Enduro — Classic & Remastered at /magga/enduro/\norigin\thttps://github.com/VeigaPunk/ds4cc-marketplace.git (fetch)\norigin\thttps://github.com/VeigaPunk/ds4cc-marketplace.git (push)\n6e88878 HEAD@{2026-10-21 05:19:05 -0300}: clone: from https://github.com/VeigaPunk/ds4cc-marketplace.git\nds4cc.com"
  },
  "event": "2026-10-21 05:19:05 -0300 clone entry for https://github.com/VeigaPunk/ds4cc-marketplace.git observed in the target .git reflog; the initiating actor and broader restoration cause are unknown.",
  "cites": [
    {
      "cite": "SKILL.md:16",
      "lineText": "| ds4cc.com (primary) | `https://ds4cc.com/` | `~/Projects/ds4cc-marketplace` | GH Actions on push to `main` (`CNAME` = ds4cc.com) **[r20-correction 2026-10-19: a repo CNAME sets the domain only for branch publishing; under Actions it is ignored and the domain is a Pages setting (`cname` in the REST API) — S005, S003, S007]** | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: The local checkout was cloned at 2026-10-21 05:19:05 -0300 from https://github.com/VeigaPunk/ds4cc-marketplace.git (reflog); its CNAME contains ds4cc.com and .github/workflows/pages.yml specifies push to main. The r18 local-state annotation is historical; the current GitHub Pages domain setting and live deployment remain unverified. -->"
    },
    {
      "cite": "SKILL.md:19",
      "lineText": "| ds4cc kimi mirror | `https://ds4cc.kimi.page/` | `~/Projects/ds4cc-marketplace` | Kimi surface, chat `1a073c43-bf42-874a-8000-0907bd80b9dc` — STALE (~Aug-29 vintage) | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: The local checkout was cloned at 2026-10-21 05:19:05 -0300 from https://github.com/VeigaPunk/ds4cc-marketplace.git (reflog); the referenced local tree is present. The r18 local-state annotation is historical; the listed Kimi chat binding and ~Aug-29 vintage remain unverified from this filesystem observation. -->"
    },
    {
      "cite": "SKILL.md:364",
      "lineText": "- `~/Projects/ds4cc-marketplace/` — ds4cc.com source: `.github/workflows/ <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": "<!-- r24 restoration 2026-10-21: The local checkout and referenced .github/workflows/pages.yml, CNAME, deploy-github-pages.sh, speedrun/, burnerchrome/, render.yaml, apps-sdk/, and apps-sdk/Dockerfile are present. The r18 local-state annotation is historical; live Render service state and deployed content remain unverified. -->"
    },
    {
      "cite": "SKILL.md:445",
      "lineText": "- [property-map:c24] **HOLD** — The map's annotation that the listed source directory is absent remains true locally. Surface: `/home/vgpnk/Projects/ds4cc-marketplace`.",
      "authored": "lane",
      "status": "presence-claim-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: The mapped source checkout is present; its birth time is 2026-10-21 05:19:01 -0300 and HEAD is 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28. The earlier HOLD describes the prior local observation and remains historical; live site state is unverified.]*"
    },
    {
      "cite": "SKILL.md:448",
      "lineText": "- [property-map:c27] **HOLD** — The property map explicitly preserves the mapped source path as historical after its removal; the corresponding local path is still absent. Surface: `/home/vgpnk/Projects/ds4cc-marketplace`.",
      "authored": "lane",
      "status": "presence-claim-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: The mapped source checkout is present; its birth time is 2026-10-21 05:19:01 -0300 and HEAD is 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28. The earlier HOLD records the map's historical treatment and prior local observation; current publication state is unverified.]*"
    },
    {
      "cite": "SKILL.md:449",
      "lineText": "- [property-map:c28] **UNVERIFIABLE** — The map's stated GH Actions-on-main publishing mechanism could not be reverified against current source configuration. Surface: `/home/vgpnk/Projects/ds4cc-marketplace`. Unverifiable: The mapped checkout is absent, and the checked public homepage does not disclose the current deployment workflow; no current repository/workflow URL is present in this property-map row to decide this from the assigned surface.",
      "authored": "lane",
      "status": "presence-claim-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: The local checkout is present and .github/workflows/pages.yml specifies push to main, verifying the checked-in workflow configuration. The earlier checkout-based UNVERIFIABLE conclusion is historical; live GitHub Pages configuration and deployment remain unverified.]*"
    },
    {
      "cite": "SKILL.md:450",
      "lineText": "- [property-map:c29] **UNVERIFIABLE** — The map's Actions-versus-branch-publishing custom-domain distinction remains documented but was not independently reverified against current GitHub Pages configuration. Surface: `/home/vgpnk/Projects/ds4cc-marketplace`. Unverifiable: The mapped checkout is absent, and the checked public homepage cannot reveal whether current Pages settings still match this historical configuration note.",
      "authored": "lane",
      "status": "presence-claim-stale",
      "action": "append-inline",
      "text": "*[r24 restoration 2026-10-21: The local checkout is present and its workflow uses configure-pages, upload-pages-artifact, and deploy-pages. The earlier checkout-based rationale is historical; the current GitHub Pages custom-domain setting remains unverified from this filesystem observation.]*"
    }
  ]
}
```

## Limits

This is a read-only freshness observation. I did not contact GitHub, ds4cc.com, Kimi, or Render, and local remote-tracking references do not establish live remote state. In particular, this observation cannot establish the current Kimi chat binding/vintage, GitHub Pages domain setting or deployment, live served index digest, or Render health. No tool was installed or updated.