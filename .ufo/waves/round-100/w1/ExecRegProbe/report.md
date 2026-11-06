# ExecRegProbe — independent re-measurement of C1 at repair commit e84a1871

Method: `git -C LANE archive e84a1871 | tar -x -C <scratch>/tree` (observed rc 0). No use of `c100_registry.py` code paths; counting re-implemented from the seat spec and the frozen counter's *definition* in `freeze.md`/counter docstring (one current registry row per committed `scripts/` tool; verdict map naming the unknown-flag exit). Frozen digests verified before attacking: `sha256sum -c controls/instrument-sha256.txt` → all `OK` (observed rc 0).

## (2) Row counts — every tool invoked by exactly one registry row
- Tools: 55 committed direct children of `scripts/` (`*.py`, `*.mjs`) at e84a1871.
- Registry rows outside fences (` ``` ` fences and HTML comments excluded, registry tables identified by required header `Name|Kind|Entry command|Verdict map|Self-test|Write scope|Owner`): 146.
- Invocation semantics: Entry-command cell's backtick spans, pipe-split, strip `VAR=` prefixes and `python3/node` + flags → first word `scripts/<tool>` (this matches the seat's parenthetical; a naive "any mention of `scripts/<tool>` in the cell" over-counts the `c89 key capability` row which mentions `scripts/cache_key.py` only as `--candidate` argument — initial naive count reported `cache_key.py=2` (rows 1617, 1707), corrected count 1).
- Result: 55 tools, `not_one_row` tools = **0** (every tool invoked by exactly 1 row; no tool with ≠1). Observed via independent Python (`probe4.py`), reproduced.

## (3) Sandboxed probes of the seven repaired tools (bwrap --unshare-net, no network fetch run)
All runs: `bwrap --unshare-net --ro-bind / / --proc /proc --tmpfs /tmp ... -- <cmd>` (bubblewrap 0.13.1, observed present, rc of bwrap itself 0 for every invocation). Each kept row's verdict map codes vs observed:

| tool | noargs | bogus `--zz-bogus-r100` | stdin `{}` | stdin `not json` | verdict codes | bogus in map? |
|---|---|---|---|---|---|---|
| cache_key.py | 1 | 1 | 1 | 1 | 0,1 | yes |
| cache_key_conformance.py | 2 | 2 | 2 | 2 | 0,1,2 | yes |
| live_snapshot.py | 64 | 64 | 64 | 64 | 0,1,2,64 | yes |
| response_snapshot.py | 2 | 64 | 2 | 2 | 0,1,2,64 | yes |
| robots_audit.py | 64 | 64 | 64 | 64 | 0,1,2,64 | yes |
| source_snapshot.py | 2 | 2 | 2 | 2 | 0,1,2 | yes |
| x_robots_tag_audit.py | 64 | 64 | 64 | 64 | 0,1,2,64 | yes |

- `probe_contradictions` (bogus rc ∉ verdict codes) = **0**. Full rc + last-line receipts in `probe.tsv` (28 rows).
- Notes: `cache_key.py` ignores argv (always reads stdin; bogus rc=1 = invalid-JSON on empty stdin, in map). `response_snapshot.py` noargs rc=2 is `capture leaf already exists ...` (default out dir already populated in the archived tree) — in map (2). `source_snapshot.py` argparse rc=2 (in map 0,1,2). `cache_key_conformance.py` rc=2 missing `--candidate` (in map). Kept-row Self-test cells run: only `robots_audit.py` and `x_robots_tag_audit.py` have runnable self-test spans among the seven (`robots_audit_selftest.py` rc 0, `204/204`; `x_robots_tag_audit.py --selftest` rc 0, `selftest: 33/33 passed`); other five kept rows read `no self-test` and their tools contain no `--selftest` (observed by grep). `selftest_fail` = **0**.

## (4) Fenced history block — verbatim
Each base line `git show 3989618d:SKILL.md | sed -n '<n>p'` compared byte-identically to the fenced block at repair `SKILL.md` lines 1758–1770 (`## Round 100 — superseded registry rows` fence): 494→1758, 1079→1760, 1104→1762, 1370→1764, 1505→1766, 1621→1768, 1624→1770 — all 7 **verbatim** (`history_verbatim=7/7`).

## (5) Diff scope
- `git diff 69cdc1eb..e84a1871 --stat` → `SKILL.md | 32 ++++---, 1 file changed, 25 insertions(+), 7 deletions(-)` (repair commit alone).
- `git diff 3989618d..e84a1871 -- SKILL.md` shows exactly 7 removed table-row lines (494, 1079, 1104, 1370, 1505, 1621, 1624) plus the 25-line history-block addition. Base→repair full diff is 54 files (instruments/controls/frozen/sources added between base `3989618d` and freeze `69cdc1eb`, pre-dating the repair); within the repair commit, `other_changes` beyond SKILL.md's 7 removals = **0**.

## Totals
tools=55, not_one_row=0, probe_contradictions=0, selftest_fail=0, history_verbatim=7/7, other_changes=0.

Evidence: `w1/ExecRegProbe/probe.tsv` (28 probe rows + selftest/history/diff/counts receipts), this report. Scratch scripts retained only in `/fast/scratch/hyaku/kake-r100/ExecRegProbe/` (probe4.py/run2.py) — copied numbers above; scratch removal on yield per spec is owned by the seat cleanup step below. No tool installs (pacman untouched; no uv/npx used). No network fetch modes run.

REGPROBE tools=55 not_one_row=0 probe_contradictions=0 selftest_fail=0 history_verbatim=7/7 other_changes=0
