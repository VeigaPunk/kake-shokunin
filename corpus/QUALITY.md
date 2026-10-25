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

## Complete knowledge citing sets and scoped synthesis — round27

Grounding: `corpus/lessons/round-27.md` Mistakes and
`corpus/lessons/round-26-verifier-spotcheck.md:11–13,117–123`.

- Expand every member of grouped/range citations before defining the reviewed
  knowledge-file set. Include provenance/date bands and EOF artifact references
  at their own stated scopes; don't drop them because they are not teaching
  claims. A new discovered obligation can enlarge, never shrink, the frozen set.
  Failure witness: the unchanged r26 input has16 unadjudicated pairs even while
  the old row counter exits0. `citing_set.py --selftest` exercises omitted
  range interiors as well as literals, metadata and EOF references.
- Judge each source's contribution to a composite recommendation, and label
  the inferential/local-policy step. A row-level HOLD does not imply support
  for every citing sentence. Do not invent an extra proposition to save an
  irrelevant member of a source range. Rejecting S005's HTML-membership
  attribution does not reject its domain-configuration teaching.
- Historical dates/base coordinates remain historical. Incorrect source-set
  attribution in a metadata band is a separate question: name precisely which
  part is corrected, keep the dated observation, and retain reasonable dissent.
  Presence of a STALE marker is not evidence that its correction is meaningful.
- A pair review is not a universally true file or a HOLD for each statement.
  Preserve inherited UNVERIFIABLE units by identity and do not rewrite earlier
  units to increase a later tally. A syntactic completeness gate and a source
  adjudication ledger are different evidences.
- Freeze expected outcomes before implementation, and retain original counter
  bytes. A stricter implementation repair names the motivating failure, old/new
  source hashes and both original/corrected replays; it must not rewrite the
  original expected set, lower the denominator or turn candidate output into
  its own oracle. Fake/stub-echo tests are not behavioral acceptance evidence.

Scope disclosure, not a weakening of the round26 criterion: this round's
frozen inherited clause is the knowledge-entry citing set for32 prior external
rows. The broader “every corpus statement” policy at lines231–233 remains
open for outside-knowledge lesson/index/registry statements. Their declaration-
revision census and the18 knowledge pairs for excluded S014/S019/S035 are
recorded in the round27 lesson. Neither a green pair count nor this clarification
claims that broader policy satisfied or retires it.

Strict-status refinement from this round's own planning mistake: inventory
carried UNVERIFIABLE subunits before promising all-pair HOLD/supported-STALE.
`seatUnverifiable>0` is not erased by a durable review record. The frozen C1
after-clause is left intact and remains unprovable while those units persist;
the counter's current-consumer selftest must reject that real input, not
invent a clean fixture or reinterpret a review tally as supported truth.
Grounding: round27 lesson Strict C1 section and `strict-c1-disposition.json`.

## Round27 author closure — evidence is not full admission

Grounding: round27 cold-reader reports and `unresolved-acceptance.json`.
Reject whole-claim admission from a fixed16 output predicate, an id-only
fixture tally, or a shape-valid whole-pair HOLD that erases unresolved units.
The real fixed-input behavior and killed mutants remain evidence, but do
not prove untested root/JSON/path/retention boundaries. Known counterexamples
must be named and the claim remain unprovable, not narrowed after freezing.

This round ends honestly stopped: no repertoire or rank credit. The8 actual
retained representations passed their independent checks, yet received HTML
bytes/attributes and general sanitizer/provenance guarantees remain unproved.
Current qualified interpretation replaces the historical six/two pointer;
old measurements/records are retained unchanged. Main's non-author closure,
not any own seat, determines admission.

## Counters and field evidence — round 28

Grounding: `lessons/round-28.md` (Mistakes, Gate) and
`lessons/round-27-verifier-spotcheck.md` routed defects. Defect 1 is repaired
in `scripts/citing_set.py` (round-28 C1); defect 2 is already carried by the
strict-status refinement above; defects 3 and 4 are the second and third
bullets below; the out-of-population debt stays where the round-27 section
records it.

- **A counter must be able to reject a constant.** A counting command for a
  repair claim carries controls on valid input (a clean input stays clean, a
  real defect stays failed, the existing fixture suite still passes) next to its
  defect checks. A gate that refuses everything, or returns a fixed answer, must
  score below the declared after-value. Show it with one recorded mutant before
  the claim is admitted (round 28: `.ufo/waves/round-28/w1a3/MutRefuseAllGate.md`).
  Fails if: the counter, run at a sandbox commit whose gate refuses every
  input, exits 0 (round 28 observed 11/15, exit 1). Limit: the round-28 K1 and
  K2 controls check the verdict, not pair counts, so an always-clean gate is
  rejected only by K3 and K4.
- **Conformance exceptions stay named.** A void smoke run earns no acceptance
  credit, a job that times out without output proves nothing, and report-length
  overruns stay listed by seat. State the fixture-oracle granularity on the
  record: the round-27 runner compares only exit code and the multiset of
  finding ids, so finer differences are outside what a passing run shows
  (routed defect 3).
- **No-harm keeps its measured scope.** A no-harm receipt covers the surfaces
  it names (knowledge prefixes, prior scripts, prior wave files, logged registry
  cells) and is never restated as universal no-harm or general CLI safety. The
  round-24 policy stop stays open, unretried and unrouted until the operator
  rules (routed defect 4).
- **No field data is not a pass.** A Core Web Vitals statement about a property
  names its field source (page-level CrUX, origin-level CrUX, or none) and its
  28-day window end (S039). A missing CrUX record is reported as "no field data"
  with the S038 eligibility checks, and a lab score never stands in for the
  field verdict (`knowledge/field-performance-cwv.md`, S036, S038).

## Fixtures, reason codes and quote truth — round 29

Grounding: `corpus/lessons/round-28-verifier-spotcheck.md:208-230` (routed
defects 1 to 3), fleet `PROTOCOL.md:385-389` (§Gate standard, Self-test), the
committed fixture set `scripts/fixtures/citing-set/` (29 cases, each
`expected.json` holding an exit code and a finding-id list only) and the
round-28 counters `.ufo/waves/round-28/c1_interface_count.py` and
`.ufo/waves/round-28/c2_source_count.py`. This section appends to "Counters
and field evidence — round 28" (`corpus/QUALITY.md:298`). The round-28
bullet "Conformance exceptions stay named" (`corpus/QUALITY.md:317`) stays as
history; the bullets below narrow it and do not replace it.

- **A committed fixture asserts the reason code, not only the finding id.**
  A gate that can emit more than one reason under the same finding id ships
  committed fixtures whose expected values name the reason code next to the
  finding id, and the fixture runner compares it. Reason codes that exist
  only in the gate source are uncovered behaviour, not regression coverage.
  Round 28's gate emitted eight new reason codes (`document_not_regular_file`,
  `document_not_json`, `corpus_directory_missing`, `corpus_empty`,
  `not_a_directory`, `population_id_unreachable`, `revision_not_found`,
  `root_not_repository_top_level`; `corpus/lessons/round-28-verifier-spotcheck.md:70-74`),
  while all 29 committed fixtures assert only the exit code and the
  finding-id list. Fails if: the committed fixture runner passes while no
  committed fixture expectation names a reason code. A round-29 wave-1 seat
  observed `grep -rl reason scripts/fixtures/citing-set` → 0 files, and in code and
  fixtures the reason labels appear only in `scripts/citing_set.py` (the other
  mentions are the round-28 lesson and spot-check prose). Limit: a fixture set that
  names a reason code while the runner never compares it fails the same way.
- **A counter compares the reason code, not only the id.** A counting
  command that grades a repair asserts, per case, the expected exit, the
  expected verdict and the expected reason code of the finding it grades.
  Collecting the observed reason into a summary for display is not a
  comparison. The round-28 counter matched on the finding id only
  (`.ufo/waves/round-28/c1_interface_count.py:141`) and carried the observed
  reason in a display field
  (`.ufo/waves/round-28/c1_interface_count.py:150-151`), so a gate that
  returned the right id with the wrong reason scored a full pass. Fails if:
  the counter exits 0 on a case whose gate output carries the expected
  finding id with an absent or different reason. This bar applies to the
  next round that works the surface; round 29 did not work it (see
  `corpus/lessons/round-29.md`, "Not repaired this round").
- **A Gate quote is found in retained source text.** A Gate quote counts
  only when it is an exact substring of retained visible source text whose
  digest the counter verifies against the round's committed receipt before
  comparing. A shape check (one quote per Gate line, the id, the URL, the
  access date, 1 to 25 words) is quote shape, not quote truth: the round-28 C2
  counter read the quote out of the entry line and counted its words
  (`.ufo/waves/round-28/c2_source_count.py:126-131`) without opening the
  source. Fails if: the counter that grades Gate quotes exits 0 on a
  committed row whose quote is not a substring of the retained text, or whose
  retained text digest differs from the receipt digest. The round-scoped
  counter `.ufo/waves/round-29/c1_quote_truth.py` (digest verification plus
  a one-letter-flip control) shows the shape of such a check; it is
  round-scoped evidence and does not by itself satisfy this standing bar for
  later rounds.
- **A new gate ships its fixtures in the same round.** Round 29 applied the
  first bullet at birth: `scripts/base_path_selftest.py` runs 30 committed
  fixtures under `scripts/fixtures/base-path/`; each `expected.json` names
  exit and verdict, and the 22 defect and input fixtures also name reason
  codes (the 7 controls and 1 usage case pin an empty or absent finding list). Fails if: the runner passes a constant-clean
  or refuse-everything stub (observed 7/30 each, exit 1, in
  `.ufo/waves/round-29/w1/BuildBasePathSelftest.md`).
- **Status of the first bullet today.** The citing-set fixtures fail it now
  (29 fixtures, 0 naming a reason code; wave-2 `QualityCriteriaCheck` also
  showed the selftest still exits 0 with all eight reason codes renamed). That
  is round-28 routed defect 1, carried as open debt, not a pass. Note also
  that the round-29 C1 counter compares quotes after collapsing whitespace, so
  "exact substring" above means exact after whitespace collapse.

## Evidence identity, live-mode bounds and counter granularity — round 30

Grounding: `corpus/lessons/round-29-verifier-spotcheck.md:230-248` (routed
defects 2 to 5), wave-1 seats `ReviewSeatBoundsSweep` and
`DraftLessonMistakes` (`.ufo/waves/round-30/w1/`). The witness scripts named
below are committed at `.ufo/waves/round-30/witness/`. This section appends;
earlier sections stay as history.

