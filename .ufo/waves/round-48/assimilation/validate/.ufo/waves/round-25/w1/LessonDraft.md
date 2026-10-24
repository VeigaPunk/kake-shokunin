# Round 25 lesson outline — C1 accessibility packet

## Axes and claim boundary

- **Operability:** the round-25 contract selects C1 as a capability claim on operability. Its intended change is from no publisher-side WCAG 2.2 A/AA review packet or runnable packet inventory to 55 source-grounded criterion cards and an offline packet inventory. The contract explicitly requires manual review and disclaims any website-conformity claim (`.ufo/waves/round-25/contract.json:4-10`).
- **Freshness:** round 24 named freshness and operability as its two claims; it described a lowest-axis tie at legacy 10 and made no scalar rating increase claim (`corpus/lessons/round-24.md:3-8`). Preserve those as axis/claim context only; this report has no new measurement or freshness finding.
- The round-25 contract identifies the source as “S035 WCAG22 pinned REC 2024-12-12” and records operability as the selected axis (`.ufo/waves/round-25/contract.json:13-16`). This report does not assert any WCAG criterion text or conformity result.

## Proposed lesson structure

1. **Claim and intended capability.** Describe the publisher-side manual-review packet as an intended operability capability, not an automated accessibility verdict. Keep the contract's 55-card target and its explicit manual-review/no-website-conformity boundary together.
2. **Evidence-source discipline.** Tie normative statements to the original pinned normative criterion text, not to an abstract or abstract-only tool response. The assignment reports that the initial original-URL read returned only an abstract and that raw pinned official content succeeded. Record this as a documentary source-boundary mistake; do not invent criterion quotations or imply that this report independently retrieved the raw source. The contract identifies S035 and its pinned REC date, but this report did not inspect that source body.
3. **Gate and status wording.** Present any eventual packet result only as packet readiness, keeping it distinct from WCAG conformance. The contract's intended after-state requires manual review and explicitly makes no website-conformity claim; do not promote a local packet result into a website assessment.
4. **Legacy-policy boundary.** State that round 24 remains withheld/unadmitted. Its policy-disposition record says no refused probe is retried, rephrased, rerouted or replaced, and distinguishes documentary verification of retained receipts from a newly executed gate result (`corpus/lessons/round-24.md:74-95`). The round-25 contract independently excludes r24 code/counter execution and bars repeating, rephrasing, rerouting or replacing refused probes (`.ufo/waves/round-25/contract.json:11-12`). The source-reading correction above changes neither that disposition nor its admission status.
5. **Limits and close.** Report only work and results actually observed for round 25. Round 24's local measurements and retained checks are not independent falsification or outside admission; its final author-side verdict says those remain incomplete and no promotion starts (`corpus/lessons/round-24.md:92-95,137-145`). Do not import those results as round-25 evidence.

## Gates and out-of-scope items

- Contract boundary: benign publisher-side accessibility documentation only; no security work, external-target tests, browser, account, publication, or r24 code/counter execution (`.ufo/waves/round-25/contract.json:11-12`).
- No live website was evaluated for this report. No WCAG criterion was marked passed, failed, inapplicable, or conformant. No packet was measured or validated.
- No builds, tests, linters, formatters, counters, source fetches, or runtime checks were run. No production files, corpus files, Git index, or jj state were changed.

## Findings, touched surface, provenance, and limits

- **Finding:** the safe lesson is a source-provenance lesson, not a policy-stop resolution: abstract-only output cannot substantiate a normative claim; use the pinned official criterion text and make the evidence boundary explicit.
- **Read:** `.ufo/waves/round-25/contract.json` (contract facts cited above) and `corpus/lessons/round-24.md` (policy-disposition and admission-boundary facts cited above).
- **Assignment-supplied observation, not independently rechecked:** the original WCAG URL read returned an abstract only; raw pinned official content succeeded. No URL fetch or source-content inspection was performed in this task.
- **Exact shell commands/outcomes:** none; no shell command was run. The two source files were read with the repository file-reading tool. No tool installation or update occurred.
- **Only affected file:** `.ufo/waves/round-25/w1/LessonDraft.md` (this report). It is an outline for the lesson, not a production lesson or an implementation result.
- **Artifact path:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-25/w1/LessonDraft.md`.
