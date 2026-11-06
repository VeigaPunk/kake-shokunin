# ExecRegProbe — C1 repair-row empirical falsification (kake round 99, w1)

Seat: ExecRegProbe. Lane: /home/vgpnk/Projects/shokunin/kake-shokunin. Repair commit under test:
9d341d1b46f16dbfbb41af75dd6d4966808dfa5d ("round-99: C1 repair — SKILL.md tool registry
completion (26 rows)"). Rows read from the extracted tree's SKILL.md lines 1700-1738
(`## Round 99 — tool registry completion`). All runs offline; all runs executed from a scratch
extraction, never from the lane working tree.

## Method

- Extraction: `git -C LANE archive 9d341d1b46f16dbfbb41af75dd6d4966808dfa5d | tar -x -C
  /fast/scratch/hyaku/kake-r99/ExecRegProbe/tree` (read-only git in LANE; archive of the repair
  commit, not master tip `7f5b1b7b`).
- Frozen digests (`controls/instrument-sha256.txt`, 11 entries) verified sha256-identical at
  2345e309640adac6c36e41eca87409085ba3a276, at freeze ab35eacebf922f4f598237590f0220d63111dc94,
  and at master — all `OK`, no mismatch, no repair license invoked. `sources/rfc9111.txt` sha256
  = `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` as frozen.
- Per row (26): run the Self-test cell command as written (18 rows have one; 8 declare
  `no self-test`); probe the Verdict map with (a) no arguments, (b) unknown flag `--zz-bogus`,
  and for the 4 stdin tools (cache_key.py, conditional_eval.py, reval_exchange.py,
  stale_extensions.py) (c) `{}` and (d) `not json` on stdin. 78 probes total.
- Network guard: fetch modes not run. live_snapshot.py/source_snapshot.py have `required=True`
  args so their no-arg path dies at the parser (observed 64 and 2, both in map).
  response_snapshot.py wires `--population`/`--out` defaults (POPULATION_DEFAULT/OUT_DEFAULT,
  response_snapshot.py:81-82,224-225), so its no-arg path IS the fetch mode: that probe was
  skipped and recorded `skipped-fetchmode` rather than executed. Its `--zz-bogus` probe is
  parser-only and returned the mapped 64 (response_snapshot.py:226-229 translates argparse
  SystemExit to 64).
- Environment: every run got `TMPDIR=/fast/scratch/hyaku/kake-r99/ExecRegProbe/tmp/tmp2`;
  `--tmpdir`/`--work` passed explicitly where the row's Write scope cell names one. Python
  3.14.8, node v24.21.0 (probe-delta.mjs). No tools installed; no host mutation; no mutating
  git/jj anywhere.

## Self-test results (18 cells run, 18 exit 0)

row | rc | observed last line vs cell claim
---|---|---
base_path_selftest.py | 0 | `45/45 fixtures passed` — cell claims 45/45: match
citing_set.py | 0 | delegates to citing_set_selftest.py, JSON `verdict` clean
citing_set_selftest.py | 0 | JSON clean (with explicit `--tmpdir` per cell's optional flag)
citing_set_hostile_selftest.py | 0 | hostile specs refused as expected (`--root . --tmpdir <scratch>`)
conditional_eval.py | 0 | `selftest 99/99` — cell claims 99/99: match
header_change_class.py | 0 | `selftest: 6/6 passed` — cell claims 6/6: match
knowledge_metatext_lint.py | 0 | `selftest 13/13` — cell claims 13/13: match
landed_check.py | 0 | `selftest 14/14` — cell claims 14/14: match
ledger_latest_check.py | 0 | `selftest: 2/2 passed` — cell claims 2/2: match
link_preview_selftest.py | 0 | `"cases": 46, "passed": 46, "passedOverTotal": "46/46", "verdict": "clean"` (full JSON re-captured in lp-receipt.json) — cell claims 46/46: match
quote_class.py | 0 | `selftest 4/4` — cell claims 4/4: match
robots_audit.py | 0 | delegates: `"passed": 204, "passedOverTotal": "204/204"` (same binary run as row below)
robots_audit_selftest.py | 0 | `"cases": 204, "failed": 0` — cell claims no tally, coverage minimums met: consistent
sidecar_reobserve.py | 0 | `sidecar_reobserve tests=10 failures=0 errors=0 passed=true` (`--selftest --work <scratch>`)
sitemap_audit_selftest.py | 0 | `PASS 271/271` — cell claims PASS 271/271: match
source_recheck_hardening_selftest.py | 0 | `"cases": 10, "passedOverTotal": "10/10", "verdict": "clean"` — cell claims 10/10: match
source_recheck_selftest.py | 0 | `"cases": 106, "passedOverTotal": "106/106"` — cell claims 106/106: match
stale_extensions.py | 0 | `selftest cases=113 passed=113 failed=0`

## Probe results — verdict-map consistency

Full table: probe.tsv (78 lines, `row/probe/rc/consistent?`). 77 executed probes produced
integer rcs; every observed rc is inside its row's Verdict map (`yes` in the TSV). Zero
observed rcs fell outside a map, so under the frozen rule ("contradicted when an observed rc
is neither in its map nor explained by argparse's usage exit 2"):

**contradictions = 0.**

Representative in-map probes: the four stdin tools refuse empty/invalid input with rc 1 and
`invalid_input:` on stderr exactly as their maps claim; custom-parser tools report usage as 64
(citing_set.py, header_change_class.py, landed_check.py, live_snapshot.py, robots_audit.py,
sitemap_audit_selftest.py, probe-delta.mjs unknown flag); argparse-3.14 raw usage exit 2 lands
only where 2 is also a mapped code (see O2/O3).

## Observations (routed, not repaired — none is a frozen-rule contradiction)

- O1 `citing_set_selftest.py` silently ignores unknown flags: `--zz-bogus` runs the full
  selftest and exits 0. 0 is in the map, so consistent per rule; but unlike its siblings it
  performs no usage rejection. Usage-hygiene observation for reviewers.
- O2 Argparse exit 2 conflates with semantic 2s in maps that use 2 for non-usage meanings
  (robots_audit_selftest.py "setup fault", sidecar_reobserve.py "refused or error",
  link_preview_selftest.py "setup fault", base_path_selftest.py "setup/input fault"): the
  bogus-flag rc 2 is in-map, so no contradiction, but the map cannot distinguish argparse usage
  from the semantic fault by code alone.
- O3 Tools without argparse SystemExit translation emit raw rc 2 on missing args while their
  maps advertise `64` usage: source_snapshot.py, wave_seat_record.py, quote_class.py (their
  no-arg rc 2 is in-map under "bad input"/"unreadable input", hence no frozen-rule
  contradiction). Contrast live_snapshot.py:198 / response_snapshot.py:226-229 which translate
  SystemExit → 64. Cosmetic claim-reachability nuance for reviewers; exit-code claims remain
  in-map in every observed case.
- O4 response_snapshot.py's no-arg path is its fetch mode (defaults wired to a population dir
  and an output dir under the lane root resolved from the script location). Untested offline by
  design; recorded as `skipped-fetchmode`.

## Write-scope audit

- All 26 tools ran with cwd = scratch extraction; TMPDIR redirected to scratch; explicit
  `--tmpdir`/`--work` wherever a row's Write scope cell names one. No file was created in the
  LANE working tree by my runs: `find LANE -newer <window>` (window 2026-11-05 20:10 → check
  time, covering the whole battery) shows only `.git`/`.jj` internals, round-99 wave
  orchestration files (`w1-spec.json`, `w1-dispatch.json`, `w1.ready*`), pre-freeze `controls/`
  receipts, and other seats' `w1/` outputs — nothing attributable to this seat's probes. One
  earlier find invocation errored (`-newer` stamp file did not exist yet, os error 2) and was
  re-run with `-newermt`; the error run itself wrote nothing.
- Declared transient write outside seat scratch: running row 4's Self-test cell exactly as
  written (`python3 -B scripts/citing_set.py --selftest`, no forwarded `--tmpdir`) delegates to
  scripts/citing_set_selftest.py whose parser defaults to `DEFAULT_TMPDIR =
  "/fast/scratch/hyaku/kake-r27"` (citing_set_selftest.py:158,824-825): it creates a private
  `citing-set-selftest-<rand>` dir there, runs the cases with it as the child TMPDIR, and
  removes it afterwards (:831 `shutil.rmtree`). Post-battery observation: r27 exists, is empty
  (nlink 2, size 6) — zero residue; the directory is the row's declared Write scope ("the
  selftest writes case copies under the runner's tmpdir") and is shared with concurrent seats
  running the same cells (its mtime moved during the wave window; individual touches are not
  attributable to one seat). No LANE file was touched by this path.

## Receipts

- probe.tsv — 78 probe lines with rc and consistency verdict (this dir).
- results.json — machine-readable rc + last-line + stdout/stderr tails for every probe (this dir).
- lp-receipt.json — full stdout of the bare link_preview selftest run (46/46 evidence).
- Scratch seat dir /fast/scratch/hyaku/kake-r99/ExecRegProbe/ deleted before yield; the lane tip
  was read (`rev-parse master` → 7f5b1b7b8dbfdae74dfe6d487bbf5406c478b916) read-only; no
  mutating git/jj command was run anywhere.

## Verdict

C1 repair rows' exit-code claims survived the offline falsification battery: 26/26 rows
probed, 18/18 self-test cells exit 0 with tallies matching their cells, 0 contradictions, 0
scope escapes. Findings above are observations for the reviewer conjunct, not repairs.

REGPROBE rows=26 selftests_ok=18 contradictions=0 scope_escapes=0