- **A seat runs a lane tool that can reach a live surface only with one exact,
  named invocation that the wave context allows.** `scripts/freshness-sweep.mjs`
  reaches owned sites unless `--offline` is in effect: with no flag, or with
  `--section=armed`, `--section=plazir` or its alias `--section=pq14`, it
  fetches the pinned owned sites and runs `git ls-remote` on the pinned
  repositories; `--section=paths` reads the file system only. `--offline`
  can be swallowed: in `--section=armed --repo --offline` the parser takes
  `--offline` as the repo path and the run goes live. `--section=history`
  can spawn `scripts/probe-delta.mjs` (local, no network) and
  `systemctl --user`, and `--selftest` writes to `/tmp/kake-r16/selftest` and
  `$HOME` (wave-1 `ReviewSeatBoundsSweep`, wave-2 `CriticQualityCriteria`;
  `scripts/freshness-sweep.mjs:137-158`, `:590`, `:603`, `:620-621`, `:1025`,
  `:1215`). So a wave context that lets a seat run the tool names the exact
  command line; round 30's wave contexts barred the three live-capable
  scripts entirely. Fails if: a seat report records a run that the wave
  context did not name. Witness:
  `python3 -B .ufo/waves/round-30/witness/witness_sweep_live_mode.py --root
  <lane> --round round-<N> --revision <commit>`, which exits 1 for round 29 at
  `234524c` (naming `.ufo/waves/round-29/w2/NoHarmExistingGates.md:30`).
  Limits: it finds reported runs only, it exempts `--section=history`,
  `--selftest` and bare `--offline`, and a misspelled round (`--round 29`)
  scans nothing and exits 0.
- **A measurement receipt names the revision it measured and the digest of
  the bytes it measured.** A receipt that records a tally, verdict or count
  carries the revision and the sha256 of every tool, counter, gate or runner
  whose bytes it depends on; an absolute tool path is not a digest. Every
  round-30 counter output does (`.ufo/waves/round-30/verification/`), and the
  round-29 demonstration re-run's `.ufo/waves/round-30/r29-rerun/receipt.json`
  names revision `4580c78`, tool sha256 `c5a13a32…1dc0` and selftest
  `e6f21acb…7e4b` (45/45; real input 3 sites, 114 references, 4 findings,
  exits 1/0/1, equal to round 29). Fails if a committed tally file names no
  revision or digest. Witness:
  `.ufo/waves/round-30/witness/witness_receipt_identity.py --root <lane> --wave
  round-<N> --revision <commit>`: exit 1 for round 29 at `234524c` (7
  receipts) and also exit 1 for round 30, because the copied runner output
  `r29-rerun/real-input/summary.json` carries only an absolute tool path (its
  digest sits beside it in `receipt.json`, which the witness does not scan).
  That round-30 miss is recorded, not hidden. Limits: one top-level `sha256`
  key satisfies it, and a misspelled wave scans nothing.
- **A named measurement revision has a committed receipt that names it.**
  Every revision a report or SCORECARD names as measured has a committed
  receipt naming that revision; a glob such as `c1-after-*.json` proves
  nothing about a named revision. Witness:
  `.ufo/waves/round-30/witness/witness_claim_receipt_backing.py --root <lane>
  --report <report> --wave all --revision <commit>`. With the round-29 fleet
  report it exits 1 at `4580c78` and `04637bd` (unbacked `234524c`,
  `7697990`) and 0 at `451e98f`, where `.ufo/waves/round-30/verification/r29-remeasure/`
  is committed. Limits: it reads the report from the working tree, not at
  `--revision`, and applied to the whole `SCORECARD.md` it flags older
  rounds' short hashes, some of which are not lane commits.
- **A counter compares every field its expectation names, and judges a usage
  case on the usage object.** A counter compares, per case, the exit, the
  verdict, every finding field the expectation names and the report counts
  when named; an exit code of 64 alone is not a usage verdict. The round-29 C2
  counter never compares `id`, `page`, `resolved`, `pagesChecked` or
  `referencesChecked`: `.ufo/waves/round-30/witness/witness_c2_field_comparison.py
  --root <lane> --revision <commit>` shows a mutant tool with all of them
  wrong still scoring 30/30. The witness hard-codes that frozen counter, so it
  documents the round-29 defect and cannot pass; it is not a gate for later
  counters. `.ufo/waves/round-30/witness/strict_c2_counter.py` over
  `extended-matrix.json` compares those fields; the extended matrix pins the
  tool's own output at `234524c`, so it is a regression pin, not an
  independent oracle. The round-30 C1 counters compare exit, verdict and the
  (id, reason) tuple, and the strict supplement compares exact finding lists.
