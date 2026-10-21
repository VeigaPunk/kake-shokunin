# Review 312 — WCAG 2.2 SC 3.1.2 Language of Parts

**Recommendation: Disagree (one actionable omission).** The card is correctly identified and remains explicitly `not-assessed`, but its review population is restricted to parts differing from the page default. That misses a required language override in nested content.

## Finding — nested return-to-default phrases can be skipped

- **Card field / exact substring:** `publisherCheck`: “List every passage or phrase whose human language differs from the page default” (and “For each one…”). The same page-default-only scope appears in `evidenceNeeded`: “inventory of foreign-language passages and phrases per reviewed page or state”.
- **Why this is misleading:** On a page whose default is English, suppose a French passage has a programmatic French language declaration and contains a nested English phrase. The nested phrase matches the page default, so it is excluded from the card's inventory, but it inherits the French declaration unless its language is reset. The language of that phrase is therefore not programmatically determinable as English. This is a 3.1.2 failure despite every passage differing from the page default being inventoried. The criterion covers “each passage or phrase,” not only parts differing from the page default; checking only default-relative differences is insufficient when a marked passage contains a return to the default language.
- **Source anchor:** Saved REC source `#language-of-parts` (source-wcag22.html lines 1789–1800), especially the complete criterion at lines 1795–1797: language of “each passage or phrase” must be programmatically determinable except for the four listed exceptions. Its linked `#dfn-programmatically-determinable` definition (lines 3501–3516) defines the software-extractable information and gives markup and accessibility-API examples. The linked `#dfn-human-language-s` definition and note (lines 3081–3089) and `#dfn-text` definition (lines 3903–3908) do not add an exception for nested phrases that happen to match the page default. There is no note in the criterion section itself.
- **Minimal correction:** Change the inventory/check scope to cover each passage or phrase whose actual language differs from the *effective programmatically determined language at that point*, including a return to the page-default language inside a region declared in another language. Verify that the effective language matches the actual language for each such part (while retaining the four criterion exceptions). Reflect that scope in `evidenceNeeded`, rather than limiting it to “foreign-language” passages.

## Checks that are sound

- `id` `3.1.2`, title `Language of Parts`, level `AA`, and source URL match the pinned population entry (`population.json` lines 376–382).
- `sourceQuote` is an exact opening substring of the complete normative criterion and does not exceed the requested 25-word limit.
- The four exclusions in `publisherCheck` match the criterion's four express exceptions. The requirement to record exception rationales is useful review evidence, not a claim that WCAG itself mandates a rationale record.
- The failure example of an unmarked French quotation on an English page is a plausible 3.1.2 failure. `limitation` explicitly denies any page pass/fail/conformance finding, and `status` is `not-assessed`; neither source-only evidence nor packet readiness is presented as conformance.

## Verification gap

No LSP device was available (`xd://lsp` returned “No such tool”), so no LSP status/references/definition/diagnostics were obtainable. This review is based on direct reads of the assigned card, pinned population, and saved source; no website or runtime was tested. No tools were installed or updated.