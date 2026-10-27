# ExecutorCounterMutation12 — counter strictness on response-header entry citation form

Seat: `ExecutorCounterMutation12` (executor, advisory)
Item: assess the frozen counter's strictness on response-header entry citation
form; count true positive vs false positive on base; scratch only.
Base: `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`
Counter: `.ufo/waves/round-62/c62_calibration.py`, sha256
`ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d` (verified
unchanged at report time).
Scope note: this seat made **no** change to the claim, the counter, the
criteria or any score. Everything below is measurement in scratch only.

## Verdict

The counter is **sound as a do-nothing control and unreliable as a measure of
citation form**. On base it is exactly right on all seven signals
(TP=7, FP=0, FN=0). Its `quote_correction` bit, however, does not measure
citation form at all: it is three independent substring tests with no locality
and no grounding check, and the one conjunct that names the section
(`"S432 §3.6"`) is **vacuous** because the base entry already contains that
literal twice.

Advisory, for the L1 and the implementers of the after-state: the after-state
must be verified by **reading the entry**, not by trusting `met=true`.

## Evidence

### 1. Base control reproduces exactly

`python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`

```
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
exit 1
```

Byte-identical to the recorded base control. A scratch git fixture whose
`corpus/` blobs are a byte mirror of the base (`git show <base>:<path>` for
the five counter paths) reproduced the same line and the same exit 1.

### 2. Base truth table — 7 TP, 0 FP, 0 FN

| signal | counter | ground truth on base | class |
|---|---|---|---|
| `disagreements=1` | 1 | exactly one S432 `Disagree` row in `corpus/lessons/round-61-verifier-spotcheck.md` (line 33) | TP |
| `unresolved=1` | 1 | the disagreement is unresolved; no correction exists | TP |
| `quote_correction=0` | 0 | no correction in `corpus/knowledge/response-header-expectations.md` | TP |
| `criterion=0` | 0 | no QUALITY.md criterion cites the spot-check | TP |
| `lesson_gate=0` | 0 | `corpus/lessons/round-62.md` does not exist at base | TP |
| `source_row=1` | 1 | `corpus/SOURCES.md:178` carries `\| S432 \|` | TP |
| `met=false` | false | the claim is not met at base | TP |

**False positives on base: 0. False negatives on base: 0.** The base control
is honest; the base-control requirement in the contract is satisfied.

### 3. The `"S432 §3.6"` conjunct is vacuous — the decisive finding

The predicate (counter lines 33–35) is:

```python
correction = int(QUOTE in data["knowledge"] and "S432 §3.6" in data["knowledge"]
                 and "Round-62 correction" in data["knowledge"])
```

Three independent substring tests over the **whole file**, with no locality
requirement and no check that they co-occur.

The base entry already contains the literal `S432 §3.6` **twice**:

```
line  75: location [S432 §3.6]:
line  86: the first one to `nosniff` as an ASCII case-insensitive match (S432 §3.6,
```

(verified against the lane base blob, 216 lines total.) So the section citation
conjunct is satisfied by the **pre-existing** entry, and the counter cannot
tell a new block that cites S432 §3.6 from one that cites nothing, the wrong
section, or a different source.

Citation-form dimension in isolation (quote/marker/support held canonical,
only the citation form varied) — **6 TP, 5 FP, 0 FN**:

| citation form in the new block | contract | counter | class |
|---|---|---|---|
| `[S432 §3.6]` | accept | 1 | TP |
| `S432 §3.6` | accept | 1 | TP |
| `S432, §3.6` | accept | 1 | TP |
| `§3.6 of S432` | accept | 1 | TP |
| `Fetch §3.6` | accept | 1 | TP |
| `Fetch, §3.6` | accept | 1 | TP |
| `[S432 §3.5]` — wrong section | reject | 1 | **FP** |
| `[S432 §3.7]` — wrong section | reject | 1 | **FP** |
| `[S431 §3.1]` — wrong source | reject | 1 | **FP** |
| `[S430 §7.1]` — wrong source | reject | 1 | **FP** |
| *(no citation at all)* | reject | 1 | **FP** |

