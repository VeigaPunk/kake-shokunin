# Round 72 — lessons (kake, attempt 1)

Base `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1` (lane master at round open). Frozen contract
`.ufo/waves/round-72/contract.md` at freeze `a19d38ea` (predicates, base receipts and the C2 counter frozen before any
seat ran). Wave `w1`: 15 seats, one v1 wave, band 8–16 (scout 3, connector 1, executor 2, scribe 2, reviewer 2,
critic 2, mutation-tester 1, sentinel 1, revenger 1; attack share 6/15 = 40 %; the L1 held the planner role). All 15
seats settled (`.ufo/waves/round-72/w1-results.json`); none dead.

Claims: C1 calibration (lowest owned axis, score 2) and C2 operability (score 10, HOLD).

## Claims and verdicts

| Claim | Predicate (frozen) | Before (base `3c68645a`) | After (measured tip `5013c0ee`) | Verdict |
|---|---|---|---|---|
| C1 calibration | c66 gate-status `agreement == 25`, `evaluated == 28`, only `c56_selftally` changes | `agreement=24 mismatches=4 evaluated=28` (`controls/c1-base.txt`, exit 0) | `agreement=25 mismatches=3 evaluated=28`, exit 0; the only member whose mismatch set changed is c56 (`controls/c1-tip-final.txt`) | met on the frozen predicate (calibration HOLD 2; no score move) |
| C2 operability | c72 selftest 11/11; J3 control c71 exit 0 and c72 exit 1; base `cc6b4e0b` exit 1; tip exit 0 | selftest 11/11; base-red exit 1 (`controls/c2-base-red.txt`) | tip exit 0, `findings=[]` (`controls/c2-tip-final.txt`); J3 control `c71_exit=0`, `c72_exit=1` (`controls/c2-j3-control-r3.txt`) | met on the frozen predicate (operability HOLD 10); residual holes routed |

Both verdicts are on the frozen predicates. Scores stay operability 10, freshness 10, calibration 2 (HOLD; no scalar move).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| M1 adoption residue — the round-70 adopted entry `corpus/knowledge/crux-bigquery-origin-membership.md` cites three staged package ids (S303, S304, S352) that no kake registry row holds; the id resolver reports `ids_cited=121 ids_resolved=118 dangling=3`, and gates c57, c58, c59 fail their real-lane leg on exactly this | `.ufo/waves/round-72/w1/ScoutDangling.md`; the resolver output at base; `corpus/knowledge/gate-status-ledger.md` § r72 | none — the round-70 closure did not run `scripts/id_resolver.py --root` at the adopting tip; the census and the append guard do not read body ids | routed to the operator (L0, kake round-72 line). Not repaired in-lane: an in-place rewrite is a changed finding under the append guard, and registering staged ids as lane ids breaks the next-unused rule. Candidate QUALITY criterion once a ruling lands: an adoption round runs the id resolver at its tip and reports the count |
| M2 vacuous counter — the round-71 C2 counter `.ufo/waves/round-71/c71_tmp.py` accepts a phrase-only annotation on a command-bearing `/tmp` line and exits 0 | `.ufo/waves/round-72/controls/c2-j3-control-r3.txt` (`c71_exit=0` on the J3 control); round-71 lesson M5 | none — the round-71 counter was frozen after a do-nothing control only; M5 named the gap but no control was built against it | `c72_tmp_v2.py` classifies a command-bearing `/tmp` token as a command finding even when annotated: the same J3 line gives `c71_exit=0` and `c72_exit=1`; selftest 11/11 (`controls/c2-selftest.txt`). Shown able to fail: the J3 control. Residual holes, routed (below) |
| M3 pre-freeze diagnosis — the L1 ran the frozen gate family at base to locate red gates before the claims were frozen, so the claims were chosen after seeing diagnostic greens and reds | `.ufo/waves/round-72/contract.md` § Disclosure; these runs are not controls | none — the freeze protocol has no field for pre-freeze diagnosis | disclosed in the contract and the report; the non-author closure weighs C1 and C2 on their frozen predicates |
| M4 harness exit masking — the J3 control script ran under `set -e`, so a counter exit 1 aborted before the `c72_exit=` line; the receipt needed an out-of-script wrapper (ReviewerC2 C3, CriticCoupling F1, SentinelC2 B1). A `set -u` fix then made the script exit 0 when both counters were unevaluable (SentinelC2 R1) | `controls/c2-j3-control.txt` (committed, set -e: no `c72_exit` line), `controls/c2-j3-control-r2` (never committed) | none — the first harness was run only on the happy path | harness keeps `set -e`, captures each counter exit with `|| rc=$?`, and exits with the c72 code; checked: with the tools missing the script exits 127, not 0; receipt `controls/c2-j3-control-r3.txt` |

