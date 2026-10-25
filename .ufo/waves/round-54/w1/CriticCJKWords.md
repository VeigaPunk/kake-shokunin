# CriticCJKWords — round-54 CJK quote accounting vs CORPUS.md ≤25-word rule

Scope: challenge whether the lane treats the 31/27/27 counter units for
S367/S372/S373 as words or as compliant quotes. Measured at lane tip `8e408e0`
(round-54 claim commit). All quoted file lines are committed bytes; CJK unit
counts re-derived locally with the counter's own `units()` definition
(`.ufo/waves/round-52/c52_quote_truth.py:136-140`, regex line 74:
`[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]`).

## Verdict

On the labeling axis: **the lane is clean**. Every committed text says "units"
and explicitly denies that a unit count proves CORPUS rule-1 compliance; no text
calls the 31/27/27 values "words" or claims the quotes meet ≤25 words.

On the compliance axis: **the lane still treats the three quotes as usable-by-omission**.
Two structural facts leave S367/S372/S373 in the registry without ever passing
the rule-1 Gate quote test the maintenance item is supposed to hold open.

## Evidence — labeling is correct (pro-lane findings)

- Frozen convention, stated as convention not compliance:
  `.ufo/waves/round-54/contract.md:60-68` — "the inherited round-52 `units()`
  convention counts each CJK character as one unit and each non-CJK whitespace
  token as one unit. This differs from literal “word” counting in CORPUS.md
  rule 1; S367/S372/S373's 31/27/27 units do **not** prove compliance with the
  ≤25-word rule." Correct non-overclaim.
- Quality criterion, correct and enforceable:
  `corpus/QUALITY.md:1133-1144` — "CJK quote length names its unit and does not
  imply word-rule compliance … report the exact counting convention and the
  gate's accepted range … report it as units, never as “words”."
- `corpus/lessons/round-54.md:28` (Mistakes row): "CJK quote “word” counts were
  conflated with unit counts … These values exceed 25 units; they do not
  establish how many lexical words the CORPUS rule means for Japanese."
  Honest, correctly classed as mistake not compliance.
- `.ufo/waves/round-53/sources/gate-draft.md:15-22` labels all five quotes
  "(N units)" and cites the counting convention verbatim with its bound:
  "Units per `.ufo/waves/round-52/c52_quote_truth.py` `units()` (one per CJK
  character, one per non-CJK whitespace token; bound 6–40)." Units, not words.
- `corpus/lessons/round-52.md:16-20` declares the same: "one unit per CJK
  character, one per non-CJK whitespace token, bound 6–40 units" and states the
  prior counter's "6 to 25 whitespace words" rule would make CJK quotes
  unquotable — the unit rule is presented as the gate's own, not as the CORPUS
  word rule.
- `corpus/lessons/round-54.md:10-11` labels the S374 Gate quote "(24 units
  under the lane's CJK counter)" — units, and incidentally the only CJK quote
  in the lane that could satisfy a ≤25 reading under any unit convention.

Counts re-derived, all match recorded values (exact `units()` port):
S367=31, S372=27, S373=27, S390=16, S409=15, S416=15, S417=20, S374-r54=24.
Raw-substring claims verified: each quoted span occurs exactly once in its
retained body (`grep -o -F | wc -l` → 1 for S367/S372/S373 under
`.ufo/waves/round-53/sources/` and S374 under `.ufo/waves/round-52/sources/`).

## Counterexample — compliance is sidestepped, not resolved

**C1. The 31/27/27-unit quotes are never recorded in the place the ≤25-word
rule attaches.** CORPUS.md SOURCES rule 1 (shared checkout, lines 112-115):
"The round lesson's `## Gate` records, for every new row, the URL, the access
date, and a ≤25-word quote with its location grounding `teaches`."

`corpus/lessons/round-53.md:35-37` `## Gate` registers S367/S372/S373/S390/S409
but contains **no quote spans** — it delegates: "URLs, exact quotes, located
anchors, access date, HTTP status, byte counts and SHA-256 digests are recorded
in `.ufo/waves/round-53/sources/gate-draft.md`". The quotes live only in a wave
artifact, outside the `## Gate` where rule 1 evaluates the ≤25-word quote. The
over-25 quotes were therefore registered while structurally evading the rule-1
compliance surface — treated as compliant rows (`status mined`, `used-by`
populated, held-ground citations in `corpus/knowledge/*.md`) without ever being
recorded as rule-1 Gate quotes at all. The round-54 maintenance fix relabels
the numbers but leaves this omission intact.

**C2. The only adjudication in the corpus accepts the ambiguity in the lane's
favor.** `corpus/lessons/round-53-verifier-spotcheck.md:57`: "the CORPUS
≤25-word letter is ambiguous for CJK; routed as a nit, not an admission
failure." Ambiguity is a two-edged sword: it equally fails to prove
*non-compliance*, but rule 1 requires a compliant quote — under-specified does
not mean compliant. The lane's own r54 texts correctly downgrade this to
"unresolved" (contract) and "do not claim" (lesson); the spotcheck line is a
protected non-author artifact and stays, but it is the strongest remaining text
treating over-25-unit quotes as acceptable.

**C3 (minor). Mislabeled bound survives in a protected artifact.**
`corpus/lessons/round-52-verifier-spotcheck.md:96`: "The ≤25-unit rule the
lesson declares (one unit per CJK character, one per non-CJK whitespace token;
6–40) holds for all three quotes as counted." The lesson's declared bound is
6–40 (`round-52.md:17`); "≤25-unit" is a mislabel leaking the word bound into
unit space. Historical text, append-only — but it is exactly the unit/word
conflation the r54 criterion now names, left unannotated.

**C4 (minor). False-precision footnote.** `contract.md:68-69` "The count is
re-derived at the measured commit in the report" — satisfied here (31/27/27
re-derived identically at `8e408e0`); no defect, noted so the obligation is not
silently dropped by a future round.

## Impacted axes

- **quality** — C1 is the live defect: rule-1 Gate records are incomplete for 5
  of 7 CJK rows; the ≤25-word question is unresolved while the rows are fully
  operative as `mined` held ground.
- **discernment** — C2/C3 are residual ambiguity-acceptance and a mislabeled
  bound inside protected artifacts; the r54 criterion fixes forward behavior
  but leaves the old text unmarked.
- freshness/operability: no impact found.

## Smallest safe correction

Append-only; no protected-artifact edits:

1. In the next round lesson's `## Gate` (or an appended `### Gate supplement`
   subsection under it), record each of S367/S372/S373/S390/S409's quote with
   its location **in the Gate itself**, labeled units, and state explicitly
   that the ≤25-word question remains unresolved per `QUALITY.md:1133`.
   Alternatively shorten S367/S372/S373's Gate-recorded quotes to ≤25-unit
   spans via append-only correction (e.g. S373 can drop the trailing clause);
   S390 (16), S409 (15), S416 (15), S417 (20), S374 (24) already fit under 25.
2. Annotate the `round-52-verifier-spotcheck.md:96` "≤25-unit" mislabel and the
   `round-53-verifier-spotcheck.md:57` "nit, not an admission failure" line in
   the next lesson's corrections paragraph — supersede, don't edit.

## Tool installs

None. Verification used read-only `git log`/`status`/`ls-files`, `grep`, and a
local reimplementation of `units()`; no counters executed, no repo files
changed besides this report.
