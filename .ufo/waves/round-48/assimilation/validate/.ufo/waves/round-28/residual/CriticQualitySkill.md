# CriticQualitySkill — round 28 residual attack on the QUALITY criteria and the Mistakes row

Target: `corpus/QUALITY.md:298-324` ("Counters and field evidence — round 28") and `corpus/lessons/round-28.md:63-70` (Mistakes) at `e57f601`; shipped head `8ecbefe`. Axes: operability (counter can fail), freshness (field evidence rule). Advisory only; no verdict on the round.

## Per-criterion verdicts

1. **"A counter must be able to reject a constant"** (QUALITY.md:303-308). Grounded: Mistakes row cites `round-27-verifier-spotcheck.md:21` (constant 16-pair mutant passed the finite predicate) and `round-26-verifier-spotcheck.md:11,13`; both lines checked and say what is claimed. No contradiction with QUALITY.md:101-106 (derived counts) or :285-289 (no admission from a fixed 16 predicate); it extends them. Checkable, and shown able to fail (see the mutant section). Two defects:
   - **Pointer not durable.** `.ufo/waves/round-28/w1a3/MutRefuseAllGate.md` is untracked: `git ls-files --others` lists it, `git log --all -- <path>` is empty, and `git ls-tree 8ecbefe -- .ufo/waves/round-28/w1a3` has 0 entries. Its evidence JSONs exist only under `/fast/scratch/.../w1/MutRefuseAllGate/count/`, and the mutant commits `eab579d`/`611af42` exist only in that scratch clone. Round 27 did commit its wave reports (`cd2e95b` holds `w2/MutateConstant.md`). Fix: commit the w1a3 note and copy the four counter JSONs into `.ufo/waves/round-28/verification/` before admission.
   - **Checkability convention.** Earlier counter criteria carry a "Fails if `<command>` exits ..." clause (QUALITY.md:105, :111, :161, :162). This one names a document, not a command. Fix: append "Fails if the C1 counter exits 0 on the recorded refuse-all or always-clean mutant", with the mutant bytes retained.
   - Tradeoff (not a defect): K1/K2 check exit, verdict and empty findings but not pair counts (`c1_interface_count.py:132-145, 251-254`). The always-clean mutant with counts 0 passes both (`always-clean-counter.json`, controls 2/4), so K3 and K4 alone reject it.
2. **"Conformance exceptions stay named"** (QUALITY.md:309-314). Matches routed defect 3 (`round-27-verifier-spotcheck.md:73`, details at :57). No contradiction: SKILL.md:678 already refuses credit for the void stub smoke. Checkable by reading the record. Open item: the wave-1 limit is "under 100 lines" (`w1a3-spec.json`), and `w1a3/ReviewUnreachableId.md` has 105 lines. It was written at 06:35:58 -03:00, after `e57f601` (06:32:58) and `8ecbefe` (06:34:48), so it is not a defect of `e57f601`. Under this criterion the round record must still list it.
3. **"No-harm keeps its measured scope"** (QUALITY.md:315-319). Consistent with routed defect 4 but only partial. Defect 4 (`round-27-verifier-spotcheck.md:74`) names three things: no-harm scope, the r24 policy stop and the out-of-population debt. The bullet says "(routed defect 4)" but leaves out the debt. The debt is not lost: it stays at QUALITY.md:266-272 and `round-28.md:78-79`. Fix: add "the out-of-population debt stays listed" to the bullet.
4. **"No field data is not a pass"** (QUALITY.md:320-324). Grounded: `round-28.md` Gate quotes S036/S038, `field-performance-cwv.md:13-14,104-114`, and SKILL.md:691-697 agrees row for row. No earlier QUALITY.md or SKILL.md rule about lab tools, Lighthouse, CrUX or percentiles conflicts (grep over both files). Checkable. Pointer gap: the "28-day window end" rule comes from S039 (`sources/a3/S039.txt`, collectionPeriod firstDate/endDate, "will always show 28-days, even if the data is not for the full 28 days"), but the bullet cites only S036 and S038. Fix: cite S039.

