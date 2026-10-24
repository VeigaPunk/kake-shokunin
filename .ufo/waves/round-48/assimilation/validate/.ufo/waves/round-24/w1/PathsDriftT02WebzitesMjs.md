## Verdict

T02's current target, `/home/vgpnk/Projects/webzites/bin/webzites.mjs`, was absent at `2026-10-21T11:50:52Z`. The frozen paths evidence classifies it as `drift`; its only gate-reported unannotated cite is `corpus/knowledge/free-read-verbs.md:321`. That row has no absence word within its own scanner window. The round-18/round-20 annotations are outside that window or refer to another token. The smallest proposed correction is one append-only, dated HTML comment at the end of line 321. This is an author-side observation, not an admission or an integration claim.

## Findings

### P2 — Target absent; line 321 remains unannotated

**Impacted claim/axis:** C1 / freshness, T02.

**Exact observation commands:**

```text
date -u +%Y-%m-%dT%H:%M:%SZ
test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs
stat -c '%n %w %y' /home/vgpnk/Projects/webzites/bin/webzites.mjs /home/vgpnk/Projects
ls -la /home/vgpnk/Projects
git -C /home/vgpnk/Projects/webzites log -3 --format='%H %cI %s'
git -C /home/vgpnk/Projects/webzites remote -v
```

**Exact observed output (the `ls` rendering is faithfully abbreviated because the tool elided 12 listing lines):**

```text
2026-10-21T11:50:52Z
test_exit=1
stat: cannot stat '/home/vgpnk/Projects/webzites/bin/webzites.mjs': No such file or directory (os error 2)
/home/vgpnk/Projects 2026-10-03 17:48:28.004231881 -0300 2026-10-21 05:19:01.033916520 -0300
ls -la /home/vgpnk/Projects: 0 files, 24 dirs; the listing has no webzites entry (it includes ds4cc-marketplace); ls_exit=0
git log: fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory; exit 128
git remote: fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory; exit 128
```

The T02 record in `.ufo/waves/round-24/paths-before.json` lists `corpus/knowledge/free-read-verbs.md:321` as its `unannotatedCites` entry. Its current cite row (321) and ±3 context (318–324) contain no absence vocabulary. The line 325 annotation is four lines after the cite and concerns `~/Projects/webzites/scripts/kimi-surface.mjs`, not this target; the end-of-file note at line 483 is also outside the ±2 window.

The round-18 note is likewise not local to line 321: the relevant free-read-verbs source-list annotation is at line 9, hundreds of lines earlier. Round-18 commit `b0feb30886585d8df6d4671845a2d18989ca722b` (2026-10-14) records that the standing sweep caught the 2026-10-12 `~/Projects` prune and lists `webzites` among 33/36 removed children. The round-20 restoration record says four table-distance citations remained uncleared; `.ufo/waves/round-22/w1/LegacyDebt.md:37` identifies line 321 and explains that the line-325 note names a different token four lines away. `corpus/QUALITY.md:35-39` records the no-table-splitting constraint that informed this prior treatment.

**Smallest proposed fix:** append the following exact text to the end of line 321 (do not rewrite the existing row):

```text
 <!-- r24 citation-local 2026-10-21: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration (round-18 sweep records webzites among 33/36 removed children); this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked. -->
```

### P3 — The ±2 lexical window admits unrelated absence words

**Impacted claim/axis:** C1 / freshness, reliability of per-citation status for T02. This is a limitation of the observed gate contract, not an additional frozen `unannotatedCites` item.

`scripts/freshness-sweep.mjs:314-337` implements `annotate()`: it blanks all path citations, searches the citing line and its ±2 window for `ABSENT_RE`, and by default accepts a matching word whether or not the window line names the target. The `mentions` filter only rejects that case when strict mode is enabled; `scanCitations()` enables it only when `pins.pathsAbsenceStrictSameLine === true` (`:413`). The round-18 pins do not enable that setting. Thus the `annotated-true` labels in the receipt below mean “covered by the gate's literal window,” not semantic proof that the neighboring absence statement is about this target.

