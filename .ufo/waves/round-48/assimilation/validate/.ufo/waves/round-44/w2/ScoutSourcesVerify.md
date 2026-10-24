# ScoutSourcesVerify — round 44 wave 2

- **Axes:** freshness (quoted bytes still at the named sections); operability (the check is one re-runnable extraction).
- **Attack:** each quoted passage behind lesson rows S131/S132 appears verbatim in the named section's first section-prose paragraph, and is at most 25 words.
- **Result:** **PASS** on the three Gate quotes. **MISSING** at the extra S131 locator `ReviewFreeze.md` §1 (the sha256 sentence is not in that section).
- **Opened:** 2026-10-23. LSP definition/references not used: these are markdown prose passages, not symbols. Proof is the file bytes.

## Quotes checked

From `corpus/lessons/round-44.md` Gate (the passages S131/S132 correct locators for):

| id | lesson string | named section | words | in first section-prose paragraph |
|---|---|---|---|---|
| Q1 | The do-nothing shortcut never reaches predicate_pass=true | CtlDoNothing.md `## Verdict` | 6 | FOUND after hard-wrap join and code-span backtick strip; raw `grep -F` is 0 |
| Q2 | every pinned sha256 verifies over the committed blob | ReviewFreeze.md `## Verdict` | 8 | FOUND raw (`grep -cF` = 1), paragraph index 1 only |
| Q3 | records a calibration error present when the statement was written | self-assessment-at-writing.md `# Checking self-assessment statements at writing` | 10 | FOUND raw (`grep -cF` = 1), paragraph index 1 only |

All three are ≤25 words. Each occurs once in its file. Q2 and Q3 are contiguous source bytes. Q1 is the same words in paragraph 1, but the source hard-wraps the sentence and writes `` `predicate_pass=true` ``. That is the lane's standing quote convention (SOURCES.md round-36 note: quotes hold modulo markdown code-span backticks; round-43 `ReviewSourcesRows` recorded the same Q1 caveat). It is not a different sentence.

## Actual first section-prose paragraphs

Section-prose = blank-line blocks after the heading; fenced code is not prose. Paragraph index 1 is the first such block.

**CtlDoNothing.md `## Verdict` (heading line 7), paragraph 1:**

```
**The control is caught.** Under the amended counter (commit `27902a16`, amendment 1), controls mode
reports `ctl.py kill=0/18 accept=8/8 predicate_pass=False`, `all_false=True`, exit 0. The do-nothing
shortcut never reaches `predicate_pass=true`.
```

**ReviewFreeze.md `## Verdict` (heading line 3), paragraph 1:**

```
**CONFORMANT.** The freeze commit f6d8a891f1d966c5c3cdda385090da3a6e804675 matches the contract's claimed frozen_artifacts: every pinned sha256 verifies over the committed blob, the runner is byte-untouched, SCORECARD.md/LOG.md/corpus are byte-identical to base 66e1fb4, the before receipts carry real captured exits (proven `;`-form) and predate the freeze, and the dev selftest receipt shows 21/21 with exit 0. No conformance defect found in the freeze. Named observations and residual risks follow the evidence; none blocks data.
```

**self-assessment-at-writing.md `# Checking self-assessment statements at writing` (heading line 5), paragraph 1:**

```
Round 29 C1 checks only the statement forms extracted from lines of `SCORECARD.md` and `SHONEN.md` at the frozen base. For each line, the counter gets writing revision `W` from `git blame --line-porcelain`; Git documents blame as attributing each line to the revision that last modified it, and `--line-porcelain` emits commit information for each line (S174). The check then evaluates the statement against the committed tree/history at `W`, not just against the current tip. A mismatch therefore records a calibration error present when the statement was written (for example, an overclaim or wrong pointer), rather than later drift from a once-correct statement. That is why C1 is a calibration check, not a freshness-only check.
```

## S131 "and §1" — quote missing

