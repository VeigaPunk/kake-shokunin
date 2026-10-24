# CriticKillRules — C1 kill rules 1–4

## Scope and axes

Axes: **operability** (control attribution, semantic witnessing, build repeatability, non-circular generation) and **freshness** (accurate receipt/provenance presentation only; no C2 adjudication).

Read-only critic review, not a canonical judgment. No counter, candidate tool, class module, test suite, judge, or other UFO runtime was executed by this seat. Python scripts below only parse source/JSON and read the held build's Git object.

The L1 clarified that round-44's evidence set is the **uncommitted frozen working copy plus declared SHA-256 pins**, not paths present at HEAD. HEAD was `18cb2c28f47c3ec3732ffa06c456e61b3444b1a2`; neither HEAD nor the two inspected reachable snapshot objects contained the requested round-44 paths. The held build's revision object `020bc4574729ed674299f6cab02faac1582d9464` is readable and its tool bytes hash to `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`. I do not describe the reviewed round-44 working files as already committed.

## Named attacks: initial evidence

| Attack | Result | Decisive evidence |
|---|---|---|
| 1: remaining family/class misattribution | **PASS: none found across 27 source/TSV pairs.** | All control hashes match; `buildport-m6` is now `default_port/G2`. Its source inverts `port is None` to `port is not None`, not a port-digit memo. |
| Kill rule 1: every registered control witnessed | **FAIL in the original named summary.** | `after-v5.json` says `witnessed=23/27`, `ok=false`; casememo-v3/v4/v7/v8 each have `met=true`, `21/21`, empty `caughtBy` and `classCaught`. This is existing evidence, not a new score. |
| 2: timing-only or otherwise false witness | **PASS on recovered original: no timing-only, legacy-only, or counter-error witness. FAIL shared-directory auditability.** | The preserved original cohort substantiates all 23 claimed names with actual G stdout divergence and all 27 receipt identities match. Independently, the live extraction caught 17 row/receipt inconsistencies in a mixed 8-v4/19-v5 directory. That capture is NOT a coherent new 14/27 score; both observations are preserved below. |
| 3: fixed-seed/cache build runs | **PASS the falsification attempt, with a provenance limit.** | All three original claim build receipts are met, `21/21`, with distinct seeds and distinct reference output hashes on every run key. Three placebo build receipts also have distinct seeds. Audit source supplies no `--seed`; counter defaults to `os.urandom(6)`. Receipts record a seed number, NOT seed origin, argv, or cache-use evidence, so they cannot independently prove historical unseeded invocation or absence of reuse. |
| 4: runtime reads of control source by classes | **PASS: no circular runtime file read found in the inspected ten modules.** | No imports, open/read calls, dynamic-execution calls, or controls-r43 string literals. Their five counter helper calls are generation-only helpers and contain no such I/O. Module hashes are recorded below. |

### Strongest new counterexample: simultaneous audit cohorts destroy provenance

The original `verification/claim/after-v5.json` pins `portlen-v1` to seed **4615886500219**, `met=false`, equality **19/21**, `caughtBy=[G1,G10]`, receipt `tools/portlen-v1.json`. A later direct read of that linked file returned this verbatim result:

```json
{
  "classesMode": "v4",
  "seed": 173982992146176,
  "met": true,
  "equalRuns": "11/11",
  "counterSha256": "5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc",
  "toolSha256": "752a8de5baba3d14f8edb8e77052c0f8dd164f814c4c74c2922283abda5d7df6",
  "classRuns": [],
  "note": null
}
```

That receipt cannot substantiate that summary row. The original summary SHA-256 remained `2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902` in the extraction. Earlier direct reads had seen v5 receipts at the same paths, including `portlen-v4`'s G1 stdout divergence and `repeat-len-band`'s G7 plus C/T5 divergences. The later mismatch is therefore not grounds to invent a replacement score or infer that the original witness was timing-only.

Root cause is visible in the frozen driver, verbatim tool-search output:

```text
130:    outdir = os.path.dirname(os.path.abspath(a.out))
131:    tools_dir = os.path.join(outdir, "tools")
148:        out = os.path.join(tools_dir, row["name"] + ".json")
174:            out = os.path.join(outdir, "build-%d.json" % (i + 1))
```

