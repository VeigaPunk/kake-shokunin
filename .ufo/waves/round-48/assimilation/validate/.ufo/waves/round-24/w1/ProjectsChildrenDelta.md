## Verdict

**P3 — Freshness (informational P2b): recommend re-censusing `pins.projectsChildrenSet` in round 24.** The round-18 pin (`updated: 2026-10-14`) has 14 names; the live `/home/vgpnk/Projects` directory and round-24 round-open census both have 24. All 14 pinned names remain present; 10 names are added and none are removed. This pin is explicitly informational and never gating. Resetting it would remove persistent delta noise and provide a current baseline; it must not be treated as a freshness gate. The set is volatile, so this is a point-in-time baseline, not a durable claim about future membership.

## Findings

### P3 — Ten added children; no removals from the pin

**Exact observation command (run with `~/Projects`, which expands to `/home/vgpnk/Projects`):**

```sh
find ~/Projects -mindepth 1 -maxdepth 1 -exec stat -c '%n|%F|birth=%w|birthEpoch=%W|mtime=%y|inode=%i' {} + | sort
```

The following are the exact birth-time fields observed in its output (local time, `-0300`):

| Child | Birth time (`stat %w`) | Literal mention in lane files | `Projects/<child>` path citation |
|---|---|---|---|
| `BTVREV` | `2026-10-17 00:02:15.106138653 -0300` | Yes — census/sweep records only | No |
| `TPSnCONC` | `2026-10-18 15:00:00.032659543 -0300` | Yes — census/sweep records only | No |
| `audio-shokunin-publish` | `2026-10-16 12:54:46.767999189 -0300` | Yes — census/sweep records only | No |
| `ds4cc-marketplace` | `2026-10-21 05:19:01.033916520 -0300` | Yes — current and historical source-path references | Yes |
| `gkeep` | `2026-10-17 16:46:10.658148512 -0300` | Yes — census/sweep records only | No |
| `kaidoku-r21-battery` | `2026-10-21 05:06:52.953559476 -0300` | Yes — round-23/24 census records only | No |
| `kaidoku-r21-compare` | `2026-10-21 05:06:52.530558241 -0300` | Yes — round-23/24 census records only | No |
| `kaidoku-r21-coverage` | `2026-10-21 05:06:51.553555387 -0300` | Yes — round-23/24 census records only | No |
| `kimi-code` | `2026-10-15 04:45:37.954789965 -0300` | Yes — census records plus unrelated provider/cache-name mentions | No |
| `xsnapshot` | `2026-10-19 20:42:11.007874434 -0300` | Yes — census records plus unrelated `xsnapshot-app`/site mentions | No |

The name-search evidence for the first four names consists of the round-20 resume census files (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/round-20/resume/paths-after.txt`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/round-20/resume/paths-before.json`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/round-20/resume/paths-before.txt`), `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-21/paths-after.json`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/final-suite.json`, and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/paths-before.json`. The `kaidoku-r21` family appears in the last two census records only. The `kimi-code` and `xsnapshot` bare-name results include unrelated meanings; the path-form result below is the criterion used to distinguish project-path citations.

**Exact set-delta output** (computed by comparing the sorted `readdirSync` names file with `pins.projectsChildrenSet`):

```text
LIVE_COUNT=24 PIN_COUNT=14
ADDED_vs_pin=["BTVREV","TPSnCONC","audio-shokunin-publish","ds4cc-marketplace","gkeep","kaidoku-r21-battery","kaidoku-r21-compare","kaidoku-r21-coverage","kimi-code","xsnapshot"]
ADDED_COUNT=10
REMOVED_vs_pin=[]
REMOVED_COUNT=0
```

The independent round-open capture `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/paths-before.json` reports `projectsChildrenDelta.pinned: true`, `removed: []`, and the same 10-name `added` array. The exact sorted live JSON array for a re-census is:

```json
[
  "BTVREV",
  "TPSnCONC",
  "audio-shokunin-publish",
  "burnerchrome",
  "ds4cc-marketplace",
  "gamez",
  "gkeep",
  "godspeed-core",
  "kaidoku-r21-battery",
  "kaidoku-r21-compare",
  "kaidoku-r21-coverage",
  "kimi-code",
  "kimi-shokunin",
  "myskills",
  "omarchy-usage-tray",
  "ompskills",
  "opencodeufo",
  "prymeagnt",
  "prymeagnt-archive",
  "shokunin",
  "the-kimiraikkoner",
  "tog",
  "ufo-fsd-alpha",
  "xsnapshot"
]
```

**Impacted claim/axis:** round-24 P2b / freshness. `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/freshness-sweep.md:54` still labels the baseline `projectsChildrenSet` as “(36 entries)”; the actual pinned array has 14 entries and the current directory has 24. The pin-file comment says to re-pin in the same commit as corrected corpus prose and to record the round for each value. **Smallest fix:** replace `pins.projectsChildrenSet` with the exact array above and update the P2b row's count to 24 in the same integration change; advance the shared pin metadata (`updated`, `round`) as applicable to the integration. Leave the informational, never-gating behavior unchanged.

### P3 — Path-citation check distinguishes the census mentions from source citations

**Exact search request:** `functions.grep(pattern="Projects/(BTVREV|TPSnCONC|audio-shokunin-publish|gkeep|kaidoku-r21-battery|kaidoku-r21-compare|kaidoku-r21-coverage|kimi-code|xsnapshot)\\b", path="/home/vgpnk/Projects/shokunin/kake-shokunin", gitignore=false)`.

**Exact observed output:** `No matches found`.

Thus the nine other than `ds4cc-marketplace` are mentioned in lane measurement/history files, but no lane file contains a `Projects/<name>` path citation for them. `ds4cc-marketplace` does have path citations, including `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:16,19` and `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/fleet-registry.md:49-51`; its directory birth time is 2026-10-21 05:19:01.033916520 -0300. The round-24 contract and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/paths-before.json` identify this as the just-reappeared source tree. Several older ds4cc citations still carry r18 absence annotations, so the separate C1 reconciliation must append the required restoration corrections; this report does not alter or substitute for those receipts.

## Checked and held

- Read `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/freshness-pins.json`: `updated` is `2026-10-14`, `round` is `18`, and `projectsChildrenSet` contains the 14 names still present.
- Read `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/freshness-sweep.md:52-55` and `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs:489-505`: P2b is informational, never gating; the script prints added/removed names but does not use this delta in its `ok` predicate.
- Read the round-24 contract and its round-open census. The latter's 24-name live array and 10-name delta agree with the filesystem comparison.
- `stat` shows the three `kaidoku-r21-*` directories were born at 05:06:51–52 -0300; `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/final-suite.json` was created at 05:12:20.975525757 -0300 and recorded those names. `ds4cc-marketplace` was born later, at 05:19:01.033916520 -0300. This timing is consistent with its appearance after that round-23 snapshot; it does not establish the cause of any directory creation.
- No tools were installed or updated.

## Limits

- Birth times are filesystem `stat %w` observations at this host, not source-control creation dates or proof of who created the directories.
- The 24-name array is point-in-time and the project root includes transient worktrees; membership can change again. Recheck the array at integration if time has elapsed.
- The bare-name search results for `kimi-code` and `xsnapshot` include unrelated provider/cache or site identifiers. The path-form search is the basis for the path-citation conclusion.
- This is a scoped freshness report only; no pin, corpus prose, C1 receipt, or production file was edited, and no freshness sweep or other verification was run.