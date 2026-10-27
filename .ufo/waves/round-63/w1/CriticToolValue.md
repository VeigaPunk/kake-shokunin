# CriticToolValue — YAGNI attack on `scripts/quote_class.py` (round 63, C2)

Seat: CriticToolValue (critic, leaf). Claim under attack: C2 operability —
`scripts/quote_class.py` (frozen sha256 `431e75e8…41f14`) is a genuinely
operability-improving artifact and not dead weight. Method: steelman the YAGNI
case, test it against local evidence, weigh against the capability-table
precedent, conclude. No fleet files were edited; the only writes are this
report and an empty scratch dir (removed). No tools installed.

## Verdict

The YAGNI case fails against the lane's own operability definition and the
committed receipts: the tool is **genuinely operability-improving as measured**
— a runnable artifact with a committed green run at the measured revision and a
red do-nothing at base, filling a defect class round 50 left `captured-by:
none`. But the attack lands **three fixable defects**: (1) the tool's
`classify` is raw-anchored while the frozen round-50 counter it claims to
implement is text-anchored — they diverge on markup-bearing quotes; (2) the
round-63 lesson falsely states the C1 counter "consumes" the tool, contradicting
the contract's separability clause; (3) the capability-table precedent means the
tool earns capability credit only when the round-63 closure enters a row — as
of the measured commit no row exists, so the credit is prospective, not
admitted. None of the three breaches a kill rule; C1 and C2 receipts stand.

## 1. The YAGNI case, steelmanned

**(a) The counter already inlines the tool's entire logic.**
`.ufo/waves/round-63/c63_calibration.py:51-55` carries a `classify` that is
byte-identical to `scripts/quote_class.py:32-38`:

```python
if quote in raw:
    return "raw-substring"
if quote in text:
    return "collapsed-only"
return "absent"
```

The contract's Separability section states C1 "never gates on
`scripts/quote_class.py`" and C2's counter "only reads the tool and its
selftest". So the derivation the tool exists to perform is duplicated inside
the frozen judge, and the judge never calls the tool.

**(b) `extract_text.py` already exists, and the ledger records the result.**
The derivation chain for the only real case (S432) is fully reproducible
without the tool: retained blobs → `extract_text.py` recipe → flat text →
3-line substring test → `quote-classes.json` ledger with both blob digests.
The knowledge entry (`corpus/knowledge/response-header-expectations.md:222-247`)
cites exactly this chain.

**(c) The tool is a fourth artifact in a chain of three.**
Blobs, recipe, ledger — then tool. It is sha-frozen and already cost one
pre-wave re-freeze: the contract freeze note records the sha changing
`40655dd8…f88a1` → `431e75e8…41f14` solely because the selftest resolved
fixtures against its own file location, which the C2 counter's scratch-copy
run cannot see; commit `05b0d7f4` fixed exactly one line
(`LANE_ROOT = Path(__file__).resolve().parent.parent` → `Path.cwd()`,
`git show 05b0d7f4 -- scripts/quote_class.py`). The artifact's only runner is
its own counter, and its first revision was incompatible with that runner —
shaped by the counter, not by a user.

**(d) Selftest cargo out of proportion to the logic protected.** 147 lines of
tool plus four fixture files guard a 3-line function. Three of four selftest
cases are one-line toy fixtures (`scripts/fixtures/quote-class/inline.*`,
`markup.*`); the one real case (`s432_real`) re-checks the same two blobs the
C1 counter already gates on.

**(e) Zero organic consumers.** Repo-wide grep: outside `.ufo/waves/round-63/`
and the C2 counter, nothing imports, shells out to, or links the tool. Its
single corpus citation is the r63-correction block itself
(`response-header-expectations.md:240-241`). The tool's only exercised purpose
is to be measured by `c63_quote_tool.py` — a circular justification: land an
artifact so a counter can count it.

## 2. Counterevidence — why the steelman fails here

**(a) The frozen predicate and receipts are the operability definition.**
AXES.md:13 defines operability as "Runnable artifacts: checklists that are
executable, commands that exist, scripts that run… A checklist item can be run
and produces the stated outcome." C2's predicate is exactly that. Reproduced
this session, read-only:

```
$ python3 -B scripts/quote_class.py --selftest
selftest 4/4                                    exit=0
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
present=1 selftest=4/4 frozen_cases=ok met=true exit=0
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
present=0 selftest=unevaluable met=false        exit=1
```

matching the committed receipts `controls/after-c2.txt` and
`controls/base-c2.txt` byte-for-byte. A do-nothing tree cannot reach met; a
stub tool is rejected by the frozen-case-set check. Whatever else the tool is,
it is a demonstrated runnable artifact — the axis signal AXES names.

