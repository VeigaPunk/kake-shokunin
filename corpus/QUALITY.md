# Kake publishing-evidence quality bar

Source: `corpus/lessons/round-20.md`; local CLI evidence in
`.ufo/round-20/{baseline-proof,candidate-proof}.json`. This is the first
quality-bar file in the inspected lane, not a reconstructed historical mint.

| Criterion | Admit | Reject | Grounding |
|---|---|---|---|
| Citation-local absence | A deleted publishing-source citation carries its own annotation under P1's documented local rule, or is fixed to a verified surviving source. | Borrowing a historical annotation from a different occurrence, including a canonical-home alias, or treating membership in `pathsMissSet` as permission to leave a live instruction unmarked. | Round-20 mixed, same-file, alias and brace CLI cases; `scanCitations` reports `unannotatedCites`. |
| Replayable claim | The report names the source revision or script digest, exact argv, full verdict and exit; frozen input expectations pin their bytes. | An old HTTP result presented as current, a selftest tally substituted for a live-corpus measurement, or a partial/offline run presented as a complete publishing check. | Round-20 separates isolated proof from path/offline acceptance; online checks are not authorized. |
| Missing substrate stays visible | Source/history unavailability is marked as named debt with an owner and concrete restore-or-retire action. | Re-pinning a missing source or weakening the gate solely to recover a green verdict. | Round-19 lesson's deleted-source debt and round-20 false-green reproduction. |
| Admission authority | Local implementation evidence is labelled local; specialist dispatch and non-author review are evidenced separately. | A rendered 32-scope plan counted as an executed wave, a launch counter counted as verified rounds, or a self-dispatched reviewer treated as independent promotion authority. | Round-20 route blocker; canonical `LEARNING.md` outside spot-check rule. |
| Shape-only probe environment | Record override variable names and lane-local isolation shape; use symbolic placeholders in captured output. Keep replay paths only as ordinary fixture metadata. | Serializing assigned environment values or copying env-derived paths from stdout, even when generated locally. | Round-20 shape-only evidence erratum and `.ufo/round-20/redaction-validation.json`; the initial representation was rejected and corrected without rewriting history. |
| Absence annotation content (r20 resume) | The annotation names the exact missing target and its dated absence event, and says the cited recipe is a historical record, not an executable instruction. | Any absence word that merely falls inside the ±2-line window (the sweep accepts it; this bar does not), or an annotation beside a still-imperative command. | `corpus/lessons/round-20.md` §Round-20 resume (26-location disposition; critic counterexample: selftest fixture F passes on an unrelated "missing"). |
| Platform mechanism (r20 resume) | A claim about what a hosting, CI or crawler platform serves, ignores or validates cites a tier-A row in `corpus/SOURCES.md` at a pinned tag, commit or dated doc, with a recheck argv. | Inferring platform behaviour from repo files or workflow shape alone; taking a version, date or mechanism from a tier-B/C source without a tier-A recheck. | `corpus/lessons/round-7.md:21-25` (served set inferred from workflow shape); `corpus/knowledge/publish-channels.md:9` (CNAME file read as domain config); `corpus/lessons/round-20.md` §Round-20 resume. |
| Validator is not identity (r20 resume) | A validator claim names the generating mechanism, decodes the literal, and states what it cannot prove; content identity uses a normalized digest. | An ETag flip read as a content change, a matching ETag read as byte identity, or a fetch from another replica offered as refutation. | `corpus/lessons/round-16.md:35-38`; `corpus/knowledge/ghp-etag-anatomy.md`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Self-source confinement (r20 resume) | Write-region markers are exact standalone comment lines; a mutation case plants a write at every out-of-region function and must see each one caught; the report names the API list it covers. | A marker matched anywhere in a line (header prose or checker literals opening the region); a passing tally with no planted out-of-region write. | `corpus/lessons/round-19-recensus.md:44`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Population unit named (r20 resume) | Every dead-path or count claim names its population (live citations, unannotated locations, pinned miss-set), the scanner contract and the command. | Reporting counts from different units (77 live citations, 8 fleet hits, 26 unannotated locations) as one number. | `corpus/lessons/round-19-recensus.md:52-53`; `corpus/lessons/round-20.md` §Round-20 resume. |
| Index continuity (r20 resume) | An edit to index or list prose keeps or explicitly supersedes every continuation line; the diff is read before commit. | A sentence left ending mid-clause with no continuation or pointer. | `corpus/README.md:60-63` (continuation dropped in `dd4eabf`, restored from `cd5b381`); `corpus/lessons/round-20.md` §Round-20 resume. |
| Append-only tails (r20 resume) | A correction or absence note in an existing file is an appended tail; every base line survives byte-for-byte once the tails are stripped (checked by a stripped-diff over `git show <base>:<file>`). | Inserting characters into the original words, or dropping table delimiters, while "appending". | `corpus/lessons/round-20.md` §Mistakes R2 (backtick inserted at `round-4-aggregator-audit.md:31`; trailing pipes dropped at `SKILL.md:227` and `corpus/README.md:26`; restored before commit). |

