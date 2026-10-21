## Verdict

**HOLD recommendation for C1 freshness** — the selected current-path claim is stale, the cited six-hour timer is not installed in either systemd manager, and core behavior/count claims cannot be reverified because the documented webzites source and retained run captures are absent. This is a scoped re-verification report, not an independent admission.

## Findings

### P2 — The documented command path and automatic recovery timer are stale

- Exact check `test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs` observed: `ABSENT  /home/vgpnk/Projects/webzites/bin/webzites.mjs`.
- Exact command `command -v webzites || echo "webzites: not on PATH"` observed: `webzites: not on PATH`.
- Exact commands `systemctl --user show webzites-probe.timer --property=LoadState,ActiveState,SubState,NextElapseUSecRealtime,FragmentPath --no-pager` and `systemctl show webzites-probe.timer --property=LoadState,ActiveState,SubState,NextElapseUSecRealtime,FragmentPath --no-pager` observed `LoadState=not-found`, `ActiveState=inactive`, `SubState=dead`, empty `FragmentPath` and `NextElapseUSecRealtime`, exit 0, for both managers.
- **Impacted claim/axis:** C1 freshness; the absolute invocation assertion and the statement that a six-hour `webzites-probe.timer` restores the 18-row snapshot.
- **Smallest fix:** in the round-23 correction, mark the documented script invocation unavailable and remove/correct the timer recovery statement unless the source path and timer are restored and rechecked.

### P2 — Core verb behavior and current universe counts are not live-verifiable

- Exact existence checks observed `ABSENT` for `/home/vgpnk/Projects/webzites/src/cli.mjs`, `/home/vgpnk/Projects/webzites/fleet/fleet.config.json`, `/tmp/kake-r11/probe-ds4cc.out`, `/tmp/kake-r11/labrat-probe.md`, `/tmp/kake-r12/live/status-json.out`, and `/tmp/kake-r12/labrat.md`.
- A current public GET to the Plazir 15 page returned HTTP 200 and 38,337 downloaded bytes, but that cannot establish what the absent CLI does or whether its local source body matches.
- **Impacted claim/axis:** C1 freshness; `probe` snapshot clobbering, `status` exit semantics, fleet counts, and the `reconcile` source-comparison result remain UNVERIFIABLE rather than current confirmations.
- **Smallest fix:** restore the named source/config surfaces and rerun the read-only checks, or retain these statements only as explicitly dated history with the reasons below; a live page GET alone is not a substitute.

## Checked and held

The unit was read in full. Its anchors were confirmed to be from the frozen base: `git show b5d599e19bead54b96f589444e9ec64cdf67c28a:corpus/knowledge/free-read-verbs.md` and the worktree file both had SHA-256 `50e070f5ce6edb6185655c737e2ba862c91f68f3a3ea19b209745bbcf75502eb`; the base-to-candidate and base-to-worktree diffs for that file both returned exit 0. Observed lane HEAD was `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`.

