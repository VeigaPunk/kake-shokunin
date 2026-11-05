# ReviewReval — round 96 w1 report (independent C2-line review)

**Verdict line (also in `w1/ReviewReval/grid.md`):**
`REVIEW-REVAL agree=24/24 tooldefects=0 contractdefects=0 referencedefects=0`

## Scope and method

Independent, non-author review of the C2 revalidation-exchange line, per the
seat spec: (1) a fresh 24-case grid derived by this seat from the frozen
contract (`reval-contract-v1.md`, sha `65f0a347…` verified) and RFC 9111 §4.3
(read from the retained body `aeb52adb…`, quote anchors verified at exactly
the freeze's lines 848/852/861/935/938/944; etag grammar from the retained
RFC 9110 S455 body, lines 3570–3617); (2) scoring of the delivered candidate
over that grid; (3) clause-by-clause check of the in-counter `reference()`
against the fetched RFC text. No instrument, contract, population or
candidate byte was patched — this seat is a reporter.

## Findings

**No defect found in any of the three classes.** All checks below name
command and observed rc; full per-case output is receipted.

1. **Candidate (delivered work): clean on my grid.**
   `python3 -B runner.py scripts/reval_exchange.py receipt-run-candidate.txt
   candidate` → rc=0, `agree=24/24 reference_agree=22/22`. Scored bytes:
   sha256 `192b3bf7596abad8ef76a7a8262ecc29c0d565587153547ee61b5ee7566c7212`
   (untracked worktree file at scoring time; digest stable before/after the
   run and at report time). The candidate was **present** when I ran, so the
   spec's absent-candidate fallback did not apply; the frozen positive
   control was additionally scored as corroboration (`receipt-run-control.txt`,
   rc=0, agree=24/24, sha `47c65725…` = population pin).
2. **Contract: no defect.** Every expected decision I derived from a clause
   was matched by both the in-counter reference and both subjects; the
   contract's labeling discipline holds everywhere it matters — C2
   ("both validators together") and C5 ("200–499 by status code alone") are
   the two designed divergences from RFC-exact reading and both are labeled
   lane conventions with the exclusions named (subrange condition; payload-
   less 204). Had either been labeled RFC-exact, that would have been a
   contract defect; neither is.
3. **In-counter reference vs RFC text: no clause disagreement.** C1/C3/C4
   are RFC-exact at the level the decision names report (quotes at lines
   848, 935, 944); C5's status-class mapping is the labeled lane convention
   over line 938's content-defined class; C6's etagc set
   {0x21, 0x23–0x7E, 0x80–0xFF} and case-sensitive `W/` are byte-exact to
   RFC 9110 §8.8.3, including the two boundary directions my grid pins:
   `""` (empty opaque tag) is grammar-valid — the RFC's own example
   `ETag: ""` — and is constructed by reference/control/candidate alike,
   while the zero-length string and SP-inside-opaque are refused.

Grid properties: 24 cases, none colliding with the frozen 37 hand cases
(`receipt-nonoverlap.txt`: input-digest intersection = 0); coverage includes
the seat-spec asks (299/300, 499/500/501, 304 with only-LM, raw duplicate
keys in a nested object and at top level, single obs-text-byte etag,
last_modified = 0, received 200 with exists=false and no validator) plus
grid-derived edges the frozen set lacks (grammar-valid `""`; huge LM with no
ceiling; exists=false at construction; LM bool; 1xx upper edge 199).

## Observations (routed notes, no repair made)

- **obs-text ↔ JSON mapping is unpinned** (reference resolves obs-text as
  single code points U+0080–U+00FF, refuses above). Conservative and
  consistent; a one-sentence pin belongs in a future contract v2 if this
  line gets a successor. Routed as a note, not a defect.
- **Harness erratum, disclosed:** my first runner scored the reference's
  refusal-by-`Invalid` as failure on six expected-refusal cases
  (printed `reference_agree=16/22` in the superseded first-run receipts).
  Corrected in my harness only; final receipts show `reference_agree=22/22`
  with rc=0. No lane byte was touched at any point.
- `lsp` device unavailable in this harness; semantic checks were made by
  full direct reads of the reference/control bytes plus byte-level runs
  (noted per protocol; quote anchoring used the retained bodies, which pin
  exact lines).

## Residual risk / verification gaps

- My 24/24 covers candidate bytes `192b3bf7…` only; the L1's frozen counter
  reads committed bytes at `--revision`, and any later repair produces bytes
  this receipt does not cover.
- My grid does not exercise the counter's forgery/mutant/anti-table/
  generated-case machinery (frozen counter surface, out of seat scope).
- Runs were sandbox-free (`python3 -B`) per the seat authorization; the
  counter's audit-hook sandbox path was not exercised by my grid.

## Deliverables

- `w1/ReviewReval/grid.md` — verdict line, 24-case table with per-case
  grounding (RFC-exact quotes at retained-body lines vs lane-convention
  labels), clause-by-clause analysis, receipts index.
- `w1/ReviewReval/cases.json` — the 24 cases (inputs; raw payloads as text;
  expected; clause; grounding; quotes/lines; notes).
- `w1/ReviewReval/receipt-run-candidate.txt`,
  `receipt-run-control.txt`, `receipt-nonoverlap.txt`,
  `receipt-digests.txt` — command+rc receipts (flat filenames).
- Scratch tree `/fast/scratch/hyaku/kake-r96/ReviewReval/` deleted after
  receipt copy, per seat bounds.

No tool was installed or upgraded (none needed).