Source tiers (A/B/C, scoped per claim) are defined in `corpus/SOURCES.md`;
admission stays here.

The ±2-line vocabulary heuristic is not a semantic classifier. An admitted
local annotation does not prove a historical publish recipe is executable.
No credential values, session bodies, raw journals or external target probes
belong in this round's corpus evidence. Criteria changes append a superseding
row and its motivating lesson; they do not erase earlier criteria.

## Post-review append-only ruling — round 20

The orchestrator rejects the earlier “Append-only tails” criterion: a suffix
changes the original line's bytes and hash even if its old text survives.
Superseding rule: preserve every prior lesson/knowledge line byte-identically;
use pure new-line additions or end-of-file correction blocks citing the old
line. Never split a table to satisfy the citation-local gate. An adjacent
standalone note is allowed only with an inbound-anchor movement census and
corrections for moved pointers; otherwise leave the location uncleared.
Grounding: `corpus/lessons/round-20.md` §Post-review fixes; the original
criterion remains above as rejected history.

## Historical metadata and reconstructed gates — round 21

Grounding: `corpus/lessons/round-21.md` §Mistakes; S019's local audit of the
canonical corpus contract. A provenance header records the original evidence
date/revision and names whether that evidence is historical; installing a
header is never live re-verification. A retrospective Gate names its
reconstruction round and leaves absent admission, rejection and non-author
review records explicitly unknown. A heading count alone cannot prove those
decisions occurred.

Metadata prefixes preserve every prior byte. Where adding new lines moves
inbound literal pointers, the round ships a same-byte line mapping and a
correction register; frozen historical evidence is not rewritten. Reject a
green structural census as proof of source restoration, publishing readiness,
or independent round admission.

### Bounded confinement and pointer coordinates — round 21

Clarification of “Self-source confinement” above: round-20 enumerators cover
named function declarations and their pinned API/site payload population,
not arrow functions, methods or every possible write mechanism. API coverage
is the list in `scripts/freshness-sweep.mjs`'s confinement comment; aliases,
bracket/split calls, metadata/fd operations and child processes remain outside
that proof. Grounding: `lessons/round-21.md` and `w1/Round20Debt.md` under the
round-21 wave evidence.

All pre-round-21 literal pointers into knowledge entries that receive the
four-line metadata prefix retain their baseline coordinates. Add four for
current coordinates, using the round-21 lesson's explicit per-file register.
This supersedes the unqualified current-coordinate reading of old pointers
in this file; it does not rewrite the historical lessons they cite.

## Canonical signal and reconstruction ordering — round 22

Grounding: `corpus/lessons/round-22.md` §Mistakes and the non-author
`round-21-verifier-spotcheck.md` routed notes 1–4.

- A reconstructed Gate names its observation revision and is written only
  after the sources it cites exist. Read-time absence statements remain
  historical and require an explicit correction register; never invent their
  original admission chronology. The old round-4/9/16 Gates fail this current
  criterion and remain superseded only by round21's existing register.
- A canonical preflight proves the declared signal matches explicit publisher
  policy over the named static-file population. It never proves Google's
  selected canonical, content duplication, live delivery or JavaScript state.
  Source recommendations are distinguished from stricter local policy.
- An unregistered evidence helper's red diagnostics cannot be relabelled as
  gate success. The round21 anchor census is intentionally outside gate claims.
  Legacy missing-path reds are carried, not counted as a round22 improvement.
- SHONEN marks do not advance from a local fixture/corpus repair: an end-to-end
  domain task and all other boxes still need a named independent non-author
  verifier. This round's own seats remain author-side; no promotion is claimed.

### Derived counts and resolver neighbours — round 22 recovery

