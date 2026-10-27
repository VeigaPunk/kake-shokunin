# ReviewerC1Relabels

ATTACKS: the four label changes at B1 `8b33fd248d126b48d838af5c38bc175850f41a09` — (1) `c53_gate_truth.py` → `never met`
(pin `fd91527a`), (2) `receipt-pin-counter` pin `32754df7` → `20217f23`, (3) `crawler-identity-quote-truth-counter` →
`historical` (pin `b322ccab`), (4) `ops-debt-counter` (`c54_ops_debt.py`) → `historical` (pin `a631cc02`). Method: `--shared`
clone of the lane detached at B1 in scratch; every member run with `env -i PATH=/usr/bin:/bin HOME=… TMPDIR=<scratch>
LANG=C.UTF-8 python3 -B <path> …` (the A3/A2 parse of the row's Entry command), cwd = clone, `--revision` varied; plus the
frozen counter `c60_gate_status.py` v1 (blob equal at `1ea3059` and B1) run over all 28 members at B1. Evidence in
`ReviewerC1Relabels.files/` (29 files).

## RUNS:

1. **Frozen `c60_gate_status.py` v1 at B1** (`--work` scratch, `--jobs 4`): exit **0**, `members=28 mismatches=0
   scores_held=3 met=True` (`.files/c60_gate_status.at-B1.txt`). All four attacked members observed by the counter with the
   expected e_T/e_P: c53 never-met e_T=1, e_P(fd91527a)=1; c57pins historical e_T=1, e_P(20217f23)=0; crawler-identity
   historical e_T=1, e_P(b322ccab)=0; ops-debt historical e_T=1, e_P(a631cc02)=0. C1's frozen predicate holds at B1.
2. **c53 "never met" swept over EVERY committed revision**: all 369 commits reachable from any ref (366 in HEAD ancestry +
   round-53 preservation branches `958f46d`/`3ed0f7d` + post-B1 w2 dispatch commit `45f46fb`), each run with its own
   committed script blob (exactly one blob `63bd9cfd` ever exists — script never changed): **0 green**, every run
   `gate-truth 2/7 met=False` (L1/L2/L3/R1/R2 fail). Script `.files/c53-nevergreen-sweep.sh`; key outputs
   `.files/c53_gate_truth.at-{fd91527a,97cdc122,8b33fd24,45f46fb2}.txt`. No committed tree was ever green; the only green is
   the selftest's in-memory fixture. Pin `fd91527a` is a strict ancestor, member present there, exit 1 — A5 satisfied.
3. **c57_receipt_pins pin change**: exit **1** at old pin `32754df7` with exactly the Kind text's terms `new_receipts=0
   scorecard_pin=0`; exit **0** at `20217f23` (`new_receipts=3 scorecard_pin=1 met=True`); exit 1 at `31b61a4d`
   (`new_receipts=2 new_unpinned=1`) — the only commit between the two pins, so `20217f23` is genuinely the **first** green;
   exit 1 at `32754df7~1`, `4cb225fb` (r56), `1ae8de5d` (r52), base, B1 — no earlier green. `git diff 31b61a4d 20217f23`:
   `after-c1-receipt-pins.txt` went `pending` → real body + `tip:` line, so "the commit that landed the third round-57
   after-receipt" is accurate. Mechanism of "red on later trees" reproduced via module `measure()` notes
   (`.files/c57-receipt-pins.notes.txt`): at later tips `scripts/id_resolver.py differs between the tip and
   countersFrozenAt` → measured_rev=None → all three after-receipts fail → Kind text's "frozen file set includes the
   round-57 resolver and receipts" is a fair summary. Outputs `.files/c57_receipt_pins.at-*.txt`.
4. **crawler-identity (round-59 `c59_quote_truth.py`)**: 9/9 exit 0 at pin `b322ccab`, at base, and at all three pre-B1
   commits (`b3b9e29`, `1ea3059`, `81db050`); exit **1** at B1 (6/9). Flip lands exactly at B1 — the commit that appends
   S427–S429. Pin provenance: `b322ccab` is round-59 T0/measured (SCORECARD L4416, L4428). Script blob constant
   (`d2182242`) across pin/base/B1. BUT the B1 red is not only the disclosed C8 — see FINDINGS F1.
5. **ops-debt (`c54_ops_debt.py`)**: exit 0 at pin `a631cc02` (round-54 measured, SCORECARD L4284) and at **all 55 commits**
   in `(a631cc02..base]` plus r54 tip and every round 55–59 measured revision (`red_in_interval=0`); exit 1 at r54 base
   `68228b2d` (pre-measured, outside the claimed green interval, irrelevant to A5); exit **1** at B1 with
   `registry=absent manifest=present` — code line 69 requires the c53 row's Kind cell `cells[1] == "gate"` literally, the
   disclosed coupling. Claim "green at a631cc02 and on every tree up to the round-60 base" verified over every commit.
6. Pin provenance for c53: fleet-root `.ufo/reports/round-53/kake.md` L23 "measured on the source-row commit
   `fd91527a…`" — the Kind text's "its round-53 measured revision" is grounded.

## FINDINGS:

| Sev | Target | Issue | Evidence | Fix |
|---|---|---|---|---|
| medium | `SKILL.md:1309` (crawler-identity-quote-truth-counter Kind cell) | "red from round 60 on by design — C8 … round 60 appends S427-S429" is incomplete: at B1 the counter fails **C5 and C7 too**, and those are NOT the disclosed mirror mechanism. C5: the new `[r60-correction 2026-10-27]` line in the S426 entry `corpus/knowledge/googlebot-verification.md:40` double-quotes S428's wording ("Because the fetch was requested by a user, these fetchers generally ignore…"), which round-59 C5 judges as every-quoted-span-vs-own-row-body against S426's retained body → not a substring. C7: the census-validate receipt's scratch entry predates the append ("S426: validated scratch entry differs from the landed entry"). Consequence: reverting S427–S429 would NOT restore green (C5/C7 remain); only C8's red is "by design". `w1/CriticD1Collision.md` proved C8 alone on a sim rows-append and never ran the real correction block, and the row cites it as the complete cause. | `python3 -B .ufo/waves/round-59/c59_quote_truth.py --root . --revision 8b33fd24…` → 6/9, `C5 FAIL - S426: entry line 40 quotes 'Because the fetch was requested by a use'… not a raw substring of the retained body`, `C7 FAIL - S426: validated scratch entry differs…`, `C8 FAIL - registry rows 167 != mirror rows 162 + 2` (`.files/c59_quote_truth.at-8b33fd24.txt`); `git diff 97cdc122 8b33fd24 -- corpus/knowledge/googlebot-verification.md` (`.files/googlebot-verification.r60-append.diff`) | Extend the Kind cell to disclose the C5/C7 causes (the correction block's cross-row quote and the validate-receipt entry mismatch); a counter v2 may not loosen, so the fix is disclosure in the Kind cell/lesson, not code. Label itself (historical, e_T=1, e_P=0 at `b322ccab`) stays honest — no predicate impact. |
| low | `SKILL.md:213` (c53 row, Verdict map cell) | Cell claims `64=usage`; the counter uses stock argparse and exits **2** on usage error. `w1/ExecC1Data53.md` explicitly flagged this and drafted the replacement row with the corrected map (0/1/2, "no 64"), but the landed relabel row kept the known-false `64=usage`. Outside C1's structural check (only `0=`/`1=` required) and declared out of counter scope — ledger-accuracy only. | `python3 -B .ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py --no-such-flag` → exit 2, `error: unrecognized arguments` (`.files/c53-usage-badflag-exit2.txt`); row text `.files/SKILL-row213-c53.txt` | Drop `64=usage` from the cell (map is 0/1/2). |

Residual risk / verification gaps: the full-counter `met=True` at B1 includes `c57_idresolver_gate` run with `--fleet`
(non-hermetic, reads live sibling registries — disclosed in SKILL.md); sibling changes could flip it independently of these
labels. c57pins/c54ops/c59qt were verified at e_T, e_P, and flip-window/sample revisions, not at every post-pin tree (the
A5 contract does not require it); the c53 never-green claim is verified at 100% of committed revisions. The C5 failure in
F1 was reproduced once per revision run; it is deterministic (committed bytes only).

No pacman/tool installs; no lane mutation (only this report and `ReviewerC1Relabels.files/`); scratch
`/fast/scratch/hyaku/kake-r60/ReviewerC1Relabels/` deleted after evidence copy.

VERDICT: all four relabels are observation-accurate and C1's frozen predicate holds at B1 (28/0/3, exit 0; c53 green on 0
of 369 commits; `20217f23` is the correct first-green pin with accurate Kind text); two Kind-text defects —
crawler-identity's "by design" cause omits that C5/C7 also fail because the r60 correction block quotes S428 wording inside
the S426 entry, and the c53 row still carries the known-false `64=usage` verdict-map claim w1 proposed to fix.
