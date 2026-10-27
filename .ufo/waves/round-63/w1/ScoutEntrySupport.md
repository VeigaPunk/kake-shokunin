# ScoutEntrySupport — round-63 w1 semantic-support judgment

Seat: ScoutEntrySupport (leaf; no subagent dispatch, no git/jj mutation).
Question: Does the admitted collapsed-only span state the same proposition the
`xcto_nosniff_value` section attributes to S432 (a field-purpose statement)?
Does the round-62 QUALITY criterion (substantive support) accept this admission?

## Evidence read (all read-only; nothing frozen edited)

- Attributing section: `corpus/knowledge/response-header-expectations.md`
  `xcto_nosniff_value` (lines 69-97).
- Admission block: same file, `[r63-correction 2026-10-27]` (lines 224-247),
  above it the `[r62-correction]` held block (lines 213-220).
- Retained source: `.ufo/waves/round-61/sources/S432.html` raw lines 6150-6154
  (authoritative numbering re-verified with awk, see below).
- Criterion: `corpus/QUALITY.md` "## Round-62 criteria" (line 1412); class rule:
  `corpus/QUALITY.md` round-50 quote-class criterion (lines 1100-1108).
- Ledger: `.ufo/waves/round-63/quote-class/quote-classes.json`; rendering:
  `.ufo/waves/round-63/quote-class/S432.txt`; recipe:
  `.ufo/waves/round-63/quote-class/extract_text.py`.

## The two texts

Attributed proposition (`response-header-expectations.md:71-72`): "WHATWG
Fetch §3.6 gives the field its purpose in the response-processing steps; the
sentence is fragmented by inline markup — the field's name sits in the section
heading and in a code element immediately before the first span — so the
quotable pieces are short and the normative value grammar is cited by location
[S432 §3.6]". The two fragments then quoted (lines 77-81) are "can be used to
require checking of a" and "Web developers and conformance checkers must use
the following". So the section attributes to S432 §3.6 exactly one
field-purpose statement: `X-Content-Type-Options` exists to require checking a
response's `Content-Type` header against the destination of a request.

Admitted span (`response-header-expectations.md:229-231`):

> "The `X-Content-Type-Options` response header can be used to require checking of a response's `Content-Type` header against the destination of a request."

Retained raw lines 6150-6154 (`S432.html`, awk-verified):

```
6150:    <p>The
6151: `<dfn ...><code>X-Content-Type-Options</code></dfn>`
6152: response <a ...>header</a> can be used to require checking of a <a ...>response</a>’s
6153: `<code>Content-Type</code>` <a ...>header</a> against the <a ...>destination</a> of a
6154: <a ...>request</a>.
```

The span is the textContent rendering of precisely that sentence. My own
derivation check (commands run at the fleet root, read-only):

```
$ sha256sum .ufo/waves/round-63/quote-class/S432.txt .ufo/waves/round-61/sources/S432.html
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  .ufo/waves/round-63/quote-class/S432.txt
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  .ufo/waves/round-61/sources/S432.html
$ python3 -c '...membership test...'
span in flat text: True
span in raw html: False
```

Both digests match the ledger (`textSha256` 8b90d096…, `rawSha256`
63b0a018…), and the class derivation reproduces: substring of the flat
rendering, not of the retained HTML → `collapsed-only` under the round-50
rule (`QUALITY.md:1100-1108`). The ledger's `locatedRawLines: "6150-6154"` is
exact — line 6150 opens `<p>The` and line 6154 carries the sentence-final
"`request`.".

## Question 1 — same proposition?

**Yes (confidence: high).** Component-by-component, the span and the attributed
statement contain the same four semantic parts:

1. field identity: "`X-Content-Type-Options` response header" (raw: dfn +
   "response header", lines 6150-6152);
2. action: "can be used to require checking of" (line 6152);
3. object checked: "a response's `Content-Type` header" (lines 6152-6153);
4. check target: "the destination of a request" (lines 6153-6154).

The attributing section itself concedes the sentence exists but is
"fragmented by inline markup" and calls the fragments "the quotable pieces" —
the first fragment is literally a severed piece of the admitted span. The
admission does not introduce a new proposition; it quotes the whole sentence
the fragments were cut from, in its located rendering. The round-62 held
correction rejected the fragment because it "ends before its object" and the
lead-in because it is generic; the admitted span has all four components, so
the defects that made the earlier spans insubstantive are absent here.