Zero false negatives here, five false positives: **the citation-form half of
the predicate is one-directional — it never rejects a bad citation, and it
cannot reject a good one either, because the good-citation token was already
present before the wave.**

### 4. Quote byte-form: 6 false negatives

The `QUOTE` literal is byte-exact, including U+2019 (RIGHT SINGLE QUOTATION
MARK). The retained source body at `.ufo/waves/round-61/sources/S432.html`
lines 6151–6154 flattens to exactly that byte string, so the counter's quote is
faithful to the source. But any typographic or layout deviation is rejected —
**3 TP, 6 FN**:

| quote form | contract | counter | class |
|---|---|---|---|
| U+2019 apostrophe, one line | accept | 1 | TP |
| U+2019 + trailing period | accept | 1 | TP |
| U+2019 + trailing space | accept | 1 | TP |
| U+0027 straight apostrophe | accept | 0 | **FN** |
| U+2018 left quote | accept | 0 | **FN** |
| hard-wrapped at 78 cols | accept | 0 | **FN** |
| backticked `` `Content-Type` `` | accept | 0 | **FN** |
| double space mid-sentence | accept | 0 | **FN** |
| NBSP inside | accept | 0 | **FN** |

Two of these are live risks for this round specifically:

- **Hard-wrapping.** The entry's prose wraps at a median of 75 columns
  (`corpus/knowledge/response-header-expectations.md`, median 75, p90 79), and
  the corpus contains 80 wrapped `> ` blockquote continuation lines across
  `corpus/knowledge/`. A wrapped quote silently fails the counter.
- **Backticked field name.** The *source body itself* renders the field as
  `<code>Content-Type</code>`, so a faithful quotation with ticks is rejected.
  Note the counter's own quote uses the un-ticked `Content-Type`, so the
  counter's quote and the source's markup disagree on that one token.

### 5. Marker token: 6 false negatives

`"Round-62 correction"` is matched case- and hyphen-sensitively and with no
word boundary. **4 TP, 6 FN**:

| marker | contract | counter | class |
|---|---|---|---|
| `## Round-62 correction` | accept | 1 | TP |
| `## Round-62 correction.` | accept | 1 | TP |
| `## Round-62 corrections` | accept | 1 | TP |
| `## Round-62 correction (S432)` | accept | 1 | TP |
| `## round-62 correction` | accept | 0 | **FN** |
| `## Round 62 correction` | accept | 0 | **FN** |
| `## Round-62-correction` | accept | 0 | **FN** |
| `## Round 62 Correction` | accept | 0 | **FN** |
| `## Correction (round-62)` | accept | 0 | **FN** |
| `## Round-62 fix` | accept | 0 | **FN** |

The heading must be spelled exactly `Round-62 correction`.

### 6. No locality, no grounding, no support requirement

- **Scattered tokens suffice.** A marker line at the top of the file and the
  quote at the bottom, with no shared block and no citation, scores
  `quote_correction=1`.
- **The quote is never checked against the retained source.** The counter
  reads only the five committed blobs; it never opens `S432.html`. A quote
  with the wrong apostrophe, the wrong wrapping, or a wrong field name is
  rejected purely on bytes, while a quote attributed to the wrong source is
  accepted.
- **The counter never requires the correction to explain its support.** The
  contract requires the correction to "explain its support"; no conjunct
  checks this.
- **The quote may sit inside a rejection.** A block whose text is
  `Round-62 correction candidate (rejected, not adopted): "<quote>" [S432 §3.6]`
  scores `quote_correction=1` — the marker substring is present in the
  rejection notice.

### 7. `unresolved` is derived, not measured

Counter lines 39–41:

```python
resolved = correction == 1 and criterion == 1 and lesson_gate == 1 and source_row == 1
unresolved = disagreements if not resolved else 0
met = unresolved == 0 and resolved
```

Once all four other signals hold, `unresolved` is forced to 0 and the
`disagreements` count stops influencing `met`. Consequence: **the counter
cannot enforce the contract's "the existing S432 row is kept; do not mark it
rejected" requirement.** Full landings that mutate the row still reach
`met=true`:

| S432 spot-check row | counter verdict |
|---|---|
| kept as `Disagree` (contract-correct) | `met=true`, exit 0 |
| `Disagree` cell changed to `Agree` | `met=true`, exit 0 |
| row deleted from the table | `met=true`, exit 0 |
| `Admit` cell changed to `Reject` | `met=true`, exit 0 |

In the correct case the counter prints `disagreements=1 unresolved=0`; in the
violating cases it prints `disagreements=0 unresolved=0`. **`disagreements=1`
alongside `met=true` is the observable signature of the contract-correct
landing**, and it is the only signal that distinguishes it.

The `disagreements` counter itself is a line-level test
(`"S432" in line and "Disagree" in line`), so it counts *lines*, not rows:
an appended prose line containing `S432` and the substring `Disagree` (e.g.
`Disagreement`) raises it to 2; a lowercase `disagree` or a `Disagree` about a
different item does not; `S432` and `Disagree` on separate lines do not count.

### 8. The other two after-state bits are equally loose

- **`criterion`** = `"substantive located quote" in QUALITY.md` and
  `"round-61-verifier-spotcheck.md" in QUALITY.md`. Case-sensitive: a
  QUALITY.md row labelled `Substantive located quote` scores **0** (every
  existing criterion label in QUALITY.md is Capitalised — `Citation-local
  absence`, `Replayable claim`, …), while the lowercase literal scores 1.
  The two tokens need not be in the same row: split across two unrelated
  rows → 1; inside an HTML comment → 1.
- **`lesson_gate`** = `"## Gate"`, `"S432"`, `"Agree"`, `"Reject"` all present
  in `corpus/lessons/round-62.md`, with no requirement that they address the
  S432 disagreement. A Gate section reading `S432 was noted. Some Agree and
  some Reject decisions exist.` scores 1.

### 9. End-to-end: `met=true` is reachable with the after-state violated

Full landings (canonical quote/marker/criterion/lesson) with one violation
each, all reaching `met=true` / exit 0:

| landing | contract | counter |
|---|---|---|
| canonical everywhere | ok | `met=true` |
| S432 Disagree row deleted | violated | `met=true` (**FP**) |
| S432 Disagree cell → Agree | violated | `met=true` (**FP**) |
| new block cites no section | violated | `met=true` (**FP**) |
| new block cites S432 §3.5 | violated | `met=true` (**FP**) |
| new block cites S431 §3.1 | violated | `met=true` (**FP**) |
| quote only inside a rejected-candidate list | violated | `met=true` (**FP**) |
| no support explanation | violated | `met=true` (**FP**) |
| QUALITY tokens split across two rows | violated | `met=true` (**FP**) |
| QUALITY tokens only in an HTML comment | violated | `met=true` (**FP**) |
| lesson Gate never addresses the disagreement | violated | `met=true` (**FP**) |

Symmetrically, three contract-correct landings are **rejected** by the counter
(`met=false`): the quote hard-wrapped at house-style width, the quote with a
straight ASCII apostrophe, and the QUALITY row labelled `Substantive located
quote`.

### 10. Aggregate over the full combinatorial matrix

672 combinations (7 quote forms × 6 marker forms × 8 citation forms × 2
explanation forms), labelled against the contract's stated after-state:
**TP=45, FP=99, FN=165, TN=363** → precision 0.3125, recall 0.2143.

A 24-case hand-labelled grid over realistic authoring choices (canonical
single-line, unquoted blockquote, house-style wrap, trailing period, code
fence, straight apostrophe, three citation reorderings, spec-name citation,
marker case/hyphen variants, missing explanation, rejected-candidate list,
marker-only, negated marker, wrong source, wrong section, sibling file, no-op
control, backticked field name, single-quoted field name) gave
**TP=8, FP=4, FN=6, TN=4**, with the structural heuristic agreeing with the
hand label on 20 of 24 cases.

The matrix numbers are lower-bound quality figures for a *form-sensitive*
checker: they count every spelling of the same sentence as a separate case.
They are reported because the item asked for a true/false count, not as an
estimate of a realistic authoring distribution.

## Risks for the wave

