# ScribeQualityScope — round 62 (kake)

Seat: advisory scribe, leaf member, no subagent dispatch. Item: *review proposed criterion
scope for web-property publishing evidence; ensure it is domain-specific and not generic
source-method duplication owned by chousa. Do not edit files.*

Behavior: read-only on every lane file. No claim, counter, criterion, criterion draft,
score or Git/jj state was written or altered. The only artifact written is this report.
Scratch `/fast/scratch/hyaku/kake-r62/ScribeQualityScope/` was created and left unused
(no command needed it); deleted before yield. No installs, no pacman, no network fetch,
no counter execution.

## Frozen inputs and base binding

```
$ sha256sum .ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d  .ufo/waves/round-62/c62_calibration.py
$ git rev-parse HEAD
c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13
$ git status --porcelain
?? .ufo/waves/round-62/
$ grep -c '' corpus/QUALITY.md
1408
$ grep -c 'round-61-verifier-spotcheck' corpus/QUALITY.md   # 0
$ grep -c 'substantive' corpus/QUALITY.md                   # 0
```

HEAD equals the contract base and the only worktree difference is the untracked wave
directory, so every `corpus/` reading below is a base-revision reading. The base-control
line in the lane task (`unresolved=1 quote_correction=0 criterion=0 lesson_gate=0
source_row=1 met=false exit 1`) is quoted as assigned context; this seat did not re-run
the counter.

## 1. The boundary this review enforces

The rule being checked is not taste. Three committed statements fix it:

- Fleet `CORPUS.md:119-121`: “**No second method.** Claim admission stays in
  `corpus/QUALITY.md`; the research method stays chousa's (`chousa-shokunin/SKILL.md`:
  question → source hierarchy → citation chain → claim-vs-source check).”
- `kake-shokunin/PROVINCE.md:42-43`: “`chousa` owns research method and source hierarchy;
  kake keeps only domain findings and its own `corpus/SOURCES.md` rows.”
- `chousa-shokunin/PROVINCE.md:5-8`: chousa owns “citation chaining and hop resolution;
  claim-vs-source verification”.

So kake **may** own an admission bar, and **may not** own the general method of deciding
whether a source supports a claim. chousa already states that method at
`chousa-shokunin/SKILL.md:20` (“Verify a claim | claim → source → the source's own
evidence”), `:23` (four support states, “`verified` requires state 3”) and
`chousa-shokunin/corpus/QUALITY.md:28-33` (criterion 8, “Support states stay distinct”).
chousa also already owns the *mechanics* that a kake draft must not absorb:
`SKILL.md:24` (re-open a located quote; the named error is “reading `VERBATIM` as support
or truth”), `corpus/QUALITY.md:169` (criterion 25), `:211` (criterion 30), `:917`
(criterion 87, “A capture is read through a defined text form before a quote is located
in it”) and `:735-747` (criterion 72, substance floor by length).

This seat confirms, rather than assumes, that the pointer the criterion reviewer used is
correct: `kake-shokunin/corpus/SOURCES.md:3` does restate “Claim admission stays in
`corpus/QUALITY.md`; the research method remains chousa's”, so `ReviewerQualityCriterion.md:7`
cites a real line. No pointer defect there.

## 2. What is actually being proposed

Two drafts exist and agree on the gap:

- `w1/ScribeQualityCriterion.md:73` — a four-part admit rule bundling (a) the substance
  test, (b) a rendering form (“tags stripped, code-span backticks dropped, whitespace
  collapsed”), (c) two numeric thresholds (“6..25 units and at most 160 characters”),
  (d) page-uniqueness and (e) section/line printing.
- `w1/ReviewerQualityCriterion.md:9-11` — a leaner wording: “Admit a web-publishing claim
  only when its retained, source-true quoted excerpt states evidence that substantively
  supports the specific teaching attached to it”.

Both correctly refuse to supersede `QUALITY.md:375-388` (quote truth) and `:1116`
(locator). Neither is yet the domain-specific object this seat is asked to protect, and
the first is a second method three times over.

## 3. Findings

### Q1 — The bundled admit rule is a compound criterion, so it cannot fail for one reason

