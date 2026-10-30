# W1 seat MutC1Counter — mutation test of `c64_calibration.py` (round-64 C1)

Seat: MutC1Counter-2 · Date 2026-10-30 · Leaf, no subagents. Lane untouched:
read-only `git show/status` on
`/home/vgpnk/Projects/shokunin/kake-shokunin`; every clone, fixture and mutant
lived under `/fast/scratch/hyaku/kake-r64/MutC1Counter-2/` (deleted before this
report was finalized; all evidence is inlined below).

## What was attacked

The frozen C1 instrument
`.ufo/waves/round-64/c64_calibration.py` — sha256 re-verified before and after
the whole session:

```
5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf  c64_calibration.py
```

16 single-fault mutants (the 8 seat-named faults plus 8 extras), each one
minimal source edit applied to a scratch copy. Detector question per seat spec:
**does a committed control fixture (marker / fabrication / junk / ledger-mut)
or the counter's own selftest kill it?**

## Baseline (pristine) — green, so mutant results are meaningful

Fixtures were rebuilt with the frozen builder
`.ufo/waves/round-64/fixtures/build_fixtures.py` (sha256
`7fbd8cbc67c17264096e44474a698b3f0d7702c3e1cc23f0b5bdaa26ee0271d3`) into the
scratch dir, plus a ledger-mut repo built to the committed receipt's spec
(marker-repo tree with `locatedRawLines` `6150-6154` → `6150-6156`; verified by
`diff -r --brief` that only `quote-classes.json` differs from marker-repo).
Commit hashes differ from the frozen receipt hashes (commit time differs);
content is identical. Pristine detector suite (all outputs matched the
committed receipts token-for-token):

```
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root <lane> --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb
revision=4c8295fa… disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok
derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1
lesson_gate=1 source_row=1 unresolved=0 met=true     exit=0        # = controls/after-c1.txt
$ … --revision 1a48131577ba82c967650561be34e8dba909432a
… lesson_gate=0 source_row=1 unresolved=1 met=false  exit=1        # = controls/base-c1.txt
marker-repo       … quote_correction=0 criterion=0 lesson_gate=0 … unresolved=1 met=false exit=1  # = control-marker.txt
fabrication-repo  … quote_correction=0 criterion=0 lesson_gate=0 … unresolved=1 met=false exit=1  # = control-fabrication.txt
junk-repo         … pins=0 pin_drift=drift:raw,text,ledger,recipe recipe_rederive=0 … met=false exit=1 # = control-junk.txt
ledger-mut-repo   … pins=0 pin_drift=drift:ledger … met=false exit=1                        # = control-ledger-mut.txt
$ … --selftest --selftest-work <scratch>/selftest-work
selftest 26/26  exit=0                                                                     # = selftest-c1.txt
```

Kill levels: **A** = predicate flip (`met`/exit changes on T0, base or a
control — breaks the frozen C1 predicate); **B** = component-level kill (a
control's output line changes but `met` stays false — the receipt detects the
weakening, the predicate does not); **C** = survivor (byte-identical output
everywhere); **E** = survivor by equivalence-under-pins (argued, below).

## Kill matrix (16 mutants)

| # | Single fault (mutated line, pristine file) | Killed by | Selftest | Verdict |
|---|---|---|---|---|
| M01 | pins check dropped for **ledger**: `drift` filter gains `k != "ledger"` (line 207) | ledger-mut + junk, **B only** (`pin_drift=drift:ledger`→`none`; `met` stays false) + t3 drift FAIL | 25/26 | **Partial kill** — see Probe P5: predicate survives a note-only ledger edit |
| M02 | recipe equality loosened to sha-only (lines 227-228 → single sha compare) | none | 26/26 | **Survivor (E)** — equivalent under pins |
| M03 | located equality to pinned constant dropped: line 241 keeps only the ledger compare | none | 26/26 | **Survivor (E)** — equivalent under pins |
| M04 | class_match inverted to `raw-substring` (line 238) | **T0, A-level**: `met=true`→`met=false` exit 0→1 at the measured revision; also base/marker/fabrication component changes | 25/26 (t4 class1 FAIL) | **Killed (A)** |
| M05 | quote_correction loosened to file-level: `int(FROZEN_QUOTE in knowledge and LEDGER_REL in knowledge)` (line 248) | none | 26/26 | **Survivor — finding F2** (Probe P3 flips `met`) |
| M06 | criterion reduced to terms-only: `CRITERION_SENTENCE in r62` dropped (line 250) | marker/fabrication/junk/ledger-mut, **B** (`criterion=0`→`1`; `met` stays false) | 26/26 | **Killed (B)** |
| M07 | lesson_gate span dropped: `and SPOT_VERDICT_SPAN in gate` removed (line 256) | all four controls, **B** (`lesson_gate=0`→`1`, `unresolved=1`→`0`; `met` stays false) | 24/26 (t4 gate0, t4 unresolved FAIL) | **Killed (B)** |
| M08 | unresolved masked like c63: `unresolved = 0` (line 267) | base + all four controls, **B** (`unresolved=1`→`0`; `met` stays false everywhere — base stays red only because `lesson_gate=0` there) | 25/26 (t4 unresolved FAIL) | **Killed (B)** — but note the mask alone never flips a predicate; it rides on other gates |
| M09 | `source_row` gate dropped from `met` (line 268-269) | none | 26/26 | **Survivor — finding F2** (Probe P1 flips `met`) |
| M10 | `disagreements >= 1` gate dropped from `met` | none | 26/26 | **Survivor — finding F2** (Probe P6 flips `met`) |
| M11 | pins check dropped for **raw**: `k != "raw"` (line 207) | junk, **B only** (`pin_drift` list loses `raw`) + t3 drift FAIL | 25/26 | **Partial kill** — Probe P4: predicate survives a non-rendered raw edit |
| M12 | ledger `matchClass` equality dropped from class_match (line 238-239) | none | 26/26 | **Survivor (E)** — equivalent under pins |
| M13 | recipe output check removed entirely (`if True:` at line 227; `recipe_rederive` always 1) | none | 26/26 | **Survivor (E)** — equivalent under pins |
| M14 | derive_located keeps first start, not minimum span: `span < best[0]` → first-match (line 177) | **T0, A-level**: `located=6139-6154`≠`6150-6154` → `met=false` exit 1 at the measured revision | 23/26 (t4 class1, t4 located, t7 located FAIL) | **Killed (A)** |
| M15 | lesson_gate author-side label dropped: `and ("author-side" in gate or …)` removed (line 259) | none | 26/26 | **Survivor — finding F2** (Probe P2 flips `met`) |

