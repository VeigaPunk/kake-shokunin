# MutC2Gate

Mutation test of the round-59 C2 counter `.ufo/waves/round-59/c59_resolver_cases.py` (frozen, version 1)
by mutating the tool it scores, `scripts/id_resolver.py`.

Everything below was executed in scratch clones under `/fast/scratch/hyaku/kake-r59/MutC2Gate/`
(`git clone -q --shared` from the lane). The lane repo, its Git index and jj state were never
mutated: `git -C <lane> status --porcelain` shows only other seats' edits; my commits exist only in
scratch clones. Receipts: `.ufo/waves/round-59/w1/MutC2Gate.files/`.

Bases used:
- contract commit `45a92b64ac8a0f82dba369100e30682f14de81fb` (= `BASE_REV` in the counter);
- `scripts/id_resolver.py` is byte-identical at `fd6303c…` and `45a92b6…` (verified by
  `git diff --stat` — empty), so the base sweep mutates the tool the claim will be measured on.

## METHOD

Two sweeps, both with the frozen gate (`python3 -B c59_resolver_cases.py --root <clone> --revision <mutant commit>
--work <scratch> --seed 59`, the same seed as the frozen base control `controls/base-c2-resolver-cases.txt`):

- **Base sweep (M01–M20)** — 20 single-point mutants of the contract-commit tool. Baseline at
  `45a92b6`: **13/21, exit 1**, reproducing the frozen base control exactly (same 13 pass / 8 fail).
- **Green sweep (G01–G26, H01–H20)** — 46 single-point mutants of a **green reference tool** I wrote in
  scratch (`.files/reference-tool-builder.py`): the seven round-59 routes closed and the tool's own
  selftest extended to 67 cases. It scores **21/21, exit 0** on the frozen gate, so every mutant here
  is measured against a tool that passes — a survivor is a real hole in the gate, not an artefact of
  an already-failing case.

Each mutant is one edit committed in the scratch clone with the selftest identity
(`-c user.name=selftest -c user.email=selftest@local`); `git diff --numstat` against the green base
shows `1 1` for 43 of 46 green mutants (G02/G04/G07 are 2-line and 4-line rewrites of one statement;
H01 is 2 lines) — all are single-point behavioural mutations. The pristine blob is restored after each
sweep and the sha256 of the restored file equals the pre-sweep sha256
(`restored_ok: true` in both sweep JSONs; `GIT_STATUS` clean or one staged restore only).

Total: **66 mutants, 43 killed, 23 survived** (base sweep 10/20; green sweep 33/46).

## MUTANTS:

Killed by the frozen 21 cases. `tally` = cases passed of 21; `flipped` = the cases whose verdict
changed against the baseline for that sweep (base baseline 13/21, green baseline 21/21).

