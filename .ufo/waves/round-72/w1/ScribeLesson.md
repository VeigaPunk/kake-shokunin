draft_lines=68 report_tail_lines=64 total_lines=132

# Round 72 — lesson body draft (ScribeLesson)

Author-side text draft for the L1 to integrate into `corpus/lessons/round-72.md`. Not landed, not
committed; this seat wrote no lane tracked file. Frozen contract `.ufo/waves/round-72/contract.md` at
`a19d38ea`; base `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`. Tip numbers are placeholders
(`TIP_C1_AGREEMENT`, `TIP_C1_MISMATCHES`, `TIP_C2_EXIT`) for the L1 to fill from the landed tip; the
verdict cells are the L1's `TIP_C1_VERDICT` / `TIP_C2_VERDICT` placeholders.

## Claims and verdicts

| Claim | Predicate (frozen) | Before (base) | After (tip) | Verdict |
|---|---|---|---|---|
| C1 calibration | "C1 is met iff, over the frozen counter `.ufo/waves/round-66/c66_gate_status_hostportable.py` run at the measured tip, `agreement == 25`, `evaluated == 28`, and the only member whose per-member label agreement changed from base to tip is `c56_selftally.py`, which moves from disagreement to agreement." | `agreement=24 mismatches=4 evaluated=28 members=28 structural=0 scores_held=3/3 met=True`, exit 0 (`controls/c1-base.txt`, re-measured by this seat) | `agreement=TIP_C1_AGREEMENT mismatches=TIP_C1_MISMATCHES evaluated=28` | TIP_C1_VERDICT |
| C2 operability | "C2 is met iff `c72_tmp_v2.py --selftest` exits 0 with `11/11`, `c71_tmp.py` exits 0 and `c72_tmp_v2.py` exits 1 on the J3 control commit that `.ufo/waves/round-72/controls/j3-control.sh` builds (a scratch clone of base tip `3c68645a` with line 27 replaced by a command-form `cp` line carrying the phrase; the commit hash differs per run and is printed by the script; the script is the frozen artifact), the counter exits 1 at the round-71 base `cc6b4e0b8c35e72dfb02c6184b847f68c1262153` (red-before), and exits 0 at the measured tip." | selftest `11/11` exit 0; red-before `cc6b4e0b` exit 1 (7 findings); base `3c68645a` exit 0; J3 control: c71 exit 0, c72 exit 1 (`controls/c2-selftest.txt`, `controls/c2-base-red.txt`, `controls/c2-base-head.txt`, `controls/c2-j3-control.txt`) | `c72_tmp_v2.py` exit TIP_C2_EXIT | TIP_C2_VERDICT |

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| M1 adoption residue — the round-70 adopted entry `corpus/knowledge/crux-bigquery-origin-membership.md` cites staged package ids S303, S304 and S352, and no kake registry row holds them; the lane's own id resolver reports `ids_cited=121 ids_resolved=118 dangling=3`, all three cited by that one file | `scripts/id_resolver.py --root <lane> --revision 3c68645a` (this seat, exit 1: three `DANGLING` lines, `dangling=3 owned_elsewhere=3 unowned=0`); `.ufo/waves/round-72/w1/ScoutDangling.md` (seat report, L0 question draft); the resolver's own summary | none — the round-70 closure did not run the id resolver on the adopted entry, and neither the source census nor the append guard reads ids cited in a knowledge file's prose (the census validates registry rows; the guard validates file bytes) | routed to the operator (L0) with the rewrite-by-document question: may the entry's staged-id citations be re-grounded on the lane's own document-derived row (the r70 renumber map was `S352 → S438`), or must the entry be left as it stands and the resolver's citation rule gain a stated exclusion for ids the entry itself marks as staged and refused? Registering S303/S304/S352 as lane ids is not available (see the Gate) |
| M2 vacuous counter — the round-71 C2 counter `.ufo/waves/round-71/c71_tmp.py` accepts a phrase-only annotation on a command-bearing `/tmp` line and exits 0, so the round-71 C2 verdict passed on a line whose command status no instrument read | `.ufo/waves/round-72/controls/c2-j3-control.txt` (`c71_exit=0`; the c72 leg on the same control prints `command_findings=1 findings=[(27, 0, 1, 0)] met=False`); the round-71 lesson M5 | none — the round-71 counter was frozen after a do-nothing control only; M5 named the gap and routed it to round 72, but no control was built against it | `c72_tmp_v2.py` rejects the J3 control: the c72 leg of the same receipt exits 1 on the same commit, and `c72_tmp_v2.py --selftest` is 11/11 exit 0 (`controls/c2-selftest.txt`). Read the receipt literally: the token `c72_exit=1` the contract names is **not** in the frozen receipt — the control script runs under `set -eu`, so it aborts at the failing c72 invocation and the receipt carries the script's own status `j3_script_exit=1` instead (see the seat report) |
| M3 pre-freeze diagnosis — before the contract was frozen, the L1 ran the frozen gate family at the base revision to locate the lane's red gates and prototyped an in-scratch repair of the adopted CrUX entry, so the claims were chosen after seeing diagnostic receipts; the prototype was discarded | `.ufo/waves/round-72/contract.md` § Disclosure (pre-freeze diagnosis); the diagnostic runs are not controls and carry no receipt | none — the freeze protocol has no field for pre-freeze diagnosis; only the contract's disclosure carries it | disclosed in the contract and in the report; the non-author closure is asked to weigh C1 and C2 on their frozen predicates, not on the diagnostic greens, and to treat the discarded prototype as an unreceipted non-result |

