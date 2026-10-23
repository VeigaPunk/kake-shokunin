MET

Axes: operability (judgment parity, CPU cost, structural-defect detection); freshness (unchanged). Two regex mutants met, but neither supplied a changed tool judgment; five behavior-changing mutants were killed. No genuine surviving control found.
Sandbox S = `/fast/scratch/hyaku/kake-r42w1/MutRegexStructure/`; all artifact/receipt names below are relative to S. Only this report was written in the lane.
Counter: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-42/c42_count.py`, sha256 `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`; seed 42042 throughout.
Reference tip41 sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`; base40 `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`.
Rewrite `rewrite.py:76-86`: disjoint run alternatives and possessive quantifiers; sha256 R = `42a48c3cb9e728c2d0eb86fe304cb60e7b56407196ee53bb5af8fbb5edb9c0aa`.
Pristine `pristine.json`: exit 0; equalRuns 8/8; ratios [T1,T2,T3,T4,T5] = [1.124,1.374,1.085,1.084,1.593]; met true; all timing candRepsEqual 5/5.
Independent `generated-pristine.json`: 84,028 generated values, zero `_parse_url` and zero regex differences. Generator includes empty authorities/ports, scheme variants, all ASCII insertions, Unicode, malformed percent escapes, repeated delimiters and long values.
Rewrite-only late-defect CPU seconds for 64 repetitions at 65,536/131,072/262,144/524,288/1,048,576 characters: .007108/.014241/.026949/.056971/.107010 (approximately linear; not a universal equivalence proof).

Exact executed detector commands (each completed; no detached child remains):
`timeout 900 prlimit --as=8000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-42/c42_count.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file /fast/scratch/hyaku/kake-r42w1/MutRegexStructure/rewrite.py --label MutRegexStructure-pristine --seed 42042 --out /fast/scratch/hyaku/kake-r42w1/MutRegexStructure/pristine.json` → 0.
`timeout 180 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/MutRegexStructure/compare_generated.py --tool /fast/scratch/hyaku/kake-r42w1/MutRegexStructure/rewrite.py --out /fast/scratch/hyaku/kake-r42w1/MutRegexStructure/generated-pristine.json --expect-equal --linear` → 0.
`timeout 900 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/MutRegexStructure/probe_batch.py --phase mutated --generated` → 0.
`timeout 900 prlimit --as=8000000000 -- python3 -B /fast/scratch/hyaku/kake-r42w1/MutRegexStructure/probe_batch.py --phase restored --generated` → 0.
The driver used at most TWO counters concurrently. Exact nested argv, exit codes, stdout/stderr and pre/post detector hashes are retained in `executions-mutated.json`, `executions-restored.json` and `execution-<phase>-<name>.json`. Initial async launches did not start (global background-job limit); synchronous execution succeeded.
Expected detector: inequality to tip41 must make met false even if all CPU ratios pass. The same counter/seed and independent generated detector were run on pristine, every mutant, and every exact-byte restoration; pristine results are shared because all seven probes began as identical R bytes.

