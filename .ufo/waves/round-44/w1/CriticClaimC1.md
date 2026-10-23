# CriticClaimC1 — C1 design falsification, pre-freeze review

Axes: **operability** (assigned: trustworthy offline audit, semantic observability, bounded capability); **freshness** is relevant only to evidence identity/provenance, not scored here. No round judgment or admission is made.

## Decisive counterexample

The existing skip-work receipt already falsifies the literal **27/27 blind under fresh `--classes v4`** premise. I did not run the counter again.

`.ufo/waves/round-44/verification/freeze/control-v4blind.json` records `controls:27`, `witnessed:2`, `ok:false`, `verdict:"witnessed 2/27"`. Its two per-tool receipts have **different stdout hashes**, not timing-only failures:

| Manifest control | Seed | Existing run carrying divergence | Required new-class evidence |
|---|---:|---|---|
| `buildscope-m5` | 181346457990762 | `D`; equal 10/11 | `G3` |
| `repeat-depth-deep` | 5994504518804 | `C`; equal 10/11 | `G7` |

Both receipts say `classesMode:"v4"`, `classRuns:[]`; both tools exit 2 like the reference, but their output bytes differ. Counter SHA in these receipts equals the bytes I hashed: `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc`.

This does **not** show that v4 already witnesses all 27, nor that the counter is necessarily wrong. It shows that historical meeting receipts do not establish universal/fresh-seed blindness, and that two current catches need no G-class work. Do not discard this receipt or search for a green replacement seed while retaining the unconditional 27/27-blind assertion.

## Attacks / how decided / what the L1 must add

### (a1) Legacy catches can masquerade as newly acquired class coverage — concrete falsifier

- **Attack:** A count based on any not-met verdict or any run divergence can credit an existing `C`/`D` catch to G7/G3. The two actual receipts above demonstrate that route before any new class is loaded.
- **How decided:** Read `verification/freeze/control-v4blind.json:1-21,435-436`, `tools/buildscope-m5.json:43-49`, and `tools/repeat-depth-deep.json:35-41`. The receipt extractor command below prints seeds, empty `classRuns`, differing hashes, and counter identity. Source decision: `c44_count_v5.py:1046-1065` excludes all G runs in v4 mode.
- **L1 must add:** State **“the named 27 historically met v4 on their reported seeds; the current skip-work calibration is 25 met / 2 semantically caught”**, if that is the intended factual bound. Separately require a new registered G-run semantic witness for each named control and disclose overlapping legacy catches. If fresh 27/27-blind is an immutable acceptance condition, the existing receipt is a miss; changing the condition requires an explicit pre-score declaration, not a relabel. Keep any new-class count distinct from the skip-work count.
- **Impacted axis:** operability. This is a claim-design defect, not just a wording preference.

### (a2) “Not met” is not a semantic witness; mixed-key rejection is also wrong

- **Attack:** Initial audit snapshot `A783`, `c44_audit.py:113-118`, counted `r["met"] is False` as witnessed. The predicate also includes timing (`c44_count_v5.py:1111-1112`) and starts with `met=False` before evaluation (`:996`); neither timing failure nor cannot-evaluate proves a judgment difference.
- **Concrete local example:** The committed r43 `verification/freeze/ref41-base.json` is the reference itself: equal **11/11**, `caughtBy=[]`, `met:false`, T1 **4.207**, T5 **7.047**. Replaying the initial six-line selection loop counts that actual receipt as “witnessed.” That falsifies the initial observable definition without inventing a tool or running the counter.
- **Intervening correction observed:** The audit owner edited during this review. At tested audit SHA `aed7d7711e17c750293a72acf81e686f3f49c0ae5715f393268b24b5644d0e7e`, the timing-only example is correctly excluded. However, its `semantic_witness` required **all** caught keys to start with G: `['G3']` counted, while hypothetical `['D','G3']` did not; likewise `['G7']` versus `['C','G7']`. These mixed-key inputs are explicit classifier examples, **not claimed scored receipts**. A real G witness is not invalidated by an additional old-run witness.
- **How decided:** `python3 -B /fast/scratch/hyaku/kake-r44/CriticClaimC1/classifier_evidence.py` executes only selected audit helper ASTs and the quoted initial classifier, never counter/tool/module execution. At the observed snapshot, blind expectation still requires every tool met; the “witnessed=0 by construction” print note must not be mistaken for a measured blind result.
- **L1 must add:** Define a class witness as at least one **registered** G key whose recorded exit/stdout comparison diverges because of a URL judgment; require a successful evaluation, not missing tool/crash/timeout. Retain all `caughtBy` keys but expose `classCaught` and `legacyCaught` separately. Use `any`/set intersection for class evidence, not `all`; a G3+D result still witnesses G3. Preserve timing as a separate predicate and preserve the failed blind receipt. The transient source/classifier defects are fixable before freeze; the report does not certify the final concurrently edited audit.
- **Impacted axis:** operability.

