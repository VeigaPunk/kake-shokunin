## Verdict

T15 is absent at the observed path as of `2026-10-21T11:52:47Z`. Its sole cite is lane-authored and already directly says the cited run log is absent; that statement is true, so no append to the cite is proposed (`action: none`). The historical log existed: round 16's 28-journal census says `operatorNext` appeared only in `state/rebuild-charter-fire.log`. Lane history dates the removal event to the 2026-10-12 W7 `~/Projects` prune/migration, with the tree's removal recorded in round 18 on 2026-10-14; the precise deletion time is not recorded. T15 was never included in `pins.pathsMissSet`, so this target remains a C1 freshness pin debt for integration.

## Findings

### P1 — T15 is an observed miss not represented in `pathsMissSet`

- **Exact command:** `node -e 'const p=require("/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/freshness-pins.json").pins.pathsMissSet; console.log(JSON.stringify({tokenPinned:p.includes("~/Projects/webzites/state/rebuild-charter-fire.log"), related:p.filter(x=>x.startsWith("~/Projects/webzites"))}, null, 2))'`
- **Exact observed output:** `"tokenPinned": false`; the related entries include `"~/Projects/webzites"`, `"~/Projects/webzites/state"`, and `"~/Projects/webzites/state/probe-history.jsonl"`, but not the rebuild log. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -S'rebuild-charter-fire' --all --format='%h %cI %s' -- corpus/knowledge/freshness-pins.json` produced no output.
- **Impact:** C1 / freshness. T15 is class `newMissing` in the frozen population and its current miss must be absorbed into `pins.pathsMissSet` for the round's pin equality condition.
- **Smallest fix:** Integrate the T15 receipt below and add exactly `~/Projects/webzites/state/rebuild-charter-fire.log` to `pins.pathsMissSet`; no corpus cite edit is needed.

## Checked and held

- **Current observation:** The exact read-only existence command returned `token=absent`, `state_dir=absent`, and `webzites_dir=absent`. `stat -c '%n %w %y'` failed with “No such file or directory” for all three absent paths; the nearest existing ancestor, `/home/vgpnk/Projects`, reported birth `2026-10-03 17:48:28.004231881 -0300` and mtime `2026-10-21 05:19:01.033916520 -0300`. `ls -la /home/vgpnk/Projects` listed 24 directory entries and no `webzites` entry.
- **Git availability:** The requested `git -C /home/vgpnk/Projects/webzites log -3 --format='%H %cI %s'` and `git -C /home/vgpnk/Projects/webzites remote -v` both failed with `fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory`. The lane-local `git log --all --format=%h -- state/rebuild-charter-fire.log` produced no output; the log is not tracked at that lane-relative path.
- **Historical existence:** Lane history for `corpus/knowledge/fire-journal-codes.md` includes round 4 (`6b1cd07`, 2026-09-28T16:07:52-03:00) and round 16 (`ab87a48`, 2026-09-28T23:44:18-03:00). The r16 census text states “over all 28 journals” and that `operatorNext` appears “only in `state/rebuild-charter-fire.log`” (`fire-journal-codes.md:12-18`), corroborating that the log had existed and been read by then.
- **Vanishing event:** `LOG.md:400-417` dates the W7 mega-prune to 2026-10-12 and reports in the 2026-10-14 round-18 entry that 33 of 36 `~/Projects` children were removed, including `webzites`. This accounts for the log's disappearance under that tree. Round-23's `fire-journal-codes.json` c5 receipt (observed 2026-10-21) records the exact log path as absent and the historical result as `UNVERIFIABLE`.
- **Cite classification:** The only population cite, `corpus/knowledge/fire-journal-codes.md:86`, is lane-authored. Its current line directly says “The cited run log is absent” and qualifies the rebuild facts as `UNVERIFIABLE`; current checks confirm the absence. It is `annotated-true`, with action `none` and empty append text. No rewrite or extra annotation is proposed.
- **T15 receipt:**

```json
{
  "id": "T15",
  "token": "~/Projects/webzites/state/rebuild-charter-fire.log",
  "class": "newMissing",
  "observedAt": "2026-10-21T11:52:47Z",
  "state": "absent",
  "observation": {
    "commands": [
      "date -u +%Y-%m-%dT%H:%M:%SZ; test -e /home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log && echo token=present || echo token=absent; test -e /home/vgpnk/Projects/webzites/state && echo state_dir=present || echo state_dir=absent; test -e /home/vgpnk/Projects/webzites && echo webzites_dir=present || echo webzites_dir=absent",
      "stat -c '%n %w %y' /home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log /home/vgpnk/Projects/webzites/state /home/vgpnk/Projects/webzites /home/vgpnk/Projects",
      "ls -la /home/vgpnk/Projects",
      "git -C /home/vgpnk/Projects/webzites log -3 --format='%H %cI %s'; echo \"exit=$?\"; git -C /home/vgpnk/Projects/webzites remote -v; echo \"exit=$?\"",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -S'rebuild-charter-fire.log' --format='%h %cI %s' -- corpus/knowledge/fire-journal-codes.md",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --all --format=%h -- state/rebuild-charter-fire.log",
      "git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -S'rebuild-charter-fire' --all --format='%h %cI %s' -- corpus/knowledge/freshness-pins.json"
    ],
    "output": "2026-10-21T11:52:47Z; token=absent; state_dir=absent; webzites_dir=absent. stat: No such file or directory for the log, state directory, and webzites directory; /home/vgpnk/Projects: birth 2026-10-03 17:48:28.004231881 -0300, mtime 2026-10-21 05:19:01.033916520 -0300. ls: 24 directories, no webzites entry. webzites log and remote: fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory (exit 128 each). Lane cite history: 6b1cd07 2026-09-28T16:07:52-03:00 round-4; ab87a48 2026-09-28T23:44:18-03:00 round-16; df6196b 2026-10-20T06:08:53-03:00 round-21; 83098b5 2026-10-21T04:26:49-03:00 round-23. Lane-local state path history: no output. Pin token history: no output."
  },
  "event": "2026-10-12 W7 ~/Projects prune/migration: the lane's 2026-10-14 round-18 LOG.md entry (lines 400-417) says 33 of 36 children were removed, including webzites; this explains the now-absent log under that tree. The precise deletion time is not recorded.",
  "cites": [
    {
      "cite": "corpus/knowledge/fire-journal-codes.md:86",
      "lineText": "- [fire-journal-codes:c5] **UNVERIFIABLE** — The historical charter rebuild created version efc1830, had a marker-present 200 preview, and ended with stillDead true. Surface: `/home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log`. Unverifiable: The cited run log is absent, and the local artifacts needed to re-establish the historical preview result are unavailable.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    }
  ]
}
```

## Limits

The domain repository is absent, so its commit history and remotes could not be read. A recursive home search timed out after 300 seconds; this report does not claim to rule out an archive outside `~/Projects`. The exact prune/deletion time for this individual file is not established beyond the lane's dated 2026-10-12 W7 event and subsequent absence observations. No tools were installed or updated; no builds, tests, or formatters were run.