`ScribeQualityCriterion.md:73` makes admission conditional on rendering form, a unit floor
and ceiling, a character cap, page uniqueness and printed coordinates **and** on semantic
support. A falsifier therefore cannot isolate substance: a rejected span may have failed
rendering, the cap, uniqueness, or support, and an admitted span proves all six at once.
`chousa-shokunin/corpus/QUALITY.md:735-747` is the precedent for why that matters — its
criterion exists because “structural legs … all pass a single-space quote over a
whole-capture span”, i.e. shape legs cannot stand in for substance. A criterion that fuses
them re-creates the confusion it is meant to end.

Every non-semantic leg of the draft already has an owner in this lane:

| Draft clause | Existing kake row | Verdict |
|---|---|---|
| “deterministic rendering … whitespace collapsed” | `QUALITY.md:1100` (round 50, match class raw-substring vs collapsed-only) | covered as a *class label*, not as a rendering contract |
| “6..25 units”, “at most 160 characters” | `QUALITY.md:1160-1165` (≤25 units; “so no word-segmentation ruling is needed”) | contradicted in part, see Q2 |
| “occurs once on the page” | `QUALITY.md:1207-1210` (page-unique across every retained body) | duplicate |
| “printed beside its section and retained-body line range” | `QUALITY.md:1116` (locator/section) + `:1398` (attribution) | duplicate |

`QUALITY.md:27-29` requires that changes “append a superseding row and its motivating
lesson; they do not erase earlier criteria.” A new row that silently restates four old
properties is neither a supersession nor an addition.

### Q2 — The numeric thresholds are example-fitted and conflict with the lane's one length rule

`grep -n '160 char' corpus/QUALITY.md` → no match (exit 1); `grep -n '25 units'` → `:1140`, `:1160`, `:1169`.
The lane's single length bar is r55's ≤25 units, adopted explicitly to avoid a
word-segmentation ruling. The draft adds a **floor of 6 units** and a **160-character cap**
with no grounding, and the motivating example sits at 21 units / 148 characters
(`ScribeQualityCriterion.md:43`, peer-measured; not re-derived here) — twelve characters
of headroom. A threshold set by one example is a fit, not a bar: the next legitimate
multi-node sentence in a different specification can exceed it and be rejected for the
wrong reason. Length belongs to r55 and must not be re-opened inside the substance row.

### Q3 — The rendering rule is chousa's text-form province, and it globalizes a one-page artifact

“Tags stripped, code-span backticks dropped, whitespace collapsed” is a corpus-wide
HTML→text contract. chousa owns exactly that object: `corpus/QUALITY.md:917` (criterion 87,
a capture “read through a defined text form before a quote is located in it”),
`SKILL.md:134`/`:139` (`tools/capture-text.py`). Kake has no rendering contract today; its
quote rules are properties of the *entry's printed span* (`:1100` match class, `:1207`
page-unique over retained bytes), not of a renderer.

The backtick clause exists because S432 §3.6 wraps `X-Content-Type-Options` and
`Content-Type` in `<code>` (`S432.html:6151-6154`). Writing that one page's markup artifact
into a standing criterion is the definition of a non-domain-specific rule: it says nothing
about publishing evidence and everything about a tokenizer. If a rendered-text form is
genuinely needed, it is a separate row grounded in its own fixtures, or a citation to
chousa's form — never a clause inside the substance bar.

### Q4 — “States the proposition … attributes to the source” / “supports the specific teaching” is chousa's claim-vs-source check

