# ScribeAdmin — round 70, W1 (attempt 1)

Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`; base `e5f6fd9e4c243d092160bc74e8bea24256087173`; frozen contract `.ufo/waves/round-70/contract.md` (commit `908b20b00f7479a61596e93e05104d1cd0054349`, blob `c2c47ac80b32940386c158c81c08f8667016bcd2`); Amendment 0 seat-shape note commit `d76ae92656bc24bc935d28201267a5d8b293de5a`. Draft-only seat: prose here, no repo file written except this report, no tracked file edited, no tool installed, no pacman, no campaign tool run, `shokuknow` untouched.

## Pointer calibration draft
The L1 appends this section at the end of `SCORECARD.md` (append-only; earlier rows are never edited):
```markdown
## Pointer calibration (round 70)

Append-only calibration ledger for this file's path-like evidence pointers that do not resolve at the measured base revision `e5f6fd9e4c243d092160bc74e8bea24256087173`; a pointer counts as annotated only when its exact token is the first cell of a row below. Counter: `.ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <rev>` — predicate `unannotated=0`, exit 0. The L1 fills the real dated rows after the base run.

| Pointer | Status | Dated event | Note |
|---|---|---|---|
| /tmp/kake-r10 | EXAMPLE | scratch-discipline cleanup | EXAMPLE row — exact-token format only; the L1 replaces the Dated event and Note cells with the real dated record before landing. |
| ~/DIRMAP.md | EXAMPLE | 2026-10-12 W7 prune | EXAMPLE row — exact-token format only; the L1 replaces the Dated event and Note cells with the real dated record before landing. |
```
The first cell is the bare token and nothing else — that is the string the counter matches; `EXAMPLE` sits in the Status cell, never in the Pointer cell. Rows for the remaining dangling pointers are the L1's to add after the base run; this draft does not enumerate them.

## LOG skeleton
Append at the end of `LOG.md` (round-69 entry style: bold lead-in per bullet):
```markdown
## Round 70 — 2026-11-03 (hyaku run 15; attempt 1; Linux host; claims frozen before data)

- **Frozen contract.** `.ufo/waves/round-70/contract.md` committed `908b20b00f7479a61596e93e05104d1cd0054349` before any seat ran; Amendment 0 (`.ufo/waves/round-70/amendment-0-note.md`, seat shape only, no predicate change) committed `d76ae92656bc24bc935d28201267a5d8b293de5a`. Base `e5f6fd9e4c243d092160bc74e8bea24256087173`.
- **Motivating evidence.** <what made C1 and C2 worth a round, with pointers>.
- **Landed at `<T1>`:** <files landed, with the counter, the calibration section, the lesson, the QUALITY addendum, the entry and the registry row>.
- **Measured.** C1: base <before> → tip <after> (`<receipt path>`). C2: base <before> → tip <after> (`<receipt path>`).
- **Attacks at the landed tip.** <seat: attack and verdict, one per attack>.
- **Sources & frontier.** <registry before → after, id and class>; census exit 0 at base and at tip.
- **Assimilation verdict.** <what was or was not admitted from the staged entry, and why>.
- **Not done this round.** <explicit non-claims>.
```

## Lesson skeleton
New file `corpus/lessons/round-70.md` (round-69 lesson shape; the L1 lands it):
```markdown
# Round 70 — lessons (kake, attempt 1)

Base `e5f6fd9e4c243d092160bc74e8bea24256087173`. Frozen contract `.ufo/waves/round-70/contract.md` (commit `908b20b00f7479a61596e93e05104d1cd0054349`). Two claims: C1 calibration (2 → 2, HOLD), C2 freshness (10 → 10, HOLD). Wave: W1, one v1 wave of 14 seats (4 attack seats, ~28.6 %).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| M1 — self-assessment drift: the scorecard's own evidence pointers name scratch paths and host-tree paths that no round ever annotated | `.ufo/waves/round-70/contract.md` §Frontier step (M1); `SCORECARD.md` move-log rows 10–18 at base `e5f6fd9e` | none — the corpus append-only rules never covered `SCORECARD.md`, and the freshness sweep scans corpus files, not `SCORECARD.md` | the C1 counter `.ufo/waves/round-70/c70_pointer_audit.py` + the `## Pointer calibration (round 70)` section of `SCORECARD.md` + a QUALITY criterion (round-70 addendum, `corpus/QUALITY.md`) |

