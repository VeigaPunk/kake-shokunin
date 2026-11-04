## Round 90 — measured claims

Base `209027f49959e2e2f0e16867a90a7bb38bbcd3f4`; freeze `4ee62b18fec15af45654a9c8f8d5e7938d2bb796`
(`.ufo/waves/round-90/freeze.md`); C2 carrier (gate commit) `7f6c68f10fbf4caca3912d6e23fa6eed6413857d`;
C1 carrier `e50c95660a9651fd9abe45119abab0bc3e8aaa56`; receipts commit `79e1aac24654e01dc0559eb3beb8abbe61ec73a8`.
Counters: `.ufo/waves/round-90/c90_defects.py` (sha256 `462224f6…5d519b`) and `.ufo/waves/round-90/c90_gate.py`
(sha256 `703b0058…cfa`), population pins `.ufo/waves/round-90/frozen/c2-population.sha256` (sha256 `a57f8985…850c`);
counter and pin bytes unchanged from the freeze to `79e1aac2` (`git diff --stat 4ee62b18 79e1aac2` over the three
paths is empty). Wave `w1`: one v1 wave, 13 seats (scout 2, executor 4, mutation-tester 2, reviewer 2, critic 1,
scribe 1, connector 1; attack share 5/13), dispatched `2026-11-04T19:14:24` after the freeze commit
(`.ufo/waves/round-90/w1-spec.json`, `w1.ready.dispatched`). Scores held: operability 10 HOLD, freshness 10 HOLD,
calibration 2 HOLD.

| Claim | Axis / score delta | Before → after | Counting command | Evidence / author verdict |
|---|---|---|---|---|
| C1 the three round-89 spot-check defects (D89-1 lane-root scratch, D89-2 unreceipted C1 statement at `f62e7954`, D89-3 S463 scope vs construction use) close | calibration 2→2 HOLD, lowest owned | base `209027f4`: `C1v90 revision=209027f49959e2e2f0e16867a90a7bb38bbcd3f4 items=3 open=3 closed=0 met=false`, exit 1 (`.ufo/waves/round-90/controls/base-c1.txt`) → carrier `e50c9566`: `C1v90 revision=e50c95660a9651fd9abe45119abab0bc3e8aaa56 items=3 open=0 closed=3 met=true`, exit 0 (`.ufo/waves/round-90/controls/after-c1-carrier.txt`) | `python3 -B .ufo/waves/round-90/c90_defects.py --root . --revision <REV> --work <scratch>` | measured met; pre-freeze controls `controls/ctl-c1.txt` (do-nothing `open=3`, seven forgeries each `met=false`, positive fixture `open=0 closed=3 met=true`) and `controls/ctl-c1-v0-before-parse-fix.txt` (positive fixture `open=1 closed=2 met=false` before the parse fix). Re-read at `79e1aac2`: `open=0 closed=3 met=true`, exit 0 (`w1/ScribeLedger/receipts/c1-at-79e1aac2.txt`). D1 carries one live working-tree conjunct, so the reading is not revision-bound |
| C2 `scripts/cache_key_conformance.py` refuses the 57-subject non-conforming population and admits the 4 conforming subjects under nonce renaming (capability) | operability 10→10 HOLD (capability) | base `209027f4`: `C2v90 revision=209027f49959e2e2f0e16867a90a7bb38bbcd3f4 gate=absent positives=0/4 negatives_refused=0/57 false_admits=0 errors=0 anti_table=n/a population=n/a seed=2087649613 met=false`, exit 1 (`.ufo/waves/round-90/controls/base-c2.txt`) → carrier `7f6c68f1`: `C2v90 revision=7f6c68f10fbf4caca3912d6e23fa6eed6413857d gate=present positives=4/4 negatives_refused=57/57 false_admits=0 errors=0 anti_table=ok population=ok seed=923161196 met=true`, exit 0 (`.ufo/waves/round-90/controls/after-c2-carrier.txt`) | `python3 -B .ufo/waves/round-90/c90_gate.py --root . --revision <REV> --work <scratch>` | measured met, and the counter's `met` alone is forgeable: a 16-line gate with no conformance logic that strips the nonce trailer, hashes the subject and admits the first four pinned hashes read at run time reaches `positives=4/4 negatives_refused=57/57 … anti_table=ok population=ok … met=true`, exit 0 (`w1/ScribeLedger/receipts/forgery-c2-pin-reading-gate.txt`, gate `forgery-pin-reading-gate.py`). The behavioural support is the per-subject gate lines in `after-c2-carrier.txt` (`clauses=6/6 hand=70/70 generated=120/120 sandbox=ok` on the four positives; every negative `met=false`) plus two held-out subjects outside the pins: comment-stripped `scripts/cache_key.py` `clauses=6/6 … met=true` exit 0, value HTAB not trimmed `clauses=5/6 hand=68/70 … met=false` exit 1 (`w1/ScribeLedger/receipts/heldout-*.txt`). Re-read at `79e1aac2`: `positives=4/4 negatives_refused=57/57 … seed=970713380 met=true`, exit 0 (`w1/ScribeLedger/receipts/c2-at-79e1aac2.txt`) |

