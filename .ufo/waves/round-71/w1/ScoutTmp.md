# ScoutTmp — Round 71 w1 (kake lane)

- Seat: ScoutTmp (role: scout, leaf member, read-only on lane)
- Base revision: `cc6b4e0b8c35e72dfb02c6184b847f68c1262153`
- File analyzed: `SKILL.md` (committed bytes via `git show`)

## Per-line inventory (/tmp/ tokens in SKILL.md at base)

| Line | Token | Classification | Has phrase | `test -e` | Repo tree | C2 Repair Action |
|---|---|---|---|---|---|---|
| 27 | `/tmp/kake-r12/live/` | Citation of past receipt (r12 log) | No | exit 1 | Absent | Annotate (dated absence + phrase) |
| 95 | `/tmp/probe-latest.backup.json` | Runnable recipe (`cp` backup) | No | exit 1 | Absent | Repoint to mktemp (no `/tmp`) |
| 227 | `/tmp/kake-r12/live/` | Citation of past receipt (r12 sha) | No | exit 1 | Absent | Annotate (dated absence + phrase) |
| 356 | `/tmp/kake-r11/` | Citation of past receipt (r11 art) | No | exit 1 | Absent | Annotate (dated absence + phrase) |
| 359 | `/tmp/kake-r12/live/` | Citation of past receipt (r12 sha) | No | exit 1 | Absent | Annotate (dated absence + phrase) |
| 463 | `/tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md` | Citation of past receipt (r23 c41) | No | exit 1 | Absent | Annotate (dated absence + phrase) |
| 464 | `/tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md` | Citation of past receipt (r23 c42) | No | exit 1 | Absent | Annotate (dated absence + phrase) |

## Confirmation of C2 Repair Rule
- Line 95 is the sole runnable recipe in the population: repoint to `$(mktemp -d)` (or mktemp scratch path) with no `/tmp/` token.
- The remaining six lines (27, 227, 356, 359, 463, 464) are historical citations/annotations; under the QUALITY absence-annotation rule they require recording the dated absence (`test -e` exit 1) and the phrase `historical record, not an executable instruction`.
- Table integrity: Lines 27 and 227 reside in markdown tables; neither table may be split across rows.

## Exercised verification
1. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc6b4e0b8c35e72dfb02c6184b847f68c1262153:SKILL.md | grep -n "/tmp/"` -> 7 lines (27, 95, 227, 356, 359, 463, 464), exit 0.
2. `test -e` for all 7 tokens on host -> all return exit 1 (all absent).
3. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree -r cc6b4e0b8c35e72dfb02c6184b847f68c1262153 --name-only` -> 0 matches for any token path, exit 1.
4. `grep -F "not an executable instruction"` across the 7 lines -> 0 matches, exit 1.
5. `python3 -B .ufo/waves/round-71/c71_tmp.py --lane /home/vgpnk/Projects/shokunin/kake-shokunin --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153` -> exit 1, `unannotated_tokens=7`.

## Attacks and verdicts
- Attack 1: Are any lines among {27, 227, 356, 359, 463, 464} runnable recipes? Verdict: Refuted. All 6 cite past round verification artifacts. Line 95 is the only recipe.
- Attack 2: Does any base line already carry `not an executable instruction`? Verdict: Refuted. None carries the phrase at base.
- Attack 3: Does any token exist on this host? Verdict: Refuted. All exit 1 on `test -e`.
- Attack 4: Does any token resolve to a committed file in the base repo tree? Verdict: Refuted. All are absent from base tree.

## Tooling authorization
No tools installed or updated. No scratch directory retained.