**Section grounding line** (QUALITY.md:300-301) says "routed defects 1–4", and the `e57f601` subject says "routed defects 2-4 as QUALITY criteria". No bullet covers defect 2 (presence versus strict support, 7 unknown units); the existing QUALITY.md:274-280 covers it. This overstates provenance. Fix: say "1, 3, 4; defect 2 stays under QUALITY.md:274-280".

## Mistakes row (`round-28.md:65-67`) and its fix

- Class and evidence: grounded, as in criterion 1.
- "Captured-by: none" overstates. QUALITY.md:285-289 already rejected admission from a fixed 16 predicate. QUALITY.md:161 already required pristine replay controls for the round-24 counters. Neither was a general rule that a counter must carry controls, so "partial" is the accurate entry. Fix: "partial — QUALITY.md:285-289 (admission side), :161 (round-24 replay controls); no general counter rule".
- **Dangling pointer.** `round-28.md:69` says "see the round-28 LOG entry". LOG.md has no round-28 entry at `e57f601` or `8ecbefe`: its last heading is LOG.md:1190 (Round27 non-author closure), and `git diff --stat 22c1669 8ecbefe` does not touch LOG.md. Fix: write the entry, or drop the sentence until it exists. Fleet-root check, read-only: `/home/vgpnk/Projects/shokunin/.ufo/waves/round-28/` holds only an empty `build/` from Oct 21. I checked no other fleet path.
- "Shown able to fail": true as recorded. The scratch JSON hashes match the note (pristine `65acffdf…`, refuse-all `86179507…`, always-clean `c44db28b…`, restored `152295c4…`). Re-parsed: refuse-all 11/15 (defects 11/11, controls 0/4); always-clean 2/15; pristine and restored 15/15. `restoration.json` records exactBytesEqual=true.

## Strongest counterexamples run (own sandbox, shipped head `8ecbefe`)

Sandbox `/fast/scratch/hyaku/kake-r28a3/res/CriticQualitySkill/clone` (git clone of the lane, checkout `8ecbefe`). TMPDIR, TMP and TEMP set to the sandbox, PYTHONDONTWRITEBYTECODE=1. Counter SHA-256 `a30d9d94…` is the same as recorded in the note and at `e57f601`. Command for each run: `python3 -B <lane>/.ufo/waves/round-28/c1_interface_count.py --root <clone> --revision <rev> --scratch <sandbox>/count`.

| Gate | Revision | Exit | Total | Failing cases |
|---|---|---:|---:|---|
| Pristine `8ecbefe` (gate SHA `6b83299d…`) | 8ecbefe | 0 | 15/15 | none |
| A: fixed "failed" answer (round-27-style constant: exit 1, one `unadjudicated_citing_pair`) | a24cc27 | 1 | 1/15 | all 11 defects, K1, K2, K4 |
| B: real input validation, `unadjudicated_citing_pair` findings dropped in `evaluate` | 86291a3 | 1 | 13/15 | K3 (exit 0, want 1), K4 (fixture selftest 15/29 failed) |

All stderr files were empty. Output SHA-256: pristine `30548c35…`, A `e4aaafa7…`, B `f794815d…`, all under `<sandbox>/count/`. Afterwards the sandbox gate was restored to `8ecbefe` bytes (commit `02fe061`; `git diff --quiet 8ecbefe HEAD -- scripts/citing_set.py` exit 0). Conclusion: the counter rejects three different constants or near-constants at the shipped head. B, the strongest one, is caught only by K3 and K4, which supports the counts tradeoff under criterion 1.

## Not verified

- No other input-keyed mutant was tried. Strength against every possible constant is not established.
- The C2 counter and S036-S039 quote fidelity were not re-run (other seats own them).
- The fleet root was not swept beyond the one directory named above.
- No network, no installs or updates, no lane Git or jj writes. The only lane write is this report.