Grounding: `corpus/lessons/round-22.md` §Recovery attempt 2 Mistakes;
`.ufo/waves/round-22/w2/{FalsifyCounting,Attack05,BoundaryCLIErrors}.md`.

- A counting command derives its numerator from per-case rows against the
  digest-pinned oracle and cross-checks every declared aggregate (accepted,
  discrepancies, matrix exit) against them. A count that repeats the
  instrument's own declared total is not evidence. An unmeasurable baseline
  (instrument not validated) exits nonzero, never with the "proven absent" code.
  Fails if `postfix/counter-probe.py` against the counter exits 0.
- Every URL-resolution branch of a gate has a one-character adversarial
  neighbour outside the frozen claim population (selftest or probe), because
  a frozen positive case (`scheme_relative`) does not cover its malformed
  sibling (`///path` with an empty authority). A stdlib join or split is never
  the validator (S027-S029). Fails if `postfix/defect-probe.py` against the gate exits 1.
- A documented output contract ("always one JSON object") covers every exit
  path including usage errors, and an argument that can be repeated either
  has defined multi-value semantics or is a usage error; "last value wins"
  never decides a verdict.

### Correction register — round 23

Grounding: `corpus/lessons/round-22-verifier-spotcheck.md` routed notes 1–3.

- **[r23-correction 2026-10-21]** In "Derived counts and resolver neighbours —
  round 22 recovery" the first criterion's last sentence ("Fails if
  `postfix/counter-probe.py` against the counter exits 0.") inverts the
  predicate: counter-probe.py exits 0 when every counter-example is rejected.
  Read it as: the criterion fails if `counter-probe.py` against the counter
  exits nonzero (any counter-example accepted). The defect-probe sentence
  ("exits 1") is correct as written. The original line stays for history.
- A receipt that names a disposable runner path (`/tmp/...`) must carry the
  command that recreates the runner from Git (e.g. `git show <commit>:<path>`);
  a tmpfs path alone is not evidence. Round 22's runners are recorded in
  `.ufo/waves/round-22/postfix/REPRODUCE.md`.
- Recovered misroot files keep their content but live with the wave evidence
  that produced them, not at the lane root.

### Parser relaxations and live receipts — round 23

Grounding: `corpus/lessons/round-23.md` §Mistakes; `.ufo/waves/round-23/w1/{FalsifyForeignContent,CritCounterC1,CritCounterC2}.md`.

- A change that turns an unsupported input class into an evaluated one lists
  every way the newly evaluated region can feed the decision (for canonical:
  base, head, canonical link, end-tag mismatch, raw-text hiding, integration
  points) and ships a probe for each. Fails if
  `python3 .ufo/waves/round-23/relaxation_probe.py --validator scripts/canonical_audit.py`
  exits nonzero.
- A freshness receipt counts only with at least one claim decided against a
  live surface; "surface gone" is recorded as UNVERIFIABLE with a reason and is
  never relabelled HOLD. A presence claim whose surface is gone is STALE.
- A live-page receipt states what it proves: the policy result of the bytes
  served at `fetchedAt`. Receipt coverage (reproducible receipts / population)
  is reported separately from policy outcomes (clean / failed-policy /
  not-served); a 404 is never a canonical result.


Round-23 falsifier clarification: canonical policy is not redirect/navigation readiness. A meta-refresh page may match its declared canonical; that never implies publish approval. A counting command validates receipt structure and replay consistency, not the truth of a claimed GET/HOLD: author seat observations and the non-author review must establish the latter. Select operationally load-bearing claims, not merely convenient live URL statuses (w2/HoldDriftDetection, HoldFleetRegistry, HoldOpsAutomation, HoldVaultProperties).


## Receipt-field parsing and recovered-source pins — round 24

Grounding: `corpus/lessons/round-24.md` Mistakes; outside r23 closure in MANIFEST rounds[394]; `.ufo/waves/round-24/w1/ReviewQualityCriteria.md` (captured-by: none for the two counter gaps).