### (a3) A class label does not establish the cause; one manifest row is misclassified

- **Attack:** The manifest’s `class` field is metadata, not causal proof. A `G9`-labelled control need not be a port-digit-cache control. `controls-27.tsv:26` puts `buildport-m6` in G9/portdigit, but `controls-r43/buildport-m6-default-branch.py:303-304` flips the **default-port branch**: `if port is not None: port = 80 if scheme == "http" else 443`. The original r43 witness (`w1/MutBuildPort.md:24-29`) compares explicit versus implicit default ports, not memoized digit keys.
- **How decided:** The exact targeted deciding command is **unrun by this seat**:
  `python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G2 --tool-file .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py --seed 44`.
  G2 currently generates explicit-default-port sitemap URLs and implicit-port locs (`classes/g2_default_port.py:13-22`). G4 can also reveal port collapse; a G9 catch alone must not be described as proving the port-digit-cache mechanism.
- **L1 must add:** A frozen expected witness map grounded in each skip’s source/witness, with `buildport-m6` correctly described as default-port inversion and allowed causal keys stated explicitly. The intended keys for the other manifest groups are G1 grammar/long ports; G2 default-port normalization; G3 empty path; G4 port-scope; G5 prefix/head-tail cache keys; G6 fold memos; G7 guarded memo bands; G8 the known host tables; G9 the three actual port-digit/cache controls; G10 long-port windows. If only **any** G-run divergence is claimed, say so and do not infer closure of each advertised mechanism from the row label.
- **Impacted axis:** operability.

### (b) Named-cohort identity holds; an exhaustive denominator does not

- **Attack result:** I found **no mismatch with the canonical declared 27**. The manifest has 27 distinct names, 27 distinct tool hashes, no file/hash mismatches, and exactly the membership in `corpus/lessons/round-43-verifier-spotcheck.md:92-95` and `SCORECARD.md:3385-3399`. No audit result outside that manifest should enter the numerator.
- **Stronger counterexample to an exhaustive reading:** The durable seat reports now contain additional distinct meeting controls outside that named cohort:
  - `w1/CtlHeadTail.md:12`: `V5_tail_cache64.py`, SHA prefix `494077bb`, met at seed **238536594047229**, although two other seeds caught it. The original kill rule says **any** meeting receipt, not stable meeting only.
  - `w1/CtlPrefixCache.md:24-27,32,34-42`: `p45_noreval` (`164aa4d5902b`, seed **157897586892236**), `p46_noreval` (`442c84ea8aaa`, **246453014200990**), `p64_noreval` (`678fec6dc61f`, **186734228306336**), and `p48_weakreval` (`4905148a5cc2`, **275074208186561**) meet and have semantic witnesses. They are absent from `controls-27.tsv`. Exact-tail `*_reval` memos are correctly excluded: that report explicitly says no divergent witness exists.
- **How decided:** The receipt/manifest extractor below computes name/hash uniqueness and compares the named set; the cited report rows decide the additional-survivor issue without rescoring. The canonical closure’s tally is still 27; these findings do not silently replace that historical denominator.
- **L1 must add:** Say **“the 27 named tools in manifest SHA …, matching the r43 closure’s declared cohort”**, not “all round-43 meeting controls,” “27 independent shortcut families,” or exhaustive escape closure. Preserve a named exclusions/late-report note or explicitly expand the population before scoring if exhaustiveness is desired. Count is per distinct specimen, not independent family: several controls share mechanisms and host populations.
- **Impacted axis:** operability; provenance/freshness only if the population is silently changed.

### (c1) Source-adapted fixtures demonstrate known-specimen regression, not blind family generalization

