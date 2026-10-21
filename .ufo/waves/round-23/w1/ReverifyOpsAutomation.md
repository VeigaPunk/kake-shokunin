## Verdict

C1 `ops-automation` rechecked on 2026-10-21. The probe and keeper timer claims and the documented CLI surface are stale as live interfaces; the stated live history source is absent; a dated history transition and the “never fired” assertion cannot be re-established from current evidence. This is an author-side re-verification report, not independent admission. I changed no production files; only this scoped report is written.

## Findings

### P2 — Probe timer schedule is not a current live surface

**Impacted claim/axis:** C1 freshness; `webzites-probe.timer` is described as the installed six-hour probe timer with a five-minute boot delay, persistence, and `webzites probe --all --quiet` execution.

**Exact checks and observed output:** `test -e /home/vgpnk/.config/systemd/user/webzites-probe.timer` → `ABSENT /home/vgpnk/.config/systemd/user/webzites-probe.timer`. `systemctl --user show webzites-probe.timer webzites-keeper.timer -p Id -p LoadState -p ActiveState -p UnitFileState -p NextElapseUSecRealtime -p LastTriggerUSec -p FragmentPath` returned `Id=webzites-probe.timer`, `LoadState=not-found`, `ActiveState=inactive`, and empty `FragmentPath`, `UnitFileState`, `NextElapseUSecRealtime`, and `LastTriggerUSec`. `systemctl --user list-timers --all --no-pager webzites-probe.timer webzites-keeper.timer` returned `NEXT LEFT LAST PASSED UNIT ACTIVATES`, a blank line, then `0 timers listed.`

**Smallest fix:** Add a dated round-23 correction to the unit stating that the cited probe timer is absent/not loaded and the historic schedule must not be treated as current; retire or restore the source before describing its cadence as live.

### P2 — Keeper timer’s recorded loaded state is no longer current

**Impacted claim/axis:** C1 freshness; the keeper timer is presented as loaded, disabled, and inactive, with a daily schedule.

**Exact checks and observed output:** `test -e /home/vgpnk/.config/systemd/user/webzites-keeper.timer` → `ABSENT /home/vgpnk/.config/systemd/user/webzites-keeper.timer`. The `systemctl --user show ...` command above returned `Id=webzites-keeper.timer`, `LoadState=not-found`, `ActiveState=inactive`, and empty `FragmentPath`, `UnitFileState`, `NextElapseUSecRealtime`, and `LastTriggerUSec`.

**Smallest fix:** Add a dated round-23 correction that the unit is absent and `LoadState=not-found`; keep the older r12 state clearly historical rather than current.

### P2 — The documented `webzites` CLI is absent from its cited live surface

**Impacted claim/axis:** C1 freshness; `bin/webzites.mjs --help` is cited as the live CLI surface, including `status`, `map`, `auth`, and `install` verbs.

**Exact checks and observed output:** `test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs` → `ABSENT /home/vgpnk/Projects/webzites/bin/webzites.mjs`. `if command -v webzites >/dev/null 2>&1; then printf 'FOUND %s\\n' "$(command -v webzites)"; webzites --help; else printf 'NOT_FOUND webzites\\n'; fi` returned `NOT_FOUND webzites`.

**Smallest fix:** Add a dated correction that the cited script and executable are absent, and do not describe the verb table as a live interface unless an authoritative implementation is restored or identified.

### P3 — History-dependent claims cannot be fully reverified

**Impacted claim/axis:** C1 freshness; the current-file row-count floor is stale because the file is absent, while the dated `veigapunk-page` transition cannot be checked against raw rows.

**Exact check and observed output:** `test -e /home/vgpnk/Projects/webzites/state/probe-history.jsonl` → `ABSENT /home/vgpnk/Projects/webzites/state/probe-history.jsonl`.

**Smallest fix:** In the round-23 correction section, record the dated absence and distinguish the 78-row 2026-09-29 measurement from any live count; mark row-dependent historic transitions UNVERIFIABLE rather than repeating them as rechecked facts.

## Checked and held