## Gate

- **Admit — c56 relabel (C1).** The Kind cell now states what the gate observed: green at its r56 pin
  (`controls/c56-pin-linux.txt`, exit 0, tally 10/10) and red at the lane base only because the counter's `scripts/fixtures`
  tree gained four `quote-class` files after the pin. The first draft of this cell named six changed tools; that was wrong
  (ReviewerC1: the ten audited script hashes are identical pin→base; CriticClaims E12: restoring the fixture tree turns the
  tip green). The cell and a tagged correction in the ledger now say so. The c66 label rule (historical needs an ancestor
  40-hex pin and a green pin run; RevengerLabel) is satisfied and a green tip under `historical` is never counted as agreement.
- **Reject — rewriting the adopted entry in place to drop S303, S304, S352.** The append-only guard reads a replaced line as
  a changed finding, so no in-place correction can land. Routed (M1).
- **Reject — registering S303, S304, S352 as kake registry rows.** Adopted ids are next-unused (CORPUS.md rule 2; round-70
  `S438`); the staged ids belong to another campaign's numbering. Registration would turn the resolver green while the body
  still cites staged ids. Routed (M1).
- **Admit — S439 registry row** (Git gitcli, tier A, opened 2026-11-03). Its located quote is a single-line raw substring of
  the retained bytes, `.ufo/waves/round-72/sources/gitcli.html` (sha256 `4e1ea3a5…a02714a1e`): counts 1, 1 and 1 for Q1, Q2, Q3
  (`w1/ScoutCorpusDelta.md`), receipt `sources/receipts.json`. A two-line quote was first drafted and rejected: the raw bytes
  break the sentence across a line, so grep finds 0 (CriticCoupling F2).
- **Reject — "all gates green" as the round's outcome.** c57, c58 and c59 stay live and red (M1); the ledger says so.
- **Reject — treating the round-71 counter as a control to keep.** Frozen bytes are not edited; c72 is a new numbered file.
- **Reject — the first c2-j3-control receipt as C2 evidence.** It came from a script that cannot print the c72 exit (M4).
  The corrected receipt `c2-j3-control-r3.txt` replaces it as evidence; the earlier receipt stays as history.

Spot-check: the non-author closure is owed. The L1 sample is 2 admits (c56 relabel, S439) and 3 rejects (in-place rewrite,
registration of staged ids, all-green reading).

## Routed to round 73 (defects found by the attack seats; not fixed here; the frozen counter is not edited)

- C2 counter, command vocabulary: the frozen 17-word verb list (`COMMAND_WORDS`) misses command-form lines whose verb is
  outside it (`rm`, `sed`, `tee`, `head`, …); such a line annotated with the phrase passes (ReviewerC2 finding 2, commit
  `193fa3d5` in its scratch, met=True exit 0). Fix: a new numbered counter.
- C2 counter, `${TMPDIR:-/tmp}` fallback repoint escapes both regexes (ReviewerC2 finding 1 — the F2 class the docstring
  claims to kill).
- C2 counter, symlinked SKILL.md: `git show <rev>:SKILL.md` on a mode-120000 blob returns the link text; a commit making
  SKILL.md a symlink to `/dev/null` gives `met=True` (SentinelC2 R2).
- C2 counter, phrase constant: `PHRASE` is not pinned by any leg (MutC2 M-f, M-h survive); a counter that prints the phrase
  as a constant is not a control of the phrase.
- C2 counter, two basename-collision shapes redden legitimate dated-absence rows (ReviewerC2 finding 3; note).
- c66 counter: exit 0 at base with the three host-bound reds present; claims read `agreement`, never the exit (CriticClaims A2).
- L0 (operator): the dangling-id ruling for M1 (`.ufo/l0-questions.md`, kake round-72 line).

## Sourced claims

- **C2 rests on S439** (Git gitcli: `--end-of-options` ends option parsing before a revision argument; the counter passes the
  revision after it to `git show`, so a crafted revision cannot be read as an option — round-71 M7).
- **C1 rests on no web source.** Its evidence is the lane's own receipts and the c66 counter's documented label rule.