The wave-2 assignments give baseline, placebo, v4 support and canary summaries different filenames **under the same `verification/claim/` parent**. They therefore share `tools/<control>.json`; baseline build receipts also reuse `build-1.json` through `build-3.json`. Different summary basenames are not isolation. Reads during concurrent writes are a mixed observation, not an atomic cohort snapshot.

The L1 confirmed this as an instrument defect and directed that this failure be preserved, the frozen driver remain unedited, and each decisive cohort be rerun in its own output directory. This seat changed none of those files.

### Attribution and limits, not identity changes

All 27 source mechanisms were inspected directly, using CONTROL/comment blocks where present and the actual mutated statements for the four build mutants. Source ranges reviewed:

- portlen-v1 328–361; portlen-v5 328–372; portlen-v4 328–367.
- buildscheme-M5 286–310; buildscope-m5 291–310; buildscope-m4 501–516; buildport-m6 286–310.
- headtail-V1/V2/V7 and prefixcache-p48 284–313; headtail-V4/V8 284–312.
- casememo-v3/v4 211–236; casememo-v7/v8 287–335.
- all five repeat controls 212–237.
- hosttable-A/B 345–383; hosttable-F 332–367.
- both portvalue controls 287–335.

`headtail-V2` really caches first48+last48; G5 explicitly constructs equal-end/different-middle pairs, so it is not a second misattribution. `portlen-v4` really drops port digits from its cache key and retains digit count: G9 remains an accurate mechanism label even though the original receipt's actual catch is **G1 only**. That is a cross-class witness, not proof that G9 caught this specimen. Do not relabel its source mechanism to make the receipt appear aligned.

G8 embeds literal hosts from the known tables but does not read those control files at runtime. That passes the named circularity attack. Generalization from a finite, known 27-specimen cohort to every possible shortcut/table is a separate claim the canonical judge must not infer.

### Build-seed/cache limits

The original claim build seeds are **179061606630571, 189368299344378, 249576241445357**. All three receipts match the held build hash and revision, have no note, equality `21/21`, and five candidate/five baseline CPU samples for each timing shape. Their largest exact ratios are 1.308772, 1.363835 and 1.301408. The three placebo build seeds are different again. Distinct seeds/hashes refute reuse of one identical receipt, but do not prove that three different fixed seeds were not supplied outside the audited driver.

Static evidence: `c44_audit.py:48–54,173–175` launches fresh counter subprocesses without `--seed`; `c44_count_v5.py:995` chooses OS entropy when none is supplied; `1036–1045` creates a fresh RNG/tempdir; `933–955` launches a new sandbox process per run with a cleared environment and a fresh tmpfs, not a result-cache reader. Process-global dictionaries in the **controls** are the shortcut specimens under attack, not build-result caches. None of these source observations reconstructs a missing historical argv log.

## Exact local commands and tool searches