- Parse every receipt field against its documented grammar and JSON type before method calls or comparisons. Timestamp fields use real calendar/offset validation and the declared commit-time bound, never a date prefix; JSON booleans do not stand in for numeric exits/counts. Preserve producer-legal nullable headers and accepted controls. A nonzero process exit accompanied by a Python traceback is a crash, not a successful rejection. Fails if the fixed-population `python3 -B .ufo/waves/round-24/measure_c2.py --root . --revision <commit> --json` exits nonzero or either pristine C1/C2 replay control rejects.
- Reconcile recovered tokens as well as new misses: each re-pin has a dated observation; a recovered target leaves pathsMissSet so its next disappearance is armed. Original corpus lines remain byte-identical under the round20 ruling; line-hash-bound sidecars plus separate correction blocks replace suffix edits. Restoration notes carry no absence vocabulary, preventing neighbour annotation bleed. Fails if `python3 -B .ufo/waves/round-24/measure_c1.py --root . --revision <commit> --json` is nonzero or `node scripts/freshness-sweep.mjs --selftest` loses its recovered-list/sidecar/vocabulary controls.

These round-bound counters establish the named frozen expectations, not a universal schema proof or current publication readiness. A later filesystem change requires a new dated reconciliation; rerunning a historical paths measurement against a changed host need not stay green.

## Accessibility preparation and complete source reads — round 25

Grounding: `corpus/lessons/round-25.md` Mistakes; S035 WCAG 2.2 section 5.2.

- A source adapter's abstract-only result is not a normative source read.
  Open the pinned official document and locate the criterion body; retain
  the source bytes and digest. A card quote must be in normativeText, never
  merely a heading, doclink, badge or informative note.
- A complete accessibility-review packet is preparation, not a website
  assessment. Every card and every tool JSON result retains not-assessed.
  Reject a source-only, automated-only or partial-page conformance claim;
  full pages, complete processes, accessibility support and non-interference
  remain required by S035. The packet selftests exercise false status and
  heading-quote rejection; an unrun witness is not a proved repair.
- A policy-interrupted assignment stays held. Changing a role, provider or
  wording is not permission to repeat it. Round25's new accessibility
  preparation is separate work and carries no round24 admission credit.

### Round-25 falsification refinements

Grounding: `corpus/lessons/round-25.md` build/falsify dispositions and
`.ufo/waves/round-25/w2/{ReviewTool,ReviewCounter,ReviewLimits,ReviewSelftest}.md`.

- Source-reviewed card prose is judged by people, not a nonempty-string rule.
  The readiness gate reports only structure and quote binding; the finite
  measurement additionally pins the exact reviewed card bytes.
- A candidate that ships a tool must ship its own pinned inputs. Only an
  absent-tool baseline may use a separately pinned source oracle; a Git read
  failure is not evidence of absent capability.
- JSON interoperability applies to every new packet input, not merely an
  older receipt profile: duplicate members, non-finite constants and
  unsupported nesting are could-not-evaluate with JSON, not last-value-wins
  or a traceback. These are local data-profile choices.
- A heading-quote fixture must contain enough words to survive the quote
  floor and must include raw text beside normativeText, so a haystack
  regression can actually fail. Status fixtures include an unlisted value
  and missing key, not only a denylist that the test itself teaches.
- A review finding quotes the actual saved field, never a reconstructed
  complete source sentence. Review322's reported29-word quote did not match
  the stored25-word field; its unrelated semantic findings were still kept.

## Recheck adjudication — round 26

Grounding: `corpus/lessons/round-26.md` Mistakes (vacuous, stale-premise,
survivor rows) and `.ufo/waves/round-26/statements.json`.

- A recheck HOLD needs a row-specific located quote: page chrome or any text
  that also occurs in a different source's bytes cannot ground a row. Formats
  of one document (RFC 9110 html/txt) may share text but need distinct quotes.
  Fails if `python3 -B .ufo/waves/round-26/measure.py --selftest` loses its
  boilerplate_quote case.
- STALE means the statement is wrong or unsupported at its own stated scope.
  A historical verified-at date, a pointer explicitly scoped to a base
  revision, or a patch-version label in the same documented family is not a
  stale claim; record it as a note. A statement whose attribution was false
  even at its base revision is STALE.
- A text extractor decodes character references exactly once; a second
  unescape turns literal `&lt;` text into markup. Fails if
  `.ufo/waves/round-26/text_selftest.py` loses its double-escape cases.

- Falsify-wave addendum (round 26): wording that is weaker than, or consistent
  with, the source is not STALE; nor is a locator shape judged HOLD for other
  rows. Such admitted tags stay (append-only) and are counted as
  `reclassified`. Fails if `measure.py --selftest` loses
  `statement_tags_unaccounted` or `reclassified_accounted`.
- A recheck covers every corpus statement that cites a rechecked row, not only
  files listed in `usedBy`; derived locators (offsets, digests) are re-derived
  after any extractor change.
