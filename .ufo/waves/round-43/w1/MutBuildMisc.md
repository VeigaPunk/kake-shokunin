SURVIVED: 6 of 8 one-member entry/exit-handling mutants meet C1's frozen predicate under counter v4 (11/11 on two seeds each); only the two output-observable mutants were killed.

# Scope and controls
Attack: build 020bc4574729ed674299f6cab02faac1582d9464, scripts/sitemap_audit.py sha256 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021 (read-only git show); area: entry/exit handling. Counter .ufo/waves/round-43/c43_count_v4.py sha256 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab.
Baseline: pristine bytes met=true, 11/11, seed 262089020222497 (pristine-baseline.json) — green baseline, so survival is not an artifact. Reference round-41 tool 50287ac6... verified from git by the counter at scoring time.
No tools installed, no network, no lane writes. Artefacts under /fast/scratch/hyaku/kake-r43/MutBuildMisc/.

# Command (per mutant; timeout 900, prlimit --as=8000000000, no --seed)
python3 -B .ufo/waves/round-43/c43_count_v4.py --root <lane> --tool-file <mutant>.py \
  --label MutBuildMisc-<mutant> --out <mutant>.json
Exit codes: 1 for M1, M6 (not met); 0 for M2, M3, M4, M5, M7, M8 and pristine (met).

# Mutants — all single-hunk, compile-checked, one member each
| mutant / build.py line | one-member change | sha256 | equalRuns, met (seed) | verdict |
|---|---|---|---|---|
| M1_exitfindings:35 | class member: `EXIT_FINDINGS = 1` -> `0` | a25dae3742e2a8beabdd4e8960933ff0f887458ef3b1e919e40a80c44e0547d8 | 7/11, false (14890596587925) | KILLED |
| M2_argvbound:616 | boundary: `len(argv) != 3` -> `len(argv) < 3` | 2e1e96d9846d911bda62295bc3ccf3aefc2ac72d51e0e3ca5172bc8f80d4f9c0 | 11/11, true (102135883016709; 65345067779101) | SURVIVED |
| M3_dropchecksempty:550 | branch condition: drop `or not checks` | 1fe35266ac04a2e9d2ed86bc60ebdfd7be52b15da7e5cfce5ba11ad63d127617 | 11/11, true (257592044019014; 204868616768914) | SURVIVED |
| M4_bomstrip:534-535 | branch: delete BOM strip in `_load_manifest` | 305bd57c27a7b512467a5d9e3935569a104262dab5f450bd8b302a60fff579df | 11/11, true (25743683027506; 78152104079704) | SURVIVED |
| M5_ensureascii:606 | formatting member: `ensure_ascii=True` -> `False` | 4f8cc255add777f8a4e1b9f1483f26d2fc6587d931e3eb630a83ef5664432612 | 11/11, true (174935987945679; 34864168934441) | SURVIVED |
| M6_newline:606 | formatting member: drop trailing `+ "\n"` | 7e72cb7e41f39a6fbd68a861bf7b1834aa4f8403162016fc5a0b4e5ccd435d38 | 0/11, false (211904159239995) | KILLED |
| M7_fileunreadable:411 | class member: error string `file_unreadable` -> `file_unreadable_x` | 85aae2ca756a60f21e2b9fd41933c7fbc710be15726c00cf08ef0b3f8e9ffd57 | 11/11, true (93466332564388; 101728868945955) | SURVIVED |
| M8_cannotcode:612 | exit member: `_cannot` returns `EXIT_USAGE` not `EXIT_CANNOT` | 37752efbb61800a6ca8f8f6214d03a8305dad1d73de531523d5d20a8c89fe321 | 11/11, true (118173619126750; 114353482663617) | SURVIVED |

Kill detail: M1 — T1-T4 ref41Exit 1 vs candExit 0, candRepsEqual 0/5 (A-F and T5 stay equal because
they exit 2); M6 — A-F and T1-T5 all unequal on stdout bytes. Each receipt is its own file
(M<name>.json, M<name>-s2.json); witnesses.json holds the survivor witnesses.

# Survivor witnesses (round-41 tool vs mutant, same args, outside counter's generated runs)
- M2: argv `--manifest m.json extra` -> ref exit 64, empty stdout; mutant exit 2, full document.
- M3: manifest `{"version":1,"checks":[]}` -> ref exit 2 `input_invalid`; mutant exit 0 `clean`, checks [].
- M4: manifest with UTF-8 BOM + missing named file -> ref emits per-check `file_unreadable`; mutant
  exit 2 `input_invalid` (json.loads rejects BOM).
- M5: check id `café` -> ref stdout `"caf\u00e9"` (escaped); mutant raw UTF-8 `"café"`; same exit 2.
- M7: named file absent -> ref error `file_unreadable`; mutant `file_unreadable_x` (build.py:411 unreached).
- M8: manifest version 2 -> same bytes, ref exit 2, mutant exit 64 (build.py:612 unreached).

# Findings (holds / overstated / wrong)
- Counter compares exit code and stdout bytes on every equality run (c43_count_v4.py:913-940): holds.
- "Counter v4 covers the tool's entry/exit handling": overstated. Its only reachable entry/exit paths
  are a valid manifest, existing files, exactly `--manifest <path>`, ASCII ids.
- "Manifest faults are covered": wrong. Every generated manifest is `{"version": 1, checks: [...]}`
  with non-empty checks (c43_count_v4.py:565,641,733,751,822); build.py:534-550,610-612 unreachable.
- "Missing files are covered": wrong. Every named file is written before the run
  (c43_count_v4.py:536-560,633,708-742,806-851); build.py:411 (file_unreadable) is never reached.
- "Output formatting lines are covered": partially. The trailing newline (build.py:606) and the
  EXIT_FINDINGS member (build.py:35, via findings-only T1-T4) are compared; the ensure_ascii branch
  is not, because every equality-run id is ASCII (tok(), c43_count_v4.py:123-124).

# Restoration
No lane file was touched. Pristine sandbox copy sha256 914ebdee...cd021 before and after all probing;
mutants exist only as copies in the sandbox. No process left running.

Conclusion: C1's predicate is met by the build (pristine 11/11), but at v4 strength the counter does
not test manifest faults, missing-file handling, the usage argv boundary, the cannot-evaluate exit
code, or output escaping — six live defects in that area would pass. This is a counter-coverage
finding, not a contract change.
