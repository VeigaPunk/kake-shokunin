# MutUrlAuthority — r39-controls-a3
Axes: operability, contract-sentence isolation, witness discrimination, exact-byte restoration.
Built 12 full-copy, single-line mutants; every local witness killed its assigned mutant. No equivalent mutant shipped. These are witness results, NOT sealed-key scores; no round verdict.
Source: /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py; SHA256 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8 before and after probes.

## Commands actually run
- `timeout 10s sha256sum /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py` → exit 0.
- `timeout --signal=TERM --kill-after=2s 120s prlimit --as=4000000000 -- python3 -I -B /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/probe.py` → exit 0.
- `timeout 10s sha256sum /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/probe.py /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants.json /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/reference.py` → exit 0.
The harness used two concurrent workers, each running the SAME bounded command on pristine, mutated, then restored tool bytes: `/usr/bin/timeout --signal=TERM --kill-after=1s 10s /usr/bin/prlimit --as=4000000000 -- /usr/bin/python3 -I -B <sandbox>/runs/<Mxx>/tool.py --manifest <sandbox>/witnesses/<Mxx>/manifest.json`. Every expanded command, exit code, stdout JSON and stderr is recorded in mutants.json. All 36 stderr streams were empty.
Expected detector: exit code plus the complete contract JSON and empty stderr must match the pristine expectation. All 12 pristine and restored detector runs passed; all mutants produced the intended differing JSON. Reference policy exits 1 for M10/M12 are expected outcomes, not detector failures.

## Findings and delivered mutant hashes
Exit triplets below are pristine/mutated/restored; C=clean, O=loc_out_of_scope entry 1, A=loc_not_absolute entry 1, E=check_invalid. All rows: local verdict killed.
| Mutation point (absolute path:line) | Sentence / defect | Actual output transition; exits | SHA256 |
|---|---|---|---|
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M01.py:35 | 24 / HTTP missing port normalized to 443; explicit :80 differs | C→O→C; 0/1/0 | 1ea37018aebeb35ddd0b626e4bef5517d4446af0c52b8fe8b343a01e5ffe566e |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M02.py:35 | 24 / HTTPS missing port normalized to 80; explicit :443 differs | C→O→C; 0/1/0 | cc57a77971ce1d21637caf14b597662045ae2b506e9d1480a0fa458d21eebcb3 |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M03.py:215 | 4 / sitemapUrl empty port rejected | C→E→C; 0/2/0 | f867398ec86b38fe9c4941ff7aa11d71541028287b5a6a0bf3156ad2fbebb886 |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M04.py:170 | 22 / loc userinfo rejected | C→A→C; 0/1/0 | d2fd1f2f063c8482d83164172e763a71b1c0e07b30964d3fe78b5a019995b0f2 |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M05.py:170 | 22 / loc IPv6 literal rejected | C→A→C; 0/1/0 | 560fb760e645a1750e63d2feb70055fd01a2a8d849f5f65ec42eb2b34bdc810a |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M06.py:170 | 22 / loc upper-case scheme rejected | C→A→C; 0/1/0 | e44e6fbe0c749b4e8259c476ca9e1ced82a592c88cba76bc9fd4f79df03c562b |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M07.py:36 | 25 / empty loc path not read as slash | C→O→C; 0/1/0 | ad79d22bd1f2eca6b4078997f7dcbbb3c89477944541af29e7c1067d0aa9e6d9 |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M08.py:215 | 4 / sitemapUrl query rejected | C→E→C; 0/2/0 | a274fbe5171f154825874f7c4fea64e3f1cf1c5c82d2807ffc9446ca45741a16 |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M09.py:215 | 4 / sitemapUrl fragment rejected | C→E→C; 0/2/0 | 95fae2ad406c3df6bf9c4688d19c2803426d64657495dce977ad2c496f8c6497 |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M10.py:149 | 25 / sitemapUrl trailing slash removed before directory extraction | O→C→O; 1/0/1 | aa54ad12ffc5cd49d13d93449bfa972d8af0176842343a28695fd194f53f5a41 |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M11.py:175 | 27 / sitemapindex wrongly constrained by directory | C→O→C; 0/1/0 | 62357ac49a36f3ac62629a45de7d577dc9ae30e87e2ed6da124bd7ae524f449f |
| /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M12.py:175 | 26 / path prefix compared case-insensitively | O→C→O; 1/0/1 | 0d85fc9aa77c4db1dca4d710498f94690f2df0e7f299741256896bc480de49db |

## Evidence and restoration
- /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants.json — SHA256 3b95a883123486e672dc96b5b4349ac59d74bd3c99acc60e73f2ef6420614fc1; per-mutant sentence, one-line diff, minimal manifest+sitemap contents, absolute fixture paths and hashes, both actual outputs, restored output, commands and restoration hashes.
- /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/probe.py — SHA256 fb2a3086806b3933531be18a1d7956c0ab488de5c7883ba09eb87a7403ed14c9; exact exercised harness. Replay requires temporarily recopying the authorized shared reference to sandbox/reference.py, then deleting that copy again.
- Fixtures remain under /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/witnesses/M01/ through M12/; each has exactly one check and one sitemap entry; every fixture hash is in mutants.json.
- Each working tool was restored in finally to exact pristine bytes, SHA256 663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8, and rerun against the same witness before removal; mutated hashes are the table hashes.
- All working probe copies/runs directories were removed by the harness. The copied /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/reference.py was then deleted with the edit tool (reported deletion); only mutants retain intentionally changed reference copies.
- No sealed key/counter, network, sibling source, lane index or runtime dispatch used. No background processes remain. No tool installation/update performed.
