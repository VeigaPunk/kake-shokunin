# DraftSkillTable — scoped findings (kake round 29, wave 1)

Seat: scribe, leaf. Axes: operability, freshness. No product code, judge,
commit or network fetch performed.

## What I built

Draft of the SKILL.md decision table "Project-site base-path triage — round 29",
in my sandbox only:

`/fast/scratch/hyaku/kake-r29/w1/DraftSkillTable/SKILL-round29-base-path-table.md`

It contains (a) the proposed SKILL.md section text, (b) a row-by-row citation
map with the supporting retained-text quote for every cited id, (c) the tool
contract the check column assumes, copied from the frozen matrix `interface`
field, and (d) an explicit limits list.

## Shape I matched

`SKILL.md` round-28 section is `## Field performance triage — round 28` with a
`Knowledge: corpus/knowledge/field-performance-cwv.md (S036–S039)` line, then
one table (`| Situation | kake does |`) and a second gate-registry table. The
round-28 section sits at `SKILL.md:680-697` (last section of the file). My
draft proposes the same shape: a `Knowledge:` line naming
`corpus/knowledge/pages-base-path.md (S040–S043)`, then a single decision
table with columns Symptom | Check | Remedy | Cited ids. The task asked for
symptom/check/remedy with cited ids, so I used a fourth column rather than
round 28's two-column `Situation | kake does` shape; the L1 may fold the
cited ids into the remedy cell to keep round-28 width.

## The six rows and their cited ids

| # | Symptom | Cited ids |
|---|---|---|
| R1 | Asset 404s only on the project site; same file loads from a local root server | S040, S041, S042, S043 |
| R2 | Links jump to the owner root `https://<owner>.github.io/…` | S040, S042, S043, S041 |
| R3 | Correct on custom domain, broken at the `github.io` project URL (or reverse) | S040, S041, S043, S042 |
| R4 | A `base` element in the head rewrites relative references | S040, S024, S043 |
| R5 | Local preview green, deployed project site broken | S040, S041, S043 |
| R6 | Audit returns exit 2 `could-not-evaluate` or exit 64 | S040, S043 |

Every row cites at least one of S040–S043. R4 additionally cites S024
(WHATWG base element, already a mined registry row at `corpus/SOURCES.md:32`,
opened 2026-10-20) because none of S040–S043 says which `base` element wins;
the frozen matrix `interface` field names S024 for exactly that rule. Flagging
it so the L1 can decide whether a round-29 entry may lean on a round-22 row.

## Commands run and observed outcomes

- `read /home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md` — read; round-28
  decision table at lines 680-697 (raw).
- `grep -n "S040|S043" .../corpus/SOURCES.md` — S040–S043 have no registry row
  yet at drafting time; S024 present at `corpus/SOURCES.md:32`.
- `ls -la .../scripts/base_path_audit.py` — exit 2, "No such file or directory".
  The C2 tool is not in the lane yet, so the check column cites the frozen
  matrix contract, not a run I performed.
- Python substring check of every quote in the draft against
  `.ufo/waves/round-29/sources/S040.txt`–`S043.txt` (whitespace-collapsed, the
  same normalization the C1 counter uses) — exit 0, 13/13 quotes are exact
  substrings, 0 misses, longest quote 22 words (S041). The 13 quotes are
  listed verbatim in the draft's citation-map table: 2 from S040, 4 from
  S041, 2 from S042, 5 from S043.
- Python read of `.ufo/waves/round-29/c2-matrix.json` — exit 0. Case mix
  7 control / 14 defect / 8 input / 1 usage = 30; defect reason is uniformly
  `outside_base_path`; input reasons are `input_invalid` and
  `page_outside_base_path`; exit map 0 clean, 1 failed-policy, 2
  could-not-evaluate, 64 usage.

## Evidence pointers

- Draft file: `/fast/scratch/hyaku/kake-r29/w1/DraftSkillTable/SKILL-round29-base-path-table.md`
- Round-28 shape: `SKILL.md:680-697`
- Tool contract: `.ufo/waves/round-29/c2-matrix.json` field `interface`
  (invocation, manifest v1, exit map, reference list, S024 base rule)
- Retained sources: `.ufo/waves/round-29/sources/S040.txt`–`S043.txt`,
  digests in `receipts.json`
- S024 registry row: `corpus/SOURCES.md:32`

## Out of scope / not done

- No live property was probed; no owned web property was fetched.
- `scripts/base_path_audit.py` was never run — it does not exist in the lane
  yet. The check column is written against the frozen interface and must be
  re-checked against the landed script by the L1.
- No SKILL.md, corpus or SOURCES.md file in the lane was modified; the only
  file I wrote in the lane is this report.

## Limits the draft states on purpose

The four sources do not settle how GitHub serves `/<repo>` without a final
slash, whether Pages paths are case-sensitive, or whether Pages sets a Jekyll
`baseurl` automatically. The draft says nothing on those three. It also does
not claim the audit proves deployment correctness — it audits built HTML.

## Tooling

No install was performed or needed; every check used python3 stdlib and
read-only shell. Host-wide pacman transactions remain paused; nothing was
installed.