| id | sweep | locus | tally | flipped |
| --- | --- | --- | --- | --- |
| M01 | base | ID_RE 3+ digits → 4+ | 10/21 | K3, K6, P7 |
| M03 | base | ROW_RE indent 0-3 → 0-2 | 12/21 | P1 |
| M04 | base | ROW_RE indent 0-3 → 0-4 | 12/21 | P3 |
| M05 | base | FENCE_OPEN_RE needs 4+ chars | 9/21 | K1, K2, K3, K6 |
| M10 | base | `_nul_paths` splits on newline, not NUL | 10/21 | K4, K5, K7, K14, P7 |
| M11 | base | os.walk follows symlinks | 14/21 | K10 |
| M15 | base | url-match never populated | 12/21 | P4 |
| M16 | base | `--fleet` directory check removed | 12/21 | P5 |
| M17 | base | exit code: dangling never yields 1 | 4/21 | K1–K7, P3, P4 |
| M18 | base | selftest tally print faked to the floor | 14/21 | P6 |
| G01 | green | K8 route reverted: HTML comments not stripped | 19/21 | K8 |
| G02 | green | K9 route reverted: setext heading no longer ends the section | 19/21 | K9 |
| G03 | green | K10 route reverted: os.walk does not follow symlinks | 19/21 | K10 |
| G04 | green | K11 route reverted: committed symlink read as its target string | 19/21 | K11 |
| G05 | green | K12 route reverted: registry symlinked out of the lane trusted | 19/21 | K12 |
| G06 | green | K13 route reverted: revision read by path (non-UTF-8 name fatal) | 14/21 | K4, K5, K7, K11, K13, P7 |
| G07 | green | K14 route reverted: non-toplevel `--root` measured through the ancestor | 19/21 | K14 |
| G08 | green | ID_RE 3+ → 4+ digits | 17/21 | K3, K6, P7 |
| G09 | green | ROW_RE indent 0-3 → 0-2 | 19/21 | P1 |
| G10 | green | ROW_RE indent 0-3 → 0-4 | 19/21 | P3 |
| G11 | green | fence machine: a fence needs 4+ chars | 16/21 | K1, K2, K3, K6 |
| G12 | green | fence machine: closing run must be exactly as long | 20/21 | P6 |
| G13 | green | section end: a `##` heading no longer ends the section | 20/21 | P6 |
| G15 | green | `--fleet` check removed | 19/21 | P5 |
| G16 | green | exit code: dangling never yields 1 | 6/21 | K1–K7, P3, P4 |
| G17 | green | url-match never populated | 19/21 | P4 |
| G18 | green | ls-tree -z parse: split on newline instead of NUL | 14/21 | K4, K5, K7, K11, K13, P7 |
| G19 | green | realpath containment dropped for knowledge files | 20/21 | P6 |
| G20 | green | realpath containment dropped for the registry | 19/21 | K12 |
| G22 | green | selftest total faked upward | 20/21 | P6 |
| G23 | green | dangling ids no longer sorted | 20/21 | P6 |
| G24 | green | citing paths no longer sorted | 20/21 | P6 |
| H03 | green | sibling registry read from the dirty worktree, not HEAD | 20/21 | P6 |
| H04 | green | HTML-comment stripping handles only one line | 19/21 | K8 |
| H07 | green | the Registry heading no longer required (any row registers) | 3/21 | 18 cases |
| H09 | green | registry URL cell keeps trailing punctuation | 20/21 | P6 |
| H10 | green | ID_RE accepts a lowercase id | 20/21 | P6 |
| H11 | green | ID_RE accepts a trailing underscore | 19/21 | P6, P7 |
| H12 | green | any knowledge-file extension is read at a revision | 20/21 | P6 |
| H14 | green | sibling directory scan accepts any name | 20/21 | P6 |
| H16 | green | dangling set difference inverted | 5/21 | 18 cases |
| H17 | green | registry read at the worktree even in revision mode | 20/21 | P6 |
| H19 | green | the git environment no longer scrubbed | 20/21 | P6 |

Note the concentration: **P6_tool_selftest flips in all 33 green-sweep kills, and is the only case that
flips in 13 of them** (G12, G13, G19, G22, G23, G24, H03, H09, H10, H12, H14, H17, H19). The 21
cases are a thin wrapper; most of the discrimination comes from running the tool's own selftest and
reading its printed tally — which is exactly the surface the tally cheat attacks.

## SURVIVORS:

23 survivors. 10 from the base sweep and 13 from the green sweep. Each was then probed against
sharper fixtures (`.files/survivor-probe.py`) to separate *behaviourally equivalent* mutants from
*real holes*.

**Base sweep survivors (10) — M02, M06, M07, M08, M09, M12, M13, M14, M19, M20.**
All 10 keep the tally at 13/21 with no case verdict changed. M02 (ID_RE lookbehind dropped), M06
(`##` heading no longer ends the section), M07 (`ID_CELL_RE` accepts any `S`-digit cell), M08
(registry URL trailing punctuation kept), M09 (registry URL cell keeps the whole row), M12
(realpath containment dropped), M13 (lane exclusion by realpath dropped), M14 (owner list unsorted),
M19 (citing paths unsorted), M20 (dangling ids unsorted). **These are not holes in the 21 cases.**
They are invisible *at this base* only because the eight base-failing cases (K8–K14, P6) already
absorb the change: e.g. M12/M13 change containment behaviour that K11/K12 already fail, M14/M19/M20
change output ordering that no case asserts. Re-measured on the green tool, the equivalent behaviours
are still not asserted by any frozen case (G14/G25/G26 below), so the base-sweep survivors and the
green-sweep survivors overlap.

**Green sweep survivors (13), classified:**

