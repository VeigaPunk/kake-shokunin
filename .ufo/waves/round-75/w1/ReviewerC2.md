# ReviewerC2 — round 75, w1

## Latest measured update — supersedes stale selftest finding

After executor notification, I measured updated snapshot SHA256 `62b795eaa8ad446d28daa433ff203b4961ac96f326888e7989f39859828749c9`, preserved as `ReviewerC2/instrument_receipts.updated.py`. Its selftest now passes **15/15, exit 0**. The medium 12/13 finding below is **historical and resolved**, not an outstanding defect against this newer snapshot.

The principal finding persists: after `--write` on unchanged committed base B, default `--check` still returns **bound=16 mismatches=0 met=true, exit 0, committed=absent**. New opt-in `--require-committed` correctly returns **met=false, exit 1** for that same uncommitted receipt. Thus strict mode provides the needed distinction, but default green remains insufficient evidence for the frozen committed-receipt claim. Recommendation: L1 must use/enforce the strict admission path rather than present a default precommit content check as committed evidence.

`ReviewerC2/updated-results.json` records all four exact commands and exits: write 0; default-uncommitted 0; strict-uncommitted 1; updated-selftest 0. The full 16-forgery matrix below was run on the earlier identified snapshot, not rerun against this update. No claim of a final landed-tip verification is made. The provenance finding below is likewise snapshot-scoped; the updated default commitment defect was directly reproduced.


Axes: committed-byte integrity; receipt provenance; population completeness; adversarial rejection; deterministic writing. Recommendation: hold C2 admission for the measured snapshot. This recommendation is not an admission decision.

## Scope and identity

Base: `c9c5e484c533aa65f4374b841a3edcf572ed19a9` (B). Historical comparison revision: `c9fd964354b03b163994519ae43d741b3ee3a81d` (O). All 16 frozen instrument blobs are identical between B and O. Contract read before attacks; no lane production file was changed.

The executor artifact appeared during review and changed during reads. Actual-tool results below use the preserved `ReviewerC2/instrument_receipts.snapshot.py`, SHA256 `169e2136527531de568f84ec0ba8ea8256a743ca01424f5bead448b37f949eb3`. It is a copy of `w1/ExecC2Tool/instrument_receipts.py`, not a committed after-state. Line citations below refer to this immutable snapshot, not the moving executor artifact. Initial contract-only reference-checker experiments are **not** evidence of actual-tool behavior and are excluded from the verdict.

LSP unavailable: `read xd://lsp` returned “No such tool”; semantic LSP references/definition/diagnostics could not be performed. Evidence is execution, git committed bytes, and direct source inspection, not semantic proof from grep.

## Findings, highest severity first

### High — uncommitted receipts satisfy the committed-receipt target

`load_receipt` at snapshot lines 371–395 prefers a worktree file, even when no receipt exists at the measured commit. `evaluate` lines 509–526 reports `receipt_committed` but does not gate `met` on it.

On the clone at B, where the committed receipt is absent:

1. `--check`: exit 1, `bound=0 mismatches=16 met=false`.
2. `--write --date 2026-11-03`: exit 0; only an untracked receipt is created.
3. `--check` at **the same B**: exit 0, `bound=16 mismatches=0 met=true`, with `receipt: worktree committed=absent`.

Evidence: `ReviewerC2/actual-results.json`, cases `baseline-no-receipt`, `write-first`, `UNCOMMITTED-valid-receipt-at-base`. No instrument or committed tree changed. Thus an unchanged committed base plus an uncommitted generated file reaches the advertised target. The do-nothing committed tree must not reach it under the assignment. Reporting `committed=absent` is honest diagnostics but does not enforce the claim.

Required decision: enforce a committed receipt carrier for an admission check; keep worktree-injection controls distinguishable from admission. Do not simply require that a receipt contain the hash of the commit carrying itself: that creates a commit-hash self-reference. Subject revision and committed carrier must have an explicit relationship authorized by the contract owner.

### High — receipt revision provenance is not validated

