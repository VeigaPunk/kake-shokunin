# CriticClaimScope — round 62

## Counterexample and assessment

The frozen claim is properly scoped to one known calibration failure: the round-61 non-author S432 admission disagreement. It does **not** authorize resolving all corpus disagreements. Its counted predicate is round-61 spot-check S432 disagreement count reaching zero only when this specific correction, criterion, lesson gate, and preserved S432 source row are all present. The prose explicitly caps calibration and forbids claiming all-disagreement resolution (contract.md:7,11).

Strong counterexample to any broader reading: an unrelated disagreement elsewhere in the corpus can remain untouched while this single S432 disagreement is resolved. The counter's `disagreements` calculation only counts lines containing both `S432` and `Disagree` in `corpus/lessons/round-61-verifier-spotcheck.md` (c62_calibration.py:31); it does not inventory the corpus or other rounds. Its `resolved` condition additionally checks the specific correction/criterion/lesson/source signals (lines 33–40). Therefore `unresolved=0` is local to this predicate, not evidence of corpus-wide consensus.

## Explicit limits

- One disagreement: the unique S432 `Disagree` entry in the named round-61 verifier spot-check; preserve it and the existing S432 source row. Do not mark the row rejected or rewrite the historical verifier record (contract.md:7,9).
- One knowledge entry: append a correction to `corpus/knowledge/response-header-expectations.md` using the substantive S432 §3.6 sentence and explain its support; preserve old prose (contract.md:7,9).
- One quality rule: append a criterion that located quotes must substantively support associated claims, grounded in the verifier finding. This is not a general corpus audit or automatic resolution of other cases (contract.md:7; ScoutQUALITY.md:9,14–16).
- One bounded subject: Fetch-defined `X-Content-Type-Options`; the claim makes no assertion about a property's live headers (contract.md:9).
- Calibration ceiling remains; no second claim or promotion of extra axis work (contract.md:11).

## Falsification cases

1. The committed correction only substitutes another generic lead-in, or lacks the substantive §3.6 text and explanation: the claim's quote-correction requirement is not satisfied, even if a string-level counter were to recognize a matching substring.
2. The QUALITY addition merely repeats quote existence, locator, or digest checks without requiring semantic relevance to the attached teaching claim: it does not establish the claimed substantive-support criterion (ScoutQUALITY.md:5,9,12,16).
3. The old S432 disagreement row or source row is deleted/rejected, or the verifier record rewritten: violates explicit preservation limits (contract.md:7).
4. An unrelated round/corpus disagreement remains: this does not falsify this narrow claim; any report that treats `unresolved=0` as proof of all-corpus resolution is false scope expansion (counter.py:31–40).
5. The correction, criterion, lesson gate, or source pointer is absent in the measured committed revision: the frozen conjunction is false (contract.md:7; counter.py:33–41).

## Evidence / commands

- Read `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/contract.md:7` and `:9-11` (frozen scope and limits).
- Read `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py:31-43` (actual S432-only disagreement count and conjunctive resolution logic).
- Read `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/w1/ScoutQUALITY.md:5,9,12,14-16` (criterion gap and substantive-support requirement).
- No commands were run; no claim, counter, criterion, source, score, or other lane file was modified. Only this assigned report was written; no scoring or counter action was taken.
