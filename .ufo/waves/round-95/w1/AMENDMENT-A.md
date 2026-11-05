# Amendment A — C1 instrument digest change (pre-scoring)

Before any seat scored data, the frozen C1 identity surface was corrected:
knowledge entries are pinned by PRESENCE only (their heads legitimately gain
[r95-correction]-tagged edits the claim itself must land); lessons keep
full-content digests. No predicate, target or kill rule changed.

Superseding digests for the C1 instrument ONLY:
- c95_selfassess.py sha256 04be4a7dc32adee08e386936e2af8257a191421bd2005c97b40af49933a24a32
- frozen/c1-surfaces.json sha256 9eff04c5a0567f50a3a27004ac7d5aab4d4dc2d1311c4a8d8eb623db8ec4f665

Full rationale: ../freeze.md "## Amendment A". Regenerated receipts:
../controls/{base-c1.txt,ctl-c1-selftest.txt,instrument-sha256.txt}.
C2 instrument unchanged: c95_conditional.py f09f84090fdda405992d7b51191be8838549e3df402b0898eb2ca00c4c3ff312.
A context-digest mismatch you reproduce on the C1 counter is explained by this
amendment; verify against the digests above.
