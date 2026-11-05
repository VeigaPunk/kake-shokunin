VERDICT: registry rows and frontier section are in place in the working tree (uncommitted; L1 lands). Item B (C1 registry conjunct) closes on my row, but it also closes on a bare prose line (F1, routed). C2 is not yet measurable: the tool does not exist at HEAD.

# ScribeRegistry — round-92 registry and frontier (kake)

Base HEAD read: `f0b2dc635e34cc1c593655d926af74f19bd21034`. Freeze `a5640ca02c20f94a0fa03af41b977b46ae99808e`. Nothing committed or staged in LANE; the only git mutations were inside a scratch clone.

## Delivered

| Item | Where | State |
|---|---|---|
| SKILL.md section + three registry rows (`c92_defects.py`, `c92_heuristic.py`, `heuristic_freshness.py`) | `SKILL.md` lines 1649–1680 (after the round-91 section) | in place, uncommitted |
| corpus/README.md `## Round-92 frontier step — heuristic freshness` | `corpus/README.md` line 736 to EOF | in place, uncommitted |
| corpus/README.md frontier ground-map row (extra; same as round 91's map row) | `corpus/README.md` line 136 | in place, uncommitted |
| capability row, frontier line, notes | `.ufo/waves/round-92/w1/ScribeRegistry/{capability-row.md,frontier-line.md,Notes.md}` | written |
| receipts | `.ufo/waves/round-92/w1/ScribeRegistry/receipts/` (sha256 in `sha256.txt`) | written |

SCORECARD.md, LOG.md, corpus/SOURCES.md, PROVINCE.md and every frozen file were not touched.

## Commands and exit codes (receipts in `receipts/`)

| Command | Exit | Reading | Receipt |
|---|---|---|---|
| `python3 -B .ufo/waves/round-92/c92_defects.py --selftest` | 0 | `selftest 12/12` | `receipts/selftest.txt` |
| `c92_defects.py --root <clone> --revision c5b0db82 --skip-battery --skip-replay` (SKILL.md with my rows) | 1 | `open=1 closed=1`; B closed (`B_rows=2`); open set `{A}`, expected: no mutation receipt at that commit | `receipts/itemB-registry-row.txt` |
| same, FC simulation (all counter-naming lines stripped, commit 0cae8c6c) | 1 | `open=2`; B open (`B_rows=0`) | `receipts/itemB-FC-simulation.txt` |
| same, prose-only (table rows removed, one prose line kept, commit e02479c9) | 1 | `open=1`; B closed (`B_rows=1`) | `receipts/itemB-prose-only.txt` |
| `python3 -B .ufo/waves/round-92/c92_heuristic.py --root . --revision HEAD --work <scratch>` | 1 | `candidate=absent … met=false` (no tool at HEAD; base as frozen) | `receipts/c2-at-HEAD.txt` |
| reference population, seed 92 (python import of the frozen counter's functions, read-only) | 0 | 28 hand cases; 120 generated; decisions explicit 65, heuristic 21, heuristic-undecided 17, not-heuristically-cacheable 10, not-storable 7; 0 generation refusals | `receipts/population.txt` |
| grep of edits, `stored_reuse.py` clause-11 site, `git status --porcelain -- SKILL.md corpus/README.md` | 0 | the edits are present; `M` on the two files only | `receipts/edits-grep.txt` |

Item B's FC simulation is consistent with the frozen battery's expectation (`{"B"}`) for the no-row case. The frozen battery was not run; my runs used `--skip-battery`, and the battery needs a receipt-bearing revision to be meaningful.

## Findings

**F1 — item B accepts a prose line (counter defect, routed to the K91-2 closure review).** `c92_defects.py` item B (lines 150–160 of the frozen counter) passes when any line of `SKILL.md` contains `c92_defects.py`, `--revision` and `met`. It does not check for a table row. My "How to verify" paragraph satisfied it alone (`receipts/itemB-prose-only.txt`). The frozen battery's FC fixture still refuses, because it strips every counter-naming line. So the defect is the weaker "row" conjunct, not a broken fixture. Frozen; not repaired. Round-92 lesson should carry it.

**F2 — the `heuristic_freshness.py` row cannot be paste-verified yet.** The file is absent at HEAD. The row's command (`printf … | python3 -B scripts/heuristic_freshness.py`) and its selftest (`--selftest` → `selftest <n>/<n>`) must be re-run at the L1's landing revision. Until then the row is a claim about a file that is not in the commit.

**F3 — dangling citations until the L1 lands.** README and SKILL cite S470 and `corpus/knowledge/heuristic-freshness.md`. ScribeEntry-11 confirms the knowledge entry is on disk (414 lines, sha256 `6c43aef0…f86f97`), and its draft row is at `w1/ScribeEntry/sources-row.md` (validated against a scratch copy, census exit 0, one advisory W04 for the shared RFC URL). S470 is not yet in `corpus/SOURCES.md`; the L1 appends it.

**F4 — wording corrected in place.** My first intro sentence called the round-91 counter "repaired as an instrument". Corrected to: C1 is a new frozen instrument that measures K91-1/2/4/5; it does not repair the round-91 counter.

**F5 — C2 anti-table is a designed substring screen.** `c92_heuristic.py` refuses a candidate that contains any hand-case input digest (16-hex prefix) or any forgery stem. A legitimate candidate that quotes a stem in prose is refused. Recorded in the row's limits paragraph, not a defect.

## Limits

- I verified the registry conjuncts by running the frozen counter on scratch revisions. I did not run the frozen battery or the replay; they need a receipt-bearing revision, which does not exist yet.
- The SKILL.md rows describe contract conformance, not the RFC, and not any deployed cache. The rows and README say so.
- I did not verify the knowledge entry's quotes; SentinelQuote owns that.
- The RFC body I referenced is only the retained copy `L1/src/rfc9111.txt` (sha256 `aeb52adb…5302cf3e`, equal to the frozen hash). I made no live GET.

## Tooling

No tool installed or upgraded. Read `RULES.md` was not needed for this seat's work; no pacman, no uv or npm install.

## Handoff to the L1

1. Apply `w1/ScribeRegistry/capability-row.md` to SCORECARD.md (the Demonstrated repertoire round-92 section and the claim pair).
2. Append S470 from `w1/ScribeEntry/sources-row.md` to `corpus/SOURCES.md`.
3. After `scripts/heuristic_freshness.py` lands, re-run its `--selftest` and the frozen C2 counter at the landing revision, then check the SKILL.md row's `selftest <n>/<n>` wording against the actual output.
4. Route F1 into the round-92 lesson's Routed list.