Snapshot `evaluate` lines 438–451 proceeds from valid JSON directly to entries. Lines 520–521 expose `receipt_revision` and `revision_match` only as telemetry.

Both O→B and B→O receipts with unchanged instrument bytes return exit 0, `bound=16 mismatches=0 met=true`. Content equality across two real revisions is not itself a defect: those digests genuinely match both. However, even `revision="not-a-real-revision"` returns the same green result, `committed=absent revision_match=false`. This does **not** establish bytes at the receipt's declared revision, as the schema/claim describes.

Evidence: `actual-results.json` cases f06, f14, `base-generated-checked-at-ancestor`; `invalid-revision-result.json` contains the nonexistent-revision counterexample. At minimum resolve and validate the declared subject revision, and pin its relationship to the measured/carrier revision. If the owner intends content-only portable receipts, say so explicitly; do not present unchecked revision provenance as established.

### Medium — supplied selftest fails its own revision fixture

Actual snapshot `--selftest --work <scratch>/actual-selftest` exits **1**, tally **12/13**. The only failed fixture is `receipt at another revision`: snapshot lines 882–897 expect exit 1 / bound 0, but the checker now returns exit 0 / bound 16 / `revision_match=false`. This is an observed incompatible expectation, not a hypothetical coverage request.

Evidence: `actual-results.json`, `actual-selftest`. Resolve the provenance decision above, then align implementation and fixture; changing only the expected result would not repair the committed-receipt issue.

## Actual forged receipts: 16 cases

All cases below ran the preserved actual tool against the scratch clone at B, with fixture JSON placed at the receipt path. Exit codes and full commands are preserved in `actual-results.json`; fixture documents are in `actual-fixtures/`. `Bnd/Mis` abbreviates the observed counters.

| Fixture | Forgery | Bnd/Mis | met / exit |
|---|---|---|---|
| f01 | Correct digest, wrong byte count | 15/1 | false / 1 |
| f02 | Correct byte count, wrong digest | 15/1 | false / 1 |
| f03 | Digest AND length of edited, uncommitted working-tree bytes, not the blob | 15/1 | false / 1 |
| f04 | Duplicate population path, one incorrect duplicate | 15/1 | false / 1 |
| f05 | 16 valid entries plus two outside-population paths | 16/0 | true / 0; extras reported |
| f06 | Different revision field O, matching digests | 16/0 | true / 0; revision_match=false |
| f07 | Registered mode true→false | 15/1 | false / 1 |
| f08 | Delegates c57 and c69 mode false→true | 14/2 | false / 1 |
| f09 | One population path omitted | 15/1 | false / 1 |
| f10 | 16 entries, two paths retain their names but exchange digest and byte length | 14/2 | false / 1 |
| f11 | Uppercase digest strings | 0/16 | false / 1 |
| f12 | Wrong schema version | 0/16 | false / 1 |
| f13 | Byte counts encoded as strings | 0/16 | false / 1 |
| f14 | Receipt derived at O, checked at B | 16/0 | true / 0 |
| f15 | Valid 16 plus traversal-path entry | 16/0 | true / 0; outside entry reported |
| f16 | Empty files array | 0/16 | false / 1 |

Reverse cross-revision test: base-generated receipt checked at O also returns 16/0, true / 0. No future round tip existed for this review; B and O exercise both directions with real committed revisions and unchanged population blobs, rather than inventing an after-state. A nonexistent declared revision was separately tested and accepted, as above.

f05/f15 acceptance is **not** a defect under the frozen outside-population rule: these entries do not contribute to bound and are reported separately. Their green status must not be described as forged extra paths successfully binding instruments. f06/f14 content-portability alone likewise is not proof of bad digests. The actionable defect is unchecked provenance, demonstrated by the nonexistent revision and uncommitted receipt.

Positive control: the honest generated receipt returns 16/0, true / 0. Registration truth is 14 true / 2 false: c57 and c69 only delegate `--selftest` to other tools. The actual AST classifier correctly rejects their false→true forgeries; the naive-substring hazard found during early reference experiments is **not an actual-tool finding**.

