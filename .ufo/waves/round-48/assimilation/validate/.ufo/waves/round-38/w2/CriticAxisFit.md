# CriticAxisFit — C2 axis naming and claim sizing after data (wave 2, falsify)

Attacked C2's axis label, the 20-case sizing, and universal clauses in the measured-results and lesson texts. Tip `adab4c7e`; read-only clone `/fast/scratch/hyaku/kake-r38w2/CriticAxisFit/clone` (HEAD `adab4c7e9ec2178657395f49346f18800ff4796f`). No network, no installs, no writes outside the report and sandbox; all runs `timeout`-capped and finished.

## Reproductions (command → exit → observed)

1. `python3 -B .ufo/waves/round-38/sealed_count_v3.py --root . --revision 3ed8e15c… --key-revision 99357694` → exit 0; cases 20, passed 20, met true, tool sha256 `f4d057c4…baace`, counter sha256 `28b120a5…`.
2. same, `--revision af43a50f` → exit 1; passed 8; passed ids exactly `c1 c2 c3 c4 d1 d2 d3 d4`; all `j1-4 u1-4 r1-4` failed.
3. `python3 -B clone/scripts/robots_audit_selftest.py --tool <git show af43a50f:scripts/robots_audit.py, sha256 944d2f51…>` → exit 1; 194 cases, 149 passed, **45 failed = h10+i26+k9**.
4. same selftest, round-37 shortcut `CtlC1Shortcut-followup-robots_audit.py` → exit 1; **44 failed** (b2, c4, d7, h5, i26).
5. Identity: `sha256(sealed_count_v3.py)` at `2dab7f31` == at tip == `28b120a5…`; `cases_v3.json` == `749ef6a6…` (pin); `git show --stat 3ed8e15c` = only `scripts/robots_audit.py`, +86/−10.

## Verdicts

- **"operability (tool repair)" is the surface changed — HOLDS.** Only the tool's bytes change at the measured commit (`git show --stat 3ed8e15c`), `AXES.md:13` defines operability as runnable artifacts whose command produces the stated outcome, and the claim names the tool's validation/comparison (`SCORECARD.md:2213-2216`), not the number; score stays 10→10 (`SCORECARD.md:2287`). "Repair" is stronger than the declaration says: (k) restates a held clause already at `SCORECARD.md:1841` ("The path `/robots.txt` is always allowed when (a) says the file decides") and (h) restates (g)'s "not JSON" (`SCORECARD.md:1855`); only (i) adds a rule. Holds.
- **Is (c)/(d) re-scoring counted as the move? — HOLDS ON THE DELTA, TARGET OVERSTATED.** Delta = exactly the 12 claimed-rule cases (repro 2), so (c)/(d) earn nothing; but 8 of the 20 predicate cases are held-rule behavior the base already passes, so the declared "surface unmoved" command returns **8 of 20, not 0**, and the row "passed 8 of 20 → passed 20 of 20" (`SCORECARD.md:2270`) gives 40 % of the target to held behavior. Honest after-state on the moved surface: 0/12 → 12/12.
- **"the base tool fails exactly the 45 (h), (i), (k) fixtures"** (`SCORECARD.md:2277-2278`, `corpus/lessons/round-38.md:96-97`) — **HOLDS exactly** (repro 3).
- **"the round-37 shortcut fails 44"** (`corpus/lessons/round-38.md:97`) — **HOLDS exactly** (repro 4).
- **"all 42 mutants and 8 ablations scored at most 19 (`verification/v3/`)"** (`corpus/lessons/round-38.md:67-68`) — true numerically (50/50 receipts present, max passed 19), but the counting command scores one tool per call and no committed command enumerates the 50; §6 item 9 requires a universal clause's set to be enumerated by the counting command. Clause true, **sizing text overstated as written**.
- **"Every post-measurement receipt names the tool's sha256"** (`SCORECARD.md:2135`) — holds numerically (154 verification receipts carry tool fields, 0 lack `toolSha256`) but cites no sweep; same enumeration gap, minor.
- **"Every run states `checksEvaluated`"** (`SCORECARD.md:2233-2234`) — holds for the 22 sealed-key runs (all carry it); counter refusal `verification/c2-keyrev-at-99357694.json` has none, so it is true only under the "key run" reading.
- **"Every control of the named classes scored at most 16 of 20 under v3"** (`corpus/lessons/round-38.md:67-68`) — true for the seven classes as enumerated (`SCORECARD.md:2243-2246`), but class membership is prose the counter cannot enumerate. Counterexample to the general reading: wave-1 `CtlExampleK` = **19 of 20** (`verification/w1attack/CtlExampleK.json`), a partial-rule tool in no named class and not a build. **Overstated if read as "all controls".**
- **Build rule "A tool implementing all three rules is a build, whatever its packaging"** (`SCORECARD.md:2250-2252`) — declared pre-freeze at `2dab7f31`, the four 20/20 tools are named at declaration (`SCORECARD.md:2241-2242`), and it is consistent with C1's withdrawal. Holds; the counter cannot separate packaging, so the after-state reads "the rules are implementable", which the changed tool bytes satisfy.
- Secondary doc drift (operability): `SKILL.md:1092` says the selftest has "(137 fixtures)" while `SKILL.md:1109` says 194 — **wrong (stale)**, one-number fix.

## Impacted axes

- **operability**: holds; repaired surface reproduced, score 10→10 HOLD, no harm found.
- **calibration**: three universal clauses rest on sets no counting command enumerates, and the round-37 rule of record (28/28) plus its 137-fixture selftest pass the base tool although it violates held clauses (e)/(g) — an honest-stop note for the closure, not a C2 defect.

## Smallest safe corrections (no counter, predicate, key or data change)

1. Report the split in the measured row and the lesson C2 bullet: base 8/8 (c)/(d) + 0/12 (j/u/r); after 8/8 + 12/12. Keep 20/20 as the predicate.
2. Replace "all 42 mutants and 8 ablations" / "Every post-measurement receipt" with one committed sweep command and its output (max passed 19; 0 receipts missing `toolSha256`), or drop the universal.
3. Qualify "every control of the named classes" to the classes as enumerated and cite the 19/20 `CtlExampleK` near-miss.
4. `SKILL.md:1092`: 137 → 194 fixtures.

## Deliverables (sandbox, absolute)

- `/fast/scratch/hyaku/kake-r38w2/CriticAxisFit/counter_after.json` sha256 `01677dac…89cf`
- `/fast/scratch/hyaku/kake-r38w2/CriticAxisFit/counter_before.json` sha256 `c20050c2…b3a1`
- `/fast/scratch/hyaku/kake-r38w2/CriticAxisFit/selftest_base.txt` sha256 `22621eca…064c`
- `/fast/scratch/hyaku/kake-r38w2/CriticAxisFit/selftest_r37shortcut.txt` sha256 `c6d151a0…974e`
