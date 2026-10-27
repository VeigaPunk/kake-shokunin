# ReviewerClaimCounter — adversarial C1 review

## Findings

**High — the frozen counter can report `met=true` without resolving the extant disagreement.** In `.ufo/waves/round-62/c62_calibration.py:31-41`, the counter counts disagreement lines, but `resolved` is determined only by four marker-presence bits (`:33-38`); if all are true, `unresolved` is forcibly zero irrespective of the disagreement count (`:39-40`). The marker tests do not establish the source-corrected meaning, the criterion's rule, or preservation of the original record. For example, a knowledge blob containing the expected quote and three labels in unrelated prose, a QUALITY blob containing the two marker strings in unrelated prose, and lesson/source blobs containing their tokens suffice for the booleans. No test ties correction text to the content-type expectation or criterion text to a substantive-support requirement. Thus the measured predicate's “unresolved ... == 0” is not independently derived from the disagreement; it is inferred from loose tokens.

**High — the promised substantive postcondition and append-only preservation are not counter-enforced.** Contract `.ufo/waves/round-62/contract.md:7` requires an explained substantive quote correction, a grounded criterion citing the verifier finding, and preservation of the old knowledge prose, source row, and verifier record. Counter `:33-38` checks only substrings in whole blobs; it neither compares the old/new records nor locates the quote in the retained S432 source, nor binds criterion wording to the cited finding. It also does not check that the quality criterion is appended rather than merely present. The claim could therefore be implemented incorrectly while these checks pass. The intended quote is grounded: retained `.ufo/waves/round-61/sources/S432.html:6151-6154` says the response header can require checking a response's Content-Type against request destination; current `corpus/knowledge/response-header-expectations.md:77-87` instead quotes the generic lead-in and a fragment, matching the verifier's criticism at `corpus/lessons/round-61-verifier-spotcheck.md:33,36,46`.

**Counter weakness / exact predicate:** the counter also makes `lesson_gate` require only the presence anywhere of `## Gate`, `S432`, `Agree`, `Reject` (`:36-37`), and `source_row` require only `| S432 |` anywhere (`:38`). These are not exact postconditions for a gate or preserved row. `disagreements` counts any line with both strings, not a uniquely identified row (`:31-32`). The count is then discarded when token gates pass. A zero-disagreement input with all other markers present would still print `met=true`, as would a multiple-disagreement input, because `unresolved` is assigned zero in either case; conversely it has no semantic distinction between real resolution and marker coincidence.

## Axis fit and do-nothing control

The round-61 verifier explicitly calls calibration unprovable because its distinct counter was absent (`corpus/lessons/round-61-verifier-spotcheck.md:15,21`) and identifies the S432 quote-quality failure and missing criterion (`:33,36,41-46`). A substantive correction plus a grounded criterion is directionally responsive to that learned disagreement, and the frozen claim correctly limits the claim and ceiling (`contract.md:7-11`). But the counter's all-token proxy is too weak to demonstrate the behavioral learning/postcondition it purports to score. The specified do-nothing control is reported in `contract.md:7` as `unresolved=1 quote_correction=0 criterion=0 met=False exit 1`; I did not rerun the counter or score anything. Because its base checks are literal presence tests, merely adding strings can reach the counter's success branch; this establishes syntactic reachability, not valid semantic completion.

## Evidence and commands

Read-only inspection commands/tool reads:

- `read .../.ufo/waves/round-62/contract.md:5-10:raw` — frozen claim, required preservation, source grounding and limits.
- `read .../.ufo/waves/round-62/c62_calibration.py` — lines 31-43 establish the proxy logic above.
- `read .../corpus/lessons/round-61-verifier-spotcheck.md` — lines 33, 36, 41-47 state the disagreement and routed defect.
- `read .../corpus/knowledge/response-header-expectations.md` — lines 69-87 show current generic/fractured quotations; lines 89-94 scope the field-value audit policy.
- `read .../.ufo/waves/round-61/sources/S432.html:6151-6154:raw` — retained substantive source sentence.
- `read .../corpus/QUALITY.md:329-380` — existing round-29 criterion requires quote truth against retained source and digest; relevant precedent for distinguishing shape/token checks from grounding.
- `sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py` → `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d` (matches frozen digest).
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kake-shokunin`.
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --short` → `?? .ufo/waves/round-62/` (wave files already untracked; no changes made by this reviewer).

No counter execution, mutation probe, score, or LSP request was made. LSP availability/status was not established, so source inspection is textual evidence only. I did not independently verify the contract's recorded base-control output or live web fetch. Findings concern frozen predicate enforceability, not a judgment that any post-freeze implementation or score passes.