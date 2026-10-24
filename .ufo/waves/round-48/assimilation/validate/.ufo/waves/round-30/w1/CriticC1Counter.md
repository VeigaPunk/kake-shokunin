# Round 30 wave 1 — CriticC1Counter: can C1 reach 14/14 for the wrong reason?

Verdict: yes. Two stub commits I built in my sandbox score 14/14 with counter exit 0, and both break the C1 interface contract. Each would be a false pass.
Counter attacked: `.ufo/waves/round-30/c1_reason_count.py`, sha256 be2a1287ab7f2abdca8695d8274504d14b9e1c6b0afe95e940c890bfb8bcc53e. Host: Linux 7.2.11, Python 3.14.8. Base gate sha256 d7e79ba1… (same as the before receipt).

## Sandbox artifacts (all under /fast/scratch/hyaku/kake-r30/w1/CriticC1Counter/)
- `stub_gate.py` (199abb40…): wraps the unchanged round-29 gate, which it copies to `scripts/citing_set_base.py`. It has four deliberate defects: (a) with OMNI set, every refusal lists all ten reason codes; (b) a repeated option is detected only as an exact space-separated token; (c) a non-regular document is refused by os.stat before any open, and no code path uses O_NOCTTY; (d) the corpus walk stays recursive and only the recursion limit is raised to 20000.
- `runner_stub.py` (ec59d371…): the base runner plus object entries in expected.json, plus fixture `setup`/`args` fields that the contract does not define. In MODE "contract" it compares the (id, reason) multiset. In MODE "ids+lint" it compares ids only, plus a lint that requires every code in the gate's `REASONS = (...)` block to appear in some fixture.
- `build_variant.py` (eeabfce0…): writes fixtures 30-39, one per code. In the omni variant, every input_invalid fixture (including 15 and 16) expects all ten codes. In the honest variant, each fixture names a deliberately wrong reason, rotated by one (for example, `33-critic-corpus-empty` expects `not_a_directory`).
- Commits in `clone/`: branch critic-omni 9517617752e059fe010c28d875e4d81ca1185efc and branch critic-honest 816201fbf47a6d6c02bccc48ad3802c8e73dedf5, both on 4580c78.
- `probes.py` (c06aca87…) with output in `probes.json`. Counter outputs are in `count-omni.json`/`.err` and `count-honest.json`/`.err`. The mutant runner output is in `mutant-runner.json`.

## Commands run (TMPDIR=sandbox/tmp; exit codes observed)
1. `python3 -B scripts/citing_set_selftest.py --root . --tmpdir …` on each branch: exit 0 and exit 0, 39 cases.
2. `python3 -B <counter> --root <sandbox>/clone --revision critic-omni --scratch <sandbox>/scr-omni`: exit 0, stderr `C1 14/14 at 9517617… (controls True, constant gates rejected True)`.
3. The same command with `--revision critic-honest`: exit 0, `C1 14/14 at 816201f…`. Constant gates scored 0/14 in both runs.
4. `python3 -B probes.py`: exit 0. In the honest export I renamed `"corpus_empty"` (one occurrence) and ran the runner: exit 1. Repeated-option probes: see H4.

## Holes (counterexample, evidence, axis, smallest safe correction)
H1. The behaviour check is a membership test, so a gate that never singles out a reason passes. `refused()` (line 208) uses `want_tuple`, which only asks that the expected finding appear somewhere in the findings list. On critic-omni, every R, F01 and F02 case passes with ten input_invalid findings (count-omni.json, for example R04 observed findings). The contract runner agrees because the fixtures expect all ten codes too. Axis: operability, because the reason code carries no diagnostic value.
Correction: judge refusals with `want_exactly=[("input_invalid", code)]`. At base the gate raises exactly one InputInvalid for each of these inputs. Also require the fixture naming the code to list exactly one input_invalid object.

