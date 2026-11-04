
## Round-76 criterion — quoted receipts are whole

Appended 2026-11-03 by the round-76 C1 repair; every criterion above stands unchanged.

- **A quote of observed output is one whole receipt line, an explicitly elided span, or a correction.**
  The round-75 criterion above quoted the deletion control as `files=15 append_only=false met=false`, which
  splices across the observed mismatches=2 classes=E3 between files=15 and append_only=false; no committed
  receipt line contains that fragment. The whole line in
  `.ufo/waves/round-75/controls/ctl-deletion.txt:1` is `C1v1 revision=afc73a87759b4218d54369b583e021b6e800de73 rows=27 live=15 files=15 mismatches=2 classes=E3 append_only=false met=false`.
  Admit: a span equal to a committed receipt line after trimming, or an explicitly elided span whose
  fragments are each contiguous there, or a later correction row that quotes the whole line and names the
  defective span. Reject: a splice that silently skips a field between two observed tokens, a quote that is
  only a fragment of a receipt line, and a quote whose receipt file and line are not named.
  `[r76-correction 2026-11-03]`
