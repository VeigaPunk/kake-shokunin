MET

Three of six one-member mutants survived the counter and have observed behavioral witnesses. This is a counter-coverage finding, not a round verdict.
Axes: operability (equality/cost detector); freshness (reference/counter hashes held; not scored).
Paths: `R=/home/vgpnk/Projects/shokunin/kake-shokunin`; `S=/fast/scratch/hyaku/kake-r42w1/MutRegexNonAscii`; `C=$R/.ufo/waves/round-42/c42_count.py`.
Own rewrite: `$S/rewrite.py:73-97`, possessive disjoint character-class chunks/percent alternatives; delimiters cannot be consumed by their preceding chunk, removing backtracking without changing the language.
Rewrite SHA256: `94c8280551852ceec3cce9a66f88a52f65ddeb6b0f676bdfbd5e4fe5eef27fa6`.
Reference `$S/../../kake-r42/shared/tip41.py` is actually `/fast/scratch/hyaku/kake-r42/shared/tip41.py`: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`.
Counter SHA256: `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`; Python 3.14.8; no installs/updates.

Exact counter command, with file/label/receipt substitutions below: `timeout 900 prlimit --as=8000000000 -- python3 -B "$C" --root "$R" --tool-file "$S/$file" --label "MutRegexNonAscii-$label" --seed 42101 --out "$S/$receipt"`.
All exact argv, exits, stdout and stderr are retained in `$S/command-log.json` (including initial witness and final clean witness).

| label | file | receipt | exit | equalRuns | ratios T1,T2,T3,T4,T5 | met | caught by |
|---|---|---|---:|---|---|---|---|
| rewrite | rewrite.py | rewrite.json | 0 | 8/8 | 1.198,1.459,1.129,1.037,1.907 | true | none |
| start_a0 | m_start_a0.py | start_a0.json | 0 | 8/8 | 1.199,1.444,1.139,1.085,1.815 | true | none; survived |
| no_surrogates | m_no_surrogates.py | no_surrogates.json | 0 | 8/8 | 1.218,1.458,1.154,1.061,1.747 | true | none; survived |
| no_fffe_ffff | m_no_fffe_ffff.py | no_fffe_ffff.json | 0 | 8/8 | 1.196,1.429,1.115,1.089,1.793 | true | none; survived |
| no_astral | m_no_astral.py | no_astral.json | 1 | 7/8 | 1.173,1.396,1.121,1.100,1.688 | false | C; killed |
| include_7f | m_include_7f.py | include_7f.json | 1 | 7/8 | 1.161,1.373,1.162,1.050,1.796 | false | A; killed |
| no_a0 | m_no_a0.py | no_a0.json | 1 | 7/8 | 1.222,1.467,1.145,1.063,1.803 | false | C; killed |
| restored | m_start_a0.py | restored.json | 0 | 8/8 | 1.218,1.436,1.099,1.086,1.715 | true | none |
All timing repetitions: `candRepsEqual=5/5` on T1–T5 for every scored tool.

Preserved rerunnable mutant artifacts are `$S/control_<name>.py`; the scored `m_<name>.py` files were restored after probing. One member/one source line changes per mutant:
| name | artifact line and one-line change | mutant SHA256 |
|---|---|---|
| start_a0 | control_start_a0.py:75, `"\u0080-\u009f"` → `""` (range starts at U+00A0) | c4184c65098c76baac12bb7369c5d50c158f0a7c1e62def0aba59443b07e29a0 |
| no_surrogates | control_no_surrogates.py:78, `"\ud800-\udfff"` → `""` | cd99a158b918e40b517a40d6f4f7a10776afa29e9092b6d439a08cf0bed18d89 |
| no_fffe_ffff | control_no_fffe_ffff.py:80, `"\ufffe-\uffff"` → `""` | 020dc7ae1ead9157caa02c113b418a2126e6c60681d11ebe90a9d7fec002d019 |
| no_astral | control_no_astral.py:81, `"\U00010000-\U0010ffff"` → `""` | 5aa2064ebb59dfea45c04df795df99d72ca6ae3f35bc28584e89dbd7fbdccf3a |
| include_7f | control_include_7f.py:75, insert `"\u007f"` | cd5b2f064df07fe9fe3c393d9aba5f5748caf0841a0b8d8ecc67c0c8d5c220f0 |
| no_a0 | control_no_a0.py:76, `"\u00a0"` → `""` | 83580abd73ba3bb5eb00bc15fdb8e64eef735571efd00ff6ff176109e4d11f76 |

Own generated detector: `timeout 300 prlimit --as=8000000000 -- python3 -B "$S/check.py" --tool "$S/$file" --out "$S/$output" --full`.
Pristine `file=rewrite.py, output=rewrite-differential.json`: exit 0, 1,135,045 values, zero differences; includes every Python code point in a URL path, boundary code points across seven positions, random structure/percent edits and values through 200,000 characters.
For each name above, `file=m_<name>.py, output=<name>-differential.json`: exit 1; differences respectively 178,2068,12,1048732,6,135. After restoration, same file with `output=<name>-restored-differential.json`: exit 0, same 1,135,045 values, zero differences each.
Witness command: `timeout 150 prlimit --as=8000000000 -- python3 -B "$S/witness.py"` → exit 0. Its four CLI commands are `timeout 30 prlimit --as=8000000000 -- python3 -B <tip41-or-control-path> --manifest "$S/witness-manifest.json"`; final original exit 0, each surviving control exit 2 (`check_invalid` instead of clean), all exact outputs in `$S/witness.json`.
Survivor values: start_a0 `https://a/\u0080`; no_surrogates `https://a/\ud800`; no_fffe_ffff `https://a/\ufffe` (backslash forms denote actual code points; JSON manifest escapes them). Original `_parse_url` returns `('https','a',443,'/<codepoint>')`; each corresponding mutant returns `None`.

Finding — **overstated**: sampled equality establishes every URL judgment. `c42_count.py:69-81,275-288` does not exercise these three excluded ranges outside IP literals; three genuine controls meet the full predicate.
Checked statement — **holds**: this rewrite matches tip41 on the generated differential and counter; all six mutants differ on observed values; astral, DEL and NBSP mutants are caught on C/A/C respectively. No universal-equivalence proof is claimed from sampling.
Restoration — **holds**: every active `m_*.py` before mutation and after restoration has the rewrite SHA256 above; mutant hashes are recorded before restoration and preserved in `control_*.py`. Restoration command per file: `timeout 10 prlimit --as=8000000000 -- install -D "$S/rewrite.py" "$S/m_<name>.py"` → exit 0. `$S/restoration.json` records all hashes; pristine and restored counter exits are both 0.
Reference and counter final hashes equal their initial hashes. `$S/process-cleanup.json`: bounded `pgrep` exit 1, no live probe processes; every started detector completed. Sandbox artifacts approximately 317 KB, below 300 MB. Only sandbox and this report were written.
