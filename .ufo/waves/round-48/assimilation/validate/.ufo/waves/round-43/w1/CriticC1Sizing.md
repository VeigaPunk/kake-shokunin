DEFECT: control-before-build ordering fails; frozen SCORECARD numbers do not describe the committed receipts.

Axis: operability. Freshness and round admission are not judged.
Scope: freeze b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee through dispatch revision 7c070797eb5b6661983995705b546a0b07a9ea41 and the inspected working files.
Below, F = .ufo/waves/round-43/verification/freeze/; E = /fast/scratch/hyaku/kake-r43/CriticC1Sizing/scoring-order.txt.
Authority: fleet .ufo/prompts/kake-round-43.md:350-367; lane corpus/QUALITY.md:703-713,955-965. These are scoped findings, not a round verdict.

## Checked statements
- HOLDS — ref41-base and build-1..3, their seeds, and counter v4 are committed together at b49cba9c; git ls-tree resolves every blob. This establishes durability, not control-before-build order.
- WRONG — the requested control-before-build receipt order: the final counter's nine scorings were backgrounded in one batch, with only a final wait, at 19:36:05Z. Builds finished before the baseline; F/exits.txt:3-9 records build-3/1/2 exit 0 before ref41-base exit 1. E:4-25 preserves the exact historical command/output (original KakeR43.jsonl:195-197).
- Corroboration: stat shows build-3/1/2 receipts created at 19:36:28.985/29.171/29.217Z, ref41-base at 19:36:35.937Z. All four were first committed together, not controls in an earlier commit. The target build itself committed at 12:05:47Z, hours earlier; QUALITY.md:703-713's stronger pre-build-commit requirement is also unmet.
- OVERSTATED — “a do-nothing control cannot reach the target” as a current-round sizing assertion (SCORECARD.md:3218-3219): the actual round-43 base is 61046fcf (:3183), whose sitemap tool blob is identical to target 020bc457 (both 21553d19f93a14facddfa95f07c8f852d64fa82e). The named red control instead uses older 1ef7a0e9, blob cc906686889c52268a3f478b97a6761f8e1bbdf3. Thus the recorded met×3 bytes are already held at this round's unchanged base. No new base scoring was run; this is an identity counterexample, not a new receipt.
- HOLDS, narrowly — the specifically assigned historical ref41-base control fails: F/ref41-base.json:3,14,188-193 gives met=false, equal 11/11, exact T1=4.206529680365296 and T5=7.047329019160006 >2.0; recorded scorer exit 1 (F/exits.txt:9). This does not prove universal impossibility for every do-nothing baseline.
- HOLDS — target receipts record met×3, equal 11/11, scorer exits 0; seeds 9325990526163, 265206435053987, 269853680553917. The historical launch omitted --seed for all three, and c43_count_v4.py:953 draws os.urandom(6).
- HOLDS — the sentence at SCORECARD.md:3199 equals concatenated PREDICATE at c43_count_v4.py:78-80 and all nine C1 receipts' predicate fields (:2). Exact JSON equality queries returned true 9/9. Code :1046-1062 additionally requires every timing repetition equal and five exact ratios <=2.0; it does not judge rounded ratios.
- HOLDS within inspected history — kill rules/control classes at SCORECARD.md:3230-3241 are unchanged from freeze through dispatch and current files; counter and receipts also have no diff. The freeze precedes the 19:51Z dispatch log. No post-seat rule change was found; pre-freeze L1 redesign is not evidence of such a change.
- WRONG provenance — SCORECARD.md:3217-3223 quotes superseded measurements. Committed baseline rounded ratios are 4.207/1.917/1.152/1.228/7.047, not 4.272/1.931/1.223/1.229/8.679. Committed build ranges T1..T5 are 1.004–1.009 / 1.201–1.250 / 1.318–1.334 / 1.211–1.266 / 1.105–1.215 (each receipt :181-193). E:27-31 traces the quoted older numbers to discarded pre-T2-fix receipts. Met/not-met outcomes survive this prose error.
- WRONG protocol detail — ref41-base was explicitly scored with --seed 43001 (E:5), despite c43_count_v4.py:21's “build and every control” unseeded protocol and SCORECARD.md:3212-3213. The fixed seed is disclosed, not urandom evidence.

