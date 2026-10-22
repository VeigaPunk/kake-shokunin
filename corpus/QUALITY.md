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
