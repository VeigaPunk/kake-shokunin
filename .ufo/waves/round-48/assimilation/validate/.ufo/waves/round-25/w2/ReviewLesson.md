# Round 25 lesson / record audit

**Axes:** operability (tally and admission integrity); freshness (pinned-source identity and pointer validity).

## Findings

### 1. Source review is not full packet admission; two residual semantic corrections remain unsubstantiated

The current records do **not** claim that 55 cards establish an AA website pass. The lesson expressly rejects that inference and keeps every card and tool result `not-assessed` (round-25 lesson lines 37–50); the packet doc separates packet readiness from website conformance; QUALITY rejects source-only, automated-only and partial-page conformance claims (round-25 QUALITY section). `SOURCES.md` also defines “included” as retained in the registry, not admitted as a knowledge claim. W1 `SourceReview.md`'s “COMPLETE — no errors found” is scoped to the pinned source population and membership, not card semantics or round admission; that report expressly excludes quote validation from its scope.

However, the current assembled cards still do not express two corrections required by `.ufo/waves/round-25/residual-card-review.md`:

- **2.2.2:** the review asks the limitation to say that Guideline 2.3 adds flash-safety requirements without waiving applicable 2.2.2 conditions. The current limitation instead says “Flickering or flashing content is addressed by Guideline 2.3, not this card,” although the same card's publisher check includes blinking items. It does not resolve the identified scope ambiguity.
- **2.3.1:** the review asks the example to establish both that the flash exceeds the general-flash threshold and that it is not below both thresholds. The current example says a full-frame white strobe flashes about five times per second and has no threshold analysis; it does not state either threshold conclusion. Absence of analysis alone does not establish the criterion's failure condition.

The residual review is author-side and says these corrections must precede any final admission assertion. The current lesson does not name either applied correction or a final measured revision; it says proof execution remains pending. No revision-bound measurement receipt was found under the round-25 wave paths (the only `*measure*` match is `measure.py`). **Disposition:** no full packet/capability admission is supported by these records yet. This is not a finding that the source population is wrong, nor a live-site conformance result.

### 2. Source quote count: correction is accurate

The lesson's Gate originally labels its §5.2.2 excerpt as 12 whitespace-delimited words. The appended erratum corrects it to **10**, which is correct. The excerpt is “Conformance (and conformance level) is for full web page(s) only” (tokens: `Conformance` / `(and` / `conformance` / `level)` / `is` / `for` / `full` / `web` / `page(s)` / `only` = 10). It matches the words in the pinned HTML at `.ufo/waves/round-25/source-wcag22.html:2192`; inline anchor markup does not add a word. For distinction, the full sentence continuing “and cannot be achieved if part of a web page is excluded” is **22** whitespace-delimited words. The packet doc repeats the same 10-word excerpt. No quote-wording defect remains in the lesson after its erratum.

### 3. Audited counts and tense

- Pinned population JSON contains **55** criteria: **31 A + 24 AA**. Current card JSON contains **55** statuses, all `not-assessed`. These are static-record counts, not a successful CLI or counter result.
- `SOURCES.md` contains S035 as a mined tier-A source; its round-25 search log says identified 1 / screened 1 / included 1 / excluded 0. That is one curated source row, not a claim that a website was assessed or the round admitted. The lesson's historical “34→35 rows”/“original 34 unchanged” statement is not independently checked against a pre-round source snapshot in this review.
- W1 `w1-outcomes.json` supports the lesson's dispatch accounting: 64 spawned; 63 credited completions; one terminal-failure seat; 64 retained reports because the later PacketTool draft is retained but uncredited; zero replacements. W2 spec lists 64 seats: 55 reviewers, 4 critics, 2 connectors, 2 scouts, 1 scribe. Thus the lesson's 128 total is a dispatched-seat count, not 128 completions. The separate residual review identifies six W2 card-review seats that died on capacity and says they remain uncredited; it is not an independent replacement or outside verifier.
- SCORECARD labels round 25 “declared,” gives an intended after-state, and says execution/outcomes are appended only after observation; it also says a capability-table row requires an observed working run. Its “Score stays 10→10 (HOLD)” should therefore be read as a provisional no-admission hold, not a measured post-run result. LOG likewise says measurements are recorded only after running. No observed round-25 measurement is reported in these records.

### 4. Nonexistent pointer is disclosed and replaced; external source not independently opened

The round-25 lesson records that `corpus/lessons/round-24-verifier-spotcheck.md` was not present; an exact path lookup here also returned “Path not found.” The current lesson identifies the disposition instead as the user-provided “rejected-honest-stop closure rounds[407]” and explicitly says the missing path is not a local lesson. That resolves the dangling local filename in the current lesson, but the external `rounds[407]` record itself was not opened in this review. The historical W1 ClaimCritic note that the round-25 lesson “does not exist yet” is time-scoped to its earlier report; the lesson now exists.

### 5. Legacy policy-stop debt is retained, not erased

The lesson, SCORECARD, LOG, contract, and candidate record consistently state that round-24 C1/C2 remain unadmitted, refused/interrupted work is not retried or rerouted, and the L0 policy-stop disposition remains open. The new packet grants no round-24 credit. I did not open or rerun any round-24 interrupted probe, counter, or code.

## Gates and behavior represented

The packet is publisher-side preparation for the pinned 12 December 2024 WCAG 2.2 Recommendation. Its intended behavior is an offline structural inventory plus one manual-review aid per selected A/AA criterion; all card outcomes remain `not-assessed`. S035 supports that source scope and the stated WCAG conformance boundaries. It cannot establish page-level results, a complete evaluation, or conformance.

## Surfaces and provenance reviewed

- `corpus/lessons/round-25.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`.
- `corpus/knowledge/accessibility-review-packet.md` and `accessibility-review-cards.json` (static JSON queries: 55 cards and 55 `not-assessed` statuses).
- `.ufo/waves/round-25/contract.json`, `contract-amendment.json`, `candidate.json`, `population.json`, `w1-outcomes.json`, `w2-spec.json`, `residual-card-review.md`, `w1/SourceReview.md`, `w1/ClaimCritic.md`, and the pinned `source-wcag22.html`.
- Pinned source digest recorded by the source/lesson records: `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057`; the exact quote was read at HTML line 2192.

## Checks, limits, and out-of-scope

No shell or executable command, build, test, counter, or formatter was run for this review; no tool was installed or updated. The documented measurement command is `python3 -B .ufo/waves/round-25/measure.py --root . --revision <commit>`; it was **not** run. Static reads, JSON queries, and path lookup only. This report does not claim source-byte baseline continuity, a completed outside spot-check, a measured after-state, or live website accessibility. No production files were edited.

**Only file written:** `.ufo/waves/round-25/w2/ReviewLesson.md`.