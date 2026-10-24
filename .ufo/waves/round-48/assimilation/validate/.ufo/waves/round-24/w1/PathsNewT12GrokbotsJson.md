## Verdict

T12 is **absent** at the observed path. The registry did exist: the lane records a live `grokbots --check` read of the registry and a 20-row `bots list` result on 2026-09-28. The lane's round-18 W7 record attributes the loss to the 2026-10-12 `~/Projects` prune/migration, with the tree observed missing in the 2026-10-14 census; no evidence here establishes the exact file-deletion time. `SKILL.md:429` already states the current absence, and that statement is true, so its C1 cite action is `none`. The target remains a newly missing, unpinned C1 token and must be added to `pins.pathsMissSet` by the integration owner.

## Findings

### P2 — T12 is a truthful annotated absence, but is not pinned (C1 freshness)

- **Exact commands and current output:**
  - `test -e /home/vgpnk/Projects/webzites/fleet/grokbots.json` → `exists-rc=1` (no file exists).
  - `stat -c '%n %w %y' /home/vgpnk/Projects/webzites/fleet/grokbots.json` → `stat: cannot stat '/home/vgpnk/Projects/webzites/fleet/grokbots.json': No such file or directory (os error 2)`; exit 1.
  - `ls -la /home/vgpnk/Projects/webzites/fleet` → `ls: cannot access '/home/vgpnk/Projects/webzites/fleet': No such file or directory`; exit 2.
  - Nearest existing ancestor: `ls -la /home/vgpnk/Projects` showed the current project children (including `ds4cc-marketplace` and `ufo-fsd-alpha`) and no `webzites` directory. `stat -c '%n %w %y' /home/vgpnk/Projects` returned `/home/vgpnk/Projects 2026-10-03 17:48:28.004231881 -0300 2026-10-21 05:19:01.033916520 -0300`; this ancestor timestamp does not date the webzites removal.
- **Historical existence:** `corpus/knowledge/free-read-verbs.md:357-380, 412-419` records that the 2026-09-28 read-only `grokbots --check` read `fleet/grokbots.json`, checked 21 fleet rows, and returned `FAIL lucario: no registry row`; `bots list` reported 20 keepers. It also records the registry mtime as 2026-09-20. The raw `/tmp/kake-r12/live/` captures are no longer present, so this is the lane's retained contemporaneous record, not a re-read of the original capture.
- **Disappearance evidence:** `LOG.md:400-422` and the round-18 commit `b0feb308865d` say the W7 prune/migration removed 33 of 36 `~/Projects` children, including `webzites`, and that the round-18 baseline sweep on 2026-10-14 found 36 unannotated path misses. Its event attribution says the prune occurred on 2026-10-12. `corpus/knowledge/freshness-sweep.md:110-128` documents the webzites state directory still present in the 2026-09-29 r17 sweep (33-file hash set). Thus the disappearance is bounded by the lane's 2026-09-29 positive observation and 2026-10-14 negative census, with 2026-10-12 as the lane-recorded prune date; the precise deletion time is unknown.
- **History checks:** `git log -S'webzites/fleet/grokbots.json' --format='%h %cI %s' -- SKILL.md` first returns the absolute c8 cite at `83098b5` (2026-10-21T04:26:49-03:00), after the round-18 removal. The relative registry cite appears in the round-12-era `SKILL.md` history (`a642f93`, 2026-09-28T19:46:14-03:00). The lane is not a git history of the removed webzites source. `git -C /home/vgpnk/Projects/webzites rev-parse --is-inside-work-tree` fails because the directory is absent; the enclosing `/home/vgpnk` repository has no `Projects/webzites` history or tracked files. No source-repo remote can be read from an absent checkout.
- **Existing cite assessment:** the exact current bytes at `SKILL.md:429` are: `- [property-map:c8] **STALE** — Interpreting the relative second-registry path under the same \`~/Projects/webzites\` root, the file is absent and the paragraph does not annotate that registry as historical. Surface: \`test -e /home/vgpnk/Projects/webzites/fleet/grokbots.json\`. Correction: As of 2026-10-21, \`/home/vgpnk/Projects/webzites/fleet/grokbots.json\` is absent, so mark this second-registry location unavailable/historical or replace it with a verified current absolute path.` Its absence and date claims are truthful; no append is warranted for this cite. The `STALE` verdict is about the still-unannotated registry-of-record paragraph at `SKILL.md:34-36`, not a false current absence claim at line 429.
- **Impact:** C1 freshness. The path is absent but absent from the frozen `pins.pathsMissSet`, so it contributes to `newMissing` until reconciled.
- **Smallest fix:** have the L1 integration add exactly `~/Projects/webzites/fleet/grokbots.json` to `pins.pathsMissSet`; make no change to `SKILL.md:429` for this already-true absence cite. This report does not modify lane production files or pins.