- **Status of the round-29 first bullet ("A committed fixture asserts the
  reason code").** For the citing-set gate the bullet now holds for 13 of
  the 25 reason codes the gate can emit (the eight round-28 codes, the two
  new JSON-profile codes, `descending_range`, `span_too_large` and
  `document_shape_invalid`); the runner compares (id, reason) pairs, and
  renaming any of the ten graded codes fails the fixtures naming it
  (`.ufo/waves/round-30/c1_strict_checks.py`, check S2; wave-2
  `CriticQualityCriteria` observed exactly those fixtures failing for all 13
  named codes, which S2 itself does not assert). No committed command counts
  the 25 codes, so a new uncovered code would make this count stale silently. The other 12 codes
  stay uncovered and are listed in `SKILL.md`, "Citing-set reason-code
  registry — round 30".

## Round-31 criteria (from the round-30 spot-check)

Grounded in `corpus/lessons/round-30-verifier-spotcheck.md` "Routed defects"
and `corpus/lessons/round-31.md` "Mistakes".

- **A containment repair is backed by one hostile probe per shape it
  claims.** A commit that says a runner or gate refuses hostile input names
  the shapes, and each shape has a committed spec run by a selftest that also
  checks for harm (code ran, a repository outside the case changed, the run
  hung). Reviewer check: run `scripts/citing_set_hostile_selftest.py` with
  `--runner` set to the pre-repair runner; it must exit 1. Source: routed
  defect 1 (lines 250-262).
- **A declared closure command is run once before it is declared, and names
  files, not a directory that will grow.** Reviewer check: run the command
  as written with both revisions equal to the declaration commit (exit 0
  expected), and once on a sandbox commit that changes a named file (exit 1
  expected); `.ufo/waves/round-31/verification/closure-command-check.txt`.
  Source: routed defect 6 (lines 283-286).
- **Every seat's end state is recorded.** Each wave commits a
  `seat-status.json` naming every seat as returned, dead at spawn, refused or
  cancelled, and a report written by a seat that stopped early is listed as
  partial. Reviewer check: the count of returned seats equals the number of
  reports not listed as partial. Source: routed defect 5 (lines 280-282);
  round-30 list in `.ufo/waves/round-30/w2/partial-reports.json`.
- **A qualifier a source does not state is marked.** A word such as
  "lowercase" or "only" that narrows a quoted fact is either in the quote or
  marked `[INFERENCE]`. Reviewer check: for each such word in a new entry,
  search the retained text. Source: routed defect 3 (lines 271-276).

## Round-31 wave-2 corrections to the round-31 criteria

Grounded in `.ufo/waves/round-31/a2-w2/CriticQualityCriteria.md` (F2–F5) and
`CriticSymlinkCases.md`. They narrow or replace the reviewer checks above; the
criteria themselves stand.

- **Containment probes cover each name shape the claim covers.** The first
  criterion passed while a dot-named symlinked case was still skipped,
  because spec P5 used one name shape. Reviewer check, added: for every
  refusal the docs state without a name restriction, the spec has at least
  one case per name class the runner filters on (here: plain and dot-named);
  the pre-repair runner must fail that spec (`verification/a2-fixes/hostile-selftest-fde133a-runner.json`: P5 fails on `.h5b`).
- **Closure command check, replaced (F2).** Step 1 (both revisions equal) can
  never fail. Run instead: (a) no path argument names a directory
  (`git ls-tree <declaration commit> -- <path>` shows a blob for each); (b) a
  sandbox commit that adds an unrelated file beside the named paths, exit 0
  expected; (c) a sandbox commit that changes a named file, exit 1 expected.
  The round-30 directory command fails (a) and (b).
- **Seat end states, set comparison (F3).** The status set is: returned,
  returned-after-safety-filter, dead at spawn, refused, cancelled. A partial
  report is either listed as partial or starts with `PARTIAL:`. Reviewer
  check: the set of seats with a non-partial report equals the set of
  returned seats (either returned status), compared by name, not by count.
  Only dispatched waves need a `seat-status.json`.
- **Qualifier search within the cited sentence (F4).** Search each word from
  the list only, always, never, every, all, must, each, lowercase in the
  sentence that holds the cited quote, not in the whole page; a claim made
  over a list of keys is checked key by key. A mark `[INFERENCE]` placed on a
  fact the retained text states is also a defect (round-31 line 22, PORT).

## Round-32 criteria

- **Stated times are read, not estimated.** A declaration that states the
  time it was declared must state a time no later than its declaring commit
  (`git show -s --format=%cI <commit>`). Check:
  `python3 -B .ufo/waves/round-32/declared_time_check.py --rev <commit> --section "<heading>"`
  (exit 1 on a violation; it reports one on the round-32 declaration at
  `5b32cc7`, which said 18:58Z for a commit made at 18:54:19Z).
- **A defence-in-depth guard is pinned by the layer that refuses first.** When
  removing one guard leaves a hostile shape refused by a later layer, a probe
  that only asks "was it refused" cannot kill that mutant; the spec names the
  refusing layer's reason (`reason_contains`). Reviewer check: run the round's
  mutation probe on the guard (`.ufo/waves/round-32/c1_m3_probe.py`); killed
  must be 1 with `guard_ok` true. Limit: this reads the runner's reported
  reason text for that case.
- Limits of the round-32 time check (wave-1 seat `ScribeMistakeDraft`,
  sandbox repos): it reads only the wording `Declared at HH:MMZ`, places that
  time on the commit's UTC date (a stamp across midnight is misjudged), and
  exits 2 on other wording. A reviewer applying the criterion reads the
  stated time by hand when the check exits 2 or the commit is within minutes
  of midnight UTC.

## Round-33 criteria

- **A hostile spec that pins which layer refused names a structured code, not
  message text.** When removing one guard leaves the hostile shape refused by
  a later layer, the spec shows the intended guard refused first through a
  `reason_code` key that the hostile selftest compares for equality with the
  runner's reported per-case `code`. `reason_contains` may stay as a secondary
  assertion, never as the only pin. Reject: a case pinned only by
  `reason_contains`; a code the runner never emits; a key the loader tolerates
  and the comparison ignores. Grounding: round-32 routed item 2
  (`corpus/lessons/round-32-verifier-spotcheck.md`, "Routed defects" 2); at
  `bc6c4a8` a reworded load-time message fails P6 on a correct runner. Check:
  `python3 -B .ufo/waves/round-33/criteria/refusal_code_check.py --root . --rev <commit>`
  (exit 1, 1 of 5 at `bc6c4a8`; exit 0, 5 of 5 at `e490381`; receipts
  `.ufo/waves/round-33/verification/criterion-refusal-code-at-*.txt`). Limit:
  structural over committed bytes; behaviour is the round's C1 probe and its
  strict supplement (`.ufo/waves/round-33/c1_code_probe.py`,
  `c1_strict_supplement.py`). This supersedes the `reason_contains` mechanism
  and the `c1_m3_probe.py` reviewer check in the round-32 bullet above; that
  probe does not gate a kill on `guard_ok` and raises on a timeout (round-32
  routed item 3), so it is not reused.
- **A repair counter pins the identity it claims, and a hollow control scores
  below its after-value.** A counting command that grades a retention,
  registration or citation repair names, per condition, the identity it
  checks (registry row id, retained path, Git mode, citing section). One
  hollow commit fakes the repair at every condition (same bytes at an
  unrelated path, a fabricated row id, an unrelated mention of it), and the
  counter must score it strictly below the declared after-value. Check:
  `python3 -B .ufo/waves/round-33/criteria/counter_control_check.py --counter <counter> --repo <repo> --before <rev> --after <rev> --hollow <rev>`
  (exit 1 when the hollow commit reaches the after-value). Round-32 evidence:
  the frozen round-32 C2 counter scores the landed repair `e9283ec` and the
  hollow commit `6ffa03e` (retained as
  `.ufo/waves/round-33/verification/hollow-r32-c2-6ffa03e.bundle`) both 3,
  exit 1 (`verification/criterion-counter-control-r32-c2.txt`). Limit: one
  hollow commit tests discrimination for the shapes it fakes, not the truth
  of the retained bytes.

## Round-34 criteria

- **A cited artifact resolves from committed lane bytes, not a seat's sandbox.** A cited
  counterexample commit, patch, retained source or receipt is committed under the lane; the
  citing line names a lane-relative path that `git cat-file -e <revision>:<path>` resolves at
  the revision it is added or corrected in. A `/fast/scratch/...` or `/tmp/...` path stands
  beside that path as provenance, never as the only pointer; a preserved earlier line stays
  byte-identical and the lane path arrives as an appended correction. Reject: a pointer that
  resolves only in a seat's sandbox; a retained file no committed line cites; a citing line
  whose retained path is absent at the citing revision. Grounding: routed item 2
  (`corpus/lessons/round-33-verifier-spotcheck.md:192-196`), where `489714be` and the
  option-table patch were cited from `/fast/scratch/hyaku/kake-r33/w1/...` only; round 34 now
  retains them at `.ufo/waves/round-34/retained/` as
  `r33-c1-counterexample-489714be.bundle` (`a2fe31b2`, sha256 `6ff6c403…77c00`, head
  `489714be413c…` on tag `r33-c1-counterexample`), `r33-option-table-dedup-patch.diff`
  (`28fd9adf…47d6e`) and `r33-option-table-alt-patch.diff` (`daeaa738…0ce6e`), beside the
  pinned ds4cc bytes under `.ufo/waves/round-34/sources/`. Check: per cited sandbox path,
  `git cat-file -e <revision>:<retained path>` for each retained file the section names;
  able to fail at `d08d8de` (exit 128) and pass at `a2fe31b2` (exit 0). Limit: retention
  makes bytes reachable, not proved; whether the bundled commit or patch says what the
  citing line claims stays with the round's probes and the non-author read.
- **A round's `## Gate` records at least one screened reject with its reason.** Every
  candidate the Gate screens carries a decision, and each reject states the located fact
  that failed it (the quote or byte that did not match), not a status word or the verdict
  again. Reject: a Gate whose decisions are all admits; a reject with no reason; a screened
  rejection recorded only in a wave report. Grounding: routed item 3
  (`corpus/lessons/round-33-verifier-spotcheck.md:197-198`); the round-33 Gate
  (`corpus/lessons/round-33.md:25-37`) holds two `admit` rows and no `reject` word
  (`grep -c reject` there: 0), so the LEARNING admit+reject sample used a code patch; round
  34 screened S071 and S072 as rejection candidates (`SCORECARD.md:1202-1203`). Check:
  `python3 -B .ufo/waves/round-34/criteria/gate_reject_check.py --repo . --rev <commit> --lesson <path>`
  (its docstring states the exit contract; this criterion requires it to fail a Gate with no
  reject and a reject with no located reason). Receipts: exit 1 on
  `corpus/lessons/round-33.md` at `93359ff`
  (`.ufo/waves/round-34/verification/criterion-gate-reject-r33-at-93359ff.txt`), exit 0 on
  `corpus/lessons/round-29.md` (`criterion-gate-reject-r29-at-a2fe31b.txt`). Limit: structural over the
  lesson text at `--rev`; a present reason is not a true reason.
- **Every run a report cites ships a committed receipt.** A report line stating that a
  command ran at a revision names the receipt committed in that round whose `revision` field
  equals the stated revision; a run without one is written as not run, and "run, not
  committed" is not a result. Reject: a tally with no receipt; a glob (`c1-after-*.json`)
  offered for a named revision; a receipt naming a different commit than the citing line.
  Grounding: routed item 4 (`corpus/lessons/round-33-verifier-spotcheck.md:199-201`) and its
  quoted line `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kake.md:62`
  ("`93359ff`: 4/4 (run, not committed)"), harmless only because `git diff 3abfc44 93359ff
  --stat -- scripts/` is empty. It extends the round-30 bullet at `corpus/QUALITY.md:450-460`
  to every run a report cites; that witness reads the working tree and stays for claim
  revisions. Check:
  `python3 -B .ufo/waves/round-34/criteria/receipt_presence_check.py --report <md> --repo . --rev <commit> --round <N>`
  (report read from disk, possibly the fleet path; receipts resolved in `--repo` at `--rev`).
  Receipts: exit 1 naming `93359ff` on the round-33 report
  (`.ufo/waves/round-34/verification/criterion-receipt-presence-r33-report.txt`). Limit: presence and revision agreement, not replay or tally truth.
- **A counter scores a lookup-table control below its full score, and this is
  run before the counter is frozen.** A control commit that does none of the claimed work
  and only replays what the counter makes visible (for a matrix counter, a tool that reads
  the case directory name and prints the published expected output; for a source counter,
  rows and an entry copied from a published receipt) must score below the declared
  after-value; the declaring round runs that control before the counter is committed.
  Reject: a counter that materializes cases under directory names equal to case ids next to
  a published matrix; a counter whose before-receipt prints the full recount the after-state
  must state; a declaration that freezes a counter with no hollow or lookup control run.
  Grounding: round-34 mistake row 4 (`corpus/lessons/round-34.md`); wave-1
  `CriticDeclarationFit` built `dcef39b5` (C1 lookup tool, 28/28) and `0cce15f0` (C2
  transcription, 5/5), both retained in `.ufo/waves/round-34/retained/`. Check:
  `python3 -B .ufo/waves/round-34/criteria/lookup_control_check.py --counter <counter> --repo <repo> --control <rev>`
  (exit 1 on the frozen round-34 C1 counter with control `dcef39b5`:
  `.ufo/waves/round-34/verification/criterion-lookup-control-c1-dcef39b.txt`). Limit: one
  control tests the leak it exploits; a counter that hides case names can still be
  satisfied by other transcription paths, so the non-author read of the landed work stays
  part of admission.

## Round-34 wave-2 corrections to the round-34 criteria

- (b): "its docstring states the exit contract" is wrong; the exits are in
  the code (0 a reasoned reject found, 1 none, 2 bad input). At `76fac3b` the
  check also skips fenced lines and requires a reason of at least four words
  beyond decision, tier, kind and status tokens, so "reject, tier C, kind
  docs, status rejected" now fails (wave-2 `ReviewQualityCriteria34` B1,
  `MutGateRejectCheck`; `.ufo/waves/round-34/verification/criterion-gate-reject-fixtures-at-76fac3b.txt`).
  A present reason is still not shown true.
- (c): text receipts count only when the file name carries the hash (wave-2
  `MutReceiptPresenceCheck`); the check prefix-matches the JSON `revision`
  rather than requiring equality.
- (d): an honest tool also reaches the full score and exits 1; the check
  only means something for a control whose diff shows it does none of the
  work (wave-2 `ReviewLookupControlCheck`).

## Round-35 criteria

Round 34 was rejected because a do-nothing control met each declared counter
(`corpus/lessons/round-34-verifier-spotcheck.md`, routed defect 1). Round 35
answers with sealed test inputs and controls scored before any build. These
four criteria carry that design into the bar. Each names a check. The three new
scripts landed at `fd0d53b2` under `.ufo/waves/round-35/criteria/`, and their
receipts are under `.ufo/waves/round-35/verification/criterion-*.txt`. Drafted by
wave-1 `ScribeQualityCriteria`; the L1 integrated it.

