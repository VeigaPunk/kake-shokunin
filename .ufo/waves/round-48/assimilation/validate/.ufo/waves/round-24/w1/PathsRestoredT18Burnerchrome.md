## Verdict

C1 T18 (`~/Projects/ds4cc-marketplace/burnerchrome`, class `recovered`) was observed present at `2026-10-21T11:50:24Z`. The target is a tracked subdirectory of the restored `ds4cc-marketplace` clone, not a standalone repository. All five frozen cites are lane-authored and require append-only restoration corrections; exact proposed text is included in the receipt below. No production citation was edited. This is scout evidence for L1's integration, not an independent admission.

## Findings

- **P2 — T18's older path results are stale as current-state claims.** Exact checks: `test -e ~/Projects/ds4cc-marketplace/burnerchrome && echo EXISTS || echo ABSENT`; `stat -c '%n %w %y' ~/Projects/ds4cc-marketplace/burnerchrome`; `ls -la ~/Projects/ds4cc-marketplace/burnerchrome`; `git -C ~/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'`; `git -C ~/Projects/ds4cc-marketplace remote -v`. Exact outputs: `EXISTS`; `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome 2026-10-21 05:19:05.038621636 -0300 2026-10-21 05:19:05.040003658 -0300`; directory listing contains `README.md`, `adapters/`, `assets/`, `burner.html`, `compare.html`, `delegate.html`, `family.html`, `favicon.svg`, `fonts/`, `index.html`, `install.html`, `marketplace.html`; HEAD log begins `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 ...`, then `95dbeb69b2db413f00f5310a171334967c368924 2026-10-21T05:21:55-03:00 ...`, then `6e888784ae1bac9d341cc9af7fe12f9c5d83f31f 2026-10-20T14:33:09Z ...`; remote is `origin https://github.com/VeigaPunk/ds4cc-marketplace.git` for fetch and push. Impact: C1 freshness, T18. Smallest fix: append the five receipt corrections to their cited lines; preserve the earlier text as historical evidence.
- **P2 — Nearby r18 parent-root notes are also stale as current-state statements, but belong to the distinct parent token/T16.** Exact commands: `stat -c '%n %w %y' ~/Projects/ds4cc-marketplace`; `ls -la ~/Projects/ds4cc-marketplace`. Exact output: `/home/vgpnk/Projects/ds4cc-marketplace 2026-10-21 05:19:01.033916520 -0300 2026-10-21 05:21:03.733544920 -0300`; ancestor listing includes `.git/`, `CNAME`, `burnerchrome/`, `speedrun/`, and `apps-sdk/`. The nearby comments at `SKILL.md:19`, `fleet-registry.md:49-50`, and `fleet-registry.md:64` say the parent `~/Projects/ds4cc-marketplace` was absent; this observation establishes it is now present. Impact: parent-path freshness/T16, not the five T18 cite receipts. Smallest fix: route those parent-token corrections through T16; do not alter these non-T18 lines in this report.
- **P2 — The repository reflog records two pushes; the public-side result and authorization were not independently checked.** Exact command: `cat ~/Projects/ds4cc-marketplace/.git/logs/refs/remotes/origin/main`. Exact output: `6e888784ae1bac9d341cc9af7fe12f9c5d83f31f 95dbeb69b2db413f00f5310a171334967c368924 r20 <r20@example.invalid> 1792571698 -0300\tupdate by push` and `95dbeb69b2db413f00f5310a171334967c368924 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 r20 <r20@example.invalid> 1792572686 -0300\tupdate by push`. Impact: publishing/PQ-2 context, outside T18's local-presence determination; publishing remains operator-owned. Smallest fix: owner reviews these recorded events and independently checks the remote if needed. I did not contact the remote.

## Checked and held

