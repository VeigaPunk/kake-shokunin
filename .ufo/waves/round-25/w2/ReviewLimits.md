# ReviewLimits — r25 C1 falsify: executable capability vs. mere checklist

Seat: KakeR25.ReviewLimits (critic, author-side, read-only). Axes judged: operability, freshness.
Base read: HEAD `9f62cda`; packet doc and SKILL.md are byte-identical to HEAD; `corpus/lessons/round-25.md` has uncommitted additions (read from the working tree).
Production files edited: none. Delegation: none. Tools installed: none. Suite not run.
The only code executed was one read-only, in-memory probe: it imported `scripts/accessibility_packet.validate()` and wrote no files, ran no website, browser or network action, and touched no r24 material.

## Verdict

C1 holds as a **source-grounded checklist plus a structural gate**. As written it does not establish an **executable handoff/evidence workflow**. The prohibition boundary holds: nothing approves a website, publication or an evaluation. The operability "after" ("runnable offline packet inventory") is runnable only in the sense that it checks the shape of the checklist. The workflow itself (steps 1–5 in the packet doc) is prose that no tool emits, checks or records. Most of this is fixable wording and scope. Defect D1 is the substantive one.

## Counterexamples

### D1 — A hollow checklist passes the gate as "clean" (operability; fixable)
- Probe: replace every `publisherCheck`, `evidenceNeeded`, `failureExample` and `limitation` field in all 55 real cards with the string `"x"`, then call `validate(population, cards)`.
- Observed: `hollow 0 clean 55 []`, which is exit code 0, verdict `clean`, 55 accepted, no findings. The real cards give the same result: `real 0 clean 55`.
- Cause: `scripts/accessibility_packet.py` lines 72–73 accept any prose field that is a non-empty string. The supposedly independent counter in `.ufo/waves/round-25/measure.py` uses the same rule (lines 218–220, `type(...) is str and .strip()`). The selftest fixtures confirm that one generic sentence passes: `accessibility_packet.py` lines 114–118 and `packet_selftest.py` lines 58–59 ("Retain review notes and evidence for the examined content.").
- Impact: a clean result shows that strings exist and quotes are bound. It does not show that any card carries the evidence workflow the packet doc requires (step 4: "naming the tested build, dates, page/process scope, methods and limitations"). The two counters share this rule, so they agree because they are the same check, not because one independently confirms the other.

### D2 — The cards do not consistently require the step-4 evidence record (operability; fixable)
I counted case-insensitive matches in the real `accessibility-review-cards.json`. All counts are out of 55 cards, and they are upper bounds because the patterns are loose.

| Required by step 4 | Cards whose `evidenceNeeded` matches |
|---|---|
| reviewer | 27 |
| date / dated | 20 |
| build / version / revision | 9 (some of these are only browser or AT versions) |
| page / state | 44 |
| applicability judgment (step 4: "documented applicability judgment") | 2 |

Example: card 1.4.2 asks for "reviewer, date, and page version", while card 2.2.2 names no reviewer, date or build. The packet promises one evidence contract, but the cards provide a different one for each criterion, and no gate notices.

### D3 — The workflow is not executable and has no named artifact or recipient (operability; fixable or a tradeoff)
- The inventory output keys are exactly `accepted, criteria, expected, findings, schema, verdict, websiteConformance`. Each criteria row contains only `id/accepted/findings`, so the inventory emits no card text and no work list. Packet step 2 says "Run the packet inventory and read the relevant card", but the run itself gives the reviewer nothing to assign.
- Step 4's "separate work item" has no path, schema or owner. The validator rejects any `status` other than `not-assessed` (line 86), so evidence can never be recorded in the packet itself, which is by design. However, no other destination is defined either.
- The handoff recipients are roles, not names. The packet says "browser owner", "property operator" and "qualified reviewer", and the SKILL.md round-25 section says "adjacent ownership" and "operator-gated". The named owner exists only elsewhere: `PROVINCE.md` line 30 ("`tabi` drives browsers") and line 18 ("Publishing itself stays operator-gated: kake prepares, verifies and hands off"). "Separately authorized evaluation" never says who authorizes it.

