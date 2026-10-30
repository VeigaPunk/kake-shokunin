# ExecAppendOnly — Round 64 audit

## Verdict

The scoped append-only audit passes for the frozen base/T0 comparison. No deletions occur in `corpus/*.md`, `LOG.md`, or `SCORECARD.md`. The only changed base lines outside `corpus/knowledge/freshness-sidecar.json` are appended lines in `SKILL.md` and `corpus/QUALITY.md`; `corpus/lessons/round-64.md` is new. The sidecar contains seven `line` value updates and seven corresponding `lineSha256` updates (seven JSON entries), with no other changed file in this scoped diff.

## Exact evidence

Compared revisions: base `1a48131577ba82c967650561be34e8dba909432a` to T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`.

Command:
```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb --numstat -- corpus/ SCORECARD.md LOG.md SKILL.md
```
Output:
```text
2	0	SKILL.md
4	0	corpus/QUALITY.md
7	7	corpus/knowledge/freshness-sidecar.json
110	0	corpus/lessons/round-64.md
```
This directly shows zero deletions in the changed Markdown files and no `LOG.md` or `SCORECARD.md` rows (unchanged).

Command:
```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb --name-status -- corpus/ SCORECARD.md LOG.md SKILL.md
```
Output:
```text
M	SKILL.md
M	corpus/QUALITY.md
M	corpus/knowledge/freshness-sidecar.json
A	corpus/lessons/round-64.md
```

Command:
```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --unified=0 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb --numstat -- LOG.md SCORECARD.md corpus/QUALITY.md SKILL.md corpus/knowledge/freshness-sidecar.json corpus/lessons/round-64.md
```
Observed hunk summaries and classification:

| File (absolute path) | Hunks | Change | Classification |
|---|---:|---:|---|
| `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md` | 1 | +2 / -0 | Two appended gate-registry rows: `calibration-counter`, `quote-tool-counter` (diff hunk starts at line 1363). |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md` | 1 | +4 / -0 | Appended Round-64 quality criterion section (diff hunk starts at line 1423). |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-64.md` | 1 | +110 / -0 | New lesson file. |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/freshness-sidecar.json` | 7 | +7 / -7 | Seven entries, each changing the `line` and `lineSha256` cells; no other sidecar cells changed in the diff. |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/LOG.md` | 0 | 0 / 0 | Unchanged. |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/SCORECARD.md` | 0 | 0 / 0 | Unchanged. |

Sidecar hunks are at JSON file lines 60, 69, 78, 87, 96, 195, and 204. The `line` shifts are respectively 364→365, 445→446, 448→449, 449→450, 450→451, 423→424, and 431→432. Their adjacent `lineSha256` cell changes are part of the same seven entries.

No changed or deleted base line outside the sidecar JSON was found; all non-sidecar changes listed above are insertions only. The scoped `--stat` output was:
```text
 SKILL.md                                |   2 +
 corpus/QUALITY.md                       |   4 ++
 corpus/knowledge/freshness-sidecar.json |  14 ++--
 corpus/lessons/round-64.md              | 110 ++++++++++++++++++++++++++++++++
 4 files changed, 123 insertions(+), 7 deletions(-)
```

## Scope and risks

Only the requested append-only property was evaluated. Frozen claim instruments, receipts, contract, and lesson were not modified by this seat. No installs or tests/builds were run. No remaining scratch artifacts were needed; seat scratch directory was removed before yielding.
