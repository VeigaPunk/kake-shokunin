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
No seat output exists for them; the L1 authored their planned deliverables
directly (recovery attempt 2 correction of an earlier "integrates their
reachable prose work" wording, w2/FalsifyAdmissions Finding 1). Full
routing/death evidence is in `.ufo/waves/round-22/w1-deaths.json` and the
wave registry.

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

## Recovery attempt 2 (2026-10-21)

Attempt 1 ended without a report (`.ufo/watchdog.log` 2026-10-21T02:47:17
`lane-dead-no-report kake round=22`). Recovery coordinator: KakeR22Recovery,
operator-authorized; the claim base `7c61c8c`, the frozen contract, the 32-case
population and oracle are preserved unchanged.

### Reuse and discard

- Reused after re-verification: landed `c0fd6d5` (validator, matrix, cases,
  fixtures, contract, measure/replay, S020-S027, knowledge entry, QUALITY round-22
  criteria) and checkpoint `26b27af` (w2 reports). Re-verified: matrix 32/32 at
  the post-fix tree, cases/fixtures/matrix/contract byte-identical to `c0fd6d5`
  (`residual/CritAdmission.md` Attack 2), round-21 spot-check notes 1-4 already
  mapped to QUALITY lines 75-94.
- Integrated: the 43 w2 seat reports that exist. Of 64 w2 seats, 21 left no report
  (dead; never respawned, never credited): Attack23, ReopenRFC6596,
  ReopenGoogleCanonical, ReopenGoogleTroubleshoot, ReopenHTMLLink, ReopenHTMLBase,
  ReopenHTMLTemplate, ReopenPythonParser, ReopenPythonURL, BoundaryManifestKeys,
  BoundaryTraversal, BoundaryURLAuthority, BoundaryHeadRecovery,
  BoundaryInertContexts, BoundaryAttributes, BoundaryReadOnly,
  BoundaryReplayIntegrity, ConnectBrowser, ConnectSource, ConnectCapability,
  ConnectProof (9 reviewer, 8 scout, 4 connector). Their `/tmp/kake-r22-*`
  scratch directories are unverifiable partial work and are discarded.
- Discarded as claim evidence: attempt-1 `measure-before.json`,
  `measure-after.json` and `replay-integrated.json` (instrument/validator since
  changed); they stay as attempt-1 history. Superseded by
  `measure-before-v2.json`, the post-land `measure-after-v2.json`, and
  `postfix/replay-after.json`.
- Budget: attempt 1 spent 128 seats (w1 64, w2 64); 72 remained, below a genuine
  64-item wave of distinct new work after the dead w2 items (which may not be
  replaced). One ordinary task call of 8 residual seats (6 reviewer, 2 critic)
  attacked the fixes; round total 136.

### Wave-2 defects fixed (author-side; admission stays with the closure)

| Defect | Source | Fix | Before → after |
|---|---|---|---|
| `///path` / `//` / base `///` silently inherit the document host: false clean | w2/Attack05 | reject a `//` reference with empty authority (S028, S029) | defect probe false on `c0fd6d5` → met |
| usage errors print no stdout JSON | w2/BoundaryCLIErrors P2a | print `{"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}`, exit 64 | probe false → met |
| repeated `--manifest`, last path wins | w2/BoundaryCLIErrors P2b | usage error | probe false (clean) → met (64) |
| manifest symlink followed; manifest dir and pages resolved separately | w2/BoundarySymlinks | one directory fd, manifest opened no-follow; caller prefix documented as followed | probe false → met |
| `alias/../manifest.json` audits a lexical, different file | residual/CritScope P2 | split without `abspath`, kernel resolves once | probe false → met |
| counter repeats the matrix's declared numerator | w2/FalsifyCounting CE1 | derive from rows vs pinned oracle; cross-check aggregates | counter probe CE1 accepted → rejected |
| unmeasurable baseline exits 0 | w2/FalsifyCounting CE2 | exit 2 when the instrument is not validated | CE2 exit 0 → 2 |
| self-consistent stub matrix passes the counter | residual/ResRevCounter P2 | pin matrix/cases digests in the counter; `executed >= derived` | CE3 accepted → rejected |
| replay compares aggregates only | w2/FalsifyAdmissions F2 | per-case exit+findings vs pinned oracle | shown able to fail by residual/ResRevReplayRepin |
| help synopsis advertises `--selftest [--json]` | residual/ResRevCliUsage P3 | explicit usage string | text fix |
| intermediate dir fd can leak if close raises | residual/ResRevManifestFd P3 | transfer ownership before close | fault-injection finding, fix by inspection |

`frozen/expected.json` re-pins only the validator digest
(`35433e50…` → `5de32200…`); the oracle (`cases.json`, exit 0, 32/32) is unchanged.
The last five rows' fixes were applied after the residual seats returned and
were not re-reviewed by a seat; probes and the selftest exercise them.
Evidence: `.ufo/waves/round-22/postfix/{defect-probe,counter-probe}-{before,after}.json`,
`selftest-after.json` (62/62; `c0fd6d5` selftest 56/56 has none of the new cases),
`replay-after.json`.

### Sources opened in recovery (Gate receipts)

| Row | URL | Access | Location and quote |
|---|---|---|---|
| S028 | https://www.rfc-editor.org/rfc/rfc9110.txt | 2026-10-21 | Section 4.2.1 (same in 4.2.2): “A recipient that processes such a URI reference MUST reject it as invalid.” |
| S029 | https://www.rfc-editor.org/rfc/rfc3986.txt | 2026-10-21 | Section 3: “When authority is not present, the path cannot begin with two slash characters ("//").” |

Admitted: both, tier A, mined by `corpus/knowledge/static-canonical-preflight.md`
and this lesson. Not opened, not a row: WHATWG URL slash-skipping (the policy
rejects both readings). No existing row's status/recheck/used-by changed.
Independent re-open: `residual/ResRevSources.md` (digests match both rows).

### Recovery mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| frozen-population blind spot: a positive case hides its malformed one-character sibling | w2/Attack05; `postfix/defect-probe-before.json` | none (32 frozen cases only; no neighbour rule) | QUALITY "resolver neighbours" criterion + selftest cases; shown able to fail: defect probe 2/8 on `c0fd6d5`, 8/8 now |
| count-only oracle: the counter certified a numerator it never derived | w2/FalsifyCounting; residual/ResRevCounter | wave-1 FrozenReplay F5 warned; nothing enforced it | QUALITY "derived counts" criterion; counter probe fails on the `c0fd6d5` runner (3/3 accepted), passes now |
| dead-seat credit wording | w2/FalsifyAdmissions F1 | QUALITY dead-seat rule (not applied to own lesson text) | line 81 reworded above; no score depended on it |
| lexical path normalisation in a no-follow design | residual/CritScope P2 | none | kernel resolves the manifest path once; probe `dotdot_after_symlink` fails before, passes now |

Misroot sweep (2026-10-21, `git -C /home/vgpnk/Projects/shokunin status --porcelain`):
no kake-authored file at the fleet root; `-.rej` (charter-scribe census
content) and `.ufo/state/*` belong to others and were left untouched.
A residual seat left `scripts/__pycache__/` in the lane; removed, never committed.

Tool installs/updates in recovery: none. pacman pause respected.

### Measurement (recovery)

`python3 .ufo/waves/round-22/measure.py --root . --revision b539cc17c25e5f42fe8803e2aa42b4574c4b44c6`
→ exit 0, accepted 32/32 derived from rows, two identical runs
(`measure-after-v2.json`); baseline `--revision 7c61c8c… --cases-root .` → exit 0,
accepted 0, available false, instrumentValidated true (`measure-before-v2.json`).
Same runner sha256 `fa916ada…` both sides. Final suite: corpus-contract exit 0;
paths gate exit 1 with the carried 3-target / missSet-55 red and no new miss
(`final-suite.txt`). Census after: exit 0 (`census-after.txt`).
