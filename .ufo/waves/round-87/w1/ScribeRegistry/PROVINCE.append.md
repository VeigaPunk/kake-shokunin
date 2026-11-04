
## Round 87 — Age arithmetic only

`corpus/knowledge/cache-current-age.md` (S462, RFC 9111 §4.2.3) and
`scripts/cache_current_age.py` add the conservative current-age calculation to
bounded held Frontier ground. The offline probe accepts caller-supplied integer
epoch seconds and emits all six arithmetic terms; absent Age is zero, missing
Date is unsupported, and invalid inputs fail. Integer epoch representation and
arbitrary-precision arithmetic are local conventions, not RFC mandates. The
conservative maximum is a chosen allowed profile alongside the RFC's MAY path.

This advances Age arithmetic only: not header extraction or Date parsing, cache
storage/reuse permission, Cache-Control policy, browser/runtime observations,
credential custody or publishing. Existing general-classifier semantic debt and
the independent changed-row oracle remain open. Browser execution stays adjacent
work; publishing stays operator-owned. No live-property verdict or repair follows
from a calculated current age, and this registry appendix is not an execution
receipt or outside admission.
