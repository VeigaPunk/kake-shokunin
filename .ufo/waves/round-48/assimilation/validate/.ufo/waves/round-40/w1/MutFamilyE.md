# MutFamilyE — E-only mutation family
**SURVIVORS FIRST: M07-urlset-only, M08-http-loc-only, M09-skip-leading-comment, M10-short-files-only, M11-trailing-newline.**
Axes: operability (judged), freshness (unchanged). Twelve one-line E-only mutants; five survived, seven killed, none inconclusive. No round verdict.
Paths: S=`/fast/scratch/hyaku/kake-r40w1/MutFamilyE`; R=`/home/vgpnk/Projects/shokunin/kake-shokunin`; mutant paths below are relative to S.
Reference (read-only) `/fast/scratch/hyaku/kake-r40/shared/ref_fix.py:189-190`; SHA256 `03a8fba4930ad7628a569e7aa30b3ece728fbb6eb3fa4ac7c9a78dfbeb07b22b`.
Frozen detector `R/.ufo/waves/round-40/c1_count.py`; SHA256 `6d73b8f498a29a5a86c9a7f1ce5d87cd135c40f1b634d869d14659cc10bee8d8`.
Exact counter command, substituting the declared S/R paths and ID from each row: `timeout 1200 prlimit --as=4000000000 -- python3 -B $R/.ufo/waves/round-40/c1_count.py --root $R --tool-file $S/probe.py --label MutFamilyE-$ID --seed 40040 --out $S/receipts/$ID.json`.
IDs `pristine`, each mutant basename, and `restored` were run; exact expanded mutant commands, exits and every per-mutation restoration hash are in `S/run-evidence.json`. Mutated bytes ran at `S/probe.py`; identical retained artifacts below match each receipt toolSha256.
Pristine and restored: exit 0, passed=30/30, byClass E=9/9 U=13/13 R=8/8, selftest={exit:0,summary:"PASS 150/150"}, met=true (`receipts/pristine.json`, `receipts/restored.json`).
Every mutant below also has U=13/13, R=8/8 and selftest={exit:0,summary:"PASS 150/150"}; each row states passed/E/met/exit and verdict. Expected detector: exit 1/not met for any genuine weakening.
| Tool path:line | Sole replacement line | SHA256 | passed; E; met; exit; verdict |
|---|---|---|---|
| `mutants/M07-urlset-only.py:189` | `if "\x00" in text and "urlset" in text.replace("\x00", ""):` | `8e5a91222a1a9d1451c020ac3323ffc445e4f143ac2dc8e701c1a5c56d80e25a` | 30/30; 9/9; true; 0; SURVIVED |
| `mutants/M08-http-loc-only.py:189` | `if "\x00" in text and "<loc>http://" in text.replace("\x00", ""):` | `e13325e1aa59e087b58f84e26d7313eca5e41aa46f8c0ee2b77d71e82fb159bd` | 30/30; 9/9; true; 0; SURVIVED |
| `mutants/M09-skip-leading-comment.py:189` | `if "\x00" in text and not text.replace("\x00", "").lstrip().startswith("<!--"):` | `db6b815b21de4f4b52b854d4042bb7373e186e592d45225b167f856623487f4c` | 30/30; 9/9; true; 0; SURVIVED |
| `mutants/M10-short-files-only.py:189` | `if "\x00" in text and len(text) < 1024:` | `b597f6bd227a28db85248116113436b5561692b89ea1d51f39f1837841b29ade` | 30/30; 9/9; true; 0; SURVIVED |
| `mutants/M11-trailing-newline.py:189` | `if "\x00" in text and text.endswith(("\n\x00", "\x00\n")):` | `271855d35af5d3d685b1315054d046a36b9cd1987e709f2054c3a2e27394df9a` | 30/30; 9/9; true; 0; SURVIVED |
| `mutants/M01-wrong-character.py:189` | `if "\x01" in text:` | `f7bcdb47e09924a92c077db247a9d01d7f195ef4ed3fefd60c613d5e5fc02bbd` | 25/30; 4/9; false; 1; KILLED |
| `mutants/M02-wrong-code.py:190` | `return (None, {("encoding_invalid", None)})   # U+0000 is not an XML Char` | `58e132fcca76ba3508f23788add1d8398e8419803816d1feda1042f318a92326` | 25/30; 4/9; false; 1; KILLED |
| `mutants/M03-first-character.py:189` | `if text[:1] == "\x00":` | `c46158020f815b0eb0e1e189d254de4e9aa85dcc5aa75d6c8d319ea52747f2c1` | 27/30; 6/9; false; 1; KILLED |
| `mutants/M04-second-character.py:189` | `if text[1:2] == "\x00":` | `4420c338c63fa47eeecb041a39be81c87e007ae68e0bc4bb00118d40f57706c7` | 28/30; 7/9; false; 1; KILLED |
| `mutants/M05-declaration-marker.py:189` | `if text.startswith("<\x00?\x00x\x00m\x00l\x00"):` | `7288432aef9c55aa0d63b09616e70f0a256c994dfa36fa8ce8695ff421ba82cd` | 27/30; 6/9; false; 1; KILLED |
| `mutants/M06-double-nul.py:189` | `if "\x00\x00" in text:` | `eeac132be4e8e0088da3b96977164ccbac833d8911c0e992e581d1089470847f` | 25/30; 4/9; false; 1; KILLED |
| `mutants/M12-bom-gated.py:189` | `if "\x00" in text and data.startswith(b"\xef\xbb\xbf"):` | `2dbf8a37e5735e812528009be780cee1d6334646d5ac665464e69357a6cc1cbd` | 25/30; 4/9; false; 1; KILLED |
## Actual outputs and blind spots
Killed M01/M06/M12: E1–E5 all returned exit 0 instead of 1. M02: E1–E5 returned `encoding_invalid` instead of `xml_malformed`. M03 failed E1/E3/E5; M04 failed E2/E4; M05 failed E2/E3/E4 (exit 0 instead of 1). Full reasons are in the receipts.
`R/.ufo/waves/round-40/c1_count.py:82-92` supplies only short HTTP-loc urlsets with final LF, no leading comment; no sitemapindex/HTTPS/long/no-final-LF E-positive case. Random names do not vary those shapes.
Fresh challenge command, with NAME and TOOL mappings below: `timeout 180 prlimit --as=4000000000 -- python3 -B $S/residual_probe.py --tool $TOOL --out $S/receipts/residual-$NAME.json`; expanded commands/exits: `S/residual-commands.json`.
Fresh detector SHA256 `20f7a12a935c427f9da971e9f491780643888b05dd8613decebe4887514c2a1d`; its five ASCII UTF-16LE/no-BOM cases are `S/residual_probe.py:18-22`. Expected every case: tool exit 1, findings=[{code:xml_malformed,entry:null}].
NAME=pristine, TOOL=S/pristine.py; NAME=restored, TOOL=S/probe.py: detector exit 0, 5/5, every tool response exactly `xml_malformed` with exit 1.
NAME=M07-urlset-only, TOOL=S/mutants/M07-urlset-only.py: detector exit 1, 4/5; `M07-sitemapindex` (366 bytes, residual_probe.py:18) actually returned tool exit 0, status=clean, findings=[]; counter nevertheless met=true.
NAME=M08-http-loc-only, TOOL=S/mutants/M08-http-loc-only.py: detector exit 1, 4/5; `M08-https` (314 bytes, residual_probe.py:19) actually returned tool exit 0, status=clean, findings=[]; counter nevertheless met=true.
NAME=M09-skip-leading-comment, TOOL=S/mutants/M09-skip-leading-comment.py: detector exit 1, 4/5; `M09-leading-comment` (306 bytes, residual_probe.py:20) actually returned tool exit 0, status=clean, findings=[]; counter nevertheless met=true.
NAME=M10-short-files-only, TOOL=S/mutants/M10-short-files-only.py: detector exit 1, 4/5; `M10-long-file` (1528 bytes, residual_probe.py:21) actually returned tool exit 0, status=clean, findings=[]; counter nevertheless met=true.
NAME=M11-trailing-newline, TOOL=S/mutants/M11-trailing-newline.py: detector exit 1, 4/5; `M11-no-final-newline` (310 bytes, residual_probe.py:22) actually returned tool exit 0, status=clean, findings=[]; counter nevertheless met=true.
## Restoration and attacked statements
Before each mutation: pristine SHA256 above. Every mutated SHA256 is recorded in its row and counter receipt. After each mutation, probe.py was restored in finally; all 12 actual sha256sum results equal the pristine SHA256 (`S/run-evidence.json`). Final sha256sum also matched shared ref_fix.py, pristine.py and probe.py. Mutant artifacts remain intentionally available for rescoring.
Same frozen seed/counter ran on pristine, all mutated bytes, and restored bytes; pristine/restored both met. Same fresh detector ran on pristine, each survivor artifact, and restored bytes; only the mutants failed. No baseline failure was called a kill.
**Wrong:** “nine E witnesses kill every weakening” — five genuine E-only weakenings meet the predicate but fail fresh in-class cases.
**Overstated:** treating the predicate as evidence of complete class-E repair — the five omitted sub-shapes above remain distinguishable by incorrect tools; the contract and frozen predicate were not changed.
**Holds on exercised inputs:** the reference repair handles all nine E witnesses correctly and rejects all five fresh probes with `xml_malformed`; the counter reports its stated 30/30 plus 150/150 predicate accurately for these artifacts.
No installs/updates, network requests, subagents, commits or integration. All spawned detectors returned; no services/process trees left running. Lane writes were limited to this report.