### D4 — The §5.2 comparison against the saved source shows gaps in the step-1 work-item scope (operability; fixable)
Saved source `source-wcag22.html`, lines 2171–2232:
- **§5.2.4** (line 2208): "Only accessibility-supported ways of using technologies are relied upon…". **§5.2.5** (line 2216): the page must keep conforming when any technology that is not relied upon is turned on, turned off, or not supported. Neither can be scoped without a list of the technologies the page relies on. Step 1 asks for "page URLs, source revision/build, page variants, complete user processes and intended WCAG version/level" but omits that list. Only 3 of 55 `evidenceNeeded` fields and 4 of 55 `publisherCheck` fields mention relied-upon technologies or accessibility support. The packet doc names §5.2.4 and §5.2.5 only in its Conformance boundaries paragraph.
- **§5.2.1** (line 2181): "…or a conforming alternate version is provided." Step 1 does not ask whether an alternate version is relied on, and 0 of 55 cards mention one.
- **§5.2.2** (line 2192): the packet quotes "Conformance (and conformance level) is for full web page(s) only". That is accurate, 10 words, and matches the lesson erratum. It stops before "and cannot be achieved if part of a web page is excluded". Note 3 on responsive variations is reflected in step 1 ("page variants") and in the last row of the decision table, so this is acceptable.
- This doc-level §5.2 quote is not machine-bound. `population.json` has the keys `source, sourceSha256, opened, criteria` and no §5.2 text, so the gate checks only the card quotes.
- Positive control: the four criteria that §5.2.5 applies to all content (1.4.2, 2.1.2, 2.2.2, 2.3.1; source lines 2224–2227) each state that all content is in scope, including content not relied upon. Cards 1.4.2, 2.1.2 and 2.2.2 cite Non-Interference by name. **No defect.**

### D5 — The packet's pointer to execution evidence is premature (freshness, false provenance; fixable)
- The packet doc (line 111) says: "Evidence of capability execution and fixed-population before/after measurements is recorded in `corpus/lessons/round-25.md`".
- The lesson at HEAD says "After is measured only after execution" (line 8) and "Execution results… are appended after observation; no pending check is called passed here" (lines 71–72). The working-tree additions add "Proof execution remains pending until observed".
- No output from `measure.py`, `frozen_replay.py` or `--selftest` is recorded anywhere in the lesson. The contract's "runnable" claim therefore has no recorded run.
- The other freshness fields are sound: `verified-at` is 2026-10-21, the S035 row in `SOURCES.md` line 43 has a matching SHA256, and the recheck trigger is a WCAG version change on a pinned REC.

## Prohibition boundary: holds (no defect)
- Every result carries a hardcoded `websiteConformance: 'not-assessed'` (lines 31 and 148). No output field means approve, pass or publish. Step 5 says "Deployment, external account operations and publishing remain gated. This round performs none of them." Card 4.1.3 requests a separately authorized browser/AT evaluation and says "this packet performs no browser or account operation".
- `PROVINCE.md` lines 72–78 match this boundary. No live site, browser, account or publication action is implied.

## Smallest safe corrections (author-side; I made no edits)
1. **D1/D2:** state the gap honestly, or close it with one gate rule. The honest version: scope C1's "runnable inventory" to "structure + quote binding only; prose is unverified". The gate version: require every `evidenceNeeded` to name reviewer, date, tested build/revision, page/state scope, and an applicability judgment. Add a fixture with one-character prose to both the selftest and `measure.py` so the shared non-empty rule is shown to reject it.
2. **D3:** name the handoff targets in the packet doc and SKILL.md: browser/AT evaluation goes to `tabi` under separate authorization; source fixes, the evaluation request and publishing go to the operator. Name the location and format of the separate evaluation work item, or state plainly that the packet defines none.
3. **D4:** add to step 1: "technologies relied upon and their accessibility-support basis (§5.2.4/§5.2.5), and any conforming alternate version relied on (§5.2.1)".
4. **D5:** change packet doc line 111 to say execution evidence is *to be* recorded, or append the observed revision-bound `measure.py` output before admission.

## Judge-facing classification
- D1 makes the operability capability a checklist plus a shape gate, not a workflow. The canonical judge should either credit C1 only at that scope or require correction 1. D2–D5 are fixable defects, not tradeoffs.
- No regression, duplicate authority or identity change was found. The approval boundary holds.