Read `corpus/knowledge/ops-automation.md` in full and read the base-revision version with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show b5d599e19bead54b96f589444e9ec64cdf67c28a:corpus/knowledge/ops-automation.md`; receipt anchors below are copied from that base content. Checked the referenced user-unit files, timer state, event-log path, CLI source path, and keeper-log directory. The keeper-log directory check returned `ABSENT /home/vgpnk/Projects/webzites/reports/keepers`.

```json
{
  "unit": "ops-automation",
  "path": "corpus/knowledge/ops-automation.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "`webzites-probe.timer` | `OnUnitActiveSec=6h`, `OnBootSec=5min`, `Persistent=true` | `webzites probe --all --quiet`",
      "claim": "The cited probe timer is an installed live timer, scheduled every six hours with a five-minute boot delay and persistence to run `webzites probe --all --quiet`.",
      "surface": "systemctl --user show webzites-probe.timer webzites-keeper.timer -p Id -p LoadState -p ActiveState -p UnitFileState -p NextElapseUSecRealtime -p LastTriggerUSec -p FragmentPath",
      "method": "run",
      "observation": "Id=webzites-probe.timer\nLoadState=not-found\nActiveState=inactive\nFragmentPath=\nUnitFileState=\nNextElapseUSecRealtime=\nLastTriggerUSec=",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, `webzites-probe.timer` is not loaded (`LoadState=not-found`) and its cited user unit file is absent, so the documented schedule is not a current live timer configuration."
    },
    {
      "id": "c1",
      "anchor": "status (r12): loaded, DISABLED, inactive (dead), zero journal entries; has never fired.",
      "claim": "The keeper timer is currently loaded, disabled, and inactive, with the cited daily timer configuration.",
      "surface": "systemctl --user show webzites-probe.timer webzites-keeper.timer -p Id -p LoadState -p ActiveState -p UnitFileState -p NextElapseUSecRealtime -p LastTriggerUSec -p FragmentPath",
      "method": "run",
      "observation": "Id=webzites-keeper.timer\nLoadState=not-found\nActiveState=inactive\nFragmentPath=\nUnitFileState=\nNextElapseUSecRealtime=\nLastTriggerUSec=",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, `webzites-keeper.timer` is not loaded (`LoadState=not-found`) and its cited user unit file is absent, so the `loaded, DISABLED, inactive (dead)` state is historical rather than current."
    },
    {
      "id": "c1",
      "anchor": "**78 rows** 2026-09-20→09-29 (r16 re-read 2026-09-29T02:2xZ; row 77 =",
      "claim": "The cited `probe-history.jsonl` is a live source with at least 78 rows and a row-count floor that must be re-derived as it grows.",
      "surface": "/home/vgpnk/Projects/webzites/state/probe-history.jsonl",
      "method": "test -e",
      "observation": "ABSENT /home/vgpnk/Projects/webzites/state/probe-history.jsonl",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the cited `probe-history.jsonl` path is absent, so it has no live row count to report; `78 rows` remains only the dated 2026-09-29 observation."
    },
    {
      "id": "c1",
      "anchor": "## CLI surface beyond probe/reconcile (`bin/webzites.mjs --help`, verbatim)",
      "claim": "The cited `bin/webzites.mjs` help surface exists and provides the listed live CLI verbs, including `status`, `map`, `auth`, and `install`.",
      "surface": "if command -v webzites >/dev/null 2>&1; then printf 'FOUND %s\\n' \"$(command -v webzites)\"; webzites --help; else printf 'NOT_FOUND webzites\\n'; fi",
      "method": "run",
      "observation": "NOT_FOUND webzites",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, the cited `bin/webzites.mjs` file is absent and no `webzites` executable is on PATH, so the listed verbs are not available from the documented live surface."
    },
    {
      "id": "c1",
      "anchor": "**`veigapunk-page` flipped violated→ok** between the 2026-09-21T03:32:06",
      "claim": "The probe-history rows show `veigapunk-page` flipping from violated to ok between the 2026-09-21T03:32:06 and 04:14:50 full sweeps.",
      "surface": "/home/vgpnk/Projects/webzites/state/probe-history.jsonl",
      "method": "test -e",
      "observation": "ABSENT /home/vgpnk/Projects/webzites/state/probe-history.jsonl",
      "verdict": "UNVERIFIABLE",
      "reason": "The raw event-log file is absent, so no live surface remains from which to inspect the two dated rows and verify this historical transition."
    },
    {
      "id": "c1",
      "anchor": "status (r12): loaded, DISABLED, inactive (dead), zero journal entries; has never fired.",
      "claim": "The keeper timer had never fired by the historical r12 check and had zero journal entries at that time.",
      "surface": "journalctl --user --unit=webzites-keeper.service --no-pager -o short-iso",
      "method": "run",
      "observation": "-- No entries --",
      "verdict": "UNVERIFIABLE",
      "reason": "The current retained journal has no entries and the cited unit file is absent, but this does not establish that the historical journal was complete or prove the timer never fired by the r12 check."
    }
  ]
}
```

**Skipped claims and why:** I did not individually receipt the `charter-ghp`, `lucario`, `xsnapshot-app`, or `ufo-fsd-kimi` row transitions; the 67/11 full-sweep/spot split, gap distribution, detector counts, or probe-latest `at`/mtime relationship; these depend on the absent `probe-history.jsonl` and/or `probe-latest.json`. I did not receipt the keeper-log format or the `charter-ghp` source-lag example because `reports/keepers` is absent. I did not verify service `SuccessExitStatus=1` behavior, install behavior, or the operational behavior of individual CLI verbs because the `.service` files, cited source tree, and executable are absent; I did not run probe/install/keeper commands that could write state. No public URLs are cited by this unit.

## Limits

All checks were read-only. `journalctl` returning `-- No entries --` is not evidence of an exhaustive historical journal, and no missing-source claim was upgraded to HOLD. The report records current local observations only; it does not restore the webzites source or establish what happened after the cited 2026-09 evidence.