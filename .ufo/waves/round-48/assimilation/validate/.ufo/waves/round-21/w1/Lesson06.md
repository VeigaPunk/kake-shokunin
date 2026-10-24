# Lesson06 — round-18 historical Gate (round-21 wave 1)

Seat: `KakeR21.Lesson06` (scribe, leaf). Target: `corpus/lessons/round-18.md` only.

## Behavior

- Target had no `## Gate` heading. Appended a retrospective `## Gate` section at EOF. Labelled as a round-21 reconstruction, not the original admission.
- No other file was edited. No commit. No subagent dispatched. No tool installed or upgraded.

## File change (exact)

| Field | Before | After |
|---|---|---|
| Lines | 64 | 100 |
| Bytes | 3783 | 10644 |
| sha256 | `9285af3a0ff175c8ce64c33617c198c7f05cc29242b5fef84e3e395d2fa8506c` | prefix of 3783 bytes still `9285af3a…8506c` (every prior byte preserved) |
| Read tag | `6A4C` | `D73D` |

Appended range: lines 65-100 (blank line 65, `## Gate` at line 66). `grep -c '^## Gate$'` = 1. `git status`: `M corpus/lessons/round-18.md` only.

## Gate contents (what the appended section records)

- Label: "Retrospective round-21 reconstruction, not original admission"; no live state re-verified, no check re-run, no `/tmp/kake-r18/` artifact opened.
- Original sections cited with line ranges: `## The catch` (7-19), `## What the instrument proved…` (21-35), `## Repairs (this commit)` (37-52), `## Carried debt` (53-61), final state (63-64).
- Round-21 lesson: `corpus/lessons/round-21.md` is **absent** at read time (lessons dir lists round-1..round-20). Cited the round-21 contract `.ufo/waves/round-21/wave1-spec.json` instead.
- S019 contract: quoted from the round-21 spec; located canonical text at `~/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` (18-20, 112-115, 162-165) and `LEARNING.md` (42-46, 71-73). No S019 row exists in `corpus/SOURCES.md` at read time; none cited, none added (L1 owns SOURCES).
- Candidates C1-C9 with outcomes: admitted with qualification / admitted as finding / unverified / carried. Basis is the round-18 lesson, `LOG.md` round-18 entry (starts line 400), and later on-disk references (round-19-recensus.md, round-20.md).
- Rejected candidates: **not recorded** (none documented in round-18 lesson or LOG).
- Outside spot-check: **not recorded** for round 18. Round-19 `## Independent audit erratum` / `Audit detail` / `Dead-path sweep` (round-19-recensus.md 42-60) touch round-18 marker coverage but are not a spot-check of round-18 admit/reject decisions; not counted as agree/disagree.
- Gate completeness: no admit/reject row for C1-C9; no outside spot-check; 22-file (lesson) vs 21-file (LOG item 2) count unreconciled; `keeper-timer-inert.md:91` and `publish-queue.md:167` unmarked per round-19, no repair recorded.

## Findings

1. The round-18 record has no gate section and no recorded admit/reject ledger. The reconstruction does not supply one.
2. Round-18 repairs were later partly superseded: §history suspend semantics narrowed and selftest made hermetic in round 19 (`round-19-recensus.md` Landed change, 6-18).
3. Completeness gap: round-19 found two present-tense `origin-work` cites unmarked (`keeper-timer-inert.md:91`, `publish-queue.md:167`). Round-18's "63 cite lines" repair does not cover them, and no repair is recorded.
4. Count discrepancy: round-18 lesson says 63 lines across 22 files; LOG says 21 corpus md errata files plus SCORECARD and LOG. Not reconciled (reconciliation needs a live count, out of scope).

## Out-of-scope items (not touched)

- `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md` — owned by L1 or other seats.
- `corpus/lessons/round-21.md` — absent; not created by this seat.
- No S019 row added; registration is L1's.
- Other lessons, knowledge entries, and `/tmp/kake-r18/` artifacts — not read or changed.

## Limitations

- No live-state re-verification by design; the round-18 figures are cited as recorded, not measured.
- Credential/auth files and `~/.omp/agent/agent.db*` not read. `omp` CLI not launched.
- Build/lint/tests not run (assignment: main agent verifies once). Byte-preservation check above is the only post-edit verification run.

## Checks for the main agent

- `grep -c '^## Gate$' corpus/lessons/round-18.md` → 1
- `head -c 3783 corpus/lessons/round-18.md | sha256sum` → `9285af3a…8506c`
- `wc -l corpus/lessons/round-18.md` → 100