- **A declared target is out of reach of the cheapest do-nothing controls, scored
  with the frozen counter and committed before the build.** The declaring round names its
  counter by sha256, and before the first build commit it scores at least three controls with
  that same counter: the base tree or a no-op, the previous round's retained hollow control,
  and a constant tool that prints a clean result and exits 0. Each control's receipt records a
  value below the declared target. Where a lookup or transcription control could reach the
  target, the round seals its test inputs before the declaration, keeps them outside the lane
  until a reveal commit, pins them by sha256 inside the counter, and the counter refuses
  (exit 2) to measure a revision that holds a key file. Reject: a target a retained or trivial
  control reaches; controls scored after the build; a control receipt whose counter sha256
  differs from the declaration's; a target stated only in a report or narrowed after landing.
  Grounding: round-34 routed defect 1 (`dcef39b5` C1 28/28 and `0cce15f0` C2 5/5 on the frozen
  round-34 counters). Round 35: sealed keys `/fast/scratch/hyaku/kake-r35/sealed/` (mode 0700,
  outside the lane), declaration `81d9fd74`, controls `318561ef`, counter sha256
  `c4d58daea09d27a15f7792aae320cd56ac44dc1a6911307d6320f0a2c04349ef`; receipts
  `.ufo/waves/round-35/verification/control-*.json` with matching `.exit`; control commits
  retained as `.ufo/waves/round-35/retained/r35-control-*.bundle` (prerequisite `81d9fd74`).
  Check (after fetching the bundles into the clone):
  ```
  git merge-base --is-ancestor 81d9fd74f1460ba8cff007fc42f8fb8265aa2d4d 318561efa67206699fdaf259ffb86e39f2d916a8
  git merge-base --is-ancestor 318561efa67206699fdaf259ffb86e39f2d916a8 <first build commit>
  python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision 5f767534f4cacb8d041f51dfb1854c2a14395389 --key-revision <reveal commit>
  python3 -B .ufo/waves/round-35/sealed_count.py c2 --root . --revision ae9fb36146474fbac513930e61e116de6ac96904 --key-revision <reveal commit>
  ```
  Observed from the committed receipts: C1 constant clean `passed` 7 of 24 against target 22
  (exit 1), C1 lookup 7, C1 base and declaration 14; C2 junk 0 of 12, keyword 3, transcript 8
  against target 9, transcript `copiedShare` 0.9951. No control reaches its target. Counter
  version 2 (`bd14096a`, before any build was measured) rescored every control
  (`verification/control-v2-*.json`). Under it the critic's hidden-padding and zero-width
  transcriptions and a mechanically reworded transcription also stay below target (8, 8 and 6
  probes). Limit: it
  scores only the controls the round names, so a cheaper control it did not build can still
  reach the target; the seal refuses revisions that contain the key path, but a control can
  read a key by path, or reconstruct expected findings from the public contract (the C1 cases
  are 24 short synthetic pages), and still score; ancestry is commit order, not wall-clock
  order, so a rebase can place controls before a build that was written first; a frozen
  counter can still be wrong, and the non-author read stays part of admission.

- **No pre-build receipt publishes a value the build is later measured by.** A receipt
  committed before the build does not carry the numbers that a committed measured-result line
  will state, so copying the receipt cannot satisfy the condition. Thresholds (`target`,
  `probeTarget`) and control scores are the receipt's own content and are not measured values.
  Reject: a pre-build receipt with a `derived` census or per-condition counts that the entry
  later restates; a measurement line assembled from receipt values; a receipt named for the
  measured revision but committed after the build. Grounding: round-34 routed defect 4.
  `.ufo/waves/round-34/verification/c2-at-d08d8de.json` (file added at `a2fe31b`; its
  `revision` field is `d08d8de`) carries `census.derived`
  `pages=102 og:title=87 og:type=87 og:image=1 og:url=87 all-four=1 og-url-equals-canonical=87`
  before any entry existed, and the entry at `ce72dd1b` restates them at
  `corpus/knowledge/link-preview-metadata.md:128`. Check:
  ```
  python3 -B .ufo/waves/round-35/criteria/prebuild_leak_check.py --repo . \
    --receipt-rev a2fe31b --receipt .ufo/waves/round-34/verification/c2-at-d08d8de.json \
    --entry-rev ce72dd1b --entry corpus/knowledge/link-preview-metadata.md \
    --line-regex '^ds4cc-7fc6aa2f-og-census:'
  ```
  Exit 1 with the matched values on that pair; exit 0 with `c1-at-d08d8de.json` as the
  receipt, because that receipt holds none of the line's numbers (`passed` 0 of 28). The
  check reads the receipt from the revision named by `--receipt-rev`; `d08d8de` does not hold
  the file (exit 2), so the file-holding revision is the one that resolves. Limit: literal
  key=value matching only; prose, arrays, `perCase`/`perProbe` booleans, rounded or
  renormalised numbers, or the same quantity in another unit leak without matching; it reads
  one entry line, so the same numbers stated elsewhere in the entry or in another committed
  file are invisible; a receipt may legitimately carry the target threshold, so running the
  check on a threshold line gives a false fail. Run it on the measured-result line.

- **A retained control is described by quoting its own bytes.** A paragraph or table row that
  names a retained control (bundle and revision) quotes at least one whole non-blank line of
  the control file, backticked and at least 20 characters, and names that line's number. A
  correction is appended; the earlier wrong sentence survives byte-identically. Reject: a
  description of what the control "keys on" or "does" with no quoted line; a quote from a
  different control or a line that does not support the stated mechanism; a correction that
  rewrites the earlier line instead of appending. Grounding: round-34 routed defect 2.
  `corpus/lessons/round-34.md:68` says `dcef39b5` "keys on the case directory name the C1
  counter chooses"; its bytes at `scripts/link_preview_audit.py:5-15` hash argv plus every
  relative path and file content under the cwd (`:8`
  `files[p] = open(p, encoding="utf-8", errors="surrogateescape").read()`; `:12`
  `h.update(rel.encode() + b"\0" + files[rel].encode("utf-8", "surrogateescape") + b"\0")`),
  and a one-comment HTML perturbation drops it to 7 of 28. Check:
  ```
  python3 -B .ufo/waves/round-35/criteria/control_description_check.py --repo . \
    --bundle .ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle \
    --revision dcef39b5f4e8373970eb74858d2c6175524cdfd0 \
    --path scripts/link_preview_audit.py \
    --doc corpus/lessons/round-34.md --doc-rev fd0d53b2 --anchor dcef39b5
  ```
  Exit 1 on that row (no quoted line); exit 0 on an appended paragraph that quotes line 8 and
  names it. Limit: one quoted line shows bytes at that line, not that the quotation is
  representative or that the described mechanism causes the control's score; a long irrelevant
  line (an import, a print) can satisfy it; it reads only the paragraph or row containing the
  anchor, so a quoted line elsewhere does not count and an unquoted overclaim beside a quoted
  line survives; it does not check append-only, which needs a stripped diff against the base
  file.

- **Every lane tool with an exit contract has a gate registry row.** Each `scripts/*.py` that
  defines `EXIT_` constants or documents exit codes 0/1/2/64 has a row in the 8-column gate
  registry table of `SKILL.md` (`Name | Kind | Entry command | Verdict map | Self-test |
  Pinned values / frozen proof | Write scope | Owner`; header at `SKILL.md:409`, precedents
  `canonical-audit` at `:411` and `base-path-audit` at `:725`), with the row's name the tool's
  kebab name and its exit map matching the code. Selftests are out of scope. Reject: a tool
  with exits and a selftest but no row; a row that exists only in a task table; a row whose
  exit map omits an exit the code returns. Grounding: round-34 routed defect 3;
  `scripts/link_preview_audit.py` documents `Exit codes: 0 clean, 1 failed-policy,
  2 could-not-evaluate, 64 usage` (`:43`, constants `:55-58`) and has
  `scripts/link_preview_selftest.py`, yet no registry row exists at `318561ef`. Check:
  ```
  python3 -B .ufo/waves/round-35/criteria/registry_row_check.py --repo . --rev 318561ef
  ```
  Exit 1 listing `scripts/link_preview_audit.py`; exit 0 at the commit that lands the
  round-35 row. Every other tool the check flags is a finding, not a waiver. Limit: presence
  and name matching only; a row with stale exits, a wrong verdict map or an unimplemented
  command passes, and a tool whose exit codes are implicit (`sys.exit(1)` with no constant or
  docstring line) is not discovered. It also cannot tell a gate registry row from any markdown
  table row that merely names the command unless it restricts itself to the registry table's
  exact `Name` and `Entry command` columns: `SKILL.md:1003` already names
  `python3 -B scripts/link_preview_audit.py --manifest ...` in the round-34 task table
  (`Situation | What to check | Evidence command | Grounding phrase`), so a path-in-any-cell
  match exits 0 at `318561ef` and defeats its own acceptance. The implementing seat states it
  matches only those two cells of a table with those headers; that restriction is the
  criterion's requirement, and dropping it makes the check pass a file with no registry row.

- **A knowledge counter refuses an inverted-facts entry and an unsourced entry (criterion (e),
  added after wave 2).** Before a sourced knowledge claim is built, its frozen counter must give
  `met` false on two retained controls. The first states the probed topics with the facts
  inverted. The second is written from the public topic list without opening any retained
  source text. Probes should rest on facts found only in the round's opened texts (for example
  a registration date or a served field value), not on facts any reader could supply from
  memory. Reject: a counter that cannot tell a negated fact from the fact, or a prior-knowledge
  entry from a sourced one. Grounding: round-35 C2 — `retained/r35-w2-c2-inverted-facts.bundle`
  (`dc8e1adf`, met true, 12 of 12) and `r35-w2-c2-sufficiency.bundle` (`0b7779dc`, met true,
  11 of 12). Check:
  ```
  python3 -B .ufo/waves/round-35/criteria/knowledge_control_check.py --root . \
    --counter .ufo/waves/round-35/sealed_count.py --claim c2 --key-revision 4c6be2bd \
    --control dc8e1adf --control 0b7779dc
  ```
  Exit 1 on the round-35 counter (`verification/criterion-knowledge-controls-r35-c2.txt`);
  exit 0 on the pre-build controls `04848219`, `e5263d41` and `c2e38e5d`
  (`criterion-knowledge-controls-r35-prebuild.txt`). Limit: it checks only the controls it is
  given. A truthful entry built from memory still meets a counter that passes this check unless
  the probes rest on facts only the opened texts hold.

## Round-35 wave-2 corrections to the round-35 criteria

Limits found by wave-2 `ReviewCriteriaChecks` and `MutCriteriaChecks` (reports in
`.ufo/waves/round-35/w2/`); the criteria stay as landed.
- (b) `prebuild_leak_check.py` fails only when every value of the line appears as a JSON value. A
  receipt that publishes six of seven values, or holds them as object keys, passes.
- (c) `control_description_check.py` checks form, not support. A quoted boilerplate line such as
  `import hashlib, json, os, sys` passes beside a false mechanism.
