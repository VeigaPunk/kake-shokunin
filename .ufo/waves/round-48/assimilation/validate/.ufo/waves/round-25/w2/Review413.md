# Review413 — card 4.1.3 Status Messages (AA) semantic review

Reviewer: KakeR25.Review413 (author-side falsification, not independent closure). Round 25, C1 accessibility packet.
Grounds: pinned source `.ufo/waves/round-25/source-wcag22.html` (S035, WCAG 2.2 REC 2024-12-12), §4.1.3 at anchor `status-messages` (line 2145) and glossary entries `dfn-status-messages` (line 3804), `dfn-change-of-context` (line 2716); card at `corpus/knowledge/accessibility-review-cards.json` (entry `"id": "4.1.3"`); population entry `.ufo/waves/round-25/population.json` (`"id": "4.1.3"`, line 493).
Method: read-only; no network, browser, or website contact. Programmatic checks: quote substring containment via documented whitespace normalization, word count, id/title/level/source equality against population, status field.

## Verdict: AGREE — card is source-faithful. No blocking defect. One minor wording nit.

## Verification matrix (criterion-specific)

- **Identity**: `"id": "4.1.3"`, `"title": "Status Messages"`, `"level": "AA"`, `"source": "https://www.w3.org/TR/2024/REC-WCAG22-20241212/#status-messages"` all equal the population entry; source line 2149 shows `(Level AA)`. No duplicate or stray 4.1.3 card in the file.
- **Quote**: `"sourceQuote": "status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus"` — verified exact contiguous substring of the population `normativeText` under the packet's whitespace normalization; 25 whitespace-delimited words (at the inclusive 25-word cap, legal). Starts/ends at word boundaries, case preserved.
- **No invented requirements**: SC 4.1.3 is a single sentence in the REC with no notes or exceptions (source lines 2145–2153: doclinks, level marker, one `<p>` only). The card invents none. `publisherCheck` explicitly states `"Specific ARIA roles and implementation sequences are possible techniques, not additional requirements of this criterion"` — this is the exact criterion-specific trap (reading aria-live/role="status" as mandated) and the card pre-empts it rather than committing it.
- **No omitted scope/exception**: the two normative limits are both captured in `limitation`: (1) markup-language scope — matches "In content implemented using markup languages"; (2) the status-message boundary — definition requires a "change in content that is not a change of context" (glossary, line 3804), and the card's claim that the criterion does not reach `"messages delivered by moving focus"` is grounded: `dfn-change-of-context` lists "focus;" among "Changes in context include changes of:" (line 2716). The change-of-context note (informative) is not upgraded to a MUST anywhere in the card.
- **No informative→MUST inversion**: `publisherCheck` frames browser/AT evaluation as a request to a separately authorized evaluator, not as a WCAG obligation; "Distinguish WCAG-defined status messages from changes of context using the normative glossary" points at the normative definition rather than substituting a technique list.
- **No source-only-as-conformance**: `evidenceNeeded` demands runtime evidence (DOM before/after, focus location, AT transcript with product/browser versions); `limitation` states source inspection "cannot establish ... whether assistive technologies actually announce them without focus". Status remains `"status": "not-assessed"`.
- **Failure example accuracy**: `failureExample` (plain div, no role or aria-live, focus unchanged, success message inaudible) is the canonical 4.1.3 failure shape: the message is a status message by definition (success/result of an action, no change of context) yet cannot be programmatically determined. Not a misstatement.

## Findings

### Minor 1 — evidence template presupposes the insert-into-container idiom
- Field/substring: `evidenceNeeded`, substring `"the role or live-region attributes on the container and the inserted text"`.
- Why: role/property semantics may sit on the inserted/changed element itself, and a status message can also be a text replacement or removal, not only an insertion; the phrasing reads as if a live-region container plus inserted text were the expected shape.
- Severity: minor — this is a work-aid evidence checklist, not a normative restatement, and any role-based implementation is still covered by "the role ... attributes"; it cannot inflate WCAG requirements.
- Minimal correction: `"showing the role or live-region-related attributes on the changed element or its container, and the inserted or changed text"`.

### Verified-fidelity notes (no change required)
- `publisherCheck` compresses the definition's four limbs to "an action's result, a waiting state, progress, or errors". Only `sourceQuote` is verbatim-bound; this paraphrase drops no normative content that would mislead triage ("success or results of an action, on the waiting state of an application, on the progress of a process, or on the existence of errors" — glossary line 3804).
- `limitation` correctly keeps "changes of context" and focus-delivery out of scope, matching the normative definition chain status message → change of context → focus.

## Residual risk / verification gaps

- Review relied on the committed population extract plus the retained source bytes; `normativeText` for 4.1.3 matches the visible source paragraph, but per-criterion note-stripping elsewhere was not re-derived here (out of scope for this card).
- "Accessibility support" evidence sufficiency (whether a single AT transcript establishes the "can be presented" capability) is a conformance-methodology judgment the packet explicitly defers to the authorized evaluator; the card already scopes that honestly.
- No tool installs or updates were performed (existing python3 only; all pacman transactions paused per host policy).

## Discipline

Read-only production; only this report written. No fleet/sibling/domain-tree/Git/jj changes, no delegation, no live targets, no r24 work.
