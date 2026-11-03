# MutC2 — mutation check of the frozen round-73 attack corpus

Round 73, kake, attempt 1, wave `w1`, seat `MutC2` (leaf; no subagents, no peer messages).
Base revision `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`; committted inputs read from the lane at
`HEAD = 4c7c53bc563a66ae0676b468966781f023ae0110` (freeze commit, which introduces the round-73
contract and corpus). All commands run from an absolute path; the lane checkout was read-only for this seat
(no `git add/commit/stash/checkout/reset/pull/push`, no `jj`, no writes except this report file).

## Question

Can the frozen corpus at `.ufo/waves/round-73/attack-corpus.txt` distinguish a detector that is correct from
detectors that are missing exactly one rule — H1 (brace fallback), H2 (command-position check), H4 (phrase
annotation)? The stand-in detector is the frozen round-72 counter's `line_findings` (the contract's declared
do-nothing control and the base of the rules under mutation).

## Inputs (committed bytes)

| file | revision | sha256 | check |
|---|---|---|---|
| `.ufo/waves/round-72/c72_tmp_v2.py` | base `c1f3d8d4` == HEAD | `af2f0c9c6b7ba04facdf63397b1e2e66ca20dd464984745354409d91fcf6e6ca` | copied, never edited |
| `.ufo/waves/round-73/attack-corpus.txt` | HEAD `4c7c53bc` (does not exist at base) | `9da8778285b3e8c0dbdd85efcbcd55beae1771a9b82218201066f778579ed44b` | `cmp` vs worktree rc=0 |
| `.ufo/waves/round-73/contract.md` | HEAD `4c7c53bc` | `35ca5bfc3917c0a8e450d72ea6a6dc55b26784f7e81416c79921a3d9bd5ffa98` | `cmp` vs worktree rc=0 |

Commands and exit codes:

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse --show-toplevel
  -> /home/vgpnk/Projects/shokunin/kake-shokunin   rc=0
git -C <lane> show 4c7c53bc:.ufo/waves/round-73/attack-corpus.txt > $S/corpus.head.txt   rc=0   (sha 9da87782…44b)
cmp $S/corpus.head.txt <lane>/.ufo/waves/round-73/attack-corpus.txt                       rc=0
cmp $S/contract.head.md <lane>/.ufo/waves/round-73/contract.md                            rc=0
git -C <lane> show c1f3d8d4:.ufo/waves/round-72/c72_tmp_v2.py > $S/c72.base.py            rc=0   (sha af2f0c9c…e6ca)
git -C <lane> show 4c7c53bc:.ufo/waves/round-72/c72_tmp_v2.py > $S/c72.head.py            rc=0   (same sha)
```

Scratch: `/fast/scratch/hyaku/kake-r73/MutC2/` (created, used with `TMPDIR` pointing there, deleted — see
Cleanup). Harness `mut_harness.py` sha256 `7f4802cb1905abba98635d1f1c65eabd98f1f612928295b4d625929f64875a76`.
No tool was installed or upgraded (operator directive): system `python3` only, `Python 3.14.8` (`python3 --version` rc=0).

## Method

1. Copied `command_span_words`, `line_findings` and the constants `PHRASE`, `TMP_ROOT`, `TOKEN_RE`,
   `BRACE_TOKEN_RE`, `COMMAND_WORDS`, `SPAN_RE` verbatim into the scratch harness; the original file was
   never written.
2. Fidelity check: imported the frozen module read-only and compared its `line_findings` with the copied
   baseline on every corpus line — `fidelity_check lines=15 mismatches=0 OK`. The copy is behaviourally
   identical to the frozen counter (so no mutation is an artefact of the transcription).
3. Classification rule, matching c72 `evaluate()`: a line is a `finding` iff `brace+command+prose > 0`,
   else `clean`.
4. Six single-rule mutants of the copied body:

| mutant | rule removed / altered |
|---|---|
| M1 | brace branch removed (`brace=0`, no brace-span masking) |
| M2 | command-span branch removed (`in_cmd_span` never consulted; imperative kept) |
| M3 | imperative first-word branch removed (`imperative=False`; command span kept) |
| M4 | annotation test inverted (`annotated = PHRASE not in line`) |
| M5 | PHRASE truncated to `not an executable` |
| M6 | annotation exemption dropped (`annotated = False`) |

5. Ran baseline + 6 mutants over all 15 data lines of the committed corpus (11 `attack`, 4 `legit`; 3 header
   lines ignored) and compared each classification with the `expected` column.

```
python3 -B $S/mut_harness.py $S/corpus.head.txt <lane>/.ufo/waves/round-72/c72_tmp_v2.py
  rc=0  (full log reproduced below)