- (d) `registry_row_check.py` accepts any table with Name and Entry command columns anywhere in
  `SKILL.md`. It does not find a tool whose exit codes are not declared by name or in the
  docstring.
- (a) The C1 target of 22 of 24 let a whole contract bullet be skipped: (c) moves only two sealed
  cases (`w2/ExecPartialRepairs.md`). A sealed target should be set so that no declared bullet
  can be skipped, and each bullet needs at least one more sealed case than the slack.

## Round-36 criteria

Round 35's routed defects 1–4 set these bars. Apply (c) to the frozen C1 counter and its declared target of 25/28; retain each check's inputs and output under `.ufo/waves/round-36/verification/`.

- **(a) A sourced-learning counter distinguishes true, sourced claims from cheap controls.** It refuses an inverted-facts entry and an entry written without opening retained source text; a bare source-id line alone does not satisfy a `cites` condition. Reject: either the inverted or unsourced control meets the target, or a bare-id-only citation earns a cite. Grounding: round-35 routed defect 1 (`corpus/lessons/round-35-verifier-spotcheck.md:185-189`); controls `dc8e1adf` and `0b7779dc` met the old counter (`.ufo/waves/round-35/verification/criterion-knowledge-controls-r35-c2.txt`). Check: `.ufo/waves/round-35/criteria/knowledge_control_check.py`, run against separately identified inverted-facts, unsourced, and bare-id-only controls. It is shown able to fail by its recorded exit 1 on the round-35 controls; acceptance of any of those controls, including a bare-id-only control run alone, must likewise produce its failing result. The candidate counter must refuse all three. Limit: the checker only tests the controls supplied to it.

- **(b) A counter version bump preserves the declared predicate.** A version bump changes no target, threshold, cap, pin, or predicate unless a scored control forced that exact change and the round's note names the control, its score, and the reason. Reject: an unexplained change in any of those values, or a post-measurement change not remeasured against the declared bound. Grounding: round-35 routed defect 2; v1's 1500-whitespace-word cap became a 2200-overlap-word cap in v2 without any control forcing it (`corpus/lessons/round-35-verifier-spotcheck.md:190-193`). Check: `.ufo/waves/round-36/criteria/version_bump_check.py`. It is shown able to fail on that round-35 v1→v2 change (nonzero/fail); it must also fail a negative fixture that changes a pinned value without a named scored control, and pass only a change whose forcing control and score are documented.

- **(c) Every C1 contract bullet is necessary to reach the frozen target.** For each contract bullet (a)–(g), the corresponding one-bullet ablation scores below 25/28. Reject: any ablation reaches or exceeds 25/28, including an omitted bullet whose behavior is not exercised by the sealed cases. Grounding: round-35 routed defect 3, where 22/24 met target with bullet (c) skipped and the sealed set lacked a nested `<template>`, `<svg>`, or `<math>` case (`corpus/lessons/round-35-verifier-spotcheck.md:194-196`). Check: `.ufo/waves/round-36/criteria/ablation_floor_check.py`; it is shown able to fail with a negative fixture in which any one ablation is at or above 25/28 (including the prior 22/24-at-22 slack pattern), while the round-36 receipt must show all seven ablations below 25/28.

- **(d) Every control is built from a key-free tree.** For each control, preserve the source-tree identity and its listing; that listing must contain no sealed-key path, and the control must be built from that listed tree. Reject: a missing listing or any control tree whose listing contains a key path. Grounding: round-35 routed defect 4; the post-reveal control clone `0b7779dc` held `sealed/c2-probes.json` (`corpus/lessons/round-35-verifier-spotcheck.md:197-198`). Check: `.ufo/waves/round-36/criteria/control_tree_check.py`; it is shown able to fail on a negative listing containing `sealed/c2-probes.json` (as in `0b7779dc`), and must pass only when every control's recorded listing is key-free.

- **(e) Every full commit hash a declaration writes resolves.** Reject: a 40-hex hash in a
  SCORECARD declaration section that names no commit. Grounding: the round-36 declaration's
  "Base" line (`3555f63f`) carried a hash that names no object (lesson round-36 mistake row 1).
  Check: `.ufo/waves/round-36/criteria/hash_resolve_check.py`, exit 1 on that section
  (`verification/criterion-hash-resolve-r36-decl-at-3555f63f.txt`), exit 0 on the round-35
  declaration (`criterion-hash-resolve-r35-decl-at-cd321279.txt`).
- **(f) Each sealed bullet carries both answer polarities.** For every contract bullet whose
  rules read a body, at least one check per case expects a finding that a skipped rule would
  turn into a hold, and the checks do not share one fixed label (contentType, file name) that a
  tool could key on. Reject: a bullet whose checks all expect the same polarity, or a shortcut
  control that passes a bullet's cases without opening a body. Grounding: round-36 key version 1,
  where `CtlShortcut` passed every (e) and (f) case without opening a body
  (`verification/v2/control-CtlShortcut.json`, 17 of 28; lesson round-36 mistake row 2). Check:
  the shortcut ablations `verification/ablations/ablation-s_ctkey.json` (13) and
  `ablation-s_unsure.json` (24) against `criteria/ablation_floor_check.py`, and the control-wave
  rescore (`verification/control-CtlShortcut.json`, 9).

## Round-37 criteria

Apply these bars to the round-37 evidence without changing the frozen C1 predicate (`passed >= 25 of 28`). C1 is the round's only claim; withdrawn C2 fixture work is non-claim evidence. A planned check or an old incident is not an executed red-before receipt.

- **(a) A wave seat writes deliverables only in its sandbox; the L1 checks lane state after each wave.** The L1 copies reviewed deliverables into the lane and checks `jj-lane.sh state` for stray paths after every wave before integration. Reject: a seat writes a deliverable into the lane outside its report path, or an unexpected lane path is integrated without review. Grounding: round-36 routed defect 2 (`corpus/lessons/round-36-verifier-spotcheck.md:155-157`); two executors wrote under the lane's `round-36/criteria/` despite a report-only allowance (`corpus/lessons/round-36.md:80`). Check: L1's post-wave `jj-lane.sh state` review against the allowed report paths. Red-before receipt: **no check yet**; the round-36 writes are the incident, not a demonstrated failing state check.

- **(b) A key repair keeps the original-key measurement as the rule of record.** If the sealed key is repaired after any score, retain and use the originally declared key/counter measurement to decide the claim; any repaired-key result is separately labeled supplemental and cannot replace that result. Reject: the claim is decided only by a post-repair key or its changed case set. Grounding: round-36 routed defect 4 (`corpus/lessons/round-36-verifier-spotcheck.md:161-163`); round-36 key v2 followed control scores and loosened the casefold class (`corpus/lessons/round-36.md:61-65`). Check: retain the pre-repair key/counter identity and score the build under that original pair; show a separate receipt for any repaired pair. Red-before receipt: no policy-check receipt yet. The historical original-key measurement `verification/c1-counter-v1-keyv1-at-4d5b3d55.json` is 28/28, but is not a red-before failure of this criterion (`corpus/lessons/round-36-verifier-spotcheck.md:71-75`).

- **(c) Coverage wording names the exact ablations and a mutation pass, and claims no more than those measurements.** State which listed ablations were scored and their observed range/maximum, then report the reference mutation pass as a separate result; do not generalize either into proof that every way of skipping a contract rule is caught. Reject: an unqualified claim that meeting 25/28 certifies every contract rule, or a sentence that omits the listed ablations or the mutation pass. Grounding: round-36 routed defect 3 (`corpus/lessons/round-36-verifier-spotcheck.md:158-160`); 9/32 tool mutants and 5/6 new reference mutants survived in round 36 (`corpus/lessons/round-36.md:134-143`). Check: compare the coverage sentence with every named ablation receipt and the pre-build mutation-pass table. Round-37 design reports 34 listed ablations at most 24/28 (`SCORECARD.md:1778-1784`) and a 42-mutant pass with 28 meeting the predicate (`.ufo/waves/round-37/ctl/MutRefPass.md:3-4`; per-mutant table at `:11-52`); the declaration limits the claim to those listed rules (`SCORECARD.md:1924-1932`). Red-before receipt: **no wording-check receipt yet**; these are supporting measurements, not a check shown red on an overclaim.

- **(d) Every cited commit hash resolves in lane history, or the citation names the bundle that contains it.** Do not present a bundle-only hash as a lane commit. Reject: an unresolved citation with no exact bundle path, or a citation claiming lane-history provenance when it exists only in a bundle. Grounding: round-36 routed defect 1 (`corpus/lessons/round-36-verifier-spotcheck.md:153-154`); `bf9b2089` was absent from lane objects and present only in `retained/r36-l1-postfix-remeasure.bundle` (`corpus/lessons/round-36-verifier-spotcheck.md:22-23`). Check: test commit citations with `git cat-file -e <hash>^{commit}`; if unresolved, verify the named bundle with `git bundle list-heads <bundle>` and cite its path. The existing `.ufo/waves/round-36/criteria/hash_resolve_check.py` red-before receipt caught a bad full hash in the round-36 declaration (`.ufo/waves/round-36/verification/criterion-hash-resolve-r36-decl-at-3555f63f.txt`), but it does not enforce bundle fallback or every short hash citation. Red-before receipt for that broader rule: **no check yet**.

- **(e) Body-reading case sets exercise both answer polarities, with the round-37 per-case promise preserved.** For every body-reading bullet, its cases must include an outcome that correctly produces a finding and one that correctly produces no finding; no single fixed id or file-name label may substitute for reading the body. Round 37 additionally declares at least one finding-producing and one hold-producing check in every case. Reject: a bullet whose cases exercise only one polarity, or a shortcut can pass by keying on fixed labels. Grounding: round-36 routed defect 7 (`corpus/lessons/round-36-verifier-spotcheck.md:169-170`); key v1 let `CtlShortcut` pass every (e)/(f) case (17/28), while the 17-to-9 rescore was not a criterion-check receipt (`corpus/lessons/round-36.md:79`; verifier spot-check `:169-170`). Check: a polarity check over the sealed key; round-37's repair assignment specifies red on round-36 key v1 and green on v2 (`.ufo/waves/round-37/make_w1_spec.py:82`). The requested check tests per-bullet presence; the stronger round-37 per-case promise and label independence need explicit evidence too. Red-before receipt: **no check receipt yet**.