Score: 2 × A-killed, 5 × B-killed (of which M01/M11 partial), 4 × E-equivalent,
4 × true survivors. Matrix data was emitted by
`mutate_c1.py` → `logs/matrix.json` (scratch, deleted; per-mutant outputs
summarized above).

## Survivor probes (each = T0 tree + one edit, run pristine vs mutant)

Probes confirm each true survivor is a real semantic weakening, not noise:
on these T0-derived fixtures **pristine prints met=false and the mutant prints
met=true** — i.e. a committed control shaped like the probe would kill, but no
committed control has that shape.

- **P1 → M09.** S432 `corpus/SOURCES.md` row `mined`→`admitted` (all else T0).
  pristine: `source_row=0 … met=false` exit 1. M09: `source_row=0 … met=true`
  exit 0. No committed control has `source_row=0` (all four control receipts
  print `source_row=1`).
- **P2 → M15.** Lesson Gate loses `author-side`/`self-assessment`
  (`author-side\nself-assessment;` → `reviewer\nreview;`). pristine:
  `lesson_gate=0 … unresolved=1 met=false`. M15: `lesson_gate=1 … unresolved=0
  met=true`. Both committed Gate prose at T0 contains both words, so the
  controls can never isolate this clause.
- **P3 → M05.** Frozen quote removed from the `[r63-correction]` block and
  re-planted under `## Limits`. pristine: `quote_correction=0 … met=false`.
  M05: `quote_correction=1 … met=true`. The fabrication control plants prose
  *without* the quote (file-level check stays 0 either way), so the committed
  fixture never tests block placement.
- **P4 → M11.** Raw blob gains `\n<!-- planted -->\n` (HTMLParser skips it, so
  recipe output, class and located are unchanged). pristine:
  `pins=0 pin_drift=drift:raw … met=false`. M11: `pins=1 … met=true` exit 0.
  The junk control mutates raw *and* text/ledger/recipe at once, so the raw
  pin is never isolated.
- **P5 → M01.** Ledger `note` field edited (`Retained-HTML raw lines` →
  `PLANTED-NOTE Retained-HTML raw lines`); the counter reads only
  `id`/`matchClass`/`locatedRawLines`. pristine: `pins=0
  pin_drift=drift:ledger … met=false`. M01: `pins=1 … met=true` exit 0. The
  ledger-mut control mutates `locatedRawLines`, which the located
  re-derivation also catches — so the ledger pin's own isolated coverage
  (unread fields) is zero.
- **P6 → M10.** Round-61 spot-check row `| Disagree |` → `| Agree |`.
  pristine: `disagreements=0 … met=false`. M10: `disagreements=0 … met=true`
  exit 0. Every control receipt prints `disagreements=1`, so the ≥1 gate is
  never exercised.

## Finding F1 (pristine counter, not a mutant) — spot-check binding is one-way

`corpus/lessons/round-61-verifier-spotcheck.md` is **not pinned** (the pin set
is raw/text/ledger/recipe only, lines 90-95; the spot file is only read to
count `S432`+`Disagree` lines, line 198). The lesson-gate span
(`SPOT_VERDICT_SPAN`, line 256) is a constant mirrored into the lesson — it is
never compared against the spot-check file's actual bytes. Probes on T0
trees, **pristine counter**:

- **P7** — spot-check reason rewritten to assert the opposite
  (`is only a generic lead-in, not substantive evidence…` → `is substantive
  evidence…`, `Disagree` kept):
  `disagreements=1 pins=1 … lesson_gate=1 … unresolved=0 met=true` **exit 0**.
