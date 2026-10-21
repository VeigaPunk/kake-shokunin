## Verdict

T14 `~/Projects/webzites/state/probe-latest.json` was observed absent at `2026-10-21T11:52:48Z`. It is already cited with a truthful, direct absence annotation; leave `corpus/knowledge/ops-automation.md:141` unchanged (`action: none`). The lane's history establishes that the snapshot existed and was read by round-15 (2026-09-29) and that the webzites state tree was still present at round-17 (2026-09-29T03:2xZ). The first round-18 absence census was 2026-10-14T12:40Z. Thus disappearance is bounded after the round-17 observation and by the round-18 census; the lane attributes it to a 2026-10-12 W7 prune/migration, but I did not independently establish that precise day or mechanism. The T14 token is absent from the current `pins.pathsMissSet`, so it is a C1 new miss despite the annotated cite.

## Findings

- **P2 — C1 / freshness: observed absent path is an unpinned new miss.** Exact observation command and output:

  ```text
  date -u +%Y-%m-%dT%H:%M:%SZ
  2026-10-21T11:52:48Z
  test -e /home/vgpnk/Projects/webzites/state/probe-latest.json && echo EXISTS || echo ABSENT
  ABSENT
  stat -c '%n %w %y' /home/vgpnk/Projects
  /home/vgpnk/Projects 2026-10-03 17:48:28.004231881 -0300 2026-10-21 05:19:01.033916520 -0300
  ls -la /home/vgpnk/Projects/webzites
  ls: cannot access '/home/vgpnk/Projects/webzites': No such file or directory
  git -C /home/vgpnk/Projects/webzites log -3 --format='%H %cI %s'
  fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory (exit 128)
  git -C /home/vgpnk/Projects/webzites remote -v
  fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory (exit 128)
  command -v webzites
  NOT_FOUND_webzites
  ls -la /home/vgpnk/Projects
  total 0; listing contains `ds4cc-marketplace` (Oct 21 05:21) and other project directories, but no `webzites` entry.
  ```

  Claim/axis: C1, freshness. The current read-only replay command was `cd /home/vgpnk/Projects/shokunin/kake-shokunin && timeout 120 node scripts/freshness-sweep.mjs --section=paths --json --offline`; it exited 1. The captured T14-specific output was:

  ```text
  "counts": {"resolve":19,"declaredAbsent":60,"declaredAbsentIndirect":4,"drift":3,"unresolved":10,"newDrift":0,"newMissing":12}
  "t14_declaredAbsent": [{"path":"~/Projects/webzites/state/probe-latest.json","cites":["corpus/knowledge/ops-automation.md:141"],"evidence":{"word":"absent","line":141,"direct":true,"mentions":true,"cite":"corpus/knowledge/ops-automation.md:141"},"indirect":false}]
  "t14_drift": []
  "t14_newMissing": ["~/Projects/webzites/state/probe-latest.json"]
  "pinned": true
  ```

  Independently checked the current pin object with `node -e 'const p=require("./corpus/knowledge/freshness-pins.json").pins; console.log(JSON.stringify({pathsMissSetIncludesProbeLatest:p.pathsMissSet.includes("~/Projects/webzites/state/probe-latest.json"),pathsMissSetTail:p.pathsMissSet.slice(-12)},null,2))'`; output: `pathsMissSetIncludesProbeLatest: false`. The full tail ends with `~/Projects/webzites/state/probe-history.jsonl`, then `~/projects`, and has no `probe-latest.json`. The same token count was zero in `git show 72eb112:corpus/knowledge/freshness-pins.json` and `git show b0feb30:corpus/knowledge/freshness-pins.json`. Smallest fix: L1 records this round's observed missing token in `pins.pathsMissSet`; do not edit the already-annotated citation.

