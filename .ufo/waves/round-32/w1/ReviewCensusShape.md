# ReviewCensusShape — census and registry shape after S062 (r32 wave 1)

Seat: KakeR32.ReviewCensusShape (reviewer, axis: freshness). Leaf, no subagents.
Scope: SOURCES.md registry shape at base a0b0dff vs tip 285abca; validate + row count.

## Required commands

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` (reads the live working copy, now at 7e05aa8, one commit past tip):
```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```
exit 0. No error codes.

`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show <r>:corpus/SOURCES.md | grep -c '^| S0'`:
- a0b0dffcd95b2215f638a5ff7591dd4fde325d27 rows=61 (exit 0)
- 285abcad632e3c1c57bb402232e7d218054db383 rows=62 (exit 0)

## Extra checks (sandbox clone at /fast/scratch/hyaku/kake-r32/w1/ReviewCensusShape/clone)

`validate --file` and `census --file` on the checked-out registry at each rev:
- a0b0dff: `W04 S033` (pre-existing, same warning as tip) + `ok`, exit 0. rows 61, tier.A 52 / B 1 / C 8, mined 48 / queued 6 / rejected 7.
- 285abca: `W04 S033` + `ok`, exit 0. rows 62, tier.A 53 / B 1 / C 8, mined 49 / queued 6 / rejected 7.
- 2f2f12d (build rev where the after-receipts were taken): `W04 S033` AND `E09 S062 recheck=on ds4cc-marketplace render.yaml or Dockerfile change`, exit 1.

`git diff 2f2f12d 285abca -- corpus/SOURCES.md`: exactly 2 changed lines (one `-`/`+` pair) — the S062 row's recheck cell changed `on ds4cc-marketplace render.yaml or Dockerfile change` → `90d`. No other cell touched.
`diff` of extracted SOURCES.md base vs tip (sandbox copies): exactly 1 inserted line, the S062 row at line 70 inside `## Registry`, before `## Paths`.
`git log --oneline 285abca..7e05aa8 -- corpus/SOURCES.md scripts/citing_set_hostile_selftest.py scripts/fixtures`: empty — the newer commit touches lesson/QUALITY/SCORECARD/spec files only, not the registry.

## Findings

1. No new warning or error at tip: the only output line is W04 on S033, identical at base a0b0dff. S062 row itself is shape-clean: 11 cells (NF=13, no E01), unique id (no E03), unique URL+scope (no E04), valid kind `code`, tier `A`, status `mined`, opened `2026-10-22`, recheck `90d` (no E09), used-by `corpus/knowledge/render-web-services.md` present on disk (no E11).
2. Timing observation, advisory only: at build rev 2f2f12d (where c2-after receipt was taken) the registry itself failed validation with E09 — S062 was committed with a free-text recheck `on ds4cc-marketplace render.yaml or Dockerfile change`. Lane tip 285abca is the fix ("S062 recheck 90d (census E09 fix)", verified above). The declared-claims receipts at 2f2f12d were captured while the registry was invalid; the fix lands the correct shape. No residual defect at tip.
3. Delta is exactly +1 row and +1 tier.A mined (61→62, tier.A 52→53, mined 48→49). No status/tier churn of other rows.

## Not verified
- Byte-identity of the retained blobs vs `~/Projects/ds4cc-marketplace` (C2 substance — other seats).
- Fleet-wide multi-lane census (scoped to kake per assignment).
- Live URL fetch (owned-site bound: not attempted).

## Tooling
No installs or updates. Used existing bash/git/gawk; sandbox only: /fast/scratch/hyaku/kake-r32/w1/ReviewCensusShape/ (clone/, SOURCES-base.md, SOURCES-tip.md, s062-*.txt, tmp/).
