# CtlHandTokenizer — r39-controls-a3
Axes: operability; freshness unchanged (offline, no web publishing/fetch).
Built one Python 3 control using str.split/partition on `<`/`>`, a hand-maintained lexical tag stack, and literal-prefix comparisons; no direct re/xml/html imports.
Boundary: only the canonical contract was read; no sealed key, counter, reference implementation, claimed build, or round judge was read/run. No lane writes except this report.
Tools already present: Python 3.14.8; bubblewrap 0.13.1; prlimit util-linux 2.42.4. Installs/updates: none.
## Commands and observed results
`timeout 10s /usr/bin/python3 --version && timeout 10s /usr/bin/bwrap --version && timeout 10s /usr/bin/prlimit --version` → exit 0; versions above.
`timeout 10s /usr/bin/readlink -f /lib /lib64 /lib64/ld-linux-x86-64.so.2` → exit 0; /usr/lib, /usr/lib, /usr/lib/ld-linux-x86-64.so.2.
`timeout 60s /usr/bin/prlimit --as=4000000000 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/run_selftests.py` → initial exit 1, final exit 0.
Initial local harness omitted Arch's loader aliases: every child exited 1 before executing Python (`execvp ... No such file or directory`). Added only /lib and /lib64 symlinks to usr/lib in that harness; no counter change.
Final harness uses two concurrent workers, a 15-second subprocess timeout, no environment/network, read-only /usr, /work and /tool/tool.py, private /tmp, and inherited 4,000,000,000-byte AS limit.
Exact child command (S=/fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer; N takes each filename listed next):
`/usr/bin/prlimit --as=4000000000 /usr/bin/bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib /lib64 --dir /tool --ro-bind "$S/control.py" /tool/tool.py --ro-bind "$S/t" /work --tmpfs /tmp --chdir /work /usr/bin/python3 -B /tool/tool.py --manifest "/work/$N"`
Final child exits: 01-clean.json=0; 02-findings.json=1; 03-input-invalid.json=2; 04-errors.json=2; 05-namespace-gap.json=1. All stderr empty; 5/5 matched locally specified outputs, including exact finding sets and error precedence.
IMPORTANT: 05 asserts the deliberately incomplete control's behavior, NOT contract compliance. It exhibits three known namespace errors below; 5/5 is not a sealed score.
Hash commands: `timeout 10s /usr/bin/sha256sum control.py NOTE.md run_selftests.py t/*.json t/*.xml` → exit 0 (before harness correction); `timeout 10s /usr/bin/sha256sum control.py NOTE.md run_selftests.py t/expected.json t/01-clean.json t/02-findings.json t/03-input-invalid.json t/04-errors.json t/05-namespace-gap.json t/alias.xml t/rebound.xml t/undeclared.xml` → exit 0 (final). CWD for both: S above.
## Deliverables — final SHA-256 and absolute paths
edf2ed363f2afd46ff4184eee2b466910dc1e98b938422f0ec3e75b206945322  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/control.py
4cadee4c1d51eb2a63c68ccee79ba6964044f4243b27041e29dcefce7bbff2f2  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/NOTE.md
9f3067029a1c66ff15aab223f6e5ca3a7dd90b1e4cd40ae781275082574a99ce  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/run_selftests.py
153396717393b1ed2a0e0d14bcd1e2e053826f52c909913e0c34c972ed379a5c  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/01-clean.json
2311a9c1d36e0d1da6fa0fcba157c7f2f02213365aa88bf3ecad7727a23bb2d7  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/02-findings.json
109bf298adbcf89b5deafb2952a52e0f56c6594be80bd1577075d98d2f0b78bd  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/03-input-invalid.json
dd65fe283838105edcb961c85ef846459bd1153e4b145b0fd28b619e4c4758c0  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/04-errors.json
f0c906d06751cbdf33d39e1ad8ee207767300e1232c788b5a7366f89e8d0a2c8  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/05-namespace-gap.json
66fc244fcb5a4204d0c5533b511234cebea26549cc995d2be6d37439376df6fe  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/expected.json
8fdbdc6bccb691f2bcca94e7c98651c888bdd9a6264b094f91daad7f9de6fdbb  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/alias.xml
bab35e8e2ec283cf859125431dae22dd22aa67016a2133c0d370a48baeebb463  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/clean.xml
175997916aa3fb8fc9fa8ac07444d25fe2aca62644f6f57e0e47e4d5791ccf14  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/doctype.xml
5877d8cb63d496376f443fdc0a31998a72aa09e455b2b701b37f49be956240bd  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/empty.xml
c315d6a91a0298f596b06b4661ca555f965302a589c7f5953404d889edab5231  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/encoding.xml
22760b645286e4719601df730ef1b8177910d547a3d7547e4822148e4d192f67  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/findings.xml
44b109e4ac0cfbbb44f762970a0a3857381ae52048dc80eba5488f5e4699a5c8  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/index-findings.xml
62078853b9ca64a458046003f912b9c135105136d1033dd64e70ac4a51a31ae1  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/index.xml
2290175b80a51e018312a36ca61939b723e93595d9b25353ea62badc673cf740  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/malformed.xml
bddd1d27a8f4f7147a10f0202b47bc91c3e29429152dc895832edebb2503330b  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/rebound.xml
17f31a1da247dd27c9065659c6891a595256b50d9dd7a8880355a703e57facc3  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/root-invalid.xml
9d49814ca87d4c33cd1c1bc7a950e908bf2d2124c067795dfaf1bdc61c514bf3  /fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/undeclared.xml
## Counterexamples, evidence, and smallest safe correction
/fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/rebound.xml:1 — observed clean although its only url changes the default namespace to urn:foreign; contract sentence 11–14 requires no_entries (foreign subtree ignored). Strongest false-clean counterexample.
/fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/alias.xml:1 — observed no_entries although q:url/q:loc and s:urlset bind the same sitemap URI; contract sentences 10–14 require clean.
/fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/t/undeclared.xml:1 — observed clean despite unbound u:ignored; contract sentence 8 requires xml_malformed.
/fast/scratch/hyaku/kake-r39a3w1/CtlHandTokenizer/control.py:371,379,396 — root-only literal binding check and literal-prefix equality cause these intentional omissions; :187 also skips full DOCTYPE parsing.
Impacted axis: operability (false-clean and false-finding results). Freshness does not move. No sealed discrimination or saturation conclusion is supported by these local results.
Smallest safe correction: retain this control unchanged for L1 scoring; use the three tiny namespace counterexamples as discrimination probes. Production correctness requires scoped namespace resolution and namespace well-formedness checks, outside this control's deliberate omissions. Only L1 can assess whether the frozen key already distinguishes them; no counter/key changes or round judgment here.
All runs are finished; no persistent processes or services were started.