## Corrections

(None yet — the L1 appends correction rows after the base run; earlier rows are never edited.)

## Gate

(Empty stub: the assimilation set is adjudicated in the ScribeEntries gate draft, `.ufo/waves/round-70/w1/ScribeEntries.md` §Gate draft; the L1 gates on the critic/reviewer evidence, not on this stub.)
```

## SHONEN lines
Assessment lines for the lane's four `SHONEN.md` boxes (lines 5–8 of the committed file; the file itself stays unchanged, no `[x]`):

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:57` (audit → source-fix → publish checklist), `SKILL.md:208` (owned freshness gate registry), `SKILL.md:332` (cited paths); author-side reading, no non-author verifier.
- [~] At least one end-to-end domain task executed and logged in LOG.md — the round-70 LOG entry (this round; section to be appended by the L1 at the tip), with the entry and registry row it lands.
- [ ] Instructions executable by an agent without oral context — residual procedure paths in `SKILL.md:95`, `SKILL.md:356`, `SKILL.md:359` and the corpus citation debt carried in `corpus/lessons/round-69.md` §Known residuals.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md:3` (domain line unchanged at base) and `PROVINCE.md:24` (CrUX / field-performance frontier the round-70 entry sits under).

## Findings (for the canonical judge; conflicts quoted)

1. **Contract vs committed bytes (Frontier M1 count).** The contract's Frontier step says the SCORECARD names "12 `/tmp/kake-rNN` tokens, rounds 10–18". The base bytes hold **9 unique** tokens (`/tmp/kake-r10` … `/tmp/kake-r18`) in **11 occurrences** (rows 89–101 one each, plus two more `r17` at lines 4461 and 4478). The correction rows must cover what the counter enumerates, not 12.
2. **Population census at base** (contract's three regexes over `git show e5f6fd9e:SCORECARD.md`): repo 552 occurrences / 333 distinct / 8 dangling; home 19 / 6 / 3; tmp 11 / 9 / 8 — **19 distinct dangling** at base, matching ScoutPointers' 19.
3. **Load-bearing coupling.** The calibration section's preamble names the counter path `.ufo/waves/round-70/c70_pointer_audit.py`, which is itself a repo-class population token. It must exist at the measured revision (counter and section land together), else `unannotated=0` is unreachable.
4. **The section is inside its own population.** Any path-like token written in the section (prose, Note cells) becomes a population member needing its own first-cell row; the preamble and rows above are kept free of such tokens.
5. **EXAMPLE rows must be replaced before landing**, not merely annotated: a left-in EXAMPLE row credits one dangling pointer without naming a dated record, failing the annotation content duty at review.

## Verification exercised

- `git show e5f6fd9e:SCORECARD.md | wc -l` → 4727; `| sha256sum` → `e11f211840de2ea483e82179a194454c2b2a1a1eda92313dbd0695794330b902`; `git rev-parse e5f6fd9e:SCORECARD.md` → `1ac34091f170d50849c52911aac21996378d2853`.
- `git show e5f6fd9e:SCORECARD.md | grep -c 'Pointer calibration'` → `0`, exit 1 (no annotation section at base).
- `git show e5f6fd9e:LOG.md | grep -n '^## Round 69'` → `2408`; `git show e5f6fd9e:SHONEN.md | cat -n` → four unchecked boxes at lines 5–8.
- Python census with the contract's regexes over the base bytes → per-class counts in Finding 2, exit 0; `git cat-file -e e5f6fd9e:<path>` per repo token (8 dangling); `test -e` per home and tmp token (3 and 8 dangling) — the `..`-form token exits 128 while its normalized path resolves.
- No tools installed; no pacman; scratch tree `/fast/scratch/hyaku/kake-r70/ScribeAdmin/` removed (`rm -rf`, verified absent).

- Artifact: this report only (`.ufo/waves/round-70/w1/ScribeAdmin.md`); no seat artifact directory was needed. Out of scope and untouched: all tracked lane files, the `LOG.md`/`SCORECARD.md`/`SHONEN.md` bodies, `corpus/`, other lanes, the fleet root, `.scratch/`, `.ufo/state/`, `shokuknow`, any campaign tool, any publish or deploy action.
