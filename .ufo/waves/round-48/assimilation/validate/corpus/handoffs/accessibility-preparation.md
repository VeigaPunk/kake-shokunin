# Accessibility review preparation — operator handoff, round 25

Owner receiving this prepared packet: **the property operator**.
Preparation author: kake. Browser and assistive-technology evaluation recipient:
**tabi**, only after the operator names the target, scope and authorizes that
separate evaluation. Credential custody, if later required, belongs to **kagi**;
this handoff includes no credentials and authorizes no account operations.

## Delivered preparation

- Standard: S035, W3C WCAG 2.2 Recommendation of 12 December 2024.
- Fixed population and official bytes: `.ufo/waves/round-25/population.json`
  and `.ufo/waves/round-25/source-wcag22.html` (paths relative to lane root).
- Criterion-specific review instructions:
  `corpus/knowledge/accessibility-review-cards.json`.
- Scope, decision table and conformance limits:
  `corpus/knowledge/accessibility-review-packet.md`.
- Readiness command: `python3 -B scripts/accessibility_packet.py --root . --json`.
- To display the actual assignment instructions, not just readiness totals:
  `python3 -m json.tool corpus/knowledge/accessibility-review-cards.json`.

This is the completed preparation work item. Its outcome is a source-bound
manual-review packet, not a commissioned or completed evaluation of a property.
No target property or user process is asserted to have passed, failed, or been
excluded. All card statuses remain `not-assessed`.

## Operator decision needed before any evaluation

The operator must name the property, delivered build/revision, full page set,
responsive/interactive variants, complete user processes, intended WCAG level,
relied-upon technologies and claimed accessibility-support combinations.
Record whether a conforming alternate version is being relied upon and why
it meets the standard's definition; an arbitrary alternate page is not enough.
Include third-party content and technology that is not relied upon when
scoping non-interference. No action is taken if this scope or permission is
missing; packet readiness alone grants no authority.

## Required evaluation record

After authorization, the named evaluator keeps a separate work item in the
operator's chosen evaluation system and links it back to this handoff. Every
criterion/page/process decision must name:

| Field | Required meaning |
|---|---|
| property / full-page set | Exact authorized URLs and included complete processes |
| delivered build / revision | What was actually evaluated, not an assumed checkout/deployment match |
| criterion / version / level | S035 criterion id and intended conformance target |
| variants / technology support | Responsive and interaction states, relied-upon technologies, browser/AT combinations and support evidence |
| method / raw observation | Human procedure, source or rendered evidence, tool/product versions, and limitations |
| reviewer / evaluation date | The evaluator who made the judgment and when |
| applicability / rationale | Why the criterion applies or does not; no silent omission |
| finding / evidence pointer | Judgment confined to the named build/scope with a resolvable record |
| authorization | Operator's explicit permission for the evaluation and any account interaction |

The shared record requirements apply to **every** card in addition to its
criterion-specific `evidenceNeeded`. They are not inferred from whether a card
happens to contain the words date, reviewer or build. No site-specific judgment
is stored back into the reusable packet's fixed `not-assessed` status.

## Boundaries

The structural gate does not semantically validate human instructions or
establish WCAG conformance. Card prose is source-reviewed by people, and the
round's finite measurement pins the reviewed packet bytes. Automation that
finds zero issues, a complete checklist, an isolated page, a canonical signal,
or a source-only inspection cannot replace the full WCAG conformance
requirements. Publishing remains an operator action after any separate fixes
and evaluation. The earlier round-24 policy-stop remains unrelated and open.