- **(f) A control-tree check proves the control was built from the listed, key-free tree.** Bind the tree identity/listing to the control artifact and reject any key/sealed-case path anywhere in the tree; a root listing must not pass when the source tree contains a key. Reject: a detached listing or a listing that omits a sealed key in the control's source tree. Grounding: round-36 routed defect 7 (`corpus/lessons/round-36-verifier-spotcheck.md:170-171`); the old check falsely passed a root listing over a tree holding a key (`.ufo/waves/round-36/w2/ReviewCriteriaChecks.md:40-49`). Check: `control_tree_check.py` v2, as specified for round 37, must fail on both the round-35 key-path listing and a constructed root listing over a key-holding tree, and pass a key-free control listing (`.ufo/waves/round-37/make_w1_spec.py:81-83`). Red-before receipt: **no corrected-check receipt yet**; the cited review is the demonstrated false pass of the old check, not a red result from v2.

- **(g) A bare source id alone does not satisfy a knowledge-entry `cites` condition.** A citation must accompany claim text; the source-id-only line is not evidence that the entry uses the source. Reject: a bare-id-only knowledge entry meeting the cite condition. Grounding: round-36 routed defect 7 (`corpus/lessons/round-36-verifier-spotcheck.md:169-171`); round-36 criterion (a) stated this rule but lacked the negative receipt. Check: `bare_id_check.py` on a constructed source-id-only entry, with an ordinary claim-bearing citation as a positive control (`.ufo/waves/round-37/make_w1_spec.py:82`). Red-before receipt: **no check/negative receipt yet**.

Receipts landed this round after the drafts above (wave-1 `ExecCriteriaRepairs`, run by the seat
in its sandbox; receipts copied to `.ufo/waves/round-37/criteria/receipts/`): (e)
`polarity_check.py` exits 1 on round-36 key v1 (bullets e and f have no body-decided finding)
and 0 on key v2; (f) `control_tree_check.py` v2 exits 1 on the round-35 key-path listing and on
a constructed root listing over a key-holding tree (the round-36 v1 exits 0 on the same report),
0 on the round-37 and round-36 control reports; (g) `bare_id_check.py` exits 1 on a constructed
bare-id entry and 0 on the knowledge directory. These replace the "no check yet" notes of (e),
(f) and (g); (a) to (d) stay rules checked by reading.

- **(h) A counter over fixture data is scored against a recorded-oracle fixture set before it is
  declared.** A fixture set whose expectations are recorded from an implementation on random
  inputs (no contract reading) must not meet it; if it does, the counter does not measure
  contract-grounded fixtures. Grounding: round-37 C2 (`SCORECARD.md` "Round 37 — control call";
  `ctl/CtlC2FixtureSets.md`: snapshot set 32 of 32). Check: the snapshot control receipt
  `retained/controls/c2/c2-snapshot.json` (met true) is the red receipt of the withdrawn C2.
- **(i) Control seats never share a parent directory with the sealed key.** Key-blindness must
  not rest on instructions alone. Grounding: round-37 wave-1 `ReviewRoutedDisposition` G2 (the
  control sandboxes sat under `/fast/scratch/hyaku/kake-r37/`, beside `private/`). Check: none
  yet; the wave-1 sandboxes moved to `/fast/scratch/hyaku/kake-r37w1/`.
- **(j) The consequence of a control meeting a predicate is applied as declared.** If a control
  meets the predicate before data, the counter is redesigned (with the original kept as the rule
  of record) or the claim is dropped or declared exploratory; a disposition that reclassifies the
  control is not an option unless the declaration named that class beforehand. Grounding: round-37
  shortcut follow-up (`SCORECARD.md` `ccc3b2b9` section; `w2/ReviewTimeline.md`). Check: none yet.

## Round-38 criteria

Grounding: `corpus/lessons/round-37-verifier-spotcheck.md` (round-37 C1 not admitted; routed
defects 1–6) and `corpus/lessons/round-38.md` `## Mistakes`. Drafted by wave-1
`ScribeQualityCriteria`; checks landed by `ExecQualityJCheck`, `ScribeMistakeMine` and
`ExecReceiptPin` (`.ufo/waves/round-38/criteria/`).

