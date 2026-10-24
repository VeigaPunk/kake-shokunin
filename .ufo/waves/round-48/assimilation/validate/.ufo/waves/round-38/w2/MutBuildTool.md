# MutBuildTool — round-38 wave-2 mutation probe
Axes: **operability attacked**; freshness unchanged/unmeasured (offline; no site requests).
Scope: built (h)/(i)/(k) at `3ed8e15c2707ac4cec88f48fc9be48b35be4f2b0`; expected detector: selftest and/or v3 rejects each semantic defect. No admission judgment or contract change.
Paths below abbreviate `S=/fast/scratch/hyaku/kake-r38w2/MutBuildTool`, `C=/fast/scratch/hyaku/kake-r38w2/MutBuildTool/clone`, `P=/fast/scratch/hyaku/kake-r38w2/MutBuildTool/probe.py`; cwd `C`; GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; TMPDIR=`S/tmp`.
Executed probe: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=$S/tmp timeout --kill-after=5s 850s prlimit --as=4000000000 -- python3 -B $S/run_probe.py` → exit **0** (344.58 s).
Exact detector argv per state: `prlimit --as=4000000000 -- python3 -B scripts/robots_audit_selftest.py --tool $P`; `prlimit --as=4000000000 -- python3 -B .ufo/waves/round-38/sealed_count_v3.py --root $C --tool-file $P --key-revision 99357694` (180 s/process deadline; exits below).
Executed witnesses: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=$S/tmp timeout --kill-after=5s 120s prlimit --as=4000000000 -- python3 -B $S/witness_probe.py` → exit **0**; each direct `python3 -B $P --manifest <saved manifest>` has the same prlimit and a 10 s deadline.
Pristine: **194/194, exit 0; v3 20/20, exit 0**. The identical two detectors also passed after **each of 36 exact restorations**; zero inconclusive probes.
Observed: selftest killed **27/36**, v3 killed **27/36**; union killed **30/36**. **Six survived both**, all demonstrated non-equivalent by saved contract witnesses.
Each row is `/fast/scratch/hyaku/kake-r38w2/MutBuildTool/mutants/<ID>.py`, staged byte-for-byte at P only while tested. Cells are `passed/total; exit`; SHA-256 identifies the mutated bytes. `@L` is the original tool line.
| Mutant / single behavior change | Selftest | v3 | Both survive | SHA-256 |
|---|---:|---:|:---:|---|
| H01@L465 — Drop non-JSON constant rejection | 189/194; 1 | 18/20; 1 | no | `b8f1b782df515e2fee5ba8533e7ea7cb42497aab1145caa38d2c4a8825d7d638` |
| H02@L465 — Use default bounded integer conversion | 189/194; 1 | 18/20; 1 | no | `1e42b023c31c05c3eb9088f81d990db93f58b83d0ab0c68f59a7fad77b151caa` |
| H03@L426 — Lose the sign of short JSON integers | 194/194; 0 | 20/20; 0 | yes | `8f8add5a3125204c9210789b0bb6c6efc2da060b7ccd8fc78836f667e0cf2e70` |
| H04@L426 — Truncate short integer values to three decimal digits | 194/194; 0 | 20/20; 0 | yes | `f50ab442dee40fed021f621be2d98a744b0196b04bce8297f381d9ed3f61f4b9` |
| H05@L431 — Accept NaN as an ignored constant | 192/194; 1 | 19/20; 1 | no | `5b9f99a6a7f7c4705ba816cc11de9546a3a4c25188d593acc2235c04353fced0` |
| H06@L431 — Accept Infinity as an ignored constant | 192/194; 1 | 19/20; 1 | no | `67ab71abf16aaf58b680301574634ede172121476dc3707afddf2851ce5fb48d` |
| H07@L431 — Accept -Infinity as an ignored constant | 193/194; 1 | 19/20; 1 | no | `e015b696cb2742c80bfdc13fc5f52fe0013617157cbd709e3794375133bb2cff` |
| H08@L154 — Reject ordinary three-digit status integers as long | 75/194; 1 | 1/20; 1 | no | `d76f44db4c2993c422507ef24d486dea37faae60fcaa4a60f66306bb2d07f6c8` |
| H09@L154 — Convert integer tokens through 5000 digits | 192/194; 1 | 18/20; 1 | no | `66d045a5b70162a21f2b8d66548d0f586e20afac2549b150e53bbd617ee21ccc` |
| H10@L425 — Reject long JSON integers at manifest scope | 189/194; 1 | 18/20; 1 | no | `8f304b7b2e4d8e33ca581a8329ce9ad57190c8250d0e164651862489cbc5badd` |
| I01@L510 — Check only the first URL character | 169/194; 1 | 16/20; 1 | no | `79591f90057acd95230fa1a894633e1b1e790f08b19989b60517472ba0fa1131` |
| I02@L510 — Strip forbidden URL whitespace before validation | 191/194; 1 | 16/20; 1 | no | `f2582cb0be5fe61b7933f52bde5342e953185e8cd6a44310ceb83f8092314204` |
| I03@L510 — Validate path characters only | 185/194; 1 | 16/20; 1 | no | `660334342c4c84c3885a064ae0f6873139b46ac8a9568cd7a5b7baca43fa9e1c` |
| I04@L510 — Ignore fragment characters | 192/194; 1 | 18/20; 1 | no | `bc8198a396047dc0cb777ba5306e2752f99adb7605149420d9e3beb4433ca0e3` |
| I05@L149 — Permit ASCII space | 184/194; 1 | 18/20; 1 | no | `1fba2410360b140e1eed5ea909e0a62ad49977d70096055a924a1872970bf116` |
| I06@L149 — Permit ASCII NUL | 193/194; 1 | 19/20; 1 | no | `5b1546c7779ba895fe931f59835b1c1bc0996b6f09eaeb73d207eed7584b62c5` |
| I07@L149 — Permit ASCII unit separator | 193/194; 1 | 19/20; 1 | no | `92d9695c571d7b169212b84f4f321842922ce2387705cde3c291f50ffcd808e3` |
| I08@L149 — Permit ASCII STX | 194/194; 0 | 19/20; 1 | no | `e30978882d4f58ad569c26cf86f6e5791c5a03e4e7fed9b60839e597a70185e4` |
| I09@L149 — Permit ASCII DEL | 193/194; 1 | 20/20; 0 | no | `5d0bd3ee07ed6832576050af84b2b55269b47d3465bc8fcf0bf685f1e9d959e3` |
| I10@L149 — Permit a backslash | 193/194; 1 | 19/20; 1 | no | `7428dc3d1351529b4bdd8871ae8b889cbb399da3e435ffeed168632d0cbea0da` |
| I11@L149 — Reject the allowed percent character | 176/194; 1 | 14/20; 1 | no | `1fc1c91eeb9eac3f92d0dfab535c56ba618dd90389f0864523727443525ea663` |
| I12@L149 — Reject the allowed tilde character | 193/194; 1 | 20/20; 0 | no | `90cf9e7fd6422d08979eb7c4a81da9be027172fc9940e5785a75b7ca1601eaf6` |
| I13@L149 — Reject the allowed underscore character | 194/194; 0 | 20/20; 0 | yes | `78616821f2dc81939e2a662079b4c98d5d89d7e9c912dc8c2fe51d5a107110a3` |
| I14@L149 — Reject the allowed plus character | 193/194; 1 | 20/20; 0 | no | `adadee92b6d249153c7a58a4a29c83c341639f561c5a5dd2c36eb0c90004aa4f` |
| I15@L510 — Reject every non-ASCII URL | 190/194; 1 | 19/20; 1 | no | `60e3fe99c5aed1b609b93604016e1246f0560fd9ad938932f149cf29ebc76803` |
| I16@L510 — Reject non-printable Unicode URL characters | 194/194; 0 | 20/20; 0 | yes | `a51f80688c92eda0abac41f821d94de2b3a5bb1ea83868aed96273b886b3f0fb` |
| K01@L605 — Compare the raw unnormalized path | 186/194; 1 | 16/20; 1 | no | `344c2dcdfad7edf7aebad5927371ebeae6304aae10961a5dcc236d514b346430` |
| K02@L606 — Case-fold the implicit-allow path | 192/194; 1 | 18/20; 1 | no | `a2942db1aaf28d473b83169fa8288a87d8486feb0f1e1b68d3545c0014ebef9d` |
| K03@L606 — Ignore a non-empty query for implicit allow | 193/194; 1 | 18/20; 1 | no | `5b972fd00b8751a38b3638e8f493d04e587982453b0e941017b2bcc6b7d8d257` |
| K04@L606 — Implicitly allow a robots.txt path prefix | 193/194; 1 | 18/20; 1 | no | `22d83c66ddf540ccdb1ec692a7ddb3aa6b06ef2333f878ced19ad93604d222a4` |
| K05@L606 — Ignore trailing slashes for implicit allow | 194/194; 0 | 19/20; 1 | no | `782827868803cc9a67279682e785a40ddc493818249c739bb602eefcec5ba45b` |
| K06@L606 — Turn implicit allow into an explicit denial | 184/194; 1 | 16/20; 1 | no | `6fea618964f492f3aada130722158881724c0b0790fa6f8f04e097f0cc97ce79` |
| K07@L606 — Require an empty selected rule list for implicit allow | 184/194; 1 | 16/20; 1 | no | `29f52cc87f9f1880879f2c7ec45a373133d58b69b1afe4b39746ba905d3795e1` |
| K08@L606 — Limit implicit allow to HTTPS URLs | 194/194; 0 | 20/20; 0 | yes | `d3fcdc23413ca85b6dbf7f8d1dbb24e244894a8dc2f8cdb8be8efa66d58a89c7` |
| K09@L606 — Implicitly allow robots.txt below another directory | 194/194; 0 | 20/20; 0 | yes | `b30ef0a1f7f998773249c0c21921dbcb41841be39669489fc678c94a5b185f25` |
| K10@L606 — Collapse dot segments before implicit-allow comparison | 194/194; 0 | 19/20; 1 | no | `d55b49931bf308e626287ba2b6b7468a36a9465c71a6c9a4854243f50d647875` |
Witness outputs (pristine → mutant → restored), full argv/stdout/stderr/exits in witnesses.json:
H03/H04: statuses **-200 / 1200**; `check_invalid`, evaluated=1, exit **2 → clean, evaluated=2, exit 0 → original, exit 2**.
I13/I16: valid **underscore / U+00A0** URLs; `clean`, evaluated=1, exit **0 → check_invalid, evaluated=0, exit 2 → clean, exit 0**.
K08/K09: **HTTP /robots%2Etxt / HTTPS /nested/robots.txt**; `exposed / blocked`, evaluated=1, exit **1 → clean, exit 0 → original, exit 1**.
Additional differential: I08/K05/K10 survive selftest but v3 kills them; I09/I12/I14 survive v3 but selftest kills them. Neither instrument subsumes the other.
**Verdict — holds:** SCORECARD.md:2270 numeric build result (20/20), and :2276 selftest result (194/194), reproduced with these exact tool bytes.
**Verdict — overstated if read as comprehensive protection:** the two instruments leave six demonstrated (h)/(i)/(k) defects undetected. This is a coverage finding, not evidence the pristine tool has those defects; the declared 42-reference-mutant result was not rejudged.
**Verdict — URL coverage incomplete:** I09 permits DEL yet v3 stays 20/20; selftest catches `i13-delete-in-path` (expected tool exit 2, observed 0). Key DEL checks are leading DEL before the scheme (cases_v3.json:1062), or DEL with a backtick (:1396), so other validation masks the missing DEL rule. Do not infer full isolation from SCORECARD.md:2229–2230.
Restoration: pristine/P/clone tool SHA-256 **f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace** before/after; every row records before/mutated/restored hashes and restored detector outputs. Mutant artifacts are intentionally retained; lane source never mutated.
Evidence: `/fast/scratch/hyaku/kake-r38w2/MutBuildTool/evidence/results.json:1` SHA-256 `2a9d56112848aeea1e60eb03d037d3b7f458c1e484810e13ab0c84fe41e0e7e1` (all 146 instrument runs, actual outputs, exits, restoration).
Mutations: `/fast/scratch/hyaku/kake-r38w2/MutBuildTool/mutations.json:1` SHA-256 `99aa3cf4a9a94e65190ac1d38c851b667c635834ad4af6892e0e2c03543df1a8` (exact old/new point, source line, path, hash).
Witnesses: `/fast/scratch/hyaku/kake-r38w2/MutBuildTool/evidence/witnesses.json:1` SHA-256 `e4a03bd88fbcc86c814bb39b131280dbd311b6f31c2d864d9e1ebd69336f1d23` (six manifests and 18 actual runs).
Runner: `/fast/scratch/hyaku/kake-r38w2/MutBuildTool/run_probe.py:1` SHA-256 `98a3f7a460046c1cdce8221fbba99c87fab94088335488b299eb9c7e14158de4`; witness runner `/fast/scratch/hyaku/kake-r38w2/MutBuildTool/witness_probe.py:1` SHA-256 `21a78ff2805c54d72413f57be7f78106b9621f7019e6589bd2ae937d809d50a0`.
Artifact index: `/fast/scratch/hyaku/kake-r38w2/MutBuildTool/SHA256SUMS:1` SHA-256 `6edf2a0849621d66ce5351d83f14029145933086e58a064b77fd758b7573a348` (absolute paths and hashes for all mutants, receipts, witnesses, runners, pristine/staged bytes).
Instrument SHA-256: selftest `bab98f444bdb6b10a375652977beb083c1d28adbed9b60b1857f36f0bec508c1`; v3 `28b120a5a38061825094c17f0e978d7e6a5ec3fb131094e2cdfd59360f38f9e4`; key `749ef6a65de67f09abffad33fa6d7efcb1e7f1515b1d2fa51a93ff9977b63aa6`.
Bounds: two detector parents at once; bounded subprocess groups terminated/reaped; no installs, network, sibling writes, lane index/jj changes. Initial async launch was rejected by the global background-job cap; the synchronous launch above completed.
