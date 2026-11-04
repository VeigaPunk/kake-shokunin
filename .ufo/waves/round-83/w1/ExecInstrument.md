# ExecInstrument — round 83 wave w1

Seat scope: C1/D3 **state conjunct** only — produce the missing `instrument_receipts.py --check`
receipt at `.ufo/waves/round-83/controls/after-c83-instrument-check.txt`. The D3 **row** conjunct
(a line in `corpus/lessons/round-83.md`) is not mine and was not touched.

## Commands and exit codes

All run with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`; streams captured under
`/fast/scratch/hyaku/kake-r83/ExecInstrument/raw/` then copied to `w1/ExecInstrument/`.

| # | Command | Exit |
|---|---|---|
| 1 | `python3 -B scripts/instrument_receipts.py --check` (run 1) | 0 |
| 2 | same command (run 2, determinism) | 0 |
| 3 | `python3 -B scripts/instrument_receipts.py --check --json` | 0 |
| 4 | `git rev-parse HEAD` / `git rev-parse master` | 0 / 0 |
| 5 | `git status --porcelain` at the run instant | 0 |
| 6 | `diff <(git cat-file -p HEAD:corpus/knowledge/instrument-receipts.json) corpus/knowledge/instrument-receipts.json` | 0 (identical) |
| 7 | `git merge-base --is-ancestor 70c8241b57ceec1a8bf6e4aba7ed6ecdd1c31235 HEAD` | 0 (ancestor) |
| 8 | `python3 -B .ufo/waves/round-83/c83_defect_queue.py --root . --fleet /home/vgpnk/Projects/shokunin` | 1 (other items still open) |
| 9 | `... c83_defect_queue.py --root . --revision 64b71992… --work <scratch>/exportwork --fleet …` | 1 |
| 10 | independent D3-parse replication (same regex as the counter) | 0 |

Run 1 and run 2 stdout are byte-identical (`diff -q` clean, 17 lines, 1185 bytes) and stderr is
empty in both (0 bytes) — the measured line is deterministic.

## Re-derived binding (step 3)

From `--check --json` at revision `64b7199281e5457df0e08652977f698c4f34f46e`:

- `population_size` = **30**, `bound` = **30**, `mismatches` = **0**, `missing_frozen` = **[]**,
  `met` = **true**, `findings` = `[]`, `malformed` = `[]`, `outside` = `[]`.
- population composition: 16 frozen + 14 beyond-frozen (round-75/79/80/82 counters and 7 scripts,
  including `scripts/instrument_receipts.py` itself).
- receipt: `receipt_source=committed`, `receipt_worktree=identical`,
  `receipt_revision=70c8241b57ceec1a8bf6e4aba7ed6ecdd1c31235`, `receipt_revision_valid=true`,
  `revision_match=false`. The mismatch is the documented subject-vs-carrier case: the receipt pins
  subject revision 70c8241b, which is an ancestor of the measured carrier, so `met` does not depend on
  equality.

Exact line emitted (copied verbatim into the receipt):

    C2v1 revision=64b7199281e5457df0e08652977f698c4f34f46e population=30 bound=30 mismatches=0 met=true

## Receipt written

`.ufo/waves/round-83/controls/after-c83-instrument-check.txt`, 27 lines, 1824 bytes, sha256
`b5316d08f9cb07b10bd8108808182fd10dfd49c279e6c2284aff40639869b8b5`, trailing newline present.
Contents: the command line, the one exact `C2v1` line, the two run summary lines
(`population:` derived/frozen/missing_frozen/beyond_frozen; `receipt:` source/worktree/declared/
declared_match/declared_valid), `findings: none` with the JSON field list, the 14 beyond-frozen
paths, the measured-revision and ancestor note, the uncommitted-worktree note, determinism note,
`stderr: empty`, and `exit=0`. Only one line starts with `C2v1 `, so the counter's first-match scan
cannot lock onto a secondary line.

Independent replication of the counter's D3 parse (`startswith("C2v1 ")` + `\b[0-9a-f]{40}\b`, then
`(\w+)=(\S+)`): candidate lines = 1, `bound=30`, `population=30`, `mismatches=0`, `met=true`,
`revision` 40-hex → ok = True.

## Which revision the line names, and worktree state at that instant

The line names `64b7199281e5457df0e08652977f698c4f34f46e` — the lane `master` tip and the detached
`HEAD` at the run instant (both `git rev-parse` calls printed the same 40-hex). The declared
revision `70c8241b…` (round-82 scorecard commit) was verified an ancestor of it.

At that instant `git status --porcelain` showed **no tracked modification**: two untracked paths
(`.ufo/waves/round-83/w1.ready`, `.ufo/waves/round-83/w1.ready.partial`) and a sibling seat
directory (`.ufo/waves/round-83/w1/ScoutSources/`). The committed receipt blob at HEAD and the
worktree receipt blob were byte-identical (diff exit 0). So `source=committed`,
`worktree=identical` are literal, not assumed. No new untracked file of mine existed yet at run
time: the receipt I then wrote is new state.

## Caveats / risks (named, not hidden)

1. **Row conjunct still missing.** `corpus/lessons/round-83.md` does not exist, so the frozen
   counter prints `D3 open … log=no`. D3 closes only when that lesson carries one line containing
   `D3`, `after-c83-instrument-check.txt` and `--check` (the matcher needs `\bD3\b` and both tokens
   on the same line). That file is another seat's write scope; I did not create or edit it.
2. **Commit is required.** `--revision` mode reads committed bytes only. I measured that directly:
   `c83_defect_queue.py --root . --revision 64b71992… --work <scratch>/exportwork` printed
   `D3 open after-c83-instrument-check.txt absent`, exit 1. My receipt is untracked until the L1
   commits it; only the worktree-mode run is green.
3. **Population drift at the integration commit.** The receipt pins the 30-member population at
   `64b71992`. Population is derived from live `### Round <N> gate registry additions` rows in
   `SKILL.md` (no Round 83 section existed at HEAD). If the integration commit (a) adds a live
   Round 83 row naming a new instrument (e.g. `killers/run_killers.py`) or (b) changes any pinned
   population blob (the receipt pins sha256 and byte length for all 30, including
   `scripts/instrument_receipts.py`), `--check` at that carrier reads `mismatches ≥ 1` and
   `met=false`. Mitigation for the L1, in order:
   `python3 -B scripts/instrument_receipts.py --root . --revision <integration-tip> --write --date 2026-11-04`,
   commit `corpus/knowledge/instrument-receipts.json`, then
   `python3 -B scripts/instrument_receipts.py --root . --check` at the follow-up carrier. My green
   line must not be cited for a population it did not measure.
4. No tool install or upgrade was performed (nothing was needed); no network call was made; all
   scratch lived under `/fast/scratch/hyaku/kake-r83/ExecInstrument/` and was removed after the
   receipts were copied here.

## Verdict

**D3 state conjunct GREEN** at revision `64b7199281e5457df0e08652977f698c4f34f46e`:
`population=30 bound=30 mismatches=0 met=true`, exit 0, deterministic across two runs, receipt file
written with exactly one conforming `C2v1` line. D3 as a whole remains **open** on two non-mine
items: the L1 commit of the untracked receipt (verified necessary by the `--revision` run) and the
lesson row anchor owned by another seat (`log=no`).
