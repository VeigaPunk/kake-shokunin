FINDING — 25 snapshot mutants exercised: 22 killed by a green-baseline detector, 3 survived; C2's own selftest missed all seven measurement-path mutants. The authoritative C3 matrix attempt was inconclusive, not a kill.

## Scope and axes

Calibration, freshness, operability; detector sensitivity and exact restoration are the probe axes. Scratch-only mutations; no lane implementation edits, commits, integrations or scores claimed. Instruments changed during the wave, so results bind the retained snapshots below, not a future carrier. Receipts are under `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-78/w1/MutC/` (abbreviated **R** below).

Frozen contract and amendment 1 were read. A1 now requires body tags to join the effective set while reporting the hygiene finding; A2 now REQUIRES date-only acceptance. Accordingly the date-only defect tested below is rejection, not acceptance. The assignment's literal date-only-acceptance mutant is now correct behavior, not a surviving defect.

Snapshot SHA256:

- C1 `c1-pristine.py`: `c2dc1cbf6cc1e860c87f77903b6ea865edbdc781b40ca537575eab958cde6673`.
- C2 `c2-pristine.py`: `46acb450a2042249d0b589ed6614ab0c83e67e48da3eb5da69efd2ecbadb2821`.
- C3 `c3-pristine.py`: `d32fb5808c1de8f9abdb10248247acc7ff779937ba51c09dabf82c1f8611acf4`.

## C1 — `.ufo/waves/round-78/c78_shonen_population.py`

Pristine detector: `selftest: 9/9 passed`, exit 0. Every restored run: exit 0, exact original SHA256. Actual outputs, mutant hashes and restored outputs: **R/results-c1.json**, `mutants[]`; command output: **R/c1-c2-final.log**.

| Mutant | One-line mutation | Result / killing case | Actual mutant output |
|---|---|---|---|
| m01 | Count undeclared rows as declared and matching | KILLED, s3 | 8/9, exit 1; undeclared row incorrectly met=true |
| m02 | Compare population with `<` rather than `!=` | KILLED, s2 | 8/9, exit 1; oversized declaration incorrectly met=true |
| m03 | Grade count_at_least growth exactly, without tolerance | KILLED, s5 | 8/9, exit 1; tolerated growth incorrectly red |
| m04 | Grade no_match with the floor rule | KILLED, s7 | 8/9, exit 1; exact drift incorrectly tolerated |
| m05 | Drop `len(rows) == 4` | SURVIVED, unreachable redundancy | 9/9, exit 0 |
| m06 | Ignore c77 findings entirely | KILLED, s6/s7/s8 | 6/9, exit 1 |
| m07 | Drop population suffix filter | KILLED, s1/s2/s4/s5 | 5/9, exit 1 |
| m08 | Drop population exclude filter | KILLED, s4 | 8/9, exit 1 |

m05 is logically redundant: `declared == 4` AND an empty undeclared list implies every row is declared and therefore `len(rows) == 4`. No legitimate ledger can distinguish that single-conjunct deletion. m07 is reachable because the fixture ledger JSON itself sits inside the population directory: dropping the suffix admits it.

## C2 — `.ufo/waves/round-78/c78_sweep_truth.py`

Pristine `--selftest`: 6/6, exit 0. **Every measurement-path mutant below ALSO reports 6/6, exit 0.** The selftest independently recomputes the predicate and never calls `measure()`. Therefore it cannot protect the actual measurement implementation. See **R/c2-pristine.py**, `selftest()` versus `measure()`.

A second, explicitly synthetic end-to-end detector runs the real counter against scratch git fixtures, whose local Node sweep emits controlled JSON. This is a counter probe, not a production-sweep measurement. Pristine and restored outputs match the contract in every mode:

- A: clean base + red planted control => met=true, counter exit 0.
- B: base exit 0, drift=0, newMissing=1, paths.ok=true => met=false, exit 1.
- C: clean base + control exit 1, drift=0 => met=false, exit 1.
- D: clean base + green planted control => met=false, exit 1.
- E: base exit 64 with otherwise clean JSON => met=false, exit 1.
- F: base exit 0, drift=0, newMissing=0, paths.ok=false => met=false, exit 1.
- G: clean base + control exit 2, drift=0 => met=false, exit 1.
- H: clean base + control exit 2, drift=1 => met=false, exit 1.

