# ConnOverlap — kake round 72, w1, cross-claim overlap scan (read-only)

Verdict: c1_touches_c2_measurement=no c1_changes_other_c66_member=no c2_depends_on_dangling=no

Seat ConnOverlap · base `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1` · C2 round-71 base `cc6b4e0b8c35e72dfb02c6184b847f68c1262153` · contract freeze `a19d38ea`.
Scratch `/fast/scratch/hyaku/kake-r72/ConnOverlap/` (clone, clone2, clone3, c57 copy, c66 logs). Lane tree: read via `git show` / `git grep` / `git log` only. No lane file written. Scratch deleted before yield.

Scope note: the C1 relabel is the planned Kind cell of the `selftest-tally-counter` row (c56). The replacement text is the exact `ExecRelabel` item text. It was applied in a scratch clone only (`211232d7`, 1 line changed, `git diff --numstat` = `1 1 SKILL.md`).

## (1) Can the C1 SKILL.md edit change a C2 measurement? — NO

Mechanism of c72 (`c72_tmp_v2.py`, read in full): it reads only `SKILL.md` at BASE and at `--revision` (`show()`, `PATH="SKILL.md"`). It counts `/tmp/` tokens per line (`TOKEN_RE`). A line is a command finding if a backticked span has a command word as first word, or the line's own first word is a command word. Otherwise it is a prose finding unless the phrase `not an executable instruction` is on the line. `guard_ok` requires every ADDED line that carries a token to carry the phrase.

The C1 edit adds no `/tmp` token and no command-span to any line. The only added line is the c56 row, which has no token, so the guard is not engaged by it.

Evidence:

- Candidate replacement Kind cell, scored with `line_findings` imported by path from `.ufo/waves/round-72/c72_tmp_v2.py`:
  - Kind cell alone: `(brace, command, prose) = (0, 0, 0)`.
  - Full candidate row (Kind cell plus the other cells of the base row): `(0, 0, 0)`.
  - Old (base) Kind cell: `(0, 0, 0)`.
  - `TOKEN_RE.findall(newKind) == []`.
  - Backtick spans in newKind and `command_span_words`: `4cb225fb…` → None; `.ufo/waves/round-72/controls/c56-pin-linux.txt` → None; `tally_mismatches=6` → None; `tool_changed` → None; `.ufo/waves/round-72/controls/c56-tip-linux.txt` → None.
  - Member-path substring check in newKind: none of the 28 FROZEN paths appear in it (only the c56 path appears in the base row's Entry cell).
- Full counter at the C1 tip (`c72_tmp_v2.py --lane <clone> --revision 211232d7…`): `C2v2 … brace=0 command=0 prose=0 findings=[] removed=8 added=8 guard=ok met=True`, exit 0.
  - Base (same clone, `--revision 3c68645a…`): `removed=7 added=7 … met=True`, exit 0.
  - The only numeric change is removed/added 7→8. The C1 row is a new line not present at BASE, so the old and new lines each count once more. The predicate does not read these counts.
- C1 + frontier step (`fcb03718…`, adds the S439 row and `corpus/lessons/round-72.md`): exit 0, `removed=8 added=8 guard=ok`.
- Dangling-id repair alone (`a021ec3f…`, scratch): exit 0.
- C1 + dangling-id repair (`01409769…`): exit 0.
- Receipt `controls/c2-base-red.txt` (not re-run here): `cc6b4e0b` red, exit 1, `command_findings=2 prose_findings=5`.
- Counterfactual, to show what would couple (not the dispatched text):
  - CF-1 (receipt path written as `/tmp/kake-r72/…`): `prose=1` → C2-red.
  - CF-2 (same plus no phrase): `prose=1` → C2-red.
  - CF-3 (`cp … /tmp/…` in backticks): `command=1` → C2-red.
  - So the coupling is latent: it becomes live only if a future C1 Kind text names a `/tmp` path. The dispatched Kind text uses repo-relative receipt paths, so it is not live.

## (2) Can C1 change the c66 agreement of any member other than c56? — NO (for the C1 edit)

The c66 counter (`round-66/c66_gate_status_hostportable.py`, `eval_member`) reads, for a member:
- the Entry cell (`cells[2]`) to count its row and to get its command span (`counted`, `span`). The Kind cell is not an input to this.
- the Kind cell of its own row only, for the label word (`historical` / `never met`) and the 40-hex pin (`HEX40`).
- `rows_mentioning(skill, member)` (duplicate_row check): any row whose cells contain the member path. For the c56 Kind text this matters only if the new text contains another member's path, which it does not.

So the Kind cell of the c56 row can change only c56's own label, pin and class. The Verdict-map and Entry cells are not touched.

Empirical per-member diff (each run's `label e_T e_P eval class` lines, parsed and compared to the base run):

| run (clone, `--jobs 6`) | agreement | mismatches | members whose line differs from base |
|---|---|---|---|
| base `3c68645a` (`c66_base.txt`) | 24 | 4 | — |
| C1 tip `211232d7` (`c66_c1tip.txt`) | 25 | 3 | `c56_selftally.py` only: `live e_T=1 MISMATCH live_not_green` → `historical e_T=1 e_P=0 ok` |
| C1 + frontier `fcb03718` (`c66_frontier.txt`) | 25 | 3 | `c56_selftally.py` only (same change) |
| C1 + dangling fix `01409769` (`c66_both.txt`) | 27 | 1 | `c56_selftally.py`, `c58_resolver_cases.py`, `c59_resolver_cases.py` |

Exit codes: all three c66 runs exit 0 (`met=True`). `measure.last`: `evaluated=28` in every run. Sets of mismatching members at the C1 tip: c57_idresolver_gate, c58_resolver_cases, c59_resolver_cases.

The last row shows a coupling that is not the C1 edit. It is the dangling-id repair (routed to L0) that moves c58 and c59. That is covered in section (3) and is flagged for the L1.

## (3) Does C2 depend on the r70 adopted entry or the three dangling ids? — NO

Evidence:
- `c72_tmp_v2.py` reads one committed file, `SKILL.md`. It does not read `corpus/knowledge/crux-bigquery-origin-membership.md`, `corpus/SOURCES.md`, or `scripts/id_resolver.py`.
- `SKILL.md` at `cc6b4e0b` and at `3c68645a` contains 0 matches for `S438` or `crux-bigquery`. The r70 adoption commit `50ec1446` does not touch `SKILL.md`.
- Dangling ids at base (`scripts/id_resolver.py --root . --revision 3c68645a…`): `DANGLING S303`, `S304`, `S352`, `ids_cited=121 ids_resolved=118 dangling=3`. These are cited only in `corpus/knowledge/crux-bigquery-origin-membership.md` (lines 11 and 43).
- Removing the three staged citations in scratch (`a021ec3f…`, 2 lines changed) gives `dangling=0`. c72 at that revision: exit 0, `removed=7 added=7 met=True`.
- c72 at `01409769…` (dangling fix + C1): exit 0.

The dangling ids are not a C2 input. C2's red-before is caused by the SKILL.md `/tmp` lines (receipt `c2-base-red.txt`), which are unchanged by the dangling fix.

## Coupling found that is not C1↔C2 (for the L1)

The contract's C1 predicate `agreement == 25` is not invariant under the operator-routed dangling-id repair. Measured in scratch: the repair alone takes c58_resolver_cases and c59_resolver_cases from red to agreement (their P7 leg is the dangling check: `P7_real_lane_green FAIL ids_cited=121 dangling=3` at base, `PASS ids_cited=118 dangling=0` after). With C1 applied as well, `agreement=27`. The C1 kill rule (agreement != 25 → unprovable) would then fire, although the C1 edit itself is correct. This is a sequencing dependency, not an overlap in the measurement. The C1 round should record it if L0 repairs the entry later.

c57 is different: its c66 argv passes `--fleet C:/Users/jpvei/…`, which is not a directory on this host, so c66 records `e_T=2` (exit 2, unevaluable). Its red is therefore a host-path problem in the frozen command, not the dangling ids. Run with a real fleet path (`--fleet /home/vgpnk/Projects/shokunin`), `c57_idresolver_gate.py` exits 1 with G5 red (`dangling=3`), so its real-fleet check does depend on the dangling ids. That is a separate fact and does not change the verdict on C1↔C2.

## Frontier rule (C2 cites S439)

The S439 row is not in the base registry (`corpus/SOURCES.md` at base has rows up to S438). Adding it in scratch (`fcb03718`) leaves c66 unchanged apart from c56, and leaves c72 at exit 0. I did not run `scripts/sources-census.sh validate --root <clone> kake`: it exits 2 (`config not found … shokunin.conf`), because the scratch clone is not a fleet root. This seat did not produce a census result.

## Tooling

None installed, upgraded or removed. Read-only tools used: `git show`, `git grep`, `git log`, `git merge-base`, `git rev-list`, `git diff --stat`, `grep`, `python3 -B` (importlib of the frozen counter for `line_findings`; counter runs), `sh controls/j3-control.sh`. No pacman transaction. No sudo.

## Other runs (not C1/C2 overlap, reported for the record)

- `controls/j3-control.sh` re-run (scratch, its own trap removed the clone): `J3_CONTROL_COMMIT=17c0e1d0…`, `c71_exit=0`, `c72_exit=1` (printed by the script). The shell exit I captured was from the pipe (`tail`), not the script; the script's printed values are the evidence.

## Conformance

- No lane tracked or untracked file written. Every lane access was `git show`/`git grep`/`git log`/`git merge-base`/`git rev-list`/`git diff --stat` (read-only), or a counter run with `--root`/`--lane` pointing at a scratch clone. Counter runs from the lane directory read committed bytes of the scratch clones.
- Scratch tree `/fast/scratch/hyaku/kake-r72/ConnOverlap/` deleted before yield (see the final command).
- Not verified here: c2-selftest, c2-base-red and c2-base-head receipts were read, not re-run (except the J3 script and the single C2 counter runs listed above).
