# Criterion 2.5.7 — Dragging Movements (AA)

**Verdict: Agree with the card's core interpretation, with one exception-detail correction recommended.**

## Finding — Low: Essential exception is not operationalized

- **Card field / exact text:** `publisherCheck`: “Treat a function as exempt only when there is a documented reason that dragging is essential”; `evidenceNeeded`: “A written rationale for any claim that dragging is essential”.
- **Source anchor:** [2.5.7](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#dragging-movements) links “essential” to [the definition](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#dfn-essential): “if removed, would fundamentally change the information or functionality of the content, and information and functionality cannot be achieved in another way that would conform”. Both conditions are required. The card asks for a reason but leaves this defined threshold unstated, so a reviewer could accept a broad, ordinary-language claim that dragging is merely necessary or useful.
- **Minimal correction:** In `publisherCheck`, specify that removing dragging must fundamentally change the content's information or functionality **and** there must be no other conforming way to achieve it. In `evidenceNeeded`, request a rationale addressing both limbs. Frame documentation as evidence for this review, not as an extra WCAG conformance condition.

## Checks that agree

- The card's `id` (`2.5.7`), `title` (`Dragging Movements`), `level` (`AA`), and `source` URL match the saved population entry and the pinned source section. `status` is `not-assessed`.
- `sourceQuote` is an exact 22-word substring of the criterion's `normativeText`, within the packet's quote-length rules. It ends after the essential exception, but the `publisherCheck` also includes the user-agent exception, so the excerpt does not omit that exception from the card's operative guidance.
- The `publisherCheck` correctly asks for the same result via a single pointer without dragging; its tap/click and click-to-select/click-to-place examples are consistent with the `single pointer` definition (one point at a time, including mouse, single finger, or stylus). The drag-to-upload, sortable-list, and task-board examples are plausible review examples, not blanket claims that those patterns fail.
- The user-agent exception and the note excluding actions required to operate the user agent or assistive technology are represented. The limitation correctly says keyboard operability alone does not satisfy this pointer-specific criterion.
- The failure example illustrates dragging-only functionality without asserting that every task board must provide a particular UI. The evidence requirement calls for a reviewer-performed non-dragging procedure and comparison, and the limitation disclaims source-only proof and any conformance result.

## Residual risk and verification gaps

No website or implementation was evaluated. The card's user-agent paraphrase (“behavior is provided by the user agent”) is close to, but not verbatim with, the source's “functionality is determined by the user agent”; matching the latter wording would remove minor interpretive latitude. The card's `not-assessed` status and limitation appropriately preserve that boundary.