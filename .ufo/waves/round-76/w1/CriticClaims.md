# CriticClaims — attack on C1 and C2 (kake r76, w1)

Seat: `CriticClaims`. Base `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`. Lane tip at first measurement:
`6b52407b` (amendment 3); re-measured at `d2555766` (amendments 4–7 + the C1 repair `442d36c6`); amended
terms read through amendment 8 (`d00ea7fb`); amendment 5 committed at the final tip `152bffd5`. Contract
and amendments 1–8 read before every counterexample. No model named.

**Provenance warning.** This file quotes the defective C1 spans verbatim so they can be checked. It lives
in `round-76/w1/`, which amendment 5 §D1 / amendment 7 §F1 excludes from the receipt universe, and it is
`.md` outside a receipt directory, so the counter does not read it as a receipt. Copying any block below
into `controls/`, `verification/`, `receipts/`, `cases/`, `fixtures/`, `frozen/`, `resid/`, `sources/`,
`live/`, or into a `.txt/.json/.csv/.log/.out` file **would itself satisfy C1** — that is the tautology the
round had to close, not a repair.

Method: every counterexample runs in `git clone --shared` under
`/fast/scratch/hyaku/kake-r76/CriticClaims` (`TMPDIR` and every `--work` inside that scratch), against
committed objects; the lane checkout was only read. Scratch removed at seat close.

---

## 1. Do-nothing control

### C1 — red at base, red again under the amended universe; the v1 counter still says green for the wrong reason

| State / predicate | Exact command | Observed |
|---|---|---|
| base `a0491fcd`, v1 counter | `python3 -B c76_quote_truth.py --root <clone> --revision a0491fcd… --base a0491fcd… --rounds 75,76` | `C1v1 revision=a0491fcd rows=19 receipt_files=10452 spans=30 exempted=0 corrections=0 findings=8 met=false`, exit 1 |
| tip `6b52407b`, **nothing added**, v1 | same, `--revision 6b52407b` | `C1v1 revision=6b52407b rows=19 receipt_files=10460 spans=30 exempted=0 corrections=0 findings=0 met=true`, exit 0 |
| tip `d2555766`, **repair rows present**, v1 | same, `--revision d2555766` | `C1v1 revision=d2555766 rows=26 receipt_files=10460 spans=30 exempted=0 corrections=7 findings=0 met=true`, exit 0 |
| base and tip, **amended receipt universe** (A3 B1–B6, A4, A5 D1–D3, A7 F1) | probe in Appendix A | base receipts `7757`, tip `7759`; all **6 unique** span texts absent at **both** revisions |

The middle row is the counterexample that amendments 4 and 5 now cite as their motivation: committing the
round's own failing transcript made every span contiguous, because each diagnostic line ends with the span
it reports as absent, e.g. `controls/base-c1-quote-truth.txt:2`:

```
  T1 SCORECARD.md:4892 files=18 mismatches=0 append_only=true met=true missing_frozen=0
```

I confirmed causality by re-running the same HEAD tree with `/round-76/controls/` removed from the receipt
universe only: `receipt_files=10452 spans=30 exempted=0 corrections=0 findings=8 met=False`.