- Parent repo clone event: `.git/logs/HEAD` records `clone: from https://github.com/VeigaPunk/ds4cc-marketplace.git` at `2026-10-21 05:19:05 -0300` (`2026-10-21T08:19:05Z`); T18's directory birth time is `2026-10-21 05:19:05.038621636 -0300`. The actor/cause of the restoration is unknown.
- Current parent-repo HEAD is `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`; remote URL is `https://github.com/VeigaPunk/ds4cc-marketplace.git`. `git -C ~/Projects/ds4cc-marketplace rev-parse HEAD:burnerchrome` returned tree `7f9781cc711e314d6c57676482a6b1e6886bb0ac`. `git -C ~/Projects/ds4cc-marketplace ls-tree -r --name-only HEAD -- burnerchrome | wc -l` and `find ~/Projects/ds4cc-marketplace/burnerchrome -type f | wc -l` each returned `23`; scoped `git --no-optional-locks -C ~/Projects/ds4cc-marketplace status --porcelain --ignored --untracked-files=all -- burnerchrome` returned no output. The latest commit touching the subtree is `27168273c255a95bcf912439674b4c01e2f1271d` (`2026-09-30T02:02:19-03:00`, `plugins: burnerchrome catalog count + xbrd broken doc refs`).
- `od -c ~/Projects/ds4cc-marketplace/CNAME` returned `0000000   d   s   4   c   c   .   c   o   m` and `0000011`; this matches the corpus's cited `ds4cc.com` value. `stat` reports 9 bytes. The cited root entries `.github/workflows/pages.yml`, `CNAME`, `deploy-github-pages.sh`, `speedrun/`, `burnerchrome/`, `render.yaml`, and `apps-sdk/` all passed `test -e`. Under T18, `adapters/` contains four HTML files; `assets/` has `app.js`, `delegate.css`, `delegate.js`, `delegate.test.cjs`, `styles.css`; `fonts/` has five JetBrains Mono WOFF2 files.
- Restored subtree vs corpus/candidate claims: the corpus's old `f3d2ecd` pin is not a valid object name in this clone; `e6bd071887bfaa87eff07ab03d323d5b92760fba` is an ancestor of HEAD, and `0b1116766de2d9895a3673c88678049b4946cf3c` is also an ancestor. Current HEAD is 28 commits after `e6bd071` and matches the local `origin/main` ref (`rev-list --left-right --count origin/main...HEAD` returned `0\t0`). Thus the old local unpushed-commit/sitemap state is not reproduced by this checkout; public remote state was not queried.
- The surviving standalone `~/Projects/burnerchrome` is a separate repository at HEAD `ee834920de8411f8014236948e2d5b9f5f82dde2` (`git -C ~/Projects/burnerchrome log -1 --format='%H %cI %s'` returned `ee834920de8411f8014236948e2d5b9f5f82dde2 2026-08-21T12:29:57-03:00 Point the Musketeer family site at kimi.ai for the Kimi adapter.`); its origin is `https://github.com/VeigaPunk/burnerchrome.git`. The restored-vendored and standalone trees differ under `diff -rq --exclude=.git`; their local `index.html` files both show title `burnerchrome — Musketeer family` and h1 `Four adapters. One permanent burner Chrome.`, but the restored index is 12,029 bytes and the candidate index 11,775 bytes. The local comparison does not establish either file's correspondence to the live page. The r23 candidate-vs-live title/H1 statement, the specific Kimi chat binding, and current live deployment correspondence remain unverified here.
- Current restoration evidence does not change the scope of a row's Kimi status or `queued`/null-URL designation. Presence of the source directory alone verifies no Kimi chat binding, public response, deployment identity, or publishing configuration.
- No tools were installed. No lane production files, source trees, git refs, or remotes were changed by this scout; only this report was written.

## Limits

- The parent source tree was inspected read-only. No web request was made; public-page and live deployment facts remain unverified. No freshness sweep or C1 counter was run, and this report does not claim lane-level admission. Round-24 integration must apply the proposed append-only text and run its assigned checks.
- Parent-root claims noted above are outside the T18 receipt and should be reconciled by the T16 owner. The clone's reflog records `update by push`, but no remote endpoint query was made.

