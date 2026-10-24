# MutC2CounterControl — mutation probe of the round-30 C2 counter

Seat: leaf (no subagents dispatched). Axis: freshness. Milestone: r30-build.
Scope: `.ufo/waves/round-30/c2_quote_truth.py` only. The lane was never mutated
by this probe; every build ran in a sandbox clone.

## What I attacked

The C2 counter (lane path `.ufo/waves/round-30/c2_quote_truth.py`, sha256
`a2cd3164f67e221f0d38609afd50be61260902f963f05f96bd1b223451975e7a`) claims it
rejects a Render source row not backed by a true quote in the retained text. I
built a synthetic corpus that passes 4/4 in a clone, changed one point at a
time, and watched the counter; later I repeated the probe against the real
`corpus/knowledge/render-static-sites.md` a sibling seat had landed. Method:
clone the lane into `/fast/scratch/hyaku/kake-r30/w1/MutC2CounterControl/clone`
at base `4580c78cca1185d059efa6970722bbcf2f9c1b0f`, one commit per scenario,
counter run from the unmodified lane file (byte-identical copy, sha256 verified
equal before and after every batch). Batches 4 to 6 used a second sandbox copy
`real/`, a snapshot of the live lane worktree.

## Commands run (observed exit codes)
```
cd /fast/scratch/hyaku/kake-r30/w1/MutC2CounterControl
TMPDIR=$PWD/tmp python3 -B run_probe{,2,3,4,5,6}.py   # each exit 0
#   -> results.jsonl .. results6.jsonl
python3 -B c2_quote_truth.py --root $PWD/clone --revision <rev>   # per scenario
```

## Mutant ledger, synthetic corpus (observed output)
| id | mutation | rev | exit | passed | failed id | verdict |
|---|---|---|---|---|---|---|
| S0 | pristine lane base, no corpus | 4580c78c | 1 | 0/4 | all | reference, matches c2-before receipt |
| S1 | synthetic corpus, all four true quotes | f82bc173 | 0 | 4/4 | none | baseline true positive |
| M1 | S049 gate quote absent from retained text | 24dafb9b | 1 | 3/4 | S049 | rejected |
| M2 | S050.txt byte-edited, receipts sha left stale | a0dae578 | 1 | 3/4 | S050 | rejected |
| M3 | S051 registry row status `queued` | 5bb4b5d5 | 1 | 3/4 | S051 | rejected |
| M4 | S052 cited only in the entry header | be32a2a1 | 1 | 3/4 | S052 | rejected |
| M5 | S049 text also holds the one-letter flip variant | 4c8aba05 | 1 | 4/4 | none | control fires, `controlBroken=true` |
| N1 | counter minus sha256 comparison, M2 corpus | 6ad529fc | 0 | 4/4 | none | sha check load-bearing |
| N2 | counter minus status/opened/url test, M3 corpus | 36114514 | 0 | 4/4 | none | check a load-bearing |
| N3 | counter accepting header citations, M4 corpus | 5e045113 | 0 | 4/4 | none | check b load-bearing |
| N4 | counter minus substring test, M1 corpus | 810d26b6 | 0 | 4/4 | none | substring test load-bearing |
| N5 | S051 quote truncated but still an exact substring | d9b4bd17 | 0 | 4/4 | none | survived |
| N6 | variant differing at a letter other than the first | 9a999191 | 0 | 4/4 | none | survived |
| N7 | S049 gate line placed under `## Notes` | 062a691e | 1 | 3/4 | S049 | rejected |
| N8 | S050 gate line duplicated | ca74fc63 | 1 | 3/4 | S050 | rejected |

Failing check per rejected case: M1 fails `d_quote_in_retained_text`; M2 fails
the same check (sha_ok false); M3 fails `a_row`; M4 fails `b_entry_body_cites`;
N7 and N8 fail `c_gate_quote` and `d_quote_in_retained_text`. Every rejected
case exits 1 and names the failed id. N1 to N4 remove one check from the
counter itself and each then accepts the matching fabrication, so all four
checks are load-bearing. The one-letter flip control behaves as documented: it
fires when the flipped quote sits in the retained text (M5: `controlBroken=true`,
exit 1 even at 4/4) and stays silent otherwise (S1, N5, N6). The flipped form
used in M5 was `qtatic sites are fast and free to deploy.`, the first
alphabetic character replaced per `flip_letter`.

## Mutant ledger, real landed corpus
| id | mutation | exit | passed | verdict |
|---|---|---|---|---|
| R0 | real worktree snapshot, no `corpus/lessons/round-30.md` | 1 | 0/4 | rejected; `c_gate_quote` false for all four |
| R5 | lesson gate built from usable entry-attributed quotes | 0 | 4/4 | passes |
| T1 | S049 gate quote = full attributed sentence with its period | 0 | 4/4 | passes |
| T2 | same sentence, trailing period removed | 0 | 4/4 | passes, indistinguishable from T1 |
| T3 | S050 quote drops `or URL` from the real sentence | 0 | 4/4 | passes, the changed meaning is invisible |
| T4 | S051 gate quote = `Pricing`, a navigation word | 0 | 4/4 | passes, a non-substantive quote |

