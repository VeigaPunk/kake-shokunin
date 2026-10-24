# Draft `QUALITY.md` criterion (o)

**Axis:** operability (with freshness of the byte-level evidence record).

- **(o) Pre-declaration scores have a byte-pinned, classed disposition.** If any tool was scored with the frozen counter before a claim declaration, the declaration's control-class text MUST identify every byte-bearing scored tool by its full 64-hex `toolSha256` and score label, assign each one explicit class and consequence treatment (including whether an oracle/reference is or is not a control), and identify the committed summary revision from which the inventory is derived. A scored absence with no tool bytes MUST be listed as an absent-tool baseline with no invented digest. The control rule MUST distinguish these pre-declaration dispositions from the general rule for tools first scored after declaration; an oracle cannot be implicitly swept into or out of the control consequence. A path, abbreviated digest, count, or class-only list is insufficient.

Grounding: round-39 C1's control-class sentence and drafting-defect note (`SCORECARD.md` at `ceecb1b1f9093471eb0b17d2c9190e78bceb0b78`, defect recorded at `915e9e87dd64cbcf8bad107e476520707efe4d27`); existing `QUALITY.md` (j) and (n) require declared control consequences to be applied and reject control lists that can contain builds/near-complete work. The defect is that the unqualified sentence includes a 24/24 pre-declaration oracle/reference under a literal reading, while its bytes and class are not enumerated in the control rule.

## Mechanical check

`check_control_inventory.py` reads `SCORECARD.md` and `verification/pre-summary.jsonl` with `git show <revision>:<path>` (never the worktree). It requires every non-null `toolSha256` row in the committed summary to appear exactly once in the inventory table with the same label, full digest, and expected class; it also requires the null-hash absent baseline and an explicit post-declaration scope sentence. Checker SHA-256: `26f0911bf7866fc678d4180076ff1df2da3aa78c94f52f7293a9f08a1fa0fb30`.

```sh
timeout 30s python3 -B /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/check_control_inventory.py \
  --repo /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision ceecb1b1f9093471eb0b17d2c9190e78bceb0b78
```

Red, on the committed round-39 declaration bytes (scorecard SHA-256 `0d4b1134eb1e36457fac37f061da17e28ec2e4b35cb2e267f0a12b87d252d378`; committed pre-summary SHA-256 `98e44fe613c85b660f3b12cd60ecc8973fe989114bcd1eb758fff56d2d16998b`):

```text
FAIL: 39 of 39 byte-bearing scores missing/wrong; 0 extra labels; 0 duplicate labels; duplicate_sha256=false; absent_baseline=missing; post-declaration_scope=missing
exit=1
```

Green, on the corrected inventory below, stored as Git tree object `d54b1c33ecd027a454822023d7219ef1249d387a` (not a commit; the check reads the corrected bytes from the immutable tree and the actual committed summary from `ceecb1b1`):

```sh
timeout 30s python3 -B /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/check_control_inventory.py \
  --repo /fast/scratch/hyaku/kake-r39a3w1/ScribeQualityCriterion/corrected-sample \
  --revision d54b1c33ecd027a454822023d7219ef1249d387a \
  --summary-repo /home/vgpnk/Projects/shokunin/kake-shokunin \
  --summary-revision ceecb1b1f9093471eb0b17d2c9190e78bceb0b78
```

```text
PASS: 39/39 byte-bearing pre-declaration scores SHA-pinned and classed; absent baseline explicit; post-declaration scope explicit
exit=0
```

## Corrected inventory excerpt used by the green run

Source: `.ufo/waves/round-39/verification/pre-summary.jsonl` committed at `ceecb1b1f9093471eb0b17d2c9190e78bceb0b78`. Each digest is the complete recorded `toolSha256`. The oracle/reference is explicitly outside the control consequence; all 34 single-sentence reference ablations are controls.