### C1 T18 receipt

```json
{
  "id": "T18",
  "token": "~/Projects/ds4cc-marketplace/burnerchrome",
  "class": "recovered",
  "observedAt": "2026-10-21T11:50:24Z",
  "state": "present",
  "observation": {
    "commands": [
      "test -e ~/Projects/ds4cc-marketplace/burnerchrome && echo EXISTS || echo ABSENT",
      "stat -c '%n %w %y' ~/Projects/ds4cc-marketplace/burnerchrome",
      "ls -la ~/Projects/ds4cc-marketplace/burnerchrome",
      "ls -la ~/Projects/ds4cc-marketplace",
      "git -C ~/Projects/ds4cc-marketplace log -3 --format='%H %cI %s'",
      "git -C ~/Projects/ds4cc-marketplace remote -v",
      "git -C ~/Projects/ds4cc-marketplace reflog -6 --date=iso --format='%H %gd %gs %ci'",
      "git -C ~/Projects/ds4cc-marketplace rev-parse HEAD",
      "git -C ~/Projects/ds4cc-marketplace rev-parse HEAD:burnerchrome",
      "git -C ~/Projects/ds4cc-marketplace ls-tree -r --name-only HEAD -- burnerchrome | wc -l",
      "find ~/Projects/ds4cc-marketplace/burnerchrome -type f | wc -l",
      "od -c ~/Projects/ds4cc-marketplace/CNAME",
      "git --no-optional-locks -C ~/Projects/ds4cc-marketplace status --porcelain --ignored --untracked-files=all -- burnerchrome"
    ],
    "output": "EXISTS; stat target: /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome 2026-10-21 05:19:05.038621636 -0300 2026-10-21 05:19:05.040003658 -0300; ls target: README.md, adapters/, assets/, burner.html, compare.html, delegate.html, family.html, favicon.svg, fonts/, index.html, install.html, marketplace.html; ancestor stat: /home/vgpnk/Projects/ds4cc-marketplace 2026-10-21 05:19:01.033916520 -0300 2026-10-21 05:21:03.733544920 -0300; ancestor ls includes .git/, CNAME, burnerchrome/, speedrun/, apps-sdk/; CNAME od -c: 0000000   d   s   4   c   c   .   c   o   m / 0000011; HEAD 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28; HEAD:burnerchrome tree 7f9781cc711e314d6c57676482a6b1e6886bb0ac; tracked count 23; on-disk regular-file count 23; scoped status output empty. Repo log: 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 2026-10-21T05:51:24-03:00 omarchy-usage: sync page to usage-tray 1.10.0 (14 omp-metered providers, how it works, working install); 95dbeb69b2db413f00f5310a171334967c368924 2026-10-21T05:21:55-03:00 os-tuning: add gkeep (local post-it notes for the Omarchy bar) at /gkeep/; 6e888784ae1bac9d341cc9af7fe12f9c5d83f31f 2026-10-20T14:33:09Z magga: Enduro — Classic & Remastered at /magga/enduro/. Remote: origin https://github.com/VeigaPunk/ds4cc-marketplace.git (fetch); origin https://github.com/VeigaPunk/ds4cc-marketplace.git (push). Parent reflog records clone from that URL at 2026-10-21 05:19:05 -0300. origin/main reflog records two lines ending `update by push` (at 05:34:58 and 05:51:26 -0300)."
  },
  "event": "2026-10-21T08:19:05Z: the parent repository reflog records a clone from https://github.com/VeigaPunk/ds4cc-marketplace.git, and the target directory birth time is 2026-10-21 05:19:05.038621636 -0300. The restoration actor and reason are unknown.",
  "cites": [
    {
      "cite": "SKILL.md:20",
      "lineText": "| burnerchrome kimi | `https://burnerchrome.kimi.page/` | `~/Projects/ds4cc-marketplace/burnerchrome` | Kimi surface, chat `1a0ada42-28e2…` |",
      "authored": "lane",
      "status": "presence-claim-true",
      "action": "append-inline",
      "text": " <!-- r24 restoration 2026-10-21: observed `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` present at 2026-10-21T11:50:24Z (birth 2026-10-21 05:19:05 -0300; repo HEAD `1fbdb8ed`). This confirms the local source path and contents only; the listed Kimi chat binding and live-page correspondence remain unverified. -->"
    },
    {
      "cite": "SKILL.md:423",
      "lineText": "- [property-map:c2] **STALE** — The mapped local source directories for the active plazir front, burnerchrome, and lucario (including lucario/site) are absent; the explicit-path test output is recorded below. The missing ds4cc and charter roots and the plazir dead-slot path are separately annotated as historical/unavailable in the source map. Surface: `test -e /home/vgpnk/Projects/plazir-15-site; test -e /home/vgpnk/Projects/ds4cc-marketplace/burnerchrome; test -e /home/vgpnk/Projects/lucario; test -e /home/vgpnk/Projects/lucario/site`. Correction: As of 2026-10-21, `/home/vgpnk/Projects/plazir-15-site`, `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome`, `/home/vgpnk/Projects/lucario`, and `/home/vgpnk/Projects/lucario/site` are absent, so these mapped local source paths need a verified replacement or an explicit unavailable/history annotation.",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": " *[r24 restoration 2026-10-21: `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` was observed present (birth 2026-10-21 05:19:05 -0300; 23 on-disk files match 23 entries in HEAD tree `7f9781cc`). The parent `/home/vgpnk/Projects/ds4cc-marketplace` was also observed present (birth 2026-10-21 05:19:01 -0300). The earlier burnerchrome and ds4cc-root path results remain historical snapshots; the plazir, charter, and lucario clauses were not re-observed here.]*"
    },
    {
      "cite": "SKILL.md:431",
      "lineText": "- [property-map:c10] **STALE** — The map's listed source directory is present as a current local source path. Surface: `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome`. Correction: As of 2026-10-21, the mapped ds4cc-marketplace/burnerchrome path is absent, but a surviving source candidate is /home/vgpnk/Projects/burnerchrome (VeigaPunk/burnerchrome, commit ee834920de8411f8014236948e2d5b9f5f82dde2); its title and h1 match the live page, not a proved deployment binding.",
      "authored": "lane",
      "status": "annotated-stale",
      "action": "append-inline",
      "text": " *[r24 restoration 2026-10-21: `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` was observed present, with 23 files matching its 23 HEAD-tracked entries (subtree `7f9781cc`; repo HEAD `1fbdb8ed`). The earlier c10 path result and candidate-vs-live title/H1 statement remain historical snapshots; this local check does not verify Kimi chat binding or current live-page correspondence.]*"
    },
    {
      "cite": "corpus/knowledge/fleet-registry.md:51",
      "lineText": "| burnerchrome-kimi | burnerchrome.kimi.page | live | `~/Projects/ds4cc-marketplace/burnerchrome` |",
      "authored": "lane",
      "status": "presence-claim-true",
      "action": "append-inline",
      "text": " <!-- r24 restoration 2026-10-21: observed `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` present (birth 2026-10-21 05:19:05 -0300; parent repo HEAD `1fbdb8ed`). This filesystem observation verifies the local sourceDir only; the row's Kimi status and surface binding remain unverified. -->"
    },
    {
      "cite": "corpus/knowledge/fleet-registry.md:66",
      "lineText": "| burnerchrome-com | null | queued | `~/Projects/ds4cc-marketplace/burnerchrome` |",
      "authored": "lane",
      "status": "presence-claim-true",
      "action": "append-inline",
      "text": " <!-- r24 restoration 2026-10-21: observed `/home/vgpnk/Projects/ds4cc-marketplace/burnerchrome` present (birth 2026-10-21 05:19:05 -0300; parent repo HEAD `1fbdb8ed`). This filesystem observation verifies the local sourceDir only; the queued/null-URL designation and any publication state remain unverified. -->"
    }
  ]
}
```