R0 is the actionable one: at lane HEAD `04637bdd` the real entry and the four
registry rows are in place, but `corpus/lessons/round-30.md` does not exist, so
the counter reads 0/4 with `a_row` and `b_entry_body_cites` true and
`c_gate_quote` false for every id. The counter needs one lesson file with a
`## Gate` section holding one `- <id> — “quote”` line per id. R5 shows the
counter reaches 4/4 on the real corpus once such a file exists, using only
quotes the entry already attributes correctly. I audited every attributed quote
against the two Gate constraints (1 to 25 words, exact substring of its own
retained text) in `entry_quote_audit.json`: 56 of 57 satisfy both. The single
exception is the S051 sentence at entry line 49, 30 words long, over the
25-word ceiling, so it cannot serve as a Gate quote. The other S051 quotes
are usable.

## Surviving mutants (coverage findings, not contract changes)
- **T2 and T3, semantic fidelity is not checked.** The counter verifies that a
  quote is an exact substring of the retained text, so a quote that drops a
  limiting clause still passes. T3 turned the real S050 sentence `The browser
  can't detect that content was served from a different path or URL.` into
  `...from a different path`, a still-exact substring that no longer says the
  same thing. **T4, a navigation string passes**: `Pricing` is in the site
  navigation of every retained page, so it satisfies both checks while carrying
  no claim. **N5** shows the same gap on a synthetic corpus, where truncating
  `Matches /tokens.css and /mode.css , but not /assets/theme.css` to `Matches
  /tokens.css and /mode.css` passes 4/4.
- **N6, the flip control samples one character position.** `flip_letter`
  replaces the first alphabetic character only, so a variant differing at any
  later letter is not detected. Inherent to a one-letter control, the
  documented limit rather than a defect.
- `b_entry_body_cites` accepts the id as a bare word anywhere in the body, so a
  negated or table-only mention would count as a citation.
- Freshness note: the counter hardcodes `cells[8] == "2026-10-22"` and the id
  list S049-S052. Re-opening these sources later, or adding ids, needs a
  counter edit rather than a rerun.

T2, T3 and T4 match the limits the L1 already disclosed in SCORECARD at
`04637bdd` ("a navigation string or a one-word quote would also pass"; "the
closure should read the entry body and match each quote to the sentence that
relies on it"). My probe gives that disclosure an executable form: the missing
check is sentence-level containment, not substring containment.

## Restoration and lane integrity
- Sandbox clone reset to `4580c78cca1185d059efa6970722bbcf2f9c1b0f`, clean
  worktree, after the last batch; the mutated counter copy
  `c2_quote_truth_mut.py` was overwritten by a fresh copy of the lane file.
- Lane counter sha256 after the probe:
  `a2cd3164f67e221f0d38609afd50be61260902f963f05f96bd1b223451975e7a`, unchanged,
  and identical at the newer lane HEAD `04637bdd`. Lane retained text shas
  unchanged: S049 `3604f8f5…6f7`, S050 `1c413643…52c5ed`, S051 `e98982ce…a27d`,
  S052 `6c1616f8…f769`; receipts.json `39d36ec0…577b`.
- The lane moved to `04637bdd` (integrator commit) during my probe; I did not
  make it. My probe wrote no lane file except this report; the
  `corpus/SOURCES.md` change in `git status` is a sibling seat's S049-S052
  registry rows, not mine. No git or jj mutation ran against the lane or the
  fleet repo. No owned web property was contacted; the retained snapshots were
  the only input.

## Evidence pointers and not verified
- Scripts and raw outputs, all under
  `/fast/scratch/hyaku/kake-r30/w1/MutC2CounterControl/`: `run_probe{,2..6}.py`,
  `results{,2..6}.jsonl`, `entry_quote_audit.json`; mutant commits reachable in
  `clone/` and `real/`. Counter under test:
  `.ufo/waves/round-30/c2_quote_truth.py` lines 62-64 (`gate_lines`), 67-70
  (`flip_letter`), 100-121 (the four checks and control).
- Not verified: the counter was not run against a committed real corpus,
  because `corpus/lessons/round-30.md` does not exist in the lane yet; R0 and
  R5 used a sandbox snapshot, and R5's lesson file was mine, not the lane's.
  Exit code 2 and argument handling were not exercised; only exits 0 and 1. A
  missing `corpus/SOURCES.md` table or missing entry file was not tested; S0
  covers only the present-but-empty case. No tooling was installed or
  upgraded, so nothing to record there.

Report: .ufo/waves/round-30/w1/MutC2CounterControl.md
