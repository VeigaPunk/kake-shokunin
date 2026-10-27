# ExecC1BaseAudit

Claim C1 base re-derivation, independent of the counter: `SCORECARD.md` axis table (lines 15–19) at
`fd6303ce5c14b3f892dec586297a942ab6e4193b`. Method: hand list of every path-like token per evidence cell plus my own
regex (backticked span → token if it has a `/` segment or a known extension; bare absolute/home paths outside spans),
each checked with `git cat-file -e <rev>:<path>` and `ls` in the lane worktree; each `A/B` tally grepped in the row's
cited committed blobs. The counter was NOT imported for the derivation; I ran the committed v1 (extracted from contract
commit `45a92b6`) only to confirm the receipt reproduces. Read-only git; fixture clone in scratch; no lane/Git/jj mutation.

## TOKENS

**operability** — 5 path pointers, 4 unresolved:

| token | cat-file -e at rev | ls (host) | ruling |
|---|---|---|---|
| `cli.mjs:935` | ABSENT | absent | unresolved. `cli.mjs` is in no lane commit (`git log --all -- '*cli.mjs'` empty); the real file is `src/cli.mjs` of the external webzites tree (cmdProbe handoff:8,14,20) |
| `:836-839` | line continuation of `cli.mjs` | n/a | unresolved |
| `:932` | line continuation of `cli.mjs` | n/a | unresolved |
| `:393` | line continuation of `cli.mjs` | n/a | unresolved |
| `corpus/handoffs/cmdProbe-merge-fix.md` | blob | file (4382 B) | resolved |

Not paths: `status --json`, `grokbots --check`, `bots list`, `bots report`, `probe <id> --all` (commands), `--stale` (flag),
and the prose compounds `probe/status/reconcile/sync-check`, `before/after`, `corrupt/deleted`, `free-read/writer`.

**freshness** — 10 pointers by the counter's rule, 12 on a strict hand rule:

| token | cat-file -e at rev | ls (host) | ruling |
|---|---|---|---|
| `corpus/claims` | ABSENT | absent | unresolved; never in any lane commit (`git log --all --diff-filter=AD -- corpus/claims/**` empty) |
| `corpus/knowledge/freshness-sweep.md` | blob, has `## r17 run` (line 110) | file | resolved |
| `corpus/lessons/round-17.md` | blob | file | resolved |
| `LOG.md` | blob, r17 entry line 311, tallies 331–332 | file (186354 B) | resolved |
| `/tmp/kake-r17/{scout-claims.md,claims-delta.tsv,critic.md,reviewer-cites.md,scout-pins.md,scout-live.md}` | absolute, brace-expanded to 6 | `/tmp/kake-r17` absent | 6 × unresolved |
| `~/projects` (hand) | not committed bytes | absent | non-committed (r17 world change) |
| `~/Projects` (hand) | not committed bytes | dir | non-committed |

Not paths: `pathsMissSet`, `projectsChildrenSet`, `pathsFiles`, `plazir-live-source-gap` (identifiers), `--selftest` (flag).

**calibration** — 0 path tokens. The cell is prose only ("each note pointer/blob/kind"); `pointer/blob/kind` is not a path.

## TALLIES

**operability** — no `A/B` tally in the cell. Its counts are `31-file`, `5 violated+1 error`, `20 keepers`,
`checked=21`, `35 rows`, `2 independent L2 re-runs`. Grepped the only committed blob it cites
(`corpus/handoffs/cmdProbe-merge-fix.md`): `5 violated` 2 hits (lines 17, 44 — cmdProbe snapshot context);
`31-file`, `35 rows`, `20 keepers`, `checked=21`, `keeper`, `lucario`, `scribe`, `push-gate`, `836`, `932`, `935` → 0 hits.

**freshness** — 4 tallies; hits per cited blob at the revision:

| tally | freshness-sweep.md | round-17.md | LOG.md |
|---|---|---|---|
| `117/117` | 0 | 0 | 1 (r17 entry, line 331) |
| `15/15` | 0 | 0 | 6 (r17 at 331; others are other rounds) |
| `16/16` | 0 | 0 | 5 (r17 at 332) |
| `10/10` | 1 (`Selftest 10/10`, §r17) | 2 | 7 |

All four are "found" only because `LOG.md` is cited; the two corpus files named first carry none of the inventory
tallies. The cell's non-`A/B` numbers also check: `66 targets / 49 resolve / 10 declaredAbsent / 0 drift / 39 files` =
freshness-sweep §r17 (line 113); `160 claims` = 117+15+7+21 (LOG.md:226, 331–332); `missSet 9→10`; `33-file` sha set;
`36` children — all present in the cited blobs.

**calibration** — no `A/B` tally; states 19 events / 19 re-derived / 0 undisclosed. Committed receipts corroborate:
`round-58/controls/base-c1-receipt-rewrites-v2.txt` (`events=19 undisclosed=19`), `after-c1-receipt-rewrites.txt`
(`events=19 undisclosed=0 new_receipts=2`), `round-58/receipt-rewrites.json` (`events` list = 19). The cell names no path.

## AGREEMENT

- The committed v1 counter at the base revision reproduces `controls/base-c1-axis-evidence.txt` body-identically
  (only my wrapper `argv:`/`EXIT_CODE=` lines differ).
