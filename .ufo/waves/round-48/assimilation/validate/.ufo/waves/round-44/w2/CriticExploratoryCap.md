# CriticExploratoryCap — round 44 wave 2

**Final review status: PASS.** The initial snapshot's missing S131/S132 link was subsequently repaired by its owning scribe and rechecked below. The historical failure evidence is retained; it is no longer an open defect.

## Axes and result

Axes: **operability** (C1), **freshness** (C2). This is a bounded declaration/provenance review, not a claim measurement or admission judgment.

- **PASS — claim-cap attack:** the round-44 addition declares exactly two measured-contract claims, C1 and C2, and zero exploratory claims. Each has its own predicate, counting command and kill rules. Capability acquisition does not create a third claim; the amendments revise the same two claims.
- **PASS — named sourced-claim attack:** C1's `Sourced.` line names existing row S129; C2's names existing row S130. The round-44 lesson's `## Gate` records their local paths and re-opening date **2026-10-23**. The three quotes are **6, 8 and 10 words**, all below 25. I re-opened all three cited sibling files; each quote matches its named section's first prose paragraph after removing Markdown code delimiters and folding whitespace. These are rendered-prose matches, not assertions of byte-identical Markdown.
- **FAIL — additional citation-repair link at the audited snapshot:** SCORECARD.md:3535–3536 says the locator repairs are carried by **S131/S132**, and the lesson's Gate supplies prospective superseding-row cells, but neither row exists in `corpus/SOURCES.md`. The original S129/S130 links pass; the assertion that their append-only locator correction is carried by registry rows does not yet resolve.

## Counterexample, evidence and smallest safe correction

The strongest local counterexample is a reader following the advertised corrected citation chain: `SCORECARD.md` → `S131/S132` → registry. That lookup finds zero rows for both IDs. Meanwhile S129 still locates the CtlDoNothing quote in paragraphs two to four, and S130 still locates its quote in paragraph two; the re-opened passages are in the first prose paragraph, as the Gate itself records. Thus a Gate correction alone has not completed the registry supersession.

This is **fixable provenance debt affecting both axes' sourcing**, not evidence of an axis tradeoff or a reason to relabel either claim exploratory. Smallest safe correction: append complete S131/S132 registry rows with the corrected first-paragraph locators and `teaches` beginning `supersedes S129 —` / `supersedes S130 —`, preserving S129/S130. Tie the new IDs explicitly to the existing Gate re-opening evidence if needed. Do not rewrite the frozen claim declaration. I notified the owning `kake-r44.ScribeSourcesRows` seat of the missing link; no source/corpus/scorecard edit was made by this seat.

## Commands and decisive output

Working directory for shell commands: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

Exact shell commands executed:

```sh
git diff -- SCORECARD.md
mkdir -p /fast/scratch/hyaku/kake-r44/CriticExploratoryCap
python3 -B /fast/scratch/hyaku/kake-r44/CriticExploratoryCap/claim_chain_audit.py
```

`git diff -- SCORECARD.md` exited 0 and showed the round-44 addition (169 insertions). Selected verbatim diff lines:

```diff
+### C1 — operability (capability acquisition): the witness-class gate
```

```diff
+**Sourced.** S129 (tameshi r33: control classes scored against a frozen counter before any
+build is judged) is re-opened this round; the G1–G10 classes are its method applied to the
+counter rather than the build.
```

```diff
+### C2 — freshness: the r43 ledger's receipt-derived figures re-derive
```

```diff
+**Sourced.** S130 (kama r29: a stated count must re-derive from committed bytes at the
+revision it was measured over) is re-opened this round; the r43 tally is its second failure.
```

```diff
+counted. **§8.7** (SOURCES anchor locators) is carried by the contract-rule-2 superseding rows
+S131/S132, not by this count. Each repair line must name the receipt file(s) and the derived
+value; a bare number does not repair.
```

`mkdir` exited 0, no output. The audit exited **1** solely because the additional S131/S132 repair link was missing. Complete verbatim audit stdout:

```text
INPUT SCORECARD.md sha256=1bd43d8fa5d4c8997c4da8e74c81cec00d2e4ae4142729ff75cdc577629e8832
INPUT corpus/lessons/round-44.md sha256=a6658296c9a1946456894163b3c60cbd61c9d13ca7c98cd5da54f1bc58e3f606
INPUT corpus/SOURCES.md sha256=9ec92ad6ff29ae4890f7a40955ccf78b31f9724b6c41af0eeefe56693cc7cf2f
CLAIM C1 axis=operability (capability acquisition): the witness-class gate measured_contract=True exploratory=False sourced=S129
CLAIM C2 axis=freshness: the r43 ledger's receipt-derived figures re-derive measured_contract=True exploratory=False sourced=S130
CLAIM_CAP declared=2 measured=2 exploratory=0: PASS
SOURCE C1->S129 sourced_line=True registry_rows=1 gate_rows=1
GATE S129 reopened_date=2026-10-23 paths=2 registered_and_exist=True quotes=2
QUOTE S129.1 words=6 limit=25 first_section_paragraph_match=True: The do-nothing shortcut never reaches predicate_pass=true
QUOTE S129.2 words=8 limit=25 first_section_paragraph_match=True: every pinned sha256 verifies over the committed blob
CHAIN C1->S129: PASS
SOURCE C2->S130 sourced_line=True registry_rows=1 gate_rows=1
GATE S130 reopened_date=2026-10-23 paths=1 registered_and_exist=True quotes=1
QUOTE S130.1 words=10 limit=25 first_section_paragraph_match=True: records a calibration error present when the statement was written
CHAIN C2->S130: PASS
NAMED_ATTACK cap_and_original_sourced_chain: PASS
SUPERSESSION S129->S131 scorecard_and_gate_reference=True registry_rows=0 supersedes_row=False
SUPERSESSION S130->S132 scorecard_and_gate_reference=True registry_rows=0 supersedes_row=False
CITATION_REPAIR_LINK: FAIL missing_registry_rows=S131,S132
```

Additional read-only tool evidence: SCORECARD.md:3401–3575; corpus/lessons/round-44.md:1–21; corpus/SOURCES.md:137–140; `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md`:7–21; the same directory's `ReviewFreeze.md`:3–7; `/home/vgpnk/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`:5–9. Skill/protocol text was read as review guidance; no alternate runtime or judge was invoked.

## Files written, unrun checks and blockers

Every file written by this seat:

1. `/fast/scratch/hyaku/kake-r44/CriticExploratoryCap/claim_chain_audit.py` — bounded offline audit used above.
2. `.ufo/waves/round-44/w2/CriticExploratoryCap.md` — this report.

No installs/updates, commits, pushes, production edits or frozen-artifact edits. No blocker to this review. The missing registry rows may be in flight with their owning scribe; the failure above is tied to the printed input hashes, not a claim about subsequent edits. C1 control/build/canary measurements and `scripts/ledger_latest_check.py` were **unrun by this seat** and are outside this item's attack. Once the owning seat lands the superseding rows, the same bounded audit is the check to run; no claim outcome was re-measured here.

## Closure addendum — notified superseding-row insertion

After the initial review, `kake-r44.ScribeSourcesRows` notified me that S131/S132 had landed. I read `corpus/SOURCES.md:137–143` and confirmed the complete new rows at 139–140, with the corrected first-paragraph locators, the required `supersedes` openers, and links to the round-44 lesson. S129/S130 remain present. The smallest safe correction described above is now present; **no missing link remains in this item's examined citation chain**. The original named cap/sourced attacks still pass.

Because the notified input changed, I ran the same bounded audit once on the new snapshot:

```sh
python3 -B /fast/scratch/hyaku/kake-r44/CriticExploratoryCap/claim_chain_audit.py
```

Exit **0**. Complete verbatim stdout:

```text
INPUT SCORECARD.md sha256=02c0111ee2c063c1a195f7144da1e423495fc8abf6979b3bdc77c3642d05ad37
INPUT corpus/lessons/round-44.md sha256=b8cee7f50b2fc5edbdc3b83add7a41e1612d095207d3daf697dd0e7124643508
INPUT corpus/SOURCES.md sha256=d54d630cdea5d0199ce457486d7c342d21fd4008de7112ce4f5893929277ddbd
CLAIM C1 axis=operability (capability acquisition): the witness-class gate measured_contract=True exploratory=False sourced=S129
CLAIM C2 axis=freshness: the r43 ledger's receipt-derived figures re-derive measured_contract=True exploratory=False sourced=S130
CLAIM_CAP declared=2 measured=2 exploratory=0: PASS
SOURCE C1->S129 sourced_line=True registry_rows=1 gate_rows=1
GATE S129 reopened_date=2026-10-23 paths=2 registered_and_exist=True quotes=2
QUOTE S129.1 words=6 limit=25 first_section_paragraph_match=True: The do-nothing shortcut never reaches predicate_pass=true
QUOTE S129.2 words=8 limit=25 first_section_paragraph_match=True: every pinned sha256 verifies over the committed blob
CHAIN C1->S129: PASS
SOURCE C2->S130 sourced_line=True registry_rows=1 gate_rows=1
GATE S130 reopened_date=2026-10-23 paths=1 registered_and_exist=True quotes=1
QUOTE S130.1 words=10 limit=25 first_section_paragraph_match=True: records a calibration error present when the statement was written
CHAIN C2->S130: PASS
NAMED_ATTACK cap_and_original_sourced_chain: PASS
SUPERSESSION S129->S131 scorecard_and_gate_reference=True registry_rows=1 supersedes_row=True
SUPERSESSION S130->S132 scorecard_and_gate_reference=True registry_rows=1 supersedes_row=True
CITATION_REPAIR_LINK: PASS
```

No additional file was written by this seat; only this report was updated. No full claim measurement, source-census run, canonical judgment, commit or integration was performed by this seat. The owning scribe's separate census result was not rerun here.