| id | locus | equivalent or real hole? |
| --- | --- | --- |
| G14 | sibling owner list no longer sorted | **equivalent** — `sibling_dirs` already yields lanes in sorted order, so `owners` is sorted either way; probe output byte-identical |
| G26 | sibling registry read from the dirty worktree | **equivalent / invalid mutant** — the applied diff is a comment-only edit (no behaviour change; `git diff` against the green base shows only `# (mutant G26)` appended), so it is a no-op by construction |
| G25 | symlink resolution: a link that leaves the tree followed anyway | **equivalent on the fixtures probed** — the tree-containment check is redundant with `key in entries`; byte-identical output on a link to `../../outside.md` |
| G21 | selftest tally faked to the floor (`max(passed,66)/max(len,66)`) | **real hole** (see below) |
| H01 | selftest always exits 0 and prints a faked 66/66 | **real hole** (see below) |
| H02 | selftest swallows a failing case (tally fixed at 66/66) | **real hole** (see below) |
| H05 | registry containment compares the path prefix only (no separator) | **real hole** — a registry symlinked to `<fleet>/kake-shokunin-evil/corpus/SOURCES.md` is accepted; green exit 2, mutant exit 1 with the outside ids resolved |
| H06 | knowledge containment compares the path prefix only (no separator) | **real hole** — a knowledge symlink to `<fleet>/kake-shokunin-evil/corpus/knowledge/leak.md` is read; green exit 0 (no citation), mutant exit 1 with `DANGLING S011 cited-by=corpus/knowledge/leak.md` |
| H08 | URL_RE no longer stops at a backtick | **real hole** — a sibling registry URL ending in a backtick: green `url-match=alpha-shokunin`, mutant `url-match=-` |
| H13 | the working-tree knowledge walk accepts any file extension | **real hole** — `corpus/knowledge/notes.json` citing an id: green ignores it, mutant reports it dangling |
| H15 | the fleet root defaults to the lane itself instead of its parent | **real hole** — without `--fleet`, green finds the owning sibling lane, mutant reports `owners=-` |
| H18 | symlink resolved without the tree-containment check | **real hole** — a symlink to a symlink: green cites `corpus/knowledge/leaf.md` only, mutant also cites `corpus/knowledge/mid.md` (it read the inner link's target string) |
| H20 | the fence machine accepts a backtick fence whose info string holds a backtick | **real hole** — CommonMark says such a fence does not open: green resolves the row after it, mutant reports it dangling |

**The decisive hole: the printed selftest tally is trusted (G21, H01, H02).**
The frozen P6 reads the tally the tool prints (`re.findall(r"(?m)^selftest: (\d+)/(\d+)\s*$", text)`)
and checks only `passed == total` and `total >= 66`. A tool that prints `selftest: 66/66` and returns 0
satisfies P6 whatever its own cases did. Measured end-to-end (`files/false-green-receipt.txt`):
a tool carrying a **real defect** (the working-tree knowledge walk accepts any file extension — a
behaviour no frozen case asserts) plus a faked tally scores **21/21, met=True, exit 0** on the frozen
counter, while its own `--selftest` reports one failing case. The frozen gate therefore certifies a
broken tool. G21 additionally shows the floor itself is reachable by print: a tool with 66 cases and one
failing case prints 66/66.

The counter's own `--selftest` is still the version-1 stub (`c59 resolver-cases selftest: version 1 stub
(not yet ported); exit 2`), so the round-58 cheat classes (constant green, always-exit-1, id masks,
canned output) are **not** in the gate as the contract requires ("ported into the gate selftest by wave 1
before data"). I measured them anyway against the 21 cases: constant-green output 4/21, always-exit-0
6/21, id-mask 17/21, canned-output 5/21 — all four are caught by the 21 cases themselves, so porting
them into the gate selftest would be cheap insurance, not the main gap.

## PROPOSED CASES:

Eight cases, validated against the green tool and against every survivor
(`.files/c59_resolver_cases_proposed.py` = frozen counter + `_proposed_cases`; validator
`.files/validate_proposed.py`). On the green reference tool the extended counter scores **29/29,
exit 0** — the additions are green-compatible, not tautologies.

| id | case | kills | green result |
| --- | --- | --- | --- |
| Q1 | `Q1_non_markdown_knowledge_file_is_not_read` — a `corpus/knowledge/notes.json` citing an id is not a citation source | H13 | exit 0, `ids_cited=1 ids_resolved=1 dangling=0` |
| Q2 | `Q2_backtick_fence_info_string_blocks_a_fence` — a backtick fence whose info string holds a backtick does not open a block, so the next row registers | H20 | exit 0, `ids_cited=2 ids_resolved=2 dangling=0` |
| Q3 | `Q3_default_fleet_root_is_the_lane_parent` — without `--fleet` the fleet root is the lane's parent, so a sibling lane is found | H15 | exit 1, `DANGLING … owners=alpha-shokunin` |
| Q4 | `Q4_prefix_sharing_symlink_is_outside_the_lane` — a knowledge symlink to `<fleet>/kake-shokunin-evil/…` shares the lane's path prefix but is outside it | H06 | exit 0, `ids_cited=1 ids_resolved=1 dangling=0` |
| Q5 | `Q5_prefix_sharing_registry_symlink_is_unevaluable` — a registry symlinked to a prefix-sharing path outside the lane is unevaluable | H05 | exit 2, `registry outside the lane` |
| Q6 | `Q6_selftest_tally_is_independently_verified` — the tool's selftest output is checked against itself: no `FAIL` line may appear, the printed total must equal the number of case lines the tool actually emitted, and the floor must hold | H02 | `tally=('67','67') case_lines=67` |
| Q7 | `Q7_registry_url_ending_in_a_backtick_is_not_matched` — a registry URL ending in a backtick is not matched verbatim | H08 | exit 1, `owners=alpha-shokunin url-match=alpha-shokunin` |
| Q8 | `Q8_symlink_to_a_symlink_is_not_read_as_its_target_string` — a symlink pointing at another symlink is never read as its target string | H18 | exit 1, `DANGLING … cited-by=corpus/knowledge/leaf.md` |

Measured: with Q1–Q8 the extended counter kills 7 of the 8 real green-sweep holes (H13, H20, H15,
H06, H05, H08, H18) and the tally cheat H02. Against the decisive false-green mutant (real defect +
faked `selftest: 66/66`) the extended counter returns **27/29, exit 1** (Q1 and Q6 fail) where the
frozen counter returns 21/21, exit 0.

Still uncovered after Q1–Q8 (proposals only, not validated as cases):
- **G21** (tally faked with `max(passed,66)/max(len,66)`): Q6 catches the hard-coded variant H02 but
  not the `max()` variant, because with 66 or 67 cases the floored numbers coincide with the true ones.
  A check that the printed denominator equals the number of emitted case lines (as Q6 does) **does**
  catch G21 when the case count differs — Q6 is the right shape; the residual is that G21 is only
  detectable when the tool's case count and the floor coincide in a way the check can see. [INFERENCE]
- **H01** (always exits 0): with a faked tally the exit code is not evidence; Q6's case-line count is
  the only independent signal and it does not see a *swallowed* case unless the case still prints.
  [INFERENCE]
- **G14, G25**: equivalent mutants — no case can kill them and none should. **G26** is an invalid mutant
  (comment-only diff), so it is not evidence of a hole at all.
- A counter-level guard the wave should also add: the counter's own `--selftest` must be ported from the
  round-58 seven-control gate (constant green, always-exit-1, id masks, canned output) and must assert
  that the tool's printed selftest tally is consistent with the case lines it emitted, so a future
  cheat of the G21/H01/H02 family is caught by the gate rather than by a proposed case.

Verification run by the main agent: `python3 -B .ufo/waves/round-59/c59_resolver_cases.py --root <lane>
--revision <rev> --work <scratch> --seed 59` on the base, on the green reference tool, and on each
mutant commit. All mutant commits live only in scratch clones; the lane Git index was not touched.

VERDICT: The frozen C2 counter kills 43 of 66 single-point mutants of `scripts/id_resolver.py` (all seven round-59 route reverts are caught) but has a decisive false green: it trusts the tool's printed selftest tally, so a tool with a real defect plus `selftest: 66/66` passes 21/21 — the eight proposed cases Q1–Q8 close 7 of the 8 real holes and that false green.