- **Attack:** The class contract forbids runtime source reads and tool imports, but the loader does not enforce purity. `c44_count_v5.py:136-151` imports modules in the host process, and `:1064` passes the entire counter module as `h`. Host file access and invocation state exist there before the candidate enters its sandbox. A generator that reads the control file to pick its exact witness could improve the count without acquiring a general shortcut-class detector; that would violate the declared module contract even if every count were green.
- **Actual local boundary, not an accusation of forbidden I/O:** `classes/g8_host_tables.py:8-143,147-157` embeds the A/B/F host lists and iterates them. Static extraction found **46 unique hosts**, not 126 independent hosts: the tables have sizes 46/46/34, A=B and F is a subset. Seeds rotate path defects; they do not draw fresh hosts. `fresh-r44.invalid` is not in this G8 population. I did not claim it escapes every other counter run. G8 contains no imports in the observed source. Its owner explicitly documents copied data/no runtime I/O and the fixed-population limitation in `w1/ExecG8Hosts.md:7-8`.
- **How decided:** `python3 -B /fast/scratch/hyaku/kake-r44/CriticClaimC1/population_evidence.py` parses literals/imports only; source lines above decide the fixed population. A generator-source audit against the stated no-I/O/no-environment/no-control-import contract decides a forbidden runtime dependency. Reading control source **while authoring** a regression fixture is not itself forbidden or circular.
- **L1 must add:** Declare an **open-book, targeted regression corpus for these named controls and fixed populations**. Do not call fresh RNG seeds blind controls or independent host holdouts. If the capability claim extends to unseen shortcut implementations/hosts/cutoffs, it needs genuinely held-out implementations/populations fixed after the generator freeze and independent semantic witnesses. Otherwise keep the narrower observable. Targeting known files is a legitimate tradeoff for the bounded regression claim, but cannot establish the broader capability by itself.
- **Impacted axis:** operability.

### (c2) Counter hash alone does not freeze the effective instrument

- **Attack:** The same `c44_count_v5.py` bytes can load different `classes/gN_*.py` bytes. Receipts record `counterSha256` and class **names**, not class-content hashes (`:994-1003`), while the loader resolves current files (`:142-148`). `build_v5.py --check` only compares the generated counter file, not imported generator contents. Thus “same counter bytes” is insufficient evidence of an unchanged evaluated population.
- **How decided:** Those exact loader/receipt lines decide the omission; class SHA extraction below shows the independent files. No mutation was performed. Also, one shared RNG flows through runs A–F, then G1–G10, then T1–T5 (`:1036,1047-1070`); even equal seeds in v4/v5 do not give identical later timing-shape inputs after the extra generators/layouts consume randomness. A fresh-seed before/after tally is not a paired identical-corpus experiment.
- **L1 must add:** Freeze and retain a manifest/commit binding **counter + all ten class modules + audit driver + controls TSV + control files**, and bind each reported tally to it. Say which runs are common versus newly generated; require G-run evidence rather than crediting changed later T populations to the class work. A companion manifest/receipt reference is sufficient if frozen counter bytes cannot be edited.
- **Impacted axes:** operability; evidence freshness/identity. This is a fixable provenance gap, not evidence that a source substitution happened.

### (d) Same rejected build can be a positive control, not a new admitted capability or broad harm proof

- **Attack:** Reusing `020bc457` does not itself invalidate a positive regression control. The rejection history concerns the measured claim/instrument, not a demonstrated new scanner regression. Conversely, three v5 passes cannot turn old rejected C1s into admitted work or prove the broader URL/harm contract.
- **How decided:** The three inherited r43 build receipts below pin the exact same `914ebdee…cd021` bytes and met 11/11. `round-42-verifier-spotcheck.md:43-51` calls the freeze defect substantive/fatal to the measured admission while retaining scoped H1–H5 evidence; `round-43-verifier-spotcheck.md:29-32,88-95,232-239` preserves NOT MET and no operability admission. `SCORECARD.md:3242-3246` preserves H4 **in-class only**. The actual r42 H4 seed-42001 receipt contains `inClass:19720`, `outOfClass:280`, `outOfClassChanged:21`, `validReject:0`, `newAccept:0`; a blanket “no changed judgments/no harm anywhere” inference is false. Those out-of-class changes are not labelled harms by this review.
- **L1 must add:** Name the newly measured object as **audit-corpus discrimination**, if that is the claim; describe the scanner as a held, byte-identical **positive compatibility/performance control**, not a new scanner optimization or reopened admission. Preserve historical rejected verdicts and H4’s population qualification. Supply new frozen-v5 receipts for **exactly three fresh, distinct seeds**, expected revision and tool SHA, all 21 runs evaluated, all five timing ratios present and within bound. The observed audit expectation uses `bool(build)`/all-met, which alone does not enforce three runs or distinct seeds; the exact invocation and receipts must. Supply separate receipts for the four named r42 controls and junk; they are not in the 27-row manifest, so the principal 27-row audit alone cannot establish their continued rejection.
- **Impacted axis:** operability. Bounded positive-control reuse is a tradeoff, not automatically a defect; overclaiming admission or broad harm preservation is the defect.

