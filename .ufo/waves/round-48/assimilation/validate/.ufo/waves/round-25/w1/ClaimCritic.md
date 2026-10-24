# ClaimCritic — round 25 C1 (operability capability)

Seat: `KakeR25.ClaimCritic`, read-only critic. Axes: operability, freshness.
Inputs: `.ufo/waves/round-25/contract.json` (C1), `population.json`, `source-wcag22.html`, `w1/SC*.md` (55 scout cards),
`corpus/knowledge/accessibility-review-cards.json`, `corpus/knowledge/accessibility-review-packet.md`,
`scripts/accessibility_packet.py`, working-tree diff of `corpus/SOURCES.md`. Round-24 material was not read or run.
Counterexamples ran in memory by importing `validate()` with deep copies; nothing in the repo was written apart from this report.

## Verdict

C1's direction is sound. The 55 cards add a human-executable review checklist plus an offline structural-readiness check, and they do not assert website conformity: every card is `not-assessed`, the output carries the constant `websiteConformance: "not-assessed"`, and the packet doc's conformance-boundaries section cites §5.2.1–5.2.5.

Two measurable overclaims remain, and both are fixable:

- **OC1:** "source-grounded" is enforced only by raw substring containment, with no minimum length.
- **OC2:** "validates … source bindings" is false, because the tool trusts any 55-row `population.json` without binding it to the pinned hash.

A third risk sits in the counter. If the counter gates on `accepted`, it can admit a packet that the tool itself marks `failed`.

## Evidence (observed)

| Check | Result |
|---|---|
| `sha256(source-wcag22.html)` | `6e3c5fe3…7057`, equal to `population.sourceSha256` |
| `sha256(population.json)` | `4751dc24db2e3698c2b276bb81bff57412c8fbf6c1c0a62f1aa2ad9e0f903058` (untracked at the time of the check) |
| Population | 55 rows: 31 A, 24 AA, no duplicates. 4.1.1 is excluded, and the source marks it "Parsing (Obsolete and removed)" |
| Notes in `normativeText` | 0 notes leak in. The source says notes are informative ("…diagrams, examples, and notes are informative") |
| Scout cards | 55 of 55 pass structurally: keys exact, metadata exact, every quote contained verbatim and 6–25 words, status `not-assessed`. All 55 `publisherCheck`, `evidenceNeeded`, `failureExample` and `limitation` values are distinct (no boilerplate) |
| Assembled `accessibility-review-cards.json` | A 55-element list, identical to the scout cards |
| `validate(pop, cards)` pristine | `clean`, accepted 55, exit 0 |

The conformity-lexicon hits in card prose (pass, fail, conform, meets, satisfy) occur in 54 of 55 cards. On inspection, nearly all of them are disclaimers in `limitation`, such as "does not establish pass/fail/conformance". The `publisherCheck` hits are reviewer instructions, not claims. Examples: 2.5.2 "the function meets the No Down-Event option" and 3.3.4 "rather than marking them as passed". So no card prose asserts that a site conforms.

## Counterexamples (in-memory, against `scripts/accessibility_packet.py`)

| # | Mutation | Tool result | Impact |
|---|---|---|---|
| CE1 | `sourceQuote = "a"` on all 55 cards | **clean, accepted 55, exit 0** | OC1: the grounding check is vacuous. The same applies to a lowercase heading word such as `"keyboard"`; 9 of 55 titles occur case-insensitively in their `normativeText` |
| CE2 | `sourceQuote = "on"` | failed (51 accepted) | Only incidental; substring matching works at the character level, not the word level |
| CE3 | Every `normativeText` gets `+ " fabricated"` and `sourceSha256 = 0…0` | **clean, accepted 55, exit 0** | OC2: nothing binds the population to the pinned bytes. Because the candidate commit carries both the cards and the population they are judged against, this is a duplicate authority |
| CE4 | Every `limitation` set to "This site passes and conforms to WCAG 2.2 AA."; every `publisherCheck` set to "Already verified: conformant." | **clean, accepted 55, exit 0** | The no-conformity claim is guarded by `status` only. A lexicon gate is **not** a safe fix, because the legitimate disclaimers (54 of 55 cards, CE5) would all fail it. This is a tradeoff left to human review |
| CE5 | An extra `4.1.1 Parsing` card appended | `failed`, but **accepted = 55**, exit 1 | A counter that gates on `accepted<55` would admit a packet the tool rejects |
| CE6 | `level` changed to `"a"` | failed, 54 accepted | Correctly rejected |

The doc's sentence at line 94, "Substituting a heading for a grounding quote: require a nonempty quote of at most 25 … words from `normativeText`", does not hold. Exact title substitution is blocked only because no title occurs case-sensitively in its `normativeText`. A lowercase heading word, or any character, passes (CE1).

## Falsification requirements C1 must survive

These are measurable; the counter or the selftest should fail if any of them is violated.

1. **F1, population pin.** `sha256(population.json)` at the measured revision equals a constant recorded in `measure.py` (currently `4751dc24…3058`). Otherwise exit 2. Alternatively, re-derive id, title, level, anchor and `normativeText` from `source-wcag22.html`, after first checking `6e3c5fe3…7057`. This kills CE3.
2. **F2, quote substance.** The quote is token-aligned (it starts and ends on word boundaries of `normativeText`), and it has at least `min(6, words(normativeText))` words while staying at or under 25. All 55 current cards already meet this: the minimum is 6, and 2.4.6 has 7 words in its whole text. This kills CE1 and CE2 without changing any card.
3. **F3, counter gate.** Admit only when the tool exits 0, `verdict == "clean"`, `accepted == expected == 55`, `len(criteria) == 55`, `findings == []`, and `websiteConformance == "not-assessed"`. It must also agree with the counter's own independent per-card derivation. Gating on `accepted` alone fails on CE5.
4. **F4, no result surface.** The only status value is `not-assessed`; any additional card key fails with `fields_mismatch`, which already holds. The output schema must contain no per-criterion pass, fail or applicability field. The packet selftest should assert that `status ∈ {passed, failed, inapplicable, conformant}` each yields `status_not_assessed`, not just `"passed"`.
5. **F5, the 4.1.1 negative.** A selftest case adds a `4.1.1` card and expects exit 1, `metadata_mismatch`, and a non-clean verdict even though `accepted == 55`.