`ScribeQualityCriterion.md:73` (“states the proposition the sentence citing it attributes to
the source”) and `ReviewerQualityCriterion.md:11` (“states evidence that substantively
supports the specific teaching attached to it”) are the general support relation. That is
`chousa-shokunin/SKILL.md:20` (claim → source → the source's own evidence) and
`corpus/QUALITY.md:28-33` (state 3, “source states the claim”), owned by chousa under
`PROVINCE.md:5-8` and reserved to it by fleet `CORPUS.md:119-121`.

The defect is not that kake tests support; kake must admit its own claims. The defect is
that the *predicate as worded has no kake object*: it would read identically in chousa's
corpus, in kagi's, or in lore's. What makes it kake's is the object it is applied to —
the recorded-header audit rule derived from a response field's specification. The
criterion must name that object, or it is a second copy of chousa's method with a kake
file path attached.

### Q5 — “Substantive” already means *length* in both lanes

- `kake-shokunin/.ufo/waves/round-25/quote_proof.py:43`:
  `'substantiveQuote': quote_exit == 1 and 'quote_too_short' in quote['findings']` — a
  length floor for a card quote.
- `chousa-shokunin/corpus/QUALITY.md:735-747`: “A span-quote counter has a **substance
  floor**” — `<3` non-space characters, `<12` characters, overwide spans.

A reader who meets the new frozen literal “substantive located quote”
(`c62_calibration.py:17`) will parse “substantive” as the length property it currently
denotes in both lanes. The new row must therefore define its term in place — substance =
carries the field's operative job, **not** a length property — and defer length to
`QUALITY.md:1160`. The term collision is created by the frozen literal and cannot be
removed by this seat; it can be neutralized by definition.

### Q6 — The domain object already exists in the entry; the criterion should bind to it

`corpus/knowledge/response-header-expectations.md` already declares the object:

- `:5` `ground: publisher-side operability — what a recorded response header list can be
  checked against offline, without a browser and without a fetch at audit time`
- `:6` `scope: the six expectation classes the round-61 audit declares (…six ids…)`
- `:7` `coverage: the response field each class reads, the specification sentence that
  grounds it, the audit rule the class encodes, and the limits of reading a recorded
  header list`

`:7` is the ready-made, committed predicate for the criterion: **the span must be the
specification sentence that grounds the class.** Nothing needs inventing, and the
resulting test is not chousa's — a quote can be verbatim, page-unique, correctly located,
attributed and “about the claim”, and still fail because it is not the sentence the *audit
class's rule* reads. That last clause is kake's alone.

## 4. Recommended scope (proposal — not applied)

One property, one population, one reject test, no length, no rendering, no supersession.

```
## Round-62 criteria

- **A publishing-evidence quote is a substantive located quote only when it is the
  specification sentence the entry's audit rule reads.** Population: a quoted span offered
  in an admitted `corpus/knowledge/` entry as the ground for a declared kake audit rule —
  the six response-field classes of `corpus/knowledge/response-header-expectations.md:6`
  and any later kake gate. Admit a span when it names the field the class reads and states
  the operative action or value the class encodes, so the rule printed beside it follows
  from the span without an inference the entry does not mark `[INFERENCE]`. Reject a
  heading, a section lead-in, a "use the following" transition, a truncated fragment, or a
  span that would ground any other class in the same entry unchanged (the
  field-substitution test — not the sentence this class reads); and reject a quote-true,
  correctly located span offered as ground for a rule it does not state. Quote truth
  (`corpus/QUALITY.md:375`), match class (`:1100`), locator (`:1116`), length (`:1160`) and
  attribution (`:1398`) are necessary, not sufficient; this row adds one property and
  supersedes none. It decides no source tier or suitability (`corpus/SOURCES.md`; chousa's
  method), no question of whether a field should be set, and nothing about a browser or a
  live header. Grounding: `corpus/lessons/round-61-verifier-spotcheck.md:33` (S432 admitted
  on the lead-in) and `:36` (the harm and the missing criterion); retained body
  `.ufo/waves/round-61/sources/S432.html:6183` (lead-in) against `:6151-6154` (the field's
  job). The counter's criterion condition tests presence only, so this bar is reviewed and
  is not established by `criterion=1`. Falsifier: under the field-substitution test the
  sentence at `S432.html:6151-6154` admits and the lead-in at `:6183` rejects; a landed row
  that admits the lead-in fails this criterion.
```

Properties of this wording, stated so a reviewer can falsify the review:

1. **Required literals preserved.** It contains `substantive located quote` and
   `round-61-verifier-spotcheck.md` (as part of a resolvable path), which is all
   `c62_calibration.py:35` reads; nothing about the counter is being gamed, since the
   counter cannot distinguish this row from a hollow one.
2. **Domain-specific.** The population is a kake audit rule over a recorded header list
   (`entry:5-7`); the admit test is “the sentence the rule reads”; the reject test operates
   on kake's own six-class list. None of it transfers to a research window, a bounty
   package, or lore.
3. **Not a second method.** It does not restate support states, tiers, hop resolution,
   re-open verdicts, text forms or length; it points at chousa only as a non-decision.
4. **Single-testable.** A rejection has exactly one cause: the span is not the sentence the
   rule reads (with the four named shapes as instances of that cause).
5. **Append-only conformant.** A new `## Round-62 criteria` section; no prior byte changes;
   the verifier record and the S432 row stay as they are.

If the lane instead prefers the reviewer's leaner sentence (`ReviewerQualityCriterion.md:11`),
the minimum repair is to append its object: “Admit a **response-field expectation** in a kake
publishing-evidence entry only when the quoted span **states the field's job or value rule
the entry's audit class encodes** …”. Without that substitution the wording is chousa's
criterion 8 with a different subject.

## 5. Gates and limits

- Not run by this seat: `c62_calibration.py` at any revision, any census, any selftest, any
  Git/jj mutation, any network fetch. The base-control line is quoted, not re-executed.
- Executed commands were reads only: `sha256sum`, `git rev-parse`, `git status`,
  `grep`/`sed`/`nl`/`wc`, `mkdir`/`rmdir` on own scratch.
- This is a scope review of a *proposal*. The criterion is not inserted, not scored, and
  confers no credit. It does not establish that any admitted row passes it.
- The falsifier above is a reviewer check, not a counter: no committed command tests
  substance (`grep -rn 'substantive' .ufo/waves/*/*.py scripts/*.py` → only
  `round-25/quote_proof.py:43`, a length check, and `round-62/c62_calibration.py:17`, the
  literal). Under the contract no post-freeze predicate change is allowed, so no substance
  counter can be added to C1 this round; any such build is extra-axis work that cannot be
  promoted as a claim.
- I did not verify the peer's rendering measurements (21 units / 148 characters) or the
  S432 line renders; those belong to `ScoutFetchSemantics.md` and `ScribeQualityCriterion.md`
  and are cited here as peer-measured.

## 6. Conflicts observed (verbatim; not adjudicated by this seat)

- `w1/ScoutCounterPredicate.md:7`: “the correction and criterion tests do not establish
  their substantive content … `:35` tests only for `substantive located quote` and the
  verifier filename anywhere in QUALITY.md, not that the appended criterion states the
  intended rule or cites/follows the verifier finding.”
- `w1/ReviewerCounterDataflow.md:5`: “`criterion` only requires `substantive located quote`
  and the spotcheck filename anywhere in QUALITY (`:35`); it never verifies the criterion
  text actually distinguishes substantive evidence from a generic lead-in”.
- `w1/CriticCalibrationMeaning.md:7`: a text-only append carrying the exact `QUOTE`,
  `S432 §3.6`, `Round-62 correction`, `substantive located quote` and the spotcheck filename
  “would count `quote_correction=1` and `criterion=1` … despite no measured calibration
  change.”
- `w1/ScribeQualityCriterion.md:110-111` (F2): the spot-check row's clause “Lesson itself
  identifies it as a generic lead-in” is not supported by `corpus/lessons/round-61.md`.

The first three agree with `c62_calibration.py:35`; this seat's independent reading of that
line is identical. They are counter-strength findings, not scope findings, and remain with
those seats.

## 7. Out of scope for this seat

- Any edit to `corpus/QUALITY.md`, the knowledge entry, the lesson, `SOURCES.md`, the
  counter, the contract, or any score.
- Judging whether the S432 quote correction is substantively correct (ReviewerSourceSupport)
  or whether the lesson Gate is adequate (ReviewerLessonGate).
- Adding a substance counter or proposing a predicate change.
- Chousa's own criteria: nothing here proposes a change to `chousa-shokunin`.

## 8. Artifacts

- This report: `.ufo/waves/round-62/w1/ScribeQualityScope.md`
- Reviewed proposals: `.ufo/waves/round-62/w1/ScribeQualityCriterion.md`,
  `.ufo/waves/round-62/w1/ReviewerQualityCriterion.md`
- Frozen inputs: `.ufo/waves/round-62/c62_calibration.py` (sha256
  `ba7b7737…78548d`), `corpus/QUALITY.md` (1408 lines), `corpus/lessons/round-61-verifier-spotcheck.md`,
  `corpus/knowledge/response-header-expectations.md`, `.ufo/waves/round-61/sources/S432.html`
- Boundary sources: `/home/vgpnk/Projects/shokunin/CORPUS.md:119-121`,
  `kake-shokunin/PROVINCE.md:42-43`, `chousa-shokunin/PROVINCE.md:5-8`,
  `chousa-shokunin/SKILL.md:20,23,24`, `chousa-shokunin/corpus/QUALITY.md:28,169,211,735,917`