**Amendments 4 + 5 close it in terms, and I re-verified the closure.** The amended universe admits only
files under receipts directories, excludes this round's `base-c1-quote-truth*`/`ctl-*`, excludes the newest
measured round's `w1/`, and strips `T1|T2|T4|A1 file:line` diagnostic lines. Under that universe all six
unique span texts are absent from every receipt at **both** the base and the repair tip — so the do-nothing
state is red under the amended predicate, and the after-state now requires the repair. The seven repair
rows are substantive: each names its defective span and quotes a whole receipt line that my probe found
verbatim at the cited file:line (six distinct whole lines across seven rows: rows 1 and 5 share one, row 3
quotes two, the QUALITY and lesson corrections share one; row 3's second line is `after-c2-receipts.txt:6`). The v1 `findings=0` at the tip is still produced by the old tautology; the
amended predicate also returns 0, but only because the repair rows are valid. A v1 green receipt therefore
does not evidence the amended predicate.

Residual defects at the tip (measured):

1. **No delivered amended counter.** `scripts/doc_quote_truth.py` is absent
   (`git ls-tree -r --name-only HEAD -- scripts/doc_quote_truth.py` → empty) and
   `c76_quote_truth.py` is byte-identical to the freeze blob `627ac245…`. The only executable counter is
   the v1 one, which does **not** implement A3 B1–B6, A4, A5 D1–D3, or A7 F1. Its tip verdict is
   therefore not evidence for the amended predicate.
2. **Amendment 5 was untracked when the terms above were first measured; it is committed at the final tip.**
   At `d2555766` `git ls-files .ufo/waves/round-76/amendment-5.md` was empty and amendment 7 already cited it
   as standing terms; at `152bffd5` (seat close) it is committed. That ordering defect is closed; the
   missing counter and receipt below are not.
3. **The re-measured receipt is untracked and shows the superseded number.** On disk,
   `controls/base-c1-quote-truth-v2.txt` reads
   `C1v2 revision=a0491fcd rows=16 receipt_files=7724 spans=25 exempted=0 corrections=0 findings=9 met=false`
   — the pre-F1 (D1-over-exclusion) build, not the `findings=7` that A3 B6, A5 D4 and A7 F2 assert. No
   receipt anywhere shows 7.

### C2 — do-nothing is genuinely red

At base the tool does not exist and no round-76 matrix exists:

```
$ test -e scripts/hreflang_audit.py    -> absent
$ python3 -B scripts/hreflang_audit.py --selftest --work …
python3: can't open file '…/scripts/hreflang_audit.py': [Errno 2] No such file or directory
exit=2
$ git ls-tree -r --name-only a0491fcd | grep -E 'round-76/.*(hreflang|matrix)'  -> none
```

No tool → no parseable JSON → 0 cases decided, 0 correct. C2 cannot be reached by doing nothing. The
delivered artifacts live only in the untracked `w1/` tree (see §2), so no committed after-state exists at
the tip either.

---

## 2. Predicate fidelity

### C1

Contract predicate (`contract.md:44`): `met = (findings == 0) and append_only`.

| Surface | Text | Verdict |
|---|---|---|
| contract | `met = (findings == 0) and append_only`; findings `T1,T2,T4,A1` (`contract.md:39-44`) | reference |
| counter code | `"met": len(findings) == 0 and append_only` (`c76_quote_truth.py:303`) | **matches** |
| counter docstring | `met = (findings == 0)` (`:23`) — omits append-only | **diverges** |
| counter docstring | `8-64` hex (`:10`) and `7-40` hex (`:17`); contract says 7–64 (`:28-30`) | **diverges** |
| counter docstring | documents ids `T5`, `E`, `T3`; the code emits only `A1,T1,T2,T4` (grep) | **diverges** |
| receipt label | `C1v1 revision=master …` (`controls/base-c1-quote-truth.txt:1`), not the hash | **diverges** |

The label divergence is executable: the receipt's own command with `--revision master` at the tip now
prints the opposite verdict. The receipt does not identify the tree it measured.

Population, v1 code (before B2): `sections()` accepts any heading level whose title matches
`round[- ]?75` (`:122-139`; patterns in `rows_for` `:200-218`), so `SCORECARD.md:4899/4904/4905` are
collected under both `## Round 75` (`:4882`) and `### Capabilities acquired in round 75` (`:4895`):

```
rows enumerated = 19   unique(file,line) = 16
spans enumerated = 30  unique(file,line,span) = 25
base findings = 8      unique(file,line,detail) = 7   unique span texts = 6
```

So the v1 before-numbers are inflated by three duplicate physical rows and one duplicate finding
(`SCORECARD.md:4904` twice), over six unique span texts. Amendment 3 B2 fixes this in terms; the delivered
v1 counter still double-counts (tip `rows=26` includes this defect), and the untracked v2 receipt `rows=16`
shows the corrected population.

Amended predicate vs delivered instrument:

- A3 B1–B6, A4, A5 D1–D3, A7 F1 are not implemented by any delivered counter (blob unchanged; contract
  command absent). The contract sentence and the only runnable code still diverge on the receipt universe,
  section identity, append-only exactness, `*.ready*`, and the whole-line correction rule.
- A5 D5 requires the delivered counter's selftest to be green; there is no delivered counter to test.
- The v1 docstring documents a different predicate (`met = (findings == 0)`; `T5/E/T3`). If the wave copies
  v1 to `scripts/doc_quote_truth.py` without rewriting the docstring, the "same predicate" acceptance bar
  fails on the file's own text.

### C2

Amended claim sentence (contract `:69-71` + amendments 1, 2, 6): *every decided case correct AND every
constant fails ≥1 case AND selftest green AND the 8-page real-input run recorded.* Amendment 2 A16 adds:
parseable JSON carrying `version`, `pages` (== manifest count), `findings`, `counts`, `exit`; a no-output
run is a failed case; ids compared as a **multiset**.

Matrix `met` (`c76_hreflang_matrix.py:353-358`):

```
met = (wrong == 0 and decided >= min_decided
       and constants_failed == len(constants)
       and not matrix_defect and decided > 0)
```

Divergences from the claim predicate:

1. **The tool's selftest is not a conjunct.** `emit_run` never invokes `--selftest`. A matrix can print
   `met=true` while the tool selftest is red. That state was real during this seat: at tool hash
   `0a2454c6…` the selftest printed `selftest 33/38 passed`, exit 1; at `f4b9a163…` it aborted with
   `KeyError: 'external_dirs'`; at `e13bd80a…` it printed `56/56`; at the bytes current at seat close
   (`0762452f…`) it printed `59/59`, exit 0.
2. **The four constants are not required.** `discover_constants` (`:319-324`) requires ≥1 `const_*.py`, not
   the four named ones; `constants_failed == len(constants)` is satisfied by one. Measured: one case, one
   constant, `--min-decided 1` → `cases=1 decided=1 correct=1 wrong=0 … constants_failed=1/1 met=true`,
   exit 0.
3. **`--min-decided` is caller-controlled.** `met=true` does not imply ≥24 cases; the run above printed
   `met=true` with `decided=1`. The receipt must be read for `decided`, not for `met`.
4. A16 is otherwise implemented correctly at the current bytes (credited): `observed_report` requires all
   five keys, checks `pages` against the manifest, checks JSON `exit` == process exit, and accumulates ids
   in a `collections.Counter`. A shape-incomplete or one-id stub is scored `wrong`.

Tool vs amendments (tool `sha256 0762452f…`; matrix `sha256 4958ede0…`):

| Probe | Command | Observed | Reading |
|---|---|---|---|
| A13/A14 scanner | `tool --manifest fx13/manifest.json --root fx13 --json` | exit 1, ids `2× hreflang_invalid_tag, 2× hreflang_external_target` | svg/math/template/comment/script/style skipped; `<noscript>` scanned; `<svg/>` opens nothing — **matches A13/A14** |
| A4 antecedent | `fxrel`: one page, canonical self, one relative alternate | exit 1, ids `hreflang_relative_href, hreflang_self_missing` | A4 says the relative href "contributes to no other finding (self-reference…)"; it does not say whether it counts toward "≥1 hreflang alternate". **Undecidable** |
| duplicate equality | `fxdup`: same tag, hrefs `https://a.test` and `https://a.test/` | exit 0, ids `[]` | contract says "same (lowercased tag, **exact href**)" (`:85`); A3 says URL equality is RFC-3986-normalized with empty path → `/`. **Contract and amendment collide; the tool picked the contract.** |

Live disagreement between two implementations of the same contract, from the real-run seat's own
`receipts/differential-probe.txt`:

```
[p3_two_xdefault_same_href] agree=false
  tool exit=1 ids=['hreflang_duplicate_pair','hreflang_multiple_xdefault','hreflang_multiple_xdefault']
  ref  exit=1 ids=['hreflang_duplicate_pair','hreflang_multiple_xdefault']
```

Amendment 6 §E2 now decides the x-default side (once per x-default element), so this specific split is
resolved in terms; the tool's 2× is the amended reading. `duplicate_pair` multiplicity on three identical
links remains undecided (A2's "offending annotation" is still undefined for that predicate).

**Classes that remain undecidable after amendments 6 and 8** (kill rule 1 must mark them `undecided`).
Amendment 8 §G3 records three; the other five are additions from this seat:

1. A4 antecedent: does a non-absolute alternate count toward "a page with ≥1 hreflang alternate" for
   `self_missing` / `canonical_not_self`?
2. `duplicate_pair` equality: contract "exact href" vs A3 normalized URL equality (verdict-changing).
3. `duplicate_pair` multiplicity with ≥3 identical links: which links are "offending"? A6 §E2 fixes only
   `multiple_xdefault`.
4. `hreflang_nonreciprocal` when the manifest-internal target B is unreadable: A8 says unreadable pages
   contribute no policy findings, but the finding is emitted on readable A about B.
5. Self-reference credit from an invalid-tag annotation that carries the page's own URL: A2/A3 never say
   whether an invalid annotation counts for `self_missing`.
6. href whitespace asymmetry (A8 §G3): is `href=" https://a.test/ "` trimmed before the absolute-URL test?
7. shared-file fault id (A8 §G3): A15 prohibits two pages sharing a `file` but assigns no input id; the
   tool emits `input_unreadable`, the matrix marks the case `undecided`.
8. crossing/encoding policy (A8 §G3): unclosed foreign-content crossing and the UTF-8/latin-1 fallback are
   tool choices A13 does not fix.

Amendment 6 §E1 decides the relative-canonical question (no canonical finding) and §E2 decides x-default
multiplicity per element, so both are removed from the list. Amendment 8 §G2 binds the wording of the
capability row and knowledge entry ("frozen ASCII grammar validator for BCP-47-shaped tags", never "BCP-47
validator"); that is a report/knowledge constraint, not a tool behavior.

---

## 3. Axis honesty

**C1 (calibration, score 2).** The historical rows are not rewritten (kill rule 3), so the repair is an
annotation layer: seven correction rows that name the exact splices (`classes=-`, `met=false`,
`worktree=identical`, …) and quote the true whole lines. That is a real recalibration of *traceability* —
after the repair, each defective quote has a named receipt line that shows what the row should have said.
It is not bookkeeping: the rows identify the missing fields, and the amended universe makes the before red
again. The remaining honesty gap is evidential, not semantic: the amended counter is not delivered
(`scripts/doc_quote_truth.py` absent) and the only re-measured receipt on disk shows the superseded
`findings=9`, not the asserted 7. Amendment 5 was untracked at `d2555766` and is committed at `152bffd5`. So C1's after-state is defensible **only if** the
L1 lands the amended counter with a green selftest and a committed receipt that shows `findings=0
corrections=7 exempted=7`. A v1 green receipt at the tip would prove nothing.

**C2 (operability, score 10).** Not bookkeeping: at base there is no tool and no cases; the delivered
artifact is a real auditor. On the current untracked bytes the tool parses the amended structure classes
correctly (`fx13`), emits the A16 shape, and the real-input receipt reads 8 pages with 8/8 retained
sha256 matches and exit 0. At matrix `4958ede0…` and tool `0762452f…` the matrix prints `cases=71
decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true` (earlier, `b8333969…`: 69/66/3,
also met). So the artifact would move the axis **if landed with those receipts**. The gap is in the
predicate, not the capability: the matrix's `met` does not prove the claim's conjuncts (selftest omitted,
constant count and case floor caller-controlled), and "every frozen contract case" is quantified over cases
the author chose — the ambiguous classes above are absent rather than marked `undecided`, so 69/69 does not
cover them.

Not claimed closed, but worth the judge's line: unlike round-75 C2 (instruments bound to a committed digest
receipt), nothing in C2 requires the new tool to enter the instrument population or `SKILL.md`. The
capability exists on disk; the lane's operability surface is not bound to it.

---

## 4. Junk-row check

Cheapest states a lazy author might commit:

| Junk state | Exact/observed | Verdict |
|---|---|---|
| plausible `[r76-correction]` rows, fabricated spans, no quotes | base-receipts-only run: `rows=21 … findings=10 met=false` (8 T1 + 2 T4), exit 1 | **red, correct** |
| validated quote that names no defective span (launder) | `corrections=1 exempted=0 findings=8 met=false`, exit 1 | **red, correct** |
| one row naming all spans + `findings=0` | v1 rules: `exempted=8 corrections=1 findings=0 met=true`; under B3 `findings=0` is not a whole receipt line, so this specific row is T1 | **v1 hole; closed by B3** |
| one row naming a defect + quoting any whole line | B3 accepts any line: `## Gate` is a whole line in **8** amended receipts (first: `.ufo/waves/round-21/frozen/before/corpus/lessons/round-20.md:41`) | **still green under B3** |
| nothing at all | amended universe: all six span texts absent at base and tip | **red, correct** |

So the emptiest state is no longer green (amendments 4+5), and B3 closes fragment-only closure. What
survives is relevance: B3 requires a whole receipt line but not the *right* line. A correction row that
names the span (exempted via B3-bis because it is a base T1) and quotes `## Gate` satisfies the letter
while saying nothing about the claim. The delivered repair does not exploit this — all seven rows
quote the correct lines — but the predicate does not stop a lazy author from doing so.

C2 junk — expected verdicts copied from the tool's own output. Measured with a shape-complete stub and the
delivered matrix: one case whose expected ids equal the stub's output, one `const_*.py`, `--min-decided 1`
→ `met=true`, exit 0. Nothing in the matrix records that the expectation was copied rather than derived;
A16's shape/multiset rules do not help because both sides come from the same implementation. The delivered
matrix does carry two `undecided` cases — the right handling under kill rule 1 — but the §2 ambiguous
classes are simply not present, so the 69/69 does not constrain them.

---

## 5. Strongest reason each claim could still be wrong after landing

**C1.** The amended predicate is sound in terms and the repair rows are honest, but no delivered executable
implements it: the contract command is absent, the counter blob is the v1 tautology, and the only
re-measured receipt on disk shows the superseded `findings=9` (amendment 5 itself is committed at
`152bffd5`). A green v1 run at
the tip is exactly what the tautology produced, so it cannot be the acceptance receipt. If the L1 lands
`scripts/doc_quote_truth.py` without A3–A5, C1's receipt is vacuous; if it lands the amended counter with a
committed v2 receipt showing `findings=0 corrections=7`, C1 is defensible subject only to the B3 relevance
hole above.

**C2.** The matrix's `met` is not the claim's predicate: it omits the tool's selftest, accepts any number of
constants, and honours a caller-chosen case minimum. A green C2 receipt can therefore coexist with a red
selftest, a one-case matrix, or one constant. The current bytes happen to satisfy the stronger reading
(59/59, 69 decided, 4/4 constants, 8-page run), but the receipt's own `met` would not prove it, and the
cheapest way to keep it green is to align expectations with the tool's output — which is exactly what the
five red selftest cases at hash `0a2454c6…` invited.

---

## Appendix A — probes and time-scoped artifacts

Amended-universe probe (not a counter): receipts = committed files under a receipts directory
(`controls/verification/resid/receipts/frozen/fixtures/cases/sources/live`) of any round; exclude
`round-76/w1/`; exclude `round-76/controls/base-c1-quote-truth*` and `ctl-*`; strip lines matching
`^\s*(T1|T2|T4|A1)\s+\S+:\d+\s`; data-extension files outside a receipts directory excluded. Observed:

```
base a0491fcd amended receipts=7757   tip d2555766 amended receipts=7759
all 6 unique span texts: absent at BOTH revisions
repair rows: 7 named defects, 6 distinct whole receipt lines across 7 rows, every quoted line found at
the cited receipt file:line (after-c2-receipts.txt:5, :6, :7; ctl-deletion.txt:1;
ctl-deletion-landed.txt:3; after-c1-row-truth.txt:4)
```

The v2 receipt on disk (untracked): `C1v2 revision=a0491fcd rows=16 receipt_files=7724 spans=25
exempted=0 corrections=0 findings=9 met=false` — the D1-over-exclusion build, not the asserted 7.
`amendment-5.md` was untracked at `d2555766` and is committed at `152bffd5`; `scripts/doc_quote_truth.py`
is absent at both; the counter blob is `627ac245…`.

C2 artifacts are untracked and were edited during this seat:

| Bytes | sha256 | Observed |
|---|---|---|
| `ExecAuditTool/hreflang_audit.py` | `0a2454c6…` | `selftest 33/38 passed`, exit 1; five failures named in §Appendix B |
| same | `f4b9a163…` | selftest aborts: `KeyError: 'external_dirs'` in `_write_case`, exit 1 |
| same | `e13bd80a…` | `selftest 56/56 passed`, exit 0 |
| same | `0762452f…` (current at seat close) | `selftest 59/59 passed`, exit 0 |
| `ExecAuditMatrix/c76_hreflang_matrix.py` | `b8333969…` measured; `4958ede0…` current | `69/66/3` then `71/69/2` decided/correct/undecided, `constants_failed=4/4 met=true`, exit 0 both times |
| `ExecAuditRealRun/receipts/*` | untracked | 8-page run: `pages=8 findings=[] exit=0`; `sha256-check.txt` 8 retained `true`, 4 absent `n/a`; absent surfaces run: `exit=2` with 4× `input_unreadable` |

Four of the five failures at `0a2454c6…` are stale expectations contradicting amendments, not tool defects:
`relative_href_scheme_relative_red` (A4 forbids the external-target side effect it expected),
`relative_href_absent_red` (A9 says a link without href is not an alternate and is not reported),
`multiple_xdefault_red` (A2 plus A6 §E2), `alternate_stylesheet_red` (A13 says `alternate stylesheet` is
not an alternate). Only `relative_href_red` is the genuine A4-antecedent ambiguity (undecidable class 1),
where the tool's `relative_href + self_missing` is one defensible reading and the selftest's
`relative_href` the other.

Amendment 1's "four not-served surfaces … never counted as clean or as an error" is contradicted by the
delivered `absent-surfaces-run.txt`, which runs a 12-page manifest and observes `exit=2` with 4×
`input_unreadable`. The 8-page run itself is clean (`exit=0`), so the real-input conjunct is met; the
absent-surface record counts the four as input faults, which amendment 1 forbids.

## Appendix B — smallest safe corrections

1. **C1 instrument.** Land `scripts/doc_quote_truth.py` implementing A3 B1–B6, A4, A5 D1–D3, A7 F1, with a
   docstring that states `met = (findings == 0) and append_only` and the ids it actually emits; ship a
   selftest that exits 0 with every case executed (A5 D5).
2. **C1 provenance.** Commit a `base-c1-quote-truth-v2.txt` produced by the delivered counter at
   `a0491fcd`; the on-disk receipt is the superseded `findings=9` build. The assertion `findings=7` still
   has no committed receipt (amendment 5 itself is committed at `152bffd5`).
3. **C1 B3 relevance.** Scope the whole-line quote to the receipt named in the row's counting-command cell,
   not "any whole receipt line"; `## Gate` currently satisfies it.
4. **C1 receipt label.** Record the measured hash, not `master`, in every before/after receipt.
5. **C2 `met`.** Require, hard-coded: the tool's `--selftest` exit 0 with ≥20 cases; exactly the four named
   constants present and each failing ≥1 case; `decided >= 24`; and record the tool sha256 and selftest
   output in the receipt. Remove or floor `--min-decided`.
6. **C2 derivability.** Require each case to carry the contract/amendment line that decides it (the scout's
   matrix skeleton already does this) and forbid expectations generated from the tool. Mark the eight
   remaining undecidable classes `undecided` rather than omitting them; `duplicate_pair` equality and the
   A4 antecedent in particular cannot be scored consistently without a ruling.
