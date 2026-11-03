# ExecRepairC2 — round 71, kake lane, w1 (attempt 1)

Seat: executor (C2 repair). Base: `cc6b4e0b8c35e72dfb02c6184b847f68c1262153`.
Read first: `contract.md` (freeze 04557e17) and `amendment-1.md`. No lane-tree mutation.

## Change (scratch clone only)

Scratch clone: `/fast/scratch/hyaku/kake-r71/ExecRepairC2/clone` (checked out at base,
`git rev-parse --show-toplevel` = that dir). Commit `652356421e2899689bb4724b01301da53e5c1ed9`
(`git -c user.name=kake-seat -c user.email=seat@fixture commit`).
Diff: 7 insertions, 7 deletions, SKILL.md only; 1396 → 1396 lines. No other line changed.

- Line 95 (runnable recipe): `/tmp/probe-latest.backup.json` → `$(mktemp -d)/probe-latest.backup.json`;
  surrounding text kept; no `/tmp` token left on the line.
- Lines 27, 227, 356, 359, 463, 464: base text kept verbatim, appended
  `[r71 absence: <token> absent on 2026-11-03 (test -e exit 1); historical record, not an executable instruction]`
  with tokens: 27/227/359 `/tmp/kake-r12/live/`; 356 `/tmp/kake-r11/`;
  463/464 `/tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md`.

## Commands and exit codes (exercised)

`test -e <token>` for all four distinct paths on 2026-11-03 → exit 1 each
(`/tmp/kake-r12/live/`, `/tmp/kake-r11/`, `/tmp/kake-r23-SurfacePlazir15Kimi-bnbU/SKILL-base.md`,
`/tmp/probe-latest.backup.json`).

`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-71/c71_tmp.py --lane /fast/scratch/hyaku/kake-r71/ExecRepairC2/clone --revision 652356421e2899689bb4724b01301da53e5c1ed9`
→ `C2 revision=65235642... tokens_total=12 unannotated_tokens=0 unannotated_lines=[] removed=7 added=7 guard=ok met=True`, exit 0.

Same counter, `--revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153`
→ `tokens_total=7 unannotated_tokens=7 unannotated_lines=[27, 95, 227, 356, 359, 463, 464] removed=0 added=0 guard=ok met=False`, exit 1.
Matches the contract's base receipt (`controls/c2-base.txt`).

Artifact: `.ufo/waves/round-71/w1/ExecRepairC2/SKILL.repair.diff` (55 lines), saved via
`git diff cc6b4e0… 65235642… -- SKILL.md` (exit 0);
sha256 `c964f08c03f7c409c4d80b0e7e8ff1e6e09113f33f339aa30c01fecebcbaa8cd`.

Extra checks: `git -C $S/clone apply --check -R <diff>` → exit 0 (diff reproduces the tip from the
working tree); `git -C <lane> diff --quiet cc6b4e0… -- SKILL.md` → exit 0 (lane SKILL.md untouched
vs base); `git -C $S/clone status --porcelain` → empty after commit.

## Attacks / controls

No attack seats assigned to this seat. Only the base control (red, exit 1) and the target
(green, exit 0) were exercised; no counter edit was made, so the C2 kill rule was not touched.

## Risks / notes

- Tip `tokens_total=12` because each annotation repeats its token; every occurrence sits on a line
  carrying `not an executable instruction`, so `unannotated_tokens=0`.
- Contract wording keeps line 95 at a bare `$(mktemp -d)/…` path: each shell expansion yields a
  fresh directory, so the "run → cp back" prose needs an explicit variable if run literally. This
  follows the contract text and does not affect the counter.
- Table rows 27/227 keep their closing `|`; annotations are appended after it (no table split).

## Tooling

No installs or upgrades. Scratch tree deleted after the measurements above.
