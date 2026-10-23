# CriticReclassification — are C2's control classes a post-hoc reclassification?

Attacked: `SCORECARD.md` (tip `adab4c7`) lines 2243–2251 (class list, withdrawal clause, build definition), the round-38 (j) check's green, and the C2 before/after receipts. Sandbox `/fast/scratch/hyaku/kake-r38w2/CriticReclassification/` (clone at tip, `TMPDIR` set; read-only git in the lane). No tool installs; no lane file touched except this report.

## Facts

1. **Timing** (`git log --format='%h %cI'`, exit 0): C1 declaration `b0ab7f6` 04:14:15Z; ctl dispatch 04:15:37Z (`ctl-dispatched-at.txt`); withdrawal + C2 + class list `2dab7f3` 04:28:54Z; wave-1 dispatch 04:29:52Z; build `3ed8e15c` 04:38:59Z.
2. **The class that carries the verdict did not exist at declaration.** `git grep -c 'implements all three' b0ab7f6 -- .` → exit 1 (no match in the whole tree). The build/control boundary first appears at `2dab7f3`:SCORECARD:2250–2251 — after the control scores, in the same commit as them. C1's declaration names the wrapper family as **controls** (:2168 "a cheapest-wrapper shortcut around the base tool") and forbids reclassification (:2171).
3. **The four met tools are byte- and score-identical under both counters** (receipts read with `python3 json`): care `3215ae1a…`, delegate_ceiling `5c80fb01…`, rulepatch `8a5712b4…`, rulepatch_pct `b2c86c8c…` — 20/20 v2 and 20/20 v3, `same_sha=True`. v3 changed nothing about them; only the label changed.
4. **They are true positives, not false passes.** 8 independent (h)/(i)/(k) probes agree across the care wrapper, the private reference and the build (`probe-results.txt`, sha256 `34eeae2a…`, 8/8 AGREE): NaN outside a string → `input_invalid` exit 2; NaN inside a string evaluated; URL space → `check_invalid`; non-ASCII kept; `/robots.txt` implicit allow; `/robots.txt?x=1` decided by rules; 5000-digit status → `check_invalid`. Care only; the other three were not behaviorally probed.
5. **The v3 redesign was substantive elsewhere**: mutant distributions from receipts — v2 `{16:5, 18:8, 19:16, 20:13}` (13 meet the 20 bar), v3 `{16:6, 18:14, 19:22, 20:0}`. 13 genuine false passes closed.
6. **The (j) check's green is naming-dependent.** `control_consequence_check.py --root . --revision adab4c7 --verification .ufo/waves/round-38/verification` → exit 0, `tainted_counters=1 violations=0`, four `note:` lines calling the 20/20 v3 receipts "not a control for this verdict" (`ccc-tip.txt`, sha256 `91b45318…`). Copying one receipt to `control-…v3.json` (same bytes) → exit 1, `tainted_counters=2 violations=2` including `c2-at-3ed8e15c` (`ccc-renamed.txt`, sha256 `e4fc28d6…`). The script encodes the C2 class itself (`control_consequence_check.py:33`).
7. **C2 numbers reproduce**: `sealed_count_v3.py --revision 3ed8e15c --key-revision 99357694` → exit 0, 20/20, `toolSha256 f4d057c4…baace`, `counterSha256 28b120a5…` (`v3-rerun-build.json`, sha256 `01677dac…`). Counter hashes match every receipt; key `749ef6a6…` matches the pin.

## Verdicts

| Attacked statement | Verdict | Basis |
|---|---|---|
| "Control classes, named before any v3 control score is read as a control" (:2243) | **overstated** | True only for v3 and unverifiable from git (classes and v3 receipts share one commit; no receipt timestamps). False for the scores the boundary actually disposes (C1's 20/20s, 04:2xZ). |
| "A tool implementing all three rules is a build… not as controls" (:2250–2251) | **holds on substance, post-hoc as a disposition** | Fact 4: the tools implement the rules, so "control" would be a category error. But the seat's report calls care a control (`ctl/CtlBaseWrapper.md:1,29`), C1 declared the wrapper class a control, and QUALITY (j) (`corpus/QUALITY.md:926-928`) allows redesign/drop/exploratory, not reclassification unless the class was named beforehand — it was not (Fact 2). |
| "A tool of any of these classes meeting the predicate withdraws C2; no further redesign this round" (:2247) | **holds formally, vacuous in practice** | Classes (1)–(7) are exactly the faulty classes; the only tools that ever met (four, all rule-complete) are defined out at :2250. No correct tool can now withdraw C2. |
| Round-38 (j) check green ⇒ (j) applied | **wrong as evidence** | Fact 6: PASS→FAIL under a rename; the green is a property of file names. |
| C2 measured before/after (8/20 → 20/20) | **holds** | Fact 7; receipts and hashes match. |

## What a closure following the round-37 ruling would most likely decide

Round-37's closure refused the same merit argument — "this control does not skip the claimed work" — as "a rule change after a seat had scored". The naked words of QUALITY (j) ("unless the declaration named that class beforehand", the declaration being C1's, under which the control scored) point the same way, and v3 does not move the four tools (Fact 3), so the C1 failure survives in substance. On that strict reading: **C2 not admitted**, tool/selftest/harm standing as non-claim work.

The honest counterweight is Fact 4 plus Fact 5: the four tools are correct implementations and v3 fixes 13 real false passes, so this is not round-37's false positive (which disagreed with the contract on 6 of 9 probes). A closure that reads (j)'s "declaration" as the one under which the score is read (C2's) and treats "implements the named rules" as a definition of the target rather than a disposition would **admit C2** and route the class list and the check as defects. A strict, precedent-following closure is more likely to reject; the stake is high because C2's own text says "no further redesign this round".

## Evidence that would change the verdict

- A pre-dispatch artifact (before 04:15:37Z) naming "a tool implementing all three rules is a build" — absent from today's tree (`git grep` exit 1 at `b0ab7f6`); a prompt/brief outside the lane would flip the timing finding.
- Any of the four met tools being wrong on (h)/(i)/(k) — would make v3 unsound and force withdrawal regardless of class. My 8 probes found care correct; the other three are untested behaviorally.
- v3 separating the build from the four tools — it does not (all 20); a counter that put a correct wrapper below the build would make the redesign responsive and the class list harmless.
- An explicit ruling on which declaration QUALITY (j)'s "beforehand" refers to.