S131's anchor and teaches cells still say `ReviewFreeze.md "## Verdict", first paragraph and §1`. §1 is `## 1. Mandated diff (66e1fb4 → f6d8a89)` (heading line 9). Its first section-prose paragraph is:

```
Command (run in /home/vgpnk/Projects/shokunin/tameshi-shokunin, read-only flags; scratch capture /fast/scratch/hyaku/tameshi-r33-seats/ReviewFreeze/difftree.z, exit `0` in difftree.exit):
```

Q2 is not in that paragraph and not anywhere in the §1 body. The Gate table itself places Q2 only at §Verdict, first section-prose paragraph, which holds. The leftover "and §1" is not a location of the quoted passage.

## Commands and decisive output

Working directory: inline reads of the three source paths. Scratch dir created; no script file kept (heredoc).

```text
=== WORD COUNTS (whitespace split, lesson strings) ===
Q1 do-nothing: wc=6 le25=True text='The do-nothing shortcut never reaches predicate_pass=true'
Q2 sha256: wc=8 le25=True text='every pinned sha256 verifies over the committed blob'
Q3 calibration: wc=10 le25=True text='records a calibration error present when the statement was written'

=== SECTION FIRST PROSE + MEMBERSHIP ===

## Q1 do-nothing
heading_exact_matches=1 heading='## Verdict'
heading_line=7
blocks=3 prose_paragraphs=3
in_first_raw_ws=False
in_first_backticks_stripped=True
prose_paragraph_indexes_containing_quote_backticks_stripped=[1]
prose_paragraph_indexes_containing_quote_raw=[]

## Q2 sha256
heading_exact_matches=1 heading='## Verdict'
heading_line=3
blocks=2 prose_paragraphs=2
in_first_raw_ws=True
in_first_backticks_stripped=True
prose_paragraph_indexes_containing_quote_backticks_stripped=[1]
prose_paragraph_indexes_containing_quote_raw=[1]

## Q3 calibration
heading_exact_matches=1 heading='# Checking self-assessment statements at writing'
heading_line=5
blocks=7 prose_paragraphs=7
in_first_raw_ws=True
in_first_backticks_stripped=True
prose_paragraph_indexes_containing_quote_backticks_stripped=[1]
prose_paragraph_indexes_containing_quote_raw=[1]

=== REVIEWFREEZE §1 (## 1. Mandated diff) ===
heading='## 1. Mandated diff (66e1fb4 → f6d8a89)' line=9 prose_count=2
sha256_quote_anywhere_in_section1_prose=False
sha256_quote_anywhere_in_section1_body=False

=== QUOTE OCCURRENCE COUNTS IN WHOLE FILE (ws-normalized, backticks stripped) ===
Q1 do-nothing count=1
Q2 sha256 count=1
Q3 calibration count=1

=== RAW FIXED-STRING (no join) ===
Q1 do-nothing raw_count=0 backticked_variant_count=0
Q2 sha256 raw_count=1 backticked_variant_count=n/a
Q3 calibration raw_count=1 backticked_variant_count=n/a
--- wc -w ---
6
8
10
--- grep -cF single-line ---
0
1
1
--- grep -cF backticked do-nothing fragment ---
1
```

`grep -cF` paths, in order: `tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md` (Q1 unbackticked = 0), `ReviewFreeze.md` (Q2 = 1), `kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` (Q3 = 1), then `never reaches ` + backtick + `predicate_pass=true` + backtick in CtlDoNothing.md = 1. Q1's full backticked sentence is not one line (`backticked_variant_count=0`) because the prose hard-wraps before `shortcut never reaches`.

## Files written

- `.ufo/waves/round-44/w2/ScoutSourcesVerify.md` (this report)
- Directory `/fast/scratch/hyaku/kake-r44/ScoutSourcesVerify/` created; no file left there

## Installs

None.

## Blockers

None. Unrun: no census, no build, no LSP.