## Smallest safe correction
Append an erratum with the committed numbers, historical-baseline qualification, actual concurrent order, and fixed-seed exception; preserve frozen bytes and receipts. Do not claim the missing pre-build ordering was repaired by a later rerun. Current-round no-op reachability needs explicit disposition against the declared sizing rule; excluding it after scores or silently substituting another baseline would change the claim. The valid counter-repair evidence can be described separately without asserting a new tool-cost gain. Canonical admission remains the judge's decision.

## SHA256 evidence
Counter .ufo/waves/round-43/c43_count_v4.py: 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab
Candidate scripts/sitemap_audit.py at target (also actual base blob): 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021
Historical ref41 tool (receipt :11,13): 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d; round40 timing reference (:12): 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e
| Receipt under F | SHA256 |
|---|---|
| ref41-base.json | 4544741de94223282604301f79b14a32091b35c5e38a5184e772f695ca2ba325 |
| build-1.json | 162235107ce8d2fab443886e8d0e62b176161608ff36d0816e2ebff417d7072d |
| build-2.json | ba264bb02e3b7fdc0c6263a058c436f9f90284243b3bc5cecff2362deb0e22a6 |
| build-3.json | ea929cdd99950ad8d762e782844beeeeeef8841560be5a464da4495bdf5747c6 |
| r42ctl-M8-port-five-digits.json | 9b0eddc94a3253316c8e3d1d904bc8dc9e2c740b6545c4f493c19af0eaaa5660 |
| r42ctl-v1_casefold.json | b3a55fa9b69f086e3cc7f8e56257553a20f60b18511103cdc18174b081318dd9 |
| r42ctl-v2_prefix32.json | 26b3f395ce9c84fa8b638027ebaf8ad958cc4411f296b5c45233dfd2dd3c2e3f |
| r42ctl-v4_hosttable.json | 2985be16b6202c634090020201c7a465a380db86c5cd2c61946ff97dffd56717 |
| r42ctl-junk_constant.json | a52a59b920274fefc21876824003bedfbf8dfaa210a7f865e9bb8c2b5b7525ed |
E SHA256: 185773f6eaf55932f360f267ca2d394d6713ae0c21f18b0646496a821a9dedcf.

## Exact audit commands and observed exits
Working directory: /home/vgpnk/Projects/shokunin/kake-shokunin. Each following command exited 0.
`timeout 45 prlimit --as=8000000000 -- sha256sum .ufo/waves/round-43/verification/freeze/*.json .ufo/waves/round-43/c43_count_v4.py SCORECARD.md scripts/sitemap_audit.py`
`timeout 45 prlimit --as=8000000000 -- git ls-tree b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee SCORECARD.md .ufo/waves/round-43/c43_count_v4.py .ufo/waves/round-43/verification/freeze/`
`timeout 45 prlimit --as=8000000000 -- git diff --exit-code b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee 7c070797eb5b6661983995705b546a0b07a9ea41 -- SCORECARD.md .ufo/waves/round-43/c43_count_v4.py .ufo/waves/round-43/verification/freeze/`
`timeout 45 prlimit --as=8000000000 -- git diff b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee -- SCORECARD.md .ufo/waves/round-43/c43_count_v4.py .ufo/waves/round-43/verification/freeze/` (empty)
`timeout 45 prlimit --as=8000000000 -- git rev-parse 61046fcffa23898cd93b7a5a0af4906dac9926c9:scripts/sitemap_audit.py 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py`
`timeout 45 prlimit --as=8000000000 -- git merge-base --is-ancestor 020bc4574729ed674299f6cab02faac1582d9464 61046fcffa23898cd93b7a5a0af4906dac9926c9`
`timeout 45 prlimit --as=8000000000 -- stat --printf='%n birth=%w modify=%y\n' .ufo/waves/round-43/c43_count_v4.py .ufo/waves/round-43/verification/freeze/ref41-base.json .ufo/waves/round-43/verification/freeze/build-1.json .ufo/waves/round-43/verification/freeze/build-2.json .ufo/waves/round-43/verification/freeze/build-3.json`
`timeout 45 prlimit --as=8000000000 -- git log -1 --format=fuller 020bc4574729ed674299f6cab02faac1582d9464`
`timeout 45 prlimit --as=8000000000 -- sha256sum /fast/scratch/hyaku/kake-r43/CriticC1Sizing/scoring-order.txt`
Historical scoring commands and their exits are copied in E; none was rerun. No tool/counter tests or judge runtime invoked, no installs, and no process left running.