```json
{
  "unit": "free-read-verbs",
  "path": "corpus/knowledge/free-read-verbs.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "tree absent since the 2026-10-12 ~/Projects prune",
      "claim": "The documented webzites source tree remains absent at its ~/Projects path.",
      "surface": "test -e /home/vgpnk/Projects/webzites",
      "method": "test -e",
      "observation": "ABSENT  /home/vgpnk/Projects/webzites",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "Invocation is always the absolute node path from any cwd",
      "claim": "The documented absolute Node invocation is currently runnable from any cwd because its script is present.",
      "surface": "test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs",
      "method": "test -e",
      "observation": "ABSENT  /home/vgpnk/Projects/webzites/bin/webzites.mjs",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, /home/vgpnk/Projects/webzites/bin/webzites.mjs is absent, so the documented absolute Node invocation cannot run from any cwd."
    },
    {
      "id": "c1",
      "anchor": "bare `webzites` is not on PATH on this host",
      "claim": "The bare `webzites` command is still unavailable on PATH.",
      "surface": "command -v webzites || echo \"webzites: not on PATH\"",
      "method": "run",
      "observation": "webzites: not on PATH",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "Read straight off `fleet/fleet.config.json` (21 rows, `schema`",
      "claim": "The present-day fleet universe is the recorded 21-row population with 18 URL-bearing rows, 15 kimi-surface rows, and 13 sourceDir rows.",
      "surface": "test -e /home/vgpnk/Projects/webzites/fleet/fleet.config.json",
      "method": "test -e",
      "observation": "ABSENT  /home/vgpnk/Projects/webzites/fleet/fleet.config.json",
      "verdict": "UNVERIFIABLE",
      "reason": "The live fleet/fleet.config.json surface is absent, so its present-day contents and counts cannot be checked."
    },
    {
      "id": "c1",
      "anchor": "Therefore `probe <id>` replaces the 18-row fleet snapshot with a **1-row** file;",
      "claim": "A single-id `probe` currently replaces an 18-row snapshot with one row and appends a history entry.",
      "surface": "test -e /home/vgpnk/Projects/webzites/src/cli.mjs; test -e /tmp/kake-r11/probe-ds4cc.out; test -e /tmp/kake-r11/labrat-probe.md",
      "method": "test -e",
      "observation": "ABSENT  /home/vgpnk/Projects/webzites/src/cli.mjs\nABSENT  /tmp/kake-r11/probe-ds4cc.out\nABSENT  /tmp/kake-r11/labrat-probe.md",
      "verdict": "UNVERIFIABLE",
      "reason": "The source file and cited round-11 probe captures are absent; no current executable or retained transcript can reproduce the reported state mutation."
    },
    {
      "id": "c1",
      "anchor": "**Exit asymmetry — snapshot-relative, not fleet-relative.** `status --json`",
      "claim": "`status --json` always exits 0, while plain `status` is snapshot-relative.",
      "surface": "test -e /home/vgpnk/Projects/webzites/src/cli.mjs; test -e /tmp/kake-r12/live/status-json.out; test -e /tmp/kake-r12/labrat.md",
      "method": "test -e",
      "observation": "ABSENT  /home/vgpnk/Projects/webzites/src/cli.mjs\nABSENT  /tmp/kake-r12/live/status-json.out\nABSENT  /tmp/kake-r12/labrat.md",
      "verdict": "UNVERIFIABLE",
      "reason": "The CLI source and cited round-12 status/run captures are absent, so the exit branches cannot be checked against current execution or retained output."
    },
    {
      "id": "c1",
      "anchor": "except the 6h `webzites-probe.timer` sweep,",
      "claim": "A six-hour `webzites-probe.timer` is installed and re-widens narrowed snapshots.",
      "surface": "systemctl --user show webzites-probe.timer --property=LoadState,ActiveState,SubState,NextElapseUSecRealtime,FragmentPath --no-pager; systemctl show webzites-probe.timer --property=LoadState,ActiveState,SubState,NextElapseUSecRealtime,FragmentPath --no-pager",
      "method": "run",
      "observation": "--- user systemd timer ---\nLoadState=not-found\nActiveState=inactive\nSubState=dead\nFragmentPath=\nNextElapseUSecRealtime=\nuser_rc=0\n--- system systemd timer ---\nLoadState=not-found\nActiveState=inactive\nSubState=dead\nFragmentPath=\nNextElapseUSecRealtime=\nsystem_rc=0",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, neither systemd manager has a `webzites-probe.timer` unit (`LoadState=not-found`), so no such six-hour sweep is available to re-widen narrowed snapshots."
    },
    {
      "id": "c1",
      "anchor": "`reconcile plazir15-ghp --json` → **exit 0, match** (sha `d82af77a…`, 38 337 B",
      "claim": "The `plazir15-ghp` public page currently serves HTTP 200 with a 38,337-byte response; this GET does not reverify equality with the historical local source body.",
      "surface": "https://veigapunk.github.io/plazir-15-site/",
      "method": "GET",
      "observation": "status=200 effective_url=https://veigapunk.github.io/plazir-15-site/ size_download=38337 content_type=text/html; charset=utf-8 redirects=0",
      "verdict": "HOLD"
    }
  ]
}
```

**Skipped claims and why:**

- The current fleet counts, `probe` side effects, and `status` exit behavior are included above as UNVERIFIABLE; their present-day source/config files are missing, and the cited `/tmp/kake-r11` and `/tmp/kake-r12` artifacts checked here are absent.
- Other `grokbot reconcile` and `sync-check` claims (row selection, verdict rules, no-write behavior, 404 sentinel, and the 2026-09-28 fleet outcomes) were not given separate receipt rows. Their implementation files and fleet config are under the absent webzites tree; the cited round-11 sync/reconcile captures checked here are also absent. The current Plazir GET confirms only its served status/length, not the local-source comparison or CLI result.
- Round-12 `grokbots --check`, `bots list`, and `bots report` implementation/results were not separately rechecked: the CLI is absent and `/tmp/kake-r12` plus the cited output files are absent.
- The source's explicitly excluded mutating, metered, browser/lease, and speedrun verbs were not run: they are outside this free-read unit's tested scope, and the lane contract forbids writes, publishing, and metered/chat actions.

## Limits

- Only public GETs and read-only path, git, command lookup, and systemd queries were used; no tools were installed or updated, no subagents were dispatched, and no build/lint/formatter was run.
- The Plazir response is current as of this observation, but the matching historical `sourceDir` and `reconcile` result were not re-established.
- This report is the only file written. No production files, lane index, or `.ufo/state` were modified.