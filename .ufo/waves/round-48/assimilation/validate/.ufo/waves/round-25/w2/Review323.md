# Review323 — card 3.2.3 Consistent Navigation (AA), author-side falsify wave r25

Scope: single criterion card `"id": "3.2.3"` in `corpus/knowledge/accessibility-review-cards.json` (card object begins at line 530) vs saved pinned source `.ufo/waves/round-25/source-wcag22.html` (criterion section at line 1883, normative paragraph line 1889) and `.ufo/waves/round-25/population.json` (entry lines 402–410). Read-only semantic review; no website, browser, or code edits.

## Verdict: AGREE — card is faithful; no defect found

Falsification axes attacked, each grounded in the saved source:

1. **Quote hygiene (pass).** `sourceQuote` — `"Navigational mechanisms that are repeated on multiple web pages within a set of web pages occur in the same relative order"` (21 words) — is an exact case-sensitive word-boundary prefix of `normativeText` (population.json line 409; source line 1889). The criterion body is a single sentence with no note wrapper inside the section (source lines 1883–1892), so no heading/link/conformance-label text leaked into the quote.

2. **No important exception omitted (pass).** The SC's only exception is `"each time they are repeated, unless a change is initiated by the user"` (source line 1889). The card carries it in `publisherCheck`: `"Treat a reordering as covered by the exception only when the user initiated that change (for example the user rearranged or customized the menu), and record what the user did."` That matches the normative clause without tightening (e.g., no demand for a persistent preference mechanism) or widening (no claim that any reordering is fine). The exception cannot fit inside the quote itself: the full sentence is 34 words against the packet's ≤25-word cap, so truncation is structural, and the truncated prefix is mitigated by the explicit exception handling two fields later.

3. **Check phrasing matches the governing definition (pass).** `publisherCheck`'s `"confirm that items appearing on several pages keep the same order relative to each other"` correctly encodes `#dfn-same-relative-order` (source lines 3700–3705): "same position relative to other items" plus its Note that items remain in the same relative order "even if other items are inserted or removed from the original order" (source line 3704). The card scopes comparison to shared items and never demands an identical item set, so benign insertion/expansion of navigation (the definition's own expanding-menu example) is not falsely criminalized.

4. **Failure example is a genuine failure (pass).** `failureExample` permutes a four-item menu (Home, Products, Support, Contact → Support, Home, Contact, Products). Pairwise, this inverts Home↔Support and Products↔Support while the item set is unchanged — a true relative-order change not explainable as insertion/removal, explicitly stated as occurring "without any user action", so the exception does not apply. It is a valid instantiation, not a misstatement.

5. **No conformance leakage (pass).** `status` is `"not-assessed"`; `limitation` states the card "is a manual-review aid only and does not establish conformance; no website was evaluated" and denies that source inspection or scans can alone decide set membership, mechanism status, or user-initiation. No source-only evidence is offered as conformance anywhere on the card.

6. **Scope honesty on an undefined term (pass).** "Navigational mechanism" has no glossary definition in the saved source (its only occurrence is the criterion sentence itself, line 1889). The card handles this honestly: it exemplifies (main menu, breadcrumb, footer links, search, skip link) and `limitation` assigns the judgment "which mechanisms count as repeated navigation" to human review. The closing limitation sentence — the criterion "constrains relative order of repeated mechanisms, not page-specific navigation that is not repeated" — matches the SC's repeated-on-multiple-pages scope and the `#dfn-set-of-web-pages` binding (source line 3736).

## Observations (not defects)

- `publisherCheck`/`evidenceNeeded` require capture of both the rendered visual sequence and the programmatic reading/focus sequence. That exceeds the normative sentence, but it is framed as evidence-capture methodology for the publisher's own review, not as what the SC text requires, and the limitation blocks conformance claims. Conservative over-capture risk only: a publisher could record a programmatic-order divergence that a reviewer would not treat as an SC violation; the card's wording does not itself misclassify that as a failure.
- The `sourceQuote` ends mid-sentence before the exception clause; safe here because `publisherCheck` carries the exception, but a quote read in isolation would read exceptionless. Structural to the 25-word cap; no correction that fits the cap.

## Tooling

No tools installed or upgraded; read-only review satisfied with bundled read/grep. No commands run against packet scripts (not assigned; suite runs once at integration).