### C1 target receipt

```json
{
  "id": "T12",
  "token": "~/Projects/webzites/fleet/grokbots.json",
  "class": "newMissing",
  "observedAt": "2026-10-21T11:50:08Z",
  "state": "absent",
  "observation": {
    "commands": [
      "test -e /home/vgpnk/Projects/webzites/fleet/grokbots.json",
      "stat -c '%n %w %y' /home/vgpnk/Projects/webzites/fleet/grokbots.json",
      "ls -la /home/vgpnk/Projects/webzites/fleet",
      "ls -la /home/vgpnk/Projects",
      "stat -c '%n %w %y' /home/vgpnk/Projects"
    ],
    "output": "test -e: exit 1; stat target: stat: cannot stat '/home/vgpnk/Projects/webzites/fleet/grokbots.json': No such file or directory (os error 2) (exit 1); ls fleet: ls: cannot access '/home/vgpnk/Projects/webzites/fleet': No such file or directory (exit 2); ls nearest existing ancestor /home/vgpnk/Projects: total 0; listing has current child directories and no webzites; stat ancestor: /home/vgpnk/Projects 2026-10-03 17:48:28.004231881 -0300 2026-10-21 05:19:01.033916520 -0300."
  },
  "event": "2026-10-12 W7 ~/Projects prune/migration; round-18 LOG.md:400-422 and commit b0feb308 attribute removal of webzites among 33 removed children to this event. The 2026-10-14 round-18 census recorded the tree absent; exact file-deletion time is not observed.",
  "cites": [
    {
      "cite": "SKILL.md:429",
      "lineText": "- [property-map:c8] **STALE** — Interpreting the relative second-registry path under the same `~/Projects/webzites` root, the file is absent and the paragraph does not annotate that registry as historical. Surface: `test -e /home/vgpnk/Projects/webzites/fleet/grokbots.json`. Correction: As of 2026-10-21, `/home/vgpnk/Projects/webzites/fleet/grokbots.json` is absent, so mark this second-registry location unavailable/historical or replace it with a verified current absolute path.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    }
  ]
}
```

## Checked and held

- Read the frozen contract, the C1 population entry, and `SKILL.md:426-432`; the population names exactly `SKILL.md:429` for T12.
- Read `freshness-pins.json:57-113`: the `pathsMissSet` already includes the webzites root and several children (including `fleet.config.json`), but not `~/Projects/webzites/fleet/grokbots.json`.
- Read the round-23 c8 report (`.ufo/waves/round-23/w1/ReverifyPropertyMapRegistry.md:26-44`) which records `ABSENT /home/vgpnk/Projects/webzites/fleet/grokbots.json`; the c8 reviewer (`.ufo/waves/round-23/w2/StalePropertyMap.md:39`) says this absence and proposed unavailable/historical correction are correct.
- The target is not a git repository at observation time. The requested git `log`/`remote` check against the source cannot be run on a nonexistent checkout; there is no lane source history proving its deletion commit. No tool was installed or updated.
- `SKILL.md:34` still describes the relative `fleet/grokbots.json` as a 20-row registry. The scanner explicitly excludes non-`~/` relative citations from path resolution (`corpus/knowledge/freshness-sweep.md:130-133`), and this assignment's population cite is the separate absolute T12 citation at line 429; no change is proposed to that out-of-population line here.
- No builds, tests, or formatters were run.

## Limits

The lane's round-12 live-run record establishes that the registry existed and was read on 2026-09-28, and the round-17 path sweep records the webzites state directory present on 2026-09-29. Round-18 records absence on 2026-10-14 and attributes it to the 2026-10-12 W7 prune/migration, but neither the source repository nor a direct deletion record is available here to prove the exact file-removal instant. Historical `/tmp` round-12 captures have expired. The current `~/Projects` mtime is not evidence of the webzites deletion time.