## Measurable overclaims and the smallest safe corrections

- **OC1.** The doc's lines 94–96 and the decision-table row at line 71 ("Source quote and title match → refers to the pinned criterion") overstate what the quote check enforces.
  - **Fix:** add the F2 check in `validate()` and a selftest case for the one-character quote (expected finding: `quote_not_from_source`, or a new stable id such as `quote_too_short`; coordinate with PacketTests).
  - **Tradeoff:** none, since current cards are unaffected.
- **OC2.** The doc's line 41 says the command "validates the packet's structure and source bindings", but the tool binds cards only to whatever `population.json` it reads.
  - **Fix:** apply F1 in `measure.py`, which is the authority for admission.
  - **Optional:** the tool could check `population.sourceSha256` against the sibling `source-wcag22.html`, but that would not catch a population edited while the HTML stays the same. The real pin is the population hash in the counter.
- **OC3, minor false provenance.** The 1.3.1 and 2.5.3 quotes carry extraction spacing artifacts that the REC doesn't render. The 1.3.1 quote is "Information, structure , and …", while the pinned HTML has `structure</a>,`. In all, 30 of 55 `normativeText` values contain space-before-punctuation artifacts.
  - **Fix:** document in the packet doc that quotes are verbatim against the pinned extraction (`normativeText`), not against the rendered REC.
  - **Alternative:** normalize spacing identically in the tool, the counter and the population. That changes the population hash, so do it before pinning or not at all.
  - **Do not** normalize in the tool only; that would split the authority with the counter.
- **OC4, pending reference.** `SOURCES.md` S035 and the doc's line 102 cite `corpus/lessons/round-25.md`, which does not exist yet. It must land in the same commit, or the provenance is dangling.

## Does C1 add an executable publisher review capability?

The packet adds **executable readiness** and a **human-executable review checklist**. It does not add executable review, and the contract's "after" text claims exactly that, so this is not an overclaim. The operability delta is real: before, there was no bound A/AA inventory; after, there are 55 validated, distinct, criterion-specific cards. However, `measure.py` measures card validity. It does not measure whether a publisher can run a review. The packet doc's step 4 routes results to a separate work item, which is the correct design, since keeping `status` fixed is what blocks a conformity claim.

## One source-grounded manual evidence workflow (3.1.1 Language of Page, Level A)

**Source:** the S035 `normativeText` for 3.1.1, "The default human language of each web page can be programmatically determined". The card for 3.1.1 is the one in `accessibility-review-cards.json`.

This workflow needs no browser, live site, account or publishing; it runs offline against the publisher's own build output.

1. **Scope.** Record the build revision and the list of built HTML documents that make up the in-scope pages. Name each locale variant separately. Per the packet doc's step 1, do not infer the served build from a checkout.
2. **Extract the declaration.** For each document, record the `lang` value on the root `html` element exactly as delivered in the built file, or "absent".
3. **Human judgment.** A reviewer reads each page's human-readable content and records the predominant language. Then they record whether the declared value identifies that language. Absent, empty, or mismatched (for example, `en` on German pages) gets noted with a reason.
4. **Evidence record,** one per page, in a separate work item and not in the packet:
   - page or template id
   - build revision
   - declared value and where it came from (file path)
   - the language the reviewer identified
   - a one-line rationale
   - reviewer and date
5. **Falsifiable output.** "Not established" for any page lacking a record. The packet card stays `not-assessed`. A complete set of records supports a 3.1.1 finding for those named pages and that named build only.
6. **Limits.** Programmatic determination via the delivered markup is a source fact. Whether it matches the content is human judgment. Language changes within passages belong to 3.1.2. Conformance additionally requires the doc's §5.2 boundaries: full pages, complete processes, accessibility support and non-interference.

## Impacted axes

- **Operability:** OC1, OC2 and F3 decide whether the "accepted 55" figure means anything. The fixes are small: one validate predicate, one counter constant, one gate expression.
- **Freshness:**
  - The source is pinned as the dated 2024-12-12 REC, and the saved HTML names `https://www.w3.org/TR/WCAG22/` as its "Latest published version".
  - The `on-release` cadence has precedent in S001, S002, S019, S026 and S027.
  - [INFERENCE] I did not check whether a WCAG 2.2 version newer than 2024-12-12 exists, because this seat ran offline. SourceReview should confirm the latest-version check date.
- **No regression found** in existing corpus files. The only modified tracked file is `corpus/SOURCES.md`, with one additive row and one round paragraph.

## Checks the main agent should run after integration

- `python3 -B scripts/accessibility_packet.py --root . --json` (expected: exit 0, clean, 55)
- `python3 -B scripts/accessibility_packet.py --selftest`
- `python3 -B .ufo/waves/round-25/packet_selftest.py --root .`, including the F2 and F5 cases
- `python3 -B .ufo/waves/round-25/measure.py --root . --revision <commit>`, including the F1 hash pin and the F3 gate

No tools were installed or updated.