| Mutant | One-line mutation | End-to-end verdict / killing mode |
|---|---|---|
| m01 | Skip control execution, substitute a constant red control | KILLED, C/D/G/H; mutant falsely met=true, exit 0 |
| m02 | Accept control_drift==0 (`>=0`) | KILLED, C; falsely met=true, exit 0 |
| m03 | Drop newMissing conjunct | KILLED only by synthetic B; falsely met=true, exit 0 |
| m04 | Accept any nonzero control exit, not exactly 1 | KILLED, H; falsely met=true, exit 0 |
| m05 | Treat base exit 64 as met | KILLED, E; falsely met=true, exit 0 |
| m06 | Ignore paths_ok | KILLED only by synthetic F; falsely met=true, exit 0 |
| m07 | Drop tree_identity divergence conjunct | SURVIVED; all eight modes retain pristine results |

B and F deliberately test inconsistent JSON: production `freshness-sweep.mjs:588` makes paths.ok false when newMissing>0; `:1076` forces nonzero exit when paths.ok is false. Thus m03/m06's kills test defensive counter clauses, not reachable coherent production outputs. In the existing production sweep those clauses overlap other conjuncts.

m07 survives because the fixture control always adds the planted Markdown file, so the computed input identity differs already. A direct measurement test with equal mocked identities but clean-base/red-control decisions would isolate this clause; it would be synthetic rather than evidence that the ordinary plant path can produce equal identities.

Coverage fix indicated by m01/m02/m05: run existing logical t4/t5/t6 scenarios THROUGH `measure()` using controlled sweep outputs; do not merely recompute the predicate in selftest. No counter repair was made by this seat.

Evidence: **R/results-c2.json**, `pristine_probe`, `conclusive`, `mutants[].live`, `mutants[].restored_live`; **R/mutate_c2.py** contains the exact Node fixtures. All restored selftests exit 0; all restored live results match the pristine results; all original-byte hashes match.

## C3 — `scripts/meta_robots_audit.py`