## `--write` idempotence and selftest coverage

Two actual `--write --date 2026-11-03` calls at B both exit 0 and emit byte-identical 3,397-byte documents, SHA256 `b37d1b09415e2e63816c701324cf53d86b5e8dcc150130609583dcc836d81a69`. With an uncommitted edit to a population file, `--write` still emits that identical document: the writer correctly hashes committed blobs, not worktree bytes. These facts are recorded independently in `actual-results.json` (`idempotent=true`, `dirty_write_identical=true`).

Snapshot selftest covers writing twice, missing receipt, wrong digest, wrong bytes, true→false mode, duplicate, outside-population reporting, revision mismatch (currently failing), all-fabricated digests, grown population, missing frozen path, classifier snippets, and usage errors.

Omitted end-to-end fixture classes: omitted receipt entry; false→true mode flip; exchanged digest/length across two paths; dirty-worktree generation/checking; invalid schema and typed fields; uppercase digests; a green result with no committed receipt; nonexistent declared revision; committed-receipt fallback versus a conflicting worktree override. Some are exercised by this review but are absent from the built-in selftest. Classifier snippets are useful but do not substitute for end-to-end file-binding fixtures.

## Tautology assessment and strongest honest claim

A same-repository digest receipt is not independent attestation. `git show R:path` plus SHA256 re-derives the same identity without the receipt. The useful additional artifact is an explicit population inventory and static registration classification, serialized for later comparisons. It proves neither execution, passing selftests, registry correctness, nor trustworthy authorship.

Strongest sentence the **measured tool** supports: “The supplied receipt's 16 path entries match the committed blobs' SHA256, byte lengths and static selftest classification at the requested revision.” It cannot currently add “the receipt is committed” or “the receipt's declared revision was validated.” C1's execution truth remains separate.

Pure absent-receipt base is red; unchanged committed base plus uncommitted `--write` is green. Therefore the frozen committed-receipt target is **not protected** against a do-nothing committed tree by this implementation.

## Commands, constraints, residual risk

Canonical actual command (exit 0 driver, per-check exits captured inside):

`python3 -B /fast/scratch/hyaku/kake-r75/ReviewerC2/actual_attacks.py`

It invokes `python3 -B <scratch>/instrument_receipts.snapshot.py --root <scratch>/clone --revision <B-or-O> --check`, `--write --date 2026-11-03`, and `--selftest --work <scratch>/actual-selftest`. Complete argument arrays and exits are in the JSON receipt. Supplemental nonexistent-revision command is recorded verbatim in `invalid-revision-result.json`.

The C1 base control was also exercised, exit 1: `python3 -B <lane>/.ufo/waves/round-75/c75_row_truth.py --root <scratch>/clone --revision B --base B --work <scratch>/c1work`; observed `rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false`.

Initial reference-driver attempt failed with KeyError during fixture construction; its shell pipeline masked that Python failure. It is not counted as a passing check. Subsequent reference experiments were superseded by the actual snapshot results above. Fixture-only git mutations occurred in the scratch clone after asserting its toplevel; no lane git mutation occurred. No tool installed or updated. No subagents spawned. The executor artifact is in flight, so these findings are snapshot-specific; no landed-tip verdict is claimed. Canonical runtime/rerouting/resume-saturation rules are outside this receipt review's changed behavior, not verified here.

Self-evaluation: accuracy 4 (real snapshot/commands, no final-tip evidence); completeness 4 (all named attack classes and idempotence, tip represented by real historical pair); clarity 4 (source and snapshot separated); actionability 4 (provenance decision precedes fix); conciseness 4 (full outputs kept in artifacts). Average 4.0. Main should re-evaluate only the eventual committed candidate after the provenance decision; do not admit this snapshot on the 12/13 selftest.

Cleanup: copied the actual-tool fixtures, immutable snapshots, driver and result receipts into `w1/ReviewerC2/`, then executed `rm -rf -- /fast/scratch/hyaku/kake-r75/ReviewerC2` (exit 0). The owned scratch tree was removed before yielding.