- **P8** — verdict span deleted from the spot file entirely:
  `… met=true` **exit 0**.

So the counter's green binds the lesson's *quote* of the outside verdict, not
the outside verdict itself: a tree whose unpinned spot-check file says the
opposite (or omits the verdict) stays `met=true`. The contract's C1 kill rule
names "digest-consistent fabrication" as unprovable-trigger; whether
rewriting an unpinned verifier receipt counts is an integrator call, but the
mechanism is exactly the round-63 shape this round claims to have closed:
prose that quotes a verdict whose source is not bound to committed bytes.
Cheapest repair shape (not applied — frozen instrument): add the spot-check
file sha256 at the measured revision to `PIN_SHAS`, and/or derive
`SPOT_VERDICT_SPAN` from the spot file bytes instead of a constant.

## Equivalence-under-pins arguments (E survivors)

- **M02**: reachable only when `pins=1`, i.e. `sha256(blobs["text"]) ==
  TEXT_SHA`; output sha == TEXT_SHA then implies byte-equality to the committed
  blob. Differs only under a sha256 collision.
- **M03**: reachable only when `pins=1`, i.e. the ledger blob is byte-pinned,
  and its `locatedRawLines` is then the constant `6150-6154` == `EXPECTED_LOCATED`;
  the ledger equality subsumes the constant check. Differs only in a
  double-fault that also breaks the ledger pin (M01+M03).
- **M12**: same ledger-pinned-bytes argument for `matchClass`.
- **M13**: reachable only when `pins=1`; the recipe blob is pinned and raw is
  pinned, and `extract()` is deterministic (pure HTMLParser render, verified in
  the committed recipe), so the executed output is fixed to the committed
  text already. Differs only in a double fault that breaks the text pin — note
  the round-63 circular-text-blob kill therefore rests on the **text pin +
  recipe re-execution pair**; neither alone covers it (M13 vs a text-pin-only
  drop).

These four are coverage observations, not contract breaches: the claimed
repairs are made redundant by other pins, which is defense-in-depth working —
but it means the committed controls could not detect if a future edit removed
the redundant check *and* its backup in one commit.

## Method, exact commands

All work under `/fast/scratch/hyaku/kake-r64/MutC1Counter-2/`:

1. `python3 -B <lane>/.ufo/waves/round-64/fixtures/build_fixtures.py $S/fixtures --lane <lane>`
   → stub/marker/fabrication/junk repos (toplevel asserted by the builder);
   ledger-mut-repo built by copying marker-repo, mutating
   `locatedRawLines`, re-init, toplevel asserted.
2. `mutate_c1.py` — 16 `(anchor, replacement)` single-fault edits, each
   asserted to occur exactly once in the frozen source; per mutant runs the
   7-detector suite (T0, base, 4 fixtures, selftest with a fresh
   `--selftest-work` dir) and diffs against the pristine suite.
3. `probes_c1.py` — T0 tree materialized blob-by-blob via
   `git -C <lane> show 4c8295fa…:<rel>` into 9 probe fixture repos, one edit
   each, pristine vs targeted mutant.
4. Frozen sha re-check after all runs (value above, unchanged).

Tooling: **no installs** (operator authorization recorded as unused); Python
3.14.8 (system), git 2.56.0 (system). No mutating git/jj command anywhere; the
lane's `git status --porcelain` shows only untracked files belonging to other
seats (`w1/`, `w1-spec.json`, …), none created by this seat except this
report.

## Verdict

- The 8 seat-named faults: 5 are killed by committed controls (M04 at
  predicate level; M06, M07, M08, and partially M01 at component level —
  M01's predicate survives note-only ledger edits per P5, and M11, the second
  pin-drop probe, likewise survives non-rendered raw edits per P4), M02/M03
  survive as equivalent-under-pins. Of the named eight exactly one —
  **M05 (quote_correction file-level)** — is a true undetected survivor.
- The selftest alone (26/26 green under M02, M03, M05, M06, M09, M10, M12,
  M13, M15) is **not** a kill signal for any prose/presence weakening except
  via the two T4 component expectations (gate0/unresolved); treat selftest
  green as necessary, not sufficient.
- **Findings for the integrator:**
  - **F1 (highest weight):** the round-61 verifier spot-check file is
    unpinned and its verdict span is only mirrored as a constant; P7/P8 keep
    `met=true` after the outside verdict is rewritten or deleted. Candidate
    digest-consistent-fabrication reproduction — C1 kill-rule call.
  - **F2:** four gates have zero isolated committed coverage — SOURCES row
    (M09), ≥1 disagreement (M10), author-side label (M15), block-level
    quote binding (M05); each flips `met=true→false` under pristine on a
    T0+one-edit fixture, so cheap controls exist (e.g. a fifth fixture per
    gate) if the wave wants them.
  - **F3:** raw/ledger pins are each singly-covered only by multi-drift junk;
    single-field drift detection rests entirely on the pins (P4/P5 mutants
    green the predicate), which is acceptable only while both pins stand —
    and M01+M13-style double faults are the next attack to try.
