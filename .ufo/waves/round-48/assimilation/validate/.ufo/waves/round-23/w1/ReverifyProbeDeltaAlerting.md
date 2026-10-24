# Round 23 C1 re-verification — probe-delta-alerting

## Verdict

Freshness result: **5 HOLD, 1 STALE, 2 UNVERIFIABLE; 0 stale history-path observations.** The named six-hour timer is not installed in the checked system/user systemd scopes. The old webzites source tree and canonical history input are absent, so source-line behavior and run-derived historical counts cannot be re-derived. This is an author-side receipt, not independent admission.

Observed lane HEAD: `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`. The working-tree unit matched its base (`b5d599e19bead54b96f589444e9ec64cdf67c28a`) byte-for-byte; `scripts/probe-delta.mjs` had no diff since that base. The candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc` is an ancestor of the observed HEAD. All receipt anchors below were matched against the extracted base unit.

## Findings

- **P2 — STALE, claim `c6`: six-hour timer cadence as a current live schedule.** Command: `systemctl show webzites-probe.timer --property=LoadState,ActiveState,UnitFileState,TimersCalendar` and `systemctl --user show webzites-probe.timer --property=LoadState,ActiveState,UnitFileState,TimersCalendar`. Exact output from each: `LoadState=not-found`, `ActiveState=inactive`, `UnitFileState=`. The checked system/user unit-file paths (`/etc/systemd/system`, `/usr/lib/systemd/system`, `/home/vgpnk/.config/systemd/user`, `/home/vgpnk/.local/share/systemd/user`) all reported `ABSENT`. Impact: C1 freshness of the six-hour cadence / 12-hour coverage threshold. Smallest fix: add the correction sentence in claim `c6` and mark the 6h period as historical unless a current timer is restored and its schedule is rechecked.
- **P3 — UNVERIFIABLE, claims `c7` and `c8`: companion-source behavior and history-derived counts.** `test -d /home/vgpnk/Projects/webzites` reported `ABSENT`; the prescribed history check printed `ABSENT`; the default detector invocation reported `probe-delta: cannot read /home/vgpnk/Projects/webzites/state/probe-history.jsonl: ENOENT: no such file or directory, open '/home/vgpnk/Projects/webzites/state/probe-history.jsonl'` and `JSON_EXIT=2`. Impact: C1 freshness of the cited `src/cli.mjs`, `kimi-surface.mjs`, `src/fleet.mjs`, `src/probe.mjs` behaviors and historical event/coverage totals. Smallest fix: keep these explicitly historical (as the unit currently does), or restore the authoritative source/history and re-derive; neither is established by this check.

## Checked and held

- **`c1` HOLD — detector artifact/syntax.** `node --version` printed `v24.21.0`; `node --check /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/probe-delta.mjs` printed nothing and returned `CHECK_EXIT=0`; `test -e` returned `PRESENT_EXIT=0`.
- **`c2` HOLD — external history and cited CLI paths remain absent.** The prescribed `test -r /home/vgpnk/Projects/webzites/state/probe-history.jsonl && wc -l /home/vgpnk/Projects/webzites/state/probe-history.jsonl || echo ABSENT` printed `ABSENT` (`CHAIN_EXIT=0`); `test -e` probes found the history file, repository root, `bin/webzites.mjs`, `scripts/kimi-surface.mjs`, and `state/` absent. A glob for `/home/vgpnk/Projects/**/probe-history.jsonl` returned `No files found matching pattern`.
- **`c3` HOLD — detector's observable CLI contract.** A scratch-only JSONL fixture (not the historical input) produced `rows: 5`, `fullSweeps: 4`, `spotProbesSkipped: 1`, one `ENTER` and one `EXIT`, and a 13-hour coverage hole; `FIXTURE_EXIT=0`. This exercised parsing, spot exclusion, baseline behavior and output only; it does not re-derive the recorded historical results. With the default missing input the detector printed the ENOENT line quoted above and exited 2. `node scripts/probe-delta.mjs --definitely-not-a-flag` printed `unknown flag: --definitely-not-a-flag` and `FLAG_EXIT=64`. The source read showed `fs.readFileSync` for input and no file-write operation.
- **`c4` HOLD — bare command PATH observation.** `command -v webzites; echo COMMANDEXIT=$?` produced no command path and printed `COMMANDEXIT=1`.
- **`c5` HOLD — SKILL.md absolute-form text.** `SKILL.md:59` contains `node ~/Projects/webzites/bin/webzites.mjs probe --all`; the same line carries the r20 citation-local annotation that the target is absent and the command is historical, so this holds as a documentation-text claim, not as proof the command is executable.
- **S019 checked but skipped from the receipt:** `corpus/SOURCES.md:27` contains S019. Its row describes the own-work publishing corpus-contract audit (`scripts/corpus-contract.mjs`), says its scope is a local provenance-field/lesson-heading census with no verification of historical platform claims, and lists `corpus/lessons/round-21.md` as its use. I did not treat it as evidence for probe-delta behavior or event counts because it is provenance metadata, not a live operational surface.

### C1 receipt

```json
{
  "unit": "probe-delta-alerting",
  "path": "corpus/knowledge/probe-delta-alerting.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "node --check scripts/probe-delta.mjs; test -r ~/Projects/webzites/state/probe-history.jsonl && wc -l",
      "claim": "The local detector artifact exists in the lane and parses under Node without a syntax error.",
      "surface": "node --check /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/probe-delta.mjs",
      "method": "run",
      "observation": "Node v24.21.0; command emitted no output and returned exit 0; test -e confirmed the script is present (exit 0).",
      "verdict": "HOLD"
    },
    {
      "id": "c2",
      "anchor": "r18 re-census 2026-10-14: ~/Projects/webzites/state/probe-history.jsonl absent",
      "claim": "The canonical history input and the two cited webzites CLI paths remain absent at their documented ~/Projects/webzites locations.",
      "surface": "test -e /home/vgpnk/Projects/webzites/state/probe-history.jsonl; test -e /home/vgpnk/Projects/webzites/bin/webzites.mjs; test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs; test -e /home/vgpnk/Projects/webzites",
      "method": "test -e",
      "observation": "History test returned exit 1; path loop reported ABSENT for repository root, bin/webzites.mjs, scripts/kimi-surface.mjs and state/. The prescribed readability check printed ABSENT; the Projects-tree glob found no probe-history.jsonl.",
      "verdict": "HOLD"
    },
    {
      "id": "c3",
      "anchor": "(this is a report, not a gate); 2 = unreadable input; 64 = bad flag.",
      "claim": "The current CLI parses valid input into a non-gating report with exit 0, exits 2 for unreadable input, and exits 64 for an invalid flag.",
      "surface": "node scripts/probe-delta.mjs --history /tmp/kake-r23-ProbeDeltaAlerting-DX8R/probe-history-fixture.jsonl --json; node scripts/probe-delta.mjs --json; node scripts/probe-delta.mjs --definitely-not-a-flag",
      "method": "run",
      "observation": "Scratch fixture: rows 5, malformed 0, fullSweeps 4, spotProbesSkipped 1, ENTER x and EXIT x, maxGapH 13 with one 13h hole; exit 0. Missing default history: `probe-delta: cannot read /home/vgpnk/Projects/webzites/state/probe-history.jsonl: ENOENT: no such file or directory, open '/home/vgpnk/Projects/webzites/state/probe-history.jsonl'`, exit 2. Bad flag: `unknown flag: --definitely-not-a-flag`, exit 64.",
      "verdict": "HOLD"
    },
    {
      "id": "c4",
      "anchor": "not on PATH; SKILL.md now carries the absolute form)",
      "claim": "The bare webzites command is not resolvable on PATH at verification time.",
      "surface": "command -v webzites",
      "method": "run",
      "observation": "No command path was printed; COMMANDEXIT=1.",
      "verdict": "HOLD"
    },
    {
      "id": "c5",
      "anchor": "SKILL.md now carries the absolute form",
      "claim": "SKILL.md contains the absolute webzites CLI invocation form; it is documented with an absent/historical-target annotation.",
      "surface": "/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:59",
      "method": "read",
      "observation": "Line 59 contains `node ~/Projects/webzites/bin/webzites.mjs probe --all`, followed by the r20 citation-local note that the binary is absent and the command is historical, not executable until restored and rechecked.",
      "verdict": "HOLD"
    },
    {
      "id": "c6",
      "anchor": "6h timer period). Baseline 2026-09-28:",
      "claim": "The cited six-hour probe-timer cadence remains a current installed live schedule in the inspected system and user scopes.",
      "surface": "systemctl show webzites-probe.timer --property=LoadState,ActiveState,UnitFileState,TimersCalendar; systemctl --user show webzites-probe.timer --property=LoadState,ActiveState,UnitFileState,TimersCalendar",
      "method": "run",
      "observation": "Both commands returned `LoadState=not-found`, `ActiveState=inactive`, `UnitFileState=`. The checked system and user timer-file paths were all ABSENT.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, system and user systemd both report webzites-probe.timer as LoadState=not-found, and the checked system and user timer-file paths are absent; the cited six-hour cadence is not a current installed timer in those scopes."
    },
    {
      "id": "c7",
      "anchor": "violated/error row** (`src/cli.mjs:99`) — read its stdout, never its exit",
      "claim": "The cited companion webzites source-line behaviors (status exit handling, kimi-surface behavior, merge semantics, probe-error handling and timer writes) are verifiable from the current source tree.",
      "surface": "~/Projects/webzites/src/cli.mjs:99; scripts/kimi-surface.mjs:1197-1198; src/fleet.mjs:30-37; src/probe.mjs:79-81; src/cli.mjs:78,1002",
      "method": "test -e",
      "observation": "The cited ~/Projects/webzites repository root and named CLI paths returned ABSENT; no source file is available at those locations for line-level re-verification.",
      "verdict": "UNVERIFIABLE",
      "reason": "The source tree cited for these line-specific behaviors has been pruned and is absent at ~/Projects/webzites, so no live source surface can decide whether the historical implementation details still hold."
    },
    {
      "id": "c8",
      "anchor": "76 rows → 66 full sweeps / 10 spot",
      "claim": "The historical baseline and r16 re-pin row, sweep, event and coverage counts recorded in the unit are correct.",
      "surface": "~/Projects/webzites/state/probe-history.jsonl",
      "method": "test -e",
      "observation": "The canonical history file is absent (`test -e` exit 1); the detector reports ENOENT on its default input; no copy was found under /home/vgpnk/Projects.",
      "verdict": "UNVERIFIABLE",
      "reason": "The canonical history input is absent and no copy was found under /home/vgpnk/Projects, so the historical row/event/coverage totals cannot be re-derived from the designated live surface now."
    }
  ]
}
```

## Limits

- No public URLs were relevant to this unit. I made no authenticated requests, writes, publishes, deploys, or systemd mutations.
- The fixture was written only under `/tmp/kake-r23-ProbeDeltaAlerting-DX8R`; it verifies current CLI behavior, not the historic dataset. No lane files other than this report were written.
- No tool was installed or updated; Node v24.21.0 was already available.
- Not separately re-derived: per-event historic ground-truth rows (charter-ghp, lucario, veigapunk-page, xsnapshot-app), naive-diff precision/recall, deficit-row counts, merged-row caveats, and `probe-latest.json` marker details. These require the missing history or webzites source surfaces and are covered as historical/unverifiable rather than treated as fresh evidence. The six-hour timer-status claim was checked separately and is STALE as recorded in `c6`.
