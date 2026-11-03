# Round 72 — W1 CriticClaims (kake, attempt 1)

Seat: CriticClaims (critic, leaf). Contract: `.ufo/waves/round-72/contract.md` at freeze `a19d38ea`; base `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1`. Read-only lane; all work in `/fast/scratch/hyaku/kake-r72/CriticClaims-2/` (deleted before yield). No tool installs. No pacman.

## Verdict

- **c1 = survives** — the frozen C1 predicate reproduces exactly on a simulated relabel tip (agreement 24→25, evaluated 28, structural 0, scores 3/3, and only `c56_selftally.py` changes label). Kill rule does not fire. Survives with routed caveats: (A1) the relabel text must state the true cause (see A1, the text I drafted in the simulation was wrong); (A2) `c66` exits 0 at base, so the claim is admissible only by reading `agreement`, never by exit code.
- **c2 = survives** — the four legs reproduce on the frozen counter: selftest `11/11` exit 0; J3 control c71=0, c72=1; red-before (cc6b4e0b) exit 1; base tip (3c68645a) exit 0. Survives on its J3-specific predicate. Routed: the claim sentence is broader than the predicate and the class is not closed (B1).

## Evidence commands (exit codes observed by this seat)

| # | Command (cwd = scratch clone at freeze `a19d38ea` unless noted) | Exit | Observed |
|---|---|---|---|
| E1 | `python3 -B .ufo/waves/round-66/c66_gate_status_hostportable.py --root . --revision 3c68645a… --jobs 6 --work <scratch>` | 0 | `members=28 evaluated=28 mismatches=4 structural=0 agreement=24 scores_held=3/3 met=True` (matches `controls/c1-base.txt`) |
| E2 | same, `--revision 2d5e26fa…` (scratch commit: c56 row relabelled `historical`) | 0 | `mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True`; per-member diff vs E1: only `c56_selftally.py` `live e_T=1 …MISMATCH` → `historical e_T=1 e_P=0 … ok` |
| E3 | `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision 4cb225fb…` | 0 | `tally_mismatches=0 rows_checked=10 met=True` |
| E4 | same, `--revision 3c68645a…` | 1 | `tally_mismatches=6`; the six rows are the scripts/ tools, each `observed=N/N MISMATCH tool_changed` (observed selftest tally is itself green) |
| E5 | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --selftest` | 0 | `C2v2 selftest 11/11` |
| E6 | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --revision cc6b4e0b…` | 1 | `met=False`, findings at lines 27,95,227,356,359,463,464 |
| E7 | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --revision 3c68645a…` | 0 | `met=True` |
| E8 | `HYAKU_SCRATCH=<scratch> sh .ufo/waves/round-72/controls/j3-control.sh` | 1 | prints `c71 … met=True` then `c71_exit=0`; `c72 … command_findings=1 … met=False`; script exits 1 (see B2) |
| E9 | `python3 -B .ufo/waves/round-71/c71_tmp.py --lane <clone> --revision 2d5e26fa…` | 1 | `guard=fail met=False` (relabel removed a non-token line; contract says re-reddens by design) |
| E10 | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane <clone> --revision 2d5e26fa…` | 0 | `met=True` (C2 unaffected by the C1 relabel) |
| E11 | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane <clone> --revision 9cb1305d…` (scratch: line 27 = `tar cf … && mv … /tmp/kake-r12/… (historical record, not an executable instruction)`) | 0 | `command_findings=0 prose_findings=0 met=True`; c71 same variant exit 0 |
| E12 | `git -C <clone> rm -r scripts/fixtures/quote-class` at 3c68645a, then `python3 -B .ufo/waves/round-56/c56_selftally.py --root <clone> --revision 41315a5f…` | 0 | `tally_mismatches=0 rows_checked=10 met=True` |
| E13 | `node scripts/freshness-sweep.mjs --offline` at base | 2 | `paths sidecar binding invalid: corpus/SOURCES.md:140` (pre-existing host state; freshness not re-measurable here) |
| E14 | `git diff --name-status 4cb225fb… 3c68645a… -- scripts/fixtures 'scripts/*.py'` | 0 | 4 added `scripts/fixtures/quote-class/*`; added `append_guard.py header_audit.py id_resolver.py quote_class.py response_snapshot.py`; the six pinned gate scripts (`base_path_audit.py source_recheck.py robots_audit.py sitemap_audit.py redirect_audit.py citation_lint.py`) are **byte-identical** pin→tip |

Freeze-diff check: `git diff --name-status 3c68645a a19d38ea` adds only `.ufo/waves/round-72/*`. No `corpus/SOURCES.md` row S439 is present at the freeze commit (see Note N3).

## Attacks on C1 (calibration)

**A1 — routed. The relabel's stated cause is wrong in the drafted text; the true cause is scope-pin drift.** I drafted the relabel text as "the six r56-era selftest rows it pins were superseded by later counter upgrades". That is false. E14 shows the six gate scripts are byte-identical pin→tip. The red comes from the counter's `scripts/fixtures` tree check: that tree gained four `quote-class` fixture files after `4cb225fb`. E12 restores the tree and c56 goes green at tip (`10/10`, exit 0). The honest row must say: "red at base only because `scripts/fixtures` gained files after the round-56 pin; the six selftests are green at tip (observed `N/N`)". Only with that wording is the relabel a non-author-honest re-adjudication. A non-author who reads "superseded by later counter upgrades" against E14 would call it inaccurate.

**A2 — routed; blocking for any exit-keyed consumer. `c66` exits 0 at base.** E1: the counter exits 0 with `met=True` at base, where agreement is 24, not 25. The counter's `met` gates only `members==28 AND evaluated==28 AND scores_held==3`; `agreement` is reported, never gated (c66 header, D5). So the C1 predicate (`agreement==25`) is readable only from the printed number. A gate that keys on the exit code would green C1 at base. The contract's kill rule is explicit, so C1 is not unprovable; the closure must read the number.

**A3 — note. The metric measures label-vs-exit consistency, not discernment.** LEARNING.md defines discernment as gate decisions checked against an outside spot-check of admits and rejects. c66 `agreement` checks that each `historical`/`live` label matches the member's observed exit. Its `historical` rule is "green at pin, not green at tip". A relabel that matches the observed exit raises agreement by construction. This is not gaming in the sense of hiding a failure here (A1 shows the red is real-but-scope, not behaviour), but C1 does not exercise the discernment trend and cannot be read as a calibration score move. `scores_held` correctly keeps calibration at 2 (E2 shows 3/3 held). No score credit is claimed.

**A4 — note. Selection after diagnosis.** At base four members are red (`c56`, `c57`, `c58`, `c59`). The contract names c56 as the one row to relabel and excludes c57–c59 with a stated cause (staged ids). I did not test whether c58 or c59 have green pins that would permit a `historical` relabel (**[INFERENCE]**: unverified; c58/c59 `e_T=1`, so a green pin is possible). The target `25` is reachable through one relabel the diagnostic run exposed. The contract discloses the diagnostic (see §Pre-freeze), so this is a selection-bias note, not concealment.

**A5 — note. Harm to the frozen round-71 counter.** E9: `c71_tmp.py` exits 1 at the relabel tip (guard fail). The contract states it "re-reddens on any later SKILL.md edit by design", so this is expected. The operator should know that `c71` is now permanently red on this lane tip and is superseded by `c72`.

## Attacks on C2 (operability)

**B1 — routed. The claim sentence is broader than its predicate; the class is not closed.** The claim says c72 "rejects a phrase-only annotation on a command-bearing `/tmp` line that the round-71 counter accepts". The predicate tests only the J3 control (a `cp` line). E11 is a command-bearing `/tmp` line with a non-listed verb (`tar … && mv … /tmp/…`) plus the phrase: c72 exits 0 `met=True`, and c71 also exits 0. Cause: `COMMAND_WORDS` lists `cp mv git …` but not `tar`/`rsync`/`dd`, and a leading non-listed verb (e.g. `echo backing up; cp …`) passes too (probed in-process: `tar_with_phrase`, `rsync_with_phrase`, `echo_semicolon_cp` all `ACCEPT`). The M2 mistake class is therefore still open for verbs outside the list. C2 survives on its own J3 predicate; the round report should bound the claim to the `cp`-led J3 instance and record the residual.

**B2 — note. The frozen J3 script's receipt does not show `c72_exit=`.** `j3-control.sh` runs under `set -eu`; the round-72 counter exits 1 and the script aborts before its `echo "c72_exit=$?"`. E8 prints the c72 line and exits 1, with no `c72_exit=` line. `controls/c2-j3-control.txt` has the same shape. The script's own exit 1 is consistent only with `c72` exit 1 (a `c72` exit 2 would also yield script exit 2, so exit 1 is still discriminating), so the predicate is evaluable, but the literal printed token the contract's counting command names is absent.

**B3 — note. Four-leg exit predicate: constants fail, sufficiency unproven.** Exit-code legs (selftest=0, J3 c72=1, red-before=1, tip=0), applied to stubs:
- always-exit-1: selftest leg FAIL, tip leg FAIL → predicate false.
- always-exit-0: J3 leg FAIL, red-before leg FAIL → predicate false.
- a counter meeting all four: predicate true.
So no constant satisfies it, as the contract asserts. The four legs are not sufficient for "the counter is correct": a counter keyed to the exact J3 bytes would pass every leg (**[INFERENCE]**, not built). B1 is the observed instance of this gap.

## Pre-freeze diagnosis (attack 4)

Disclosed in `contract.md`. Materiality check: the C1 and C2 base receipts reproduced exactly on fresh runs (E1 agreement 24/exit 0; E6 exit 1; E7 exit 0; E5 11/11), so the diagnostic runs did not change the base measurements. The diagnostic did shape claim choice (A4). The disclosed discarded CrUX prototype was never landed. **Admission effect: none by itself**; carry it as a conformance caveat for the non-author closure, as the contract already requires.

## Axis harm (attack 5)

- **operability 10**: no registry gate is newly red except `c71` (superseded, A5). `c72` is green at the relabel tip (E10). No operability harm observed. Survives.
- **freshness 10**: `freshness-sweep --offline` exits 2 at base on this host (E13), so freshness drift cannot be re-measured here. Unprovable for this axis. The C1 edit lands at SKILL.md line 1253, which is beyond the sidecar's highest bound line (935; `corpus/knowledge/freshness-sidecar.json`), so it does not touch a sidecar-bound line by construction (**[INFERENCE]** from the sidecar's bound-line set, not from a sweep run).
- **calibration 2**: held (`scores_held=3/3` in E2). C1 moves calibration only through its own `agreement` predicate and gives no score credit.

## Notes for the closure (not claims)

- **N1** The contract's frontier step says `corpus/SOURCES.md` gains S439 this round; the freeze commit adds no SOURCES row (`git diff --name-status 3c68645a a19d38ea` shows none). Census acceptance is still open.
- **N2** `c72` was not run against any SKILL.md revision that includes a `/tmp` line of the B1 form; the residual is in the frozen counter and is not fixed here.
- **N3** `c66`'s SKILL.md registry row for `selftest-tally-counter` says `live`; any landed relabel must also update that row's `Kind` cell and the `historical` pin (`4cb225fb…`) must be an ancestor of tip (c66 `pin_not_ancestor` check).

## Scope and cleanup

- Scratch commits created and discarded: `2d5e26fa` (C1 sim relabel), `9cb1305d` (C2 tar/mv variant), `41315a5f` (fixtures-restored c56). Not landed; the lane is unmodified.
- No installs or upgrades. No mutating git inside the lane. No writes to the fleet root or to shokuknow.
- Scratch tree `/fast/scratch/hyaku/kake-r72/CriticClaims-2/` removed before yield.