- **P3 — C1 / freshness: the removal window is evidenced, but the exact W7 date is lane-attributed.** Evidence chain: `LOG.md` round-15 records `probe-latest` `at` = `00:01:09.976Z` at 2026-09-29T00:44:25Z; `corpus/knowledge/freshness-sweep.md` r17 records the 2026-09-29T03:2xZ run and `~/Projects/webzites/state/`'s 33-file SHA set unchanged; `LOG.md` and `corpus/lessons/round-18.md` record the 2026-10-14 12:40Z census (33/36 pinned children removed, including `webzites`; §history could not read `probe-history.jsonl`). The 2026-10-12 W7 prune/migration date appears in the r18 commit message and subsequent lane annotations, but no independent removal timestamp was found. The host search found only agent-session records and a fake-home fixture named `webzites`, not the live target. Smallest fix: retain the 2026-10-12 date as the lane's reported event, not an independently verified removal time; state the evidence-backed bound when describing disappearance.

## Checked and held

- The only cite is lane-authored `corpus/knowledge/ops-automation.md:141`. Its exact current bytes are included in the receipt below. The line directly says the snapshot and implementation are absent and marks the preceding freshness-gate behavior `UNVERIFIABLE`; that is truthful for the observed absent source and does not claim current age or live implementation behavior. `paths-before.json` also records `word: absent`, `line: 141`, `direct: true`, `mentions: true`, `indirect: false`. No append is needed.
- `git log -S'probe-latest.json' --format='%h %cI %s' -- corpus/knowledge/ops-automation.md` returned `1b309c9 2026-10-21T05:11:16-03:00 round-23: integrate falsifier corrections and snapshot integrity fixes`, `2a5502c 2026-09-28T20:05:41-03:00 round-13: freshness re-verification …`, and `18537e9 2026-09-28T16:15:02-03:00 round-5`. The round-23 change added c7 with its absent/unverifiable qualification; older round-13/round-5 entries and the round-15 logs record the snapshot age/observations. This establishes historical existence from lane records, not a Git history of the external source tree.
- No tools installed or updated. No production files changed; this report is the only file written.

### C1 target receipt

```json
{
  "id": "T14",
  "token": "~/Projects/webzites/state/probe-latest.json",
  "class": "newMissing",
  "observedAt": "2026-10-21T11:52:48Z",
  "state": "absent",
  "observation": {
    "commands": [
      "date -u +%Y-%m-%dT%H:%M:%SZ",
      "test -e /home/vgpnk/Projects/webzites/state/probe-latest.json && echo EXISTS || echo ABSENT",
      "stat -c '%n %w %y' /home/vgpnk/Projects",
      "ls -la /home/vgpnk/Projects/webzites",
      "ls -la /home/vgpnk/Projects",
      "git -C /home/vgpnk/Projects/webzites log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/webzites remote -v",
      "command -v webzites"
    ],
    "output": "date: 2026-10-21T11:52:48Z; test -e: ABSENT; stat: /home/vgpnk/Projects 2026-10-03 17:48:28.004231881 -0300 2026-10-21 05:19:01.033916520 -0300; ls -la /home/vgpnk/Projects/webzites: ls: cannot access '/home/vgpnk/Projects/webzites': No such file or directory; ls -la /home/vgpnk/Projects: total 0; existing directory listing includes ds4cc-marketplace but no webzites entry; git log: fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory (exit 128); git remote: fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory (exit 128); command -v webzites: NOT_FOUND_webzites"
  },
  "event": "The lane records probe-latest data in the 2026-09-29 round-15 observation and the webzites/state 33-file set present at r17 (2026-09-29T03:2xZ), then records webzites removed by the 2026-10-14T12:40Z r18 census. R18 attributes the removal to the 2026-10-12 W7 prune/migration; that exact date and mechanism were not independently established. Disappearance is bounded after the r17 observation and by the r18 census.",
  "cites": [
    {
      "cite": "corpus/knowledge/ops-automation.md:141",
      "lineText": "- [ops-automation:c7] **UNVERIFIABLE** — The pre-probe freshness gate reads the last snapshot at field rather than mtime. Surface: `/home/vgpnk/Projects/webzites/state/probe-latest.json`. Unverifiable: The snapshot and implementation are absent, so neither current last-run age nor implementation enforcement can be established; reading at rather than mtime remains a safety recommendation, not live verified behaviour.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    }
  ]
}
```

## Limits

The target tree is not a Git repository at its former path, so its `git log` and remote could not be queried. Lane history proves the snapshot existed and brackets its disappearance but cannot independently establish the exact removal date or whether it was deleted versus moved elsewhere. The 2026-10-12 event date remains a lane-recorded attribution.