## Gate

Candidates considered this round, with decisions:

- **Admit — the c56 row relabel (C1).** The `selftest-tally-counter` row's Kind cell now states what the
  gate observed at its pin and at the tip: green at the round-56 measured revision `4cb225fb`
  (`controls/c56-pin-linux.txt`, exit 0, tally 10/10) and red on this Linux host at the lane base, where six
  audited tools have changed since the frozen base (`controls/c56-tip-linux.txt`, `tally_mismatches=6`, every
  row `tool_changed`, observed equal to claim). The relabel is one cell of one row, the pin is a 40-hex
  ancestor of the measured revision, and the counter's own label rule turns the Kind cell's word `historical`
  into the label it then re-derives. Reason: the label was wrong, not the gate — the r67 Windows-host mechanism
  does not carry to this host, where the gate runs and reads real content.
- **Reject — rewriting the adopted entry in place (M1).** Reason: the append-only guard reads an in-place
  replacement as a changed finding — replacing the entry's staged-id sentence with a lane-row sentence is
  `changed corpus/knowledge/crux-bigquery-origin-membership.md` under `scripts/append_guard.py`, exit 1
  (this seat's scratch probe). A replacement of a finding is not an append; the entry stays as written and the
  question about re-grounding its citations goes to the operator.
- **Reject — registering the staged ids S303, S304 and S352 as lane ids (M1).** Reason: the id rule —
  `CORPUS.md` §SOURCES.md Shape, "id — `S` + 3 or more digits, the next unused; never reused" — and the
  round-70 precedent that followed it (`S352 → S438`, id follows the document). S303/S304/S352 are staged-package
  numbers already in use in sibling registries (the resolver names them as owned elsewhere), and S303/S304 are
  sources this lane refused in rounds 52, 53 and 70 as never opened here; registering them would mint rows for
  sources the lane holds no opening receipt for.
- **Admit — the S439 registry row (gitcli).** Opened this round; the retained body
  `.ufo/waves/round-72/sources/gitcli.html` (sha256 `4e1ea3a5…`) carries the located quote, the row's id is the
  lane's next unused id (max registry id at base is S438), and the census stays green (exit 0 before and after).
  Reason: C2's `--end-of-options` mitigation for revision arguments (round-71 M7) rests on it, and the frontier
  rule needs one claim on a row opened this round.
- **Reject — the "all gates green" reading.** Reason: c57, c58 and c59 remain live and red on this host, each
  failing its real-lane leg on exactly the three dangling ids of M1 (`ids_cited=121 ids_resolved=118
  dangling=3`). No claim is made that the lane's gate family is green; the cause is routed, not repaired here.

## Sourced claims

- **C2 rests on S439** (git-scm gitcli, tier A, opened 2026-11-03). The located quote is in
  `.ufo/waves/round-72/sources/gitcli.html` (sha256 `4e1ea3a5…`, 51,306 bytes): `--` disambiguates revisions
  and paths in some commands, so it cannot separate options from revisions, and `--end-of-options` is the
  option that ends option parsing — the mitigation the round-71 M7 residual asked for. The row itself is
  drafted by `ScribeSources` and is not yet in the registry at this writing.
- **C1 rests on no new web source.** The relabel is re-adjudication of the lane's own gate against its own
  committed bytes, with the pin and tip receipts cited above.

<!-- ===== end of lesson body draft; the L1 integrates everything above this line ===== -->

## Seat report — evidence commands and exit codes (all read-only; no lane tracked file written)

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root . --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1 --jobs 6` (run in the lane root, `TMPDIR` = this seat's scratch) | 0 | `members=28 evaluated=28 mismatches=4 structural=0 agreement=24 scores_held=3/3 met=True` — byte-identical to `controls/c1-base.txt` |
| 2 | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --selftest` | 0 | `C2v2 selftest 11/11` |
| 3 | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane <lane> --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1` | 0 | `brace_findings=0 command_findings=0 prose_findings=0 removed=7 added=7 guard=ok met=True` — matches `controls/c2-base-head.txt` |
| 4 | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane <lane> --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153` | 1 | `command_findings=2 prose_findings=5`, 7 findings at lines 27/95/227/356/359/463/464, `met=False` — matches `controls/c2-base-red.txt` |
| 5 | `sh .ufo/waves/round-72/controls/j3-control.sh` (frozen script, `HYAKU_SCRATCH` = this seat's scratch) | 1 | `J3_CONTROL_COMMIT=d313d30b…`; c71 leg `met=True` (`c71_exit=0`); c72 leg `command_findings=1 findings=[(27, 0, 1, 0)] met=False`. Same shape as the frozen receipt `controls/c2-j3-control.txt` (its commit `bbf0c072…`) |
| 6 | `python3 -B scripts/id_resolver.py --root <lane> --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1 --fleet /home/vgpnk/Projects/shokunin` | 1 | three `DANGLING` lines (S303, S304, S352), each `cited-by=corpus/knowledge/crux-bigquery-origin-membership.md`; `ids_cited=121 ids_resolved=118 dangling=3 owned_elsewhere=3 unowned=0` |
| 7 | `python3 -B scripts/append_guard.py --root <scratch clone> --base 3c68645a… --revision <probe> --scope corpus/knowledge/crux-bigquery-origin-membership.md` (probe = one line of that entry replaced in place) | 1 | `changed corpus/knowledge/crux-bigquery-origin-membership.md` — an in-place rewrite is a changed finding, so it is rejected as a repair |
| 8 | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | 0 | 16 `W04` duplicate-url warnings, 0 `E*`; last line `kake ok …/kake-shokunin/corpus/SOURCES.md`; 176 registry rows at base |
| 9 | `sha256sum .ufo/waves/round-72/sources/gitcli.html` | 0 | `4e1ea3a5951e10f5c31157d1b03e0938d9b09130c5db099aa5baec6a02714a1e` (51,306 bytes); identical to the blob at freeze `a19d38ea` |
| 10 | `grep -F -c` of the three S439 quotes in that file | 0 (each) | each quote count = 1 |
| 11 | `git merge-base --is-ancestor 4cb225fb032b04166fb0232bc98a7bcce72675ec 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1` | 0 | the c56 pin is an ancestor of the base, so the `historical` label's pin leg is satisfiable |
| 12 | `git show 3c68645a:corpus/SOURCES.md \| grep -c S439` | 1 | 0 — S439 is absent from the base registry; max registry id at base is S438 |
| 13 | `git diff a19d38ea -- .ufo/waves/round-72/c72_tmp_v2.py` | 0 | empty — the frozen counter's bytes are unchanged (`sha256 af2f0c9c…`) |

## Counterexample / findings for the judge

1. **The contract's C2 receipt label names a token the receipt does not contain.** Contract line 55 says the
   receipt `controls/c2-j3-control.txt` shows "`c71_exit=0` and `c72_exit=1`". The frozen receipt contains
   `c71_exit=0` (line 4) and `j3_script_exit=1` (last line) and **no** `c72_exit=` token at all
   (`git show a19d38ea:.ufo/waves/round-72/controls/c2-j3-control.txt | grep -c c72_exit` → 0). Cause: the
   frozen `j3-control.sh` runs under `set -eu`, so the script aborts at the failing c72 invocation before its
   own `echo "c72_exit=$?"` line runs; my re-run of the same frozen script (exit 1) likewise prints the c72
   verdict line and no `c72_exit=`. The substantive claim is unaffected — the receipt's c72 leg prints
   `command_findings=1 … met=False` and the script's exit status is 1 — but the receipt label in the contract
   and in the seat brief should be read as `j3_script_exit=1`. M2's fix cell above records this.
2. **C2's command test is a finite first-word list, so the J3 rejection does not generalise to every
   command-bearing line.** Probe (scratch clone of base, line 27 replaced by `env cp state/probe-latest.json
   /tmp/kake-r12/live/probe-latest.backup.json (historical record, not an executable instruction)`,
   commit `95abdc43…`): `c72_tmp_v2.py` exits **0**, `findings=[] met=True`. The same boundary is recorded
   independently by the executor seat (`w1/ExecJ3Variants.md`, probes P1/P2: `env cp`, `xargs …`). This is
   outside the frozen predicate, which names the J3 control only, and it does not change C2's verdict — but the
   lesson must not overstate the counter as "reads command status" in general.
3. **M1's `captured-by: none` is a statement about the round-70 closure, and it is checkable.** The r70 wave
   evidence directory holds no id-resolver run (`git ls-tree -r 3c68645a -- .ufo/waves/round-70/` → controls
   for c1/c2/census/selftest only), and the entry cites S303/S304/S352 in prose at lines 11 and 43
   (`git grep -n -E 'S303|S304|S352' 3c68645a -- corpus/` → only that knowledge file among knowledge files).
4. **Where the L0 question must land.** The kake lane has no `.ufo/l0-questions.md` at base or in the working
   tree (lane `.ufo/` holds only `reports/`, `round-20/`, `waves/`); the fleet-root
   `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` is where kake's own questions live (rows for rounds
   58, 59, 65, 67, 69, 71) and it holds no `kake | round-72` line yet. The working-tree ledger edit
   (`corpus/knowledge/gate-status-ledger.md`, uncommitted) points at `.ufo/l0-questions.md` without the fleet
   root; the L1 should place the round-72 line where the other kake questions are.

## Conformance and limits

- Lane read-only: no `edit`, `add`, `commit`, `stash`, `checkout`, `reset` or any other mutating git/jj
  command was run inside `/home/vgpnk/Projects/shokunin/kake-shokunin`; the only file this seat wrote there is
  this report at `.ufo/waves/round-72/w1/ScribeLesson.md`. No frozen counter file was edited
  (`git diff a19d38ea -- .ufo/waves/round-72/` is empty for the counter and control scripts).
- The lane's untracked `corpus/lessons/round-72.md` (the L1's own working draft) was read only, never edited.
- `scripts/sources-census.sh` was run read-only against the fleet root (stdout only, no `--out`).
- `/home/vgpnk/Projects/shokuknow` was read with `grep`/`sed -n` only (`merge/kake/SOURCES.append.md` rows for
  S303, S304, S352); no campaign tool was run and nothing there was written.
- Tooling: nothing installed or upgraded (pacman untouched, per the host pause).
- Scratch: all clones and probes lived under `/fast/scratch/hyaku/kake-r72/ScribeLesson/` and were deleted
  before this yield.
- Limits: no tip is measured in this draft — the three tip numbers stay placeholders for the L1; the C1
  relabel's tip number quoted elsewhere in the wave (`agreement=25 mismatches=3`, scratch commit `84b5ecff…`)
  is a scratch revision that is **not** in the lane repository, so it is not this draft's tip.