Concrete bleed in this cite set: free-read-verbs.md:10 is inside the window of line 9's r18 absence note, which names the `src/` files but not `bin/webzites.mjs`; both round-5 aggregator cites are within the window of line 13's `No such file`, which applies to `package.json` even though that same historical command output reports the CLI file as present; and round-9.md:43 and :121 are within ±2 of “missing paths,” referring to the in-repo count rather than this CLI. These words pass the current lexical rule, while the target itself is now absent. The direct r20 annotations at SKILL.md:59, README.md:86, free-read-verbs.md:483, and probe-delta-alerting.md:82, and the explicit current correction at free-read-verbs.md:490, do specifically identify the target.

**Smallest fix:** no additional source edits are proposed in this scoped receipt: the frozen paths output lists only line 321 as unannotated, and the round-5 file is non-author. Keep the distinction between gate coverage and semantic applicability visible when interpreting the receipts; stronger attribution or a target-bound sidecar would require a separate lane decision.

## C1 target receipt

```json
{
  "id": "T02",
  "token": "~/Projects/webzites/bin/webzites.mjs",
  "class": "drift",
  "observedAt": "2026-10-21T11:50:52Z",
  "state": "absent",
  "observation": {
    "commands": [
      "date -u +%Y-%m-%dT%H:%M:%SZ",
      "test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs",
      "stat -c '%n %w %y' /home/vgpnk/Projects/webzites/bin/webzites.mjs /home/vgpnk/Projects",
      "ls -la /home/vgpnk/Projects",
      "git -C /home/vgpnk/Projects/webzites log -3 --format='%H %cI %s'",
      "git -C /home/vgpnk/Projects/webzites remote -v"
    ],
    "output": "2026-10-21T11:50:52Z; test_exit=1; stat: cannot stat '/home/vgpnk/Projects/webzites/bin/webzites.mjs': No such file or directory (os error 2); /home/vgpnk/Projects 2026-10-03 17:48:28.004231881 -0300 2026-10-21 05:19:01.033916520 -0300; ls -la /home/vgpnk/Projects exited 0, 0 files and 24 dirs, no webzites entry (12 listing lines elided by tool); git log and git remote each: fatal: cannot change to '/home/vgpnk/Projects/webzites': No such file or directory (exit 128)."
  },
  "event": "2026-10-12 ~/Projects prune/migration; round-18 commit b0feb30886585d8df6d4671845a2d18989ca722b (2026-10-14T09:45:43-03:00) records the sweep catching the prune and names webzites among 33/36 removed children. The file's exact removal time was not independently observed.",
  "cites": [
    {
      "cite": "SKILL.md:59",
      "lineText": "1. **Probe, don't guess.** `node ~/Projects/webzites/bin/webzites.mjs probe --all` *[r20 citation-local 2026-10-19: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/README.md:86",
      "lineText": "  bare `webzites` not on PATH (invoke `node ~/Projects/webzites/bin/webzites.mjs`), *[r20 citation-local 2026-10-19: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/drift-detection.md:7",
      "lineText": "Source: `~/Projects/webzites/{bin/webzites.mjs, scripts/kimi-surface.mjs,",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:1",
      "lineText": "source: ~/Projects/webzites/{bin/webzites.mjs, src/cli.mjs, src/fleet.mjs, src/probe.mjs, src/reconcile.mjs, scripts/kimi-surface.mjs, fleet/fleet.config.json} — local webzites tree read 2026-09-28, entry-internal live-run captures cited in body; metadata contract S019 (corpus/SOURCES.md, metadata authority only, not platform authority)",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:10",
      "lineText": "`~/Projects/webzites/bin/webzites.mjs`, `~/Projects/webzites/scripts/kimi-surface.mjs`",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:3",
      "lineText": "recheck: on webzites source change or operator restore — `ls -l ~/Projects/webzites/bin/webzites.mjs ~/Projects/webzites/src/cli.mjs ~/Projects/webzites/scripts/kimi-surface.mjs`; tree absent since the 2026-10-12 ~/Projects prune, so operator must restore it and re-run the cited verbs, or retire the live-run claims and counts in this entry",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:321",
      "lineText": "| probe | `node ~/Projects/webzites/bin/webzites.mjs probe ds4cc-com --json` | `/tmp/kake-r11/probe-dscc.out` → `/tmp/kake-r11/probe-ds4cc.out` (1-row JSON), `probe-ds4cc.err`, `/tmp/kake-r11/labrat-probe.md` (step log incl. the restore + re-verified sha); `probe-latest.json` row count/sha before–after; the new `probe-history.jsonl` line |",
      "authored": "lane",
      "status": "unannotated",
      "action": "append-inline",
      "text": " <!-- r24 citation-local 2026-10-21: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration (round-18 sweep records webzites among 33/36 removed children); this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked. -->"
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:483",
      "lineText": "> *[r20 citation-local 2026-10-19: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/free-read-verbs.md:490",
      "lineText": "- [free-read-verbs:c2] **STALE** — The documented absolute Node invocation is currently runnable from any cwd because its script is present. Surface: `test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs`. Correction: As of 2026-10-21, /home/vgpnk/Projects/webzites/bin/webzites.mjs is absent, so the documented absolute Node invocation cannot run from any cwd.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/probe-delta-alerting.md:120",
      "lineText": "- [probe-delta-alerting:c2] **HOLD** — The canonical history input and the two cited webzites CLI paths remain absent at their documented ~/Projects/webzites locations. Surface: `test -e /home/vgpnk/Projects/webzites/state/probe-history.jsonl; test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs; test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs; test -e /home/vgpnk/Projects/webzites`.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/probe-delta-alerting.md:81",
      "lineText": "  `node ~/Projects/webzites/bin/webzites.mjs …`,",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/knowledge/probe-delta-alerting.md:82",
      "lineText": "> *[r20 citation-local 2026-10-19: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-5-aggregator-mirror-pathless-cli-invocation.md:11",
      "lineText": "`SKILL.md:46` (`6b1cd07`) opens the checklist with `` `webzites probe --all` `` — invoked as a bare command; the CLI's real location is named only in the \"Cited paths\" trailer (`~/Projects/webzites/bin/webzites.mjs`), with no step declaring it on `PATH` and no prerequisite row for it.",
      "authored": "non-author",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-5-aggregator-mirror-pathless-cli-invocation.md:13",
      "lineText": "Host verification (2026-09-28): `command -v webzites` → empty (exit 1); `ls ~/.local/bin | grep -i webzites` → no match; `ls -la ~/Projects/webzites/bin/webzites.mjs` → `-rwxr-xr-x 1 vgpnk vgpnk 410 Sep 20 22:42`; `ls ~/Projects/webzites/package.json` → No such file (no root manifest to install a `bin` link from). So every pasted `webzites …` command in this file is non-runnable as written for a reader whose shell lacks the mission root's `bin/` on `PATH`.",
      "authored": "non-author",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-9.md:121",
      "lineText": "  `node ~/Projects/webzites/bin/webzites.mjs`). Admitted with qualification as",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    },
    {
      "cite": "corpus/lessons/round-9.md:43",
      "lineText": "  PATH — canonical invocation `node ~/Projects/webzites/bin/webzites.mjs`.",
      "authored": "lane",
      "status": "annotated-true",
      "action": "none",
      "text": ""
    }
  ]
}
```

## Checked and held

- Read all 16 population cites with surrounding context, checked the T02 population and frozen `paths-before.json` record, and inspected `annotate()` / `scanCitations()` at `scripts/freshness-sweep.mjs:300-338,405-413`.
- Confirmed the population class is `drift` and its listed actionable cite is only `free-read-verbs.md:321`; the target itself is included in `freshness-pins.json` `pathsMissSet`.
- Read the historical round-18 prune commit, round-20 post-review record, and round-22 residual-debt note for the line-321 provenance.
- No LSP device/server was exposed in the mounted tool inventory. Literal file reads and grep were used; no grep output is presented as semantic LSP proof.
- The requested target directory is absent, so its `git log` and `git remote` could not run. No target runtime, current full paths sweep, build, lint, formatter, or test was run. No tools were installed or updated.

## Limits

The path existence result is a direct host observation at the timestamp above. The 2026-10-12 prune/migration event is supported by the round-18 lane commit record, not by an independently observed deletion log; the `/home/vgpnk/Projects` mtime is 2026-10-21 and does not date webzites' removal. The home search was bounded and does not prove there is no copy on other storage. The gate's default ±2 lexical rule can accept neighboring absence terms that refer to another file or claim; `annotated-true` above records that gate-local result, not target-specific semantic attribution.