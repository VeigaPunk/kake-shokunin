# CriticClaimC2 — freshness claim design review

**Axis:** freshness (assigned). Operability/C1 and round admission are not judged.
**Result:** the original four-family, last-regex-match design can report numerical agreement without establishing meaningful supersession or immutable provenance. The L1 has adopted a narrower three-figure declaration, endpoint equality, and same-line receipt attribution. Those decisions address important defects; they are not evidence that an implementation or a repair has landed.

## Final L1 decision incorporated

The final decision arrived in the authoritative parent interjection during this review:

- **Three counted figures:** §8.1 re-score tally, §8.5 do-nothing ratios, §8.5 build ratio range. The declaration must say three, not four.
- **Equality, not containment:** compare every quoted scalar/range endpoint with the receipt-derived value rounded to the same quoted precision. A build-range family is red if any endpoint differs.
- **§8.4 wave composition is excluded from the count on the record.** The L1's reason is that the worktree now has 51 Markdown reports whereas the historical revision had 50; the directory/settle-prose denominator is revision-dependent rather than one of the selected receipt-derived figures. Its LOG/SCORECARD corrections remain routed work, not counted success.
- **§8.7 SOURCES anchors:** S131/S132 will carry contract-rule-2 supersession, separately from this count.
- **Each repair line must name its receipt file(s) and the derived value.** A bare number is not a repair.

The narrower declaration can legitimately reach zero while excluded work remains, **provided that this exclusion is explicit**. It cannot be presented as the original four-family repair or as closure of the whole routed set. Revision dependence does not itself make the wave figure unauditable: the historical tree can be pinned. Its exclusion is a disclosed scope decision, not proof that historical composition cannot be measured.

## Local evidence

Sources below are lane-relative unless marked fleet:

1. `corpus/lessons/round-43-verifier-spotcheck.md:195-228` is the routed-defect inventory, not the round-44 proposal text.
2. `SCORECARD.md:3393` says re-scored **18 of 27**. The 14 JSON files in `.ufo/waves/round-43/verification/l1-rescores/` have 14 distinct `toolSha256` values; the spot-check independently records that same distinction at `:197-201`.
3. `LOG.md:1660-1662` contains build T1 **1.00–1.02**, T5 **1.13–1.18**, and do-nothing T1 **4.27**, T5 **8.68**. Its final correction entry does not supply the replacement ratios. The receipt `ref41-base.json` has `ratios.T1=4.207`, `ratios.T5=7.047`; the three build receipts have:

   | Receipt | T1 | T5 |
   |---|---:|---:|
   | `build-1.json` | 1.005 | 1.105 |
   | `build-2.json` | 1.009 | 1.144 |
   | `build-3.json` | 1.004 | 1.215 |

   Therefore the receipt-derived extrema are T1 **1.004–1.009**, T5 **1.105–1.215**. The same receipts identify the held build by `toolSha256=914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`.
4. `LOG.md:1679` and `SCORECARD.md:3297-3298` both retain **47 reports / 15 dead / 4 live**. The settle line says **50 reports / 15 dead / 1 live**. The historical tree at `a377c5d0b98e7d5f28171bc47096e9592ac989a5` contains 50 `.md` reports plus `swarm-registry.json`; it does not contain `CtlPrefixCache.md`. The worktree directory listing includes that additional report. This is a real local example of a mutable glob changing expected history.
5. `corpus/knowledge/claim-count-derivation.md:7-9,22-25` requires a count's measured revision and an appended correction naming the superseded text. `corpus/QUALITY.md:31-41` preserves old lines and permits EOF correction blocks citing the old line. `SCORECARD.md:3334-3339` already demonstrates legitimate appended ratio supersession without rewriting the frozen text.
6. At inspection, both `scripts/ledger_latest_check.py` and `.ufo/waves/round-44/ledger-quotes.json` were absent. I reviewed the declared design at `.ufo/waves/round-44/make_w1_spec.py:117-127` and the final L1 decision, not an observed implementation. The executor's intermediate description of containment/full-text `re.S` matching is superseded by the final equality decision; it is not treated as code evidence.

## Attacks, survival, minimum correction

### (a) Bare numerical suffix: correct bytes without a meaningful correction

