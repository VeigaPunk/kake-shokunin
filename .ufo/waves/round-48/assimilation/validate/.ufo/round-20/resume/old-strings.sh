#!/bin/sh
# Round-20 resume, claim C3: count lines in SKILL.md + corpus/ that still carry one of the six
# superseded GitHub Pages literals WITHOUT an appended `r20-correction` tail. Run from the lane root
# (or any tree with the same layout). Base cb807bc: 9. Measures token presence, not semantic
# correctness; paraphrased mentions are covered by the 27-tail ledger in citation-disposition.json.
for s in 'served set ≡' 'full tree snapshot' 'full-tree artifact' 'CNAME` file pins' 'CNAME` = ds4cc.com' 'entire checked-out tree'; do
  grep -rnF -- "$s" corpus SKILL.md
done | grep -vc 'r20-correction' || true