Pre-freeze C2 controls (`.ufo/waves/round-90/controls/ctl-c2.txt`): do-nothing `gate=absent … met=false`; blanket-refuse
gate `positives=0/4 negatives_refused=57/57 … met=false`; blanket-admit gate `positives=4/4 negatives_refused=0/57
false_admits=57 … met=false`; hash-table and name-table gates each `positives=4/4 negatives_refused=0/57 false_admits=57
… met=false`; all exit 1. No control embeds a subject hash or stem in gate source, so the `anti_table` conjunct has no
able-to-fail witness in that receipt. Registry 202 → 205 rows (S466, S467, S468), knowledge entries 77 → 78, at
`209027f4` → `e50c9566` (`git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`;
`git ls-tree -r --name-only <rev> -- corpus/knowledge | grep -c '\.md$'`). Census `validate --root … kake` exit 0 before
(26 × W04, `controls/census-before.txt`) and after (29 × W04, `controls/census-after.txt`); the three new W04 are
S466–S468, whose plain-text URLs are shared with earlier rows across scopes. No owned axis is claimed improved.

### Demonstrated repertoire — round 90

| Capability | What it can now do | Evidence | First-working round |
|---|---|---|---|
| Behavioural cache-key conformance gate | Given a stdin/stdout key-constructor script, decide whether it implements `.ufo/waves/round-89/c2-contract.md`: six contract clauses scored over 70 hand cases and 120 seeded generated cases (seed printed), the candidate run under an execution-time audit-hook sandbox (a delegating or oracle-importing subject dies with `sandbox=violation`), and an unscored `advisory=` line for inputs the contract leaves open (non-UTF-8 input, raw control characters in JSON, NUL in a value); decides contract conformance only, not storability, reuse, freshness or what any cache does | `scripts/cache_key_conformance.py` (`7f6c68f1`, 471 lines); `.ufo/waves/round-90/controls/after-c2-carrier.txt`; `corpus/knowledge/cache-key-conformance-gate.md`; S466, S467, S468 | 90 (demonstrated; the round counter's `met` is forgeable by a pin-reading gate, so the capability rests on the per-subject lines and held-out subjects, not on the counter verdict) |

### Move log (round 90)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 90 | calibration (HOLD 2) | `open=3 closed=0 met=false` at `209027f4`; inherited `baseclean.out` untracked at the lane root, round-89 C1 statement at `f62e7954` unreceipted, S463 scope cell against its construction use | `open=0 closed=3 met=true` at `e50c9566`; file relocated byte-exact to `.ufo/waves/round-90/inherited/baseclean.out`, appended correction tails receipted by the frozen round-89 counter re-run at `f62e7954` (`controls/r89-c1-at-f62e7954.txt`: `open=5 closed=1`, only item E closed), S467 supersedes S463 by a new row | `.ufo/waves/round-90/c90_defects.py`, `controls/base-c1.txt` → `controls/after-c1-carrier.txt`, `controls/ctl-c1.txt`, `corpus/lessons/round-90.md` §Gate, §Registry, §Mistakes |
| 90 | operability (HOLD 10) | no conformance gate; the round-89 counter admits 7 of 15 ExecControls stubs (`.ufo/waves/round-89/w1/ExecControls/scoring-receipt.txt`, 7 `cand_met=true` lines) | `positives=4/4 negatives_refused=57/57 false_admits=0 errors=0 met=true` at `7f6c68f1`; round-89 MutKey M37 (filed as equivalent) refused `clauses=5/6 hand=69/70` | `scripts/cache_key_conformance.py`, `.ufo/waves/round-90/c90_gate.py`, `controls/base-c2.txt` → `controls/after-c2-carrier.txt`, `controls/ctl-c2.txt` |

### Planned — after round 90

Outside closure owns admission and the admit/reject spot-check of `corpus/lessons/round-90.md` §Gate. Routed
contract gaps, each a contract-revision decision and not a gate change: R90-1 the contract does not say what non-UTF-8
input does (advisory `utf8-required`); R90-2 NUL in a field value is kept by the candidate while S466 says a recipient
must reject it or replace it with SP (advisory `nul-in-value`); R90-3 contract example 5 says the separators are sent raw,
against RFC 8259 §7 (S468; advisory `raw-control`); R90-4 the key omits the request method that RFC 9111 §2 (S467)
composes it from (adapter limit). Instrument item for the next C2-shaped counter, from this wave: the frozen
`c90_gate.py` accepts a pin-reading gate (`w1/ScribeLedger/receipts/forgery-c2-pin-reading-gate.txt`); a successor must
withhold the pins and labels from the gate's reachable tree, make the nonce non-strippable, and score at least one
held-out subject per label; the frozen round-90 counter is not repaired after scoring. Carried: RC-1…RC-10 for the
frozen round-89 C1 counter; the round-89 L0 questions. Frontier stays open: cache-key storage, revalidation,
freshness and serving; browser Vary and Pragma behaviour; the D84-2/3 and literal L2-planner items.