**(b) YAGNI presumes the need is not real; here it recurred.**
`corpus/lessons/round-50.md:27` records class "quote class blurred …
captured-by: none" — and the round-61 S432 disagreement is the same class
recurring. A defect recorded once with no capturer, then re-observed, is the
strongest local refutation of "you aren't gonna need it". The tool is the
captured-by that round 50 lacked.

**(c) House idiom.** `scripts/` holds ~30 runnable tools, most with
`--selftest`; several (canonical, base-path, link-preview, robots, sitemap,
header audits) pair a script with a wave counter exactly as C2 does. On this
evidence, a small script + selftest is the lane's standard response to a
standing operational need, not a novelty.

**(d) Distinct authorities — no duplicate authority.** The four artifacts do
not hold the same power: `extract_text.py` is the recipe (how text derives),
`quote-classes.json` is the recorded fact (class + digests), the counters are
frozen judges (gate claims), the tool is the generic operational interface
(any `--quote/--raw/--text`). The counter never calls the tool; the tool never
writes the ledger. Duplication of a 3-line function across a frozen judge and
its human-facing interface is the same pattern as every other scripts/ tool
whose semantics a counter re-checks; it is not two authorities issuing verdicts
over the same fact.

**(e) The tool reproduces the precedent corpus.** Driving both `classify`
implementations over the three round-50 real ids:

```
S273: ledger=collapsed-only  tool=collapsed-only  c50=collapsed-only
S274: ledger=raw-substring   tool=raw-substring   c50=raw-substring
S286: ledger=raw-substring   tool=raw-substring   c50=raw-substring
```

and the CLI works end-to-end on a real id:
`python3 -B scripts/quote_class.py classify --quote "It reduces your site's crawl rate across the whole hostname" --raw .ufo/waves/round-49/sources/S274.raw.html --text .ufo/waves/round-49/sources/S274.txt` → `derived=raw-substring`, exit 0.

## 3. The capability-table precedent

AXES.md:62-64: rows enter only through a round that demonstrates the
capability running; "a capability without a passing demonstration in the round
report is pre-claiming and does not enter the table." SCORECARD.md:215-216
repeats it. Applied here:

- A quote-class capability row **already exists** — SCORECARD.md:204,
  "Quote-class ledger for cited source spans", evidenced by the round-50
  counter. The tool does not create a new capability kind; it operationalizes
  an existing one. A second row would need to justify itself as an extension,
  or the closure should update the round-50 row's evidence pointer.
- The round-63 wave is in flight: no SCORECARD round-63 row, no LOG entry yet.
  So as of the measured commit the tool is **demonstrated but uncredentialed**.
  Precedent says that is not a defect: round-22 kept a working tool out of the
  table deliberately (`.ufo/waves/round-22/w2/FalsifyPolicy.md:40-43`) and the
  residual review flagged only the converse — claiming a capability without a
  demonstration (`.ufo/waves/round-22/residual/CritAdmission.md:49-50`).
- `after-c2.txt` is exactly the "passing demonstration in the round report"
  the rule requires; the row itself is closure-time bookkeeping.

Net: the precedent neither brands the tool dead weight nor admits it yet. It
sets the condition under which C2's operability credit becomes durable: the
round-63 closure must enter (or extend) the row with the after-c2 evidence
pointer.

## 4. Strongest counterexample found — the anchor divergence (fixable defect)

The tool's docstring (`scripts/quote_class.py:4`) claims it "derives the
round-50 match class of a quoted span". It does not, on one reachable quadrant.
The frozen round-50 counter anchors on text (`.ufo/waves/round-50/c50_quote_class.py:100-106`):

```python
if quote not in text:
    return "absent"
if quote in raw:
    return "raw-substring"
return "collapsed-only"
```

The tool (and the byte-identical copy inlined in `c63_calibration.py:51-55`)
anchors on raw. For any quote that is a substring of the retained HTML but
does not survive into the flat rendering, the two committed semantics give
different labels. Probe against committed blobs (read-only, this session):

```
quote='response</a>’s'   in_raw=True  in_text=False
  tool classify  -> raw-substring   (scripts/quote_class.py CLI, exit 0)
  c50 classify   -> absent          (imported from .ufo/waves/round-50/c50_quote_class.py)
```

The S432 frozen quote sits in the `collapsed-only` quadrant where both anchors
agree, which is why no receipt is affected:

- C1 at measured: `disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`, exit 0 — reproduced.
- C1 at base `13d45198…`: `met=false`, exit 1 — reproduced.
- All four frozen shas re-derived at `05b0d7f4…`: tool `431e75e8…41f14`, c63_calibration `bcd16f68…3fc91`, ledger `5f48e26b…0c42d`, c63_quote_tool `9fcbfad0…7f01e` — all match the contract.

