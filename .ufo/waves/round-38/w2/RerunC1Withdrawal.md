# R38 w2 — RerunC1Withdrawal (v2 re-score of retained tools; SCORECARD control-call sentences)

Axes: operability (counter integrity, control verdicts), freshness (SCORECARD sentences vs re-run data).

## Attacked
C1 withdrawal facts: v2 receipts `verification/control-*.json` (12), `verification/mutref/` (42), `verification/pre/` under `.ufo/waves/round-38/sealed_count.py`, key `cases.json` (v2 pin `8b3fac55…2941`); and every sentence of SCORECARD "Round 38 — control call results".

## Method (all runs in sandbox clone at tip adab4c7e, TMPDIR + unset GIT_*; bwrap present)
- Counter hash: `sha256sum .ufo/waves/round-38/sealed_count.py` → `52daff55a2b8…7096e7b` = declared pin. Key at 99357694: `8b3fac558641…992941` = pin (counter also self-checks; any mismatch → exit 2; none seen).
- 64 tools re-scored: `timeout 850 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=…/tmp python3 -B .ufo/waves/round-38/sealed_count.py --root <clone> --tool-file <F> --key-revision 99357694f68886d3175fc6c386979c350be789bc`, 8-way parallel, exit 0/1 recorded (raws: `/fast/scratch/hyaku/kake-r38w2/RerunC1Withdrawal/rescore/`).

## Results (independent re-run vs lane receipts)
- 63/64 tools reproduce their receipt byte-for-byte on toolSha256, passed, met, counterSha256, cases, target, predicate, claim. The 64th (`w1-CtlExampleK`) has no same-named receipt; its receipt is `w1attack/CtlExampleK.json` — toolSha and passed=19 equal, met differs only by predicate (receipt: v3 counter `28b120a5`, ≥20 → False; my run: v2 ≥19 → True). No contradiction.
- Mutants: **29 of 42 met** (≥19), **13 at 20** (M12,14,15,22,29,32,33,34,35,36,38,41,42), 16 at 19, range 16–20. Identical in receipts and re-run.
- Control receipts met (passed=20, met=true): CriticPredicate-rulepatch, CriticPredicate-rulepatch_pct, CtlLabelShortcut-delegate_ceiling, CtlBaseWrapper-care. All other control receipts met=false: base 8, CtlTrivial 0/0/0, no_reader 1, label 16, min 18, CtlStdlibV2 13. Re-run matched every value.
- Separation/pre receipts re-run: reference 20 met; ablations A1–A8 = 18,18,16,16,17,16,18,18, none met — matches SCORECARD's declared ablation numbers.

## SCORECARD "Round 38 — control call results" — verdicts
- Counter sha `52daff55…6e7b`, predicate `passed >= 19 of 20 sealed cases`: **holds** (hash + receipts + code `PREDICATE`/`TARGET = 19`).
- Table rows base 8 / trivial 0,0,0 / no-reader 1 / label 16 / delegate ceiling 20 met / min 18 / stdlib 13 / care 20 met / rulepatch,rulepatch_pct 20,20 met: **holds** (all reproduced).
- Mutant row "16–20; **28 meet**": **wrong as written** — 29 meet (13 at 20, 16 at 19). Overstated precision, understated count; corrected later in the same document ("measured results": "29 of 42 … not 28"). Direction: anti-self-serving (more controls met ⇒ withdrawal even more forced); no verdict changes.
- "each breaks one contract sentence; 13 pass all 20": **holds** (13 confirmed by id list).
- "**C1 is withdrawn before any build**" / "No build seat had been dispatched": **holds** on observables — `git diff --stat b0ab7f60 2dab7f31 -- scripts/robots_audit.py` = 0 lines (tool untouched between declaration and withdrawal); the only later tool change is C2's 3ed8e15 (touches only `scripts/robots_audit.py`, 86+/10−).
- "Controls of both listed kinds met it": **holds** (mutation pass: 29 of 42; wrapper arms implementing all three rules: 4 receipts at 20).
- "The wrapper arms do the claimed work, so no counter can put them below target": **consistent** (all four at 20 under v2; also 20 under v3 per declaration receipts — not re-verified by me under v3).
- Counter defects listed (F1 echo-id accepted, F2 traceback without receipt, checksEvaluated not compared): checksEvaluated non-comparison **holds by inspection** (v2 docstring: "`checksEvaluated` and any other field are not compared"); F1/F2 not re-derived (out of scope; v3 receipts `c2-keyrev-*` exist as the fix's artifacts).
- Declaration defects listed (PREDICATE lacked `met: ` prefix; 19-of-20 tolerates one failed held-rule case): **holds** — v2 `PREDICATE = "passed >= 19 of 20 sealed cases"` (no prefix), `TARGET = 19`.

## Net
Withdrawal rationale is sound and, if anything, understated: the only wrong figure in the section ("28 meet") flips to 29 on re-run, same conclusion. No overstatement that favors the landed work was found in this section.

## Residual risk / gaps
- "Every tool a seat named was scored": I scored the 64 retained files; a seat-named tool absent from `retained/` would be invisible to me (no counter-evidence either way).
- F1/F2 counter defects accepted from reports, not re-derived; v3 fix not re-verified here (v3 is C2's counter, other seats' scope).
- wrapper-arms "no counter can put them below target" is an argument, not a theorem; I confirmed only v2 (and v3 receipts' say-so).

No tools installed (used system python3, git, bwrap). Sandbox artifacts: `/fast/scratch/hyaku/kake-r38w2/RerunC1Withdrawal/rescore/` (64×.json/.exit/.err), `tool_list.txt`.
