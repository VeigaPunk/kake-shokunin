# Review — WCAG 2.5.2 Pointer Cancellation

**Verdict: Disagree (two low-severity clarifications).** The card has the correct id, title, Level A, source URL, a criterion-body quote, and `not-assessed` status. Its check covers the four alternatives and Note 1; its limitation includes Note 2's boundary. It does not present source inspection or packet readiness as website conformance. The issues below are narrow wording gaps, not a finding that the packet reports a conformance result.

## Findings

### Low — The limitation treats essentiality as something shown by operation

**Card field:** `limitation`; substring: “Only human operation shows whether an abort, undo, or up-reversal option actually works, or whether completing on press is essential.”

**Source:** `source-wcag22.html#pointer-cancellation`, Essential option and Notes 1–2 (around lines 1656–1662); `source-wcag22.html#dfn-essential` (lines 2967–2974). Essentiality is defined by whether removing the behavior would fundamentally change the information or functionality **and** whether it can be achieved another conforming way. Note 1 separately deems keyboard/numeric-keypad emulation essential. That is a reasoned assessment of the function and alternatives, not an outcome established merely by operating the page. The sentence overstates the need for human operation as evidence for this option.

**Minimal correction:** Separate behavioral observation from the Essential judgment, e.g. “Manual operation can show whether an abort, undo, or up-reversal works. Assess Essential against the definition and Note 1, and record the rationale.”

### Low — The failure example does not explicitly rule out Up Reversal

**Card field:** `failureExample`; substring: “The item is gone before the pointer is released.”

**Source:** `source-wcag22.html#pointer-cancellation`, Up Reversal (around lines 1653–1654): “The up-event reverses any outcome of the preceding down-event.” The example establishes a down-event deletion and says there is no “undo or restore option,” but does not explicitly state what releasing does. An automatic restoration on release could satisfy Up Reversal without an offered undo option, so the stated observations alone do not unambiguously establish a failure.

**Minimal correction:** Add that releasing leaves the item deleted (the up-event does not reverse the deletion). The existing no-cancel/no-undo details otherwise make the example clear.

## Residual risk and verification gaps

No website or runtime was tested; this review is limited to the card and the saved WCAG source, as assigned. The criterion's four alternatives, the essential definition, and both criterion notes were checked against the pinned source. No tools were installed or updated.