<!-- Draft for corpus/QUALITY.md — append at EOF, after the round-80 criterion.
     The file's post-round-75 convention is a `## Round NN criterion — <name>` heading plus one
     bolded bullet; the bullet is written so it also renders as a single table row of the main
     `| Criterion | Admit | Reject | Grounding |` table if the L1 prefers that insertion point. -->

## Round 81 criterion — an audit verdict re-derives from committed bytes

- **Audit verdict from committed bytes, not from a seat's word (round 81).** *Admit* an audit verdict
  only when its capture tree is committed under the lane and a counter re-derives, offline and
  without fetching, every receipt in it — the retained body's sha256 and byte count, an integer
  status, an RFC 3339 fetch time on or after the round that claims the capture, GET and not
  truncated, the URL host inside a declared allowlist — **and** the audit's own stdout equals the
  committed audit receipt line-for-line at the measured revision; an absent-resource answer (404 or
  410, S454) is recorded with its status and is not an audit failure. *Reject* a verdict whose
  capture tree lives only in scratch or is re-fetched at measurement time, whose audit receipt was
  written by anything other than the audited tool's stdout, whose fetch time predates the round, or
  whose absent-resource answers are folded into header findings. *Grounding:*
  `corpus/lessons/round-81.md` §Mistakes and §Gate; `.ufo/waves/round-81/c81_capture_audit.py` with
  `controls/base-c81-capture-audit.txt` (`surfaces=0 met=false`), `controls/after-c2.txt`,
  `controls/after-c2-audit.txt` and `controls/c81-selftest-c2.txt` (12/12, five mutants opening the
  predicate); the class it closes is the round-80 closure's R80-5 (a junk control that named a
  `/fast/scratch` tree no committed builder recreated) and R80-6 (a cause asserted outside committed
  bytes). `S454` (RFC 9110 §15.5.5 404 Not Found and §15.5.11 410 Gone; amendment 1 A2 corrects the
contract's §15.5.4 anchor) bounds the verdict's conclusion; C2's
  `capture-expectations.json` fixes the expectations before the capture is audited.