**Counterexample shape (static, not an executed checker witness):** append a parser example containing the expected numbers, while the surrounding text explicitly says it is an example, not a correction. A regex that only extracts numbers can select those bytes without changing which historical statement is operative. An unlabelled line with correct numbers has the same problem: it need not identify the round, source receipt, or superseded assertion.

A genuinely explicit appended correction can repair staleness; absence of an inline receipt pointer alone does not prove its numbers false. The defect is treating any matching number as sufficient evidence of repair. The lane's existing count-derivation rule requires the superseded text and measured revision as well.

**Original design survives? No:** its declared predicate only compares captured values. **Final design:** same-line receipt attribution is adopted, so the bare-number form is disallowed by the final instruction. Enforcement and the distinction between examples and operative corrections remain unobserved.

**Smallest safe correction:** require an identified correction record with round + figure ID, explicit `supersedes` target, receipt file(s) + source revision, derived value, and counting/derivation command. The parser should select an operative correction record, not arbitrary quoted/example text. Receipt text must identify the actual source used, not merely contain the word `receipt`.

### (b) Mutable specification / mutable expected source: two editable authorities

**Strongest observed counterexample:** the historical r43 tree has 50 reports but the current worktree has 51 because `CtlPrefixCache.md` is now present. The original expected-value rule used a worktree glob. A later report can therefore change what an unchanged r43 sentence is expected to mean. Similarly, a spec can be made easier by changing its entry set, receipt path, or derivation instead of repairing a ledger. Committing a new source does not make it the evidence for the original r43 event.

This is not an allegation that editing any receipt is forbidden or that a local checker can resist an owner who rewrites both code and its trust anchor. The relevant boundary is the independently reviewable frozen declaration and its immutable source objects.

**Original design survives? No:** no fixed source commit, complete entry-set assertion, or input-digest binding is required. **Final design:** excluding the wave glob removes the demonstrated moving-denominator case from C2. Binding the remaining JSON receipts and spec against substitution is still required; it has not been observed.

**Smallest safe correction:** freeze the exact three IDs and derivations; pin the historical receipt revision and exact receipt set/blob identities independently of ledger text; read those committed bytes, not mutable glob results. Record the measured ledger revision separately. Missing/duplicate/replaced entries or sources must not produce a smaller successful denominator. Do not silently mix a worktree ledger with a `master` fallback and another receipt snapshot. A missing measured ledger is not repaired by reading a different revision.

### (c) Last matching text is not necessarily the latest assertion of that figure

**Counterexample shapes:** a later historical quotation, a rejected counterfactual, a table from another context, or a correction that quotes the old value. None automatically updates the r43 figure. Conversely, LOG's original do-nothing pair wraps across `:1661-1662`; a literal single-line rule can miss it. Replacing that with unrestricted full-text matching can join T1 and T5 from different statements unless the statement boundary is explicit.

**Original design survives? No guarantee:** the specification says “last line matching the pattern,” not “latest operative correction for this stable figure identity.” The actual patterns were unavailable. **Final design:** neither equality nor a receipt pointer alone resolves this identity/context problem.

**Smallest safe correction:** use a narrow, stable correction-record grammar keyed by round and figure; parse each record within its own boundary; reject ambiguous records and require complete values from the same record. Ignore code/example/quoted material rather than allowing later incidental text to silently replace an assertion. Add negative cases for an unrelated suffix, a stale-value quotation in a correction, wrapped originals, and mixed-record T1/T5 extraction. A generic one-green/one-red numeric selftest does not establish these properties.

**Additional minimum for the former four-family design:** wave composition exists in **both** ledgers. A spec entry with one `file` cannot establish that both copies were corrected. Require two target assertions aggregated into one wave family, or honestly count **five assertions for four families**. The new three-family count excludes this issue rather than solving it; the routed LOG/SCORECARD correction should still cover both locations.

### (d) Four figures were not the whole routed set; three certainly are not