H2. The "compared" check is satisfied by any mutant failure, not by reason comparison. Lines 446-449 only require that the mutant runner exits non-zero. On critic-honest the runner compares ids only. The mutant fails solely because the lint finds no fixture for the renamed code: `failedCases 0`, with one case-less failure, "reason codes without a fixture: ['corpus_empty_mutated']". The renamed literal was not even the emitted one. The mutated gate still prints `"reason": "corpus_empty"`, taken from `citing_set_base.py`, which the mutation never touches (lines 423-431 rename only in `citing_set.py`). The same hole is open to a runner that pins the gate's sha256 or size.
Correction: (a) require `failedCases > 0`, no failure without a case, and the set of failing cases to equal exactly the fixtures that name the code (read from the summary's `failures[].case`, which the contract keeps). (b) Run the mutated gate on the counter's own behaviour case for that code and require the reason it emits to become `<code>_mutated`. That proves the renamed literal is the emitted one.

H3. A fixture can name a reason that is false. `fixture_codes()` (lines 391-404) only reads expected.json and never checks that the case produces that reason. Every critic-honest fixture 30-39 names the wrong reason, and the run still scores 14/14.
Correction: the H2 checks fix this when combined with exact reason comparison. As an independent check, have the counter run each fixture that names a code through the exported gate and require that (id, reason).

H4. F04 does not isolate repetition. Lines 304-321 test only the space-separated form, and in three of the four variants the first value is unusable.
- On the honest stub, `--population=does-not-exist.json --population=population.json` exits 0. So do `--population X --population=Y` and `--pop X --population Y`. The space-separated form exits 64.
- The base gate accepts `--pop` (argparse abbreviation), so abbreviation is a live third spelling that the contract does not mention.
- The probes.json stub `missing_is_usage` detects repetition only for `--revision` and turns any missing root or document into exit 64. It passes F04 4/4, K1-K3 and R01-R08 behaviour.
Correction: give both repeated values usable targets (two valid population files; `--revision HEAD --revision HEAD`), add the `--name=value` and mixed forms, and require stdout to have the gate's usage-object shape. The L1 has to decide on abbreviations: either `allow_abbrev=False` or count prefix matches.

H5. F05 checks the finding id only. `want_exactly` at line 332 compares (id, reason="None"), so row and file are never checked. In probes.json, a constant gate reporting row S999 and file nowhere.md passes F05; only K1 catches it, through the whole-run control. The stub also shows that F05 measures "no traceback at depth 1000", not "iterative": the base recursive `_walk` passes once the recursion limit is raised.
Correction: compare (id, row, file) = (unadjudicated_citing_pair, S001, corpus/knowledge/d/…/entry.md). Either restate the declared property as "no traceback at depth 1000", or add a static check of the walk.

H6. F06 only observes the wrapper process. In probes.json, the unchanged round-29 gate, which opens documents without O_NOCTTY, passes F06 when it is merely run in a child process (tty_nr 0, document_not_regular_file). Run in-process, the same gate fails with tty_nr 34817. A child is not a session leader, so the kernel never assigns a controlling terminal. A gate that stats before opening also passes, because it opens nothing (critic-honest F06 passed). Stat-then-open reintroduces the race that the round-29 open-then-fstat design avoids.
Correction: in NOCTTY_WRAPPER, wrap os.open before runpy and record (path, flags). Pass F06 only if the device was opened in-process and every such open carried O_NOCTTY. Optionally, also check statically that every `os.open(` in the exported `scripts/citing_set*.py` includes O_NOCTTY.
Environment: without /dev/pts or openpty, F06 fails closed (line 342) rather than passing falsely. Tested only on this host.

H7. The contract leaves the fixture side unfinished; this is not a counter false pass. Git cannot store a FIFO or an empty directory, so R01 and R04 cannot be committed as static working-tree fixtures (a directory as population.json does work for R01). The contracted runner command passes no `--revision`, so R07 and R08 cannot be fixtured. In the counter's exported tree, which has no `.git`, an R08 fixture using `--revision HEAD` yields revision_not_found instead of root_not_repository_top_level. To reach 14/14 I needed the uncontracted `setup.mkdir`, `setup.gitSub` and `args` fields. Builders will invent divergent versions.
Correction: the L1 should add a fixture-setup and extra-argument clause to the interface contract.

## Attacks tried that did not produce a false pass
- Reason names built at run time: `compared` requires `renamedOccurrences > 0` (line 448), so the check fails rather than passes falsely. I read this from the code and did not build a stub; H2 is the live version of this attack.
- Constant clean and refuse-everything gates: both scored 0/14 in both runs; observed.
- A runner that compares reasons for only some cases: subsumed by H2, where the runner compares reasons for no case and still passes.

## Not verified
Any C1 build by another seat (none was read); other kernels or Python versions for F06; a counter run with the corrections applied.
No installs or updates. No live network. No lane-tracked files written; this report is the only lane write.
