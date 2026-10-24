# CtlValuesOnly — r39-controls-a3
Axes: operability; freshness (offline scope only, not measured).
Built a standalone stdlib values-only control and a 12-line NOTE; no lane implementation changed.
Shape: rules 21–32 on matching local names anywhere; manifest/output/verdict handling retained; index scope and urlset-only value applicability retained.
Deliberately omits encoding/DOCTYPE/root/entry-structure/repeat/size/count enforcement and extension-namespace exclusion.
Evidence: /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/control.py:74 parses bytes directly; :95 matches local names; :125 scans descendants without structural rejection.
Counterexamples exercised through skipped.json: t/empty.xml:1 is clean instead of no_entries; t/missing-loc.xml:1 is clean instead of loc_missing; t/repeats.xml:1 is clean instead of loc_repeated and field_repeated.
Further exercised splits: t/wrong-root.xml:1 is clean instead of root_invalid; t/declared-latin.xml:1 clean instead of encoding_invalid; t/doctype.xml:1 clean instead of doctype_present.
Strong opposite-direction counterexample: /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/extension.xml:1 gets loc_not_absolute at entry 1, whereas contract sentence 14 requires ignoring that extension loc and returning clean.
Impacted axis: operability (missed policy violations and false findings). These are deliberate control defects, not acceptable product tradeoffs.
Smallest safe correction to a counter that admits this shape: discriminate at least one demonstrated omitted-rule case and the extension-local-name false positive; preserve this control's omissions. Sealed coverage is unknown, not asserted deficient.
Self-test command (exit 0): timeout 90s /usr/bin/prlimit --as=4000000000 -- /usr/bin/python3 -B /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/selftest.py
Observed five manifest results: valid.json=0, values.json=1, input-invalid.json=2, check-errors.json=2, skipped.json=1; all exact expected JSON/check/finding sets matched.
Observed three invalid argument lists: [], [--manifest], [--manifest,/work/valid.json,extra]; each exit 64 with no output. No self-test failures.
Each invocation used timeout 10s, prlimit --as=4000000000 and bwrap --unshare-all --clearenv with read-only /usr, /work, /tool/tool.py and private /tmp; tests ran sequentially, with no network or persistent process.
Hash command (exit 0; cwd /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly): timeout 10s /usr/bin/sha256sum control.py NOTE.md t/selftest.py t/*.json t/*.xml
Tool check (exit 0): timeout 10s /usr/bin/python3 --version && timeout 10s /usr/bin/which bwrap prlimit timeout sha256sum
Tools: existing Python 3.14.8 and existing sandbox utilities; no installations or upgrades.
No sealed key, counter execution, reference implementation, claimed build or network was accessed. No round judgment or 24/24 claim.
## Deliverables — SHA256 and absolute path
ff518efed54a96246e87754add88c137b5b5159df1bfbd7fe340df226c72ddf3  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/control.py
9d4513143eacf7e0cb9359815decec27af7bd1d7a3b2b6ec4e5a9842b4ef70f1  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/NOTE.md
06671789282b6abcbc19fb0a3a3bd239834e26e0158ef53214f8693a49e977a5  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/selftest.py
f515c654cf368b8d12a9afb5245ca3fc5786c23ea9d148a1fff69010b666a9c5  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/check-errors.json
bf6e2824ab3586e26cc28948d6ee4bb517a1958223e68cfdcfd4fdf8366606d4  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/input-invalid.json
6ec467eea066125ec8d8bb684ea97308ac319ef3649504f8518ae7c7b3c03c6e  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/skipped.json
3c337dd9c00040c60e26eee5eb23a8e7059a989d048090594c716901f7638079  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/valid.json
b9ee8a86db807f14ddb176155ecb4bf6ecc62ebdf2850c8f4e32c7575a3f4964  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/values.json
8713fe8b14123b89868602365da4b85543351150a77563ba4ae32a9f5294a8bd  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/declared-latin.xml
cda6c8015a982fc43b8bc70532c15e6fae4abd547120a37a52b52fbb37d48c44  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/doctype.xml
27050978a33b93b67e6ba6dc72fbee931bb5e69dfa871637101588080d83e0f9  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/empty.xml
b7b16ba27687630afff6ac2c2595a9a1e51e7867de1475993aa0870a29053599  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/extension.xml
6e26fee6ca0a4759b22d156ce4202dba78bbeba9a8d9849720e631b9090fdf25  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/index.xml
9261934a0e880ecab6f96038c722d5407062dec14d50b371963f01c4928ef2dd  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/malformed.xml
a56df3145103b12eb53f7ceea376f818027e7cbb9122ab985e3bc01d7183c270  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/missing-loc.xml
47f9668400d2ac2a164f2cdaa064e256a5655f853f895032c80df7c5546a5baf  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/repeats.xml
a9c5472c7f67431628255a75c2030d8525a87ea7e905beb138a24493ba490a36  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/valid.xml
684eb24aa05e247f70c2c839f80a27b58f8a03000c38b6e44b4032aabcfc186e  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/values.xml
4a3c86d18bc182a2ea6597f26287c75eb67387c19f4e50018cd99141664cd643  /fast/scratch/hyaku/kake-r39a3w1/CtlValuesOnly/t/wrong-root.xml