So the divergence is **immaterial to the frozen claims** (fixable defect, not a
tradeoff the judge must reject). But it is real: had a future seat recorded a
markup-bearing span in a round-50-style ledger, the tool would call it
`raw-substring` while the frozen round-50 counter would fail it as `absent` —
the exact "swapped label" failure class QUALITY.md:1100-1108 warns about, and
nothing in the tree would have caught it, because nothing exercises the tool
against the precedent beyond the one agreeing case. That nothing caught it is
itself corroboration that the tool is not yet load-bearing for its stated
general purpose — the one point where the YAGNI case retains teeth.

## 5. Secondary defects

1. `corpus/lessons/round-63.md:14-16` — "the committed quote-class derivation
   tool … that the C1 counter consumes". False under the contract's
   Separability clause and `c63_calibration.py:51-56`'s own docstring ("never
   as a C1 gate"). Prose overstates coupling; fix the wording.
2. Capability row not yet entered (§3). Closure-time action, not a claim
   defect.
3. Fixture binding to `Path.cwd()` means the selftest only passes when invoked
   from the lane root — a documented consequence of the pre-wave re-freeze, but
   it narrows the tool's operability surface (running it from any other cwd
   fails its own selftest). Acceptable for a lane tool; worth a line in the
   closure.

## 6. Conclusion

- **Dead weight? No — as measured.** Under AXES operability and the frozen
  predicate, a script that exists, runs, self-verifies 4/4 at the measured
  revision, and is absent (red) at base is the axis's named signal. The YAGNI
  premises "the counter inlines it" and "extract_text.py exists" are true and
  were verified, but they show functional overlap, not redundancy of
  authority; and the need is demonstrably recurring, not hypothetical.
- **Genuinely operability-improving? Conditionally yes.** The improvement is
  durable only if the closure enters the capability-table row (extend the
  round-50 quote-class row) with the after-c2 evidence pointer; otherwise the
  demonstration stands but the capability credit does not, per the precedent.
- **Smallest safe corrections** (none touches the frozen claims):
  1. Reconcile the anchor: next round, either make the tool text-anchored to
     match the frozen round-50 counter, or record in QUALITY.md/lesson that
     round-63 semantics are raw-anchored and that the two agree on all
     rendered-prose quotes (the only quotes the corpus cites), differing only
     on markup-bearing spans.
  2. Fix `corpus/lessons/round-63.md:14-16`: the C1 counter re-derives inline
     and never consumes the tool (contract Separability).
  3. At closure, enter/extend the SCORECARD capability row for quote-class
     derivation citing `controls/after-c2.txt`.

## Evidence index (all commands run read-only; fleet untouched)

- Receipt reproduction: c63_quote_tool.py @ `05b0d7f4…` → `present=1 selftest=4/4 frozen_cases=ok met=true` exit 0; @ `13d45198…` → `present=0 … met=false` exit 1. c63_calibration.py @ `05b0d7f4…` → `met=true` exit 0; @ base → `met=false` exit 1.
- Selftest: `python3 -B scripts/quote_class.py --selftest` → `selftest 4/4`, exit 0 (from lane root, cwd-bound fixtures).
- Sha re-derivation at `05b0d7f4…` via `git show <rev>:<path> | sha256sum` — all four match the contract.
- Base absence: `git ls-tree 13d45198… scripts/quote_class.py` → no entry; counter prints `present=0`.
- Divergence probe: `python3 -B scripts/quote_class.py classify --quote "response</a>’s" --raw .ufo/waves/round-61/sources/S432.html --text .ufo/waves/round-63/quote-class/S432.txt` → `derived=raw-substring` exit 0; imported `c50.classify` on identical inputs → `absent`.
- Round-50 id cross-check: S273/S274/S286 via tool and c50 — all three equal the ledger.
- Consumers: `grep -rn quote_class corpus/ scripts/` → tool referenced only in the r63-correction block (`corpus/knowledge/response-header-expectations.md:240-241`); no code consumer besides `c63_quote_tool.py`.
- Precedent texts: AXES.md:13, :57-64; SCORECARD.md:191-216 (row at :204);
  `.ufo/waves/round-22/residual/CritAdmission.md:49-50`;
  `.ufo/waves/round-22/w2/FalsifyPolicy.md:40-43`;
  `corpus/lessons/round-50.md:27`; corpus/QUALITY.md:1100-1108;
  `.ufo/waves/round-63/contract.md` §Separability;
  freeze note + `git show 05b0d7f4 -- scripts/quote_class.py` (one-line cwd fix).
- Installs: none. Writes: this report only (scratch dir
  `/fast/scratch/hyaku/kake-r63/CriticToolValue` created empty and removed).