- **(j) check (fills "Check: none yet").** `.ufo/waves/round-38/criteria/control_consequence_check.py`
  groups a round's receipts by `counterSha256`; a `control-*` receipt (or a control-seat-named
  receipt under `controls/` or `pre/`) with `met: true` taints its counter, and a claim receipt
  (`c<N>-*`, `claim-*`) with `met: true` under a tainted counter fails (exit 1). Red: round 37
  (`criteria/receipts/ccc-r37-at-99357694.txt`, exit 1: `c1-at-9dbc88bb` and `c1-keyrev-at-9dbc88bb`
  under the counter the shortcut control met). Green: round 36 and round 38 (exit 0); selftest
  10/10. Limit: classification is by file name, so a renamed control escapes it; round 38's
  full-rule tools are named under `v3/` and printed as notes, per the C2 declaration's build
  class (that class is itself open to the closure's ruling).
- **(k) A dead seat's item is reported unbuilt, never handed to a living seat.** Grounding:
  round-37 spot-check routed defect 4 (`CtlC1Shortcut` died; `CtlC1NoReader` built its control).
  Check: none yet (round 38 had no dead seat to test it on).
- **(l) A post-measurement receipt pins the measured tool bytes** (revision and sha256, re-derivable
  from the revision). Check: `.ufo/waves/round-38/pinned_selftest.py` writes `toolRevision`,
  `toolSha256`, `selftestSha256`; red: the round-37 postfix receipt has a path only; its pinned
  re-run `verification/postfix/r37-postfix-selftest-pinned.json` (137/137 on `944d2f51…d3e5`).
- **(m) Control receipts are committed before the build wave is dispatched.** Check:
  `.ufo/waves/round-38/criteria/timeline_check.py` compares the receipt's add-commit time with
  `w1-dispatched-at.txt`. Red: round 37 (`criteria/receipts/timeline-r37.txt`, exit 1, 435 s
  late). Green: round 38 (`timeline-r38.txt`, three control receipts, exit 0, 58 s before
  dispatch).
- **(n) A control list names only tools that skip declared work.** A declaration that lists, as
  controls, tools that may do all of the claimed work (a wrapper that implements every declared
  rule) or near-complete work (single-point mutants of the reference) makes its own consequence
  fire on a correct build. Grounding: round-38 C1, withdrawn before any build
  (`SCORECARD.md` "Round 38 — control call results"). Check: none yet; read the control list
  against the claimed rules before freezing.

## Round-39 criteria

- **(o) The key's power is measured by non-author seats before the declaration freezes it.** A sealed
  key is admitted as a counter only after independent mutant families of the reference (one seat
  per family, written from the contract) and at least one tweaked shortcut control (a parser-free or
  convenience reader improved key-blind toward the target) have been scored against it, and none
  meets the predicate. The declaration names, by sha256, every tool scored with the counter before
  it (oracle, reference, ablations) and the class each belongs to. Grounding: round 39 (lesson
  `corpus/lessons/round-39.md` Mistakes 1–2): 15 of 54 single-sentence mutants and a regex reader
  reach 24 of 24 on a key whose pre-declaration evidence was L1-written ablations only; the class
  sentence covered the pre-declaration reference. Check: the round's receipts under
  `.ufo/waves/round-39/criteria/control_consequence_check.py` v2.1 (content-only; red on round 39,
  exit 1 under both readings, `verification/a3-jcheck/v21-{A,B}.txt`). The inventory half has a draft
  checker, not yet adopted (`.ufo/waves/round-39/criteria/draft-o/`, reported in
  `.ufo/waves/round-39/w1a3/ScribeQualityCriterion.md`).
- **(p) Code-writing or code-running items are never routed to critic seats.** Grounding: lesson
  round 39 Mistake 3. Check: `.ufo/waves/round-39/criteria/route_check.py <spec>` — red on
  `w1-spec.json` (12) and `w1a3-spec.json` (11), green on `w2a3-spec.json`
  (`verification/a3-jcheck/route_check.txt`).
- **(j) amended reading, round 39:** the content check is v2.1
  (`.ufo/waves/round-39/criteria/control_consequence_check.py`); it decides by receipt bytes (frozen
  counter, predicate, key; rows; build by tool bytes), never by file name, label or class text
  (round-38 closure routed defect 4).

## Round-40 criteria

- **(o) amended, round 40: it applies to every counter, public or sealed.** A counter (witness set,
  fixture key or sealed key) is admitted only when non-author control receipts scored with the same
  counter bytes are committed at or before the declaration revision. Grounding: lesson round-40
  Mistake 1 (round-40 declaration frozen on L1-only controls; 27 of 76 later non-author controls met it;
  round-39 spot-check routed defect 4 had named this duty). Check:
  `.ufo/waves/round-40/criteria/preseal_order_check.py --revision <declaration> --counter <path>
  --receipts <dir>` — red at `f043c721` and at round 39's `ceecb1b1`, green at `12211cc5`
  (`.ufo/waves/round-40/verification/criteria/preseal-*.txt`).
- **(q) A routed defect is re-derived from its source or contract sentence before a fix is built.** A
  fix the source contradicts is recorded as a reject with the quote, not built. Grounding: lesson
  round-40 Mistake 2 (routed "fix D1" contradicted by S110 §2.8; a D1-"fixed" mutant meets the round's
  counter, so only a dedicated check catches it). Check for the D1 instance:
  `.ufo/waves/round-40/criteria/d1_check.py --tool <tool>` (exit 1 on `criteria/mutant_d1_fixed.py`,
  exit 0 on the base and the build) and selftest fixture `r40_d1_version_1_1_clean`.
- **(r) A counter's sandbox exposes no witness identity.** Case directories, mount sources, argv and
  environment visible to the tool carry no witness id or label, and the regression half runs under the
  same sandbox. Grounding: lesson round-40 Mistake 1 evidence (`CtlKeyFinder`: witness id read from
  `/proc/1/cmdline` and `/proc/self/mountinfo`; selftest case directory names key a 150-row table;
  `CtlLabelKeyed`: same leak). Check: the committed `CtlKeyFinder` and `CtlLabelKeyed` tools
  (`.ufo/waves/round-40/controls/w1/`) are standing controls — a future counter must score them below
  its target; the round-40 counter scores them 30 of 30 (`verification/w1/CtlKeyFinder__*.json`,
  `CtlLabelKeyed__ctl_label_keyed.json`), so this check is red on it.
- **(r) status, round 41:** green on the round-41 counter (`.ufo/waves/round-41/c1_count.py`): the
  standing `CtlKeyFinder` tools score 0 of 1434, `CtlLabelKeyed` 1012 and 1023, `CtlPositionKeyed` ≤1051
  (`.ufo/waves/round-41/verification/r40standing/`). Still open on it: bubblewrap's own environment at
  `/proc/1/environ` (counter v2 passes a minimal one), inherited stdin, no output byte cap
  (`.ufo/waves/round-41/w1/SentinelSandbox.md`).

## Round-41 criteria

- **(s) A control tally counts live seats only.** Receipts of a seat the dispatch log records as dead are
  listed apart and never counted as independent controls. Grounding: round-40 spot-check routed defect 1
  (lesson round-41 Mistake 2: "27 of 76" included four dead-seat receipts; live seats only 26 of 72).
  Check: `.ufo/waves/round-41/criteria/live_tally_check.py --dispatch-log <log>... --receipts <dir>` —
  red on round 40 (exit 1, four `CtlUTabOnly-dead__*` receipts,
  `.ufo/waves/round-41/verification/criteria/live-tally-r40.txt`), green on round 41 wave 1 (no dead seat).
- **(t) A build changed after any attack gets a fresh seat's review of its final bytes before the report.**
  A seat report (not the L1's reruns) names the final tool's sha256. Grounding: round-40 spot-check routed
  defect 2 (lesson round-41 Mistake 3). Check: `.ufo/waves/round-41/criteria/fresh_review_check.py
  --tool-sha <sha256> --reports <dir>...` — red on round 40's final tool `4de35f8c…`
  (`verification/criteria/fresh-review-r40.txt`, 0 seat reports). Weakness to test: a report that only
  quotes the sha passes it; read the report as well.
- **(u) A generated counter covers the support of the class it names.** Units are inserted at every
  position of a component, both ends included; optional components are generated absent and present-empty;
  every non-target part varies over its forms (no single template). A control that is right only on a
  skipped position or template meets a counter that lacks this. Grounding: lesson round-41 Mistake 1
  (`terminal_pct` and `v1_shape` met counter v1). Check: those two tools
  (`.ufo/waves/round-41/controls/w1/CtlNoPct/terminal_pct.py`,
  `controls/w1/CtlGeneratorShape/v1_shape.py`) are standing controls — red on counter v1 (both meet),
  green on counter v2 (both fail; `verification/w1v2/`).
- **(n) amended reading, round 41:** when a control list names a construction ("an allow-list", "a
  repertoire test"), a tool of that construction that agrees with the oracle on the whole generated class
  still meets, and the classification cannot be settled after scores. Name control classes by the behaviour
  they skip (a position, a component, a sub-shape the class generates), and decide equivalence by a
  frozen differential before scores, not by how the tool is written.

## Round-42 criteria

- **(v) A frozen harm rule names each new fixture's class and prices cost, before data.** A change
  fixture is red on the base, a guard is green on the base (or "guards only" is declared), and the rule
  carries a numeric cost bound against a named baseline. A rule that demands every new fixture red cannot be
  met by a round that adds guards, and a rule without a cost bound leaves cost unpriced. Grounding: round-41
  spot-check routed defect 1 (13 of 42 guards green on the base; ×12.87 cost unpriced); lesson round-42
  Mistake 1. Check: `.ufo/waves/round-42/criteria/harm_rule_check.py <SCORECARD> <round>` — red on round 41
  (exit 1, `verification/criteria/harm-rule-r41.txt`), green on round 42 (exit 0, `harm-rule-r42.txt`).
  Weakness: the check is lexical; a reviewer still reads the rule.
- **(w) A cost counter reads CPU through a channel the measured tool cannot write.** The measuring process
  is non-dumpable before it starts the tool, the timing record is appended after every descendant is
  reaped, and a forging control is a standing control. Grounding: wave-1 `CtlCpuHide`/`SentinelCounterSandbox`
  (lesson round-42 Mistake 2). Check: `controls/w1/CtlCpuHide/ctl_fake_timing.py` meets counter v1
  (`verification/criteria/fake-timing-c42_count.py.json`, ratios 0.003–0.026, met) and fails counter v3
  (`verification/w1v3/CtlCpuHide__ctl_fake_timing.json`, honest CPU T1 3.903, not met).
- **(x) A counter that tests "keeps every judgment" by sampling inserts every unit of the repertoire it
  guards into every slot, Unicode look-alikes of ASCII classes included.** Random samples of a few
  non-ASCII characters miss one-member mutants of a range (U+0080–U+009F, surrogates, U+FFFE/U+FFFF), of a
  zone-id set (`~`) and of a widened class (`\d` admitting `١`). Grounding: wave-1 `MutRegexNonAscii`,
  `MutRegexIP`, `MutRegexPct` (met v1 with witnesses); lesson round-42 Mistake 2. Check: those five mutants are
  standing controls — met v1 (`w1/MutRegex*.md`), fail v3 run E (`verification/w1v3/`).
- **Receipt identity for filed counts (round 46).** Any filed count or verdict against a receipt cites that receipt's path + sha256; a receipt citation without sha256 violates this criterion. Grounding: round-45 Mistake 15's fix says a count against "the claim receipt" must bind to that receipt's identity (path + sha256), and the count must be re-derived from the named receipt's committed bytes rather than another same-named receipt's values.
- **Citation reason fidelity (round 47).** An adjudication/ledger row's reason names the same repository, critic or provenance its citing line names; a reason naming a different repo than the citing line is a defect even when the class is correct, and is fixed by an append-only correction block citing the old line, never an in-place cell edit. Grounding: round-46 routed defect R4 (five rows misattributed charter vs ds4cc-marketplace / the wrong critic; `corpus/lessons/round-46-verifier-spotcheck.md`); the round-47 corrections at `corpus/quality/citation-adjudications.md` §Round-47 corrections.
- **Verdicts carry committed receipts (round 47).** A filed verdict-time gate result (exit code or tally) has its output committed as a receipt at the round it is claimed; prose restatement in a report or LOG is not the receipt. Grounding: round-46 routed defect R6 (verdict-time `--offline` exit 0 unreceipted); round-47 receipt `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`.

## Round-47 pointer correction — R6

The preceding criterion's initial working filename `offline-sweep-r46-verdict-time.txt` was withdrawn as misleading: the retained run is a round-47 rerun, not contemporaneous r46 evidence. Current receipt: `.ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt` (2026-10-24T06:46:36Z, sha256 `b86bc45992aa4f93c2c6d55d972a7d1a84ac0ffb46bedb7a674afd4a9822a717`); it does not retroactively receipt the r46 claim.

## Round-47 criterion grounding note

The round-47 criteria above are motivated and shown able to fail in `corpus/lessons/round-47.md`: Mistake 2 (R4 reason drift; `.ufo/waves/round-47/verification/c2-r4-mutation.txt`, sha256 `1e7636ecb023b2d2fa61d5bb6904166ebe84337514beed175c8010675cd507c3`, rejects 5/5 old-reason mutants) and Mistake 3 (the withdrawn r46 verdict-time claim and separate r47 rerun receipt). This note adds their motivating lesson pointer without changing either criterion.

## Round-47 counter receipt-label criterion

- **Counter matches the receipt's explicit exit label (round 47).** A count over a committed receipt accepts the explicit exit field the receipt records (`exit=0` or `OFFLINE_EXIT=0`), rather than hard-coding a spelling absent from the artifact; the `--offline` argv and the receipt's non-retroactive scope still have to match. Grounding: `corpus/lessons/round-47.md` Mistake 4; `verification/c2-after-846138c.json` (R6 false, sha256 `af6fcdbfd48927dab3662b420ef1dd2e967d1238d271c77e0b2553f693fb1674`) and `verification/c2-after-714e707.json` (C2_MET, sha256 `141ede64f4539481557c946dfc40fa5af574771b3a15a1cc58a0a2299d1b5dba`).
- **Open residual findings stay open after admission (round 49).** An admitted tool's residual-attack findings are named, with a count, in the next lesson; admission does not close them, and orchestrator-owned residual reports are not swept into a lane commit to make the count zero. Grounding: `considerthese/2026-10-24.md` (2026-10-24), first unimplemented proposal; opened pointer `.ufo/waves/round-46/residual/CriticCitationOverreach.md` (eight reports remain uncommitted; round 48 closed that file's Finding 1 only).

## Round-50 criteria

- **A wave citation carries its own grant (round 50).** A round that cites a dispatched wave commits
  the wave-slot grant stdout and the exact dispatch command as committed bytes at a revision that is
  a strict ancestor of the revision the citation is made in. The grant line names the lane, the wave,
  the seat count and the live/pending/cap triple; the dispatch command names the transport. A grant
  line that exists only in a report, in a LOG entry or in a `/tmp` file is not evidence, and `live=`
  is never re-derived by hand. Grounding: round-49 verifier routed defect 1 (the grant and the
  `kimi --prompt` transport lived only in the report and the LOG; `live=39` was never re-derived);
  lesson round-50 Mistake 1; check
  `python3 -B .ufo/waves/round-50/c50_durable.py --root . --revision <commit>`, which is durable 0 at
  the base and met only when the grant commit is a strict ancestor of the measured revision.
- **A quote's match class is derived from its own two blobs, never asserted (round 50).** A quoted
  span's class is derived by comparing the span against both retained blobs of that id: a span that
  is a substring of the retained HTML is `raw-substring`, a span that survives only whitespace
  collapse is `collapsed-only`. The class is recorded together with the sha256 of both blobs, and a
  collapsed-only span is never described as a raw substring nor the reverse — the two classes are
  different facts and a swapped label fails the check. Grounding: round-49 verifier spot-check
  (S273 collapsed-only, S274 a raw substring); lesson round-50 Mistake 2; check
  `python3 -B .ufo/waves/round-50/c50_quote_class.py --root . --revision <commit>`, with the
  swapped-label control in `.ufo/waves/round-50/verification/blur-control.txt`.
- **Operator-owned and inherited artifacts are not swept to zero a count (round 50).** Files the lane
  did not author — orchestrator-owned residual reports and inherited validation copies — stay
  uncommitted and untouched. A count is reported as it stands; it is never reduced by committing
  somebody else's file. Grounding: round-49 verifier routed defect 3; lesson round-50 (eight
  `.ufo/waves/round-46/residual/` reports and nine `>1MiB` copies under
  `.ufo/waves/round-48/assimilation/validate/` left uncommitted and untouched).
- **A source id cited as held ground resolves in this lane's own registry (round 53).** Every `S###` cited in `corpus/knowledge/` as supporting a claim or describing lane-held ground names a row in this lane's `corpus/SOURCES.md` at the citing revision; another lane's or a staged package's identically numbered row is not a substitute. A source that is not registered must be opened and registered under CORPUS rule 1 before it is cited, or the unsupported claim must be withdrawn by an append-only correction. Grounding: `corpus/lessons/round-53.md` §Mistakes (staged ids presented as held ground); the source census validates registry rows but does not resolve prose citations.
- **A source locator points to the section containing its quote (round 53).** For a retained HTML source, the cited heading text must occur in the body and identify the section containing the quoted span; a page-header date is not a section date. Corrected source anchors use superseding registry rows (`CORPUS.md` SOURCES rule 2), and corrections to admitted prose are appended rather than rewritten. Grounding: `corpus/lessons/round-53.md` § Mistakes; the locator falsifier `c53_gate_truth.py --revision 3994101` rejects the round-52 S329/S312 Gate and registry anchors (2 of 7 checks pass, exit 1), while its corrected-input selftest includes passing and failing heading/date cases.

## Round-54 criteria

- **A translation preserves a material source qualifier (S374).** A gloss of
  a quoted source phrase preserves each material action/subject qualifier
  from the located source context; when the source states that an operator
  does not recommend crawling a link target, the gloss must retain the crawl
  qualifier and must not collapse it into endorsement alone. Correct a
  historical gloss with an appended, source-anchored correction; never
  rewrite the old wording. Grounding: `corpus/lessons/round-53-verifier-spotcheck.md`
  §Discernment (S374, disagreement); retained body
  `.ufo/waves/round-52/sources/S374.html` (source title and paragraph);
  round-54 S374 correction in `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`.
  Falsifier: `python3 -B .ufo/waves/round-54/c54_s374_calib.py --root . --revision <commit>`;
  the committed base control must report `mismatches=1 met=False`, and the corrected
  entry must report `mismatches=0 met=True`.
- **CJK quote length names its unit and does not imply word-rule compliance.**
  For a source quote whose script does not use whitespace-delimited words,
  report the exact counting convention and the gate's accepted range. The
  inherited counter's `units()` counts each CJK character as one unit and each
  non-CJK whitespace token as one unit. A 6–40-unit Gate result is a local
  source-truth floor/ceiling; it does not prove conformance to CORPUS.md's
  ≤25-word rule. In particular S367/S372/S373 were measured at 31/27/27 units,
  above 25 units; their CJK lexical segmentation remains unresolved by that
  counter. Grounding: round-53 verifier spot-check §Discernment quote-length
  note; `.ufo/waves/round-52/c52_quote_truth.py` `units()` and its 6–40 Gate
  check; `CORPUS.md` SOURCES rule 1. Re-derive each CJK quote's count from its
  exact stored Gate span and report it as units, never as “words”.

## Round-55 criteria

- **An entry lands with its index row.** A knowledge file is not held until a
  row of `corpus/README.md` §Coverage map names it as `knowledge/<path>` in the
  Entry cell and describes it (5+ tokens, sharing a non-common word with the
  file's own head). An index row is a claim (`CORPUS.md` rules from the
  round-1/2 audits); 21 of 46 knowledge files had none across rounds 21–54.
  Grounding: `corpus/lessons/round-55.md` §Mistakes (reference-drift);
  `.ufo/waves/round-55/controls/base-c1-readme-index-v2.txt` (exit 1,
  `unindexed=21`). Falsifier:
  `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <commit>`
  must print `index_mismatches=0`; its `--selftest` carries the junk cases (a
  mega-row, a constant cell, a swapped population, an entry edited to fit its
  row) that the version-1 counter accepted.
- **New quotes stay at or under 25 units, so no word-segmentation ruling is
  needed.** A Gate quote and every quoted span in a new entry is at most 25
  units (one per CJK character, one per non-CJK whitespace token), a raw
  substring of the retained body, inside the page's content block; at least
  three page-unique spans per entry keep a navigation string from passing as a
  rule quote. This does not resolve the S367 (31 units) overrun; it stops the
  ambiguity from growing. Grounding:
  `corpus/lessons/round-54-verifier-spotcheck.md` routed defect 3;
  `.ufo/waves/round-55/w1/ExecStagedQuoteAudit.md` (6 of 6 staged spans over
  25 units); `.ufo/waves/round-55/w1/CriticC2Contract.md` A1.
- **A held row reused by a new entry changes `used-by` only.** The other ten
  cells stay byte-equal to the base row and each `used-by` change is logged
  old→new in the round lesson. Grounding: `CORPUS.md` SOURCES rule 2;
  counter condition C3/C4 in `.ufo/waves/round-55/c55_quote_truth.py`.
- **A validated append block is the appended block.** The scratch registry that
  the census validated before the append is byte-equal to the landed registry,
  and its three entries are byte-equal to the landed entries; a receipt of a
  census run is not a run. Grounding:
  `.ufo/waves/round-55/w1/CriticC2Contract.md` A6/A8; condition C7. Falsifier:
  the C2 counter's `--selftest` (`fail_validated_doc_differs`,
  `fail_census_forged_shape`, `fail_validated_entry_differs`).
