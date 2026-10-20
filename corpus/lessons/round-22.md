# Round 22 — offline static canonical publishing preflight

Date: 2026-10-20. Baseline master: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.

## Claim

C1, operability capability: introduce a read-only local canonical-policy
preflight, measured against a frozen 32-case positive/negative matrix. Baseline
has no lane-owned canonical validator (accepted cases 0/32, unavailable), not
32 observed wrong answers. Candidate must accept all matrix expectations,
including stable finding ids and exit codes. The claim contract and case names
were frozen before dispatch in `.ufo/waves/round-22/contract.json`.

This is a capability move under SCORECARD's saturation line 10 and one-round
stagnation window: round 21 added no capability. Freshness stays unchanged;
old network evidence is not re-verified. No numeric score increase is claimed.
The validator compares a publisher's declared canonical with an explicit local
policy, not Google's selected canonical. It reads serialized static HTML with
an explicit head; no browser, JavaScript execution, headers, redirects, target
content comparison, indexing proof, live property probe or publishing action.

## Gate

Candidates: an offline publisher-side canonical-policy validator; its frozen
32-case matrix and revision-bound counter; source-backed knowledge of the
canonical signal, relative references, first base and parser limitations.
Author-side implementation and rejection decisions are recorded below after
integration. Independent admission and admit/reject spot-check belong to the
orchestrator's non-author closure, never this L1 or its seats.

Rejected scope: recovering green by changing the legacy missing-path pin set;
calling an HTML-policy match live freshness or search-engine selection;
crediting dispatched/dead seats as completed review; interpreting reconstructed
historical Gates as contemporaneous decisions.

### Sources opened for C1 (2026-10-20)

All new rows are tier A scoped primary sources; no old row's status/recheck/
used-by cell changes. Located quotes below are each at most 25 words.

| Row | URL | Location and quote |
|---|---|---|
| S020 | https://www.rfc-editor.org/rfc/rfc6596.html | Section 3: “Specify a relative IRI (see [RFC3986], Section 4.2).” |
| S021 | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | The rel=canonical link element: “Even though relative paths are supported by Google, they can cause problems in the long run” |
| S022 | https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting | Opening paragraph: “Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons” |
| S023 | https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | Section 4.6.8.4: “The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document.” |
| S024 | https://html.spec.whatwg.org/multipage/semantics.html#the-base-element | Section 4.2.3: “If there are multiple base elements with href attributes, all but the first are ignored.” |
| S025 | https://html.spec.whatwg.org/multipage/scripting.html#the-template-element | Section 4.12.3: “The template contents of a template element are not children of the element itself.” |
| S026 | https://docs.python.org/3/library/html.parser.html | HTMLParser introduction: “This parser does not check that end tags match start tags” |
| S027 | https://docs.python.org/3/library/urllib.parse.html | urlsplit warning: “urlsplit() does not perform validation.” |

The Python URLs opened as Python 3.15 documentation; that version labels the
documentation, not the installed runtime or claimed tested interpreter.
Living Standard citations are date-anchored, not immutable revision pins.
C1's knowledge entry cites S020/S021/S026/S027; the remaining rows ground its
implementation/rejection boundaries in this Gate. Matrix expectations are
explicit local publisher policy, not a second platform conformance standard.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| retrospective-chronology | `round-21-verifier-spotcheck.md` routed note 3: old Gates in round-4:50, round-9:185, round-16:171 describe S019/round21 as absent and are superseded only by the round21 register | QUALITY historical metadata rule lacked a source-landed-before-reconstruction condition | Append a QUALITY criterion requiring retrospective decision records to name the observation revision and source-landed ordering; leave historical Gates untouched and point readers to the existing round21 correction register. |
| signal-is-not-selection | RFC 6596 section 3 permits applications to ignore improper canonical designations; Google canonical guidance describes a signal, not a guarantee | QUALITY Platform mechanism / Replayable claim | Bound C1 to declared publisher-policy comparison; the negative frozen cases must fail and positive controls must stay clean. Runtime rejection evidence is recorded after integration. |

## Carried review and operational boundaries

Round 21's non-author admission remains authoritative: C1 historical provenance
4/21→21/21; C2 fixed baseline lesson Gates 1/15→15/15. That work was not live
re-verification. Its routed debts remain unchanged: paths red (three targets,
four old citation locations, missSet55), broad anchor-census red with 78
baseline-inapplicable diagnostics (not a gate), reconstructed chronology only
superseded by the round21 register, and SHONEN not independently checkable.
Restore-or-retire and publishing remain operator-owned. No protected verifier
or aggregator file is writable here.

L1 holds the canonical planner seat; the validator excludes planner from swarm
roles. Build wave is a single validated 64-seat dispatch. Four scribe seats died
at provider startup with `anthropic/claude-haiku-5-5` HTTP 429 rate_limit_error,
`retry-after-ms=8182000`; no output or completion credit and no replacement.
The L1 integrates their reachable prose work. Full routing/death evidence is
in `.ufo/waves/round-22/w1-deaths.json` and the wave registry.

Tool installs/updates by L1: none. All pacman transactions remain paused;
no package, host-service, credential/account or domain-facing operation is
included. Private implementation clones are temporary author workspaces, not
landed evidence; their delivered files and receipts must be committed here.

## Pre-execution policy clarifications

Wave1 reviewers exposed ambiguities before any L1 candidate run. L1 freezes:
empty or ASCII-whitespace-only href is `canonical_href_missing`/exit1,
invalid first base is `base_url_invalid`/exit1 (stricter local policy than
browser fallback), absent explicit head is `html_unsupported`/exit2.
Duplicates count link elements, not distinct normalized target strings;
cardinality failure does not choose an arbitrary target to compare.
Any literal fragment delimiter, including a trailing empty `#`, is rejected;
percent-encoded `%23` is not a fragment delimiter. Rel token separation is
ASCII whitespace only, never Python's wider Unicode split set.

These interpretations were sent to the existing Implement/Matrix seats
before their delivered programs were executed; oracle expectations are not
learned from candidate output. Reports recommending another defensible
interpretation remain read-time author proposals, not independent judgments.
The tool is not an HTML5 tree builder. Canonical/base declarations in
ambiguous unsupported contexts such as noscript or foreign content cannot
be promoted to a browser-equivalent clean verdict. Supplementary adversarial
checks remain separate from the frozen32 case denominator.

An actual static publisher source is archived in
`.ufo/waves/round-22/domain-snapshot/`: source
`ufo-fsd-alpha` commit `31c465f15669f744848bd9f5d56191c5085670f7`,
`docs/charter-ufo-fsd/index.html`, with exact blob SHA-256 in provenance.json.
Its expected canonical comes from the lane's pre-existing charter property
policy, not from harvesting the audited tag. This snapshot is not a live
network observation and does not assert that the current deployment matches it.
