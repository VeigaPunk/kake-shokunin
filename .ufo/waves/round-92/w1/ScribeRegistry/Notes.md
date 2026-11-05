# ScribeRegistry — working notes (round 92)

Seat: ScribeRegistry (scribe, leaf). Lane: kake-shokunin. Base HEAD read: f0b2dc63.
Freeze: a5640ca0. No commit, stage or mutating git in LANE. Scratch clone only.

## What I changed in LANE (uncommitted working-tree edits; L1 lands them)

1. `SKILL.md`
   - New section `## Round 92 — heuristic freshness decision and the round-91 instrument repairs`
     appended at EOF (after the round-91 section). Three table rows in the house
     eight-column form: `c92_defects.py`, `c92_heuristic.py`, `heuristic_freshness.py`.
     Plus a "How to verify" paragraph and a two-limits paragraph, as in round 91.
2. `corpus/README.md`
   - One new row in the Frontier ground map table (line 136), after the round-91 row.
     Not strictly in the instruction (the instruction named only the section), but
     round 91 added a map row the same way (`corpus/README.md` gains the r91 map row),
     so this is house form. Disclosed here.
   - `## Round-92 frontier step — heuristic freshness` appended at EOF, in the
     round-91 section's shape: what moved, from where to where, S470, frontier line.

## Draft artifacts (my directory only)

- `capability-row.md` — SCORECARD `Demonstrated repertoire — round 92` row, a
  move-log pair and a claim-table pair, in round 91's shape. Honest-limit bullets.
- `frontier-line.md` — three forms: the README line (already in place), a
  SCORECARD "Planned — after round 92" paragraph, and a PROVINCE.md tail proposal
  (PROVINCE is outside my scope and I did not write it), plus an open-items table.
- `receipts/` — the executed evidence (sha256 manifest in `receipts/sha256.txt`).

## Verification I actually ran

- `c92_defects.py --selftest` → `selftest 12/12`, exit 0.
- Item B on my SKILL.md (scratch clone, commit c5b0db82): `B_rows=2`, B closed,
  open set `{A}` (A is expected: no mutation receipt at that commit).
- Item B on FC simulation (every counter-naming line stripped): `B_rows=0`, B open.
  Matches the frozen battery's FC expectation `{"B"}` at the level of item B.
- Item B on a prose-only line (table rows removed, one prose line kept): B CLOSED.
  See finding F1 below.
- `c92_heuristic.py` at HEAD: `candidate=absent … met=false`, exit 1 (base as
  frozen; expected, no candidate yet).
- Reference population at seed 92: 28 hand cases, 120 generated, decision counts
  explicit 65 / heuristic 21 / heuristic-undecided 17 / not-heuristically-cacheable 10
  / not-storable 7; refusals during generation: 0.
- `scripts/stored_reuse.py` `heuristic-undecided`: line 224 (`if lifetime is None`,
  clause 11), so the README sentence that it reports `heuristic-undecided` when no
  explicit freshness lifetime is present is correct as written.

## Findings (lane-internal)

- **F1 (routed to K91-2 closure review, a counter defect).** `c92_defects.py` item B
  accepts ANY line of `SKILL.md` that contains `c92_defects.py`, `--revision` and
  `met`. It does not require a table row. The prose "How to verify" line I wrote
  satisfies it by itself. The frozen FC fixture only strips lines naming the
  counter, so it still catches the no-line case. The defect is a weaker-than-intended
  "registry row" conjunct. Routed; not repaired (frozen).
- **F2 (instrument coupling, not a defect).** The registry row for
  `heuristic_freshness.py` cites `scripts/heuristic_freshness.py` and its `--selftest`
  before the file exists. The row cannot be paste-verified until ExecHeuristic
  lands the tool with a `--selftest` that prints `selftest K/K`. The row says `<n>/<n>`
  as a placeholder format. Must be re-checked at the L1's landing revision.
- **F3 (dangling citations until L1 lands).** README and SKILL cite
  `corpus/knowledge/heuristic-freshness.md` and S470. Neither exists on disk nor in
  `corpus/SOURCES.md` at HEAD. ScribeEntry-11 confirmed S470 by IRC. Landing order:
  the L1 appends S470 and the knowledge entry, then re-runs the sources census.
- **F4 (wording, fixed).** My first draft of the SKILL.md intro said the round-91
  counter was "repaired as an instrument". It is not: C1 is a new frozen counter. Fixed
  to "a new frozen instrument that measures the four routed round-91 defects; it does
  not repair the round-91 counter". Line 1658-1659.
- **F5 (C2 counter, observed on read; not run as a finding).** The C2 counter's
  `anti_table` conjunct checks the 28 hand-case input digests by a 16-hex-prefix
  substring over the candidate source. A candidate that embeds those digests is
  refused. Noted as designed; it is recorded in the row's limits paragraph.

## Scope notes

- I did not edit `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`, `PROVINCE.md` or any
  frozen file.
- I did not fetch any URL. The RFC body I quoted from is only the lane's retained
  copy (`L1/src/rfc9111.txt`, sha256 aeb52adb…); ScribeEntry-11 owns the live GET.
- No tool was installed or upgraded.