1. **The after-state can satisfy `met=true` while violating the contract.**
   The counter will not catch a deleted or flipped S432 row, a wrong-section
   or wrong-source or absent citation, a quote placed inside a rejection, a
   missing support explanation, or a criterion whose two tokens sit in
   unrelated rows. The counter's own `disagreements` value is the only
   observable that separates the contract-correct landing (`disagreements=1`)
   from a row-mutating one (`disagreements=0`).
2. **The counter can reject a good after-state.** A house-style wrapped quote,
   a straight ASCII apostrophe, or a Capitalised `Substantive located quote`
   label each produce `met=false` on a contract-correct landing. Because the
   entry's prose wraps at ~75 columns and every existing QUALITY criterion
   label is Capitalised, these are the two most likely accidental failures.
3. **The `S432 §3.6` conjunct proves nothing about the new block.** It was
   already satisfied by base lines 75 and 86. A `quote_correction=1` result
   therefore says only that the byte-exact quote string and the marker string
   appear somewhere in the file.
4. **The counter never opens the retained source.** Nothing in
   `quote_correction=1` attests that the quoted sentence is in
   `.ufo/waves/round-61/sources/S432.html`. (Independently confirmed here:
   flattening source lines 6151–6154 with tags stripped and whitespace
   collapsed yields `X-Content-Type-Options response header can be used to
   require checking of a response’s Content-Type header against the
   destination of a request.`, which contains the counter's `QUOTE` verbatim
   at char 109137 of the whole document — so the counter's quote text *is*
   faithful to the retained body. The defect is that the counter never
   checks this.)

## Recommendations (advisory only; no change made)

For the implementer of the after-state, the safe landing is the one that
maximises the counter's chance of agreeing *and* satisfies the contract on
inspection:

- append a block headed exactly `## Round-62 correction` (capital R, hyphen,
  singular) to `corpus/knowledge/response-header-expectations.md`;
- quote the sentence on **one line** as
  `> "response header can be used to require checking of a response’s
  Content-Type header against the destination of a request"` with U+2019 and
  an un-ticked `Content-Type`;
- cite it as `[S432 §3.6]` in that same block;
- state plainly what the sentence supports and that it is not the generic
  lead-in the round-61 spot-check rejected;
- append a QUALITY.md criterion row whose label contains the **lowercase**
  literal `substantive located quote` and whose grounding cites
  `corpus/lessons/round-61-verifier-spotcheck.md` in the same row;
- add a `## Gate` section to `corpus/lessons/round-62.md` naming S432, the
  Disagree decision, and both an Agree and a Reject row;
- **keep** the S432 `Disagree` row in
  `corpus/lessons/round-61-verifier-spotcheck.md` unchanged, and expect
  `disagreements=1` in the after-state output.

If the L1 wants the counter itself hardened, the minimal changes that would
close the measured gaps are: require the `S432 §3.6` citation **inside the
correction block** rather than anywhere in the file; normalise the quote
(strip whitespace, normalize apostrophes) before comparison; and compare the
quote against the retained `S432.html` body rather than against a hard-coded
literal. **The counter is frozen and must not change after any score, so this
is recorded as a future-round observation only.**

## Reproducibility

All measurements ran in a scratch git fixture at
`/fast/scratch/hyaku/kake-r62/ExecutorCounterMutation12/fixture`, built from
`git show <base>:<path>` of the five counter paths. Every fixture git
operation used explicit `git -C <fixture>`; the fixture root was asserted
with `git rev-parse --show-toplevel` before use. Scratch scripts:
`harness.py`, `grid.py`, `probe.py`, `probe2.py`, `probe3.py`, `probe4.py`,
`probe5.py`, `probe6.py`, `probe7.py`, `citation.py`; JSON outputs
`grid.json`, `matrix.json`, `dims.json`, `results.json`. The scratch
directory was deleted before yielding.

No pacman transactions. No installs. No lane, fleet, sibling-repo, source-tree
or operator-config writes. Verified at report time: lane `git status
--porcelain` shows only the untracked `.ufo/waves/round-62/` directory, lane
HEAD is still `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`, and the counter
sha256 is still
`ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`.