- **A counter is attacked before it scores.** A counter that gates a claim is
  run against do-nothing and junk changes by a critic and a mutation-tester
  before any build is measured; a survivor becomes a selftest fixture in the
  same round. Grounding: `.ufo/waves/round-55/w1/MutC1Counter.md` (9 of 16
  mutants survived the version-1 selftest); `corpus/lessons/round-55.md`
  §Mistakes (vacuous).

## Round-56 criteria

- **A stated selftest tally is the tally its documented command prints.** A `SKILL.md` gate-registry row that says how many fixtures a
  selftest holds is a self-assessment; it is true only if the command in that row's Self-test cell, run in a clean clone of the revision
  under a fixed environment, exits 0 and prints that total. 7 of the 10 tally-bearing rows were false at round 55's base (claimed
  101/137/150/8/35/47 against 106/204/235/9/44/54, one selftest failing). Write the number from the printed output with its command
  (`claim-count-derivation.md`), never from memory of the round that wrote the row. Grounding: `corpus/lessons/round-56.md` §Mistakes
  (number-drift); `.ufo/waves/round-56/controls/base-c1-selftally-v2.txt` (exit 1). Falsifier:
  `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision <commit>` must print `tally_mismatches=0`; its `--selftest` carries
  the junk cases (a fake `python3 -c` command, a duplicate earlier row, a padded claim, a command in the Entry-command column, a rewritten
  selftest or helper, a host-exported pin).
- **A selftest that rebuilds from `HEAD` names its fixture revision in its row.** A selftest whose fixtures are `git show` of the
  checked-out tree rots as the tree grows: the round-52 quote-truth selftest printed 17/18 at the round-56 base while its row and receipt
  said 18/18. The row's documented command carries the pin (`KAKE_R52_SELFTEST_REV=1ae8de5d4dee`, `KAKE_R55_SELFTEST_REV=64c0ce12…`); the
  counter reads only the one pin its population entry names. Grounding: `.ufo/waves/round-56/w1/ExecPinProof.md`; `corpus/lessons/round-56.md` §Mistakes (stale-premise). Falsifier: `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` prints 18/18 and the unpinned form 17/18; the C1 selftest cases `env_pin_removed`, `pin_added_to_a_no_pin_row` and `pin_swapped_for_a_different_word` are `command_invalid`.
- **A held row reused by a new entry is re-opened by pinning its body, not by matching its title.** The held S367 row's title uses
  fullwidth punctuation the page does not print, so a title-substring check rejected the truthful build (7 of 8) and a three-character edit
  of the retained body satisfied it. The held row's body is pinned by the sha256 recorded when the row was opened. Grounding:
  `.ufo/waves/round-56/w1/CriticC2Contract.md` WR-1/A1, `CritCheatC2.md`; `corpus/lessons/round-56.md` §Mistakes (vacuous); counter C5 `HELD_BODY_SHA256`. Falsifier: `c56_quote_truth.py --selftest` case `fail_held_body_edited` (a one-comment edit of the retained S367 body, receipt recomputed, exits 1).
- **Sibling pages share phrases; page-unique means unique across every retained body, and a Gate quote occurs once in its own page.**
  The deleted-URL and non-existent-URL pages share four spans (the 404 status clause, the fallback clause, the head-tag clause); an entry
  may quote them for fidelity but they do not count toward the three page-unique spans, and the located Gate quote is chosen from the
  unique ones. Grounding: `.ufo/waves/round-56/w1/EntryDeletedUrl.md` §Quote classes; `CriticControls.md` (Gate repeat inside the article block); `corpus/lessons/round-56.md` §Gate. Falsifier: `c56_quote_truth.py --selftest` cases `fail_gate_quote_shared_with_sibling`, `fail_entry_only_sibling_shared_spans`, `fail_entry_only_spans_shared_with_unadopted_body`.
- **A staged candidate is re-derived, not renamed.** The page for S376 never says soft 404; the landed entry is
  `yahoo-japan-nonexistent-url-recrawl` and keeps the term only as a tagged lane reading; the staged file name must be absent from the
  tree. A staged claim the page does not state (a per-link-URL refusal on the S367 page, "the crawl loop follows what the server
  answers") is dropped, not softened. Grounding: `w1/ScoutClaimsAudit.md`, `w1/ReviewerStaged.md`, `w1/CritCheatC2.md` (staged name survives); `corpus/lessons/round-56.md` §Gate (rejects). Falsifier: `c56_quote_truth.py --selftest` case `fail_staged_name_survives`.
- **A quote is not taken from a line that contains a raw double quote.** The S367 meta-tag examples carry `name="robots"`; the ASCII
  quote regex splits them and the value-bearing piece is never verified. Describe such lines in prose and tag the description; quote the
  sentence around them. Grounding: `w1/CriticC2Contract.md` A6/WR-2; `corpus/lessons/round-56.md` §Mistakes (vacuous). Falsifier: `c56_quote_truth.py --selftest` cases `fail_entity_span_decoded` and `fail_long_single_token_fabricated`.