| Tool label | SHA-256 | Class / consequence |
|---|---|---|
| A_abs | 2169b49317c954b9b3f5201c3b3cd48e07390473ac2dfdcbc382dded361e2328 | single-sentence reference ablation; control |
| A_checkinv | 0d0563e7aa4a762631e08991f8001dec3f260e577fff34b9da29f28003719e02 | single-sentence reference ablation; control |
| A_count | 99f47db0321b391549bbd340cc80dfb0f65fbef176dab1936417ccb7a7a20fa8 | single-sentence reference ablation; control |
| A_dir | f3a28cda143f83a9d9f4846a7b9ec40a82e2de3e61e37da49a8b0d4fcf6e2ed0 | single-sentence reference ablation; control |
| A_doctype | 972fd1bf6867578145ad640db2c1eacb04314817237b4f54c1af8b502dcf03c0 | single-sentence reference ablation; control |
| A_dotdot | 0498d3c0a0618bde3641fcdeb2e735e28d4533dc7f1e9dd9ef5bc33988c5bc57 | single-sentence reference ablation; control |
| A_dupid | 7554db4cd7c8d0cffdd64de1f45d29e83fcfcf2185489fd3990ddc7856571660 | single-sentence reference ablation; control |
| A_enc | e24749d2901c43e662ff587da96281e4beb4d8f5c3517c0a82de1e81a6dedd26 | single-sentence reference ablation; control |
| A_entryunexp | bf6050c3e1bbe3dde91645dc12c51eee0d1b0e0aef4b912f3b44eeb2350aa207 | single-sentence reference ablation; control |
| A_fieldrep | 77cd1c42574e20d0d2705a0040639f616d1c25c875efc3da63da40c9648748d6 | single-sentence reference ablation; control |
| A_freqcase | 20101975a866f8c02c202c5a7b2960741abb7ea6c9c197bf8c6b54c1d6f137b0 | single-sentence reference ablation; control |
| A_freq | a25658ae81b6262eea185a7cbb3d794a22fad5f55dffef0e2295cca2ef219363 | single-sentence reference ablation; control |
| A_hostcase | 5ea453b57a7e8fdb271b718ca779088b167c95a9f37059f081766904ce2e9568 | single-sentence reference ablation; control |
| A_idxdir | 62357ac49a36f3ac62629a45de7d577dc9ae30e87e2ed6da124bd7ae524f449f | single-sentence reference ablation; control |
| A_lastmod | b00372b70b8a0332b274599e38f944c0e57b2a1b2046437902fc3e79399d4a32 | single-sentence reference ablation; control |
| A_lenbytes | 082ded3fcbabc8cab0a9931d878f75dc78926cf60ff7356302a17e5c2cef96bf | single-sentence reference ablation; control |
| A_len | bba96d107517f9835958d4654de51042c195eefd9e1f72509b6b3e520a80d601 | single-sentence reference ablation; control |
| A_lm_cal | 414c77629db743a02d4849f87884c616e5a71f9a6310d662b553fead36f0c938 | single-sentence reference ablation; control |
| A_lm_tz | 23b5b5676f00bd61d709b4b1bfac1419da2a6b98619c263bc669228629cf62e6 | single-sentence reference ablation; control |
| A_lm_ym | 811ddd1a89d5e7c2f1fb18256e19a3c01e9d69d1f8c1ce5170a2fe8c495c1af8 | single-sentence reference ablation; control |
| A_locrep | ba920404df311f68c2eee12086c38f465cf795f032f98519962386c50c85a981 | single-sentence reference ablation; control |
| A_noentries | cc56463156076c1eb9d8a5fc72c2e69dc73acde7a4c4702a42de48054c2bb658 | single-sentence reference ablation; control |
| A_pctdecode | 5371db24062fdf9c147633d2e9c8881bb36ed34c84e12515d5f5ddffb40fadc2 | single-sentence reference ablation; control |
| A_port | c07af298c83863d8e71da4ca40c5ea5a6301f2d9e4fe45cb5ed98f895c4fb825 | single-sentence reference ablation; control |
| A_priofloat | a6190718e658681f22fc1b134651b87563b91ef9bfccb375978e3a78a8ea6149 | single-sentence reference ablation; control |
| A_prio | 3fdc81b152ba0339a4c5f077e43d99653a4b5d26b3279d3e8f7c45e1dfbf2885 | single-sentence reference ablation; control |
| A_root | bf6af1a3c5643579c0bd63a6444b70c9d0574475154d752d6a6c49ae78e35184 | single-sentence reference ablation; control |
| A_rootunexp | 3a38f0183f17bc3b7748b1e8ddf384dfe33bde2df9feda855d49cad1692ffccf | single-sentence reference ablation; control |
| A_scope | 5bd64a4238646cb5474fa236d70e67cffca879bfe842936adda93d1ad9c6af61 | single-sentence reference ablation; control |
| A_size | 69502e19885712c36617f43976908bd1a350d9f3f1e935e0ea4c01f36731191b | single-sentence reference ablation; control |
| A_strip | 91974fd11b42bf233bac1aebec517ac1154f871324214935974ccd951b00518f | single-sentence reference ablation; control |
| A_usage | 34426e6bc2d6f4db5fa7dac60147e3ebf7ae5d4c79993df5800c4a304f2b752b | single-sentence reference ablation; control |
| A_verdict | ef3657c08c549112fec7f50d03d2a57be86bebc6fe8eeeaf3676752a691d4fbb | single-sentence reference ablation; control |
| A_version | 01be1154cf2eecbacee04819a66ee11a39ab067eaa77fb70f20c32fe9645b1e6 | single-sentence reference ablation; control |
| base | — | absent-tool baseline; no bytes to hash |
| const_clean | 4c48e68e28cce82188a3beac3c0f5b207964530cbf7c9756e6d4e6e394258fcd | constant-clean control |
| junk | a1ee21b179ac9b6021288160adadb9eee3dcf15a69b04fbc40c6d27528a6bcac | junk-output control |
| no_reader | f54e29451d2ece12f32b00265c54eb0a240c447e22e2bb7ffae36fb719b12a1e | manifest-only/no-reader control |
| shallow | 7edb06a265b657816b57fca5168bf2528ed7544f3392bb84cda872cbca3f052a | shallow-reader control |
| sitemap_audit_ref | 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8 | oracle/private reference; excluded from control consequence |