| Spot-check route | What actually needs repair | Counted by final C2? / minimum separate action |
|---|---|---|
| §8.1 | SCORECARD and fleet report overstate L1 re-scores as 18; durable set is 14 | **SCORECARD tally counted.** Correct the closed fleet-report copy via a named erratum in the current report or an appended erratum, not a rewrite. |
| §8.3 | Fleet report attributes README index row to freeze; it landed at settle | **No.** Current-report erratum must name the false attribution and correct commit. Numerical ledger equality does not test attribution. |
| §8.4 | Both ledgers say 47/15/4 instead of historical 50/15/1 | **Explicitly excluded.** Correct both with a pinned historical revision and retain the exclusion in the declaration. |
| §8.5 | LOG baseline ratios and build extrema remain superseded-but-uncorrected there | **Yes, two figures.** Same-line receipt-backed appended replacements, with exact endpoint comparison. |
| §8.7 | SOURCES S129/S130 anchors still have old paragraph locators | **No.** L1 adopted S131/S132 superseders; require actual rows opening `supersedes S129 —` / `supersedes S130 —` and grounded corrected locators. A lesson erratum alone was already insufficient. |
| §8.8 | Uncaptured Mistakes 7/9/10/11 have no new QUALITY criterion citing the lesson | **No.** Add grounded criterion/criteria with explicit capture mapping and lesson citation; numerical C2 success is not evidence this learning duty was met. My search found no `round-43`/`round-44` citation in QUALITY at inspection. |

Other routed defects reinforce the scope boundary: §8.2's dead-seat citation and §8.6's role-mix arithmetic are in the closed fleet report, outside these figure families; §8.9's formerly undurable prefix report is not established by counting ratios; §8.10 is operator-side, not lane debt. In particular, the closed report's “build 16 — 14 executor, 3 scribe, 1 connector” adds to 18 without explaining the two scribes assigned to attack. A current-report erratum can clarify that split; no old report rewrite is needed.

**Original design survives? Only as an explicitly limited four-family claim, not as whole-routed-set repair. Final three-family design:** survives this scope attack at the declaration level because the L1 explicitly names the exclusions. The minimum is the explicit scope sentence plus separately evidenced routing outcomes; adding an unrelated fifth number would not repair SOURCES, attribution, or learning-duty defects. The useful fifth *assertion* in the original design was the second ledger's wave statement, not an invented freshness metric.

### (e) Append-only LOG: repair is possible without deleting old ratios

**Counterexample to the alleged impossibility:** SCORECARD already preserves the old freeze values and appends true receipt values at `:3334-3339`. LOG can do the same. Append-only does not mean the last correct statement must erase all historical wrong tokens, and leaving clearly superseded history is not itself current staleness.

**Survives? Yes, if the correction is explicit.** A rule requiring the old ratio text to vanish would conflict with the record-preservation contract; a bare numerical tail would under-specify supersession.

**Smallest safe correction:** append a dated correction naming `LOG.md`'s r43 entry/old lines at the old revision, state which values it supersedes, identify `ref41-base.json` or the three exact build receipt filenames and source revision, and give the derived replacement values. Preserve prior bytes. No rewrite, suffix edit, or insertion into the old sentence is needed. Prefix preservation is a separate assertion from numerical agreement; it was not executed in this review.

## Equality/precision attack and adopted correction

The intermediate containment proposal would accept an arbitrarily broad range such as 0–999 for every positive recorded build ratio. That is not the recorded min/max, even though it encloses all receipts. This is a static counterexample to containment-as-range-freshness, not an observed run.

**L1 adopted the safe correction:** endpoint equality after rounding to the quoted precision. For clarity, at two decimal places T1's lower endpoint `1.00` agrees with 1.004, but its upper `1.02` does **not** agree with 1.009 (1.01). The T5 endpoints 1.13/1.18 also do not match the receipt extrema. Thus both the T1 and T5 range pairs are wrong, but not every individual T1 endpoint is wrong. The family still contributes only one mismatch.

Freeze the intended precision/rounding policy, and compare both T1 and T5 pairs, not just the failing T5 range. Writing the corrected receipt values at their existing three-decimal precision avoids the two-decimal tie ambiguity. Equality corrects the containment defect; it does not replace source/identity assertions.

## Minimum-strengthening checklist / adoption status

