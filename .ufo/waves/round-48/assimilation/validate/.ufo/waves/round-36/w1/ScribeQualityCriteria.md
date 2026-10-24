# Round 36 wave 1 — criteria draft

- **Axes:** operability (judged axis); freshness (lane axis, reflected in the C1 audit criterion).
- **Behavior:** drafted `## Round-36 criteria` with (a)–(d), mapping to routed defects 1–4. Each criterion names its requested checker and a concrete negative/failing case. Draft also requires the C1 contract's seven individual ablations to score below 25/28.
- **Draft artifact:** `/fast/scratch/hyaku/kake-r36w1/ScribeQualityCriteria/quality.md`, lines 1–11; sha256 `8c46981557914cdeeff96c1394385b2d769afa316ed820bdf64c1400b2082258`.
- **Provenance:** shaped from lane `corpus/QUALITY.md` Round-34 (lines 606–675) and Round-35 criteria (lines 693–844); routed defects from `corpus/lessons/round-35-verifier-spotcheck.md:183-201`; read the existing `knowledge_control_check.py` contract at `.ufo/waves/round-35/criteria/knowledge_control_check.py:1-63`. These references supplied the known R35 failures quoted in the draft.
- **Gates/evidence:** no checker, counter, build, test, network request, or sealed-case access was run. The cited round-35 checker failure is pre-existing evidence in `corpus/QUALITY.md:839-841`, not execution by this seat. The three round-36 checker paths and negative cases are proposed criteria, not evidence that those scripts exist or have run.
- **Commands and outcomes:** `timeout 30s mkdir -p /fast/scratch/hyaku/kake-r36w1/ScribeQualityCriteria` — exit 0, no output. `timeout 30s sha256sum /fast/scratch/hyaku/kake-r36w1/ScribeQualityCriteria/quality.md` — exit 0; printed the hash above.
- **Touched surfaces:** wrote the draft only in the assigned sandbox; this report is the only lane file written. No product file, Git state, or other lane was changed. No tool installed or updated.
- **Out of scope / limits:** did not run the listed criterion checks, independently score the counter, or verify the proposed round-36 checker interfaces/receipts. No conclusions about round admission or verdict.
- **Report artifact:** `.ufo/waves/round-36/w1/ScribeQualityCriteria.md`.
