# CriticCalibrationMeaning — round 62

## Counterexample / judgment

A source-quote correction plus a new QUALITY criterion is not, by itself, evidence of a measurable *calibration axis move*. It can be a source-quality improvement and a structural gate addition without showing the system learned to distinguish correct from incorrect admissions. In particular, the frozen counter checks for exact substrings, not quote truth, semantic support, application to decisions, or changed admission outcomes. A candidate can satisfy both checks by appending the mandated words while retaining the same mistaken decision behavior.

The strongest concrete counterexample is a text-only append to `corpus/knowledge/response-header-expectations.md` containing the exact `QUOTE`, `S432 §3.6`, and `Round-62 correction` strings, plus a row in `corpus/QUALITY.md` containing `substantive located quote` and `round-61-verifier-spotcheck.md`; no disagreement is adjudicated and no future case is tested. The frozen predicate would count `quote_correction=1` and `criterion=1` (subject to the other gates), despite no measured calibration change. Conversely, the source itself does support the bounded substantive quote: retained S432 §3.6, lines 6151–6154, says the `X-Content-Type-Options` response header can require checking a response's `Content-Type` header against request destination. That establishes source grounding, not that the prior admission decision was corrected or that future decisions improve.

## Evidence and axis separation

- Frozen contract `.ufo/waves/round-62/contract.md:5-10` defines the claim as resolving the unique round-61 disagreement, adding the quote correction and criterion; it also explicitly bounds the policy to Fetch's defined field and disclaims claims about live headers.
- Frozen instrument `.ufo/waves/round-62/c62_calibration.py:16,33-35,39-42` tests literal inclusion and conjunctive gate text. It counts disagreements from the spot-check but sets `unresolved=0` whenever correction, criterion, lesson gate, and source row exist; it does not inspect a changed disposition or independently assess criterion application. Thus its measured construct is completion of required textual/gate artifacts, not calibration quality.
- Source evidence `.ufo/waves/round-61/sources/S432.html:6149-6154` is normative §3.6 body. Its substantive sentence is materially better than a generic lead-in and supports the narrow policy statement. That is the source-quality/attribution axis.
- Calibration would require evidence that the admission rule now discriminates: preserve the original disagreement identity and non-author dissent, state what evidence would change the ruling, then apply the criterion to a fixed, independently judged set of relevant cases with before/after decisions and an error/disagreement measure. The source quote alone cannot provide that outcome evidence.
- A QUALITY criterion can improve future source adjudication if it requires a located substantive quote and a separately reasoned support link; a criterion's presence is not proof it was followed. The corpus's own QUALITY.md:7-10 distinguishes criterion definitions from grounded evidence, while its lines 25-29 warn criteria changes append a superseding row and motivating lesson. The current round's criterion phrase is too opaque by itself to establish semantics or application.

## Impacted axes

- **Source quality / provenance:** positive, grounded improvement if the correction identifies the §3.6 body rather than the generic lead-in and explains its actual support.
- **Calibration / learning:** not established by the current literal counter; only potentially supported by a preserved disagreement disposition plus independently measured application/outcome evidence.
- **Measurement validity:** materially limited: artifact-presence predicates are proxies for the stated behavioral construct, and the `resolved` shortcut can erase the disagreement without observing its disposition.

## Smallest safe correction

Do not alter the frozen claim, counter, criterion, or score. Report the distinction and avoid claiming a measured calibration move from substring completion. For any next calibration claim, freeze a small, fixed set of independently adjudicated admission cases and an explicit before/after outcome measure; retain the S432 disagreement and dissent as an identity-bound case, and have the QUALITY rule require both a located substantive source passage and a reasoned link to the specific admission decision. Treat the current round as source-grounding plus gate-artifact evidence unless the canonical judge finds separate behavioral evidence sufficient.

## Reproduction evidence

Commands run (read-only):

```sh
# Read contract, frozen instrument, retained source body, and QUALITY.md
```

Observed lines are cited above. No lane files were modified other than this assigned report; no counter or score was run or changed.
