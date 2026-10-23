# ScribeQualityCriterion — scoped findings

Axes: operability; freshness of the scored-byte record.

## Behavior and finding
Drafted criterion (o): every pre-declaration tool score with bytes must be named by label and full SHA-256, assigned an explicit class and consequence treatment, and reconciled to the committed summary. The no-tool baseline is explicit; post-declaration control scope is distinguished. The corrected example lists 39 byte-bearing tools (34 reference ablations, reference/oracle, and four other controls) plus the absent baseline.

Findings:
- `SCORECARD.md:2380-2384` cites the pre-summary and prior oracle/ablation/control scores but does not enumerate their digests in the control-class sentence.
- `SCORECARD.md:2385-2393` broadly makes every scored non-build tool a control, leaving the already-scored oracle/reference's consequence ambiguous.
- `SCORECARD.md:2404-2414` records the reference's abbreviated digest and literal-reading defect.
- `corpus/QUALITY.md:926-930` (j) covers consequence application; `corpus/QUALITY.md:960-965` (n) rejects control lists that may include builds/near-complete work.
- Public `.ufo/waves/round-39/verification/pre-summary.jsonl:1-40` records 39 non-null tool hashes and one null `base` row. No key/case file or reference implementation was read.

## Gates and commands
Original declaration gate (expected fail):
```sh
timeout 30s python3 -B /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/check_control_inventory.py --repo /home/vgpnk/Projects/shokunin/kake-shokunin --revision ceecb1b1f9093471eb0b17d2c9190e78bceb0b78
```
Output: `FAIL: 39 of 39 byte-bearing scores missing/wrong; 0 extra labels; 0 duplicate labels; duplicate_sha256=false; absent_baseline=missing; post-declaration_scope=missing`; exit 1.

Corrected-sample gate (expected pass; reads a Git tree object, not a commit, because no commit was made):
```sh
timeout 30s python3 -B /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/check_control_inventory.py --repo /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/corrected-sample --revision d54b1c33ecd027a454822023d7219ef1249d387a --summary-repo /home/vgpnk/Projects/shokunin/kake-shokunin --summary-revision ceecb1b1f9093471eb0b17d2c9190e78bceb0b78
```
Output: `PASS: 39/39 byte-bearing pre-declaration scores SHA-pinned and classed; absent baseline explicit; post-declaration scope explicit`; exit 0.

Setup/provenance:
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 915e9e87:SCORECARD.md` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 72edf2123f92b9dc546494cbffcc777ed3c3cd3a:SCORECARD.md` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e ceecb1b1f9093471eb0b17d2c9190e78bceb0b78:SCORECARD.md && git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e ceecb1b1f9093471eb0b17d2c9190e78bceb0b78:.ufo/waves/round-39/verification/pre-summary.jsonl` — exit 0.
- `timeout 30s mkdir -p /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/corrected-sample` — exit 0.
- `timeout 30s git -C /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/corrected-sample init -q && timeout 30s git -C /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/corrected-sample add -- SCORECARD.md && timeout 30s git -C /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/corrected-sample write-tree` — exit 0, tree `d54b1c33ecd027a454822023d7219ef1249d387a`; no commit.

Source blob hashes: declaration `SCORECARD.md` `0d4b1134eb1e36457fac37f061da17e28ec2e4b35cb2e267f0a12b87d252d378`; pre-summary `98e44fe613c85b660f3b12cd60ecc8973fe989114bcd1eb758fff56d2d16998b`.
Hash commands (exit 0): `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show ceecb1b1f9093471eb0b17d2c9190e78bceb0b78:SCORECARD.md | sha256sum && git -C /home/vgpnk/Projects/shokunin/kake-shokunin show ceecb1b1f9093471eb0b17d2c9190e78bceb0b78:.ufo/waves/round-39/verification/pre-summary.jsonl | sha256sum` → source hashes above; `timeout 30s sha256sum /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/criterion-o.md /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/check_control_inventory.py /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/corrected-sample/SCORECARD.md` → artifact hashes below.

## Touched surfaces and limits
Created only sandbox deliverables and this required report; no product file, QUALITY.md, SCORECARD.md, lane index, or lane Git state was changed. No counter, key, build, network request, or package installation. The mechanical check establishes hash/label/class completeness against the committed summary; it does not establish semantic correctness of a class assignment, tool behavior, or a round verdict. No unrun check is represented as passed.

## Artifact paths and SHA-256
- `/fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/criterion-o.md` — `cf54466958cb8ade07cf98c8eb3655a9f8867476e69d5c218a2bc634b4c4b798`
- `/fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/check_control_inventory.py` — `26f0911bf7866fc678d4180076ff1df2da3aa78c94f52f7293a9f08a1fa0fb30`
- `/fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/corrected-sample/SCORECARD.md` — `3a86c1c2b0cb14f4f801119ddfbfb30dc3f0395728931cd4a26f8156a1cc0880`