1. **Explicit three-figure scope and named exclusions — adopted by L1.** Do not report four-to-zero or whole-routed-set closure.
2. **Exact rounded scalar/endpoint equality, not interval containment — adopted by L1.** Fixed precision/rounding policy should be explicit.
3. **Receipt filenames plus derived values on each repair line — adopted by L1.** Add source revision, stable figure ID, and named superseded location to make the pointer meaningful.
4. **Immutable historical receipt set/revision; complete fixed entry set; measured ledger revision — still an implementation/evidence requirement, not observed.** Prevent mutable-spec and mixed-snapshot success.
5. **Latest operative statement rather than last incidental regex match; adversarial negative fixtures — still an implementation/evidence requirement, not observed.**
6. **Append-only preservation plus explicit supersession — required by existing lane rules; not executed here.**
7. **Both wave-ledger locations, or a fifth target assertion under the original four-family design — excluded from final C2; remains separately routed work.**
8. **S131/S132 source-row supersession — adopted as separate work, not observed landed here.** Attribution/report errata and QUALITY capture mapping likewise cannot be credited by the three-number counter.

No canonical judgment/admission is made. These are fixable design defects and disclosed scope boundaries, not a request to silently broaden the final claim.

## Commands and decisive verbatim output

All shell commands ran with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`.

```text
$ mkdir -p /fast/scratch/hyaku/kake-r44/CriticClaimC2
(no output)

$ git rev-parse HEAD
18cb2c28f47c3ec3732ffa06c456e61b3444b1a2

$ git ls-tree -r --name-only HEAD -- .ufo/waves/round-43/w1/
[output trimmed to two verbatim inventory lines; the complete result had 50 .md paths and this registry]
.ufo/waves/round-43/w1/CtlPortValue.md
.ufo/waves/round-43/w1/swarm-registry.json

$ git ls-tree -r --name-only a377c5d0b98e7d5f28171bc47096e9592ac989a5 -- .ufo/waves/round-43/w1/ | wc -l
51

$ git ls-tree -r --name-only a377c5d0b98e7d5f28171bc47096e9592ac989a5 -- .ufo/waves/round-43/w1/CtlPrefixCache.md
(no output)
```

`51` above counts **all entries**, including the one JSON registry, not 51 historical Markdown reports. The worktree `read`/`glob` inventory separately included:

```text
- CtlPrefixCache.md 5.6KB 2h ago
```

Read-only tools inspected the source paths cited above. Decisive exact invocations/results (only relevant output retained):

```text
functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-43-verifier-spotcheck.md:1-260")
197:1. **Re-score tally overstates its receipts.** Report Before → after and `SCORECARD.md:3393` say
198:   "L1 re-scored 18 of 27"; `verification/l1-rescores/` holds **14** re-score receipts (11 in
199:   `exits.txt` + 3 in `exits2.txt`, 14 distinct `toolSha256`), and no other committed set carries
207:4. **Wave composition drift.** `SCORECARD.md` (settle section) and the LOG "Round 43 correction"
208:   entry say "47 reports, 15 dead, 4 live-at-settle"; the settle line and `w1/`'s 50 `.md` files say
209:   50 reports, 15 dead, 1 live.

functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/verification/freeze/ref41-base.json:178-196")
181: "ratios": {
182:  "T1": 4.207,
186:  "T5": 7.047

functions.grep(pattern="round-43|round-44", path="/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md", case=false, gitignore=false)
No matches found

functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/ledger_latest_check.py:1-250")
Path '/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/ledger_latest_check.py' not found

functions.read(path="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/ledger-quotes.json:1-210")
Path '/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/ledger-quotes.json' not found
```

The fourteen `toolSha256` fields were read with `functions.grep(pattern="\"toolSha256\"", path="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/verification/l1-rescores/*.json", case=true, gitignore=false)`; all fourteen displayed identities were distinct. Each build receipt was read with its JSON selector `?q={label,seed,toolSha256,met,ratios}`. These are source inspections, not counter executions.

**Unrun:** checker, checker selftest, before/after counter, full C1 counter, builds/linters/tests, append-only preservation check. No zero-mismatch output, numeric counter delta, or implementation conformance is claimed.

**Writes:** this report only; empty scratch directory `/fast/scratch/hyaku/kake-r44/CriticClaimC2/` created as required. No lane implementation, ledger, source row, receipt, fleet, or sibling file edited. No tools installed or updated.

**Blocker/limit:** checker and spec were absent at inspection, preventing implementation-specific pattern/exit testing. The assigned design review is complete; the final L1 decision is incorporated, and adoption is distinguished from observed code/repair landing.