```

## Kill table

Two numbers are given because the unmutated baseline itself disagrees with the expectation column (the
corpus is written to defeat c72's known holes, so the baseline is not "correct" on 9 lines):

- `diff_vs_expected` — corpus lines whose classification differs from the frozen `expected` column (the
  seat's literal kill count; lower is better);
- `newly_wrong` — lines the mutant classifies differently from the unmutated copy **and** wrongly
  (the discriminating power of the corpus for the mutated rule; empty = corpus cannot see the mutation).

| run | diff_vs_expected | newly_wrong vs baseline | lines | verdict |
|---|---|---|---|---|
| baseline (unmutated copy) | 9 / 15 | — | 4,5,6,7,8,9,10,11,12 | reference (holds the four routed holes) |
| M1 brace branch | 9 / 15 | none | same as baseline | **SURVIVES** — corpus cannot detect removal |
| M2 command-span branch | 10 / 15 | 1 (`13`) | 4,5,6,7,8,9,10,11,12,13 | **KILLED** by line 13 |
| M3 imperative first-word | 9 / 15 | none | same as baseline | **SURVIVES** — corpus cannot detect removal |
| M4 annotation inverted | 5 / 15 | 3 (`15,16,18`) | 4,5,15,16,18 | **KILLED** (breaks 3 legit lines) |
| M5 phrase truncated | 9 / 15 | none | same as baseline | **SURVIVES** — corpus cannot detect removal |
| M6 annotation dropped | 5 / 15 | 3 (`15,16,18`) | 4,5,15,16,18 | **KILLED** (breaks 3 legit lines) |

Raw output lines (exit 0):

```
fidelity_check lines=15 mismatches=0 OK
baseline  diff_vs_expected= 9 wrong=[4,5,6,7,8,9,10,11,12] newly_wrong=[] newly_right=[]
M1        diff_vs_expected= 9 wrong=[4,5,6,7,8,9,10,11,12] newly_wrong=[] newly_right=[]
M2        diff_vs_expected=10 wrong=[4,5,6,7,8,9,10,11,12,13] newly_wrong=[13] newly_right=[]
M3        diff_vs_expected= 9 wrong=[4,5,6,7,8,9,10,11,12] newly_wrong=[] newly_right=[]
M4        diff_vs_expected= 5 wrong=[4,5,15,16,18] newly_wrong=[15,16,18] newly_right=[6,7,8,9,10,11,12]
M5        diff_vs_expected= 9 wrong=[4,5,6,7,8,9,10,11,12] newly_wrong=[] newly_right=[]
M6        diff_vs_expected= 5 wrong=[4,5,15,16,18] newly_wrong=[15,16,18] newly_right=[6,7,8,9,10,11,12]
```

Per-line classification (`c`=clean, `f`=finding; `n` is the corpus file line number):

```
 n class  expected | baseline | M1 | M2 | M3 | M4 | M5 | M6
 4 attack finding  | c | c | c | c | c | c | c
 5 attack finding  | c | c | c | c | c | c | c
 6 attack finding  | c | c | c | c | f | c | f
 7 attack finding  | c | c | c | c | f | c | f
 8 attack finding  | c | c | c | c | f | c | f
 9 attack finding  | c | c | c | c | f | c | f