**Best counter-argument.** Semantic identity is not provenance identity. The
span is a substring of a lane-produced rendering (`extract_text.py`,
textContent semantics, whitespace-collapsed), not of the retained source
bytes; the knowledge entry now displays a normalized cross-markup string
while citing S432. If "quotes" in a knowledge entry are required to be raw
source substrings, the span is a derivation, not a quote. This is a real
evidentiary distinction — it is exactly why the r62 held correction refused
the substitution — but it is a question about *admissibility and labeling*,
not about whether the same proposition is stated. On the proposition itself,
the counter-argument has no traction: the rendering is deterministic,
committed, sha-pinned, and lossless for this sentence (every text node of
lines 6150-6154 survives in order; only markup is dropped).

## Question 2 — does the round-62 criterion accept the admission?

**Yes, with one binding condition (confidence: high).** The criterion
(`QUALITY.md:1412`) is a substantive-support test: "Admit a claim only when
the located quote states the same scoped proposition as the sentence it
grounds; keep a field's purpose separate from claims about its exact value or
algorithm." Its falsifier has two negative clauses; the admission must fail
neither:

- Clause 1 — reject if "the quoted S432 §3.6 purpose sentence does not
  identify the `X-Content-Type-Options` response header or its check of
  `Content-Type` against request destination". The span identifies all three
  named items verbatim. Not triggered.
- Clause 2 — reject if "the `nosniff`-only claim is attributed to that
  purpose sentence". The r63 block explicitly keeps them apart ("a
  field-purpose statement, kept separate from the `nosniff`-only value rule
  per the round-62 criterion"); the audit-semantics value rule
  (`response-header-expectations.md:89-97`) still rests on the ABNF block and
  the determine-nosniff algorithm, cited by location, untouched. Not
  triggered.

The "same scoped proposition" limb is met per Question 1. The r62 held
block's stated ground for refusal was procedural, not semantic: "Existing
`corpus/QUALITY.md` quote rules require raw-substring evidence" (line 219).
That objection is resolved by classing the span under the standing round-50
quote-class rule (`QUALITY.md:1100-1108`), which predates round-62 and admits
`collapsed-only` as a distinct, recorded class. The admission satisfies that
rule's hard labeling discipline — "a collapsed-only span is never described
as a raw substring nor the reverse": the block says "never described as a raw
substring", the ledger records `matchClass: "collapsed-only"` with both blob
digests, and my re-derivation from the committed blobs confirms the class.
The class, the digests and the recipe are all committed bytes, so the
admission is replayable, not asserted.

**Best counter-argument.** Read the r62 criterion together with its held
correction, the only admissible quote form for a knowledge entry is
raw-substring; then a collapsed-only span is inadmissible in principle, and
the r63 admission is a criterion change smuggled in as a correction. Against
that: the round-50 class rule already defines collapsed-only as a first-class
recorded class and the r62 correction itself acknowledges the sentence "is
not a raw substring of the retained HTML" while declining to *substitute* it
unilaterally — round-63 supplies the missing machinery (ledger, digests,
recipe, inline re-derivation) rather than lowering any bar. On that reading
the admission is the intended resolution path, not a weakening.

**Binding condition.** Acceptance holds only while the class is never
mislabeled and the value rule is never re-attributed to the purpose sentence.
Both are currently maintained and machine-checkable (C1's `quote_correction`
re-derives class from the pinned blobs; the falsifier text is the guard).

## Conclusion

1. The admitted collapsed-only span states the same proposition the
   `xcto_nosniff_value` section attributes to S432 — the complete
   field-purpose sentence ("same scoped proposition": high confidence).
2. The round-62 substantive-support criterion accepts the admission: its
   falsifier is not triggered on either clause, purpose and value rule remain
   separated, and the round-62 held correction's raw-substring objection is
   properly resolved through the pre-existing round-50 collapsed-only class
   with committed, re-derivable evidence (high confidence, conditional on the
   labeling discipline holding).

Residual unknowns: (a) the r62 held block locates the sentence at
"S432.html:6150-6156" while r63/ledger say 6150-6154 — awk verification shows
6150-6154 is the exact sentence span (6150 `<p>The` … 6154 `request.`), so
the r63 locator is the precise one and the discrepancy is cosmetic; (b)
acceptance presumes `extract_text.py`'s textContent semantics are the agreed
rendering — guarded by the committed recipe, its pinned output digest, and
C1's inline, tool-independent re-derivation.

No tools installed this seat. No files written except this Report.