Each row's archived tool is `mutant_<name>.py`; it differs from R at exactly the stated source line. Mutation receipts are `mutated-<name>.json`; ratios are ordered T1–T5.
| Name / one-member change | Mutant sha256 | Receipt: exit; equalRuns; ratios; met | Caught by / verdict |
|---|---|---|---|
| empty_host:81 host repetition `++` → `*+` | `4686d24626a68e0eded04a2621c4d3c2af8c0d6e6cbbbc3100fd70ad08200b9e` | 0; 8/8; [1.097,1.330,1.076,1.071,1.600]; true | none; survived, masked change |
| port_letters:82 `[0-9]` → `[0-9a]` | `0995bba947ca9b858b76b9619f98016609276d1ec78967b9800e42f1a99e7c9d` | 0; 8/8; [1.115,1.315,1.159,1.068,1.629]; true | none; survived, masked change |
| port_nonempty:82 port `*+` → `++` | `780aa7d91419c62ae5e495dfcc4f3d64fccfc4a464084486d70279355bd7bece` | 1; 7/8; [1.113,1.287,1.131,1.084,1.681]; false | A; killed |
| userinfo_optional_at:79 `@` → `@?+` | `858370ac4e404d88acfb0c1b07ba2045feecf8ebc86f866175f26e4919de8c3a` | 1; 0/8; [.074,.080,.086,.086,1.000]; false | A,B,C,T1–T5; killed |
| second_hash:85 add `#` to fragment class | `4007f8d6f58611d921029124066776fbca94321eda3149193ba9ffef5568eb03` | 1; 7/8; [1.110,1.353,1.135,1.056,1.626]; false | A; killed |
| fragment_question:85 remove `?` from fragment class | `d944e0abbab367a3c3d8f16d6670ae525a645efe8fcd93814e0176db71b23bc7` | 1; 2/8; [1.060,1.232,1.069,1.062,1.541]; false | A,C,T1,T2,T3,T5; killed |
| scheme_s:78 remove lowercase `s` via `[A-Za-rt-z0-9+.\-]` | `7d1e85686dee013126e598e933332dda4e57397a6c690f9074f6136d6fcd4c08` | 1; 0/8; [.073,.071,.076,.084,1.340]; false | A,B,C,T1–T5; killed |

Witnesses/independent outputs (`generated-mutated-<name>.json`, 84,028 values each):
empty_host and port_letters: no differing `_parse_url` witness found (0 differences each), despite 1,051 and 2,907 regex-match differences. `[INFERENCE]` added empty authorities are rejected by `_parse_url:100-101`; added alphabetic ports by `parts.port`/`ValueError` at :102-104. These are not controls under the assigned definition.
port_nonempty: `http://x:` → tip41 `(http,x,80,/)`, mutant None; 2,419 parse differences.
userinfo_optional_at: `http://x` → tip41 `(http,x,80,/)`, mutant None; 4,411 differences (possessive optional userinfo consumes the bare host).
second_hash: `http://x/a#b#c` → tip41 None, mutant `(http,x,80,/a)`; 575 differences.
fragment_question: `http://x/a#b?c` → tip41 `(http,x,80,/a)`, mutant None; 4,542 differences.
scheme_s: `https://x` → tip41 `(https,x,443,/)`, mutant None; 6,198 differences.

Restoration: every `probe_<name>.py` was restored from its mutant hash above to exactly R; `sha256sum` confirmed R for all seven and the retained mutant hashes above. Seven bounded `cmp -s rewrite.py probe_<name>.py` commands joined by `&&` exited 0. Archived `mutant_*.py` files intentionally retain replayable mutant bytes.
| Restored receipt | exit; equalRuns; ratios T1–T5; met |
|---|---|
| restored-empty_host.json | 0; 8/8; [1.082,1.313,1.059,1.038,1.557]; true |
| restored-port_letters.json | 0; 8/8; [1.081,1.339,1.099,1.080,1.585]; true |
| restored-port_nonempty.json | 0; 8/8; [1.100,1.301,1.076,1.059,1.557]; true |
| restored-userinfo_optional_at.json | 0; 8/8; [1.105,1.311,1.084,1.048,1.555]; true |
| restored-second_hash.json | 0; 8/8; [1.102,1.325,1.086,1.050,1.629]; true |
| restored-fragment_question.json | 0; 8/8; [1.124,1.334,1.167,1.033,1.553]; true |
| restored-scheme_s.json | 0; 8/8; [1.085,1.292,1.090,1.040,1.666]; true |
Every restored independent detector exited 0 with zero parse/regex differences across 84,028 values. All detector hashes before/after were unchanged within each phase.
Checked statements: **holds**—tested rewrite parity and timing bound; **holds**—all five observed judgment-changing mutants caught by equality run A; **holds**—exact restoration and successful repeated detectors; **wrong**—treating either masked survivor as proof of a counter hole; **overstated**—inferring every-value equivalence solely from these finite generated runs. No round-level judgment.
Python 3.14.8; no tool installs/updates, no network access, no sibling/shared-source modifications. All process trees completed and were waited/reaped.