10 attack finding  | c | c | c | c | f | c | f
11 attack finding  | c | c | c | c | f | c | f
12 attack finding  | c | c | c | c | f | c | f
13 attack finding  | f | f | c | f | f | f | f
14 attack finding  | f | f | f | f | f | f | f
15 legit  clean    | c | c | c | c | f | c | f
16 legit  clean    | c | c | c | c | f | c | f
17 legit  clean    | c | c | c | c | c | c | c
18 legit  clean    | c | c | c | c | f | c | f
```

Baseline counts per line (brace/command/prose) that explain the table: lines 4–12 all `0/0/0`; line 13
`0/1/0`; line 14 `0/1/0`; legit 15,16,18 `0/0/0`; legit 17 `0/0/0` (no token at all). The do-nothing control
figure for the contract is therefore **c72 accepts k = 9 of 11 attack lines** (contract requires `k ≥ 1`:
satisfied).

## Answer

**No — the frozen corpus cannot distinguish a correct detector from one missing H1, the H2 imperative
command-position rule, or H4.** M1, M3 and M5 produce classification vectors identical to the unmutated
counter on all 15 lines: they change zero expectations, so they survive; the corpus is too weak for the
claim on those three rules. The corpus does kill M2 (command-span branch), M4 and M6 — but M4/M6 are killed
only because they start rejecting `legit` lines, not because they reject attacks.

Root causes, each verified (not inferred):

1. **H1 lines are invisible to the token grammar.** Corpus lines 4 and 5 are written
   `BK="${TMPDIR:-/tmp}/kake-r12"` — the brace default is `${TMPDIR:-/tmp}` with **no trailing slash**.
   `TOKEN_RE` needs the literal `/tmp/` and `BRACE_TOKEN_RE` needs `${TMPDIR:-/tmp/`. Direct probe (rc=0):

   ```
   corpus line 4: text='run the tool with BK="${TMPDIR:-/tmp}/kake-r12" first'
      TOKEN_RE.search -> None  BRACE_TOKEN_RE.search -> None  '/tmp/' in line -> False
   corpus line 5: text='repoint with BK=${TMPDIR:-/tmp}/kake-r12 before any write'
      TOKEN_RE.search -> None  BRACE_TOKEN_RE.search -> None  '/tmp/' in line -> False
   ```

   Both lines yield `0/0/0` under *every* run, including the unmutated counter: no branch can fire, so the
   brace rule is untested. Consequently a counter that keeps the frozen token grammar also cannot satisfy
   these two expectations; the corpus silently forces a wider token grammar (a counter change) rather than
   discriminating the brace rule.
2. **No attack line pairs the full absence phrase with an imperative first word.** Line 14 (`cp … /tmp/…`, no
   annotation) is caught by the *prose* fallback once the imperative branch is removed (M3: `0/0/1`), so the
   imperative rule is redundant on this corpus.
3. **No H4 shape exists.** Every annotation in the corpus is the full phrase `not an executable
   instruction`; no line carries a truncated phrase (`not an executable`, `historical record` alone).
   M5 therefore behaves identically to the baseline. Note the corpus header defines attacks as "holes H1-H3",
   while contract §C2 says attack lines carry "H1–H4" — the H4 shape is claimed but absent.
4. Only one attack line (13, the backticked `cp … /tmp/…` with the phrase) is discriminated by any recognised
   rule branch — and it is exactly the J3 shape already covered by c72's own selftest.

## Held-out lines (report only — corpus untouched)

One line per survivor, each verified to be `finding` under the unmutated counter and `clean` under its
target mutant; each is a legitimate `attack` line under the corpus's own semantics (a token-bearing line that
must not pass) and would be appended to the corpus by a corpus owner, not by this seat. Probe rc=0:

| survivor | held-out line (proposed `attack | finding |` payload) |
|---|---|---|
| M1 (brace) | `run the tool with BK="${TMPDIR:-/tmp/}kake-r12" (historical record, not an executable instruction)` |
| M3 (imperative) | `cp state/probe-latest.json /tmp/kake-r12/live/backup.json (historical record, not an executable instruction)` |
| M5 (phrase) | `the tool used to write under /tmp/kake-r12/live/ (historical record, not an executable)` |

Observed per-line counts (brace/command/prose):

```
--- H-M1: run the tool with BK="${TMPDIR:-/tmp/}kake-r12" (historical record, not an executable instruction)
   frozen c72 line_findings: (1, 0, 0) -> finding
   baseline 1/0/0 finding | M1 0/0/0 clean | M2 1/0/0 | M3 1/0/0 | M4 1/0/0 | M5 1/0/0 | M6 1/0/0
--- H-M3: cp state/probe-latest.json /tmp/kake-r12/live/backup.json (historical record, not an executable instruction)
   frozen c72 line_findings: (0, 1, 0) -> finding
   baseline 0/1/0 finding | M1 0/1/0 | M2 0/1/0 | M3 0/0/0 clean | M4 0/1/0 | M5 0/1/0 | M6 0/1/0
--- H-M5: the tool used to write under /tmp/kake-r12/live/ (historical record, not an executable)
   frozen c72 line_findings: (0, 0, 1) -> finding
   baseline 0/0/1 finding | M1 0/0/1 | M2 0/0/1 | M3 0/0/1 | M4 0/0/0 clean | M5 0/0/0 clean | M6 0/0/1
```

H-M1 isolates M1 exactly; H-M3 isolates M3 exactly; H-M5 kills M5 (and M4, already killed elsewhere) but no
other mutant. H-M1 deliberately uses the trailing-slash brace form the frozen regex can see; the corpus's
own no-slash form remains undetectable by the frozen grammar (root cause 1).

## Restoration / cleanup evidence

The frozen files were never edited; this seat mutated only its scratch copy.

```
pre:  9da87782…44b  attack-corpus.txt      post: 9da87782…44b   (unchanged)
pre:  35ca5bfc…a98  contract.md            post: 35ca5bfc…a98   (unchanged)
pre:  af2f0c9c…6ca  c72_tmp_v2.py          post: af2f0c9c…6ca   (unchanged)
rm -rf -- /fast/scratch/hyaku/kake-r73/MutC2     rc=0
test ! -d /fast/scratch/hyaku/kake-r73/MutC2     rc=0   (scratch tree gone; parent /fast/scratch/hyaku/kake-r73 left for siblings)
git -C <lane> rev-parse HEAD                     -> 4c7c53bc563a66ae0676b468966781f023ae0110
git -C <lane> status --porcelain -- .ufo/waves/round-73/w1/ <c72> <corpus>
                                                 -> ?? .ufo/waves/round-73/w1/   (this report is the only new path)
```

Frozen counters and the corpus were run as documented and not modified; no lane git/jj state was touched.

## Boundary of this seat

Findings are coverage facts about the frozen corpus, not a change to the claim, the corpus or the future
c73 counter. The corpus owner decides whether to add the three held-out lines; the executor's counter must
still satisfy the frozen predicate, and this report does not assert any after-state measurement.