All Bash commands ran with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`:

```sh
mkdir -p /fast/scratch/hyaku/kake-r44/CriticKillRules
git rev-parse --show-toplevel HEAD
git ls-tree -r --name-only 18cb2c28f47c3ec3732ffa06c456e61b3444b1a2 -- .ufo/waves/round-44/classes .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/verification/claim .ufo/waves/round-44/verification/tools
git log --all -8 --format='%H %s'
git show --no-patch --format=fuller 18cb2c28f47c3ec3732ffa06c456e61b3444b1a2 020bc4574729ed674299f6cab02faac1582d9464
git show --no-patch --format=fuller df3e45021002cb0b3dcccd9d3541eb3e2b07d575 2dde92b28b49042764c8e112de5986c476c27445
git ls-tree -r --name-only df3e45021002cb0b3dcccd9d3541eb3e2b07d575 -- .ufo/waves/round-44/classes .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/verification/claim .ufo/waves/round-44/verification/tools
git ls-tree -r --name-only 2dde92b28b49042764c8e112de5986c476c27445 -- .ufo/waves/round-44/classes .ufo/waves/round-44/controls-27.tsv .ufo/waves/round-44/verification/claim .ufo/waves/round-44/verification/tools
python3 -B /fast/scratch/hyaku/kake-r44/CriticKillRules/audit_receipts.py
```

The extractor internally runs only `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py` and hashes its returned bytes. It never executes them.

Specialized `grep` calls, rather than shell grep, searched:

- `controls-r43/*.py`: `CONTROL` (case-sensitive), then `control` (case-insensitive, pages skip=0 and skip=20).
- `classes/g*.py`: `controls-r43|controls_r43|round-43|round_43|\bopen\s*\(|\bread(?:_text|_bytes)?\s*\(|\bimport\b|\bexec\s*\(|\beval\s*\(|\bgetattr\s*\(|\b__import__\s*\(`, case-insensitive. Only harmless round-43 documentation mentions matched. The subsequent AST pass covers all ten registered modules and their actual helper call set.
- `c44_audit.py`: `outdir =|tools_dir =|out = os\.path\.join\(tools_dir|out = os\.path\.join\(outdir`.
- `w2-spec.json`: `--out|verification/claim|verification/v4|verification/after`.

`read` inspected the source ranges above, counter class loading/generation/sandbox code, the full audit driver, original claim inline rows and build metadata, inherited v4 receipts, and source-derived round-43 mechanism references. Dead ends: Git trees contained no r44 evidence, as subsequently explained by L1; an optional guessed historical report name was missing; initial JSON queries using `.tasks`/`.task` did not match the wave-spec schema. None was used as evidence of absence.

## Verbatim decisive extractor output (initial, contaminated capture)

These are complete decisive lines copied from the command, not a rewritten score. The extractor reads sequentially while other seats write; its mixed receipt counts cannot be treated as one completed cohort.

```text
AXES operability; freshness (receipt/provenance accuracy only)
EVIDENCE on-disk frozen r44 working copy; held build read from Git object
PIN c44_count_v5.py sha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc matches=True
PIN c44_audit.py sha256=8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75 matches=True
PIN controls-27.tsv sha256=a1f0e364dad5ff937666966a16622e6895591a2eb3db714d6ecf3f3948c31bf8
MAP portlen-v1 declared=portlen/G1 source=portlen/G1 shaMatch=True
MAP portlen-v5 declared=portlen/G1 source=portlen/G1 shaMatch=True
MAP buildscheme-M5 declared=default_port/G2 source=default_port/G2 shaMatch=True
MAP buildscope-m5 declared=empty_path/G3 source=empty_path/G3 shaMatch=True
MAP buildscope-m4 declared=port_scope/G4 source=port_scope/G4 shaMatch=True
MAP headtail-V1 declared=prefix/G5 source=prefix/G5 shaMatch=True
MAP headtail-V2 declared=prefix/G5 source=prefix/G5 shaMatch=True
MAP headtail-V7 declared=prefix/G5 source=prefix/G5 shaMatch=True
MAP prefixcache-p48 declared=prefix/G5 source=prefix/G5 shaMatch=True
MAP casememo-v3 declared=fold/G6 source=fold/G6 shaMatch=True
MAP casememo-v4 declared=fold/G6 source=fold/G6 shaMatch=True
MAP casememo-v7 declared=fold/G6 source=fold/G6 shaMatch=True
MAP casememo-v8 declared=fold/G6 source=fold/G6 shaMatch=True
MAP repeat-len-band declared=band/G7 source=band/G7 shaMatch=True
MAP repeat-depth-band declared=band/G7 source=band/G7 shaMatch=True
MAP repeat-defpos-band declared=band/G7 source=band/G7 shaMatch=True
MAP repeat-depth-deep declared=band/G7 source=band/G7 shaMatch=True
MAP repeat-defpos-late declared=band/G7 source=band/G7 shaMatch=True
MAP hosttable-A declared=host/G8 source=host/G8 shaMatch=True
MAP hosttable-B declared=host/G8 source=host/G8 shaMatch=True
MAP hosttable-F declared=host/G8 source=host/G8 shaMatch=True
MAP portvalue-digits declared=portdigit/G9 source=portdigit/G9 shaMatch=True
MAP portvalue-digits-67 declared=portdigit/G9 source=portdigit/G9 shaMatch=True
MAP portlen-v4 declared=portdigit/G9 source=portdigit/G9 shaMatch=True
MAP buildport-m6 declared=default_port/G2 source=default_port/G2 shaMatch=True
MAP headtail-V4 declared=window/G10 source=window/G10 shaMatch=True
MAP headtail-V8 declared=window/G10 source=window/G10 shaMatch=True
ATTRIBUTION rows=27 sourceMismatches=[] hashMismatches=[]
PIN verification/claim/after-v5.json sha256=2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902
CLAIM controls=27 witnessed=23 ok=False verdict=witnessed 23/27 notMet=23 build met 3/3
RECEIPT_PATH claim-relative={"v4": 8, "v5": 19} root-verification/tools={"v4": 27}
KR1_UNWITNESSED casememo-v3,casememo-v4,casememo-v7,casememo-v8
KR2 claimed=23 genuineClassStdoutDivergences=14 timingOnly=[] legacyOnly=[] counterErrors=[] summaryInconsistencies=['portlen-v1', 'portlen-v5', 'buildscheme-M5', 'buildscope-m5', 'buildscope-m4', 'headtail-V1', 'headtail-V2', 'headtail-V7', 'prefixcache-p48', 'casememo-v3', 'casememo-v4', 'casememo-v7', 'casememo-v8', 'repeat-len-band', 'repeat-depth-band', 'repeat-defpos-band', 'repeat-depth-deep']
HELD_BUILD revision=020bc4574729ed674299f6cab02faac1582d9464 sha256=914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021
BUILD claim/build-1.json seed=179061606630571 met=True equal=21/21 maxRatio=1.308772 note=None toolHashMatch=True revisionMatch=True unequal=[] cpuSamples=[(5, 5), (5, 5), (5, 5), (5, 5), (5, 5)] provenanceKeys=['seed']
BUILD claim/build-2.json seed=189368299344378 met=True equal=21/21 maxRatio=1.363835 note=None toolHashMatch=True revisionMatch=True unequal=[] cpuSamples=[(5, 5), (5, 5), (5, 5), (5, 5), (5, 5)] provenanceKeys=['seed']
BUILD claim/build-3.json seed=249576241445357 met=True equal=21/21 maxRatio=1.301408 note=None toolHashMatch=True revisionMatch=True unequal=[] cpuSamples=[(5, 5), (5, 5), (5, 5), (5, 5), (5, 5)] provenanceKeys=['seed']
BUILD_REFERENCE_HASH_DIVERSITY claim {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G1": 3, "G10": 3, "G2": 3, "G3": 3, "G4": 3, "G5": 3, "G6": 3, "G7": 3, "G8": 3, "G9": 3, "T1": 3, "T2": 3, "T3": 3, "T4": 3, "T5": 3}
BUILD placebo/build-1.json seed=49601489066767 met=True equal=21/21 maxRatio=1.338564 note=None toolHashMatch=True revisionMatch=True unequal=[] cpuSamples=[(5, 5), (5, 5), (5, 5), (5, 5), (5, 5)] provenanceKeys=['seed']
BUILD placebo/build-2.json seed=21933982208200 met=True equal=21/21 maxRatio=1.355204 note=None toolHashMatch=True revisionMatch=True unequal=[] cpuSamples=[(5, 5), (5, 5), (5, 5), (5, 5), (5, 5)] provenanceKeys=['seed']
BUILD placebo/build-3.json seed=107355758038766 met=True equal=21/21 maxRatio=1.319080 note=None toolHashMatch=True revisionMatch=True unequal=[] cpuSamples=[(5, 5), (5, 5), (5, 5), (5, 5), (5, 5)] provenanceKeys=['seed']
BUILD_REFERENCE_HASH_DIVERSITY placebo {"A": 3, "B": 3, "C": 3, "D": 3, "E": 3, "F": 3, "G1": 3, "G10": 3, "G2": 3, "G3": 3, "G4": 3, "G5": 3, "G6": 3, "G7": 3, "G8": 3, "G9": 3, "T1": 3, "T2": 3, "T3": 3, "T4": 3, "T5": 3}
BUILD_SEEDS distinct=6/6
COUNTER_SEED_EXPRESSION a.seed if a.seed is not None else int.from_bytes(os.urandom(6), 'big')
AUDIT_RUN_COUNTER suppliesSeedArgument=False; receipts record neither seed-origin nor cache-use nor invocation argv
CLASS G1 g1_longport_grammar.py sha256=23b7df085509abad950f960c5aefd8ecd00876bb0b0464df0b926bf821148854 imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G2 g2_default_port.py sha256=5ac93f570a65ad98b2fe3afdfbbc448fcc19b333c2fd6ba99f8a2b9e43031194 imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G3 g3_empty_path.py sha256=c108356c24aa924ae4c6c0a48e0df1526d174e66f3c58f38df8d7cd354009578 imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G4 g4_port_scope.py sha256=53fe7bfa8968112da8b2708920254deb39523f877f7ecb129d5336f174c37e1b imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G5 g5_prefix_cut_45plus.py sha256=50765682e1d27cfee6d106370e7d4989f7a512cb882d8b6c31a7eb414e0bc1b2 imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G6 g6_fold_pairs.py sha256=f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G7 g7_band_memos.py sha256=06e5a6a086a63f228f71113e4b11fa6ebb418593be1bdebdf173b3a5ff182c33 imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G8 g8_host_tables.py sha256=6385a4c040ed83c01fb010b2ac12724e9a9e4863398768a33a0d41c9b472ea4b imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G9 g9_port_digits.py sha256=0e1d294648aae5fdca6a0333a4dc2db14ac70059bcf79c0547c1e1028fa78453 imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS G10 g10_headtail_windows.py sha256=c2986c3726c0a963aac8e3ec8ea6645cae966b89987568f12187ad23e5bc296f imports=[] ioOrDynamicCalls=[] controlPathLiterals=[]
CLASS_HELPERS fill,long_port,rcase,short_url,tok
KR4 modules=10 circularCandidates=[] helperIoOrDynamicCalls=[]
REVIEW_MODE static source/receipt inspection only; no counter/build/class execution; no canonical judgment
```

## Recovered original cohort: all 23 witnesses are semantic

ExecAfterBaseline cited its pre-run backup at `/fast/scratch/hyaku/kake-r44/ExecAfterBaseline/l1-after-v5-backup/`. This seat read it without modifying it. Its summary has the same SHA-256 as the original claim summary. Unlike the collided live directory, these preserved linked receipts substantiate all 23 original witnesses. Every claimed G catch has a different stdout hash, so this is not inference from `met=false` or from a timing ratio. `repeat-len-band` has a real G7 difference in addition to C/T5 differences; its G7 witness is not disqualified by legacy catches under the declared mixed-key reading. Four casememo controls remain genuinely unwitnessed.

Exact command:

```sh
python3 -B /fast/scratch/hyaku/kake-r44/CriticKillRules/check_cohort.py /fast/scratch/hyaku/kake-r44/ExecAfterBaseline/l1-after-v5-backup/after-v5.json
```

Verbatim decisive output:

```text
COHORT /fast/scratch/hyaku/kake-r44/ExecAfterBaseline/l1-after-v5-backup/after-v5.json sha256=2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902 mode=v5 controls=27 witnessed=23 notMet=23 ok=False errors=[]
  ROW portlen-v1 seed=4615886500219 met=False equal=19/21 classes=G1,G10 legacy=- stdoutDiff=G1,G10 exitDiff=G1,G10 note=None identitiesMatch=True
  ROW portlen-v5 seed=198910954065337 met=False equal=19/21 classes=G1,G10 legacy=- stdoutDiff=G1,G10 exitDiff=- note=None identitiesMatch=True
  ROW buildscheme-M5 seed=236129566264534 met=False equal=20/21 classes=G2 legacy=- stdoutDiff=G2 exitDiff=G2 note=None identitiesMatch=True
  ROW buildscope-m5 seed=58350418381865 met=False equal=20/21 classes=G3 legacy=- stdoutDiff=G3 exitDiff=- note=None identitiesMatch=True
  ROW buildscope-m4 seed=108772845014364 met=False equal=19/21 classes=G4,G9 legacy=- stdoutDiff=G4,G9 exitDiff=G4 note=None identitiesMatch=True
  ROW headtail-V1 seed=73542651892409 met=False equal=19/21 classes=G5,G7 legacy=- stdoutDiff=G5,G7 exitDiff=- note=None identitiesMatch=True
  ROW headtail-V2 seed=198479021916740 met=False equal=19/21 classes=G5,G7 legacy=- stdoutDiff=G5,G7 exitDiff=- note=None identitiesMatch=True
  ROW headtail-V7 seed=107190109943535 met=False equal=19/21 classes=G5,G7 legacy=- stdoutDiff=G5,G7 exitDiff=- note=None identitiesMatch=True
  ROW prefixcache-p48 seed=194133481817131 met=False equal=19/21 classes=G5,G7 legacy=- stdoutDiff=G5,G7 exitDiff=- note=None identitiesMatch=True
  ROW casememo-v3 seed=37611002469796 met=True equal=21/21 classes=- legacy=- stdoutDiff=- exitDiff=- note=None identitiesMatch=True
  ROW casememo-v4 seed=147120660939040 met=True equal=21/21 classes=- legacy=- stdoutDiff=- exitDiff=- note=None identitiesMatch=True
  ROW casememo-v7 seed=123595050640513 met=True equal=21/21 classes=- legacy=- stdoutDiff=- exitDiff=- note=None identitiesMatch=True
  ROW casememo-v8 seed=82003496704499 met=True equal=21/21 classes=- legacy=- stdoutDiff=- exitDiff=- note=None identitiesMatch=True
  ROW repeat-len-band seed=187179068777863 met=False equal=18/21 classes=G7 legacy=C,T5 stdoutDiff=G7 exitDiff=- note=None identitiesMatch=True
  ROW repeat-depth-band seed=198137707594239 met=False equal=20/21 classes=G7 legacy=- stdoutDiff=G7 exitDiff=- note=None identitiesMatch=True
  ROW repeat-defpos-band seed=88528679686849 met=False equal=20/21 classes=G7 legacy=- stdoutDiff=G7 exitDiff=- note=None identitiesMatch=True
  ROW repeat-depth-deep seed=176409570659924 met=False equal=20/21 classes=G7 legacy=- stdoutDiff=G7 exitDiff=- note=None identitiesMatch=True
  ROW repeat-defpos-late seed=187110366188425 met=False equal=20/21 classes=G7 legacy=- stdoutDiff=G7 exitDiff=- note=None identitiesMatch=True
  ROW hosttable-A seed=171691956040788 met=False equal=20/21 classes=G8 legacy=- stdoutDiff=G8 exitDiff=G8 note=None identitiesMatch=True
  ROW hosttable-B seed=154531073456578 met=False equal=20/21 classes=G8 legacy=- stdoutDiff=G8 exitDiff=G8 note=None identitiesMatch=True
  ROW hosttable-F seed=227466094467482 met=False equal=20/21 classes=G8 legacy=- stdoutDiff=G8 exitDiff=- note=None identitiesMatch=True
  ROW portvalue-digits seed=165981742274513 met=False equal=19/21 classes=G2,G9 legacy=- stdoutDiff=G2,G9 exitDiff=G2 note=None identitiesMatch=True
  ROW portvalue-digits-67 seed=145012289665654 met=False equal=20/21 classes=G9 legacy=- stdoutDiff=G9 exitDiff=- note=None identitiesMatch=True
  ROW portlen-v4 seed=33524905891364 met=False equal=20/21 classes=G1 legacy=- stdoutDiff=G1 exitDiff=- note=None identitiesMatch=True
  ROW buildport-m6 seed=192327699929616 met=False equal=18/21 classes=G2,G4,G9 legacy=- stdoutDiff=G2,G4,G9 exitDiff=G2,G4 note=None identitiesMatch=True
  ROW headtail-V4 seed=123278255537009 met=False equal=19/21 classes=G1,G10 legacy=- stdoutDiff=G1,G10 exitDiff=- note=None identitiesMatch=True
  ROW headtail-V8 seed=202638500963215 met=False equal=20/21 classes=G10 legacy=- stdoutDiff=G10 exitDiff=- note=None identitiesMatch=True
  WITNESS_CHANNELS claimed=23 genuine=23 timingOnly=[] legacyOnly=[] invalid=[] identityMismatches=[] namedClassMisses=['casememo-v3', 'casememo-v4', 'casememo-v7', 'casememo-v8', 'portlen-v4']
  BUILD 1 revision=020bc4574729ed674299f6cab02faac1582d9464 seed=179061606630571 met=True equal=21/21 maxRatio=1.308772 note=None identitiesMatch=True provenanceKeys=['seed']
  BUILD 2 revision=020bc4574729ed674299f6cab02faac1582d9464 seed=189368299344378 met=True equal=21/21 maxRatio=1.363835 note=None identitiesMatch=True provenanceKeys=['seed']
  BUILD 3 revision=020bc4574729ed674299f6cab02faac1582d9464 seed=249576241445357 met=True equal=21/21 maxRatio=1.301408 note=None identitiesMatch=True provenanceKeys=['seed']
  BUILD_LINKS seeds=[179061606630571, 189368299344378, 249576241445357] unique=3/3 identityMismatches=[]
READ_ONLY no lane counter/build/class execution; not a canonical verdict
```

## Final isolated cohorts — completed receipt review

On the L1's close-out instruction, this seat read the completed `after-final/` and `canary-final/` cohorts once; no new scoring or subtask was started. Their inline rows and linked receipt identities agree. **Kill-rule attacks 1–4 find no current source misattribution, invalid/timing-only witness, failed recorded build run, or circular class read in these final artifacts.** The final after cohort has **27/27 genuine class stdout divergences**, including all four casememo controls, and three recorded met builds. This is a review of supplied evidence, not admission of C1 or a canonical verdict.

The final G6 source was read at lines 1–59. It generates IP-zone and first-path-segment fold pairs using only RNG/string operations; it imports nothing and reads no control file. Its SHA-256 differs from the initial G6, as expected. A focused circularity search returned `No matches found`. The final portlen-v4 catches are **G1 and G6**, still not G9: retain the portdigit/G9 source label, but do not invent a G9 catch.

Exact commands:

```sh
python3 -B /fast/scratch/hyaku/kake-r44/CriticKillRules/check_cohort.py .ufo/waves/round-44/verification/claim/after-final/after-v5.json .ufo/waves/round-44/verification/claim/canary-final/canary.json
sha256sum .ufo/waves/round-44/classes/g6_fold_pairs.py
```

Verbatim decisive output excerpts:

```text
COHORT .ufo/waves/round-44/verification/claim/after-final/after-v5.json sha256=9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1 mode=v5 controls=27 witnessed=27 notMet=27 ok=True errors=[]
  ROW casememo-v3 seed=51991230635285 met=False equal=20/21 classes=G6 legacy=- stdoutDiff=G6 exitDiff=- note=None identitiesMatch=True
  ROW casememo-v4 seed=66763655055034 met=False equal=20/21 classes=G6 legacy=- stdoutDiff=G6 exitDiff=- note=None identitiesMatch=True
  ROW casememo-v7 seed=149260863541903 met=False equal=20/21 classes=G6 legacy=- stdoutDiff=G6 exitDiff=- note=None identitiesMatch=True
  ROW casememo-v8 seed=22899741442922 met=False equal=20/21 classes=G6 legacy=- stdoutDiff=G6 exitDiff=- note=None identitiesMatch=True
  ROW repeat-len-band seed=187926495163792 met=False equal=19/21 classes=G7 legacy=T5 stdoutDiff=G7 exitDiff=- note=None identitiesMatch=True
  ROW portlen-v4 seed=40135015234810 met=False equal=19/21 classes=G1,G6 legacy=- stdoutDiff=G1,G6 exitDiff=- note=None identitiesMatch=True
  WITNESS_CHANNELS claimed=27 genuine=27 timingOnly=[] legacyOnly=[] invalid=[] identityMismatches=[] namedClassMisses=['portlen-v4']
  BUILD 1 revision=020bc4574729ed674299f6cab02faac1582d9464 seed=93543170178044 met=True equal=21/21 maxRatio=1.355205 note=None identitiesMatch=True provenanceKeys=['seed']
  BUILD 2 revision=020bc4574729ed674299f6cab02faac1582d9464 seed=234322826174562 met=True equal=21/21 maxRatio=1.325697 note=None identitiesMatch=True provenanceKeys=['seed']
  BUILD 3 revision=020bc4574729ed674299f6cab02faac1582d9464 seed=96267491316273 met=True equal=21/21 maxRatio=1.337283 note=None identitiesMatch=True provenanceKeys=['seed']
  BUILD_LINKS seeds=[93543170178044, 234322826174562, 96267491316273] unique=3/3 identityMismatches=[]
COHORT .ufo/waves/round-44/verification/claim/canary-final/canary.json sha256=cf16e8ee3e12e2f0ecc1db830e63dc5153de82340989296a8205a3adc943b148 mode=v5 controls=5 witnessed=3 notMet=5 ok=True errors=[]
  ROW r42ctl-M8-port-five-digits seed=85929108625596 met=False equal=15/21 classes=G1,G3,G9,G10 legacy=F,T3 stdoutDiff=G1,G3,G9,G10 exitDiff=G3,G9,G10 note=None identitiesMatch=True
  ROW r42ctl-v1_casefold seed=209294289829574 met=False equal=19/21 classes=- legacy=F,T2 stdoutDiff=- exitDiff=- note=None identitiesMatch=True
  ROW r42ctl-v2_prefix32 seed=84488226294537 met=False equal=13/21 classes=G1,G5,G6,G7,G9,G10 legacy=F,T3 stdoutDiff=G1,G5,G6,G7,G9,G10 exitDiff=G5 note=None identitiesMatch=True
  ROW r42ctl-v4_hosttable seed=217256610054643 met=False equal=19/21 classes=- legacy=F,T3 stdoutDiff=- exitDiff=- note=None identitiesMatch=True
  ROW r44ctl-junk-constant seed=51503988362367 met=False equal=0/21 classes=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 legacy=A,B,C,D,E,F,T1,T2,T3,T4,T5 stdoutDiff=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 exitDiff=G1,G3,G4,G5,G6,G7,G8,G9,G10 note=None identitiesMatch=True
  WITNESS_CHANNELS claimed=3 genuine=3 timingOnly=[] legacyOnly=[] invalid=[] identityMismatches=[] namedClassMisses=['r42ctl-M8-port-five-digits', 'r42ctl-v1_casefold', 'r42ctl-v2_prefix32', 'r42ctl-v4_hosttable', 'r44ctl-junk-constant']
  BUILD_LINKS seeds=[] unique=0/0 identityMismatches=[]
READ_ONLY no lane counter/build/class execution; not a canonical verdict
cddc5c7d862addbe4087b6bf4e741df4014ed5c2d5c70896ae78a42e86cda0e8  .ufo/waves/round-44/classes/g6_fold_pairs.py
```

`namedClassMisses` is informational, not an extra predicate: the declared gate accepts any registered G catch. Canary labels are not G keys, so their entries in that informational list do not invalidate `notMet=5/5`. Two canaries fail only legacy runs; none meets the counter. The L1 reported audit exit 0 for both final cohorts; those audit processes were **not run by this seat**.

**Dependency finding at close-out:** `read verification/claim/placebo-final/` showed an in-progress `tools/` directory but no completed summary; `read verification/claim/v4-final/` returned `(empty directory)`. The L1 explicitly said these two reruns were still in progress after an argparse fix and instructed immediate return without waiting. Their final counts/exits are **unreviewed**, not assumed. This does not change the completed after/canary findings, and it prevents this report from asserting the entire before/after claim complete.

## Smallest safe correction and classification

1. **Fixable evidence defect:** leave the frozen audit driver untouched. Give each audit invocation a unique **parent directory**, not merely a unique output basename; retain each summary with its own `tools/` and `build-N.json` files. The L1 named `verification/claim/{after-final,placebo-final,v4-final,canary-final}/`. Preserve the collided historical summary and this failure evidence; cite new isolated receipts rather than silently treating old paths as repaired.
2. **G6 correction observed, not inferred:** the assigned owner changed `classes/g6_fold_pairs.py`; the L1's isolated final cohort supplies all four new G6 stdout divergences plus full-cohort/build evidence above. Preserve the original 23/27 receipt and record the final module hash rather than retroactively attributing its old rows to the new class bytes.
3. **Not a permissible correction:** relabelling source families, dropping the four unwitnessed controls, counting timing ratios as semantic catches, treating v4-only receipts as v5 witnesses, claiming G9 caught portlen-v4, or generalizing named-specimen coverage into universal shortcut-family closure. Those change identity/provenance or the claim, rather than repair the observed defect; canonical acceptance is not this seat's authority.

## Files written, verification and blockers

Files written by this seat only:

- `/fast/scratch/hyaku/kake-r44/CriticKillRules/audit_receipts.py` — read-only source/receipt extractor used above.
- `/fast/scratch/hyaku/kake-r44/CriticKillRules/check_cohort.py` — read-only completed-cohort receipt reader.
- `.ufo/waves/round-44/w2/CriticKillRules.md` — this report.

Created scratch directory: `/fast/scratch/hyaku/kake-r44/CriticKillRules/`.

No product/class/counter/audit/manifest/receipt/history file was edited by this seat; no tool was installed or updated. No build, test, lint, formatter, counter scoring or smoke run was performed. The historical overwritten-link blocker was resolved for original channel inspection by the cited pre-run backup, without erasing the observed contamination. Remaining provenance limits are absent invocation/seed-origin/cache fields and class-module hashes in the frozen receipt schema. Final placebo/v4 summaries were unavailable at the directed close-out, so their review is unrun. The missing committed round-44 tree was explained by L1's working-copy freeze instruction, not treated as proof that artifacts did not exist.
