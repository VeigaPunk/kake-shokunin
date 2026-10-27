# CriticQuoteClass — round-63 C1: does admitting the S432 collapsed-only span violate the round-62 lesson?

Seat: CriticQuoteClass (leaf critic). Scope: attack only the quote-class admission step of
C1 (the S432 field-purpose span admitted as `collapsed-only`); the counter-mechanics attack
belongs to sibling seats. Frozen artifacts were not edited; verified hashes only.
Measured `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`, base `13d4519818db28cd0aa912e49020659140d7b9fa`.

Independent reproduction (read-only, against the fleet repo):

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4…fccb06f
revision=05b0d7f4… disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true   (exit 0)
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818…
… quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 … unresolved=1 met=false   (exit 1)
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4…
present=1 selftest=4/4 frozen_cases=ok met=true   (exit 0)
$ python3 -B scripts/quote_class.py --selftest --json   → 4/4, s432_real derived=expected=collapsed-only
```

sha256 re-verified on disk: counter `bcd16f68…fc91`, ledger `5f48e26b…00c42d`,
tool `431e75e8…841f14`, raw `63b0a018…911b`, flat `8b90d096…2a69` — all match the frozen
contract values. `git diff base..measured -- corpus/SOURCES.md` is 0 lines; the diff is
append-only (`+19669 -0` across 19 files).

Derived facts re-derived from committed bytes (not from the counter's word):

* `python3 -c "quote in raw"` → `quote in raw: False`, `quote in text: True` for
  `.ufo/waves/round-61/sources/S432.html` vs `.ufo/waves/round-63/quote-class/S432.txt`
  → the class really is `collapsed-only` under the round-50 semantics.
* Raw lines 6150–6154 of the retained HTML split the sentence across
  `<p>`, `<dfn …>`, `<code>`, `<a …>` and newlines; raw substrings recover only
  fragments. Both round-62-rejected spans ("Web developers and conformance checkers must
  use the following", "can be used to require checking of a") are raw substrings
  (`True`/`True`) — the old failure was substance, not form.
* The span occurs exactly once in the flat rendering; 21 whitespace tokens (≤ 25).
* `extract_text.py` is deterministic HTMLParser/textContent semantics with
  `convert_charrefs=True` (no double-unescape, cf. round-26 lesson); recipe committed.

---

## Case A — strongest case that the admission VIOLATES the round-62 lesson's reading

A1. The round-62 lesson said what it said, in a committed Gate, twice.
`corpus/lessons/round-62.md` Gate: "Because existing `corpus/QUALITY.md` requires
raw-substring quotes, this round does **not** admit it as a replacement quote and leaves
the S432 knowledge citation unresolved." Its Mistakes fix column: "keep the correction
held while the only complete S432 sentence fails the existing raw-substring rule." Round
63 landed exactly the held correction as green without any round-63 QUALITY.md row
amending the raw-substring bar (the round-63 QUALITY.md addition is a *counter-binding*
criterion, not a quote-admission criterion). A wave does not overrule a prior Gate by
classifying harder; under QUALITY.md's own Admission-authority row (round 20: local
evidence stays local; author-side self-assessment is not promotion authority), flipping
that Gate is the non-author closure's job, not the build's.

A2. The textual basis for the round-62 reading exists, and it post-dates S273.
The round-62 gloss is not invented. `corpus/QUALITY.md` (round-55 criterion, ~line 1162):
"A Gate quote and every quoted span in a new entry is at most 25 units … **a raw
substring of the retained body**, inside the page's content block." Round 51 hardened the
same direction (counter condition C5: each Gate quote a raw substring, after measuring
15 body quotations as 3 raw / 2 whitespace-collapsed-only / 10 markup-bound —
`corpus/lessons/round-51.md:15,96`). Against those two bars, a correction whose quoted
span is *not* a raw substring is hard to distinguish from the cases round 55 stopped
admitting.

A3. The counterexample generalizes too far. If "any span failing raw can be grounded by
a lane-produced flat rendering + ledger", then for every markup-heavy retained source
(RFCs, WHATWG specs) the round-55 bar is voidable at will: the comparison corpus moves
from "retained body" to "lane rendering of retained body", and the lane authors the
renderer (`extract_text.py` round 63). The recipe is committed and deterministic, so one
instance is bounded — but the *authority* conceded is the precedent, and the round-63
lesson records no flip condition for it. A critic must name that: nothing in the corpus
text limits this correction-shaped hole, and a future seat can drive a navigation string
or a ToC line through the same door (round 55's "three page-unique spans" guard was
written for exactly this; the r63 correction is body text, but the precedent text is
loose).

A4. Separability cuts the wrong way for the admission. The contract's separability note
and the r63 lesson make C1's class derivation independent of the C2 tool — good
counter hygiene, but it means the *admission decision itself* has no independent
non-author instrumentation behind it this round; it rests on the author-side gate
(`corpus/lessons/round-63.md`: "This round's own gate decisions … are lane
self-assessment, author-side"). The strongest form of Case A is therefore not "the bytes
don't match" — they do — but "the lane overruled its own recorded Gate without a
criterion amendment and graded the override itself."

## Case B — strongest case that the S273 precedent does not transfer

B1. Different era — S273 is the patient, not the doctor. S273 was admitted at round 49
under a counter that "checked a substring of the collapsed blob only"
(`corpus/lessons/round-50.md` Mistake 2); the round-50 rule was forged *because* that
admission blurred the class. The standing QUALITY.md row names "S273 collapsed-only,
S274 a raw substring" as **examples of the two derived classes**, with a swapped-label
falsifier — a classification instrument, never an admission permission. Citing S273 as
authority for a post-round-55 admission inverts the lesson's polarity: the precedent
text is the record of the defect class, repaired one round later.

B2. No verifier sign-off on round-63's use. The round-49 verifier's "admit/agree" decided
the *row* (with the collapsed status disclosed); the round-50 verifier spot-check
re-derived the *class* of three ids and checked the blur control
(`corpus/lessons/round-50-verifier-spotcheck.md:105-121`). Neither decided "collapsed-only
spans may ground new admissions after round 55." Round 63 has no such signature and says
so itself. A precedent without present verification is an analogy, and the corpus's
round-20 admission-authority row rejects analogy-as-authority for exactly this kind of
promotion.

B3. Different grounding shape. S273's span was verified twice: against the live body
after whitespace collapse and against the committed retained text, with a live re-open
agreeing (`corpus/lessons/round-49-verifier-spotcheck.md:87`). The S432 span is verified
against a *lane-rendered* flat text produced this round; the live re-open
(`corpus/lessons/round-63.md` S432 re-open record) byte-matched the HTML but did not
independently render the live page's textContent. One grounding leg is missing relative
to the precedent.

## Honest counter-reading

C1. No criterion says what the round-62 lesson says. The only raw-substring *requirement*
in QUALITY.md is round 55's, scoped to "a Gate quote and every quoted span in a **new
entry**"; its own rationale is growth-control ("stops the ambiguity from growing"), not a
redefinition of quote truth, and it explicitly leaves its own overrun unresolved rather
than reaching backward. The round-63 correction is an append-only tail to a round-61
entry under a routed defect — not a new entry, not a registry Gate quote. The round-62
lesson gloss "QUALITY.md requires raw-substring quotes" is an overbroad reading of
round 55, and it cannot be grounded in the round-50 rule, which is the corpus's only
quote-class rule and which treats `collapsed-only` as a first-class recorded fact whose
only sin is being blurred into `raw-substring`.

C2. The corpus's older quote-truth bar already compares against visible text. Round 29:
a Gate quote counts when it is an exact substring of "retained **visible** source text"
— "exact substring … means exact after whitespace collapse". The flat rendering is
precisely retained visible text; a digest-pinned span of it is quote-truth-positive under
the pre-existing bar, not under a newly invented one.

C3. Impossibility proves the reading wrong. The routed defect demands "a substantive
located excerpt" of S432. I re-derived: the field-purpose sentence is not a raw
substring of the retained HTML (verified above), and every raw fragment ends before its
object — which is why round 62 rejected them. A reading of the quality bar under which
the routed repair is logically impossible, forever, for any WHATWG-style source, cannot
be the intended reading; and the round-62 lesson itself recorded the state as
"unresolved" (held), not "rejected". Held means the door is open; round 63 walked
through it with the corpus's own instrument.

C4. The admission's hygiene is the strongest the two-class system allows. Class derived
from both blobs inline in the counter (`classify()` in `c63_calibration.py`); recorded
in a committed ledger with both sha256s and the recipe; re-derived by the lane tool as
an independent claim (C2 selftest case `s432_real`); the correction text quotes "in its
located rendering" and states the class is `collapsed-only — never described as a raw
substring`; the live body is byte-identical to the retained blob; the registry row is
untouched (`git diff base..measured -- corpus/SOURCES.md` → 0 lines); the round-62 held
correction survives verbatim above the r63 block. This is S273 done right: the blur the
round-50 rule was written to kill is not present here.

C5. S273 transfers in the only sense that matters. QUALITY.md's standing row cites
"S273 collapsed-only" *inside the operative criterion* as a correct classification
enforced by a swapped-label control. The round-63 claim is not "S273 permits anything";
it is "the round-50 rule — already verifier-signed as a derivation, already in the bar —
governs this span". Era difference noted in B1 is real but cuts against B2's conclusion:
the framework S273 prompted is now the thing being applied.

## Conclusion — reading the non-author closure should apply

Apply the counter-reading (C1–C5): **admit the S432 span as `collapsed-only` under the
round-50 machinery, and reject the round-62 lesson's sentence "QUALITY.md requires
raw-substring quotes" as an overbroad gloss.** The operative bars are (i) round-55's
raw-substring rule in its literal scope — new entries and registry Gate quotes — and
(ii) round-50's no-blur classification rule, which round 63 satisfies in full. The
round-62 Gate's operative holding ("the citation stays unresolved; no substitution
claimed") is satisfied, not violated: the disagreement that made it unresolved is
resolved by the same class the round-50 rule exists to record.

Smallest safe correction — no artifact changes; three closure annotations:

1. In the round-63 closure note, record that the round-62 lesson's raw-substring gloss
   is superseded-in-place by the scope reading above, so a future seat cannot cite
   "QUALITY.md requires raw-substring quotes" as a flat bar against corrections.
2. Bind the extract_text.py recipe: any future change to it re-derives every recorded
   class (round-26's "re-derived after any extractor change" already states the rule;
   name it for this recipe).
3. Keep round 55's bar absolute for *new* entries: this correction-shaped path must not
   become a general rendering-until-match permission; a future source needing it must
   either find a raw span or amend round 55 explicitly, with a verifier-signed class
   derivation like S273's — which is the one piece of the S273 precedent round 63 has
   not yet replicated (no non-author has signed this admission).

Residual exposure closure should weigh before scoring C1 calibration: the admission is
author-side until the non-author closure signs it (the lesson says so); the strongest
fixable defect is not the class but the missing *verification leg* — recommend closure
re-derive the class from committed bytes (command above, exit 0 path) and record the
verdict explicitly, since C1's counter evidence alone cannot promote an admission
authority decision.

## Evidence index

* Round-62 reading attacked: `corpus/lessons/round-62.md` (Gate; Mistakes fix column,
  line 9 raw: "…keep the correction held while the only complete S432 sentence fails the
  existing raw-substring rule").
* Quote-class rule: `corpus/QUALITY.md:1100-1108` (round 50); raw-substring bar:
  `corpus/QUALITY.md` round-55 row ("a raw substring of the retained body"); visible-text
  quote truth: `corpus/QUALITY.md` round-29 row (lines 376-401).
* S273/S274 grounding: `corpus/lessons/round-49-verifier-spotcheck.md:61,87-88`;
  class derivation sign-off: `corpus/lessons/round-50-verifier-spotcheck.md:105-121`;
  blur control `.ufo/waves/round-50/verification/blur-control.txt`.
* Round-63 admission: `corpus/knowledge/response-header-expectations.md:218-251`
  (r62 held block verbatim at 218-220; r63 correction 222-251);
  `corpus/lessons/round-63.md` Gate + "author-side" label; ledger
  `.ufo/waves/round-63/quote-class/quote-classes.json`; retained blobs
  `.ufo/waves/round-61/sources/S432.html:6150-6154`, `.ufo/waves/round-63/quote-class/S432.txt`.
* Receipts re-run: `.ufo/waves/round-63/controls/{after-c1,after-c2,base-c1,base-c2}.txt`
  reproduced byte-for-byte in verdict lines by this seat.