- Counts agree exactly: `unresolved=11` (operability 4 + freshness 7), `rows_no_receipt=3`, `receipts_off_axis=0`,
  `tallies_unfound=0`, `rows_no_tally=2`, `rows=3`, `scores_held=2`, `superseded_kept=0` → `mismatches=16`, exit 1.
- All 11 unresolved tokens are genuinely non-committed at the revision — I found no false accusation among them.
- 16 decomposes as 4 (`cli.mjs` family) + 1 (`corpus/claims`) + 6 (one `/tmp` brace group) + 3 (no receipt cited)
  + 2 (operability and calibration have no `A/B` tally).
- `rows_no_receipt=3` is right: no axis cell cites any `.ufo/waves/round-N/` blob at base.
- `superseded_kept=0` is right: the base cells are the table cells, so they cannot also appear outside the table.

## DISAGREEMENTS

1. **`corpus/claims` is counted — fair by the letter, not by intent.** Facts: absent at the revision and never present
   in any lane commit (so no commit can make it resolve). The cell names it as a *finding*: "9 new deltas found and
   resolved/qualified (… dangling `corpus/claims` …)", and LOG.md:336 says "nonexistent `corpus/claims` cite". The
   frozen after-state ("every axis cell names only committed paths") makes the count formally correct; semantically the
   counter equates a quoted defect with an evidence pointer. Remedy is rewording, not re-pointing — and the base cell
   survives verbatim outside the table under `superseded_kept`, so the history is not lost.
2. **The counter is inconsistent about the same class: backticked home paths are invisible.** Probe on a fixture clone
   with the committed v1: adding backticked `~/nonexistent-probe` and `~/Projects/multi/segment` to the freshness cell
   produced **0 new pointers**; only an unbackticked `/tmp/...` was flagged. Cause: `PATHISH` needs a second `/`
   segment (`~/x` never matches) and `BARE` both requires a `/tmp|~|/home` prefix and a lookbehind a preceding backtick
   defeats (backtick spans are stripped anyway). Consequence: the base freshness cell's `~/projects` (host absent) and
   `~/Projects` are two non-committed paths the counter never counts. Strict hand count → `unresolved=13`,
   `mismatches=18`, not 16. Same probe: an unbackticked *relative* path (`corpus/ghost-path-zzz.md`) also yields 0 new
   pointers under v1.
3. **One missing file is counted four times.** `cli.mjs:935` fails, so `last_file` resets and each bare
   `:836-839`/`:932`/`:393` becomes its own "line pointer with no preceding resolved file". Distinct root causes behind
   the 16: `cli.mjs` absent, `corpus/claims` dangling, `/tmp/kake-r17` gone, no receipt cited, no `A/B` tally in 2 rows
   — five, not sixteen.
4. **`rows_no_tally` penalizes grammar, not absence of evidence.** Operability states six counts, calibration three;
   neither uses `A/B`, and the tally regex is `\d+/\d+` (no spaces). The round-58 calibration row in the same file also
   uses `undisclosed=19, phantom=0 …`, so the calibration axis's house style systematically fails this test.
5. **Tally "found" is a substring-anywhere test.** 3 of 4 freshness tallies live only in `LOG.md`; `15/15` (6 hits) and
   `16/16` (5 hits) also occur in unrelated rounds there. At base the r17 context does exist (LOG.md:331–332), so the
   claim holds — but the check would also pass on coincidence alone.
6. **The operability cell's one committed citation does not carry the cell's numbers.** `cmdProbe-merge-fix.md` holds
   only `5 violated` of the six counts and none of the four line pins. Under the predicate this is invisible (no `A/B`
   tally → only `rows_no_tally`). After-state note: cite the blob that holds the numbers, or state none.
7. **Counter drift observed mid-wave (not mine).** `.ufo/waves/round-59/c59_axis_evidence.py` is modified in the lane
   working tree (+88/−28, mtime 2026-10-26T22:50:41-0300) and behaves differently: the version present at that mtime
   had a predicate including `tables == 1`, and on an unbackticked-path probe yielded
   `mismatches=22 tallies_unfound=4 rows_no_tally=3` where committed v1 yields `15 / 0 / 2`. All numbers here are the
   committed v1 at `45a92b6`.
8. **Build-side constraint, measured by probe.** Citing `.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` in an
   axis cell moves `rows_no_receipt` 3→2 but raises `receipts_off_axis` 0→1: base SCORECARD (and HEAD) has no
   `## Round 59` section, so a round-59 blob cannot be on-axis. Round-58 receipts are on-axis today (the Round 58
   section has rows naming calibration, operability and freshness), e.g. `after-c1-receipt-rewrites.txt`,
   `after-c2-resolver-cases.txt`, `after-c3-quote-truth.txt`.

No tools installed or upgraded (none needed). Scratch `/fast/scratch/hyaku/kake-r59/ExecC1BaseAudit` deleted after the
receipt extracts above were taken.

VERDICT: Base C1 re-derived independently and agrees with the frozen control at 16 mismatches (11 unresolved, 3 no-receipt, 2 no-tally); the count is arithmetically right but over-counts one missing file 4×, ignores backticked home paths, and 5 distinct root causes carry all 16.
