# Round 76 — Amendment 6 (terms-only, recorded before the final after-state)

Motivation: `w1/ExecAuditTool.md` §4 asks for three C2 decisions to be frozen because they change finding
counts; the tool and the matrix already implement them consistently. Each is a clarification of Amendment 2,
not a change of any decided verdict elsewhere.

## E1 (I3/I4) — a non-absolute canonical contributes no canonical finding
Amendment 2 §A4 is applied to the `rel=canonical` link as well: a canonical `href` that does not parse as an
absolute URL is not resolved, so it yields **no** `hreflang_canonical_not_self` finding on that page. (The
page's own hreflang findings, if any, are unaffected.)

## E2 (I5) — `hreflang_multiple_xdefault` is per element
`hreflang_multiple_xdefault` is emitted **once per x-default `<link>` element** on a page that carries more
than one (so a page with four x-default links yields four findings), consistent with Amendment 2 §A2's
one-per-annotation rule. `hreflang_self_missing` and `hreflang_canonical_not_self` remain once per page.

## E3 — the undecided residue
The matrix reports 3 `undecided` cases out of 69. Kill rule 1 stands: undecided cases are excluded from the
score, never counted as passes, and the C2 target is stated over **decided** cases (66/66 correct at the
carrier, 4/4 constants failed).
