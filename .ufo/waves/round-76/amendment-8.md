# Round 76 — Amendment 8 (terms-only, recorded before the final after-state)

Motivation: `w1/ReviewerC2.md` found that the contract's `hreflang_nonreciprocal` rule — target B must
return an alternate with **A's url and the same tag** — is stricter than the only opened source that states
a reciprocity rule. S444 (Google) says: "Missing return links : If page X links to page Y, page Y must link
back to page X." It does not require the return link to carry the same tag. Under the as-written rule a
Google-canonical mixed cluster (two pages each declaring `en→A` and `fr→B`) is flagged twice.

## G1 — the rule stays, as a declared stricter policy
`hreflang_nonreciprocal` keeps the same-tag requirement. It is a **lane policy**, not a restatement of
S444: the tool flags strictly more than Google's stated rule. The knowledge entry's Reciprocity section and
the capability row's limits must say so in those words, and the real-input run's nonreciprocal findings are
reported as consequences of the stricter rule, never as a claim that Google would flag those pages.

## G2 — the grammar is a frozen ASCII validator
The tag grammar is the contract's frozen ASCII production. It rejects RFC 5646 grandfathered tags
(`en-GB-oed`), redundant extlang forms and extension singletons. The capability row says "frozen ASCII
grammar validator for BCP-47-shaped tags", never "BCP-47 validator"; the knowledge entry's Limits say the
same.

## G3 — the undecidable residue is recorded, not hidden
ReviewerC2's three remaining undecidable classes (href whitespace asymmetry, the shared-file fault id,
the crossing/encoding policy) stay `undecided` in the matrix and are named in the report as contract
defects for a later round. Kill rule 1 stands: they are excluded from the score.