## Exact executable commands and observed output

All executable commands were run from the lane root. No full counter, class probe, tool selftest, build, formatter, judge, integration, commit, or other orchestration runtime was invoked by this seat. Reader/grep tool calls supplied the cited source ranges and existing receipts; no reported failure was rerun to confirm it.

### 1. Directory creation

```text
mkdir -p /fast/scratch/hyaku/kake-r44/CriticClaimC1 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w1
```

Exit 0; no output.

### 2. Manifest/receipt extraction (partial success; transient concurrent edit blocked AST step)

```text
python3 -B /fast/scratch/hyaku/kake-r44/CriticClaimC1/review_evidence.py
```

Verbatim decisive output:

```text
MANIFEST rows=27 unique_names=27 unique_sha256=27 sha_mismatches=[]
CLOSURE_TALLY missing=[] extra=[]
CLASSES {"G1": 2, "G10": 2, "G2": 1, "G3": 1, "G4": 1, "G5": 4, "G6": 4, "G7": 5, "G8": 3, "G9": 4}
EXISTING_SKIP_WORK {"classesMode": "v4", "controls": 27, "counterSha256": "5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc", "ok": false, "witnessed": 2}
EXISTING_SKIP_ROW {"caughtBy": ["D"], "classRuns": [], "equalRuns": "10/11", "met": false, "name": "buildscope-m5", "requiredClass": "G3", "seed": 181346457990762}
EXISTING_DIVERGENCE {"candExit": 2, "candOutSha256": "3406aa7462b7a76d02effa25f2ccc926fb87f010cfcf3675e70d2cefae2ee566", "key": "D", "name": "buildscope-m5", "ref41Exit": 2, "ref41OutSha256": "7bdf3ebd80c57e7e08a32dbeb7db07d4f0e3ba7cfc090e26fd061918c862f99a"}
EXISTING_SKIP_ROW {"caughtBy": ["C"], "classRuns": [], "equalRuns": "10/11", "met": false, "name": "repeat-depth-deep", "requiredClass": "G7", "seed": 5994504518804}
EXISTING_DIVERGENCE {"candExit": 2, "candOutSha256": "8b0791818af0feba0381ca80567700a48b9c481714d16ee0e5deb5bd62ffdbd1", "key": "C", "name": "repeat-depth-deep", "ref41Exit": 2, "ref41OutSha256": "665f50f04fa3c6db17b8e7f3f3aadec2c00f4967006e88cf5cddac8b91eabcca"}
```

The subsequent AST step exited 1 during the owner’s concurrent audit edit:

```text
  File "<unknown>", line 218
    CUT 61.=171
        ^^^
SyntaxError: invalid syntax
```

Owner notified; the file was re-read before further action. This was transient, not asserted as the final audit state. Already completed extraction was not rerun; the following separate command exercised the failed classifier step on a new snapshot.

### 3. Classifier counterexamples and inherited identity extraction

```text
python3 -B /fast/scratch/hyaku/kake-r44/CriticClaimC1/classifier_evidence.py
```

Exit 0. Verbatim decisive output:

```text
CURRENT_AUDIT_SHA256 aed7d7711e17c750293a72acf81e686f3f49c0ae5715f393268b24b5644d0e7e
INITIAL_AUDIT_TIMING_ONLY {"caughtBy": [], "equalRuns": "11/11", "met": false, "ratios": {"T1": 4.207, "T2": 1.917, "T3": 1.152, "T4": 1.228, "T5": 7.047}, "source": ".ufo/waves/round-43/verification/freeze/ref41-base.json", "witnessed": ["actual-r43-ref41-base-receipt"]}
CURRENT_AUDIT_TIMING_ONLY {"witnessed": false}
HYPOTHETICAL_KEY_CLASSIFICATION {"caughtBy": ["G3"], "witnessed": true}
HYPOTHETICAL_KEY_CLASSIFICATION {"caughtBy": ["D", "G3"], "witnessed": false}
HYPOTHETICAL_KEY_CLASSIFICATION {"caughtBy": ["G7"], "witnessed": true}
HYPOTHETICAL_KEY_CLASSIFICATION {"caughtBy": ["C", "G7"], "witnessed": false}
CURRENT_BLIND_GATE_EXISTING_ROWS {"ok": false}
COUNTER current_sha256=5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc skip_receipt_same_counter=True
INHERITED_BUILD {"equalRuns": "11/11", "met": true, "revision": "020bc4574729ed674299f6cab02faac1582d9464", "seed": 9325990526163, "source": ".ufo/waves/round-43/verification/freeze/build-1.json", "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021"}
INHERITED_BUILD {"equalRuns": "11/11", "met": true, "revision": "020bc4574729ed674299f6cab02faac1582d9464", "seed": 265206435053987, "source": ".ufo/waves/round-43/verification/freeze/build-2.json", "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021"}
INHERITED_BUILD {"equalRuns": "11/11", "met": true, "revision": "020bc4574729ed674299f6cab02faac1582d9464", "seed": 269853680553917, "source": ".ufo/waves/round-43/verification/freeze/build-3.json", "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021"}
H4_RECEIPT {"counts": {"baseOracleDisagree": 3989, "baseOracleDisagreeAcceptInvalid": 3989, "baseOracleDisagreeRejectValid": 0, "candidateAcceptsBaseRejects": 0, "candidateRejectsBaseAccepts": 3989, "inClass": 19720, "n": 20000, "newAccept": 0, "oracleDisagree": 0, "oracleDisagreeAcceptInvalid": 0, "oracleDisagreeRejectValid": 0, "outOfClass": 280, "outOfClassChanged": 21, "outOfClass_base1_cand0_oracle0": 21, "validReject": 0}, "seed": 42001, "source": ".ufo/waves/round-42/verification/harm/h4-020bc457-42001.json", "toolSha256": "914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021"}
```

### 4. Static fixed-population extraction

```text
python3 -B /fast/scratch/hyaku/kake-r44/CriticClaimC1/population_evidence.py
```

Exit 0. Verbatim decisive line (remaining output was the host list and observed class-file hashes, not final freeze certification):

```text
G8_STATIC_POPULATION {"imports": [], "probeHost": "fresh-r44.invalid", "probeHostCovered": false, "sha256": "6385a4c040ed83c01fb010b2ac12724e9a9e4863398768a33a0d41c9b472ea4b", "source": ".ufo/waves/round-44/classes/g8_host_tables.py", "tableSizes": [46, 46, 34], "uniqueHosts": 46}
```

## Write scope, coordination, and bounds

Files written by this seat only:

- `/fast/scratch/hyaku/kake-r44/CriticClaimC1/review_evidence.py`
- `/fast/scratch/hyaku/kake-r44/CriticClaimC1/classifier_evidence.py`
- `/fast/scratch/hyaku/kake-r44/CriticClaimC1/population_evidence.py`
- `.ufo/waves/round-44/w1/CriticClaimC1.md` (this report)

No frozen artifact, production source, ledger, history, state file, fleet file, or sibling lane was edited. No subagent was dispatched. No tool was installed or upgraded. Peer messages identified the audit classifier/mixed-key issue, the fixed-host bound, and the cohort mapping issue; the audit and G8 owners retain their own edit authority. The blocker message to L1 initially mistyped the depth receipt seed; it was promptly corrected to **5994504518804**, the directly read/extracted value used everywhere in this report.

Review complete within scope. No information-access blocker remains. The **claim-design blocker** is the existing red skip-work calibration. Full counter/probe execution and final concurrent-audit verification remain unrun by this seat, intentionally; the L1 must use frozen final bytes and retain all failed calibration evidence before claiming the declared end-to-end counts.