Snapshot baseline: `selftest 84/84 passed`, exit 0; independent frozen-case probe: `matrix: cases=34 decided=34 correct=34 failed=0`, exit 0. The 34-case snapshot is retained in **R/cases-snapshot/**, avoiding later concurrent case renames/additions. Probe compares tool process exit and sorted finding-id lists against each expect.json; expected effective rules are checked by the tool's manifest comparison. These are not claims that the later round matrix/carrier passed.

| Mutant | One-line mutation | Verdict / killing case IDs | Selftest; matrix result |
|---|---|---|---|
| c01 | Remove head/body distinction: suppress outside-head hygiene finding | KILLED: g19-tag-outside-head, g19b-body-only-tag | 79/84; 32/34; both exit 1 |
| c02 | Drop agents filter | KILLED: g17-googlebot-ignored-default-agents | 81/84; 33/34; exit 1 |
| c03 | none expands only noindex | KILLED: g03-none | 82/84; 33/34; exit 1 |
| c04 | Numeric merges take max instead of min | KILLED: g08-max-snippet-most-restrictive | 82/84; 33/34; exit 1 |
| c05 | -1 participates in minimum, becoming most restrictive | KILLED: g08b-max-snippet-unlimited-loses, g10-max-video-preview-unlimited-loses | 82/84; 32/34; exit 1 |
| c06 | Reject date-only unavailable_after (amendment A2 inversion) | KILLED: g12b-unavailable-after-date-only | 82/84; 33/34; exit 1 |
| c07 | Silently ignore unknown tokens | KILLED: g16-unknown-directive, g16b-non-ascii-token | 83/84; 32/34; exit 1 |
| c08 | Compare manifest findings in supplied sequence rather than sorted order | SURVIVED | 84/84; 34/34; both exit 0 |
| c09 | Return exit 0 on findings | KILLED: g11-max-snippet-invalid (plus eight others) | 69/84; 25/34; exit 1 |
| c10 | Order max-image-preview alphabetically | KILLED: g09-max-image-preview-most-restrictive | 82/84; 33/34; exit 1 |

c08 is a real snapshot coverage gap, not a logical redundancy. All 34 manifest finding lists have at most one item. Close it with two meta elements (`content=""` and `content="bogus"`) and manifest expected findings in reverse alphabetic order: `["meta_robots_unknown_directive","meta_robots_empty_content"]`. Correct sorted comparison must match; the sequence mutant adds expected_mismatch. The tested tool contract says sorted-list comparison, so this tests order invariance, not duplicate-elimination semantics.

All ten restored selftests and matrix probes exit 0; restored SHA256 equals the pristine SHA256. Exact mutation anchors, counts, outputs and hashes: **R/mutate_c3.py**, **R/results-c3.json** and **R/c3-final.log**.

### Authoritative matrix attempt: INCONCLUSIVE

A separate scratch fixture committed each mutated tool solely so the round matrix could extract a revision blob. The baseline itself failed: `C3v1 revision=HEAD cases=36 decided=0 correct=0 wrong=0 constants_failed=0/4 met=false`, exit 1. Diagnostics: expected underscore case directory names did not match supplied hyphen names; selftest parser also rejected the tool's `selftest 84/84 passed` output (`selftest_ok=false`). Routed to KakeR78.

**Every KILLED label in R/results-c3-matrix.json is INVALID:** that exploratory harness erroneously classified any nonzero mutant exit as a kill without honoring its red baseline. Retained unchanged for honesty; NONE contributes to the 22 kills reported here. This receipt is inconclusive, including c08. The green-baseline independent 34-case detector above supplies the actual case-level evidence.

Attempt command:
`python3 -B /fast/scratch/hyaku/kake-r78/MutC/mutate_c3_mx.py` (harness exit 0; individual matrix invocations exit 1).
Its matrix argv:
`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-78/c78_meta_robots_matrix.py --root /fast/scratch/hyaku/kake-r78/MutC/mx-fixture --tool-revision HEAD --cases /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-78/cases --consts /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-78/consts --work /fast/scratch/hyaku/kake-r78/MutC/mx-work/<case>`.

## Exact final mutant-set commands

`TMPDIR=/fast/scratch/hyaku/kake-r78/MutC python3 -B /fast/scratch/hyaku/kake-r78/MutC/mutate_c1.py` — exit 0 (individual mutant selftest exits listed above).

`TMPDIR=/fast/scratch/hyaku/kake-r78/MutC python3 -B /fast/scratch/hyaku/kake-r78/MutC/mutate_c2.py` — exit 0.

`TMPDIR=/fast/scratch/hyaku/kake-r78/MutC python3 -B /fast/scratch/hyaku/kake-r78/MutC/mutate_c3.py` — exit 0.

The final two independent paths ran concurrently; C1/C2 ran sequentially because their harnesses share a scratch tree. Leaf seat: no agent dispatch. Harnesses and frozen inputs retained in R. `SHA256SUMS` covers retained receipt bytes. Scratch cleanup status is in **R/cleanup.json**.

## Method limitations and self-evaluation

Cleanup defect: `shutil.rmtree` removed this probe's fixtures but failed with `OSError: [Errno 39] Directory not empty` on the assigned seat root. Immediate directory inspection showed newly-created `work/restored-T5/` (not one of this harness's paths), indicating a concurrent namespace collision. That remaining tree was not deleted to avoid destroying another writer's work; the exact collision was routed to KakeR78. Cleanup therefore is NOT claimed complete.

No tools installed or updated. Existing C1 selftest creates fixture commits before its own top-level assertion; the exploratory C2 harness used a fixed scratch fixture directory rather than mktemp. Those are method deviations from the requested fixture guard, not evidence of production-repo mutation. All such repos were confined to this seat's scratch tree. Initial tool exploration preceded reading the godspeed skill; later parallelism used independent local process detectors, not subagents (leaf-seat constraint).

Self-evaluation: accuracy 4 (authoritative-matrix red baseline explicitly invalidates its kill labels); completeness 4 (all requested mutation behaviors exercised, with A2 inversion stated); clarity 4 (snapshot versus later carrier distinguished); actionability 4 (specific missing order-invariance case and measurement-path tests identified); conciseness 3 (extra exploratory matrix receipt requires explanation). Overall 3.8/5. The user should treat this as mutation evidence, not admission or a shipped fix.
